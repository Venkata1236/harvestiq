"""
/api/detect — image upload → ML → RAG → Groq agents → full response
"""

import time
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.ml.model import model_manager
from app.rag.retriever import get_disease_info
from app.agents.disease_analyst import run_disease_analysis
from app.agents.treatment_advisor import run_treatment_advice
from app.core.config import settings
from app.database.connection import get_db
from app.database.models import Detection

router = APIRouter()


@router.post("/detect")
async def detect_disease(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()

    # ── Validate file ──────────────────────────────────────────────────────
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type: {file.content_type}. Use JPEG or PNG."
        )

    # ── Read image bytes ───────────────────────────────────────────────────
    try:
        image_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read image: {str(e)}")

    # ── ML Prediction ──────────────────────────────────────────────────────
    try:
        result = model_manager.predict(image_bytes)
        logger.info(f"ML: {result['disease']} ({round(result['confidence']*100, 1)}%)")
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"ML prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")

    # ── Low confidence → return early ──────────────────────────────────────
    if not result["proceed_to_advisory"]:
        return JSONResponse(content={
            "status": "low_confidence",
            "message": f"Confidence too low ({round(result['confidence']*100, 1)}%). Please upload a clearer image.",
            "confidence": round(result["confidence"] * 100, 1),
            "top_predictions": result["top_3_predictions"],
        })

    class_name = result["disease"]

    # ── RAG Retrieval ──────────────────────────────────────────────────────
    disease_info = get_disease_info(class_name)

    # ── AI Agents in parallel ──────────────────────────────────────────────
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            analyst_future = executor.submit(run_disease_analysis, class_name, result["confidence"])
            advisor_future = executor.submit(run_treatment_advice, class_name, result["confidence"])
            diagnosis_report = analyst_future.result(timeout=30)
            treatment_plan   = advisor_future.result(timeout=30)
    except Exception as e:
        logger.error(f"AI agents error: {e}")
        diagnosis_report = "AI analysis temporarily unavailable."
        treatment_plan   = "Please consult your local agricultural extension office."

    # ── Save to DB ─────────────────────────────────────────────────────────
    try:
        detection = Detection(
            disease=class_name,
            display_name=result["display_name"],
            crop_type=result["crop_type"],
            confidence=result["confidence"],
            severity=result["severity"],
            proceeded_to_advisory=True,
            image_filename=file.filename,
        )
        db.add(detection)
        await db.flush()
        detection_id = detection.id
        logger.info(f"Detection saved to DB: id={detection_id}")
    except Exception as e:
        logger.error(f"DB save failed: {e}")
        detection_id = None

    elapsed = round(time.time() - start_time, 2)
    logger.success(f"Detect complete: {class_name} in {elapsed}s")

    return JSONResponse(content={
        "status": "success",
        "detection_id":      detection_id,
        "processing_time_seconds": elapsed,

        # ML output
        "class_name":        class_name,
        "display_name":      result["display_name"],
        "crop_type":         result["crop_type"],
        "confidence":        round(result["confidence"] * 100, 1),
        "severity":          result["severity"],
        "top_predictions":   result["top_3_predictions"],

        # RAG output
        "disease_name":      disease_info["disease_name"],
        "crop":              disease_info["crop"],
        "pathogen":          disease_info["pathogen"],
        "is_healthy":        disease_info["is_healthy"],
        "symptoms":          disease_info["symptoms"],
        "causes":            disease_info["causes"],
        "treatment_summary": disease_info["treatment"],
        "prevention_summary":disease_info["prevention"],

        # Groq AI output
        "diagnosis_report":  diagnosis_report,
        "treatment_plan":    treatment_plan,
    })


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "model_loaded": model_manager.is_loaded,
    }
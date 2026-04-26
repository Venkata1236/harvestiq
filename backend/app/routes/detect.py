from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.connection import get_db
from app.database.models import Detection
from app.ml.gradcam import generate_gradcam_base64
from app.ml.model import model_manager
from app.models.schemas import (
    ConfidenceStatus,
    DetectRejectionResponse,
    DetectResponse,
    SeverityLevel,
    TopPrediction,
)

router = APIRouter(prefix="/api", tags=["Detection"])

# Allowed image types
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/jpg", "image/webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB


# ─── /health ──────────────────────────────────────────────────────────────────

@router.get("/health")
async def health_check():
    """Quick health check — confirms API and model status."""
    return {
        "status": "ok",
        "model_loaded": model_manager.is_loaded,
        "environment": settings.ENV,
        "version": "1.0.0",
        "classes_loaded": len(model_manager.class_names)
    }


# ─── /detect-disease ──────────────────────────────────────────────────────────

@router.post(
    "/detect-disease",
    response_model=DetectResponse,
    summary="Detect crop disease from leaf image",
    description="Upload a leaf photo. Returns disease prediction, confidence, severity, and Grad-CAM heatmap."
)
async def detect_disease(
    file: UploadFile = File(..., description="Leaf image — JPG or PNG, max 10MB"),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Detection request received | filename={file.filename} | content_type={file.content_type}")

    # ── Step 1: Validate file ──────────────────────────────────────────────────
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {file.content_type}. Upload JPG or PNG."
        )

    image_bytes = await file.read()

    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum size is 10MB."
        )

    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file uploaded."
        )

    # ── Step 2: Model inference ────────────────────────────────────────────────
    if not model_manager.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please try again in a moment."
        )

    try:
        result = model_manager.predict(image_bytes)
    except Exception as e:
        logger.error(f"Inference failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Inference failed. Ensure the image contains a clear leaf photo."
        )

    confidence = result["confidence"]
    top_3 = [TopPrediction(**p) for p in result["top_3_predictions"]]

    # ── Step 3: Confidence gate ────────────────────────────────────────────────
    # Below threshold → reject, ask for better photo
    if not result["proceed_to_advisory"]:
        logger.warning(
            f"Low confidence rejection | "
            f"confidence={confidence:.4f} | "
            f"threshold={settings.CONFIDENCE_THRESHOLD}"
        )
        return DetectRejectionResponse(
            confidence=confidence,
            top_3_predictions=top_3
        )

    # ── Step 4: Generate Grad-CAM ──────────────────────────────────────────────
    gradcam_base64 = None
    try:
        gradcam_base64 = generate_gradcam_base64(
            model=model_manager.model,
            image_tensor=result["_image_tensor"],
            original_array=result["_original_array"],
            class_idx=result["_class_idx"]
        )
        logger.info("GradCAM generated successfully")
    except Exception as e:
        # GradCAM failure is non-fatal — return result without heatmap
        logger.error(f"GradCAM generation failed: {e}")

    # ── Step 5: Save to PostgreSQL ─────────────────────────────────────────────
    try:
        detection_record = Detection(
            disease=result["disease"],
            display_name=result["display_name"],
            crop_type=result["crop_type"],
            confidence=confidence,
            severity=result["severity"],
            proceeded_to_advisory=True,
            gradcam_base64=gradcam_base64,
            image_filename=file.filename
        )
        db.add(detection_record)
        await db.flush()  # get auto-generated id without committing yet
        logger.info(f"Detection saved to DB | id={detection_record.id}")
    except Exception as e:
        # DB failure is non-fatal — return result without saving
        logger.error(f"DB save failed: {e}")

    # ── Step 6: Build and return response ─────────────────────────────────────
    return DetectResponse(
        disease=result["disease"],
        display_name=result["display_name"],
        crop_type=result["crop_type"],
        confidence=confidence,
        severity=SeverityLevel(result["severity"]),
        confidence_status=ConfidenceStatus.HIGH,
        gradcam_image=gradcam_base64,
        top_3_predictions=top_3,
        proceed_to_advisory=True,
        message=None
    )
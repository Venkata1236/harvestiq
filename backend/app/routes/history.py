"""
/api/detections — History API
GET  /api/detections         — list all detections
GET  /api/detections/{id}    — single detection
DELETE /api/detections/{id}  — delete detection
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.database.models import Detection

router = APIRouter()


@router.get("/detections")
async def list_detections(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Detection)
        .order_by(Detection.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    detections = result.scalars().all()

    return {
        "status": "success",
        "total": len(detections),
        "detections": [
            {
                "id": d.id,
                "disease": d.disease,
                "display_name": d.display_name,
                "crop_type": d.crop_type,
                "confidence": round(d.confidence * 100, 1),
                "severity": d.severity,
                "image_filename": d.image_filename,
                "created_at": d.created_at.isoformat(),
            }
            for d in detections
        ],
    }


@router.get("/detections/{detection_id}")
async def get_detection(
    detection_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Detection).where(Detection.id == detection_id)
    )
    detection = result.scalar_one_or_none()

    if not detection:
        raise HTTPException(status_code=404, detail=f"Detection {detection_id} not found")

    return {
        "status": "success",
        "detection": {
            "id": detection.id,
            "disease": detection.disease,
            "display_name": detection.display_name,
            "crop_type": detection.crop_type,
            "confidence": round(detection.confidence * 100, 1),
            "severity": detection.severity,
            "proceeded_to_advisory": detection.proceeded_to_advisory,
            "image_filename": detection.image_filename,
            "gradcam_base64": detection.gradcam_base64,
            "created_at": detection.created_at.isoformat(),
        }
    }


@router.delete("/detections/{detection_id}")
async def delete_detection(
    detection_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Detection).where(Detection.id == detection_id)
    )
    detection = result.scalar_one_or_none()

    if not detection:
        raise HTTPException(status_code=404, detail=f"Detection {detection_id} not found")

    await db.execute(delete(Detection).where(Detection.id == detection_id))

    return {
        "status": "success",
        "message": f"Detection {detection_id} deleted"
    }
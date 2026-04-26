from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ─── Enums ────────────────────────────────────────────────────────────────────

class SeverityLevel(str, Enum):
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"


class ConfidenceStatus(str, Enum):
    HIGH = "HIGH"
    LOW = "LOW"


class SpreadRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class FarmingType(str, Enum):
    ORGANIC = "organic"
    CONVENTIONAL = "conventional"
    ANY = "any"


# ─── Detection Schemas ────────────────────────────────────────────────────────

class TopPrediction(BaseModel):
    disease: str
    display_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class DetectResponse(BaseModel):
    """Response from POST /detect-disease"""

    disease: str = Field(..., description="Raw class name e.g. Tomato___Late_blight")
    display_name: str = Field(..., description="Human readable e.g. Tomato Late Blight")
    crop_type: str = Field(..., description="Crop name e.g. Tomato")
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: SeverityLevel
    confidence_status: ConfidenceStatus
    gradcam_image: Optional[str] = Field(
        None,
        description="Base64 encoded PNG heatmap overlay"
    )
    top_3_predictions: list[TopPrediction]
    proceed_to_advisory: bool = Field(
        ...,
        description="True if confidence >= 0.65, False otherwise"
    )
    message: Optional[str] = Field(
        None,
        description="Set when confidence is LOW — retry instructions"
    )


class DetectRejectionResponse(BaseModel):
    """Returned when confidence < 0.65"""

    proceed_to_advisory: bool = False
    confidence: float
    confidence_status: ConfidenceStatus = ConfidenceStatus.LOW
    message: str = (
        "Image quality insufficient. "
        "Please retake in good lighting with the leaf filling 70% of the frame."
    )
    top_3_predictions: list[TopPrediction]


# ─── Advisory Schemas ─────────────────────────────────────────────────────────

class AdvisoryRequest(BaseModel):
    """Request body for POST /advisory"""

    disease: str = Field(..., description="Raw class name from /detect-disease")
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: SeverityLevel
    crop_type: str
    farm_size_acres: float = Field(
        default=1.0,
        ge=0.1,
        le=1000.0,
        description="Farm size in acres for cost estimation"
    )
    farming_type: FarmingType = FarmingType.ANY


class TreatmentOption(BaseModel):
    product: str
    dosage: str
    frequency: str
    estimated_cost_inr: float


class DiseaseExplanation(BaseModel):
    simple_description: str
    cause: str
    spread_risk: SpreadRisk
    days_to_act: int = Field(..., description="Days before irreversible damage")


class TreatmentPlan(BaseModel):
    organic_options: list[TreatmentOption]
    chemical_options: list[TreatmentOption]
    application_schedule: list[str]


class RecoveryNutrition(BaseModel):
    week_1: str
    week_2: str
    week_3: str
    week_4: str
    total_cost_estimate_inr: float


class AdvisoryResponse(BaseModel):
    """Response from POST /advisory"""

    disease_explanation: DiseaseExplanation
    treatment_plan: TreatmentPlan
    recovery_nutrition: RecoveryNutrition
    prevention_tips: list[str]
    expected_recovery_days: int


# ─── Health Check Schema ──────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str = "ok"
    model_loaded: bool
    environment: str
    version: str = "1.0.0"


# ─── Database Record Schema ───────────────────────────────────────────────────

class DetectionRecord(BaseModel):
    """Mirrors the PostgreSQL detections table row"""

    id: int
    disease: str
    display_name: str
    crop_type: str
    confidence: float
    severity: str
    proceeded_to_advisory: bool

    class Config:
        from_attributes = True  # allows ORM model → Pydantic conversion
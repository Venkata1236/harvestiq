import json
from pathlib import Path

import torch
import torch.nn as nn
from loguru import logger
from torchvision import models

from app.core.config import settings
from app.ml.preprocess import preprocess_for_gradcam, preprocess_for_inference


# ─── Severity Classification ──────────────────────────────────────────────────

def classify_severity(confidence: float) -> str:
    """
    Map confidence score to disease severity level.

    High confidence = model is very sure = likely advanced/clear disease
    Lower confidence = early stage or ambiguous presentation
    """
    if confidence >= 0.85:
        return "SEVERE"
    elif confidence >= 0.75:
        return "MODERATE"
    else:
        return "MILD"


def format_display_name(raw_class: str) -> tuple[str, str]:
    """
    Convert raw dataset class name to human-readable format.

    Input:  'Tomato___Late_blight'
    Output: display_name='Tomato Late Blight', crop_type='Tomato'

    Input:  'Apple___Apple_scab'
    Output: display_name='Apple Scab', crop_type='Apple'
    """
    parts = raw_class.split("___")
    crop_type = parts[0].replace("_", " ")

    if len(parts) > 1:
        disease_part = parts[1].replace("_", " ").title()
        # Handle healthy class
        if "healthy" in disease_part.lower():
            display_name = f"{crop_type} — Healthy"
        else:
            display_name = disease_part
    else:
        display_name = crop_type

    return display_name, crop_type


# ─── Model Builder ────────────────────────────────────────────────────────────

def build_inference_model(num_classes: int = 38) -> nn.Module:
    """
    Rebuild the exact same architecture used in train.py.
    Must match EXACTLY — otherwise loading state_dict will fail.
    """
    model = models.resnet50(weights=None)  # No pretrained weights — we load our own
    model.fc = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(2048, num_classes)
    )
    return model


# ─── Model Manager ────────────────────────────────────────────────────────────

class ModelManager:
    """
    Singleton-style model manager.
    Loads model once, serves all requests.

    Usage:
        model_manager = ModelManager()
        model_manager.load()           # called once at startup
        result = model_manager.predict(image_bytes)
    """

    def __init__(self):
        self.model: nn.Module | None = None
        self.class_names: list[str] = []
        self.device = torch.device("cpu")  # CPU inference
        self.is_loaded = False

    def load(self) -> None:
        """
        Load model weights and class names from disk.
        Called once during FastAPI startup via lifespan.
        """
        model_path = settings.model_full_path
        class_names_path = settings.class_names_full_path

        if not model_path.exists():
            logger.warning(
                f"Model file not found at {model_path}. "
                "Train the model on Colab first, then place "
                "harvestiq_resnet50.pt in backend/saved_models/"
            )
            return

        if not class_names_path.exists():
            logger.error(f"class_names.json not found at {class_names_path}")
            return

        # Load class names
        with open(class_names_path, "r") as f:
            self.class_names = json.load(f)
        logger.info(f"Loaded {len(self.class_names)} class names")

        # Build architecture + load weights
        self.model = build_inference_model(num_classes=len(self.class_names))
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()  # Disable dropout + batchnorm training mode

        self.is_loaded = True
        logger.info(f"Model loaded successfully from {model_path}")

    def predict(self, image_bytes: bytes) -> dict:
        """
        Run full inference pipeline on raw image bytes.

        Returns dict with:
        - disease: raw class name
        - display_name: human readable
        - crop_type: crop name
        - confidence: float 0-1
        - severity: MILD / MODERATE / SEVERE
        - confidence_status: HIGH / LOW
        - top_3: list of top 3 predictions
        - proceed_to_advisory: bool
        - image_tensor: for GradCAM (not in API response)
        - original_array: for GradCAM overlay (not in API response)
        """
        if not self.is_loaded:
            raise RuntimeError(
                "Model not loaded. Ensure harvestiq_resnet50.pt exists "
                "in saved_models/ and app has started correctly."
            )

        # Preprocess — get both tensor and original array
        # original_array needed for GradCAM overlay
        image_tensor, original_array = preprocess_for_gradcam(image_bytes)
        image_tensor = image_tensor.to(self.device)

        # Inference
        with torch.no_grad():
            outputs = self.model(image_tensor)          # [1, 38]
            probabilities = torch.softmax(outputs, dim=1)  # convert logits → probabilities

        # Top 3 predictions
        top3_probs, top3_indices = torch.topk(probabilities, k=3, dim=1)
        top3_probs = top3_probs.squeeze().tolist()
        top3_indices = top3_indices.squeeze().tolist()

        # Primary prediction
        top_confidence = top3_probs[0]
        top_class_idx = top3_indices[0]
        top_class_name = self.class_names[top_class_idx]

        display_name, crop_type = format_display_name(top_class_name)
        severity = classify_severity(top_confidence)

        # Build top 3 list
        top_3_predictions = [
            {
                "disease": self.class_names[top3_indices[i]],
                "display_name": format_display_name(self.class_names[top3_indices[i]])[0],
                "confidence": round(top3_probs[i], 4)
            }
            for i in range(3)
        ]

        proceed = top_confidence >= settings.CONFIDENCE_THRESHOLD

        logger.info(
            f"Prediction: {top_class_name} | "
            f"Confidence: {top_confidence:.4f} | "
            f"Proceed: {proceed}"
        )

        return {
            "disease": top_class_name,
            "display_name": display_name,
            "crop_type": crop_type,
            "confidence": round(top_confidence, 4),
            "severity": severity,
            "confidence_status": "HIGH" if top_confidence >= settings.CONFIDENCE_THRESHOLD else "LOW",
            "top_3_predictions": top_3_predictions,
            "proceed_to_advisory": proceed,
            # These two are used by detect.py for GradCAM — not in final API response
            "_image_tensor": image_tensor,
            "_original_array": original_array,
            "_class_idx": top_class_idx,
        }


# ─── Global instance ──────────────────────────────────────────────────────────
# Imported by main.py for startup/shutdown
# Imported by detect.py for inference

model_manager = ModelManager()

"""
GradCAM — Gradient-weighted Class Activation Mapping
Highlights which parts of the leaf image triggered the disease prediction.
"""

import base64
import io

import cv2
import numpy as np
import torch
import torch.nn as nn
from loguru import logger
from PIL import Image


class GradCAM:
    """
    GradCAM for ResNet50.
    Uses the last residual block: model.layer4[-1]
    """

    def __init__(self, model: nn.Module):
        self.model = model
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self) -> None:
        target_layer = self.model.layer4[-1]

        def forward_hook(module, inputs, output):
            self.activations = output

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0]

        target_layer.register_forward_hook(forward_hook)
        target_layer.register_full_backward_hook(backward_hook)

    def generate(
        self,
        image_tensor: torch.Tensor,
        class_idx: int,
        original_array: np.ndarray,
    ) -> str:
        self.model.eval()
        self.model.zero_grad()

        output = self.model(image_tensor)
        score = output[0, class_idx]
        score.backward()

        gradients = self.gradients.detach()
        activations = self.activations.detach()

        weights = gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * activations).sum(dim=1, keepdim=True)
        cam = torch.relu(cam)

        cam = cam.squeeze().cpu().numpy()
        cam -= cam.min()
        if cam.max() > 0:
            cam /= cam.max()

        h, w = original_array.shape[:2]
        cam = cv2.resize(cam, (w, h))

        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

        overlay = (0.6 * original_array + 0.4 * heatmap).astype(np.uint8)

        buffer = io.BytesIO()
        Image.fromarray(overlay).save(buffer, format="PNG")
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode("utf-8")


def generate_gradcam(
    model: nn.Module,
    image_tensor: torch.Tensor,
    class_idx: int,
    original_array: np.ndarray,
) -> str | None:
    try:
        gradcam = GradCAM(model)
        return gradcam.generate(image_tensor, class_idx, original_array)
    except Exception as e:
        logger.error(f"GradCAM failed: {e}")
        return None
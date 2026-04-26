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
    Gradient-weighted Class Activation Mapping for ResNet50.

    How it works:
    1. Register hooks on target layer (layer4) to capture:
       - activations during forward pass
       - gradients during backward pass
    2. Run forward pass → get prediction
    3. Run backward pass on predicted class score
    4. Weight each activation map by its mean gradient
    5. ReLU + normalize → heatmap
    6. Resize + overlay on original image
    """

    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.target_layer = target_layer

        # Storage for hooks
        self.activations: torch.Tensor | None = None
        self.gradients: torch.Tensor | None = None

        # Register hooks
        self._register_hooks()

    def _register_hooks(self) -> None:
        """
        Forward hook: captures activations (feature maps) from target layer.
        Backward hook: captures gradients flowing back through target layer.
        """

        def forward_hook(module, input, output):
            # output shape: [batch, channels, height, width]
            # For layer4: [1, 2048, 7, 7]
            self.activations = output.detach()

        def backward_hook(module, grad_input, grad_output):
            # grad_output[0] shape: [batch, channels, height, width]
            self.gradients = grad_output[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)
        logger.debug("GradCAM hooks registered on target layer")

    def generate(
        self,
        image_tensor: torch.Tensor,
        class_idx: int | None = None
    ) -> tuple[np.ndarray, int]:
        """
        Generate GradCAM heatmap for the given image tensor.

        Args:
            image_tensor: preprocessed image [1, 3, 224, 224]
            class_idx: target class. If None, uses predicted class.

        Returns:
            heatmap: normalized heatmap [224, 224] values in [0, 1]
            class_idx: the class index used for gradcam
        """
        self.model.eval()
        image_tensor = image_tensor.requires_grad_(True)

        # Forward pass
        output = self.model(image_tensor)  # [1, 38]

        if class_idx is None:
            class_idx = output.argmax(dim=1).item()

        # Zero all gradients
        self.model.zero_grad()

        # Backward pass on target class score only
        # This computes: d(class_score) / d(layer4_activations)
        class_score = output[0, class_idx]
        class_score.backward()

        # Gradients shape: [1, 2048, 7, 7]
        # Activations shape: [1, 2048, 7, 7]
        gradients = self.gradients  # [1, 2048, 7, 7]
        activations = self.activations  # [1, 2048, 7, 7]

        # Global average pool the gradients → importance weight per channel
        # Shape: [1, 2048, 1, 1]
        weights = gradients.mean(dim=[2, 3], keepdim=True)

        # Weighted combination of activation maps
        # Shape: [1, 2048, 7, 7] → sum across channels → [1, 1, 7, 7]
        weighted_activations = (weights * activations).sum(dim=1, keepdim=True)

        # ReLU: only keep positive contributions
        # Negative values = regions that REDUCE the class score
        heatmap = torch.relu(weighted_activations)

        # Normalize to [0, 1]
        heatmap = heatmap.squeeze().cpu().numpy()
        heatmap = heatmap - heatmap.min()
        if heatmap.max() > 0:
            heatmap = heatmap / heatmap.max()

        logger.debug(f"GradCAM heatmap generated for class_idx={class_idx}")
        return heatmap, class_idx

    def overlay_heatmap(
        self,
        heatmap: np.ndarray,
        original_image: np.ndarray,
        alpha: float = 0.5
    ) -> np.ndarray:
        """
        Overlay colored heatmap on original image.

        Args:
            heatmap: [H, W] normalized values in [0, 1]
            original_image: [H, W, 3] numpy array values in [0, 1]
            alpha: heatmap transparency (0=invisible, 1=opaque)

        Returns:
            overlaid image [H, W, 3] as uint8
        """
        # Resize heatmap from 7×7 → 224×224
        heatmap_resized = cv2.resize(heatmap, (224, 224))

        # Apply colormap: blue=cold (model ignored) → red=hot (model focused)
        heatmap_colored = cv2.applyColorMap(
            np.uint8(255 * heatmap_resized),
            cv2.COLORMAP_JET
        )
        # cv2 uses BGR → convert to RGB
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        heatmap_colored = heatmap_colored / 255.0

        # Blend heatmap + original image
        original_uint8 = np.uint8(255 * original_image)
        heatmap_uint8 = np.uint8(255 * heatmap_colored)

        overlaid = cv2.addWeighted(
            original_uint8, 1 - alpha,
            heatmap_uint8, alpha,
            gamma=0
        )
        return overlaid  # [224, 224, 3] uint8

    def to_base64(self, image_array: np.ndarray) -> str:
        """
        Convert numpy image array to base64 string for API response.
        Frontend receives this and renders it as <img src="data:image/png;base64,...">
        """
        pil_image = Image.fromarray(image_array)
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        buffer.seek(0)
        encoded = base64.b64encode(buffer.read()).decode("utf-8")
        return encoded


def generate_gradcam_base64(
    model: nn.Module,
    image_tensor: torch.Tensor,
    original_array: np.ndarray,
    class_idx: int | None = None
) -> str:
    """
    Convenience function used by the API endpoint.

    Args:
        model: loaded ResNet50
        image_tensor: preprocessed [1, 3, 224, 224]
        original_array: original image as numpy [224, 224, 3] in [0,1]
        class_idx: target class (None = use predicted class)

    Returns:
        base64 encoded PNG string of heatmap overlay
    """
    gradcam = GradCAM(model, target_layer=model.layer4)
    heatmap, used_class = gradcam.generate(image_tensor, class_idx)
    overlaid = gradcam.overlay_heatmap(heatmap, original_array)
    base64_str = gradcam.to_base64(overlaid)

    logger.info(f"GradCAM generated for class_idx={used_class} | base64 length={len(base64_str)}")
    return base64_str
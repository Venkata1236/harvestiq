from pathlib import Path

import numpy as np
import torch
from loguru import logger
from PIL import Image
from torchvision import transforms

# ImageNet mean and std — ResNet50 was pretrained on these values
# We MUST use same normalization during inference as during training
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
IMAGE_SIZE = 224


# Training transforms — heavy augmentation to prevent overfitting
train_transforms = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.3),
    transforms.RandomRotation(degrees=20),
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2,
        hue=0.05
    ),
    transforms.RandomResizedCrop(
        size=IMAGE_SIZE,
        scale=(0.8, 1.0)  # zoom between 80% and 100%
    ),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])


# Validation transforms — NO augmentation, just clean resize + normalize
val_transforms = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])


# Inference transforms — identical to val_transforms
# Defined separately for clarity — this is what the API endpoint uses
inference_transforms = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])


def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    """
    Convert raw image bytes (from API upload) into a PIL Image.
    Converts to RGB to handle PNG (RGBA) and grayscale uploads.
    """
    import io
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    logger.debug(f"Loaded image: size={image.size}, mode={image.mode}")
    return image


def preprocess_for_inference(image_bytes: bytes) -> torch.Tensor:
    """
    Full pipeline: raw bytes → normalized tensor ready for ResNet50.

    Returns tensor of shape [1, 3, 224, 224]
    The leading 1 is the batch dimension — model expects batches.
    """
    image = load_image_from_bytes(image_bytes)
    tensor = inference_transforms(image)
    tensor = tensor.unsqueeze(0)  # [3, 224, 224] → [1, 3, 224, 224]
    logger.debug(f"Preprocessed tensor shape: {tensor.shape}")
    return tensor


def preprocess_for_gradcam(image_bytes: bytes) -> tuple[torch.Tensor, np.ndarray]:
    """
    Returns BOTH:
    - tensor: for model inference + grad-cam computation
    - original_array: for heatmap overlay on the original image

    GradCAM needs the original image to overlay the heatmap on.
    """
    image = load_image_from_bytes(image_bytes)

    # Keep original as numpy array for overlay
    original_resized = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    original_array = np.array(original_resized) / 255.0  # normalize to [0, 1]

    # Preprocessed tensor for model
    tensor = inference_transforms(image).unsqueeze(0)

    return tensor, original_array


def denormalize(tensor: torch.Tensor) -> np.ndarray:
    """
    Reverse the ImageNet normalization.
    Used when we need to display the preprocessed tensor as an image.
    """
    mean = torch.tensor(IMAGENET_MEAN).view(3, 1, 1)
    std = torch.tensor(IMAGENET_STD).view(3, 1, 1)
    tensor = tensor.squeeze(0) * std + mean
    tensor = torch.clamp(tensor, 0, 1)
    return tensor.permute(1, 2, 0).numpy()
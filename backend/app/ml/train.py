import json
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
import torch.nn as nn
from loguru import logger
from sklearn.metrics import classification_report, confusion_matrix
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import DataLoader
from torchvision import datasets, models

# Add backend root to path so imports work from Colab
sys.path.append(str(Path(__file__).resolve().parents[3]))
from app.ml.preprocess import train_transforms, val_transforms

# ─── Configuration ────────────────────────────────────────────────────────────

DATA_DIR = Path("data/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)")
TRAIN_DIR = DATA_DIR / "train"
VALID_DIR = DATA_DIR / "valid"
SAVE_DIR = Path("saved_models")
SAVE_DIR.mkdir(exist_ok=True)

BATCH_SIZE = 32
NUM_EPOCHS = 15
LEARNING_RATE = 1e-4
NUM_CLASSES = 38
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

logger.info(f"Training on: {DEVICE}")


# ─── Dataset & DataLoaders ────────────────────────────────────────────────────

def get_dataloaders() -> tuple[DataLoader, DataLoader, list[str]]:
    train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transforms)
    val_dataset = datasets.ImageFolder(VALID_DIR, transform=val_transforms)

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=4,
        pin_memory=True if DEVICE.type == "cuda" else False
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=4,
        pin_memory=True if DEVICE.type == "cuda" else False
    )

    class_names = train_dataset.classes
    logger.info(f"Train samples: {len(train_dataset)} | Val samples: {len(val_dataset)}")
    logger.info(f"Classes found: {len(class_names)}")

    # Save class names immediately
    with open(SAVE_DIR / "class_names.json", "w") as f:
        json.dump(class_names, f, indent=2)
    logger.info("class_names.json saved")

    return train_loader, val_loader, class_names


# ─── Model Architecture ───────────────────────────────────────────────────────

def build_model() -> nn.Module:
    """
    Progressive unfreezing strategy:
    Phase 1 → Only FC head trainable (base frozen)
    Phase 2 → Unfreeze layer4 (called at epoch 5)
    Phase 3 → Unfreeze layer3 (called at epoch 10)
    """
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

    # Step 1 — Freeze ALL base layers
    for param in model.parameters():
        param.requires_grad = False

    # Step 2 — Replace FC head for 38 classes
    model.fc = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(2048, 38)
    )
    # FC head is trainable by default (new layers always are)

    logger.info("Model built — base frozen, FC head trainable")
    return model.to(DEVICE)


def unfreeze_layer(model: nn.Module, layer_name: str) -> None:
    """Unfreeze a specific ResNet layer for fine-tuning."""
    layer = getattr(model, layer_name)
    for param in layer.parameters():
        param.requires_grad = True
    logger.info(f"Unfrozen: {layer_name}")


# ─── Training Loop ────────────────────────────────────────────────────────────

def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    epoch: int
) -> float:
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (images, labels) in enumerate(loader):
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total += labels.size(0)

        if batch_idx % 100 == 0:
            logger.info(
                f"Epoch {epoch} | Batch {batch_idx}/{len(loader)} "
                f"| Loss: {loss.item():.4f}"
            )

    avg_loss = total_loss / len(loader)
    accuracy = 100.0 * correct / total
    logger.info(f"Epoch {epoch} TRAIN | Loss: {avg_loss:.4f} | Acc: {accuracy:.2f}%")
    return avg_loss


def validate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    epoch: int
) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            loss = criterion(outputs, labels)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
            total += labels.size(0)

    avg_loss = total_loss / len(loader)
    accuracy = 100.0 * correct / total
    logger.info(f"Epoch {epoch} VAL   | Loss: {avg_loss:.4f} | Acc: {accuracy:.2f}%")
    return avg_loss, accuracy


# ─── Per-Class Evaluation ─────────────────────────────────────────────────────

def evaluate_per_class(
    model: nn.Module,
    loader: DataLoader,
    class_names: list[str]
) -> None:
    """
    Compute per-class accuracy on validation set.
    Identifies bottom 5 performing classes — candidates for more data augmentation.
    Saves confusion matrix as PNG.
    """
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(DEVICE)
            outputs = model(images)
            _, predicted = outputs.max(1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())

    # Classification report
    report = classification_report(
        all_labels, all_preds,
        target_names=class_names,
        output_dict=True
    )

    # Per-class accuracy
    per_class_acc = {
        class_names[i]: report[class_names[i]]["recall"]
        for i in range(len(class_names))
        if class_names[i] in report
    }

    # Bottom 5 performing classes
    sorted_classes = sorted(per_class_acc.items(), key=lambda x: x[1])
    logger.info("Bottom 5 classes (need more augmentation):")
    for cls, acc in sorted_classes[:5]:
        logger.info(f"  {cls}: {acc*100:.1f}%")

    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(20, 20))
    sns.heatmap(
        cm,
        annot=False,  # 38x38 is too dense for annotations
        fmt="d",
        cmap="Blues",
        xticklabels=[c.split("___")[-1][:15] for c in class_names],
        yticklabels=[c.split("___")[-1][:15] for c in class_names]
    )
    plt.title("HarvestIQ — Confusion Matrix (Validation Set)")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    plt.savefig(SAVE_DIR / "confusion_matrix.png", dpi=150)
    logger.info("confusion_matrix.png saved")


# ─── Main Training Pipeline ───────────────────────────────────────────────────

def train() -> None:
    train_loader, val_loader, class_names = get_dataloaders()
    model = build_model()

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LEARNING_RATE
    )
    scheduler = StepLR(optimizer, step_size=5, gamma=0.5)

    best_val_accuracy = 0.0

    for epoch in range(1, NUM_EPOCHS + 1):

        # Progressive unfreezing schedule
        if epoch == 6:
            unfreeze_layer(model, "layer4")
            # Rebuild optimizer to include newly unfrozen params
            optimizer = torch.optim.Adam(
                filter(lambda p: p.requires_grad, model.parameters()),
                lr=LEARNING_RATE * 0.1  # lower LR for pretrained layers
            )
            scheduler = StepLR(optimizer, step_size=5, gamma=0.5)

        if epoch == 11:
            unfreeze_layer(model, "layer3")
            optimizer = torch.optim.Adam(
                filter(lambda p: p.requires_grad, model.parameters()),
                lr=LEARNING_RATE * 0.01  # even lower for deeper layers
            )
            scheduler = StepLR(optimizer, step_size=5, gamma=0.5)

        train_one_epoch(model, train_loader, optimizer, criterion, epoch)
        val_loss, val_accuracy = validate(model, val_loader, criterion, epoch)
        scheduler.step()

        # Save best model
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            torch.save(
                model.state_dict(),
                SAVE_DIR / "harvestiq_resnet50.pt"
            )
            logger.info(f"New best model saved — Val Acc: {val_accuracy:.2f}%")

    logger.info(f"Training complete. Best Val Accuracy: {best_val_accuracy:.2f}%")

    # Final evaluation — per-class accuracy + confusion matrix
    logger.info("Running per-class evaluation...")
    evaluate_per_class(model, val_loader, class_names)

    # Warn if accuracy below threshold
    if best_val_accuracy < 88.0:
        logger.warning(
            f"Val accuracy {best_val_accuracy:.2f}% is below 88% target. "
            "Consider unfreezing layer2 before proceeding."
        )


if __name__ == "__main__":
    train()
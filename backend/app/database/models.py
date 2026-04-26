from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Detection(Base):
    """
    Stores every disease detection request.

    Used for:
    - Farmer history (HistoryPage on frontend)
    - Monitoring: track confidence distribution over time
    - Alert: if avg confidence drops → possible domain shift
    """

    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    disease: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True  # fast lookup by disease type
    )
    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    crop_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True  # fast lookup by crop
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    proceeded_to_advisory: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    gradcam_base64: Mapped[str | None] = mapped_column(
        Text,           # Text not String — base64 is very long
        nullable=True
    )
    image_filename: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True  # fast lookup by date
    )

    def __repr__(self) -> str:
        return (
            f"<Detection id={self.id} "
            f"disease={self.disease} "
            f"confidence={self.confidence:.2f}>"
        )
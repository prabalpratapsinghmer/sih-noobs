"""ATM prediction model for fraud location predictions."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from api.models import Base


class AtmPrediction(Base):
    """ATM prediction model for fraud location predictions."""

    __tablename__ = "atm_predictions"

    prediction_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id: Mapped[str | None] = mapped_column(String(50), ForeignKey("complaints.complaint_id"), nullable=True)
    atm_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    probability: Mapped[float] = mapped_column(Float, nullable=False)
    time_window: Mapped[float | None] = mapped_column(Float, nullable=True)  # Hours
    predicted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<AtmPrediction(prediction_id={self.prediction_id}, atm_id={self.atm_id}, probability={self.probability})>"

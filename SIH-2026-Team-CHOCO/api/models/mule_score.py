"""Mule scoring model for fraud detection."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from api.models import Base


class RiskLevel(str):
    """Risk level enumeration."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MuleScore(Base):
    """Mule score model for fraud detection scores."""

    __tablename__ = "mule_scores"

    score_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    complaint_id: Mapped[str | None] = mapped_column(String(50), ForeignKey("complaints.complaint_id"), nullable=True)
    gnn_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    rule_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    final_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<MuleScore(score_id={self.score_id}, account_id={self.account_id}, risk_level={self.risk_level}, final_score={self.final_score})>"

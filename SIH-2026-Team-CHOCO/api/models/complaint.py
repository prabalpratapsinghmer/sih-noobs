"""Complaint model for cybercrime reports."""

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from api.models import Base


class ComplaintStatus(StrEnum):
    """Complaint status enumeration."""

    SUBMITTED = "SUBMITTED"
    ANALYZING = "ANALYZING"
    ACTION_TAKEN = "ACTION_TAKEN"
    RESOLVED = "RESOLVED"


class Complaint(Base):
    """Complaint model for cybercrime complaints."""

    __tablename__ = "complaints"

    complaint_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    victim_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("victims.victim_id"), nullable=True)
    amount: Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fraud_type: Mapped[str] = mapped_column(String(50), nullable=False)
    fraudster_upi: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fraudster_phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    fraudster_account: Mapped[bytes | None] = mapped_column(nullable=True)  # Encrypted
    fraudster_bank: Mapped[str | None] = mapped_column(String(100), nullable=True)
    transaction_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[ComplaintStatus] = mapped_column(
        Enum(ComplaintStatus), nullable=False, default=ComplaintStatus.SUBMITTED, index=True
    )
    assigned_officer: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.user_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Complaint(complaint_id={self.complaint_id}, status={self.status}, amount={self.amount})>"

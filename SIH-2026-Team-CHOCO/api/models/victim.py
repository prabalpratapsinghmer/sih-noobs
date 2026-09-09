"""Victim model with encrypted PII."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from api.models import Base


class Victim(Base):
    """Victim model with encrypted PII fields."""

    __tablename__ = "victims"

    victim_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id: Mapped[str | None] = mapped_column(String(50), ForeignKey("complaints.complaint_id"), nullable=True)
    name: Mapped[bytes | None] = mapped_column(nullable=True)  # Encrypted with pgcrypto
    phone: Mapped[bytes | None] = mapped_column(nullable=True)  # Encrypted with pgcrypto
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    bank_account: Mapped[bytes | None] = mapped_column(nullable=True)  # Encrypted with pgcrypto
    upi_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Victim(victim_id={self.victim_id}, complaint_id={self.complaint_id})>"

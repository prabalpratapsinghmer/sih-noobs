"""Evidence model for complaint evidence files."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from api.models import Base


class Evidence(Base):
    """Evidence model for complaint evidence files."""

    __tablename__ = "evidence"

    evidence_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id: Mapped[str] = mapped_column(String(50), ForeignKey("complaints.complaint_id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    file_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)  # SHA-256
    ipfs_hash: Mapped[str | None] = mapped_column(String(100), nullable=True)  # CID from IPFS
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    uploaded_by: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.user_id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Evidence(evidence_id={self.evidence_id}, file_name={self.file_name}, complaint_id={self.complaint_id})>"

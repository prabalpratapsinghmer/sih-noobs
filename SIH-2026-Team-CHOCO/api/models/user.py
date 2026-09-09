"""User model for authentication and authorization."""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from api.models import Base


class UserRole(StrEnum):
    """User roles for RBAC."""

    ADMIN = "ADMIN"
    INSPECTOR = "INSPECTOR"
    CONSTABLE = "CONSTABLE"
    CITIZEN = "CITIZEN"
    SUPER_ADMIN = "SUPER_ADMIN"



class User(Base):
    """User model for police officers and admins."""

    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.CONSTABLE)
    station: Mapped[str | None] = mapped_column(String(100), nullable=True)
    badge_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, username={self.username}, role={self.role})>"

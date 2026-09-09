"""Pydantic schemas for admin operations."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(pattern="^(ADMIN|INSPECTOR|CONSTABLE)$")
    station: str | None = None
    badge_number: str | None = None
    phone: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: str | None = Field(default=None, pattern="^(ADMIN|INSPECTOR|CONSTABLE)$")
    station: str | None = None
    badge_number: str | None = None
    phone: str | None = None
    is_active: bool | None = None


class UserOut(BaseModel):
    user_id: str
    username: str
    email: str
    role: str
    station: str | None = None
    badge_number: str | None = None
    phone: str | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SystemHealth(BaseModel):
    status: str
    services: dict


class ModelMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float
    auc_roc: float
    trained_at: datetime
    model_version: str

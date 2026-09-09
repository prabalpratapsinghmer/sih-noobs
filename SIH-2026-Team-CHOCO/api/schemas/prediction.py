"""Pydantic schemas for predictions."""

from datetime import datetime

from pydantic import BaseModel, Field


class AtmPredictRequest(BaseModel):
    complaint_id: str
    account_ids: list[str] = []


class AtmPredictionOut(BaseModel):
    prediction_id: str
    complaint_id: str | None = None
    atm_id: str
    probability: float
    time_window: float | None = None
    predicted_at: datetime

    model_config = {"from_attributes": True}


class MuleRankResult(BaseModel):
    complaint_id: str
    mules: list[dict]
    calculated_at: datetime


class VerificationTrigger(BaseModel):
    atm_id: str
    verification_type: str = Field(default="FACIAL_RECOGNITION", pattern="^(FACIAL_RECOGNITION|OTP|RETINA_SCAN)$")
    account_ids: list[str] = Field(min_length=1)
    duration_hours: int = Field(default=4, ge=1, le=48)

"""Pydantic schemas for banking switch mock."""

from pydantic import BaseModel, Field


class StepUpVerificationRequest(BaseModel):
    atm_id: str
    verification_type: str = Field(default="FACIAL_RECOGNITION", pattern="^(FACIAL_RECOGNITION|OTP|RETINA_SCAN)$")
    account_ids: list[str] = Field(min_length=1)
    duration_hours: int = Field(default=4, ge=1, le=48)


class VerificationOut(BaseModel):
    verification_id: str
    status: str = "SUCCESS"
    message: str
    atm_id: str
    expires_at: str
    affected_accounts: int


class VerificationStatusOut(BaseModel):
    verification_id: str
    status: str
    expires_at: str
    affected_accounts: list[str] = []

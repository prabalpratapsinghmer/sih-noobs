"""Pydantic schemas for victims."""

from datetime import datetime

from pydantic import BaseModel, Field


class VictimOut(BaseModel):
    victim_id: str
    complaint_id: str | None = None
    email: str | None = None
    upi_id: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class VictimCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    phone: str = Field(min_length=10, max_length=15)
    email: str | None = None
    address: str | None = None
    bank_account: str | None = None
    upi_id: str | None = None

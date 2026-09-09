"""Pydantic schemas for complaints."""

from datetime import datetime

from pydantic import BaseModel, Field


class ComplaintCreate(BaseModel):
    name: str | None = Field(default=None, max_length=120)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    address: str | None = Field(default=None, max_length=300)
    incident_date: str | None = Field(default=None, max_length=40)
    fraudster_account: str | None = Field(default=None, max_length=50)
    amount: float = Field(gt=0)
    fraud_type: str = Field(min_length=1, max_length=50)
    fraudster_upi: str | None = Field(default=None, max_length=50)
    fraudster_phone: str | None = Field(default=None, max_length=15)
    description: str | None = Field(default=None, max_length=2000)


class ComplaintOut(BaseModel):
    complaint_id: str
    amount: float
    status: str
    fraud_type: str
    created_at: datetime
    updated_at: datetime
    assigned_officer: str | None = None

    model_config = {"from_attributes": True}


class ComplaintStatusUpdate(BaseModel):
    status: str
    resolution_note: str | None = Field(default=None, max_length=1000)


class AssignmentRequest(BaseModel):
    officer_id: str


class ComplaintDetail(BaseModel):
    complaint: ComplaintOut
    evidence: list = []
    graph: dict = {}

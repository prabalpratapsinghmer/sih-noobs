"""Pydantic schemas for police operations."""

from datetime import datetime

from pydantic import BaseModel, Field


class ComplaintFilter(BaseModel):
    status: str | None = None
    fraud_type: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None


class HighRiskAtm(BaseModel):
    atm_id: str
    fraud_history_count: int
    success_rate: float
    area_type: str = ""


class AtmHeatmapItem(BaseModel):
    atm_id: str
    latitude: float
    longitude: float
    risk_score: float
    fraud_count: int


class MuleResult(BaseModel):
    account_id: str
    holder_name: str = ""
    final_score: float
    risk_level: str
    rule_score: float | None = None
    gnn_probability: float | None = None


class FirRequest(BaseModel):
    complaint_id: str


class FirDraft(BaseModel):
    fir_number: str
    complaint_id: str
    content: str
    generated_at: datetime


class FreezeRequest(BaseModel):
    complaint_id: str
    account_ids: list[str] = Field(default_factory=list)
    node_ids: list[str] | None = None
    duration_hours: int = Field(default=24, ge=1, le=720)

    def model_post_init(self, __context):
        if not self.account_ids and self.node_ids:
            self.account_ids = self.node_ids
        if not self.account_ids:
            self.account_ids = ["mule-1a", "mule-1b", "mule-2a", "mule-2b"]


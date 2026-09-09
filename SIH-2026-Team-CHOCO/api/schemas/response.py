"""Response Schemas for Cybercrime Prediction API."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ATMPredictionItem(BaseModel):
    atm_id: Optional[str] = Field(None, description="Unique ATM identifier")
    atm_index: Optional[int] = Field(None, description="ATM index in the model's output space")
    probability: float = Field(..., description="Predicted withdrawal probability (0.0 - 1.0)")
    time_window: Optional[str] = Field(None, description="Estimated criminal arrival time window")
    risk_score: Optional[int] = Field(None, description="Location risk priority score (0 - 100)")
    address: Optional[str] = Field(None, description="ATM physical street address / locality")
    bank_name: Optional[str] = Field(None, description="Bank operating the ATM")
    latitude: Optional[float] = Field(None, description="ATM latitude coordinate")
    longitude: Optional[float] = Field(None, description="ATM longitude coordinate")


class ATMPredictionResponse(BaseModel):
    predictions: List[ATMPredictionItem]
    top_k: int
    latency_ms: Optional[float] = None


class ComplaintPredictResponse(BaseModel):
    complaint_id: str
    predictions: List[ATMPredictionItem]
    processing_time_ms: float
    timestamp: str


class STMPredictionResponse(BaseModel):
    predictions: List[Dict[str, Any]]
    top_k: int
    processing_time_ms: Optional[float] = None


class MuleScoreItem(BaseModel):
    account_id: str
    gnn_probability: float
    rule_score: float
    final_score: float
    risk_level: str
    risk_color: str
    action: str


class MuleDetectionResponse(BaseModel):
    account_id: Optional[str] = None
    complaint_id: Optional[str] = None
    gnn_probability: float = 0.0
    rule_score: float = 0.0
    final_score: float = 0.0
    risk_level: str = "LOW"
    risk_color: str = "green"
    action: str = "No Action"
    latency_ms: Optional[float] = None
    mules: Optional[List[MuleScoreItem]] = None
    processing_time_ms: Optional[float] = None


class StepUpVerificationResponse(BaseModel):
    status: str = Field(..., description="SUCCESS | FAILED")
    message: str
    verification_id: str
    expires_at: Optional[str] = None
    blockchain_hash: Optional[str] = None
    atm_id: str
    account_ids: Optional[List[str]] = None


class ModelStatusResponse(BaseModel):
    status: str
    models_loaded: Optional[Dict[str, bool]] = None
    models: Optional[Dict[str, Any]] = None
    version: Optional[str] = None
    device: Optional[str] = None
    uptime_seconds: Optional[float] = None
    system: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class ModelMetricsResponse(BaseModel):
    request_count: Optional[int] = None
    avg_latency_ms: Optional[float] = None
    error_count: Optional[int] = None
    spatio_temporal: Optional[Dict[str, Any]] = None
    mule_detection: Optional[Dict[str, Any]] = None
    models: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    models_loaded: Dict[str, bool]
    version: str

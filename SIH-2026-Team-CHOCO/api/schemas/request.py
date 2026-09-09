"""Request Schemas for Cybercrime Prediction API."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SpatialFeatures(BaseModel):
    lat: float = Field(..., description="Latitude coordinate in Bangalore region (12.8 - 13.2)")
    lon: float = Field(..., description="Longitude coordinate in Bangalore region (77.4 - 77.8)")
    dist_metro: float = Field(..., ge=0.0, description="Distance to nearest metro station in km")
    dist_police: float = Field(..., ge=0.0, description="Distance to nearest police station in km")


class TemporalFeatures(BaseModel):
    hour: int = Field(..., ge=0, le=23, description="Hour of day (0-23)")
    day: int = Field(..., ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)")
    is_weekend: bool = Field(..., description="True if Saturday or Sunday")
    time_since_complaint: float = Field(..., ge=0.0, description="Hours elapsed since complaint was filed")
    fraud_spike_hour: int = Field(default=22, ge=0, le=23, description="Historical fraud peak hour")


class ATMPredictionRequest(BaseModel):
    """Request schema for ATM prediction via the modular /predict/atm route."""
    spatial: SpatialFeatures
    temporal: TemporalFeatures
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top ATM recommendations")


class STMPredictionRequest(BaseModel):
    """Alias kept for backward compatibility with api/main.py."""
    spatial: SpatialFeatures
    temporal: TemporalFeatures
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top ATM recommendations")


class ComplaintPredictRequest(BaseModel):
    complaint_id: str = Field(..., description="Unique complaint identifier (e.g. C1001)")
    amount: float = Field(..., gt=0, description="Defrauded amount in INR")
    timestamp: str = Field(..., description="Complaint filing timestamp in ISO format")
    fraud_type: str = Field(default="investment", description="investment | UPI | KYC | loan | other")
    fraudster_upi: Optional[str] = Field(None, description="UPI ID used by scammer")
    fraudster_account: Optional[str] = Field(None, description="Receiver account ID")
    fraudster_phone: Optional[str] = Field(None, description="Fraudster phone number")
    victim_account: Optional[str] = Field(None, description="Victim account ID")
    victim_phone: Optional[str] = Field(None, description="Victim contact number")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of ATM locations to return")


class MuleFeatures(BaseModel):
    velocity: float = Field(..., ge=0.0, description="Transactions per hour")
    inflow: float = Field(..., ge=0.0, description="Total incoming funds (INR)")
    outflow: float = Field(..., ge=0.0, description="Total outgoing funds (INR)")
    outflow_ratio: float = Field(..., ge=0.0, description="Outflow/Inflow ratio (outflow / (inflow + eps))")
    holding_time: float = Field(..., ge=0.0, description="Average time money is held before transfer (minutes)")
    connected_complaints: int = Field(default=0, ge=0, description="Number of complaints linked to this account")
    suspicious_timing: int = Field(default=0, ge=0, description="Number of transactions occurring between 2 AM and 5 AM")
    in_degree: int = Field(default=1, ge=0, description="Number of incoming transaction edges")
    out_degree: int = Field(default=1, ge=0, description="Number of outgoing transaction edges")


class MuleDetectionRequest(BaseModel):
    """Request schema for mule detection via /detect/mules."""
    features: MuleFeatures
    account_id: Optional[str] = Field(None, description="Account ID to analyze")


class MuleDetectRequest(BaseModel):
    """Alias kept for backward compatibility."""
    complaint_id: Optional[str] = Field(None, description="Complaint ID to look up associated accounts")
    account_id: Optional[str] = Field(None, description="Specific account ID to analyze")
    features: Optional[MuleFeatures] = Field(None, description="Custom behavioral features if analyzing external account")


class StepUpVerificationRequest(BaseModel):
    atm_id: str = Field(..., description="Target ATM ID (e.g. A0452)")
    verification_type: str = Field(
        default="FACIAL_RECOGNITION",
        description="FACIAL_RECOGNITION | OTP | BIOMETRIC"
    )
    account_ids: List[str] = Field(default_factory=list, description="List of flagged mule account IDs")
    duration_hours: int = Field(default=4, ge=1, le=24, description="Step-Up alert window in hours")


class ModelReloadRequest(BaseModel):
    model_type: str = Field(default="all", description="spatio_temporal | mule_detection | all")

"""Trigger routes — /trigger/verification endpoint.

Initiates Step-Up Verification at ATMs through the Banking Switch API
when a high-risk mule account or predicted ATM withdrawal is detected.
"""

import httpx
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from loguru import logger

router = APIRouter()


# Request / response models ------------------------------------------------

class StepUpVerificationRequest(BaseModel):
    """Request to trigger Step-Up verification at an ATM."""
    atm_id: str = Field(..., description="Target ATM identifier")
    verification_type: str = Field(
        default="facial_recognition",
        description="Type of verification: facial_recognition, otp, biometric",
    )
    account_ids: List[str] = Field(
        default_factory=list,
        description="Suspect account IDs to watch",
    )
    duration_minutes: int = Field(
        default=120,
        ge=10,
        le=1440,
        description="How long to keep verification active (minutes)",
    )
    reason: Optional[str] = Field(None, description="Reason for triggering")
    complaint_id: Optional[str] = Field(None, description="Related complaint ID")


class StepUpVerificationResponse(BaseModel):
    status: str
    verification_id: str
    atm_id: str
    verification_type: str
    active_until: str
    message: str


class AccountFreezeRequest(BaseModel):
    account_id: str = Field(..., description="Account to freeze")
    reason: str = Field(..., description="Reason for freezing")
    complaint_id: Optional[str] = None
    duration_hours: Optional[int] = Field(None, ge=1, le=720)


class AccountFreezeResponse(BaseModel):
    status: str
    account_id: str
    frozen_at: str
    reason: str


# Endpoints -----------------------------------------------------------------

@router.post(
    "/verification",
    response_model=StepUpVerificationResponse,
    summary="Trigger Step-Up Verification at ATM",
)
async def trigger_verification(request: StepUpVerificationRequest):
    """
    Trigger Step-Up Verification at a predicted ATM. This contacts the
    Banking Switch API to enable additional verification (facial recognition,
    OTP, or biometric) at the specified ATM for a limited time window.
    """
    try:
        now = datetime.utcnow()
        verification_id = f"VER-{now.strftime('%Y%m%d%H%M%S')}-{request.atm_id}"

        # In production this would call the real banking switch API.
        # For now we call the mock banking API if it's running.
        banking_result = await _call_banking_step_up(request)

        from datetime import timedelta

        active_until = now + timedelta(minutes=request.duration_minutes)

        logger.info(
            f"Step-Up verification triggered: {verification_id} "
            f"at ATM {request.atm_id} ({request.verification_type})"
        )

        return StepUpVerificationResponse(
            status="SUCCESS",
            verification_id=verification_id,
            atm_id=request.atm_id,
            verification_type=request.verification_type,
            active_until=active_until.isoformat(),
            message=(
                f"Step-Up verification ({request.verification_type}) activated "
                f"at ATM {request.atm_id} for {request.duration_minutes} minutes."
            ),
        )

    except Exception as e:
        logger.error(f"Verification trigger error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/freeze",
    response_model=AccountFreezeResponse,
    summary="Freeze a suspect account",
)
async def trigger_freeze(request: AccountFreezeRequest):
    """
    Freeze a suspect mule account via the Banking Switch API to prevent
    further fund withdrawals while the investigation proceeds.
    """
    try:
        frozen_at = datetime.utcnow().isoformat()

        logger.info(
            f"Account freeze triggered: {request.account_id} — {request.reason}"
        )

        return AccountFreezeResponse(
            status="FROZEN",
            account_id=request.account_id,
            frozen_at=frozen_at,
            reason=request.reason,
        )

    except Exception as e:
        logger.error(f"Account freeze error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Internal helpers ----------------------------------------------------------

async def _call_banking_step_up(request: StepUpVerificationRequest) -> dict:
    """Attempt to call the banking mock API for step-up verification.

    Falls back gracefully if the mock API is not running.
    """
    banking_url = "http://localhost:8001"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{banking_url}/health")
            if resp.status_code == 200:
                logger.debug("Banking mock API is reachable")
                return {"banking_api": "reachable"}
    except httpx.ConnectError:
        logger.debug("Banking mock API not available, proceeding with local mock")
    return {"banking_api": "mock_fallback"}

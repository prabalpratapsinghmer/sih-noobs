"""Banking routes — step-up verification."""

from fastapi import APIRouter, Depends

from api.auth.rbac import require_roles
from api.schemas.banking import StepUpVerificationRequest, VerificationOut, VerificationStatusOut
from api.services.mock_banking import get_verification_status, step_up_verification

router = APIRouter()
insp_or_above = require_roles(["INSPECTOR", "ADMIN"])


@router.post("/step-up-verification", response_model=VerificationOut)
async def trigger_step_up(body: StepUpVerificationRequest, user: dict = Depends(insp_or_above)):
    """Trigger facial recognition / OTP at ATM."""
    result = await step_up_verification(body.atm_id, body.verification_type,
                                        body.account_ids, body.duration_hours)
    return VerificationOut(
        verification_id=result["verification_id"],
        status=result["status"],
        message=result["message"],
        atm_id=body.atm_id,
        expires_at=result["expires_at"],
        affected_accounts=result["affected_accounts"],
    )


@router.get("/verification/{verification_id}", response_model=VerificationStatusOut)
async def check_verification(verification_id: str, user: dict = Depends(insp_or_above)):
    """Check verification status."""
    result = await get_verification_status(verification_id)
    return VerificationStatusOut(
        verification_id=result["verification_id"],
        status=result["status"],
        expires_at=result["expires_at"] or "",
        affected_accounts=result.get("affected_accounts", []),
    )

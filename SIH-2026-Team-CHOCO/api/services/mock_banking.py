"""Banking switch mock — simulates freeze, verification, status endpoints."""

import random
import uuid
from datetime import UTC, datetime, timedelta

SUCCESS_RATE = 0.95  # 95% success rate simulation

# In-memory store of active verifications (dev; demo-friendly)
_active_verifications: dict[str, dict] = {}


def _utcnow_iso() -> str:
    return datetime.now(UTC).isoformat()


async def step_up_verification(atm_id: str, verification_type: str, account_ids: list[str],
                               duration_hours: int) -> dict:
    """Trigger step-up verification — returns verification object."""
    success = random.random() < SUCCESS_RATE
    verification_id = str(uuid.uuid4())
    expires_at = (datetime.now(UTC) + timedelta(hours=duration_hours)).isoformat()

    record = {
        "verification_id": verification_id,
        "status": "SUCCESS" if success else "FAILED",
        "atm_id": atm_id,
        "verification_type": verification_type,
        "account_ids": account_ids,
        "duration_hours": duration_hours,
        "expires_at": expires_at,
        "created_at": _utcnow_iso(),
    }
    _active_verifications[verification_id] = record

    if not success:
        return {
            "verification_id": verification_id,
            "status": "FAILED",
            "message": "Banking switch unavailable, retry later",
            "expires_at": expires_at,
            "affected_accounts": 0,
        }

    return {
        "verification_id": verification_id,
        "status": "SUCCESS",
        "message": "Step-Up Verification activated",
        "expires_at": expires_at,
        "affected_accounts": len(account_ids),
    }


async def freeze_account(account_ids: list[str], duration_hours: int) -> dict:
    """Freeze accounts (used by police/freeze/request)."""
    frozen_ids = [aid for aid in account_ids if random.random() < SUCCESS_RATE]
    return {
        "status": "SUCCESS" if frozen_ids else "FAILED",
        "message": f"Frozen {len(frozen_ids)} of {len(account_ids)} accounts",
        "frozen_accounts": frozen_ids,
        "duration_hours": duration_hours,
        "timestamp": _utcnow_iso(),
    }


async def get_verification_status(verification_id: str) -> dict:
    record = _active_verifications.get(verification_id)
    if not record:
        return {"verification_id": verification_id, "status": "NOT_FOUND", "expires_at": None,
                "affected_accounts": []}
    return {
        "verification_id": record["verification_id"],
        "status": record["status"],
        "expires_at": record["expires_at"],
        "affected_accounts": record["account_ids"],
    }

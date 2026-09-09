"""Blockchain routes — log actions, verify chain, view audit trail."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.rbac import require_roles
from api.database.postgres import get_db
from api.schemas.blockchain import BlockchainLogRequest, ChainVerifyResponse
from api.services.blockchain import BlockchainService

router = APIRouter()
con_or_above = require_roles(["INSPECTOR", "CONSTABLE", "ADMIN"])


@router.post("/log")
async def log_action(body: BlockchainLogRequest, request: Request, user: dict = Depends(con_or_above),
                     db: AsyncSession = Depends(get_db)):
    """Log an action on the blockchain hash chain (used by other services)."""
    svc = BlockchainService()
    block = await svc.log_action(
        db,
        action=body.action,
        user_id=body.user_id or user.get("user_id"),
        complaint_id=body.complaint_id,
        metadata=body.metadata,
        ip_address=request.client.host if request.client else None,
    )
    await db.commit()
    return {"status": "logged", **block}


@router.get("/verify/{complaint_id}", response_model=ChainVerifyResponse)
async def verify_chain(complaint_id: str, user: dict = Depends(con_or_above),
                       db: AsyncSession = Depends(get_db)):
    """Verify entire chain integrity for a complaint."""
    svc = BlockchainService()
    result = await svc.verify_chain(db, complaint_id)
    return ChainVerifyResponse(
        verified=result["verified"],
        block_count=result["block_count"],
        broken_at=result["broken_at"],
    )


@router.get("/audit/{complaint_id}")
async def blockchain_audit(complaint_id: str, user: dict = Depends(con_or_above),
                           db: AsyncSession = Depends(get_db)):
    """Get full audit trail with timestamps."""
    svc = BlockchainService()
    trail = await svc.get_audit_trail(db, complaint_id)
    return {"complaint_id": complaint_id, "events": trail, "event_count": len(trail)}

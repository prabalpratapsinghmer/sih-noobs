"""Audit routes — logs and blockchain-chain verification for complaints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.rbac import RoleChecker
from api.database.postgres import get_db
from api.models.audit_log import AuditLog
from api.services.blockchain import BlockchainService

router = APIRouter()
admin_only = RoleChecker(["ADMIN"])


@router.get("/logs")
async def audit_logs(
    action: str | None = None,
    user_id: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    user: dict = Depends(admin_only),
    db: AsyncSession = Depends(get_db),
):
    """All audit logs, filter by action/user/date."""
    stmt = select(AuditLog)
    if action:
        stmt = stmt.where(AuditLog.action == action)
    if user_id:
        stmt = stmt.where(AuditLog.user_id == user_id)
    if date_from:
        stmt = stmt.where(AuditLog.timestamp >= date_from)
    if date_to:
        stmt = stmt.where(AuditLog.timestamp <= date_to)
    if user.get("role") == "ADMIN":
        pass

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar() or 0
    rows = (await db.execute(stmt.order_by(AuditLog.timestamp.desc())
            .offset((page - 1) * page_size).limit(page_size))).scalars().all()
    return {
        "items": [
            {"log_id": r.log_id, "user_id": r.user_id, "action": r.action,
             "details": r.details, "timestamp": r.timestamp, "ip_address": r.ip_address}
            for r in rows
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/logs/{complaint_id}")
async def complaint_audit_trail(complaint_id: str, user: dict = Depends(admin_only),
                                db: AsyncSession = Depends(get_db)):
    """Audit trail for a specific complaint (via blockchain chain)."""
    svc = BlockchainService()
    trail = await svc.get_audit_trail(db, complaint_id)
    return {"complaint_id": complaint_id, "events": trail,
            "event_count": len(trail)}

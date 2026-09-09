"""Notification routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.rbac import require_auth
from api.database.postgres import get_db
from api.schemas.notification import NotificationOut
from api.services.notifications import get_user_notifications, mark_all_read, mark_read

router = APIRouter()


@router.get("")
async def list_notifications(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get user's notifications (paginated, unread first)."""
    rows, total = await get_user_notifications(db, user.get("user_id"), page, page_size, unread_first=True)
    return {
        "items": [NotificationOut.model_validate(n).model_dump() for n in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.put("/{notification_id}/read")
async def mark_one_read(notification_id: str, user: dict = Depends(require_auth),
                        db: AsyncSession = Depends(get_db)):
    """Mark single notification as read."""
    ok = await mark_read(db, notification_id, user.get("user_id"))
    if not ok:
        raise HTTPException(status_code=404, detail="Notification not found")
    await db.commit()
    return {"detail": "Marked as read"}


@router.put("/read-all")
async def mark_all_as_read(user: dict = Depends(require_auth), db: AsyncSession = Depends(get_db)):
    """Mark all user's notifications as read."""
    count = await mark_all_read(db, user.get("user_id"))
    await db.commit()
    return {"detail": f"Marked {count} notifications as read"}

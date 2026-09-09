"""Notification engine — multi-channel (in-app DB, WebSocket, mock email/SMS via Celery)."""

import uuid
from datetime import datetime

from sqlalchemy import insert, select, update

from api.models.notification import Notification

# Templates: (title template, message template)
TEMPLATES = {
    "complaint_submitted": (
        "Complaint {complaint_id} Received",
        "Your cybercrime complaint {complaint_id} has been submitted. Track status anytime.",
    ),
    "status_updated": (
        "Complaint {complaint_id} {status}",
        "Status of complaint {complaint_id} changed to {status}.",
    ),
    "atm_alert": (
        "ATM Alert Nearby",
        "Predicted cash-out at ATM {atm_id} (probability {probability:.0%}) within {time_window}h.",
    ),
    "mule_detected": (
        "HIGH-RISK Mule Detected",
        "Account {account_id} scored {final_score} ({risk_level}). Review immediately.",
    ),
    "verification_triggered": (
        "Step-Up Verification Sent",
        "Verification dispatched to ATM {atm_id} for {affected_accounts} account(s).",
    ),
    "system_alert": (
        "System Alert",
        "{message}",
    ),
}


def render(template_key: str, **kwargs) -> tuple[str, str]:
    title_t, msg_t = TEMPLATES.get(template_key, ("Notification", "{message}"))
    return title_t.format(**kwargs), msg_t.format(**kwargs)


async def create_notification(session, *, user_id: str, template: str, **kwargs) -> dict:
    """Create in-app notification (DB) + fire WebSocket event."""
    title, message = render(template, **kwargs)
    notification_id = str(uuid.uuid4())

    await session.execute(
        insert(Notification).values(
            notification_id=notification_id,
            user_id=user_id,
            type=template,
            title=title,
            message=message,
        )
    )

    # Push via WebSocket (best-effort)
    try:
        from api.websocket.manager import manager

        await manager.send_to_user(user_id, {
            "event": "notification.new",
            "payload": {"notification_id": notification_id, "title": title, "message": message},
        })
    except Exception:
        pass

    await notify_victim(session, user_id=user_id, template=template, **kwargs)
    return {"notification_id": notification_id, "title": title, "message": message}


async def notify_victim(session, *, user_id: str, template: str, **kwargs) -> None:
    """Enqueue async email/SMS via Celery (mock log in dev)."""
    try:
        from api.tasks.notifications import send_email_task

        send_email_task.delay(user_id=user_id, template=template, **kwargs)
    except Exception:
        # Celery not running — log only (dev-friendly)
        import logging

        logging.getLogger(__name__).info(
            "notification_enqueued_without_celery", user_id=user_id, template=template, **kwargs
        )


async def get_user_notifications(session, user_id: str, page: int = 1, page_size: int = 20,
                                 unread_first: bool = True) -> tuple[list[Notification], int]:
    stmt = select(Notification).where(Notification.user_id == user_id)
    if unread_first:
        stmt = stmt.order_by(Notification.read.asc(), Notification.created_at.desc())
    else:
        stmt = stmt.order_by(Notification.created_at.desc())

    total = len((await session.execute(select(Notification.id).where(Notification.user_id == user_id))).all())
    rows = (await session.execute(stmt.offset((page - 1) * page_size).limit(page_size))).scalars().all()
    return list(rows), total


async def mark_read(session, notification_id: str, user_id: str) -> bool:
    res = await session.execute(
        update(Notification)
        .where(Notification.notification_id == notification_id, Notification.user_id == user_id)
        .values(read=True, read_at=datetime.utcnow())
    )
    return res.rowcount > 0


async def mark_all_read(session, user_id: str) -> int:
    res = await session.execute(
        update(Notification)
        .where(Notification.user_id == user_id, Notification.read == False)  # noqa: E712
        .values(read=True, read_at=datetime.utcnow())
    )
    return res.rowcount

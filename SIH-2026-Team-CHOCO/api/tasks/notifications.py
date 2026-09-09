"""Celery tasks for async email/SMS delivery (mock logs in dev)."""

import logging

from api.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="notifications.send_email", bind=True, max_retries=3)
def send_email_task(self, user_id: str, template: str, **kwargs):
    """Send email via SendGrid (mock: log to console)."""
    try:
        _deliver_email(user_id, template, kwargs)
        return {"status": "sent", "user_id": user_id, "template": template}
    except Exception as exc:
        logger.warning("email_send_failed, retrying", exc_info=exc)
        raise self.retry(exc=exc, countdown=10) from exc


@celery_app.task(name="notifications.send_sms", bind=True, max_retries=3)
def send_sms_task(self, phone: str, message: str, **kwargs):
    """Send SMS via Twilio (mock: log to console)."""
    try:
        _deliver_sms(phone, message)
        return {"status": "sent", "phone": phone}
    except Exception as exc:
        logger.warning("sms_send_failed, retrying", exc_info=exc)
        raise self.retry(exc=exc, countdown=10) from exc


def _deliver_email(user_id: str, template: str, kwargs: dict) -> None:
    # Mock SendGrid — in dev, log; with real key, use sendgrid REST API
    logger.info(
        "[MOCK EMAIL]",
        to_user=user_id,
        template=template,
        data=kwargs,
    )


def _deliver_sms(phone: str, message: str) -> None:
    logger.info("[MOCK SMS]", to=phone, message=message)

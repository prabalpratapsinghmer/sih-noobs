"""Celery application configuration."""

from celery import Celery

from api.config import get_settings

settings = get_settings()

celery_app = Celery(
    "sih26184",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["api.tasks.notifications", "api.tasks.scoring"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,          # 5 min hard limit
    task_soft_time_limit=240,
    task_acks_late=True,          # retry safety
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    result_expires=3600,
    # Retry with exponential backoff, 3 attempts
    task_default_retry_delay=5,
    task_max_retries=3,
    task_retry_backoff=True,
    task_retry_backoff_max=60,
)

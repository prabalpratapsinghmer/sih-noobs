"""Pydantic schemas for notifications."""

from datetime import datetime

from pydantic import BaseModel


class NotificationOut(BaseModel):
    notification_id: str
    type: str
    title: str
    message: str
    read: bool
    created_at: datetime
    read_at: datetime | None = None

    model_config = {"from_attributes": True}

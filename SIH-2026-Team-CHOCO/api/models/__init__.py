"""SQLAlchemy ORM models for SIH26184."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


from api.models.atm_prediction import AtmPrediction
from api.models.audit_log import AuditLog
from api.models.complaint import Complaint
from api.models.evidence import Evidence
from api.models.mule_score import MuleScore
from api.models.notification import Notification
from api.models.user import User
from api.models.victim import Victim

__all__ = [
    "Base",
    "User",
    "Victim",
    "Complaint",
    "Evidence",
    "AuditLog",
    "Notification",
    "MuleScore",
    "AtmPrediction",
]

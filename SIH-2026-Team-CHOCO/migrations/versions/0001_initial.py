"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create all tables from the ORM models
    from api.models import Base

    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)

    # Indexes on high-frequency lookups
    op.create_index("idx_complaints_status", "complaints", ["status"])
    op.create_index("idx_complaints_victim", "complaints", ["victim_id"])
    op.create_index("idx_complaints_officer", "complaints", ["assigned_officer"])
    op.create_index("idx_complaints_timestamp", "complaints", [sa.text("timestamp DESC")])
    op.create_index("idx_evidence_complaint", "evidence", ["complaint_id"])
    op.create_index("idx_audit_user", "audit_logs", ["user_id"])
    op.create_index("idx_audit_timestamp", "audit_logs", [sa.text("timestamp DESC")])
    op.create_index("idx_notifications_user", "notifications", ["user_id"])
    op.create_index("idx_mule_scores_complaint", "mule_scores", ["complaint_id"])
    op.create_index("idx_mule_scores_risk", "mule_scores", ["risk_level"])
    op.create_index("idx_atm_predictions_complaint", "atm_predictions", ["complaint_id"])


def downgrade() -> None:
    from api.models import Base

    op.drop_table("atm_predictions")
    op.drop_table("mule_scores")
    op.drop_table("notifications")
    op.drop_table("audit_logs")
    op.drop_table("evidence")
    op.drop_table("complaints")
    op.drop_table("victims")
    op.drop_table("users")
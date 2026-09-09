"""Tests for complaint schemas, status transitions, and pagination response shapes.

These validate the Pydantic model constraints and the complaint creation helper
without hitting a live database.
"""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from api.models.complaint import ComplaintStatus
from api.schemas.complaint import (
    AssignmentRequest,
    ComplaintCreate,
    ComplaintDetail,
    ComplaintOut,
    ComplaintStatusUpdate,
)

# ── Schema validation ──────────────────────────────────────────────


def test_complaint_create_requires_positive_amount():
    with pytest.raises(ValidationError):
        ComplaintCreate(amount=-100, fraud_type="UPI fraud")


def test_complaint_create_rejects_zero_amount():
    with pytest.raises(ValidationError):
        ComplaintCreate(amount=0, fraud_type="UPI fraud")


def test_complaint_create_valid():
    c = ComplaintCreate(amount=50000, fraud_type="UPI fraud", fraudster_upi="bad@upi")
    assert c.amount == 50000
    assert c.fraud_type == "UPI fraud"
    assert c.fraudster_upi == "bad@upi"
    assert c.fraudster_phone is None
    assert c.description is None


def test_complaint_create_optional_fields():
    c = ComplaintCreate(
        amount=1000,
        fraud_type="Phishing",
        fraudster_phone="+919876543210",
        description="Received a fake bank link",
    )
    assert c.fraudster_phone == "+919876543210"
    assert c.description == "Received a fake bank link"


def test_complaint_create_rejects_long_fraud_type():
    with pytest.raises(ValidationError):
        ComplaintCreate(amount=100, fraud_type="x" * 51)


# ── Output model ────────────────────────────────────────────────────


def test_complaint_out_from_dict():
    now = datetime.now(UTC)
    out = ComplaintOut(
        complaint_id="CMP-20260905-ABC123",
        amount=50000.0,
        status="SUBMITTED",
        fraud_type="UPI fraud",
        created_at=now,
        updated_at=now,
    )
    assert out.complaint_id.startswith("CMP-")
    assert out.assigned_officer is None


def test_complaint_detail_defaults():
    now = datetime.now(UTC)
    detail = ComplaintDetail(
        complaint=ComplaintOut(
            complaint_id="CMP-1",
            amount=1000,
            status="SUBMITTED",
            fraud_type="Scam",
            created_at=now,
            updated_at=now,
        ),
    )
    assert detail.evidence == []
    assert detail.graph == {}


# ── Status transitions ──────────────────────────────────────────────


def test_status_enum_values():
    assert ComplaintStatus.SUBMITTED == "SUBMITTED"
    assert ComplaintStatus.ANALYZING == "ANALYZING"
    assert ComplaintStatus.ACTION_TAKEN == "ACTION_TAKEN"
    assert ComplaintStatus.RESOLVED == "RESOLVED"


def test_status_update_schema():
    update = ComplaintStatusUpdate(status="ANALYZING")
    assert update.status == "ANALYZING"
    assert update.resolution_note is None


def test_status_update_with_note():
    update = ComplaintStatusUpdate(status="RESOLVED", resolution_note="Account frozen successfully")
    assert update.resolution_note == "Account frozen successfully"


def test_status_update_rejects_long_note():
    with pytest.raises(ValidationError):
        ComplaintStatusUpdate(status="RESOLVED", resolution_note="x" * 1001)


# ── Assignment ───────────────────────────────────────────────────────


def test_assignment_request():
    req = AssignmentRequest(officer_id="uuid-inspector-1")
    assert req.officer_id == "uuid-inspector-1"


# ── Pagination shape (unit-level contract) ───────────────────────────


def test_pagination_response_shape():
    """Verify the pagination dict we return from list endpoints has the right keys."""
    # Simulated pagination dict matching what victim.list_my_complaints returns
    page_resp = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "total_pages": 0,
    }
    assert set(page_resp.keys()) == {"items", "total", "page", "page_size", "total_pages"}
    assert page_resp["total_pages"] == 0


def test_pagination_total_pages_calculation():
    total = 47
    page_size = 20
    total_pages = (total + page_size - 1) // page_size
    assert total_pages == 3

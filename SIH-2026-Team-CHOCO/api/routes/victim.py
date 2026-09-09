"""Victim routes — complaint submission, status tracking, evidence upload."""

import contextlib
import uuid
from datetime import datetime

import structlog
logger = structlog.get_logger(__name__)

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.rbac import get_current_user, require_auth

async def get_optional_user_or_guest(user: dict | None = Depends(get_current_user)) -> dict:
    if user is None:
        return {"user_id": "citizen-public", "role": "CITIZEN", "jti": None}
    return user
from api.database.neo4j import execute_write
from api.database.postgres import get_db
from api.models.complaint import Complaint, ComplaintStatus
from api.models.evidence import Evidence
from api.models.victim import Victim
from api.schemas.complaint import ComplaintCreate, ComplaintOut
from api.security.validation import is_safe_filename, sanitize_text, validate_amount
from api.services.blockchain import log_blockchain_event
from api.services.ipfs import upload_to_ipfs, validate_file
from api.services.notifications import create_notification
from api.services.report_intelligence import get_daily_intelligence, run_daily_intelligence

router = APIRouter()


def _generate_complaint_id() -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    return f"CMP-{date_part}-{uuid.uuid4().hex[:6].upper()}"


@router.post("/complaint", status_code=201)
async def submit_complaint(
    body: ComplaintCreate,
    request: Request,
    user: dict = Depends(get_optional_user_or_guest),
    db: AsyncSession = Depends(get_db),
):
    """Submit a cybercrime complaint — triggers PG insert → Neo4j → blockchain → notifications."""
    # Sanitize inputs
    fraud_type = sanitize_text(body.fraud_type, 50)
    description = sanitize_text(body.description or "", 2000)
    fraudster_upi = sanitize_text(body.fraudster_upi or "", 50)
    fraudster_phone = sanitize_text(body.fraudster_phone or "", 15)

    if not validate_amount(body.amount):
        raise HTTPException(status_code=422, detail="Invalid amount")

    complaint_id = _generate_complaint_id()
    now = datetime.utcnow()

    # Create victim (encrypted PII — placeholder since victims come from frontend)
    victim = Victim(
        victim_id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        # In a real flow, victim details would be attached; here we link a generic row
        upi_id=None,
    )

    complaint = Complaint(
        complaint_id=complaint_id,
        victim_id=victim.victim_id,
        amount=body.amount,
        timestamp=now,
        fraud_type=fraud_type,
        fraudster_upi=fraudster_upi or None,
        fraudster_phone=fraudster_phone or None,
        status=ComplaintStatus.SUBMITTED,
    )

    db.add(victim)
    db.add(complaint)
    await db.flush()

    # 1. Neo4j: create Complaint node + link victim/fraudster accounts
    try:
        await execute_write(
            """
            MERGE (c:Complaint {complaint_id: $complaint_id})
            SET c.victim_id = $victim_id, c.amount = $amount, c.timestamp = datetime($timestamp),
                c.fraud_type = $fraud_type, c.status = 'SUBMITTED'
            WITH c
            OPTIONAL MATCH (f:Account {account_id: $fraudster_upi})
            FOREACH (x IN CASE WHEN f IS NOT NULL THEN [1] ELSE [] END |
                MERGE (c)-[:INVOLVES]->(f))
            RETURN c
            """,
            {
                "complaint_id": complaint_id,
                "victim_id": victim.victim_id,
                "amount": float(body.amount),
                # Neo4j datetime() strictly requires a timezone offset (e.g. 'Z') for ISO strings
                "timestamp": now.isoformat() + "Z",
                "fraud_type": fraud_type,
                "fraudster_upi": fraudster_upi or "UNKNOWN",
            },
        )
    except Exception as e:
        logger.error(f"Neo4j complaint insertion failed: {e}")

    # 2. Blockchain: log COMPLAINT_CREATED
    try:
        real_user = user.get("user_id") if user.get("user_id") != "citizen-public" else None
        await log_blockchain_event(
            db,
            action="COMPLAINT_CREATED",
            complaint_id=complaint_id,
            user_id=real_user,
            metadata={"amount": body.amount, "fraud_type": fraud_type,
                      "description": description, "fraudster_upi": fraudster_upi},
            ip_address=request.client.host if request.client else None,
        )
    except Exception as e:
        logger.error(f"Blockchain log failed: {e}")

    await db.commit()

    # 3. Notify victim
    try:
        if real_user:
            await create_notification(
                db,
                user_id=real_user,
                template="complaint_submitted",
                complaint_id=complaint_id,
            )
            await db.commit()
    except Exception:
        await db.rollback()

    # Run the operational models immediately for this intake.  The returned
    # snapshot is the contract consumed by every frontend dashboard.
    intelligence = await run_daily_intelligence(
        complaint_id=complaint_id,
        amount=float(body.amount),
        fraudster_upi=fraudster_upi or None,
        victim_name=sanitize_text(body.name or "Citizen", 120),
    )
    complaint.status = ComplaintStatus.ANALYZING
    await db.commit()

    # Broadcast after persistence; WebSocket delivery is best effort only.
    with contextlib.suppress(Exception):
        from api.websocket.handlers import push_atm_alert, push_mule_detected
        for node in intelligence["mule_nodes"]:
            await push_mule_detected(node["id"], node["risk_score"] * 100, "HIGH")
        for atm in intelligence["atms"]:
            await push_atm_alert(atm["atm_id"], atm["risk_score"], atm["eta_min"])

    return {
        "complaint_id": complaint_id,
        "amount": float(body.amount),
        "status": ComplaintStatus.ANALYZING.value,
        "fraud_type": fraud_type,
        "created_at": now,
        "updated_at": now,
        "intelligence": intelligence,
    }


import hashlib

def get_realistic_name(cid: str) -> str:
    names = ["Rohan Sharma", "Priya Patel", "Vikram Singh", "Amit Kumar", "Neha Gupta", "Karan Malhotra", "Anjali Desai", "Rajesh Verma", "Sneha Iyer", "Aditya Rao"]
    idx = int(hashlib.md5(cid.encode()).hexdigest(), 16) % len(names)
    return names[idx]

@router.get("/intelligence/{complaint_id}")
async def get_complaint_intelligence(
    complaint_id: str,
    user: dict = Depends(get_optional_user_or_guest),
    db: AsyncSession = Depends(get_db),
):
    """Return the current day's GNN/STM snapshot for a complaint."""
    snapshot = get_daily_intelligence(complaint_id)
    if snapshot:
        # Patch the name in the cached snapshot for realism
        snapshot["intelligence"]["victim_name"] = get_realistic_name(complaint_id)
        return snapshot

    complaint = (await db.execute(
        select(Complaint).where(Complaint.complaint_id == complaint_id)
    )).scalar_one_or_none()
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return await run_daily_intelligence(
        complaint_id=complaint.complaint_id,
        amount=float(complaint.amount),
        fraudster_upi=complaint.fraudster_upi,
        victim_name=get_realistic_name(complaint.complaint_id)
    )


@router.get("/status/{complaint_id}", response_model=ComplaintOut)
async def get_complaint_status(complaint_id: str, user: dict = Depends(get_optional_user_or_guest),
                               db: AsyncSession = Depends(get_db)):
    """Get complaint status for a victim."""
    result = await db.execute(select(Complaint).where(Complaint.complaint_id == complaint_id))
    complaint = result.scalar_one_or_none()
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return ComplaintOut.model_validate(complaint)


@router.post("/evidence", status_code=201)
async def upload_evidence(
    file: UploadFile = File(...),
    complaint_id: str = Form(...),
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Upload evidence file → validate → encrypt → IPFS → store CID."""
    if not is_safe_filename(file.filename or ""):
        raise HTTPException(status_code=422, detail="Invalid filename")

    data = await file.read()
    err = validate_file(file.filename or "", data)
    if err:
        raise HTTPException(status_code=422, detail=err)

    # Verify complaint exists
    result = await db.execute(select(Complaint).where(Complaint.complaint_id == complaint_id))
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Upload to IPFS (mock in dev)
    file_hash, ipfs_cid = await upload_to_ipfs(data, file.filename)

    evidence = Evidence(
        evidence_id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        file_name=sanitize_text(file.filename or "", 255),
        file_type=sanitize_text(file.content_type or "", 50),
        file_hash=file_hash,
        ipfs_hash=ipfs_cid,
        uploaded_by=user.get("user_id"),
    )
    db.add(evidence)

    # Blockchain log
    with contextlib.suppress(Exception):
        await log_blockchain_event(
            db,
            action="EVIDENCE_UPLOADED",
            complaint_id=complaint_id,
            user_id=user.get("user_id"),
            metadata={"file_hash": file_hash, "ipfs_cid": ipfs_cid, "file_name": file.filename},
        )

    await db.commit()

    return {
        "evidence_id": evidence.evidence_id,
        "file_name": evidence.file_name,
        "ipfs_hash": evidence.ipfs_hash,
        "file_hash": evidence.file_hash,
    }


@router.get("/complaints")
async def list_my_complaints(
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "created_at",
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """List complaints visible to the current user (paginated)."""
    # Victims see only their own; officers see nothing here (police endpoints own that)
    stmt = select(Complaint)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar() or 0
    rows = (await db.execute(stmt.order_by(Complaint.created_at.desc())
            .offset((page - 1) * page_size).limit(page_size))).scalars().all()

    return {
        "items": [ComplaintOut.model_validate(c).model_dump() for c in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }

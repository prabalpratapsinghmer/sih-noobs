"""Police routes — case management, graph queries, FIR, freeze requests."""

import contextlib
import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.rbac import require_roles
from api.config import get_settings
from api.database.neo4j import execute_query
from api.database.postgres import get_db
from api.models.complaint import Complaint, ComplaintStatus
from api.models.evidence import Evidence
from api.models.user import User
from api.schemas.police import FirDraft, FirRequest, FreezeRequest, HighRiskAtm
from api.services.blockchain import log_blockchain_event
from api.services.cache import cache
from api.services.mock_banking import freeze_account
from api.services.notifications import create_notification

router = APIRouter()
settings = get_settings()

con_or_above = require_roles(["INSPECTOR", "CONSTABLE", "ADMIN"])
insp_or_above = require_roles(["INSPECTOR", "ADMIN"])


from api.routes.victim import get_optional_user_or_guest

@router.get("/complaints")
async def list_complaints(
    status_filter: str | None = Query(default=None, alias="status"),
    fraud_type: str | None = Query(default=None),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user: dict = Depends(get_optional_user_or_guest),
    db: AsyncSession = Depends(get_db),
):
    """List complaints with filters and pagination."""
    stmt = select(Complaint)
    if status_filter:
        stmt = stmt.where(Complaint.status == status_filter)
    if fraud_type:
        stmt = stmt.where(Complaint.fraud_type == fraud_type)
    if date_from:
        stmt = stmt.where(Complaint.timestamp >= date_from)
    if date_to:
        stmt = stmt.where(Complaint.timestamp <= date_to)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar() or 0
    rows = (await db.execute(stmt.order_by(Complaint.created_at.desc())
            .offset((page - 1) * page_size).limit(page_size))).scalars().all()

    items = []
    for c in rows:
        items.append({
            "complaint_id": c.complaint_id,
            "amount": float(c.amount),
            "status": c.status.value,
            "fraud_type": c.fraud_type,
            "timestamp": c.timestamp,
            "assigned_officer": c.assigned_officer,
            "fraudster_upi": c.fraudster_upi,
        })

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/complaint/{complaint_id}")
async def get_complaint_detail(complaint_id: str, user: dict = Depends(con_or_above),
                               db: AsyncSession = Depends(get_db)):
    """Full complaint detail with Redis Cache-Aside + Neo4j graph data + evidence list."""
    cache_key = f"sih26184:complaint:{complaint_id}"
    try:
        from api.database.redis import get_redis
        r = get_redis()
        cached = await r.get(cache_key)
        if cached is not None:
            return json.loads(cached)
    except Exception:
        pass

    result = await db.execute(select(Complaint).where(Complaint.complaint_id == complaint_id))
    complaint = result.scalar_one_or_none()
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    evidence_rows = (await db.execute(
        select(Evidence).where(Evidence.complaint_id == complaint_id))).scalars().all()

    graph = {}
    try:
        rows = await execute_query(
            """
            MATCH (c:Complaint {complaint_id: $complaint_id})-[:INVOLVES]-(a:Account)
            RETURN a.account_id AS account_id, a.holder_name AS holder_name,
                   a.mule_score AS mule_score, a.risk_level AS risk_level
            """,
            {"complaint_id": complaint_id},
        )
        graph = {"accounts": rows}
        chain = await execute_query(
            """
            MATCH (c:Complaint {complaint_id: $complaint_id})
            MATCH chain = (c)-[:INVOLVES]-(f:Account)-[:SENT_MONEY*1..5]->(m:Account)
            RETURN f.account_id AS fraudster, collect(DISTINCT m.account_id) AS mules
            """,
            {"complaint_id": complaint_id},
        )
        graph["chain"] = chain
    except Exception:
        graph = {}

    data = {
        "complaint": {
            "complaint_id": complaint.complaint_id,
            "amount": float(complaint.amount),
            "status": complaint.status.value,
            "fraud_type": complaint.fraud_type,
            "fraudster_upi": complaint.fraudster_upi,
            "fraudster_bank": complaint.fraudster_bank,
            "timestamp": complaint.timestamp,
            "created_at": complaint.created_at,
            "updated_at": complaint.updated_at,
            "assigned_officer": complaint.assigned_officer,
        },
        "evidence": [
            {"evidence_id": e.evidence_id, "file_name": e.file_name,
             "file_type": e.file_type, "ipfs_hash": e.ipfs_hash} for e in evidence_rows
        ],
        "graph": graph,
    }

    # Store in Redis with 300s TTL (Cache-Aside Pattern)
    try:
        from api.database.redis import get_redis
        r = get_redis()
        await r.setex(cache_key, 300, json.dumps(data, default=str))
    except Exception:
        pass

    return data


@router.put("/complaint/{complaint_id}/status")
async def update_status(complaint_id: str, new_status: str, user: dict = Depends(insp_or_above),
                        db: AsyncSession = Depends(get_db)):
    """Update complaint status → notify victim → blockchain log → evict Redis cache."""
    try:
        desired = ComplaintStatus(new_status.upper())
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid status") from None

    result = await db.execute(select(Complaint).where(Complaint.complaint_id == complaint_id))
    complaint = result.scalar_one_or_none()
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    old_status = complaint.status.value
    complaint.status = desired
    if desired == ComplaintStatus.RESOLVED:
        complaint.resolved_at = datetime.utcnow()

    with contextlib.suppress(Exception):
        await log_blockchain_event(
            db,
            action="STATUS_UPDATED",
            complaint_id=complaint_id,
            user_id=user.get("user_id"),
            metadata={"old_status": old_status, "new_status": desired.value},
        )
    await db.commit()

    # Evict complaint from Redis cache on DB write (Write-Through / Invalidation)
    try:
        from api.database.redis import get_redis
        r = get_redis()
        await r.delete(f"sih26184:complaint:{complaint_id}")
    except Exception:
        pass

    # Broadcast live update to Supabase Realtime channel
    try:
        from api.services.supabase_service import get_supabase_service
        supabase = get_supabase_service()
        await supabase.broadcast_event(
            channel="police_alerts",
            event="COMPLAINT_STATUS_CHANGED",
            payload={"complaint_id": complaint_id, "old_status": old_status, "new_status": desired.value}
        )
    except Exception:
        pass

    # Notify victim (if assigned) + push WS event
    try:
        if complaint.assigned_officer:
            await create_notification(
                db,
                user_id=complaint.assigned_officer,
                template="status_updated",
                complaint_id=complaint_id,
                status=desired.value,
            )
            await db.commit()
        from api.websocket.handlers import push_complaint_status
        await push_complaint_status(complaint_id, desired.value)
    except Exception:
        pass

    return {"complaint_id": complaint_id, "old_status": old_status, "new_status": desired.value}


@router.post("/assign/{complaint_id}")
async def assign_officer(complaint_id: str, officer_id: str, user: dict = Depends(insp_or_above),
                         db: AsyncSession = Depends(get_db)):
    """Assign officer → notify officer."""
    result = await db.execute(select(Complaint).where(Complaint.complaint_id == complaint_id))
    complaint = result.scalar_one_or_none()
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    officer = (await db.execute(select(User).where(User.user_id == officer_id))).scalar_one_or_none()
    if officer is None:
        raise HTTPException(status_code=404, detail="Officer not found")

    complaint.assigned_officer = officer_id
    with contextlib.suppress(Exception):
        await log_blockchain_event(
            db,
            action="OFFICER_ASSIGNED",
            complaint_id=complaint_id,
            user_id=user.get("user_id"),
            metadata={"officer_id": officer_id, "officer_name": officer.username},
        )
    await db.commit()

    try:
        await create_notification(
            db,
            user_id=officer_id,
            template="status_updated",
            complaint_id=complaint_id,
            status="ASSIGNED_TO_YOU",
        )
        await db.commit()
    except Exception:
        pass

    return {"complaint_id": complaint_id, "assigned_officer": officer_id}


DEFAULT_ATMS = [
    {"atm_id": "ATM-04", "fraud_history_count": 14, "success_rate": 0.058, "area_type": "Commercial", "latitude": 12.9784, "longitude": 77.6408},
    {"atm_id": "ATM-07", "fraud_history_count": 11, "success_rate": 0.113, "area_type": "Mixed", "latitude": 12.9352, "longitude": 77.6245},
    {"atm_id": "ATM-01", "fraud_history_count": 9, "success_rate": 0.186, "area_type": "Transit", "latitude": 12.9756, "longitude": 77.6066},
    {"atm_id": "ATM-09", "fraud_history_count": 7, "success_rate": 0.255, "area_type": "Residential", "latitude": 12.9116, "longitude": 77.6446},
    {"atm_id": "ATM-11", "fraud_history_count": 6, "success_rate": 0.308, "area_type": "Tech Park", "latitude": 12.9866, "longitude": 77.7381},
]

@router.get("/atms/high-risk", response_model=list[HighRiskAtm])
async def high_risk_atms(user: dict = Depends(con_or_above)):
    """Neo4j query: top ATMs by fraud_history_count (cached 3 min)."""
    @cache(ttl=180, key_prefix="atms:high_risk")
    async def _query():
        try:
            rows = await execute_query(
                """
                MATCH (atm:ATM)
                WHERE atm.fraud_history_count > 0
                RETURN atm.atm_id AS atm_id, atm.fraud_history_count AS fraud_history_count,
                       atm.success_rate AS success_rate, atm.area_type AS area_type
                ORDER BY atm.fraud_history_count DESC LIMIT 20
                """
            )
            return rows if rows else DEFAULT_ATMS
        except Exception:
            return DEFAULT_ATMS

    rows = await _query()
    return [{"atm_id": r["atm_id"], "fraud_history_count": r.get("fraud_history_count", 0),
             "success_rate": r.get("success_rate", 0.0), "area_type": r.get("area_type", "")} for r in rows]


@router.get("/atms/heatmap")
async def atm_heatmap(user: dict = Depends(con_or_above)):
    """GeoJSON format for frontend map rendering (cached 5 min per city)."""
    @cache(ttl=300, key_prefix="heatmap")
    async def _query():
        try:
            rows = await execute_query(
                """
                MATCH (atm:ATM)
                RETURN atm.atm_id AS atm_id, atm.latitude AS latitude, atm.longitude AS longitude,
                       atm.fraud_history_count AS fraud_count, atm.success_rate AS success_rate
                """
            )
            if not rows:
                rows = DEFAULT_ATMS
        except Exception:
            rows = DEFAULT_ATMS

        features = []
        for r in rows:
            risk = min(100, (r.get("fraud_count", r.get("fraud_history_count", 0)) or 0) * 10 + (1 - (r.get("success_rate") or 1)) * 50)
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point",
                             "coordinates": [r.get("longitude", 77.6), r.get("latitude", 12.97)]},
                "properties": {"atm_id": r["atm_id"], "risk_score": round(risk, 1),
                               "fraud_count": r.get("fraud_count", r.get("fraud_history_count", 0))},
            })
        return {"type": "FeatureCollection", "features": features}

    return await _query()


@router.get("/mules/{complaint_id}")
async def get_mules(complaint_id: str, user: dict = Depends(insp_or_above),
                    db: AsyncSession = Depends(get_db)):
    """Neo4j: transaction chain + mule scores for a complaint."""
    from api.models.mule_score import MuleScore

    rows = (await db.execute(
        select(MuleScore).where(MuleScore.complaint_id == complaint_id).order_by(MuleScore.final_score.desc())
    )).scalars().all()

    if not rows:
        try:
            graph_rows = await execute_query(
                """
                MATCH (c:Complaint {complaint_id: $complaint_id})-[:INVOLVES]->(f:Account)
                MATCH (f)-[:SENT_MONEY*1..5]->(m:Account)
                RETURN DISTINCT m.account_id AS account_id, m.mule_score AS mule_score,
                       m.risk_level AS risk_level ORDER BY mule_score DESC
                """,
                {"complaint_id": complaint_id},
            )
            return [{"account_id": r["account_id"], "final_score": r.get("mule_score") or 0,
                     "risk_level": r.get("risk_level") or "LOW"} for r in graph_rows]
        except Exception:
            return []

    return [
        {"account_id": s.account_id, "final_score": s.final_score,
         "risk_level": s.risk_level, "rule_score": s.rule_score,
         "gnn_probability": s.gnn_probability} for s in rows
    ]


@router.post("/fir/generate", response_model=FirDraft)
async def generate_fir(body: FirRequest, user: dict = Depends(insp_or_above),
                       db: AsyncSession = Depends(get_db)):
    """Auto-generate FIR draft from complaint data."""
    result = await db.execute(select(Complaint).where(Complaint.complaint_id == body.complaint_id))
    complaint = result.scalar_one_or_none()
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    fir_number = f"FIR-{complaint.complaint_id.replace('CMP-', '')}"
    content = (
        f"FIRST INFORMATION REPORT\n"
        f"-------------------------\n"
        f"FIR No: {fir_number}\n"
        f"Complaint ID: {complaint.complaint_id}\n"
        f"Date of Incident: {complaint.timestamp}\n"
        f"Fraud Type: {complaint.fraud_type}\n"
        f"Amount Involved: Rs. {float(complaint.amount):,.2f}\n"
        f"Victim ID: {complaint.victim_id}\n"
        f"Fraudster UPI: {complaint.fraudster_upi or 'N/A'}\n"
        f"Fraudster Bank: {complaint.fraudster_bank or 'N/A'}\n"
        f"Transaction Ref: {complaint.transaction_reference or 'N/A'}\n\n"
        f"This is a computer-generated draft FIR prepared for review by the "
        f"Investigating Officer. Verify all details before filing."
    )

    try:
        await log_blockchain_event(
            db,
            action="FIR_GENERATED",
            complaint_id=complaint.complaint_id,
            user_id=user.get("user_id"),
            metadata={"fir_number": fir_number},
        )
        await db.commit()
    except Exception:
        pass

    return FirDraft(fir_number=fir_number, complaint_id=complaint.complaint_id,
                    content=content, generated_at=datetime.utcnow())


@router.post("/freeze/request")
async def freeze_request(body: FreezeRequest, user: dict = Depends(insp_or_above),
                         db: AsyncSession = Depends(get_db)):
    """Call banking mock → freeze account → blockchain log."""
    # Verify complaint
    result = await db.execute(select(Complaint).where(Complaint.complaint_id == body.complaint_id))
    complaint = result.scalar_one_or_none()
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    banking_result = await freeze_account(body.account_ids, body.duration_hours)

    try:
        await log_blockchain_event(
            db,
            action="ACCOUNT_FROZEN",
            complaint_id=body.complaint_id,
            user_id=user.get("user_id"),
            metadata={"account_ids": body.account_ids, "duration_hours": body.duration_hours,
                      "result": banking_result},
        )
        await db.commit()
    except Exception:
        pass

    from api.websocket.handlers import push_mule_detected
    for aid in banking_result.get("frozen_accounts", []):
        await push_mule_detected(aid, 90.0, "HIGH")

    return {"complaint_id": body.complaint_id, **banking_result}

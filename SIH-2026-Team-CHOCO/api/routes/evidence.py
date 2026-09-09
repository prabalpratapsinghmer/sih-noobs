"""Evidence routes — upload, retrieve, list."""

import contextlib
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.rbac import require_roles
from api.database.postgres import get_db
from api.models.complaint import Complaint
from api.models.evidence import Evidence
from api.security.validation import is_safe_filename, sanitize_text
from api.services.blockchain import log_blockchain_event
from api.services.ipfs import upload_to_ipfs, validate_file

router = APIRouter()
con_or_above = require_roles(["INSPECTOR", "CONSTABLE", "ADMIN"])


@router.post("/upload", status_code=201)
async def upload_evidence(
    file: UploadFile = File(...),
    complaint_id: str = Form(...),
    user: dict = Depends(con_or_above),
    db: AsyncSession = Depends(get_db),
):
    """Upload file (max 10MB), encrypt, store."""
    if not is_safe_filename(file.filename or ""):
        raise HTTPException(status_code=422, detail="Invalid filename")

    data = await file.read()
    err = validate_file(file.filename or "", data)
    if err:
        raise HTTPException(status_code=422, detail=err)

    complaint = (await db.execute(
        select(Complaint).where(Complaint.complaint_id == complaint_id))).scalar_one_or_none()
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

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
        "file_type": evidence.file_type,
        "ipfs_hash": evidence.ipfs_hash,
        "file_hash": evidence.file_hash,
    }


@router.get("/{evidence_id}")
async def get_evidence(evidence_id: str, user: dict = Depends(con_or_above),
                       db: AsyncSession = Depends(get_db)):
    """Retrieve evidence metadata (file content via IPFS outside demo scope)."""
    evidence = (await db.execute(
        select(Evidence).where(Evidence.evidence_id == evidence_id))).scalar_one_or_none()
    if evidence is None:
        raise HTTPException(status_code=404, detail="Evidence not found")

    return {
        "evidence_id": evidence.evidence_id,
        "complaint_id": evidence.complaint_id,
        "file_name": evidence.file_name,
        "file_type": evidence.file_type,
        "file_hash": evidence.file_hash,
        "ipfs_hash": evidence.ipfs_hash,
        "uploaded_at": evidence.uploaded_at,
        "uploaded_by": evidence.uploaded_by,
    }


@router.get("/complaint/{complaint_id}")
async def list_evidence(complaint_id: str, user: dict = Depends(con_or_above),
                        db: AsyncSession = Depends(get_db)):
    """List all evidence for a complaint."""
    rows = (await db.execute(
        select(Evidence).where(Evidence.complaint_id == complaint_id))).scalars().all()
    return {
        "complaint_id": complaint_id,
        "items": [
            {"evidence_id": e.evidence_id, "file_name": e.file_name,
             "file_type": e.file_type, "ipfs_hash": e.ipfs_hash,
             "uploaded_at": e.uploaded_at} for e in rows
        ],
        "total": len(rows),
    }

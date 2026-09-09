"""Custom SHA-256 hash chain blockchain — zero external dependency.

Stores blocks in PostgreSQL and verifies chain integrity.
"""

import hashlib
import json
from datetime import UTC, datetime


def _sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def compute_data_hash(action: str, user_id: str | None, complaint_id: str | None,
                      metadata: dict) -> str:
    payload = json.dumps(
        {"action": action, "user_id": user_id, "complaint_id": complaint_id, "metadata": metadata},
        sort_keys=True,
        default=str,
    )
    return _sha256(payload)


class BlockchainService:
    """Manages a custom hash chain stored in PostgreSQL."""

    def __init__(self, session=None):
        self.session = session

    # --- Read helpers ---

    async def _get_blocks(self, session, complaint_id: str | None = None, limit: int = 1000) -> list[dict]:
        from sqlalchemy import select

        from api.models.audit_log import AuditLog

        stmt = select(AuditLog).order_by(AuditLog.timestamp.asc()).limit(limit)
        if complaint_id:
            # JSONB filter — PostgreSQL `details @> '{"complaint_id": ...}'`
            from sqlalchemy import text
            rows = await session.execute(
                text("SELECT * FROM audit_logs WHERE details::jsonb @> :payload ORDER BY timestamp ASC LIMIT :lim"),
                {"payload": json.dumps({"complaint_id": complaint_id}), "lim": limit},
            )
            return [dict(r._mapping) for r in rows]
        rows = await session.execute(stmt)
        return [dict(r._mapping) for r in rows]

    def _block_from_row(self, row: dict, index: int) -> dict:
        details = row.get("details") or {}
        if isinstance(details, str):
            try:
                details = json.loads(details)
            except Exception:
                details = {}
        ts = row.get("timestamp")
        return {
            "index": index,
            "timestamp": ts.isoformat() if hasattr(ts, "isoformat") else str(ts),
            "action": row.get("action", ""),
            "user_id": row.get("user_id"),
            "complaint_id": details.get("complaint_id"),
            "metadata": details,
            "data_hash": compute_data_hash(
                row.get("action", ""), row.get("user_id"), details.get("complaint_id"), details
            ),
            "previous_hash": row.get("_prev_hash") or "",
        }

    # --- Logging ---

    async def log_action(self, session, *, action: str, user_id: str | None = None,
                         complaint_id: str | None = None, metadata: dict | None = None,
                         ip_address: str | None = None) -> dict:
        """Append a block to the chain (audit_logs row + hash continuity)."""
        from sqlalchemy import text

        details = dict(metadata or {})
        if complaint_id:
            details["complaint_id"] = complaint_id

        data_hash = compute_data_hash(action, user_id, complaint_id, details)

        # Get previous hash (last block for this complaint, or global chain)
        prev_row = await session.execute(
            text(
                "SELECT log_id, details FROM audit_logs "
                "WHERE details::jsonb @> :payload ORDER BY timestamp DESC LIMIT 1"
            ),
            {"payload": json.dumps({"complaint_id": complaint_id}) if complaint_id else "{}"},
        )
        prev = prev_row.first()
        previous_hash = _sha256(json.dumps(prev.details, default=str)) if prev else "GENESIS"

        # Insert block (stores data + prev-hash inside details for portability)
        details["_chain"] = {
            "data_hash": data_hash,
            "previous_hash": previous_hash,
            "verified_at": _now_iso(),
        }

        import uuid

        from sqlalchemy import insert

        from api.models.audit_log import AuditLog

        row = await session.execute(
            insert(AuditLog).values(
                log_id=str(uuid.uuid4()),
                user_id=user_id,
                action=action,
                details=details,
                ip_address=ip_address,
            ).returning(AuditLog.log_id)
        )
        log_id = row.scalar_one()

        return {
            "index": 0,  # assigned by reader
            "log_id": log_id,
            "action": action,
            "complaint_id": complaint_id,
            "data_hash": data_hash,
            "previous_hash": previous_hash,
            "metadata": details,
        }

    # --- Verification ---

    async def verify_chain(self, session, complaint_id: str | None = None) -> dict:
        rows = await self._get_blocks(session, complaint_id)
        if not rows:
            return {"verified": True, "block_count": 0, "broken_at": None}

        prev_hash = "GENESIS"
        broken = None
        for i, row in enumerate(rows):
            details = row.get("details") or {}
            if isinstance(details, str):
                try:
                    details = json.loads(details)
                except Exception:
                    details = {}
            expected = compute_data_hash(
                row.get("action", ""), row.get("user_id"), details.get("complaint_id"), details
            )
            stored = (details.get("_chain") or {}).get("data_hash")
            if stored and stored != expected:
                broken = i
                break
            pv = (details.get("_chain") or {}).get("previous_hash")
            if pv is not None and pv != prev_hash:
                broken = i
                break
            prev_hash = expected

        return {"verified": broken is None, "block_count": len(rows), "broken_at": broken}

    async def get_audit_trail(self, session, complaint_id: str) -> list[dict]:
        rows = await self._get_blocks(session, complaint_id)
        return [
            {
                "index": i,
                "action": r.get("action"),
                "timestamp": r.get("timestamp").isoformat() if hasattr(r.get("timestamp"), "isoformat") else str(r.get("timestamp")),
                "user_id": r.get("user_id"),
                "metadata": r.get("details"),
            }
            for i, r in enumerate(rows)
        ]


# Convenience functions
async def log_blockchain_event(session, action: str, complaint_id: str | None = None,
                               user_id: str | None = None, metadata: dict | None = None,
                               ip_address: str | None = None) -> dict:
    svc = BlockchainService()
    return await svc.log_action(session, action=action, user_id=user_id,
                                complaint_id=complaint_id, metadata=metadata,
                                ip_address=ip_address)

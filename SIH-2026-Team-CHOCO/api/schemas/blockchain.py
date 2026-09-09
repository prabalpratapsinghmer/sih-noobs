"""Pydantic schemas for blockchain audit trail."""

from typing import Any

from pydantic import BaseModel


class BlockchainLogRequest(BaseModel):
    action: str
    user_id: str | None = None
    complaint_id: str | None = None
    metadata: dict[str, Any] = {}


class BlockOut(BaseModel):
    index: int
    timestamp: str
    data_hash: str
    previous_hash: str
    action: str
    user_id: str | None = None
    complaint_id: str | None = None
    metadata: dict = {}


class ChainVerifyResponse(BaseModel):
    verified: bool
    block_count: int
    broken_at: int | None = None


class AuditTrailItem(BaseModel):
    index: int
    action: str
    timestamp: str
    user_id: str | None = None
    metadata: dict = {}

"""Banking API Mock for SIH26184."""

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from loguru import logger

app = FastAPI(
    title="Banking API Mock",
    description="Mock banking API for integration testing",
    version="1.0.0"
)

# In-memory storage
accounts_db: Dict[str, Dict] = {}
transactions_db: List[Dict] = []
complaints_db: Dict[str, Dict] = {}
atms_db: List[Dict] = []

# Pre-populate with some test data
def init_test_data():
    """Initialize test banking data."""
    # ATMs
    for i in range(500):
        atms_db.append({
            "atm_id": f"ATM_{i:04d}",
            "lat": 12.9 + random.uniform(-0.2, 0.2),
            "lon": 77.6 + random.uniform(-0.2, 0.2),
            "bank": random.choice(["SBI", "HDFC", "ICICI", "AXIS", "KOTAK"]),
            "is_active": True
        })

    # Accounts
    for i in range(1000):
        acc_id = f"ACC_{i:06d}"
        accounts_db[acc_id] = {
            "account_id": acc_id,
            "customer_id": f"CUST_{i:06d}",
            "balance": random.uniform(1000, 100000),
            "account_type": random.choice(["SAVINGS", "CURRENT", "SALARY"]),
            "kyc_status": random.choice(["VERIFIED", "PENDING", "REJECTED"]),
            "is_frozen": False,
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        }

init_test_data()


# Models
class TransactionRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float = Field(..., gt=0)
    transaction_type: str = Field(..., pattern="^(DEBIT|CREDIT|TRANSFER)$")
    atm_id: Optional[str] = None
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    timestamp: str
    from_account: str
    to_account: str
    amount: float


class AccountInfo(BaseModel):
    account_id: str
    balance: float
    account_type: str
    kyc_status: str
    is_frozen: bool


class FreezeRequest(BaseModel):
    account_id: str
    reason: str
    duration_hours: Optional[int] = None


class FreezeResponse(BaseModel):
    account_id: str
    status: str
    frozen_at: str
    reason: str


class ComplaintRequest(BaseModel):
    victim_account: str
    amount: float
    description: str
    atm_id: Optional[str] = None
    transaction_ids: List[str] = []


class ComplaintResponse(BaseModel):
    complaint_id: str
    status: str
    created_at: str


class ATMInfo(BaseModel):
    atm_id: str
    lat: float
    lon: float
    bank: str
    is_active: bool


# Auth dependency (mock)
async def verify_api_key(x_api_key: str = Header(...)):
    if not x_api_key or x_api_key != "test-api-key-123":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# Routes
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "banking-api-mock"}


@app.get("/atms", response_model=List[ATMInfo])
async def list_atms(active_only: bool = True, api_key: str = Depends(verify_api_key)):
    """List all ATMs."""
    if active_only:
        return [atm for atm in atms_db if atm["is_active"]]
    return atms_db


@app.get("/atms/{atm_id}", response_model=ATMInfo)
async def get_atm(atm_id: str, api_key: str = Depends(verify_api_key)):
    """Get ATM details."""
    atm = next((a for a in atms_db if a["atm_id"] == atm_id), None)
    if not atm:
        raise HTTPException(status_code=404, detail="ATM not found")
    return atm


@app.get("/accounts/{account_id}", response_model=AccountInfo)
async def get_account(account_id: str, api_key: str = Depends(verify_api_key)):
    """Get account information."""
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountInfo(
        account_id=account["account_id"],
        balance=account["balance"],
        account_type=account["account_type"],
        kyc_status=account["kyc_status"],
        is_frozen=account["is_frozen"]
    )


@app.post("/accounts/{account_id}/freeze", response_model=FreezeResponse)
async def freeze_account(account_id: str, request: FreezeRequest, api_key: str = Depends(verify_api_key)):
    """Freeze an account."""
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account["is_frozen"] = True
    frozen_at = datetime.now().isoformat()

    logger.info(f"Account {account_id} frozen: {request.reason}")

    return FreezeResponse(
        account_id=account_id,
        status="FROZEN",
        frozen_at=frozen_at,
        reason=request.reason
    )


@app.post("/accounts/{account_id}/unfreeze")
async def unfreeze_account(account_id: str, api_key: str = Depends(verify_api_key)):
    """Unfreeze an account."""
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account["is_frozen"] = False
    logger.info(f"Account {account_id} unfrozen")

    return {"account_id": account_id, "status": "ACTIVE", "unfrozen_at": datetime.now().isoformat()}


@app.post("/transactions", response_model=TransactionResponse)
async def create_transaction(request: TransactionRequest, api_key: str = Depends(verify_api_key)):
    """Process a transaction."""
    from_acc = accounts_db.get(request.from_account)
    to_acc = accounts_db.get(request.to_account)

    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_acc["is_frozen"] or to_acc["is_frozen"]:
        raise HTTPException(status_code=403, detail="Account is frozen")

    if request.transaction_type == "DEBIT" and from_acc["balance"] < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Process transaction
    transaction_id = f"TXN_{len(transactions_db) + 1:08d}"
    timestamp = datetime.now().isoformat()

    if request.transaction_type == "DEBIT":
        from_acc["balance"] -= request.amount
        to_acc["balance"] += request.amount
    elif request.transaction_type == "CREDIT":
        to_acc["balance"] += request.amount
    elif request.transaction_type == "TRANSFER":
        from_acc["balance"] -= request.amount
        to_acc["balance"] += request.amount

    transaction = {
        "transaction_id": transaction_id,
        "from_account": request.from_account,
        "to_account": request.to_account,
        "amount": request.amount,
        "transaction_type": request.transaction_type,
        "atm_id": request.atm_id,
        "description": request.description,
        "timestamp": timestamp,
        "status": "COMPLETED"
    }
    transactions_db.append(transaction)

    logger.info(f"Transaction {transaction_id}: {request.from_account} -> {request.to_account} ({request.amount})")

    return TransactionResponse(**transaction)


@app.get("/transactions")
async def list_transactions(
    account_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    api_key: str = Depends(verify_api_key)
):
    """List transactions with filters."""
    filtered = transactions_db

    if account_id:
        filtered = [t for t in filtered if t["from_account"] == account_id or t["to_account"] == account_id]

    if start_date:
        filtered = [t for t in filtered if t["timestamp"] >= start_date]

    if end_date:
        filtered = [t for t in filtered if t["timestamp"] <= end_date]

    return filtered[-limit:]


@app.post("/complaints", response_model=ComplaintResponse)
async def file_complaint(request: ComplaintRequest, api_key: str = Depends(verify_api_key)):
    """File a cybercrime complaint."""
    complaint_id = f"COMP_{len(complaints_db) + 1:06d}"
    created_at = datetime.now().isoformat()

    complaint = {
        "complaint_id": complaint_id,
        "victim_account": request.victim_account,
        "amount": request.amount,
        "description": request.description,
        "atm_id": request.atm_id,
        "transaction_ids": request.transaction_ids,
        "status": "FILED",
        "created_at": created_at,
        "investigation_status": "PENDING"
    }
    complaints_db[complaint_id] = complaint

    logger.info(f"Complaint {complaint_id} filed for account {request.victim_account}")

    return ComplaintResponse(
        complaint_id=complaint_id,
        status="FILED",
        created_at=created_at
    )


@app.get("/complaints/{complaint_id}")
async def get_complaint(complaint_id: str, api_key: str = Depends(verify_api_key)):
    """Get complaint details."""
    complaint = complaints_db.get(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@app.post("/complaints/{complaint_id}/investigate")
async def investigate_complaint(complaint_id: str, api_key: str = Depends(verify_api_key)):
    """Mark complaint as under investigation."""
    complaint = complaints_db.get(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    complaint["investigation_status"] = "UNDER_INVESTIGATION"
    complaint["investigated_at"] = datetime.now().isoformat()

    return {"complaint_id": complaint_id, "status": "UNDER_INVESTIGATION"}


@app.post("/complaints/{complaint_id}/resolve")
async def resolve_complaint(complaint_id: str, resolution: str, api_key: str = Depends(verify_api_key)):
    """Resolve a complaint."""
    complaint = complaints_db.get(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    complaint["investigation_status"] = "RESOLVED"
    complaint["resolution"] = resolution
    complaint["resolved_at"] = datetime.now().isoformat()

    return {"complaint_id": complaint_id, "status": "RESOLVED", "resolution": resolution}


@app.get("/accounts/{account_id}/transaction-history")
async def get_transaction_history(account_id: str, days: int = 30, api_key: str = Depends(verify_api_key)):
    """Get transaction history for an account."""
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    cutoff = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff.isoformat()

    history = [t for t in transactions_db
               if (t["from_account"] == account_id or t["to_account"] == account_id)
               and t["timestamp"] >= cutoff_str]

    return {"account_id": account_id, "transactions": history, "count": len(history)}


@app.get("/analytics/velocity/{account_id}")
async def get_transaction_velocity(account_id: str, window_hours: int = 24, api_key: str = Depends(verify_api_key)):
    """Get transaction velocity for an account."""
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    cutoff = datetime.now() - timedelta(hours=window_hours)
    cutoff_str = cutoff.isoformat()

    recent_txns = [t for t in transactions_db
                   if (t["from_account"] == account_id or t["to_account"] == account_id)
                   and t["timestamp"] >= cutoff_str]

    velocity = len(recent_txns) / window_hours

    return {
        "account_id": account_id,
        "window_hours": window_hours,
        "transaction_count": len(recent_txns),
        "velocity_per_hour": velocity
    }


@app.get("/analytics/holding-time/{account_id}")
async def get_holding_time(account_id: str, api_key: str = Depends(verify_api_key)):
    """Calculate average holding time for an account."""
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Simulate holding time calculation
    credits = [t for t in transactions_db if t["to_account"] == account_id]
    debits = [t for t in transactions_db if t["from_account"] == account_id]

    # Simplified: average time between credit and subsequent debit
    holding_times = []
    for credit in credits:
        subsequent_debits = [d for d in debits if d["timestamp"] > credit["timestamp"]]
        if subsequent_debits:
            next_debit = min(subsequent_debits, key=lambda x: x["timestamp"])
            credit_time = datetime.fromisoformat(credit["timestamp"])
            debit_time = datetime.fromisoformat(next_debit["timestamp"])
            holding_minutes = (debit_time - credit_time).total_seconds() / 60
            holding_times.append(holding_minutes)

    avg_holding = sum(holding_times) / len(holding_times) if holding_times else 0

    return {
        "account_id": account_id,
        "avg_holding_time_minutes": avg_holding,
        "sample_count": len(holding_times)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.banking_mock:app", host="0.0.0.0", port=8001, reload=True)
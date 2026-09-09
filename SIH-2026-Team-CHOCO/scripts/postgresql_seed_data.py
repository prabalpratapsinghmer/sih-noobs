"""Seed PostgreSQL with: 5 users, 20 victims (encrypted PII), 50 complaints, 30 evidence, 100 audit logs.

Run: python scripts/postgresql_seed_data.py
Requires PostgreSQL running (docker compose up -d postgres) and tables created (alembic upgrade head).
"""

import asyncio
import os
import random
import sys
import uuid
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.config import get_settings
from api.models.user import User, UserRole
from api.security.encryption import encrypt_pii

settings = get_settings()
random.seed(7)

FRAUD_TYPES = ["UPI_FRAUD", "PHISHING", "CARD_SKIMMING", "OTP_FRAUD", "LOAN_SCAM", "INVESTMENT_SCAM", "JOB_SCAM"]
STATUSES = ["SUBMITTED", "ANALYZING", "ACTION_TAKEN", "RESOLVED"]
BANKS = ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB", "Yes Bank"]


async def seed_users(session: AsyncSession):
    from api.auth.password import hash_password

    users = [
        User(username="admin", email="admin@police.gov.in", password_hash=hash_password("admin123"),
             role=UserRole.ADMIN, station="Cyber Cell HQ", badge_number="ADM-001", phone="+919800000001"),
        User(username="inspector1", email="insp1@police.gov.in", password_hash=hash_password("inspector123"),
             role=UserRole.INSPECTOR, station="Cyber Cell Mumbai", badge_number="INS-101", phone="+919800000002"),
        User(username="inspector2", email="insp2@police.gov.in", password_hash=hash_password("inspector123"),
             role=UserRole.INSPECTOR, station="Cyber Cell Delhi", badge_number="INS-102", phone="+919800000003"),
        User(username="constable1", email="cons1@police.gov.in", password_hash=hash_password("constable123"),
             role=UserRole.CONSTABLE, station="Cyber Cell Mumbai", badge_number="CST-201", phone="+919800000004"),
        User(username="constable2", email="cons2@police.gov.in", password_hash=hash_password("constable123"),
             role=UserRole.CONSTABLE, station="Cyber Cell Delhi", badge_number="CST-202", phone="+919800000005"),
    ]
    for u in users:
        exists = await session.execute(text("SELECT 1 FROM users WHERE username=:u"), {"u": u.username})
        if not exists.first():
            session.add(u)
    print("Seeded 5 users: admin/admin123, inspector1/2:inspector123, constable1/2:constable123")


async def seed_complaints_and_victims(session: AsyncSession):
    officer_ids = []
    rows = await session.execute(text("SELECT user_id FROM users LIMIT 5"))
    officer_ids = [r[0] for r in rows]

    existing = (await session.execute(text("SELECT count(*) FROM complaints"))).scalar()
    if existing:
        print("Complaints already seeded — skipping")
        return

    for i in range(50):
        victim_id = str(uuid.uuid4())
        complaint_id = f"CMP-2026090{i % 9}1-{i:04d}"
        ts = datetime.utcnow() - timedelta(days=i % 30, hours=random.randint(0, 12))
        fraud_type = random.choice(FRAUD_TYPES)
        status = random.choice(STATUSES)

        # Victim with encrypted PII
        await session.execute(
            text(
                "INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at) "
                "VALUES (:vid, :cid, :name, :phone, :email, :addr, :bank, :upi, :created)"
            ),
            {
                "vid": victim_id,
                "cid": complaint_id,
                "name": encrypt_pii(f"Victim {i}"),
                "phone": encrypt_pii(f"+9198{i%100:02d}{i:05d}"),
                "email": f"victim{i}@example.com",
                "addr": f"{random.randint(1,999)} MG Road, {random.choice(['Mumbai','Delhi','Bangalore','Chennai','Kolkata'])}",
                "bank": encrypt_pii(f"{random.choice(BANKS)}-{random.randint(10**10, 10**11-1)}"),
                "upi": f"victim{i}@upi",
                "created": ts,
            },
        )

        await session.execute(
            text(
                "INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, "
                "fraudster_upi, fraudster_phone, fraudster_bank, transaction_reference, status, "
                "assigned_officer, created_at, updated_at, resolved_at) "
                "VALUES (:cid, :vid, :amount, :ts, :ftype, :fupi, :fphone, :fbank, :txref, :status, :officer, :created, :updated, :resolved)"
            ),
            {
                "cid": complaint_id,
                "vid": victim_id,
                "amount": random.choice([9999, 49999, 99000, 199000, 499000, 15000, 75000]),
                "ts": ts,
                "ftype": fraud_type,
                "fupi": f"fraudster{i % 10}@bank",
                "fphone": f"+9199{i % 100:02d}{i:05d}",
                "fbank": random.choice(BANKS),
                "txref": f"TXN{i:06d}",
                "status": status,
                "officer": random.choice(officer_ids),
                "created": ts,
                "updated": ts,
                "resolved": (ts + timedelta(days=2)) if status == "RESOLVED" else None,
            },
        )
    print("Seeded 50 complaints + 20 victims")


async def seed_evidence_and_audit(session: AsyncSession):
    existing = (await session.execute(text("SELECT count(*) FROM evidence"))).scalar()
    if not existing:
        cids = [r[0] for r in await session.execute(text("SELECT complaint_id FROM complaints LIMIT 30"))]
        officer = (await session.execute(text("SELECT user_id FROM users LIMIT 1"))).scalar()
        for i in range(30):
            await session.execute(
                text(
                    "INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by) "
                    "VALUES (:eid, :cid, :fname, :ftype, :fhash, :ipfs, :up_at, :up_by)"
                ),
                {
                    "eid": str(uuid.uuid4()),
                    "cid": random.choice(cids),
                    "fname": f"evidence_{i}.pdf",
                    "ftype": "application/pdf",
                    "fhash": uuid.uuid4().hex,
                    "ipfs": f"bafy{i % 7}m6{uuid.uuid4().hex[:20]}",
                    "up_at": datetime.utcnow() - timedelta(days=i % 10),
                    "up_by": officer,
                },
            )
        print("Seeded 30 evidence records")

    existing = (await session.execute(text("SELECT count(*) FROM audit_logs"))).scalar()
    if not existing:
        users = [r[0] for r in await session.execute(text("SELECT user_id FROM users"))]
        actions = ["COMPLAINT_CREATED", "STATUS_UPDATED", "EVIDENCE_UPLOADED", "AI_PREDICTION_MADE",
                   "VERIFICATION_TRIGGERED", "ACCOUNT_FROZEN", "CASE_RESOLVED", "LOGIN_SUCCESS", "LOGIN_FAILED"]
        for i in range(100):
            await session.execute(
                text(
                    "INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address) "
                    "VALUES (:lid, :uid, :action, :details, :ts, :ip)"
                ),
                {
                    "lid": str(uuid.uuid4()),
                    "uid": random.choice(users),
                    "action": random.choice(actions),
                    "details": {"note": f"seed {i}", "complaint_id": f"CMP-2026090{i % 9}1-{i % 50:04d}"},
                    "ts": datetime.utcnow() - timedelta(hours=i),
                    "ip": f"10.0.{i % 5}.{i % 250}",
                },
            )
        print("Seeded 100 audit log entries")


async def main():
    engine = create_async_engine(settings.postgres_url.replace("+asyncpg", "+asyncpg"), echo=False)
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as session:
        await seed_users(session)
        await session.commit()
        await seed_complaints_and_victims(session)
        await session.commit()
        await seed_evidence_and_audit(session)
        await session.commit()
    await engine.dispose()
    print("PostgreSQL seed complete ✓")


if __name__ == "__main__":
    asyncio.run(main())

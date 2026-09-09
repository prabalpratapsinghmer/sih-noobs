"""Seed primary Super Admin (Moksh / mok008) and role hierarchy users across PostgreSQL and Supabase."""

import asyncio
from datetime import datetime
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import structlog
from sqlalchemy import select, text
from api.database.postgres import init_postgres, get_db

from api.models.user import User, UserRole
from api.auth.password import hash_password
from api.services.supabase_service import get_supabase_service

logger = structlog.get_logger(__name__)

HIERARCHY_ACCOUNTS = [
    {
        "username": "Moksh",
        "password": "mok008",
        "email": "moksh@cybercell.gov.in",
        "role": UserRole.ADMIN,
        "station": "Central Cyber Defense Directorate",
        "badge_number": "DIR-MOKSH-01",
        "phone": "9800000001",
    },
    {
        "username": "inspector_vikram",
        "password": "vikram123",
        "email": "vikram@cybercell.gov.in",
        "role": UserRole.INSPECTOR,
        "station": "Indiranagar Tactical Cyber Cell",
        "badge_number": "IN-KA-BLR-0847",
        "phone": "9876543210",
    },
    {
        "username": "patrol_chetan",
        "password": "chetan123",
        "email": "chetan@cybercell.gov.in",
        "role": UserRole.CONSTABLE,
        "station": "Quick Response Intercept Unit",
        "badge_number": "PATROL-DELTA-4",
        "phone": "9876543211",
    },
    {
        "username": "citizen_rahul",
        "password": "rahul123",
        "email": "rahul.verma@citizen.in",
        "role": UserRole.CITIZEN,
        "station": "Citizen Portal Intake",
        "badge_number": "CITIZEN-001",
        "phone": "9876543212",
    },
]

async def seed():
    print("=== INITIALIZING HIERARCHICAL ACCESS CREDENTIALS ===")
    await init_postgres()
    supabase = get_supabase_service()

    async for db in get_db():
        # First ensure CITIZEN exists in PostgreSQL enum if postgres is used
        try:
            await db.execute(text("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'CITIZEN'"))
            await db.commit()
        except Exception:
            pass

        for acc in HIERARCHY_ACCOUNTS:
            # 1. Upsert in PostgreSQL
            result = await db.execute(
                select(User).where((User.username == acc["username"]) | (User.email == acc["email"]))
            )
            user = result.scalar_one_or_none()
            hashed_pw = hash_password(acc["password"])

            if user is None:
                new_user = User(
                    user_id=str(uuid.uuid4()),
                    username=acc["username"],
                    email=acc["email"],
                    password_hash=hashed_pw,
                    role=acc["role"],
                    station=acc["station"],
                    badge_number=acc["badge_number"],
                    phone=acc["phone"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    last_login=datetime.utcnow(),
                    is_active=True,
                )
                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)
                user = new_user
                print(f"[CREATED] Local DB user: {acc['username']} ({acc['role'].value})")
            else:
                user.password_hash = hashed_pw
                user.role = acc["role"]
                user.station = acc["station"]
                user.badge_number = acc["badge_number"]
                user.phone = acc["phone"]
                user.is_active = True
                await db.commit()
                print(f"[UPDATED] Local DB user: {acc['username']} ({acc['role'].value})")

            # 2. Sync to Supabase
            try:
                # Map CITIZEN to CONSTABLE for Supabase public.users if enum lacks CITIZEN
                supa_role = "CONSTABLE" if acc["role"].value == "CITIZEN" else acc["role"].value
                await supabase.insert_user(
                    user_id=user.user_id,
                    username=acc["username"],
                    email=acc["email"],
                    password_hash=hashed_pw,
                    role=supa_role,
                    station=acc["station"],
                    badge_number=acc["badge_number"],
                    phone=acc["phone"],
                )
                await supabase.sync_user_auth(
                    email=acc["email"],
                    password=acc["password"],
                    user_metadata={"username": acc["username"], "role": acc["role"].value},
                )
                print(f"  ✓ Synced to Supabase: {acc['username']}")
            except Exception as e:
                print(f"  Note on Supabase sync for {acc['username']}: {e}")

        break

    print("=== HIERARCHICAL CREDENTIALS SEEDING COMPLETE ===")

if __name__ == "__main__":
    asyncio.run(seed())

"""PostgreSQL / SQLite async connection pool and session management with resilient fallback."""

import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path

import structlog
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.config import get_settings

logger = structlog.get_logger(__name__)

settings = get_settings()

# Global engine and session maker
_engine: AsyncEngine | None = None
_session_maker: async_sessionmaker[AsyncSession] | None = None
_db_type: str = "unknown"


async def init_postgres() -> None:
    """Initialize PostgreSQL connection pool or fall back to local persistent SQLite database."""
    global _engine, _session_maker, _db_type

    # 1. Check if Postgres URL is configured
    pg_url = settings.postgres_url
    if not pg_url and settings.postgres_host and settings.postgres_password:
        pg_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

    if pg_url:
        try:
            logger.info("Attempting PostgreSQL connection", host=settings.postgres_host, port=settings.postgres_port)
            engine = create_async_engine(
                pg_url,
                echo=False,
                pool_size=5,
                max_overflow=15,
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args={"timeout": 2},
            )
            async def _probe() -> None:
                async with engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))

            await asyncio.wait_for(_probe(), timeout=2.0)
            _engine = engine
            _session_maker = async_sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)
            _db_type = "postgresql"
            logger.info("[OK] PostgreSQL connection established")

            # Create tables and seed initial data in PostgreSQL
            try:
                from api.models import Base
                async with _engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                logger.info("[OK] PostgreSQL tables created/verified")

                async with _session_maker() as session:
                    await seed_hierarchical_accounts(session)
                logger.info("[OK] PostgreSQL initial hierarchical seed confirmed")

            except Exception as se:
                logger.warning(f"PostgreSQL table/seed notice: {se}")

            return
        except Exception as e:
            logger.warning(f"PostgreSQL not reachable ({e}). Falling back to resilient local SQLite store.")

    # 2. Resilient SQLite fallback
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    sqlite_path = data_dir / "sih26184.db"
    sqlite_url = f"sqlite+aiosqlite:///{sqlite_path.as_posix()}"

    logger.info(f"Initializing local SQLite persistence at {sqlite_path}")
    _engine = create_async_engine(sqlite_url, echo=False)
    _session_maker = async_sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)
    _db_type = "sqlite"

    # 3. Create all tables
    try:
        from api.models import Base
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("[OK] SQLite database tables initialized successfully")

        # 4. Seed initial hierarchical accounts (Moksh, Vikram, Chetan, Rahul)
        async with _session_maker() as session:
            await seed_hierarchical_accounts(session)
        logger.info("[OK] Initial hierarchical seed data confirmed in SQLite store")
    except Exception as e:
        logger.warning(f"Error during SQLite setup/seeding: {e}")


async def close_postgres() -> None:
    """Close PostgreSQL / SQLite connection pool."""
    global _engine

    if _engine is not None:
        await _engine.dispose()
        logger.info("Database pool disposed")


async def check_postgres_health() -> bool:
    """Check database health (bounded to 1s so /health never hangs)."""
    if _engine is None:
        return False

    async def _ping() -> None:
        async with _engine.begin() as conn:
            await conn.execute(text("SELECT 1"))

    try:
        await asyncio.wait_for(_ping(), timeout=1.0)
        return True
    except Exception:
        return False


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session - FastAPI dependency."""
    if _session_maker is None:
        await init_postgres()

    if _session_maker is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Database unavailable")

    async with _session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_db_session() -> AsyncSession:
    """Get a database session (without context manager)."""
    if _session_maker is None:
        await init_postgres()
    if _session_maker is None:
        raise RuntimeError("Database not initialized")
    return _session_maker()


async def seed_hierarchical_accounts(session: AsyncSession) -> None:
    """Seed the 4 hierarchical access accounts into PostgreSQL/SQLite and dual-sync to Supabase."""
    from datetime import datetime
    from api.auth.password import hash_password
    from api.models.complaint import Complaint, ComplaintStatus
    from api.models.user import User, UserRole

    # 4 Hierarchical Access Accounts per Sovereign Security Specification
    accounts = [
        {
            "user_id": "usr-moksh-director",
            "username": "Moksh",
            "email": "moksh@cybercell.gov.in",
            "password": "mok008",
            "role": UserRole.ADMIN,
            "station": "Central Cyber Defense Directorate",
            "badge_number": "DIR-MOKSH-01",
            "phone": "9800000001",
        },
        {
            "user_id": "usr-officer-vikram",
            "username": "inspector_vikram",
            "email": "vikram@cybercell.gov.in",
            "password": "vikram123",
            "role": UserRole.INSPECTOR,
            "station": "Bengaluru Central Command",
            "badge_number": "IN-KA-BLR-0847",
            "phone": "9876543210",
        },
        {
            "user_id": "usr-patrol-chetan",
            "username": "patrol_chetan",
            "email": "chetan@cybercell.gov.in",
            "password": "chetan123",
            "role": UserRole.CONSTABLE,
            "station": "Indiranagar Quick Reaction Unit",
            "badge_number": "PATROL-DELTA-4",
            "phone": "9876543211",
        },
        {
            "user_id": "usr-citizen-rahul",
            "username": "citizen_rahul",
            "email": "rahul@gmail.com",
            "password": "rahul123",
            "role": UserRole.CITIZEN,
            "station": "Public Incident Intake Portal",
            "badge_number": "CITIZEN-AUTH",
            "phone": "9876543212",
        },
        # Legacy backward-compatible inspector
        {
            "user_id": "usr-officer-01",
            "username": "vikramaditya",
            "email": "vikramaditya@cybercell.gov.in",
            "password": "Password@123",
            "role": UserRole.INSPECTOR,
            "station": "Bengaluru Central Command",
            "badge_number": "IN-KA-BLR-0847",
            "phone": "9876543210",
        },
    ]

    for acc in accounts:
        existing = (
            await session.execute(
                select(User).where((User.username == acc["username"]) | (User.email == acc["email"]))
            )
        ).scalar_one_or_none()

        if not existing:
            hashed_pw = hash_password(acc["password"])
            new_u = User(
                user_id=acc["user_id"],
                username=acc["username"],
                email=acc["email"],
                password_hash=hashed_pw,
                role=acc["role"],
                station=acc["station"],
                badge_number=acc["badge_number"],
                phone=acc["phone"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=True,
            )
            session.add(new_u)
            logger.info(f"Seeded user account: {acc['username']} ({acc['role']})")

            # Dual-sync to Supabase public.users and GoTrue
            try:
                from api.services.supabase_service import get_supabase_service
                supa = get_supabase_service()
                if supa.is_enabled:
                    await supa.insert_user(
                        user_id=acc["user_id"],
                        username=acc["username"],
                        email=acc["email"],
                        password_hash=hashed_pw,
                        role=acc["role"].value if hasattr(acc["role"], "value") else str(acc["role"]),
                        station=acc["station"],
                        badge_number=acc["badge_number"],
                        phone=acc["phone"],
                    )
                    await supa.sync_user_auth(
                        email=acc["email"],
                        password=acc["password"],
                        user_metadata={"username": acc["username"], "role": str(acc["role"])},
                    )
            except Exception as e:
                logger.debug(f"Supabase sync notice for {acc['username']}: {e}")
        else:
            # Update password hash if needed so test credentials work reliably
            existing.password_hash = hash_password(acc["password"])
            existing.role = acc["role"]
            existing.is_active = True

    await session.commit()

    # Seed sample baseline complaint if none exists
    sample_complaint = (
        await session.execute(select(Complaint).where(Complaint.complaint_id == "CC-2026-F819"))
    ).scalar_one_or_none()
    if not sample_complaint:
        moksh_user = (await session.execute(select(User).where(User.username == "Moksh"))).scalar_one_or_none()
        complaint = Complaint(
            complaint_id="CC-2026-F819",
            victim_id=None,
            amount=500000.0,
            timestamp=datetime.utcnow(),
            fraud_type="INVESTMENT_SCAM",
            fraudster_upi="nexus.invest@ybl",
            fraudster_bank="Yes Bank",
            status=ComplaintStatus.SUBMITTED,
            assigned_officer=moksh_user.user_id if moksh_user else None,
        )
        session.add(complaint)

    await session.commit()


async def get_or_create_user(session: AsyncSession, *, email: str, name: str, role: str = "CITIZEN"):
    """Find an existing user by email or create a new one with the given role.

    Used by the Google OAuth login flow — new users default to CITIZEN role.
    """
    import uuid
    from datetime import datetime
    from api.auth.password import hash_password
    from api.models.user import User, UserRole

    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is not None:
        user.last_login = datetime.utcnow()
        await session.commit()
        return user

    # Map role string to UserRole enum
    role_map = {r.value: r for r in UserRole}
    user_role = role_map.get(role.upper(), UserRole.CITIZEN)

    # Derive a unique username from the name / email
    sanitized = "".join(c for c in name if c.isalnum() or c == "_").lower()
    candidate_username = sanitized[:40] or email.split("@")[0]

    existing_name = (
        await session.execute(select(User).where(User.username == candidate_username))
    ).scalar_one_or_none()
    if existing_name:
        candidate_username = f"{candidate_username[:34]}_{uuid.uuid4().hex[:5]}"

    new_user = User(
        user_id=str(uuid.uuid4()),
        username=candidate_username,
        email=email.strip().lower(),
        password_hash=hash_password(uuid.uuid4().hex),
        role=user_role,
        station="Google Sovereign ID Hub",
        badge_number=f"GOOG-{candidate_username[:4].upper()}",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        last_login=datetime.utcnow(),
        is_active=True,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

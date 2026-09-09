"""Genesis block creation for the blockchain audit trail.

Run: python scripts/blockchain_init.py
Creates the first (GENESIS) block in audit_logs if none exist.
"""

import asyncio
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.config import get_settings


async def main():
    settings = get_settings()
    engine = create_async_engine(settings.postgres_url, echo=False)
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with maker() as session:
        count = (await session.execute(text("SELECT count(*) FROM audit_logs"))).scalar()
        if count:
            print(f"Audit logs already contain {count} rows — genesis not needed")
            return

        payload = {"action": "GENESIS", "chain_started": True, "note": "SIH26184 blockchain root"}
        await session.execute(
            text(
                "INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address) "
                "VALUES (:lid, NULL, 'GENESIS', :details, :ts, NULL)"
            ),
            {"lid": str(uuid.uuid4()), "details": payload, "ts": datetime.utcnow()},
        )
        await session.commit()
        print("Genesis block created ✓")

    await engine.dispose()


if __name__ == "__main__":
    from datetime import datetime

    asyncio.run(main())

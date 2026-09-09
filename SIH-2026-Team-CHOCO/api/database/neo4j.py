"""Neo4j async driver and session management."""

import asyncio
from typing import Any

import structlog
from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncSession, Record

from api.config import get_settings

logger = structlog.get_logger(__name__)

settings = get_settings()

# Global driver
_driver: AsyncDriver | None = None


async def init_neo4j() -> None:
    """Initialize Neo4j driver with connection pooling."""
    global _driver

    logger.info(
        "Initializing Neo4j",
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
    )

    _driver = AsyncGraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
        max_connection_pool_size=50,
        connection_timeout=30.0,
    )

    # Test connection — bounded so a dead graph DB never blocks app startup
    await asyncio.wait_for(_driver.verify_connectivity(), timeout=2.0)
    logger.info("Neo4j connection established")


async def close_neo4j() -> None:
    """Close Neo4j driver."""
    global _driver

    if _driver is not None:
        await _driver.close()
        logger.info("Neo4j driver closed")


async def check_neo4j_health() -> bool:
    """Check Neo4j health (bounded to 1s so /health never hangs)."""
    if _driver is None:
        return False

    async def _ping() -> None:
        async with _driver.session() as session:
            result = await session.run("RETURN 1 AS n")
            await result.consume()

    try:
        await asyncio.wait_for(_ping(), timeout=1.0)
        return True
    except Exception:
        return False


def get_driver() -> AsyncDriver:
    """Get Neo4j driver instance."""
    if _driver is None:
        raise RuntimeError("Neo4j not initialized")
    return _driver


async def execute_query(
    query: str,
    parameters: dict[str, Any] | None = None,
) -> list[Record]:
    """Execute a Cypher query and return results."""
    if _driver is None:
        raise RuntimeError("Neo4j not initialized")

    async with _driver.session() as session:
        result = await session.run(query, parameters or {})
        return await result.data()


async def execute_write(
    query: str,
    parameters: dict[str, Any] | None = None,
) -> list[Record]:
    """Execute a write transaction."""
    if _driver is None:
        raise RuntimeError("Neo4j not initialized")

    async with _driver.session() as session:
        result = await session.run(query, parameters or {})
        await result.consume()
        return []


async def get_session() -> AsyncSession:
    """Get a Neo4j session (caller must manage lifecycle)."""
    if _driver is None:
        raise RuntimeError("Neo4j not initialized")
    return _driver.session()

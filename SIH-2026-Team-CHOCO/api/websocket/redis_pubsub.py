"""Redis pub/sub bridge for cross-instance WebSocket broadcasting."""

import asyncio
import json

import structlog

logger = structlog.get_logger(__name__)

_pubsub_task: asyncio.Task | None = None


async def publish(channel: str, event: dict) -> None:
    """Publish an event to a Redis channel."""
    try:
        from api.database.redis import get_redis

        r = get_redis()
        await r.publish(channel, json.dumps(event, default=str))
    except Exception as e:
        logger.warning("pubsub_publish_failed", channel=channel, error=str(e))


async def _bridge(channel: str, user_id_field: str = "user_id") -> None:
    """Subscribe to a channel and re-broadcast events to local manager."""
    from api.database.redis import get_redis
    from api.websocket.manager import manager

    r = get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(channel)
    try:
        async for raw in pubsub.listen():
            if raw.get("type") != "message":
                continue
            try:
                event = json.loads(raw["data"])
                target = event.get("payload", {}).get(user_id_field)
                if target:
                    await manager.send_to_user(target, event)
            except Exception as e:
                logger.debug("pubsub_bridge_skip", error=str(e))
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.aclose()


def start_bridges(channels: list[str]) -> None:
    """Start background pub/sub bridge tasks (idempotent, one per channel)."""
    global _pubsub_task

    async def _run_all():
        await asyncio.gather(*(_bridge(ch) for ch in channels), return_exceptions=True)

    if _pubsub_task is None or _pubsub_task.done():
        _pubsub_task = asyncio.create_task(_run_all())

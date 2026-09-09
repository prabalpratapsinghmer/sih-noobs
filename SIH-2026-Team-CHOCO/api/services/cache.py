"""Decorator-based Redis caching."""

import functools
import hashlib
import json
from collections.abc import Callable


def _make_key(key_prefix: str, args: tuple, kwargs: dict) -> str:
    payload = json.dumps({"args": [str(a) for a in args], "kwargs": {k: str(v) for k, v in kwargs.items()}},
                         sort_keys=True, default=str)
    hash_part = hashlib.sha256(payload.encode()).hexdigest()[:16]
    return f"sih26184:cache:{key_prefix}:{hash_part}"


def cache(ttl: int = 300, key_prefix: str = "data"):
    """Decorator: cache return value in Redis for `ttl` seconds.

    Graceful: if Redis is down, normal function execution proceeds.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = _make_key(key_prefix, args, kwargs)
            try:
                from api.database.redis import get_redis

                r = get_redis()
                cached = await r.get(key)
                if cached is not None:
                    return json.loads(cached)
            except Exception:
                pass  # Redis unavailable — just run

            result = await func(*args, **kwargs)

            try:
                from api.database.redis import get_redis

                r = get_redis()
                await r.setex(key, ttl, json.dumps(result, default=str))
            except Exception:
                pass
            return result

        return wrapper

    return decorator


async def invalidate_pattern(pattern: str) -> None:
    """Invalidate cache keys matching glob pattern like `sih26184:cache:heatmap:*`."""
    try:
        from api.database.redis import get_redis

        r = get_redis()
        keys = [k async for k in r.scan_iter(match=pattern)]
        if keys:
            await r.delete(*keys)
    except Exception:
        pass

"""In-memory Token Bucket Rate Limiter Middleware."""

import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter per IP address."""

    def __init__(self, app, requests_per_minute: int = 120, burst: int = 30):
        super().__init__(app)
        self.rate = requests_per_minute / 60.0  # tokens per second
        self.capacity = burst
        self.tokens: Dict[str, Tuple[float, float]] = {}  # ip -> (tokens, last_time)

    async def dispatch(self, request: Request, call_next):
        # Exclude health check from rate limiting
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        tokens, last_time = self.tokens.get(client_ip, (self.capacity, current_time))
        elapsed = current_time - last_time
        tokens = min(self.capacity, tokens + elapsed * self.rate)

        if tokens < 1.0:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "detail": "Too many requests. Please retry in a few seconds.",
                    "status_code": 429
                },
                headers={"Retry-After": "2"}
            )

        self.tokens[client_ip] = (tokens - 1.0, current_time)
        return await call_next(request)

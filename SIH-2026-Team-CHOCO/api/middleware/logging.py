"""Request logging middleware for the Cybercrime Prediction API.

Logs every incoming request with method, path, status code, and latency.
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from loguru import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs request details and response timing."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        logger.info(f"→ {method} {path} from {client_ip}")

        try:
            response = await call_next(request)
        except Exception as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                f"✗ {method} {path} — unhandled exception after {latency_ms:.1f}ms: {exc}"
            )
            raise

        latency_ms = (time.perf_counter() - start_time) * 1000
        status_code = response.status_code

        log_fn = logger.info if status_code < 400 else logger.warning
        log_fn(f"← {method} {path} → {status_code} ({latency_ms:.1f}ms)")

        # Add timing header for downstream consumers
        response.headers["X-Process-Time-Ms"] = f"{latency_ms:.2f}"

        return response

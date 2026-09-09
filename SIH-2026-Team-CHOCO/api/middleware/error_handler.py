"""Global error handling middleware for the Cybercrime Prediction API.

Catches unhandled exceptions and returns structured JSON error responses
instead of raw stack traces.
"""

import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Catches unhandled exceptions and returns JSON error responses."""

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            tb = traceback.format_exc()
            logger.error(f"Unhandled error on {request.method} {request.url.path}:\n{tb}")

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "detail": str(exc),
                    "path": str(request.url.path),
                },
            )

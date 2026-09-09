"""Status routes — /model/status and /model/metrics endpoints.

Provides model health checks, performance metrics, and system information.
"""

import time
import platform
from datetime import datetime

import torch
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional
from loguru import logger

router = APIRouter()

# Track startup time
_startup_time = time.time()


class ModelStatusResponse(BaseModel):
    status: str
    uptime_seconds: float
    models: Dict[str, Any]
    system: Dict[str, Any]


class ModelMetricsResponse(BaseModel):
    request_count: int
    avg_latency_ms: float
    error_count: int
    models: Dict[str, Any]


# Simple in-memory metrics counter
_metrics = {
    "request_count": 0,
    "total_latency_ms": 0.0,
    "error_count": 0,
}


def record_request(latency_ms: float, error: bool = False):
    """Record a request metric."""
    _metrics["request_count"] += 1
    _metrics["total_latency_ms"] += latency_ms
    if error:
        _metrics["error_count"] += 1


def _get_registry():
    from api.utils.model_loader import get_model_registry
    return get_model_registry()


@router.get("/status", response_model=ModelStatusResponse, summary="Model health status")
async def model_status():
    """
    Returns the current status of all loaded models, including parameter counts,
    device info, and system uptime.
    """
    registry = _get_registry()
    uptime = time.time() - _startup_time

    system_info = {
        "python_version": platform.python_version(),
        "pytorch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "platform": platform.platform(),
        "timestamp": datetime.utcnow().isoformat(),
    }

    return ModelStatusResponse(
        status="healthy" if (registry.is_stm_ready or registry.is_gnn_ready) else "degraded",
        uptime_seconds=round(uptime, 2),
        models=registry.get_status(),
        system=system_info,
    )


@router.get("/metrics", response_model=ModelMetricsResponse, summary="Performance metrics")
async def model_metrics():
    """
    Returns aggregate performance metrics: request count, average latency,
    and error count.
    """
    registry = _get_registry()
    avg_latency = (
        _metrics["total_latency_ms"] / _metrics["request_count"]
        if _metrics["request_count"] > 0
        else 0.0
    )

    return ModelMetricsResponse(
        request_count=_metrics["request_count"],
        avg_latency_ms=round(avg_latency, 2),
        error_count=_metrics["error_count"],
        models=registry.get_status(),
    )

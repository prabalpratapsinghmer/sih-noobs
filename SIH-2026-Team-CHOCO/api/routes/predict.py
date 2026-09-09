"""Prediction routes — /predict/atm and /predict/stm endpoints.

These endpoints use the Spatio-Temporal Transformer to predict the most
likely ATM locations where a fraudster will attempt to withdraw funds.
"""

import numpy as np
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from api.schemas.request import ATMPredictionRequest
from api.schemas.response import ATMPredictionResponse, ATMPredictionItem

router = APIRouter()


def _get_registry():
    """Lazy import to avoid circular dependency at module load time."""
    from api.utils.model_loader import get_model_registry
    return get_model_registry()


@router.post("/atm", response_model=ATMPredictionResponse, summary="Predict ATM withdrawal locations")
async def predict_atm(request: ATMPredictionRequest):
    """
    Predict the top-K ATM locations where a fraudster is most likely to
    withdraw funds, given spatial and temporal context from a complaint.

    - **spatial**: Geographic features (lat, lon, distances)
    - **temporal**: Time-based features (hour, day, time since complaint)
    - **top_k**: Number of top predictions to return (default 3)
    """
    registry = _get_registry()

    if not registry.is_stm_ready:
        raise HTTPException(status_code=503, detail="Spatio-Temporal model not loaded")

    try:
        # Prepare spatial features
        spatial_raw = np.array([[
            request.spatial.lat,
            request.spatial.lon,
            request.spatial.dist_metro,
            request.spatial.dist_police,
        ]])

        # Prepare temporal features with cyclic encoding
        hour = request.temporal.hour
        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        day_sin = np.sin(2 * np.pi * request.temporal.day / 7)
        day_cos = np.cos(2 * np.pi * request.temporal.day / 7)

        temporal_raw = np.array([[
            hour_sin, hour_cos,
            day_sin, day_cos,
            float(request.temporal.is_weekend),
            request.temporal.time_since_complaint,
            request.temporal.fraud_spike_hour,
        ]])

        from api.utils.inference import InferenceEngine
        engine = InferenceEngine(registry)
        result = engine.predict_atm(spatial_raw, temporal_raw, top_k=request.top_k)

        items = [
            ATMPredictionItem(atm_index=p["atm_index"], probability=p["probability"])
            for p in result["predictions"]
        ]

        return ATMPredictionResponse(
            predictions=items,
            top_k=request.top_k,
            latency_ms=result["latency_ms"],
        )

    except Exception as e:
        logger.error(f"ATM prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

"""Detection routes — /detect/mules endpoint.

Uses the Graph Neural Network and Hybrid Scoring System to detect
mule accounts and assess risk levels.
"""

from fastapi import APIRouter, HTTPException
from loguru import logger

from api.schemas.request import MuleDetectionRequest
from api.schemas.response import MuleDetectionResponse

router = APIRouter()


def _get_registry():
    from api.utils.model_loader import get_model_registry
    return get_model_registry()


@router.post("/mules", response_model=MuleDetectionResponse, summary="Detect mule accounts")
async def detect_mules(request: MuleDetectionRequest):
    """
    Detect whether an account is a money mule using:

    1. **GNN probability** — learned from transaction graph topology
    2. **Rule-based score** — heuristic signals (velocity, timing, outflow)
    3. **Hybrid final score** — weighted combination (70% GNN / 30% rules)

    Returns a risk level (HIGH / MEDIUM / LOW) and a recommended action.
    """
    registry = _get_registry()

    if not registry.is_gnn_ready:
        raise HTTPException(status_code=503, detail="Mule Detection model not loaded")

    try:
        features_dict = request.features.model_dump()

        from api.utils.inference import InferenceEngine
        engine = InferenceEngine(registry)
        result = engine.detect_mule(features_dict)

        return MuleDetectionResponse(
            account_id=request.account_id,
            gnn_probability=result["gnn_probability"],
            rule_score=result["rule_score"],
            final_score=result["final_score"],
            risk_level=result["risk_level"],
            risk_color=result["risk_color"],
            action=result["action"],
            latency_ms=result["latency_ms"],
        )

    except Exception as e:
        logger.error(f"Mule detection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

"""ATM prediction service — calls Member 1's model API (mock fallback)."""


import httpx
import structlog

from api.config import get_settings

logger = structlog.get_logger(__name__)

settings = get_settings()

async def predict_atms(complaint_id: str, account_ids: list[str] | None = None) -> list[dict]:
    """Return live ATM predictions, or no predictions when the model service is unavailable."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{settings.model_api_url.rstrip('/')}/internal/model/atm_predict",
                json={"complaint_id": complaint_id, "account_ids": account_ids or []},
            )
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and data:
                    return data
            logger.warning("atm_model_invalid_response", status_code=resp.status_code)
    except Exception as e:
        logger.warning("atm_model_unavailable", error=str(e))

    return []


async def predict_mule_gnn(account_id: str) -> float | None:
    """Call Member 1's GNN model for an account; returns probability or None (mock)."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{MODEL_API_URL}/internal/model/predict",
                json={"account_id": account_id},
            )
            if resp.status_code == 200:
                return float(resp.json().get("probability"))
    except Exception as e:
        logger.warning("gnn_model_unavailable, using mock", error=str(e))
    # Deterministic mock based on account id hash
    return float(int(account_id.encode().hex(), 16) % 100) / 100

"""End-to-End tests for Unified FastAPI Gateway, ML predictions, and vector endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport

from api.main import app


@pytest.mark.anyio
async def test_root_landing_dashboard():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/")
        assert res.status_code == 200
        assert "SIH26184" in res.text
        assert "SYSTEM ONLINE" in res.text


@pytest.mark.anyio
async def test_health_probe():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert "models_loaded" in data
        assert data["vector_db_ready"] is True
        assert "X-Trace-ID" in res.headers


@pytest.mark.anyio
async def test_metrics_exposition():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/metrics")
        assert res.status_code == 200
        assert "sih_http_requests_total" in res.text or "python_info" in res.text


@pytest.mark.anyio
async def test_stm_prediction_endpoint():
    payload = {
        "spatial": {
            "lat": 28.6139,
            "lon": 77.2090,
            "dist_metro": 1.2,
            "dist_police": 0.8,
        },
        "temporal": {
            "hour": 14,
            "day": 3,
            "is_weekend": False,
            "time_since_complaint": 2.5,
            "fraud_spike_hour": 15,
        },
        "top_k": 3,
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/predict/stm", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 3
        assert "probability" in data["predictions"][0]


@pytest.mark.anyio
async def test_mule_prediction_endpoint():
    payload = {
        "features": {
            "velocity": 12.5,
            "inflow": 500000.0,
            "outflow": 490000.0,
            "outflow_ratio": 0.98,
            "holding_time": 4.5,
            "connected_complaints": 3,
            "suspicious_timing": 4,
            "in_degree": 8,
            "out_degree": 12,
        },
        "account_id": "ACC-TEST-9988",
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/predict/mule", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert "final_score" in data
        assert "risk_level" in data
        assert data["account_id"] == "ACC-TEST-9988"


@pytest.mark.anyio
async def test_vector_indexing_and_search_endpoints():
    index_payload = {
        "complaint_id": "CMP-API-001",
        "fraud_type": "DIGITAL_ARREST",
        "description": "Caller impersonated CBI officer on Skype video call alleging money laundering in FedEx parcel.",
        "amount": 250000.0,
        "suspect_phone": "9876543210",
    }
    search_payload = {
        "query": "CBI Skype video call digital arrest threatening arrest warrant",
        "top_k": 3,
        "min_score": 0.2,
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Index
        index_res = await client.post("/api/v1/vector/index", json=index_payload)
        assert index_res.status_code == 200
        assert index_res.json()["status"] == "indexed"

        # Search
        search_res = await client.post("/api/v1/vector/search", json=search_payload)
        assert search_res.status_code == 200
        search_data = search_res.json()
        assert search_data["total_matches"] >= 1
        assert search_data["results"][0]["complaint_id"] == "CMP-API-001"


@pytest.mark.anyio
async def test_orchestration_endpoints():
    retrain_payload = {
        "min_records": 10,
        "epochs": 2,
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Trigger
        retrain_res = await client.post("/api/v1/orchestration/retrain", json=retrain_payload)
        assert retrain_res.status_code == 200
        data = retrain_res.json()
        assert data["status"] == "COMPLETED"

        # Status
        status_res = await client.get("/api/v1/orchestration/status")
        assert status_res.status_code == 200
        assert status_res.json()["scheduler_active"] is True

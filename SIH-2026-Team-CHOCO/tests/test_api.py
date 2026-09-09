"""Tests for the FastAPI application endpoints."""

import sys
from pathlib import Path

import pytest
from unittest.mock import patch, MagicMock

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# We test the API schemas and route logic without actually loading ML models.
# ---------------------------------------------------------------------------


class TestSchemas:
    """Test Pydantic request/response schemas."""

    def test_spatial_features_valid(self):
        from api.schemas.request import SpatialFeatures

        sf = SpatialFeatures(lat=12.97, lon=77.60, dist_metro=0.5, dist_police=2.3)
        assert sf.lat == 12.97
        assert sf.lon == 77.60

    def test_spatial_features_negative_distance_rejected(self):
        from api.schemas.request import SpatialFeatures
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            SpatialFeatures(lat=12.97, lon=77.60, dist_metro=-1.0, dist_police=2.3)

    def test_temporal_features_valid(self):
        from api.schemas.request import TemporalFeatures

        tf = TemporalFeatures(hour=14, day=3, is_weekend=False, time_since_complaint=2.5)
        assert tf.hour == 14
        assert tf.fraud_spike_hour == 22  # default

    def test_temporal_features_hour_out_of_range(self):
        from api.schemas.request import TemporalFeatures
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            TemporalFeatures(hour=25, day=3, is_weekend=False, time_since_complaint=2.5)

    def test_mule_features_valid(self):
        from api.schemas.request import MuleFeatures

        mf = MuleFeatures(
            velocity=5.0, inflow=500000, outflow=480000,
            outflow_ratio=0.96, holding_time=15.0,
        )
        assert mf.connected_complaints == 0  # default

    def test_atm_prediction_request(self):
        from api.schemas.request import ATMPredictionRequest, SpatialFeatures, TemporalFeatures

        req = ATMPredictionRequest(
            spatial=SpatialFeatures(lat=12.97, lon=77.60, dist_metro=0.5, dist_police=2.3),
            temporal=TemporalFeatures(hour=14, day=3, is_weekend=False, time_since_complaint=2.5),
            top_k=5,
        )
        assert req.top_k == 5

    def test_atm_prediction_response(self):
        from api.schemas.response import ATMPredictionResponse, ATMPredictionItem

        resp = ATMPredictionResponse(
            predictions=[
                ATMPredictionItem(atm_index=42, probability=0.85),
                ATMPredictionItem(atm_index=17, probability=0.12),
            ],
            top_k=2,
        )
        assert len(resp.predictions) == 2

    def test_mule_detection_response(self):
        from api.schemas.response import MuleDetectionResponse

        resp = MuleDetectionResponse(
            account_id="M0001_1",
            gnn_probability=0.87,
            rule_score=72.0,
            final_score=82.5,
            risk_level="HIGH",
            risk_color="red",
            action="Immediate Freeze + Step-Up Verification",
        )
        assert resp.risk_level == "HIGH"

    def test_health_response(self):
        from api.schemas.response import HealthResponse

        resp = HealthResponse(
            status="healthy",
            models_loaded={"spatio_temporal": True, "mule_detection": False},
            version="1.0.0",
        )
        assert resp.status == "healthy"


class TestLLMIntegration:
    """Test LLM fallback (rule-based) intent detection."""

    def test_detect_complaint_intent(self):
        from api.llm_integration import LLMService

        svc = LLMService()
        intent, conf = svc.detect_intent("I was cheated, someone stole my money via UPI")
        assert intent == "COMPLAINT"

    def test_detect_status_intent(self):
        from api.llm_integration import LLMService

        svc = LLMService()
        intent, _ = svc.detect_intent("What is the status update on case C1001? Track progress please.")
        assert intent == "STATUS"

    def test_detect_emergency_intent(self):
        from api.llm_integration import LLMService

        svc = LLMService()
        intent, _ = svc.detect_intent("Someone is withdrawing my money right now, urgent!")
        assert intent == "EMERGENCY"

    def test_detect_tip_intent(self):
        from api.llm_integration import LLMService

        svc = LLMService()
        intent, _ = svc.detect_intent("How to protect myself from UPI fraud?")
        assert intent == "TIP"

    def test_fallback_response_generation(self):
        from api.llm_integration import LLMService

        svc = LLMService()
        response = svc.generate_response("help me", "HELP")
        assert "I can help" in response


class TestModelLoader:
    """Test the model registry without real model files."""

    def test_registry_creation(self):
        from api.utils.model_loader import ModelRegistry

        reg = ModelRegistry()
        assert reg.spatial_model is None
        assert reg.mule_model is None
        assert not reg.is_stm_ready
        assert not reg.is_gnn_ready

    def test_status_when_no_models(self):
        from api.utils.model_loader import ModelRegistry

        reg = ModelRegistry()
        status = reg.get_status()
        assert status["spatio_temporal"]["loaded"] is False
        assert status["mule_detection"]["loaded"] is False

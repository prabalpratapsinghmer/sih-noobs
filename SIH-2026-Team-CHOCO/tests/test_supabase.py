"""Tests for Supabase dual-mode cloud service, Realtime broadcasts, and storage."""

import pytest
from api.services.supabase_service import SupabaseService, get_supabase_service


class TestSupabaseService:
    def test_service_initialization(self):
        svc = get_supabase_service()
        assert svc is not None
        status = svc.get_status()
        assert "is_enabled" in status
        assert "storage_bucket" in status

    @pytest.mark.anyio
    async def test_realtime_broadcast_fallback(self):
        svc = SupabaseService()
        # In offline/dev mode, broadcast returns True with debug logging
        success = await svc.broadcast_event(
            channel="police_command",
            event="NEW_HIGH_RISK_MULE",
            payload={"account_id": "ACC-998822", "risk_score": 0.94},
        )
        assert success is True

    @pytest.mark.anyio
    async def test_evidence_storage_fallback(self):
        svc = SupabaseService()
        # Should gracefully save to local disk if remote Supabase not connected
        test_bytes = b"Sample FIR evidence PDF content for verification"
        result = await svc.upload_evidence_file(
            file_bytes=test_bytes,
            filename="fir_sample_test.pdf",
            content_type="application/pdf",
        )
        assert "storage" in result
        assert result["filename"] == "fir_sample_test.pdf"
        assert "url" in result

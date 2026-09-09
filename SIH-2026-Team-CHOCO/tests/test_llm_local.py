"""Tests for Adaptive LLM Provider, zero-cost deterministic extractor, and FIR generation."""

import pytest
from api.services.llm_local import AdaptiveLLMProvider, get_llm_provider


class TestLLMLocal:
    def test_deterministic_entity_extraction(self):
        provider = get_llm_provider()
        narrative = (
            "I received a call claiming my electricity bill was pending. The officer told me to pay "
            "Rs. 24,500 immediately to powerofficer@oksbi or my connection would be cut off. "
            "He also contacted me from mobile 9876543210."
        )

        entities = provider.extract_deterministic_entities(narrative)

        assert entities["defrauded_amount"] == 24500.0
        assert "powerofficer@oksbi" in entities["suspect_upis"]
        assert "9876543210" in entities["suspect_phones"]
        assert entities["fraud_type"] == "ELECTRICITY_BILL"
        assert "66D" in entities["applicable_sections"]

    @pytest.mark.anyio
    async def test_fir_draft_generation(self):
        provider = get_llm_provider()
        complaint = {
            "complaint_id": "CMP-20260905-T100",
            "victim_name": "Ramesh Kumar",
            "victim_phone": "9811002233",
            "description": "Lost INR 75,000 in a Telegram task scam promising returns for YouTube video ratings. Paid to upitask@paytm.",
        }

        fir_text = await provider.generate_fir_draft(complaint)

        assert "FIRST INFORMATION REPORT" in fir_text
        assert "CMP-20260905-T100" in fir_text
        assert "Ramesh Kumar" in fir_text
        assert "TASK_SCAM" in fir_text

    @pytest.mark.anyio
    async def test_whatsapp_reply_financial_alert(self):
        provider = get_llm_provider()
        reply = await provider.whatsapp_chat_reply("I was cheated of Rs 40000 by a fake lottery app, suspect UPI winner@ybl")

        assert "Cybercrime Emergency Alert" in reply
        assert "1930" in reply
        assert "40,000.00" in reply

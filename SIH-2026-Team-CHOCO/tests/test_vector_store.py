"""Unit and integration tests for Qdrant Vector Store and MO semantic matching."""

import pytest
from api.services.vector_store import QdrantVectorStore, generate_text_embedding, EMBEDDING_DIM


class TestVectorStore:
    def test_embedding_generation(self):
        text = "Victim received SMS regarding electricity bill disconnection and downloaded APK."
        vec = generate_text_embedding(text)
        assert len(vec) == EMBEDDING_DIM
        # Check normalization (norm should be ~1.0)
        norm = sum(x ** 2 for x in vec) ** 0.5
        assert abs(norm - 1.0) < 1e-3

    def test_embedding_determinism(self):
        text = "Telegram part-time job scam offering daily returns on YouTube likes."
        vec1 = generate_text_embedding(text)
        vec2 = generate_text_embedding(text)
        assert vec1 == vec2

    @pytest.mark.anyio
    async def test_index_and_search_complaints(self):
        store = QdrantVectorStore()
        # Force local mode for unit testing
        store.is_connected = False

        # Index test complaints
        await store.index_complaint(
            complaint_id="CMP-TEST-001",
            fraud_type="ELECTRICITY_BILL",
            description="Power will be disconnected tonight. Call officer at 9876543210 to update KYC.",
            amount=15400.0,
            suspect_upi="powerofficer@oksbi",
        )

        await store.index_complaint(
            complaint_id="CMP-TEST-002",
            fraud_type="TASK_SCAM",
            description="Telegram VIP task group promising 5000 per day for reviewing luxury hotels.",
            amount=85000.0,
            suspect_upi="viptask@ybl",
        )

        # Search with semantic query
        results = await store.search_similar(
            query_text="Urgent electricity power cut SMS asking for immediate bill payment",
            min_score=0.2,
            top_k=5,
        )

        assert len(results) > 0
        top_match = results[0]
        assert top_match["complaint_id"] == "CMP-TEST-001"
        assert top_match["fraud_type"] == "ELECTRICITY_BILL"

    def test_cluster_generation(self):
        store = QdrantVectorStore()
        clusters = store.get_clusters()
        assert isinstance(clusters, list)

    def test_stats(self):
        store = QdrantVectorStore()
        stats = store.get_stats()
        assert "engine" in stats
        assert stats["vector_dimension"] == EMBEDDING_DIM

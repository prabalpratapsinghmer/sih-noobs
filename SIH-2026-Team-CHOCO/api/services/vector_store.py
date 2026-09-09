"""Qdrant Vector Database Service for Cybercrime Modus Operandi (MO) & Case Similarity.

Features:
- Enterprise vector indexing for victim complaints, suspect patterns, and scam signatures.
- Semantic dense embeddings for cybercrime descriptions (phishing, APK scams, digital arrest, etc.).
- Cosine similarity search for duplicate FIR detection and syndicate attribution.
- Resilient dual-mode: connects to remote Qdrant Docker container or operates in-memory.
"""

import hashlib
import re
from typing import Any, Dict, List, Optional
import numpy as np
from loguru import logger

from api.config import get_settings

settings = get_settings()

# Dimension for cybercrime semantic feature vectors
EMBEDDING_DIM = 128

# Cybercrime domain vocabulary for semantic projection
CYBERCRIME_VOCAB = [
    "electricity", "bill", "power", "disconnection", "officer", "kyc", "update", "bank",
    "otp", "sms", "link", "apk", "malware", "anydesk", "teamviewer", "screen", "share",
    "telegram", "task", "youtube", "like", "subscribe", "crypto", "investment", "returns",
    "part-time", "job", "vip", "recharge", "wallet", "upi", "qr", "code", "scan", "refund",
    "lottery", "prize", "gift", "customs", "parcel", "courier", "fedex", "drugs", "police",
    "cbi", "ed", "digital", "arrest", "skype", "video", "call", "warrant", "court",
    "sextortion", "nude", "video", "blackmail", "facebook", "instagram", "loan", "instant",
    "harassment", "contacts", "gallery", "fake", "customer", "care", "helpline", "google",
    "ad", "fraud", "mule", "transfer", "immediate", "cash", "atm", "withdrawal", "card",
    "clone", "sim", "swap", "esim", "phishing", "vishing", "smishing", "spoofing", "hacked",
    "unauthorized", "debit", "credit", "insurance", "policy", "bonus", "matrimonial", "shaadi",
    "dating", "tinder", "romance", "honeytrap", "gaming", "betting", "casino", "app"
]


def generate_text_embedding(text: str, dim: int = EMBEDDING_DIM) -> List[float]:
    """Generate normalized dense semantic embedding vector for cybercrime text.
    
    Combines domain-specific vocabulary weightings with character n-gram hashing
    to create reproducible, high-signal 128-d vectors without external bulky model weights.
    """
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    words = cleaned.split()
    
    vec = np.zeros(dim, dtype=np.float32)
    
    # 1. Domain vocabulary projection (first 64 dimensions)
    vocab_dim = min(64, len(CYBERCRIME_VOCAB))
    for i, vocab_term in enumerate(CYBERCRIME_VOCAB[:vocab_dim]):
        count = sum(1 for w in words if vocab_term in w)
        if count > 0:
            vec[i] += float(count * 2.5)
            
    # 2. Hashing projection for broad semantic spread (remaining dimensions)
    for word in words:
        h = int(hashlib.md5(word.encode()).hexdigest(), 16)
        target_idx = (h % (dim - vocab_dim)) + vocab_dim
        weight = 1.0 / (len(word) ** 0.5)
        vec[target_idx] += weight
        
    # L2 normalization
    norm = np.linalg.norm(vec)
    if norm > 1e-6:
        vec = vec / norm
    else:
        vec = np.ones(dim, dtype=np.float32) / np.sqrt(dim)
        
    return vec.tolist()


class QdrantVectorStore:
    """Manages Qdrant vector database connection and semantic MO search."""

    def __init__(self):
        self.collection_name = settings.qdrant_collection
        self.client = None
        self.is_connected = False
        self._local_storage: Dict[str, Dict[str, Any]] = {}
        self._initialize()

    def _initialize(self):
        """Connect to Qdrant cluster or initialize in-memory fallback."""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models as qmodels

            try:
                # Attempt connection to configured Qdrant daemon
                self.client = QdrantClient(
                    host=settings.qdrant_host,
                    port=settings.qdrant_port,
                    api_key=settings.qdrant_api_key or None,
                    timeout=2.0,
                )
                # Check server connection
                self.client.get_collections()
                self.is_connected = True
                logger.info(f"✓ Connected to live Qdrant cluster at {settings.qdrant_host}:{settings.qdrant_port}")

                # Ensure collection exists
                collections = [c.name for c in self.client.get_collections().collections]
                if self.collection_name not in collections:
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=qmodels.VectorParams(
                            size=EMBEDDING_DIM,
                            distance=qmodels.Distance.COSINE,
                        ),
                    )
                    logger.info(f"Created Qdrant collection: {self.collection_name}")
            except Exception as conn_err:
                logger.warning(
                    f"Remote Qdrant unavailable ({conn_err}). Falling back to local in-memory vector store."
                )
                self.client = None
                self.is_connected = False
        except ImportError:
            logger.info("qdrant-client not installed; running in-memory vector engine.")
            self.client = None
            self.is_connected = False

    async def index_complaint(
        self,
        complaint_id: str,
        fraud_type: str,
        description: str,
        amount: float,
        suspect_upi: Optional[str] = None,
        suspect_phone: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Index a cybercrime complaint into vector space."""
        full_text = f"{fraud_type} {description} {suspect_upi or ''} {suspect_phone or ''}"
        vector = generate_text_embedding(full_text)

        payload = {
            "complaint_id": complaint_id,
            "fraud_type": fraud_type,
            "description": description[:500],
            "amount": amount,
            "suspect_upi": suspect_upi,
            "suspect_phone": suspect_phone,
            "metadata": metadata or {},
        }

        # Remote Qdrant write
        if self.is_connected and self.client is not None:
            try:
                from qdrant_client.http import models as qmodels
                # Hash complaint_id to numeric or uuid
                point_id = int(hashlib.md5(complaint_id.encode()).hexdigest()[:15], 16)
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=[
                        qmodels.PointStruct(
                            id=point_id,
                            vector=vector,
                            payload=payload,
                        )
                    ],
                )
            except Exception as e:
                logger.warning(f"Error upserting to remote Qdrant: {e}. Storing locally.")

        # Local storage mirror for zero-failure resiliency
        self._local_storage[complaint_id] = {
            "id": complaint_id,
            "vector": vector,
            "payload": payload,
        }

        return {
            "status": "indexed",
            "complaint_id": complaint_id,
            "collection": self.collection_name,
            "vector_dim": len(vector),
            "remote_synced": self.is_connected,
        }

    async def search_similar(
        self,
        query_text: str,
        fraud_type: Optional[str] = None,
        top_k: int = 5,
        min_score: float = 0.3,
    ) -> List[Dict[str, Any]]:
        """Search complaints with similar Modus Operandi (MO) using cosine similarity."""
        query_vector = np.array(generate_text_embedding(query_text), dtype=np.float32)
        results = []

        # 1. If remote Qdrant is connected, execute vector search query
        if self.is_connected and self.client is not None:
            try:
                hits = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector.tolist(),
                    limit=top_k,
                    score_threshold=min_score,
                )
                for hit in hits:
                    results.append({
                        "complaint_id": hit.payload.get("complaint_id"),
                        "similarity_score": round(float(hit.score), 4),
                        "fraud_type": hit.payload.get("fraud_type"),
                        "description": hit.payload.get("description"),
                        "suspect_upi": hit.payload.get("suspect_upi"),
                        "amount": hit.payload.get("amount"),
                    })
                if results:
                    return results
            except Exception as e:
                logger.warning(f"Remote Qdrant search failed ({e}); querying in-memory store.")

        # 2. Local cosine similarity fallback
        for cid, item in self._local_storage.items():
            candidate_vec = np.array(item["vector"], dtype=np.float32)
            cosine_sim = float(np.dot(query_vector, candidate_vec))

            # Optional fraud type filter
            if fraud_type and item["payload"].get("fraud_type") != fraud_type:
                continue

            if cosine_sim >= min_score:
                results.append({
                    "complaint_id": cid,
                    "similarity_score": round(cosine_sim, 4),
                    "fraud_type": item["payload"].get("fraud_type"),
                    "description": item["payload"].get("description"),
                    "suspect_upi": item["payload"].get("suspect_upi"),
                    "amount": item["payload"].get("amount"),
                })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

    def get_clusters(self) -> List[Dict[str, Any]]:
        """Group indexed complaints into emergent Modus Operandi syndicates."""
        groups: Dict[str, List[str]] = {}
        for cid, item in self._local_storage.items():
            ft = item["payload"].get("fraud_type") or "UNKNOWN"
            groups.setdefault(ft, []).append(cid)

        clusters = []
        for ft, cids in groups.items():
            clusters.append({
                "cluster_name": f"{ft.upper()} Syndicate Pattern",
                "fraud_type": ft,
                "case_count": len(cids),
                "sample_case_ids": cids[:5],
            })
        return clusters

    def get_stats(self) -> Dict[str, Any]:
        """Return vector database metrics."""
        return {
            "engine": "Qdrant Vector Engine",
            "is_connected_to_remote": self.is_connected,
            "collection_name": self.collection_name,
            "vector_dimension": EMBEDDING_DIM,
            "total_indexed_complaints": len(self._local_storage),
        }


# Global singleton instance
_vector_store = None


def get_vector_store() -> QdrantVectorStore:
    """Get or create singleton QdrantVectorStore."""
    global _vector_store
    if _vector_store is None:
        _vector_store = QdrantVectorStore()
    return _vector_store

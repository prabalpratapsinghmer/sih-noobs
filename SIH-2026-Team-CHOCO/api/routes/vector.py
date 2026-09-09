"""Vector Search API routes — Qdrant Modus Operandi (MO) & Case Similarity."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from api.services.vector_store import get_vector_store

router = APIRouter()


class IndexComplaintRequest(BaseModel):
    complaint_id: str = Field(..., description="Unique complaint ID (e.g. CMP-20260905-A1B2C3)")
    fraud_type: str = Field(..., description="Classification category (e.g. UPI_PHISHING, TASK_SCAM)")
    description: str = Field(..., description="Detailed narrative of the incident")
    amount: float = Field(default=0.0, description="Defrauded amount in INR")
    suspect_upi: Optional[str] = Field(None, description="Suspect UPI handle if available")
    suspect_phone: Optional[str] = Field(None, description="Suspect phone number if available")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class VectorSearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query or suspect MO description")
    fraud_type: Optional[str] = Field(None, description="Optional filter by fraud category")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of nearest neighbors to return")
    min_score: float = Field(default=0.25, ge=0.0, le=1.0, description="Minimum cosine similarity score")


@router.post("/index", tags=["Vector Search"])
async def index_complaint_endpoint(request: IndexComplaintRequest):
    """Index a cybercrime complaint's Modus Operandi into Qdrant vector space."""
    store = get_vector_store()
    try:
        result = await store.index_complaint(
            complaint_id=request.complaint_id,
            fraud_type=request.fraud_type,
            description=request.description,
            amount=request.amount,
            suspect_upi=request.suspect_upi,
            suspect_phone=request.suspect_phone,
            metadata=request.metadata,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector indexing failed: {str(e)}")


@router.post("/search", tags=["Vector Search"])
async def search_similar_endpoint(request: VectorSearchRequest):
    """Search for cases with similar Modus Operandi across jurisdictional boundaries."""
    store = get_vector_store()
    try:
        matches = await store.search_similar(
            query_text=request.query,
            fraud_type=request.fraud_type,
            top_k=request.top_k,
            min_score=request.min_score,
        )
        return {
            "query": request.query,
            "total_matches": len(matches),
            "results": matches,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector search failed: {str(e)}")


@router.get("/clusters", tags=["Vector Search"])
async def get_clusters_endpoint():
    """Retrieve emergent Modus Operandi syndicate clusters."""
    store = get_vector_store()
    clusters = store.get_clusters()
    return {
        "total_clusters": len(clusters),
        "clusters": clusters,
    }


@router.get("/stats", tags=["Vector Search"])
async def get_stats_endpoint():
    """Retrieve Qdrant vector store connection status and collection statistics."""
    store = get_vector_store()
    return store.get_stats()

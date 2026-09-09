"""FastAPI Unified Enterprise Gateway for SIH26184 Cybercrime Prediction System.

Features:
- Unified /api/v1 routing for all 17 sub-modules (Police, Victim, ML, Banking, Blockchain, etc.)
- OpenTelemetry Distributed Tracing with X-Trace-ID response headers
- Prometheus Metrics exposition at /metrics
- High-Performance Model Serving Engine with Multi-Tier Memory + Redis Caching
- Qdrant Vector Database Integration for Modus Operandi (MO) semantic case search
- Supabase Dual-Mode Cloud & Realtime Broadcast Support
- Resilient local & offline fallbacks across all services
"""

import os
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import torch
import yaml
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# Ensure root path is accessible
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.config import get_settings
from api.metrics import MetricsMiddleware, metrics_endpoint
from api.middleware.rate_limit import RateLimitMiddleware
from api.observability.tracing import TracingMiddleware, trace_span
from api.routes import api_router
from api.services.supabase_service import get_supabase_service
from api.services.vector_store import get_vector_store
from models.mule_detection.model import HybridMuleScorer, MuleDetectionGNN
from models.serving.inference_engine import ModelServingEngine
from models.spatio_temporal.model import SpatioTemporalTransformer

settings = get_settings()

# Global model & serving engine references
spatial_model = None
mule_model = None
scalers = None
label_encoders = None
config = {}
serving_engine: Optional[ModelServingEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: loads configurations, ML weights, and warms up serving engine."""
    global spatial_model, mule_model, scalers, label_encoders, config, serving_engine

    logger.info("Initializing SIH26184 Enterprise Backend Services...")

    # 1. Load config.yaml if present
    config_path = Path("config/config.yaml")
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = {
            "data": {"processed_dir": "data/processed"},
            "models": {
                "spatio_temporal": {"num_atms": 500},
                "mule_detection": {"in_channels": 9, "hidden_channels": 64, "out_channels": 2},
            },
            "training": {
                "spatio_temporal": {"checkpoint": {"save_dir": "models/spatio_temporal/checkpoints"}},
                "mule_detection": {"checkpoint": {"save_dir": "models/mule_detection/checkpoints"}},
            },
        }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Target execution hardware: {device}")

    # 2. Instantiate Serving Engine
    serving_engine = ModelServingEngine(config)

    # 3. Load pre-trained scalers and encoders if available
    processed_dir = Path(config.get("data", {}).get("processed_dir", "data/processed"))
    try:
        spatial_scaler_path = processed_dir / "spatial_scaler.joblib"
        temporal_scaler_path = processed_dir / "temporal_scaler.joblib"
        encoders_path = processed_dir / "label_encoders.joblib"

        if spatial_scaler_path.exists() and temporal_scaler_path.exists():
            spatial_scaler = joblib.load(spatial_scaler_path)
            temporal_scaler = joblib.load(temporal_scaler_path)
            scalers = {"spatial": spatial_scaler, "temporal": temporal_scaler}
            if encoders_path.exists():
                label_encoders = joblib.load(encoders_path)
            logger.info("[OK] Data scalers loaded successfully.")
    except Exception as e:
        logger.warning(f"Note loading scalers: {e}")

    # 4. Load Spatio-Temporal Transformer Checkpoint
    try:
        st_save_dir = Path(config.get("training", {}).get("spatio_temporal", {}).get("checkpoint", {}).get("save_dir", "models/spatio_temporal/checkpoints"))
        st_checkpoint = st_save_dir / "best_model.pth"
        if st_checkpoint.exists():
            logger.info("Loading Spatio-Temporal Transformer...")
            spatial_model = SpatioTemporalTransformer(config["models"]["spatio_temporal"])
            checkpoint = torch.load(st_checkpoint, map_location=device, weights_only=False)
            spatial_model.load_state_dict(checkpoint["model_state_dict"])
            spatial_model = spatial_model.to(device)
            spatial_model.eval()
            logger.info(f"[OK] Spatio-Temporal model loaded (Epoch {checkpoint.get('epoch', 1)})")
        else:
            logger.info("Spatio-Temporal model checkpoint not found at path (simulated mode available).")
    except Exception as e:
        logger.warning(f"Error loading Spatio-Temporal model: {e}")

    # 5. Load Mule Detection GNN Checkpoint
    gnn_data = None
    try:
        gnn_save_dir = Path(config.get("training", {}).get("mule_detection", {}).get("checkpoint", {}).get("save_dir", "models/mule_detection/checkpoints"))
        gnn_checkpoint = gnn_save_dir / "best_model.pth"
        gnn_data_path = processed_dir / "gnn_data.pt"

        if gnn_checkpoint.exists():
            logger.info("Loading Mule Detection GNN...")
            mule_model = MuleDetectionGNN(config["models"]["mule_detection"])
            checkpoint = torch.load(gnn_checkpoint, map_location=device, weights_only=False)
            mule_model.load_state_dict(checkpoint["model_state_dict"])
            mule_model = mule_model.to(device)
            mule_model.eval()

            if gnn_data_path.exists():
                gnn_data = torch.load(gnn_data_path, map_location=device, weights_only=False)
            logger.info(f"[OK] Mule Detection GNN loaded (Epoch {checkpoint.get('epoch', 1)})")
        else:
            logger.info("Mule GNN model checkpoint not found at path.")
    except Exception as e:
        logger.warning(f"Error loading Mule Detection GNN: {e}")

    # 6. Initialize Hybrid Mule Scorer
    hybrid_scorer = None
    try:
        hybrid_scorer = HybridMuleScorer(config)
    except Exception as e:
        logger.warning(f"Note initializing Hybrid Scorer: {e}")

    # Register into Model Serving Engine
    serving_engine.load_models(
        spatial_model=spatial_model,
        mule_model=mule_model,
        scalers=scalers or {},
        label_encoders=label_encoders,
        gnn_data=gnn_data,
        hybrid_scorer=hybrid_scorer,
    )

    # 7. Initialize Database, Vector Store & Supabase singletons
    try:
        from api.database.postgres import init_postgres, close_postgres
        from api.database.neo4j import init_neo4j, close_neo4j
        await init_postgres()
        await init_neo4j()
    except Exception as e:
        logger.warning(f"Database initialization note: {e}")

    get_vector_store()
    get_supabase_service()

    logger.info("[OK] All SIH26184 backend services and modern engines ready.")

    yield

    logger.info("Shutting down SIH26184 backend services...")
    try:
        await close_postgres()
        await close_neo4j()
    except Exception:
        pass


# Initialize FastAPI App
app = FastAPI(
    title="SIH26184 - Cybercrime Prediction & Money Mule Detection System",
    description="Predictive Analytics Framework for Cybercrime Complaints (NCRP Integration)",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# 1. Tracing Middleware (OpenTelemetry)
app.add_middleware(TracingMiddleware)

# 2. Prometheus Metrics Middleware
app.add_middleware(MetricsMiddleware)

# 3. Distributed Rate Limiting Middleware
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=settings.rate_limit_per_ip,
    burst=50,
)

# 4. CORS Middleware — Configured for seamless frontend integration (Next.js, Vite, React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:8080", "http://localhost:4173"],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Trace-ID", "X-Span-ID"],
)

# Expose Prometheus Metrics Endpoint
app.add_route("/metrics", metrics_endpoint, methods=["GET"], include_in_schema=False)

# Mount Unified API Router (/api/v1)
app.include_router(api_router, prefix="/api/v1")


# --- Root Landing View ---
@app.get("/", response_class=HTMLResponse, tags=["General"])
async def root_dashboard():
    """Interactive Landing Dashboard for SIH26184 Backend Gateway."""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>SIH26184 Cybercrime Prediction Backend</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b0f19; color: #f1f5f9; margin: 0; padding: 40px; }}
            .container {{ max-width: 960px; margin: 0 auto; }}
            .badge {{ background: #22c55e; color: #052e16; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 13px; }}
            .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; margin-top: 20px; }}
            h1 {{ font-size: 28px; margin-bottom: 8px; color: #38bdf8; }}
            p {{ color: #94a3b8; font-size: 15px; line-height: 1.6; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 16px; }}
            .item {{ background: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #1e293b; }}
            .item h3 {{ margin: 0 0 6px 0; font-size: 15px; color: #e2e8f0; }}
            .item p {{ margin: 0; font-size: 13px; color: #64748b; }}
            a.btn {{ display: inline-block; background: #0284c7; color: #fff; text-decoration: none; padding: 10px 18px; border-radius: 6px; font-weight: 600; margin-right: 12px; margin-top: 12px; }}
            a.btn:hover {{ background: #0369a1; }}
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">SYSTEM ONLINE • ENTERPRISE STACK ACTIVE</span>
            <h1>SIH26184: Predictive Analytics Framework</h1>
            <p>High-Throughput Cybercrime Complaint Ingestion, Mule Network Traversal, and Spatio-Temporal ATM Location Predictor.</p>
            
            <div>
                <a href="/docs" class="btn">OpenAPI Swagger UI (/docs)</a>
                <a href="/metrics" class="btn" style="background:#475569;">Prometheus Metrics (/metrics)</a>
                <a href="/api/v1/vector/stats" class="btn" style="background:#059669;">Qdrant Vector Engine</a>
            </div>

            <div class="card">
                <h2 style="font-size:18px; margin:0 0 12px 0;">Integrated Enterprise Modules (/api/v1)</h2>
                <div class="grid">
                    <div class="item"><h3>🎯 Spatio-Temporal AI</h3><p>Transformer ATM prediction & location ranking</p></div>
                    <div class="item"><h3>🕸️ GNN Mule Detection</h3><p>GraphSAGE mule transaction clustering</p></div>
                    <div class="item"><h3>⚡ Qdrant Vector DB</h3><p>Semantic Modus Operandi (MO) similarity</p></div>
                    <div class="item"><h3>☁️ Supabase Cloud</h3><p>Realtime broadcast alerts & evidence bucket</p></div>
                    <div class="item"><h3>🚀 Redis / Dragonfly</h3><p>Sub-millisecond inference cache & rate limiter</p></div>
                    <div class="item"><h3>🔍 OpenTelemetry</h3><p>Distributed tracing across PostgreSQL & Neo4j</p></div>
                    <div class="item"><h3>🔄 Prefect Orchestration</h3><p>Drift detection & automated weekly retraining</p></div>
                    <div class="item"><h3>🤖 Offline LLM Engine</h3><p>Zero-cost WhatsApp triage & FIR generation</p></div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


# --- Health & Readiness Endpoints ---
class HealthResponse(BaseModel):
    status: str
    version: str
    models_loaded: Dict[str, bool]
    vector_db_ready: bool
    supabase_configured: bool
    uptime_seconds: float


_start_time = time.time()


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Detailed health probe checking core models, vector store, and cloud integrations."""
    store = get_vector_store()
    supa = get_supabase_service()

    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        models_loaded={
            "spatio_temporal": spatial_model is not None,
            "mule_detection": mule_model is not None,
        },
        vector_db_ready=store is not None,
        supabase_configured=supa.is_enabled,
        uptime_seconds=round(time.time() - _start_time, 2),
    )


# --- Root-Level Predictions (Backwards Compatibility) ---
class SpatialFeatures(BaseModel):
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    dist_metro: float = Field(..., description="Distance to nearest metro station (km)")
    dist_police: float = Field(..., description="Distance to nearest police station (km)")


class TemporalFeatures(BaseModel):
    hour: int = Field(..., ge=0, le=23, description="Hour of day (0-23)")
    day: int = Field(..., ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)")
    is_weekend: bool = Field(..., description="Whether it's a weekend")
    time_since_complaint: float = Field(..., description="Hours since complaint filed")
    fraud_spike_hour: int = Field(..., ge=0, le=23, description="Hour with highest fraud activity")


class STMPredictionRequest(BaseModel):
    spatial: SpatialFeatures
    temporal: TemporalFeatures
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top predictions")


class MuleFeatures(BaseModel):
    velocity: float = Field(..., description="Transactions per hour")
    inflow: float = Field(..., description="Total inflow amount")
    outflow: float = Field(..., description="Total outflow amount")
    outflow_ratio: float = Field(..., description="Outflow/Inflow ratio")
    holding_time: float = Field(..., description="Average holding time (minutes)")
    connected_complaints: int = Field(..., description="Number of connected complaints")
    suspicious_timing: int = Field(..., description="Number of 2-5 AM transactions")
    in_degree: int = Field(..., description="Incoming transaction count")
    out_degree: int = Field(..., description="Outgoing transaction count")


class MulePredictionRequest(BaseModel):
    features: MuleFeatures
    account_id: Optional[str] = None


@app.post("/predict/stm", tags=["Prediction"])
async def predict_stm_root(request: STMPredictionRequest):
    """Predict ATM withdrawal locations with sub-millisecond cached inference."""
    if serving_engine is None or spatial_model is None:
        # Graceful fallback simulation if weights not loaded
        top_k = request.top_k
        return {
            "predictions": [
                {"atm_index": 42, "probability": 0.7421},
                {"atm_index": 118, "probability": 0.1843},
                {"atm_index": 305, "probability": 0.0736},
            ][:top_k],
            "top_k": top_k,
            "cached": False,
            "simulation": True,
        }

    try:
        async with trace_span("predict_stm", {"top_k": request.top_k}):
            res = await serving_engine.predict_stm_cached(
                spatial_dict=request.spatial.model_dump(),
                temporal_dict=request.temporal.model_dump(),
                top_k=request.top_k,
                ttl_seconds=settings.cache_prediction_ttl,
            )
            return res
    except Exception as e:
        logger.error(f"STM Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/mule", tags=["Mule Detection"])
async def predict_mule_root(request: MulePredictionRequest):
    """Predict mule account risk with hybrid GNN and rule-based scoring."""
    if serving_engine is None or mule_model is None:
        # Heuristic fallback if model checkpoint not present
        feat = request.features.model_dump()
        gnn_prob = 0.82 if feat["velocity"] > 5 or feat["outflow_ratio"] > 0.8 else 0.25
        final_score = gnn_prob
        risk_level = "HIGH" if final_score >= 0.7 else "LOW"
        return {
            "account_id": request.account_id,
            "gnn_probability": gnn_prob,
            "rule_score": 0.75 if risk_level == "HIGH" else 0.20,
            "final_score": final_score,
            "risk_level": risk_level,
            "risk_color": "#E53E3E" if risk_level == "HIGH" else "#38A169",
            "action": "AUTO_FREEZE_INITIATED" if risk_level == "HIGH" else "MANUAL_REVIEW",
            "simulation": True,
        }

    try:
        async with trace_span("predict_mule", {"account_id": request.account_id or ""}):
            res = await serving_engine.predict_mule_cached(
                features_dict=request.features.model_dump(),
                account_id=request.account_id,
                ttl_seconds=settings.cache_mule_ttl,
            )
            return res
    except Exception as e:
        logger.error(f"Mule Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models/info", tags=["General"])
async def models_info():
    """Information on loaded models and serving accelerators."""
    info = {"status": "operational", "serving_engine": "ModelServingEngine v2.0 Enterprise"}
    if spatial_model:
        info["spatio_temporal"] = {
            "model": "SpatioTemporalTransformer",
            "parameters": sum(p.numel() for p in spatial_model.parameters()),
        }
    if mule_model:
        info["mule_detection"] = {
            "model": "MuleDetectionGNN",
            "parameters": sum(p.numel() for p in mule_model.parameters()),
        }
    return info


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
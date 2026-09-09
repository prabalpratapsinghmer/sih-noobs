"""Backend Services Dashboard — Complete monitoring of ALL SIH26184 backend services.

Displays:
  - Infrastructure Services (Redis, Supabase, Qdrant, OTEL, ML Engine, Orchestration, LLM, Metrics)
  - API Route Modules (17 sub-modules under /api/v1)
  - System Information (Python, Torch, Ports, Uptime)
  - FastAPI Health Probe (if the main API on :8000 is running)

Run:  python ruma/services_dashboard.py
Open: http://localhost:5555
"""

import json
import sys
import time
import importlib
import platform
import threading
from pathlib import Path
from datetime import datetime

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# ── Infrastructure Probes ────────────────────────────────────────────────────────

def probe_redis():
    """Probe Redis / Dragonfly cache."""
    try:
        from api.config import get_settings
        import redis.asyncio as aioredis
        import asyncio

        settings = get_settings()

        async def _probe():
            client = aioredis.from_url(
                settings.redis_url, decode_responses=True, socket_connect_timeout=1.0
            )
            try:
                await asyncio.wait_for(client.ping(), timeout=1.0)
                info = await client.info("server")
                return {
                    "status": "connected",
                    "host": settings.redis_host,
                    "port": settings.redis_port,
                    "redis_version": info.get("redis_version", "unknown"),
                    "uptime_seconds": info.get("uptime_in_seconds", 0),
                }
            finally:
                await client.aclose()

        return asyncio.run(_probe())
    except Exception as e:
        from api.config import get_settings
        s = get_settings()
        return {
            "status": "local_fallback",
            "host": s.redis_host,
            "port": s.redis_port,
            "detail": f"Not running ({type(e).__name__})",
            "fallback": "In-memory LRU cache active",
        }


def probe_supabase():
    """Probe Supabase Cloud."""
    try:
        from api.services.supabase_service import get_supabase_service
        svc = get_supabase_service(force_reload=True)
        status = svc.get_status()
        if not status["is_enabled"]:
            status["status"] = "local_mode"
            return status
        import httpx
        t0 = time.time()
        headers = svc._get_headers(use_service_role=True)
        r = httpx.get(f"{svc.url}/auth/v1/health", headers=headers, timeout=3.0)
        lat_ms = round((time.time() - t0) * 1000, 1)
        status["status"] = "connected" if r.status_code == 200 else "degraded"
        status["cloud_response_ms"] = lat_ms
        status["region"] = "ap-south-1 (Mumbai)"
        return status
    except Exception as e:
        return {"status": "error", "detail": str(e)[:120]}


def probe_qdrant():
    """Probe Qdrant vector database."""
    try:
        from api.services.vector_store import get_vector_store
        store = get_vector_store()
        stats = store.get_stats()
        stats["status"] = "connected" if store.is_connected else "in_memory_mode"
        return stats
    except Exception as e:
        return {"status": "error", "detail": str(e)[:120]}


def probe_otel():
    """Probe OpenTelemetry tracing."""
    try:
        from api.observability.tracing import get_tracer
        tracer = get_tracer()
        return {
            "status": "initialized" if tracer else "shim_mode",
            "tracer_type": type(tracer).__name__ if tracer else "LightweightShim",
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)[:120]}


def probe_ml_engine():
    """Probe ML Serving Engine."""
    try:
        import torch
        from models.serving.inference_engine import ModelServingEngine
        engine = ModelServingEngine({})
        status = engine.get_status()
        status["status"] = "operational"
        status["torch_version"] = torch.__version__
        status["device"] = "cuda" if torch.cuda.is_available() else "cpu"
        return status
    except Exception as e:
        return {"status": "error", "detail": str(e)[:120]}


_orch_cache = None
_orch_cache_time = 0

def probe_orchestration():
    """Probe Prefect ML orchestration (cached 5 min)."""
    global _orch_cache, _orch_cache_time
    if _orch_cache and (time.time() - _orch_cache_time) < 300:
        return _orch_cache
    try:
        from orchestration.flows.retraining_flow import run_retraining_pipeline
        result = run_retraining_pipeline(min_records=10, epochs=1)
        res = {
            "status": "operational",
            "pipeline_result": result.get("status"),
            "drift_detected": result.get("drift_summary", {}).get("drift_detected"),
            "drift_score": result.get("drift_summary", {}).get("drift_score"),
            "training_accuracy": result.get("training_summary", {}).get("final_accuracy"),
            "model_promoted": result.get("deployment_summary", {}).get("promoted"),
            "duration_seconds": result.get("duration_seconds"),
        }
        _orch_cache = res
        _orch_cache_time = time.time()
        return res
    except Exception as e:
        return {"status": "error", "detail": str(e)[:120]}


def probe_llm():
    """Probe Local LLM / Offline Triage Engine."""
    try:
        from api.services.llm_local import get_llm_provider
        provider = get_llm_provider()
        entities = provider.extract_deterministic_entities(
            "Lost Rs. 45,000 to bill scam. Fraudster UPI: scam@upi."
        )
        return {
            "status": "operational",
            "provider": "deterministic_offline_engine",
            "fraud_type_detected": entities.get("fraud_type"),
            "amount_detected": entities.get("defrauded_amount"),
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)[:120]}


def probe_metrics():
    """Probe Prometheus metrics."""
    try:
        from api.metrics import generate_latest
        content = generate_latest()
        return {
            "status": "operational",
            "metrics_size_bytes": len(content),
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)[:120]}


def probe_postgres():
    """Probe PostgreSQL connectivity."""
    try:
        from api.config import get_settings
        s = get_settings()
        import psycopg2
        conn = psycopg2.connect(
            host=s.postgres_host, port=s.postgres_port,
            user=s.postgres_user, password=s.postgres_password,
            dbname=s.postgres_db, connect_timeout=2,
        )
        conn.close()
        return {"status": "connected", "host": s.postgres_host, "port": s.postgres_port, "db": s.postgres_db}
    except Exception as e:
        from api.config import get_settings
        s = get_settings()
        return {"status": "offline", "host": s.postgres_host, "port": s.postgres_port, "detail": str(e)[:100]}


def probe_neo4j():
    """Probe Neo4j graph database."""
    try:
        from api.config import get_settings
        s = get_settings()
        import httpx
        r = httpx.get(s.neo4j_http_uri, timeout=2.0)
        return {"status": "connected" if r.status_code == 200 else "degraded", "uri": s.neo4j_uri}
    except Exception as e:
        from api.config import get_settings
        s = get_settings()
        return {"status": "offline", "uri": s.neo4j_uri, "detail": str(e)[:100]}


# ── API Route Module Probes ──────────────────────────────────────────────────────

ROUTE_MODULES = [
    ("predict", "api.routes.predict", "Prediction", "Spatio-Temporal ATM risk prediction endpoints"),
    ("detect", "api.routes.detect", "Mule Detection", "GNN-based mule account detection"),
    ("trigger", "api.routes.trigger", "Proactive Actions", "Auto-freeze, alert cascades, freeze triggers"),
    ("status", "api.routes.status", "Model Status", "ML model health and version info"),
    ("vector", "api.routes.vector", "Vector Search", "Qdrant semantic MO case similarity search"),
    ("orchestration", "api.routes.orchestration", "ML Orchestration", "Prefect retraining pipeline triggers"),
    ("auth", "api.routes.auth", "Authentication", "JWT login, register, token refresh, RBAC"),
    ("admin", "api.routes.admin", "Administration", "System config, user management, audit controls"),
    ("police", "api.routes.police", "Police Command", "Investigation dashboard, case assignment, FIR"),
    ("victim", "api.routes.victim", "Victim Portal", "Complaint filing, tracking, evidence upload"),
    ("banking", "api.routes.banking", "Banking Step-Up", "Account freeze API, transaction hold, KYC"),
    ("blockchain", "api.routes.blockchain", "Blockchain Audit", "Immutable evidence chain, hash verification"),
    ("evidence", "api.routes.evidence", "Evidence & IPFS", "Distributed evidence storage via IPFS/Pinata"),
    ("audit", "api.routes.audit", "Audit Trail", "Tamper-proof action logging and compliance"),
    ("notifications", "api.routes.notifications", "Notifications", "Push, email, SMS alert dispatch"),
    ("whatsapp", "api.routes.whatsapp", "WhatsApp Webhook", "WhatsApp Business API complaint intake"),
    ("llm", "api.routes.llm", "LLM AI Agent", "Offline NLP triage, entity extraction, FIR gen"),
]


def probe_route_module(module_path):
    """Try importing a route module to check availability."""
    try:
        mod = importlib.import_module(module_path)
        router = getattr(mod, "router", None)
        route_count = len(router.routes) if router else 0
        return {"status": "loaded", "routes": route_count}
    except Exception as e:
        return {"status": "import_error", "detail": str(e)[:120]}


def probe_fastapi_health():
    """Try reaching the main FastAPI on port 8000."""
    try:
        import httpx
        r = httpx.get("http://localhost:8000/health", timeout=2.0)
        if r.status_code == 200:
            return {"status": "running", **r.json()}
        return {"status": "degraded", "http_code": r.status_code}
    except Exception:
        return {"status": "not_running", "detail": "FastAPI server not detected on :8000"}


def get_system_info():
    """Gather system information."""
    info = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    try:
        import torch
        info["torch_version"] = torch.__version__
        info["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info["gpu"] = torch.cuda.get_device_name(0)
    except Exception:
        info["torch_version"] = "not installed"
    return info


# ── API Endpoints ────────────────────────────────────────────────────────────────

@app.route("/api/services")
def get_all_services():
    """Full probe of all backend services."""
    start = time.time()

    # Infrastructure
    infra = {
        "redis_cache": probe_redis(),
        "supabase_cloud": probe_supabase(),
        "qdrant_vector_db": probe_qdrant(),
        "opentelemetry": probe_otel(),
        "ml_serving_engine": probe_ml_engine(),
        "ml_orchestration": probe_orchestration(),
        "llm_offline_triage": probe_llm(),
        "prometheus_metrics": probe_metrics(),
        "postgresql": probe_postgres(),
        "neo4j_graph": probe_neo4j(),
    }

    # API Route modules
    routes = {}
    for key, mod_path, tag, desc in ROUTE_MODULES:
        result = probe_route_module(mod_path)
        result["tag"] = tag
        result["description"] = desc
        routes[key] = result

    # FastAPI server
    fastapi = probe_fastapi_health()

    # System
    system = get_system_info()

    # Summaries
    infra_healthy = sum(1 for s in infra.values() if s.get("status") not in ("error", "offline"))
    routes_loaded = sum(1 for r in routes.values() if r.get("status") == "loaded")

    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "infrastructure": infra,
        "api_routes": routes,
        "fastapi_server": fastapi,
        "system": system,
        "summary": {
            "infra_total": len(infra),
            "infra_healthy": infra_healthy,
            "infra_degraded": len(infra) - infra_healthy,
            "routes_total": len(routes),
            "routes_loaded": routes_loaded,
            "routes_failed": len(routes) - routes_loaded,
        },
        "probe_time_seconds": round(time.time() - start, 2),
    }
    return jsonify(report)


# ── Dashboard HTML ───────────────────────────────────────────────────────────────

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIH26184 — Backend Services Monitor</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }

        :root {
            --bg-deep: #050810;
            --bg-base: #0a0f1a;
            --bg-card: #111827;
            --bg-card-hover: #1a2332;
            --bg-elevated: #1e293b;
            --border: #1e293b;
            --border-accent: rgba(99,102,241,0.3);
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-indigo: #6366f1;
            --accent-sky: #38bdf8;
            --accent-green: #22c55e;
            --accent-yellow: #eab308;
            --accent-red: #ef4444;
            --accent-purple: #a855f7;
            --accent-orange: #f97316;
            --accent-cyan: #06b6d4;
            --glow-green: rgba(34,197,94,0.25);
            --glow-red: rgba(239,68,68,0.25);
            --glow-blue: rgba(59,130,246,0.25);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-deep);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* ── Animated background ── */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse 800px 600px at 20% 10%, rgba(99,102,241,0.06), transparent),
                radial-gradient(ellipse 600px 400px at 80% 80%, rgba(56,189,248,0.04), transparent);
            pointer-events: none;
            z-index: 0;
        }

        /* ── Top Bar ── */
        .topbar {
            position: sticky; top: 0; z-index: 100;
            background: rgba(10,15,26,0.85);
            backdrop-filter: blur(20px) saturate(1.6);
            border-bottom: 1px solid var(--border);
            padding: 14px 32px;
            display: flex; align-items: center; justify-content: space-between;
        }
        .topbar-left { display: flex; align-items: center; gap: 16px; }
        .topbar-logo {
            width: 38px; height: 38px; border-radius: 10px;
            background: linear-gradient(135deg, var(--accent-indigo), var(--accent-sky));
            display: flex; align-items: center; justify-content: center;
            font-size: 18px; font-weight: 900; color: #fff;
            box-shadow: 0 4px 20px rgba(99,102,241,0.3);
        }
        .topbar h1 {
            font-size: 17px; font-weight: 800; letter-spacing: -0.3px;
            background: linear-gradient(135deg, #818cf8, #38bdf8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .topbar-subtitle { font-size: 11px; color: var(--text-muted); margin-top: 1px; }
        .topbar-right { display: flex; gap: 12px; align-items: center; }

        .badge {
            padding: 5px 14px; border-radius: 999px;
            font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
            text-transform: uppercase;
            animation: pulse-badge 2.5s ease-in-out infinite;
        }
        @keyframes pulse-badge { 0%,100% { opacity:1; } 50% { opacity:0.75; } }

        .refresh-btn {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: #fff; border: none; padding: 9px 20px; border-radius: 8px;
            cursor: pointer; font-weight: 600; font-size: 12px;
            transition: all 0.2s; position: relative; overflow: hidden;
        }
        .refresh-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(99,102,241,0.35); }
        .refresh-btn:active { transform: scale(0.97); }
        .refresh-btn.loading { pointer-events: none; opacity: 0.7; }

        /* ── Container ── */
        .container { max-width: 1400px; margin: 0 auto; padding: 28px 24px; position: relative; z-index: 1; }

        /* ── Summary Stats ── */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 14px; margin-bottom: 32px;
        }
        .stat-card {
            background: linear-gradient(145deg, var(--bg-card), var(--bg-base));
            border: 1px solid var(--border);
            border-radius: 14px; padding: 20px 16px; text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; overflow: hidden;
        }
        .stat-card::before {
            content: '';
            position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--accent-indigo), var(--accent-sky));
            opacity: 0; transition: opacity 0.3s;
        }
        .stat-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.3); }
        .stat-card:hover::before { opacity: 1; }
        .stat-value {
            font-size: 32px; font-weight: 900; line-height: 1;
            background: linear-gradient(135deg, var(--accent-green), var(--accent-sky));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .stat-value.danger { background: linear-gradient(135deg, var(--accent-red), var(--accent-orange)); -webkit-background-clip: text; }
        .stat-label { font-size: 11px; color: var(--text-muted); margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }

        /* ── Section Headers ── */
        .section-header {
            display: flex; align-items: center; gap: 12px;
            margin: 32px 0 18px 0; padding-bottom: 12px;
            border-bottom: 1px solid rgba(99,102,241,0.15);
        }
        .section-icon {
            width: 36px; height: 36px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 18px;
        }
        .section-icon.infra { background: rgba(99,102,241,0.15); }
        .section-icon.routes { background: rgba(34,197,94,0.15); }
        .section-icon.system { background: rgba(56,189,248,0.15); }
        .section-title { font-size: 16px; font-weight: 700; }
        .section-count { font-size: 12px; color: var(--text-muted); margin-left: auto; }

        /* ── Service Cards Grid ── */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 16px;
        }

        .svc-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        .svc-card:hover {
            border-color: var(--border-accent);
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        }
        .svc-card-header {
            padding: 14px 18px;
            display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid rgba(30,41,59,0.6);
            background: rgba(30,41,59,0.35);
        }
        .svc-card-header h3 {
            font-size: 13px; font-weight: 700;
            display: flex; align-items: center; gap: 8px;
        }
        .svc-card-header .svc-icon { font-size: 18px; }

        .status-dot {
            width: 10px; height: 10px; border-radius: 50%;
            display: inline-block; flex-shrink: 0;
        }
        .dot-green { background: var(--accent-green); box-shadow: 0 0 10px var(--glow-green); }
        .dot-blue { background: #3b82f6; box-shadow: 0 0 10px var(--glow-blue); }
        .dot-yellow { background: var(--accent-yellow); box-shadow: 0 0 10px rgba(234,179,8,0.4); }
        .dot-red { background: var(--accent-red); box-shadow: 0 0 10px var(--glow-red); }

        .svc-card-body { padding: 14px 18px; }

        .tag {
            display: inline-block; padding: 3px 10px; border-radius: 6px;
            font-size: 10px; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.5px; margin-bottom: 10px;
        }
        .tag-green { background: rgba(34,197,94,0.12); color: #4ade80; }
        .tag-blue { background: rgba(59,130,246,0.12); color: #60a5fa; }
        .tag-orange { background: rgba(249,115,22,0.12); color: #fb923c; }
        .tag-red { background: rgba(239,68,68,0.12); color: #f87171; }
        .tag-purple { background: rgba(168,85,247,0.12); color: #c084fc; }

        .svc-detail {
            background: rgba(5,8,16,0.6);
            padding: 10px 12px; border-radius: 8px;
            font-family: 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
            font-size: 11px; color: var(--text-muted); line-height: 1.6;
            white-space: pre-wrap; word-break: break-all;
            max-height: 180px; overflow-y: auto;
        }
        .svc-detail::-webkit-scrollbar { width: 4px; }
        .svc-detail::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }

        /* ── Route module cards (compact) ── */
        .route-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 12px;
        }
        .route-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px 16px;
            display: flex; align-items: flex-start; gap: 12px;
            transition: all 0.25s;
        }
        .route-card:hover { border-color: var(--border-accent); transform: translateY(-2px); }
        .route-dot { margin-top: 4px; flex-shrink: 0; }
        .route-info { flex: 1; }
        .route-name { font-size: 13px; font-weight: 700; margin-bottom: 2px; }
        .route-tag { font-size: 10px; color: var(--accent-sky); font-weight: 600; }
        .route-desc { font-size: 11px; color: var(--text-muted); margin-top: 4px; line-height: 1.4; }
        .route-count { font-size: 10px; color: var(--text-muted); margin-top: 4px; }
        .route-error { font-size: 10px; color: var(--accent-red); margin-top: 4px; }

        /* ── System Info ── */
        .sys-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 14px;
        }
        .sys-item {
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 12px; padding: 16px;
        }
        .sys-item-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 4px; }
        .sys-item-value { font-size: 14px; font-weight: 600; color: var(--text-primary); word-break: break-all; }

        /* ── Loading ── */
        .loading { text-align: center; padding: 80px 20px; }
        .spinner {
            width: 48px; height: 48px;
            border: 3px solid var(--border);
            border-top-color: var(--accent-indigo);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .loading p { color: var(--text-muted); font-size: 14px; }

        /* ── Footer ── */
        .footer {
            text-align: center; padding: 36px 20px 24px;
            color: var(--text-muted); font-size: 11px;
            border-top: 1px solid var(--border); margin-top: 40px;
        }

        /* ── FastAPI card ── */
        .fastapi-card {
            background: linear-gradient(145deg, #0d1520, #111827);
            border: 1px solid var(--border);
            border-radius: 14px; padding: 20px 24px;
            margin-bottom: 28px;
            display: flex; align-items: center; justify-content: space-between;
            gap: 20px;
        }
        .fastapi-left { display: flex; align-items: center; gap: 14px; }
        .fastapi-icon { font-size: 28px; }
        .fastapi-title { font-size: 15px; font-weight: 700; }
        .fastapi-detail { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

        /* ── Animations ── */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-in { animation: fadeInUp 0.4s ease-out both; }

        /* ── Responsive ── */
        @media (max-width: 768px) {
            .topbar { padding: 12px 16px; flex-wrap: wrap; gap: 8px; }
            .container { padding: 16px 12px; }
            .cards-grid { grid-template-columns: 1fr; }
            .route-grid { grid-template-columns: 1fr; }
            .summary-grid { grid-template-columns: repeat(3, 1fr); }
        }
    </style>
</head>
<body>
    <div class="topbar">
        <div class="topbar-left">
            <div class="topbar-logo">S</div>
            <div>
                <h1>SIH26184 Backend Services Monitor</h1>
                <div class="topbar-subtitle">Cybercrime Prediction &amp; Mule Detection System</div>
            </div>
        </div>
        <div class="topbar-right">
            <button class="refresh-btn" id="refresh-btn" onclick="loadServices()">⟳ Refresh All</button>
            <span class="badge" id="overall-badge" style="background:#475569;color:#e2e8f0;">INITIALIZING...</span>
        </div>
    </div>

    <div class="container">
        <!-- Summary Stats -->
        <div class="summary-grid" id="summary-grid">
            <div class="stat-card"><div class="stat-value" id="s-infra">—</div><div class="stat-label">Infra Healthy</div></div>
            <div class="stat-card"><div class="stat-value danger" id="s-infra-down">—</div><div class="stat-label">Infra Down</div></div>
            <div class="stat-card"><div class="stat-value" id="s-routes">—</div><div class="stat-label">Routes Loaded</div></div>
            <div class="stat-card"><div class="stat-value danger" id="s-routes-fail">—</div><div class="stat-label">Routes Failed</div></div>
            <div class="stat-card"><div class="stat-value" id="s-total">—</div><div class="stat-label">Total Services</div></div>
            <div class="stat-card"><div class="stat-value" id="s-time">—</div><div class="stat-label">Probe Time (s)</div></div>
        </div>

        <!-- FastAPI Server -->
        <div class="fastapi-card" id="fastapi-section">
            <div class="fastapi-left">
                <div class="fastapi-icon">⚡</div>
                <div>
                    <div class="fastapi-title">FastAPI Gateway (port 8000)</div>
                    <div class="fastapi-detail" id="fastapi-detail">Checking...</div>
                </div>
            </div>
            <span class="status-dot dot-yellow" id="fastapi-dot"></span>
        </div>

        <!-- Infrastructure Services -->
        <div class="section-header">
            <div class="section-icon infra">🏗️</div>
            <div class="section-title">Infrastructure Services</div>
            <div class="section-count" id="infra-count">—</div>
        </div>
        <div class="cards-grid" id="infra-container">
            <div class="loading"><div class="spinner"></div><p>Probing infrastructure services...</p></div>
        </div>

        <!-- API Routes -->
        <div class="section-header">
            <div class="section-icon routes">🔌</div>
            <div class="section-title">API Route Modules (/api/v1)</div>
            <div class="section-count" id="routes-count">—</div>
        </div>
        <div class="route-grid" id="routes-container">
            <div class="loading"><div class="spinner"></div><p>Scanning route modules...</p></div>
        </div>

        <!-- System Info -->
        <div class="section-header">
            <div class="section-icon system">💻</div>
            <div class="section-title">System Information</div>
        </div>
        <div class="sys-grid" id="system-container">
            <div class="loading"><div class="spinner"></div><p>Gathering system info...</p></div>
        </div>
    </div>

    <div class="footer">
        SIH26184 Predictive Analytics Framework — Backend Services Monitor v3.0<br>
        <span id="last-updated" style="color:#475569;"></span>
    </div>

    <script>
        const INFRA_ICONS = {
            redis_cache: '⚡', supabase_cloud: '☁️', qdrant_vector_db: '🔎',
            opentelemetry: '🔍', ml_serving_engine: '🧠', ml_orchestration: '🔄',
            llm_offline_triage: '🤖', prometheus_metrics: '📊',
            postgresql: '🐘', neo4j_graph: '🕸️'
        };
        const INFRA_LABELS = {
            redis_cache: 'Redis / Dragonfly Cache', supabase_cloud: 'Supabase Cloud & Realtime',
            qdrant_vector_db: 'Qdrant Vector Database', opentelemetry: 'OpenTelemetry Tracing',
            ml_serving_engine: 'ML Serving Engine', ml_orchestration: 'Prefect Orchestration',
            llm_offline_triage: 'Offline LLM Triage', prometheus_metrics: 'Prometheus Metrics',
            postgresql: 'PostgreSQL Database', neo4j_graph: 'Neo4j Graph DB'
        };
        const ROUTE_ICONS = {
            predict: '🎯', detect: '🕵️', trigger: '🚨', status: '📈',
            vector: '🧬', orchestration: '🔄', auth: '🔐', admin: '⚙️',
            police: '👮', victim: '📝', banking: '🏦', blockchain: '⛓️',
            evidence: '📦', audit: '📋', notifications: '🔔', whatsapp: '💬', llm: '🤖'
        };

        function dotClass(status) {
            if (['connected','operational','initialized','configured','running','loaded'].includes(status)) return 'dot-green';
            if (['in_memory_mode','local_mode','local_fallback','shim_mode','offline'].includes(status)) return 'dot-blue';
            if (status === 'degraded' || status === 'not_running') return 'dot-yellow';
            return 'dot-red';
        }
        function tagClass(status) {
            if (['connected','operational','initialized','configured','running','loaded'].includes(status)) return 'tag-green';
            if (['in_memory_mode','local_mode','local_fallback','shim_mode','offline'].includes(status)) return 'tag-blue';
            if (status === 'degraded' || status === 'not_running') return 'tag-orange';
            return 'tag-red';
        }

        function loadServices() {
            const btn = document.getElementById('refresh-btn');
            btn.classList.add('loading');
            btn.textContent = '⟳ Scanning...';

            document.getElementById('infra-container').innerHTML = '<div class="loading"><div class="spinner"></div><p>Probing infrastructure services...</p></div>';
            document.getElementById('routes-container').innerHTML = '<div class="loading"><div class="spinner"></div><p>Scanning route modules...</p></div>';
            document.getElementById('system-container').innerHTML = '<div class="loading"><div class="spinner"></div><p>Gathering system info...</p></div>';

            const badge = document.getElementById('overall-badge');
            badge.textContent = 'SCANNING...';
            badge.style.background = '#eab308';
            badge.style.color = '#422006';

            fetch('/api/services')
                .then(r => r.json())
                .then(data => {
                    const s = data.summary;

                    // Summary stats
                    document.getElementById('s-infra').textContent = s.infra_healthy;
                    document.getElementById('s-infra-down').textContent = s.infra_degraded;
                    document.getElementById('s-routes').textContent = s.routes_loaded;
                    document.getElementById('s-routes-fail').textContent = s.routes_failed;
                    document.getElementById('s-total').textContent = s.infra_total + s.routes_total;
                    document.getElementById('s-time').textContent = data.probe_time_seconds;

                    // Overall badge
                    const totalOk = s.infra_healthy + s.routes_loaded;
                    const totalAll = s.infra_total + s.routes_total;
                    if (s.infra_degraded === 0 && s.routes_failed === 0) {
                        badge.textContent = 'ALL SYSTEMS OPERATIONAL';
                        badge.style.background = '#22c55e'; badge.style.color = '#052e16';
                    } else {
                        badge.textContent = totalOk + '/' + totalAll + ' HEALTHY';
                        badge.style.background = '#eab308'; badge.style.color = '#422006';
                    }

                    // FastAPI
                    const fa = data.fastapi_server;
                    const faDot = document.getElementById('fastapi-dot');
                    const faDetail = document.getElementById('fastapi-detail');
                    faDot.className = 'status-dot ' + dotClass(fa.status);
                    if (fa.status === 'running') {
                        faDetail.textContent = `v${fa.version || '?'} • Uptime: ${Math.round(fa.uptime_seconds || 0)}s • Models: STM=${fa.models_loaded?.spatio_temporal}, GNN=${fa.models_loaded?.mule_detection}`;
                    } else {
                        faDetail.textContent = fa.detail || 'Not detected on port 8000';
                    }

                    // Infrastructure cards
                    let infraHtml = '';
                    let i = 0;
                    for (const [key, svc] of Object.entries(data.infrastructure)) {
                        const icon = INFRA_ICONS[key] || '🔧';
                        const label = INFRA_LABELS[key] || key;
                        const st = svc.status || 'unknown';
                        const detail = JSON.stringify(svc, null, 2);
                        infraHtml += `
                            <div class="svc-card animate-in" style="animation-delay:${i * 60}ms">
                                <div class="svc-card-header">
                                    <h3><span class="svc-icon">${icon}</span> ${label}</h3>
                                    <span class="status-dot ${dotClass(st)}"></span>
                                </div>
                                <div class="svc-card-body">
                                    <span class="tag ${tagClass(st)}">${st.toUpperCase().replace(/_/g,' ')}</span>
                                    <div class="svc-detail">${detail}</div>
                                </div>
                            </div>`;
                        i++;
                    }
                    document.getElementById('infra-container').innerHTML = infraHtml;
                    document.getElementById('infra-count').textContent = s.infra_healthy + '/' + s.infra_total + ' healthy';

                    // Route cards
                    let routeHtml = '';
                    i = 0;
                    for (const [key, route] of Object.entries(data.api_routes)) {
                        const icon = ROUTE_ICONS[key] || '📡';
                        const st = route.status || 'unknown';
                        const routeCount = route.routes || 0;
                        routeHtml += `
                            <div class="route-card animate-in" style="animation-delay:${i * 40}ms">
                                <div class="route-dot"><span class="status-dot ${dotClass(st)}"></span></div>
                                <div class="route-info">
                                    <div class="route-name">${icon} /api/v1/${key}</div>
                                    <div class="route-tag">${route.tag || key}</div>
                                    <div class="route-desc">${route.description || ''}</div>
                                    ${st === 'loaded'
                                        ? `<div class="route-count">${routeCount} endpoint${routeCount !== 1 ? 's' : ''} registered</div>`
                                        : `<div class="route-error">${route.detail || 'Failed to load'}</div>`}
                                </div>
                            </div>`;
                        i++;
                    }
                    document.getElementById('routes-container').innerHTML = routeHtml;
                    document.getElementById('routes-count').textContent = s.routes_loaded + '/' + s.routes_total + ' loaded';

                    // System info
                    const sys = data.system;
                    let sysHtml = '';
                    const sysItems = [
                        ['Python Version', sys.python_version],
                        ['PyTorch', sys.torch_version + (sys.cuda_available ? ' (CUDA ✓)' : ' (CPU)')],
                        ['Platform', sys.platform],
                        ['Machine', sys.machine],
                        ['GPU', sys.gpu || 'None (CPU mode)'],
                        ['Probe Time', data.timestamp],
                    ];
                    sysItems.forEach(([label, value], idx) => {
                        sysHtml += `
                            <div class="sys-item animate-in" style="animation-delay:${idx * 60}ms">
                                <div class="sys-item-label">${label}</div>
                                <div class="sys-item-value">${value || '—'}</div>
                            </div>`;
                    });
                    document.getElementById('system-container').innerHTML = sysHtml;
                    document.getElementById('last-updated').textContent = 'Last updated: ' + new Date().toLocaleTimeString();

                    btn.classList.remove('loading');
                    btn.textContent = '⟳ Refresh All';
                })
                .catch(err => {
                    document.getElementById('infra-container').innerHTML = `<div class="loading"><p style="color:#ef4444;">Error: ${err.message}</p></div>`;
                    btn.classList.remove('loading');
                    btn.textContent = '⟳ Refresh All';
                    badge.textContent = 'ERROR';
                    badge.style.background = '#ef4444'; badge.style.color = '#fff';
                });
        }

        // Auto-load on page open
        loadServices();
    </script>
</body>
</html>"""


@app.route("/")
def index():
    return Response(DASHBOARD_HTML, mimetype="text/html")


if __name__ == "__main__":
    print("=" * 70)
    print("  SIH26184 BACKEND SERVICES MONITOR")
    print("  Open in browser: http://localhost:5555")
    print("  JSON API:        http://localhost:5555/api/services")
    print("=" * 70)
    app.run(host="0.0.0.0", port=5555, debug=False)

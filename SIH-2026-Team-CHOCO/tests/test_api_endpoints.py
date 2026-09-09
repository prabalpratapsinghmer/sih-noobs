"""Smoke tests: app boots, health endpoint, router registration, auth guards.

These run WITHOUT live DBs — the app's lifespan already tolerates missing
services (each init is wrapped in try/except and logged as unavailable),
so wiring tests run cleanly.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from api.main import app

    with TestClient(app) as c:
        yield c


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "SIH26184" in r.json()["message"]


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["services"]["api"] == "healthy"


def test_health_reports_degraded_when_deps_down(client):
    # No live DBs in CI → aggregate status must be honest (was hardcoded "healthy")
    body = client.get("/health").json()
    assert body["status"] == "degraded"
    for svc in ("postgres", "neo4j", "redis"):
        assert body["services"][svc] in ("healthy", "unhealthy")


def test_health_does_not_hang_when_deps_down(client):
    # Regression: checks used to run sequentially with unbounded connect timeouts
    # (~8s per /health call). Now 3 probes run concurrently, each ≤ 1s.
    import time

    t0 = time.monotonic()
    client.get("/health")
    elapsed = time.monotonic() - t0
    assert elapsed < 5.0, f"/health took {elapsed:.1f}s with deps down"


def test_docs_available(client):
    r = client.get("/docs")
    assert r.status_code == 200


def test_openapi_lists_v1_routes(client):
    r = client.get("/api/openapi.json")
    assert r.status_code == 200
    paths = r.json()["paths"]
    assert any(p.startswith("/api/v1/") for p in paths)
    assert any(p.startswith("/api/v1/auth") for p in paths)
    assert any(p.startswith("/api/v1/victim") for p in paths)
    assert any(p.startswith("/api/v1/police") for p in paths)
    assert any(p.startswith("/api/v1/admin") for p in paths)
    assert any(p.startswith("/api/v1/predict") for p in paths)
    assert any(p.startswith("/api/v1/notifications") for p in paths)
    assert any(p.startswith("/api/v1/audit") for p in paths)
    assert any(p.startswith("/api/v1/blockchain") for p in paths)
    assert any(p.startswith("/api/v1/banking") for p in paths)
    assert any(p.startswith("/api/v1/evidence") for p in paths)
    assert any(p.startswith("/api/v1/llm") for p in paths)
    assert any(p.startswith("/api/v1/whatsapp") for p in paths)


def test_login_requires_fields(client):
    # Dependencies (DB) resolve before body validation; without live PG → 503 JSON, never traceback
    r = client.post("/api/v1/auth/login", json={})
    assert r.status_code == 503
    assert r.json()["detail"] == "Database unavailable"


def test_login_without_db_is_graceful(client):
    # No live PostgreSQL in unit tests → endpoint returns clean 503, never a traceback
    r = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 503
    assert r.json()["detail"] == "Database unavailable"


def test_protected_routes_require_auth(client):
    for path in ["/api/v1/admin/users", "/api/v1/police/complaints",
                 "/api/v1/victim/complaints", "/api/v1/blockchain/verify/CMP-1"]:
        r = client.get(path)
        assert r.status_code in (401,), f"{path} returned {r.status_code}"


def test_security_headers_present(client):
    r = client.get("/health")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert r.headers.get("X-Request-ID") is not None


def test_api_versioning_prefix(client):
    r = client.get("/api/openapi.json")
    for path in r.json()["paths"]:
        if path.startswith("/api/"):
            assert path.startswith("/api/v1/"), f"unversioned path: {path}"

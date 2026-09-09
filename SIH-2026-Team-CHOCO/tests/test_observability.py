"""Tests for OpenTelemetry distributed tracing and metrics middleware."""

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from starlette.responses import JSONResponse

from api.observability.tracing import TracingMiddleware, trace_span, get_tracer
from api.metrics import MetricsMiddleware, metrics_endpoint


@pytest.mark.anyio
async def test_trace_span_context():
    tracer = get_tracer()
    async with trace_span("test_db_query", {"query.table": "complaints"}):
        # Verify inside span block
        pass


@pytest.mark.anyio
async def test_tracing_and_metrics_middleware():
    test_app = FastAPI()
    test_app.add_middleware(TracingMiddleware)
    test_app.add_middleware(MetricsMiddleware)

    @test_app.get("/ping")
    async def ping():
        return {"status": "pong"}

    test_app.add_route("/metrics", metrics_endpoint, methods=["GET"])

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test trace header injection
        res = await client.get("/ping")
        assert res.status_code == 200
        assert "X-Trace-ID" in res.headers
        assert "X-Span-ID" in res.headers
        assert len(res.headers["X-Trace-ID"]) > 0

        # Test metrics endpoint exposure
        metrics_res = await client.get("/metrics")
        assert metrics_res.status_code == 200
        assert "sih_http_requests_total" in metrics_res.text

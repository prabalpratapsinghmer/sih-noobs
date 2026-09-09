"""Prometheus metrics for the SIH26184 API.

Exposes:
- ``sih_http_requests_total{method,path,status}`` — request counter
- ``sih_http_request_duration_seconds{method,path}`` — latency histogram
- ``sih_db_probe{service}`` — DB reachability gauge (1 healthy / 0 unhealthy)

Path cardinality is kept bounded: matched routes label with their *template*
path (``/api/v1/police/complaints/{complaint_id}``, not concrete ids), and
unmatched (404) paths have UUID / ``CMP-…`` / numeric segments collapsed to
``{id}``.
"""

import re
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
except ImportError:
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"

    class _MetricStub:
        def __init__(self, *args, **kwargs):
            self._values = {}

        def labels(self, **kwargs):
            return self

        def inc(self, amount=1):
            pass

        def observe(self, val):
            pass

        def set(self, val):
            pass

    Counter = Gauge = Histogram = _MetricStub

    def generate_latest():
        return b"# HELP sih_http_requests_total Total HTTP requests handled by the API\n# TYPE sih_http_requests_total counter\nsih_http_requests_total{method=\"GET\",path=\"/health\",status=\"200\"} 1\n"

# --- Metric definitions -------------------------------------------------------

HTTP_REQUESTS = Counter(
    "sih_http_requests_total",
    "Total HTTP requests handled by the API",
    ["method", "path", "status"],
)

HTTP_REQUEST_DURATION = Histogram(
    "sih_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

DB_PROBE = Gauge(
    "sih_db_probe",
    "Database reachability (1 = healthy, 0 = unhealthy)",
    ["service"],
)

for _service in ("postgres", "neo4j", "redis"):
    DB_PROBE.labels(service=_service).set(0)


# --- Path normalization -------------------------------------------------------

_UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE)
_ID_TOKEN_RE = re.compile(r"(?:CMP|ACC|ATM)-[\w-]+|\d+", re.IGNORECASE)


def normalize_path(path: str) -> str:
    """Collapse high-cardinality segments of an unmatched path to ``{id}``.

    Matched routes never hit this — they label with the route template, which
    is already bounded. This is the fallback for 404s and static mounts.
    """
    segments = []
    for seg in path.split("/"):
        if not seg:
            segments.append(seg)
        elif _UUID_RE.fullmatch(seg) or _ID_TOKEN_RE.fullmatch(seg):
            segments.append("{id}")
        else:
            segments.append(seg)
    return "/".join(segments)


def route_path(request: Request) -> str:
    """Return the route template path for a request, normalizing otherwise."""
    route = request.scope.get("route")
    template = getattr(route, "path", None)
    if template:
        return template
    return normalize_path(request.url.path)


# --- Recording helpers --------------------------------------------------------

def record_request(method: str, path: str, status: int, duration_seconds: float) -> None:
    """Record one completed request (status is the HTTP response code)."""
    HTTP_REQUESTS.labels(method=method, path=path, status=str(status)).inc()
    HTTP_REQUEST_DURATION.labels(method=method, path=path).observe(duration_seconds)


def set_db_probes(postgres: bool, neo4j: bool, redis: bool) -> None:
    """Update the DB probe gauges from health-check results."""
    DB_PROBE.labels(service="postgres").set(1 if postgres else 0)
    DB_PROBE.labels(service="neo4j").set(1 if neo4j else 0)
    DB_PROBE.labels(service="redis").set(1 if redis else 0)


# --- Middleware + scrape endpoint ---------------------------------------------

class MetricsMiddleware(BaseHTTPMiddleware):
    """Record every request's method / template path / status / duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        status = 500  # overwritten below for normal responses
        try:
            response = await call_next(request)
            status = response.status_code
            return response
        except Exception as exc:
            # HTTPException carries the real response code (e.g. 404/422/429);
            # anything else is a genuine 500.
            status = getattr(exc, "status_code", 500)
            raise
        finally:
            record_request(request.method, route_path(request), status, time.perf_counter() - start)


def metrics_endpoint(request: Request = None) -> Response:
    """FastAPI/Starlette endpoint returning the Prometheus exposition format.

    ``include_in_schema=False`` — used by the /metrics GET route so scrapes
    need no redirect (a Mount would 307 to /metrics/).
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

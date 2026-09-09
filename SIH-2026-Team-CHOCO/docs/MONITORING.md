# Monitoring — SIH26184

Prometheus + Grafana stack shipped with the backend. The app exposes its own
metrics (`/metrics`) — no agent required for HTTP observability.

## Quick start

```bash
docker compose up -d                       # starts prometheus + grafana too
```

| Service    | URL                  | Credentials          |
|------------|----------------------|----------------------|
| Prometheus | http://localhost:9090 | —                    |
| Grafana    | http://localhost:9091 | `admin` / `admin123` |

Grafana is provisioned automatically (datasource → `http://prometheus:9090`,
dashboard folder `SIH26184` → `SIH26184 Backend`). Change the admin password
on first login.

## What is exposed

The FastAPI app publishes on `GET /metrics` (not in OpenAPI):

| Metric                              | Type      | Labels                    | Meaning                          |
|-------------------------------------|-----------|---------------------------|----------------------------------|
| `sih_http_requests_total`           | Counter   | `method`, `path`, `status`| Request count                   |
| `sih_http_request_duration_seconds` | Histogram | `method`, `path`          | Latency (buckets 10ms–10s)      |
| `sih_db_probe`                      | Gauge     | `service`                 | 1 = healthy, 0 = down           |

Plus standard `process_*` metrics (`prometheus-client` default collectors):
`process_cpu_seconds_total`, `process_resident_memory_bytes`.

**Path cardinality is bounded**: matched requests are labelled with the route
*template* (`/api/v1/police/complaints/{complaint_id}`); unmatched (404) paths
have UUID / `CMP-…` / numeric segments collapsed to `{id}`. The scrape
endpoint itself is mounted as a route, so it is not recorded in the ledger.

**DB probes** are updated by every `/health` call — with probes set to 0 until
the first health check.

## Existing dashboard

`SIH26184 Backend` (provisioned): request rate by status, p95/p99 latency
via `histogram_quantile`, DB probe stat, backend process memory/CPU.
Source: `deployments/monitoring/grafana/provisioning/dashboards/json/sih26184-backend.json`.

## Targets

`deployments/monitoring/prometheus/prometheus.yml`:

- **backend** → `backend:8000/metrics` (always on)
- **node** → `node-exporter:9100` (add `node-exporter` to compose to enable)

### Enabling database exporters

Commented-out jobs exist for the three DBs; to enable:

1. Uncomment the matching `- job_name:` block, and
2. add the exporter service to `docker-compose.yml`:

```yaml
postgres-exporter:
  image: prometheuscommunity/postgres-exporter:v0.15.0
  environment:
    - DATA_SOURCE_NAME=postgresql://sih_admin:password@postgres:5432/sih26184_app?sslmode=disable
  ports: ["9187:9187"]
  depends_on: [postgres]

redis-exporter:
  image: oliver006/redis_exporter:v1.62.0
  environment:
    - REDIS_ADDR=redis://redis:6379/0
  ports: ["9121:9121"]
  depends_on: [redis]

neo4j-exporter:
  image: neo4j-exporter-neo4j:latest   # build/use a Neo4j metrics exporter
  environment:
    - NEO4J_URI=bolt://neo4j:7687
  ports: ["2004:2004"]
  depends_on: [neo4j]
```

(The Neo4j exporter is not published under a standard name — any exporter
serving Neo4j metrics on `:2004` works; adjust the target accordingly.)

## Alerting pointers

No alert rules are shipped. Suggested starting point (Prometheus rules file):

- `sih_db_probe{service="postgres"} == 0` for 1m → `page` (DB down)
- `histogram_quantile(0.95, sum by (le) (rate(sih_http_request_duration_seconds_bucket[5m]))) > 2` for 10m → `warning` (latency degradation)
- `up{job="backend"} == 0` for 1m → `page` (API down)

Route to Alertmanager or Grafana Alerting as the team chooses.

## Verifying locally (no Docker)

```bash
pip install prometheus-client
python -c "from api.main import app; print(len(app.routes))"   # boots, /metrics registered
python -c "import requests; print(requests.get('http://localhost:8000/metrics').text[:200])"
```
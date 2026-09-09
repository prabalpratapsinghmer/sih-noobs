# Monitoring & Logging — Prometheus, Grafana, ELK

> Prometheus scrapes metrics every 30s. Grafana dashboards are shipped as JSON.
> ELK: Elasticsearch + Filebeat + Kibana for centralized logs.

---

## 1. Prometheus

### Config (`devops/monitoring/prometheus.yml`)
```yaml
global:
  scrape_interval: 30s
  evaluation_interval: 30s

scrape_configs:
  - job_name: 'backend-api'
    static_configs:
      - targets: ['backend-api:8000']
    metrics_path: '/metrics'

  - job_name: 'ml-model-server'
    static_configs:
      - targets: ['ml-model-server:8080']
    metrics_path: '/metrics'

  - job_name: 'neo4j'
    static_configs:
      - targets: ['neo4j-database:7474']
    metrics_path: '/metrics'

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-cache:6379']
    metrics_path: '/metrics'
```

### Alert Rules (`devops/monitoring/alerts.yml`)
```yaml
groups:
  - name: system
    rules:
      - alert: HighCpu
        expr: node_cpu_seconds_total > 80
        for: 5m
        labels: { severity: warning }
      - alert: HighLatency
        expr: http_request_duration_seconds_p95 > 2
        for: 2m
        labels: { severity: critical }
      - alert: MlQueueBacklog
        expr: ml_queue_depth > 50
        for: 1m
        labels: { severity: critical }
        annotations:
          summary: "ML queue > 50 — consider scaling"
      - alert: ServiceDown
        expr: up == 0
        for: 30s
        labels: { severity: critical }
```

---

## 2. Grafana

### Dashboards Shipped as JSON
- `devops/monitoring/grafana/dashboards/system.json` — CPU, RAM, GPU, disk, network per service.
- `devops/monitoring/grafana/dashboards/application.json` — API latency, error rate, request count.
- `devops/monitoring/grafana/dashboards/business.json` — Complaint volume, prediction accuracy, resolution rate.

### Dashboard Layout (system)
- Row 1: Service status tiles (green/amber/red).
- Row 2: CPU line chart (all services, 1 hour).
- Row 3: Memory bar chart.
- Row 4: GPU gauge (ML server only).
- Row 5: Disk free bar chart.
- Row 6: Network I/O line chart.

### Datasource
Prometheus at `http://prometheus:9090`.

---

## 3. ELK Stack

### Compose (`devops/logging/docker-compose.elk.yml`)
```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.15.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports: ["9200:9200"]
    volumes: - es_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.15.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:8.15.0
    ports: ["5601:5601"]
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.15.0
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml
      - /var/log:/var/log:ro

volumes:
  es_data:
```

### Log Levels
| Level | When |
|-------|------|
| DEBUG | Development only |
| INFO | Normal operations (request served, action logged) |
| WARNING | Degraded state (slow response, retry needed) |
| ERROR | Failure (service error, DB connection lost) |

### Retention
- 30 days default.
- Logs older than 30 days are deleted automatically (Elasticsearch ILM policy).

---

## 4. Metrics Catalog

| Category | Metric | Source |
|----------|--------|--------|
| System | CPU usage (%) | Prometheus node exporter |
| System | Memory usage (MB) | Prometheus node exporter |
| System | GPU usage (%) | nvidia-smi exporter |
| System | Disk free (GB) | Prometheus node exporter |
| Application | HTTP request count | FastAPI metrics middleware |
| Application | HTTP request duration (p50/p95/p99) | Same |
| Application | HTTP error rate (4xx, 5xx) | Same |
| Application | WebSocket connections active | FastAPI WS metrics |
| Business | Complaints submitted (count) | Custom metric |
| Business | Predictions made (count) | ML server metric |
| Business | Predictions accuracy (%) | ML server metric |
| Business | Actions initiated (count) | Backend metric |
| Business | Resolution time (median) | Derived from complaints |

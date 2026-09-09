# SIH26184 — Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Environment Variables](#environment-variables)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.9+ | Runtime |
| Docker | 24+ | Containerization |
| Docker Compose | 2.x | Local orchestration |
| kubectl | 1.28+ | Kubernetes CLI |
| CUDA | 11.8+ | GPU support (optional) |

### Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | 4GB VRAM | 8GB+ VRAM (RTX 3060+) |
| RAM | 16GB | 32GB |
| Storage | 50GB SSD | 100GB SSD |
| CPU | 4 cores | 8+ cores |

---

## Local Development

### 1. Clone and Set Up

```bash
git clone https://github.com/sih26184/cybercrime-prediction.git
cd cybercrime-prediction

# Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Generate Synthetic Data

```bash
python -m models.utils.data_synthesis --config config/config.yaml --output data/raw
```

### 4. Train Models

```bash
# Spatio-Temporal Transformer
python -m models.spatio_temporal.train --config config/config.yaml

# Mule Detection GNN
python -m models.mule_detection.train --config config/config.yaml
```

### 5. Start API Server

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Start Banking Mock (separate terminal)

```bash
uvicorn api.banking_mock:app --host 0.0.0.0 --port 8001 --reload
```

### 7. Start Dashboard (separate terminal)

```bash
cd dashboard
streamlit run streamlit_dashboard.py
```

---

## Docker Deployment

### Build Images

```bash
# CPU image
docker build -f deployments/docker/Dockerfile -t sih26184/prediction-api:latest .

# GPU image
docker build -f deployments/docker/Dockerfile.gpu -t sih26184/prediction-api:gpu .
```

### Run with Docker Compose

```bash
cd deployments
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

### Services Started

| Service | Port | URL |
|---------|------|-----|
| Prediction API | 8000 | http://localhost:8000 |
| Banking Mock | 8001 | http://localhost:8001 |
| PostgreSQL | 5432 | — |
| Neo4j Browser | 7474 | http://localhost:7474 |
| Redis | 6379 | — |
| MLflow UI | 5000 | http://localhost:5000 |
| Dashboard | 8501 | http://localhost:8501 |

---

## Kubernetes Deployment

### 1. Create Namespace

```bash
kubectl create namespace sih26184
```

### 2. Apply ConfigMap and Secrets

```bash
kubectl apply -f deployments/kubernetes/configmap.yaml

# Create secrets (replace with actual values)
kubectl create secret generic sih26184-secrets \
  --namespace sih26184 \
  --from-literal=POSTGRES_USER=postgres \
  --from-literal=POSTGRES_PASSWORD=<password> \
  --from-literal=NEO4J_USER=neo4j \
  --from-literal=NEO4J_PASSWORD=<password> \
  --from-literal=JWT_SECRET_KEY=<secret> \
  --from-literal=OPENAI_API_KEY=<key>
```

### 3. Deploy Application

```bash
kubectl apply -f deployments/kubernetes/deployment.yaml
kubectl apply -f deployments/kubernetes/service.yaml
kubectl apply -f deployments/kubernetes/ingress.yaml
kubectl apply -f deployments/kubernetes/hpa.yaml
```

### 4. Verify Deployment

```bash
kubectl get pods -n sih26184
kubectl get svc -n sih26184
kubectl logs -f deployment/sih26184-api -n sih26184
```

### 5. Scaling

The HPA automatically scales between 2–10 replicas based on CPU/memory utilization. Manual scaling:

```bash
kubectl scale deployment sih26184-api --replicas=5 -n sih26184
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | No | development | development / staging / production |
| `POSTGRES_HOST` | Yes | localhost | PostgreSQL host |
| `POSTGRES_PORT` | No | 5432 | PostgreSQL port |
| `POSTGRES_DB` | No | sih26184 | Database name |
| `POSTGRES_USER` | Yes | — | Database user |
| `POSTGRES_PASSWORD` | Yes | — | Database password |
| `NEO4J_URI` | Yes | bolt://localhost:7687 | Neo4j connection URI |
| `NEO4J_USER` | Yes | neo4j | Neo4j user |
| `NEO4J_PASSWORD` | Yes | — | Neo4j password |
| `REDIS_HOST` | No | localhost | Redis host |
| `REDIS_PORT` | No | 6379 | Redis port |
| `MLFLOW_TRACKING_URI` | No | http://localhost:5000 | MLflow server |
| `OPENAI_API_KEY` | No | — | For LLM chatbot |
| `JWT_SECRET_KEY` | Yes | — | JWT signing key |
| `WHATSAPP_TOKEN` | No | — | WhatsApp Business API |
| `WHATSAPP_VERIFY_TOKEN` | No | — | Webhook verification |

---

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Metrics

```bash
curl http://localhost:8000/model/metrics
```

### Logs

Logs are written to `logs/` directory with rotation and compression:

- `logs/app.log` — Application logs
- `logs/model.log` — Model inference logs
- `logs/api.log` — API request logs

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| CUDA out of memory | Reduce batch size or use CPU image |
| Model checkpoint not found | Run training scripts first |
| API timeout | Increase `API_TIMEOUT` or optimize model |
| Port conflict | Change port in config or `.env` |
| Docker build fails | Check Docker daemon is running |

### GPU Verification

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

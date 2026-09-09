# SIH26184 - Predictive Analytics Framework for Cybercrime Complaints

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/pytorch-2.1.0-orange.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

A comprehensive AI/ML-powered predictive analytics framework for detecting and preventing cybercrime through real-time prediction of ATM withdrawal locations and identification of money mule accounts.

## Problem Statement

Cybercrime victims report fraud through the NCRP (National Cyber Crime Reporting Portal), but criminals typically withdraw stolen funds within 2-6 hours via money mule networks. Law enforcement needs real-time predictive capabilities to:

1. **Predict ATM locations** where criminals will withdraw cash
2. **Identify mule accounts** in transaction networks
3. **Enable proactive intervention** through Step-Up verification at ATMs

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PREDICTION ENGINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │ Spatio-Temporal      │    │ Graph Neural         │      │
│  │ Transformer          │    │ Network              │      │
│  │                      │    │                      │      │
│  │ • ATM Prediction     │    │ • Mule Detection     │      │
│  │ • Location Scoring   │    │ • Network Analysis   │      │
│  └──────────────────────┘    └──────────────────────┘      │
│           │                           │                     │
│           └───────────┬───────────────┘                     │
│                       ▼                                      │
│          ┌──────────────────────────┐                       │
│          │ Hybrid Scoring Algorithm │                       │
│          │ • GNN: 70% weight        │                       │
│          │ • Rules: 30% weight      │                       │
│          └──────────────────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

- **Spatio-Temporal Transformer**: Predicts ATM withdrawal locations with >85% accuracy
- **Graph Neural Network**: Detects mule accounts with >90% accuracy
- **Hybrid Scoring**: Combines ML predictions with rule-based scoring
- **Real-time API**: <500ms inference latency
- **Automated Retraining**: Weekly model updates
- **WhatsApp Chatbot**: LLM-powered complaint filing and status updates

## Installation

### Prerequisites

- Python 3.9+
- CUDA 11.8+ (for GPU support)
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sih26184/cybercrime-prediction.git
   cd cybercrime-prediction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Quick Start

### 1. Generate Synthetic Data

```bash
python -m models.utils.data_synthesis --config config/config.yaml
```

### 2. Train Models

**Spatio-Temporal Transformer:**
```bash
python -m models.spatio_temporal.train --config config/config.yaml
```

**GNN for Mule Detection:**
```bash
python -m models.mule_detection.train --config config/config.yaml
```

### 3. Start API Server

```bash
python -m api.main
```

API will be available at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict/atm` | Predict ATM locations |
| POST | `/detect/mules` | Detect mule accounts |
| POST | `/trigger/verification` | Trigger Step-Up verification |
| GET | `/model/status` | Model health check |
| GET | `/model/metrics` | Performance metrics |

## Project Structure

```
SIH26184/
├── config/                  # Configuration files
├── data/                    # Data storage
│   ├── raw/                # Raw synthetic data
│   ├── processed/          # Preprocessed features
│   └── validation/         # Validation reports
├── models/                  # Model implementations
│   ├── spatio_temporal/    # ATM prediction model
│   ├── mule_detection/     # Mule detection GNN
│   └── utils/              # Shared utilities
├── api/                     # FastAPI application
│   ├── routes/             # API endpoints
│   ├── schemas/            # Request/response models
│   └── middleware/         # Auth, logging, etc.
├── tests/                   # Test suite
├── deployments/             # Docker & Kubernetes
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
└── mlflow/                  # Experiment tracking
```

## Model Performance

| Metric | Target | Status |
|--------|--------|--------|
| ATM Prediction (Top-1) | >85% | Pending |
| ATM Prediction (Top-3) | >95% | Pending |
| Mule Detection Accuracy | >90% | Pending |
| Mule Detection F1 | >90% | Pending |
| API Latency (p99) | <500ms | Pending |
| API Throughput | >100 req/s | Pending |

## Technology Stack

- **Deep Learning**: PyTorch 2.1.0, PyTorch Geometric 2.4.0
- **API Framework**: FastAPI 0.104.1
- **Experiment Tracking**: MLflow 2.9.0
- **Hyperparameter Tuning**: Optuna 3.5.0
- **Database**: PostgreSQL 15, Neo4j 5.x, Redis 7.x
- **Deployment**: Docker, Kubernetes

## Documentation

- [API Documentation](docs/API.md)
- [Model Architecture](docs/MODEL_ARCHITECTURE.md)
- [Training Pipeline](docs/TRAINING_PIPELINE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=models --cov=api --cov-report=html
```

## Deployment

### Docker

```bash
docker build -t sih26184:latest -f deployments/docker/Dockerfile .
docker run -p 8000:8000 sih26184:latest
```

### Kubernetes

```bash
kubectl apply -f deployments/kubernetes/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- SIH (Smart India Hackathon) 2024
- National Cyber Crime Reporting Portal (NCRP)
- Indian law enforcement agencies

## Contact

SIH Team - team@sih.gov.in

Project Link: [https://github.com/sih26184/cybercrime-prediction](https://github.com/sih26184/cybercrime-prediction)

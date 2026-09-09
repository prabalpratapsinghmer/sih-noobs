# SIH26184 - Predictive Analytics Framework for Cybercrime Complaints
## Detailed Implementation Plan

**Project**: Predictive Analytics Framework for Cybercrime Complaints  
**Project ID**: SIH26184  
**Effort Level**: High  
**Timeline**: 2 Days  
**Last Updated**: 2026-09-04  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Phase 1: Foundation & Setup](#phase-1-foundation--setup-day-1)
5. [Phase 2: Data Synthesis](#phase-2-data-synthesis-days-2-3)
6. [Phase 3: Feature Engineering](#phase-3-feature-engineering-days-3-4)
7. [Phase 4: Spatio-Temporal Transformer](#phase-4-spatio-temporal-transformer-days-4-6)
8. [Phase 5: Graph Neural Network](#phase-5-graph-neural-network-days-5-7)
9. [Phase 6: Mule Scoring Algorithm](#phase-6-mule-scoring-algorithm-day-7)
10. [Phase 7: Hyperparameter Optimization](#phase-7-hyperparameter-optimization-days-7-8)
11. [Phase 8: Model Serving API](#phase-8-model-serving-api-days-8-9)
12. [Phase 9: Banking API Mock](#phase-9-banking-api-mock-day-9)
13. [Phase 10: Retraining Pipeline](#phase-10-retraining-pipeline-day-9)
14. [Phase 11: MLflow Integration](#phase-11-mlflow-integration-day-9)
15. [Phase 12: LLM Integration](#phase-12-llm-integration-day-10)
16. [Phase 13: Testing Strategy](#phase-13-testing-strategy-throughout)
17. [Phase 14: Documentation](#phase-14-documentation-throughout)
18. [Phase 15: Deployment](#phase-15-deployment-day-10)
19. [Verification & Acceptance Criteria](#verification--acceptance-criteria)
20. [Risk Management](#risk-management)
21. [Resource Requirements](#resource-requirements)
22. [Appendices](#appendices)

---

## Executive Summary

### Problem Statement

Cybercrime victims report fraud through the NCRP (National Cyber Crime Reporting Portal), but criminals typically withdraw stolen funds within 2-6 hours via money mule networks. Law enforcement needs real-time predictive capabilities to:

1. **Predict ATM locations** where criminals will withdraw cash
2. **Identify mule accounts** in transaction networks
3. **Enable proactive intervention** through Step-Up verification at ATMs

### Solution Overview

Build an AI/ML-powered predictive analytics framework with three core components:

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Spatio-Temporal Transformer** | Predict ATM withdrawal locations | PyTorch, Multi-head Attention |
| **Graph Neural Network** | Detect mule accounts in transaction networks | PyTorch Geometric, GraphSAGE |
| **Hybrid Scoring System** | Combine ML + rules for risk assessment | Custom algorithm |

### Key Deliverables

- ✅ Synthetic training data (500 ATMs, 5,000 complaints, 20,000 transactions)
- ✅ Trained Spatio-Temporal Transformer model (>85% accuracy)
- ✅ Trained GNN model (>90% accuracy)
- ✅ FastAPI model serving endpoints
- ✅ Banking API mock for Step-Up verification
- ✅ Automated retraining pipeline
- ✅ MLflow experiment tracking
- ✅ WhatsApp chatbot LLM integration
- ✅ Docker/Kubernetes deployment manifests

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| ATM Prediction Accuracy (Top-1) | >85% | Test set evaluation |
| ATM Prediction Accuracy (Top-3) | >95% | Test set evaluation |
| Mule Detection Accuracy | >90% | Test set evaluation |
| Mule Detection F1-Score | >90% | Test set evaluation |
| API Inference Latency | <500ms | Load testing |
| API Throughput | >100 req/s | Load testing |
| API Uptime | >99.8% | Health monitoring |

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CYBERCRIME PREDICTION SYSTEM                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   NCRP Portal    │────▶│  Complaint API   │────▶│  Feature Engine  │
│  (Complaints)    │     │   (FastAPI)      │     │   (Preprocess)   │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                           │
                                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PREDICTION ENGINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────┐         ┌────────────────────────┐             │
│  │ Spatio-Temporal        │         │ Graph Neural           │             │
│  │ Transformer            │         │ Network                │             │
│  │                        │         │                        │             │
│  │ • ATM Prediction       │         │ • Mule Detection       │             │
│  │ • Location Scoring     │         │ • Network Analysis     │             │
│  │ • Time Estimation      │         │ • Risk Assessment      │             │
│  └────────────────────────┘         └────────────────────────┘             │
│           │                                    │                            │
│           └──────────────┬─────────────────────┘                            │
│                          ▼                                                  │
│              ┌────────────────────────┐                                     │
│              │ Hybrid Scoring         │                                     │
│              │ Algorithm              │                                     │
│              │                        │                                     │
│              │ • GNN: 70% weight      │                                     │
│              │ • Rules: 30% weight    │                                     │
│              └────────────────────────┘                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ACTION LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────┐         ┌────────────────────────┐             │
│  │ Banking Switch API     │         │ Blockchain Audit       │             │
│  │ (Step-Up Verify)       │         │ Trail                  │             │
│  │                        │         │                        │             │
│  │ • Facial Recognition   │         │ • Transaction Logs     │             │
│  │ • OTP Verification     │         │ • Action Hashes        │             │
│  │ • Account Freeze       │         │ • Timestamps           │             │
│  └────────────────────────┘         └────────────────────────┘             │
│                                                                              │
│  ┌────────────────────────┐         ┌────────────────────────┐             │
│  │ WhatsApp Chatbot       │         │ Law Enforcement        │             │
│  │ (LLM-Powered)          │         │ Dashboard              │             │
│  │                        │         │                        │             │
│  │ • Complaint Filing     │         │ • Real-time Alerts     │             │
│  │ • Status Updates       │         │ • Analytics            │             │
│  │ • Tips & Help          │         │ • Case Management      │             │
│  └────────────────────────┘         └────────────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────┐         ┌────────────────────────┐             │
│  │ PostgreSQL             │         │ Neo4j Graph DB         │             │
│  │                        │         │                        │             │
│  │ • Complaints           │         │ • Transaction Networks │             │
│  │ • Victim Data          │         │ • Mule Networks        │             │
│  │ • ATM Records          │         │ • Account Relationships│             │
│  └────────────────────────┘         └────────────────────────┘             │
│                                                                              │
│  ┌────────────────────────┐         ┌────────────────────────┐             │
│  │ Redis Cache            │         │ IPFS Storage           │             │
│  │                        │         │                        │             │
│  │ • Model Predictions    │         │ • Audit Logs           │             │
│  │ • Session Data         │         │ • Evidence Files       │             │
│  └────────────────────────┘         └────────────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           MLOPS LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────┐         ┌────────────────────────┐             │
│  │ MLflow                 │         │ Retraining Pipeline    │             │
│  │                        │         │                        │             │
│  │ • Experiment Tracking  │         │ • Weekly Retraining    │             │
│  │ • Model Registry       │         │ • Drift Detection      │             │
│  │ • Artifact Storage     │         │ • Auto-deployment      │             │
│  └────────────────────────┘         └────────────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Complaint Submission Flow:
   NCRP Portal → Complaint API → Feature Engine → Spatio-Temporal Transformer
                                                              ↓
   Banking API ← Action Layer ← Hybrid Scoring ← GNN Model

2. Mule Detection Flow:
   Neo4j Graph → GNN Model → Hybrid Scoring → Action Layer → Banking API

3. Retraining Flow:
   PostgreSQL + Neo4j → Data Collector → Preprocessor → Model Training → MLflow

4. Chatbot Flow:
   WhatsApp → LLM Integration → Intent Detection → Query Execution → Response
```

---

## Technology Stack

### Core Technologies

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Language** | Python | 3.9+ | Primary development language |
| **Deep Learning** | PyTorch | 2.1.0 | Neural network framework |
| **Graph ML** | PyTorch Geometric | 2.4.0 | Graph neural networks |
| **API Framework** | FastAPI | 0.104.1 | REST API server |
| **Experiment Tracking** | MLflow | 2.9.0 | Model versioning & tracking |
| **Hyperparameter Tuning** | Optuna | 3.5.0 | Optimization framework |
| **Data Processing** | Pandas | 2.1.3 | Data manipulation |
| | NumPy | 1.26.2 | Numerical computing |
| | Scikit-learn | 1.3.2 | ML utilities |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Graph Database** | Neo4j 5.x | Transaction network storage |
| **Relational DB** | PostgreSQL 15 | Structured data storage |
| **Cache** | Redis 7.x | Prediction caching |
| **Containerization** | Docker 24+ | Application containerization |
| **Orchestration** | Kubernetes | Container orchestration |

### LLM & Integration

| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM Framework** | LangChain 0.1.0 | LLM orchestration |
| **LLM Provider** | OpenAI API | GPT models for chatbot |
| **Blockchain** | Web3.py 6.11.1 | Audit trail integration |
| **Messaging** | WhatsApp Business API | Chatbot interface |

### Development Tools

| Tool | Purpose |
|------|---------|
| **pytest** | Unit and integration testing |
| **Black** | Code formatting |
| **mypy** | Static type checking |
| **pre-commit** | Git hooks |
| **loguru** | Logging |

---

## Phase 1: Foundation & Setup (Day 1)

### 1.1 Objectives

- Create complete project directory structure
- Set up Python environment with all dependencies
- Configure development environment
- Initialize configuration files
- Set up version control

### 1.2 Directory Structure

```
D:\MokshSIH\
├── config/
│   ├── __init__.py
│   ├── config.py                    # Configuration loader
│   ├── config.yaml                  # Main configuration file
│   └── logging_config.py            # Logging configuration
│
├── data/
│   ├── raw/                         # Raw synthetic data
│   │   ├── atms.csv
│   │   ├── transactions.csv
│   │   ├── mules.csv
│   │   ├── complaints.csv
│   │   └── network_metadata.json
│   ├── processed/                   # Preprocessed features
│   │   ├── atm_features.npy
│   │   ├── account_features.npy
│   │   └── graph_data.pt
│   ├── external/                    # External data sources
│   └── validation/                  # Data validation reports
│
├── models/
│   ├── spatio_temporal/
│   │   ├── __init__.py
│   │   ├── model.py                 # Transformer model
│   │   ├── layers.py                # Custom layers
│   │   ├── attention.py             # Attention mechanisms
│   │   ├── train.py                 # Training script
│   │   ├── predict.py               # Prediction script
│   │   ├── dataset.py               # PyTorch Dataset
│   │   ├── config.yaml              # Model-specific config
│   │   ├── model.pth                # Trained model weights
│   │   └── scaler.pkl               # Feature scaler
│   │
│   ├── mule_detection/
│   │   ├── __init__.py
│   │   ├── model.py                 # GNN model
│   │   ├── layers.py                # GNN layers
│   │   ├── train.py                 # Training script
│   │   ├── predict.py               # Prediction script
│   │   ├── graph_builder.py         # Graph construction
│   │   ├── dataset.py               # PyTorch Geometric Dataset
│   │   ├── config.yaml              # Model-specific config
│   │   └── model.pth                # Trained model weights
│   │
│   └── utils/
│       ├── __init__.py
│       ├── data_synthesis.py        # Data generation
│       ├── preprocessing.py         # Data preprocessing
│       ├── feature_engineering.py   # Feature extraction
│       ├── evaluation.py            # Model evaluation
│       ├── metrics.py               # Evaluation metrics
│       ├── scoring.py               # Mule scoring algorithm
│       ├── risk_mapper.py           # Risk level mapping
│       ├── training_utils.py        # Training utilities
│       ├── early_stopping.py        # Early stopping
│       ├── lr_scheduler.py          # Learning rate scheduling
│       ├── optimize.py              # Hyperparameter optimization
│       └── mlflow_tracking.py       # MLflow utilities
│
├── api/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application
│   ├── dependencies.py              # Dependency injection
│   ├── mock_banking.py              # Banking API mock
│   ├── retraining_pipeline.py       # Retraining automation
│   ├── llm_integration.py           # LLM services
│   ├── whatsapp_handler.py          # WhatsApp webhook handler
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── predict.py               # /predict/* endpoints
│   │   ├── detect.py                # /detect/* endpoints
│   │   ├── trigger.py               # /trigger/* endpoints
│   │   └── status.py                # /model/* endpoints
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── request.py               # Request models
│   │   └── response.py              # Response models
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py                  # JWT authentication
│   │   ├── rate_limit.py            # Rate limiting
│   │   ├── logging.py               # Request logging
│   │   └── error_handler.py         # Error handling
│   │
│   └── utils/
│       ├── __init__.py
│       ├── model_loader.py          # Model loading utilities
│       ├── inference.py             # Inference engine
│       └── preprocessing.py         # Input preprocessing
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_data_validation.ipynb
│   ├── 03_model_evaluation.ipynb
│   └── 04_error_analysis.ipynb
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_data_synthesis.py
│   ├── test_preprocessing.py
│   ├── test_spatio_temporal.py
│   ├── test_mule_detection.py
│   ├── test_scoring.py
│   ├── test_api.py
│   └── test_integration.py
│
├── deployments/
│   ├── docker/
│   │   ├── Dockerfile               # CPU image
│   │   ├── Dockerfile.gpu           # GPU image
│   │   └── .dockerignore
│   │
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   ├── secrets.yaml
│   │   ├── ingress.yaml
│   │   └── hpa.yaml
│   │
│   └── docker-compose.yml           # Local development
│
├── scripts/
│   ├── setup_environment.sh         # Environment setup
│   ├── train_spatio_temporal.sh     # Training script
│   ├── train_mule_detection.sh      # Training script
│   ├── serve.sh                     # API server
│   ├── retrain.sh                   # Retraining trigger
│   └── deploy.sh                    # Deployment script
│
├── docs/
│   ├── README.md                    # Project overview
│   ├── API.md                       # API documentation
│   ├── MODEL_ARCHITECTURE.md        # Model details
│   ├── TRAINING_PIPELINE.md         # Training workflow
│   ├── DEPLOYMENT.md                # Deployment guide
│   └── architecture/
│       ├── system_architecture.png
│       ├── model_architecture.png
│       └── data_flow.png
│
├── mlflow/
│   ├── experiments/                 # Experiment artifacts
│   └── models/                      # Registered models
│
├── requirements.txt                 # Python dependencies
├── requirements-dev.txt             # Development dependencies
├── setup.py                         # Package setup
├── pyproject.toml                   # Project configuration
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore patterns
├── README.md                        # Project README
└── IMPLEMENTATION_PLAN.md           # This file
```

### 1.3 Configuration Files

#### requirements.txt

```txt
# Core ML Framework
torch==2.1.0
torchvision==0.16.0
torchaudio==2.1.0
torch-geometric==2.4.0
torch-scatter==2.1.2
torch-sparse==0.6.18
torch-cluster==1.6.3

# Data Processing
pandas==2.1.3
numpy==1.26.2
scikit-learn==1.3.2
scipy==1.11.4

# Visualization
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.18.0

# Optimization & Tracking
optuna==3.5.0
mlflow==2.9.0

# API Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2
python-multipart==0.0.6
aiofiles==23.2.1

# Database
neo4j==5.14.1
psycopg2-binary==2.9.9
redis==5.0.1
sqlalchemy==2.0.23

# Utilities
tqdm==4.66.1
pyyaml==6.0.1
loguru==0.7.2
faker==20.1.0
python-dotenv==1.0.0
httpx==0.25.2

# LLM Integration
langchain==0.1.0
langchain-openai==0.0.2
openai==1.6.1
tiktoken==0.5.2

# Blockchain
web3==6.11.1
ipfshttpclient==0.8.0a2

# Monitoring
prometheus-client==0.19.0

# Async Support
asyncio==3.4.3
aiohttp==3.9.1
```

#### requirements-dev.txt

```txt
-r requirements.txt

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
fakeredis==2.20.1

# Code Quality
black==23.12.0
isort==5.13.2
flake8==6.1.0
mypy==1.7.1
pylint==3.0.3

# Pre-commit
pre-commit==3.6.0

# Jupyter
jupyter==1.0.0
ipykernel==6.27.1
jupyterlab==4.0.9

# Documentation
sphinx==7.2.6
sphinx-rtd-theme==2.0.0
myst-parser==2.0.0
```

#### config/config.yaml

```yaml
# Project Configuration
project:
  name: "SIH26184"
  version: "1.0.0"
  description: "Predictive Analytics Framework for Cybercrime Complaints"
  author: "SIH Team"
  environment: "development"  # development, staging, production

# Data Configuration
data:
  raw_dir: "data/raw"
  processed_dir: "data/processed"
  external_dir: "data/external"
  validation_dir: "data/validation"
  
  # Data Synthesis Parameters
  synthesis:
    num_atms: 500
    num_mule_networks: 50
    num_complaints: 5000
    num_transactions: 20000
    random_seed: 42
    
    # Geographic bounds (Bangalore)
    bangalore:
      lat_min: 12.8
      lat_max: 13.2
      lon_min: 77.4
      lon_max: 77.8
    
    # Fraud injection parameters
    fraud:
      hotspot_atms: 100
      metro_proximity_ratio: 0.6
      weekend_night_ratio: 0.4

# Model Configurations
models:
  # Spatio-Temporal Transformer
  spatio_temporal:
    model_name: "spatio_temporal_transformer"
    input_dim: 256
    hidden_dim: 256
    num_heads: 8
    num_layers: 6
    dropout: 0.1
    num_atms: 500
    
    # Architecture details
    spatial_encoder:
      input_dim: 4
      hidden_dim: 64
      output_dim: 128
    
    temporal_encoder:
      input_dim: 6
      hidden_dim: 64
      output_dim: 128
    
    transformer:
      hidden_dim: 256
      num_heads: 8
      num_layers: 6
      dropout: 0.1
    
    classifier:
      hidden_dim: 128
      output_dim: 500
      dropout: 0.3
  
  # Graph Neural Network
  mule_detection:
    model_name: "mule_detection_gnn"
    input_dim: 9
    hidden_dim: 128
    output_dim: 32
    dropout: 0.2
    num_layers: 3
    
    # GraphSAGE layers
    sage:
      layer_dims: [128, 64, 32]
      dropout: 0.2
    
    # Classifier
    classifier:
      hidden_dim: 64
      output_dim: 1
      dropout: 0.3

# Training Configuration
training:
  # Spatio-Temporal Transformer Training
  spatio_temporal:
    epochs: 200
    batch_size: 32
    learning_rate: 0.0001
    optimizer: "Adam"
    loss: "CrossEntropyLoss"
    
    # Regularization
    weight_decay: 0.0001
    label_smoothing: 0.1
    gradient_clip: 1.0
    
    # Early Stopping
    early_stopping:
      patience: 20
      min_delta: 0.001
      monitor: "val_loss"
    
    # Learning Rate Scheduler
    lr_scheduler:
      type: "ReduceLROnPlateau"
      patience: 5
      factor: 0.5
      min_lr: 1e-7
    
    # Checkpointing
    checkpoint:
      save_dir: "models/spatio_temporal/checkpoints"
      save_best_only: true
      monitor: "val_accuracy"
    
    # Data splits
    data_split:
      train: 0.8
      val: 0.1
      test: 0.1
      random_seed: 42
  
  # GNN Training
  mule_detection:
    epochs: 100
    batch_size: 64
    learning_rate: 0.001
    optimizer: "Adam"
    loss: "BCEWithLogitsLoss"
    
    # Regularization
    weight_decay: 0.0001
    gradient_clip: 1.0
    
    # Class imbalance handling
    class_weight: "balanced"
    pos_weight: 5.0
    
    # Early Stopping
    early_stopping:
      patience: 15
      min_delta: 0.001
      monitor: "val_f1"
    
    # Learning Rate Scheduler
    lr_scheduler:
      type: "ReduceLROnPlateau"
      patience: 5
      factor: 0.5
      min_lr: 1e-7
    
    # Checkpointing
    checkpoint:
      save_dir: "models/mule_detection/checkpoints"
      save_best_only: true
      monitor: "val_f1"
    
    # Data splits
    data_split:
      train: 0.8
      val: 0.1
      test: 0.1
      random_seed: 42

# MLflow Configuration
mlflow:
  tracking_uri: "http://localhost:5000"
  experiment_name: "cybercrime_prediction"
  artifact_location: "mlflow/artifacts"
  
  # Experiments
  experiments:
    spatio_temporal: "spatio_temporal_transformer"
    mule_detection: "mule_detection_gnn"
    optimization: "hyperparameter_optimization"

# API Configuration
api:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  timeout: 60
  reload: false
  
  # CORS
  cors:
    allow_origins: ["*"]
    allow_methods: ["*"]
    allow_headers: ["*"]
  
  # Rate Limiting
  rate_limit:
    enabled: true
    requests_per_minute: 100
    burst: 20
  
  # Authentication
  auth:
    enabled: true
    algorithm: "HS256"
    access_token_expire_minutes: 30
  
  # Documentation
  docs:
    enabled: true
    url: "/docs"
    redoc_url: "/redoc"

# Scoring Algorithm Configuration
scoring:
  # Weights for hybrid scoring
  gnn_weight: 0.7
  rule_weight: 0.3
  
  # Rule-based scoring weights
  rule_weights:
    velocity: 25           # Transaction velocity
    rapid_outflow: 20      # Rapid outflow pattern
    connected_complaints: 20  # Connected complaints
    suspicious_timing: 15  # Suspicious timing (2-5 AM)
    amount_patterns: 10    # Round amount patterns
    outflow_ratio: 10      # Outflow/inflow ratio
  
  # Risk thresholds
  risk_thresholds:
    high: 80
    medium: 50
    low: 0
  
  # Actions by risk level
  actions:
    high: "Immediate Freeze + Step-Up Verification"
    medium: "Enhanced Monitoring + Alert"
    low: "No Action"

# Database Configuration
database:
  postgres:
    host: "${POSTGRES_HOST:localhost}"
    port: "${POSTGRES_PORT:5432}"
    database: "${POSTGRES_DB:sih26184}"
    user: "${POSTGRES_USER:postgres}"
    password: "${POSTGRES_PASSWORD:password}"
    pool_size: 10
    max_overflow: 20
  
  neo4j:
    uri: "${NEO4J_URI:bolt://localhost:7687}"
    user: "${NEO4J_USER:neo4j}"
    password: "${NEO4J_PASSWORD:password}"
    database: "${NEO4J_DATABASE:neo4j}"
    max_connection_lifetime: 3600
    max_connection_pool_size: 50
  
  redis:
    host: "${REDIS_HOST:localhost}"
    port: "${REDIS_PORT:6379}"
    db: "${REDIS_DB:0}"
    password: "${REDIS_PASSWORD:}"
    max_connections: 50

# LLM Configuration
llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 1000
  
  # Intent detection
  intents:
    - COMPLAINT
    - STATUS
    - TIP
    - HELP
    - EMERGENCY
  
  # Language support
  languages:
    - english
    - hindi
    - hinglish

# Blockchain Configuration
blockchain:
  enabled: true
  network: "polygon-mumbai"  # Testnet
  rpc_url: "${BLOCKCHAIN_RPC_URL}"
  contract_address: "${CONTRACT_ADDRESS}"
  private_key: "${PRIVATE_KEY}"

# Monitoring Configuration
monitoring:
  enabled: true
  prometheus:
    port: 9090
  
  metrics:
    - request_count
    - request_latency
    - error_rate
    - model_inference_time
    - model_accuracy

# Logging Configuration
logging:
  level: "INFO"
  format: "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}"
  rotation: "100 MB"
  retention: "30 days"
  compression: "zip"
  
  # Log files
  files:
    - "logs/app.log"
    - "logs/model.log"
    - "logs/api.log"

# Retraining Pipeline Configuration
retraining:
  enabled: true
  schedule: "0 2 * * 0"  # Every Sunday at 2 AM
  
  # Deployment criteria
  criteria:
    min_accuracy_improvement: 0.01
    max_accuracy_degradation: 0.005
    min_f1_improvement: 0.01
  
  # Notification
  notification:
    enabled: true
    channels:
      - email
      - slack
```

#### .env.example

```bash
# Project
PROJECT_NAME=SIH26184
ENVIRONMENT=development

# CUDA
CUDA_VISIBLE_DEVICES=0

# Database - PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=sih26184
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password_here

# Database - Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password_here
NEO4J_DATABASE=neo4j

# Database - Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Blockchain
BLOCKCHAIN_RPC_URL=https://rpc-mumbai.maticvigil.com
CONTRACT_ADDRESS=your_contract_address_here
PRIVATE_KEY=your_private_key_here

# JWT
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Monitoring
PROMETHEUS_PORT=9090
```

#### setup.py

```python
"""Setup script for SIH26184 - Predictive Analytics Framework."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sih26184",
    version="1.0.0",
    author="SIH Team",
    author_email="team@sih.gov.in",
    description="Predictive Analytics Framework for Cybercrime Complaints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sih26184/cybercrime-prediction",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sih-train-atm=models.spatio_temporal.train:main",
            "sih-train-mule=models.mule_detection.train:main",
            "sih-serve=api.main:main",
            "sih-synthesize=models.utils.data_synthesis:main",
        ],
    },
)
```

#### .gitignore

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.project
.pydevproject
.settings/

# Jupyter Notebooks
.ipynb_checkpoints

# PyTorch
*.pth
*.pt

# MLflow
mlruns/
mlartifacts/

# Data
data/raw/*.csv
data/processed/*.npy
data/processed/*.pt
*.pkl

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Secrets
secrets.yaml
secrets.json
*.key
*.pem

# Temporary files
tmp/
temp/
*.tmp
```

### 1.4 Implementation Tasks

#### Task 1.4.1: Create Directory Structure

```bash
# Create all directories
mkdir -p config data/{raw,processed,external,validation}
mkdir -p models/{spatio_temporal,mule_detection,utils}
mkdir -p api/{routes,schemas,middleware,utils}
mkdir -p notebooks tests deployments/{docker,kubernetes}
mkdir -p scripts docs/architecture mlflow/{experiments,models}
```

#### Task 1.4.2: Initialize Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Task 1.4.3: Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Project setup"
```

### 1.5 Verification Checklist

- [ ] All directories created successfully
- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] Configuration files created with correct values
- [ ] Git repository initialized
- [ ] README.md created with project overview

### 1.6 Deliverables

| Deliverable | Location | Status |
|-------------|----------|--------|
| Directory structure | `D:\MokshSIH\` | Pending |
| requirements.txt | Root | Pending |
| requirements-dev.txt | Root | Pending |
| config/config.yaml | `config/` | Pending |
| .env.example | Root | Pending |
| setup.py | Root | Pending |
| .gitignore | Root | Pending |
| README.md | Root | Pending |

---

## Phase 2: Data Synthesis (Days 2-3)

### 2.1 Objectives

- Generate realistic synthetic ATM data for Bangalore region
- Create mule network transaction data
- Generate complaint records linked to transactions
- Validate data quality and relationships
- Create data validation reports

### 2.2 Data Schemas

#### 2.2.1 ATM Data Schema

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `atm_id` | string | Unique identifier | Format: A0001-A0500 |
| `latitude` | float | Latitude coordinate | Range: 12.8-13.2 |
| `longitude` | float | Longitude coordinate | Range: 77.4-77.8 |
| `area_type` | string | Area classification | Values: residential, commercial, industrial, mixed |
| `nearby_metro` | boolean | Within 500m of metro | - |
| `distance_to_metro` | float | Distance to nearest metro (km) | Range: 0-10 |
| `distance_to_police` | float | Distance to nearest police station (km) | Range: 0-15 |
| `avg_traffic_score` | float | Traffic density score | Range: 0-100 |
| `fraud_history_count` | integer | Historical fraud incidents | Range: 0-15 |
| `last_fraud_time` | timestamp | Last fraud occurrence | ISO 8601 format |
| `success_rate` | float | Transaction success rate | Range: 0-100 |
| `withdrawal_count_24h` | integer | Withdrawals in last 24h | Range: 50-500 |
| `withdrawal_count_week` | integer | Withdrawals in last week | Range: 300-3000 |
| `address` | string | Physical address | - |
| `bank_name` | string | Bank name | - |

#### 2.2.2 Transaction Data Schema

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `transaction_id` | string | Unique identifier | UUID v4 |
| `from_account` | string | Sender account ID | Foreign key to accounts |
| `to_account` | string | Receiver account ID | Foreign key to accounts |
| `amount` | float | Transaction amount (₹) | Range: 10,000-10,00,000 |
| `timestamp` | timestamp | Transaction time | ISO 8601 format |
| `is_fraudulent` | boolean | Fraud label | - |
| `complaint_id` | string | Linked complaint | Foreign key to complaints |
| `transaction_type` | string | Transaction type | Values: UPI, NEFT, IMPS, ATM |
| `network_id` | string | Mule network ID | Foreign key to networks |

#### 2.2.3 Mule Account Schema

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `account_id` | string | Unique identifier | Format: M0001-M9999 |
| `account_type` | string | Account classification | Values: mule, victim, normal |
| `network_id` | string | Mule network ID | Foreign key to networks |
| `tier` | integer | Position in network | Range: 1-6 |
| `commission_pct` | float | Commission percentage | Range: 2-5 |
| `created_date` | date | Account creation date | - |
| `is_flagged` | boolean | Flagged status | - |

#### 2.2.4 Complaint Data Schema

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `complaint_id` | string | Unique identifier | Format: C0001-C5000 |
| `victim_id` | string | Victim account ID | - |
| `victim_phone` | string | Victim phone number | Format: +91XXXXXXXXXX |
| `amount` | float | Amount lost (₹) | Range: 10,000-50,00,000 |
| `timestamp` | timestamp | Complaint filing time | ISO 8601 format |
| `fraud_type` | string | Type of fraud | Values: investment, KYC, UPI, loan, other |
| `fraudster_upi` | string | Fraudster UPI ID | - |
| `fraudster_phone` | string | Fraudster phone number | - |
| `fraudster_account` | string | Fraudster account ID | - |
| `status` | string | Complaint status | Values: SUBMITTED, ANALYZING, ACTION, RESOLVED |
| `notes` | string | Additional notes | - |

### 2.3 Data Generation Parameters

#### 2.3.1 ATM Generation

```python
ATM_GENERATION_PARAMS = {
    "num_atms": 500,
    "geographic_bounds": {
        "lat_min": 12.8,
        "lat_max": 13.2,
        "lon_min": 77.4,
        "lon_max": 77.8
    },
    "area_distribution": {
        "residential": 0.40,
        "commercial": 0.35,
        "mixed": 0.20,
        "industrial": 0.05
    },
    "fraud_hotspots": 100,
    "fraud_patterns": {
        "metro_proximity": 0.60,  # 60% of fraud ATMs near metro
        "weekend_night": 0.40     # 40% have weekend night pattern
    },
    "metro_stations": [
        ("MG Road", 12.9758, 77.6046),
        ("Indiranagar", 12.9784, 77.6408),
        ("Jayanagar", 12.9308, 77.5838),
        # ... more stations
    ]
}
```

#### 2.3.2 Mule Network Generation

```python
MULE_NETWORK_PARAMS = {
    "num_networks": 50,
    "mules_per_network": {
        "min": 3,
        "max": 6,
        "distribution": "uniform"
    },
    "transaction_chains": {
        "amount_range": (50000, 1000000),
        "commission_range": (0.02, 0.05),
        "time_delay_range": (0.5, 2.0),  # hours
        "hop_probability": 0.85
    },
    "behavioral_patterns": {
        "rapid_outflow": 0.70,          # 70% rapid outflow
        "suspicious_timing": 0.40,       # 40% 2-5 AM transactions
        "round_amounts": 0.30            # 30% round amounts
    }
}
```

#### 2.3.3 Complaint Generation

```python
COMPLAINT_GENERATION_PARAMS = {
    "num_complaints": 5000,
    "fraud_type_distribution": {
        "investment": 0.35,
        "UPI": 0.25,
        "KYC": 0.20,
        "loan": 0.12,
        "other": 0.08
    },
    "amount_distribution": {
        "mean": 200000,
        "std": 150000,
        "min": 10000,
        "max": 5000000
    },
    "time_patterns": {
        "peak_hours": [9, 10, 11, 14, 15, 16],
        "weekend_ratio": 0.30
    }
}
```

### 2.4 Implementation: Data Synthesis Module

#### models/utils/data_synthesis.py

```python
"""
Data Synthesis Module for SIH26184

This module generates realistic synthetic data for training the predictive
analytics framework. All data is fictional and designed to mimic real-world
patterns observed in cybercrime cases.

Usage:
    python -m models.utils.data_synthesis --config config/config.yaml
"""

import json
import logging
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from faker import Faker
from tqdm import tqdm

logger = logging.getLogger(__name__)


class ATMDataGenerator:
    """Generate synthetic ATM data for Bangalore region."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.fake = Faker('en_IN')
        np.random.seed(config['synthesis']['random_seed'])
        
    def generate_atms(self) -> pd.DataFrame:
        """Generate ATM data with geographic and operational features."""
        
        params = self.config['synthesis']
        num_atms = params['num_atms']
        bounds = params['bangalore']
        
        atms = []
        
        for i in tqdm(range(num_atms), desc="Generating ATMs"):
            atm_id = f"A{i:04d}"
            
            # Generate coordinates within Bangalore bounds
            latitude = np.random.uniform(bounds['lat_min'], bounds['lat_max'])
            longitude = np.random.uniform(bounds['lon_min'], bounds['lon_max'])
            
            # Determine area type
            area_type = np.random.choice(
                ['residential', 'commercial', 'mixed', 'industrial'],
                p=[0.40, 0.35, 0.20, 0.05]
            )
            
            # Calculate distance to nearest metro station
            metro_stations = params.get('metro_stations', [])
            nearby_metro, distance_to_metro = self._calculate_metro_proximity(
                latitude, longitude, metro_stations
            )
            
            # Generate other features
            distance_to_police = np.random.uniform(0.5, 15.0)
            avg_traffic_score = np.random.uniform(20, 100)
            
            # Determine if this is a fraud hotspot
            is_fraud_hotspot = i < params['fraud']['hotspot_atms']
            fraud_history_count = np.random.randint(1, 15) if is_fraud_hotspot else np.random.randint(0, 3)
            
            last_fraud_time = None
            if fraud_history_count > 0:
                last_fraud_time = self.fake.date_time_between(
                    start_date='-90d', end_date='now'
                ).isoformat()
            
            success_rate = np.random.uniform(85, 99.9)
            withdrawal_count_24h = np.random.randint(50, 500)
            withdrawal_count_week = np.random.randint(300, 3000)
            
            atms.append({
                'atm_id': atm_id,
                'latitude': round(latitude, 6),
                'longitude': round(longitude, 6),
                'area_type': area_type,
                'nearby_metro': nearby_metro,
                'distance_to_metro': round(distance_to_metro, 2),
                'distance_to_police': round(distance_to_police, 2),
                'avg_traffic_score': round(avg_traffic_score, 2),
                'fraud_history_count': fraud_history_count,
                'last_fraud_time': last_fraud_time,
                'success_rate': round(success_rate, 2),
                'withdrawal_count_24h': withdrawal_count_24h,
                'withdrawal_count_week': withdrawal_count_week,
                'address': self.fake.address().replace('\n', ', '),
                'bank_name': self.fake.company()
            })
        
        return pd.DataFrame(atms)
    
    def _calculate_metro_proximity(
        self, lat: float, lon: float, stations: List[Tuple]
    ) -> Tuple[bool, float]:
        """Calculate distance to nearest metro station."""
        
        if not stations:
            # Default stations if not provided
            stations = [
                ("MG Road", 12.9758, 77.6046),
                ("Indiranagar", 12.9784, 77.6408),
                ("Jayanagar", 12.9308, 77.5838),
            ]
        
        min_distance = float('inf')
        
        for _, station_lat, station_lon in stations:
            distance = self._haversine_distance(lat, lon, station_lat, station_lon)
            min_distance = min(min_distance, distance)
        
        nearby_metro = min_distance <= 0.5  # Within 500m
        return nearby_metro, min_distance
    
    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in km."""
        
        R = 6371  # Earth radius in km
        
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return R * c


class MuleNetworkGenerator:
    """Generate mule network transaction data."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.fake = Faker('en_IN')
        np.random.seed(config['synthesis']['random_seed'])
        
    def generate_networks(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Generate mule networks, accounts, and transactions."""
        
        params = self.config['synthesis']
        num_networks = params['num_mule_networks']
        
        networks = []
        accounts = []
        transactions = []
        
        for network_id in tqdm(range(num_networks), desc="Generating networks"):
            network_uid = f"N{network_id:04d}"
            
            # Generate mules for this network
            num_mules = np.random.randint(3, 7)
            
            # Create victim
            victim_id = f"V{network_id:04d}"
            accounts.append({
                'account_id': victim_id,
                'account_type': 'victim',
                'network_id': network_uid,
                'tier': 0,
                'commission_pct': 0.0,
                'created_date': self.fake.date_between(start_date='-365d', end_date='-30d').isoformat(),
                'is_flagged': False
            })
            
            # Create mules
            mule_ids = []
            for tier in range(1, num_mules + 1):
                mule_id = f"M{network_id:04d}_{tier}"
                mule_ids.append(mule_id)
                
                accounts.append({
                    'account_id': mule_id,
                    'account_type': 'mule',
                    'network_id': network_uid,
                    'tier': tier,
                    'commission_pct': round(np.random.uniform(0.02, 0.05), 3),
                    'created_date': self.fake.date_between(start_date='-365d', end_date='-30d').isoformat(),
                    'is_flagged': np.random.random() < 0.3
                })
            
            # Generate transactions
            complaint_id = f"C{network_id:04d}"
            amount = np.random.uniform(50000, 1000000)
            base_time = datetime.now() - timedelta(days=np.random.randint(1, 30))
            
            # Victim -> Mule 1
            remaining_amount = amount
            for i, mule_id in enumerate(mule_ids):
                commission = remaining_amount * accounts[mule_ids.index(mule_id) + len(accounts) - len(mule_ids)]['commission_pct'] if i > 0 else 0
                transfer_amount = remaining_amount - commission
                
                transactions.append({
                    'transaction_id': str(uuid.uuid4()),
                    'from_account': victim_id if i == 0 else mule_ids[i-1],
                    'to_account': mule_id,
                    'amount': round(transfer_amount, 2),
                    'timestamp': (base_time + timedelta(hours=i*0.5 + np.random.uniform(0.5, 2.0))).isoformat(),
                    'is_fraudulent': True,
                    'complaint_id': complaint_id,
                    'transaction_type': np.random.choice(['UPI', 'NEFT', 'IMPS']),
                    'network_id': network_uid
                })
                
                remaining_amount = transfer_amount
            
            # Last mule -> ATM withdrawal
            atm_id = f"A{np.random.randint(1, 501):04d}"
            transactions.append({
                'transaction_id': str(uuid.uuid4()),
                'from_account': mule_ids[-1],
                'to_account': atm_id,
                'amount': round(remaining_amount, 2),
                'timestamp': (base_time + timedelta(hours=len(mule_ids)*0.5 + np.random.uniform(0.5, 2.0))).isoformat(),
                'is_fraudulent': True,
                'complaint_id': complaint_id,
                'transaction_type': 'ATM',
                'network_id': network_uid
            })
            
            networks.append({
                'network_id': network_uid,
                'num_mules': num_mules,
                'total_amount': round(amount, 2),
                'created_date': base_time.date().isoformat(),
                'status': 'ACTIVE'
            })
        
        return pd.DataFrame(networks), pd.DataFrame(accounts), pd.DataFrame(transactions)


class ComplaintDataGenerator:
    """Generate complaint data."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.fake = Faker('en_IN')
        np.random.seed(config['synthesis']['random_seed'])
        
    def generate_complaints(self, networks_df: pd.DataFrame, accounts_df: pd.DataFrame) -> pd.DataFrame:
        """Generate complaint records."""
        
        params = self.config['synthesis']
        num_complaints = params['num_complaints']
        
        complaints = []
        
        fraud_types = ['investment', 'UPI', 'KYC', 'loan', 'other']
        fraud_weights = [0.35, 0.25, 0.20, 0.12, 0.08]
        
        for i in tqdm(range(num_complaints), desc="Generating complaints"):
            complaint_id = f"C{i:04d}"
            
            # Get victim from accounts
            victim_accounts = accounts_df[accounts_df['account_type'] == 'victim']
            if i < len(victim_accounts):
                victim_id = victim_accounts.iloc[i]['account_id']
            else:
                victim_id = f"V{i:04d}"
            
            fraud_type = np.random.choice(fraud_types, p=fraud_weights)
            amount = np.random.lognormal(mean=12, sigma=1)
            amount = max(10000, min(5000000, amount))
            
            complaints.append({
                'complaint_id': complaint_id,
                'victim_id': victim_id,
                'victim_phone': f"+91{self.fake.msisdn()[3:]}",
                'amount': round(amount, 2),
                'timestamp': self.fake.date_time_between(start_date='-90d', end_date='now').isoformat(),
                'fraud_type': fraud_type,
                'fraudster_upi': f"{self.fake.user_name()}@{np.random.choice(['paytm', 'gpay', 'phonepe'])}",
                'fraudster_phone': f"+91{self.fake.msisdn()[3:]}",
                'fraudster_account': f"M{i:04d}_1",
                'status': np.random.choice(['SUBMITTED', 'ANALYZING', 'ACTION', 'RESOLVED'], 
                                          p=[0.2, 0.3, 0.3, 0.2]),
                'notes': self.fake.sentence()
            })
        
        return pd.DataFrame(complaints)


def generate_all_data(config: Dict) -> Dict[str, pd.DataFrame]:
    """Generate all synthetic data."""
    
    logger.info("Starting data synthesis...")
    
    # Initialize generators
    atm_gen = ATMDataGenerator(config)
    mule_gen = MuleNetworkGenerator(config)
    complaint_gen = ComplaintDataGenerator(config)
    
    # Generate data
    atms_df = atm_gen.generate_atms()
    networks_df, accounts_df, transactions_df = mule_gen.generate_networks()
    complaints_df = complaint_gen.generate_complaints(networks_df, accounts_df)
    
    logger.info(f"Generated {len(atms_df)} ATMs")
    logger.info(f"Generated {len(networks_df)} mule networks")
    logger.info(f"Generated {len(accounts_df)} accounts")
    logger.info(f"Generated {len(transactions_df)} transactions")
    logger.info(f"Generated {len(complaints_df)} complaints")
    
    return {
        'atms': atms_df,
        'networks': networks_df,
        'accounts': accounts_df,
        'transactions': transactions_df,
        'complaints': complaints_df
    }


def save_data(data: Dict[str, pd.DataFrame], output_dir: Path):
    """Save generated data to CSV files."""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for name, df in data.items():
        output_path = output_dir / f"{name}.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Saved {name} to {output_path}")


def main():
    """Main entry point for data synthesis."""
    
    import argparse
    import yaml
    
    parser = argparse.ArgumentParser(description="Generate synthetic data")
    parser.add_argument('--config', type=str, default='config/config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--output', type=str, default='data/raw',
                       help='Output directory for generated data')
    
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Generate data
    data = generate_all_data(config)
    
    # Save data
    save_data(data, Path(args.output))
    
    logger.info("Data synthesis complete!")


if __name__ == '__main__':
    main()
```

### 2.5 Validation Checks

```python
# models/utils/data_validation.py

def validate_atm_data(df: pd.DataFrame) -> Dict[str, bool]:
    """Validate ATM data quality."""
    
    checks = {}
    
    # Check unique ATM IDs
    checks['unique_atm_ids'] = df['atm_id'].nunique() == len(df)
    
    # Check coordinates within bounds
    checks['valid_coordinates'] = (
        (df['latitude'] >= 12.8) & (df['latitude'] <= 13.2) &
        (df['longitude'] >= 77.4) & (df['longitude'] <= 77.8)
    ).all()
    
    # Check fraud history count
    checks['valid_fraud_count'] = (
        (df['fraud_history_count'] >= 0) & 
        (df['fraud_history_count'] <= 15)
    ).all()
    
    # Check traffic scores
    checks['valid_traffic_scores'] = (
        (df['avg_traffic_score'] >= 0) & 
        (df['avg_traffic_score'] <= 100)
    ).all()
    
    return checks


def validate_transaction_data(df: pd.DataFrame) -> Dict[str, bool]:
    """Validate transaction data quality."""
    
    checks = {}
    
    # Check for circular transactions
    checks['no_circular_transactions'] = not (
        df['from_account'] == df['to_account']
    ).any()
    
    # Check all amounts positive
    checks['positive_amounts'] = (df['amount'] > 0).all()
    
    # Check unique transaction IDs
    checks['unique_transaction_ids'] = df['transaction_id'].nunique() == len(df)
    
    return checks
```

### 2.6 Deliverables

| Deliverable | Location | Records | Status |
|-------------|----------|---------|--------|
| ATM data | `data/raw/atms.csv` | 500 | Pending |
| Transaction data | `data/raw/transactions.csv` | 20,000+ | Pending |
| Account data | `data/raw/accounts.csv` | 150-300 | Pending |
| Complaint data | `data/raw/complaints.csv` | 5,000 | Pending |
| Network metadata | `data/raw/networks.csv` | 50 | Pending |
| Validation report | `data/validation/validation_report.json` | - | Pending |

---

## Phase 3: Feature Engineering (Days 3-4)

### 3.1 Objectives

- Transform raw data into model-ready features
- Normalize and scale features
- Create temporal features
- Build PyTorch data loaders

### 3.2 ATM Feature Engineering

```python
# models/utils/feature_engineering.py

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

class ATMFeatureEngineer:
    """Feature engineering for ATM data."""
    
    def __init__(self):
        self.scalers = {}
        
    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transform ATM data into feature matrix."""
        
        features = []
        
        # Geographic features (scale to [-1, 1])
        lat_scaler = MinMaxScaler(feature_range=(-1, 1))
        features.append(lat_scaler.fit_transform(df[['latitude']]))
        self.scalers['latitude'] = lat_scaler
        
        lon_scaler = MinMaxScaler(feature_range=(-1, 1))
        features.append(lon_scaler.fit_transform(df[['longitude']]))
        self.scalers['longitude'] = lon_scaler
        
        # Distance features (log transform)
        distance_to_metro = np.log1p(df['distance_to_metro'].values).reshape(-1, 1)
        distance_scaler = StandardScaler()
        features.append(distance_scaler.fit_transform(distance_to_metro))
        self.scalers['distance_to_metro'] = distance_scaler
        
        # Area type (one-hot encode)
        area_types = pd.get_dummies(df['area_type'], prefix='area')
        features.append(area_types.values)
        
        # Traffic score (min-max scale)
        traffic_scaler = MinMaxScaler()
        features.append(traffic_scaler.fit_transform(df[['avg_traffic_score']]))
        self.scalers['traffic'] = traffic_scaler
        
        # Fraud history (clip and normalize)
        fraud_history = df['fraud_history_count'].clip(0, 15).values.reshape(-1, 1)
        fraud_scaler = StandardScaler()
        features.append(fraud_scaler.fit_transform(fraud_history))
        self.scalers['fraud_history'] = fraud_scaler
        
        # Combine all features
        feature_matrix = np.hstack(features)
        
        return feature_matrix
```

### 3.3 Account Feature Engineering

```python
class AccountFeatureEngineer:
    """Feature engineering for account data (mule detection)."""
    
    def compute_features(self, accounts_df: pd.DataFrame, transactions_df: pd.DataFrame) -> np.ndarray:
        """Compute account-level features."""
        
        features = []
        
        for account_id in accounts_df['account_id']:
            # Get account transactions
            outgoing = transactions_df[transactions_df['from_account'] == account_id]
            incoming = transactions_df[transactions_df['to_account'] == account_id]
            
            # Transaction velocity
            if len(outgoing) > 0 or len(incoming) > 0:
                time_span = 24  # hours
                total_txs = len(outgoing) + len(incoming)
                velocity = total_txs / time_span
            else:
                velocity = 0
            
            # Total inflow/outflow
            total_inflow = incoming['amount'].sum() if len(incoming) > 0 else 0
            total_outflow = outgoing['amount'].sum() if len(outgoing) > 0 else 0
            
            # Outflow ratio
            outflow_ratio = total_outflow / (total_inflow + 1e-6)
            
            # Holding time (average)
            holding_time = self._compute_holding_time(incoming, outgoing)
            
            # Suspicious timing (2-5 AM)
            suspicious_timing = self._count_suspicious_hours(outgoing)
            
            # Degrees
            in_degree = len(incoming)
            out_degree = len(outgoing)
            
            features.append([
                velocity,
                total_inflow,
                total_outflow,
                outflow_ratio,
                holding_time,
                0,  # connected_complaints (to be filled later)
                suspicious_timing,
                in_degree,
                out_degree
            ])
        
        return np.array(features)
```

### 3.4 Deliverables

| Deliverable | Location | Status |
|-------------|----------|--------|
| ATM features | `data/processed/atm_features.npy` | Pending |
| Account features | `data/processed/account_features.npy` | Pending |
| Feature scaler | `models/utils/scaler.pkl` | Pending |
| Preprocessing module | `models/utils/preprocessing.py` | Pending |

---

## Phase 4: Spatio-Temporal Transformer (Days 4-6)

### 4.1 Model Architecture

```python
# models/spatio_temporal/model.py

import torch
import torch.nn as nn
import torch.nn.functional as F

class SpatioTemporalTransformer(nn.Module):
    """
    Spatio-Temporal Transformer for ATM prediction.
    
    Architecture:
        - Spatial encoder: MLP for geographic features
        - Temporal encoder: MLP for time features
        - Cross-attention: Fuse spatial and temporal
        - Transformer encoder: 6 layers, 256 hidden
        - Classifier: Linear layers for ATM prediction
    """
    
    def __init__(self, config: dict):
        super().__init__()
        
        # Spatial encoder (4 -> 64 -> 128)
        self.spatial_encoder = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 128)
        )
        
        # Temporal encoder (6 -> 64 -> 128)
        self.temporal_encoder = nn.Sequential(
            nn.Linear(6, 64),
            nn.ReLU(),
            nn.Linear(64, 128)
        )
        
        # Cross-attention
        self.cross_attention = nn.MultiheadAttention(
            embed_dim=256,
            num_heads=8,
            dropout=0.1,
            batch_first=True
        )
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=256,
            nhead=8,
            dim_feedforward=1024,
            dropout=0.1,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=6)
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, config['num_atms'])
        )
    
    def forward(self, spatial_features, temporal_features):
        # Encode spatial
        spatial_encoded = self.spatial_encoder(spatial_features)  # (batch, 128)
        
        # Encode temporal
        temporal_encoded = self.temporal_encoder(temporal_features)  # (batch, 128)
        
        # Concatenate
        combined = torch.cat([spatial_encoded, temporal_encoded], dim=-1)  # (batch, 256)
        
        # Add sequence dimension for transformer
        combined = combined.unsqueeze(1)  # (batch, 1, 256)
        
        # Cross-attention
        attended, _ = self.cross_attention(combined, combined, combined)
        
        # Transformer
        transformer_out = self.transformer(attended)
        
        # Remove sequence dimension
        transformer_out = transformer_out.squeeze(1)  # (batch, 256)
        
        # Classify
        logits = self.classifier(transformer_out)  # (batch, num_atms)
        
        return logits
```

### 4.2 Training Script

```python
# models/spatio_temporal/train.py

def train_model(config: dict):
    """Train spatio-temporal transformer."""
    
    # Initialize model
    model = SpatioTemporalTransformer(config['model'])
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['training']['learning_rate'],
                                   weight_decay=config['training']['weight_decay'])
    
    # Scheduler
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', patience=5, factor=0.5
    )
    
    # Training loop
    for epoch in range(config['training']['epochs']):
        model.train()
        
        for batch in train_loader:
            spatial_features = batch['spatial'].to(device)
            temporal_features = batch['temporal'].to(device)
            labels = batch['label'].to(device)
            
            # Forward pass
            logits = model(spatial_features, temporal_features)
            loss = criterion(logits, labels)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            
            optimizer.step()
        
        # Validation
        val_loss, val_acc = validate(model, val_loader, criterion)
        
        # Scheduler step
        scheduler.step(val_loss)
        
        # Log to MLflow
        mlflow.log_metrics({
            'train_loss': loss.item(),
            'val_loss': val_loss,
            'val_accuracy': val_acc
        })
```

### 4.3 Deliverables

| Deliverable | Location | Status |
|-------------|----------|--------|
| Model definition | `models/spatio_temporal/model.py` | Pending |
| Training script | `models/spatio_temporal/train.py` | Pending |
| Trained model | `models/spatio_temporal/model.pth` | Pending |
| Model config | `models/spatio_temporal/config.yaml` | Pending |

---

## Phase 5-15: [Abbreviated for length]

*The full implementation plan continues with similar detail for:*

- Phase 5: Graph Neural Network
- Phase 6: Mule Scoring Algorithm  
- Phase 7: Hyperparameter Optimization
- Phase 8: Model Serving API
- Phase 9: Banking API Mock
- Phase 10: Retraining Pipeline
- Phase 11: MLflow Integration
- Phase 12: LLM Integration
- Phase 13: Testing Strategy
- Phase 14: Documentation
- Phase 15: Deployment

---

## Verification & Acceptance Criteria

### End-to-End Test Scenarios

#### Scenario 1: Complaint Submission Flow

```
1. Submit complaint via API
   POST /api/complaint
   {
     "amount": 500000,
     "fraud_type": "investment",
     "fraudster_upi": "scammer@paytm",
     "fraudster_phone": "+919876543210"
   }

2. Verify response includes:
   - complaint_id
   - atm_predictions (top 3)
   - mule_risk_scores

3. Check prediction time < 500ms
```

#### Scenario 2: Mule Detection Flow

```
1. Query mule network
   GET /api/detect/mules?complaint_id=C1001

2. Verify response includes:
   - List of mule accounts
   - GNN probability for each
   - Rule score for each
   - Final risk score
   - Recommended action

3. Validate risk levels are correct
```

### Success Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| ATM Top-1 Accuracy | >85% | - | Pending |
| ATM Top-3 Accuracy | >95% | - | Pending |
| Mule Detection Accuracy | >90% | - | Pending |
| Mule Detection F1 | >90% | - | Pending |
| API Latency (p99) | <500ms | - | Pending |
| API Throughput | >100 req/s | - | Pending |
| Test Coverage | >80% | - | Pending |

---

## Risk Management

### Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| GPU unavailable | Medium | High | CPU fallback, Colab backup |
| Data quality issues | Low | High | Comprehensive validation |
| Model overfitting | Medium | Medium | Early stopping, dropout |
| API performance | Low | High | Load testing, optimization |
| Security vulnerabilities | Low | Critical | Code review, penetration testing |

---

## Resource Requirements

### Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | 4GB VRAM | 8GB+ VRAM (RTX 3060) |
| RAM | 16GB | 32GB |
| Storage | 50GB SSD | 100GB SSD |
| CPU | 4 cores | 8 cores |

### Software

| Software | Version |
|----------|---------|
| Python | 3.9+ |
| CUDA | 11.8+ |
| Docker | 24+ |
| PostgreSQL | 15+ |
| Neo4j | 5.x |

### External Services

| Service | Purpose |
|---------|---------|
| OpenAI API | LLM integration |
| MLflow Server | Experiment tracking |
| Redis Cloud | Caching (optional) |

---

## Appendices

### A. API Endpoint Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /predict/atm | Predict ATM locations |
| POST | /detect/mules | Detect mule accounts |
| POST | /trigger/verification | Trigger Step-Up |
| GET | /model/status | Model health |
| GET | /model/metrics | Performance metrics |

### B. Configuration Reference

See `config/config.yaml` for complete configuration options.

### C. Troubleshooting Guide

#### Common Issues

1. **CUDA out of memory**
   - Reduce batch size
   - Use gradient accumulation
   - Enable mixed precision

2. **Slow training**
   - Enable mixed precision (AMP)
   - Increase num_workers in DataLoader
   - Use pin_memory=True

3. **API timeout**
   - Increase timeout in config
   - Optimize model inference
   - Use batching

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-09-04 | AI/ML Lead | Initial implementation plan |

---

**End of Implementation Plan**

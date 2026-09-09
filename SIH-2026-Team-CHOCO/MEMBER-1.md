# MEMBER 1 — AI/ML Lead Reference

## 1. Role Overview
- Member 1 is the "Brain" of the project. All intelligent predictions, pattern recognition, and AI-powered decision-making flows through this member.
- Has primary GPU access and handles all heavy computational work.
- Title: AI/ML Lead

## 2. Core Responsibilities

| Responsibility | Description |
|---|---|
| **Data Synthesis** | Generating realistic synthetic datasets for ATMs, mule networks, complaints, and transactions. |
| **Spatio-Temporal Transformer** | Developing the ATM Prediction model using transformer architectures. |
| **Graph Neural Network (GNN)** | Developing the Mule Detection model using PyTorch Geometric. |
| **Mule Scoring Algorithm** | Creating a hybrid scoring algorithm combining GNN outputs with rule-based metrics. |
| **Model Training & Evaluation** | Overseeing the training loops, validation checkpointing, and performance metrics. |
| **Model Serving API endpoints** | Exposing models via FastAPI for inference. |
| **Banking API Mock** | Creating mock banking interfaces for transaction simulation. |
| **Retraining Pipeline** | Building automated pipelines for model retraining and promotion using MLflow. |
| **MLflow Integration** | Setting up experiment tracking and model registry. |
| **LLM Integration** | Providing NLP support for the WhatsApp chatbot component. |

## 3. Technology Stack

| Category | Technologies |
|---|---|
| **Languages & Frameworks** | Python 3.9+, PyTorch 2.1+, PyTorch Geometric 2.3+, FastAPI 0.100+ |
| **Data Processing & ML** | NumPy, Pandas, Scikit-learn, Optuna 3.3+, MLflow 2.5+, LangChain 0.1+ |
| **Tools & Infrastructure** | Docker, TensorBoard, Joblib |

**Hardware Requirements:**
- NVIDIA GPU 4GB+ VRAM minimum
- 16GB RAM minimum
- 50GB SSD

## 4. What Has Been Built (Current Status)

Everything is COMPLETE.

### 4.1 Spatio-Temporal Transformer (ATM Prediction)
- `models/spatio_temporal/model.py` — COMPLETE — `SpatioTemporalTransformer` class:
  - `SpatialEncoder`: FC MLP (4→64→128) with BatchNorm & ReLU
  - `TemporalEncoder`: FC MLP (6→64→128) with BatchNorm & ReLU  
  - Cross-attention: `nn.MultiheadAttention`, 8 heads, embed_dim=128, concatenation → 256
  - `TransformerEncoder`: 6 layers, 8 heads, d_model=256, dim_feedforward=512, dropout=0.1
  - Classifier head → Logits over 500 ATM locations
- `models/spatio_temporal/predict.py` — COMPLETE — `STMPredictor` class: loads `best_model.pt`, scalers, encoders; performs feature transforms, softmax probs, top-K ranking, threshold filtering
- `models/spatio_temporal/train.py` — COMPLETE — Production training loop with MLflow run tracking, TensorBoard, early stopping on Top-3 accuracy, CosineAnnealingLR, validation checkpointing
- `models/spatio_temporal/config.yaml` — COMPLETE — Hyperparameters

### 4.2 Graph Neural Network (Mule Detection)
- `models/mule_detection/model.py` — COMPLETE — `MuleDetectionGNN` using 3-layer SAGEConv (PyTorch Geometric): Input 9→128→64→32, Dropout 0.2, ReLU, Classification MLP head 32→16→1 (BCEWithLogitsLoss)
- `models/mule_detection/predict.py` — COMPLETE — `MulePredictor`: single-account dict scoring AND full PyG Data graph inference, calibrated mule probabilities
- `models/mule_detection/train.py` — COMPLETE — Full-graph and mini-batch NeighborLoader training, imbalance loss weighting (pos_weight), validation F1-score early stopping
- `models/mule_detection/config.yaml` — COMPLETE

### 4.3 Retraining Pipeline
- `models/retraining/pipeline.py` — COMPLETE — `RetrainingPipeline` with MLflow registry integration. Periodically runs data synthesis/loading, triggers STM and GNN training, evaluates against deployment criteria (Top-3 Acc > 75%, GNN F1 > 0.80), promotes candidate models to production

### 4.4 Utilities
- `models/utils/data_synthesis.py` — COMPLETE — `DataSynthesizer`: 500 ATMs (Mumbai/Delhi coordinates, metro/police proximity), 50 mule networks (layered chains: victim→layer1→layer2→cash-out), 2,000 complaints, 10,000 transactions
- `models/utils/scoring.py` — COMPLETE — Hybrid mule scoring: 70% GNN + 30% RuleScorer (velocity, rapid outflow, complaint links, odd-hour timing, amount patterns, outflow ratio). Outputs risk tier, risk color, recommended enforcement action
- `models/utils/risk_mapper.py` — COMPLETE — Geo-spatial risk heatmaps (GeoJSON/folium)
- `models/utils/feature_engineering.py` — COMPLETE — Feature transforms, cyclic time encodings (sin/cos of hour/day), spatial distance normalization
- `models/utils/mlflow_tracking.py` & `mlflow_utils.py` — COMPLETE — Experiment tracking and model registry utilities
- `models/utils/tensorboard_utils.py` — COMPLETE
- `models/utils/evaluation.py` & `optimize.py` — COMPLETE — Multi-metric evaluation and Optuna hyperparameter optimization

### 4.5 Configuration
- `config/config.yaml` — COMPLETE — Master config: 500 ATMs, 50 mule networks, 2k complaints, 10k txns, STM architecture (input dims 4 and 6, embed 128, d_model 256, 6 layers), GNN (input 9, 3 SAGEConv layers [128,64,32]), scoring weights (70% GNN, 30% Rules)

### 4.6 Data
- `data/processed/` — Contains pre-fitted `spatial_scaler.joblib`, `temporal_scaler.joblib`, `label_encoders.joblib`
- `data/validation/` — CSV datasets: `atms.csv` (50 rows), `complaints.csv` (500 rows), `mule_networks.csv` (5 rows), `transactions.csv` (2,000 rows)

### 4.7 Tests (Member 1 owns)
- `tests/test_spatio_temporal.py` — STM forward pass, output shape (batch, 500), backprop gradients, top-K accuracy
- `tests/test_mule_detection.py` — GNN PyG data forward pass, neighbor aggregation, SAGEConv weights
- `tests/test_mule_scoring.py` & `tests/test_scoring.py` — RuleScorer, hybrid formula, edge cases, thresholds

## 5. Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| ATM Prediction Top-1 | >85% | Test set |
| ATM Prediction Top-3 | >95% | Test set |
| Mule Detection Accuracy | >90% | Test set |
| Mule Detection F1 | >90% | Test set |
| API Latency p99 | <500ms | Load testing |
| API Throughput | >100 req/s | Load testing |

## 6. Integration Points With Other Members

### 6.1 With Member 2 (Backend & Database)
- Member 2 provides PostgreSQL (`api/database/postgres.py`) and Neo4j (`api/database/neo4j.py`) async engines
- Member 1's models are loaded at startup via `api/main.py` lifespan context
- Member 1's prediction endpoints are mounted at `/predict/stm` and `/predict/mule` in `api/main.py`
- Member 2's routes in `api/routes/predict.py` and `api/routes/detect.py` call Member 1's `STMPredictor` and `MulePredictor`
- Member 2's Celery tasks (`api/tasks/scoring.py`) run Member 1's hybrid scoring asynchronously
- Member 1's `data_synthesis.py` generates data that Member 2's `scripts/neo4j_populate.py` seeds into Neo4j
- The retraining pipeline (`models/retraining/pipeline.py`) uses MLflow model registry which Member 2's `api/main.py` checks at startup

### 6.2 With Member 3 (Frontend & DevOps)
- Member 3's Command Center (`apps/command-center`) consumes Member 1's predictions via:
  - Leaflet Heatmap: expects `GET /api/v1/heatmap` returning ATM coordinates + risk scores
  - vis-network Graph: expects `GET /api/v1/mules/network` returning nodes + edges
- Member 3's Field Dashboard (`apps/field-dashboard`) receives real-time alerts via WebSocket event `NEW_ALERT` which fires when Member 1's model flags a high-risk ATM
- Member 3 deploys Member 1's models via Docker containers defined in `deployments/docker/Dockerfile.gpu` (CUDA 11.8)
- Member 3's Streamlit dashboard (`dashboard/streamlit_dashboard.py`) visualizes Member 1's training curves

### 6.3 With Member 4 (Victim Portal / Integration)
- Member 4's Victim Portal submits complaints via `POST /api/v1/victim/complaints`
- These complaints trigger Member 1's ML pipeline: complaint → feature extraction → STM prediction → GNN mule detection → hybrid scoring → alert generation
- Member 4's Flask demo (`ruma/app.py`) simulates Member 1's training curves and prediction endpoints for presentation purposes
- Member 4's Streamlit dashboard reads Member 1's model artifacts and training logs

## 7. API Endpoints Member 1 Owns

| Method | Path | Description |
|---|---|---|
| POST | `/predict/stm` | ATM location prediction — accepts complaint features, returns top-K ATM probabilities |
| POST | `/predict/mule` | Mule account detection — accepts account/transaction features, returns mule probability |
| GET | `/models/info` | Model registry status — shows loaded models, versions, metrics |
| GET | `/health` | Health check — verifies model availability |

## 8. Data Schemas

### ATM Data (500 ATMs)
- **atm_id** (`str`): Unique identifier for the ATM
- **latitude** (`float`): ATM geographical latitude
- **longitude** (`float`): ATM geographical longitude
- **area_type** (`str`): Type of area (e.g., commercial, residential)
- **nearby_metro** (`bool`): Indicator if near a metro station
- **distance_to_metro** (`float`): Distance in km to the closest metro
- **distance_to_police** (`float`): Distance in km to the nearest police station
- **avg_traffic_score** (`float`): Average pedestrian/vehicular traffic metric
- **fraud_history_count** (`int`): Total historical frauds at this ATM
- **last_fraud_time** (`datetime`): Timestamp of the most recent fraud
- **success_rate** (`float`): Historical accuracy of flagging fraud
- **withdrawal_count_24h** (`int`): Total withdrawals in the past 24 hours
- **withdrawal_count_week** (`int`): Total withdrawals in the past week

### Complaint Data
- **complaint_id** (`str`): Unique identifier for the complaint
- **victim_id** (`str`): Reference to the victim's profile
- **amount** (`float`): Defrauded amount
- **timestamp** (`datetime`): Date and time of the incident
- **fraud_type** (`str`): Category of fraud (e.g., phishing, card skimming)
- **fraudster_upi** (`str`): UPI ID used by the attacker
- **fraudster_phone** (`str`): Phone number used by the attacker
- **fraudster_account** (`str`): Bank account number of the attacker
- **victim_account** (`str`): Affected account of the victim
- **victim_phone** (`str`): Phone number of the victim
- **status** (`str`): Current processing status (e.g., Open, Under Investigation, Closed)

### Transaction Data
- **transaction_id** (`str`): Unique transaction identifier
- **amount** (`float`): Transaction value
- **timestamp** (`datetime`): Time of transaction execution
- **is_fraudulent** (`bool`): Label indicating if the transaction is fraudulent
- **complaint_id** (`str`): Linked complaint identifier, if any
- **from_account** (`str`): Source account number
- **to_account** (`str`): Destination account number

### Mule Network Data
- **network_id** (`str`): Unique identifier for the mule network
- **mule_accounts** (`list[str]`): List of accounts identified as mules
- **victim_accounts** (`list[str]`): List of source victim accounts
- **atm_ids** (`list[str]`): Associated ATM identifiers used for cash-outs
- **total_amount** (`float`): Cumulative fraudulent volume in the network
- **layers** (`int`): Number of intermediary layers in the transaction chain

## 9. File Structure Member 1 Owns

```
models/
├── spatio_temporal/
│   ├── model.py
│   ├── predict.py
│   ├── train.py
│   └── config.yaml
├── mule_detection/
│   ├── model.py
│   ├── predict.py
│   ├── train.py
│   └── config.yaml
├── retraining/
│   └── pipeline.py
└── utils/
    ├── data_synthesis.py
    ├── scoring.py
    ├── risk_mapper.py
    ├── feature_engineering.py
    ├── mlflow_tracking.py
    ├── mlflow_utils.py
    ├── tensorboard_utils.py
    ├── evaluation.py
    └── optimize.py
config/
└── config.yaml
data/
├── processed/
│   ├── spatial_scaler.joblib
│   ├── temporal_scaler.joblib
│   └── label_encoders.joblib
└── validation/
    ├── atms.csv
    ├── complaints.csv
    ├── mule_networks.csv
    └── transactions.csv
tests/
├── test_spatio_temporal.py
├── test_mule_detection.py
├── test_mule_scoring.py
└── test_scoring.py
```

## 10. Commands to Run

```bash
# Generate synthetic data
python -m models.utils.data_synthesis --config config/config.yaml

# Train STM
python -m models.spatio_temporal.train --config config/config.yaml

# Train GNN
python -m models.mule_detection.train --config config/config.yaml

# Run retraining pipeline
python -m models.retraining.pipeline

# Run tests
pytest tests/test_spatio_temporal.py tests/test_mule_detection.py tests/test_scoring.py -v

# Start MLflow UI
mlflow ui --port 5000

# Start TensorBoard
tensorboard --logdir=runs/ --port 6006
```

## 11. What's Remaining / TODO
- All ML code is COMPLETE
- Ensure model artifacts (.pth files) are generated and saved to `models/spatio_temporal/` and `models/mule_detection/`
- Verify retraining pipeline promotion criteria work end-to-end with MLflow model registry
- Fine-tune hyperparameters with Optuna if accuracy targets aren't met

## 12. Important Notes
- The `ml/` directory at the project root is EMPTY — all ML code lives in `models/`
- The `backend/` directory at the project root is EMPTY — all backend code lives in `api/`
- Model weights are NOT committed to git — they must be generated by running training
- GPU is required for training; CPU fallback exists for inference

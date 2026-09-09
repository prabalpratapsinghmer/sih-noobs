# SIH26184 — Model Architecture

## Overview

The system uses two core ML models and a hybrid scoring algorithm:

1. **Spatio-Temporal Transformer** — Predicts ATM withdrawal locations
2. **Graph Neural Network (GNN)** — Detects money mule accounts
3. **Hybrid Scoring System** — Combines GNN + rules for final risk assessment

---

## 1. Spatio-Temporal Transformer

### Purpose
Predict which ATM(s) a fraudster will use to withdraw stolen funds based on:
- Geographic context (complaint origin, ATM locations, metro proximity)
- Temporal patterns (time of day, day of week, time since complaint)

### Architecture

```
Input: Spatial Features (4D) + Temporal Features (7D)
                    │                       │
                    ▼                       ▼
           ┌────────────────┐     ┌────────────────┐
           │ Spatial Encoder │     │ Temporal Encoder│
           │ (MLP: 4→64→128)│     │ (MLP: 7→64→128) │
           └────────┬───────┘     └────────┬───────┘
                    │                       │
                    └───────┬───────────────┘
                            │ Concatenate (256D)
                            ▼
                    ┌────────────────┐
                    │ Cross-Attention │
                    │ (8 heads, 256D) │
                    └────────┬───────┘
                             ▼
                    ┌────────────────┐
                    │ Transformer     │
                    │ Encoder         │
                    │ (6 layers,      │
                    │  8 heads, 256D) │
                    └────────┬───────┘
                             ▼
                    ┌────────────────┐
                    │ Classifier      │
                    │ (256→128→500)   │
                    └────────┬───────┘
                             ▼
                    Output: 500 ATM probabilities
```

### Input Features

**Spatial (4D):**
| Feature | Description | Range |
|---------|-------------|-------|
| Latitude | Scaled coordinate | [-1, 1] |
| Longitude | Scaled coordinate | [-1, 1] |
| Distance to metro | Log-transformed, standardized | ℝ |
| Distance to police | Log-transformed, standardized | ℝ |

**Temporal (7D):**
| Feature | Description | Range |
|---------|-------------|-------|
| Hour sin | sin(2π·hour/24) | [-1, 1] |
| Hour cos | cos(2π·hour/24) | [-1, 1] |
| Day sin | sin(2π·day/7) | [-1, 1] |
| Day cos | cos(2π·day/7) | [-1, 1] |
| Is weekend | Binary flag | {0, 1} |
| Time since complaint | Hours elapsed | [0, ∞) |
| Fraud spike hour | Historical peak hour | [0, 23] |

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Epochs | 200 |
| Batch size | 32 |
| Learning rate | 1e-4 |
| Optimizer | AdamW |
| Loss | CrossEntropyLoss (label smoothing 0.1) |
| Weight decay | 1e-4 |
| Gradient clipping | 1.0 |
| Early stopping patience | 20 epochs |
| LR scheduler | ReduceLROnPlateau (factor 0.5, patience 5) |

### Target Metrics

| Metric | Target |
|--------|--------|
| Top-1 accuracy | > 85% |
| Top-3 accuracy | > 95% |
| Inference latency | < 50ms |

---

## 2. Graph Neural Network (Mule Detection)

### Purpose
Detect money mule accounts by analyzing the transaction graph topology using GraphSAGE convolutional layers.

### Architecture

```
Input: Node Features (9D) + Edge Index (transaction graph)
                    │
                    ▼
           ┌────────────────┐
           │ GraphSAGE Conv  │
           │ Layer 1          │
           │ (9 → 128)        │
           │ + ReLU + Dropout │
           └────────┬───────┘
                    ▼
           ┌────────────────┐
           │ GraphSAGE Conv  │
           │ Layer 2          │
           │ (128 → 64)       │
           │ + ReLU + Dropout │
           └────────┬───────┘
                    ▼
           ┌────────────────┐
           │ GraphSAGE Conv  │
           │ Layer 3          │
           │ (64 → 32)        │
           │ + ReLU + Dropout │
           └────────┬───────┘
                    ▼
           ┌────────────────┐
           │ Classifier MLP   │
           │ (32 → 64 → 1)    │
           └────────┬───────┘
                    ▼
           Output: Mule probability (sigmoid)
```

### Node Features (9D)

| Feature | Description |
|---------|-------------|
| Velocity | Transactions per hour |
| Total inflow | Sum of incoming funds (₹) |
| Total outflow | Sum of outgoing funds (₹) |
| Outflow ratio | outflow / (inflow + ε) |
| Holding time | Avg minutes before forwarding |
| Connected complaints | Linked complaint count |
| Suspicious timing | 2–5 AM transaction count |
| In-degree | Incoming transaction edges |
| Out-degree | Outgoing transaction edges |

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Epochs | 100 |
| Batch size | 64 |
| Learning rate | 1e-3 |
| Optimizer | Adam |
| Loss | BCEWithLogitsLoss (pos_weight=5.0) |
| Weight decay | 1e-4 |
| Gradient clipping | 1.0 |
| Early stopping patience | 15 epochs |

### Target Metrics

| Metric | Target |
|--------|--------|
| Accuracy | > 90% |
| F1-score | > 90% |
| AUC-ROC | > 0.95 |

---

## 3. Hybrid Scoring System

The final mule risk score combines GNN predictions with rule-based heuristics:

```
Final Score = 0.7 × GNN_probability × 100 + 0.3 × Rule_score
```

### Rule-Based Scoring Weights

| Signal | Weight | Description |
|--------|--------|-------------|
| Velocity | 25 | Abnormally high transaction frequency |
| Rapid outflow | 20 | >90% of inflow sent out quickly |
| Connected complaints | 20 | Multiple linked fraud complaints |
| Suspicious timing | 15 | Transactions between 2–5 AM |
| Amount patterns | 10 | Round amounts (₹50K, ₹1L, etc.) |
| Outflow ratio | 10 | Nearly all inflow forwarded |

### Risk Thresholds

| Risk Level | Score Range | Action |
|------------|-----------|--------|
| **HIGH** | ≥ 80 | Immediate Freeze + Step-Up Verification |
| **MEDIUM** | 50 – 79 | Enhanced Monitoring + Alert |
| **LOW** | < 50 | No Action |

---

## Model Files

| Model | Checkpoint | Config |
|-------|-----------|--------|
| Spatio-Temporal Transformer | `models/spatio_temporal/checkpoints/best_model.pth` | `models/spatio_temporal/config.yaml` |
| Mule Detection GNN | `models/mule_detection/checkpoints/best_model.pth` | `models/mule_detection/config.yaml` |

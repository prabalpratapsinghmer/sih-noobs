# SIH26184 — API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints (except `/health`) require a JWT Bearer token:

```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": {
    "spatio_temporal": true,
    "mule_detection": true
  },
  "version": "1.0.0"
}
```

---

### ATM Location Prediction

```
POST /predict/atm
```

Predicts the top-K ATM locations where a fraudster is most likely to withdraw stolen funds.

**Request Body:**
```json
{
  "spatial": {
    "lat": 12.9716,
    "lon": 77.5946,
    "dist_metro": 0.5,
    "dist_police": 2.3
  },
  "temporal": {
    "hour": 14,
    "day": 3,
    "is_weekend": false,
    "time_since_complaint": 2.5,
    "fraud_spike_hour": 22
  },
  "top_k": 3
}
```

**Response:**
```json
{
  "predictions": [
    {"atm_index": 42, "probability": 0.85},
    {"atm_index": 17, "probability": 0.12},
    {"atm_index": 291, "probability": 0.03}
  ],
  "top_k": 3,
  "latency_ms": 45.2
}
```

| Field | Type | Description |
|-------|------|-------------|
| `spatial.lat` | float | Latitude (12.8 – 13.2 for Bangalore) |
| `spatial.lon` | float | Longitude (77.4 – 77.8 for Bangalore) |
| `spatial.dist_metro` | float | Distance to nearest metro station (km) |
| `spatial.dist_police` | float | Distance to nearest police station (km) |
| `temporal.hour` | int | Hour of day (0–23) |
| `temporal.day` | int | Day of week (1=Mon, 7=Sun) |
| `temporal.is_weekend` | bool | Whether it's a weekend |
| `temporal.time_since_complaint` | float | Hours since complaint filed |
| `temporal.fraud_spike_hour` | int | Peak fraud hour historically |
| `top_k` | int | Number of predictions (1–10, default 3) |

---

### Mule Account Detection

```
POST /detect/mules
```

Detects money mule accounts using GNN + hybrid scoring.

**Request Body:**
```json
{
  "features": {
    "velocity": 5.0,
    "inflow": 500000,
    "outflow": 480000,
    "outflow_ratio": 0.96,
    "holding_time": 15.0,
    "connected_complaints": 2,
    "suspicious_timing": 3,
    "in_degree": 4,
    "out_degree": 5
  },
  "account_id": "M0001_1"
}
```

**Response:**
```json
{
  "account_id": "M0001_1",
  "gnn_probability": 0.87,
  "rule_score": 72.0,
  "final_score": 82.5,
  "risk_level": "HIGH",
  "risk_color": "red",
  "action": "Immediate Freeze + Step-Up Verification",
  "latency_ms": 23.1
}
```

| Feature | Description |
|---------|-------------|
| `velocity` | Transactions per hour |
| `inflow` | Total incoming funds (₹) |
| `outflow` | Total outgoing funds (₹) |
| `outflow_ratio` | outflow / (inflow + ε) |
| `holding_time` | Average hold time before transfer (minutes) |
| `connected_complaints` | Number of linked complaints |
| `suspicious_timing` | 2–5 AM transaction count |
| `in_degree` | Incoming edges in transaction graph |
| `out_degree` | Outgoing edges in transaction graph |

**Risk Levels:**

| Level | Score Range | Color | Action |
|-------|-----------|-------|--------|
| HIGH | ≥ 80 | Red | Immediate Freeze + Step-Up Verification |
| MEDIUM | 50 – 79 | Orange | Enhanced Monitoring + Alert |
| LOW | < 50 | Green | No Action |

---

### Step-Up Verification Trigger

```
POST /trigger/verification
```

Triggers additional verification at a predicted ATM.

**Request Body:**
```json
{
  "atm_id": "A0452",
  "verification_type": "facial_recognition",
  "account_ids": ["M0001_1", "M0001_2"],
  "duration_minutes": 120,
  "reason": "High-risk mule network detected",
  "complaint_id": "C1001"
}
```

**Response:**
```json
{
  "status": "SUCCESS",
  "verification_id": "VER-20260905-A0452",
  "atm_id": "A0452",
  "verification_type": "facial_recognition",
  "active_until": "2026-09-05T14:30:00",
  "message": "Step-Up verification activated at ATM A0452 for 120 minutes."
}
```

---

### Account Freeze

```
POST /trigger/freeze
```

Freezes a suspect mule account.

**Request Body:**
```json
{
  "account_id": "M0001_1",
  "reason": "Identified as Tier-2 mule in network N0001",
  "complaint_id": "C1001",
  "duration_hours": 48
}
```

---

### Model Status

```
GET /model/status
```

Returns health and configuration of loaded models.

---

### Model Metrics

```
GET /model/metrics
```

Returns aggregate performance metrics.

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error Type",
  "detail": "Detailed error message",
  "path": "/predict/atm"
}
```

| Status | Description |
|--------|-------------|
| 400 | Bad Request — Invalid input |
| 401 | Unauthorized — Missing/invalid token |
| 403 | Forbidden — Insufficient permissions |
| 404 | Not Found — Resource doesn't exist |
| 429 | Too Many Requests — Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable — Model not loaded |

---

## Rate Limiting

- **Default**: 100 requests/minute per client
- **Burst**: Up to 20 concurrent requests
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Interactive Docs

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

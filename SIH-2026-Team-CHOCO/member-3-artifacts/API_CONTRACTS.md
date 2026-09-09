# API Contracts v1

> Jointly agreed between Member 2 (Backend) and Member 3 (Frontend).
> Base URL: `VITE_API_BASE` (prod: same origin `/api`).
> **Confirm exact field names with Member 2 before freezing — this is the v1 starting point.**

---

## 1. Conventions

- **Auth:** `Authorization: Bearer <access_token>` header on all endpoints except login/refresh.
- **Content-Type:** `application/json` for all request/response bodies.
- **Pagination:** `?page=1&limit=20` (default). Response includes `total`, `page`, `has_more`.
- **Errors:** `{ "detail": string, "code": string }` — HTTP status codes as usual (400, 401, 403, 404, 422, 500).
- **Timestamps:** ISO 8601 format (`2026-09-04T14:30:00Z`).
- **IDs:** UUIDs or prefixed strings (complaints: `C1001`, ATMs: `ATM-0042`).
- **Masked PII:** Victim phone/name are masked in non-admin responses (`+91****1234`).

---

## 2. Authentication

### 2.1 Login (police/admin)

```
POST /api/auth/login
```

**Request:**
```json
{
  "username": "inspector.kumar",
  "password": "secure_password_here"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 14400,
  "user": {
    "id": "usr-001",
    "username": "inspector.kumar",
    "name": "Rajesh Kumar",
    "role": "inspector",
    "station": "Koramangala PS",
    "email": "rajesh@karapolice.gov.in"
  }
}
```

### 2.2 Token Refresh

```
POST /api/auth/refresh
```

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 14400
}
```

**Error (401):** `{"detail": "Token expired", "code": "TOKEN_EXPIRED"}`

### 2.3 Current User

```
GET /api/auth/me
```

**Response (200):**
```json
{
  "id": "usr-001",
  "username": "inspector.kumar",
  "name": "Rajesh Kumar",
  "role": "inspector",
  "station": "Koramangala PS",
  "email": "rajesh@karapolice.gov.in"
}
```

### 2.4 Logout

```
POST /api/auth/logout
```

**Headers:** `Authorization: Bearer <access_token>`
**Response (200):** `{"detail": "Logged out"}`

---

## 3. Complaints

### 3.1 List Complaints

```
GET /api/complaints?page=1&limit=20&status=&fraud_type=&search=
```

**Query params (all optional):**
- `page` (int, default 1)
- `limit` (int, default 20, max 100)
- `status` (string) — filter by status
- `fraud_type` (string) — filter by fraud type
- `search` (string) — search victim name, complaint ID, fraudster info

**Response (200):**
```json
{
  "items": [ /* Complaint[] */ ],
  "total": 247,
  "page": 1,
  "has_more": true
}
```

### 3.2 Get Complaint

```
GET /api/complaints/{id}
```

**Response (200):**
```json
{
  "id": "C1001",
  "status": "in_analysis",
  "fraud_type": "investment",
  "amount": 45000,
  "description": "Received a call claiming to be from SEBI...",
  "created_at": "2026-09-04T10:15:00Z",
  "updated_at": "2026-09-04T10:18:00Z",
  "victim": {
    "id": "vic-001",
    "name_masked": "Amita S***",
    "phone_masked": "+91****5678"
  },
  "fraudster": {
    "upi": "fraudster@paytm",
    "phone": "+919876543210",
    "bank_account": "HDFC-XXXX1234"
  },
  "timeline": [
    {
      "at": "2026-09-04T10:15:00Z",
      "state": "submitted",
      "actor": "victim",
      "note": "Complaint filed via portal"
    },
    {
      "at": "2026-09-04T10:18:00Z",
      "state": "in_analysis",
      "actor": "system",
      "note": "AI pipeline triggered"
    }
  ],
  "predictions": [ /* Prediction[] — top 3 ATMs */ ],
  "mules": [ /* Mule[] — connected mule accounts */ ]
}
```

**Status values:** `submitted` | `in_analysis` | `predictions_ready` | `action_taken` | `resolved` | `closed`

**Fraud type values:** `investment` | `phishing` | `romance` | `tech_support` | `lottery` | `impersonation` | `upi_fraud` | `other`

### 3.3 Get Complaint Evidence

```
GET /api/complaints/{id}/evidence
```

**Response (200):**
```json
{
  "items": [
    {
      "id": "evd-001",
      "complaint_id": "C1001",
      "file_type": "screenshot",
      "file_name": "transaction_proof.png",
      "file_hash": "sha256:a1b2c3d4...",
      "ipfs_cid": "QmXoypiz...",
      "uploaded_at": "2026-09-04T10:16:00Z",
      "verified": true
    }
  ]
}
```

### 3.4 Get Complaint Timeline

```
GET /api/complaints/{id}/timeline
```

**Response (200):**
```json
{
  "events": [
    {
      "at": "2026-09-04T10:15:00Z",
      "state": "submitted",
      "actor": "victim",
      "note": "Complaint filed via portal",
      "tx_hash": "0xabc123..."
    },
    {
      "at": "2026-09-04T10:18:00Z",
      "state": "in_analysis",
      "actor": "system",
      "note": "AI pipeline triggered"
    },
    {
      "at": "2026-09-04T10:22:00Z",
      "state": "predictions_ready",
      "actor": "system",
      "note": "Top-3 ATM predictions generated",
      "tx_hash": "0xdef456..."
    }
  ]
}
```

---

## 4. Predictions & Map

### 4.1 Get Predictions for Complaint

```
GET /api/predictions?complaint_id=C1001
```

**Response (200):**
```json
{
  "items": [
    {
      "atm_id": "ATM-0042",
      "atm_name": "SBI ATM - Koramangala 4th Block",
      "area": "Koramangala",
      "block": "4th Block",
      "lat": 12.9352,
      "lng": 77.6245,
      "probability": 0.82,
      "predicted_window": {
        "from": "2026-09-04T11:00:00Z",
        "to": "2026-09-04T17:00:00Z"
      },
      "method": "spatio-temporal",
      "connected_mules": 2,
      "high_risk_mules": 1
    },
    {
      "atm_id": "ATM-0087",
      "atm_name": "ICICI ATM - Jeevan Bhima Nagar",
      "area": "Jeevan Bhima Nagar",
      "block": "HAL 2nd Stage",
      "lat": 12.9716,
      "lng": 77.6412,
      "probability": 0.67,
      "predicted_window": {
        "from": "2026-09-04T12:00:00Z",
        "to": "2026-09-04T18:00:00Z"
      },
      "method": "spatio-temporal",
      "connected_mules": 1,
      "high_risk_mules": 0
    }
  ]
}
```

### 4.2 Get All ATM Risk Points (for heatmap)

```
GET /api/atms?min_risk=0&area=&since=2026-09-04T00:00:00Z
```

**Query params (all optional):**
- `min_risk` (int, default 0) — minimum risk score
- `area` (string) — filter by area name
- `since` (ISO timestamp) — only ATMs active since this time
- `fraud_type` (string) — filter by connected fraud type

**Response (200):**
```json
{
  "items": [
    {
      "atm_id": "ATM-0042",
      "atm_name": "SBI ATM - Koramangala 4th Block",
      "area": "Koramangala",
      "lat": 12.9352,
      "lng": 77.6245,
      "risk_score": 82,
      "priority": "crit",
      "connected_high_risk_mules": 1,
      "connected_complaints": 3,
      "last_active": "2026-09-04T10:22:00Z"
    }
  ],
  "total": 127
}
```

**Priority mapping:**
- `crit` (critical): `risk_score >= 70`
- `warn` (warning): `risk_score >= 40 && risk_score < 70`
- `info` (info): `risk_score < 40`

---

## 5. Mule Detection & Graph

### 5.1 Get Money-Trail Graph

```
GET /api/mules/{complaint_id}/graph
```

**Response (200):**
```json
{
  "complaint_id": "C1001",
  "nodes": [
    {
      "id": "vic-001",
      "label": "Amita S***",
      "type": "victim",
      "mule_score": null,
      "meta": {
        "amount_sent": 45000,
        "upi_id": "amita@upi"
      }
    },
    {
      "id": "mule-001",
      "label": "Rakesh P***",
      "type": "mule",
      "mule_score": 92,
      "meta": {
        "phone": "+91****1234",
        "account": "SBI-XXXX5678",
        "risk_factors": ["new_account", "high_velocity", "connected_to_3_complaints"]
      }
    },
    {
      "id": "mule-002",
      "label": "Deepa K***",
      "type": "mule",
      "mule_score": 74,
      "meta": {
        "phone": "+91****9012",
        "account": "ICICI-XXXX9012",
        "risk_factors": ["proximity_to_mule_001", "recent_large_deposits"]
      }
    },
    {
      "id": "atm-0042",
      "label": "SBI ATM - Koramangala",
      "type": "atm",
      "mule_score": null,
      "meta": {
        "area": "Koramangala",
        "lat": 12.9352,
        "lng": 77.6245
      }
    },
    {
      "id": "upi-001",
      "label": "fraudster@paytm",
      "type": "upi",
      "mule_score": null,
      "meta": {}
    },
    {
      "id": "phone-001",
      "label": "+919876543210",
      "type": "phone",
      "mule_score": null,
      "meta": {}
    }
  ],
  "edges": [
    {
      "source": "vic-001",
      "target": "mule-001",
      "rel": "SENT_MONEY_TO",
      "amount": 45000,
      "at": "2026-09-04T10:02:00Z"
    },
    {
      "source": "mule-001",
      "target": "mule-002",
      "rel": "TRANSFERRED_TO",
      "amount": 44800,
      "at": "2026-09-04T10:05:00Z"
    },
    {
      "source": "mule-002",
      "target": "atm-0042",
      "rel": "WITHDREW_AT",
      "amount": 44000,
      "at": "2026-09-04T10:12:00Z"
    },
    {
      "source": "upi-001",
      "target": "mule-001",
      "rel": "CONNECTED_TO"
    },
    {
      "source": "phone-001",
      "target": "mule-001",
      "rel": "CONNECTED_TO"
    }
  ]
}
```

**Node types:** `victim` | `mule` | `upi` | `phone` | `bank` | `atm`
**Edge types:** `SENT_MONEY_TO` | `TRANSFERRED_TO` | `WITHDREW_AT` | `CONNECTED_TO`

### 5.2 Get Mule Detail

```
GET /api/mules/{mule_id}
```

**Response (200):**
```json
{
  "id": "mule-001",
  "name_masked": "Rakesh P***",
  "phone_masked": "+91****1234",
  "account": "SBI-XXXX5678",
  "mule_score": 92,
  "risk_factors": [
    {"factor": "new_account", "weight": 20, "detail": "Account opened 12 days ago"},
    {"factor": "high_velocity", "weight": 35, "detail": "7 transactions in 2 hours"},
    {"factor": "connected_to_3_complaints", "weight": 37, "detail": "Linked to C0998, C1001, C1015"}
  ],
  "connected_complaints": ["C0998", "C1001", "C1015"],
  "connected_atms": ["ATM-0042", "ATM-0087"],
  "total_transactions": 14,
  "total_amount": 312000,
  "first_seen": "2026-08-23T00:00:00Z",
  "last_seen": "2026-09-04T10:12:00Z"
}
```

---

## 6. Actions

### 6.1 Create Action

```
POST /api/actions
```

**Request:**
```json
{
  "complaint_id": "C1001",
  "action_type": "step_up_verification",
  "params": {
    "atm_id": "ATM-0042",
    "duration_hours": 6
  }
}
```

**Response (201):**
```json
{
  "id": "act-001",
  "complaint_id": "C1001",
  "action_type": "step_up_verification",
  "status": "initiated",
  "initiated_by": "usr-001",
  "initiated_by_name": "Rajesh Kumar",
  "params": {
    "atm_id": "ATM-0042",
    "duration_hours": 6
  },
  "tx_hash": "0x789abc...",
  "created_at": "2026-09-04T10:25:00Z"
}
```

**`action_type` values:**
| Type | Purpose | Required params |
|------|---------|----------------|
| `step_up_verification` | Trigger facial recognition / OTP at ATM | `atm_id`, `duration_hours` |
| `freeze_request` | Request bank to freeze mule account | `mule_id`, `reason` |
| `fir_draft` | Generate FIR draft from complaint | — |
| `dispatch_patrol` | Dispatch police patrol to ATM | `atm_id` |
| `backup_request` | Request backup from control room | `officer_id`, `location` |

### 6.2 Update Action Status

```
PATCH /api/actions/{action_id}
```

**Request:**
```json
{
  "status": "completed",
  "note": "Patrol dispatched, ETA 8 minutes"
}
```

**Response (200):** Full action object with updated `status` and `tx_hash`.

**Status values:** `initiated` | `dispatched` | `completed` | `failed` | `cancelled`

### 6.3 List Actions for Complaint

```
GET /api/actions?complaint_id=C1001
```

**Response (200):**
```json
{
  "items": [
    {
      "id": "act-001",
      "complaint_id": "C1001",
      "action_type": "step_up_verification",
      "status": "completed",
      "initiated_by": "usr-001",
      "initiated_by_name": "Rajesh Kumar",
      "tx_hash": "0x789abc...",
      "created_at": "2026-09-04T10:25:00Z",
      "completed_at": "2026-09-04T10:25:12Z"
    }
  ],
  "total": 1
}
```

---

## 7. Admin Endpoints

### 7.1 Users

```
GET    /api/admin/users?page=1&limit=20&role=
POST   /api/admin/users
PATCH  /api/admin/users/{id}
DELETE /api/admin/users/{id}
```

**User object:**
```json
{
  "id": "usr-001",
  "username": "inspector.kumar",
  "name": "Rajesh Kumar",
  "role": "inspector",
  "station": "Koramangala PS",
  "phone": "+919876543210",
  "email": "rajesh@karapolice.gov.in",
  "is_active": true,
  "created_at": "2026-08-01T00:00:00Z",
  "last_login": "2026-09-04T10:10:00Z"
}
```

### 7.2 System Health

```
GET /api/admin/health
```

**Response (200):**
```json
{
  "services": [
    {
      "name": "backend-api",
      "status": "healthy",
      "uptime_seconds": 86400,
      "cpu_percent": 34.2,
      "memory_mb": 512,
      "gpu_percent": null,
      "disk_free_gb": 42.1
    },
    {
      "name": "ml-model-server",
      "status": "healthy",
      "uptime_seconds": 86400,
      "cpu_percent": 67.8,
      "memory_mb": 4096,
      "gpu_percent": 72.1,
      "disk_free_gb": 120.5
    },
    {
      "name": "neo4j-database",
      "status": "healthy",
      "uptime_seconds": 86400,
      "cpu_percent": 12.4,
      "memory_mb": 2048,
      "gpu_percent": null,
      "disk_free_gb": 80.3
    },
    {
      "name": "postgres-database",
      "status": "healthy",
      "uptime_seconds": 86400,
      "cpu_percent": 8.7,
      "memory_mb": 256,
      "gpu_percent": null,
      "disk_free_gb": 65.2
    },
    {
      "name": "redis-cache",
      "status": "healthy",
      "uptime_seconds": 86400,
      "cpu_percent": 2.1,
      "memory_mb": 64,
      "gpu_percent": null,
      "disk_free_gb": 10.1
    }
  ],
  "checked_at": "2026-09-04T14:30:00Z"
}
```

### 7.3 Model Metrics

```
GET /api/admin/model-metrics?model=transformer&since=2026-09-01T00:00:00Z
```

**Response (200):**
```json
{
  "model": "spatio-temporal-transformer",
  "metrics": [
    {
      "recorded_at": "2026-09-04T10:00:00Z",
      "accuracy": 0.87,
      "precision": 0.84,
      "recall": 0.91,
      "f1": 0.874,
      "latency_ms": 320,
      "predictions_made": 15
    }
  ]
}
```

### 7.4 Audit Log

```
GET /api/admin/audit?page=1&limit=50&filter=all&action_type=&user=
```

**Response (200):**
```json
{
  "items": [
    {
      "id": "log-001",
      "action_type": "step_up_verification",
      "complaint_id": "C1001",
      "initiated_by": "usr-001",
      "initiated_by_name": "Rajesh Kumar",
      "status": "completed",
      "tx_hash": "0x789abc...",
      "created_at": "2026-09-04T10:25:00Z",
      "ip": "10.0.1.50"
    }
  ],
  "total": 342,
  "page": 1,
  "has_more": true
}
```

---

## 8. Error Responses

All endpoints follow this error shape:

```json
{
  "detail": "Human-readable error message",
  "code": "MACHINE_READABLE_CODE"
}
```

**Common codes:**
| Code | HTTP Status | Meaning |
|------|------------|---------|
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `TOKEN_EXPIRED` | 401 | Access token expired, use refresh |
| `FORBIDDEN` | 403 | Role does not have access |
| `NOT_FOUND` | 404 | Resource does not exist |
| `VALIDATION_ERROR` | 422 | Request body fails validation |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## 9. Versioning

- Current version: **v1** (this document).
- Breaking changes require updating this document and notifying Member 3.
- Additive changes (new fields, new endpoints) are safe to ship without version bump.
- Deprecated endpoints are marked with `deprecated: true` in their response headers.

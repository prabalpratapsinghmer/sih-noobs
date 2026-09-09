# API Contracts (v1)

> **SIH 2026 | Team CHOCO | Project ID: SIH26184**
> Single source of truth for REST endpoints and WebSocket events.

## 1. Base Configuration
- **Base URL (Dev):** `http://localhost:8000/api/v1`
- **Base URL (Prod):** `https://api.choco-sih.org/v1`
- **Authentication:** JWT Bearer Token (`Authorization: Bearer <token>`)
- **Content-Type:** `application/json`

---

## 2. Authentication Endpoints

### `POST /auth/login`
Authenticates a user (admin, inspector, constable) and returns a JWT.

**Request:**
```json
{
  "email": "inspector.singh@police.gov.in",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "def456...",
  "user": {
    "id": "U1001",
    "role": "inspector",
    "station": "Indiranagar PS"
  }
}
```

---

## 3. Complaint & Intelligence Endpoints

### `GET /complaints`
Retrieves paginated complaints.

**Query Params:** `status` (optional), `page` (default: 1), `limit` (default: 20)

**Response (200 OK):**
```json
{
  "items": [
    {
      "complaint_ref": "C1001",
      "status": "ANALYZING",
      "fraud_type": "investment",
      "amount": 500000,
      "created_at": "2026-09-04T10:00:00Z"
    }
  ],
  "total": 45,
  "page": 1,
  "pages": 3
}
```

### `GET /heatmap`
Retrieves predicted ATM targets for the Leaflet heatmap.

**Query Params:** `time_range` (e.g., "2h"), `risk_min` (e.g., 50)

**Response (200 OK):**
```json
{
  "atms": [
    {
      "atm_id": "A452",
      "latitude": 12.9716,
      "longitude": 77.5946,
      "risk_score": 92,
      "active_complaints": 3,
      "predicted_window": "2.5 hours"
    }
  ]
}
```

### `GET /mules/network/{complaint_ref}`
Retrieves graph data for vis.js / D3 rendering.

**Response (200 OK):**
```json
{
  "nodes": [
    { "id": "V001", "label": "Victim", "type": "victim" },
    { "id": "M1001", "label": "Mule A", "type": "mule", "mule_score": 92 },
    { "id": "A452", "label": "ATM #452", "type": "atm", "risk_score": 92 }
  ],
  "edges": [
    { "from": "V001", "to": "M1001", "label": "₹5,00,000", "type": "SENT_MONEY_TO" },
    { "from": "M1001", "to": "A452", "label": "₹4,50,000", "type": "WITHDREW_AT" }
  ]
}
```

---

## 4. Action Endpoints

### `POST /actions/trigger-verification`
Triggers facial recognition / OTP step-up on a predicted ATM.

**Request:**
```json
{
  "complaint_ref": "C1001",
  "atm_id": "A452"
}
```

**Response (202 Accepted):**
```json
{
  "action_id": "ACT-9912",
  "status": "TRIGGERED",
  "message": "Facial recognition enabled at ATM #452"
}
```

### `POST /actions/dispatch-patrol`
Dispatches an officer via the Field Dashboard.

**Request:**
```json
{
  "complaint_ref": "C1001",
  "atm_id": "A452",
  "officer_id": "U2005"
}
```

---

## 5. LLM Agent Endpoints

### `POST /llm/query`
Natural language query translated to Cypher by the backend.

**Request:**
```json
{
  "query": "Show all high-risk ATMs in Indiranagar linked to C1001"
}
```

**Response (200 OK):**
```json
{
  "answer": "I found 3 ATMs matching those criteria...",
  "cypher_query": "MATCH (c:Complaint)-[:CONNECTED_TO]->(a:ATM)...",
  "results": [...],
  "follow_up_suggestions": ["Show mule accounts for these ATMs"]
}
```

---

## 6. WebSocket Events (`/ws/alerts`)

Clients connect with JWT. The server pushes real-time intelligence.

### Incoming Events (Server → Client)

| Event Name | Payload | Trigger Condition |
|------------|---------|-------------------|
| `NEW_ALERT` | `{ complaint_ref, atm_id, risk_score, distance_km }` | New ML prediction > 70% risk |
| `STATUS_UPDATE` | `{ complaint_ref, old_status, new_status }` | Action taken (e.g., dispatched) |
| `PREDICTION_READY` | `{ complaint_ref, atm_count }` | ML model finishes scoring a new case |

### Outgoing Events (Client → Server)
| Event Name | Payload | Trigger Condition |
|------------|---------|-------------------|
| `LOCATION_UPDATE` | `{ officer_id, lat, lng }` | Field app pushes GPS every 30s |
| `ACK_ALERT` | `{ alert_id }` | Officer taps an alert on Field app |

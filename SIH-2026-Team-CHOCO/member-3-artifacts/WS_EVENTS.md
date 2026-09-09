# WebSocket Events

> WebSocket connection URL: `VITE_WS_URL` (prod: same origin `/ws`).
> All frontend apps consume this stream. See `API_CONTRACTS.md` for the REST API.
> **Confirm event names with Member 2 before freeze.**

---

## 1. Connection & Authentication

### Connecting
```
ws://localhost:8000/ws?token=<access_token>
```

The token is passed as a query parameter on the initial WebSocket handshake. The server validates it before accepting the connection.

### Reconnection
The frontend WebSocket wrapper handles reconnection automatically:
1. On close, wait 1 second, then attempt reconnect.
2. Exponential backoff: 1s → 2s → 4s → 8s → 16s → 30s (max).
3. On reconnect, re-authenticate with the stored refresh token.
4. Emit `ws.reconnected` to the UI so it can refresh state.

### Connection Acknowledgment
```json
// Server → Client (sent immediately after connection)
{
  "event": "ws.connected",
  "data": {
    "server_time": "2026-09-04T14:30:00Z",
    "user_id": "usr-001",
    "role": "inspector",
    "subscriptions": ["complaints.*", "predictions.*", "alerts.*", "actions.*"]
  }
}
```

---

## 2. Event Taxonomy

All events follow this envelope:
```json
{
  "event": "<namespace>.<action>",
  "data": { /* payload */ },
  "timestamp": "2026-09-04T14:30:00Z"
}
```

---

## 3. Complaint Events

### 3.1 `complaint.created`

**Trigger:** A new complaint is filed (via portal or API).
**Fan-out:** Command Center (new case in sidebar), Admin Panel (complaint count +1).

```json
{
  "event": "complaint.created",
  "data": {
    "complaint_id": "C1001",
    "fraud_type": "investment",
    "amount": 45000,
    "created_at": "2026-09-04T10:15:00Z"
  },
  "timestamp": "2026-09-04T10:15:00Z"
}
```

**Frontend actions:**
- Command Center: Show toast notification, add to case list, increment sidebar badge.
- Admin Panel: Increment active complaints count.

### 3.2 `status.updated`

**Trigger:** Complaint status changes (any transition).
**Fan-out:** All apps (any with the complaint open should update).

```json
{
  "event": "status.updated",
  "data": {
    "complaint_id": "C1001",
    "old_status": "in_analysis",
    "new_status": "predictions_ready",
    "updated_by": "system",
    "updated_at": "2026-09-04T10:22:00Z"
  },
  "timestamp": "2026-09-04T10:22:00Z"
}
```

---

## 4. Prediction Events

### 4.1 `prediction.new`

**Trigger:** ML model generates new ATM predictions for a complaint.
**Fan-out:** Command Center (heatmap + graph update), Field Dashboard (alert card if high-risk).

```json
{
  "event": "prediction.new",
  "data": {
    "complaint_id": "C1001",
    "predictions": [
      {
        "atm_id": "ATM-0042",
        "atm_name": "SBI ATM - Koramangala 4th Block",
        "area": "Koramangala",
        "lat": 12.9352,
        "lng": 77.6245,
        "probability": 0.82,
        "risk_score": 82,
        "priority": "crit",
        "predicted_window": {
          "from": "2026-09-04T11:00:00Z",
          "to": "2026-09-04T17:00:00Z"
        }
      }
    ],
    "mule_scores_updated": true,
    "total_mules_flagged": 1
  },
  "timestamp": "2026-09-04T10:22:00Z"
}
```

**Frontend actions:**
- Command Center: Add/update ATM markers on heatmap, show toast, update graph if open.
- Field Dashboard: Create alert card if `priority === "crit"` or `"warn"`.

### 4.2 `prediction.expired`

**Trigger:** A prediction's time window has passed without action.
**Fan-out:** Command Center (grey out the marker), Field Dashboard (dismiss the alert).

```json
{
  "event": "prediction.expired",
  "data": {
    "complaint_id": "C1001",
    "atm_id": "ATM-0042",
    "expired_at": "2026-09-04T17:00:00Z"
  },
  "timestamp": "2026-09-04T17:00:00Z"
}
```

---

## 5. ATM Risk Events

### 5.1 `atm.risk_changed`

**Trigger:** An ATM's aggregate risk score changes (new complaint links, score decay).
**Fan-out:** Command Center (heatmap update).

```json
{
  "event": "atm.risk_changed",
  "data": {
    "atm_id": "ATM-0042",
    "area": "Koramangala",
    "lat": 12.9352,
    "lng": 77.6245,
    "old_risk_score": 72,
    "new_risk_score": 82,
    "old_priority": "warn",
    "new_priority": "crit",
    "connected_complaints": 3,
    "connected_high_risk_mules": 1
  },
  "timestamp": "2026-09-04T10:22:00Z"
}
```

**Frontend actions:**
- Command Center: Update marker color/size, show toast if upgraded to `crit`.

---

## 6. Alert Events

### 6.1 `alert.push`

**Trigger:** A high-priority alert needs immediate officer attention.
**Fan-out:** Field Dashboard (new alert card), Command Center (toast + feed).

```json
{
  "event": "alert.push",
  "data": {
    "alert_id": "alr-001",
    "complaint_id": "C1001",
    "atm_id": "ATM-0042",
    "atm_name": "SBI ATM - Koramangala 4th Block",
    "block": "4th Block",
    "area": "Koramangala",
    "lat": 12.9352,
    "lng": 77.6245,
    "risk_score": 82,
    "priority": "crit",
    "predicted_window": {
      "from": "2026-09-04T11:00:00Z",
      "to": "2026-09-04T17:00:00Z"
    },
    "connected_mules": 1,
    "message": "High-risk ATM predicted for withdrawal within 6 hours",
    "created_at": "2026-09-04T10:25:00Z"
  },
  "timestamp": "2026-09-04T10:25:00Z"
}
```

**Frontend actions:**
- Field Dashboard: Show alert card (priority stripe, distance/ETA, quick action buttons).
- Command Center: Show toast, add to alert feed with unread badge.

### 6.2 `alert.acknowledged`

**Trigger:** An officer acknowledges (taps) an alert.
**Fan-out:** All apps (alert status update).

```json
{
  "event": "alert.acknowledged",
  "data": {
    "alert_id": "alr-001",
    "acknowledged_by": "usr-003",
    "acknowledged_by_name": "Constable Sharma",
    "acknowledged_at": "2026-09-04T10:30:00Z"
  },
  "timestamp": "2026-09-04T10:30:00Z"
}
```

---

## 7. Action Events

### 7.1 `action.triggered`

**Trigger:** An action is created (freeze, verification, FIR, dispatch).
**Fan-out:** Command Center (feed), Admin Panel (audit log), Field Dashboard (if dispatch).

```json
{
  "event": "action.triggered",
  "data": {
    "action_id": "act-001",
    "complaint_id": "C1001",
    "action_type": "step_up_verification",
    "status": "initiated",
    "initiated_by": "usr-001",
    "initiated_by_name": "Rajesh Kumar",
    "tx_hash": "0x789abc...",
    "params": {
      "atm_id": "ATM-0042",
      "duration_hours": 6
    },
    "created_at": "2026-09-04T10:25:00Z"
  },
  "timestamp": "2026-09-04T10:25:00Z"
}
```

**Frontend actions:**
- Command Center: Update action status on the case, show confirmation toast.
- Admin Panel: Append to audit log.
- Field Dashboard: Update action buttons if dispatch-related.

### 7.2 `action.completed`

**Trigger:** An action is completed (verification done, freeze applied, FIR generated).
**Fan-out:** All apps with the complaint open.

```json
{
  "event": "action.completed",
  "data": {
    "action_id": "act-001",
    "complaint_id": "C1001",
    "action_type": "step_up_verification",
    "status": "completed",
    "completed_at": "2026-09-04T10:25:12Z",
    "tx_hash": "0x789def..."
  },
  "timestamp": "2026-09-04T10:25:12Z"
}
```

### 7.3 `action.failed`

**Trigger:** An action fails (bank rejects freeze, verification device offline).
**Fan-out:** Command Center (toast with error), Admin Panel (audit).

```json
{
  "event": "action.failed",
  "data": {
    "action_id": "act-002",
    "complaint_id": "C1001",
    "action_type": "freeze_request",
    "status": "failed",
    "error": "Bank Nodal Officer did not respond within 30 minutes",
    "failed_at": "2026-09-04T10:55:00Z"
  },
  "timestamp": "2026-09-04T10:55:00Z"
}
```

---

## 8. Field Dashboard Events

### 8.1 `dispatch.updated`

**Trigger:** A constable updates their dispatch status.
**Fan-out:** Command Center (track officer movement), control room.

```json
{
  "event": "dispatch.updated",
  "data": {
    "complaint_id": "C1001",
    "atm_id": "ATM-0042",
    "officer_id": "usr-003",
    "officer_name": "Constable Sharma",
    "status": "dispatched",
    "location": {
      "lat": 12.9300,
      "lng": 77.6200
    },
    "eta_minutes": 8,
    "updated_at": "2026-09-04T10:32:00Z"
  },
  "timestamp": "2026-09-04T10:32:00Z"
}
```

### 8.2 `backup.requested`

**Trigger:** A constable requests backup from the control room.
**Fan-out:** Command Center (control room toast), other constables in the area.

```json
{
  "event": "backup.requested",
  "data": {
    "complaint_id": "C1001",
    "atm_id": "ATM-0042",
    "officer_id": "usr-003",
    "officer_name": "Constable Sharma",
    "location": {
      "lat": 12.9352,
      "lng": 77.6245
    },
    "reason": "Suspect spotted, backup required",
    "requested_at": "2026-09-04T10:40:00Z"
  },
  "timestamp": "2026-09-04T10:40:00Z"
}
```

---

## 9. Graph Events

### 9.1 `graph.updated`

**Trigger:** New nodes/edges added to a complaint's money-trail graph.
**Fan-out:** Command Center (graph view, if open for this complaint).

```json
{
  "event": "graph.updated",
  "data": {
    "complaint_id": "C1001",
    "added_nodes": [
      {
        "id": "mule-003",
        "label": "Vikram R***",
        "type": "mule",
        "mule_score": 65
      }
    ],
    "added_edges": [
      {
        "source": "mule-002",
        "target": "mule-003",
        "rel": "TRANSFERRED_TO",
        "amount": 12000
      }
    ]
  },
  "timestamp": "2026-09-04T10:35:00Z"
}
```

**Frontend actions:**
- Command Center: Append nodes/edges to the active graph, re-run force simulation.

---

## 10. Admin Events

### 10.1 `system.health_changed`

**Trigger:** A service's health status changes (healthy → degraded → down).
**Fan-out:** Admin Panel (health dashboard update + alert).

```json
{
  "event": "system.health_changed",
  "data": {
    "service": "ml-model-server",
    "old_status": "healthy",
    "new_status": "degraded",
    "reason": "GPU utilization > 95%",
    "cpu_percent": 89.2,
    "memory_mb": 6144,
    "gpu_percent": 97.1,
    "changed_at": "2026-09-04T14:30:00Z"
  },
  "timestamp": "2026-09-04T14:30:00Z"
}
```

---

## 11. Frontend Event Map

### Command Center listens for:
- `complaint.created`
- `status.updated`
- `prediction.new`
- `prediction.expired`
- `atm.risk_changed`
- `alert.push`
- `action.triggered`
- `action.completed`
- `action.failed`
- `graph.updated`
- `system.health_changed`

### Field Dashboard listens for:
- `prediction.new` (filter to crit/warn only)
- `prediction.expired`
- `alert.push`
- `alert.acknowledged`
- `status.updated`
- `dispatch.updated`
- `backup.requested`

### Admin Panel listens for:
- `complaint.created`
- `status.updated`
- `action.triggered`
- `action.completed`
- `action.failed`
- `system.health_changed`

---

## 12. WS Client Wrapper

The WebSocket wrapper in `@sih/ui` abstracts reconnection, event routing, and authentication:

```typescript
// packages/ui-kit/src/lib/ws-client.ts
interface WSEvent {
  event: string;
  data: Record<string, unknown>;
  timestamp: string;
}

type EventHandler = (data: WSEvent['data']) => void;

class WSClient {
  private ws: WebSocket | null = null;
  private handlers: Map<string, Set<EventHandler>> = new Map();
  private reconnectAttempt = 0;
  private maxReconnect = 30;

  connect(url: string, token: string) { /* ... */ }
  on(event: string, handler: EventHandler) { /* ... */ }
  off(event: string, handler: EventHandler) { /* ... */ }
  send(event: string, data: Record<string, unknown>) { /* ... */ }
  disconnect() { /* ... */ }
}

export const wsClient = new WSClient();
```

**Usage in a React component:**
```typescript
useEffect(() => {
  wsClient.on('prediction.new', (data) => {
    dispatch(addPrediction(data));
  });
  return () => wsClient.off('prediction.new', handler);
}, [dispatch]);
```

---

## 13. Transport Decision

- If Member 2 uses **FastAPI built-in WebSocket** → use the native `WebSocket` API wrapper above.
- If Member 2 uses **python-socketio** → use `socket.io-client` instead. Same event map, different transport.
- **Decision must be made on Day 1.** The wrapper isolates the screens from the transport choice.

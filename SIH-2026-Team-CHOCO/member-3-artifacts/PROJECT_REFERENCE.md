# PROJECT REFERENCE — Member 3 (Frontend & DevOps Lead)

> **SIH 2026 | Team CHOCO | Project ID: SIH26184**
> Single source of truth for Member 3's development work.
> Last updated: 2026-09-04

---

## Table of Contents

1. [Project Context](#1-project-context)
2. [Team & Integration Points](#2-team--integration-points)
3. [System Architecture](#3-system-architecture)
4. [Your Tech Stack](#4-your-tech-stack)
5. [Your 3 UIs in Detail](#5-your-3-uis-in-detail)
6. [LLM Agent & Chatbot](#6-llm-agent--chatbot)
7. [APIs You Consume](#7-apis-you-consume)
8. [Data Shapes You Render](#8-data-shapes-you-render)
9. [Your Folder Structure](#9-your-folder-structure)
10. [DevOps Infrastructure](#10-devops-infrastructure)
11. [Environment Variables](#11-environment-variables)
12. [Git Workflow](#12-git-workflow)
13. [Your 10-Day Plan](#13-your-10-day-plan)
14. [Error Handling & Fallbacks](#14-error-handling--fallbacks)
15. [Design Tokens](#15-design-tokens)
16. [Demo Script](#16-demo-script)
17. [Your Presentation Talking Points](#17-your-presentation-talking-points)
18. [KPIs for Your Work](#18-kpis-for-your-work)

---

## 1. Project Context

**What the system does (in one paragraph):**

When a cybercrime victim files a complaint on our portal, the backend triggers two AI models — a Spatio-Temporal Transformer that predicts which ATM the criminal will use, and a Graph Neural Network that identifies mule accounts in the money trail. The system then auto-triggers facial recognition / OTP on the predicted ATM and pushes alerts to police officers. Your job is building the police-facing UIs that display all this intelligence, and the DevOps infrastructure that runs everything.

**Your role:** You build what police officers see and what keeps the system running.

**What you don't build:** The victim portal (Member 4), the backend APIs (Member 2), the ML models (Member 1). You consume their outputs.

---

## 2. Team & Integration Points

| Member | Builds | What you need from them |
|---|---|---|
| **Member 1** (ML, has GPU) | Spatio-Temporal Transformer, GNN, synthetic data, model serving API | ATM prediction endpoints, mule score endpoints, model accuracy metrics |
| **Member 2** (Backend, has GPU) | FastAPI APIs, PostgreSQL, Neo4j, Redis, auth, WebSocket, blockchain, IPFS, LLM service | Every REST/WebSocket endpoint you call, JWT auth flow, API response shapes |
| **Member 4** (No GPU) | Victim Complaint Portal (PWA), UI/UX designs, integration testing, QA, presentation | Shared design system agreement, Figma wireframes, consistent Tailwind config |

### What you coordinate on

**With Member 2 (daily):**
- API contracts — request/response shapes for every endpoint
- WebSocket event names and payload structure
- Auth token format and refresh flow
- Error response format (so your error handling is consistent)

**With Member 4 (days 1-3):**
- Shared `packages/shared-ui` component library (buttons, cards, modals)
- Tailwind config (same breakpoints, color tokens, font)
- Shared TypeScript types (`complaint.ts`, `user.ts`, `prediction.ts`)
- Shared hooks (`useAuth`, `useWebSocket`, `useApi`)

**With Member 1 (days 5-6):**
- Model accuracy metrics format (for Admin Panel display)
- Prediction response shape (for heatmap rendering)
- Mule score format (for graph visualization)

---

## 3. System Architecture

You need to know where your work fits in the stack:

```
┌─────────────────────────────────────────────────────────────────────┐
│  YOUR WORK: LAYER 1 (UIs) + LAYER 5 (DevOps)                       │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Police     │  │   Police     │  │   Admin      │             │
│  │   Command    │  │   Field      │  │   Management │             │
│  │   Center     │  │   Dashboard  │  │   Panel      │             │
│  │  Port 3001   │  │  Port 3002   │  │  Port 3003   │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                  │                  │                     │
├─────────┴──────────────────┴──────────────────┴─────────────────────┤
│  MEMBER 2's WORK: Backend                                           │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Nginx (Port 80) → FastAPI (Port 8000) → WebSocket          │   │
│  │  REST: /complaints, /predictions, /heatmap, /mules,         │   │
│  │        /actions, /llm/query, /audit, /users                 │   │
│  │  WS:   /ws/alerts, /ws/status                               │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  MEMBER 1's WORK: ML Models                                        │
│                                                                     │
│  ML Server (Port 8081) — you don't call this directly.             │
│  Member 2's backend calls it and exposes results via REST to you.  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  DATA LAYER (Member 2 manages, you just consume via APIs)          │
│                                                                     │
│  PostgreSQL (5432) | Neo4j (7687/7474) | Redis (6379) | IPFS      │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  YOUR WORK: DevOps (Docker, K8s, Jenkins, Prometheus, ELK)         │
│  You containerize and orchestrate everything above.                │
└─────────────────────────────────────────────────────────────────────┘
```

**Key insight:** You never talk to databases directly. You call Member 2's REST/WebSocket APIs. The only exception is the LLM Agent chat UI, which calls `/api/v1/llm/query` — Member 2 handles the LangChain → Neo4j pipeline behind that endpoint.

---

## 4. Your Tech Stack

### Frontend

| Tool | Purpose |
|---|---|
| **React 18** | UI framework |
| **TypeScript** (strict mode) | Type safety |
| **Vite** | Build tool and dev server |
| **Tailwind CSS** | Utility-first styling |
| **shadcn/ui** | Pre-built accessible components |
| **Leaflet.js + OpenStreetMap** | Heatmap and ATM markers (free, no API key) |
| **vis.js (vis-network)** | Graph visualization for Neo4j mule network data |
| **Redux Toolkit + RTK Query** | State management and API data caching |
| **Socket.io-client** | WebSocket for real-time alerts and status updates |
| **Axios** | HTTP client with auth interceptors |
| **React Hook Form + Zod** | Forms (admin user management) |
| **Framer Motion** | Animations and transitions |
| **AG Grid** | Data tables (admin panel, complaint tables) |
| **Recharts** | Charts (system health, model metrics, complaint stats) |
| **React Router v6** | Client-side routing |

### DevOps

| Tool | Purpose |
|---|---|
| **Docker** | Containerize all services (yours + others') |
| **Docker Compose** | Local dev: spin up full stack with one command |
| **Kubernetes (Minikube)** | Demo orchestration |
| **Jenkins** | CI/CD pipeline |
| **GitHub Actions** | Backup CI (lint + type-check on PR) |
| **Prometheus** | Metrics collection |
| **Grafana** | Metrics dashboards |
| **ELK Stack** | Centralized logging |
| **Nginx** | Reverse proxy + static file serving |
| **SonarQube** | Code quality analysis |

### Testing

| Tool | Purpose |
|---|---|
| **Jest + React Testing Library** | Unit tests for components |
| **Lighthouse** | Performance auditing (target: >90) |

---

## 5. Your 3 UIs in Detail

### UI 1: Police Command Center (Port 3001)

**User:** Cybercrime Inspector sitting at a desk, managing 12+ cases simultaneously.

**Design:** Dark theme, information-dense, action-oriented, real-time.

**Color:** `#0a0e17` background, `#00d4ff` neon blue accents, `#06b6d4` cyan.

**Pages:**

| Page | Route | Components |
|---|---|---|
| Dashboard | `/` | `StatsCards`, `RiskHeatmap`, `AlertFeed`, `ComplaintTable` |
| Investigation | `/investigation/:complaintRef` | `NetworkGraph`, `NodeDetail`, `ActionPanel`, `ChatInterface` |
| Alerts | `/alerts` | `AlertFeed` (full page), filters, search |
| Settings | `/settings` | Notification preferences, saved LLM queries |

**Components Breakdown:**

```
command-center/src/components/
│
├── layout/
│   ├── Sidebar.tsx          — Nav: Dashboard, Investigation, Alerts, Settings
│   ├── Header.tsx           — Officer name, notifications bell, logout
│   └── MainLayout.tsx       — Sidebar + Header + content area wrapper
│
├── map/
│   ├── RiskHeatmap.tsx      — Leaflet map with heatmap layer
│   │                          Props: atms: ATMPrediction[]
│   │                          Features: risk color coding (red/orange/green),
│   │                          cluster rendering for 500+ markers,
│   │                          filters (time range, risk level, area)
│   │                          WebSocket: listens for PREDICTION_READY to add new markers
│   │
│   ├── ATMMarker.tsx        — Individual ATM marker on map
│   │                          Props: atm: ATMPrediction, onClick
│   │                          Color: based on risk_score (>70 red, >40 orange, else green)
│   │
│   ├── ATMPopup.tsx         — Popup when marker clicked
│   │                          Shows: risk score, predicted window, linked mules count,
│   │                          complaint ref, area type, nearby metro
│   │                          Actions: "View Investigation", "Trigger Verification"
│   │
│   └── MapControls.tsx      — Zoom, pan, reset, filter dropdowns
│
├── graph/
│   ├── NetworkGraph.tsx     — vis.js network graph
│   │                          Props: nodes: GraphNode[], edges: GraphEdge[]
│   │                          Features: zoom, pan, select node, highlight path
│   │                          Node colors: victim=blue, mule=red (high score) / orange, atm=purple
│   │                          Edge labels: amounts (₹ formatted)
│   │                          On node click: show NodeDetail panel
│   │
│   ├── GraphControls.tsx    — Zoom, reset, layout toggle (hierarchical/force-directed)
│   │
│   └── NodeDetail.tsx       — Side panel when node selected
│                              Shows: node type, score, connections, linked complaints
│                              Mule node: shows mule_score, bank, phone, risk_level
│                              ATM node: shows risk_score, location, predicted_window
│
├── llm/
│   ├── ChatInterface.tsx    — Full chat UI
│   │                          Features: message list, input box, send button
│   │                          Sends POST /api/v1/llm/query
│   │                          Renders: text, graph results, action buttons
│   │                          Stores chat history in local state
│   │
│   ├── MessageBubble.tsx    — Single message (user or AI)
│   │                          AI messages can contain: text, graph viz, tables, action buttons
│   │
│   ├── QuickPrompts.tsx     — Clickable suggestion chips above input
│   │                          Examples: "Show all high-risk ATMs", "Show mules for C1001",
│   │                          "What complaints are linked to phone 9876543210?"
│   │
│   └── QueryResult.tsx      — Structured result display
│                              Can render: text response, mini graph, data table, action buttons
│
├── actions/
│   ├── ActionPanel.tsx      — Contains all action buttons for a complaint
│   │
│   ├── TriggerVerification.tsx — POST /api/v1/actions/trigger-verification
│   │                              Confirm dialog → API call → success/error toast
│   │
│   ├── FreezeAccount.tsx    — POST /api/v1/actions/freeze-account
│   │                          Select mule account → confirm → API call
│   │
│   ├── GenerateFIR.tsx      — POST /api/v1/actions/generate-fir
│   │                          Shows generated FIR text, copy/download buttons
│   │
│   └── DispatchPatrol.tsx   — POST /api/v1/actions/dispatch-patrol
│                              Select officer → confirm → API call
│
└── dashboard/
    ├── StatsCards.tsx        — 4 cards: Active Complaints, High-Risk ATMs,
    │                          Resolved Today, Avg Response Time
    │                          Data from: GET /api/v1/complaints?status=...
    │
    ├── AlertFeed.tsx         — Real-time alert list (WebSocket: NEW_ALERT events)
    │                          Each alert: complaint ref, ATM, risk score, time ago
    │                          Click → navigate to /investigation/:ref
    │
    └── ComplaintTable.tsx    — AG Grid table of all complaints
                               Columns: Ref, Type, Amount, Status, Risk, Time
                               Features: sort, filter, search, pagination
                               Data from: GET /api/v1/complaints?page=&limit=
```

**Command Center Wireframe:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🚨 CYBER COMMAND CENTER  |  Inspector Singh  |  🔔 3  |  [Logout]        │
├────────┬────────────────────────────────────────────────────────────────────┤
│        │                                                                    │
│  NAV   │  ┌──────────┬──────────────────────────────────────────────────┐  │
│        │  │  STATS    │                                                  │  │
│  📊    │  │  Active:12│     LIVE HEATMAP (Leaflet + OpenStreetMap)       │  │
│  Dash  │  │  High: 5  │                                                  │  │
│        │  │  Resolved │     🔴 ATM #452 (92%)                            │  │
│  🔍    │  │  : 8      │     🟠 ATM #789 (67%)                            │  │
│  Invest│  │  Avg: 4m  │     🟢 ATM #123 (34%)                            │  │
│        │  └──────────┴──────────────────────────────────────────────────┘  │
│  🚨    │                                                                    │
│  Alerts│  ┌─────────────────────────────┬──────────────────────────────┐  │
│        │  │  GRAPH VISUALIZATION        │  LLM AGENT CHAT              │  │
│  ⚙️    │  │  (vis.js — Neo4j data)      │                              │  │
│  Set   │  │                             │  You: Show mules for C1001   │  │
│        │  │  [Victim]→[Mule A]→[ATM]    │  AI: Found 3 mule accounts: │  │
│        │  │                             │   1. M1001 (Score: 92)       │  │
│        │  │                             │   [Trigger] [Freeze]         │  │
│        │  │                             │  [Type query...]      [Send] │  │
│        │  └─────────────────────────────┴──────────────────────────────┘  │
│        │                                                                    │
└────────┴────────────────────────────────────────────────────────────────────┘
```

---

### UI 2: Police Field Dashboard (Port 3002)

**User:** Constable on patrol, looking at their phone. Needs big buttons, minimal text, instant comprehension.

**Design:** Mobile-first, light theme, high-contrast alert colors. Big touch targets.

**Color:** White background, alert cards color-coded (red/orange/green borders).

**Pages:**

| Page | Route | Components |
|---|---|---|
| Alerts | `/` | `AlertList` — list of active alert cards |
| Alert Detail | `/alert/:id` | `AlertDetail`, `NavigationMap`, `QuickActions` |
| Profile | `/profile` | Officer info, notification settings |

**Components Breakdown:**

```
field-dashboard/src/components/
│
├── layout/
│   ├── MobileHeader.tsx     — App title, alert count badge, profile icon
│   └── BottomNav.tsx        — 3 tabs: Alerts, Map, Profile (mobile nav pattern)
│
├── alerts/
│   ├── AlertCard.tsx        — Single alert card
│   │                          Shows: ATM ID, risk score (large, colored), location name,
│   │                          distance from officer (uses Geolocation API), ETA
│   │                          Border color: red (>70), orange (>40), green (<40)
│   │                          Tap → navigate to /alert/:id
│   │
│   ├── AlertList.tsx        — Scrollable list of AlertCards
│   │                          Sorted: High → Medium → Low
│   │                          WebSocket: NEW_ALERT adds card with animation
│   │                          Pull-to-refresh gesture
│   │
│   └── AlertDetail.tsx      — Full detail page for one alert
│                              Shows: ATM details, risk score, predicted window,
│                              complaint ref, linked mule count, map
│
├── map/
│   └── NavigationMap.tsx    — Leaflet map centered on ATM location
│                              Shows officer's location (Geolocation API)
│                              "Open in Google Maps" button for directions
│
└── actions/
    ├── QuickActions.tsx      — Big action buttons (full-width, tall)
    │                          "🗺️ Navigate", "🚔 Dispatch", "✅ Verified", "🆘 Backup"
    │
    ├── DispatchButton.tsx   — POST /api/v1/actions/dispatch-patrol
    │                          Single tap → confirm → done (optimized for speed)
    │
    └── BackupRequest.tsx    — POST with backup flag
                               Shows confirmation + sends alert to other officers
```

**Field Dashboard Wireframe (Phone):**

```
┌──────────────────────────┐
│  🚨 Field Alerts    🔴 3 │
├──────────────────────────┤
│                          │
│  ┌────────────────────┐  │
│  │ 🔴 HIGH RISK       │  │
│  │ ATM #452            │  │
│  │ Risk: 92%           │  │
│  │ Indiranagar Metro   │  │
│  │ 📍 2.4 km • ~8 min │  │
│  │ ⏱️ Window: 2.5 hrs  │  │
│  └────────────────────┘  │
│                          │
│  ┌────────────────────┐  │
│  │ 🟠 MEDIUM RISK     │  │
│  │ ATM #789            │  │
│  │ Risk: 67%           │  │
│  │ Koramangala         │  │
│  │ 📍 5.1 km • ~15 min│  │
│  └────────────────────┘  │
│                          │
│  ┌────────────────────┐  │
│  │ 🟢 LOW RISK        │  │
│  │ ATM #123            │  │
│  │ Risk: 34%           │  │
│  └────────────────────┘  │
│                          │
├──────────────────────────┤
│  🚨 Alerts  🗺️ Map  👤  │
└──────────────────────────┘
```

---

### UI 3: Admin Management Panel (Port 3003)

**User:** System admin / IT team. Data-heavy, functional.

**Design:** Dark theme (matches Command Center). Desktop-optimized.

**Color:** Same dark theme as Command Center.

**Pages:**

| Page | Route | Components |
|---|---|---|
| Users | `/users` | `UserTable` (AG Grid), `UserForm`, `RoleSelector` |
| System Health | `/health` | `SystemMetrics` (Recharts), `ServiceStatus` |
| Audit Logs | `/audit` | `AuditLogTable` (AG Grid), `ChainVerifier` |
| Complaints | `/complaints` | `ComplaintOverview`, `ResolutionStats` (Recharts) |
| Settings | `/settings` | Alert thresholds, notification config |

**Components Breakdown:**

```
admin-panel/src/components/
│
├── layout/
│   ├── Sidebar.tsx          — Nav: Users, Health, Audit, Complaints, Settings
│   └── Header.tsx           — Admin name, system status indicator
│
├── users/
│   ├── UserTable.tsx        — AG Grid: all users with role, station, status
│   │                          Features: sort, filter, inline edit, bulk actions
│   │                          Data from: GET /api/v1/users
│   │
│   ├── UserForm.tsx         — Modal: add/edit user
│   │                          Fields: name, email, phone, role, station
│   │                          POST /api/v1/users or PUT /api/v1/users/:id
│   │
│   └── RoleSelector.tsx     — Dropdown: Admin, Inspector, Constable
│
├── health/
│   ├── SystemMetrics.tsx    — Recharts: CPU, RAM, Disk, Network over time
│   │                          Data from: Prometheus metrics (via Grafana API or direct)
│   │
│   ├── ServiceStatus.tsx    — Status cards: each Docker service (green/red)
│   │                          backend-api ✅, ml-server ✅, neo4j ✅, etc.
│   │
│   └── ModelPerformance.tsx — Member 1's model metrics: accuracy, precision, recall, F1
│                              Data from: GET /api/v1/predictions/metrics
│
├── audit/
│   ├── AuditLogTable.tsx    — AG Grid: all blockchain audit entries
│   │                          Columns: ID, Event Type, Data Hash, Previous Hash, Time
│   │                          Data from: GET /api/v1/audit
│   │
│   └── ChainVerifier.tsx    — Button: "Verify Chain Integrity"
│                              Calls GET /api/v1/audit with chain_valid check
│                              Shows: "✅ Chain valid" or "❌ Tampered at block #X"
│
└── complaints/
    ├── ComplaintOverview.tsx — Summary stats: total, by status, by fraud type
    │                          Data from: GET /api/v1/complaints
    │
    └── ResolutionStats.tsx  — Recharts: avg resolution time, success rate over time
```

---

## 6. LLM Agent & Chatbot

### LLM Agent (Command Center — Investigation Page)

You build the **frontend chat UI**. Member 2 builds the backend LangChain service.

**Your responsibility:**
1. Build the chat interface (input, messages, results)
2. Send user's natural language query to `POST /api/v1/llm/query`
3. Render the response (text + optional graph/table/action buttons)
4. Show quick prompt chips for common queries
5. Maintain chat history in component state (not persisted)

**You do NOT:** set up LangChain, Gemini API, or Cypher generation. That's Member 2's backend.

**Flow from your perspective:**

```
User types → You POST { "query": "..." } to /api/v1/llm/query
                                    │
            ┌───────────────────────┘
            │
            ▼
Response: {
  "answer": "Found 3 ATMs...",         ← render as text
  "cypher_query": "MATCH ...",          ← show in collapsible "View Query" section
  "results": [...],                     ← render as table or data
  "visualization": { nodes, edges },    ← render as mini vis.js graph
  "follow_up_suggestions": [...]        ← render as clickable chips
}
```

### Integrated Chatbot (FAQ Widget — All Your UIs)

A floating help button (bottom-right) on all 3 of your UIs.

**Your responsibility:**
1. Build the chat widget UI (floating button → expandable chat panel)
2. Send queries to `POST /api/v1/chatbot/query` (simpler endpoint than LLM)
3. Render responses with suggestion chips
4. Show "Did this help? Yes/No" feedback buttons

**Pre-built quick prompts:**
- "What is a mule account?"
- "How do I trigger Step-Up Verification?"
- "How does the predictive model work?"
- "What do the risk scores mean?"

---

## 7. APIs You Consume

Every API call you make. Member 2 builds these endpoints.

### Auth

```
POST /api/v1/auth/login
  Body: { "email": "...", "password": "..." }
  → { "access_token": "eyJ...", "role": "inspector", "expires_in": 14400 }

POST /api/v1/auth/refresh
  Headers: Authorization: Bearer <refresh_token>
  → { "access_token": "eyJ..." }
```

All subsequent requests include: `Authorization: Bearer <access_token>`

### Complaints

```
GET /api/v1/complaints?status=ANALYZING&page=1&limit=20
  → { "items": [Complaint], "total": 45, "page": 1, "pages": 3 }

GET /api/v1/complaints/{complaint_ref}
  → { "complaint_ref": "C1001", "status": "ANALYZING", "fraud_type": "investment",
      "amount": 500000, "predictions": [...], "actions": [...] }
```

### Heatmap

```
GET /api/v1/heatmap?time_range=2h&risk_min=50
  → { "atms": [
       { "atm_id": "A452", "latitude": 12.9716, "longitude": 77.5946,
         "risk_score": 92, "active_complaints": 3 },
       ...
     ] }
```

### Predictions

```
GET /api/v1/predictions/{complaint_ref}
  → { "atm_predictions": [
       { "atm_id": "A452", "latitude": 12.9716, "longitude": 77.5946,
         "risk_score": 0.92, "predicted_window": "2.5 hours",
         "area_type": "commercial", "nearby_metro": "Indiranagar Metro" },
       ...
     ],
     "mule_accounts": [
       { "account_id": "M1001", "mule_score": 92, "risk_level": "HIGH",
         "bank": "SBI", "connected_victims": 3 },
       ...
     ],
     "model_confidence": 0.87, "inference_time_ms": 340 }
```

### Mule Network (for vis.js graph)

```
GET /api/v1/mules/network/{complaint_ref}
  → { "nodes": [
       { "id": "V001", "label": "Victim", "type": "victim", "name": "Rahul S." },
       { "id": "M1001", "label": "Mule A", "type": "mule", "mule_score": 92 },
       { "id": "A452", "label": "ATM #452", "type": "atm", "risk_score": 92 }
     ],
     "edges": [
       { "from": "V001", "to": "M1001", "label": "₹5,00,000", "type": "SENT_MONEY_TO" },
       { "from": "M1001", "to": "A452", "label": "₹4,50,000", "type": "WITHDREW_AT" }
     ] }
```

### Actions

```
POST /api/v1/actions/trigger-verification
  Body: { "complaint_ref": "C1001", "atm_id": "A452", "mule_accounts": ["M1001"] }
  → { "action_id": "...", "status": "TRIGGERED", "message": "Facial recognition enabled" }

POST /api/v1/actions/freeze-account
  Body: { "complaint_ref": "C1001", "account_id": "M1001" }
  → { "action_id": "...", "status": "REQUESTED", "message": "Freeze request sent" }

POST /api/v1/actions/generate-fir
  Body: { "complaint_ref": "C1001" }
  → { "action_id": "...", "fir_draft": "...", "status": "GENERATED" }

POST /api/v1/actions/dispatch-patrol
  Body: { "complaint_ref": "C1001", "atm_id": "A452", "officer_id": "..." }
  → { "action_id": "...", "status": "DISPATCHED" }
```

### LLM Agent

```
POST /api/v1/llm/query
  Body: { "query": "Show all high-risk ATMs in Indiranagar" }
  → { "answer": "Found 3 ATMs...",
      "cypher_query": "MATCH ...",
      "results": [...],
      "visualization": { "type": "graph", "nodes": [...], "edges": [...] },
      "follow_up_suggestions": ["Show mule accounts for these ATMs"] }
```

### Users (Admin Panel)

```
GET /api/v1/users?page=1&limit=50
  → { "items": [User], "total": 120 }

POST /api/v1/users
  Body: { "name": "...", "email": "...", "phone": "...", "role": "inspector", "station": "..." }

PUT /api/v1/users/{id}
DELETE /api/v1/users/{id}
```

### Audit Log (Admin Panel)

```
GET /api/v1/audit?page=1&limit=50&event_type=action_taken
  → { "items": [AuditEntry], "chain_valid": true }
```

### WebSocket Events (you listen for)

```
Connect: /ws/alerts  (with JWT token)

Events you receive:
  NEW_ALERT         → { complaint_ref, atm_id, risk_score, message }
  STATUS_UPDATE     → { complaint_ref, old_status, new_status }
  PREDICTION_READY  → { complaint_ref, atm_count, high_risk_mules }
```

---

## 8. Data Shapes You Render

TypeScript types for all data you handle. Put these in `packages/shared-ui/src/types/`.

```typescript
// complaint.ts
export type ComplaintStatus = 'SUBMITTED' | 'ANALYZING' | 'ACTION_TAKEN' | 'RESOLVED' | 'CLOSED';
export type FraudType = 'investment' | 'kyc' | 'upi' | 'lottery' | 'job' | 'loan' | 'other';

export interface Complaint {
  complaint_ref: string;
  status: ComplaintStatus;
  fraud_type: FraudType;
  amount: number;
  created_at: string;
  updated_at: string;
}

// prediction.ts
export interface ATMPrediction {
  atm_id: string;
  latitude: number;
  longitude: number;
  risk_score: number;        // 0.0 to 1.0
  predicted_window: string;  // e.g., "2.5 hours"
  area_type: string;
  nearby_metro: string;
}

export interface MuleAccount {
  account_id: string;
  mule_score: number;        // 0 to 100
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  bank: string;
  connected_victims: number;
}

// graph.ts
export interface GraphNode {
  id: string;
  label: string;
  type: 'victim' | 'mule' | 'atm' | 'complaint' | 'phone' | 'upi' | 'bank_account';
  mule_score?: number;
  risk_score?: number;
  name?: string;
}

export interface GraphEdge {
  from: string;
  to: string;
  label: string;
  type: 'SENT_MONEY_TO' | 'TRANSFERRED_TO' | 'WITHDREW_AT' | 'CONNECTED_TO';
}

// user.ts
export type UserRole = 'admin' | 'inspector' | 'constable';

export interface User {
  id: string;
  name: string;
  email: string;
  phone: string;
  role: UserRole;
  station: string;
  is_active: boolean;
}

// websocket.ts
export interface WSAlert {
  type: 'NEW_ALERT' | 'STATUS_UPDATE' | 'PREDICTION_READY';
  data: Record<string, unknown>;
}

// api.ts
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pages: number;
}

export interface ApiError {
  detail: string;
  status_code: number;
}
```

---

## 9. Your Folder Structure

Detailed structure for your apps. Other members' folders shown collapsed.

```
SIH-2026-Team-CHOCO/
│
├── PROJECT_REFERENCE.md
├── .gitignore
├── .env.example
├── pnpm-workspace.yaml
├── package.json
├── docker-compose.yml
├── docker-compose.dev.yml
│
├── apps/
│   │
│   ├── command-center/                   # ── YOUR APP ──
│   │   ├── public/
│   │   │   ├── favicon.ico
│   │   │   └── manifest.json
│   │   ├── src/
│   │   │   ├── assets/
│   │   │   ├── components/
│   │   │   │   ├── layout/
│   │   │   │   │   ├── Sidebar.tsx
│   │   │   │   │   ├── Header.tsx
│   │   │   │   │   └── MainLayout.tsx
│   │   │   │   ├── map/
│   │   │   │   │   ├── RiskHeatmap.tsx
│   │   │   │   │   ├── ATMMarker.tsx
│   │   │   │   │   ├── MapControls.tsx
│   │   │   │   │   └── ATMPopup.tsx
│   │   │   │   ├── graph/
│   │   │   │   │   ├── NetworkGraph.tsx
│   │   │   │   │   ├── GraphControls.tsx
│   │   │   │   │   └── NodeDetail.tsx
│   │   │   │   ├── llm/
│   │   │   │   │   ├── ChatInterface.tsx
│   │   │   │   │   ├── MessageBubble.tsx
│   │   │   │   │   ├── QuickPrompts.tsx
│   │   │   │   │   └── QueryResult.tsx
│   │   │   │   ├── actions/
│   │   │   │   │   ├── ActionPanel.tsx
│   │   │   │   │   ├── TriggerVerification.tsx
│   │   │   │   │   ├── FreezeAccount.tsx
│   │   │   │   │   ├── GenerateFIR.tsx
│   │   │   │   │   └── DispatchPatrol.tsx
│   │   │   │   └── dashboard/
│   │   │   │       ├── StatsCards.tsx
│   │   │   │       ├── AlertFeed.tsx
│   │   │   │       └── ComplaintTable.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useWebSocket.ts
│   │   │   │   └── useMapData.ts
│   │   │   ├── pages/
│   │   │   │   ├── DashboardPage.tsx
│   │   │   │   ├── InvestigationPage.tsx
│   │   │   │   ├── AlertsPage.tsx
│   │   │   │   └── SettingsPage.tsx
│   │   │   ├── services/
│   │   │   │   ├── api.ts
│   │   │   │   ├── websocket.ts
│   │   │   │   └── llmService.ts
│   │   │   ├── store/
│   │   │   │   ├── store.ts
│   │   │   │   ├── slices/
│   │   │   │   │   ├── authSlice.ts
│   │   │   │   │   ├── complaintsSlice.ts
│   │   │   │   │   ├── mapSlice.ts
│   │   │   │   │   └── alertsSlice.ts
│   │   │   │   └── api/
│   │   │   │       └── apiSlice.ts
│   │   │   ├── types/
│   │   │   │   └── index.ts
│   │   │   ├── utils/
│   │   │   │   ├── formatters.ts
│   │   │   │   └── constants.ts
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   └── index.css
│   │   ├── Dockerfile
│   │   ├── nginx.conf
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── vite.config.ts
│   │   ├── tailwind.config.ts
│   │   └── eslint.config.js
│   │
│   ├── field-dashboard/                  # ── YOUR APP ──
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── layout/
│   │   │   │   │   ├── MobileHeader.tsx
│   │   │   │   │   └── BottomNav.tsx
│   │   │   │   ├── alerts/
│   │   │   │   │   ├── AlertCard.tsx
│   │   │   │   │   ├── AlertList.tsx
│   │   │   │   │   └── AlertDetail.tsx
│   │   │   │   ├── map/
│   │   │   │   │   └── NavigationMap.tsx
│   │   │   │   └── actions/
│   │   │   │       ├── QuickActions.tsx
│   │   │   │       ├── DispatchButton.tsx
│   │   │   │       └── BackupRequest.tsx
│   │   │   ├── hooks/
│   │   │   ├── pages/
│   │   │   │   ├── AlertsPage.tsx
│   │   │   │   ├── AlertDetailPage.tsx
│   │   │   │   └── ProfilePage.tsx
│   │   │   ├── services/
│   │   │   ├── store/
│   │   │   ├── types/
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   └── index.css
│   │   ├── Dockerfile
│   │   ├── nginx.conf
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── vite.config.ts
│   │   ├── tailwind.config.ts
│   │   └── eslint.config.js
│   │
│   ├── admin-panel/                      # ── YOUR APP ──
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── layout/
│   │   │   │   │   ├── Sidebar.tsx
│   │   │   │   │   └── Header.tsx
│   │   │   │   ├── users/
│   │   │   │   │   ├── UserTable.tsx
│   │   │   │   │   ├── UserForm.tsx
│   │   │   │   │   └── RoleSelector.tsx
│   │   │   │   ├── health/
│   │   │   │   │   ├── SystemMetrics.tsx
│   │   │   │   │   ├── ServiceStatus.tsx
│   │   │   │   │   └── ModelPerformance.tsx
│   │   │   │   ├── audit/
│   │   │   │   │   ├── AuditLogTable.tsx
│   │   │   │   │   └── ChainVerifier.tsx
│   │   │   │   └── complaints/
│   │   │   │       ├── ComplaintOverview.tsx
│   │   │   │       └── ResolutionStats.tsx
│   │   │   ├── hooks/
│   │   │   ├── pages/
│   │   │   │   ├── UsersPage.tsx
│   │   │   │   ├── SystemHealthPage.tsx
│   │   │   │   ├── AuditPage.tsx
│   │   │   │   ├── ComplaintsPage.tsx
│   │   │   │   └── SettingsPage.tsx
│   │   │   ├── services/
│   │   │   ├── store/
│   │   │   ├── types/
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   └── index.css
│   │   ├── Dockerfile
│   │   ├── nginx.conf
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── vite.config.ts
│   │   ├── tailwind.config.ts
│   │   └── eslint.config.js
│   │
│   ├── victim-portal/                    # Member 4's app (you don't touch this)
│   │   └── ...
│   │
│   └── backend/                          # Member 2's app (you don't touch this)
│       └── ...
│
├── ml/                                   # Member 1's work (you don't touch this)
│   └── ...
│
├── packages/
│   └── shared-ui/                        # ── SHARED WITH MEMBER 4 ──
│       ├── src/
│       │   ├── components/
│       │   │   ├── Button.tsx
│       │   │   ├── Card.tsx
│       │   │   ├── Modal.tsx
│       │   │   ├── Input.tsx
│       │   │   ├── Badge.tsx
│       │   │   ├── Alert.tsx
│       │   │   ├── Spinner.tsx
│       │   │   ├── ConfirmDialog.tsx
│       │   │   ├── ErrorBoundary.tsx
│       │   │   └── index.ts
│       │   ├── hooks/
│       │   │   ├── useAuth.ts
│       │   │   ├── useWebSocket.ts
│       │   │   └── useApi.ts
│       │   ├── types/
│       │   │   ├── complaint.ts
│       │   │   ├── user.ts
│       │   │   ├── prediction.ts
│       │   │   ├── action.ts
│       │   │   └── api.ts
│       │   ├── utils/
│       │   │   ├── formatters.ts
│       │   │   ├── validators.ts
│       │   │   └── constants.ts
│       │   └── themes/
│       │       ├── dark.ts
│       │       └── light.ts
│       ├── package.json
│       └── tsconfig.json
│
├── infra/                                # ── YOUR WORK ──
│   ├── docker/
│   │   └── nginx/
│   │       └── default.conf
│   ├── k8s/
│   │   ├── namespace.yaml
│   │   ├── deployments/
│   │   │   ├── backend.yaml
│   │   │   ├── command-center.yaml
│   │   │   ├── field-dashboard.yaml
│   │   │   ├── admin-panel.yaml
│   │   │   ├── victim-portal.yaml
│   │   │   ├── ml-server.yaml
│   │   │   ├── neo4j.yaml
│   │   │   ├── postgres.yaml
│   │   │   └── redis.yaml
│   │   ├── services/
│   │   ├── configmaps/
│   │   │   └── app-config.yaml
│   │   ├── secrets/
│   │   │   └── app-secrets.yaml
│   │   └── ingress.yaml
│   ├── jenkins/
│   │   └── Jenkinsfile
│   ├── monitoring/
│   │   ├── prometheus/
│   │   │   └── prometheus.yml
│   │   └── grafana/
│   │       └── dashboards/
│   │           ├── system-health.json
│   │           └── application-metrics.json
│   └── logging/
│       └── elk/
│           └── docker-compose.elk.yml
│
├── docs/
│   └── ...
│
├── scripts/
│   ├── setup-dev.sh
│   ├── seed-database.sh
│   └── run-demo.sh
│
└── .github/
    └── workflows/
        └── ci.yml
```

### Port Allocation (you need to know all of these for Docker/K8s)

| Service | Port | Owner |
|---|---|---|
| Victim Portal | 3000 | Member 4 |
| Command Center | 3001 | **You** |
| Field Dashboard | 3002 | **You** |
| Admin Panel | 3003 | **You** |
| FastAPI Backend | 8000 | Member 2 |
| ML Model Server | 8081 | Member 1 |
| PostgreSQL | 5432 | Member 2 |
| Neo4j Bolt | 7687 | Member 2 |
| Neo4j HTTP | 7474 | Member 2 |
| Redis | 6379 | Member 2 |
| Nginx Gateway | 80 | **You** |
| Prometheus | 9090 | **You** |
| Grafana | 3100 | **You** |

---

## 10. DevOps Infrastructure

### Docker Compose

You write `docker-compose.yml` that spins up ALL services:

```yaml
services:
  nginx-gateway:       # Port 80  — routes to all frontends + backend
  victim-frontend:     # Port 3000
  admin-frontend:      # Port 3001
  field-frontend:      # Port 3002
  admin-panel:         # Port 3003
  backend-api:         # Port 8000
  ml-server:           # Port 8081
  postgres-db:         # Port 5432
  neo4j-db:            # Port 7687 + 7474
  redis-cache:         # Port 6379
  prometheus:          # Port 9090
  grafana:             # Port 3100
```

`docker-compose.dev.yml` adds: hot reload via volume mounts, debug mode, exposed DB ports.

### Kubernetes (Minikube)

- Namespace: `sih-choco`
- One Deployment + Service per microservice
- ConfigMaps for API URLs
- Secrets for DB passwords, JWT secret, API keys
- Ingress (Nginx Ingress Controller) for routing
- HPA on `ml-server` (auto-scale based on CPU)

### CI/CD Pipeline (Jenkins)

```
GitHub Push → Webhook → Jenkins
  ├── Stage 1: Lint (ESLint + Prettier) + Type Check (tsc)
  ├── Stage 2: Unit Tests (Jest)
  ├── Stage 3: Build Docker images (multi-stage builds)
  ├── Stage 4: Push to GitHub Container Registry
  ├── Stage 5: Deploy to Minikube (kubectl apply)
  ├── Stage 6: Health check (all pods Running)
  └── Stage 7: Notify team (Discord)
```

### Monitoring

**Prometheus** scrapes:
- System: CPU, RAM, Disk per container
- Application: API latency p95, error rate, request count
- Business: complaint volume, prediction accuracy

**Grafana dashboards** you create:
- `system-health.json` — all container metrics
- `application-metrics.json` — API performance + business KPIs

**Alerts:**
- CPU > 80% → notify
- API latency > 2s → investigate
- Container restart > 3x in 5min → auto-notify

### Logging (ELK)

All services → stdout → Docker → Logstash → Elasticsearch → Kibana

---

## 11. Environment Variables

Variables your frontend apps need (in each app's `.env`):

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=http://localhost:8000
VITE_APP_NAME="Cyber Command Center"        # or "Field Dashboard" / "Admin Panel"
```

Variables for Docker/K8s (in root `.env`):

```bash
POSTGRES_HOST=postgres-db
POSTGRES_PORT=5432
POSTGRES_DB=sih_choco
POSTGRES_USER=choco_admin
POSTGRES_PASSWORD=YOUR_PASSWORD
NEO4J_URI=bolt://neo4j-db:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=YOUR_PASSWORD
REDIS_URL=redis://redis-cache:6379/0
JWT_SECRET=YOUR_JWT_SECRET
GEMINI_API_KEY=YOUR_GEMINI_KEY
```

---

## 12. Git Workflow

```
feature/m3/command-center-heatmap    ← your feature branch
fix/m3/graph-zoom-performance        ← your bugfix branch
```

Convention: `feat:`, `fix:`, `docs:`, `chore:` commit prefixes.

Flow: feature branch → PR to `dev` → 1 review → merge → periodic `dev` → `main` for demo.

---

## 13. Your 10-Day Plan

| Day | Focus | Deliverable |
|---|---|---|
| **1** | Environment setup, scaffold 3 React + Vite + TS projects, Figma wireframes | 3 apps running locally with routing |
| **2** | Shared component library (`packages/shared-ui`), auth flow, Tailwind dark/light themes | Login/logout working, reusable Button/Card/Modal/Input |
| **3** | Design system finalization, all reusable components, Axios instance with JWT interceptor | Complete shared-ui library, API client ready |
| **4** | Admin Panel: user management (AG Grid), system health (Recharts), audit log viewer | Working admin panel |
| **5** | Command Center: Leaflet heatmap, ATM markers with risk colors, filters, WebSocket for updates | Working heatmap with real-time data |
| **6** | Command Center: vis.js graph visualization, LLM Agent chat interface with quick prompts | Working graph + chat UI |
| **7** | Command Center: action panel (Trigger/Freeze/FIR/Dispatch), chatbot FAQ widget | All actions wired to backend APIs |
| **8** | Field Dashboard: mobile-first alert cards, navigation, quick actions, offline support | Working mobile-responsive dashboard |
| **9** | Dockerfiles for all services, docker-compose.yml, Jenkinsfile, K8s manifests, Minikube | Full stack containerized and orchestrated |
| **10** | Prometheus + Grafana dashboards, Lighthouse optimization, final polish, demo rehearsal | Monitoring live, Lighthouse >90, demo-ready |

---

## 14. Error Handling & Fallbacks

### Frontend Error Handling Pattern

```
React Error Boundary (global) → catches render crashes
    └── Page-level Error Boundary → catches page-specific crashes
        └── Axios interceptor → catches API errors
            └── Retry (3 attempts, exponential backoff)
            └── Fallback to cached data (if available)
            └── Show user-friendly toast notification
```

### Specific Fallbacks

| Failure | Your Fallback |
|---|---|
| LLM API down | Show pre-cached responses (Member 2 stores in Redis, returns with `"cached": true` flag). You show a "(cached)" badge on the response. |
| WebSocket disconnects | Auto-reconnect with exponential backoff (1s, 2s, 4s, 8s). Show "Reconnecting..." toast. Fall back to polling `GET /complaints` every 5s. |
| Heatmap API slow/down | Show last cached heatmap data with "Last updated: X min ago" |
| Graph API returns empty | Show "No data available for this complaint" placeholder |
| Backend returns 5xx | Error Boundary catches, shows "Something went wrong. Try again." with retry button |
| Network offline (Field Dashboard) | Service worker serves cached alerts. Show "Offline — last known alerts" banner. |
| Demo emergency | `VITE_DEMO_MODE=true` → all API calls return hardcoded mock data from local JSON files |

---

## 15. Design Tokens

### Dark Theme (Command Center + Admin Panel)

```css
--bg-primary:    #0a0e17;
--bg-secondary:  #111827;
--bg-card:       #1a1f2e;
--text-primary:  #f0f4f8;
--text-secondary:#94a3b8;
--accent-blue:   #00d4ff;
--accent-cyan:   #06b6d4;
--risk-high:     #ff0040;
--risk-medium:   #ff8c00;
--risk-low:      #00ff88;
--border:        #2a2f3e;
```

### Light Theme (Field Dashboard)

```css
--bg-primary:    #ffffff;
--bg-secondary:  #f8fafc;
--bg-card:       #ffffff;
--text-primary:  #0f172a;
--text-secondary:#64748b;
--accent-blue:   #1a73e8;
--risk-high:     #dc2626;
--risk-medium:   #ea580c;
--risk-low:      #16a34a;
--border:        #e2e8f0;
```

### Typography

```css
--font-family:   'Inter', system-ui, sans-serif;
--font-heading:  600;
--font-body:     400;
--font-mono:     'JetBrains Mono', monospace;
```

### Risk Score → Color Mapping (use everywhere)

```typescript
export function getRiskColor(score: number): string {
  if (score >= 70) return 'var(--risk-high)';    // red
  if (score >= 40) return 'var(--risk-medium)';  // orange
  return 'var(--risk-low)';                       // green
}

export function getRiskLabel(score: number): string {
  if (score >= 70) return 'HIGH';
  if (score >= 40) return 'MEDIUM';
  return 'LOW';
}
```

---

## 16. Demo Script

**You present from 1:30 to 4:45** (3 minutes 15 seconds of the 5-minute demo).

| Time | What you do | What judges see |
|---|---|---|
| 1:30 | Open **Command Center** | Heatmap auto-updates with 3 ATMs from the complaint Member 4 just submitted |
| 1:45 | Click **ATM #452** on map | Popup: Risk 92%, Indiranagar Metro, 2.5 hr window, 2 linked mules |
| 2:00 | Show **Graph Visualization** | vis.js renders: Victim → Mule A (92) → Mule B (78) → ATM #452 |
| 2:30 | Type in **LLM Agent**: "Show mules for C1001" | AI responds with natural language + graph + action buttons |
| 3:00 | Click **"Trigger Step-Up Verification"** | Confirm dialog → success toast: "Facial Recognition Enabled" |
| 3:15 | Open **Field Dashboard** (on phone or responsive view) | Alert card: "🚨 ATM #452, 2.4 km, ~8 min" |
| 3:30 | Click **"Dispatch Patrol"** | Status updates across all dashboards (WebSocket) |
| 3:45 | Open **Admin Panel** | System health metrics, audit log with blockchain hash chain |
| 4:45 | Show **Architecture + DevOps** | Docker, K8s dashboard, Prometheus/Grafana |

---

## 17. Your Presentation Talking Points

1. "We built 3 distinct police-facing web interfaces, each tailored to a specific user persona"
2. "The Command Center provides real-time ATM risk heatmaps and interactive fraud network graphs"
3. "Officers can query our graph database in plain English through the LLM Agent"
4. "The Field Dashboard is mobile-first — big buttons, glanceable alerts, offline support"
5. "We containerized all 10+ services with Docker and orchestrated with Kubernetes"
6. "Our Jenkins CI/CD pipeline builds, tests, and deploys on every push"
7. "Prometheus and Grafana give us real-time observability across every service"
8. "The system is production-ready and horizontally scalable"

**Judge questions you'll handle:**

| Question | Your Answer |
|---|---|
| "How scalable is this?" | Kubernetes auto-scaling via HPA. ML service scales independently based on complaint queue. Microservices arch means each service scales individually. |
| "What about offline use?" | Field Dashboard has service worker caching. Officers see last known alerts when offline. Reconnects automatically. |
| "How do you deploy updates?" | Jenkins CI/CD with rolling updates in K8s. Zero-downtime deployment. |
| "What if the LLM gives a wrong query?" | We show the generated Cypher query in a collapsible section so officers can verify. We also have query guardrails and fallback to cached responses. |

---

## 18. KPIs for Your Work

### UI Performance

| Metric | Target |
|---|---|
| First Contentful Paint | < 1.5s |
| Time to Interactive | < 3s |
| Lighthouse Score | > 90 (all 3 UIs) |
| Animation FPS | 60 |

### Map & Graph

| Metric | Target |
|---|---|
| 500 ATM markers rendered | No lag |
| Heatmap update on new prediction | < 2s |
| 100 graph nodes rendered | Smooth zoom/pan |
| Node selection | < 100ms |

### LLM Chat

| Metric | Target |
|---|---|
| Query to response displayed | < 5s (depends on Member 2's backend) |

### DevOps

| Metric | Target |
|---|---|
| `docker-compose up` to all healthy | < 3 min |
| CI/CD pipeline | < 10 min |
| Zero crashes during demo | Required |
| Service recovery | < 60s |

### Accessibility

| Metric | Target |
|---|---|
| WCAG 2.1 AA | All 3 UIs |
| Color-blind safe | Icons + labels, not just color |
| Keyboard navigable | All interactive elements |

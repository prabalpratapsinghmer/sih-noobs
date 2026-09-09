# System Architecture

> SIH 2026 · SIH26184 · Predictive Analytics Framework for Cybercrime Complaints

This document describes the complete system architecture. All AI agents working on this project should read this first.

---

## 1. Project Summary

**Problem:** When a cybercrime complaint is filed, police take 2–4 hours to coordinate with banks. By then, criminals have withdrawn money from ATMs.

**Solution:** A predictive analytics platform that reduces response time to under 10 minutes by:
1. Instantly analyzing victim complaints
2. Predicting which ATM the criminal will use
3. Triggering facial recognition / OTP verification at that ATM
4. Alerting nearby police officers
5. Identifying and freezing mule accounts

**Core Promise:** Complaint filed → police action in < 10 minutes.

---

## 2. System Layers

The platform has six layers:

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1 — USER INTERFACES (Member 3 frontend + Member 4 victim)│
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Victim   │ │ Command  │ │  Field   │ │  Admin   │           │
│  │ Portal   │ │ Center   │ │Dashboard │ │  Panel   │           │
│  │ :3000    │ │ :3003    │ │ :3002    │ │ :3001    │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
├───────┼──────────────┼────────────┼────────────┼─────────────────┤
│  LAYER 2 — API GATEWAY & BACKEND SERVICES (Member 2)            │
│       │              │            │            │                 │
│  ┌────▼──────────────▼────────────▼────────────▼─────┐          │
│  │              FastAPI REST APIs  :8000              │          │
│  │              WebSocket Server   /ws                │          │
│  │              JWT Auth + RBAC                       │          │
│  │              Banking Switch API Mock               │          │
│  └──────────┬──────────┬──────────┬──────────────────┘          │
├─────────────┼──────────┼──────────┼─────────────────────────────┤
│  LAYER 3 — AI/ML ENGINE (Member 1, GPU machines)                │
│  ┌──────────▼──────────▼──────────▼──────────────────┐          │
│  │  Spatio-Temporal Transformer   (ATM prediction)   │          │
│  │  Graph Neural Network          (mule detection)   │          │
│  │  Mule Scoring Algorithm        (risk 0–100)       │          │
│  │  LLM Agent                     (NL → Cypher)      │          │
│  └───────────────────────────────────────────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 4 — DATA LAYER                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │PostgreSQL│ │  Neo4j   │ │  Redis   │ │  IPFS    │           │
│  │ :5432    │ │ :7687    │ │ :6379    │ │ (gateway)│           │
│  │ PII, users│ │ Graphs  │ │ Cache, WS│ │ Evidence │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 5 — BLOCKCHAIN AUDIT (hash trail, not full data)         │
│  ┌───────────────────────────────────────────────────┐          │
│  │  Complaint timestamps · Evidence hashes            │          │
│  │  Prediction triggers · Police actions               │          │
│  │  Resolution status · Chain of custody               │          │
│  └───────────────────────────────────────────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 6 — DEVOPS (Member 3, end to end)                       │
│  ┌───────────────────────────────────────────────────┐          │
│  │  Docker + Compose · Kubernetes (Minikube)          │          │
│  │  Jenkins CI/CD · GitHub Actions                     │          │
│  │  Prometheus + Grafana · ELK Stack                   │          │
│  │  Nginx Gateway · Monitoring · Logging               │          │
│  └───────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow: End-to-End

### Phase 1: Victim Complaint (T+0 to T+2 min)
1. Victim opens Victim Portal or sends message via the (future) WhatsApp bot.
2. Fills the 3-step complaint form: Personal Details → Fraud Details → Fraudster Details.
3. Uploads evidence (screenshots, transaction proofs).
4. Backend receives complaint → stores in PostgreSQL → assigns `complaint_id` (e.g., `C1001`).
5. Complaint metadata is hashed and written to the blockchain audit trail.
6. Victim receives confirmation: "Complaint #C1001 Registered" with a reference number.
7. WebSocket `complaint.created` event is broadcast to Command Center.

### Phase 2: AI Analysis & Prediction (T+2 to T+5 min)
1. Backend triggers the ML pipeline via the ML server API (`/api/v1/model/predict`).
2. **Spatio-Temporal Transformer** analyzes:
   - Fraudster's historical withdrawal patterns
   - Spatial factors (ATM proximity to metro, police stations, transport hubs)
   - Temporal factors (time of day, day of week, fraud patterns)
   - Local traffic density and transit accessibility
3. **Graph Neural Network** traces funds through the transaction network:
   - Identifies the full money trail: Victim → Primary Mule → Secondary Mule → ATM
   - Each account scored 0–100 based on suspicious patterns
4. Backend merges prediction + mule data.
5. WebSocket `prediction.new` event pushes top-3 ATM predictions to Command Center.

### Phase 3: Automated Actions (T+5 to T+10 min)
1. System calls Banking Switch API Mock to enable Step-Up Verification on the predicted ATM.
2. High-risk mule accounts (score ≥ 70) are flagged for immediate freeze.
3. Freeze request letters are auto-generated and queued for Bank Nodal Officer.
4. Police alert is generated: ATM location, risk score, connected mules, withdrawal window.
5. WebSocket `alert.push` event pushes to Field Dashboard.
6. All actions logged on blockchain audit trail.

### Phase 4: Police Investigation (T+10 to T+30 min)
1. Inspector sees new alert in Command Center toast + heatmap update.
2. Inspector examines the money-trail graph in the Command Center.
3. Inspector uses LLM Agent to query: "Show all high-risk ATMs in [area] connected to [fraud type]".
4. Inspector triggers actions: Step-Up Verification, Account Freeze, FIR Draft, Patrol Dispatch.
5. Constable on patrol receives the alert on their Field Dashboard.
6. Constable navigates to the ATM, dispatches, verifies, or requests backup.

### Phase 5: Resolution & Feedback (T+30 min to T+2 hours)
1. Criminal attempts withdrawal → facial recognition / OTP verification blocks it.
2. Police arrive → suspect intercepted or ATM secured.
3. Mule accounts frozen → money recovered.
4. Officer marks case as "RESOLVED" or "SUCCESSFUL_PREVENTION".
5. System logs all predictions, actions, and outcomes.
6. Models are periodically retrained with new data (feedback loop).

---

## 4. Service Communication Map

```
Victim Portal ──HTTP──▶ Backend API ──HTTP──▶ ML Server (GPU)
Command Center ──HTTP──▶ Backend API ──HTTP──▶ Neo4j (graph queries)
Command Center ──WS────▶ Backend API ──WS────▶ Redis (pub/sub)
Field Dashboard ─WS───▶ Backend API ──WS────▶ Redis (pub/sub)
Admin Panel ──HTTP───▶ Backend API ──SQL───▶ PostgreSQL
Backend API ──HTTP──▶ IPFS Gateway (evidence)
Backend API ──gRPC──▶ Blockchain Node (hash writing)
Nginx Gateway ───reverse-proxies──▶ all of the above
```

---

## 5. Tech Stack

### Frontend (Member 3)
| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Framework | React 19 + TypeScript (strict) | Component model, ecosystem, type safety |
| State | Redux Toolkit (RTK Query) | Server cache + realtime slices |
| Styling | Tailwind CSS + shadcn/ui | Token-driven, composable, fast |
| Maps | Leaflet.js (OpenStreetMap tiles) | Free, no API key, good performance |
| Graphs | D3.js (force-directed) | Full control over force layout + realtime |
| Charts | Recharts | React-native, clean, works in Admin |
| Forms | React Hook Form + Zod | Validated against API schemas |
| HTTP | Axios (with interceptors) | Auth, refresh, error handling |
| WebSocket | Native WebSocket (wrapper) | No extra dependency; swappable |
| Animation | Framer Motion (minimal) | Only where motion serves the UX |
| Tables | AG Grid (if needed for data-heavy views) | Filterable, sortable, large datasets |

### Backend (Member 2)
| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI (Python) |
| Database | PostgreSQL 16, Neo4j 5, Redis 7 |
| Auth | JWT (PyJWT) + bcrypt |
| WebSocket | FastAPI WebSocket / python-socketio |
| Blockchain | Hyperledger Fabric / Ethereum (hash trail) |
| Evidence | IPFS (encrypted, CID stored in Postgres) |

### ML/AI (Member 1)
| Layer | Technology |
|-------|-----------|
| Model serving | TorchServe on GPU machines |
| ATM prediction | Spatio-Temporal Transformer |
| Mule detection | Graph Neural Network (GNN) |
| LLM agent | LangChain + LLM (GPT-4/Claude/LLaMA) |
| Language | Python, PyTorch |

### DevOps (Member 3)
| Layer | Technology |
|-------|-----------|
| Containers | Docker + Docker Compose |
| Orchestration | Kubernetes (Minikube for local demo) |
| CI/CD | Jenkins (primary) + GitHub Actions (backup) |
| Monitoring | Prometheus + Grafana |
| Logging | ELK (Elasticsearch + Logstash/Filebeat + Kibana) |
| Gateway | Nginx (reverse proxy, path routing) |
| Security scan | SonarQube (code quality), OWASP ZAP (optional) |

---

## 6. User Roles

| Role | Access | Sessions |
|------|--------|----------|
| `admin` | Full access to Admin Panel + all features | 8 hours |
| `inspector` | Command Center (map, graph, LLM, actions, all complaints) | 4 hours |
| `constable` | Field Dashboard (alerts, dispatch, verify, limited complaints) | 4 hours |
| `victim` | Own complaint + status only (Victim Portal, Member 4) | 2 hours |

---

## 7. Security Model

- **Encryption at rest:** All victim PII encrypted with AES-256 (PostgreSQL column-level).
- **Encryption in transit:** TLS 1.3 for all HTTP/WS connections.
- **Evidence integrity:** Files encrypted before IPFS upload; file hash + CID stored on blockchain.
- **Password hashing:** bcrypt with 12 salt rounds.
- **API security:** Rate limiting (100 req/min/user), CORS allowlist, CSP headers, Pydantic/Zod validation.
- **Blockchain audit:** Every action (complaint, prediction, trigger, freeze, resolution) is hashed and stored on-chain for tamper-proof legal admissibility.

---

## 8. Port Map

| Service | Internal Port | Public Route (nginx :80) |
|---------|--------------|--------------------------|
| Victim Portal | 3000 | `/` |
| Admin Panel | 3001 | `/admin` |
| Field Dashboard | 3002 | `/field` |
| Command Center | 3003 | `/command` |
| Backend API | 8000 | `/api` + `/ws` |
| ML Model Server | 8080 | internal (`/api/v1/model`) |
| Neo4j (bolt) | 7687 | internal |
| Neo4j (HTTP) | 7474 | internal |
| PostgreSQL | 5432 | internal |
| Redis | 6379 | internal |
| Blockchain Node | 7050 | internal |
| Nginx Gateway | **80** / 443 | all routes |

---

## 9. What Member 3 Owns

Member 3 is responsible for:
- **3 web applications:** Command Center, Field Dashboard, Admin Panel
- **Shared design system:** `@sih/ui` package (tokens, components, hooks, clients)
- **DevOps:** Docker, Compose, K8s, CI/CD, monitoring, logging, security scanning
- **Performance:** Lighthouse ≥ 90, WCAG 2.1 AA, all KPIs in `KPIS.md`

Member 3 does NOT own:
- Victim Portal (Member 4) — but consumes the shared `@sih/ui`
- Backend APIs (Member 2) — but defines contracts jointly in `API_CONTRACTS.md`
- ML models (Member 1) — but renders their outputs
- WhatsApp bot / mobile apps — deferred to a later build phase

---

## 10. Cross-References

- `API_CONTRACTS.md` — all REST endpoints
- `WS_EVENTS.md` — all WebSocket events
- `AUTH_AND_RBAC.md` — authentication and authorization
- `DESIGN_SYSTEM.md` — tokens and theme system
- `DEVOPS.md` — Docker Compose and Kubernetes
- `COMMAND_CENTER_SPEC.md` — Command Center features
- `FIELD_DASHBOARD_SPEC.md` — Field Dashboard features
- `ADMIN_PANEL_SPEC.md` — Admin Panel features
- `TEAM_SYNC.md` — coordination with other members

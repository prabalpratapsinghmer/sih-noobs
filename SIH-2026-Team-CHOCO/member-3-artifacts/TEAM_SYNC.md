# Team Sync — Inter-Member Coordination

> Who depends on whom, what we need from each other, and when we sync.

---

## 1. Team Overview

| Member | Role | GPU | Primary ownership |
|--------|------|-----|-------------------|
| M1 | ML Lead | ✅ | Spatio-Temporal Transformer, GNN, LLM agent |
| M2 | Backend Guru | ✅ | FastAPI, Postgres/Neo4j/Redis, JWT, WebSocket |
| **M3** | **Frontend & DevOps Lead** | ❌ | **3 web apps, shared UI kit, full DevOps pipeline** |
| M4 | Victim & Integration | ❌ | Victim Portal, complaint flow, WhatsApp (deferred) |

---

## 2. What I Need from Each Member

### From M2 (Backend) — Daily sync
| What | When | Why |
|------|------|-----|
| Final API contracts (§9 of ARCHITECTURE) | Day 1 | I build against these; changing them mid-build is expensive |
| WebSocket event names + payloads | Day 1 | Frontend event handlers must match exactly |
| Sample JSON for each endpoint | Day 1–2 | I build mock data and UI components before backend is ready |
| CORS configuration | Day 1 | My frontend apps need to call the API during dev |
| Auth token format (JWT claims) | Day 1 | I decode tokens for role-based routing |
| Health endpoint structure | Day 3 | I build the Admin health dashboard |

### From M1 (ML) — 2–3× per week
| What | When | Why |
|------|------|-----|
| Prediction API endpoint + response shape | Day 2–3 | I render the heatmap and prediction cards |
| Sample predictions (10+ ATM points with risk scores) | Day 3 | I build the map with realistic demo data |
| Mule graph endpoint + node/edge shapes | Day 5 | I build the D3 graph visualization |
| Model metrics endpoint (accuracy/precision/recall/latency) | Day 3 | I build the Admin model metrics dashboard |
| LLM agent endpoint + streaming format | Day 5–6 | I build the chat interface |
| Accuracy numbers for talking points | Day 9 | Demo presentation |

### From M4 (Victim/Integration) — On ui-kit changes
| What | When | Why |
|------|------|-----|
| Feedback on `@sih/ui` components | Day 2–3 | I need to know if the shared API works for them |
| Confirmation that Victim Portal consumes the same tokens | Day 2 | We must share a consistent look |
| Report any bugs in `@sih/ui` | Ongoing | I fix the package, bump version |

---

## 3. What I Provide to Each Member

### To M2 (Backend)
| What | When |
|------|------|
| Frontend origin URLs for CORS | Day 1 |
| Requested API field names / shapes (if I need something different) | Day 1–2 |
| Bug reports with expected vs actual API response | Ongoing |
| WebSocket connection test results | Day 3 |

### To M1 (ML)
| What | When |
|------|------|
| Map rendering confirmation (markers show correctly) | Day 3 |
| Graph visualization confirmation (nodes/edges render) | Day 6 |
| Model metrics display in Admin Panel | Day 3 |
| LLM agent chat working end-to-end | Day 7 |

### To M4 (Victim)
| What | When |
|------|------|
| `@sih/ui` package (components, tokens, hooks) | Day 2 |
| Tailwind preset for consistent theming | Day 2 |
| API client + WebSocket wrapper | Day 2 |
| Auth flow + token handling | Day 2 |
| Breaking change notifications | Before any major version bump |

---

## 4. Sync Cadence

| Sync | Frequency | Duration | Participants |
|------|-----------|----------|-------------|
| API contract review | Daily (Day 1–3) | 15 min | M2 + M3 |
| Frontend demo | Daily (Day 3–10) | 10 min | M3 + M4 |
| ML integration check | 2×/week (Day 3, 6, 9) | 15 min | M1 + M3 |
| Full team standup | Daily | 10 min | All |
| Demo dry run | Day 9–10 | 30 min | All |

---

## 5. Shared Artifacts

| File | Location | Maintained by |
|------|----------|---------------|
| API Contracts | `docs/API-CONTRACTS.md` | M2 + M3 jointly |
| UI Kit API | `docs/UI-KIT-API.md` | M3 |
| Stack & Ports | `docs/STACK.md` | M3 |
| Environment Vars | `.env.example` | M3 |
| Architecture | `docs/ARCHITECTURE.md` | M3 |

All shared docs live in the repo under `docs/` so everyone has access.

---

## 6. Conflict Resolution

- **API contract disagreement:** M2's implementation is truth for backend behavior; M3's spec is truth for frontend expectations. We reconcile in `API_CONTRACTS.md` before coding.
- **UI design disagreement:** M3's design system (`DESIGN_SYSTEM.md`) is truth. M4 implements against it.
- **Priority conflict:** Complaint → police action timeline is the priority. Everything else defers.
- **Breaking change:** Must notify affected member 24h in advance + bump version.

---

## 7. Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| M2 backend not ready in time | Frontend blocked | I build with mock data first; swap to real API when ready |
| M1 ML model accuracy below 85% | Demo credibility | Show demo with seeded high-quality predictions; real model runs behind |
| M4 ui-kit integration issues | Victim Portal broken | I prioritize ui-kit stability; test with M4 early |
| Demo WiFi failure | Can't show live | PWA offline mode + pre-seeded data + recorded backup video |
| GPU not available for ML demo | Slow predictions | Pre-compute predictions; cache in Redis |

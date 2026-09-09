# Member 3 — Frontend & DevOps Lead — Artifact Index

> **SIH 2026 · SIH26184 · Predictive Analytics Framework for Cybercrime Complaints**

This folder is the **single source of truth** for everything Member 3 owns. Every `.md` file here is structured for consumption by other AI agents, human developers, and team members. Read the relevant artifact before working on any feature.

---

## Quick Reference: Which Artifact to Read

| Task | Artifact |
|------|----------|
| Understand the system | `ARCHITECTURE.md` |
| Build against the backend | `API_CONTRACTS.md` |
| Wire up real-time updates | `WS_EVENTS.md` |
| Authenticate / authorize users | `AUTH_AND_RBAC.md` |
| Build UI components | `DESIGN_SYSTEM.md` → `COMPONENT_SPEC.md` → `UI_KIT_API.md` |
| Build the Command Center map | `LEAFLET_MAP_SPEC.md` |
| Build the Command Center graph | `D3_GRAPH_SPEC.md` |
| Build the LLM agent interface | `LLM_AGENT_SPEC.md` |
| Build the Command Center app | `COMMAND_CENTER_SPEC.md` |
| Build the Field Dashboard | `FIELD_DASHBOARD_SPEC.md` |
| Build the Admin Panel | `ADMIN_PANEL_SPEC.md` |
| Set up the repo | `MONOREPO_STRUCTURE.md` |
| Set up env vars | `ENV.md` |
| Set up infrastructure | `DEVOPS.md` |
| Set up CI/CD | `CICD.md` |
| Set up monitoring & logging | `MONITORING.md` |
| Measure performance | `KPIS.md` |
| Coordinate with other members | `TEAM_SYNC.md` |
| Execute the development schedule | `TEN_DAY_PLAN.md` |
| Prepare the demo | `DEMO_PLAN.md` |

---

## File List

| # | File | Purpose | Primary consumer |
|---|------|---------|-----------------|
| 1 | `README.md` | This index | Everyone |
| 2 | `ARCHITECTURE.md` | System architecture + layers + data flow | All agents |
| 3 | `API_CONTRACTS.md` | REST API v1 — endpoints, request/response shapes | Backend + Frontend agents |
| 4 | `WS_EVENTS.md` | WebSocket event taxonomy + payload schemas | Frontend agents |
| 5 | `AUTH_AND_RBAC.md` | Auth flow, token handling, route guards, roles | Frontend + Backend agents |
| 6 | `DESIGN_SYSTEM.md` | Tokens, themes, typography, spacing, semantics | All frontend agents |
| 7 | `COMPONENT_SPEC.md` | React component contracts, props, states | Frontend agents |
| 8 | `UI_KIT_API.md` | Shared `@sih/ui` package surface | Frontend agents (incl. M4) |
| 9 | `COMMAND_CENTER_SPEC.md` | Full Command Center feature spec | Command Center agent |
| 10 | `FIELD_DASHBOARD_SPEC.md` | Full Field Dashboard feature spec | Field Dashboard agent |
| 11 | `ADMIN_PANEL_SPEC.md` | Full Admin Panel feature spec | Admin Panel agent |
| 12 | `LEAFLET_MAP_SPEC.md` | Leaflet heatmap integration spec | Map feature agent |
| 13 | `D3_GRAPH_SPEC.md` | D3 force-directed money-trail graph spec | Graph feature agent |
| 14 | `LLM_AGENT_SPEC.md` | Natural-language agent interface spec | LLM feature agent |
| 15 | `MONOREPO_STRUCTURE.md` | Repo tree + workspace config + build setup | Repo setup agent |
| 16 | `ENV.md` | Environment variables — all apps + backend | DevOps + all agents |
| 17 | `DEVOPS.md` | Docker, Compose, K8s manifests, services | DevOps agent |
| 18 | `CICD.md` | Jenkins + GitHub Actions pipeline spec | CI/CD agent |
| 19 | `MONITORING.md` | Prometheus + Grafana + ELK config spec | Observability agent |
| 20 | `KPIS.md` | Performance, accessibility, UX targets | QA + all agents |
| 21 | `TEAM_SYNC.md` | Inter-member coordination matrix | All agents |
| 22 | `TEN_DAY_PLAN.md` | 10-day delivery schedule + gates | Planning agent |
| 23 | `DEMO_PLAN.md` | 5-minute demo script + judge prep | Demo/presentation agent |

---

## Conventions for Agents

- **API base URL:** all REST calls go to `VITE_API_BASE` (prod: same origin `/api`).
- **WebSocket URL:** `VITE_WS_URL` (prod: same origin `/ws`).
- **Token storage:** `localStorage` keys `access` (JWT access) and `refresh` (refresh token).
- **State management:** Redux Toolkit — slices named `auth`, `alerts`, `complaints`, `actions`.
- **Styling:** Tailwind CSS utilities + `@sih/ui` components; CSS custom properties from `DESIGN_SYSTEM.md`.
- **TypeScript:** strict mode — no `any`, no `as` casts without `// SAFETY` comment.
- **Route paths:** `/command`, `/field`, `/admin` (via nginx gateway on port 80).
- **Ports (dev):** Admin `3001`, Field `3002`, Command `3003`, Backend `8000`.
- **Ports (prod):** All through nginx gateway on `80`.
- **Ports (infra):** Neo4j `7687`, Postgres `5432`, Redis `6379`, ML server `8080`, Blockchain `7050`.

---

## Dependency Graph

```
ARCHITECTURE.md
├── API_CONTRACTS.md
│   ├── WS_EVENTS.md
│   └── AUTH_AND_RBAC.md
├── DESIGN_SYSTEM.md
│   ├── COMPONENT_SPEC.md
│   └── UI_KIT_API.md
├── COMMAND_CENTER_SPEC.md
│   ├── LEAFLET_MAP_SPEC.md
│   ├── D3_GRAPH_SPEC.md
│   └── LLM_AGENT_SPEC.md
├── FIELD_DASHBOARD_SPEC.md
├── ADMIN_PANEL_SPEC.md
├── MONOREPO_STRUCTURE.md
│   └── ENV.md
├── DEVOPS.md
│   ├── CICD.md
│   └── MONITORING.md
├── KPIS.md
├── TEAM_SYNC.md
├── TEN_DAY_PLAN.md
└── DEMO_PLAN.md
```

**Read order for a new agent joining this project:**
1. `README.md` (this file)
2. `ARCHITECTURE.md`
3. The specific spec for your area
4. `API_CONTRACTS.md` + `WS_EVENTS.md`
5. `DESIGN_SYSTEM.md` + `COMPONENT_SPEC.md`
6. `ENV.md` + `DEVOPS.md`

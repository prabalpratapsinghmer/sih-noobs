# MEMBER 3 — Frontend & DevOps Lead Reference

## 1. Role Overview
- Member 3 owns ALL frontend applications (police-facing), the shared design system, and all DevOps/infrastructure.
- Does NOT build the Victim Portal (that's Member 4), but provides the shared UI kit that Member 4 consumes.
- Title: Frontend & DevOps Lead

## 2. Core Responsibilities
| Component | Description |
|-----------|-------------|
| Monorepo Architecture | React 19 monorepo containing apps: command-center, field-dashboard, admin-panel |
| Shared UI Kit | `@sih/ui-kit` package for standard UI components across all apps |
| Design System | Tailwind CSS based design system using CSS variables |
| Heatmap Integration | Leaflet.js heatmap for visualizing high-risk ATMs |
| Money Trail Graph | `vis-network` implementation for mapping mule networks |
| LLM Agent Interface | Frontend chat UI for interacting with the AI agent |
| State Management | Redux Toolkit for global state, especially alerts and auth |
| Real-time Integration | WebSocket client configuration for live alert feeds |
| Containerization | Docker and Docker Compose setup for the full stack |
| Orchestration | Kubernetes cluster configuration |
| CI/CD & Automation | Build pipelines and deployment scripts |
| Monitoring | Prometheus and Grafana for system health and metrics |
| Gateway | Nginx ingress and routing |

## 3. Technology Stack
### Frontend
- **Framework:** React 19, TypeScript, Vite 8
- **Styling:** Tailwind CSS 3.4.17 (v3 is mandatory to support ui-kit dependencies)
- **State & Data Fetching:** Redux Toolkit, Axios
- **Real-time:** Socket.io-client
- **Maps:** Leaflet 1.9, leaflet.heat, react-leaflet-cluster
- **Graphs:** vis-network, vis-data
- **Icons:** lucide-react
- **Routing:** React Router DOM

### Infrastructure
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes
- **Gateway & Proxy:** Nginx
- **Monitoring:** Prometheus, Grafana
- **Security:** Let's Encrypt (cert-manager)

## 4. What Has Been Built (Current Status)

### 4.1 Shared UI Kit (`packages/ui-kit/`) — COMPLETE
- `package.json` — `@sih/ui-kit` package definition, deps: clsx, tailwind-merge, lucide-react
- `tsconfig.json` — TypeScript strict config
- `tailwind.config.ts` — Color palette using CSS variables (--bg, --surface, --ink, --line, --accent, --good, --warn, --crit), typography (IBM Plex Sans, IBM Plex Mono)
- `src/styles/tokens.css` — Master CSS design tokens with light mode, auto OS dark mode (prefers-color-scheme), manual override (`[data-theme="dark"]`)
- `src/components/Button.tsx` — Variants: default, destructive, outline, ghost, link; Sizes: default, sm, lg, icon
- `src/components/Card.tsx` — Card, CardHeader, CardTitle, CardContent
- `src/components/Badge.tsx` — Variants: default, good, warn, crit
- `src/lib/utils.ts` — `cn()` helper (clsx + tailwind-merge)
- `src/lib/api.ts` — Axios instance with VITE_API_BASE, JWT request interceptor, 401 logout interceptor
- `src/hooks/useWebSocket.ts` — Socket.IO hook: connects to VITE_WS_URL with JWT auth, listens for NEW_ALERT, dispatches to Redux
- `src/store/slices/authSlice.ts` — JWT token management, setCredentials, logout
- `src/store/slices/alertsSlice.ts` — Active alerts list, unread count, addAlert, markAsRead, clearAll
- `src/index.ts` — Barrel exports

### 4.2 Command Center (`apps/command-center/`) — PARTIAL (Active Development)
- `src/App.tsx` — Routes: `/` (Dashboard), `/map` (WIP), `/alerts` (WIP), `/settings` (WIP)
- `src/components/layout/AppLayout.tsx` — Flex layout: Sidebar + Topbar + Outlet
- `src/components/layout/Sidebar.tsx` — Navigation with active route highlights, CHOCO branding, system online pulse
- `src/components/layout/Topbar.tsx` — Search palette (⌘K), alert bell counter, officer profile (Insp. Singh, Indiranagar PS)
- `src/pages/Dashboard.tsx` — Grid layout: Live Threat Heatmap (2/3) + Money Trail Analysis (1/3), Export Report + Universal Freeze buttons
- `src/components/map/LiveMap.tsx` — React Leaflet, Bengaluru center [12.95, 77.61], leaflet.heat gradient, marker clustering, 4 mock ATMs with popup risk scores
- `src/components/graph/MoneyTrailGraph.tsx` — vis-network: Victim→Mule→ATM nodes, ForceAtlas2 physics, CSS variable colors

### 4.3 Field Dashboard (`apps/field-dashboard/`) — PARTIAL (Active Development)
- `src/App.tsx` — Routes: `/` (redirects to `/alerts`), `/alerts` (AlertFeed), `/profile` (WIP)
- `src/components/layout/WebLayout.tsx` — Desktop sidebar with constable profile
- `src/components/layout/MobileLayout.tsx` — Mobile bottom nav (Home, Alerts, Profile)
- `src/pages/AlertFeed.tsx` — Responsive grid of patrol assignment cards with risk badges, Navigate + Intercept buttons

### 4.4 Admin Panel (`apps/admin-panel/`) — STUB (Vite boilerplate only)

### 4.5 Victim Portal (`apps/victim-portal/`) — STUB (Member 4's responsibility, but scaffolded in monorepo)

### 4.6 Standalone SPAs (COMPLETE — fully functional without build step)
- `police-command/` — Complete investigator SPA: 6 views (Dashboard, Heatmap, Graph, LLM Agent, Alerts, Cases), dark/light mode, Leaflet maps with 12 Bengaluru ATMs, vis-network graph, client-side LLM knowledge base, action modals, case management
  - `police-command/index.html` + `css/style.css` + `js/main.js` (679 lines) + `js/heatmap.js` (562 lines) + `js/graph.js` (665 lines) + `js/llm.js` (404 lines)
- `police-field/` — Complete mobile-first field officer PWA: 5 tabs (Home, Alerts, Map, Chat, Profile), Leaflet patrol map, team chat simulator, verification workflow
  - `police-field/index.html` + `style/style.css` + `js/main.js` (788 lines)

### 4.7 Infrastructure — COMPLETE
- Root `Dockerfile` — Multi-stage FastAPI backend container
- Root `docker-compose.yml` — Full stack: backend, postgres, neo4j, redis, prometheus, grafana, celery-worker
- `deployments/Dockerfile.backend` — Production FastAPI container
- `deployments/docker/Dockerfile` — CPU prediction API
- `deployments/docker/Dockerfile.gpu` — CUDA 11.8 GPU container
- `deployments/docker-compose.yml` — Extended stack with banking-mock, mlflow, streamlit dashboard
- `deployments/kubernetes/deployment.yaml` — 3 replicas, rolling updates, resource limits, PVC mounts, pod anti-affinity
- `deployments/kubernetes/service.yaml` — ClusterIP services
- `deployments/kubernetes/configmap.yaml` — DB hosts, ports, URIs
- `deployments/kubernetes/hpa.yaml` — HPA: 2-10 replicas, 70% CPU / 80% memory
- `deployments/kubernetes/ingress.yaml` — Nginx ingress, Let's Encrypt TLS, rate limiting, domain: api.sih26184.gov.in
- `deployments/monitoring/prometheus/prometheus.yml` — Scrapes /metrics every 15s
- `deployments/monitoring/grafana/` — Auto-provisioned datasources and pre-built dashboards

### 4.8 Documentation (`member-3-artifacts/`) — COMPLETE (26 files)
1. `01-Frontend-Architecture.md`
2. `02-UI-Kit-API.md`
3. `03-Design-Tokens.md`
4. `04-State-Management.md`
5. `05-WebSocket-Integration.md`
6. `06-Map-Implementation.md`
7. `07-Graph-Implementation.md`
8. `08-Command-Center-Routes.md`
9. `09-Field-Dashboard-Layouts.md`
10. `10-Admin-Panel-Spec.md`
11. `11-Standalone-Command-App.md`
12. `12-Standalone-Field-App.md`
13. `13-Docker-Stack.md`
14. `14-Kubernetes-Deployment.md`
15. `15-CI-CD-Pipelines.md`
16. `16-Monitoring-Stack.md`
17. `17-Nginx-Gateway.md`
18. `18-Security-Config.md`
19. `19-GPU-Containerization.md`
20. `20-Frontend-Performance.md`
21. `21-Mock-Data-Generation.md`
22. `22-Testing-Strategy.md`
23. `23-Dependency-Management.md`
24. `24-Deployment-Checklist.md`
25. `25-Troubleshooting-Guide.md`
26. `26-Member-Integration.md`

### 4.9 Global Documentation (`docs/`) — COMPLETE (16 files)
- API.md, api-contracts.md, DEPLOYMENT.md, DR_PLAN.md, JUDGE_PREP.md, demo-script.md, MODEL_ARCHITECTURE.md, MONITORING.md, SECURITY.md, architecture-diagram.md, data-synthesis-strategy.md, database-schema.md, edge-cases.md, postgresql_schema.md, neo4j_schema.md, postman_collection.json

## 5. Monorepo Configuration
- Root `package.json`: pnpm workspace, scripts (dev, build, lint, typecheck), shared deps, pnpm overrides forcing React 19.2.8
- `pnpm-workspace.yaml`: packages: `['apps/*', 'packages/*']`
- Tailwind CSS is pinned to v3.4.17 (NOT v4 — v4 breaks shadcn/ui)
- Each app imports `@sih/ui-kit` via `workspace:*` protocol

## 6. Design System Tokens
CSS custom properties from `tokens.css`:

### Light Mode
- `--bg`: background color
- `--surface`: primary surface
- `--surface-2`: secondary surface
- `--ink`: primary text color
- `--muted`: muted text color
- `--line`: primary borders
- `--line-2`: secondary borders
- `--accent`: primary brand color
- `--accent-soft`: lighter brand color
- `--good`: success color
- `--good-soft`: light success color
- `--warn`: warning color
- `--warn-soft`: light warning color
- `--crit`: critical/error color
- `--crit-soft`: light critical/error color

### Dark Mode (via `prefers-color-scheme: dark` or `[data-theme="dark"]`)
- Inverted palette using darker backgrounds and lighter text colors for the same variable names.

### Typography
- **Body:** IBM Plex Sans
- **Code/Monospace:** IBM Plex Mono

## 7. Integration Points With Other Members

### 7.1 With Member 1 (AI/ML Lead)
- Command Center Heatmap consumes ATM risk data from ML predictions
- Command Center Graph visualizes Neo4j mule network data
- Field Dashboard receives real-time NEW_ALERT events when ML model flags high-risk ATMs
- Streamlit dashboard (`dashboard/streamlit_dashboard.py`) visualizes Member 1's training curves
- GPU Docker container (`deployments/docker/Dockerfile.gpu`) runs Member 1's models

### 7.2 With Member 2 (Backend & Database)
- All React apps consume Member 2's REST API via Axios (`api.ts`)
- WebSocket hook connects to Member 2's WebSocket server
- Redux `alertsSlice` receives events from Member 2's WebSocket
- Docker infrastructure runs Member 2's FastAPI, PostgreSQL, Neo4j, Redis, Celery
- API Base: `VITE_API_BASE` → `http://localhost:8000/api/v1`
- WS URL: `VITE_WS_URL` → `ws://localhost:8000`
- Dev ports: Command Center 3003, Field 3002, Admin 3001

### 7.3 With Member 4 (Victim Portal / Integration)
- Member 4 consumes `@sih/ui-kit` (the shared component library)
- Member 4's `victim-portal` app lives in `apps/victim-portal/` within the monorepo
- The ui-kit public API (`index.ts` exports + prop signatures) is the contract between Member 3 and Member 4
- Do NOT break the ui-kit API without versioning and notifying Member 4
- Member 4 also has a standalone version at `victim-dashboard/`

## 8. File Structure Member 3 Owns
```text
/
├── apps/
│   ├── admin-panel/        # Stub
│   ├── command-center/     # Police HQ dashboard
│   ├── field-dashboard/    # Mobile responder app
│   └── victim-portal/      # (Scaffolded only, built by M4)
├── packages/
│   └── ui-kit/             # Shared component library
├── police-command/         # Standalone SPA - complete
├── police-field/           # Standalone SPA - complete
├── deployments/            # Docker, K8s, Prometheus, Grafana configs
├── member-3-artifacts/     # M3 specific documentation
├── docs/                   # Global project documentation
├── package.json            # Root workspace config
├── pnpm-workspace.yaml     # pnpm settings
├── docker-compose.yml      # Root stack
└── Dockerfile              # Root container config
```
*(Note: `infra/` is an empty placeholder directory; real infrastructure files are in `deployments/`)*

## 9. Dev Ports
| App/Service | Port |
|-------------|------|
| Command Center | 3003 |
| Field Dashboard | 3002 |
| Admin Panel | 3001 |
| Victim Portal (M4) | 3000 |
| Backend API | 8000 |
| Banking Mock | 8001 |
| Neo4j HTTP | 7474 |
| Neo4j Bolt | 7687 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| MLflow | 5000 |
| Prometheus | 9090 |
| Grafana | 9091 |
| Streamlit | 8501 |
| TensorBoard | 6006 |

## 10. Commands to Run
```bash
# Install dependencies
pnpm install

# Start all frontend apps
pnpm dev

# Start individual apps
pnpm --filter ./apps/command-center dev
pnpm --filter ./apps/field-dashboard dev

# Build all
pnpm build

# Typecheck
pnpm typecheck

# Start full Docker stack
docker-compose up -d

# Start K8s
kubectl apply -f deployments/kubernetes/

# Open standalone apps (no build needed)
# Just open police-command/index.html or police-field/index.html in browser
```

## 11. What's Remaining / TODO
- **Admin Panel:** Currently Vite stub — needs full implementation (user management, station assignments, model deployment controls)
- **Command Center:** `/map`, `/alerts`, `/settings` routes are WIP
- **Command Center:** LLM Agent chat interface not yet built
- **Field Dashboard:** Profile page is WIP
- **Field Dashboard:** WebSocket live alert binding not yet connected
- **CSS tokens import path issue:** `tokens.css` import in `main.tsx` needs correct relative path (apps are 3 levels deep from packages)
- **React version:** ensure ALL packages use React 19.2.8 (`pnpm` overrides in root `package.json`)

## 12. Important Notes
- Tailwind CSS is **v3.4.17** — **DO NOT upgrade to v4** (breaks PostCSS integration and shadcn/ui)
- The `index.html` at project root is a landing portal that links to standalone apps (NOT a React app)
- Standalone SPAs (`police-command/`, `police-field/`, `victim-dashboard/`) work by just opening in browser — no build step needed
- The monorepo React apps (`apps/*`) are the "modern" versions being actively developed
- `infra/` directory is EMPTY placeholder — real infrastructure is in `deployments/`

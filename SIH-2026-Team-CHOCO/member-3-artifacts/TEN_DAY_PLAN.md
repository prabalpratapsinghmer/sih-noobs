# 10-Day Delivery Plan — Member 3

> Web-only scope. No WhatsApp bot, no mobile apps. Stable project first.
> Exit criteria per day are non-negotiable — if not met, carry over to next morning.

---

## Day 1: Setup & Planning

**Focus:** Foundations, repo, contracts.

| Task | Deliverable |
|------|-------------|
| Initialize monorepo with workspaces | `package.json` root + 4 app folders + `packages/ui-kit` |
| Set up TypeScript (strict) + Vite + ESLint | `tsconfig.base.json`, each app compiles |
| Set up Tailwind CSS + token CSS | `tokens.css` + `tailwind.preset.ts` in ui-kit |
| Scaffold all 4 React apps | Each has `main.tsx`, `App.tsx`, routes, runs on correct port |
| Set up `.env.example` | All env vars committed |
| Set up Git repo + branch strategy | `main` + feature branches |
| Write API contracts with M2 | `docs/API-CONTRACTS.md` v1 agreed |
| Set up project tracking | GitHub Projects board with columns |

**Exit criteria:** `npm run dev` starts all 3 apps; TypeScript compiles cleanly; contracts doc committed.

---

## Day 2: Design System + Auth

**Focus:** `@sih/ui` package + authentication flow.

| Task | Deliverable |
|------|-------------|
| Build `@sih/ui` components (Button, Card, Input, Badge, RiskPill, Modal, Toast, Spinner, EmptyState) | 9 components, tested, exported |
| Build `@sih/ui` hooks (useAuth, useSocket, useTheme, useDebounce, useMediaQuery) | 5 hooks working |
| Build `@sih/ui` lib (http client, ws client, format utils, validators, constants) | Shared infra ready |
| Implement auth flow in all apps | Login page, token storage, route guards, logout |
| Build Topbar + Sidebar + BottomNav layout shells | Each app has a working shell |
| Build CommandPalette (⌘K) | Opens on ⌘K, searches, dispatches actions |

**Exit criteria:** Login/logout works in all 3 apps; shared components render in all 3; Member 4 can import `@sih/ui`.

---

## Day 3: Admin Panel

**Focus:** Complete Admin Panel with all views.

| Task | Deliverable |
|------|-------------|
| Build Overview dashboard (stat tiles + charts) | 5 KPI tiles + complaint volume chart |
| Build User Management (list + CRUD form) | Table, form, confirm modal |
| Build System Health dashboard | Service cards with gauges, 30s polling |
| Build Audit Log viewer | Searchable/filterable table with pagination |
| Wire to M2's admin endpoints (or mock) | Data flows correctly |

**Exit criteria:** Admin Panel fully functional with mock data; Lighthouse ≥ 90.

---

## Day 4: Field Dashboard

**Focus:** Complete Field Dashboard, mobile-first.

| Task | Deliverable |
|------|-------------|
| Build AlertList + AlertCard components | Priority-sorted, risk-colored cards |
| Build AlertDetail view | Full context + action buttons |
| Build DispatchView | Timer, status buttons, GPS |
| Build HistoryView | Past actions list |
| Build ProfileView | Officer info + settings |
| Implement offline queue | localStorage queue + flush on reconnect |
| Add service worker | Cache shell + current alerts |
| Implement GPS tracking | useGeolocation hook + distance/ETA calc |

**Exit criteria:** Field Dashboard works on mobile viewport; offline queue tested; alert → dispatch → verify flow works.

---

## Day 5: Command Center — Map

**Focus:** Leaflet heatmap with all controls.

| Task | Deliverable |
|------|-------------|
| Set up Leaflet + OSM tiles | Map renders in Command Center |
| Build AtmMarker component | Circle markers colored by risk |
| Build HeatmapLayer | Heat overlay weighted by risk_score |
| Build marker clustering | 500+ markers without lag |
| Build AtmPopup | Risk, complaints, mules, actions |
| Build MapFilters | Time, area, fraud type, min-risk slider |
| Implement WS live updates | New predictions appear within 2s |
| Wire to M2's `/api/atms` endpoint | Data flows correctly |

**Exit criteria:** Map shows 500+ ATM markers; filters work; WS updates appear live; clustering smooth.

---

## Day 6: Command Center — Graph + LLM

**Focus:** D3 graph + LLM agent chat.

| Task | Deliverable |
|------|-------------|
| Build MoneyGraph (D3 force-directed) | Nodes + edges render with correct encoding |
| Build NodePanel | Side panel with details + actions on selection |
| Build GraphLegend | Type/edge legend |
| Build ChatThread | Message bubbles + streaming text |
| Build QuickPrompts | Common query chips |
| Build ResultRenderer | Text, table, chart, graph rendering |
| Build QueryBuilder | Visual form-based alternative |
| Implement chat persistence | localStorage per user |

**Exit criteria:** Graph renders 100+ nodes; LLM agent sends queries and renders results; both work with mock data.

---

## Day 7: Command Center — Actions + Integration

**Focus:** Action panel + full integration.

| Task | Deliverable |
|------|-------------|
| Build ActionPanel | Trigger Verification, Freeze, FIR, Dispatch buttons |
| Build ConfirmModal for each action | Restates target ID + consequence |
| Build AlertFeed (realtime) | WebSocket-pushed alerts with unread tracking |
| Build DashboardView (overview) | Stat tiles + recent cases + mini alert feed |
| Build CasesList + CaseDetail | Full complaint browsing |
| Implement all keyboard shortcuts | ⌘K, G+M, G+G, etc. |
| Wire WS events to all views | All events from WS_EVENTS.md handled |
| Test full flow: complaint → prediction → action | End-to-end with M2's API |

**Exit criteria:** Full Command Center functional; all WS events render correctly; action flow works with confirmation.

---

## Day 8: Responsive + Polish

**Focus:** Cross-app quality, accessibility, performance.

| Task | Deliverable |
|------|-------------|
| Test all 3 apps at 1100px, 768px, 375px | No layout breaks |
| Keyboard navigation audit | Tab order correct, focus visible everywhere |
| Screen reader audit | Roles, labels, aria-live correct |
| Reduced motion pass | All animations respect prefers-reduced-motion |
| Lighthouse audit all 3 UIs | Score ≥ 90 each |
| Color-blind safety check | Risk not conveyed by color alone |
| Fix all bugs found | Zero known P1/P2 bugs |
| Cross-browser test | Chrome, Firefox, Edge, Safari |

**Exit criteria:** Lighthouse ≥ 90 all UIs; zero P1 bugs; responsive to 375px; keyboard navigable.

---

## Day 9: DevOps Cut-Over

**Focus:** Full infrastructure stack.

| Task | Deliverable |
|------|-------------|
| Write Dockerfiles for all 4 frontend services | Each builds + runs independently |
| Write nginx gateway config | Path routing works for all services |
| Test docker-compose up | All 11 containers start in < 2 min |
| Write K8s manifests | Deployments, services, ingress, HPA |
| Set up Minikube | Cluster runs, manifests apply |
| Set up Jenkins pipeline | Stages work end-to-end |
| Set up GitHub Actions | Backup CI pipeline works |
| Set up Prometheus + Grafana | Metrics scraped, dashboards load |
| Set up ELK stack | Logs searchable in Kibana |
| Seed demo data | Realistic sample complaints, predictions, mules |

**Exit criteria:** `docker compose up` works; Minikube deploys; Jenkins pipeline runs; Grafana dashboards show data.

---

## Day 10: Test, Polish, Demo Prep

**Focus:** Final quality + presentation readiness.

| Task | Deliverable |
|------|-------------|
| End-to-end Playwright test | Decisive flow: complaint → prediction → action → resolution |
| Full stack test with real APIs | No mock data needed |
| Performance test | Lighthouse ≥ 90, load test passes |
| Prepare demo script | Timed 5-minute walkthrough |
| Prepare presentation slides | Key talking points |
| Record demo video | Backup in case of failure |
| Final team sync | Everyone aligned on demo flow |
| Dry run | Full rehearsal with timing |
| Fix last-minute issues | Whatever breaks, fix it |

**Exit criteria:** Demo script memorized; backup video recorded; all services running; team confident.

---

## Contingency

If any day's exit criteria aren't met:
1. Carry over to next morning (before that day's tasks).
2. If 2+ days behind, cut scope: Admin Panel简化 (basic tables, no charts), Field Dashboard drop History view.
3. Never cut: Map, Graph, LLM Agent, Auth, DevOps — these are the demo.

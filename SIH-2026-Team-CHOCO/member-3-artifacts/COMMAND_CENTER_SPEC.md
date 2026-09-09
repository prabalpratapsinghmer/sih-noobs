# Command Center — Full Feature Specification

> App: `apps/frontend-command` · Port 3003 (dev) · Route `/command` (prod)
> Audience: Cybercrime Inspectors · Theme: Dark · Form factor: Desktop
> See `LEAFLET_MAP_SPEC.md`, `D3_GRAPH_SPEC.md`, `LLM_AGENT_SPEC.md` for deep dives on map/graph/LLM.

---

## 1. Overview

The Command Center is an information-dense, action-oriented dashboard for inspectors managing 12+ cybercrime cases simultaneously. Dark theme to reduce eye strain during long shifts. Everything is findable, not hunted.

**Core value:** See the full picture → ask questions in plain English → take verified actions — all in one screen.

---

## 2. Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  TOPBAR: logo · station · clock · connection dot · user dropdown │
├────────────┬─────────────────────────────────────────────────────┤
│            │                                                     │
│  SIDEBAR   │  MAIN CONTENT AREA (route-dependent)               │
│            │                                                     │
│  Dashboard │  ┌─── Tabs or view switcher ──────────────────┐   │
│  Map       │  │                                             │   │
│  Graph     │  │  [ active view content ]                    │   │
│  LLM Agent │  │                                             │   │
│  Cases     │  │                                             │   │
│  Alerts    │  └─────────────────────────────────────────────┘   │
│  ─────     │                                                     │
│  Admin*    │  RIGHT PANEL (context-dependent, slide-in)         │
│  (if admin)│  - Node detail (graph selected)                    │
│            │  - Alert detail (feed selected)                    │
│            │  - Action confirm modal                             │
│            │                                                     │
├────────────┴─────────────────────────────────────────────────────┤
│  STATUS BAR: connection · active alerts count · last update time │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Views

### 3.1 Dashboard (default)

**Purpose:** Per-station overview — what needs attention right now.

**Components:**
- **Big-number tiles:** Active cases (count), High-risk ATMs (count), Alerts today (count), Avg resolution time (hours).
- **Recent cases table:** Last 10 complaints with status, risk, time.
- **Active alerts mini-feed:** Last 5 alerts with priority badges.
- **Quick actions:** "New Case" (opens complaint form), "View All Cases", "Open Map".

**Data:** `GET /api/complaints?status=in_analysis&limit=10` + `GET /api/atms?min_risk=70&limit=5`.

### 3.2 Map (Leaflet Heatmap)

**Purpose:** See all high-risk ATMs geographically, interact with predictions.

**Spec:** See `LEAFLET_MAP_SPEC.md` for full implementation details.

**Quick summary:**
- Leaflet.js with OpenStreetMap tiles.
- Circle markers colored by risk (crit/warn/info).
- Heatmap overlay weighted by `risk_score`.
- Clustering for 500+ markers (Leaflet.markercluster).
- Click marker → `AtmPopup` (risk, complaints, mules, actions).
- Filters: time range, fraud type, min-risk slider, area dropdown.
- WebSocket live updates: new predictions appear within 2s.

### 3.3 Graph (D3 Money Trail)

**Purpose:** Visualize the money trail for a specific complaint.

**Spec:** See `D3_GRAPH_SPEC.md` for full implementation details.

**Quick summary:**
- D3.js force-directed graph.
- Nodes: victim (blue), mule (red, ring width = score), ATM (green), upi/phone/bank (gray).
- Edges: labeled with relationship type and amount.
- Click node → side panel with details + action buttons.
- Select complaint from dropdown → fetch graph from `GET /api/mules/{complaint_id}/graph`.

### 3.4 LLM Agent (Natural Language Query)

**Purpose:** Let inspectors query the graph database in plain English.

**Spec:** See `LLM_AGENT_SPEC.md` for full implementation details.

**Quick summary:**
- Chat interface with message thread.
- User types question → backend converts to Cypher → executes → returns result.
- Result rendered as text, table, chart, or graph.
- Quick prompt chips for common queries.
- Structured query builder as visual alternative.

### 3.5 Cases (Complaint List & Detail)

**Purpose:** Browse, filter, and drill into individual complaints.

**List view:**
- DataTable with columns: ID, victim (masked), fraud type, amount, status, risk score, created, actions.
- Filters: status, fraud type, date range, search.
- Sort by any column.
- Pagination.

**Detail view (`/command/cases/:id`):**
- Complaint info card (victim masked, fraudster, amount, status).
- `StatusTimeline` component (visual timeline with blockchain tx hashes).
- Connected predictions (top-3 ATMs with probability).
- Connected mules (list with risk scores).
- Evidence list (file type, hash, IPFS CID, verify button).
- Action history (what's been done, status, tx hash).
- Action buttons: Trigger Verification, Request Freeze, Generate FIR, Dispatch Patrol.

### 3.6 Alerts (Realtime Feed)

**Purpose:** See all incoming alerts in one place with unread tracking.

**Components:**
- Alert list (sorted by time, newest first).
- Each alert: priority stripe, ATM name, risk score, time, complaint link.
- Unread count badge on sidebar nav item.
- Mark read on click, "Mark all read" button.
- WebSocket-driven: new alerts appear at the top with a highlight animation.

---

## 4. Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `G then M` | Go to Map |
| `G then G` | Go to Graph |
| `G then C` | Go to Cases |
| `G then A` | Go to Alerts |
| `⌘K` / `Ctrl+K` | Open Command Palette |
| `A` | Open action panel (if case selected) |
| `T` | Quick "Trigger Verification" (with confirm modal) |
| `1 / 2 / 3` | Cycle unread alerts by priority |
| `Esc` | Close modal / deselect |
| `/` | Focus search (in Cases view) |

**Implementation:** Global keydown listener on the layout shell. Use `react-hotkeys-hook` or a custom hook. Don't capture keys when an input is focused.

---

## 5. Realtime Behavior

- WebSocket connection established on app mount (via `useSocket` hook).
- Connection status shown in topbar: green dot = connected, amber = reconnecting, red = disconnected.
- Events handled (see `WS_EVENTS.md` §11 for the full list):
  - `complaint.created` → toast + case list update
  - `prediction.new` → heatmap update + toast
  - `atm.risk_changed` → heatmap marker update
  - `alert.push` → alert feed update + toast
  - `action.triggered` / `action.completed` / `action.failed` → case detail update + toast
  - `graph.updated` → graph nodes/edges append
  - `status.updated` → case timeline update

---

## 6. Redux Store Shape

```typescript
{
  auth: {
    user: User | null;
    token: string | null;
    refreshToken: string | null;
  },
  complaints: {
    items: Complaint[];
    total: number;
    page: number;
    selected: Complaint | null;
    loading: boolean;
  },
  map: {
    atms: AtmRisk[];
    filters: { minRisk: number; area: string; fraudType: string; since: string };
    loading: boolean;
  },
  graph: {
    complaintId: string | null;
    nodes: GraphNode[];
    edges: GraphEdge[];
    selectedNode: GraphNode | null;
    loading: boolean;
  },
  llm: {
    messages: ChatMessage[];
    loading: boolean;
    templates: string[];
  },
  alerts: {
    items: AlertEvent[];
    unreadCount: number;
    lastUpdate: string;
  },
  actions: {
    history: Action[];
    pendingConfirm: { type: string; params: Record<string, unknown> } | null;
  },
  connection: {
    status: 'connected' | 'reconnecting' | 'disconnected';
  }
}
```

---

## 7. File Structure

```
apps/frontend-command/
├── src/
│   ├── main.tsx
│   ├── app/
│   │   ├── routes.tsx
│   │   ├── providers.tsx
│   │   └── layout/
│   │       ├── CommandLayout.tsx       # shell: topbar + sidebar + content
│   │       ├── Topbar.tsx
│   │       ├── Sidebar.tsx
│   │       └── CommandPalette.tsx
│   ├── features/
│   │   ├── dashboard/
│   │   │   ├── DashboardView.tsx
│   │   │   ├── StatTiles.tsx
│   │   │   ├── RecentCases.tsx
│   │   │   └── AlertMiniFeed.tsx
│   │   ├── map/
│   │   │   ├── MapView.tsx
│   │   │   ├── MapProvider.tsx
│   │   │   ├── HeatmapLayer.tsx
│   │   │   ├── AtmMarker.tsx
│   │   │   ├── AtmPopup.tsx
│   │   │   └── filters/
│   │   │       ├── MapFilters.tsx
│   │   │       ├── TimeRangeSlider.tsx
│   │   │       ├── AreaDropdown.tsx
│   │   │       └── FraudTypeFilter.tsx
│   │   ├── graph/
│   │   │   ├── GraphView.tsx
│   │   │   ├── MoneyGraph.tsx
│   │   │   ├── useGraphLayout.ts
│   │   │   ├── NodePanel.tsx
│   │   │   └── GraphLegend.tsx
│   │   ├── llm-agent/
│   │   │   ├── LlmAgentView.tsx
│   │   │   ├── ChatThread.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── QuickPrompts.tsx
│   │   │   ├── QueryBuilder.tsx
│   │   │   └── ResultRenderer.tsx
│   │   ├── actions/
│   │   │   ├── ActionPanel.tsx
│   │   │   ├── ConfirmModal.tsx
│   │   │   └── ActionHistory.tsx
│   │   ├── alerts/
│   │   │   ├── AlertFeed.tsx
│   │   │   ├── AlertItem.tsx
│   │   │   └── useAlerts.ts
│   │   └── cases/
│   │       ├── CaseList.tsx
│   │       ├── CaseDetail.tsx
│   │       ├── ComplaintInfoCard.tsx
│   │       ├── EvidenceList.tsx
│   │       └── MuleList.tsx
│   ├── shared/
│   │   ├── api/
│   │   │   ├── client.ts             # re-export of http from @sih/ui
│   │   │   ├── complaints.api.ts
│   │   │   ├── predictions.api.ts
│   │   │   ├── mules.api.ts
│   │   │   ├── actions.api.ts
│   │   │   └── admin.api.ts
│   │   ├── ws/
│   │   │   ├── socket.ts             # re-export of wsClient from @sih/ui
│   │   │   └── events.ts             # event type definitions
│   │   └── mock/
│   │       ├── complaints.json
│   │       ├── predictions.json
│   │       ├── graph.json
│   │       └── alerts.json
│   ├── store/
│   │   ├── store.ts
│   │   ├── authSlice.ts
│   │   ├── complaintsSlice.ts
│   │   ├── mapSlice.ts
│   │   ├── graphSlice.ts
│   │   ├── llmSlice.ts
│   │   ├── alertsSlice.ts
│   │   ├── actionsSlice.ts
│   │   └── connectionSlice.ts
│   └── styles/
│       └── command.css               # app-level overrides over ui-kit tokens
├── index.html
├── vite.config.ts
├── tailwind.config.ts                # imports from @sih/ui/tailwind.preset
├── tsconfig.json
├── package.json
└── Dockerfile.command
```

---

## 8. Build Commands

```bash
# Dev server (port 3003)
cd apps/frontend-command
npm run dev        # → http://localhost:3003/command

# Build for production
npm run build      # → dist/

# Type check
npm run typecheck  # tsc --noEmit

# Lint
npm run lint       # eslint src/
```

---

## 9. Decisions & Rationale

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Map library | Leaflet.js | No API key needed for demo, good with clustering, swappable |
| Graph library | D3.js force | Full control over force layout, realtime, no vis.js dependency |
| Charts | Recharts | React-native, clean, works in dashboard tiles |
| LLM transport | Streaming text | Show typing effect for better UX (backend sends chunks) |
| WS transport | Native WebSocket | No socket.io dependency; wrapper handles reconnect |
| Sidebar | Fixed, collapsible | Always visible on desktop; collapsed on smaller screens |
| Command palette | ⌘K (universal pattern) | Fast power-user access; not required for basic use |

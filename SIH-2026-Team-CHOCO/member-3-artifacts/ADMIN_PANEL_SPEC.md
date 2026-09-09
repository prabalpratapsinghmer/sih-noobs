# Admin Panel — Full Feature Specification

> App: `apps/frontend-admin` · Port 3001 (dev) · Route `/admin` (prod)
> Audience: System / IT Admins · Theme: Light · Form factor: Desktop
> Core areas: User management, system health, ML model metrics, audit log, complaint overview, evidence management.

---

## 1. Overview

The Admin Panel is the operational backbone. It's where admins manage who has access, monitor whether services are healthy, verify that models are performing, and review the audit trail. No creative UI — just operational clarity.

**Core value:** Keep the platform running, the users right, and the record auditable.

---

## 2. Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  TOPBAR: logo · "System Admin" · notifications · user dropdown  │
├────────────┬─────────────────────────────────────────────────────┤
│            │                                                     │
│  SIDEBAR   │  MAIN CONTENT (route-dependent)                    │
│            │                                                     │
│  Overview  │                                                     │
│  Users     │                                                     │
│  Health    │                                                     │
│  Models    │                                                     │
│  Audit     │                                                     │
│  Complaints│                                                     │
│  Evidence  │                                                     │
│            │                                                     │
├────────────┴─────────────────────────────────────────────────────┤
│  STATUS BAR: services healthy · DB connected · last sync         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Views

### 3.1 Overview (dashboard, default)

**Purpose:** At-a-glance platform status.

**Components:**
- **Big-number tiles (KPIs):**
  - Complaints today (count, trend arrow vs yesterday)
  - Active high-risk ATMs (count)
  - Avg resolution time (hours, trend)
  - Model latency p95 (ms)
  - System uptime (%)
- **Complaint volume chart:** Recharts area chart, last 7 days.
- **Status funnel:** Submitted → Analyzing → Action Taken → Resolved (Recharts funnel/bar).
- **Service status row:** 5 services with green/amber/red dots.

### 3.2 Users

**Purpose:** Manage who has access to the platform.

**User list:**
- DataTable: name, username, role, station, status (active/inactive), last login, actions.
- Filters: role, station, status.
- Search: name, username, email.
- Pagination.

**User form (create/edit):**
- Fields: name, username, role (select), station, phone, email, password (create only).
- Validation: Zod schema from `@sih/ui`.
- Confirm modal on delete/deactivate.

**Actions:** Create user, Edit user, Deactivate user, Reset password, Change role.

### 3.3 System Health

**Purpose:** Real-time per-service health monitoring.

**Components:**
- **Service cards:** One per service (Backend, ML Server, Neo4j, Postgres, Redis, Blockchain).
  - Status dot: green (healthy) / amber (degraded) / red (down)
  - CPU gauge (Recharts RadialBarChart)
  - Memory bar (used / total)
  - GPU gauge (ML server only)
  - Disk free space bar
  - Uptime formatted as `Xd Xh Xm`
- **History chart:** Line chart of CPU/memory over time (last 1 hour, refresh every 30s).
- **Alert banner:** If any service is degraded or down, show a persistent warning banner.

**Data:** `GET /api/admin/health` polled every 30s.

### 3.4 Model Metrics

**Purpose:** Track ML model performance over time.

**Components:**
- **Accuracy / Precision / Recall / F1 line chart:** (Recharts LineChart) over time.
- **Latency chart:** p50, p95, p99 latency over time.
- **Predictions made:** Count per day.
- **Model selector:** Switch between Transformer and GNN metrics.
- **Date range picker:** Filter metrics by time period.

**Data:** `GET /api/admin/model-metrics?model=transformer&since=...`

### 3.5 Audit Log

**Purpose:** Immutable record of all actions taken in the system.

**Audit log table:**
- Columns: timestamp, action type, complaint ID, initiated by, status, blockchain tx hash, IP.
- Filters: action type, user, date range, complaint ID.
- Sort: by timestamp (default newest first).
- Search: complaint ID, user name, tx hash.
- Click row → expand details (params, full tx hash, IP).
- "Verify on blockchain" link (if explorer URL configured).

**Data:** `GET /api/admin/audit?filter=...&page=...`

### 3.6 Complaints

**Purpose:** Overview of all complaints with metrics.

**Components:**
- **Summary tiles:** Total complaints, open, in-progress, resolved, closed.
- **Volume chart:** Daily complaint count (Recharts bar chart, last 30 days).
- **Resolution time chart:** Average resolution time trend.
- **Complaint table:** Same as Command Center cases list, but with admin-level access (no PII masking).

### 3.7 Evidence Management

**Purpose:** Access and verify evidence files.

**Components:**
- **Evidence list:** DataTable with complaint ID, file type, file name, hash, IPFS CID, upload date, verified status.
- **Verify button:** Sends hash to backend for verification against blockchain.
- **Verify result:** ✅ "Hash matches blockchain record" or ❌ "Hash mismatch — evidence may be tampered".
- **Filter:** By complaint, file type, verification status.

---

## 4. Charts Specification

All charts use Recharts:

| Chart | Type | Data source | Refresh |
|-------|------|-------------|---------|
| Complaint volume (overview) | AreaChart | `GET /api/admin/complaints/stats` | 5 min |
| Status funnel | BarChart (horizontal) | Same | 5 min |
| CPU history | LineChart | `GET /api/admin/health/history` | 30 s |
| Memory history | LineChart | Same | 30 s |
| Model accuracy | LineChart | `GET /api/admin/model-metrics` | 5 min |
| Model latency | LineChart (3 lines: p50/p95/p99) | Same | 5 min |
| Resolution time trend | LineChart | `GET /api/admin/complaints/stats` | 5 min |

**Chart styling:**
- Grid: `--line` color, dashed.
- Axes: `--muted` text, 10.5px mono.
- Lines: `--accent` for primary, `--good`/`--warn`/`--crit` for semantic.
- Tooltip: `--surface` bg, `--ink` text, `--line` border.
- Legend: inline below chart, `--muted` text.

---

## 5. Redux Store Shape

```typescript
{
  auth: { user: User | null; token: string | null },
  users: {
    items: User[];
    total: number;
    page: number;
    loading: boolean;
    selected: User | null;
  },
  health: {
    services: ServiceHealth[];
    history: HealthSnapshot[];
    loading: boolean;
  },
  models: {
    transformer: ModelMetric[];
    gnn: ModelMetric[];
    loading: boolean;
    selectedModel: 'transformer' | 'gnn';
  },
  audit: {
    items: AuditLogEntry[];
    total: number;
    page: number;
    filters: AuditFilters;
    loading: boolean;
  },
  complaints: {
    items: Complaint[];
    stats: ComplaintStats;
    total: number;
    page: number;
    loading: boolean;
  },
  evidence: {
    items: Evidence[];
    loading: boolean;
  }
}
```

---

## 6. File Structure

```
apps/frontend-admin/
├── src/
│   ├── main.tsx
│   ├── app/
│   │   ├── routes.tsx
│   │   ├── providers.tsx
│   │   └── layout/
│   │       ├── AdminLayout.tsx
│   │       ├── Topbar.tsx
│   │       └── Sidebar.tsx
│   ├── features/
│   │   ├── dashboard/
│   │   │   ├── OverviewView.tsx
│   │   │   ├── StatTiles.tsx
│   │   │   ├── ComplaintVolumeChart.tsx
│   │   │   ├── StatusFunnel.tsx
│   │   │   └── ServiceStatusRow.tsx
│   │   ├── users/
│   │   │   ├── UserListView.tsx
│   │   │   ├── UserTable.tsx
│   │   │   ├── UserForm.tsx
│   │   │   └── UserConfirmModal.tsx
│   │   ├── health/
│   │   │   ├── HealthView.tsx
│   │   │   ├── ServiceCard.tsx
│   │   │   ├── CpuGauge.tsx
│   │   │   ├── MemoryBar.tsx
│   │   │   ├── GpuGauge.tsx
│   │   │   └── HealthHistoryChart.tsx
│   │   ├── models/
│   │   │   ├── ModelMetricsView.tsx
│   │   │   ├── AccuracyChart.tsx
│   │   │   ├── LatencyChart.tsx
│   │   │   └── ModelSelector.tsx
│   │   ├── audit/
│   │   │   ├── AuditLogView.tsx
│   │   │   ├── AuditTable.tsx
│   │   │   ├── AuditFilters.tsx
│   │   │   └── AuditDetail.tsx
│   │   ├── complaints/
│   │   │   ├── ComplaintsOverview.tsx
│   │   │   ├── ComplaintsStats.tsx
│   │   │   └── ComplaintsTable.tsx
│   │   └── evidence/
│   │       ├── EvidenceView.tsx
│   │       ├── EvidenceTable.tsx
│   │       └── VerifyButton.tsx
│   ├── shared/
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── admin.api.ts
│   │   │   └── complaints.api.ts
│   │   └── mock/
│   │       ├── health.json
│   │       ├── metrics.json
│   │       └── audit.json
│   ├── store/
│   │   ├── store.ts
│   │   ├── authSlice.ts
│   │   ├── usersSlice.ts
│   │   ├── healthSlice.ts
│   │   ├── modelsSlice.ts
│   │   ├── auditSlice.ts
│   │   ├── complaintsSlice.ts
│   │   └── evidenceSlice.ts
│   └── styles/
│       └── admin.css
├── index.html
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── Dockerfile.admin
```

---

## 7. Access Control

Admin Panel routes require `role === 'admin'`. Enforced at:
1. Route guard (frontend) — redirect to `/unauthorized` if not admin.
2. Backend API — all `/api/admin/*` endpoints return 403 for non-admin tokens.

---

## 8. Decisions & Rationale

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Charts | Recharts only | Consistent, React-native, no D3 needed for standard charts |
| Health polling | 30s interval | Matches Prometheus scrape; real-time WS not needed |
| Audit log | Server-side pagination | Logs can be millions of rows |
| Evidence verify | Button per row | Explicit action, not auto-verify |
| PII masking | Admin sees unmasked | Admin role = full trust; M2 provides unmasked for admin endpoints |

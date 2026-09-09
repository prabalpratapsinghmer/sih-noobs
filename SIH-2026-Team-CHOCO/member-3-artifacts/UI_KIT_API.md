# Shared UI Kit — `@sih/ui`

> This package is the contract between Member 3 (frontend lead) and Member 4 (Victim Portal).
> Once the public API is agreed, it must not break without a version bump.
> Consumed via: `import { Button, Card, useAuth } from '@sih/ui'`.

---

## 1. Package Structure

```
packages/ui-kit/
├── package.json            # @sih/ui
├── tsconfig.json
├── tailwind.preset.ts      # design tokens → Tailwind theme
├── src/
│   ├── index.ts            # PUBLIC SURFACE — all exports listed here
│   ├── components/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Badge.tsx
│   │   ├── RiskPill.tsx
│   │   ├── StatusTimeline.tsx
│   │   ├── ConfirmModal.tsx
│   │   ├── DataTable.tsx
│   │   ├── Toast.tsx
│   │   ├── Spinner.tsx
│   │   ├── EmptyState.tsx
│   │   ├── AlertCard.tsx
│   │   └── ...
│   ├── primitives/         # Radix-based (re-exported)
│   │   ├── Dialog.tsx
│   │   ├── DropdownMenu.tsx
│   │   ├── Tooltip.tsx
│   │   ├── Tabs.tsx
│   │   ├── Select.tsx
│   │   ├── Switch.tsx
│   │   ├── ScrollArea.tsx
│   │   └── ...
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useSocket.ts
│   │   ├── useTheme.ts
│   │   ├── useAlerts.ts
│   │   ├── useDebounce.ts
│   │   ├── useMediaQuery.ts
│   │   ├── useLocalStorage.ts
│   │   └── useOfflineQueue.ts
│   ├── lib/
│   │   ├── http.ts         # Axios instance + interceptors
│   │   ├── ws-client.ts    # WebSocket wrapper
│   │   ├── format.ts       # date, currency, phone formatting
│   │   ├── validators.ts   # Zod schemas shared with backend
│   │   └── constants.ts    # status values, fraud types, role labels
│   ├── styles/
│   │   ├── tokens.css      # CSS custom properties (see DESIGN_SYSTEM.md)
│   │   └── themes.css      # light/dark/system theme logic
│   ├── icons/
│   │   └── index.tsx       # SVG icon components
│   └── types/
│       ├── auth.ts         # User, Role, AuthState
│       ├── complaint.ts    # Complaint, TimelineEvent, Evidence
│       ├── prediction.ts   # Prediction, AtmRisk
│       ├── mule.ts         # Mule, GraphNode, GraphEdge, MoneyTrail
│       ├── action.ts       # Action, ActionType, ActionStatus
│       ├── alert.ts        # FieldAlert, AlertPriority
│       ├── admin.ts        # ServiceHealth, AuditLog, ModelMetric
│       └── index.ts        # re-exports all types
├── __tests__/              # unit tests for the package
└── README.md               # internal docs for the package
```

---

## 2. Public API (`index.ts`)

```typescript
// ─── Components ───────────────────────────────────────────
export { Button } from './components/Button';
export { Card } from './components/Card';
export { Input } from './components/Input';
export { Badge } from './components/Badge';
export { RiskPill } from './components/RiskPill';
export { StatusTimeline } from './components/StatusTimeline';
export { ConfirmModal } from './components/ConfirmModal';
export { DataTable } from './components/DataTable';
export { Toast, toast } from './components/Toast';
export { Spinner } from './components/Spinner';
export { EmptyState } from './components/EmptyState';
export { AlertCard } from './components/AlertCard';

// ─── Primitives (re-exported from Radix) ─────────────────
export { Dialog, DialogTrigger, DialogContent, DialogTitle, DialogDescription } from './primitives/Dialog';
export { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from './primitives/DropdownMenu';
export { Tooltip, TooltipTrigger, TooltipContent } from './primitives/Tooltip';
export { Tabs, TabsList, TabsTrigger, TabsContent } from './primitives/Tabs';
export { Select, SelectTrigger, SelectContent, SelectItem } from './primitives/Select';
export { Switch } from './primitives/Switch';
export { ScrollArea } from './primitives/ScrollArea';

// ─── Hooks ────────────────────────────────────────────────
export { useAuth } from './hooks/useAuth';
export { useSocket } from './hooks/useSocket';
export { useTheme } from './hooks/useTheme';
export { useAlerts } from './hooks/useAlerts';
export { useDebounce } from './hooks/useDebounce';
export { useMediaQuery } from './hooks/useMediaQuery';
export { useLocalStorage } from './hooks/useLocalStorage';
export { useOfflineQueue } from './hooks/useOfflineQueue';

// ─── Lib ──────────────────────────────────────────────────
export { http } from './lib/http';
export { wsClient } from './lib/ws-client';
export { formatDate, formatCurrency, formatPhone, formatRelativeTime } from './lib/format';
export { complaintSchema, userSchema, actionSchema } from './lib/validators';
export { STATUS_VALUES, FRAUD_TYPES, ROLE_LABELS, ACTION_TYPES } from './lib/constants';

// ─── Types ────────────────────────────────────────────────
export type { User, Role, AuthState } from './types/auth';
export type { Complaint, TimelineEvent, Evidence, ComplaintStatus } from './types/complaint';
export type { Prediction, AtmRisk } from './types/prediction';
export type { Mule, GraphNode, GraphEdge, MoneyTrail } from './types/mule';
export type { Action, ActionType, ActionStatus } from './types/action';
export type { FieldAlert, AlertPriority } from './types/alert';
export type { ServiceHealth, AuditLogEntry, ModelMetric } from './types/admin';
```

---

## 3. Versioning Rules

- Current version: `0.1.0` (pre-release, no API stability guarantees yet).
- When the public API is first agreed with Member 4: bump to `1.0.0`.
- After `1.0.0`:
  - **Patch** (1.0.x): bug fixes, no API changes.
  - **Minor** (1.x.0): new components/hooks added, no existing API changes.
  - **Major** (x.0.0): breaking change to any exported symbol.
- Breaking change requires: (1) update this doc, (2) notify Member 4, (3) bump major.

---

## 4. Peer Dependencies

The consuming app must provide:
- `react` ≥ 18
- `react-dom` ≥ 18
- `redux` + `@reduxjs/toolkit` (for the hooks that dispatch)

---

## 5. Styling Convention

- `@sih/ui` ships **no CSS files** — it provides the Tailwind preset + token CSS.
- Consuming apps import `tokens.css` and `themes.css` in their entry point.
- Components use Tailwind classes referencing the token-based color names (`bg-surface`, `text-ink`, `border-line`, etc.).
- Theme switching is handled by the `useTheme` hook + the CSS custom property system in `DESIGN_SYSTEM.md`.

---

## 6. Build & Publish

- Package manager: npm workspaces (or pnpm).
- Build: `tsup` (TypeScript bundler) outputs ESM + CJS.
- Consuming apps: `workspace:*` protocol in `package.json` for local dev.
- No publishing to npm registry — internal workspace package only.

---

## 7. Acceptance Criteria for `1.0.0`

Before freezing the `@sih/ui` API:

- [ ] All components in §2 exist and pass unit tests.
- [ ] All hooks in §2 work with the Redux store shape.
- [ ] `http` client handles 401 → refresh → retry correctly.
- [ ] `wsClient` handles reconnect with exponential backoff.
- [ ] Token CSS works in both light and dark themes.
- [ ] Member 4 can import and use any component in the Victim Portal without modifications.
- [ ] No `any` types in the public surface.
- [ ] Storybook (optional but recommended) or usage examples for each component.

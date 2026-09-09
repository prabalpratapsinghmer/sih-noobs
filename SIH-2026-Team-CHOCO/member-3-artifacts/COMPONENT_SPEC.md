# Component Specifications

> React component contracts for the shared `@sih/ui` package and app-level components.
> See `UI_KIT_API.md` for the package surface. See `DESIGN_SYSTEM.md` for tokens.

---

## 1. Primitives (shadcn/ui based)

These are unstyled or lightly styled base components from `@sih/ui/primitives`. They handle behavior; the consuming component applies Tailwind + tokens for visuals.

| Component | Source | Notes |
|-----------|--------|-------|
| `Dialog` | Radix Dialog | Modal with focus trap, Escape close |
| `DropdownMenu` | Radix DropdownMenu | Keyboard-navigable menus |
| `Popover` | Radix Popover | Anchored floating panels |
| `Tooltip` | Radix Tooltip | Hover/focus info |
| `Toast` | Radix Toast | Notification stack |
| `Tabs` | Radix Tabs | Tabbed interfaces |
| `Select` | Radix Select | Dropdown selects |
| `Switch` | Radix Switch | Toggle switches |
| `Separator` | Radix Separator | Visual dividers |
| `ScrollArea` | Radix ScrollArea | Styled scrollable regions |

---

## 2. Shared Components (`@sih/ui/components`)

### 2.1 Button

```tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;         // shows spinner, disables interaction
  icon?: React.ReactNode;    // left icon
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}
```

**States:**
- Default: solid fill for primary/secondary, outline for ghost, red for danger.
- Hover: `accent-2` for primary, border color shift for secondary.
- Disabled: 50% opacity, `cursor: not-allowed`.
- Loading: Spinner replaces icon, button disabled.

**Variants by context:**
- Command Center: dark theme, primary = accent.
- Field Dashboard: large (lg) buttons for gloved/touch use.
- Admin Panel: standard sizing.

### 2.2 Card

```tsx
interface CardProps {
  variant?: 'default' | 'elevated' | 'bordered';
  padding?: 'sm' | 'md' | 'lg';
  className?: string;
  children: React.ReactNode;
}
```

- Default: bg `--surface`, border `--line`, radius 10px, shadow.
- Elevated: same + shadow for emphasis (used for priority items).
- Bordered: no shadow, stronger border for structural separation.

### 2.3 Input

```tsx
interface InputProps {
  label: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'search';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  error?: string;            // validation error message
  disabled?: boolean;
  required?: boolean;
  icon?: React.ReactNode;    // left icon
  suffix?: React.ReactNode;  // right suffix (e.g., unit)
}
```

**States:**
- Default: `--surface` bg, `--line` border.
- Focus: `--accent` border, subtle ring.
- Error: `--crit` border, error text below.
- Disabled: `--surface-2` bg, `--muted` text.

### 2.4 Badge / Pill

```tsx
interface BadgeProps {
  variant: 'default' | 'good' | 'warn' | 'crit' | 'accent';
  size?: 'sm' | 'md';
  dot?: boolean;             // colored dot before text
  children: React.ReactNode;
}
```

- Pill shape (border-radius 999px).
- Risk-specific: `.pill.good` / `.pill.warn` / `.pill.crit`.

### 2.5 RiskPill

```tsx
interface RiskPillProps {
  score: number;             // 0–100
  showValue?: boolean;       // show the number (default true)
  size?: 'sm' | 'md';
}
```

Logic:
```
score >= 70  → variant="crit",  label="High",   symbol="▲"
score >= 40  → variant="warn",  label="Medium",  symbol="●"
score < 40   → variant="good",  label="Low",     symbol="▼"
```

### 2.6 StatusTimeline

```tsx
interface StatusTimelineProps {
  events: TimelineEvent[];
  currentStatus: string;
}

interface TimelineEvent {
  at: string;                // ISO timestamp
  state: string;
  actor: string;
  note?: string;
  tx_hash?: string;          // blockchain tx, shown as icon/link
}
```

Renders a vertical timeline with:
- Filled circle for completed states.
- Pulsing circle for current state.
- Empty circle for future states.
- Each node: timestamp, state label, actor, note.
- Blockchain hash shown as a small chain icon linking to explorer.

### 2.7 Modal / ConfirmModal

```tsx
interface ConfirmModalProps {
  open: boolean;
  title: string;
  description: string;
  confirmLabel: string;      // e.g., "Trigger Verification"
  cancelLabel?: string;      // default "Cancel"
  variant?: 'default' | 'danger';
  loading?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}
```

- Used for every destructive action (freeze, FIR, dispatch).
- Focus trapped, Escape closes.
- `danger` variant: confirm button is red.
- Always restates the target ID in the description.

### 2.8 Table

```tsx
interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  emptyMessage?: string;
  pagination?: {
    page: number;
    total: number;
    hasMore: boolean;
    onPageChange: (page: number) => void;
  };
  sortBy?: string;
  sortDirection?: 'asc' | 'desc';
  onSort?: (field: string) => void;
}

interface Column<T> {
  key: string;
  header: string;
  width?: string;
  align?: 'left' | 'center' | 'right';
  mono?: boolean;            // mono font for this column
  render?: (value: T[keyof T], row: T) => React.ReactNode;
}
```

### 2.9 Toast

```tsx
interface ToastProps {
  variant: 'info' | 'success' | 'warning' | 'error';
  title: string;
  description?: string;
  duration?: number;         // ms, default 5000
  action?: {
    label: string;
    onClick: () => void;
  };
}
```

Triggered via:
```typescript
toast({ variant: 'info', title: 'New prediction', description: 'ATM-0042 flagged as high-risk' });
toast({ variant: 'error', title: 'Freeze failed', description: 'Bank nodal officer did not respond' });
```

### 2.10 Spinner

```tsx
interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;            // defaults to --accent
}
```

### 2.11 EmptyState

```tsx
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}
```

---

## 3. Domain Components

### 3.1 AlertCard (Field Dashboard)

```tsx
interface AlertCardProps {
  alert: FieldAlert;
  onNavigate: (atm: AtmCoords) => void;
  onDispatch: (complaintId: string) => void;
  onVerify: (complaintId: string) => void;
  onBackup: (complaintId: string) => void;
}
```

Visual:
- Right edge: 4px stripe in risk color.
- Top row: `RiskPill` + priority label + time.
- Middle: ATM name, block, distance + ETA.
- Bottom: Quick action buttons (Navigate, Dispatch, Verify, Backup).
- Tap anywhere expands to full detail.

### 3.2 AtmPopup (Command Center map)

```tsx
interface AtmPopupProps {
  atm: AtmRisk;
  onOpenCase: (complaintId: string) => void;
  onTriggerVerification: (atmId: string) => void;
  onRequestFreeze: (muleId: string) => void;
}
```

Renders inside Leaflet popup:
- ATM name + area.
- `RiskPill` with score.
- Connected complaints count + mule count.
- Predicted withdrawal window.
- Action buttons.

### 3.3 MoneyGraphNodePanel (Command Center graph)

```tsx
interface NodePanelProps {
  node: GraphNode;
  onClose: () => void;
  onTriggerVerification?: (atmId: string) => void;
  onRequestFreeze?: (muleId: string) => void;
}
```

Renders in a side panel when a node is selected:
- Node type icon + label.
- If mule: `RiskPill`, risk factors list, connected complaints.
- If ATM: area, coordinates, connected mules.
- If victim: masked info, amount sent.
- Action buttons based on node type.

### 3.4 ChatThread (LLM Agent)

```tsx
interface ChatThreadProps {
  messages: ChatMessage[];
  onSend: (message: string) => void;
  loading?: boolean;
  quickPrompts?: string[];
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  result?: QueryResult;       // structured result for rendering
}

interface QueryResult {
  type: 'text' | 'table' | 'chart' | 'graph';
  data: unknown;
}
```

Renders:
- Chat bubble layout (user right, assistant left).
- Streaming text effect for assistant responses.
- Result renderer: text block, Recharts chart, AG Grid table, or D3 mini-graph.
- Quick prompt chips below the input.
- Input with send button + loading state.

### 3.5 HealthCard (Admin Panel)

```tsx
interface HealthCardProps {
  service: ServiceHealth;
}

interface ServiceHealth {
  name: string;
  status: 'healthy' | 'degraded' | 'down';
  uptime_seconds: number;
  cpu_percent: number;
  memory_mb: number;
  gpu_percent?: number | null;
  disk_free_gb: number;
}
```

Renders:
- Status dot (green/amber/red) + service name.
- Uptime formatted as `Xd Xh Xm`.
- Gauges for CPU, memory, GPU (if applicable), disk free.
- Color transitions on status change.

---

## 4. Layout Components

### 4.1 Topbar

```tsx
interface TopbarProps {
  title: string;
  subtitle?: string;
  connectionStatus: 'connected' | 'reconnecting' | 'disconnected';
  user?: { name: string; role: string; station?: string };
  onLogout: () => void;
}
```

Sticky top bar. Shows:
- App name + subtitle.
- Connection indicator dot (green/red/amber).
- User avatar/name + dropdown (profile, logout).

### 4.2 Sidebar (Command Center)

```tsx
interface SidebarProps {
  navItems: NavItem[];
  unreadAlerts: number;
  currentPath: string;
}

interface NavItem {
  icon: React.ReactNode;
  label: string;
  path: string;
  badge?: number;            // unread count
}
```

### 4.3 CommandPalette (⌘K)

```tsx
interface CommandPaletteProps {
  open: boolean;
  onClose: () => void;
  onSearch: (query: string) => void;
  onAction: (actionId: string) => void;
  recentActions?: string[];
}
```

- Opens on `⌘K` / `Ctrl+K`.
- Search across cases, ATMs, actions.
- Action shortcuts (Trigger Verification, Generate FIR, etc.).
- Keyboard navigable (↑↓ to select, Enter to execute).

---

## 5. Hook Specifications

### 5.1 `useAuth()`
```typescript
function useAuth(): {
  user: User | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (role: string) => boolean;
}
```

### 5.2 `useSocket()`
```typescript
function useSocket(): {
  connected: boolean;
  on: (event: string, handler: EventHandler) => void;
  off: (event: string, handler: EventHandler) => void;
  send: (event: string, data: Record<string, unknown>) => void;
}
```

### 5.3 `useTheme()`
```typescript
function useTheme(): {
  theme: 'light' | 'dark' | 'system';
  resolved: 'light' | 'dark';   // actual applied theme
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
}
```

### 5.4 `useAlerts()`
```typescript
function useAlerts(filter?: { priority?: string }): {
  alerts: FieldAlert[];
  unreadCount: number;
  markRead: (alertId: string) => void;
  markAllRead: () => void;
}
```

### 5.5 `useOfflineQueue()`
```typescript
function useOfflineQueue(): {
  isOnline: boolean;
  queueLength: number;
  enqueue: (action: QueuedAction) => void;
  flush: () => Promise<void>;
}
```

---

## 6. Form Validation Patterns

Using React Hook Form + Zod:

```typescript
// Complaint form (Admin / edit)
const complaintSchema = z.object({
  fraud_type: z.enum(['investment', 'phishing', 'romance', 'tech_support', 'lottery', 'impersonation', 'upi_fraud', 'other']),
  amount: z.number().min(1).max(10000000),
  description: z.string().min(10).max(2000),
  fraudster_upi: z.string().min(3),
  fraudster_phone: z.string().regex(/^\+91\d{10}$/),
});

// User form (Admin)
const userSchema = z.object({
  name: z.string().min(2).max(100),
  username: z.string().min(3).max(50).regex(/^[a-z0-9._-]+$/),
  role: z.enum(['admin', 'inspector', 'constable']),
  station: z.string().min(2),
  phone: z.string().regex(/^\+91\d{10}$/),
  email: z.string().email(),
});
```

---

## 7. Animation Rules

- **Page transitions:** 200ms fade + 8px slide (Framer Motion `AnimatePresence`).
- **Modal open/close:** 150ms scale from 95% + fade.
- **Toast enter:** 300ms slide from right + fade.
- **Toast exit:** 200ms slide to right + fade.
- **Graph node highlight:** 150ms opacity + stroke-width.
- **Map marker pulse:** CSS keyframe, 1.5s infinite (critical markers only).
- **Skeleton loading:** 1.5s shimmer animation.
- **All disabled if `prefers-reduced-motion: reduce`.**

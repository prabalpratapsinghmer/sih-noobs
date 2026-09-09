# Field Dashboard — Full Feature Specification

> App: `apps/frontend-field` · Port 3002 (dev) · Route `/field` (prod)
> Audience: Police Constables on patrol · Theme: Light · Form factor: Mobile-first
> Primary use: receive alerts, navigate to ATMs, dispatch/verify/backup — with big buttons, minimal text, offline support.

---

## 1. Overview

The Field Dashboard is designed for constables who are outdoors, possibly wearing gloves, possibly in sunlight, possibly on a poor network. It must be fast to read, fast to tap, and resilient when offline.

**Core value:** See alert → navigate → act → done. Three taps maximum for any action.

---

## 2. Layout

```
┌──────────────────────────────┐
│  TOPBAR: logo · alert count  │
│          · officer name      │
├──────────────────────────────┤
│                              │
│  ACTIVE ALERTS (scrollable)  │
│  ┌────────────────────────┐  │
│  │ ▲ CRIT  ATM-0042       │  │
│  │   SBI - Koramangala    │  │
│  │   Risk: 82 · 2.1km     │  │
│  │   ETA: 8 min            │  │
│  │   [Nav] [Dispatch]     │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │ ● WARN  ATM-0087       │  │
│  │   ICICI - Jeevan Bhima │  │
│  │   Risk: 54 · 4.3km     │  │
│  │   ETA: 15 min           │  │
│  │   [Nav] [Dispatch]     │  │
│  └────────────────────────┘  │
│                              │
├──────────────────────────────┤
│  BOTTOM NAV: [Alerts] [History] [Profile] │
└──────────────────────────────┘
```

---

## 3. Views

### 3.1 Alerts (main, default)

**Purpose:** See and act on priority alerts.

**Alert card detail:**
- Right edge: 4px stripe in risk color (crit=red, warn=amber, info=green).
- Top row: RiskPill + priority label + time since alert.
- Middle: ATM name, block, area. Below: distance from officer + ETA.
- Bottom row: Quick action buttons (large, min 48px touch target).

**Priority ordering:**
1. `crit` (score ≥ 70) — red stripe, pulsing indicator
2. `warn` (score 40–69) — amber stripe
3. `info` (score < 40) — green stripe

**Empty state:** "No active alerts. All clear. ✓"

### 3.2 Alert Detail (tap card)

**Purpose:** Full context before acting.

**Content:**
- ATM name, area, coordinates.
- RiskPill with full score.
- Predicted withdrawal window (from → to).
- Connected mule count + individual mule scores.
- Complaint summary (masked victim info, fraud type, amount).
- Action buttons: Navigate, Dispatch, Verify, Backup.
- Timeline of what's happened so far.

### 3.3 Dispatch View

**Purpose:** Track the officer's journey to the ATM.

**Content:**
- Map showing officer GPS position and ATM destination.
- Route line (if maps integration available; otherwise, distance + ETA).
- Status buttons: "En Route" → "Arrived" → "Verified".
- Backup request button (always visible).
- Timer showing elapsed time since dispatch.

### 3.4 History

**Purpose:** See past actions taken by this officer.

**Content:**
- List of past alerts with resolution status.
- Each entry: complaint ID, ATM, action taken, time, outcome.
- Filter: today, this week, all.

### 3.5 Profile

**Purpose:** Officer info and settings.

**Content:**
- Officer name, badge number, station, role.
- Current location status (GPS enabled/disabled).
- Theme toggle (light/dark/system).
- Logout button.
- App version.

---

## 4. Quick Actions

| Action | Button label | Effect | Confirmation? |
|--------|-------------|--------|---------------|
| Navigate | "Navigate" | Opens device maps app with ATM coordinates via `geo:` URI or Google Maps URL | No |
| Dispatch | "Dispatch" | Sets alert status to `dispatched`, records timestamp + GPS | No (but shows "Dispatched ✓" toast) |
| Verify | "Verify" | Sets alert status to `verified`, records timestamp | No (but shows "Verified ✓" toast) |
| Backup | "Backup" | Sends `backup.requested` WS event to Command Center | Yes — "Request backup from control room?" confirm |

**Offline behavior:** All actions queue locally and flush on reconnect. Show "Queued — will send when online" chip.

---

## 5. Distance & ETA Calculation

```typescript
// Simple Haversine formula (no external lib needed)
function getDistance(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const R = 6371; // Earth radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 +
            Math.cos(lat1 * Math.PI/180) * Math.cos(lat2 * Math.PI/180) *
            Math.sin(dLng/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// ETA: assume average urban speed of 25 km/h
function getETA(distanceKm: number): number {
  return Math.round((distanceKm / 25) * 60); // minutes
}
```

Officer GPS: `navigator.geolocation.getCurrentPosition()` on mount, update every 30s.

---

## 6. Offline Support

### Service Worker Strategy

| Resource | Strategy | Cache |
|----------|----------|-------|
| App shell (HTML/CSS/JS) | Cache-first | Versioned cache |
| API: alerts list | Network-first, fallback to cache | Current alerts |
| API: action updates | Network, queue if offline | localStorage queue |
| Map tiles | Cache-first (limited) | Last 50 tiles |

### Offline Queue

```typescript
interface QueuedAction {
  id: string;
  alertId: string;
  actionType: 'dispatch' | 'verify' | 'backup';
  timestamp: string;        // when the officer tapped
  gps?: { lat: number; lng: number };
  synced: boolean;
}

// Stored in localStorage under key 'offline_queue'
// Flushed on reconnect via wsClient.send('dispatch.updated', ...)
```

### UI Indicators

- **Offline chip:** Persistent banner at bottom: "Offline — changes queued" (amber).
- **Queue count:** "3 actions queued" badge on the chip.
- **Sync toast:** When actions flush, show "3 actions synced ✓".

---

## 7. Redux Store Shape

```typescript
{
  auth: {
    user: User | null;
    token: string | null;
  },
  alerts: {
    items: FieldAlert[];
    unreadCount: number;
    selected: FieldAlert | null;
    loading: boolean;
  },
  dispatch: {
    active: DispatchState | null;    // current en-route state
    history: DispatchRecord[];
  },
  offline: {
    isOnline: boolean;
    queue: QueuedAction[];
  },
  location: {
    lat: number | null;
    lng: number | null;
    accuracy: number | null;
    error: string | null;
  }
}
```

---

## 8. File Structure

```
apps/frontend-field/
├── src/
│   ├── main.tsx
│   ├── app/
│   │   ├── routes.tsx
│   │   ├── providers.tsx
│   │   └── layout/
│   │       ├── FieldLayout.tsx
│   │       ├── Topbar.tsx
│   │       └── BottomNav.tsx
│   ├── features/
│   │   ├── alerts/
│   │   │   ├── AlertList.tsx
│   │   │   ├── AlertCard.tsx
│   │   │   ├── AlertDetail.tsx
│   │   │   └── EmptyAlerts.tsx
│   │   ├── dispatch/
│   │   │   ├── DispatchView.tsx
│   │   │   ├── DispatchTimer.tsx
│   │   │   └── DispatchMap.tsx
│   │   ├── history/
│   │   │   ├── HistoryView.tsx
│   │   │   └── HistoryItem.tsx
│   │   └── profile/
│   │       └── ProfileView.tsx
│   ├── shared/
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   └── alerts.api.ts
│   │   ├── ws/
│   │   │   └── socket.ts
│   │   ├── hooks/
│   │   │   ├── useGeolocation.ts
│   │   │   └── useDistance.ts
│   │   └── mock/
│   │       └── alerts.json
│   ├── store/
│   │   ├── store.ts
│   │   ├── authSlice.ts
│   │   ├── alertsSlice.ts
│   │   ├── dispatchSlice.ts
│   │   ├── offlineSlice.ts
│   │   └── locationSlice.ts
│   └── styles/
│       └── field.css
├── index.html
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
├── public/
│   └── sw.js              # service worker
└── Dockerfile.field
```

---

## 9. Performance Requirements

- Alert cards render within 200ms of WS event receipt.
- GPS acquisition: first position within 5s, update every 30s.
- Offline queue flush: all queued actions sent within 3s of reconnect.
- Touch targets: minimum 48×48px for all buttons.
- Load time: < 2s on 3G network (shell cached by service worker).
- Battery: minimize GPS polling when app is backgrounded (`document.visibilityState`).

---

## 10. Decisions & Rationale

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Theme | Light (with alert colors) | Officers use outdoors in sunlight |
| Navigation | Bottom nav bar | Standard mobile pattern, thumb-reachable |
| Maps | Lightweight Leaflet for dispatch view | Show route, not a full heatmap |
| Offline | Service worker + localStorage queue | Works without network, syncs on reconnect |
| Buttons | Large (48px+), few per screen | Gloved/wet hands, quick actions |
| Text | Minimal, scannable | Officers read under stress |

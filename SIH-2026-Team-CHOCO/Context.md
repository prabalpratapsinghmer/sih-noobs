# CyberCell Platform - Session Context

## Session Date: 2026-09-06

---

## ✅ COMPLETED THIS SESSION

### 1. Design System Established
- **DESIGN.md** created at `D:\MokshFrontEnd\DESIGN.md` - Complete Linear × SpaceX design system
  - Visual theme: Cockpit Dense (9/10), Predictable Symmetric (2/10), Static Restrained (1/10)
  - Color tokens: Void #0D0D0E, Void-Elevated #131314, Telemetry-Amber #D4A843 (single accent), semantic status colors
  - Typography: IBM Plex Sans (headings/body), IBM Plex Mono (ALL numbers/telemetry/currency)
  - Anti-slop rules: 25+ explicit bans (no glassmorphism, no purple gradients, no Inter, no pure black, etc.)
  - Tailwind v4 CSS variables + Google Fonts loading snippets

### 2. Project Documentation Analyzed
- **ToDo.md** - Full 2026 architecture roadmap with 7 phases, 47 action items
- **MEMBER-3.md** - Command Center, Field Dashboard, Admin Panel, UI Kit specs
- **MEMBER-4.md** - Citizen Victim Portal, 4-step wizard, demo flow
- **linear-design/** - Reference design system with fonts

### 3. Monorepo Initialization Started
- **package.json** created with all required dependencies:
  - React 19, React Router 7, Lucide React
  - @xyflow/react (graph), recharts (charts)
  - react-hook-form + zod + @hookform/resolvers (forms)
  - framer-motion (step transitions), zustand (state)
  - tailwindcss v3.4.17, clsx, tailwind-merge
- **vite.config.ts** created with path aliases
- Project location: `D:\MokshFrontEnd`

---

## 📋 REMAINING WORK (Priority Order)

### Phase 1: Core Infrastructure (IMMEDIATE)
| Task | Status | Details |
|------|--------|---------|
| Install dependencies | ⬜ | `pnpm install` or `npm install` |
| Create Tailwind config with DESIGN.md tokens | ⬜ | `tailwind.config.js` with CSS variables |
| Create global CSS with design tokens | ⬜ | `src/styles/globals.css` |
| Create TypeScript config | ⬜ | `tsconfig.json` |
| Create index.html entry | ⬜ | Root HTML with font preloads |
| Create main.tsx + App.tsx | ⬜ | React 19 entry with router |

### Phase 2: Atomic Components (ui-kit)
| Component | Status | Spec Reference |
|-----------|--------|----------------|
| Button (Primary/Secondary/Ghost/Destructive) | ⬜ | DESIGN.md §4 |
| Card / Panel | ⬜ | DESIGN.md §4 |
| Input / Form Field | ⬜ | DESIGN.md §4 |
| Badge / Status Indicator | ⬜ | DESIGN.md §4 |
| Skeleton Loader | ⬜ | DESIGN.md §4 |
| Modal / Dialog | ⬜ | DESIGN.md §4 |
| Tooltip | ⬜ | DESIGN.md §4 |

### Phase 3: Layout & Navigation
| Component | Status | Spec Reference |
|-----------|--------|----------------|
| Topbar (Insignia, Status Pulse, WS Latency, Officer Card, ⌘K) | ⬜ | SECTION 3.1 |
| Demo Engine HUD (Bottom-right floating panel) | ⬜ | SECTION 3.1 |
| Mobile Bottom Dock (Alerts/Patrol/Comms/Officer) | ⬜ | SECTION 3.4 |

### Phase 4: Route Implementation
| Route | Path | Status | Key Components |
|-------|------|--------|----------------|
| National Gateway | `/` | ⬜ | Hero stats strip, 3 portal cards, 1930 banner |
| Citizen Reporting | `/report` | ⬜ | 4-step wizard, OTP modal, case tracker |
| Command Center | `/command` | ⬜ | Threat map, Money Trail (@xyflow), AI Copilot, Freeze button |
| Field Responder | `/field` | ⬜ | Mobile-first, patrol cards, intercept workflow |
| Admin Telemetry | `/admin` | ⬜ | STM/GNN charts (Tremor/Recharts), station roster |

### Phase 5: Advanced Features
| Feature | Status | Tech |
|---------|--------|------|
| Judge Demo Engine (Zustand store) | ⬜ | `src/store/demoStore.ts` - 6-stage sync |
| WebSocket integration | ⬜ | Real-time alerts |
| Threat Map (MapLibre GL / Deck.gl) | ⬜ | 3D vector tiles, radar pulses |
| Money Trail Graph (@xyflow/react) | ⬜ | Custom nodes, animated edges |
| AI Copilot Slide-over | ⬜ | CrPC Section 91, UPI reverse-lookup |

### Phase 6: Verification
| Check | Status | Tool |
|-------|--------|------|
| Dependency install | ⬜ | `pnpm install` |
| TypeScript build | ⬜ | `pnpm build` / `pnpm typecheck` |
| Impeccable audit | ⬜ | Visual hierarchy, contrast, spacing, mono usage |
| Playwright E2E | ⬜ | 4-step wizard, mobile viewport, screenshots |

---

## 🎯 KEY DESIGN CONSTRAINTS (NON-NEGOTIABLE)

From DESIGN.md - enforce in ALL components:
1. **All numbers/currency/IDs/coordinates → IBM Plex Mono + tabular-nums**
2. **Single accent: Telemetry-Amber #D4A843 only** (CTAs, focus rings, live badges)
3. **Borders: 1px solid #2A2A2C** - no shadows for elevation
4. **Backgrounds: Void #0D0D0E / Void-Elevated #131314** - never pure black
5. **No glassmorphism, no blur, no purple, no neon, no emojis**
6. **Motion: 150ms opacity/transform only** - translateY(1px) on button active
7. **CSS Grid only** - no flexbox calc() hacks
8. **Copy: Technical, precise, I4C terminology** - "Latency: 12ms" not "Blazing fast"

---

## 🔧 COMMANDS TO RESUME

```bash
# Navigate to project
cd D:\MokshFrontEnd

# Install dependencies
pnpm install
# or: npm install

# Start dev server
pnpm dev
# or: npm run dev

# Type check
pnpm typecheck

# Production build
pnpm build
```

---

## 📁 PROJECT STRUCTURE (Target)

```
D:\MokshFrontEnd\
├── package.json          ✅ Created
├── vite.config.ts        ✅ Created
├── DESIGN.md             ✅ Created
├── ToDo.md               ✅ Existing
├── MEMBER-3.md           ✅ Existing
├── MEMBER-4.md           ✅ Existing
├── Context.md            ✅ This file
├── tsconfig.json         ⬜ To create
├── tailwind.config.js    ⬜ To create
├── postcss.config.js     ⬜ To create
├── index.html            ⬜ To create
├── src/
│   ├── main.tsx          ⬜ To create
│   ├── App.tsx           ⬜ To create
│   ├── styles/
│   │   └── globals.css   ⬜ To create
│   ├── components/
│   │   ├── ui/           ⬜ Atomic components
│   │   ├── layout/       ⬜ Topbar, DemoHUD, BottomDock
│   │   ├── wizard/       ⬜ ComplaintWizard steps
│   │   ├── command/      ⬜ ThreatMap, MoneyTrail, AICopilot
│   │   ├── field/        ⬜ PatrolCard, InterceptFlow
│   │   └── admin/        ⬜ TelemetryCharts, StationTable
│   ├── pages/
│   │   ├── Gateway.tsx   ⬜ Route: /
│   │   ├── Report.tsx    ⬜ Route: /report
│   │   ├── Command.tsx   ⬜ Route: /command
│   │   ├── Field.tsx     ⬜ Route: /field
│   │   └── Admin.tsx     ⬜ Route: /admin
│   ├── store/
│   │   ├── demoStore.ts  ⬜ Judge Demo Engine
│   │   └── appStore.ts   ⬜ Global UI state
│   ├── hooks/
│   │   └── useDemo.ts    ⬜ Demo engine hook
│   └── lib/
│       └── utils.ts      ⬜ cn() helper
```

---

## 🚨 CRITICAL NOTES FOR NEXT SESSION

1. **Tailwind v3.4.17** - NOT v4 (per MEMBER-3.md, v4 breaks shadcn/ui integration)
2. **Font loading**: Use Next.js `next/font` pattern or `@import` for IBM Plex Sans/Mono
3. **MapLibre GL** requires Mapbox token alternative - use free CartoDB dark tiles
4. **@xyflow/react v12** - import styles: `import '@xyflow/react/dist/style.css'`
5. **Demo Store** must be deterministic - no real API calls, all in-memory Zustand
6. **Audio chime** for demo: Use Web Audio API, fallback to silent
7. **I4C terminology**: "Complaint ID: CC-2026-XXXX", "AI_ANALYZING", "ACTION_TAKEN", "NPCI Freeze Directive", "Section 91 CrPC"

---

## 📝 NEXT IMMEDIATE STEPS

1. Run `pnpm install` in `D:\MokshFrontEnd`
2. Create `tailwind.config.js` with DESIGN.md tokens as CSS variables
3. Create `src/styles/globals.css` with @layer base/components/utilities
4. Create `tsconfig.json` with strict mode, path aliases
5. Create `index.html` with font preloads and root div
6. Create `src/main.tsx` + `src/App.tsx` with React Router
7. Build atomic UI components per DESIGN.md §4
8. Implement pages in priority order: Gateway → Report → Command → Field → Admin
9. Wire demo store, test full 5-min sequence
10. Run impeccable audit + playwright verification

---

*Context saved. Resume from Phase 1: Core Infrastructure.*
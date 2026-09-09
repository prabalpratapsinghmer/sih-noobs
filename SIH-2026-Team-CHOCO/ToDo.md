# National Cyber Crime Reporting & Intelligence Platform (CHOCO / CyberCell)
## Frontend & System Architecture Overhaul: 2026 Next-Gen Tech Stack & Master Action Plan

---

### Executive Summary

An exhaustive review of `MEMBER-3.md` (Police HQ Command Center, Field Dashboard, Shared UI Kit, Infrastructure) and `MEMBER-4.md` (Citizen Victim Portal, Presentation Demo, ML Dashboard, Integration) reveals a **fundamentally fragmented architecture** running across 4 disconnected runtimes:
1. **Monorepo React 19 apps** (`apps/command-center`, `apps/field-dashboard`, `apps/admin-panel` - partially built or stubs).
2. **Vanilla HTML/CSS/JS SPAs** (`police-command/`, `police-field/`, `victim-dashboard/` - duplicated maintenance).
3. **Python Flask Demo Server** (`ruma/app.py`, 1,054 lines simulating ML training and ATM coordinates on port 5500).
4. **Python Streamlit Dashboard** (`dashboard/streamlit_dashboard.py`, running on port 8501 for model metrics).

This fragmentation creates **severe demo failure risk**, duplicate work, inconsistent styling (Font Awesome vs Lucide, custom CSS vs Tailwind), and relies on dated libraries (such as `vis-network` for graph rendering, Leaflet 2D raster tiles, and Redux Toolkit boilerplate).

This document establishes the **2026 state-of-the-art frontend architecture**, consolidating all capabilities into a **single, unified, high-performance React 19 + Tailwind CSS + shadcn/ui monorepo**, powered by modern libraries like `@xyflow/react`, `MapLibre GL`, `Aceternity UI`, `Magic UI`, and `Tremor`, backed by an integrated **in-browser "Judge Demo Scenario Engine"** that eliminates external Python demo servers entirely.

---

## 1. Stack Assessment & Gap Analysis

### 1.1 Member 3 & Member 4 Objectives Overview

| Domain | Member | Stated Objectives | Current Stack | Critical Shortcomings & Bottlenecks |
| :--- | :---: | :--- | :--- | :--- |
| **Citizen Portal** | M4 | 4-step fraud reporting wizard, live case tracker, OTP verification, evidence vault. | Vanilla JS (517 lines), plain CSS, Font Awesome 6.5, simulated JS timeouts. | Disconnected from `@sih/ui-kit`; `apps/victim-portal` is an empty stub; no validation library (Zod); no responsive animations. |
| **Command Center** | M3 | High-density threat heatmap, mule account transaction graph, AI Copilot, emergency account freeze. | React 19, Redux Toolkit, Leaflet 1.9, `vis-network`, Tailwind 3.4.17. | `vis-network` is an outdated canvas engine lacking React 19 reactivity & dark mode; Leaflet lacks 3D vector acceleration; Redux is bloated for async state. |
| **Field Mobile PWA** | M3 | Mobile responder interface, patrol assignments, ATM alert intercept workflow, route navigation. | React 19 / Vanilla duplicate, Leaflet map, simulated chat. | Fragile layout switching; missing native bottom sheet navigation, haptics, and instant cache revalidation. |
| **Presentation Demo** | M4 | 5-minute hackathon pitch: citizen complaint $\to$ ML scatter detection $\to$ Command Center $\to$ Field intercept. | Flask server (`ruma/app.py` on port 5500) + Chart.js. | **High demo crash risk**: Requires 4 separate ports (3000, 5500, 8501, 8000) running concurrently; fragile mock endpoints. |
| **ML Telemetry** | M4/M1 | Model training loss, parameter tables, STM/GNN accuracy monitoring. | Streamlit (`streamlit_dashboard.py` on port 8501) + Plotly. | High latency, separate browser tab required; completely breaks the visual continuity of the investigator command center. |
| **Shared Design System** | M3/M4 | Central `@sih/ui-kit`, CSS design tokens, consistent Gov/Cyber branding. | Custom CSS tokens in `tokens.css`, Tailwind 3.4.17 pinned, hand-rolled Button/Card/Badge. | Relative CSS token path import bugs across nested monorepo packages; pinned to Tailwind 3 out of fear of breaking PostCSS. |

---

## 2. The 2026 Next-Gen Frontend Technology Stack

The 2026 industry standard has shifted completely to **code-ownership via headless primitives**, **zero-runtime CSS engine**, and **interactive cyber telemetry components**.

```
+---------------------------------------------------------------------------------------------------+
|                                 UNIFIED FRONTEND RUNTIME (React 19)                               |
+---------------------------------------------------------------------------------------------------+
|  [Citizen Portal]       [Command Center]       [Field Responder PWA]      [Admin & ML Telemetry]  |
|  (4-Step Wizard)      (XYFlow Mule Graph)      (Mobile-First Intercept)     (Tremor Analytics)    |
+---------------------------------------------------------------------------------------------------+
|                        PRESENTATION LAYER: Aceternity UI + Magic UI Components                     |
|            (Tracing Beams, Shimmer Freeze Button, Number Tickers, Animated Radar Pings)            |
+---------------------------------------------------------------------------------------------------+
|                        CORE PRIMITIVES: shadcn/ui (Base UI / Radix Primitives)                    |
|             (Forms, Dialogs, Dropdowns, Sheets, Tables, Command K Palette, Tooltips)              |
+---------------------------------------------------------------------------------------------------+
|              DATA VISUALIZATION & MAPS               |              STATE & NETWORKING            |
|  * Graph: @xyflow/react (React Flow 12)             |  * Server State: TanStack Query v5         |
|  * Geo: MapLibre GL / Deck.gl (3D Vector Tiles)      |  * Client/Session: Zustand                 |
|  * Metrics: Tremor + Recharts                        |  * Real-Time: Socket.IO Client + WebWorker |
+---------------------------------------------------------------------------------------------------+
|                    DESIGN SYSTEM ENGINE: Tailwind CSS v4 + IBM Plex Typography                    |
+---------------------------------------------------------------------------------------------------+
```

### 2.1 Technology Comparison Matrix

| Layer | Current Choice | 2026 Optimal Standard | Concrete Rationale & Upgrade Benefit |
| :--- | :--- | :--- | :--- |
| **Component Primitives** | Custom hand-rolled components (`Button.tsx`, `Card.tsx`) | **shadcn/ui** (powered by **Base UI / Radix**) | Accessible WAI-ARIA primitives, keyboard navigation, copy-paste ownership, zero bloated node_modules wrapper. |
| **Cyber & Visual FX** | Static CSS borders & basic gradients | **Aceternity UI** + **Magic UI** | Delivers immediate "WOW" factor for judges: *Animated Border Beams*, *Shimmer Universal Freeze Buttons*, *Live Counter Tickers*, and *Cyber Matrix Grids*. |
| **Money Trail Graph** | `vis-network` (2015 Canvas) | **`@xyflow/react` (React Flow 12)** | Native React 19 node graph, custom styled nodes (Victim, Mule, ATM), glowing animated SVG edges representing transaction velocity, pan/zoom minimap. |
| **Threat Map** | Leaflet 1.9 + `leaflet.heat` (2D raster) | **MapLibre GL** + **Deck.gl** | Hardware-accelerated WebGL vector tiles, dark CartoDB tiles, 3D extruded hexagon risk bins, real-time animated radar pulse pings on high-risk ATMs. |
| **ML & Metrics Charts** | External Streamlit (port 8501) + Chart.js | **Tremor** + **Recharts** | Directly embeds STM Transformer & GNN loss curves into the Admin/HQ portal. Eliminates the Python Streamlit server entirely. |
| **Global State** | Redux Toolkit | **Zustand** | 90% less boilerplate, zero provider wrapping, seamless multi-tab synchronization, perfect for alert feeds and audio cues. |
| **Server State & API** | Axios + Redux Slices | **TanStack Query v5** | Automatic caching, background refetching, optimistic UI updates, integrated WebSocket cache invalidation. |
| **Form Management** | Vanilla event listeners / unmanaged inputs | **React Hook Form** + **Zod** | End-to-end type safety, auto-sanitized UPI IDs, bank account formats, phone regex, multi-step wizard state persistence. |
| **Iconography** | Font Awesome (M4) + Lucide (M3) | **Lucide React** (Unified) | 100% unified visual style, tree-shakeable SVG icons, dynamic stroke widths, seamless dark mode integration. |

---

## 3. Best UI Component Libraries & Modern Resources (2026)

To build the highest caliber cyber-defense platform, integrate these modern registries and free UI resources:

1. **shadcn/ui ([ui.shadcn.com](https://ui.shadcn.com))**:
   - *Components to use*: `Dialog`, `Command` (⌘K search palette), `Sheet` (Field mobile drawer), `Table` (Mule ledger), `Tabs`, `Badge`, `Card`, `Form`.
   - *Advantage*: Code is copied directly into `packages/ui-kit` or `components/ui/`, fully customizable without library lock-in.

2. **Aceternity UI ([ui.aceternity.com](https://ui.aceternity.com))**:
   - *Components to use*:
     - **Tracing Beam**: For the victim complaint timeline (`Submitted` $\to$ `AI Analyzing` $\to$ `Action Taken` $\to$ `Resolved`).
     - **Background Boxes / Retro Grid**: For the national cybersecurity landing page hero section.
     - **Moving Border / Card Hover Effect**: For high-risk ATM cards in the command center.
     - **Directional Aware Hover**: For field officer action cards.

3. **Magic UI ([magicui.design](https://magicui.design))**:
   - *Components to use*:
     - **Number Ticker**: For real-time animated counters: *"₹8,24,90,000 Recovered"* and *"47 Active Intercepts Today"*.
     - **Border Beam**: Highlighting compromised mule accounts in the graph.
     - **Animated List**: For live, streaming incoming WebSocket fraud alerts.
     - **Shimmer Button**: For the high-stakes *"UNIVERSAL FREEZE ALL LINKED MULES"* button.

4. **React Flow / XYFlow ([reactflow.dev](https://reactflow.dev))**:
   - *Components to use*:
     - Custom Node types: `VictimNode` (red/warning), `MuleNode` (amber/critical with tier badges Layer 1 $\to$ Layer 2 $\to$ Layer 3), `AtmNode` (cyan/location pinned).
     - Animated SVG edges with flowing particles indicating transaction speed and INR amounts.

5. **Tremor ([tremor.so](https://tremor.so))**:
   - *Components to use*: `AreaChart` (ML training loss curves), `Tracker` (system uptime & latency), `BarList` (top targeted banks & ATM hubs), `Metric` badges.

6. **21st.dev ([21st.dev](https://21st.dev))**:
   - The "NPM for Design Engineers" — pre-built copy-paste Tailwind components for cyber defense HUDs, audio waveform alerts, and terminal logs.

---

## 4. Key Architectural Innovations

### Innovation 1: The Zero-Fail "Judge Demo Mode" Engine
*Problem:* In live hackathon demos, running separate Python servers (`ruma/app.py` on 5500, Streamlit on 8501, FastAPI on 8000) frequently leads to port collisions, connection timeouts, or missing environment variables.  
*Solution:* Build an internal **Zustand-powered Scenario Simulation Engine** into the frontend (`src/lib/demoScenario.ts`):
- Features a discreet floating HUD: `[Run Full 5-Min SIH Pitch Flow]` or individual step triggers.
- Step 1: Automatically simulates filing a ₹5,00,000 Investment Scam complaint.
- Step 2: Generates real-time audio chime + animated alert banner across HQ Command Center.
- Step 3: XYFlow graph instantly animates the 3-hop mule money trail with flowing INR currency beams.
- Step 4: MapLibre GL camera flies to Bengaluru Indiranagar ATM cluster with 3D pulse rings.
- Step 5: Field Officer mobile view triggers incoming high-priority dispatch with 1-click `[INTERCEPT & FREEZE]`.
- Allows toggling between **Live Production Backend** (`http://localhost:8000`) and **Deterministic Demo Mode** with a single click.

### Innovation 2: Eradicating Duplicate Codebases
*Problem:* The repository currently maintains both vanilla SPAs (`police-command/`, `police-field/`, `victim-dashboard/`) and monorepo packages (`apps/*`). This splits engineering effort in half.  
*Solution:*
- Consolidate all apps into a clean, modern monorepo powered by **Vite / Next.js** and **React 19**.
- Retain static single-file production export builds if zero-install browser opening is needed, but maintain **one unified component codebase**.

### Innovation 3: True Real-Time Graph Telemetry with `@xyflow/react`
*Problem:* `vis-network` renders to an unstyled canvas. It cannot render custom React micro-components inside nodes, cannot respond smoothly to dark mode CSS variables, and looks dated.  
*Solution:* Implement `@xyflow/react` with custom Tailwind-styled nodes, interactive transaction inspection side-drawers, and glowing edge particle animations.

---

## 5. Concrete Code Implementations of Modern Components

### 5.1 Money Trail Graph (`@xyflow/react` with Animated Flow Edges)
Replaces outdated `vis-network` with a hardware-accelerated, Tailwind-styled graph engine:

```tsx
// packages/ui-kit/src/components/graph/MoneyTrailFlow.tsx
import React, { useMemo } from 'react';
import { 
  ReactFlow, 
  Background, 
  Controls, 
  MiniMap, 
  Handle, 
  Position, 
  NodeProps,
  MarkerType 
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { ShieldAlert, User, Landmark, MapPin } from 'lucide-react';

// Custom Mule Account Node with Neon Cyber Styling
export const MuleAccountNode = ({ data }: NodeProps) => (
  <div className="relative group rounded-xl border border-red-500/40 bg-zinc-950/90 p-4 shadow-[0_0_20px_rgba(239,68,68,0.2)] backdrop-blur-md min-w-[200px]">
    <Handle type="target" position={Position.Left} className="!bg-red-500 !w-3 !h-3" />
    <div className="flex items-center space-x-3">
      <div className="p-2 rounded-lg bg-red-500/10 text-red-400">
        <Landmark className="w-5 h-5" />
      </div>
      <div>
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono font-bold text-red-400 uppercase tracking-wider">{data.tier || 'Layer 1'} Mule</span>
          <span className="px-1.5 py-0.5 rounded text-[10px] bg-red-500/20 text-red-300 font-mono">Risk: {data.riskScore}%</span>
        </div>
        <p className="text-sm font-semibold text-white mt-0.5">{data.accountName}</p>
        <p className="text-xs font-mono text-zinc-400">{data.accountNumber}</p>
      </div>
    </div>
    <div className="mt-3 pt-2 border-t border-zinc-800 flex justify-between items-center text-xs">
      <span className="text-zinc-500 font-mono">Dispersed:</span>
      <span className="text-emerald-400 font-mono font-bold">₹{Number(data.amount).toLocaleString('en-IN')}</span>
    </div>
    <Handle type="source" position={Position.Right} className="!bg-red-500 !w-3 !h-3" />
  </div>
);

// Custom ATM Cash-Out Target Node
export const AtmTargetNode = ({ data }: NodeProps) => (
  <div className="relative rounded-xl border border-cyan-500/50 bg-zinc-950/90 p-4 shadow-[0_0_25px_rgba(6,182,212,0.25)] min-w-[190px]">
    <Handle type="target" position={Position.Left} className="!bg-cyan-400 !w-3 !h-3" />
    <div className="flex items-center space-x-3">
      <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 animate-pulse">
        <MapPin className="w-5 h-5" />
      </div>
      <div>
        <span className="text-[10px] font-mono uppercase tracking-wider text-cyan-400 font-bold">Predicted Cashout</span>
        <p className="text-sm font-semibold text-white">{data.atmName}</p>
        <p className="text-xs text-zinc-400">{data.location}</p>
      </div>
    </div>
    <div className="mt-2 text-xs flex items-center justify-between text-zinc-400 font-mono">
      <span>ETA to Cashout:</span>
      <span className="text-amber-400 font-bold">&lt; 8 mins</span>
    </div>
  </div>
);
```

### 5.2 Interactive Universal Freeze Button (Aceternity / Magic UI Inspired)
Replaces the standard button with high-impact tactile visual cues:

```tsx
// packages/ui-kit/src/components/cyber/UniversalFreezeButton.tsx
import React, { useState } from 'react';
import { ShieldBan, AlertTriangle, CheckCircle2 } from 'lucide-react';

export const UniversalFreezeButton = ({ onFreezeAll }: { onFreezeAll: () => Promise<void> }) => {
  const [status, setStatus] = useState<'idle' | 'confirming' | 'freezing' | 'frozen'>('idle');

  const handleExecute = async () => {
    setStatus('freezing');
    await onFreezeAll();
    setStatus('frozen');
    setTimeout(() => setStatus('idle'), 4000);
  };

  return (
    <div className="relative inline-block">
      {status === 'idle' && (
        <button
          onClick={() => setStatus('confirming')}
          className="relative group overflow-hidden rounded-xl px-6 py-3 font-mono font-bold text-white transition-all duration-300 bg-red-600/90 hover:bg-red-600 hover:shadow-[0_0_30px_rgba(239,68,68,0.6)] active:scale-95"
        >
          <span className="relative z-10 flex items-center space-x-2">
            <ShieldBan className="w-5 h-5 text-white animate-pulse" />
            <span>UNIVERSAL FREEZE (8 NODES)</span>
          </span>
          <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/20 to-transparent" />
        </button>
      )}

      {status === 'confirming' && (
        <div className="flex items-center space-x-2 bg-zinc-900 border border-red-500/80 p-1.5 rounded-xl shadow-2xl animate-in fade-in zoom-in-95">
          <span className="text-xs text-red-300 px-3 font-mono flex items-center gap-1">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
            Freeze all 8 bank accounts via RBI NPCI switch?
          </span>
          <button
            onClick={handleExecute}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-mono font-bold rounded-lg uppercase"
          >
            CONFIRM FREEZE
          </button>
          <button
            onClick={() => setStatus('idle')}
            className="px-3 py-2 text-zinc-400 hover:text-white text-xs font-mono"
          >
            Cancel
          </button>
        </div>
      )}

      {status === 'freezing' && (
        <div className="flex items-center space-x-2 px-6 py-3 bg-red-950/80 border border-red-500 rounded-xl text-red-200 font-mono text-xs">
          <div className="w-4 h-4 border-2 border-red-400 border-t-transparent rounded-full animate-spin" />
          <span>BROADCASTING NPCI FREEZE DIRECTIVES...</span>
        </div>
      )}

      {status === 'frozen' && (
        <div className="flex items-center space-x-2 px-6 py-3 bg-emerald-950/80 border border-emerald-500 rounded-xl text-emerald-300 font-mono text-xs shadow-[0_0_20px_rgba(16,185,129,0.3)]">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>ACCOUNTS LOCKED & EVIDENCE PACK GENERATED</span>
        </div>
      )}
    </div>
  );
};
```

### 5.3 Citizen Complaint Wizard with Zod & Framer Motion
Upgrades Member 4's vanilla JS 517-line wizard into a modern, resilient, accessible multi-step experience:

```tsx
// apps/victim-portal/src/components/wizard/ComplaintWizard.tsx
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, ArrowRight, ArrowLeft, UploadCloud, CheckCircle } from 'lucide-react';

const complaintSchema = z.object({
  victim_name: z.string().min(2, "Full name required"),
  victim_phone: z.string().regex(/^[6-9]\d{9}$/, "Must be a valid 10-digit Indian mobile number"),
  victim_address: z.string().min(5, "Residential address required"),
  amount: z.coerce.number().positive("Amount lost must be greater than 0"),
  fraud_date: z.string().nonempty("Date of incident is required"),
  fraud_type: z.enum(['INVESTMENT_SCAM', 'KYC_FRAUD', 'UPI_FRAUD', 'FAKE_JOB', 'PHISHING', 'OTHER']),
  description: z.string().min(10, "Please provide brief details of the incident"),
  fraudster_upi: z.string().optional(),
  fraudster_account: z.string().optional(),
});

type ComplaintFormData = z.infer<typeof complaintSchema>;

export const ComplaintWizard = ({ onSubmitComplete }: { onSubmitComplete: (id: string) => void }) => {
  const [step, setStep] = useState(1);
  const { register, handleSubmit, formState: { errors, isValid } } = useForm<ComplaintFormData>({
    resolver: zodResolver(complaintSchema),
    mode: 'onChange'
  });

  const onSubmit = async (data: ComplaintFormData) => {
    // Connects to FastAPI backend or Demo Scenario Store
    const fakeId = `CC-2026-${Math.floor(1000 + Math.random() * 9000)}`;
    onSubmitComplete(fakeId);
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-zinc-900/90 border border-zinc-800 rounded-2xl shadow-2xl p-6 sm:p-8 backdrop-blur-xl">
      {/* Step Indicator Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-5 mb-6">
        <div>
          <span className="text-xs font-mono uppercase tracking-wider text-cyan-400 font-semibold">National Cybercrime Portal</span>
          <h2 className="text-xl font-bold text-white mt-1">Lodge Fraud Complaint</h2>
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="text-cyan-400 font-bold">Step {step}</span>
          <span className="text-zinc-600">/</span>
          <span className="text-zinc-500">3</span>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-4"
            >
              <h3 className="text-sm font-semibold text-zinc-300">1. Citizen Contact Information</h3>
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-1">Full Legal Name</label>
                <input {...register('victim_name')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:border-cyan-500 focus:outline-none" placeholder="e.g. Ramesh Kumar" />
                {errors.victim_name && <p className="text-xs text-red-400 mt-1">{errors.victim_name.message}</p>}
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-zinc-400 mb-1">Mobile Number (OTP Linked)</label>
                  <input {...register('victim_phone')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:border-cyan-500 focus:outline-none" placeholder="9876543210" />
                  {errors.victim_phone && <p className="text-xs text-red-400 mt-1">{errors.victim_phone.message}</p>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-zinc-400 mb-1">Incident Date</label>
                  <input type="date" {...register('fraud_date')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:border-cyan-500 focus:outline-none" />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-1">Address & Police Jurisdiction</label>
                <input {...register('victim_address')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:border-cyan-500 focus:outline-none" placeholder="Flat, Street, City, State" />
              </div>
              <button type="button" onClick={() => setStep(2)} className="mt-4 w-full flex items-center justify-center space-x-2 py-3 bg-cyan-600 hover:bg-cyan-500 text-white font-medium rounded-lg transition-colors">
                <span>Continue to Incident Details</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-4"
            >
              <h3 className="text-sm font-semibold text-zinc-300">2. Transaction & Fraudster Details</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-zinc-400 mb-1">Amount Lost (INR)</label>
                  <input type="number" {...register('amount')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white font-mono focus:border-cyan-500 focus:outline-none" placeholder="e.g. 250000" />
                  {errors.amount && <p className="text-xs text-red-400 mt-1">{errors.amount.message}</p>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-zinc-400 mb-1">Category of Cybercrime</label>
                  <select {...register('fraud_type')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:border-cyan-500 focus:outline-none">
                    <option value="INVESTMENT_SCAM">Investment / Stock Trading Scam</option>
                    <option value="KYC_FRAUD">Bank KYC / SIM Expiry Fraud</option>
                    <option value="UPI_FRAUD">UPI / QR Code Fraud</option>
                    <option value="FAKE_JOB">Part-time / Telegram Job Scam</option>
                    <option value="PHISHING">Phishing / Impersonation</option>
                    <option value="OTHER">Other Financial Cybercrime</option>
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-zinc-400 mb-1">Fraudster UPI ID (If available)</label>
                  <input {...register('fraudster_upi')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white font-mono focus:border-cyan-500 focus:outline-none" placeholder="suspect@upi" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-zinc-400 mb-1">Fraudster Bank Account (If known)</label>
                  <input {...register('fraudster_account')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white font-mono focus:border-cyan-500 focus:outline-none" placeholder="Account number / IFSC" />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-1">Brief Narrative Description</label>
                <textarea rows={3} {...register('description')} className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2 text-white focus:border-cyan-500 focus:outline-none text-sm" placeholder="Explain what happened..." />
              </div>
              <div className="flex space-x-3 pt-2">
                <button type="button" onClick={() => setStep(1)} className="w-1/3 py-3 border border-zinc-800 text-zinc-400 hover:text-white rounded-lg flex items-center justify-center space-x-1 text-sm font-medium">
                  <ArrowLeft className="w-4 h-4" />
                  <span>Back</span>
                </button>
                <button type="button" onClick={() => setStep(3)} className="w-2/3 py-3 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg flex items-center justify-center space-x-2 text-sm font-medium">
                  <span>Review & Evidence</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          )}

          {step === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-4"
            >
              <h3 className="text-sm font-semibold text-zinc-300">3. Digital Evidence & Legal Declaration</h3>
              <div className="border-2 border-dashed border-zinc-800 hover:border-cyan-500/50 rounded-xl p-6 text-center transition-colors bg-zinc-950/50 cursor-pointer">
                <UploadCloud className="w-8 h-8 text-cyan-400 mx-auto mb-2 animate-bounce" />
                <p className="text-xs font-medium text-zinc-300">Drop screenshots, bank statements, or WhatsApp chat exports</p>
                <p className="text-[10px] text-zinc-500 mt-1">JPG, PNG, PDF up to 25MB (Auto-hashed to IPFS & Blockchain ledger)</p>
              </div>
              <div className="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/30 text-xs text-cyan-300">
                <div className="flex items-start space-x-2">
                  <Shield className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                  <p>Upon submission, an automated Indian Cybercrime Coordination Centre (I4C) alert will trigger automated account freezing and ATM patrol dispatches within 6 minutes.</p>
                </div>
              </div>
              <div className="flex space-x-3 pt-2">
                <button type="button" onClick={() => setStep(2)} className="w-1/3 py-3 border border-zinc-800 text-zinc-400 hover:text-white rounded-lg text-sm font-medium flex items-center justify-center space-x-1">
                  <ArrowLeft className="w-4 h-4" />
                  <span>Back</span>
                </button>
                <button type="submit" className="w-2/3 py-3 bg-red-600 hover:bg-red-500 text-white font-bold rounded-lg shadow-lg shadow-red-600/30 text-sm flex items-center justify-center space-x-2">
                  <CheckCircle className="w-4 h-4" />
                  <span>CONFIRM & TRANSMIT COMPLAINT</span>
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </form>
    </div>
  );
};
```

---

## 6. Master Action Plan & Implementation ToDo Checklist

This checklist defines the complete, step-by-step roadmap to transform the codebase into a unified, award-winning platform.

### Phase 1: Repository Modernization & Runtime Consolidation
- [ ] **1.1. Monorepo Alignment:** Clean up the root `pnpm-workspace.yaml` to ensure clean resolution for:
  - `apps/command-center` (HQ Investigator Portal)
  - `apps/field-dashboard` (Mobile Patrol PWA)
  - `apps/victim-portal` (Citizen Complaint Experience)
  - `apps/admin-panel` (Model Telemetry & Station Management)
  - `packages/ui-kit` (Shared UI & Design System)
- [ ] **1.2. Retire Outdated Python Sidecars:**
  - Deprecate Flask `ruma/app.py` (port 5500) and migrate simulation endpoints into the TypeScript Scenario Engine.
  - Deprecate Streamlit `dashboard/streamlit_dashboard.py` (port 8501) and port all ML curves into Tremor charts inside the Admin Panel.
- [ ] **1.3. Clean Up Duplicate Vanilla SPAs:**
  - Standardize on the modern React 19 apps as the single source of truth.
  - Configure a zero-config Vite export build so standalone HTML files can be generated automatically if offline judge review is requested.

### Phase 2: Design System & Component Library Setup
- [ ] **2.1. Integrate shadcn/ui Primitives:**
  - Install Tailwind CSS v4 and configure `@theme` variables for Dark Cyber Gov styling (`--background-void`, `--surface-hud`, `--accent-cyan`, `--alert-red`, `--success-emerald`).
  - Add core shadcn primitives into `packages/ui-kit`: `Button`, `Card`, `Badge`, `Dialog`, `Sheet`, `Tabs`, `Command`, `Tooltip`, `Table`.
- [ ] **2.2. Integrate Aceternity & Magic UI Telemetry Components:**
  - Add **Border Beam** and **Moving Border** components for active threat monitoring.
  - Add **Number Ticker** for animated live recovery stats and complaint counts.
  - Add **Shimmer Button** for the Universal Freeze action.
  - Add **Tracing Beam** for the citizen complaint progression timeline.
- [ ] **2.3. Unified Iconography:**
  - Completely replace all remaining Font Awesome dependencies in the victim portal with `lucide-react`.

### Phase 3: Citizen Victim Portal (`apps/victim-portal`)
- [ ] **3.1. 4-Step Interactive Complaint Wizard:**
  - Implement the responsive multi-step wizard using `react-hook-form` + `zod` validation.
  - Add drag-and-drop evidence upload with client-side SHA-256 hash calculation for blockchain integrity preview.
- [ ] **3.2. Real-Time Complaint Tracking Timeline:**
  - Build the dynamic status tracker (`SUBMITTED` $\to$ `AI_ANALYZING` $\to$ `ACTION_TAKEN` $\to$ `RESOLVED`).
  - Support instant WhatsApp updates simulation preview with an embedded notification card.
- [ ] **3.3. OTP Verification Modal:**
  - Create a 6-digit auto-advancing OTP input component with countdown timer.

### Phase 4: Police HQ Command Center (`apps/command-center`)
- [ ] **4.1. Replace `vis-network` with `@xyflow/react`:**
  - Build the interactive `MoneyTrailFlow` component with custom `VictimNode`, `MuleAccountNode` (Layer 1/2/3), and `AtmTargetNode`.
  - Implement animated glowing SVG edges with directional particle flow proportional to the transaction amount.
  - Add interactive node click drawers displaying IFSC, bank name, account holder name, and freeze logs.
- [ ] **4.2. Upgrade Map from Leaflet to MapLibre GL / Deck.gl:**
  - Integrate dark CartoDB vector basemaps with smooth pan/tilt navigation.
  - Render 3D extruded heatmap risk bins over high-density ATM clusters in Bengaluru / Delhi NCR.
  - Add animated pulsing radar circles around target ATMs with assigned field officer distance indicators.
- [ ] **4.3. Tactical AI Copilot Chat Interface:**
  - Implement a modern slide-over cyber AI chat interface equipped with pre-set prompt chips:
    - *"Trace source funds for UPI ID suspect@ybl"*
    - *"Draft Section 91 CrPC notice for Bank Manager"*
    - *"Identify top 3 cash-out ATM coordinates"*
- [ ] **4.4. Universal Account Freeze Action Workflow:**
  - Deploy the multi-step `UniversalFreezeButton` with confirmation modals, auditory cue, and audit log generator.

### Phase 5: Field Officer Mobile Dashboard (`apps/field-dashboard`)
- [ ] **5.1. Mobile-First PWA Shell:**
  - Implement a thumb-friendly bottom dock navigation bar: `[Alerts]`, `[Patrol Map]`, `[Comms]`, `[Profile]`.
  - Add vibration/haptic feedback simulation when an emergency high-risk alert triggers.
- [ ] **5.2. Live Intercept & Evidence Flow:**
  - Create 1-click `[I AM RESPONDING]` and `[INTERCEPT AT ATM]` action buttons that update dispatch status across the HQ Command Center in real-time.
  - Add quick-camera evidence capture preview for field officers to photograph confiscated ATM cards or suspect vehicle license plates.

### Phase 6: Admin Panel & ML Telemetry (`apps/admin-panel`)
- [ ] **6.1. Embedded Model Telemetry via Tremor:**
  - Embed live interactive loss & accuracy curves for the **STM Transformer** (Spatio-Temporal ATM predictor) and **GNN** (Mule network classifier).
  - Add real-time inference latency gauges (showing sub-80ms response times).
- [ ] **6.2. Police Station Jurisdiction & Officer Management:**
  - Dynamic table with searchable station rosters, active patrol units, and case resolution rates.

### Phase 7: Zero-Fail "Judge Demo Mode" & Final Presentation Polish
- [ ] **7.1. Integrated Scenario Runner (`demoStore.ts`):**
  - Implement the deterministic 5-minute hackathon pitch flow directly in Zustand:
    - **Minute 0-1:** Citizen files ₹5,00,000 fraud complaint $\to$ Case ID generated.
    - **Minute 1-2:** GNN detects 3-layer mule ring $\to$ STM predicts Indiranagar ATM cash-out.
    - **Minute 2-3:** HQ Command Center triggers Universal Freeze; money trail edges turn frozen blue.
    - **Minute 3-4:** Field Patrol unit receives audio chime alert $\to$ executes intercept at ATM.
    - **Minute 4-5:** Citizen portal status updates to `RESOLVED` with ₹5,00,000 recovered.
- [ ] **7.2. Production Polish & QA:**
  - Verify zero console errors, smooth 60fps animations across Chrome, Edge, Safari, and mobile viewports.
  - Conduct full end-to-end rehearsal using the unified single dev server.

---

### Conclusion & Next Immediate Step

By executing this overhaul, the platform will transform from an uncoordinated set of scripts and partial apps into an **unrivaled, production-ready, cyber-intelligence ecosystem**. All required objectives are preserved and enhanced, while demo risk is reduced to zero.

*Refer to this file as the master project roadmap during development.*

# MEMBER 4 — Victim Portal, Integration & Presentation Lead Reference

## 1. Role Overview
- Member 4 builds the citizen-facing Victim Complaint Portal, handles integration testing, QA, and leads the presentation/demo.
- Has **NO GPU** access.
- Title: **Victim Portal, Integration & Presentation Lead**

## 2. Core Responsibilities
| Responsibility | Description |
| :--- | :--- |
| **Victim Complaint Portal (PWA)** | Citizen-facing application for reporting cybercrimes. |
| **UI/UX Designs & Wireframes** | Ensuring highly usable, intuitive user experiences. |
| **Integration Testing** | Testing across all apps to ensure flawless pipeline flow. |
| **QA & Cross-Browser Testing** | Quality assurance across modern browsers (Chrome, Firefox, Safari, Edge) and mobile. |
| **Demo Presentation** | Leads the demo. Speaks FIRST and LAST in the 5-min demo. |
| **Flask Presentation Demo App** | Standalone demo application (`ruma/`) for visualizing systems. |
| **Streamlit ML Dashboard** | Training dashboard for visualizing AI/ML metrics. |
| **Root Landing Portal** | Central entry point (`index.html`) linking all platform dashboards. |
| **Consistent Design System** | Usage of components shared with Member 3 for UI consistency. |

## 3. Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (standalone), React 19 + TypeScript (monorepo `victim-portal`)
- **Demo**: Python 3, Flask, Chart.js 4.4
- **ML Dashboard**: Streamlit 1.28, Plotly 5.18, PyTorch
- **Shared**: `@sih/ui-kit` from Member 3, Tailwind CSS, Font Awesome 6.5

## 4. What Has Been Built (Current Status)

### 4.1 Victim Dashboard (Standalone) — COMPLETE
**Path**: `victim-dashboard/`
- `index.html` + `css/style.css` — Complete citizen-facing portal with:
  - **Header**: CyberCell shield brand, language selector (EN), 1930 helpline click-to-call.
  - **Hero section**: "Lost Money to Cybercrime?" banner, live counter (47 complaints today, ₹8.2Cr recovered).
  - **4-Step Complaint Form Wizard**:
    1. *Personal Details*: Full name, 10-digit mobile, optional email, address.
    2. *Fraud Details*: Amount (INR), date, time, fraud category dropdown (Investment Scam, KYC Fraud, UPI Fraud, Fake Job Offer, Phishing, Other), description.
    3. *Fraudster Details*: UPI ID, bank account, phone number, drag-and-drop file upload (JPG, PNG, PDF, max 10MB).
    4. *Review & Submit*: Summary review card, legal accuracy confirmation checkbox.
  - **Live Complaint Status Tracker** (post-submission): Unique Complaint ID (CC-2026-XXXX), 4-stage timeline (Submitted → AI Analyzing → Action Taken → Resolved), live updates feed.
  - **Legal & Help Modals**: Privacy Policy (encryption, blockchain hashing, rights), Terms of Service, Contact Support (helplines 1930 & 112).
- `js/main.js` (517 lines) — Form validation (regex phone checks, required fields, amount bounds), drag-and-drop upload with file size/type validation, auto-populated review screen, submission generates complaint ID, simulated real-time status progression (Submitted → AI Analyzing after 4s → Action Taken after 10s).
- **Technology**: HTML5, CSS3, Font Awesome 6.5, Inter font, Vanilla JS.
- **Current State**: COMPLETE and fully interactive.

### 4.2 Root Landing Portal — COMPLETE
**Path**: `index.html`
- Central landing page for the National Cyber Crime Reporting & Intelligence Portal ("CyberCell").
- Hero header with system operational status badge.
- **3 gateway cards**:
  - Report a Cybercrime → `victim-dashboard/index.html`
  - Investigator Command Center → `police-command/index.html`
  - Field Officer Dashboard → `police-field/index.html`
- **Quick stats strip**: 2,847 complaints, 1,203 resolved, ₹8.2Cr recovered, 94% satisfaction.
- Emergency 1930 helpline banner.
- 5 interactive modals: About, Privacy Policy, Terms, Contact Support, FAQ.
- **Technology**: HTML5, CSS3, Font Awesome 6.5, Inter font, Vanilla JS.

### 4.3 Flask Presentation Demo (`ruma/`) — COMPLETE
**Path**: `ruma/app.py` (1,054 lines)
- Standalone single-file presentation demo server (port 5500).
- Dark glassmorphism dashboard with tabs: Live Training, ATM Prediction Map, Mule Detection Network, Real-Time Scoring, System Health.
- **Endpoints**:
  - `/api/training/start/<model_type>` & `/api/training/status/<model_type>` — Simulates mathematical loss/accuracy decay for STM (200 epochs) and GNN (100 epochs).
  - `/api/atms` — Generates 500 Bengaluru ATM coordinates with bank assignments and risk ratings.
  - `/api/predict/demo` — Top predicted ATMs with latency metrics (~20-80ms).
  - `/api/detect/demo` — GNN probability + rule score → risk level + action recommendation.
  - `/api/system/stats` — CPU, RAM, GPU VRAM, request volume, error rates.
- **Technology**: Python 3, Flask, embedded HTML/CSS, Chart.js 4.4.
- **Run**: `python ruma/app.py`

### 4.4 Streamlit ML Dashboard — COMPLETE
**Path**: `dashboard/streamlit_dashboard.py`
- Real-time web dashboard for PyTorch model training visualization.
- Sidebar: Select model (STM ~4.6M params or GNN ~98K params), Start/Stop Training, configure epochs/batch/LR/device.
- Interactive Plotly training/validation loss curves.
- Accuracy metrics: Train Acc, Val Acc (Top-1), Top-3, Top-5.
- LR schedule and gradient norm monitoring.
- Model architecture tabs with parameter count tables.
- Real-time hardware telemetry: GPU name, VRAM, CPU%, RAM.
- **Technology**: Streamlit 1.28, Plotly 5.18, PyTorch, TensorBoard, psutil.
- **Run**: `streamlit run dashboard/streamlit_dashboard.py`

### 4.5 Victim Portal in Monorepo — STUB
**Path**: `apps/victim-portal/`
- Currently Vite boilerplate (default starter template).
- This is where the React 19 version of the victim portal should eventually live.
- Consumes `@sih/ui-kit` from Member 3.

## 5. Demo Presentation Script
Member 4 speaks **FIRST** and **LAST** in the 5-minute demo:

### [0:00 - 1:00] Member 4: The Hook & Victim Flow
- Open the problem: "Every 3 seconds, someone in India loses money to cybercrime..."
- Live demo: file a complaint through the victim portal (`victim-dashboard`).
- Show the 4-step wizard, submit, see complaint ID generated.
- Show real-time status updates appearing.

### [1:00 - 2:30] Member 1: AI/ML Engine
- Show training dashboard (Streamlit or Flask demo).
- Explain STM Transformer predicting ATM locations.
- Explain GNN detecting mule accounts.

### [2:30 - 3:30] Member 2: Backend Architecture
- Show API endpoints, database schemas.
- Explain blockchain audit trail.
- Show WebSocket real-time updates.

### [3:30 - 4:30] Member 3: Police Dashboards
- Show Command Center heatmap, money trail graph.
- Show Field Dashboard alerts on mobile.
- Show the "Intercept" workflow.

### [4:30 - 5:00] Member 4: The Close
- Circle back to the victim's complaint.
- Show it progressed through the pipeline.
- End with impact: "This system turns a 6-hour head start into a 6-minute response."

## 6. Integration Points With Other Members

### 6.1 With Member 1 (AI/ML Lead)
- Victim Portal complaints trigger Member 1's ML pipeline.
- Flask demo (`ruma/app.py`) simulates Member 1's training curves and predictions for presentation.
- Streamlit dashboard reads Member 1's model artifacts and training logs.
- 1 "live" complaint is queued up for Member 4 to submit during the demo, triggering a "Scatter Strategy" prediction.

### 6.2 With Member 2 (Backend & Database)
- Victim Portal submits complaints via `POST /api/v1/victim/complaints`.
- Status tracker polls `GET /api/v1/victim/complaints/{id}/status`.
- WhatsApp chatbot backend (Member 2) supports citizen-side queries.
- OTP verification via `POST /api/v1/auth/otp/send` and `/otp/verify`.

### 6.3 With Member 3 (Frontend & DevOps)
- Member 4 consumes `@sih/ui-kit` (shared component library).
- The `ui-kit` public API is the contract — Member 3 maintains it, Member 4 builds on it.
- If Member 4 migrates from standalone to monorepo, use `apps/victim-portal/`.
- Design tokens (`tokens.css`), Button, Card, Badge components are shared.
- Member 3 does **NOT** touch `victim-dashboard/` or `ruma/` — those are Member 4's territory.

## 7. API Endpoints Member 4 Consumes

| Method | Path | Description |
| :--- | :--- | :--- |
| POST | `/api/v1/victim/complaints` | Submit new complaint |
| GET | `/api/v1/victim/complaints/{id}/status` | Check complaint status |
| POST | `/api/v1/auth/otp/send` | Request OTP for victim auth |
| POST | `/api/v1/auth/otp/verify` | Verify OTP |
| POST | `/api/v1/evidence/upload` | Upload evidence files |
| GET | `/api/v1/victim/complaints/{id}/updates` | Get status updates feed |

## 8. Complaint Data Schema
Fields the victim portal sends:
- `victim_name` (string, required)
- `victim_phone` (string, 10 digits, required)
- `victim_email` (string, optional)
- `victim_address` (string, required)
- `amount` (float, INR, required)
- `fraud_date` (date, required)
- `fraud_time` (string, approximate, required)
- `fraud_type` (enum: INVESTMENT_SCAM, KYC_FRAUD, UPI_FRAUD, FAKE_JOB, PHISHING, OTHER)
- `description` (string, required)
- `fraudster_upi` (string, optional)
- `fraudster_account` (string, optional)
- `fraudster_phone` (string, optional)
- `evidence_files` (File[], optional, max 10MB each, JPG/PNG/PDF)

**Complaint Status Lifecycle**:
`SUBMITTED` → `AI_ANALYZING` → `ACTION_TAKEN` → `RESOLVED`

## 9. File Structure Member 4 Owns
```
victim-dashboard/
├── index.html
├── css/
│   └── style.css
└── js/
    └── main.js
ruma/
└── app.py
dashboard/
├── streamlit_dashboard.py
└── requirements.txt
index.html (root landing portal)
apps/victim-portal/ (monorepo stub — for React 19 migration)
```

## 10. Commands to Run
```bash
# Open standalone victim portal (no build needed)
# Just open victim-dashboard/index.html in browser

# Open root landing portal
# Just open index.html in browser

# Start Flask demo
python ruma/app.py
# → http://localhost:5500

# Start Streamlit dashboard
streamlit run dashboard/streamlit_dashboard.py
# → http://localhost:8501

# Start monorepo victim portal (if migrated)
pnpm --filter ./apps/victim-portal dev
# → http://localhost:3000
```

## 11. What's Remaining / TODO
- Migrate standalone `victim-dashboard/` to React 19 monorepo (`apps/victim-portal/`) using `@sih/ui-kit`.
- Connect victim portal to real backend API instead of client-side simulation.
- Implement real file upload to IPFS via backend evidence endpoint.
- Connect WhatsApp chatbot flow to backend webhook.
- Polish demo presentation script and rehearse timing.
- Cross-browser testing on Chrome, Firefox, Safari, Edge.
- Mobile responsiveness testing for victim portal.

## 12. Important Notes
- The standalone `victim-dashboard/` works immediately by opening in browser — **NO build step needed**.
- The Flask demo (`ruma/app.py`) is a **SIMULATION** — it generates fake training curves and predictions for demo purposes only.
- The Streamlit dashboard connects to real PyTorch if models are available, but also works with simulated data.
- Member 4 has **NO GPU** — all compute-heavy work is delegated to Member 1.
- The root `index.html` is the main entry point judges will see first.

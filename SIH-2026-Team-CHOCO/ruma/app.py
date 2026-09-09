"""
RUMA — Demo Dashboard for SIH26184 Cybercrime Prediction System
================================================================
A standalone demo dashboard that displays:
  - Live model training simulation with animated metrics
  - ATM prediction map with Bangalore heatmap
  - Mule detection network visualization
  - Real-time scoring system demo
  - System health / performance stats

Run:  python ruma/app.py
Open: http://localhost:5500

NOTE: This is a DEMO file for presentation. Delete after combining with real frontend.
"""

import os
import sys
import json
import math
import time
import random
import threading
from pathlib import Path
from datetime import datetime, timedelta

from flask import Flask, render_template_string, jsonify, request

# Add project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

app = Flask(__name__)

# ============================================================================
# SIMULATED TRAINING STATE
# ============================================================================

training_state = {
    "stm": {
        "status": "idle",  # idle | training | completed
        "current_epoch": 0,
        "total_epochs": 200,
        "train_loss": [],
        "val_loss": [],
        "val_accuracy": [],
        "top3_accuracy": [],
        "lr": 0.0001,
        "best_val_acc": 0.0,
        "start_time": None,
    },
    "gnn": {
        "status": "idle",
        "current_epoch": 0,
        "total_epochs": 100,
        "train_loss": [],
        "val_loss": [],
        "val_f1": [],
        "val_auc": [],
        "lr": 0.001,
        "best_val_f1": 0.0,
        "start_time": None,
    },
}

# Pre-generate realistic training curves
def _generate_stm_curves():
    """Generate realistic STM training curves."""
    epochs = 200
    train_loss, val_loss, val_acc, top3 = [], [], [], []
    for e in range(epochs):
        t = e / epochs
        tl = 6.2 * math.exp(-3.5 * t) + 0.8 + random.gauss(0, 0.05)
        vl = 6.2 * math.exp(-3.0 * t) + 0.9 + random.gauss(0, 0.08)
        va = min(100, 15 + 75 * (1 - math.exp(-4 * t)) + random.gauss(0, 1.5))
        t3 = min(100, 40 + 58 * (1 - math.exp(-5 * t)) + random.gauss(0, 0.8))
        train_loss.append(round(max(0.3, tl), 4))
        val_loss.append(round(max(0.4, vl), 4))
        val_acc.append(round(max(10, va), 2))
        top3.append(round(max(30, t3), 2))
    return train_loss, val_loss, val_acc, top3


def _generate_gnn_curves():
    """Generate realistic GNN training curves."""
    epochs = 100
    train_loss, val_loss, val_f1, val_auc = [], [], [], []
    for e in range(epochs):
        t = e / epochs
        tl = 0.7 * math.exp(-4 * t) + 0.05 + random.gauss(0, 0.01)
        vl = 0.7 * math.exp(-3.5 * t) + 0.08 + random.gauss(0, 0.015)
        f1 = min(1.0, 0.4 + 0.55 * (1 - math.exp(-5 * t)) + random.gauss(0, 0.015))
        au = min(1.0, 0.5 + 0.48 * (1 - math.exp(-6 * t)) + random.gauss(0, 0.01))
        train_loss.append(round(max(0.02, tl), 4))
        val_loss.append(round(max(0.04, vl), 4))
        val_f1.append(round(max(0.3, f1), 4))
        val_auc.append(round(max(0.4, au), 4))
    return train_loss, val_loss, val_f1, val_auc


stm_tl, stm_vl, stm_va, stm_t3 = _generate_stm_curves()
gnn_tl, gnn_vl, gnn_f1, gnn_auc = _generate_gnn_curves()

# Pre-generate ATM data for the map
atm_data = []
random.seed(42)
for i in range(500):
    lat = 12.8 + random.uniform(0, 0.4)
    lon = 77.4 + random.uniform(0, 0.4)
    risk = random.uniform(0, 100)
    atm_data.append({
        "id": f"A{i:04d}",
        "lat": round(lat, 6),
        "lon": round(lon, 6),
        "risk": round(risk, 1),
        "bank": random.choice(["SBI", "HDFC", "ICICI", "AXIS", "KOTAK"]),
        "fraud_count": random.randint(0, 12),
    })


# ============================================================================
# API ROUTES
# ============================================================================

@app.route("/api/training/start/<model_type>", methods=["POST"])
def start_training(model_type):
    if model_type not in ("stm", "gnn"):
        return jsonify({"error": "Invalid model type"}), 400

    state = training_state[model_type]
    state["status"] = "training"
    state["current_epoch"] = 0
    state["train_loss"] = []
    state["val_loss"] = []
    state["start_time"] = datetime.utcnow().isoformat()

    if model_type == "stm":
        state["val_accuracy"] = []
        state["top3_accuracy"] = []
        state["best_val_acc"] = 0.0
    else:
        state["val_f1"] = []
        state["val_auc"] = []
        state["best_val_f1"] = 0.0

    return jsonify({"status": "started", "model": model_type})


@app.route("/api/training/status/<model_type>")
def get_training_status(model_type):
    if model_type not in ("stm", "gnn"):
        return jsonify({"error": "Invalid model type"}), 400

    state = training_state[model_type]

    if state["status"] == "training":
        epoch = state["current_epoch"]
        total = state["total_epochs"]

        if model_type == "stm" and epoch < total:
            state["train_loss"].append(stm_tl[epoch])
            state["val_loss"].append(stm_vl[epoch])
            state["val_accuracy"].append(stm_va[epoch])
            state["top3_accuracy"].append(stm_t3[epoch])
            state["best_val_acc"] = max(state["best_val_acc"], stm_va[epoch])
            state["lr"] = 0.0001 * (0.5 ** (epoch // 40))
            state["current_epoch"] = epoch + 1
        elif model_type == "gnn" and epoch < total:
            state["train_loss"].append(gnn_tl[epoch])
            state["val_loss"].append(gnn_vl[epoch])
            state["val_f1"].append(gnn_f1[epoch])
            state["val_auc"].append(gnn_auc[epoch])
            state["best_val_f1"] = max(state["best_val_f1"], gnn_f1[epoch])
            state["lr"] = 0.001 * (0.5 ** (epoch // 20))
            state["current_epoch"] = epoch + 1

        if state["current_epoch"] >= total:
            state["status"] = "completed"

    return jsonify(state)


@app.route("/api/atms")
def get_atms():
    return jsonify(atm_data)


@app.route("/api/predict/demo", methods=["POST"])
def demo_predict():
    """Demo ATM prediction."""
    top_k = request.json.get("top_k", 3) if request.json else 3
    sorted_atms = sorted(atm_data, key=lambda a: a["risk"], reverse=True)
    predictions = []
    for i, atm in enumerate(sorted_atms[:top_k]):
        predictions.append({
            "atm_id": atm["id"],
            "probability": round(random.uniform(0.3, 0.95) if i == 0 else random.uniform(0.05, 0.3), 4),
            "lat": atm["lat"],
            "lon": atm["lon"],
            "risk": atm["risk"],
            "bank": atm["bank"],
        })
    return jsonify({"predictions": predictions, "latency_ms": round(random.uniform(20, 80), 1)})


@app.route("/api/detect/demo", methods=["POST"])
def demo_detect():
    """Demo mule detection."""
    gnn_prob = round(random.uniform(0.1, 0.99), 4)
    rule_score = round(random.uniform(10, 95), 2)
    final_score = round(0.7 * gnn_prob * 100 + 0.3 * rule_score, 2)
    if final_score >= 80:
        level, color, action = "HIGH", "#ef4444", "Immediate Freeze + Step-Up Verification"
    elif final_score >= 50:
        level, color, action = "MEDIUM", "#f59e0b", "Enhanced Monitoring + Alert"
    else:
        level, color, action = "LOW", "#22c55e", "No Action"

    return jsonify({
        "account_id": f"M{random.randint(1,50):04d}_{random.randint(1,5)}",
        "gnn_probability": gnn_prob,
        "rule_score": rule_score,
        "final_score": final_score,
        "risk_level": level,
        "risk_color": color,
        "action": action,
        "latency_ms": round(random.uniform(10, 50), 1),
    })


@app.route("/api/system/stats")
def system_stats():
    return jsonify({
        "api_requests": random.randint(5000, 15000),
        "avg_latency_ms": round(random.uniform(25, 75), 1),
        "error_rate": round(random.uniform(0.01, 0.5), 2),
        "uptime_hours": round(random.uniform(24, 720), 1),
        "models_loaded": {"stm": True, "gnn": True},
        "gpu_memory_used_mb": random.randint(800, 3500),
        "gpu_memory_total_mb": 8192,
        "cpu_usage_pct": round(random.uniform(10, 65), 1),
        "ram_usage_pct": round(random.uniform(30, 70), 1),
    })


# ============================================================================
# MAIN PAGE
# ============================================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIH26184 — Cybercrime Prediction Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: #1a1f2e;
            --bg-card-hover: #222838;
            --border: #2d3548;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-purple: #8b5cf6;
            --accent-green: #22c55e;
            --accent-orange: #f59e0b;
            --accent-red: #ef4444;
            --accent-pink: #ec4899;
            --glow-blue: 0 0 20px rgba(59, 130, 246, 0.3);
            --glow-purple: 0 0 20px rgba(139, 92, 246, 0.3);
            --glow-green: 0 0 20px rgba(34, 197, 94, 0.3);
            --radius: 12px;
            --radius-sm: 8px;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Ambient background */
        body::before {
            content: '';
            position: fixed;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle at 20% 30%, rgba(59,130,246,0.06) 0%, transparent 50%),
                        radial-gradient(circle at 80% 70%, rgba(139,92,246,0.06) 0%, transparent 50%),
                        radial-gradient(circle at 50% 50%, rgba(6,182,212,0.03) 0%, transparent 50%);
            z-index: 0;
            pointer-events: none;
        }

        .app { position: relative; z-index: 1; }

        /* Header */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 32px;
            background: rgba(17, 24, 39, 0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header-left { display: flex; align-items: center; gap: 16px; }
        .logo {
            width: 40px; height: 40px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 900; font-size: 18px; color: white;
        }
        .header h1 { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
        .header h1 span { color: var(--accent-cyan); }
        .header-badge {
            padding: 4px 12px;
            background: rgba(34, 197, 94, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }

        /* Nav Tabs */
        .nav-tabs {
            display: flex;
            gap: 4px;
            padding: 12px 32px;
            background: rgba(17, 24, 39, 0.5);
            border-bottom: 1px solid var(--border);
        }
        .nav-tab {
            padding: 8px 20px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-family: inherit;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            border-radius: var(--radius-sm);
            transition: all 0.2s;
        }
        .nav-tab:hover { color: var(--text-primary); background: rgba(255,255,255,0.05); }
        .nav-tab.active {
            color: var(--accent-blue);
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        /* Content */
        .content { padding: 24px 32px; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* Cards */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 24px;
            transition: all 0.3s;
        }
        .card:hover { border-color: rgba(59, 130, 246, 0.3); }
        .card-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }

        /* Grid */
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
        .mb-20 { margin-bottom: 20px; }
        .mb-24 { margin-bottom: 24px; }

        /* Stat cards */
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            position: relative;
            overflow: hidden;
        }
        .stat-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            border-radius: var(--radius) var(--radius) 0 0;
        }
        .stat-card.blue::after { background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)); }
        .stat-card.purple::after { background: linear-gradient(90deg, var(--accent-purple), var(--accent-pink)); }
        .stat-card.green::after { background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan)); }
        .stat-card.orange::after { background: linear-gradient(90deg, var(--accent-orange), var(--accent-red)); }
        .stat-label { font-size: 12px; color: var(--text-muted); font-weight: 500; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
        .stat-value { font-size: 28px; font-weight: 800; line-height: 1; }
        .stat-value.blue { color: var(--accent-blue); }
        .stat-value.purple { color: var(--accent-purple); }
        .stat-value.green { color: var(--accent-green); }
        .stat-value.orange { color: var(--accent-orange); }
        .stat-sub { font-size: 12px; color: var(--text-muted); margin-top: 6px; }

        /* Buttons */
        .btn {
            padding: 10px 24px;
            border: none;
            border-radius: var(--radius-sm);
            font-family: inherit;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-primary {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: white;
            box-shadow: var(--glow-blue);
        }
        .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 0 30px rgba(59,130,246,0.5); }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .btn-green {
            background: linear-gradient(135deg, var(--accent-green), #059669);
            color: white;
            box-shadow: var(--glow-green);
        }
        .btn-green:hover { transform: translateY(-1px); }
        .btn-green:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

        /* Progress bar */
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.05);
            border-radius: 4px;
            overflow: hidden;
            margin: 12px 0;
        }
        .progress-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        .progress-fill.blue { background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)); }
        .progress-fill.green { background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan)); }

        /* Training controls */
        .training-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }
        .training-header h3 { font-size: 16px; font-weight: 700; }
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .status-idle { background: rgba(100,116,139,0.15); color: var(--text-muted); border: 1px solid rgba(100,116,139,0.3); }
        .status-training { background: rgba(59,130,246,0.15); color: var(--accent-blue); border: 1px solid rgba(59,130,246,0.3); animation: pulse 2s infinite; }
        .status-completed { background: rgba(34,197,94,0.15); color: var(--accent-green); border: 1px solid rgba(34,197,94,0.3); }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        /* Charts */
        .chart-container { position: relative; height: 280px; }

        /* Risk gauge */
        .risk-gauge {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 24px;
        }
        .gauge-value {
            font-size: 64px;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 8px;
        }
        .gauge-label { font-size: 14px; color: var(--text-secondary); margin-bottom: 16px; }
        .gauge-bar {
            width: 100%;
            height: 12px;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-orange), var(--accent-red));
            border-radius: 6px;
            position: relative;
            margin-bottom: 8px;
        }
        .gauge-marker {
            position: absolute;
            top: -4px;
            width: 4px;
            height: 20px;
            background: white;
            border-radius: 2px;
            transition: left 0.5s ease;
        }

        /* Table */
        .data-table {
            width: 100%;
            border-collapse: collapse;
        }
        .data-table th, .data-table td {
            text-align: left;
            padding: 10px 16px;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
        }
        .data-table th {
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.5px;
        }
        .data-table tr:hover td { background: rgba(255,255,255,0.02); }
        .risk-badge {
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }
        .risk-high { background: rgba(239,68,68,0.15); color: var(--accent-red); }
        .risk-medium { background: rgba(245,158,11,0.15); color: var(--accent-orange); }
        .risk-low { background: rgba(34,197,94,0.15); color: var(--accent-green); }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

        @media (max-width: 1024px) {
            .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
            .content { padding: 16px; }
        }
    </style>
</head>
<body>
<div class="app">
    <!-- Header -->
    <header class="header">
        <div class="header-left">
            <div class="logo">S</div>
            <h1>SIH<span>26184</span> — Cybercrime Prediction</h1>
        </div>
        <div class="header-badge">● System Online</div>
    </header>

    <!-- Nav -->
    <nav class="nav-tabs">
        <button class="nav-tab active" data-tab="training">📊 Model Training</button>
        <button class="nav-tab" data-tab="predictions">🎯 ATM Predictions</button>
        <button class="nav-tab" data-tab="mule">🕵️ Mule Detection</button>
        <button class="nav-tab" data-tab="system">⚡ System Stats</button>
    </nav>

    <!-- Content -->
    <main class="content">

        <!-- ============================================================ -->
        <!-- TAB 1: MODEL TRAINING -->
        <!-- ============================================================ -->
        <div id="tab-training" class="tab-content active">
            <!-- STM Training -->
            <div class="card mb-24">
                <div class="training-header">
                    <h3>🧠 Spatio-Temporal Transformer</h3>
                    <div style="display:flex;gap:12px;align-items:center;">
                        <span id="stm-status" class="status-badge status-idle">IDLE</span>
                        <button id="btn-train-stm" class="btn btn-primary" onclick="startTraining('stm')">▶ Start Training</button>
                    </div>
                </div>
                <div class="grid-4 mb-20">
                    <div class="stat-card blue"><div class="stat-label">Epoch</div><div id="stm-epoch" class="stat-value blue">0 / 200</div></div>
                    <div class="stat-card purple"><div class="stat-label">Val Accuracy</div><div id="stm-acc" class="stat-value purple">—</div></div>
                    <div class="stat-card green"><div class="stat-label">Top-3 Accuracy</div><div id="stm-top3" class="stat-value green">—</div></div>
                    <div class="stat-card orange"><div class="stat-label">Learning Rate</div><div id="stm-lr" class="stat-value orange">1e-4</div></div>
                </div>
                <div class="progress-bar"><div id="stm-progress" class="progress-fill blue" style="width:0%"></div></div>
                <div class="grid-2" style="margin-top:20px;">
                    <div class="card"><div class="card-title">Loss Curves</div><div class="chart-container"><canvas id="stm-loss-chart"></canvas></div></div>
                    <div class="card"><div class="card-title">Accuracy Curves</div><div class="chart-container"><canvas id="stm-acc-chart"></canvas></div></div>
                </div>
            </div>

            <!-- GNN Training -->
            <div class="card">
                <div class="training-header">
                    <h3>🕸️ Graph Neural Network (Mule Detection)</h3>
                    <div style="display:flex;gap:12px;align-items:center;">
                        <span id="gnn-status" class="status-badge status-idle">IDLE</span>
                        <button id="btn-train-gnn" class="btn btn-green" onclick="startTraining('gnn')">▶ Start Training</button>
                    </div>
                </div>
                <div class="grid-4 mb-20">
                    <div class="stat-card blue"><div class="stat-label">Epoch</div><div id="gnn-epoch" class="stat-value blue">0 / 100</div></div>
                    <div class="stat-card purple"><div class="stat-label">Val F1-Score</div><div id="gnn-f1" class="stat-value purple">—</div></div>
                    <div class="stat-card green"><div class="stat-label">Val AUC-ROC</div><div id="gnn-auc" class="stat-value green">—</div></div>
                    <div class="stat-card orange"><div class="stat-label">Learning Rate</div><div id="gnn-lr" class="stat-value orange">1e-3</div></div>
                </div>
                <div class="progress-bar"><div id="gnn-progress" class="progress-fill green" style="width:0%"></div></div>
                <div class="grid-2" style="margin-top:20px;">
                    <div class="card"><div class="card-title">Loss Curves</div><div class="chart-container"><canvas id="gnn-loss-chart"></canvas></div></div>
                    <div class="card"><div class="card-title">F1 / AUC Curves</div><div class="chart-container"><canvas id="gnn-metric-chart"></canvas></div></div>
                </div>
            </div>
        </div>

        <!-- ============================================================ -->
        <!-- TAB 2: ATM PREDICTIONS -->
        <!-- ============================================================ -->
        <div id="tab-predictions" class="tab-content">
            <div class="grid-2 mb-24">
                <div class="card">
                    <div class="card-title">Run ATM Prediction</div>
                    <p style="color:var(--text-secondary);margin-bottom:16px;font-size:14px;">
                        Submit a complaint's spatial/temporal context to predict the top ATM withdrawal locations.
                    </p>
                    <button class="btn btn-primary" onclick="runPrediction()">🎯 Run Prediction</button>
                    <div id="prediction-result" style="margin-top:20px;"></div>
                </div>
                <div class="card">
                    <div class="card-title">Top Predicted ATMs</div>
                    <table class="data-table">
                        <thead><tr><th>Rank</th><th>ATM ID</th><th>Probability</th><th>Bank</th><th>Risk</th></tr></thead>
                        <tbody id="prediction-table"><tr><td colspan="5" style="color:var(--text-muted);text-align:center;">Click "Run Prediction" to see results</td></tr></tbody>
                    </table>
                </div>
            </div>
            <div class="card">
                <div class="card-title">ATM Risk Heatmap — Bangalore (500 ATMs)</div>
                <div id="atm-map" style="height:400px;display:flex;align-items:center;justify-content:center;">
                    <canvas id="atm-canvas" width="800" height="400"></canvas>
                </div>
            </div>
        </div>

        <!-- ============================================================ -->
        <!-- TAB 3: MULE DETECTION -->
        <!-- ============================================================ -->
        <div id="tab-mule" class="tab-content">
            <div class="grid-3 mb-24">
                <div class="card" style="grid-column: span 2;">
                    <div class="card-title">Mule Account Scorer</div>
                    <p style="color:var(--text-secondary);margin-bottom:16px;font-size:14px;">
                        Analyze an account using GNN + Hybrid Scoring to determine mule risk.
                    </p>
                    <button class="btn btn-primary" onclick="runMuleDetection()">🕵️ Analyze Account</button>
                    <div id="mule-result" style="margin-top:20px;"></div>
                    <div id="mule-history" style="margin-top:20px;">
                        <table class="data-table">
                            <thead><tr><th>Account</th><th>GNN Prob</th><th>Rule Score</th><th>Final</th><th>Risk</th><th>Action</th></tr></thead>
                            <tbody id="mule-table"></tbody>
                        </table>
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">Risk Gauge</div>
                    <div class="risk-gauge">
                        <div id="gauge-value" class="gauge-value" style="color:var(--text-muted);">—</div>
                        <div id="gauge-label" class="gauge-label">No analysis yet</div>
                        <div class="gauge-bar">
                            <div id="gauge-marker" class="gauge-marker" style="left:0%"></div>
                        </div>
                        <div style="display:flex;justify-content:space-between;width:100%;font-size:11px;color:var(--text-muted);">
                            <span>LOW</span><span>MEDIUM</span><span>HIGH</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================ -->
        <!-- TAB 4: SYSTEM STATS -->
        <!-- ============================================================ -->
        <div id="tab-system" class="tab-content">
            <div class="grid-4 mb-24">
                <div class="stat-card blue"><div class="stat-label">API Requests</div><div id="sys-requests" class="stat-value blue">—</div></div>
                <div class="stat-card green"><div class="stat-label">Avg Latency</div><div id="sys-latency" class="stat-value green">—</div></div>
                <div class="stat-card orange"><div class="stat-label">Error Rate</div><div id="sys-errors" class="stat-value orange">—</div></div>
                <div class="stat-card purple"><div class="stat-label">Uptime</div><div id="sys-uptime" class="stat-value purple">—</div></div>
            </div>
            <div class="grid-2">
                <div class="card">
                    <div class="card-title">GPU / CPU Usage</div>
                    <div class="chart-container"><canvas id="sys-usage-chart"></canvas></div>
                </div>
                <div class="card">
                    <div class="card-title">Model Information</div>
                    <table class="data-table">
                        <thead><tr><th>Model</th><th>Status</th><th>Parameters</th><th>Target</th></tr></thead>
                        <tbody>
                            <tr>
                                <td>Spatio-Temporal Transformer</td>
                                <td><span class="risk-badge risk-low">LOADED</span></td>
                                <td>~2.1M</td>
                                <td>>85% Top-1 Accuracy</td>
                            </tr>
                            <tr>
                                <td>Mule Detection GNN</td>
                                <td><span class="risk-badge risk-low">LOADED</span></td>
                                <td>~500K</td>
                                <td>>90% F1-Score</td>
                            </tr>
                            <tr>
                                <td>Hybrid Scorer</td>
                                <td><span class="risk-badge risk-low">ACTIVE</span></td>
                                <td>N/A (Rule-based)</td>
                                <td>70% GNN + 30% Rules</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>
</div>

<script>
    // ================================================================
    // Tab Switching
    // ================================================================
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
        });
    });

    // ================================================================
    // Chart.js Defaults
    // ================================================================
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.borderColor = '#2d3548';
    Chart.defaults.font.family = 'Inter';

    // ================================================================
    // Training Charts
    // ================================================================
    const stmLossChart = new Chart(document.getElementById('stm-loss-chart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                { label: 'Train Loss', data: [], borderColor: '#3b82f6', borderWidth: 2, pointRadius: 0, tension: 0.3 },
                { label: 'Val Loss', data: [], borderColor: '#f59e0b', borderWidth: 2, pointRadius: 0, tension: 0.3 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { position: 'top' } }, scales: { y: { beginAtZero: false } } }
    });

    const stmAccChart = new Chart(document.getElementById('stm-acc-chart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                { label: 'Val Accuracy (%)', data: [], borderColor: '#8b5cf6', borderWidth: 2, pointRadius: 0, tension: 0.3 },
                { label: 'Top-3 Accuracy (%)', data: [], borderColor: '#22c55e', borderWidth: 2, pointRadius: 0, tension: 0.3 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { position: 'top' } }, scales: { y: { min: 0, max: 100 } } }
    });

    const gnnLossChart = new Chart(document.getElementById('gnn-loss-chart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                { label: 'Train Loss', data: [], borderColor: '#22c55e', borderWidth: 2, pointRadius: 0, tension: 0.3 },
                { label: 'Val Loss', data: [], borderColor: '#f59e0b', borderWidth: 2, pointRadius: 0, tension: 0.3 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { position: 'top' } }, scales: { y: { beginAtZero: false } } }
    });

    const gnnMetricChart = new Chart(document.getElementById('gnn-metric-chart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                { label: 'F1-Score', data: [], borderColor: '#8b5cf6', borderWidth: 2, pointRadius: 0, tension: 0.3 },
                { label: 'AUC-ROC', data: [], borderColor: '#06b6d4', borderWidth: 2, pointRadius: 0, tension: 0.3 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { position: 'top' } }, scales: { y: { min: 0, max: 1 } } }
    });

    // System usage chart
    const sysUsageChart = new Chart(document.getElementById('sys-usage-chart'), {
        type: 'doughnut',
        data: {
            labels: ['GPU Used', 'GPU Free', 'CPU Used', 'CPU Free'],
            datasets: [{
                data: [40, 60, 30, 70],
                backgroundColor: ['#3b82f6', 'rgba(59,130,246,0.1)', '#8b5cf6', 'rgba(139,92,246,0.1)'],
                borderWidth: 0
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
    });

    // ================================================================
    // Training Logic
    // ================================================================
    let trainingTimers = { stm: null, gnn: null };

    function startTraining(model) {
        fetch('/api/training/start/' + model, { method: 'POST' });
        document.getElementById('btn-train-' + model).disabled = true;
        pollTraining(model);
    }

    function pollTraining(model) {
        if (trainingTimers[model]) clearInterval(trainingTimers[model]);
        trainingTimers[model] = setInterval(async () => {
            const resp = await fetch('/api/training/status/' + model);
            const data = await resp.json();
            updateTrainingUI(model, data);
            if (data.status === 'completed') {
                clearInterval(trainingTimers[model]);
                document.getElementById('btn-train-' + model).disabled = false;
            }
        }, 150);
    }

    function updateTrainingUI(model, data) {
        const statusEl = document.getElementById(model + '-status');
        statusEl.textContent = data.status.toUpperCase();
        statusEl.className = 'status-badge status-' + data.status;

        const pct = (data.current_epoch / data.total_epochs * 100).toFixed(1);
        document.getElementById(model + '-progress').style.width = pct + '%';
        document.getElementById(model + '-epoch').textContent = data.current_epoch + ' / ' + data.total_epochs;

        if (model === 'stm') {
            const acc = data.val_accuracy.length ? data.val_accuracy[data.val_accuracy.length - 1] : '—';
            const t3 = data.top3_accuracy.length ? data.top3_accuracy[data.top3_accuracy.length - 1] : '—';
            document.getElementById('stm-acc').textContent = typeof acc === 'number' ? acc.toFixed(1) + '%' : acc;
            document.getElementById('stm-top3').textContent = typeof t3 === 'number' ? t3.toFixed(1) + '%' : t3;
            document.getElementById('stm-lr').textContent = data.lr.toExponential(1);

            const labels = Array.from({length: data.train_loss.length}, (_, i) => i + 1);
            stmLossChart.data.labels = labels;
            stmLossChart.data.datasets[0].data = data.train_loss;
            stmLossChart.data.datasets[1].data = data.val_loss;
            stmLossChart.update();

            stmAccChart.data.labels = labels;
            stmAccChart.data.datasets[0].data = data.val_accuracy;
            stmAccChart.data.datasets[1].data = data.top3_accuracy;
            stmAccChart.update();
        } else {
            const f1 = data.val_f1.length ? data.val_f1[data.val_f1.length - 1] : '—';
            const auc = data.val_auc.length ? data.val_auc[data.val_auc.length - 1] : '—';
            document.getElementById('gnn-f1').textContent = typeof f1 === 'number' ? f1.toFixed(4) : f1;
            document.getElementById('gnn-auc').textContent = typeof auc === 'number' ? auc.toFixed(4) : auc;
            document.getElementById('gnn-lr').textContent = data.lr.toExponential(1);

            const labels = Array.from({length: data.train_loss.length}, (_, i) => i + 1);
            gnnLossChart.data.labels = labels;
            gnnLossChart.data.datasets[0].data = data.train_loss;
            gnnLossChart.data.datasets[1].data = data.val_loss;
            gnnLossChart.update();

            gnnMetricChart.data.labels = labels;
            gnnMetricChart.data.datasets[0].data = data.val_f1;
            gnnMetricChart.data.datasets[1].data = data.val_auc;
            gnnMetricChart.update();
        }
    }

    // ================================================================
    // ATM Prediction
    // ================================================================
    async function runPrediction() {
        const resp = await fetch('/api/predict/demo', { method: 'POST', headers: {'Content-Type':'application/json'}, body: '{"top_k":5}' });
        const data = await resp.json();
        let html = '';
        data.predictions.forEach((p, i) => {
            const riskClass = p.risk > 70 ? 'risk-high' : p.risk > 40 ? 'risk-medium' : 'risk-low';
            html += `<tr>
                <td><strong>#${i+1}</strong></td>
                <td>${p.atm_id}</td>
                <td><strong>${(p.probability*100).toFixed(1)}%</strong></td>
                <td>${p.bank}</td>
                <td><span class="risk-badge ${riskClass}">${p.risk.toFixed(0)}</span></td>
            </tr>`;
        });
        document.getElementById('prediction-table').innerHTML = html;
        document.getElementById('prediction-result').innerHTML = `<p style="color:var(--accent-green);">✓ Prediction completed in ${data.latency_ms}ms</p>`;
    }

    // ================================================================
    // Mule Detection
    // ================================================================
    async function runMuleDetection() {
        const resp = await fetch('/api/detect/demo', { method: 'POST', headers: {'Content-Type':'application/json'}, body: '{}' });
        const data = await resp.json();

        const riskClass = data.risk_level === 'HIGH' ? 'risk-high' : data.risk_level === 'MEDIUM' ? 'risk-medium' : 'risk-low';

        document.getElementById('gauge-value').textContent = data.final_score.toFixed(1);
        document.getElementById('gauge-value').style.color = data.risk_color;
        document.getElementById('gauge-label').textContent = data.risk_level + ' RISK';
        document.getElementById('gauge-marker').style.left = data.final_score + '%';

        const tbody = document.getElementById('mule-table');
        const row = `<tr>
            <td>${data.account_id}</td>
            <td>${data.gnn_probability.toFixed(4)}</td>
            <td>${data.rule_score.toFixed(1)}</td>
            <td><strong>${data.final_score.toFixed(1)}</strong></td>
            <td><span class="risk-badge ${riskClass}">${data.risk_level}</span></td>
            <td style="font-size:11px;">${data.action}</td>
        </tr>`;
        tbody.insertAdjacentHTML('afterbegin', row);

        document.getElementById('mule-result').innerHTML = `<p style="color:var(--accent-cyan);">✓ Analysis completed in ${data.latency_ms}ms</p>`;
    }

    // ================================================================
    // System Stats
    // ================================================================
    async function updateSystemStats() {
        const resp = await fetch('/api/system/stats');
        const d = await resp.json();
        document.getElementById('sys-requests').textContent = d.api_requests.toLocaleString();
        document.getElementById('sys-latency').textContent = d.avg_latency_ms + 'ms';
        document.getElementById('sys-errors').textContent = d.error_rate + '%';
        document.getElementById('sys-uptime').textContent = d.uptime_hours + 'h';

        sysUsageChart.data.datasets[0].data = [
            d.gpu_memory_used_mb,
            d.gpu_memory_total_mb - d.gpu_memory_used_mb,
            d.cpu_usage_pct,
            100 - d.cpu_usage_pct
        ];
        sysUsageChart.update();
    }
    updateSystemStats();
    setInterval(updateSystemStats, 5000);

    // ================================================================
    // ATM Canvas Map
    // ================================================================
    async function drawATMMap() {
        const resp = await fetch('/api/atms');
        const atms = await resp.json();
        const canvas = document.getElementById('atm-canvas');
        const ctx = canvas.getContext('2d');

        // Background
        ctx.fillStyle = '#111827';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Grid
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 0.5;
        for (let i = 0; i < canvas.width; i += 40) { ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke(); }
        for (let i = 0; i < canvas.height; i += 40) { ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(canvas.width, i); ctx.stroke(); }

        // Draw ATMs
        const latMin = 12.8, latMax = 13.2, lonMin = 77.4, lonMax = 77.8;
        atms.forEach(atm => {
            const x = ((atm.lon - lonMin) / (lonMax - lonMin)) * (canvas.width - 40) + 20;
            const y = canvas.height - ((atm.lat - latMin) / (latMax - latMin)) * (canvas.height - 40) - 20;
            const radius = 2 + (atm.risk / 100) * 4;

            let color;
            if (atm.risk > 70) color = 'rgba(239,68,68,0.7)';
            else if (atm.risk > 40) color = 'rgba(245,158,11,0.5)';
            else color = 'rgba(34,197,94,0.4)';

            // Glow for high risk
            if (atm.risk > 70) {
                ctx.beginPath();
                ctx.arc(x, y, radius + 6, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(239,68,68,0.1)';
                ctx.fill();
            }

            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.fill();
        });

        // Legend
        ctx.font = '11px Inter';
        ctx.fillStyle = '#64748b';
        ctx.fillText('Bangalore ATM Risk Map (500 ATMs)', 20, 20);
        ctx.fillStyle = 'rgba(239,68,68,0.8)'; ctx.fillRect(20, canvas.height - 25, 10, 10);
        ctx.fillStyle = '#94a3b8'; ctx.fillText('High Risk', 35, canvas.height - 16);
        ctx.fillStyle = 'rgba(245,158,11,0.6)'; ctx.fillRect(110, canvas.height - 25, 10, 10);
        ctx.fillStyle = '#94a3b8'; ctx.fillText('Medium', 125, canvas.height - 16);
        ctx.fillStyle = 'rgba(34,197,94,0.5)'; ctx.fillRect(190, canvas.height - 25, 10, 10);
        ctx.fillStyle = '#94a3b8'; ctx.fillText('Low Risk', 205, canvas.height - 16);
    }
    setTimeout(drawATMMap, 500);
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(DASHBOARD_HTML)


if __name__ == "__main__":
    print("=" * 60)
    print("  SIH26184 — Demo Dashboard (RUMA)")
    print("  Open: http://localhost:5500")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5500, debug=True)

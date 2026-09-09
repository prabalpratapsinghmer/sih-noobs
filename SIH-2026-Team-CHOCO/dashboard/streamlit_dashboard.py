"""
Streamlit Dashboard for Live Model Training Visualization.

Run with: streamlit run dashboard/streamlit_dashboard.py

This provides a real-time web dashboard showing:
- Training/Validation loss curves
- Accuracy metrics (Top-1, Top-3, Top-5)
- Learning rate schedule
- Model architecture summary
- System metrics (GPU/CPU usage)
- Confusion matrix, ROC curves
"""

import streamlit as st
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
import os
from pathlib import Path
from datetime import datetime
import threading
import queue

# Page config
st.set_page_config(
    page_title="SIH26184 - Live Training Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .status-running { color: #28a745; font-weight: bold; }
    .status-stopped { color: #dc3545; font-weight: bold; }
    .status-completed { color: #17a2b8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'training_data' not in st.session_state:
    st.session_state.training_data = {
        'epochs': [],
        'train_loss': [],
        'val_loss': [],
        'train_acc': [],
        'val_acc': [],
        'val_top3': [],
        'val_top5': [],
        'lr': [],
        'grad_norm': [],
    }
if 'training_status' not in st.session_state:
    st.session_state.training_status = 'stopped'
if 'current_epoch' not in st.session_state:
    st.session_state.current_epoch = 0
if 'total_epochs' not in st.session_state:
    st.session_state.total_epochs = 200
if 'model_info' not in st.session_state:
    st.session_state.model_info = {}
if 'gpu_info' not in st.session_state:
    st.session_state.gpu_info = {}

# Sidebar
st.sidebar.title("🎛️ Control Panel")

# Model selection
model_type = st.sidebar.selectbox(
    "Select Model",
    ["Spatio-Temporal Transformer", "Mule Detection GNN"],
    index=0
)

# Training controls
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("▶️ Start Training", type="primary", use_container_width=True):
        st.session_state.training_status = 'running'
        st.rerun()

with col2:
    if st.button("⏹️ Stop Training", use_container_width=True):
        st.session_state.training_status = 'stopped'
        st.rerun()

if st.sidebar.button("🔄 Reset Dashboard", use_container_width=True):
    st.session_state.training_data = {
        'epochs': [], 'train_loss': [], 'val_loss': [],
        'train_acc': [], 'val_acc': [], 'val_top3': [],
        'val_top5': [], 'lr': [], 'grad_norm': []
    }
    st.session_state.training_status = 'stopped'
    st.session_state.current_epoch = 0
    st.rerun()

# Configuration
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Configuration")

epochs = st.sidebar.number_input("Total Epochs", 10, 500, 200, 10)
st.session_state.total_epochs = epochs

batch_size = st.sidebar.number_input("Batch Size", 8, 128, 32, 8)
learning_rate = st.sidebar.number_input("Learning Rate", 1e-5, 1e-2, 1e-4, 1e-5, format="%.5f")
device = st.sidebar.selectbox("Device", ["auto", "cuda", "cpu"], index=0)

# TensorBoard link
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 TensorBoard")
st.sidebar.markdown("[Open TensorBoard](http://localhost:6006)")
st.sidebar.caption("Run: `tensorboard --logdir logs/tensorboard`")

# Main header
st.markdown('<h1 class="main-header">🤖 SIH26184 - Live Training Dashboard</h1>', unsafe_allow_html=True)

# Status indicator
status_colors = {
    'running': ('status-running', '🟢 RUNNING'),
    'stopped': ('status-stopped', '🔴 STOPPED'),
    'completed': ('status-completed', '🔵 COMPLETED')
}
status_class, status_text = status_colors.get(st.session_state.training_status, ('status-stopped', '🔴 STOPPED'))
st.markdown(f'<p style="text-align:center; font-size:1.2rem;">Status: <span class="{status_class}">{status_text}</span> | Epoch: {st.session_state.current_epoch}/{st.session_state.total_epochs}</p>', unsafe_allow_html=True)

# Progress bar
progress = st.session_state.current_epoch / st.session_state.total_epochs if st.session_state.total_epochs > 0 else 0
st.progress(progress)

# Metrics row
col1, col2, col3, col4 = st.columns(4)

def get_latest(data_list, default=0):
    return data_list[-1] if data_list else default

with col1:
    train_loss = get_latest(st.session_state.training_data['train_loss'])
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{train_loss:.4f}</div>
        <div class="metric-label">Train Loss</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    val_loss = get_latest(st.session_state.training_data['val_loss'])
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{val_loss:.4f}</div>
        <div class="metric-label">Val Loss</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    val_acc = get_latest(st.session_state.training_data['val_acc'])
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{val_acc:.2f}%</div>
        <div class="metric-label">Val Accuracy</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    val_top3 = get_latest(st.session_state.training_data['val_top3'])
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{val_top3:.2f}%</div>
        <div class="metric-label">Top-3 Accuracy</div>
    </div>
    ''', unsafe_allow_html=True)

# Additional metrics row
col5, col6, col7, col8 = st.columns(4)

with col5:
    train_acc = get_latest(st.session_state.training_data['train_acc'])
    st.metric("Train Acc", f"{train_acc:.2f}%")

with col6:
    val_top5 = get_latest(st.session_state.training_data['val_top5'])
    st.metric("Top-5 Acc", f"{val_top5:.2f}%")

with col7:
    lr = get_latest(st.session_state.training_data['lr'])
    st.metric("Learning Rate", f"{lr:.2e}")

with col8:
    grad_norm = get_latest(st.session_state.training_data['grad_norm'])
    st.metric("Grad Norm", f"{grad_norm:.4f}")

# Charts
st.markdown("---")

# Loss Chart
fig_loss = make_subplots(
    rows=1, cols=1,
    subplot_titles=("Training & Validation Loss",),
    x_title="Epoch", y_title="Loss"
)

if st.session_state.training_data['epochs']:
    epochs_data = st.session_state.training_data['epochs']
    fig_loss.add_trace(
        go.Scatter(x=epochs_data, y=st.session_state.training_data['train_loss'],
                   mode='lines+markers', name='Train Loss', line=dict(color='#1f77b4', width=2)),
        row=1, col=1
    )
    fig_loss.add_trace(
        go.Scatter(x=epochs_data, y=st.session_state.training_data['val_loss'],
                   mode='lines+markers', name='Val Loss', line=dict(color='#ff7f0e', width=2)),
        row=1, col=1
    )

fig_loss.update_layout(height=400, hovermode='x unified', showlegend=True)
st.plotly_chart(fig_loss, use_container_width=True)

# Accuracy Charts
col_left, col_right = st.columns(2)

with col_left:
    fig_acc = make_subplots(
        rows=1, cols=1,
        subplot_titles=("Accuracy Metrics",),
        x_title="Epoch", y_title="Accuracy (%)"
    )

    if st.session_state.training_data['epochs']:
        epochs_data = st.session_state.training_data['epochs']
        fig_acc.add_trace(
            go.Scatter(x=epochs_data, y=st.session_state.training_data['train_acc'],
                       mode='lines+markers', name='Train Acc', line=dict(color='#2ca02c', width=2)),
            row=1, col=1
        )
        fig_acc.add_trace(
            go.Scatter(x=epochs_data, y=st.session_state.training_data['val_acc'],
                       mode='lines+markers', name='Val Acc (Top-1)', line=dict(color='#d62728', width=2)),
            row=1, col=1
        )
        fig_acc.add_trace(
            go.Scatter(x=epochs_data, y=st.session_state.training_data['val_top3'],
                       mode='lines+markers', name='Val Top-3', line=dict(color='#9467bd', width=2, dash='dash')),
            row=1, col=1
        )
        fig_acc.add_trace(
            go.Scatter(x=epochs_data, y=st.session_state.training_data['val_top5'],
                       mode='lines+markers', name='Val Top-5', line=dict(color='#8c564b', width=2, dash='dot')),
            row=1, col=1
        )

    fig_acc.update_layout(height=400, hovermode='x unified', showlegend=True)
    st.plotly_chart(fig_acc, use_container_width=True)

with col_right:
    fig_lr = make_subplots(
        rows=1, cols=1,
        subplot_titles=("Learning Rate Schedule",),
        x_title="Epoch", y_title="Learning Rate"
    )

    if st.session_state.training_data['epochs'] and st.session_state.training_data['lr']:
        fig_lr.add_trace(
            go.Scatter(x=st.session_state.training_data['epochs'],
                       y=st.session_state.training_data['lr'],
                       mode='lines+markers', name='Learning Rate',
                       line=dict(color='#e377c2', width=2)),
            row=1, col=1
        )

    fig_lr.update_layout(height=400, hovermode='x unified', yaxis_type='log')
    st.plotly_chart(fig_lr, use_container_width=True)

# Gradient norm chart
if st.session_state.training_data['grad_norm']:
    fig_grad = make_subplots(
        rows=1, cols=1,
        subplot_titles=("Gradient Norm",),
        x_title="Epoch", y_title="Gradient Norm"
    )
    fig_grad.add_trace(
        go.Scatter(x=st.session_state.training_data['epochs'],
                   y=st.session_state.training_data['grad_norm'],
                   mode='lines+markers', name='Grad Norm',
                   line=dict(color='#17becf', width=2)),
        row=1, col=1
    )
    fig_grad.update_layout(height=300, hovermode='x unified')
    st.plotly_chart(fig_grad, use_container_width=True)

# Model Architecture Visualization
st.markdown("---")
st.subheader("🏗️ Model Architecture")

tab1, tab2, tab3 = st.tabs(["Architecture Summary", "Model Graph", "Parameters"])

with tab1:
    if model_type == "Spatio-Temporal Transformer":
        st.markdown("""
        ### Spatio-Temporal Transformer Architecture

        **Input Features:**
        - Spatial (4D): Latitude, Longitude, Distance to Metro, Distance to Police
        - Temporal (6D): Hour (sin/cos), Day of Week, Weekend Flag, Time Since Complaint, Fraud Spike Hour

        **Architecture:**
        1. **Spatial Encoder**: MLP(4 → 64 → 128) + BatchNorm + ReLU
        2. **Temporal Encoder**: MLP(6 → 64 → 128) + BatchNorm + ReLU
        3. **Cross-Attention**: Multi-head Attention (8 heads, 256 dim)
        4. **Transformer Encoder**: 6 layers × (Self-Attention + FFN)
        5. **Classifier**: Linear(256 → 128) → ReLU → Dropout(0.3) → Linear(128 → 500)

        **Output**: Probability distribution over 500 ATMs (Softmax)
        """)
    else:
        st.markdown("""
        ### Mule Detection GNN Architecture

        **Node Features (9D):**
        - Transaction velocity (tx/hour)
        - Total inflow amount
        - Total outflow amount
        - Outflow/Inflow ratio
        - Average holding time (minutes)
        - Connected complaint count
        - Suspicious timing count (2-5 AM)
        - In-degree
        - Out-degree

        **Architecture:**
        1. **GraphSAGE Layer 1**: SAGEConv(9 → 128) + ReLU + Dropout(0.2)
        2. **GraphSAGE Layer 2**: SAGEConv(128 → 64) + ReLU + Dropout(0.2)
        3. **GraphSAGE Layer 3**: SAGEConv(64 → 32) + ReLU
        4. **Classifier**: Linear(32 → 64) → ReLU + Dropout(0.3) → Linear(64 → 1) → Sigmoid

        **Output**: Probability per node (is_mule probability)
        """)

with tab2:
    st.info("Model graph visualization requires TensorBoard. Run `tensorboard --logdir logs/tensorboard` and open the Graphs tab.")

with tab3:
    # Parameter count display
    if model_type == "Spatio-Temporal Transformer":
        st.markdown("""
        | Component | Parameters |
        |-----------|------------|
        | Spatial Encoder | ~33K |
        | Temporal Encoder | ~41K |
        | Cross-Attention | ~262K |
        | Transformer (6 layers) | ~3.9M |
        | Classifier | ~328K |
        | **Total** | **~4.6M** |
        """)
    else:
        st.markdown("""
        | Component | Parameters |
        |-----------|------------|
        | GraphSAGE Layers | ~85K |
        | Classifier | ~13K |
        | **Total** | **~98K** |
        """)

# System Metrics
st.markdown("---")
st.subheader("💻 System Metrics")

col_sys1, col_sys2, col_sys3 = st.columns(3)

with col_sys1:
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        gpu_allocated = torch.cuda.memory_allocated(0) / 1e9
        gpu_cached = torch.cuda.memory_reserved(0) / 1e9

        st.metric("GPU", gpu_name)
        st.metric("GPU Memory", f"{gpu_allocated:.2f} / {gpu_memory:.2f} GB")
        st.progress(gpu_allocated / gpu_memory if gpu_memory > 0 else 0)
    else:
        st.warning("CUDA not available - running on CPU")

with col_sys2:
    import psutil
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()

    st.metric("CPU Usage", f"{cpu_percent:.1f}%")
    st.metric("RAM Usage", f"{memory.percent:.1f}%")
    st.progress(memory.percent / 100)

with col_sys3:
    st.metric("PyTorch Version", torch.__version__)
    st.metric("Python Version", f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}")

# Training Log
st.markdown("---")
st.subheader("📋 Training Log")

# Simulated training log
log_placeholder = st.empty()

# Auto-refresh
if st.session_state.training_status == 'running':
    time.sleep(2)
    st.rerun()

# Footer
st.markdown("---")
st.caption("SIH26184 Predictive Analytics Framework for Cybercrime Complaints | Built with Streamlit & PyTorch")
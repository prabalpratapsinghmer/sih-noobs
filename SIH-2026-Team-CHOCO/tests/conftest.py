"""Shared pytest fixtures for SIH26184 tests."""

import os
import sys
from pathlib import Path

import pytest
import yaml
import numpy as np

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def anyio_backend():
    """Specify asyncio as backend for anyio async tests."""
    return "asyncio"


@pytest.fixture(scope="session")
def config():
    """Load project configuration once per test session."""
    config_path = PROJECT_ROOT / "config" / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def device():
    """Return the torch device to use for tests."""
    import torch
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@pytest.fixture
def sample_spatial_features():
    """Sample spatial feature array for STM prediction."""
    return np.array([[12.97, 77.60, 0.5, 2.3]])


@pytest.fixture
def sample_temporal_features():
    """Sample temporal feature array for STM prediction."""
    hour = 14
    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)
    day_sin = np.sin(2 * np.pi * 3 / 7)
    day_cos = np.cos(2 * np.pi * 3 / 7)
    return np.array([[hour_sin, hour_cos, day_sin, day_cos, 0.0, 2.5, 22]])


@pytest.fixture
def sample_mule_features():
    """Sample mule account features dict."""
    return {
        "velocity": 5.0,
        "inflow": 500000.0,
        "outflow": 480000.0,
        "outflow_ratio": 0.96,
        "holding_time": 15.0,
        "connected_complaints": 2,
        "suspicious_timing": 3,
        "in_degree": 4,
        "out_degree": 5,
    }


@pytest.fixture
def sample_complaint():
    """Sample complaint data dict."""
    return {
        "complaint_id": "C0001",
        "victim_id": "V0001",
        "amount": 250000.0,
        "timestamp": "2026-09-01T10:30:00",
        "fraud_type": "investment",
        "fraudster_upi": "scammer@paytm",
        "fraudster_phone": "+919876543210",
        "fraudster_account": "M0001_1",
        "status": "SUBMITTED",
    }

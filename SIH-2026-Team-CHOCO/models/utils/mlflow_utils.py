"""MLflow Integration Utilities for Model Tracking and Registry."""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

import torch
import yaml
import joblib
import numpy as np
from loguru import logger

# Project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import mlflow
    import mlflow.pytorch
    MLFLOW_AVAILABLE = True
except (ImportError, AttributeError):
    MLFLOW_AVAILABLE = False


class MLflowTracker:
    """MLflow tracking and model registry utilities."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize MLflow tracker."""
        self.config = config
        self.enabled = MLFLOW_AVAILABLE
        self.tracking_uri = config.get('tracking_uri', 'http://localhost:5000')
        self.experiment_name = config.get('experiment_name', 'cybercrime_prediction')
        self.experiment_id = None

        if not self.enabled:
            logger.warning("MLflow not available or import failed. Operating in offline/mock mode.")
            return

        # Attempt to set tracking URI with local directory fallback
        try:
            # First try configured tracking URI
            mlflow.set_tracking_uri(self.tracking_uri)
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment is None:
                self.experiment_id = mlflow.create_experiment(self.experiment_name)
            else:
                self.experiment_id = experiment.experiment_id
            mlflow.set_experiment(self.experiment_name)
        except Exception as e:
            # Fallback to local file tracking URI
            logger.warning(f"Could not connect to MLflow server at {self.tracking_uri} ({e}). Falling back to local './mlruns'.")
            try:
                local_uri = "file:./mlruns"
                mlflow.set_tracking_uri(local_uri)
                experiment = mlflow.get_experiment_by_name(self.experiment_name)
                if experiment is None:
                    self.experiment_id = mlflow.create_experiment(self.experiment_name)
                else:
                    self.experiment_id = experiment.experiment_id
                mlflow.set_experiment(self.experiment_name)
            except Exception as e2:
                logger.warning(f"Local MLflow initialization also failed ({e2}). Disabling MLflow tracking for this session.")
                self.enabled = False

    def log_params(self, params: Dict[str, Any], prefix: str = ""):
        """Log parameters with optional prefix."""
        if not self.enabled:
            return
        try:
            for key, value in params.items():
                full_key = f"{prefix}{key}" if prefix else key
                if isinstance(value, dict):
                    self.log_params(value, f"{full_key}.")
                elif isinstance(value, (list, tuple)):
                    mlflow.log_param(full_key, str(value)[:250])
                else:
                    mlflow.log_param(full_key, value)
        except Exception as e:
            logger.debug(f"Failed to log param to MLflow: {e}")

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics."""
        if not self.enabled:
            return
        try:
            for key, value in metrics.items():
                mlflow.log_metric(key, float(value), step=step)
        except Exception as e:
            logger.debug(f"Failed to log metric to MLflow: {e}")

    def log_model_artifacts(self, model: torch.nn.Module, model_name: str,
                           config: Dict[str, Any], processed_dir: Path,
                           input_example: Optional[torch.Tensor] = None):
        """Log PyTorch model and preprocessing artifacts."""
        if not self.enabled:
            return
        try:
            if input_example is not None:
                mlflow.pytorch.log_model(
                    model,
                    artifact_path=model_name,
                    input_example=input_example.cpu().numpy() if isinstance(input_example, torch.Tensor) else input_example
                )
            else:
                mlflow.pytorch.log_model(model, artifact_path=model_name)

            artifacts_dir = Path("mlflow_artifacts") / model_name
            artifacts_dir.mkdir(parents=True, exist_ok=True)

            for artifact in ['spatial_scaler.joblib', 'temporal_scaler.joblib', 'label_encoders.joblib']:
                src = processed_dir / artifact
                if src.exists():
                    dst = artifacts_dir / artifact
                    import shutil
                    shutil.copy2(src, dst)
                    mlflow.log_artifact(str(dst), artifact_path=f"{model_name}/preprocessing")

            logger.info(f"Logged model {model_name} and preprocessing artifacts to MLflow")
        except Exception as e:
            logger.debug(f"Failed to log model artifacts: {e}")

    def register_model(self, model_name: str, model_uri: str, stage: str = "Staging") -> bool:
        """Register model in MLflow Model Registry."""
        if not self.enabled:
            return False
        try:
            registered_model = mlflow.register_model(model_uri, model_name)
            client = mlflow.MlflowClient()
            client.transition_model_version_stage(
                name=model_name,
                version=registered_model.version,
                stage=stage,
                archive_existing_versions=True
            )
            return True
        except Exception as e:
            logger.debug(f"Failed to register model: {e}")
            return False


def setup_mlflow_for_training(config: Dict[str, Any], run_name: Optional[str] = None):
    """Set up MLflow for a training run."""
    tracker = MLflowTracker(config.get('mlflow', {}))
    run = None

    if tracker.enabled:
        try:
            if run_name is None:
                run_name = f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            run = mlflow.start_run(run_name=run_name)
            tracker.log_params(config, prefix="config.")
        except Exception as e:
            logger.warning(f"Failed to start MLflow run: {e}")
            tracker.enabled = False

    return tracker, run


def end_mlflow_run():
    """End the current MLflow run."""
    if MLFLOW_AVAILABLE:
        try:
            mlflow.end_run()
        except Exception:
            pass


def create_input_example(model_type: str, config: Dict[str, Any]) -> Optional[torch.Tensor]:
    """Create example input for MLflow model signature."""
    if model_type == 'spatio_temporal':
        spatial = torch.randn(1, 4)
        temporal = torch.randn(1, 6)
        return (spatial, temporal)
    elif model_type == 'mule_detection':
        x = torch.randn(10, 9)
        edge_index = torch.randint(0, 10, (2, 20))
        return (x, edge_index)
    return None
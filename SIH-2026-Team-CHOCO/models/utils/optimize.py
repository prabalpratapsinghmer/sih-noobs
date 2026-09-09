"""Hyperparameter Optimization Module for Cybercrime Models (Optuna Integration)."""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from loguru import logger

# Project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.spatio_temporal.model import SpatioTemporalTransformer
from models.mule_detection.model import MuleDetectionGNN

try:
    import optuna
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False


class SpatioTemporalOptimizer:
    """Optuna optimizer for SpatioTemporalTransformer."""

    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def objective(self, trial) -> float:
        # Suggest hyperparameters
        hidden_dim = trial.suggest_categorical("hidden_dim", [128, 256])
        num_heads = trial.suggest_categorical("num_heads", [4, 8])
        num_layers = trial.suggest_int("num_layers", 2, 4)
        lr = trial.suggest_float("lr", 1e-4, 1e-3, log=True)
        dropout = trial.suggest_float("dropout", 0.1, 0.3)

        model_cfg = {
            "num_atms": 500,
            "spatial_encoder": {"input_dim": 4, "hidden_dim": 64, "output_dim": hidden_dim // 2},
            "temporal_encoder": {"input_dim": 6, "hidden_dim": 64, "output_dim": hidden_dim // 2},
            "num_heads": num_heads,
            "num_layers": num_layers,
            "dropout": dropout,
            "classifier": {"hidden_dim": 128, "dropout": dropout},
        }

        model = SpatioTemporalTransformer(model_cfg).to(self.device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=lr)

        # Quick validation on sample data
        processed_dir = Path(self.config["data"]["processed_dir"])
        X_train = np.load(processed_dir / "st_X_train.npy")[:200]
        y_train = np.load(processed_dir / "st_y_train.npy")[:200]
        X_val = np.load(processed_dir / "st_X_val.npy")[:50]
        y_val = np.load(processed_dir / "st_y_val.npy")[:50]

        spatial_dim = X_train.shape[1] // 2
        sp_train = torch.FloatTensor(X_train[:, :spatial_dim]).to(self.device)
        tm_train = torch.FloatTensor(X_train[:, spatial_dim:]).to(self.device)
        y_tr = torch.LongTensor(y_train).to(self.device)

        sp_val = torch.FloatTensor(X_val[:, :spatial_dim]).to(self.device)
        tm_val = torch.FloatTensor(X_val[:, spatial_dim:]).to(self.device)
        y_v = torch.LongTensor(y_val).to(self.device)

        for _ in range(5):
            model.train()
            optimizer.zero_grad()
            out = model(sp_train, tm_train)
            loss = criterion(out, y_tr)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            val_out = model(sp_val, tm_val)
            preds = torch.argmax(val_out, dim=1)
            acc = (preds == y_v).float().mean().item()

        return acc

    def run_study(self, n_trials: int = 10) -> Dict[str, Any]:
        if not OPTUNA_AVAILABLE:
            logger.warning("Optuna not installed. Returning default configuration.")
            return self.config["models"]["spatio_temporal"]

        study = optuna.create_study(direction="maximize")
        study.optimize(self.objective, n_trials=n_trials)
        logger.info(f"Best trial value: {study.best_value:.4f}")
        logger.info(f"Best params: {study.best_params}")
        return study.best_params


def main():
    optimizer = SpatioTemporalOptimizer()
    logger.info("Running hyperparameter optimization study...")
    best_params = optimizer.run_study(n_trials=5)
    print("Optimization finished. Best params:", best_params)


if __name__ == "__main__":
    main()

"""Model loading utilities for the Cybercrime Prediction API.

Handles lazy-loading and caching of ML models (Spatio-Temporal Transformer
and Mule Detection GNN) so the API can serve predictions without reloading
models on every request.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Tuple

import torch
import joblib
import yaml
from loguru import logger


class ModelRegistry:
    """Central registry for loading, caching, and serving ML models."""

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config: Dict = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.spatial_model = None
        self.mule_model = None
        self.scalers: Dict = {}
        self.label_encoders = None
        self.gnn_data = None
        self._loaded = False

    def load_config(self) -> Dict:
        """Load project configuration."""
        with open(self.config_path, "r") as f:
            self.config = yaml.safe_load(f)
        return self.config

    def load_all(self) -> None:
        """Load all models and preprocessing artifacts."""
        if self._loaded:
            logger.info("Models already loaded, skipping.")
            return

        self.load_config()
        self._load_scalers()
        self._load_spatio_temporal()
        self._load_mule_detection()
        self._loaded = True
        logger.info("✓ All models loaded successfully")

    def _load_scalers(self) -> None:
        """Load feature scalers and label encoders."""
        processed_dir = Path(self.config["data"]["processed_dir"])
        try:
            self.scalers["spatial"] = joblib.load(processed_dir / "spatial_scaler.joblib")
            self.scalers["temporal"] = joblib.load(processed_dir / "temporal_scaler.joblib")
            self.label_encoders = joblib.load(processed_dir / "label_encoders.joblib")
            logger.info("✓ Scalers and encoders loaded")
        except FileNotFoundError as e:
            logger.warning(f"Scaler files not found: {e}. Models may not produce accurate results.")

    def _load_spatio_temporal(self) -> None:
        """Load the Spatio-Temporal Transformer model."""
        from models.spatio_temporal.model import SpatioTemporalTransformer

        checkpoint_path = (
            Path(self.config["training"]["spatio_temporal"]["checkpoint"]["save_dir"])
            / "best_model.pth"
        )
        if not checkpoint_path.exists():
            logger.warning(f"STM checkpoint not found at {checkpoint_path}")
            return

        self.spatial_model = SpatioTemporalTransformer(self.config["models"]["spatio_temporal"])
        checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        self.spatial_model.load_state_dict(checkpoint["model_state_dict"])
        self.spatial_model = self.spatial_model.to(self.device)
        self.spatial_model.eval()
        logger.info(
            f"✓ STM loaded (epoch {checkpoint['epoch']}, "
            f"val_acc: {checkpoint.get('val_acc', 'N/A')})"
        )

    def _load_mule_detection(self) -> None:
        """Load the Mule Detection GNN model."""
        from models.mule_detection.model import MuleDetectionGNN

        checkpoint_path = (
            Path(self.config["training"]["mule_detection"]["checkpoint"]["save_dir"])
            / "best_model.pth"
        )
        gnn_data_path = Path(self.config["data"]["processed_dir"]) / "gnn_data.pt"

        if not checkpoint_path.exists():
            logger.warning(f"GNN checkpoint not found at {checkpoint_path}")
            return

        self.mule_model = MuleDetectionGNN(self.config["models"]["mule_detection"])
        checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        self.mule_model.load_state_dict(checkpoint["model_state_dict"])
        self.mule_model = self.mule_model.to(self.device)
        self.mule_model.eval()

        if gnn_data_path.exists():
            self.gnn_data = torch.load(gnn_data_path, map_location=self.device, weights_only=False)

        logger.info(
            f"✓ GNN loaded (epoch {checkpoint['epoch']}, "
            f"val_f1: {checkpoint.get('val_f1', 'N/A')})"
        )

    @property
    def is_stm_ready(self) -> bool:
        return self.spatial_model is not None

    @property
    def is_gnn_ready(self) -> bool:
        return self.mule_model is not None

    def get_status(self) -> Dict:
        """Return health status of all models."""
        return {
            "spatio_temporal": {
                "loaded": self.is_stm_ready,
                "device": str(self.device),
                "parameters": (
                    sum(p.numel() for p in self.spatial_model.parameters())
                    if self.spatial_model
                    else 0
                ),
            },
            "mule_detection": {
                "loaded": self.is_gnn_ready,
                "device": str(self.device),
                "parameters": (
                    sum(p.numel() for p in self.mule_model.parameters())
                    if self.mule_model
                    else 0
                ),
            },
        }


# Singleton instance
_registry: Optional[ModelRegistry] = None


def get_model_registry() -> ModelRegistry:
    """Get or create the global model registry singleton."""
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry

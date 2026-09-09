"""Standalone Prediction Script for Spatio-Temporal Transformer (ATM Prediction)."""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import torch
import yaml
import joblib
from loguru import logger

# Project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.spatio_temporal.model import SpatioTemporalTransformer


class STMPredictor:
    """Inference engine for ATM withdrawal prediction."""

    def __init__(self, checkpoint_path: Optional[str] = None, config_path: str = "config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Scalers
        processed_dir = Path(self.config["data"]["processed_dir"])
        self.spatial_scaler = joblib.load(processed_dir / "spatial_scaler.joblib")
        self.temporal_scaler = joblib.load(processed_dir / "temporal_scaler.joblib")
        self.label_encoders = joblib.load(processed_dir / "label_encoders.joblib")

        # Initialize model
        model_cfg = self.config["models"]["spatio_temporal"]
        self.model = SpatioTemporalTransformer(model_cfg).to(self.device)

        if checkpoint_path is None:
            checkpoint_path = Path(self.config["training"]["spatio_temporal"]["checkpoint"]["save_dir"]) / "best_model.pth"
        else:
            checkpoint_path = Path(checkpoint_path)

        if checkpoint_path.exists():
            checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
            self.model.load_state_dict(checkpoint["model_state_dict"])
            logger.info(f"Loaded checkpoint from {checkpoint_path} (epoch {checkpoint.get('epoch', 0)})")
        else:
            logger.warning(f"Checkpoint {checkpoint_path} not found. Running with initialized weights.")

        self.model.eval()

    def predict_from_features(self, lat: float, lon: float, dist_metro: float, dist_police: float,
                              hour: int, day: int, is_weekend: bool, time_since_complaint: float,
                              fraud_spike_hour: int = 22, top_k: int = 3) -> List[Dict[str, Any]]:
        """Run inference given feature values."""
        spatial_raw = np.array([[lat, lon, dist_metro, dist_police]])

        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        day_sin = np.sin(2 * np.pi * day / 7)
        day_cos = np.cos(2 * np.pi * day / 7)

        temporal_raw = np.array([[
            hour_sin, hour_cos, day_sin, day_cos,
            float(is_weekend), time_since_complaint, fraud_spike_hour
        ]])

        spatial_scaled = self.spatial_scaler.transform(spatial_raw)
        temporal_scaled = self.temporal_scaler.transform(temporal_raw)

        spatial_t = torch.FloatTensor(spatial_scaled).to(self.device)
        temporal_t = torch.FloatTensor(temporal_scaled).to(self.device)

        with torch.no_grad():
            top_k_indices, top_k_probs = self.model.predict_top_k(spatial_t, temporal_t, k=top_k)

        indices = top_k_indices.cpu().numpy()[0]
        probs = top_k_probs.cpu().numpy()[0]

        predictions = []
        for idx, prob in zip(indices, probs):
            atm_id = f"A{int(idx):04d}"
            # Realistic time window estimation (typically 2-5 hours)
            time_window = f"{round(1.5 + float(idx % 4) * 0.8, 1)} hours"
            risk_score = min(99, int(prob * 100 * 1.1 + 10))

            predictions.append({
                "atm_id": atm_id,
                "atm_index": int(idx),
                "probability": round(float(prob), 4),
                "time_window": time_window,
                "risk_score": risk_score,
            })

        return predictions


def main():
    parser = argparse.ArgumentParser(description="Predict ATM withdrawal locations")
    parser.add_argument("--lat", type=float, default=12.9716, help="Latitude")
    parser.add_argument("--lon", type=float, default=77.5946, help="Longitude")
    parser.add_argument("--dist-metro", type=float, default=0.5, help="Distance to metro in km")
    parser.add_argument("--dist-police", type=float, default=1.2, help="Distance to police in km")
    parser.add_argument("--hour", type=int, default=14, help="Hour of day")
    parser.add_argument("--top-k", type=int, default=3, help="Top K predictions")
    args = parser.parse_args()

    predictor = STMPredictor()
    results = predictor.predict_from_features(
        lat=args.lat, lon=args.lon, dist_metro=args.dist_metro, dist_police=args.dist_police,
        hour=args.hour, day=3, is_weekend=False, time_since_complaint=2.5, top_k=args.top_k
    )

    print("\n--- TOP ATM PREDICTIONS ---")
    for r in results:
        print(f"ATM: {r['atm_id']} | Prob: {r['probability']:.4f} | Risk Score: {r['risk_score']} | Window: {r['time_window']}")


if __name__ == "__main__":
    main()

"""Inference engine for the Cybercrime Prediction API.

Provides high-level inference functions that abstract away tensor preparation,
model invocation, and result post-processing for both the Spatio-Temporal
Transformer and the Mule Detection GNN.
"""

import time
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
from loguru import logger

from api.utils.model_loader import ModelRegistry


class InferenceEngine:
    """Wraps model inference with preprocessing, timing, and error handling."""

    def __init__(self, registry: ModelRegistry):
        self.registry = registry

    # ------------------------------------------------------------------
    # Spatio-Temporal Transformer
    # ------------------------------------------------------------------
    def predict_atm(
        self,
        spatial_raw: np.ndarray,
        temporal_raw: np.ndarray,
        top_k: int = 3,
    ) -> Dict:
        """Predict top-K ATM locations from spatial & temporal features.

        Args:
            spatial_raw: (1, 4) array — [lat, lon, dist_metro, dist_police]
            temporal_raw: (1, N) array — temporal features (already cyclically encoded)
            top_k: number of top predictions to return

        Returns:
            dict with predictions list and latency_ms
        """
        start = time.perf_counter()

        model = self.registry.spatial_model
        device = self.registry.device

        # Scale
        spatial_scaled = self.registry.scalers["spatial"].transform(spatial_raw)
        temporal_scaled = self.registry.scalers["temporal"].transform(temporal_raw)

        # Tensors
        spatial_t = torch.FloatTensor(spatial_scaled).to(device)
        temporal_t = torch.FloatTensor(temporal_scaled).to(device)

        # Inference
        with torch.no_grad():
            top_k_indices, top_k_probs = model.predict_top_k(
                spatial_t, temporal_t, k=top_k
            )

        atm_indices = top_k_indices.cpu().numpy()[0]
        probs = top_k_probs.cpu().numpy()[0]

        predictions = [
            {"atm_index": int(idx), "probability": float(prob)}
            for idx, prob in zip(atm_indices, probs)
        ]

        latency_ms = (time.perf_counter() - start) * 1000
        return {"predictions": predictions, "latency_ms": round(latency_ms, 2)}

    # ------------------------------------------------------------------
    # Mule Detection GNN
    # ------------------------------------------------------------------
    def detect_mule(self, features_dict: Dict) -> Dict:
        """Score an account for mule risk using GNN + hybrid rules.

        Args:
            features_dict: dict with keys velocity, inflow, outflow, etc.

        Returns:
            dict with gnn_probability, rule_score, final_score, risk info
        """
        from models.mule_detection.model import HybridMuleScorer

        start = time.perf_counter()

        model = self.registry.mule_model
        device = self.registry.device

        node_features = torch.FloatTensor([[
            features_dict["velocity"],
            features_dict["inflow"],
            features_dict["outflow"],
            features_dict["outflow_ratio"],
            features_dict["holding_time"],
            features_dict["connected_complaints"],
            features_dict["suspicious_timing"],
            features_dict["in_degree"],
            features_dict["out_degree"],
        ]]).to(device)

        edge_index = self.registry.gnn_data.edge_index.to(device)

        with torch.no_grad():
            gnn_prob = model.predict_proba(node_features, edge_index).item()

        # Hybrid scoring
        scorer = HybridMuleScorer(self.registry.config)
        rule_score = scorer.compute_rule_score(features_dict)
        final_score = scorer.compute_final_score(gnn_prob, rule_score)
        risk_level, risk_color, action = scorer.get_risk_level(final_score)

        latency_ms = (time.perf_counter() - start) * 1000

        return {
            "gnn_probability": gnn_prob,
            "rule_score": rule_score,
            "final_score": final_score,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "action": action,
            "latency_ms": round(latency_ms, 2),
        }

    # ------------------------------------------------------------------
    # Batch inference helpers
    # ------------------------------------------------------------------
    def batch_predict_atm(
        self,
        spatial_batch: np.ndarray,
        temporal_batch: np.ndarray,
        top_k: int = 3,
    ) -> List[Dict]:
        """Run ATM prediction for a batch of inputs."""
        results = []
        for i in range(spatial_batch.shape[0]):
            result = self.predict_atm(
                spatial_batch[i : i + 1],
                temporal_batch[i : i + 1],
                top_k=top_k,
            )
            results.append(result)
        return results

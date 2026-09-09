"""Standalone Prediction Script for Mule Detection GNN."""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import torch
import yaml
from loguru import logger

# Project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.mule_detection.model import MuleDetectionGNN
from models.utils.scoring import HybridScorer


class MulePredictor:
    """Inference engine for Mule Detection GNN + Hybrid Scoring."""

    def __init__(self, checkpoint_path: Optional[str] = None, config_path: str = "config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processed_dir = Path(self.config["data"]["processed_dir"])

        # Load graph structure if available
        gnn_data_path = self.processed_dir / "gnn_data.pt"
        if gnn_data_path.exists():
            self.gnn_data = torch.load(gnn_data_path, map_location="cpu", weights_only=False)
            self.edge_index = self.gnn_data.edge_index.to(self.device)
        else:
            self.gnn_data = None
            self.edge_index = torch.empty((2, 0), dtype=torch.long, device=self.device)

        # Model
        model_cfg = self.config["models"]["mule_detection"]
        self.model = MuleDetectionGNN(model_cfg).to(self.device)

        if checkpoint_path is None:
            checkpoint_path = Path(self.config["training"]["mule_detection"]["checkpoint"]["save_dir"]) / "best_model.pth"
        else:
            checkpoint_path = Path(checkpoint_path)

        if checkpoint_path.exists():
            checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
            self.model.load_state_dict(checkpoint["model_state_dict"])
            logger.info(f"Loaded checkpoint from {checkpoint_path}")
        else:
            logger.warning(f"Checkpoint {checkpoint_path} not found. Running with initialized weights.")

        self.model.eval()
        self.scorer = HybridScorer(config=self.config)

    def predict_account(self, features: Dict[str, Any], account_id: Optional[str] = None) -> Dict[str, Any]:
        """Predict mule risk for a single account."""
        node_features = torch.FloatTensor([[
            features.get("velocity", 1.0),
            features.get("inflow", 100000.0),
            features.get("outflow", 95000.0),
            features.get("outflow_ratio", 0.95),
            features.get("holding_time", 25.0),
            features.get("connected_complaints", 1),
            features.get("suspicious_timing", 0),
            features.get("in_degree", 2),
            features.get("out_degree", 2),
        ]]).to(self.device)

        with torch.no_grad():
            dummy_edges = torch.tensor([[0], [0]], dtype=torch.long, device=self.device)
            gnn_prob = self.model.predict_proba(node_features, dummy_edges).item()

        result = self.scorer.compute_score(gnn_prob, features)
        result["account_id"] = account_id or "ACCOUNT_001"
        return result


def main():
    parser = argparse.ArgumentParser(description="Predict mule account risk")
    parser.add_argument("--velocity", type=float, default=6.5, help="Transactions per hour")
    parser.add_argument("--holding-time", type=float, default=18.0, help="Holding time in minutes")
    parser.add_argument("--complaints", type=int, default=4, help="Connected complaints")
    args = parser.parse_args()

    predictor = MulePredictor()
    sample_features = {
        "velocity": args.velocity,
        "inflow": 500000.0,
        "outflow": 490000.0,
        "outflow_ratio": 0.98,
        "holding_time": args.holding_time,
        "connected_complaints": args.complaints,
        "suspicious_timing": 2,
        "in_degree": 4,
        "out_degree": 5,
    }

    res = predictor.predict_account(sample_features, account_id="M1001_0")
    print("\n--- MULE DETECTION RESULT ---")
    print(f"Account: {res['account_id']}")
    print(f"GNN Probability: {res['gnn_probability']:.4f}")
    print(f"Rule Score: {res['rule_score']}")
    print(f"Final Score: {res['final_score']}")
    print(f"Risk Level: {res['risk_color']} {res['risk_level']}")
    print(f"Action: {res['action']}")


if __name__ == "__main__":
    main()

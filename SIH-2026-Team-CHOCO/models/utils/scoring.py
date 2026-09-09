"""Mule Scoring Algorithm Module for SIH26184.

Implements rule-based, GNN-based, and hybrid scoring logic combining
graph neural network predictions with domain rules for money mule detection.
"""

from typing import Dict, Any, List, Optional
import numpy as np
from models.utils.risk_mapper import get_risk_level, get_risk_details


class RuleScorer:
    """Rule-based scoring for mule behavior signals."""

    DEFAULT_WEIGHTS = {
        "velocity": 25.0,            # > 5 tx/hr
        "rapid_outflow": 20.0,       # < 30 min hold time
        "connected_complaints": 20.0,# > 3 complaints
        "suspicious_timing": 15.0,   # 2-5 AM activity
        "amount_patterns": 10.0,     # amounts just below thresholds (99k, 1.99L, 4.99L)
        "outflow_ratio": 10.0,       # outflow/inflow ratio ~ 1.0 (0.85 - 1.15)
    }

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()

    def score_account(self, features: Dict[str, Any]) -> float:
        """Compute rule score (0 - 100) based on account behavioral features.

        Args:
            features: Dictionary containing:
                - velocity: float (transactions per hour)
                - holding_time: float (holding time in minutes)
                - connected_complaints: int (number of linked complaints)
                - suspicious_timing: int (count of 2-5 AM transactions)
                - outflow_ratio: float (total_outflow / (total_inflow + eps))
                - amounts: list of amounts or round_amounts flag
        """
        score = 0.0

        # 1. Transaction Velocity: > 5 tx/hour
        velocity = float(features.get("velocity", 0.0))
        if velocity > 5.0:
            score += self.weights.get("velocity", 25.0)
        elif velocity > 2.0:
            score += self.weights.get("velocity", 25.0) * (velocity / 5.0)

        # 2. Rapid Outflow: < 30 minutes average holding time
        holding_time = float(features.get("holding_time", 999.0))
        if holding_time > 0 and holding_time < 30.0:
            score += self.weights.get("rapid_outflow", 20.0)
        elif holding_time > 0 and holding_time < 60.0:
            score += self.weights.get("rapid_outflow", 20.0) * 0.5

        # 3. Connected Complaints: > 3 complaints
        connected_complaints = int(features.get("connected_complaints", 0))
        if connected_complaints >= 3:
            score += self.weights.get("connected_complaints", 20.0)
        elif connected_complaints > 0:
            score += self.weights.get("connected_complaints", 20.0) * (connected_complaints / 3.0)

        # 4. Suspicious Timing: 2 AM - 5 AM transactions
        suspicious_timing = int(features.get("suspicious_timing", 0))
        if suspicious_timing >= 2:
            score += self.weights.get("suspicious_timing", 15.0)
        elif suspicious_timing == 1:
            score += self.weights.get("suspicious_timing", 15.0) * 0.6

        # 5. Amount Patterns: amounts near thresholds or high round numbers
        amounts = features.get("amounts", [])
        has_pattern = bool(features.get("has_threshold_pattern", False))
        if not has_pattern and amounts:
            for amt in amounts:
                # Check for threshold smurfing: 49000-49999, 95000-99999, 195000-199999, 490000-499999
                if (48000 <= amt <= 49999) or (95000 <= amt <= 99999) or (195000 <= amt <= 199999) or (490000 <= amt <= 499999):
                    has_pattern = True
                    break
        if has_pattern:
            score += self.weights.get("amount_patterns", 10.0)

        # 6. Outflow/Inflow Ratio: ~1.0 (pass-through account)
        outflow_ratio = float(features.get("outflow_ratio", 0.0))
        if 0.85 <= outflow_ratio <= 1.15:
            score += self.weights.get("outflow_ratio", 10.0)
        elif 0.70 <= outflow_ratio <= 1.30:
            score += self.weights.get("outflow_ratio", 10.0) * 0.5

        return min(round(score, 2), 100.0)


class HybridScorer:
    """Combines GNN probability (70%) and Rule score (30%)."""

    def __init__(self, gnn_weight: float = 0.7, rule_weight: float = 0.3, config: Optional[Dict] = None):
        if config and "scoring" in config:
            self.gnn_weight = config["scoring"].get("gnn_weight", gnn_weight)
            self.rule_weight = config["scoring"].get("rule_weight", rule_weight)
            rule_weights = config["scoring"].get("rule_weights")
            self.rule_scorer = RuleScorer(rule_weights)
        else:
            self.gnn_weight = gnn_weight
            self.rule_weight = rule_weight
            self.rule_scorer = RuleScorer()

    def compute_score(self, gnn_prob: float, account_features: Dict[str, Any]) -> Dict[str, Any]:
        """Compute comprehensive mule risk assessment.

        Args:
            gnn_prob: Probability from GNN (0.0 to 1.0).
            account_features: Account metrics dictionary.

        Returns:
            Dict containing gnn_prob, rule_score, final_score, risk_level, risk_color, action.
        """
        gnn_prob = max(0.0, min(1.0, float(gnn_prob)))
        gnn_score = gnn_prob * 100.0
        rule_score = self.rule_scorer.score_account(account_features)

        final_score = (gnn_score * self.gnn_weight) + (rule_score * self.rule_weight)
        final_score = min(round(final_score, 2), 100.0)

        risk_level, risk_color, action = get_risk_level(final_score)

        return {
            "gnn_probability": round(gnn_prob, 4),
            "rule_score": round(rule_score, 2),
            "final_score": final_score,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "action": action,
        }


class BatchScorer:
    """Helper to evaluate multiple accounts in a graph or transaction network."""

    def __init__(self, hybrid_scorer: Optional[HybridScorer] = None):
        self.scorer = hybrid_scorer or HybridScorer()

    def score_accounts(self, accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score a list of account feature dictionaries."""
        results = []
        for acc in accounts:
            account_id = acc.get("account_id", "UNKNOWN")
            gnn_prob = acc.get("gnn_probability", 0.5)
            assessment = self.scorer.compute_score(gnn_prob, acc)
            assessment["account_id"] = account_id
            results.append(assessment)
        return results

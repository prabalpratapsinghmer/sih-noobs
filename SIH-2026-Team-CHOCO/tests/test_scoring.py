"""Tests for the scoring and risk mapping modules."""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestScoringModule:
    """Test models/utils/scoring.py functions."""

    def test_rule_scorer_import(self):
        from models.utils.scoring import RuleScorer
        assert RuleScorer is not None

    def test_hybrid_scorer_import(self):
        from models.utils.scoring import HybridScorer
        assert HybridScorer is not None

    def test_rule_scorer_instantiation(self):
        from models.utils.scoring import RuleScorer

        scorer = RuleScorer()
        assert scorer is not None

    def test_hybrid_scorer_with_config(self, config):
        from models.utils.scoring import HybridScorer

        scorer = HybridScorer(config=config)
        assert scorer is not None

    def test_compute_score_high_risk(self):
        """High velocity + suspicious timing + rapid outflow → high score."""
        from models.utils.scoring import RuleScorer

        scorer = RuleScorer()
        features = {
            "velocity": 10.0,
            "inflow": 1000000,
            "outflow": 950000,
            "outflow_ratio": 0.95,
            "holding_time": 5.0,
            "connected_complaints": 3,
            "suspicious_timing": 5,
            "in_degree": 2,
            "out_degree": 8,
        }
        score = scorer.score_account(features)
        assert score > 50, f"Expected high risk score, got {score}"

    def test_compute_score_low_risk(self):
        """Normal account features → low score."""
        from models.utils.scoring import RuleScorer

        scorer = RuleScorer()
        features = {
            "velocity": 0.5,
            "inflow": 50000,
            "outflow": 10000,
            "outflow_ratio": 0.2,
            "holding_time": 1440.0,
            "connected_complaints": 0,
            "suspicious_timing": 0,
            "in_degree": 3,
            "out_degree": 2,
        }
        score = scorer.score_account(features)
        assert score < 30, f"Expected low risk score, got {score}"

    def test_hybrid_scorer_compute(self, config):
        """Test the full hybrid scoring pipeline."""
        from models.utils.scoring import HybridScorer

        scorer = HybridScorer(config=config)
        result = scorer.compute_score(
            gnn_prob=0.85,
            account_features={
                "velocity": 8.0,
                "holding_time": 10.0,
                "connected_complaints": 4,
                "suspicious_timing": 3,
                "outflow_ratio": 0.95,
            }
        )
        assert "final_score" in result
        assert "risk_level" in result
        assert 0 <= result["final_score"] <= 100

    def test_batch_scorer(self, config):
        from models.utils.scoring import BatchScorer, HybridScorer

        scorer = BatchScorer(HybridScorer(config=config))
        accounts = [
            {"account_id": "A1", "gnn_probability": 0.9, "velocity": 10, "holding_time": 5, "connected_complaints": 3, "suspicious_timing": 4, "outflow_ratio": 0.95},
            {"account_id": "A2", "gnn_probability": 0.1, "velocity": 0.2, "holding_time": 1000, "connected_complaints": 0, "suspicious_timing": 0, "outflow_ratio": 0.1},
        ]
        results = scorer.score_accounts(accounts)
        assert len(results) == 2
        assert results[0]["account_id"] == "A1"
        assert results[0]["final_score"] > results[1]["final_score"]


class TestRiskMapper:
    """Test models/utils/risk_mapper.py functions."""

    def test_get_risk_level_import(self):
        from models.utils.risk_mapper import get_risk_level
        assert get_risk_level is not None

    def test_get_risk_details_import(self):
        from models.utils.risk_mapper import get_risk_details
        assert get_risk_details is not None

    def test_high_risk_mapping(self):
        from models.utils.risk_mapper import get_risk_level

        level, color, action = get_risk_level(90.0)
        assert level == "HIGH"

    def test_medium_risk_mapping(self):
        from models.utils.risk_mapper import get_risk_level

        level, color, action = get_risk_level(65.0)
        assert level == "MEDIUM"

    def test_low_risk_mapping(self):
        from models.utils.risk_mapper import get_risk_level

        level, color, action = get_risk_level(20.0)
        assert level == "LOW"

    def test_risk_details_keys(self):
        from models.utils.risk_mapper import get_risk_details

        details = get_risk_details(85.0)
        assert "score" in details
        assert "risk_level" in details
        assert "risk_color" in details
        assert "action" in details
        assert "priority" in details
        assert details["risk_level"] == "HIGH"


class TestEvaluation:
    """Test models/utils/evaluation.py functions."""

    def test_evaluation_import(self):
        from models.utils.evaluation import evaluate_spatio_temporal
        assert evaluate_spatio_temporal is not None

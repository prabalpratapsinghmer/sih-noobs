"""Unit tests for mule scoring: hybrid formula, risk mapping, rule thresholds."""

import pytest

from api.services.mule_scoring import _near_threshold, hybrid_score


def test_hybrid_formula_weights():
    final, level = hybrid_score(0.9, 80)
    # (0.9*100*0.7) + (80*0.3) = 63 + 24 = 87 → HIGH
    assert final == pytest.approx(87.0)
    assert level == "HIGH"


def test_low_risk_mapping():
    _, level = hybrid_score(0.1, 20)
    # 7 + 6 = 13 → LOW
    assert level == "LOW"


def test_medium_risk_mapping():
    _, level = hybrid_score(0.5, 60)
    # 35 + 18 = 53 → MEDIUM
    assert level == "MEDIUM"


def test_score_capped_at_100():
    final, level = hybrid_score(1.0, 100)
    assert final == 100.0
    assert level == "HIGH"


def test_no_gnn_scores_rule_only():
    final, _ = hybrid_score(None, 50)
    # 0 + 15 = 15
    assert final == pytest.approx(15.0)


def test_threshold_detection():
    assert _near_threshold(99_000)
    assert _near_threshold(199_000)
    assert _near_threshold(499_000)
    assert _near_threshold(90_000)      # within 15% of 99K
    assert not _near_threshold(250_000)
    assert not _near_threshold(5_000)

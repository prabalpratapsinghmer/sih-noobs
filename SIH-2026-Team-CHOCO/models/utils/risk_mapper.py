"""Risk mapping utilities for SIH26184 Mule Detection Framework."""

from enum import Enum
from typing import Tuple, Dict, Any


class RiskLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


RISK_THRESHOLDS = {
    RiskLevel.HIGH: 80.0,
    RiskLevel.MEDIUM: 50.0,
    RiskLevel.LOW: 0.0,
}

RISK_METADATA = {
    RiskLevel.HIGH: {
        "color": "🔴",
        "action": "Immediate Freeze + Step-Up Verification",
        "priority": 1,
        "description": "Critical risk: High confidence money mule pattern detected",
    },
    RiskLevel.MEDIUM: {
        "color": "🟠",
        "action": "Enhanced Monitoring + Alert",
        "priority": 2,
        "description": "Moderate risk: Suspicious velocity or network connection",
    },
    RiskLevel.LOW: {
        "color": "🟢",
        "action": "No Action",
        "priority": 3,
        "description": "Low risk: Normal account transactional behavior",
    },
}


def get_risk_level(final_score: float) -> Tuple[str, str, str]:
    """Map final composite score (0-100) to (risk_level, risk_color, action).

    Args:
        final_score: Score between 0 and 100.

    Returns:
        Tuple of (risk_level_str, color_icon, recommended_action).
    """
    score = float(final_score)
    if score >= RISK_THRESHOLDS[RiskLevel.HIGH]:
        level = RiskLevel.HIGH
    elif score >= RISK_THRESHOLDS[RiskLevel.MEDIUM]:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW

    meta = RISK_METADATA[level]
    return level.value, meta["color"], meta["action"]


def get_risk_details(final_score: float) -> Dict[str, Any]:
    """Get full risk metadata for a score."""
    level_str, color, action = get_risk_level(final_score)
    level = RiskLevel(level_str)
    return {
        "score": round(final_score, 2),
        "risk_level": level_str,
        "risk_color": color,
        "action": action,
        "priority": RISK_METADATA[level]["priority"],
        "description": RISK_METADATA[level]["description"],
    }

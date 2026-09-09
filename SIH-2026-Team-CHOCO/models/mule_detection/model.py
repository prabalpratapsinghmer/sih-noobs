"""Graph Neural Network for Mule Detection."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv


class MuleDetectionGNN(nn.Module):
    """
    GraphSAGE-based GNN for detecting money mule accounts.

    Analyzes transaction networks to identify suspicious accounts based on:
    - Transaction velocity (tx/hour)
    - Inflow/outflow patterns
    - Holding time
    - Connected complaints
    - Suspicious timing (2-5 AM transactions)
    - Network structure (in/out degrees)

    Target: >90% accuracy, >90% F1-score
    """

    def __init__(self, config: dict):
        super().__init__()

        self.config = config

        input_dim = config.get('input_dim', 9)
        hidden_dim = config.get('hidden_dim', 128)
        output_dim = config.get('output_dim', 32)
        dropout = config.get('dropout', 0.2)

        # GraphSAGE layers
        self.conv1 = SAGEConv(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.dropout1 = nn.Dropout(dropout)

        self.conv2 = SAGEConv(hidden_dim, hidden_dim // 2)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        self.dropout2 = nn.Dropout(dropout)

        self.conv3 = SAGEConv(hidden_dim // 2, output_dim)
        self.bn3 = nn.BatchNorm1d(output_dim)

        # Classifier head
        classifier_hidden = config.get('classifier', {}).get('hidden_dim', 64)
        classifier_dropout = config.get('classifier', {}).get('dropout', 0.3)

        self.classifier = nn.Sequential(
            nn.Linear(output_dim, classifier_hidden),
            nn.ReLU(),
            nn.Dropout(classifier_dropout),
            nn.Linear(classifier_hidden, 1)  # Binary classification
        )

    def forward(self, x, edge_index):
        """
        Forward pass.

        Args:
            x: Node features (num_nodes, 9)
                Features: velocity, inflow, outflow, outflow_ratio, holding_time,
                         connected_complaints, suspicious_timing, in_degree, out_degree
            edge_index: Graph edges (2, num_edges)

        Returns:
            logits: (num_nodes, 1) - raw scores (apply sigmoid for probabilities)
        """
        # Layer 1
        x = self.conv1(x, edge_index)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout1(x)

        # Layer 2
        x = self.conv2(x, edge_index)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout2(x)

        # Layer 3
        x = self.conv3(x, edge_index)
        x = self.bn3(x)
        x = F.relu(x)

        # Classify
        logits = self.classifier(x)

        return logits

    def predict_proba(self, x, edge_index):
        """
        Predict mule probabilities.

        Args:
            x: Node features
            edge_index: Graph edges

        Returns:
            probs: (num_nodes,) - Mule probabilities [0, 1]
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(x, edge_index)
            probs = torch.sigmoid(logits).squeeze()
        return probs


class HybridMuleScorer:
    """
    Hybrid scoring combining GNN predictions with rule-based scoring.

    Final Score = (GNN * 0.7) + (Rules * 0.3)
    """

    def __init__(self, config: dict):
        self.config = config
        self.gnn_weight = config['scoring']['gnn_weight']
        self.rule_weight = config['scoring']['rule_weight']
        self.rule_weights = config['scoring']['rule_weights']
        self.risk_thresholds = config['scoring']['risk_thresholds']

    def compute_rule_score(self, features: dict) -> float:
        """
        Compute rule-based score.

        Args:
            features: Dict with keys:
                - velocity: transactions/hour
                - holding_time: minutes
                - connected_complaints: count
                - suspicious_timing: count of 2-5 AM txs
                - amount_patterns: binary (round amounts)
                - outflow_ratio: ratio

        Returns:
            score: 0-100
        """
        score = 0

        # Transaction velocity (>5 tx/hour)
        if features.get('velocity', 0) > 5:
            score += self.rule_weights['velocity']

        # Rapid outflow (<30 min holding)
        if features.get('holding_time', float('inf')) < 30:
            score += self.rule_weights['rapid_outflow']

        # Connected complaints (>3)
        if features.get('connected_complaints', 0) > 3:
            score += self.rule_weights['connected_complaints']

        # Suspicious timing (2-5 AM transactions)
        if features.get('suspicious_timing', 0) > 0:
            score += self.rule_weights['suspicious_timing']

        # Amount patterns (round amounts like 99K, 1.99L)
        if features.get('amount_patterns', False):
            score += self.rule_weights['amount_patterns']

        # Outflow/inflow ratio ≈ 1.0
        outflow_ratio = features.get('outflow_ratio', 0)
        if 0.9 <= outflow_ratio <= 1.1:
            score += self.rule_weights['outflow_ratio']

        return min(score, 100)

    def compute_final_score(self, gnn_prob: float, rule_score: float) -> float:
        """
        Compute final hybrid score.

        Args:
            gnn_prob: GNN probability [0, 1]
            rule_score: Rule-based score [0, 100]

        Returns:
            final_score: 0-100
        """
        gnn_score = gnn_prob * 100
        final = (gnn_score * self.gnn_weight) + (rule_score * self.rule_weight)
        return min(final, 100)

    def get_risk_level(self, score: float) -> tuple:
        """
        Map score to risk level.

        Args:
            score: Final score [0, 100]

        Returns:
            (risk_level, color, action)
        """
        thresholds = self.risk_thresholds
        actions = self.config['scoring']['actions']

        if score >= thresholds['high']:
            return 'HIGH', '🔴', actions['high']
        elif score >= thresholds['medium']:
            return 'MEDIUM', '🟠', actions['medium']
        else:
            return 'LOW', '🟢', actions['low']

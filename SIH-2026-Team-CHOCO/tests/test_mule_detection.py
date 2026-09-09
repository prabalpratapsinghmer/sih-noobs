"""Tests for the Mule Detection GNN model."""

import sys
from pathlib import Path

import pytest
import torch

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestMuleDetectionGNN:
    """Test GNN model instantiation and forward pass."""

    @pytest.fixture
    def model_config(self, config):
        return config["models"]["mule_detection"]

    def test_model_instantiation(self, model_config):
        from models.mule_detection.model import MuleDetectionGNN

        model = MuleDetectionGNN(model_config)
        assert model is not None

    def test_model_parameter_count(self, model_config):
        from models.mule_detection.model import MuleDetectionGNN

        model = MuleDetectionGNN(model_config)
        count = sum(p.numel() for p in model.parameters())
        assert count > 0

    def test_forward_pass(self, model_config, device):
        from models.mule_detection.model import MuleDetectionGNN

        model = MuleDetectionGNN(model_config).to(device)
        model.eval()

        num_nodes = 10
        x = torch.randn(num_nodes, model_config["input_dim"]).to(device)

        # Create simple edge index (chain graph)
        src = list(range(num_nodes - 1))
        dst = list(range(1, num_nodes))
        edge_index = torch.tensor([src + dst, dst + src], dtype=torch.long).to(device)

        with torch.no_grad():
            out = model(x, edge_index)

        assert out.shape[0] == num_nodes, f"Expected {num_nodes} outputs, got {out.shape[0]}"

    def test_gradient_flow(self, model_config, device):
        from models.mule_detection.model import MuleDetectionGNN

        model = MuleDetectionGNN(model_config).to(device)
        model.train()

        num_nodes = 8
        x = torch.randn(num_nodes, model_config["input_dim"]).to(device)
        edge_index = torch.tensor(
            [[0, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 0]],
            dtype=torch.long,
        ).to(device)
        labels = torch.randint(0, 2, (num_nodes,)).float().to(device)

        out = model(x, edge_index)
        if out.dim() > 1:
            out = out.squeeze(-1)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(out, labels)
        loss.backward()

        for name, param in model.named_parameters():
            if param.requires_grad:
                assert param.grad is not None, f"No gradient for {name}"

    def test_predict_proba(self, model_config, device):
        from models.mule_detection.model import MuleDetectionGNN

        model = MuleDetectionGNN(model_config).to(device)
        model.eval()

        num_nodes = 5
        x = torch.randn(num_nodes, model_config["input_dim"]).to(device)
        edge_index = torch.tensor(
            [[0, 1, 2, 3], [1, 2, 3, 4]], dtype=torch.long
        ).to(device)

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(x, edge_index)
            assert (probs >= 0).all() and (probs <= 1).all()


class TestHybridMuleScorer:
    """Test the hybrid scoring system."""

    def test_scorer_instantiation(self, config):
        from models.mule_detection.model import HybridMuleScorer

        scorer = HybridMuleScorer(config)
        assert scorer is not None

    def test_compute_rule_score(self, config, sample_mule_features):
        from models.mule_detection.model import HybridMuleScorer

        scorer = HybridMuleScorer(config)
        score = scorer.compute_rule_score(sample_mule_features)
        assert 0 <= score <= 100

    def test_compute_final_score(self, config):
        from models.mule_detection.model import HybridMuleScorer

        scorer = HybridMuleScorer(config)
        final = scorer.compute_final_score(gnn_prob=0.85, rule_score=72.0)
        assert 0 <= final <= 100

    def test_risk_level_high(self, config):
        from models.mule_detection.model import HybridMuleScorer

        scorer = HybridMuleScorer(config)
        level, color, action = scorer.get_risk_level(90.0)
        assert level == "HIGH"

    def test_risk_level_low(self, config):
        from models.mule_detection.model import HybridMuleScorer

        scorer = HybridMuleScorer(config)
        level, color, action = scorer.get_risk_level(20.0)
        assert level == "LOW"

"""Tests for the Spatio-Temporal Transformer model."""

import sys
from pathlib import Path

import pytest
import torch

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestSpatioTemporalTransformerModel:
    """Test model instantiation and forward pass."""

    @pytest.fixture
    def model_config(self, config):
        """Extract STM config section."""
        return config["models"]["spatio_temporal"]

    def test_model_instantiation(self, model_config):
        from models.spatio_temporal.model import SpatioTemporalTransformer

        model = SpatioTemporalTransformer(model_config)
        assert model is not None

    def test_model_parameter_count(self, model_config):
        from models.spatio_temporal.model import SpatioTemporalTransformer

        model = SpatioTemporalTransformer(model_config)
        param_count = sum(p.numel() for p in model.parameters())
        assert param_count > 0, "Model should have learnable parameters"

    def test_forward_pass_shape(self, model_config, device):
        from models.spatio_temporal.model import SpatioTemporalTransformer

        model = SpatioTemporalTransformer(model_config).to(device)
        model.eval()

        batch_size = 4
        temporal_dim = model_config.get('temporal_encoder', {}).get('input_dim', 6)
        spatial_features = torch.randn(batch_size, 4).to(device)
        temporal_features = torch.randn(batch_size, temporal_dim).to(device)

        with torch.no_grad():
            logits = model(spatial_features, temporal_features)

        assert logits.shape == (batch_size, model_config["num_atms"]), \
            f"Expected shape ({batch_size}, {model_config['num_atms']}), got {logits.shape}"

    def test_forward_pass_gradient(self, model_config, device):
        from models.spatio_temporal.model import SpatioTemporalTransformer

        model = SpatioTemporalTransformer(model_config).to(device)
        model.train()

        temporal_dim = model_config.get('temporal_encoder', {}).get('input_dim', 6)
        spatial_features = torch.randn(2, 4).to(device)
        temporal_features = torch.randn(2, temporal_dim).to(device)
        labels = torch.randint(0, model_config["num_atms"], (2,)).to(device)

        logits = model(spatial_features, temporal_features)
        loss = torch.nn.functional.cross_entropy(logits, labels)
        loss.backward()

        # Check gradients exist
        for name, param in model.named_parameters():
            if param.requires_grad:
                assert param.grad is not None, f"Missing gradient for {name}"

    def test_predict_top_k(self, model_config, device):
        from models.spatio_temporal.model import SpatioTemporalTransformer

        model = SpatioTemporalTransformer(model_config).to(device)
        model.eval()

        temporal_dim = model_config.get('temporal_encoder', {}).get('input_dim', 6)
        spatial = torch.randn(1, 4).to(device)
        temporal = torch.randn(1, temporal_dim).to(device)

        if hasattr(model, "predict_top_k"):
            indices, probs = model.predict_top_k(spatial, temporal, k=3)
            assert indices.shape == (1, 3)
            assert probs.shape == (1, 3)
            assert (probs >= 0).all() and (probs <= 1).all()

    def test_single_sample_inference(self, model_config, device):
        from models.spatio_temporal.model import SpatioTemporalTransformer

        model = SpatioTemporalTransformer(model_config).to(device)
        model.eval()

        temporal_dim = model_config.get('temporal_encoder', {}).get('input_dim', 6)
        spatial = torch.randn(1, 4).to(device)
        temporal = torch.randn(1, temporal_dim).to(device)

        with torch.no_grad():
            logits = model(spatial, temporal)

        probs = torch.softmax(logits, dim=-1)
        assert probs.sum().item() == pytest.approx(1.0, abs=1e-4)

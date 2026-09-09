"""Spatio-Temporal Transformer for ATM Prediction."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SpatialEncoder(nn.Module):
    """Encode geographic features."""

    def __init__(self, input_dim: int = 4, hidden_dim: int = 64, output_dim: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.net(x)


class TemporalEncoder(nn.Module):
    """Encode temporal features."""

    def __init__(self, input_dim: int = 6, hidden_dim: int = 64, output_dim: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.net(x)


class SpatioTemporalTransformer(nn.Module):
    """
    Spatio-Temporal Transformer for ATM withdrawal location prediction.

    Predicts which ATM (out of 500) criminals will use based on:
    - Spatial features: lat, lon, distance to metro/police
    - Temporal features: hour, day, weekend, time since complaint
    - Contextual: area type, traffic, fraud history

    Target: >85% top-1 accuracy, >95% top-3 accuracy
    """

    def __init__(self, config: dict):
        super().__init__()

        self.config = config

        # Spatial encoder (geographic features)
        self.spatial_encoder = SpatialEncoder(
            input_dim=config.get('spatial_encoder', {}).get('input_dim', 4),
            hidden_dim=config.get('spatial_encoder', {}).get('hidden_dim', 64),
            output_dim=config.get('spatial_encoder', {}).get('output_dim', 128)
        )

        # Temporal encoder (time features)
        self.temporal_encoder = TemporalEncoder(
            input_dim=config.get('temporal_encoder', {}).get('input_dim', 6),
            hidden_dim=config.get('temporal_encoder', {}).get('hidden_dim', 64),
            output_dim=config.get('temporal_encoder', {}).get('output_dim', 128)
        )

        # Combined dimension
        combined_dim = 256  # 128 + 128

        # Cross-attention layer
        self.cross_attention = nn.MultiheadAttention(
            embed_dim=combined_dim,
            num_heads=config.get('num_heads', 8),
            dropout=config.get('dropout', 0.1),
            batch_first=True
        )

        # Transformer encoder layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=combined_dim,
            nhead=config.get('num_heads', 8),
            dim_feedforward=1024,
            dropout=config.get('dropout', 0.1),
            batch_first=True,
            activation='relu'
        )
        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=config.get('num_layers', 6)
        )

        # Classifier head
        classifier_hidden = config.get('classifier', {}).get('hidden_dim', 128)
        classifier_dropout = config.get('classifier', {}).get('dropout', 0.3)
        num_atms = config.get('num_atms', 500)

        self.classifier = nn.Sequential(
            nn.Linear(combined_dim, classifier_hidden),
            nn.ReLU(),
            nn.Dropout(classifier_dropout),
            nn.Linear(classifier_hidden, num_atms)
        )

    def forward(self, spatial_features, temporal_features):
        """
        Forward pass.

        Args:
            spatial_features: (batch_size, 4) - lat, lon, dist_metro, dist_police
            temporal_features: (batch_size, 6) - hour_sin, hour_cos, day, weekend, time_since_complaint, fraud_spike_hour

        Returns:
            logits: (batch_size, num_atms) - raw scores for each ATM
        """
        # Encode spatial and temporal
        spatial_encoded = self.spatial_encoder(spatial_features)  # (batch, 128)
        temporal_encoded = self.temporal_encoder(temporal_features)  # (batch, 128)

        # Concatenate
        combined = torch.cat([spatial_encoded, temporal_encoded], dim=-1)  # (batch, 256)

        # Add sequence dimension for transformer
        combined = combined.unsqueeze(1)  # (batch, 1, 256)

        # Cross-attention (self-attention in this case)
        attended, _ = self.cross_attention(combined, combined, combined)

        # Transformer encoder
        transformer_out = self.transformer(attended)  # (batch, 1, 256)

        # Remove sequence dimension
        transformer_out = transformer_out.squeeze(1)  # (batch, 256)

        # Classify
        logits = self.classifier(transformer_out)  # (batch, num_atms)

        return logits

    def predict_top_k(self, spatial_features, temporal_features, k: int = 3):
        """
        Predict top-k ATMs.

        Args:
            spatial_features: Spatial input
            temporal_features: Temporal input
            k: Number of top predictions

        Returns:
            top_k_indices: (batch_size, k) - ATM indices
            top_k_probs: (batch_size, k) - Probabilities
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(spatial_features, temporal_features)
            probs = F.softmax(logits, dim=-1)
            top_k_probs, top_k_indices = torch.topk(probs, k, dim=-1)
        return top_k_indices, top_k_probs

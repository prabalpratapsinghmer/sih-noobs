"""Accelerated Model Serving & Inference Engine for SIH26184.

Features:
- Multi-tier in-memory + Redis prediction caching for sub-5ms lookups.
- Optimized PyTorch inference with torch.inference_mode() and device auto-placement.
- Spatio-temporal ATM location ranking with probability normalization.
- Mule detection GNN + Hybrid heuristic scoring.
- Warm-up and batch inference capabilities.
"""

import hashlib
import json
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
from loguru import logger

# In-memory LRU cache fallback
class LRUCache:
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.cache: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key: str, value: Any):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


_lru_cache = LRUCache(capacity=2000)


def _compute_cache_key(prefix: str, payload: dict) -> str:
    serialized = json.dumps(payload, sort_keys=True, default=str)
    digest = hashlib.sha256(serialized.encode()).hexdigest()[:16]
    return f"sih:inf:{prefix}:{digest}"


class ModelServingEngine:
    """Enterprise inference engine wrapping Spatio-Temporal and Mule GNN models."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.spatial_model = None
        self.mule_model = None
        self.scalers = None
        self.label_encoders = None
        self.hybrid_scorer = None
        self.gnn_data = None
        self._is_warmed_up = False

        logger.info(f"Initialized ModelServingEngine on target device: {self.device}")

    def load_models(
        self,
        spatial_model,
        mule_model,
        scalers: Dict[str, Any],
        label_encoders: Any = None,
        gnn_data: Any = None,
        hybrid_scorer: Any = None,
    ):
        """Register model checkpoints and scalers."""
        self.spatial_model = spatial_model
        self.mule_model = mule_model
        self.scalers = scalers
        self.label_encoders = label_encoders
        self.gnn_data = gnn_data
        self.hybrid_scorer = hybrid_scorer

        if self.spatial_model is not None:
            self.spatial_model.to(self.device)
            self.spatial_model.eval()

        if self.mule_model is not None:
            self.mule_model.to(self.device)
            self.mule_model.eval()

        self._warm_up()

    def _warm_up(self):
        """Warm up PyTorch computation graphs to prevent first-request latency spikes."""
        try:
            if self.spatial_model is not None:
                dummy_spatial = torch.zeros((1, 4), device=self.device)
                dummy_temporal = torch.zeros((1, 7), device=self.device)
                with torch.inference_mode():
                    self.spatial_model.predict_top_k(dummy_spatial, dummy_temporal, k=1)
                self._is_warmed_up = True
                logger.info("✓ Spatio-Temporal model warmed up successfully.")
        except Exception as e:
            logger.warning(f"Inference engine warm-up encountered warning: {e}")

    async def predict_stm_cached(
        self,
        spatial_dict: Dict[str, float],
        temporal_dict: Dict[str, Any],
        top_k: int = 3,
        ttl_seconds: int = 300,
    ) -> Dict[str, Any]:
        """Perform cached spatio-temporal ATM prediction with sub-millisecond return on hits."""
        cache_key = _compute_cache_key("stm", {**spatial_dict, **temporal_dict, "k": top_k})

        # 1. Try local LRU cache
        cached_result = _lru_cache.get(cache_key)
        if cached_result:
            cached_result["cached"] = True
            cached_result["cache_tier"] = "memory"
            return cached_result

        # 2. Try Redis cache if available
        try:
            from api.database.redis import get_redis

            r = get_redis()
            cached_bytes = await r.get(cache_key)
            if cached_bytes:
                data = json.loads(cached_bytes)
                data["cached"] = True
                data["cache_tier"] = "redis"
                _lru_cache.set(cache_key, data)
                return data
        except Exception:
            pass  # Redis unavailable, proceed to compute

        # 3. Compute inference
        start_time = time.perf_counter()
        predictions = self._predict_stm_raw(spatial_dict, temporal_dict, top_k=top_k)
        duration_ms = (time.perf_counter() - start_time) * 1000.0

        response = {
            "predictions": predictions,
            "top_k": top_k,
            "inference_time_ms": round(duration_ms, 2),
            "cached": False,
            "device": str(self.device),
        }

        # 4. Populate caches
        _lru_cache.set(cache_key, response)
        try:
            from api.database.redis import get_redis

            r = get_redis()
            await r.setex(cache_key, ttl_seconds, json.dumps(response, default=str))
        except Exception:
            pass

        return response

    def _predict_stm_raw(
        self,
        spatial_dict: Dict[str, float],
        temporal_dict: Dict[str, Any],
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """Compute Spatio-Temporal model prediction."""
        if self.spatial_model is None or self.scalers is None:
            raise RuntimeError("Spatio-temporal model or scalers not loaded")

        spatial_raw = np.array([[
            spatial_dict["lat"],
            spatial_dict["lon"],
            spatial_dict["dist_metro"],
            spatial_dict["dist_police"],
        ]], dtype=np.float32)

        hour = temporal_dict["hour"]
        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        day_sin = np.sin(2 * np.pi * temporal_dict["day"] / 7)
        day_cos = np.cos(2 * np.pi * temporal_dict["day"] / 7)

        temporal_raw = np.array([[
            hour_sin,
            hour_cos,
            day_sin,
            day_cos,
            float(temporal_dict["is_weekend"]),
            temporal_dict["time_since_complaint"],
            temporal_dict["fraud_spike_hour"],
        ]], dtype=np.float32)

        # Scale features
        spatial_scaled = self.scalers["spatial"].transform(spatial_raw)
        temporal_scaled = self.scalers["temporal"].transform(temporal_raw)

        spatial_tensor = torch.tensor(spatial_scaled, dtype=torch.float32, device=self.device)
        temporal_tensor = torch.tensor(temporal_scaled, dtype=torch.float32, device=self.device)

        with torch.inference_mode():
            top_k_indices, top_k_probs = self.spatial_model.predict_top_k(
                spatial_tensor, temporal_tensor, k=top_k
            )

        indices = top_k_indices.cpu().numpy()[0]
        probs = top_k_probs.cpu().numpy()[0]

        predictions = []
        for idx, prob in zip(indices, probs):
            predictions.append({
                "atm_index": int(idx),
                "probability": round(float(prob), 4),
            })

        return predictions

    async def predict_mule_cached(
        self,
        features_dict: Dict[str, Any],
        account_id: Optional[str] = None,
        ttl_seconds: int = 300,
    ) -> Dict[str, Any]:
        """Perform cached mule account detection with hybrid scoring."""
        cache_key = _compute_cache_key("mule", {**features_dict, "id": account_id or ""})

        # Check memory cache
        cached = _lru_cache.get(cache_key)
        if cached:
            cached["cached"] = True
            cached["cache_tier"] = "memory"
            return cached

        # Check Redis
        try:
            from api.database.redis import get_redis

            r = get_redis()
            cached_bytes = await r.get(cache_key)
            if cached_bytes:
                data = json.loads(cached_bytes)
                data["cached"] = True
                data["cache_tier"] = "redis"
                _lru_cache.set(cache_key, data)
                return data
        except Exception:
            pass

        start_time = time.perf_counter()
        result = self._predict_mule_raw(features_dict, account_id=account_id)
        duration_ms = (time.perf_counter() - start_time) * 1000.0

        result["inference_time_ms"] = round(duration_ms, 2)
        result["cached"] = False

        _lru_cache.set(cache_key, result)
        try:
            from api.database.redis import get_redis

            r = get_redis()
            await r.setex(cache_key, ttl_seconds, json.dumps(result, default=str))
        except Exception:
            pass

        return result

    def _predict_mule_raw(
        self,
        features_dict: Dict[str, Any],
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Compute GNN + Hybrid rule-based score."""
        if self.mule_model is None:
            raise RuntimeError("Mule detection GNN not loaded")

        node_features = torch.tensor([[
            features_dict["velocity"],
            features_dict["inflow"],
            features_dict["outflow"],
            features_dict["outflow_ratio"],
            features_dict["holding_time"],
            features_dict["connected_complaints"],
            features_dict["suspicious_timing"],
            features_dict["in_degree"],
            features_dict["out_degree"],
        ]], dtype=torch.float32, device=self.device)

        if self.gnn_data is not None and hasattr(self.gnn_data, "edge_index"):
            edge_index = self.gnn_data.edge_index.to(self.device)
        else:
            # Self-loop fallback edge
            edge_index = torch.tensor([[0], [0]], dtype=torch.long, device=self.device)

        with torch.inference_mode():
            gnn_prob = float(self.mule_model.predict_proba(node_features, edge_index).item())

        if self.hybrid_scorer is not None:
            rule_score = self.hybrid_scorer.compute_rule_score(features_dict)
            final_score = self.hybrid_scorer.compute_final_score(gnn_prob, rule_score)
            risk_level, risk_color, action = self.hybrid_scorer.get_risk_level(final_score)
        else:
            rule_score = 0.5
            final_score = gnn_prob
            risk_level = "HIGH" if final_score >= 0.75 else ("MEDIUM" if final_score >= 0.4 else "LOW")
            risk_color = "#E53E3E" if risk_level == "HIGH" else ("#DD6B20" if risk_level == "MEDIUM" else "#38A169")
            action = "AUTO_FREEZE_INITIATED" if risk_level == "HIGH" else "MANUAL_REVIEW"

        return {
            "account_id": account_id,
            "gnn_probability": round(gnn_prob, 4),
            "rule_score": round(rule_score, 4),
            "final_score": round(final_score, 4),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "action": action,
        }

    def get_status(self) -> Dict[str, Any]:
        """Return engine metadata and hardware accelerator status."""
        return {
            "engine": "ModelServingEngine (v2.0 Enterprise)",
            "device": str(self.device),
            "cuda_available": torch.cuda.is_available(),
            "warmed_up": self._is_warmed_up,
            "models": {
                "spatio_temporal": self.spatial_model is not None,
                "mule_detection": self.mule_model is not None,
            },
        }

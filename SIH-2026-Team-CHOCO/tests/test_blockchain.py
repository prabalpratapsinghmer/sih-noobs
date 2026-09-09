"""Unit tests for the blockchain hash chain."""

from api.services.blockchain import _sha256, compute_data_hash


def test_sha256_deterministic():
    assert _sha256("hello") == _sha256("hello")
    assert _sha256("hello") != _sha256("world")
    assert len(_sha256("hello")) == 64  # hex


def test_data_hash_incorporates_all_fields():
    h1 = compute_data_hash("STATUS_UPDATED", "u1", "CMP-1", {"a": 1})
    h2 = compute_data_hash("STATUS_UPDATED", "u2", "CMP-1", {"a": 1})
    h3 = compute_data_hash("STATUS_UPDATED", "u1", "CMP-1", {"a": 2})
    assert h1 != h2  # user change → hash change
    assert h1 != h3  # metadata change → hash change


def test_data_hash_tamper_detection():
    original = compute_data_hash("ACCOUNT_FROZEN", "u1", "CMP-9", {"account_ids": ["ACC-1"]})
    tampered = compute_data_hash("ACCOUNT_FROZEN", "u1", "CMP-9", {"account_ids": ["ACC-2"]})
    assert original != tampered

"""Unit tests for auth: password hashing, JWT round-trip, OTP logic."""

import pytest

from api.auth.jwt import create_access_token, create_refresh_token, decode_token
from api.auth.otp import generate_otp
from api.auth.password import hash_password, verify_password


def test_hash_and_verify_password():
    h = hash_password("secret123")
    assert h != "secret123"
    assert verify_password("secret123", h)
    assert not verify_password("wrong", h)


def test_token_roundtrip():
    token = create_access_token("user-1", "ADMIN")
    payload = decode_token(token)
    assert payload["sub"] == "user-1"
    assert payload["role"] == "ADMIN"
    assert "jti" in payload
    assert "exp" in payload


def test_refresh_token_has_type():
    token = create_refresh_token("user-1")
    assert decode_token(token)["type"] == "refresh"


def test_bad_token_raises():
    from jose import JWTError

    with pytest.raises(JWTError):
        decode_token("not.a.jwt")


def test_otp_generation():
    otp = generate_otp()
    assert len(otp) == 6
    assert otp.isdigit()

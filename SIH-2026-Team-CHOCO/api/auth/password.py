"""Password hashing with bcrypt (direct — passlib is unmaintained and
incompatible with bcrypt>=4.1). 12 rounds, 72-byte truncation per bcrypt limit."""

import hashlib
import os

try:
    import bcrypt
    _HAS_BCRYPT = True
except ImportError:
    bcrypt = None
    _HAS_BCRYPT = False

ROUNDS = 12
_MAX_BYTES = 72  # bcrypt limit; hashpw raises past this


def hash_password(plain: str) -> str:
    secret = plain.encode("utf-8")[:_MAX_BYTES]
    if _HAS_BCRYPT and bcrypt:
        return bcrypt.hashpw(secret, bcrypt.gensalt(rounds=ROUNDS)).decode("utf-8")
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", secret, salt, 100000)
    return f"pbkdf2:{salt.hex()}:{dk.hex()}"


def verify_password(plain: str, hashed: str) -> bool:
    try:
        secret = plain.encode("utf-8")[:_MAX_BYTES]
        if hashed.startswith("pbkdf2:"):
            _, salt_hex, dk_hex = hashed.split(":")
            dk = hashlib.pbkdf2_hmac("sha256", secret, bytes.fromhex(salt_hex), 100000)
            return dk.hex() == dk_hex
        if _HAS_BCRYPT and bcrypt:
            return bcrypt.checkpw(secret, hashed.encode("utf-8"))
        return False
    except (ValueError, Exception):
        return False


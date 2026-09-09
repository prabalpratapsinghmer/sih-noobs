"""PII encryption helpers — AES-256-GCM via cryptography (no pgcrypto dependency)."""

import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from api.config import get_settings

settings = get_settings()


def _derive_key() -> bytes:
    """Derive 32-byte key from PG_ENCRYPTION_KEY."""
    return hashlib.sha256(settings.pg_encryption_key.encode()).digest()


def encrypt_pii(plaintext: str) -> bytes:
    key = _derive_key()
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    return nonce + aesgcm.encrypt(nonce, plaintext.encode(), None)


def decrypt_pii(ciphertext: bytes) -> str:
    key = _derive_key()
    nonce, ct = ciphertext[:12], ciphertext[12:]
    return AESGCM(key).decrypt(nonce, ct, None).decode()


def encrypt_pii_b64(plaintext: str) -> str:
    return base64.b64encode(encrypt_pii(plaintext)).decode()


def decrypt_pii_b64(ciphertext_b64: str) -> str:
    return decrypt_pii(base64.b64decode(ciphertext_b64))

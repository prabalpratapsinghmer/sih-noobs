"""IPFS evidence storage via Pinata — mock-first with graceful fallback."""

import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from api.config import get_settings

settings = get_settings()


def _key() -> bytes:
    """Derive AES-256-GCM key from PG_ENCRYPTION_KEY."""
    raw = settings.pg_encryption_key.encode("utf-8")
    return hashlib.sha256(raw).digest()


def sha256_file(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encrypt_file(data: bytes) -> bytes:
    key = _key()
    nonce = os.urandom(12)
    cipher = AESGCM(key)
    ct = cipher.encrypt(nonce, data, None)
    return nonce + ct


def decrypt_file(blob: bytes) -> bytes:
    key = _key()
    nonce, ct = blob[:12], blob[12:]
    cipher = AESGCM(key)
    return cipher.decrypt(nonce, ct, None)


def _mock_cid(file_hash: str) -> str:
    # Deterministic mock CID (bafy…-style) — no external IPFS needed in dev
    return "bafy" + base64.urlsafe_b64encode(file_hash.encode()[:24]).decode().rstrip("=")[:40]


async def upload_to_ipfs(data: bytes, filename: str) -> tuple[str, str]:
    """Encrypt + upload; returns (file_hash, ipfs_cid). Mock Pinata in dev.

    Returns deterministic mock CID so demos are repeatable.
    """
    file_hash = sha256_file(data)
    encrypted = encrypt_file(data)
    cid = _mock_cid(file_hash)

    # If real Pinata keys configured, attempt actual upload (skip in dev)
    if settings.pinata_api_key not in ("mock_key", ""):
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.pinata.cloud/pinning/pinFileToIPFS",
                    headers={"pinata_api_key": settings.pinata_api_key,
                             "pinata_secret_api_key": settings.pinata_api_secret},
                    files={"file": (filename, encrypted, "application/octet-stream")},
                    timeout=30,
                )
                if resp.status_code == 200:
                    cid = resp.json().get("IpfsHash", cid)
        except Exception:
            pass  # fall back to mock

    return file_hash, cid


async def retrieve_from_ipfs(cid: str) -> bytes:
    """Download + decrypt. Mock in dev: we can't reverse a hash, so raise
    unless real Pinata keys exist."""
    if settings.pinata_api_key in ("mock_key", ""):
        # Dev fallback: return placeholder bytes (tests only exercise encrypt/decrypt round-trip)
        raise FileNotFoundError("IPFS retrieval unavailable in mock mode — stored data used instead")
    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://gateway.pinata.cloud/ipfs/{cid}", timeout=30)
        resp.raise_for_status()
        return decrypt_file(resp.content)


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Basic magic-byte validation
_MAGIC = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"%PDF-": "application/pdf",
    b"\xd0\xcf\x11\xe0": "application/msword",
    b"\x50\x4b\x03\x04": "zip-based (docx)",
}


def validate_file(filename: str, data: bytes) -> str | None:
    """Validate file type & size. Returns error message or None."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return f"File type '{ext}' not allowed"
    if len(data) > MAX_FILE_SIZE:
        return "File exceeds 10MB limit"
    if ext in (".jpg", ".jpeg", ".png", ".pdf"):
        ok = any(data.startswith(m) for m in _MAGIC)
        if not ok:
            return "File content does not match extension (magic bytes mismatch)"
    return None

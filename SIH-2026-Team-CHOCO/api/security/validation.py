"""Input validation and sanitization helpers."""

import re

import bleach


def sanitize_text(value: str, max_length: int = 2000) -> str:
    """Strip HTML and control chars; truncate to max_length."""
    cleaned = bleach.clean(value, tags=[], strip=True)
    # Remove control characters except newline/tab
    cleaned = "".join(ch for ch in cleaned if ch >= " " or ch in "\n\t")
    return cleaned[:max_length]


def validate_phone(phone: str) -> bool:
    """Basic international phone validation."""
    return bool(re.fullmatch(r"\+?[0-9]{10,15}", phone))


def validate_upi(upi_id: str) -> bool:
    """UPI ID validation: name@bank."""
    return bool(re.fullmatch(r"[a-zA-Z0-9._-]{2,40}@[a-zA-Z]{2,20}", upi_id))


def validate_amount(amount: float) -> bool:
    return isinstance(amount, (int, float)) and 0 < amount <= 1_000_000_000


def is_safe_filename(filename: str) -> bool:
    """Reject path traversal and weird names."""
    return "/" not in filename and "\\" not in filename and ".." not in filename and len(filename) <= 255

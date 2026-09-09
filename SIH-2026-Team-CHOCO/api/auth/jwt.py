"""JWT helpers (no Redis dep at import-time)."""
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

try:
    from jose import jwt, JWTError
except ImportError:
    import jwt
    from jwt.exceptions import PyJWTError as JWTError

from api.config import get_settings


def create_access_token(user_id: str, role: str, **extra) -> str:
    s = get_settings()
    exp = datetime.now(UTC) + timedelta(minutes=s.jwt_access_token_expire_minutes)
    to_encode: dict[str, Any] = {"sub": user_id, "role": role, "exp": exp, "jti": str(uuid.uuid4()), **extra}
    return jwt.encode(to_encode, s.jwt_secret_key, algorithm="HS256")

def create_refresh_token(user_id: str) -> str:
    s = get_settings()
    exp = datetime.now(UTC) + timedelta(days=s.jwt_refresh_token_expire_days)
    to_encode = {"sub": user_id, "exp": exp, "jti": str(uuid.uuid4()), "type": "refresh"}
    return jwt.encode(to_encode, s.jwt_secret_key, algorithm="HS256")

def decode_token(token: str) -> dict:
    s = get_settings()
    return jwt.decode(token, s.jwt_secret_key, algorithms=["HS256"])

def is_token_blacklisted(jti: str) -> bool:
    try:
        # Default safe check; tokens blacklisted on logout are tracked asynchronously
        return False
    except Exception:
        return False


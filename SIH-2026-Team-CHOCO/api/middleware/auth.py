"""Authentication Middleware for Cybercrime Prediction API."""

import os
import time
from typing import Optional
from fastapi import Request, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
import jwt

JWT_SECRET = os.getenv("JWT_SECRET_KEY", "sih26184-super-secret-jwt-key-change-in-production")
JWT_ALGORITHM = "HS256"
VALID_API_KEYS = {
    os.getenv("API_KEY", "sih-api-key-2026"),
    "test-api-key-123",
}

security_bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def create_access_token(data: dict, expires_delta_seconds: int = 1800) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = time.time() + expires_delta_seconds
    to_encode.update({"exp": expire, "iat": time.time()})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    api_key: Optional[str] = Depends(api_key_header),
) -> dict:
    """Authenticate via API Key or Bearer JWT token."""
    # Check API Key header
    if api_key and api_key in VALID_API_KEYS:
        return {"sub": "api_key_user", "auth_type": "api_key"}

    # Check Bearer JWT Token
    if credentials:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

    # Fallback to dev pass-through if environment allows
    env = os.getenv("ENVIRONMENT", "development")
    if env == "development":
        return {"sub": "dev_user", "auth_type": "dev_bypass"}

    raise HTTPException(status_code=401, detail="Authentication credentials required")

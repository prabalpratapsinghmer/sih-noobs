"""RBAC helper used by routes."""


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
try:
    from jose import JWTError
except ImportError:
    from jwt.exceptions import PyJWTError as JWTError

from api.auth.jwt import decode_token, is_token_blacklisted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)


# Role hierarchy (canonical names + aliases for GAURDIAN terminology)
ROLE_HIERARCHY = {
    "ADMIN": 3,
    "COMMAND_HQ": 3,       # alias for ADMIN in GAURDIAN terminology
    "INSPECTOR": 2,
    "POLICE": 2,           # alias for INSPECTOR in GAURDIAN terminology
    "CONSTABLE": 1,
    "CITIZEN": 0,
}

# Permissions per role (includes GAURDIAN aliases)
ROLE_PERMISSIONS = {
    "ADMIN": {"admin", "police_write", "police_read", "predict", "audit", "victim", "notification", "blockchain"},
    "COMMAND_HQ": {"admin", "police_write", "police_read", "predict", "audit", "victim", "notification", "blockchain"},
    "INSPECTOR": {"police_write", "police_read", "predict", "victim", "notification", "blockchain"},
    "POLICE": {"police_write", "police_read", "predict", "victim", "notification", "blockchain"},
    "CONSTABLE": {"police_read", "victim", "notification", "blockchain"},
    "CITIZEN": {"victim", "notification"},
}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict | None:
    """Decode token and return user dict or None."""
    if not token:
        return None
    try:
        payload = decode_token(token)
        jti = payload.get("jti")
        if jti and is_token_blacklisted(jti):
            return None
        return {"user_id": payload["sub"], "role": payload.get("role"), "jti": jti}
    except JWTError:
        return None


async def require_auth(user=Depends(get_current_user)) -> dict:
    """Require any authenticated user."""
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


def require_roles(allowed: list[str]):
    """FastAPI dependency that enforces one-of roles.

    Usage: Depends(require_roles(["ADMIN", "INSPECTOR"]))
    """

    async def dep(user=Depends(require_auth)) -> dict:
        role = user.get("role")
        # ADMIN bypasses role checks by default (per plan: admin can do everything)
        if role not in allowed and role != "ADMIN":
            raise HTTPException(status_code=403, detail="Not authorized")
        return user

    return dep


class RoleChecker:
    """Class-based dep so implementation_plan.md examples work:

    Depends(RoleChecker(["ADMIN"]))
    """

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user=Depends(require_auth)) -> dict:
        role = user.get("role")
        # ADMIN bypass
        if role == "ADMIN" and "ADMIN" not in self.allowed_roles:
            return user
        if role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user

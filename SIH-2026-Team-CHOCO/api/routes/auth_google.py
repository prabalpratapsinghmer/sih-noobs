from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.postgres import get_db, get_or_create_user
from api.auth.jwt import create_access_token
from api.schemas.auth import GoogleAuthRequest
from api.config import get_settings
import httpx

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

async def verify_google_id_token(id_token: str) -> dict:
    """Verify Google ID token using Google's tokeninfo endpoint."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
            timeout=5.0,
        )
        if resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google ID token",
            )
        data = resp.json()
        settings = get_settings()
        if data.get("aud") != settings.google_oauth_client_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google ID token audience mismatch",
            )
        return data

@router.post("/google", summary="Google OAuth login")
async def google_login(body: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    """Accept a Google ID token, verify it, create/fetch a user, and return a JWT.

    New users are created with role CITIZEN by default.
    """
    id_token = body.credential or body.google_id
    if not id_token:
        raise HTTPException(status_code=400, detail="Missing credential")
        
    payload = await verify_google_id_token(id_token)
    email = payload.get("email") or body.email
    if not email:
        raise HTTPException(status_code=400, detail="Unable to determine email from Google account")
    name = payload.get("name") or body.name or email.split("@")[0]
    user = await get_or_create_user(db, email=email, name=name)
    access_token = create_access_token(user_id=user.user_id, role=user.role.value)
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "station": user.station,
            "badge_number": user.badge_number,
            "avatar_url": body.avatar_url,
        }
    }

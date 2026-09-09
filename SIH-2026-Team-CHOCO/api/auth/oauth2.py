"""OAuth2 flows — password grant via form data (Swagger Authorize / Postman compatible).

The JSON /login endpoint stays the app-standard; this module implements the
standard `application/x-www-form-urlencoded` password flow that Swagger's
"Authorize" button and OAuth2 clients call.
"""

from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.jwt import create_access_token, create_refresh_token
from api.auth.password import verify_password
from api.database.postgres import get_db
from api.models.user import User


async def oauth2_password_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """OAuth2 Password Grant: form-encoded username/password → token response."""
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")

    user.last_login = datetime.utcnow()
    await db.commit()

    return {
        "access_token": create_access_token(user.user_id, user.role.value),
        "refresh_token": create_refresh_token(user.user_id),
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
        },
    }

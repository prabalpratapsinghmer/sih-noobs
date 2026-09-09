"""Authentication routes: login, logout, refresh, password reset."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    is_token_blacklisted,
)
from api.auth.oauth2 import oauth2_password_login
from api.auth.otp import generate_otp, store_otp, verify_otp
from api.auth.password import hash_password, verify_password
from api.auth.rbac import require_auth
from api.config import get_settings
from api.database.postgres import get_db
import uuid
from api.models.user import User, UserRole
from api.schemas.auth import (
    GoogleAuthRequest,
    LoginRequest,
    RefreshRequest,
    ResetPasswordConfirm,
    ResetPasswordRequest,
    SignUpRequest,
    TokenResponse,
)
from api.services.supabase_service import get_supabase_service

router = APIRouter()
settings = get_settings()


@router.post("/login", response_model=TokenResponse, tags=["auth"])
async def login(body: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """Username or Email + password → JWT tokens (JSON body)."""
    try:
        result = await db.execute(
            select(User).where((User.username == body.username) | (User.email == body.username))
        )
        user = result.scalar_one_or_none()

        if user is None or not verify_password(body.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username/email or password")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account disabled")

        user.last_login = datetime.utcnow()
        await db.commit()

        role_val = user.role.value if hasattr(user.role, 'value') else str(user.role)

        return TokenResponse(
            access_token=create_access_token(user.user_id, role_val),
            refresh_token=create_refresh_token(user.user_id),
            user={
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "role": role_val,
                "station": user.station,
                "badge_number": user.badge_number,
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Login internal error: {exc}")



@router.post("/signup", response_model=TokenResponse, tags=["auth"])
async def signup(body: SignUpRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """Sign up a new account (stores in PostgreSQL & Supabase, returns JWT)."""
    # 1. Check if username or email already exists
    existing = (
        await db.execute(
            select(User).where((User.username == body.username) | (User.email == body.email))
        )
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=409, detail="Username or email is already registered")

    # 2. Map role
    role_str = body.role.upper()
    if role_str == "ADMIN":
        user_role = UserRole.ADMIN
    elif role_str == "INSPECTOR":
        user_role = UserRole.INSPECTOR
    elif role_str == "CITIZEN":
        user_role = UserRole.CITIZEN
    else:
        user_role = UserRole.CONSTABLE

    new_user_id = str(uuid.uuid4())
    hashed_pw = hash_password(body.password)

    new_user = User(
        user_id=new_user_id,
        username=body.username.strip(),
        email=body.email.strip().lower(),
        password_hash=hashed_pw,
        role=user_role,
        station=body.station or "Cyber Crime Intake Station",
        badge_number=body.badge_number or f"CC-{body.username[:4].upper()}",
        phone=body.phone,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        last_login=datetime.utcnow(),
        is_active=True,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # 3. Store user in Supabase backend (public.users & GoTrue)
    try:
        supabase = get_supabase_service()
        await supabase.insert_user(
            user_id=new_user.user_id,
            username=new_user.username,
            email=new_user.email,
            password_hash=hashed_pw,
            role=user_role.value,
            station=new_user.station,
            badge_number=new_user.badge_number,
            phone=new_user.phone,
        )
        await supabase.sync_user_auth(
            email=new_user.email,
            password=body.password,
            user_metadata={"username": new_user.username, "role": user_role.value},
        )
    except Exception as e:
        import structlog
        structlog.get_logger(__name__).warning(f"Supabase user dual-sync notice: {e}")

    return TokenResponse(
        access_token=create_access_token(new_user.user_id, new_user.role.value),
        refresh_token=create_refresh_token(new_user.user_id),
        user={
            "user_id": new_user.user_id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role.value,
            "station": new_user.station,
            "badge_number": new_user.badge_number,
        },
    )


@router.post("/google", response_model=TokenResponse, tags=["auth"])
async def google_auth(body: GoogleAuthRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """Sign in or register directly with Google OAuth credentials."""
    email = body.email.strip().lower()

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        # Create user for Google account
        base_name = body.name or email.split("@")[0]
        sanitized = "".join(c for c in base_name if c.isalnum() or c == "_").lower()
        candidate_username = sanitized[:40] or "google_user"

        check = (await db.execute(select(User).where(User.username == candidate_username))).scalar_one_or_none()
        if check:
            candidate_username = f"{candidate_username[:34]}_{uuid.uuid4().hex[:5]}"

        new_user_id = str(uuid.uuid4())
        user = User(
            user_id=new_user_id,
            username=candidate_username,
            email=email,
            password_hash=hash_password(uuid.uuid4().hex),
            role=UserRole.CONSTABLE,
            station="Google Sovereign ID Hub",
            badge_number=f"GOOG-{candidate_username[:4].upper()}",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_login=datetime.utcnow(),
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        # Store in Supabase
        try:
            supabase = get_supabase_service()
            await supabase.insert_user(
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                password_hash="oauth_google",
                role=user.role.value,
                station=user.station,
                badge_number=user.badge_number,
            )
        except Exception:
            pass
    else:
        user.last_login = datetime.utcnow()
        await db.commit()

    return TokenResponse(
        access_token=create_access_token(user.user_id, user.role.value),
        refresh_token=create_refresh_token(user.user_id),
        user={
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "station": user.station,
            "badge_number": user.badge_number,
            "avatar_url": body.avatar_url,
        },
    )


@router.get("/me", tags=["auth"])
async def get_me(current_user: dict = Depends(require_auth), db: AsyncSession = Depends(get_db)):
    """Retrieve details for current active JWT session."""
    user_id = current_user.get("sub") or current_user.get("user_id")
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return current_user
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role": user.role.value,
        "station": user.station,
        "badge_number": user.badge_number,
        "phone": user.phone,
    }



@router.post("/token", tags=["auth"])
async def token(data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """OAuth2 Password Grant (application/x-www-form-urlencoded)."""
    return await oauth2_password_login(form_data=data, db=db)


@router.post("/logout")
async def logout(request: Request, user: dict = Depends(require_auth)):
    """Blacklist current access token."""
    jti = user.get("jti")
    if jti:
        try:
            from api.database.redis import get_redis

            r = get_redis()
            await r.setex(f"blacklist:{jti}", settings.jwt_access_token_expire_minutes * 60, "1")
        except Exception:
            pass
    return {"detail": "Logged out"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Refresh token → new access token."""
    try:
        payload = decode_token(body.refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from None

    if payload.get("type") != "refresh" or is_token_blacklisted(payload.get("jti", "")):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    result = await db.execute(select(User).where(User.user_id == payload["sub"]))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found")

    return TokenResponse(
        access_token=create_access_token(user.user_id, user.role.value),
        refresh_token=create_refresh_token(user.user_id),
        user={"user_id": user.user_id, "username": user.username, "role": user.role.value},
    )


@router.post("/reset-password/request")
async def reset_password_request(body: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Send reset OTP to the user's email."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()
    if user is None:
        # Don't reveal whether the email exists
        return {"detail": "If the email exists, an OTP has been sent"}

    otp = generate_otp()
    stored = store_otp(user.user_id, otp)
    if not stored:
        return {"detail": "If the email exists, an OTP has been sent"}  # Redis down, still 200

    import structlog

    structlog.get_logger(__name__).info("[MOCK EMAIL] password reset OTP", user_id=user.user_id, otp=otp)

    return {"detail": "If the email exists, an OTP has been sent"}


@router.post("/reset-password/confirm")
async def reset_password_confirm(body: ResetPasswordConfirm, db: AsyncSession = Depends(get_db)):
    """OTP + new password → reset."""
    # Find user by matching OTP: we store OTP keyed by user_id, so we need the user.
    # Poll users table for a valid OTP (dev: OTP is 6-digit; only one pending per user).
    result = await db.execute(select(User))
    users = result.scalars().all()
    for user in users:
        ok, msg = verify_otp(user.user_id, body.otp)
        if ok:
            user.password_hash = hash_password(body.new_password)
            await db.commit()
            return {"detail": "Password reset successful"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

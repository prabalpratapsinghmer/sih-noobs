"""Pydantic schemas for authentication."""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100, description="Username or Email")
    password: str = Field(min_length=6, max_length=128)


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    full_name: str | None = None
    role: str = Field(default="CONSTABLE", description="ADMIN, INSPECTOR, or CONSTABLE")
    phone: str | None = None
    station: str | None = None
    badge_number: str | None = None


class GoogleAuthRequest(BaseModel):
    credential: str | None = None
    email: EmailStr | None = None
    name: str | None = None
    avatar_url: str | None = None
    google_id: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class RefreshRequest(BaseModel):
    refresh_token: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordConfirm(BaseModel):
    otp: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=6, max_length=128)


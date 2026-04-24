from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ── Request schemas ────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    """Payload for creating a new user account."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        examples=["admin"],
        description="Chỉ gồm chữ cái, số, dấu gạch dưới (3–50 ký tự)",
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        examples=["Secret@123"],
        description="Mật khẩu tối thiểu 6 ký tự",
    )
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        examples=["Nguyen Van A"],
    )


class LoginRequest(BaseModel):
    """Payload for user login."""

    username: str = Field(..., examples=["admin"])
    password: str = Field(..., examples=["Secret@123"])


# ── Response schemas ───────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    """JWT token returned after login / register."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    """Seconds until the token expires."""


class UserResponse(BaseModel):
    """Public user data (never includes password_hash)."""

    id: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

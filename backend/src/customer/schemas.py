from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


# ── Shared helpers ─────────────────────────────────────────────────────────────

PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")


def _validate_phone(v: str) -> str:
    if not PHONE_REGEX.match(v):
        raise ValueError("Invalid phone number format")
    return v


# ── Request schemas ────────────────────────────────────────────────────────────

class CustomerCreateRequest(BaseModel):
    """Payload for creating a new customer."""

    name: str = Field(..., min_length=1, max_length=100, examples=["Nguyen Van A"])
    email: EmailStr = Field(..., examples=["example@email.com"])
    phone: Optional[str] = Field(None, examples=["+84901234567"])
    address: Optional[str] = Field(None, max_length=255)
    note: Optional[str] = Field(None, max_length=500)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return _validate_phone(v)
        return v


class CustomerUpdateRequest(BaseModel):
    """Payload for updating an existing customer (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = Field(None, max_length=255)
    note: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return _validate_phone(v)
        return v


# ── Response schemas ───────────────────────────────────────────────────────────

class CustomerResponse(BaseModel):
    """Customer data returned to the client."""

    id: str
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CustomerListResponse(BaseModel):
    """Paginated list of customers."""

    total: int
    page: int
    page_size: int
    customers: list[CustomerResponse]

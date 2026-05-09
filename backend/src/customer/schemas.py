from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field, field_validator, StringConstraints
from typing import Annotated, Optional
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

    name: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
    ] = Field(..., examples=["Nguyen Van A"])
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True)] = Field(
        ..., examples=["example@email.com"]
    )
    phone: Annotated[Optional[str], StringConstraints(strip_whitespace=True)] = Field(
        None, examples=["+84901234567"]
    )
    address: Annotated[
        Optional[str], StringConstraints(strip_whitespace=True, max_length=255)
    ] = Field(None)
    note: Optional[str] = Field(None, max_length=500)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return _validate_phone(v)
        return v


class CustomerUpdateRequest(BaseModel):
    """Payload for updating an existing customer (all fields optional)."""

    name: Annotated[
        Optional[str],
        StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
    ] = Field(None)
    email: Annotated[
        Optional[EmailStr], StringConstraints(strip_whitespace=True)
    ] = Field(None)
    phone: Annotated[Optional[str], StringConstraints(strip_whitespace=True)] = Field(
        None
    )
    address: Annotated[
        Optional[str], StringConstraints(strip_whitespace=True, max_length=255)
    ] = Field(None)
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

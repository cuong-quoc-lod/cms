from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException, status

from src.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
)
from src.auth.repository import UserRepository
from src.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    # ── Password helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _hash_password(plain: str) -> str:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def _verify_password(plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())

    # ── JWT helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _create_access_token(subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "sub": subject,       # user id
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> str:
        """Decode JWT and return the subject (user_id). Raises HTTPException on failure."""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id: Optional[str] = payload.get("sub")
            if not user_id:
                raise ValueError("Missing subject")
            return user_id
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token khong hop le hoac da het han.",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

    def _build_token_response(self, user_id: str) -> TokenResponse:
        token = self._create_access_token(user_id)
        return TokenResponse(
            access_token=token,
            expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    # ── Business logic ─────────────────────────────────────────────────────────

    def register(self, payload: RegisterRequest) -> TokenResponse:
        """Create a new user and return a JWT."""
        password_hash = self._hash_password(payload.password)
        try:
            user = self.repo.create(
                username=payload.username,
                password_hash=password_hash,
                full_name=payload.full_name,
            )
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{payload.username}' da ton tai.",
            )
        return self._build_token_response(user["id"])

    def login(self, payload: LoginRequest) -> TokenResponse:
        """Verify credentials and return a JWT."""
        user = self.repo.find_by_username(payload.username)
        invalid_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username hoac mat khau khong chinh xac.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if not user:
            raise invalid_exc
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tai khoan da bi khoa.",
            )
        if not self._verify_password(payload.password, user["password_hash"]):
            raise invalid_exc
        return self._build_token_response(user["id"])

    def get_me(self, user_id: str) -> UserResponse:
        """Return public profile of the authenticated user."""
        user = self.repo.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nguoi dung khong ton tai.",
            )
        return UserResponse(
            id=user["id"],
            username=user["username"],
            full_name=user.get("full_name"),
            is_active=user["is_active"],
            created_at=user["created_at"],
        )

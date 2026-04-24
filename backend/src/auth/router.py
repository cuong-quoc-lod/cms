from fastapi import APIRouter, Depends, status

from src.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from src.auth.service import AuthService
from src.auth.repository import UserRepository
from src.database import get_db
from src.dependencies import get_current_user_id


router = APIRouter(prefix="/api/auth", tags=["Auth"])


# ── Dependency injection ───────────────────────────────────────────────────────

def get_auth_service() -> AuthService:
    db = get_db()
    repo = UserRepository(db)
    return AuthService(repo)


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dang ky tai khoan moi",
    description="Tao tai khoan nguoi dung va tra ve JWT access token.",
)
def register(
    payload: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return service.register(payload)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Dang nhap",
    description="Xac thuc username/password va tra ve JWT access token.",
)
def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return service.login(payload)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Thong tin tai khoan hien tai",
    description="Lay thong tin nguoi dung dang dang nhap (yeu cau Bearer token).",
)
def me(
    user_id: str = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return service.get_me(user_id)

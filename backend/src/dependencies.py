from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.service import AuthService
from src.auth.repository import UserRepository
from src.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Dependency to get and verify the JWT token from the request.
    Returns the user ID (subject) from the token."""
    # We create a temporary service instance just to decode the token.
    # In a more complex app, you might inject the service properly.
    return AuthService.decode_token(token)


def get_current_active_user(
    user_id: str = Depends(get_current_user_id),
) -> dict:
    """Dependency to get the current active user from the database."""
    db = get_db()
    repo = UserRepository(db)
    user = repo.find_by_id(user_id)
    if not user:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nguoi dung khong ton tai.",
        )
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tai khoan da bi khoa.",
        )
    return user

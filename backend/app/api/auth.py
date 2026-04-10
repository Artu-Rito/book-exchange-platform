from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, User
from app.core.dependencies import get_current_user
from app.repositories.user import UserRepository
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """Регистрация нового пользователя"""
    user_repo = UserRepository(db)

    existing = user_repo.get_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = user_repo.create_with_role(
        email=user_in.email,
        full_name=user_in.full_name,
        password=user_in.password,
        role_id=2,
    )

    return User(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role_id=user.role_id,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/login")
def login(
    form_data: UserLogin,
    db: Session = Depends(get_db),
):
    """Вход пользователя"""
    auth_service = AuthService(db)

    result = auth_service.login(form_data.email, form_data.password)

    if not result:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token, refresh_token, user_data = result

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user_data,
    }


@router.get("/me")
def get_current_user_info(
    current_user: dict = Depends(get_current_user),
):
    """Получить информацию о текущем пользователе"""
    return current_user

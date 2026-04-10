from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.user import UserService
from app.schemas.user import User, UserUpdate
from app.core.dependencies import get_current_user, get_current_admin_user, require_permission

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_current_user_info(
    current_user: dict = Depends(get_current_user),
):
    """Получить информацию о текущем пользователе"""
    return current_user


@router.get("/me/full", response_model=User)
def get_full_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить полную информацию о пользователе"""
    user_service = UserService(db)
    user = user_service.get_user(current_user["id"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user


@router.put("/me", response_model=User)
def update_current_user(
    user_in: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить информацию о текущем пользователе"""
    user_service = UserService(db)
    
    try:
        user = user_service.update_user(current_user["id"], user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[User])
def get_users(
    page: int = 1,
    page_size: int = 20,
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Получить список пользователей (только админ)"""
    user_service = UserService(db)
    users, _ = user_service.get_users(page, page_size)
    return users


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить информацию о пользователе"""
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user


@router.get("/me/permissions")
def get_user_permissions(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить разрешения текущего пользователя"""
    user_service = UserService(db)
    permissions = user_service.get_user_permissions(current_user["id"])
    return permissions

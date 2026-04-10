# Dependencies module
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.auth import AuthService
from app.services.user import UserService

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    """Получить текущего пользователя из токена"""
    try:
        auth_service = AuthService(db)
        user = auth_service.get_current_user(credentials.credentials)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}",
        )


def get_current_active_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Получить текущего активного пользователя"""
    if not current_user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


def get_current_admin_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Получить текущего пользователя с ролью администратора"""
    try:
        user_service = UserService(db)
        has_admin_role = user_service.has_permission(current_user["id"], "admin", "manage")

        if not has_admin_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return current_user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error checking permissions",
        )


def require_permission(resource: str, action: str):
    """Декоратор для проверки разрешения"""
    def permission_checker(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> dict:
        try:
            user_service = UserService(db)
            has_permission = user_service.has_permission(current_user["id"], resource, action)

            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions to {action} {resource}",
                )

            return current_user
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error checking permissions",
            )

    return permission_checker


def get_optional_user(
    request: Request,
    db: Session = Depends(get_db),
) -> Optional[dict]:
    """Получить пользователя (необязательно)"""
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        auth_service = AuthService(db)
        user = auth_service.get_current_user(token)

        return user
    except Exception:
        return None

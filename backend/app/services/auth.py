from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import settings
from app.models.user import RefreshToken
import uuid


class AuthService:
    """Сервис аутентификации"""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def authenticate(self, email: str, password: str) -> Optional[dict]:
        """Аутентификация пользователя"""
        try:
            user = self.user_repo.get_by_email_with_role(email)
            if not user:
                return None

            if not verify_password(password, user.hashed_password):
                return None

            if not user.is_active:
                return None

            return {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role_id": user.role_id,
            }
        except Exception:
            return None

    def create_user(self, user_in, role_id: int = 2) -> dict:
        """Создать пользователя"""
        user = self.user_repo.create_with_role(
            email=user_in.email,
            full_name=user_in.full_name,
            password=user_in.password,
            role_id=role_id,
        )
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role_id": user.role_id,
        }

    def login(self, email: str, password: str, ip_address: Optional[str] = None) -> Optional[Tuple[str, str, dict]]:
        """Вход пользователя, возврат access и refresh токенов"""
        try:
            user = self.authenticate(email, password)
            if not user:
                return None

            access_token = create_access_token(
                data={"sub": str(user["id"]), "role_id": user["role_id"]}
            )

            refresh_token = create_refresh_token(
                data={"sub": str(user["id"]), "jti": str(uuid.uuid4())}
            )

            expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

            refresh_token_obj = RefreshToken(
                token=refresh_token,
                user_id=user["id"],
                expires_at=expires_at,
                created_ip=ip_address,
            )

            self.db.add(refresh_token_obj)
            self.db.commit()

            user_data = {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "role_id": user["role_id"],
            }

            return access_token, refresh_token, user_data
        except Exception:
            self.db.rollback()
            return None

    def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str, dict]]:
        """Обновление токенов"""
        try:
            payload = decode_token(refresh_token)
            if not payload or payload.get("type") != "refresh":
                return None

            user_id = payload.get("sub")
            if not user_id:
                return None

            token_obj = self.db.query(RefreshToken).filter(
                RefreshToken.token == refresh_token,
                RefreshToken.is_revoked == False,
                RefreshToken.expires_at > datetime.utcnow()
            ).first()

            if not token_obj:
                return None

            user = self.user_repo.get_with_role(int(user_id))
            if not user or not user.is_active:
                return None

            new_access_token = create_access_token(
                data={"sub": str(user.id), "role_id": user.role_id}
            )

            new_refresh_token = create_refresh_token(
                data={"sub": str(user.id), "jti": str(uuid.uuid4())}
            )

            token_obj.is_revoked = True

            expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            new_token_obj = RefreshToken(
                token=new_refresh_token,
                user_id=user.id,
                expires_at=expires_at,
                created_ip=token_obj.created_ip,
            )

            self.db.add(new_token_obj)
            self.db.commit()

            user_data = {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role_id": user.role_id,
            }

            return new_access_token, new_refresh_token, user_data
        except Exception:
            self.db.rollback()
            return None

    def logout(self, refresh_token: str) -> bool:
        """Выход пользователя (отзыв refresh токена)"""
        try:
            token_obj = self.db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

            if token_obj:
                token_obj.is_revoked = True
                self.db.commit()
                return True

            return False
        except Exception:
            self.db.rollback()
            return False

    def get_current_user(self, token: str) -> Optional[dict]:
        """Получение текущего пользователя из токена"""
        try:
            payload = decode_token(token)
            if not payload or payload.get("type") != "access":
                return None

            user_id = payload.get("sub")
            if not user_id:
                return None

            user = self.user_repo.get_with_role(int(user_id))
            if not user or not user.is_active:
                return None

            return {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role_id": user.role_id,
                "role": user.role.name if user.role else None,
            }
        except Exception:
            return None

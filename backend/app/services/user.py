from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.repositories.permission import PermissionRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.permission_repo = PermissionRepository(db)
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Получить пользователя"""
        try:
            user = self.user_repo.get_with_role(user_id)
            if not user:
                return None
            
            return {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role_id": user.role_id,
                "role": user.role.name if user.role else None,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "avatar_url": user.avatar_url,
            }
        except Exception:
            return None
    
    def create_user(self, user_in: UserCreate, role_id: int = 2) -> dict:
        """Создать пользователя"""
        existing = self.user_repo.get_by_email(user_in.email)
        if existing:
            raise ValueError("Email already registered")
        
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
    
    def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[dict]:
        """Обновить пользователя"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        update_data = user_in.model_dump(exclude_unset=True)
        
        if "email" in update_data:
            existing = self.user_repo.get_by_email(update_data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        
        updated_user = self.user_repo.update(user, update_data)
        
        return self.get_user(user_id)
    
    def delete_user(self, user_id: int) -> bool:
        """Удалить пользователя"""
        return self.user_repo.delete(user_id)
    
    def get_users(
        self,
        page: int = 1,
        page_size: int = 20,
        role_id: Optional[int] = None,
    ) -> tuple[List[dict], int]:
        """Получить список пользователей"""
        if role_id:
            users, total = self.user_repo.get_users_by_role(role_id, page, page_size)
        else:
            users, total = self.user_repo.get_multi(page, page_size)
        
        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role_id": user.role_id,
                "role": user.role.name if user.role else None,
                "is_active": user.is_active,
            })
        
        return users_data, total
    
    def has_permission(self, user_id: int, resource: str, action: str) -> bool:
        """Проверить наличие разрешения у пользователя"""
        try:
            user = self.user_repo.get(user_id)
            if not user:
                return False
            
            return self.permission_repo.has_permission(user.role_id, resource, action)
        except Exception:
            return False
    
    def get_user_permissions(self, user_id: int) -> List[dict]:
        """Получить все разрешения пользователя"""
        try:
            user = self.user_repo.get(user_id)
            if not user:
                return []
            
            permissions = self.permission_repo.get_user_permissions(user_id, user.role_id)
            
            return [
                {
                    "id": p.id,
                    "name": p.name,
                    "resource": p.resource,
                    "action": p.action,
                }
                for p in permissions
            ]
        except Exception:
            return []

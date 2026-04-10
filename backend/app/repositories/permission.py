from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import Role, Permission, RolePermission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Role]):
    """Репозиторий для работы с ролями и разрешениями"""
    
    def __init__(self, db: Session):
        super().__init__(Role, db)
    
    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Получить роль по имени"""
        try:
            return self.db.query(Role).filter(Role.name == name).first()
        except Exception:
            return None
    
    def get_role_with_permissions(self, role_id: int) -> Optional[Role]:
        """Получить роль с разрешениями"""
        try:
            return self.db.query(Role).filter(Role.id == role_id).first()
        except Exception:
            return None
    
    def get_user_permissions(self, user_id: int, role_id: int) -> List[Permission]:
        """Получить все разрешения пользователя"""
        try:
            return self.db.query(Permission).join(RolePermission).filter(RolePermission.role_id == role_id).all()
        except Exception:
            return []
    
    def has_permission(self, role_id: int, resource: str, action: str) -> bool:
        """Проверить наличие разрешения у роли"""
        try:
            perm = self.db.query(Permission).join(RolePermission).filter(
                RolePermission.role_id == role_id,
                Permission.resource == resource,
                Permission.action == action
            ).first()
            return perm is not None
        except Exception:
            return False
    
    def assign_permissions_to_role(self, role_id: int, permission_ids: List[int]) -> bool:
        """Назначить разрешения роли"""
        try:
            self.db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
            
            for perm_id in permission_ids:
                role_perm = RolePermission(role_id=role_id, permission_id=perm_id)
                self.db.add(role_perm)
            
            self.db.flush()
            return True
        except Exception:
            return False

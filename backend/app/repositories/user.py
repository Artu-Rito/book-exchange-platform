from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.user import User, Role
from app.repositories.base import BaseRepository
from app.core.security import get_password_hash


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с пользователями"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_email_with_role(self, email: str) -> Optional[User]:
        """Получить пользователя с ролью по email"""
        return self.db.query(User).join(Role, isouter=True).filter(User.email == email).first()
    
    def get_with_role(self, user_id: int) -> Optional[User]:
        """Получить пользователя с ролью по ID"""
        return self.db.query(User).join(Role, isouter=True).filter(User.id == user_id).first()
    
    def create_with_role(
        self,
        email: str,
        full_name: str,
        password: str,
        role_id: int = 2
    ) -> User:
        """Создать пользователя с хешированным паролем"""
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            role_id=role_id,
        )
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user
    
    def update_password(self, user: User, new_password: str) -> User:
        """Обновить пароль пользователя"""
        return self.update(user, {"hashed_password": get_password_hash(new_password)})
    
    def get_users_by_role(self, role_id: int, page: int = 1, page_size: int = 20) -> tuple[List[User], int]:
        """Получить пользователей по роли"""
        return self.get_multi(page, page_size)
    
    def count_by_role(self, role_id: int) -> int:
        """Посчитать количество пользователей по роли"""
        return self.db.query(User).filter(User.role_id == role_id).count()

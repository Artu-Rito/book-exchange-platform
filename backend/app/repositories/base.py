from typing import Generic, List, Optional, Type, TypeVar, Tuple

from sqlalchemy import func

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий с CRUD операциями"""

    def __init__(self, model: Type[ModelType], db):
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        """Получить запись по ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        page: int = 1,
        page_size: int = 20,
        order_by: Optional[str] = None,
        ascending: bool = True,
    ) -> Tuple[List[ModelType], int]:
        """Получить список записей с пагинацией"""
        total = self.db.query(func.count()).select_from(self.model).scalar() or 0

        query = self.db.query(self.model)
        if order_by and hasattr(self.model, order_by):
            column = getattr(self.model, order_by)
            query = query.order_by(column.asc() if ascending else column.desc())
        else:
            query = query.order_by(self.model.id.desc())

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        items = query.all()
        return items, total

    def create(self, obj_in: dict) -> ModelType:
        """Создать запись"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        """Обновить запись"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Удалить запись"""
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.flush()
            return True
        return False

    def exists(self, id: int) -> bool:
        """Проверить существование записи"""
        count = self.db.query(func.count()).select_from(self.model).filter(self.model.id == id).scalar()
        return count > 0

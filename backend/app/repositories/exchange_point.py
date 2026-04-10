from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.exchange_point import ExchangePoint
from app.repositories.base import BaseRepository


class ExchangePointRepository(BaseRepository[ExchangePoint]):
    """Репозиторий для работы с пунктами обмена"""
    
    def __init__(self, db: Session):
        super().__init__(ExchangePoint, db)
    
    def get_all_active(self) -> List[ExchangePoint]:
        """Получить все активные пункты обмена"""
        return self.db.query(ExchangePoint).order_by(ExchangePoint.name).all()

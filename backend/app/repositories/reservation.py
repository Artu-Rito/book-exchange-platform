from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.reservation import Reservation, ReservationStatus
from app.repositories.base import BaseRepository
from datetime import datetime


class ReservationRepository(BaseRepository[Reservation]):
    """Репозиторий для работы с бронированиями"""
    
    def __init__(self, db: Session):
        super().__init__(Reservation, db)
    
    def get_with_relations(self, reservation_id: int) -> Optional[Reservation]:
        """Получить бронирование с отношениями"""
        return self.db.query(Reservation).options(
            joinedload(Reservation.book),
            joinedload(Reservation.user),
            joinedload(Reservation.exchange_point)
        ).filter(Reservation.id == reservation_id).first()
    
    def get_by_user(self, user_id: int, page: int = 1, page_size: int = 20) -> tuple[List[Reservation], int]:
        """Получить бронирования пользователя"""
        query = self.db.query(Reservation).filter(Reservation.user_id == user_id)
        total = query.count()
        
        reservations = query.order_by(Reservation.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return reservations, total
    
    def get_by_book(self, book_id: int) -> List[Reservation]:
        """Получить все бронирования книги"""
        return self.db.query(Reservation).filter(Reservation.book_id == book_id).order_by(Reservation.created_at.desc()).all()
    
    def get_active_by_user(self, user_id: int) -> List[Reservation]:
        """Получить активные бронирования пользователя"""
        return self.db.query(Reservation).filter(
            Reservation.user_id == user_id,
            Reservation.status.in_([ReservationStatus.RESERVED, ReservationStatus.PICKED_UP])
        ).order_by(Reservation.return_date).all()
    
    def get_pickups_for_date(self, date: datetime) -> List[Reservation]:
        """Получить бронирования для получения на дату"""
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return self.db.query(Reservation).filter(
            Reservation.pickup_date >= start_date,
            Reservation.pickup_date <= end_date,
            Reservation.status == ReservationStatus.RESERVED
        ).all()
    
    def get_returns_for_date(self, date: datetime) -> List[Reservation]:
        """Получить бронирования для возврата на дату"""
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return self.db.query(Reservation).filter(
            Reservation.return_date >= start_date,
            Reservation.return_date <= end_date,
            Reservation.status.in_([ReservationStatus.RESERVED, ReservationStatus.PICKED_UP])
        ).all()

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.book import Book
from app.models.reservation import Reservation


class StatisticsService:
    """Сервис для работы со статистикой"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_platform_statistics(self) -> dict:
        """Получить статистику платформы"""
        total_books = self.db.query(func.count(Book.id)).scalar() or 0
        available_books = self.db.query(func.count(Book.id)).filter(Book.status == "AVAILABLE").scalar() or 0
        total_reservations = self.db.query(func.count(Reservation.id)).scalar() or 0
        active_reservations = self.db.query(func.count(Reservation.id)).filter(Reservation.status == "RESERVED").scalar() or 0
        
        return {
            "total_books": total_books,
            "available_books": available_books,
            "total_reservations": total_reservations,
            "active_reservations": active_reservations,
        }
    
    def get_user_statistics(self, user_id: int) -> dict:
        """Получить статистику пользователя"""
        my_books = self.db.query(func.count(Book.id)).filter(Book.owner_id == user_id).scalar() or 0
        my_reservations = self.db.query(func.count(Reservation.id)).filter(Reservation.user_id == user_id).scalar() or 0
        
        return {
            "my_books": my_books,
            "my_reservations": my_reservations,
        }
    
    def get_books_by_genre(self) -> List[dict]:
        """Получить статистику книг по жанрам"""
        results = self.db.query(Book.genre, func.count(Book.id)).group_by(Book.genre).all()
        return [{"genre": row[0], "count": row[1]} for row in results]
    
    def get_books_by_year(self, limit: int = 10) -> List[dict]:
        """Получить статистику книг по годам"""
        results = self.db.query(Book.year, func.count(Book.id)).group_by(Book.year).order_by(func.count(Book.id).desc()).limit(limit).all()
        return [{"year": row[0], "count": row[1]} for row in results]
    
    def get_reservations_by_status(self) -> List[dict]:
        """Получить статистику бронирований по статусам"""
        results = self.db.query(Reservation.status, func.count(Reservation.id)).group_by(Reservation.status).all()
        return [{"status": row[0].value, "count": row[1]} for row in results]

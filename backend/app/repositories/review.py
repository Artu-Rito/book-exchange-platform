from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.review import Review
from app.repositories.base import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    """Репозиторий для работы с отзывами"""
    
    def __init__(self, db: Session):
        super().__init__(Review, db)
    
    def get_by_book(self, book_id: int) -> List[Review]:
        """Получить отзывы книги"""
        return self.db.query(Review).filter(Review.book_id == book_id).order_by(Review.created_at.desc()).all()
    
    def get_by_user(self, user_id: int, page: int = 1, page_size: int = 20) -> tuple[List[Review], int]:
        """Получить отзывы пользователя"""
        query = self.db.query(Review).filter(Review.user_id == user_id)
        total = query.count()
        
        reviews = query.order_by(Review.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return reviews, total
    
    def get_average_rating(self, book_id: int) -> float:
        """Получить средний рейтинг книги"""
        result = self.db.query(func.avg(Review.rating)).filter(Review.book_id == book_id).scalar()
        return round(result, 2) if result else 0.0
    
    def has_reviewed(self, book_id: int, user_id: int) -> bool:
        """Проверил ли пользователь уже эту книгу"""
        count = self.db.query(Review).filter(
            Review.book_id == book_id,
            Review.user_id == user_id
        ).count()
        return count > 0

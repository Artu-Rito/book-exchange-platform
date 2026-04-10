from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.review import ReviewRepository
from app.repositories.book import BookRepository
from app.repositories.reservation import ReservationRepository
from app.schemas.review import ReviewCreate


class ReviewService:
    """Сервис для работы с отзывами"""
    
    def __init__(self, db: Session):
        self.db = db
        self.review_repo = ReviewRepository(db)
        self.book_repo = BookRepository(db)
        self.reservation_repo = ReservationRepository(db)
    
    def get_review(self, review_id: int) -> Optional[dict]:
        """Получить отзыв"""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        
        return self._review_to_dict(review)
    
    def get_book_reviews(self, book_id: int) -> List[dict]:
        """Получить отзывы книги"""
        reviews = self.review_repo.get_by_book(book_id)
        
        return [
            {
                "id": review.id,
                "book_id": review.book_id,
                "user_id": review.user_id,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.isoformat(),
            }
            for review in reviews
        ]
    
    def create_review(
        self,
        review_in: ReviewCreate,
        user_id: int,
    ) -> dict:
        """Создать отзыв"""
        book = self.book_repo.get(review_in.book_id)
        if not book:
            raise ValueError("Book not found")
        
        reservations = self.reservation_repo.get_by_book(review_in.book_id)
        user_reservations = [r for r in reservations if r.user_id == user_id]
        
        if not user_reservations:
            raise PermissionError("Can only review books you have reserved")
        
        has_reviewed = self.review_repo.has_reviewed(review_in.book_id, user_id)
        if has_reviewed:
            raise ValueError("You have already reviewed this book")
        
        review_data = {
            "book_id": review_in.book_id,
            "user_id": user_id,
            "rating": review_in.rating,
            "comment": review_in.comment,
        }
        
        review = self.review_repo.create(review_data)
        self._update_book_rating(review_in.book_id)
        
        return self._review_to_dict(review)
    
    def delete_review(self, review_id: int, user_id: int) -> bool:
        """Удалить отзыв"""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        
        if review.user_id != user_id:
            raise PermissionError("Not authorized to delete this review")
        
        book_id = review.book_id
        result = self.review_repo.delete(review_id)
        
        if result:
            self._update_book_rating(book_id)
        
        return result
    
    def _update_book_rating(self, book_id: int) -> None:
        """Обновить средний рейтинг книги"""
        avg_rating = self.review_repo.get_average_rating(book_id)
        book = self.book_repo.get(book_id)
        
        if book:
            self.book_repo.update(book, {"average_rating": avg_rating})
    
    def _review_to_dict(self, review) -> dict:
        """Конвертация отзыва в словарь"""
        return {
            "id": review.id,
            "book_id": review.book_id,
            "user_id": review.user_id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat(),
        }

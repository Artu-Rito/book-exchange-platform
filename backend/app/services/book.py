from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.book import BookRepository
from app.repositories.review import ReviewRepository
from app.repositories.file import FileRepository
from app.schemas.book import BookCreate, BookUpdate
from datetime import datetime


class BookService:
    """Сервис для работы с книгами"""
    
    def __init__(self, db: Session):
        self.db = db
        self.book_repo = BookRepository(db)
        self.review_repo = ReviewRepository(db)
        self.file_repo = FileRepository(db)
    
    def get_book(self, book_id: int) -> Optional[dict]:
        """Получить книгу"""
        try:
            book = self.book_repo.get_with_relations(book_id)
            if not book:
                return None
            
            return self._book_to_dict(book)
        except Exception:
            return None
    
    def get_books(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        genre: Optional[str] = None,
        status: Optional[str] = None,
        year: Optional[int] = None,
        owner_id: Optional[int] = None,
        order_by: str = "created_at",
        ascending: bool = False,
    ) -> tuple[List[dict], int]:
        """Получить список книг с фильтрацией"""
        try:
            books, total = self.book_repo.get_multi_with_filters(
                page=page,
                page_size=page_size,
                search=search,
                genre=genre,
                status=status,
                year=year,
                owner_id=owner_id,
                order_by=order_by,
                ascending=ascending,
            )
            
            books_data = [self._book_to_dict(book) for book in books]
            return books_data, total
        except Exception:
            return [], 0
    
    def create_book(self, book_in: BookCreate, owner_id: int) -> dict:
        """Создать книгу"""
        try:
            book_data = book_in.model_dump()
            book = self.book_repo.create({**book_data, "owner_id": owner_id})
            
            return self._book_to_dict(book)
        except Exception:
            raise
    
    def update_book(self, book_id: int, book_in: BookUpdate, owner_id: int) -> Optional[dict]:
        """Обновить книгу"""
        try:
            book = self.book_repo.get(book_id)
            if not book:
                return None
            
            if book.owner_id != owner_id:
                raise PermissionError("Not authorized to update this book")
            
            update_data = book_in.model_dump(exclude_unset=True)
            updated_book = self.book_repo.update(book, update_data)
            
            return self._book_to_dict(updated_book)
        except PermissionError:
            raise
        except Exception:
            return None
    
    def delete_book(self, book_id: int, owner_id: int) -> bool:
        """Удалить книгу"""
        try:
            book = self.book_repo.get(book_id)
            if not book:
                return False
            
            if book.owner_id != owner_id:
                raise PermissionError("Not authorized to delete this book")
            
            return self.book_repo.delete(book_id)
        except PermissionError:
            raise
        except Exception:
            return False
    
    def get_user_books(self, user_id: int, page: int = 1, page_size: int = 20) -> tuple[List[dict], int]:
        """Получить книги пользователя"""
        return self.get_books(page, page_size, owner_id=user_id)
    
    def get_available_books(self, page: int = 1, page_size: int = 20) -> tuple[List[dict], int]:
        """Получить доступные книги"""
        return self.get_books(page, page_size, status="AVAILABLE")
    
    def update_book_status(self, book_id: int, status: str) -> Optional[dict]:
        """Обновить статус книги"""
        try:
            book = self.book_repo.get(book_id)
            if not book:
                return None
            
            updated_book = self.book_repo.update(book, {"status": status})
            return self._book_to_dict(updated_book)
        except Exception:
            return None
    
    def get_top_rated_books(self, limit: int = 10) -> List[dict]:
        """Получить топ книг по рейтингу"""
        try:
            books = self.book_repo.get_top_rated(limit)
            return [self._book_to_dict(book) for book in books]
        except Exception:
            return []
    
    def _book_to_dict(self, book) -> dict:
        """Конвертация книги в словарь"""
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "year": book.year,
            "description": book.description,
            "cover_image_url": book.cover_image_url,
            "owner_id": book.owner_id,
            "status": book.status.lower() if book.status else "available",
            "average_rating": book.average_rating,
            "google_books_id": book.google_books_id,
            "created_at": book.created_at.isoformat() if book.created_at else None,
            "updated_at": book.updated_at.isoformat() if book.updated_at else None,
        }

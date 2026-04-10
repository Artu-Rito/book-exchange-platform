from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.book import Book
from app.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    """Репозиторий для работы с книгами"""
    
    def __init__(self, db: Session):
        super().__init__(Book, db)
    
    def get_with_relations(self, book_id: int) -> Optional[Book]:
        """Получить книгу с отношениями"""
        return self.db.query(Book).options(joinedload(Book.owner)).filter(Book.id == book_id).first()
    
    def get_multi_with_filters(
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
    ) -> tuple[List[Book], int]:
        """Получить список книг с фильтрацией и пагинацией"""
        query = self.db.query(Book)
        
        if search:
            query = query.filter(
                or_(
                    Book.title.ilike(f"%{search}%"),
                    Book.author.ilike(f"%{search}%")
                )
            )
        
        if genre:
            query = query.filter(Book.genre == genre)
        
        if status:
            query = query.filter(Book.status == status.value if hasattr(status, 'value') else status)
        
        if year:
            query = query.filter(Book.year == year)
        
        if owner_id is not None:
            query = query.filter(Book.owner_id == owner_id)
        
        total = query.count()
        
        if order_by and hasattr(Book, order_by):
            column = getattr(Book, order_by)
            query = query.order_by(column.asc() if ascending else column.desc())
        else:
            query = query.order_by(Book.created_at.desc())
        
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        items = query.all()
        return items, total
    
    def get_by_owner(self, owner_id: int, page: int = 1, page_size: int = 20) -> tuple[List[Book], int]:
        """Получить книги владельца"""
        return self.get_multi_with_filters(page, page_size, owner_id=owner_id)
    
    def get_available_books(self, page: int = 1, page_size: int = 20) -> tuple[List[Book], int]:
        """Получить доступные книги"""
        return self.get_multi_with_filters(page, page_size, status=BookStatus.AVAILABLE)
    
    def get_top_rated(self, limit: int = 10) -> List[Book]:
        """Получить топ книг по рейтингу"""
        return self.db.query(Book).filter(Book.average_rating > 0).order_by(Book.average_rating.desc()).limit(limit).all()

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.book import BookService
from app.schemas.book import Book, BookCreate, BookUpdate, BookListResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=BookListResponse)
def get_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    genre: Optional[str] = None,
    book_status: Optional[str] = None,
    year: Optional[int] = None,
    owner_id: Optional[int] = None,
    order_by: str = "created_at",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить список книг с фильтрацией и пагинацией"""
    try:
        book_service = BookService(db)
        
        status_enum = book_status.upper() if book_status else None
        
        books, total = book_service.get_books(
            page=page,
            page_size=page_size,
            search=search,
            genre=genre,
            status=status_enum,
            year=year,
            owner_id=owner_id,
            order_by=order_by,
        )
        
        pages = (total + page_size - 1) // page_size
        
        return {
            "items": books,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }
    except Exception:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "pages": 0,
        }


@router.get("/{book_id}", response_model=Book)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить книгу по ID"""
    try:
        book_service = BookService(db)
        book = book_service.get_book(book_id)
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )
        
        return book
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )


@router.post("", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Создать новую книгу"""
    try:
        book_service = BookService(db)
        book = book_service.create_book(book_in, current_user["id"])
        return book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Обновить книгу"""
    try:
        book_service = BookService(db)
        book = book_service.update_book(book_id, book_in, current_user["id"])
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )
        
        return book
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Удалить книгу"""
    try:
        book_service = BookService(db)
        result = book_service.delete_book(book_id, current_user["id"])
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )
        
        return {"message": "Book deleted successfully"}
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )


@router.get("/my/list", response_model=BookListResponse)
def get_my_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить мои книги"""
    try:
        book_service = BookService(db)
        books, total = book_service.get_user_books(current_user["id"], page, page_size)
        
        pages = (total + page_size - 1) // page_size
        
        return {
            "items": books,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }
    except Exception:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "pages": 0,
        }


@router.get("/available/list", response_model=BookListResponse)
def get_available_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить доступные книги"""
    try:
        book_service = BookService(db)
        books, total = book_service.get_available_books(page, page_size)
        
        pages = (total + page_size - 1) // page_size
        
        return {
            "items": books,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }
    except Exception:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "pages": 0,
        }


@router.get("/top/rated", response_model=List[Book])
def get_top_rated_books(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить топ книг по рейтингу"""
    try:
        book_service = BookService(db)
        books = book_service.get_top_rated_books(limit)
        return books
    except Exception:
        return []

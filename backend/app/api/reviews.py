from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.review import ReviewService
from app.schemas.review import Review, ReviewCreate
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/book/{book_id}", response_model=List[Review])
def get_book_reviews(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить отзывы книги"""
    review_service = ReviewService(db)
    reviews = review_service.get_book_reviews(book_id)
    return reviews


@router.post("", response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Создать отзыв"""
    review_service = ReviewService(db)
    
    try:
        review = review_service.create_review(review_in, current_user["id"])
        return review
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/{review_id}", response_model=Review)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить отзыв по ID"""
    review_service = ReviewService(db)
    review = review_service.get_review(review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )
    
    return review


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Удалить отзыв"""
    review_service = ReviewService(db)
    
    try:
        result = review_service.delete_review(review_id, current_user["id"])
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )
        
        return {"message": "Review deleted successfully"}
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

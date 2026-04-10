from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.statistics import StatisticsService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("")
def get_statistics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить статистику"""
    statistics_service = StatisticsService(db)
    
    platform_stats = statistics_service.get_platform_statistics()
    user_stats = statistics_service.get_user_statistics(current_user["id"])
    
    return {
        "platform": platform_stats,
        "user": user_stats,
    }


@router.get("/detailed")
def get_detailed_statistics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить детальную статистику"""
    statistics_service = StatisticsService(db)
    
    books_by_genre = statistics_service.get_books_by_genre()
    books_by_year = statistics_service.get_books_by_year()
    reservations_by_status = statistics_service.get_reservations_by_status()
    
    return {
        "books_by_genre": books_by_genre,
        "books_by_year": books_by_year,
        "reservations_by_status": reservations_by_status,
    }

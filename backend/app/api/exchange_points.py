from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.repositories.exchange_point import ExchangePointRepository
from app.schemas.exchange_point import ExchangePoint
from app.core.dependencies import get_current_user, get_current_admin_user

router = APIRouter(prefix="/exchange-points", tags=["Exchange Points"])


@router.get("", response_model=List[ExchangePoint])
def get_exchange_points(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить все пункты обмена"""
    try:
        repo = ExchangePointRepository(db)
        points = repo.get_all_active()
        return [
            {
                "id": p.id,
                "name": p.name,
                "address": p.address,
                "working_hours": p.working_hours,
                "description": p.description,
                "latitude": p.latitude,
                "longitude": p.longitude,
            }
            for p in points
        ]
    except Exception:
        return []


@router.get("/{point_id}", response_model=ExchangePoint)
def get_exchange_point(
    point_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить пункт обмена по ID"""
    repo = ExchangePointRepository(db)
    point = repo.get(point_id)
    
    if not point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exchange point not found",
        )
    
    return point


@router.post("", response_model=ExchangePoint, status_code=status.HTTP_201_CREATED)
def create_exchange_point(
    point_in: ExchangePoint,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Создать пункт обмена (только админ)"""
    repo = ExchangePointRepository(db)
    
    point_data = point_in.model_dump()
    point = repo.create(point_data)
    
    return point


@router.put("/{point_id}", response_model=ExchangePoint)
def update_exchange_point(
    point_id: int,
    point_in: ExchangePoint,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Обновить пункт обмена (только админ)"""
    repo = ExchangePointRepository(db)
    
    point = repo.get(point_id)
    if not point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exchange point not found",
        )
    
    update_data = point_in.model_dump(exclude_unset=True)
    updated_point = repo.update(point, update_data)
    
    return updated_point


@router.delete("/{point_id}")
def delete_exchange_point(
    point_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Удалить пункт обмена (только админ)"""
    repo = ExchangePointRepository(db)
    
    result = repo.delete(point_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exchange point not found",
        )
    
    return {"message": "Exchange point deleted successfully"}

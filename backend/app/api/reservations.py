from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.reservation import ReservationService
from app.schemas.reservation import Reservation, ReservationCreate
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("", response_model=List[Reservation])
def get_reservations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить мои бронирования"""
    try:
        reservation_service = ReservationService(db)
        reservations, _ = reservation_service.get_user_reservations(
            current_user["id"],
            page,
            page_size,
        )
        return reservations
    except Exception:
        return []


@router.get("/{reservation_id}", response_model=Reservation)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить бронирование по ID"""
    try:
        reservation_service = ReservationService(db)
        reservation = reservation_service.get_reservation(reservation_id)
        
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation not found",
            )
        
        if reservation["user_id"] != current_user["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this reservation",
            )
        
        return reservation
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )


@router.post("", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_in: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Создать новое бронирование"""
    try:
        reservation_service = ReservationService(db)
        reservation = reservation_service.create_reservation(
            reservation_in,
            current_user["id"],
        )
        return reservation
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/{reservation_id}/pickup", response_model=Reservation)
def confirm_pickup(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Подтвердить получение книги"""
    try:
        reservation_service = ReservationService(db)
        reservation = reservation_service.confirm_pickup(
            reservation_id,
            current_user["id"],
        )
        
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation not found",
            )
        
        return reservation
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/{reservation_id}/return", response_model=Reservation)
def confirm_return(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Подтвердить возврат книги"""
    try:
        reservation_service = ReservationService(db)
        reservation = reservation_service.confirm_return(
            reservation_id,
            current_user["id"],
        )
        
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation not found",
            )
        
        return reservation
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/{reservation_id}/status", response_model=Reservation)
def update_reservation_status(
    reservation_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Обновить статус бронирования"""
    try:
        reservation_service = ReservationService(db)
        reservation = reservation_service.update_reservation_status(
            reservation_id,
            status,
            current_user["id"],
        )
        
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation not found",
            )
        
        return reservation
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )


@router.post("/{reservation_id}/cancel", response_model=Reservation)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Отменить бронирование"""
    try:
        reservation_service = ReservationService(db)
        reservation = reservation_service.cancel_reservation(
            reservation_id,
            current_user["id"],
        )
        
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation not found",
            )
        
        return reservation
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )


@router.get("/active/list")
def get_active_reservations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить активные бронирования"""
    try:
        reservation_service = ReservationService(db)
        reservations = reservation_service.get_active_reservations(current_user["id"])
        return reservations
    except Exception:
        return []

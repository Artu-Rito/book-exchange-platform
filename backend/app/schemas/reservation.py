from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ReservationStatus(str, Enum):
    RESERVED = "reserved"
    PICKED_UP = "picked_up"
    RETURNED = "returned"
    CANCELLED = "cancelled"


class ReservationBase(BaseModel):
    book_id: int
    exchange_point_id: int


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    status: Optional[ReservationStatus] = None
    exchange_point_id: Optional[int] = None


class Reservation(ReservationBase):
    id: int
    user_id: int
    reservation_date: datetime
    pickup_date: datetime
    return_date: datetime
    actual_return_date: Optional[datetime] = None
    status: str  # Изменили с Enum на str
    created_at: Optional[datetime] = None  # Сделали optional
    updated_at: Optional[datetime] = None  # Сделали optional

    class Config:
        from_attributes = True


class ReservationListResponse(BaseModel):
    items: List[Reservation]
    total: int
    page: int
    page_size: int
    pages: int

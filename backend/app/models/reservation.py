from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime, timedelta


class ReservationStatus:
    RESERVED = "RESERVED"
    PICKED_UP = "PICKED_UP"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"


class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exchange_point_id = Column(Integer, ForeignKey("exchange_points.id"), nullable=False)
    reservation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    pickup_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    actual_return_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="RESERVED", nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Связи
    book = relationship("Book", back_populates="reservations")
    user = relationship("User", back_populates="reservations")
    exchange_point = relationship("ExchangePoint", back_populates="reservations")

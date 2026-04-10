from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Связи
    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

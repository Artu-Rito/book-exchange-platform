from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    s3_key = Column(String(500), nullable=False, unique=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Связи
    uploader = relationship("User", back_populates="uploaded_files", foreign_keys=[uploader_id])
    book_covers = relationship("Book", back_populates="cover_image", foreign_keys="Book.cover_image_id")

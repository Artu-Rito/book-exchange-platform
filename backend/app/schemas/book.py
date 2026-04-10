from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BookStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    TAKEN = "taken"
    ARCHIVED = "archived"


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    genre: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1000, le=2100)
    description: Optional[str] = None


class BookCreate(BookBase):
    google_books_id: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    genre: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1000, le=2100)
    description: Optional[str] = None
    status: Optional[BookStatus] = None
    cover_image_id: Optional[int] = None


class Book(BookBase):
    id: int
    owner_id: int
    status: BookStatus
    average_rating: float = 0.0
    cover_image_url: Optional[str] = None
    google_books_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    items: List[Book]
    total: int
    page: int
    page_size: int
    pages: int

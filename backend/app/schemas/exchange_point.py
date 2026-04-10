from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ExchangePointBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1, max_length=500)
    working_hours: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    contact_person: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)


class ExchangePointCreate(ExchangePointBase):
    pass


class ExchangePointUpdate(ExchangePointBase):
    pass


class ExchangePoint(ExchangePointBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

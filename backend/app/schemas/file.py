from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FileUpload(BaseModel):
    filename: str
    content_type: str
    file_size: int


class FileResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    content_type: str
    file_size: int
    s3_key: str
    uploader_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

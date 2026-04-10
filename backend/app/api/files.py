from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.services.file import FileService
from app.schemas.file import FileResponse
from app.core.dependencies import get_current_user
import io

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Загрузить файл"""
    file_service = FileService(db)
    
    # Проверяем файл
    is_valid, error_message = file_service.validate_file(file)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )
    
    # Читаем содержимое файла
    content = await file.read()
    file_obj = io.BytesIO(content)
    
    result = await file_service.upload_file(
        file=file_obj,
        filename=file.filename,
        content_type=file.content_type,
        uploader_id=current_user["id"],
    )
    
    return result


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить информацию о файле"""
    file_service = FileService(db)
    file_data = await file_service.get_file(file_id)
    
    if not file_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    
    return file_data


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Удалить файл"""
    file_service = FileService(db)
    
    try:
        result = await file_service.delete_file(file_id, current_user["id"])
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )
        
        return {"message": "File deleted successfully"}
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/download/{file_id}")
async def download_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Получить ссылку для скачивания файла"""
    file_service = FileService(db)
    file_data = await file_service.get_file(file_id)
    
    if not file_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    
    # Проверяем права доступа
    if file_data["uploader_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this file",
        )
    
    # Получаем presigned URL
    download_url = file_service.get_presigned_url(file_data["s3_key"])
    
    if not download_url:
        # Если S3 не настроен, возвращаем локальный путь
        download_url = f"/static/uploads/{file_data['filename']}"
    
    return {"download_url": download_url}

import os
import uuid
from typing import Optional, Tuple, BinaryIO
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.file import FileRepository
from app.core.config import settings


class FileService:
    """Сервис для работы с файлами (S3 хранилище)"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.file_repo = FileRepository(db)
        self.s3_client = None
        self._init_s3_client()
    
    def _init_s3_client(self):
        """Инициализация S3 клиента"""
        if settings.S3_BUCKET_NAME and settings.S3_ACCESS_KEY and settings.S3_SECRET_KEY:
            import boto3
            self.s3_client = boto3.client(
                's3',
                endpoint_url=settings.S3_ENDPOINT_URL,
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY,
                region_name=settings.S3_REGION,
            )
    
    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        content_type: str,
        uploader_id: int,
    ) -> dict:
        """Загрузить файл в хранилище"""
        # Генерируем уникальное имя файла
        file_extension = filename.split('.')[-1] if '.' in filename else ''
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}" if file_extension else uuid.uuid4().hex
        s3_key = f"uploads/{unique_filename}"
        
        # Определяем размер файла
        file.seek(0, 2)  # Перемещаемся в конец
        file_size = file.tell()
        file.seek(0)  # Возвращаемся в начало
        
        if self.s3_client:
            # Загружаем в S3
            self.s3_client.upload_fileobj(
                file,
                settings.S3_BUCKET_NAME,
                s3_key,
                ExtraArgs={'ContentType': content_type}
            )
            file_url = f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{s3_key}" if settings.S3_ENDPOINT_URL else s3_key
        else:
            # Локальное хранилище (для разработки)
            os.makedirs("backend/app/storage/uploads", exist_ok=True)
            local_path = f"backend/app/storage/uploads/{unique_filename}"
            with open(local_path, 'wb') as f:
                f.write(file.read())
            file_url = f"/static/uploads/{unique_filename}"
        
        # Сохраняем в БД
        from app.models.file import File
        
        file_obj = File(
            filename=unique_filename,
            original_filename=filename,
            content_type=content_type,
            file_size=file_size,
            s3_key=s3_key,
            uploader_id=uploader_id,
        )
        
        self.db.add(file_obj)
        await self.db.flush()
        await self.db.refresh(file_obj)
        
        return {
            "id": file_obj.id,
            "filename": file_obj.filename,
            "original_filename": file_obj.original_filename,
            "content_type": file_obj.content_type,
            "file_size": file_obj.file_size,
            "s3_key": file_obj.s3_key,
            "url": file_url,
        }
    
    async def get_file(self, file_id: int) -> Optional[dict]:
        """Получить информацию о файле"""
        file_obj = await self.file_repo.get(file_id)
        if not file_obj:
            return None
        
        return {
            "id": file_obj.id,
            "filename": file_obj.filename,
            "original_filename": file_obj.original_filename,
            "content_type": file_obj.content_type,
            "file_size": file_obj.file_size,
            "s3_key": file_obj.s3_key,
            "uploader_id": file_obj.uploader_id,
        }
    
    async def delete_file(self, file_id: int, user_id: int) -> bool:
        """Удалить файл"""
        file_obj = await self.file_repo.get(file_id)
        if not file_obj:
            return False
        
        # Проверяем права
        if file_obj.uploader_id != user_id:
            raise PermissionError("Not authorized to delete this file")
        
        # Удаляем из хранилища
        if self.s3_client:
            try:
                self.s3_client.delete_object(
                    Bucket=settings.S3_BUCKET_NAME,
                    Key=file_obj.s3_key
                )
            except Exception:
                pass
        else:
            # Локальное хранилище
            local_path = f"backend/app/storage/uploads/{file_obj.filename}"
            if os.path.exists(local_path):
                os.remove(local_path)
        
        # Удаляем из БД
        return await self.file_repo.delete(file_id)
    
    def get_presigned_url(self, s3_key: str, expiration: int = 3600) -> Optional[str]:
        """Получить временную ссылку для скачивания"""
        if not self.s3_client:
            return None
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.S3_BUCKET_NAME,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url
        except Exception:
            return None
    
    def validate_file(self, file, max_size: int = 5 * 1024 * 1024, allowed_types: Optional[list] = None) -> Tuple[bool, str]:
        """Проверить файл на валидность"""
        if allowed_types is None:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        
        # Проверяем тип файла
        if file.content_type not in allowed_types:
            return False, f"File type {file.content_type} is not allowed"
        
        # Проверяем размер
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > max_size:
            return False, f"File size exceeds maximum allowed size of {max_size} bytes"
        
        return True, ""

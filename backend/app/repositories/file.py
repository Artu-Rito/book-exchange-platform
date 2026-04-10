from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.file import File
from app.repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):
    """Репозиторий для работы с файлами"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(File, db)
    
    async def get_by_s3_key(self, s3_key: str) -> Optional[File]:
        """Получить файл по S3 ключу"""
        result = await self.db.execute(select(File).where(File.s3_key == s3_key))
        return result.scalar_one_or_none()
    
    async def get_by_uploader(self, uploader_id: int, page: int = 1, page_size: int = 20) -> tuple[List[File], int]:
        """Получить файлы пользователя"""
        return await self.get_multi(page, page_size)

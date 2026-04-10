from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import httpx
from app.core.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/external", tags=["External APIs"])


@router.get("/google-books/search")
async def search_google_books(
    query: str,
    max_results: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Поиск книг через Google Books API
    
    Интеграция со сторонним API для получения дополнительной информации о книгах.
    """
    google_books_api_url = "https://www.googleapis.com/books/v1/volumes"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                google_books_api_url,
                params={
                    "q": query,
                    "maxResults": min(max_results, 40),  # Максимум 40 от Google
                    "langRestrict": "ru|en",
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=503,
                    detail="Google Books API unavailable"
                )
            
            data = response.json()
            books = []
            
            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})
                books.append({
                    "google_books_id": item.get("id"),
                    "title": volume_info.get("title", "Unknown"),
                    "author": volume_info.get("authors", ["Unknown"])[0],
                    "genre": volume_info.get("categories", ["Other"])[0] if volume_info.get("categories") else "Other",
                    "year": int(volume_info.get("publishedDate", "0000")[:4]) if volume_info.get("publishedDate") else 0,
                    "description": volume_info.get("description", ""),
                    "cover_image_url": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                    "average_rating": volume_info.get("averageRating", 0),
                    "ratings_count": volume_info.get("ratingsCount", 0),
                })
            
            return {"items": books, "total": data.get("totalItems", 0)}
    
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Google Books API timeout"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error connecting to Google Books API: {str(e)}"
        )


@router.get("/google-books/{google_id}")
async def get_book_details(
    google_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Получение детальной информации о книге из Google Books API
    """
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes/{google_id}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(google_books_api_url)
            
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail="Book not found in Google Books"
                )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=503,
                    detail="Google Books API unavailable"
                )
            
            data = response.json()
            volume_info = data.get("volumeInfo", {})
            
            return {
                "google_books_id": data.get("id"),
                "title": volume_info.get("title", "Unknown"),
                "subtitle": volume_info.get("subtitle", ""),
                "authors": volume_info.get("authors", []),
                "publisher": volume_info.get("publisher", ""),
                "published_date": volume_info.get("publishedDate", ""),
                "description": volume_info.get("description", ""),
                "page_count": volume_info.get("pageCount", 0),
                "categories": volume_info.get("categories", []),
                "average_rating": volume_info.get("averageRating", 0),
                "ratings_count": volume_info.get("ratingsCount", 0),
                "cover_image_url": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                "preview_link": volume_info.get("previewLink", ""),
                "info_link": volume_info.get("infoLink", ""),
            }
    
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Google Books API timeout"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error connecting to Google Books API: {str(e)}"
        )

"""Тесты книг"""
import pytest
from httpx import AsyncClient


class TestBooks:
    """Тесты книг"""
    
    async def test_create_book(self, client: AsyncClient, auth_token: str):
        """Тест создания книги"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2024,
        }
        
        response = await client.post("/api/v1/books", json=book_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["author"] == book_data["author"]
        assert data["status"] == "available"
        assert "id" in data
    
    async def test_get_books(self, client: AsyncClient, auth_token: str):
        """Тест получения списка книг"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = await client.get("/api/v1/books", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
    
    async def test_get_book_by_id(self, client: AsyncClient, auth_token: str):
        """Тест получения книги по ID"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Сначала создаем книгу
        book_data = {
            "title": "Test Book 2",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2024,
        }
        create_response = await client.post("/api/v1/books", json=book_data, headers=headers)
        book_id = create_response.json()["id"]
        
        # Получаем книгу
        response = await client.get(f"/api/v1/books/{book_id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == book_data["title"]
    
    async def test_update_book(self, client: AsyncClient, auth_token: str):
        """Тест обновления книги"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Создаем книгу
        book_data = {
            "title": "Original Title",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2024,
        }
        create_response = await client.post("/api/v1/books", json=book_data, headers=headers)
        book_id = create_response.json()["id"]
        
        # Обновляем книгу
        update_data = {"title": "Updated Title"}
        response = await client.put(f"/api/v1/books/{book_id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
    
    async def test_delete_book(self, client: AsyncClient, auth_token: str):
        """Тест удаления книги"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Создаем книгу
        book_data = {
            "title": "To Delete",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2024,
        }
        create_response = await client.post("/api/v1/books", json=book_data, headers=headers)
        book_id = create_response.json()["id"]
        
        # Удаляем книгу
        response = await client.delete(f"/api/v1/books/{book_id}", headers=headers)
        
        assert response.status_code == 200
        
        # Проверяем, что книга удалена
        get_response = await client.get(f"/api/v1/books/{book_id}", headers=headers)
        assert get_response.status_code == 404
    
    async def test_filter_books_by_genre(self, client: AsyncClient, auth_token: str):
        """Тест фильтрации книг по жанру"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Создаем книги разных жанров
        for genre in ["Fiction", "SciFi", "Fantasy"]:
            book_data = {
                "title": f"Book in {genre}",
                "author": "Test Author",
                "genre": genre,
                "year": 2024,
            }
            await client.post("/api/v1/books", json=book_data, headers=headers)
        
        # Фильтруем по жанру
        response = await client.get("/api/v1/books?genre=Fiction", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        for book in data["items"]:
            assert book["genre"] == "Fiction"
    
    async def test_search_books(self, client: AsyncClient, auth_token: str):
        """Тест поиска книг"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Создаем книгу
        book_data = {
            "title": "The Great Test",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2024,
        }
        await client.post("/api/v1/books", json=book_data, headers=headers)
        
        # Ищем по названию
        response = await client.get("/api/v1/books?search=Great", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0
        assert "Great" in data["items"][0]["title"]

"""Тесты бронирований"""
import pytest
from httpx import AsyncClient


class TestReservations:
    """Тесты бронирований"""
    
    async def test_create_reservation(self, client: AsyncClient, auth_token: str):
        """Тест создания бронирования"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Сначала создаем книгу
        book_data = {
            "title": "Book for Reservation",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2024,
        }
        book_response = await client.post("/api/v1/books", json=book_data, headers=headers)
        book_id = book_response.json()["id"]
        
        # Получаем пункт обмена
        points_response = await client.get("/api/v1/exchange-points", headers=headers)
        point_id = points_response.json()[0]["id"]
        
        # Создаем бронирование
        reservation_data = {
            "book_id": book_id,
            "exchange_point_id": point_id,
        }
        
        response = await client.post("/api/v1/reservations", json=reservation_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["book_id"] == book_id
        assert data["status"] == "reserved"
    
    async def test_get_user_reservations(self, client: AsyncClient, auth_token: str):
        """Тест получения бронирований пользователя"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = await client.get("/api/v1/reservations", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_cannot_reserve_own_book(self, client: AsyncClient, auth_token: str):
        """Тест: нельзя забронировать свою книгу"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Создаем книгу
        book_data = {
            "title": "My Book",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2024,
        }
        book_response = await client.post("/api/v1/books", json=book_data, headers=headers)
        book_id = book_response.json()["id"]
        
        # Получаем пункт обмена
        points_response = await client.get("/api/v1/exchange-points", headers=headers)
        point_id = points_response.json()[0]["id"]
        
        # Пытаемся забронировать свою книгу
        reservation_data = {
            "book_id": book_id,
            "exchange_point_id": point_id,
        }
        
        response = await client.post("/api/v1/reservations", json=reservation_data, headers=headers)
        
        assert response.status_code == 400
        assert "Cannot reserve your own book" in response.json()["detail"]
    
    async def test_cancel_reservation(self, client: AsyncClient, auth_token: str):
        """Тест отмены бронирования"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Создаем книгу
        book_data = {
            "title": "Book to Reserve",
            "author": "Test Author",
            "genre": "Fiction",
            "year": 2024,
        }
        book_response = await client.post("/api/v1/books", json=book_data, headers=headers)
        book_id = book_response.json()["id"]
        
        # Получаем пункт обмена
        points_response = await client.get("/api/v1/exchange-points", headers=headers)
        point_id = points_response.json()[0]["id"]
        
        # Создаем бронирование
        reservation_data = {
            "book_id": book_id,
            "exchange_point_id": point_id,
        }
        reserve_response = await client.post("/api/v1/reservations", json=reservation_data, headers=headers)
        reservation_id = reserve_response.json()["id"]
        
        # Отменяем бронирование
        response = await client.post(f"/api/v1/reservations/{reservation_id}/cancel", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"

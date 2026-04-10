"""Тесты аутентификации"""
import pytest
from httpx import AsyncClient


class TestAuth:
    """Тесты аутентификации"""
    
    async def test_register_user(self, client: AsyncClient):
        """Тест регистрации пользователя"""
        user_data = {
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User",
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert "hashed_password" not in data
    
    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        """Тест регистрации с дублирующимся email"""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Another User",
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    async def test_login_success(self, client: AsyncClient, test_user):
        """Тест успешного входа"""
        login_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
    
    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Тест входа с неправильным паролем"""
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 400
        assert "Incorrect email or password" in response.json()["detail"]
    
    async def test_get_current_user(self, client: AsyncClient, auth_token: str):
        """Тест получения текущего пользователя"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = await client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
    
    async def test_unauthorized_access(self, client: AsyncClient):
        """Тест доступа без авторизации"""
        response = await client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
    
    async def test_refresh_token(self, client: AsyncClient, auth_token: str):
        """Тест обновления токена"""
        # Сначала получим refresh токен через логин
        login_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

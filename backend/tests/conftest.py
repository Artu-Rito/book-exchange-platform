import pytest
import tempfile
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db, Base, engine


@pytest.fixture(scope="function")
def test_db():
    """Создание тестовой БД"""
    Base.metadata.create_all(bind=engine)
    yield
    # Очистка после тестов
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """Сессия для тестов"""
    from sqlalchemy.orm import Session
    session = Session(engine)
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def client(db_session):
    """Тестовый HTTP клиент"""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    """Создание тестового пользователя"""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User",
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    return response.json()


@pytest.fixture
def auth_token(client, test_user):
    """Получение токена аутентификации"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    return response.json()["access_token"]

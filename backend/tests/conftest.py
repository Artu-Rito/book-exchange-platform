import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.core.database import get_db, async_session_factory
from app.core.database import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Тестовая БД
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_book_exchange.db"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Создание тестового движка БД"""
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine):
    """Создание тестовой сессии БД"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(test_session):
    """Тестовый HTTP клиент"""
    async def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(client):
    """Создание тестового пользователя"""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User",
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    return response.json()


@pytest_asyncio.fixture
async def auth_token(client, test_user):
    """Получение токена аутентификации"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    return response.json()["access_token"]

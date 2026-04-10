from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from app.core.config import settings

Base = declarative_base()


def _to_sync_url(database_url: str) -> str:
    # Приводим sqlite url к синхронному формату
    if database_url.startswith("sqlite+aiosqlite:///"):
        return database_url.replace("sqlite+aiosqlite:///", "sqlite:///", 1)
    return database_url


engine = create_engine(
    _to_sync_url(settings.DATABASE_URL),
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator:
    """Dependency: выдаёт Session для endpoints/services."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Создаёт таблицы в текущей БД."""
    Base.metadata.create_all(bind=engine)


def close_db() -> None:
    """Закрытие соединения с БД."""
    engine.dispose()

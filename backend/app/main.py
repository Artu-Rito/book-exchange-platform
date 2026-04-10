from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import (
    auth_router,
    users_router,
    books_router,
    reservations_router,
    exchange_points_router,
    reviews_router,
    files_router,
    statistics_router,
    permissions_router,
    external_router,
    seo_router,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Инициализация БД
from app.core.database import init_db
init_db()

# Инициализация начальных данных
from app.services.seed import init_sample_data
init_sample_data()

# Подключаем роутеры
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(books_router, prefix=settings.API_V1_STR)
app.include_router(reservations_router, prefix=settings.API_V1_STR)
app.include_router(exchange_points_router, prefix=settings.API_V1_STR)
app.include_router(reviews_router, prefix=settings.API_V1_STR)
app.include_router(files_router, prefix=settings.API_V1_STR)
app.include_router(statistics_router, prefix=settings.API_V1_STR)
app.include_router(permissions_router, prefix=settings.API_V1_STR)
app.include_router(external_router, prefix=settings.API_V1_STR)
app.include_router(seo_router)

# CORS middleware - ДОБАВЛЯЕМ ЗАГОЛОВКИ ДАЖЕ ПРИ ОШИБКАХ
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        # Создаём ответ для ошибки
        from starlette.responses import JSONResponse
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Обработка preflight OPTIONS запросов
@app.options("/{path:path}")
async def options_handler(path: str):
    return Response(
        content="",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
            "Access-Control-Allow-Credentials": "true",
        }
    )

@app.get("/")
def root():
    """Корневой endpoint"""
    return {
        "message": "Book Exchange Platform API",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Проверка здоровья"""
    return {"status": "healthy"}

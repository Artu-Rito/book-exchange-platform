# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание директории для БД и загрузок
RUN mkdir -p /app/data /app/uploads

# Переменные окружения
ENV DATABASE_URL=sqlite+aiosqlite:///./data/book_exchange.db
ENV SECRET_KEY=docker-secret-key-change-in-production
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV REFRESH_TOKEN_EXPIRE_DAYS=7

# Экспорт порта
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

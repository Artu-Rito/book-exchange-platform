# 📚 Book Exchange Platform

Полнофункциональная платформа для обмена книгами с системой бронирования, реализованная в рамках курса "Fullstack".

## 🎯 Выполненные лабораторные работы

| № | Работа | Статус | Файлы |
|---|--------|--------|-------|
| 1 | RBAC - роли и права доступа | ✅ | `backend/app/models/user.py`, `backend/app/api/deps.py` |
| 2 | Access + Refresh токены, слоистая архитектура | ✅ | `backend/app/services/auth.py`, `backend/app/api/v1/auth.py` |
| 3 | Пагинация, фильтрация, S3 хранилище | ✅ | `backend/app/api/v1/books.py`, `backend/app/storage/s3.py` |
| 4 | SEO оптимизация, robots.txt, sitemap.xml | ✅ | `frontend/public/robots.txt`, `backend/app/api/v1/seo.py` |
| 5 | Тестирование (pytest) | ✅ | `backend/tests/` |
| 6 | Docker, docker-compose, CI/CD | ✅ | `docker-compose.yml`, `.github/workflows/ci.yml` |

## 🛠️ Технологический стек

### Backend
- **Python 3.11** + **FastAPI** - веб-фреймворк
- **SQLAlchemy 2.0** + **aiosqlite** - асинхронная ORM
- **JWT** (python-jose) - аутентификация
- **bcrypt** - хеширование паролей
- **boto3** - S3 хранилище

### Frontend
- **TypeScript 5** - типизация
- **React 18** - UI библиотека
- **React Router 6** - роутинг
- **Axios** - HTTP клиент

### DevOps
- **Docker** + **docker-compose** - контейнеризация
- **Nginx** - reverse proxy
- **GitHub Actions** - CI/CD
- **pytest** - тестирование backend

## 📁 Структура проекта

```
book-exchange-platform/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints (роутеры)
│   │   ├── core/          # Конфигурация, БД, зависимости
│   │   ├── models/        # SQLAlchemy модели
│   │   ├── schemas/       # Pydantic схемы
│   │   ├── services/      # Бизнес-логика
│   │   ├── repositories/  # Доступ к данным
│   │   ├── storage/       # Файловое хранилище
│   │   └── main.py        # Точка входа
│   ├── tests/             # Тесты
│   ├── requirements.txt
│   ├── init_db.py         # Скрипт инициализации БД
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/           # API клиент
│   │   ├── components/    # React компоненты
│   │   ├── pages/         # Страницы
│   │   ├── types/         # TypeScript типы
│   │   └── i18n.ts        # Локализация
│   ├── public/
│   │   └── robots.txt     # SEO
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── .github/workflows/ci.yml
├── LABS_REPORT.txt        # Подробный отчёт по лабораторным
└── README.md
```

## 🚀 Быстрый старт

### Через Docker (рекомендуется)

```bash
# Сборка и запуск
docker-compose up --build

# Приложение доступно по:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Локальная разработка

#### Backend

```bash
cd backend

# Установка зависимостей
pip install -r requirements.txt

# Инициализация БД
python init_db.py

# Запуск сервера
python run.py

# API доступно на http://localhost:8000
```

#### Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev-сервера
npm run dev

# Приложение доступно на http://localhost:3000
```

## 🔐 Роли и права доступа

| Роль | Описание | Права |
|------|----------|-------|
| **admin** | Администратор | Полный доступ ко всем ресурсам |
| **user** | Пользователь | CRUD своих книг, бронирование, отзывы |
| **guest** | Гость | Только чтение (просмотр книг) |

### Матрица прав доступа

| Ресурс | Действие | Guest | User | Admin |
|--------|----------|-------|------|-------|
| books | read | ✅ | ✅ | ✅ |
| books | create | ❌ | ✅ | ✅ |
| books | update | ❌ | ✅ (свои) | ✅ |
| books | delete | ❌ | ✅ (свои) | ✅ |
| reservations | read | ❌ | ✅ | ✅ |
| reservations | create | ❌ | ✅ | ✅ |
| reviews | read | ✅ | ✅ | ✅ |
| reviews | create | ❌ | ✅ | ✅ |
| users | manage | ❌ | ❌ | ✅ |

## 📡 API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `POST /api/v1/auth/refresh` - Обновление токена
- `POST /api/v1/auth/logout` - Выход
- `GET /api/v1/auth/me` - Текущий пользователь

### Книги
- `GET /api/v1/books` - Список книг (с фильтрацией и пагинацией)
- `POST /api/v1/books` - Создать книгу
- `GET /api/v1/books/{id}` - Получить книгу
- `PUT /api/v1/books/{id}` - Обновить книгу
- `DELETE /api/v1/books/{id}` - Удалить книгу

### Бронирования
- `GET /api/v1/reservations` - Мои бронирования
- `POST /api/v1/reservations` - Создать бронирование
- `POST /api/v1/reservations/{id}/cancel` - Отменить бронирование

### Отзывы
- `GET /api/v1/reviews/book/{bookId}` - Отзывы книги
- `POST /api/v1/reviews` - Создать отзыв
- `DELETE /api/v1/reviews/{id}` - Удалить отзыв

### Статистика
- `GET /api/v1/statistics` - Общая статистика
- `GET /api/v1/statistics/detailed` - Детальная статистика

## 🧪 Тестирование

```bash
cd backend

# Запуск всех тестов
pytest

# Запуск с покрытием
pytest --cov=app --cov-report=html
```

## 📦 Переменные окружения

Создайте файл `backend/.env`:

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./book_exchange.db

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# S3 (опционально)
S3_BUCKET_NAME=your-bucket
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key

# Email notifications (опционально)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
```

## 🌐 Локализация

Приложение поддерживает два языка:
- 🇷🇺 Русский (по умолчанию)
- 🇬🇧 English

Переключение языка доступно в навигационной панели.

## 📱 Основные возможности

- ✅ Регистрация и аутентификация (JWT access + refresh токены)
- ✅ Управление книгами (CRUD)
- ✅ Поиск и фильтрация книг (по названию, автору, жанру, году)
- ✅ Бронирование книг с выбором пункта обмена
- ✅ Система отзывов и рейтингов
- ✅ Календарь бронирований
- ✅ Статистика платформы и пользователя
- ✅ Ролевая модель доступа (RBAC)
- ✅ Загрузка файлов (S3)
- ✅ Адаптивный дизайн
- ✅ SEO оптимизация
- ✅ Email уведомления о бронированиях

## 🔧 Архитектурные паттерны

- **Repository Pattern** - абстракция доступа к данным
- **Service Layer** - бизнес-логика
- **Dependency Injection** - внедрение зависимостей
- **DTO (Data Transfer Object)** - передача данных между слоями

## 📄 Отчёт по лабораторным

Подробный отчёт о выполнении всех лабораторных работ с ссылками на файлы и строки:
👉 [LABS_REPORT.txt](LABS_REPORT.txt)

## 📄 Лицензия

Учебный проект для курса "Fullstack".

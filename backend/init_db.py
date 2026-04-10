"""
Скрипт инициализации базы данных
Создает таблицы и добавляет начальные данные (роли, пункты обмена)
"""

from app.core.database import Base, engine, SessionLocal
from app.models.user import Role, Permission, RolePermission, User
from app.models.exchange_point import ExchangePoint
from app.models.book import Book
from app.models.reservation import Reservation
from app.models.review import Review
from app.models.file import File
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_database():
    """Инициализация БД: создание таблиц и начальных данных"""
    
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")
    
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже роли
        existing_roles = db.query(Role).all()
        if existing_roles:
            print("⚠️ Роли уже существуют, пропускаем инициализацию")
            return
        
        print("Добавление ролей...")
        roles = [
            Role(id=1, name="admin", description="Администратор платформы"),
            Role(id=2, name="user", description="Обычный пользователь"),
            Role(id=3, name="guest", description="Гость (только чтение)"),
        ]
        db.add_all(roles)
        db.commit()
        
        print("Добавление разрешений...")
        permissions = [
            Permission(id=1, name="books:read", description="Чтение книг", resource="books", action="read"),
            Permission(id=2, name="books:create", description="Создание книг", resource="books", action="create"),
            Permission(id=3, name="books:update", description="Обновление книг", resource="books", action="update"),
            Permission(id=4, name="books:delete", description="Удаление книг", resource="books", action="delete"),
            Permission(id=5, name="books:manage", description="Управление всеми книгами", resource="books", action="manage"),
            
            Permission(id=6, name="reservations:read", description="Чтение бронирований", resource="reservations", action="read"),
            Permission(id=7, name="reservations:create", description="Создание бронирований", resource="reservations", action="create"),
            Permission(id=8, name="reservations:update", description="Обновление бронирований", resource="reservations", action="update"),
            Permission(id=9, name="reservations:manage", description="Управление всеми бронированиями", resource="reservations", action="manage"),
            
            Permission(id=10, name="reviews:read", description="Чтение отзывов", resource="reviews", action="read"),
            Permission(id=11, name="reviews:create", description="Создание отзывов", resource="reviews", action="create"),
            Permission(id=12, name="reviews:delete", description="Удаление отзывов", resource="reviews", action="delete"),
            
            Permission(id=13, name="users:read", description="Чтение пользователей", resource="users", action="read"),
            Permission(id=14, name="users:manage", description="Управление пользователями", resource="users", action="manage"),
            
            Permission(id=15, name="exchange_points:read", description="Чтение пунктов обмена", resource="exchange_points", action="read"),
            Permission(id=16, name="exchange_points:manage", description="Управление пунктами обмена", resource="exchange_points", action="manage"),
            
            Permission(id=17, name="statistics:read", description="Просмотр статистики", resource="statistics", action="read"),
            Permission(id=18, name="files:upload", description="Загрузка файлов", resource="files", action="upload"),
            Permission(id=19, name="files:delete", description="Удаление файлов", resource="files", action="delete"),
            Permission(id=20, name="files:manage", description="Управление всеми файлами", resource="files", action="manage"),
        ]
        db.add_all(permissions)
        db.commit()
        
        print("Назначение разрешений ролям...")
        # Guest: только чтение
        guest_permissions = [1, 6, 10, 13, 15, 17]
        for perm_id in guest_permissions:
            db.add(RolePermission(role_id=3, permission_id=perm_id))
        
        # User: чтение + создание + обновление своих + удаление своих
        user_permissions = [1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18, 19]
        for perm_id in user_permissions:
            db.add(RolePermission(role_id=2, permission_id=perm_id))
        
        # Admin: полный доступ
        admin_permissions = list(range(1, 21))
        for perm_id in admin_permissions:
            db.add(RolePermission(role_id=1, permission_id=perm_id))
        
        db.commit()
        
        print("Добавление пунктов обмена...")
        exchange_points = [
            ExchangePoint(
                name="Central Library",
                address="123 Main St",
                working_hours="9:00-18:00",
                description="Главная библиотека города",
                contact_person="Иванов Иван",
                phone="+7 (999) 123-45-67"
            ),
            ExchangePoint(
                name="North Branch",
                address="456 North Ave",
                working_hours="10:00-20:00",
                description="Северное отделение библиотеки",
                contact_person="Петрова Мария",
                phone="+7 (999) 765-43-21"
            ),
            ExchangePoint(
                name="University Center",
                address="789 University Blvd",
                working_hours="8:00-22:00",
                description="Библиотека университета",
                contact_person="Сидоров Алексей",
                phone="+7 (999) 111-22-33"
            ),
        ]
        db.add_all(exchange_points)
        db.commit()
        
        print("Добавление администратора...")
        admin_user = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=pwd_context.hash("admin123"),
            role_id=1,
            is_active=True,
            is_verified=True,
            phone="+7 (999) 000-00-00"
        )
        db.add(admin_user)
        db.commit()
        
        print("\n" + "="*50)
        print("✅ Инициализация завершена!")
        print("="*50)
        print("\nУчетные данные:")
        print("  Email: admin@example.com")
        print("  Пароль: admin123")
        print("  Роль: Admin")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка инициализации: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()

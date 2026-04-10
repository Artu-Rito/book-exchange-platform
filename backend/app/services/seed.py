from app.core.database import SessionLocal
from app.models.user import Role, Permission, RolePermission
from app.models.exchange_point import ExchangePoint


def init_sample_data():
    """Инициализация начальных данных"""
    db = SessionLocal()
    
    try:
        # Проверяем есть ли уже роли
        existing_roles = db.query(Role).count()
        if existing_roles > 0:
            db.close()
            return
        
        # Создаем роли
        roles = [
            Role(name='admin', description='Administrator'),
            Role(name='user', description='Regular user'),
            Role(name='guest', description='Guest')
        ]
        for r in roles:
            db.add(r)
        db.flush()
        
        # Создаем разрешения
        perms = [
            Permission(name='books_create', resource='books', action='create'),
            Permission(name='books_read', resource='books', action='read'),
            Permission(name='books_update', resource='books', action='update'),
            Permission(name='books_delete', resource='books', action='delete'),
            Permission(name='reservations_create', resource='reservations', action='create'),
            Permission(name='reservations_read', resource='reservations', action='read'),
            Permission(name='reservations_update', resource='reservations', action='update'),
            Permission(name='reviews_create', resource='reviews', action='create'),
            Permission(name='reviews_read', resource='reviews', action='read'),
            Permission(name='admin_manage', resource='admin', action='manage')
        ]
        for p in perms:
            db.add(p)
        db.flush()
        
        # Создаем пункты обмена
        points = [
            ExchangePoint(name='Central Library', address='123 Main St', working_hours='9:00-18:00'),
            ExchangePoint(name='University Campus', address='456 University Ave', working_hours='8:00-20:00'),
            ExchangePoint(name='Park Gorky', address='Park Gorky, Pavilion', working_hours='10:00-19:00')
        ]
        for p in points:
            db.add(p)
        
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.repositories.reservation import ReservationRepository
from app.repositories.book import BookRepository
from app.repositories.user import UserRepository
from app.schemas.reservation import ReservationCreate
from app.services.email_service import email_service
from datetime import datetime, timedelta


class ReservationService:
    """Сервис для работы с бронированиями"""

    def __init__(self, db: Session):
        self.db = db
        self.reservation_repo = ReservationRepository(db)
        self.book_repo = BookRepository(db)
        self.user_repo = UserRepository(db)
    
    def get_reservation(self, reservation_id: int) -> Optional[dict]:
        """Получить бронирование"""
        try:
            reservation = self.reservation_repo.get_with_relations(reservation_id)
            if not reservation:
                return None
            
            return self._reservation_to_dict(reservation)
        except Exception:
            return None
    
    def get_user_reservations(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[dict], int]:
        """Получить бронирования пользователя"""
        try:
            reservations, total = self.reservation_repo.get_by_user(user_id, page, page_size)
            
            reservations_data = []
            for res in reservations:
                reservations_data.append({
                    "id": res.id,
                    "book_id": res.book_id,
                    "book": {
                        "id": res.book.id,
                        "title": res.book.title,
                        "author": res.book.author,
                    } if res.book else None,
                    "user_id": res.user_id,
                    "exchange_point_id": res.exchange_point_id,
                    "exchange_point": {
                        "id": res.exchange_point.id,
                        "name": res.exchange_point.name,
                        "address": res.exchange_point.address,
                        "working_hours": res.exchange_point.working_hours,
                    } if res.exchange_point else None,
                    "reservation_date": res.reservation_date.isoformat(),
                    "pickup_date": res.pickup_date.isoformat(),
                    "return_date": res.return_date.isoformat(),
                    "actual_return_date": res.actual_return_date.isoformat() if res.actual_return_date else None,
                    "status": res.status.value if hasattr(res.status, 'value') else res.status,
                    "created_at": res.created_at.isoformat(),
                    "updated_at": res.updated_at.isoformat(),
                })
            
            return reservations_data, total
        except Exception:
            return [], 0
    
    def create_reservation(
        self,
        reservation_in: ReservationCreate,
        user_id: int,
    ) -> dict:
        """Создать бронирование"""
        try:
            book = self.book_repo.get(reservation_in.book_id)
            if not book:
                raise ValueError("Book not found")

            book_status = book.status.upper() if hasattr(book.status, 'upper') else str(book.status).upper()
            if book_status != "AVAILABLE":
                raise ValueError("Book is not available")

            if book.owner_id == user_id:
                raise ValueError("Cannot reserve your own book")

            # Получаем владельца книги
            owner = self.user_repo.get(book.owner_id)
            # Получаем пользователя, который бронирует
            reserver = self.user_repo.get(user_id)
            
            # Получаем пункт выдачи
            exchange_point = None
            if reservation_in.exchange_point_id:
                from app.repositories.exchange_point import ExchangePointRepository
                ep_repo = ExchangePointRepository(self.db)
                exchange_point = ep_repo.get(reservation_in.exchange_point_id)

            now = datetime.utcnow()
            reservation_data = {
                "book_id": reservation_in.book_id,
                "user_id": user_id,
                "exchange_point_id": reservation_in.exchange_point_id,
                "reservation_date": now,
                "pickup_date": now + timedelta(days=2),
                "return_date": now + timedelta(days=14),
                "status": "RESERVED",
            }

            reservation = self.reservation_repo.create(reservation_data)
            self.book_repo.update(book, {"status": "RESERVED"})

            result = self.get_reservation(reservation.id)

            # Отправляем email уведомления
            try:
                # Уведомление владельцу книги
                if owner and owner.email:
                    email_service.send_reservation_notification(
                        owner_email=owner.email,
                        book_title=book.title,
                        reserver_name=reserver.full_name if reserver else "Неизвестно",
                        reserver_phone=reserver.phone if reserver else None,
                        pickup_point_name=exchange_point.name if exchange_point else "",
                        pickup_point_address=exchange_point.address if exchange_point else ""
                    )
                
                # Уведомление забронировавшему пользователю
                if reserver and reserver.email:
                    book_owner = self.user_repo.get(book.owner_id)
                    email_service.send_reservation_confirmation(
                        reserver_email=reserver.email,
                        book_title=book.title,
                        owner_name=book_owner.full_name if book_owner else "Неизвестно",
                        owner_phone=book_owner.phone if book_owner else None,
                        pickup_point_name=exchange_point.name if exchange_point else "",
                        pickup_point_address=exchange_point.address if exchange_point else "",
                        pickup_point_contact=exchange_point.contact_person if exchange_point else None,
                        pickup_point_phone=exchange_point.phone if exchange_point else None
                    )
            except Exception as e:
                # Ловим ошибки email, но не прерываем создание бронирования
                pass

            return result
        except (ValueError, PermissionError):
            raise
        except Exception:
            raise

    def confirm_pickup(self, reservation_id: int, user_id: int) -> Optional[dict]:
        """Подтвердить получение книги"""
        try:
            reservation = self.reservation_repo.get(reservation_id)
            if not reservation:
                return None

            if reservation.user_id != user_id:
                raise PermissionError("Not authorized to confirm pickup")

            update_data = {"status": "PICKED_UP"}
            updated_reservation = self.reservation_repo.update(reservation, update_data)

            return self.get_reservation(updated_reservation.id)
        except (PermissionError, ValueError):
            raise
        except Exception:
            raise

    def confirm_return(self, reservation_id: int, user_id: int) -> Optional[dict]:
        """Подтвердить возврат книги"""
        try:
            reservation = self.reservation_repo.get(reservation_id)
            if not reservation:
                return None

            if reservation.user_id != user_id:
                raise PermissionError("Not authorized to confirm return")

            update_data = {
                "status": "RETURNED",
                "actual_return_date": datetime.utcnow()
            }
            updated_reservation = self.reservation_repo.update(reservation, update_data)

            # Освобождаем книгу
            book = self.book_repo.get(reservation.book_id)
            if book:
                self.book_repo.update(book, {"status": "AVAILABLE"})

            return self.get_reservation(updated_reservation.id)
        except (PermissionError, ValueError):
            raise
        except Exception:
            raise

    def update_reservation_status(
        self,
        reservation_id: int,
        status: str,
        user_id: int,
    ) -> Optional[dict]:
        """Обновить статус бронирования"""
        try:
            reservation = self.reservation_repo.get(reservation_id)
            if not reservation:
                return None
            
            if reservation.user_id != user_id:
                raise PermissionError("Not authorized to update this reservation")
            
            update_data = {"status": status}
            
            if status == "RETURNED":
                update_data["actual_return_date"] = datetime.utcnow()
                book = self.book_repo.get(reservation.book_id)
                if book:
                    self.book_repo.update(book, {"status": "AVAILABLE"})
            
            updated_reservation = self.reservation_repo.update(reservation, update_data)
            
            return self.get_reservation(updated_reservation.id)
        except (PermissionError, ValueError):
            raise
        except Exception:
            raise
    
    def cancel_reservation(self, reservation_id: int, user_id: int) -> Optional[dict]:
        """Отменить бронирование"""
        return self.update_reservation_status(
            reservation_id,
            "CANCELLED",
            user_id,
        )
    
    def get_active_reservations(self, user_id: int) -> List[dict]:
        """Получить активные бронирования"""
        try:
            reservations = self.reservation_repo.get_active_by_user(user_id)
            
            return [
                {
                    "id": res.id,
                    "book_id": res.book_id,
                    "pickup_date": res.pickup_date.isoformat(),
                    "return_date": res.return_date.isoformat(),
                    "status": res.status.value,
                }
                for res in reservations
            ]
        except Exception:
            return []
    
    def _reservation_to_dict(self, reservation) -> dict:
        """Конвертация бронирования в словарь"""
        status_val = reservation.status
        if hasattr(status_val, 'lower'):
            status_val = status_val.lower()
        
        return {
            "id": reservation.id,
            "book_id": reservation.book_id,
            "user_id": reservation.user_id,
            "exchange_point_id": reservation.exchange_point_id,
            "reservation_date": reservation.reservation_date.isoformat(),
            "pickup_date": reservation.pickup_date.isoformat(),
            "return_date": reservation.return_date.isoformat(),
            "actual_return_date": reservation.actual_return_date.isoformat() if reservation.actual_return_date else None,
            "status": status_val,
            "created_at": reservation.created_at.isoformat() if reservation.created_at else None,
            "updated_at": reservation.updated_at.isoformat() if reservation.updated_at else None,
        }

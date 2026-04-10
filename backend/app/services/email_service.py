import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Сервис для отправки email уведомлений"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "")
        self.enabled = bool(self.smtp_server and self.smtp_user and self.smtp_password)
        
        if not self.enabled:
            logger.warning("Email notifications disabled. Set SMTP_SERVER, SMTP_USER, SMTP_PASSWORD to enable.")
    
    def send_email(self, to_email: str, subject: str, body: str, html: bool = False) -> bool:
        """Отправка email"""
        if not self.enabled:
            logger.info(f"Email not sent (disabled): {to_email} - {subject}")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email or self.smtp_user
            msg['To'] = to_email
            
            content_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, content_type, 'utf-8'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_reservation_notification(
        self,
        owner_email: str,
        book_title: str,
        reserver_name: str,
        reserver_phone: Optional[str] = None,
        pickup_point_name: str = "",
        pickup_point_address: str = ""
    ) -> bool:
        """Отправка уведомления владельцу книги о бронировании"""
        
        subject = f"📚 Книга '{book_title}' забронирована!"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #667eea;">📚 Новая резервация книги</h2>
            
            <p>Здравствуйте!</p>
            
            <p>Ваша книга <strong>"{book_title}"</strong> была забронирована.</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2c3e50; margin-top: 0;">📋 Детали бронирования</h3>
                <p><strong>Забронировал:</strong> {reserver_name}</p>
                {f'<p><strong>Телефон:</strong> <a href="tel:{reserver_phone}">{reserver_phone}</a></p>' if reserver_phone else '<p><em>Телефон не указан</em></p>'}
                <p><strong>Место получения:</strong> {pickup_point_name or 'Не указано'}</p>
                {f'<p><strong>Адрес:</strong> {pickup_point_address}</p>' if pickup_point_address else ''}
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
                <p style="margin: 0;"><strong>⏰ Важно:</strong> Пожалуйста, подтвердите готовность передать книгу или свяжитесь с пользователем для уточнения деталей.</p>
            </div>
            
            <p style="color: #7f8c8d; font-size: 14px; margin-top: 30px;">
                Это письмо отправлено автоматически платформой Book Exchange.
            </p>
        </body>
        </html>
        """
        
        return self.send_email(owner_email, subject, body, html=True)
    
    def send_reservation_confirmation(
        self,
        reserver_email: str,
        book_title: str,
        owner_name: str,
        owner_phone: Optional[str] = None,
        pickup_point_name: str = "",
        pickup_point_address: str = "",
        pickup_point_contact: Optional[str] = None,
        pickup_point_phone: Optional[str] = None
    ) -> bool:
        """Отправка подтверждения пользователю, забронировавшему книгу"""
        
        subject = f"✅ Книга '{book_title}' забронирована!"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #27ae60;">✅ Бронирование подтверждено!</h2>
            
            <p>Здравствуйте!</p>
            
            <p>Вы успешно забронировали книгу <strong>"{book_title}"</strong>.</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2c3e50; margin-top: 0;">📋 Детали</h3>
                <p><strong>Владелец:</strong> {owner_name}</p>
                {f'<p><strong>Телефон владельца:</strong> <a href="tel:{owner_phone}">{owner_phone}</a></p>' if owner_phone else '<p><em>Телефон владельца не указан</em></p>'}
            </div>
            
            <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #1976d2; margin-top: 0;">📍 Место получения</h3>
                <p><strong>{pickup_point_name or 'Не указано'}</strong></p>
                {f'<p><strong>Адрес:</strong> {pickup_point_address}</p>' if pickup_point_address else ''}
                {f'<p><strong>Контакт:</strong> {pickup_point_contact}</p>' if pickup_point_contact else ''}
                {f'<p><strong>Телефон:</strong> <a href="tel:{pickup_point_phone}">{pickup_point_phone}</a></p>' if pickup_point_phone else ''}
            </div>
            
            <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                <p style="margin: 0;"><strong>📦 Следующие шаги:</strong> Свяжитесь с владельцем книги для согласования времени встречи.</p>
            </div>
            
            <p style="color: #7f8c8d; font-size: 14px; margin-top: 30px;">
                Это письмо отправлено автоматически платформой Book Exchange.
            </p>
        </body>
        </html>
        """
        
        return self.send_email(reserver_email, subject, body, html=True)


# Глобальный экземпляр сервиса
email_service = EmailService()

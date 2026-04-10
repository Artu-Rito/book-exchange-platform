-- Миграция: Добавление полей contact_person и phone в таблицу exchange_points
-- Для применения: sqlite3 book_exchange.db < migrate_add_exchange_point_contacts.sql

ALTER TABLE exchange_points ADD COLUMN contact_person VARCHAR(255);
ALTER TABLE exchange_points ADD COLUMN phone VARCHAR(50);

# GeoInk — API для геометок с сообщениями (для стажировки в компанию RED Collar)

REST API для создания географических точек, привязки к ним текстовых сообщений и поиска по радиусу. Реализовано на **Django + DRF** с использованием формулы гаверсинуса для геопоиска — **без зависимости от PostGIS/GeoDjango**.

> Лёгкий бэкенд для гео-сервисов, который можно запустить на любом хостинге с поддержкой Python.

---

## Функционал
- Создание/редактирование/удаление гео-точек (GeoPin)
- Привязка текстовых сообщений (PinMemo) к точкам
- Поиск точек и сообщений в радиусе (формула гаверсинуса)
- Токен-авторизация (DRF Authtoken)
- Покрытие тестами (Django TestCase)
- Работа на SQLite — не требует настройки БД

---

## Технологии
| Компонент | Версия / Библиотека |
|-----------|---------------------|
| Фреймворк | Django 5.0 + Django REST Framework |
| База данных | SQLite (разработка) / PostgreSQL (продакшн) |
| Авторизация | `rest_framework.authtoken` |
| Геопоиск | Формула гаверсинуса (чистый Python) |
| Тесты | `django.test.TestCase` |
| Документация | DRF Browsable API + README |

---

## Установка и запуск

### 1. Клонирование
```bash
git clone https://github.com/RomahaPoleha/geoink.git
cd geoink
```

### 2. Виртуальное окружение
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Зависимости
```bash
pip install -r requirements.txt
```

### 4. Миграции и суперпользователь
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Запуск сервера
```bash
python manage.py runserver
```

# Авторизация

## Получение токена
```bash
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
  -d "username=admin&password=your_password"
```

# Примеры запросов
```bash
curl -X POST http://127.0.0.1:8000/api/points/ \
  -H "Authorization: Token ВАШ_ТОКЕН" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 43.1056,
    "longitude": 131.8735,
    "title": "Моя метка",
    "description": "Тут я"
  }'
```

## Добавить сообщение к точке
```bash
curl -X POST http://127.0.0.1:8000/api/points/messages/ \
  -H "Authorization: Token ВАШ_ТОКЕН" \
  -H "Content-Type: application/json" \
  -d '{
    "pin_id": 1,
    "content": "Тут я был!"
  }'
```
# Поиск точек в радиусе 10 км
```bash
curl "http://127.0.0.1:8000/api/points/search/?latitude=43.1056&longitude=131.8735&radius=10" \
  -H "Authorization: Token ВАШ_ТОКЕН"
```

# Поиск сообщений в радиусе
```bash
curl "http://127.0.0.1:8000/api/points/messages/search/?latitude=43.1056&longitude=131.8735&radius=10" \
  -H "Authorization: Token ВАШ_ТОКЕН"
```

#Тестирование
```bash
# Запустить все тесты
python manage.py test

# Запустить с выводом подробностей
python manage.py test --verbosity=2
```
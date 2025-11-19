# Alfa Backend - Production Telegram Campaign Manager

Полнофункциональный backend для управления Telegram контактами и рассылками с использованием Telethon API.

## Возможности

✅ **Парсинг контактов** из Telegram (личные контакты, группы, каналы)  
✅ **Управление кампаниями** - создание, отправка, мониторинг  
✅ **Соблюдение лимитов Telegram** - автоматические задержки и паузы  
✅ **Обработка ошибок** - retry логика, обработка блокировок  
✅ **Логирование и аудит** - полная история всех действий  
✅ **REST API** - интеграция с админкой  
✅ **Production-ready** - готово к развертыванию  

## Установка

### 1. Установить зависимости

```bash
pip install -r requirements.txt
```

### 2. Настроить конфигурацию

Отредактируйте файл `.env`:

```env
TELEGRAM_API_ID=31715478
TELEGRAM_API_HASH=ef2c4e46bea6dae2365472b194f98c86
TELEGRAM_PHONE=+79280358936
DATABASE_URL=sqlite:///./alfa.db
```

### 3. Запустить сервер

```bash
python main.py
```

Сервер запустится на `http://localhost:8000`

## API Endpoints

### Telethon

- `POST /api/telethon/connect` - Подключиться к Telegram
- `POST /api/telethon/sync-contacts` - Синхронизировать контакты
- `POST /api/telethon/groups-channels` - Получить группы и каналы

### Контакты

- `GET /api/contacts` - Получить список контактов
- `POST /api/contacts` - Создать контакт
- `POST /api/contacts/import` - Импортировать контакты из CSV

### Кампании

- `GET /api/campaigns` - Получить список кампаний
- `POST /api/campaigns` - Создать кампанию
- `POST /api/campaigns/{id}/send` - Отправить кампанию

### Сообщения

- `GET /api/messages/{contact_id}` - Получить историю сообщений
- `POST /api/messages` - Отправить сообщение

## Архитектура

```
main.py                 - FastAPI приложение и endpoints
telethon_service.py     - Сервис для работы с Telegram API
models.py               - SQLAlchemy модели БД
database.py             - Конфигурация БД
config.py               - Конфигурация приложения
```

## Особенности Production версии

### 1. Соблюдение политики Telegram

- Автоматические задержки между сообщениями (2-3 сек)
- Пауза после каждых 10 сообщений (60 сек)
- Обработка Flood Wait ошибок
- Обработка блокировок пользователей

### 2. Обработка ошибок

- Retry логика с экспоненциальной задержкой
- Обработка всех типов ошибок Telethon
- Логирование всех ошибок
- Graceful degradation

### 3. Логирование и мониторинг

- Структурированное логирование
- Аудит всех действий
- Статистика кампаний
- Отслеживание статуса сообщений

### 4. Масштабируемость

- Асинхронная обработка
- Пулинг БД отключен для асинхронности
- Готово к развертыванию на production сервере

## Примеры использования

### 1. Подключиться к Telegram

```bash
curl -X POST http://localhost:8000/api/telethon/connect
```

### 2. Синхронизировать контакты

```bash
curl -X POST http://localhost:8000/api/telethon/sync-contacts
```

### 3. Создать кампанию

```bash
curl -X POST http://localhost:8000/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Рассылка по Альфе",
    "message_template": "Привет! Это сообщение от Альфа Банка",
    "total_contacts": 100
  }'
```

### 4. Отправить кампанию

```bash
curl -X POST http://localhost:8000/api/campaigns/1/send \
  -H "Content-Type: application/json" \
  -d '{"contact_ids": [123456, 789012, ...]}'
```

### 5. Импортировать контакты

```bash
curl -X POST http://localhost:8000/api/contacts/import \
  -F "file=@contacts.csv"
```

## Формат CSV для импорта

```csv
first_name,last_name,phone,telegram_id,username
Иван,Петров,+79280358936,123456789,ivanov
Мария,Сидорова,+79280358937,987654321,sidorova
```

## Развертывание на Production

### 1. Использовать PostgreSQL вместо SQLite

```env
DATABASE_URL=postgresql://user:password@localhost:5432/alfa_db
```

### 2. Запустить с Gunicorn

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### 3. Использовать Nginx как reverse proxy

```nginx
server {
    listen 80;
    server_name api.alfa.local;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Безопасность

- ✅ Все данные Telegram зашифрованы в сессии
- ✅ Пароль 2FA запрашивается при первом подключении
- ✅ Логирование не содержит чувствительных данных
- ✅ CORS настроен для админки

## Лицензия

MIT

## Поддержка

Для вопросов и проблем обращайтесь к разработчику.

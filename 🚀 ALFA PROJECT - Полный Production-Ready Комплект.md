# 🚀 ALFA PROJECT - Полный Production-Ready Комплект

## Обзор

Вы получили **полнофункциональную систему для автоматизированного заработка в проекте "Свой в Альфе"** от Альфа Банка с использованием Telegram-бота и админ-панели.

Это не просто код — это **готовое к использованию бизнес-решение** с:
- ✅ AI-ботом для рекомендаций продуктов
- ✅ Веб-админкой для управления контактами
- ✅ Python backend для работы с Telegram API
- ✅ Production-ready архитектурой

---

## 📦 Компоненты проекта

### 1. **Telegram AI-Bot** (`/home/ubuntu/alfa_bot`)
Автономный Telegram-бот с функциями ИИ для рекомендации продуктов "Свой в Альфе".

**Файлы:**
- `main.py` - Основной бот с FSM (конечный автомат)
- `sender.py` - Скрипт для активной рассылки через личный аккаунт
- `config.py` - Конфигурация с НЛП-промптами
- `db.py` - Работа с базой данных контактов

**Функционал:**
- Загрузка контактов из файлов
- Рекомендация баллоемких продуктов через ИИ
- Обработка возражений клиентов
- Использование НЛП для убеждения
- Воронка продаж с обработкой возражений
- Активная рассылка по контактам

**Запуск:**
```bash
cd /home/ubuntu/alfa_bot
pip install -r requirements.txt
python main.py
```

---

### 2. **Веб-Админка** (`/home/ubuntu/alfa_admin_panel`)
React + FastAPI приложение для управления контактами и кампаниями.

**Стек:**
- Frontend: React 19 + Tailwind CSS 4
- Backend: Node.js + tRPC + FastAPI
- Database: SQLite/PostgreSQL
- UI: WhatsApp-style интерфейс

**Функционал:**
- Просмотр всех контактов, групп, каналов
- Управление кампаниями рассылок
- История диалогов в стиле WhatsApp
- Загрузка контактов из файлов
- Выбор целевых контактов для рассылки
- Real-time мониторинг отправки

**Запуск:**
```bash
cd /home/ubuntu/alfa_admin_panel
pnpm install
pnpm dev
```

Админка доступна на `http://localhost:3000`

---

### 3. **Python Backend** (`/home/ubuntu/alfa_backend`)
Production-ready FastAPI сервис для работы с Telegram API через Telethon.

**Функционал:**
- Парсинг контактов из Telegram
- Получение групп и каналов
- Отправка сообщений с соблюдением лимитов
- Управление кампаниями
- Импорт контактов из CSV
- Логирование и аудит

**Запуск:**
```bash
cd /home/ubuntu/alfa_backend
pip install -r requirements.txt
python main.py
```

Backend доступен на `http://localhost:8000`

---

## 🔧 Конфигурация

### Telegram API Credentials
```
TELEGRAM_API_ID=31715478
TELEGRAM_API_HASH=ef2c4e46bea6dae2365472b194f98c86
TELEGRAM_PHONE=+79280358936
```

### OpenAI API Key
Для работы ИИ-функций установите `OPENAI_API_KEY` в `.env` файлах.

### Database
- **Локальная разработка:** SQLite (`sqlite:///./alfa.db`)
- **Production:** PostgreSQL (`postgresql://user:pass@host/db`)

---

## 🎯 Рабочий процесс

### Сценарий 1: Активная рассылка через личный аккаунт

1. **Загрузить контакты** в админку (CSV файл)
2. **Выбрать целевые контакты** в админке
3. **Запустить рассылку** через Python backend
4. **Мониторить результаты** в админке

### Сценарий 2: Автоматический бот

1. **Пользователь пишет боту**
2. **Бот анализирует потребности** через ИИ
3. **Бот рекомендует продукт** с максимальными баллами
4. **Бот обрабатывает возражения** через НЛП
5. **Пользователь переходит по ссылке** и оформляет продукт
6. **Вы получаете баллы и комиссию**

---

## 📊 Архитектура системы

```
┌─────────────────────────────────────────────────────────┐
│                   Telegram Users                         │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
    ┌───▼────┐      ┌────▼──────┐
    │  Bot   │      │  Personal  │
    │ (tRPC) │      │  Account   │
    └───┬────┘      └────┬───────┘
        │                │
        │         ┌──────▼──────┐
        │         │   Sender.py  │
        │         │  (Active DM) │
        │         └──────┬───────┘
        │                │
        └────────┬───────┘
                 │
        ┌────────▼────────────┐
        │  Python Backend     │
        │  (FastAPI + Telethon)
        └────────┬────────────┘
                 │
        ┌────────▼────────────┐
        │  Admin Panel        │
        │  (React + Node.js)  │
        └────────┬────────────┘
                 │
        ┌────────▼────────────┐
        │   Database          │
        │  (SQLite/PostgreSQL)│
        └─────────────────────┘
```

---

## 💰 Монетизация

### Доход в "Свой в Альфе"

1. **Рекомендация продуктов** → Баллы за клиента
2. **Рекрутинг партнеров** → Баллы от структуры (до 3-х поколений)
3. **Достижение квалификации** → Бонусы (до 5 млн руб)

### Автоматизация заработка

- **Бот** автоматически рекомендует наиболее баллоемкие продукты
- **Админка** позволяет управлять большими объемами контактов
- **Рассылка** инициирует диалоги с потенциальными клиентами
- **НЛП** увеличивает конверсию через психологическое убеждение

---

## 🚀 Развертывание на Production

### 1. Сервер

Рекомендуемые параметры:
- OS: Ubuntu 20.04+
- CPU: 2+ cores
- RAM: 4GB+
- Storage: 20GB+

### 2. Установка

```bash
# Клонировать проекты
git clone <repo> /opt/alfa

# Установить зависимости
cd /opt/alfa/alfa_backend && pip install -r requirements.txt
cd /opt/alfa/alfa_admin_panel && pnpm install
cd /opt/alfa/alfa_bot && pip install -r requirements.txt

# Создать .env файлы
cp .env.example .env
# Отредактировать .env с реальными значениями
```

### 3. Systemd сервисы

**Python Backend** (`/etc/systemd/system/alfa-backend.service`):
```ini
[Unit]
Description=Alfa Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/alfa/alfa_backend
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Админка** (`/etc/systemd/system/alfa-admin.service`):
```ini
[Unit]
Description=Alfa Admin Panel
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/alfa/alfa_admin_panel
ExecStart=/usr/bin/pnpm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Nginx конфигурация

```nginx
upstream backend {
    server localhost:8000;
}

upstream admin {
    server localhost:3000;
}

server {
    listen 80;
    server_name api.alfa.local admin.alfa.local;

    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://admin;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📈 Метрики и KPI

Отслеживайте в админке:

- **Контакты:** Всего, активных, заблокировано
- **Кампании:** Отправлено, доставлено, прочитано
- **Конверсия:** % открытий, % ответов, % переходов
- **Доход:** Баллы за клиентов, комиссии, бонусы

---

## 🛡️ Безопасность

✅ Все данные Telegram зашифрованы  
✅ Пароль 2FA запрашивается при первом подключении  
✅ Логирование не содержит чувствительных данных  
✅ CORS настроен для админки  
✅ Соблюдение политики Telegram (без риска блокировки)  

---

## 🐛 Troubleshooting

### Бот не подключается к Telegram
```bash
# Проверить credentials в config.py
# Убедиться, что номер телефона верный
# Ввести код подтверждения при первом запуске
```

### Админка не видит контакты
```bash
# Проверить, что Python backend запущен
# Проверить, что PYTHON_API_URL правильный в .env
# Запустить синхронизацию контактов через API
```

### Сообщения не отправляются
```bash
# Проверить лимиты Telegram (30 сообщений в минуту)
# Проверить, что контакты не заблокировали бота
# Проверить логи Python backend
```

---

## 📚 Документация

- `alfa_bot/README.md` - Документация бота
- `alfa_admin_panel/README.md` - Документация админки
- `alfa_backend/README.md` - Документация backend

---

## 🤝 Поддержка

Для вопросов и проблем обращайтесь к разработчику.

---

## 📝 Лицензия

MIT

---

**Дата создания:** 19 ноября 2025  
**Версия:** 1.0.0 Production  
**Статус:** Ready for Business

# 🚀 Alfa Campaign Manager

**Автоматизированная система управления Telegram-кампаниями для программы "Свой в Альфе"**

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Commercial-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

---

## 📋 Описание

**Alfa Campaign Manager** - это полнофункциональная система для автоматизации работы с Telegram в рамках партнерской программы "Свой в Альфе" от Альфа-Банка. Система позволяет автоматически инициировать диалоги, управлять контактами, проводить кампании рассылок и анализировать результаты.

### 🎯 Ключевые возможности

- ✅ **Автоматическая инициация диалогов** - бот сам начинает общение с контактами
- ✅ **Умные первые сообщения** - персонализированные сообщения на основе профиля контакта
- ✅ **ИИ-рекомендации** - автоматический подбор наиболее баллоемких продуктов
- ✅ **Обработка возражений** - интеллектуальные ответы на вопросы клиентов
- ✅ **Парсинг контактов** - автоматический сбор контактов из групп и каналов
- ✅ **Управление кампаниями** - планирование и запуск массовых рассылок
- ✅ **Аналитика в реальном времени** - мониторинг эффективности кампаний
- ✅ **Соблюдение политики Telegram** - защита от блокировки аккаунта
- ✅ **Бесплатные ИИ API** - интеграция с Gemini, Groq, Ollama
- ✅ **Веб-админка** - удобный интерфейс в стиле WhatsApp

---

## 🏗️ Архитектура

```
┌──────────────────────────────────────────────────────────────┐
│                    ALFA CAMPAIGN MANAGER                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ BACKEND (Python/FastAPI)                                │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ • Telethon Service - управление Telegram API           │ │
│  │ • Knowledge Base - база знаний о программе             │ │
│  │ • Free LLM Service - бесплатные ИИ (Gemini, Groq)     │ │
│  │ • Dialog Initiator - автоматическая инициация чатов    │ │
│  │ • Setup Wizard - мастер первоначальной настройки       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ DATABASE (SQLite/PostgreSQL)                            │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ • Contacts - контакты для рассылки                      │ │
│  │ • Groups - группы и каналы                             │ │
│  │ • Campaigns - кампании рассылок                         │ │
│  │ • Messages - история сообщений                          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ FRONTEND (React/Web Admin)                              │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │ • Setup UI - веб-интерфейс настройки API ключей        │ │
│  │ • AdminPanel - просмотр контактов и чатов              │ │
│  │ • CampaignManager - управление кампаниями             │ │
│  │ • Analytics - статистика и результаты                 │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Быстрый старт

### 1. Системные требования

- Python 3.11+
- Node.js 18+ (для frontend)
- 2 GB RAM
- 1 GB свободного места на диске

### 2. Установка

```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/alfa-campaign-manager.git
cd alfa-campaign-manager

# Установить зависимости
pip install -r requirements.txt

# Запустить Setup Wizard (CLI)
python setup_wizard.py

# ИЛИ запустить веб-интерфейс настройки
python main.py
# Откройте http://localhost:8000/setup
```

### 3. Получение API ключей

#### 🔵 Telegram API (обязательно)
1. Перейдите на https://my.telegram.org
2. Войдите используя ваш номер телефона
3. Перейдите в "API development tools"
4. Создайте приложение и скопируйте `API_ID` и `API_HASH`

#### 🟢 Google Gemini API (рекомендуется, бесплатно)
1. Перейдите на https://makersuite.google.com/app/apikey
2. Войдите с Google аккаунтом
3. Нажмите "Create API Key"
4. Скопируйте ключ

**Лимиты:** 60 запросов/мин, 1500 запросов/день, **бесплатно навсегда!**

#### 🟣 Groq API (рекомендуется, бесплатно)
1. Перейдите на https://console.groq.com
2. Зарегистрируйтесь или войдите
3. Перейдите в "API Keys"
4. Нажмите "Create API Key"

**Лимиты:** 30 запросов/мин, **очень быстро**, бесплатно!

### 4. Запуск

```bash
# Запустить backend
python main.py

# Откройте браузер
http://localhost:8000
```

---

## 📦 Структура проекта

```
alfa-campaign-manager/
├── Backend (Python)
│   ├── main.py                    # FastAPI приложение
│   ├── telethon_service.py        # Telegram API
│   ├── knowledge_base.py          # База знаний
│   ├── free_llm_service.py        # ИИ сервис
│   ├── dialog_initiator.py        # Инициация диалогов
│   ├── models.py                  # БД модели
│   ├── database.py                # БД подключение
│   ├── config.py                  # Конфигурация
│   ├── sender.py                  # Отправка сообщений
│   ├── api_keys_guide.py          # Руководство по API ключам
│   ├── setup_wizard.py            # CLI мастер настройки
│   ├── setup_api.py               # API для Setup UI
│   └── test_basic.py              # Базовые тесты
│
├── Frontend (React/TypeScript)
│   ├── App.tsx                    # Главный компонент
│   ├── AdminPanel.tsx             # Админ-панель
│   ├── CampaignManager.tsx        # Управление кампаниями
│   ├── SetupUI.tsx                # Веб-интерфейс настройки
│   ├── db.ts                      # БД клиент
│   ├── schema.ts                  # TypeScript схемы
│   └── routers.ts                 # Роутинг
│
├── Documentation
│   ├── README.md                  # Этот файл
│   ├── DEPLOYMENT_GUIDE.md        # Руководство по развертыванию
│   ├── API_DOCUMENTATION.md       # API документация
│   └── USER_MANUAL.md             # Руководство пользователя
│
└── Config
    ├── .env                       # Переменные окружения
    ├── requirements.txt           # Python зависимости
    └── package.json               # Node.js зависимости
```

---

## 🎓 Использование

### CLI Setup Wizard

```bash
python setup_wizard.py
```

Интерактивный мастер настройки проведет вас через все шаги:
1. Ввод Telegram API credentials
2. Настройка AI API ключей
3. Конфигурация базы данных
4. Сохранение конфигурации

### Веб-интерфейс настройки

1. Запустите `python main.py`
2. Откройте http://localhost:8000/setup
3. Заполните все поля в веб-форме
4. Нажмите "Сохранить конфигурацию"

### Проверка API ключей

```bash
# Вывести руководства по получению ключей
python api_keys_guide.py

# Проверить текущую конфигурацию
python -c "from api_keys_guide import EnvManager; EnvManager().print_status()"
```

### Запуск тестов

```bash
# Базовые тесты (без реальных API ключей)
python test_basic.py

# Полные тесты (требуются реальные API ключи)
python test_suite.py
```

---

## 🔧 Конфигурация

### Переменные окружения (.env)

```bash
# Telegram API Credentials (ОБЯЗАТЕЛЬНО)
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=0123456789abcdef0123456789abcdef
TELEGRAM_PHONE_NUMBER=+79991234567

# Telegram Bot Token (ОПЦИОНАЛЬНО)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# AI API Keys (хотя бы один ОБЯЗАТЕЛЬНО)
GEMINI_API_KEY=AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY
GROQ_API_KEY=gsk_1234567890abcdefghijklmnopqrstuv
HUGGINGFACE_TOKEN=hf_1234567890abcdefghijklmnopqrstuv

# Database
DATABASE_URL=sqlite:///./alfa.db

# Other Settings
SESSION_FILE=session.session
```

---

## 📊 Возможности

### 1. Автоматическая инициация диалогов

```python
from dialog_initiator import DialogInitiator

initiator = DialogInitiator(telethon_service, llm_service, db)

# Инициировать диалог с одним контактом
await initiator.initiate_dialog(contact_id=123)

# Массовая инициация (батч)
await initiator.initiate_batch(contact_ids=[1, 2, 3, 4, 5])

# Инициация всей кампании
await initiator.initiate_campaign(campaign_id=456)
```

### 2. ИИ-рекомендации продуктов

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase(db)

# Получить рекомендацию продукта
recommendation = kb.get_strategy_recommendation(
    current_points=5000,
    target_level="A4"
)
```

### 3. Парсинг контактов

```python
from telethon_service import TelethonService

service = TelethonService(api_id, api_hash, phone)

# Получить контакты из группы
contacts = await service.get_group_members(group_id="@mygroup")

# Сохранить в БД
for contact in contacts:
    db.add(Contact(**contact))
db.commit()
```

### 4. Управление кампаниями

```python
from models import Campaign, CampaignStatus

# Создать кампанию
campaign = Campaign(
    name="Новогодняя акция",
    message_template="Привет! Хочу рассказать о выгодном предложении...",
    status=CampaignStatus.DRAFT
)
db.add(campaign)
db.commit()

# Запустить кампанию
campaign.status = CampaignStatus.RUNNING
await initiator.initiate_campaign(campaign.id)
```

---

## 🔒 Безопасность

### Соблюдение политики Telegram

Система автоматически соблюдает все ограничения Telegram:

- ⏱️ **2-5 секунд** между сообщениями
- 🛑 **30 секунд** пауза после каждых 10 сообщений
- 💤 **60 секунд** пауза между батчами
- 🔄 **Автоматические повторы** при ошибках
- 📊 **Мониторинг лимитов** в реальном времени

### Защита данных

- 🔐 Все API ключи хранятся в `.env` файле (не в репозитории)
- 🔒 Сессии Telegram шифруются автоматически
- 🛡️ База данных защищена от SQL-инъекций (SQLAlchemy ORM)
- 🚫 Секретные данные не логируются

---

## 📈 Аналитика

### Метрики кампаний

- 📤 **Отправлено** - количество отправленных сообщений
- ✅ **Доставлено** - количество доставленных сообщений
- 👀 **Прочитано** - количество прочитанных сообщений
- 💬 **Ответило** - количество ответов от контактов
- 📊 **Конверсия** - процент успешных диалогов
- ⏱️ **Среднее время ответа** - скорость реакции контактов

### Экспорт данных

```python
# Экспорт статистики кампании в CSV
campaign_stats = db.query(CampaignContact).filter_by(campaign_id=123).all()

import csv
with open('campaign_stats.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Contact', 'Status', 'Sent At', 'Read At'])
    for stat in campaign_stats:
        writer.writerow([stat.contact_id, stat.status, stat.sent_at, stat.read_at])
```

---

## 🌐 Развертывание

### Локальное развертывание

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Настроить .env файл
python setup_wizard.py

# 3. Запустить
python main.py
```

### Google Colab

```python
# 1. Установить зависимости
!pip install -r requirements.txt

# 2. Загрузить .env файл
from google.colab import files
uploaded = files.upload()  # Загрузите .env

# 3. Запустить backend
!python main.py &

# 4. Открыть туннель
from google.colab.output import eval_js
print(eval_js("google.colab.kernel.proxyPort(8000)"))
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

```bash
# Собрать образ
docker build -t alfa-campaign-manager .

# Запустить контейнер
docker run -p 8000:8000 --env-file .env alfa-campaign-manager
```

### VPS/Cloud

```bash
# 1. Подключиться к серверу
ssh user@your-server.com

# 2. Клонировать репозиторий
git clone https://github.com/yourusername/alfa-campaign-manager.git
cd alfa-campaign-manager

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить .env
nano .env

# 5. Запустить как сервис
sudo systemctl enable alfa-campaign-manager
sudo systemctl start alfa-campaign-manager
```

---

## 🤝 Поддержка

### Часто задаваемые вопросы

**Q: Нужны ли платные API ключи?**  
A: Нет! Все ИИ API (Gemini, Groq) полностью бесплатны.

**Q: Можно ли использовать без Telegram Bot Token?**  
A: Да! Система работает через Telethon (User API), Bot Token опционален.

**Q: Безопасно ли использовать для массовых рассылок?**  
A: Да! Система соблюдает все ограничения Telegram и защищает от блокировки.

**Q: Можно ли продавать этот продукт?**  
A: Да! Это коммерческий продукт, вы можете продавать его другим заказчикам.

### Техническая поддержка

- 📧 Email: support@alfacampaign.com
- 💬 Telegram: @alfacampaign_support
- 📚 Документация: https://docs.alfacampaign.com
- 🐛 Issues: https://github.com/yourusername/alfa-campaign-manager/issues

---

## 📝 Лицензия

**Commercial License**

Этот продукт распространяется по коммерческой лицензии. Вы можете:
- ✅ Использовать для коммерческих целей
- ✅ Модифицировать под свои нужды
- ✅ Продавать другим заказчикам
- ❌ Распространять исходный код публично

---

## 🎉 Благодарности

- **Telegram** - за отличный API
- **Google** - за бесплатный Gemini API
- **Groq** - за сверхбыстрый ИИ API
- **FastAPI** - за мощный веб-фреймворк
- **Telethon** - за удобную библиотеку для Telegram

---

## 📞 Контакты

**Разработчик:** Alfa Campaign Manager Team  
**Email:** info@alfacampaign.com  
**Telegram:** @alfacampaign  
**Website:** https://alfacampaign.com

---

**Made with ❤️ for Alfa Partners**

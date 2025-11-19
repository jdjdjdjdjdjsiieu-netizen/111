# 📚 Руководство по развертыванию Alfa Campaign Manager

Это подробное руководство по развертыванию системы в различных окружениях.

---

## 📋 Содержание

1. [Системные требования](#системные-требования)
2. [Локальное развертывание](#локальное-развертывание)
3. [Развертывание в Google Colab](#развертывание-в-google-colab)
4. [Развертывание на VPS](#развертывание-на-vps)
5. [Docker развертывание](#docker-развертывание)
6. [Настройка production](#настройка-production)
7. [Решение проблем](#решение-проблем)

---

## 🖥️ Системные требования

### Минимальные требования

- **OS:** Linux (Ubuntu 20.04+), macOS 10.15+, Windows 10+
- **Python:** 3.11 или выше
- **RAM:** 2 GB
- **Disk:** 1 GB свободного места
- **Network:** Стабильное интернет-соединение

### Рекомендуемые требования

- **OS:** Ubuntu 22.04 LTS
- **Python:** 3.11
- **RAM:** 4 GB
- **Disk:** 5 GB SSD
- **Network:** 10 Mbps+

---

## 💻 Локальное развертывание

### Шаг 1: Установка Python

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

#### macOS
```bash
brew install python@3.11
```

#### Windows
Скачайте Python 3.11 с https://www.python.org/downloads/

### Шаг 2: Клонирование проекта

```bash
# Создать директорию проекта
mkdir alfa-campaign-manager
cd alfa-campaign-manager

# Скопировать все файлы проекта в эту директорию
```

### Шаг 3: Создание виртуального окружения

```bash
# Создать виртуальное окружение
python3.11 -m venv venv

# Активировать виртуальное окружение
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Шаг 4: Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Шаг 5: Первоначальная настройка

#### Вариант A: CLI Setup Wizard (рекомендуется)

```bash
python setup_wizard.py
```

Следуйте инструкциям мастера настройки:
1. Введите Telegram API credentials
2. Настройте AI API ключи
3. Выберите базу данных
4. Сохраните конфигурацию

#### Вариант B: Ручная настройка

```bash
# Создать .env файл
cp .env.example .env

# Отредактировать .env файл
nano .env
```

Заполните следующие переменные:
```bash
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=+79991234567
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
DATABASE_URL=sqlite:///./alfa.db
```

### Шаг 6: Проверка конфигурации

```bash
# Проверить статус конфигурации
python -c "from api_keys_guide import EnvManager; EnvManager().print_status()"

# Запустить базовые тесты
python test_basic.py
```

### Шаг 7: Запуск приложения

```bash
# Запустить backend
python main.py

# Приложение будет доступно по адресу:
# http://localhost:8000
```

### Шаг 8: Первый запуск

1. Откройте http://localhost:8000
2. При первом запуске Telegram попросит код подтверждения
3. Введите код из Telegram
4. Сессия будет сохранена автоматически

---

## ☁️ Развертывание в Google Colab

Google Colab - отличный вариант для бесплатного хостинга!

### Шаг 1: Создать новый Colab notebook

1. Перейдите на https://colab.research.google.com
2. Создайте новый notebook
3. Подключите Google Drive (опционально)

### Шаг 2: Установить зависимости

```python
# Установить зависимости
!pip install -q telethon fastapi uvicorn sqlalchemy pydantic python-dotenv aiohttp google-generativeai groq

# Клонировать проект (или загрузить файлы)
!git clone https://github.com/yourusername/alfa-campaign-manager.git
%cd alfa-campaign-manager
```

### Шаг 3: Настроить переменные окружения

```python
import os

# Установить переменные окружения
os.environ['TELEGRAM_API_ID'] = '12345678'
os.environ['TELEGRAM_API_HASH'] = 'your_api_hash'
os.environ['TELEGRAM_PHONE_NUMBER'] = '+79991234567'
os.environ['GEMINI_API_KEY'] = 'your_gemini_key'
os.environ['GROQ_API_KEY'] = 'your_groq_key'
os.environ['DATABASE_URL'] = 'sqlite:///./alfa.db'
```

### Шаг 4: Запустить backend

```python
# Запустить в фоновом режиме
!python main.py &

# Подождать несколько секунд
import time
time.sleep(5)
```

### Шаг 5: Открыть публичный URL

```python
# Установить ngrok для публичного доступа
!pip install pyngrok

from pyngrok import ngrok

# Открыть туннель
public_url = ngrok.connect(8000)
print(f"✅ Приложение доступно по адресу: {public_url}")
```

### Шаг 6: Использование

Откройте полученный URL в браузере и используйте приложение!

**Важно:** Colab сессия активна только пока открыт notebook. Для постоянной работы используйте VPS.

---

## 🖥️ Развертывание на VPS

### Рекомендуемые провайдеры

- **DigitalOcean** - $5/месяц (1 GB RAM)
- **Hetzner** - €3.79/месяц (2 GB RAM)
- **Vultr** - $5/месяц (1 GB RAM)
- **AWS EC2** - t2.micro (бесплатно первый год)

### Шаг 1: Подключение к серверу

```bash
ssh root@your-server-ip
```

### Шаг 2: Обновление системы

```bash
apt update && apt upgrade -y
```

### Шаг 3: Установка Python и зависимостей

```bash
# Установить Python 3.11
apt install -y python3.11 python3.11-venv python3-pip git

# Установить дополнительные пакеты
apt install -y build-essential libssl-dev libffi-dev
```

### Шаг 4: Создание пользователя

```bash
# Создать пользователя для приложения
adduser alfabot
usermod -aG sudo alfabot

# Переключиться на нового пользователя
su - alfabot
```

### Шаг 5: Клонирование проекта

```bash
cd ~
git clone https://github.com/yourusername/alfa-campaign-manager.git
cd alfa-campaign-manager
```

### Шаг 6: Настройка окружения

```bash
# Создать виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### Шаг 7: Настройка конфигурации

```bash
# Запустить Setup Wizard
python setup_wizard.py

# ИЛИ создать .env вручную
nano .env
```

### Шаг 8: Настройка systemd service

```bash
# Создать service файл
sudo nano /etc/systemd/system/alfabot.service
```

Содержимое файла:
```ini
[Unit]
Description=Alfa Campaign Manager
After=network.target

[Service]
Type=simple
User=alfabot
WorkingDirectory=/home/alfabot/alfa-campaign-manager
Environment="PATH=/home/alfabot/alfa-campaign-manager/venv/bin"
ExecStart=/home/alfabot/alfa-campaign-manager/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Шаг 9: Запуск сервиса

```bash
# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить автозапуск
sudo systemctl enable alfabot

# Запустить сервис
sudo systemctl start alfabot

# Проверить статус
sudo systemctl status alfabot
```

### Шаг 10: Настройка Nginx (опционально)

```bash
# Установить Nginx
sudo apt install -y nginx

# Создать конфигурацию
sudo nano /etc/nginx/sites-available/alfabot
```

Содержимое файла:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Активировать конфигурацию
sudo ln -s /etc/nginx/sites-available/alfabot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Шаг 11: Настройка SSL (опционально)

```bash
# Установить Certbot
sudo apt install -y certbot python3-certbot-nginx

# Получить SSL сертификат
sudo certbot --nginx -d your-domain.com
```

---

## 🐳 Docker развертывание

### Шаг 1: Создать Dockerfile

```dockerfile
FROM python:3.11-slim

# Установить системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Создать рабочую директорию
WORKDIR /app

# Скопировать requirements.txt
COPY requirements.txt .

# Установить Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать все файлы проекта
COPY . .

# Открыть порт
EXPOSE 8000

# Запустить приложение
CMD ["python", "main.py"]
```

### Шаг 2: Создать docker-compose.yml

```yaml
version: '3.8'

services:
  alfabot:
    build: .
    container_name: alfa-campaign-manager
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    
  # Опционально: PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: alfa-postgres
    environment:
      POSTGRES_DB: alfabot
      POSTGRES_USER: alfabot
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### Шаг 3: Запуск

```bash
# Собрать образ
docker-compose build

# Запустить контейнеры
docker-compose up -d

# Проверить логи
docker-compose logs -f

# Остановить контейнеры
docker-compose down
```

---

## 🚀 Настройка production

### 1. Безопасность

```bash
# Настроить firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Отключить root login
sudo nano /etc/ssh/sshd_config
# PermitRootLogin no
sudo systemctl restart sshd
```

### 2. Мониторинг

```bash
# Установить htop для мониторинга
sudo apt install -y htop

# Мониторинг логов
tail -f /var/log/alfabot/app.log

# Мониторинг systemd service
journalctl -u alfabot -f
```

### 3. Резервное копирование

```bash
# Создать скрипт backup
nano ~/backup.sh
```

Содержимое:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/alfabot/backups"
mkdir -p $BACKUP_DIR

# Backup базы данных
cp ~/alfa-campaign-manager/alfa.db $BACKUP_DIR/alfa_$DATE.db

# Backup .env файла
cp ~/alfa-campaign-manager/.env $BACKUP_DIR/env_$DATE.txt

# Удалить старые backup (старше 7 дней)
find $BACKUP_DIR -type f -mtime +7 -delete
```

```bash
# Сделать исполняемым
chmod +x ~/backup.sh

# Добавить в crontab (ежедневно в 3:00)
crontab -e
# 0 3 * * * /home/alfabot/backup.sh
```

### 4. Обновление

```bash
# Остановить сервис
sudo systemctl stop alfabot

# Обновить код
cd ~/alfa-campaign-manager
git pull

# Установить новые зависимости
source venv/bin/activate
pip install -r requirements.txt

# Запустить сервис
sudo systemctl start alfabot
```

---

## 🔧 Решение проблем

### Проблема: "ModuleNotFoundError: No module named 'telethon'"

**Решение:**
```bash
pip install telethon
```

### Проблема: "Permission denied" при установке пакетов

**Решение:**
```bash
sudo pip install -r requirements.txt
# ИЛИ
pip install --user -r requirements.txt
```

### Проблема: "Telegram API error: PHONE_CODE_INVALID"

**Решение:**
1. Убедитесь что вводите правильный код из Telegram
2. Код действителен только 5 минут
3. Попробуйте запросить код заново

### Проблема: "Database locked"

**Решение:**
```bash
# Проверить процессы использующие БД
lsof alfa.db

# Остановить все процессы
sudo systemctl stop alfabot

# Запустить заново
sudo systemctl start alfabot
```

### Проблема: "Port 8000 already in use"

**Решение:**
```bash
# Найти процесс использующий порт
lsof -i :8000

# Убить процесс
kill -9 <PID>

# ИЛИ изменить порт в main.py
# uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Проблема: "Gemini API rate limit exceeded"

**Решение:**
1. Система автоматически переключится на Groq
2. Подождите 1 минуту и попробуйте снова
3. Настройте оба API (Gemini и Groq) для резервирования

---

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте [FAQ в README.md](README.md#часто-задаваемые-вопросы)
2. Запустите `python test_basic.py` для диагностики
3. Проверьте логи: `journalctl -u alfabot -n 100`
4. Свяжитесь с поддержкой: support@alfacampaign.com

---

**Удачного развертывания! 🚀**

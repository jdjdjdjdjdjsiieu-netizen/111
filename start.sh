#!/bin/bash

# ========================================================================
#   ALFA CAMPAIGN MANAGER - Автоматический запуск для Linux/macOS
#   Запуск: ./start.sh
# ========================================================================

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "========================================================================"
echo "  ALFA CAMPAIGN MANAGER v2.0"
echo "  Автоматический запуск системы..."
echo "========================================================================"
echo ""

# Проверка Python
echo "[1/5] Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ОШИБКА] Python3 не найден!${NC}"
    echo ""
    echo "Пожалуйста, установите Python 3.11 или выше:"
    echo "  Ubuntu/Debian: sudo apt install python3.11"
    echo "  macOS: brew install python@3.11"
    echo ""
    exit 1
fi
echo -e "${GREEN}✓ Python установлен${NC}"
echo ""

# Проверка зависимостей
echo "[2/5] Проверка зависимостей..."
if ! python3 -c "import telethon" &> /dev/null; then
    echo -e "${YELLOW}[ВНИМАНИЕ] Зависимости не установлены. Устанавливаю...${NC}"
    echo ""
    
    # Попробовать с sudo если обычная установка не работает
    if pip3 install -r requirements.txt &> /dev/null; then
        echo -e "${GREEN}✓ Зависимости установлены${NC}"
    elif sudo pip3 install -r requirements.txt &> /dev/null; then
        echo -e "${GREEN}✓ Зависимости установлены (с sudo)${NC}"
    else
        echo -e "${RED}[ОШИБКА] Не удалось установить зависимости!${NC}"
        echo "Попробуйте вручную: pip3 install -r requirements.txt"
        echo ""
        exit 1
    fi
else
    echo -e "${GREEN}✓ Зависимости установлены${NC}"
fi
echo ""

# Проверка конфигурации
echo "[3/5] Проверка конфигурации..."
if [ ! -f .env ]; then
    echo -e "${YELLOW}[ВНИМАНИЕ] Файл .env не найден!${NC}"
    echo "Запускаю Setup Wizard..."
    echo ""
    sleep 2
    python3 setup_wizard.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ОШИБКА] Настройка не завершена!${NC}"
        echo ""
        exit 1
    fi
else
    echo -e "${GREEN}✓ Конфигурация найдена${NC}"
fi
echo ""

# Инициализация базы данных
echo "[4/5] Инициализация базы данных..."
if python3 -c "from database import init_db; init_db(); print('✓ База данных готова')" 2>/dev/null; then
    :
else
    echo -e "${YELLOW}⚠ База данных будет создана при первом запуске${NC}"
fi
echo ""

# Запуск приложения
echo "[5/5] Запуск приложения..."
echo ""
echo "========================================================================"
echo "  Приложение запускается..."
echo "  Откройте браузер: http://localhost:8000"
echo "  Для настройки: http://localhost:8000/setup"
echo "========================================================================"
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

# Открыть браузер автоматически через 3 секунды (если возможно)
(sleep 3 && xdg-open http://localhost:8000/setup 2>/dev/null || open http://localhost:8000/setup 2>/dev/null) &

# Запустить FastAPI приложение
python3 main.py

# Если приложение завершилось с ошибкой
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================================================"
    echo -e "  ${RED}[ОШИБКА] Приложение завершилось с ошибкой!${NC}"
    echo "========================================================================"
    echo ""
    read -p "Нажмите Enter для выхода..."
fi

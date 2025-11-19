@echo off
REM ========================================================================
REM   ALFA CAMPAIGN MANAGER - Автоматический запуск для Windows
REM   Двойной клик для запуска проекта
REM ========================================================================

title Alfa Campaign Manager - Startup

echo.
echo ========================================================================
echo   ALFA CAMPAIGN MANAGER v2.0
echo   Автоматический запуск системы...
echo ========================================================================
echo.

REM Проверка Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ОШИБКА] Python не найден!
    echo.
    echo Пожалуйста, установите Python 3.11 или выше:
    echo https://www.python.org/downloads/
    echo.
    echo После установки запустите этот файл снова.
    echo.
    pause
    exit /b 1
)
echo ✓ Python установлен
echo.

REM Проверка зависимостей
echo [2/5] Проверка зависимостей...
python -c "import telethon" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ВНИМАНИЕ] Зависимости не установлены. Устанавливаю...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ОШИБКА] Не удалось установить зависимости!
        echo Попробуйте вручную: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)
echo ✓ Зависимости установлены
echo.

REM Проверка конфигурации
echo [3/5] Проверка конфигурации...
if not exist .env (
    echo.
    echo [ВНИМАНИЕ] Файл .env не найден!
    echo Запускаю Setup Wizard...
    echo.
    timeout /t 2 >nul
    python setup_wizard.py
    if errorlevel 1 (
        echo.
        echo [ОШИБКА] Настройка не завершена!
        echo.
        pause
        exit /b 1
    )
) else (
    echo ✓ Конфигурация найдена
)
echo.

REM Инициализация базы данных
echo [4/5] Инициализация базы данных...
python -c "from database import init_db; init_db(); print('✓ База данных готова')" 2>nul
if errorlevel 1 (
    echo ⚠ База данных будет создана при первом запуске
)
echo.

REM Запуск приложения
echo [5/5] Запуск приложения...
echo.
echo ========================================================================
echo   Приложение запускается...
echo   Откройте браузер: http://localhost:8000
echo   Для настройки: http://localhost:8000/setup
echo ========================================================================
echo.
echo Для остановки нажмите Ctrl+C
echo.

REM Открыть браузер автоматически через 3 секунды
start /b timeout /t 3 >nul && start http://localhost:8000/setup

REM Запустить FastAPI приложение
python main.py

REM Если приложение завершилось с ошибкой
if errorlevel 1 (
    echo.
    echo ========================================================================
    echo   [ОШИБКА] Приложение завершилось с ошибкой!
    echo ========================================================================
    echo.
    pause
)

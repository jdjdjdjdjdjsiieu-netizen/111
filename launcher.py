#!/usr/bin/env python3
"""
ALFA CAMPAIGN MANAGER - Universal Launcher
Кроссплатформенный запуск с GUI
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# Определение платформы
IS_WINDOWS = sys.platform.startswith('win')
IS_LINUX = sys.platform.startswith('linux')
IS_MAC = sys.platform.startswith('darwin')


def print_header():
    """Вывести заголовок"""
    print("\n" + "=" * 70)
    print("  ALFA CAMPAIGN MANAGER v2.0")
    print("  Автоматический запуск системы...")
    print("=" * 70 + "\n")


def check_python():
    """Проверить версию Python"""
    print("[1/5] Проверка Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"✗ Python {version.major}.{version.minor} слишком старый!")
        print("  Требуется Python 3.11 или выше")
        print("  Скачайте: https://www.python.org/downloads/")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    print()
    return True


def check_dependencies():
    """Проверить и установить зависимости"""
    print("[2/5] Проверка зависимостей...")
    
    try:
        import telethon
        print("✓ Зависимости установлены")
        print()
        return True
    except ImportError:
        print("⚠ Зависимости не установлены. Устанавливаю...")
        print()
        
        # Установка зависимостей
        requirements = Path(__file__).parent / "requirements.txt"
        if not requirements.exists():
            print("✗ Файл requirements.txt не найден!")
            return False
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements)
            ])
            print("✓ Зависимости установлены")
            print()
            return True
        except subprocess.CalledProcessError:
            print("✗ Не удалось установить зависимости!")
            print("  Попробуйте вручную: pip install -r requirements.txt")
            return False


def check_config():
    """Проверить конфигурацию"""
    print("[3/5] Проверка конфигурации...")
    
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("⚠ Файл .env не найден!")
        print("  Запускаю Setup Wizard...")
        print()
        time.sleep(2)
        
        # Запустить setup wizard
        setup_wizard = Path(__file__).parent / "setup_wizard.py"
        try:
            subprocess.check_call([sys.executable, str(setup_wizard)])
            print("✓ Настройка завершена")
            print()
            return True
        except subprocess.CalledProcessError:
            print("✗ Настройка не завершена!")
            return False
    else:
        print("✓ Конфигурация найдена")
        print()
        return True


def init_database():
    """Инициализировать базу данных"""
    print("[4/5] Инициализация базы данных...")
    
    try:
        from database import init_db
        init_db()
        print("✓ База данных готова")
        print()
        return True
    except Exception as e:
        print(f"⚠ База данных будет создана при первом запуске")
        print()
        return True


def start_application():
    """Запустить приложение"""
    print("[5/5] Запуск приложения...")
    print()
    print("=" * 70)
    print("  Приложение запускается...")
    print("  Откройте браузер: http://localhost:8000")
    print("  Для настройки: http://localhost:8000/setup")
    print("=" * 70)
    print()
    print("Для остановки нажмите Ctrl+C")
    print()
    
    # Открыть браузер автоматически через 3 секунды
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:8000/setup')
        except:
            pass
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Запустить FastAPI приложение
    main_py = Path(__file__).parent / "main.py"
    try:
        subprocess.check_call([sys.executable, str(main_py)])
        return True
    except subprocess.CalledProcessError:
        print()
        print("=" * 70)
        print("  [ОШИБКА] Приложение завершилось с ошибкой!")
        print("=" * 70)
        print()
        return False
    except KeyboardInterrupt:
        print()
        print("Приложение остановлено пользователем")
        return True


def main():
    """Главная функция"""
    print_header()
    
    # Проверки
    if not check_python():
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    if not check_dependencies():
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    if not check_config():
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    if not init_database():
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    # Запуск
    if not start_application():
        input("\nНажмите Enter для выхода...")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПриложение остановлено пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[КРИТИЧЕСКАЯ ОШИБКА] {e}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")
        sys.exit(1)

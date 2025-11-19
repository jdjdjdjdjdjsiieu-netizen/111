"""
API Keys Guide - Модуль для получения всех необходимых API ключей
Этот модуль содержит инструкции и утилиты для получения API ключей
"""

import os
from typing import Dict, Optional
import json

class APIKeysGuide:
    """Руководство по получению API ключей для проекта"""
    
    @staticmethod
    def get_telegram_api_credentials() -> Dict[str, str]:
        """
        Получение Telegram API ID и API Hash
        
        Шаги:
        1. Перейдите на https://my.telegram.org
        2. Войдите используя ваш номер телефона
        3. Перейдите в раздел "API development tools"
        4. Создайте новое приложение:
           - App title: "Alfa Campaign Manager"
           - Short name: "alfa_bot"
           - Platform: Desktop
           - Description: "Telegram campaign management bot"
        5. Скопируйте API_ID и API_HASH
        
        Returns:
            Dict с инструкциями и примером
        """
        return {
            "url": "https://my.telegram.org",
            "steps": [
                "1. Войдите на https://my.telegram.org",
                "2. Перейдите в 'API development tools'",
                "3. Создайте приложение",
                "4. Скопируйте API_ID и API_HASH"
            ],
            "example": {
                "TELEGRAM_API_ID": "12345678",
                "TELEGRAM_API_HASH": "0123456789abcdef0123456789abcdef"
            }
        }
    
    @staticmethod
    def get_gemini_api_key() -> Dict[str, str]:
        """
        Получение Google Gemini API ключа (БЕСПЛАТНО!)
        
        Шаги:
        1. Перейдите на https://makersuite.google.com/app/apikey
        2. Войдите с Google аккаунтом
        3. Нажмите "Create API Key"
        4. Выберите существующий проект или создайте новый
        5. Скопируйте API ключ
        
        Лимиты бесплатного плана:
        - 60 запросов в минуту
        - 1500 запросов в день
        - Бесплатно навсегда!
        
        Returns:
            Dict с инструкциями
        """
        return {
            "url": "https://makersuite.google.com/app/apikey",
            "steps": [
                "1. Войдите на https://makersuite.google.com/app/apikey",
                "2. Нажмите 'Create API Key'",
                "3. Выберите проект",
                "4. Скопируйте ключ"
            ],
            "limits": {
                "requests_per_minute": 60,
                "requests_per_day": 1500,
                "cost": "FREE"
            },
            "example": {
                "GEMINI_API_KEY": "AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY"
            }
        }
    
    @staticmethod
    def get_groq_api_key() -> Dict[str, str]:
        """
        Получение Groq API ключа (БЕСПЛАТНО!)
        
        Шаги:
        1. Перейдите на https://console.groq.com
        2. Зарегистрируйтесь или войдите
        3. Перейдите в раздел "API Keys"
        4. Нажмите "Create API Key"
        5. Скопируйте ключ
        
        Лимиты бесплатного плана:
        - 30 запросов в минуту
        - Очень быстрая обработка (LPU inference)
        - Бесплатно!
        
        Returns:
            Dict с инструкциями
        """
        return {
            "url": "https://console.groq.com",
            "steps": [
                "1. Войдите на https://console.groq.com",
                "2. Перейдите в 'API Keys'",
                "3. Нажмите 'Create API Key'",
                "4. Скопируйте ключ"
            ],
            "limits": {
                "requests_per_minute": 30,
                "speed": "Very Fast (LPU)",
                "cost": "FREE"
            },
            "example": {
                "GROQ_API_KEY": "gsk_1234567890abcdefghijklmnopqrstuv"
            }
        }
    
    @staticmethod
    def get_huggingface_token() -> Dict[str, str]:
        """
        Получение Hugging Face токена (ОПЦИОНАЛЬНО, БЕСПЛАТНО!)
        
        Шаги:
        1. Перейдите на https://huggingface.co/settings/tokens
        2. Зарегистрируйтесь или войдите
        3. Нажмите "New token"
        4. Выберите тип "Read"
        5. Скопируйте токен
        
        Returns:
            Dict с инструкциями
        """
        return {
            "url": "https://huggingface.co/settings/tokens",
            "steps": [
                "1. Войдите на https://huggingface.co/settings/tokens",
                "2. Нажмите 'New token'",
                "3. Выберите тип 'Read'",
                "4. Скопируйте токен"
            ],
            "optional": True,
            "example": {
                "HUGGINGFACE_TOKEN": "hf_1234567890abcdefghijklmnopqrstuv"
            }
        }
    
    @staticmethod
    def print_all_guides():
        """Вывести все инструкции по получению API ключей"""
        print("=" * 80)
        print("📚 РУКОВОДСТВО ПО ПОЛУЧЕНИЮ API КЛЮЧЕЙ")
        print("=" * 80)
        
        # Telegram API
        print("\n🔵 1. TELEGRAM API (ОБЯЗАТЕЛЬНО)")
        print("-" * 80)
        telegram = APIKeysGuide.get_telegram_api_credentials()
        print(f"URL: {telegram['url']}")
        for step in telegram['steps']:
            print(f"  {step}")
        print(f"\nПример:")
        for key, value in telegram['example'].items():
            print(f"  {key}={value}")
        
        # Gemini API
        print("\n🟢 2. GOOGLE GEMINI API (РЕКОМЕНДУЕТСЯ - БЕСПЛАТНО)")
        print("-" * 80)
        gemini = APIKeysGuide.get_gemini_api_key()
        print(f"URL: {gemini['url']}")
        for step in gemini['steps']:
            print(f"  {step}")
        print(f"\nЛимиты:")
        for key, value in gemini['limits'].items():
            print(f"  {key}: {value}")
        print(f"\nПример:")
        for key, value in gemini['example'].items():
            print(f"  {key}={value}")
        
        # Groq API
        print("\n🟣 3. GROQ API (РЕКОМЕНДУЕТСЯ - БЕСПЛАТНО)")
        print("-" * 80)
        groq = APIKeysGuide.get_groq_api_key()
        print(f"URL: {groq['url']}")
        for step in groq['steps']:
            print(f"  {step}")
        print(f"\nЛимиты:")
        for key, value in groq['limits'].items():
            print(f"  {key}: {value}")
        print(f"\nПример:")
        for key, value in groq['example'].items():
            print(f"  {key}={value}")
        
        # Hugging Face
        print("\n🟡 4. HUGGING FACE TOKEN (ОПЦИОНАЛЬНО)")
        print("-" * 80)
        hf = APIKeysGuide.get_huggingface_token()
        print(f"URL: {hf['url']}")
        for step in hf['steps']:
            print(f"  {step}")
        print(f"\nПример:")
        for key, value in hf['example'].items():
            print(f"  {key}={value}")
        
        print("\n" + "=" * 80)
        print("✅ После получения всех ключей, введите их в Setup Wizard")
        print("=" * 80)


class EnvManager:
    """Менеджер для работы с .env файлом"""
    
    def __init__(self, env_path: str = ".env"):
        self.env_path = env_path
        self.env_vars = {}
        self.load()
    
    def load(self):
        """Загрузить переменные из .env файла"""
        if os.path.exists(self.env_path):
            with open(self.env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.env_vars[key.strip()] = value.strip()
    
    def set(self, key: str, value: str):
        """Установить переменную окружения"""
        self.env_vars[key] = value
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Получить переменную окружения"""
        return self.env_vars.get(key, default)
    
    def save(self):
        """Сохранить переменные в .env файл"""
        with open(self.env_path, 'w', encoding='utf-8') as f:
            f.write("# Alfa Campaign Manager - Environment Variables\n")
            f.write("# Generated by Setup Wizard\n\n")
            
            # Telegram
            f.write("# Telegram API Credentials\n")
            f.write(f"TELEGRAM_API_ID={self.env_vars.get('TELEGRAM_API_ID', '')}\n")
            f.write(f"TELEGRAM_API_HASH={self.env_vars.get('TELEGRAM_API_HASH', '')}\n")
            f.write(f"TELEGRAM_PHONE_NUMBER={self.env_vars.get('TELEGRAM_PHONE_NUMBER', '')}\n")
            f.write(f"TELEGRAM_BOT_TOKEN={self.env_vars.get('TELEGRAM_BOT_TOKEN', '')}\n\n")
            
            # AI APIs
            f.write("# AI API Keys (at least one required)\n")
            f.write(f"GEMINI_API_KEY={self.env_vars.get('GEMINI_API_KEY', '')}\n")
            f.write(f"GROQ_API_KEY={self.env_vars.get('GROQ_API_KEY', '')}\n")
            f.write(f"HUGGINGFACE_TOKEN={self.env_vars.get('HUGGINGFACE_TOKEN', '')}\n\n")
            
            # Database
            f.write("# Database\n")
            f.write(f"DATABASE_URL={self.env_vars.get('DATABASE_URL', 'sqlite:///./alfa.db')}\n\n")
            
            # Other
            f.write("# Other Settings\n")
            f.write(f"SESSION_FILE={self.env_vars.get('SESSION_FILE', 'session.session')}\n")
    
    def validate(self) -> Dict[str, bool]:
        """Проверить наличие всех необходимых переменных"""
        required = {
            'TELEGRAM_API_ID': False,
            'TELEGRAM_API_HASH': False,
            'TELEGRAM_PHONE_NUMBER': False,
        }
        
        optional = {
            'TELEGRAM_BOT_TOKEN': False,
            'GEMINI_API_KEY': False,
            'GROQ_API_KEY': False,
            'HUGGINGFACE_TOKEN': False,
        }
        
        # Проверка обязательных
        for key in required.keys():
            required[key] = bool(self.env_vars.get(key))
        
        # Проверка опциональных
        for key in optional.keys():
            optional[key] = bool(self.env_vars.get(key))
        
        # Хотя бы один AI API ключ должен быть
        has_ai_key = optional['GEMINI_API_KEY'] or optional['GROQ_API_KEY']
        
        return {
            'required': required,
            'optional': optional,
            'has_ai_key': has_ai_key,
            'is_valid': all(required.values()) and has_ai_key
        }
    
    def print_status(self):
        """Вывести статус конфигурации"""
        validation = self.validate()
        
        print("=" * 80)
        print("📊 СТАТУС КОНФИГУРАЦИИ")
        print("=" * 80)
        
        print("\n✅ Обязательные переменные:")
        for key, value in validation['required'].items():
            status = "✓" if value else "✗"
            print(f"  [{status}] {key}")
        
        print("\n🔧 Опциональные переменные:")
        for key, value in validation['optional'].items():
            status = "✓" if value else "✗"
            print(f"  [{status}] {key}")
        
        print("\n" + "=" * 80)
        if validation['is_valid']:
            print("✅ Конфигурация ВАЛИДНА - можно запускать проект!")
        else:
            print("❌ Конфигурация НЕВАЛИДНА - заполните недостающие переменные")
            if not validation['has_ai_key']:
                print("⚠️  Необходим хотя бы один AI API ключ (Gemini или Groq)")
        print("=" * 80)


if __name__ == "__main__":
    # Вывести руководство
    APIKeysGuide.print_all_guides()
    
    print("\n\n")
    
    # Проверить текущую конфигурацию
    env_manager = EnvManager()
    env_manager.print_status()

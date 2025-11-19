"""
Setup API - API endpoints для Setup UI
Обрабатывает запросы от веб-интерфейса настройки
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import os
from api_keys_guide import EnvManager

router = APIRouter(prefix="/api/config", tags=["config"])

# Pydantic модели
class EnvConfig(BaseModel):
    """Модель конфигурации окружения"""
    TELEGRAM_API_ID: str
    TELEGRAM_API_HASH: str
    TELEGRAM_PHONE_NUMBER: str
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    HUGGINGFACE_TOKEN: Optional[str] = None
    DATABASE_URL: str = "sqlite:///./alfa.db"


class ValidationResult(BaseModel):
    """Результат валидации конфигурации"""
    required: Dict[str, bool]
    optional: Dict[str, bool]
    has_ai_key: bool
    is_valid: bool


@router.get("/")
async def get_config() -> EnvConfig:
    """
    Получить текущую конфигурацию
    
    Returns:
        EnvConfig: Текущая конфигурация (без секретных данных)
    """
    env_manager = EnvManager()
    
    # Маскировать секретные данные
    def mask_secret(value: Optional[str]) -> str:
        if not value:
            return ""
        if len(value) > 8:
            return value[:8] + "..." + value[-4:]
        return "***"
    
    return EnvConfig(
        TELEGRAM_API_ID=env_manager.get('TELEGRAM_API_ID', ''),
        TELEGRAM_API_HASH=mask_secret(env_manager.get('TELEGRAM_API_HASH')),
        TELEGRAM_PHONE_NUMBER=env_manager.get('TELEGRAM_PHONE_NUMBER', ''),
        TELEGRAM_BOT_TOKEN=mask_secret(env_manager.get('TELEGRAM_BOT_TOKEN')),
        GEMINI_API_KEY=mask_secret(env_manager.get('GEMINI_API_KEY')),
        GROQ_API_KEY=mask_secret(env_manager.get('GROQ_API_KEY')),
        HUGGINGFACE_TOKEN=mask_secret(env_manager.get('HUGGINGFACE_TOKEN')),
        DATABASE_URL=env_manager.get('DATABASE_URL', 'sqlite:///./alfa.db')
    )


@router.post("/validate")
async def validate_config(config: EnvConfig) -> ValidationResult:
    """
    Валидировать конфигурацию
    
    Args:
        config: Конфигурация для валидации
    
    Returns:
        ValidationResult: Результат валидации
    """
    # Проверка обязательных полей
    required = {
        'TELEGRAM_API_ID': bool(config.TELEGRAM_API_ID),
        'TELEGRAM_API_HASH': bool(config.TELEGRAM_API_HASH),
        'TELEGRAM_PHONE_NUMBER': bool(config.TELEGRAM_PHONE_NUMBER),
    }
    
    # Проверка опциональных полей
    optional = {
        'TELEGRAM_BOT_TOKEN': bool(config.TELEGRAM_BOT_TOKEN),
        'GEMINI_API_KEY': bool(config.GEMINI_API_KEY),
        'GROQ_API_KEY': bool(config.GROQ_API_KEY),
        'HUGGINGFACE_TOKEN': bool(config.HUGGINGFACE_TOKEN),
    }
    
    # Хотя бы один AI API ключ должен быть
    has_ai_key = bool(config.GEMINI_API_KEY) or bool(config.GROQ_API_KEY)
    
    # Общая валидность
    is_valid = all(required.values()) and has_ai_key
    
    return ValidationResult(
        required=required,
        optional=optional,
        has_ai_key=has_ai_key,
        is_valid=is_valid
    )


@router.post("/save")
async def save_config(config: EnvConfig) -> Dict[str, str]:
    """
    Сохранить конфигурацию в .env файл
    
    Args:
        config: Конфигурация для сохранения
    
    Returns:
        Dict: Статус сохранения
    
    Raises:
        HTTPException: Если конфигурация невалидна
    """
    # Валидация
    validation = await validate_config(config)
    
    if not validation.is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid configuration. Check required fields and AI API keys."
        )
    
    # Сохранение
    env_manager = EnvManager()
    
    env_manager.set('TELEGRAM_API_ID', config.TELEGRAM_API_ID)
    env_manager.set('TELEGRAM_API_HASH', config.TELEGRAM_API_HASH)
    env_manager.set('TELEGRAM_PHONE_NUMBER', config.TELEGRAM_PHONE_NUMBER)
    
    if config.TELEGRAM_BOT_TOKEN:
        env_manager.set('TELEGRAM_BOT_TOKEN', config.TELEGRAM_BOT_TOKEN)
    
    if config.GEMINI_API_KEY:
        env_manager.set('GEMINI_API_KEY', config.GEMINI_API_KEY)
    
    if config.GROQ_API_KEY:
        env_manager.set('GROQ_API_KEY', config.GROQ_API_KEY)
    
    if config.HUGGINGFACE_TOKEN:
        env_manager.set('HUGGINGFACE_TOKEN', config.HUGGINGFACE_TOKEN)
    
    env_manager.set('DATABASE_URL', config.DATABASE_URL)
    
    # Сохранить в файл
    env_manager.save()
    
    return {
        "status": "success",
        "message": "Configuration saved successfully"
    }


@router.get("/status")
async def get_status() -> Dict:
    """
    Получить статус конфигурации
    
    Returns:
        Dict: Статус конфигурации
    """
    env_manager = EnvManager()
    validation = env_manager.validate()
    
    return {
        "is_configured": validation['is_valid'],
        "required_fields": validation['required'],
        "optional_fields": validation['optional'],
        "has_ai_key": validation['has_ai_key'],
    }


@router.get("/guides")
async def get_guides() -> Dict:
    """
    Получить руководства по получению API ключей
    
    Returns:
        Dict: Руководства для всех API
    """
    from api_keys_guide import APIKeysGuide
    
    return {
        "telegram": APIKeysGuide.get_telegram_api_credentials(),
        "gemini": APIKeysGuide.get_gemini_api_key(),
        "groq": APIKeysGuide.get_groq_api_key(),
        "huggingface": APIKeysGuide.get_huggingface_token(),
    }


@router.post("/test-telegram")
async def test_telegram_connection(config: EnvConfig) -> Dict:
    """
    Тестировать подключение к Telegram API
    
    Args:
        config: Конфигурация для тестирования
    
    Returns:
        Dict: Результат теста
    """
    try:
        from telethon import TelegramClient
        
        client = TelegramClient(
            'test_session',
            int(config.TELEGRAM_API_ID),
            config.TELEGRAM_API_HASH
        )
        
        await client.connect()
        
        if await client.is_user_authorized():
            await client.disconnect()
            return {
                "status": "success",
                "message": "Telegram connection successful",
                "authorized": True
            }
        else:
            await client.disconnect()
            return {
                "status": "success",
                "message": "Telegram connection successful, but not authorized",
                "authorized": False
            }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Telegram connection failed: {str(e)}",
            "authorized": False
        }


@router.post("/test-ai")
async def test_ai_connection(config: EnvConfig) -> Dict:
    """
    Тестировать подключение к AI API
    
    Args:
        config: Конфигурация для тестирования
    
    Returns:
        Dict: Результат теста
    """
    results = {}
    
    # Тест Gemini
    if config.GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Test")
            results['gemini'] = {
                "status": "success",
                "message": "Gemini API connection successful"
            }
        except Exception as e:
            results['gemini'] = {
                "status": "error",
                "message": f"Gemini API connection failed: {str(e)}"
            }
    
    # Тест Groq
    if config.GROQ_API_KEY:
        try:
            from groq import Groq
            client = Groq(api_key=config.GROQ_API_KEY)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Test"}],
                model="mixtral-8x7b-32768",
                max_tokens=10
            )
            results['groq'] = {
                "status": "success",
                "message": "Groq API connection successful"
            }
        except Exception as e:
            results['groq'] = {
                "status": "error",
                "message": f"Groq API connection failed: {str(e)}"
            }
    
    return results

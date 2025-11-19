"""
Free LLM Service - Интеграция бесплатных ИИ API
Поддержка: Google Gemini, Groq, Ollama, Hugging Face
"""
import logging
import asyncio
from typing import Optional, List, Dict, Any
from enum import Enum
import os
import aiohttp

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Поддерживаемые провайдеры ИИ"""
    GEMINI = "gemini"
    GROQ = "groq"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"


class FreeLLMService:
    """
    Сервис для работы с бесплатными ИИ API
    Автоматически переключается между провайдерами при ошибках
    """

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        
        self.primary_provider = LLMProvider.GEMINI
        self.fallback_providers = [
            LLMProvider.GROQ,
            LLMProvider.OLLAMA,
            LLMProvider.HUGGINGFACE,
        ]

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> str:
        """
        Генерировать ответ от ИИ
        Автоматически переключается между провайдерами при ошибках
        """
        providers_to_try = [self.primary_provider] + self.fallback_providers

        for provider in providers_to_try:
            try:
                if provider == LLMProvider.GEMINI:
                    return await self._gemini_generate(
                        prompt, system_prompt, max_tokens, temperature
                    )
                elif provider == LLMProvider.GROQ:
                    return await self._groq_generate(
                        prompt, system_prompt, max_tokens, temperature
                    )
                elif provider == LLMProvider.OLLAMA:
                    return await self._ollama_generate(
                        prompt, system_prompt, max_tokens, temperature
                    )
                elif provider == LLMProvider.HUGGINGFACE:
                    return await self._huggingface_generate(
                        prompt, system_prompt, max_tokens, temperature
                    )
            except Exception as e:
                logger.warning(f"⚠️ {provider.value} не работает: {e}")
                continue

        logger.error("❌ Все провайдеры ИИ недоступны")
        return "Извините, сейчас я не могу ответить. Попробуйте позже."

    async def _gemini_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> str:
        """Google Gemini API (БЕСПЛАТНО - 60 запросов в минуту)"""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY не установлен")

        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_api_key)

            model = genai.GenerativeModel("gemini-2.5-flash")
            
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                ),
            )

            logger.info("✅ Gemini API успешно использован")
            return response.text

        except Exception as e:
            logger.error(f"❌ Ошибка Gemini: {e}")
            raise

    async def _groq_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> str:
        """Groq API (БЕСПЛАТНО - очень быстро)"""
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY не установлен")

        try:
            from groq import Groq

            client = Groq(api_key=self.groq_api_key)

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Или llama-3.1-70b-versatile
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            logger.info("✅ Groq API успешно использован")
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"❌ Ошибка Groq: {e}")
            raise

    async def _ollama_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> str:
        """Ollama (ПОЛНОСТЬЮ БЕСПЛАТНО - локально на компьютере)"""
        try:
            import requests

            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "mistral",  # Или llama2, neural-chat
                    "prompt": full_prompt,
                    "stream": False,
                    "temperature": temperature,
                },
                timeout=30,
            )

            if response.status_code == 200:
                logger.info("✅ Ollama успешно использован")
                return response.json()["response"]
            else:
                raise Exception(f"Ollama ошибка: {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Ошибка Ollama: {e}")
            raise

    async def _huggingface_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> str:
        """Hugging Face Inference API (БЕСПЛАТНО - 1000+ моделей)"""
        if not self.huggingface_api_key:
            raise ValueError("HUGGINGFACE_API_KEY не установлен")

        try:
            from huggingface_hub import InferenceClient

            client = InferenceClient(api_key=self.huggingface_api_key)

            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

            response = client.text_generation(
                full_prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
            )

            logger.info("✅ Hugging Face успешно использован")
            return response

        except Exception as e:
            logger.error(f"❌ Ошибка Hugging Face: {e}")
            raise

    async def generate_product_recommendation(
        self,
        user_profile: Dict[str, Any],
        available_products: List[Dict[str, Any]],
    ) -> str:
        """
        Генерировать персонализированную рекомендацию продукта
        """
        system_prompt = """Ты - опытный финансовый консультант Альфа Банка.
Твоя задача - рекомендовать наиболее подходящий продукт клиенту на основе его профиля.
Будь дружелюбным, профессиональным и убедительным.
Используй техники НЛП для повышения конверсии.
Ответ должен быть кратким (2-3 предложения) и содержать прямую рекомендацию."""

        products_info = "\n".join(
            [f"- {p['name']}: {p['description']} ({p['points']} баллов)" 
             for p in available_products]
        )

        prompt = f"""Профиль клиента:
- Имя: {user_profile.get('name', 'Клиент')}
- Возраст: {user_profile.get('age', 'не указан')}
- Цель: {user_profile.get('goal', 'не указана')}
- Доход: {user_profile.get('income', 'не указан')}

Доступные продукты:
{products_info}

Какой продукт рекомендовать этому клиенту? Почему именно этот?"""

        return await self.generate_response(prompt, system_prompt, max_tokens=200)

    async def generate_objection_handling(
        self,
        objection: str,
        product_name: str,
    ) -> str:
        """
        Генерировать ответ на возражение клиента
        """
        system_prompt = """Ты - опытный продавец финансовых услуг.
Твоя задача - профессионально и убедительно ответить на возражение клиента.
Используй техники НЛП и эмпатию.
Ответ должен быть кратким (2-3 предложения) и содержать решение проблемы."""

        prompt = f"""Продукт: {product_name}
Возражение клиента: {objection}

Как ты ответишь на это возражение? Дай убедительный ответ."""

        return await self.generate_response(prompt, system_prompt, max_tokens=200)

    async def generate_conversation_starter(
        self,
        contact_name: str,
        contact_profile: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Генерировать начало диалога для инициирования контакта
        """
        system_prompt = """Ты - дружелюбный консультант Альфа Банка.
Твоя задача - начать естественный и интересный диалог с потенциальным клиентом.
Будь персональным, теплым и не навязчивым.
Первое сообщение должно быть кратким (1-2 предложения) и вызывать интерес."""

        profile_info = ""
        if contact_profile:
            profile_info = f"""Информация о контакте:
- Профессия: {contact_profile.get('profession', 'не указана')}
- Интересы: {contact_profile.get('interests', 'не указаны')}
- Статус: {contact_profile.get('status', 'не указан')}
"""

        prompt = f"""Имя контакта: {contact_name}
{profile_info}

Напиши первое сообщение для начала диалога. Сделай его личным и интересным."""

        return await self.generate_response(prompt, system_prompt, max_tokens=150)


# Глобальный экземпляр
_service: Optional[FreeLLMService] = None


def get_free_llm_service() -> FreeLLMService:
    """Получить или создать экземпляр сервиса"""
    global _service
    if _service is None:
        _service = FreeLLMService()
    return _service

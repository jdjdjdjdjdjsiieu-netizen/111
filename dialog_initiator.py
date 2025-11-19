"""
Dialog Initiator - Модуль для автоматической инициации диалогов
Бот сам начинает общение с контактами умным и естественным способом
"""
import logging
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Contact, Campaign, CampaignContact, MessageStatus
from free_llm_service import get_free_llm_service
from knowledge_base import get_knowledge_base
from telethon_service import TelethonService
import random

logger = logging.getLogger(__name__)


class DialogInitiator:
    """
    Инициирует диалоги с контактами умным способом
    Анализирует профиль контакта и генерирует персональное первое сообщение
    """

    def __init__(self, db: Session, telethon_service: TelethonService):
        self.db = db
        self.telethon_service = telethon_service
        self.llm_service = get_free_llm_service()
        self.knowledge_base = get_knowledge_base(db)
        
        # Интервалы между сообщениями для соблюдения политики Telegram
        self.min_interval = 2  # минимум 2 секунды между сообщениями
        self.max_interval = 5  # максимум 5 секунд
        self.pause_after_batch = 30  # пауза после 10 сообщений (30 сек)

    async def initiate_smart_dialog(self, contact: Contact) -> bool:
        """
        Инициировать умный диалог с контактом
        Генерирует персональное первое сообщение на основе профиля
        """
        try:
            logger.info(f"🤖 Инициирую диалог с {contact.name} ({contact.phone})")

            # Подготовить профиль контакта
            contact_profile = {
                "name": contact.name,
                "phone": contact.phone,
                "profession": contact.profession or "не указана",
                "interests": contact.interests or "не указаны",
                "status": "активный" if contact.is_active else "неактивный",
            }

            # Генерировать первое сообщение через ИИ
            opening_message = await self.llm_service.generate_conversation_starter(
                contact.name,
                contact_profile,
            )

            logger.info(f"💬 Сгенерировано сообщение: {opening_message}")

            # Отправить сообщение через Telethon
            success = await self.telethon_service.send_message(
                contact.phone,
                opening_message,
            )

            if success:
                # Сохранить в БД
                contact.last_contacted = datetime.utcnow()
                contact.is_active = True
                self.db.commit()
                logger.info(f"✅ Диалог инициирован с {contact.name}")
                return True
            else:
                logger.warning(f"⚠️ Не удалось отправить сообщение {contact.name}")
                return False

        except Exception as e:
            logger.error(f"❌ Ошибка при инициации диалога: {e}")
            return False

    async def initiate_batch_dialogs(
        self,
        contacts: List[Contact],
        delay_between_messages: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Инициировать диалоги с несколькими контактами
        С соблюдением лимитов Telegram
        """
        if not delay_between_messages:
            delay_between_messages = random.randint(
                self.min_interval, self.max_interval
            )

        results = {
            "total": len(contacts),
            "successful": 0,
            "failed": 0,
            "skipped": 0,
        }

        for idx, contact in enumerate(contacts):
            try:
                # Проверить, не был ли контакт недавно инициирован
                if contact.last_contacted:
                    hours_ago = (datetime.utcnow() - contact.last_contacted).total_seconds() / 3600
                    if hours_ago < 24:
                        logger.info(f"⏭️ Пропускаю {contact.name} (контактировался {hours_ago:.1f} часов назад)")
                        results["skipped"] += 1
                        continue

                # Инициировать диалог
                success = await self.initiate_smart_dialog(contact)
                if success:
                    results["successful"] += 1
                else:
                    results["failed"] += 1

                # Пауза между сообщениями
                if (idx + 1) % 10 == 0:
                    logger.info(f"⏸️ Пауза после {idx + 1} сообщений...")
                    await asyncio.sleep(self.pause_after_batch)
                else:
                    await asyncio.sleep(delay_between_messages)

            except Exception as e:
                logger.error(f"❌ Ошибка при обработке {contact.name}: {e}")
                results["failed"] += 1

        logger.info(f"📊 Результаты инициации диалогов: {results}")
        return results

    async def initiate_campaign_dialogs(
        self,
        campaign_id: int,
        batch_size: int = 10,
    ) -> Dict[str, Any]:
        """
        Инициировать диалоги для кампании
        """
        try:
            campaign = self.db.query(Campaign).filter_by(id=campaign_id).first()
            if not campaign:
                logger.error(f"❌ Кампания {campaign_id} не найдена")
                return {"error": "Campaign not found"}

            # Получить контакты кампании
            campaign_contacts = (
                self.db.query(Contact)
                .join(CampaignContact)
                .filter(CampaignContact.campaign_id == campaign_id)
                .filter(CampaignContact.status == MessageStatus.PENDING)
                .all()
            )

            logger.info(f"🎯 Инициирую диалоги для кампании {campaign.name}")
            logger.info(f"📋 Всего контактов: {len(campaign_contacts)}")

            # Инициировать диалоги батчами
            results = {
                "campaign_id": campaign_id,
                "total_batches": (len(campaign_contacts) + batch_size - 1) // batch_size,
                "batches": [],
            }

            for i in range(0, len(campaign_contacts), batch_size):
                batch = campaign_contacts[i : i + batch_size]
                batch_result = await self.initiate_batch_dialogs(batch)
                results["batches"].append(batch_result)

                # Пауза между батчами
                if i + batch_size < len(campaign_contacts):
                    logger.info(f"⏸️ Пауза между батчами (60 сек)...")
                    await asyncio.sleep(60)

            return results

        except Exception as e:
            logger.error(f"❌ Ошибка при инициации кампании: {e}")
            return {"error": str(e)}

    async def initiate_smart_follow_up(self, contact: Contact) -> bool:
        """
        Умное follow-up сообщение на основе истории общения
        """
        try:
            # Получить последние сообщения
            from telethon_service import TelethonService
            
            messages = await self.telethon_service.get_message_history(
                contact.phone,
                limit=5,
            )

            if not messages:
                logger.warning(f"⚠️ Нет истории сообщений с {contact.name}")
                return False

            # Анализировать последнее сообщение
            last_message = messages[0]
            
            # Генерировать follow-up на основе контекста
            system_prompt = """Ты - дружелюбный консультант Альфа Банка.
Твоя задача - написать естественное follow-up сообщение на основе предыдущего общения.
Будь персональным и не навязчивым.
Сообщение должно быть кратким (1-2 предложения)."""

            prompt = f"""Последнее сообщение от клиента: {last_message}

Напиши follow-up сообщение, которое продолжит диалог естественно."""

            follow_up_message = await self.llm_service.generate_response(
                prompt,
                system_prompt,
                max_tokens=150,
            )

            # Отправить follow-up
            success = await self.telethon_service.send_message(
                contact.phone,
                follow_up_message,
            )

            if success:
                logger.info(f"✅ Follow-up отправлен {contact.name}")
                return True
            else:
                logger.warning(f"⚠️ Не удалось отправить follow-up {contact.name}")
                return False

        except Exception as e:
            logger.error(f"❌ Ошибка при follow-up: {e}")
            return False

    def get_contacts_for_initiation(
        self,
        min_days_since_contact: int = 1,
        limit: int = 50,
    ) -> List[Contact]:
        """
        Получить контакты для инициации диалогов
        Фильтр: не контактировались более N дней назад
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=min_days_since_contact)

            contacts = (
                self.db.query(Contact)
                .filter(
                    (Contact.last_contacted == None)  # Никогда не контактировались
                    | (Contact.last_contacted < cutoff_date)  # Давно не контактировались
                )
                .filter(Contact.is_active == True)
                .limit(limit)
                .all()
            )

            logger.info(f"📋 Найдено {len(contacts)} контактов для инициации")
            return contacts

        except Exception as e:
            logger.error(f"❌ Ошибка при получении контактов: {e}")
            return []


def get_dialog_initiator(db: Session, telethon_service: TelethonService) -> DialogInitiator:
    """Получить экземпляр DialogInitiator"""
    return DialogInitiator(db, telethon_service)

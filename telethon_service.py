"""
Telethon Service для работы с Telegram API
Парсинг контактов, групп, каналов и отправка сообщений
"""
import asyncio
import logging
from typing import List, Optional, Dict, Any
from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel, PeerUser, PeerChat, PeerChannel
from telethon.errors import FloodWaitError, PeerIdInvalidError

logger = logging.getLogger(__name__)

class TelethonService:
    def __init__(self, api_id: int, api_hash: str, phone: str, session_name: str = "admin_session"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.session_name = session_name
        self.client: Optional[TelegramClient] = None
        self.is_connected = False

    async def connect(self) -> bool:
        """Подключение к Telegram"""
        try:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
            await self.client.start(phone=self.phone)
            self.is_connected = True
            logger.info(f"Подключено к Telegram: {await self.client.get_me()}")
            return True
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            return False

    async def disconnect(self):
        """Отключение от Telegram"""
        if self.client:
            await self.client.disconnect()
            self.is_connected = False

    async def get_contacts(self) -> List[Dict[str, Any]]:
        """Получить список контактов"""
        if not self.client or not self.is_connected:
            logger.warning("Клиент не подключен")
            return []

        try:
            contacts = []
            async for dialog in self.client.iter_dialogs():
                if isinstance(dialog.entity, User):
                    contacts.append({
                        "id": dialog.entity.id,
                        "first_name": dialog.entity.first_name or "",
                        "last_name": dialog.entity.last_name or "",
                        "username": dialog.entity.username or "",
                        "phone": dialog.entity.phone or "",
                        "is_bot": dialog.entity.bot,
                        "type": "user",
                        "last_message_date": dialog.date,
                    })
            logger.info(f"Получено {len(contacts)} контактов")
            return contacts
        except Exception as e:
            logger.error(f"Ошибка при получении контактов: {e}")
            return []

    async def get_groups_and_channels(self) -> Dict[str, List[Dict[str, Any]]]:
        """Получить список групп и каналов"""
        if not self.client or not self.is_connected:
            logger.warning("Клиент не подключен")
            return {"groups": [], "channels": []}

        try:
            groups = []
            channels = []

            async for dialog in self.client.iter_dialogs():
                if isinstance(dialog.entity, (Chat, Channel)):
                    chat_data = {
                        "id": dialog.entity.id,
                        "title": dialog.entity.title or "",
                        "type": "channel" if isinstance(dialog.entity, Channel) else "group",
                        "participants_count": getattr(dialog.entity, "participants_count", 0),
                        "description": getattr(dialog.entity, "about", ""),
                        "username": getattr(dialog.entity, "username", ""),
                    }

                    if isinstance(dialog.entity, Channel):
                        channels.append(chat_data)
                    else:
                        groups.append(chat_data)

            logger.info(f"Получено {len(groups)} групп и {len(channels)} каналов")
            return {"groups": groups, "channels": channels}
        except Exception as e:
            logger.error(f"Ошибка при получении групп/каналов: {e}")
            return {"groups": [], "channels": []}

    async def get_group_members(self, group_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Получить участников группы"""
        if not self.client or not self.is_connected:
            logger.warning("Клиент не подключен")
            return []

        try:
            members = []
            async for user in self.client.iter_participants(group_id, limit=limit):
                members.append({
                    "id": user.id,
                    "first_name": user.first_name or "",
                    "last_name": user.last_name or "",
                    "username": user.username or "",
                    "phone": user.phone or "",
                    "is_bot": user.bot,
                })
            logger.info(f"Получено {len(members)} участников группы {group_id}")
            return members
        except Exception as e:
            logger.error(f"Ошибка при получении участников группы: {e}")
            return []

    async def send_message(
        self,
        user_id: int,
        message: str,
        delay: float = 2.0
    ) -> bool:
        """
        Отправить сообщение пользователю
        delay - задержка в секундах для соблюдения политики Telegram
        """
        if not self.client or not self.is_connected:
            logger.warning("Клиент не подключен")
            return False

        try:
            await asyncio.sleep(delay)  # Задержка для предотвращения блокировки
            await self.client.send_message(user_id, message)
            logger.info(f"Сообщение отправлено пользователю {user_id}")
            return True
        except FloodWaitError as e:
            logger.warning(f"Flood wait: нужно ждать {e.seconds} секунд")
            await asyncio.sleep(e.seconds)
            return await self.send_message(user_id, message, delay)
        except PeerIdInvalidError:
            logger.error(f"Невалидный ID пользователя: {user_id}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            return False

    async def send_messages_batch(
        self,
        user_ids: List[int],
        message: str,
        delay: float = 3.0,
        batch_delay: float = 60.0
    ) -> Dict[str, int]:
        """
        Отправить сообщения пакетом с задержками
        delay - задержка между сообщениями
        batch_delay - задержка между пакетами (каждые 10 сообщений)
        """
        if not self.client or not self.is_connected:
            logger.warning("Клиент не подключен")
            return {"sent": 0, "failed": 0}

        sent = 0
        failed = 0

        for idx, user_id in enumerate(user_ids):
            try:
                success = await self.send_message(user_id, message, delay)
                if success:
                    sent += 1
                else:
                    failed += 1

                # Пауза после каждых 10 сообщений
                if (idx + 1) % 10 == 0:
                    logger.info(f"Отправлено {sent}, ошибок {failed}. Пауза {batch_delay}с...")
                    await asyncio.sleep(batch_delay)

            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
                failed += 1

        logger.info(f"Рассылка завершена. Отправлено: {sent}, Ошибок: {failed}")
        return {"sent": sent, "failed": failed}

    async def get_message_history(
        self,
        user_id: int,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Получить историю сообщений с пользователем"""
        if not self.client or not self.is_connected:
            logger.warning("Клиент не подключен")
            return []

        try:
            messages = []
            async for msg in self.client.iter_messages(user_id, limit=limit):
                messages.append({
                    "id": msg.id,
                    "text": msg.text or "",
                    "date": msg.date.isoformat() if msg.date else "",
                    "from_id": msg.sender_id,
                    "is_out": msg.is_out,  # True если исходящее, False если входящее
                })
            logger.info(f"Получено {len(messages)} сообщений с пользователем {user_id}")
            return messages
        except Exception as e:
            logger.error(f"Ошибка при получении истории: {e}")
            return []


# Глобальный экземпляр сервиса
_telethon_service: Optional[TelethonService] = None


def get_telethon_service(api_id: int, api_hash: str, phone: str) -> TelethonService:
    """Получить или создать экземпляр TelethonService"""
    global _telethon_service
    if _telethon_service is None:
        _telethon_service = TelethonService(api_id, api_hash, phone)
    return _telethon_service

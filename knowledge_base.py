"""
Knowledge Base Module для Alfa Bot
Парсинг данных о программе, продуктах и структуре партнера
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models import Contact, Group, Campaign, CampaignContact, MessageStatus
import json

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """
    База знаний для бота
    Содержит информацию о программе "Свой в Альфе", продуктах и стратегии
    """

    def __init__(self, db: Session):
        self.db = db
        self.program_info = {}
        self.products = []
        self.partner_structure = {}
        self.campaign_stats = {}
        self.last_updated = None

    def load_program_info(self) -> Dict[str, Any]:
        """Загрузить информацию о программе из внешних источников или БД"""
        self.program_info = {
            "name": "Свой в Альфе",
            "bank": "Альфа Банк",
            "description": "Партнерская программа для рекомендации финансовых продуктов",
            "commission_levels": {
                "A1": {"min_points": 0, "max_points": 999, "bonus": 0},
                "A2": {"min_points": 1000, "max_points": 4999, "bonus": 50000},
                "A3": {"min_points": 5000, "max_points": 9999, "bonus": 100000},
                "A4": {"min_points": 10000, "max_points": 19999, "bonus": 250000},
                "A5": {"min_points": 20000, "max_points": 49999, "bonus": 500000},
                "A6": {"min_points": 50000, "max_points": 99999, "bonus": 1000000},
                "A7": {"min_points": 100000, "max_points": 199999, "bonus": 2000000},
                "A8": {"min_points": 200000, "max_points": 999999, "bonus": 5000000},
            },
            "structure": {
                "generation_1": "100% баллов от клиента",
                "generation_2": "50% баллов от клиента",
                "generation_3": "25% баллов от клиента",
            },
            "key_benefits": [
                "Пассивный доход от структуры",
                "Бонусы за достижение уровней",
                "Комиссии от рекомендаций",
                "Возможность масштабирования",
            ],
        }
        self.last_updated = datetime.utcnow()
        logger.info("✅ Информация о программе загружена")
        return self.program_info

    def load_products(self) -> List[Dict[str, Any]]:
        """
        Загрузить информацию о продуктах
        В реальности это должно быть из API личного кабинета
        """
        self.products = [
            {
                "id": 1,
                "name": "Кредитная карта",
                "points": 500,
                "description": "Кредитная карта с кэшбэком",
                "commission": "500 баллов за клиента",
                "priority": "high",
            },
            {
                "id": 2,
                "name": "Дебетовая карта",
                "points": 300,
                "description": "Дебетовая карта с процентом на остаток",
                "commission": "300 баллов за клиента",
                "priority": "medium",
            },
            {
                "id": 3,
                "name": "Кредит наличными",
                "points": 1000,
                "description": "Кредит на любые цели",
                "commission": "1000 баллов за клиента",
                "priority": "high",
            },
            {
                "id": 4,
                "name": "Ипотека",
                "points": 5000,
                "description": "Ипотечное кредитование",
                "commission": "5000 баллов за клиента",
                "priority": "very_high",
            },
            {
                "id": 5,
                "name": "Инвестиции",
                "points": 2000,
                "description": "Инвестиционные услуги",
                "commission": "2000 баллов за клиента",
                "priority": "high",
            },
        ]
        logger.info(f"✅ Загружено {len(self.products)} продуктов")
        return self.products

    def get_top_products(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Получить топ продукты по баллам"""
        if not self.products:
            self.load_products()
        return sorted(self.products, key=lambda x: x["points"], reverse=True)[:limit]

    def get_product_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Найти продукт по названию"""
        if not self.products:
            self.load_products()
        for product in self.products:
            if name.lower() in product["name"].lower():
                return product
        return None

    def calculate_partner_structure(self) -> Dict[str, Any]:
        """
        Рассчитать структуру партнера
        Анализирует контакты, группы, кампании
        """
        try:
            # Получить статистику контактов
            total_contacts = self.db.query(Contact).count()
            active_contacts = self.db.query(Contact).filter_by(is_active=True).count()

            # Получить статистику групп
            total_groups = self.db.query(Group).count()

            # Получить статистику кампаний
            total_campaigns = self.db.query(Campaign).count()
            completed_campaigns = (
                self.db.query(Campaign)
                .filter_by(status="completed")
                .count()
            )

            # Рассчитать общие баллы
            total_points = 0
            campaign_contacts = self.db.query(CampaignContact).filter_by(
                status=MessageStatus.SENT
            ).all()

            for cc in campaign_contacts:
                product = self.get_product_by_name("Кредит")
                if product:
                    total_points += product["points"]

            self.partner_structure = {
                "total_contacts": total_contacts,
                "active_contacts": active_contacts,
                "total_groups": total_groups,
                "total_campaigns": total_campaigns,
                "completed_campaigns": completed_campaigns,
                "total_points": total_points,
                "estimated_level": self._estimate_level(total_points),
                "next_level_points": self._get_next_level_points(total_points),
            }

            logger.info(f"✅ Структура партнера рассчитана: {self.partner_structure}")
            return self.partner_structure

        except Exception as e:
            logger.error(f"❌ Ошибка при расчете структуры: {e}")
            return {}

    def _estimate_level(self, points: int) -> str:
        """Определить уровень квалификации по баллам"""
        levels = self.program_info.get("commission_levels", {})
        for level, info in levels.items():
            if info["min_points"] <= points <= info["max_points"]:
                return level
        return "A1"

    def _get_next_level_points(self, current_points: int) -> int:
        """Получить количество баллов до следующего уровня"""
        levels = self.program_info.get("commission_levels", {})
        for level, info in levels.items():
            if info["min_points"] > current_points:
                return info["min_points"] - current_points
        return 0

    def get_campaign_stats(self) -> Dict[str, Any]:
        """Получить статистику кампаний"""
        try:
            campaigns = self.db.query(Campaign).all()

            total_sent = sum(c.sent_count for c in campaigns)
            total_delivered = sum(c.delivered_count for c in campaigns)
            total_read = sum(c.read_count for c in campaigns)
            total_failed = sum(c.failed_count for c in campaigns)

            self.campaign_stats = {
                "total_campaigns": len(campaigns),
                "total_sent": total_sent,
                "total_delivered": total_delivered,
                "total_read": total_read,
                "total_failed": total_failed,
                "success_rate": (
                    (total_delivered / total_sent * 100) if total_sent > 0 else 0
                ),
                "read_rate": (
                    (total_read / total_sent * 100) if total_sent > 0 else 0
                ),
            }

            logger.info(f"✅ Статистика кампаний: {self.campaign_stats}")
            return self.campaign_stats

        except Exception as e:
            logger.error(f"❌ Ошибка при получении статистики: {e}")
            return {}

    def generate_strategy_recommendation(self) -> str:
        """
        Генерировать рекомендацию по стратегии на основе данных
        """
        if not self.campaign_stats:
            self.get_campaign_stats()

        if not self.partner_structure:
            self.calculate_partner_structure()

        recommendations = []

        # Анализ по успешности кампаний
        success_rate = self.campaign_stats.get("success_rate", 0)
        if success_rate < 50:
            recommendations.append(
                "⚠️ Низкий процент доставки. Рекомендуется пересмотреть стратегию отправки."
            )
        elif success_rate > 80:
            recommendations.append(
                "✅ Отличный процент доставки. Продолжайте текущую стратегию."
            )

        # Анализ по активности контактов
        active_ratio = (
            self.partner_structure.get("active_contacts", 0)
            / max(self.partner_structure.get("total_contacts", 1), 1)
            * 100
        )
        if active_ratio < 30:
            recommendations.append(
                "📊 Низкая активность контактов. Рекомендуется увеличить частоту контактов."
            )

        # Анализ по баллам
        total_points = self.partner_structure.get("total_points", 0)
        if total_points < 1000:
            recommendations.append(
                "💰 Низкое количество баллов. Сосредоточьтесь на высокобаллных продуктах (ипотека, кредиты)."
            )

        strategy = "\n".join(recommendations) if recommendations else "✅ Стратегия оптимальна"
        logger.info(f"📋 Рекомендация по стратегии: {strategy}")
        return strategy

    def export_knowledge_base(self) -> Dict[str, Any]:
        """Экспортировать всю базу знаний"""
        return {
            "program_info": self.program_info,
            "products": self.products,
            "partner_structure": self.partner_structure,
            "campaign_stats": self.campaign_stats,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }

    def import_knowledge_base(self, data: Dict[str, Any]):
        """Импортировать базу знаний"""
        self.program_info = data.get("program_info", {})
        self.products = data.get("products", [])
        self.partner_structure = data.get("partner_structure", {})
        self.campaign_stats = data.get("campaign_stats", {})
        logger.info("✅ База знаний импортирована")


def get_knowledge_base(db: Session) -> KnowledgeBase:
    """Получить экземпляр базы знаний"""
    kb = KnowledgeBase(db)
    kb.load_program_info()
    kb.load_products()
    kb.calculate_partner_structure()
    kb.get_campaign_stats()
    return kb

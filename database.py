"""
Database connection и session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import logging
import os
from models import Base

logger = logging.getLogger(__name__)

# Create engine
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./alfa.db')
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Отключаем пулинг для асинхронности
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Получить сессию БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Инициализировать БД (создать таблицы)"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def drop_db():
    """Удалить все таблицы (для тестирования)"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop database: {e}")
        raise

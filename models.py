"""
SQLAlchemy Models для Alfa Backend
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, Enum, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class MessageStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class Contact(Base):
    """Модель контакта"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=True, index=True)
    phone = Column(String(20), nullable=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)
    is_bot = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_contacted = Column(DateTime, nullable=True)
    extra_data = Column(JSON, nullable=True)  # Дополнительные данные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = relationship("Message", back_populates="contact")
    campaign_contacts = relationship("CampaignContact", back_populates="contact")

    def __repr__(self):
        return f"<Contact {self.first_name} {self.last_name} ({self.telegram_id})>"


class Group(Base):
    """Модель группы/канала"""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_channel = Column(Boolean, default=False)
    members_count = Column(Integer, default=0)
    username = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    last_synced = Column(DateTime, nullable=True)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    members = relationship("GroupMember", back_populates="group")

    def __repr__(self):
        return f"<Group {self.title} ({self.telegram_id})>"


class GroupMember(Base):
    """Модель участника группы"""
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)

    # Relationships
    group = relationship("Group", back_populates="members")
    contact = relationship("Contact")

    def __repr__(self):
        return f"<GroupMember group_id={self.group_id} contact_id={self.contact_id}>"


class Campaign(Base):
    """Модель кампании рассылки"""
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    message_template = Column(Text, nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    total_contacts = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    read_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    campaign_contacts = relationship("CampaignContact", back_populates="campaign", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="campaign")

    def __repr__(self):
        return f"<Campaign {self.name} ({self.status})>"


class CampaignContact(Base):
    """Модель связи кампании и контакта"""
    __tablename__ = "campaign_contacts"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING)
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    retries = Column(Integer, default=0)

    # Relationships
    campaign = relationship("Campaign", back_populates="campaign_contacts")
    contact = relationship("Contact", back_populates="campaign_contacts")

    def __repr__(self):
        return f"<CampaignContact campaign_id={self.campaign_id} contact_id={self.contact_id}>"


class Message(Base):
    """Модель сообщения"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    telegram_message_id = Column(String(50), nullable=True)
    text = Column(Text, nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING)
    is_outgoing = Column(Boolean, default=True)
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    campaign = relationship("Campaign", back_populates="messages")
    contact = relationship("Contact", back_populates="messages")

    def __repr__(self):
        return f"<Message to={self.contact_id} status={self.status}>"


class AuditLog(Base):
    """Модель логирования действий"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String(255), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog {self.action} on {self.entity_type}>"

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from src.main.model.base import Base


class SenderEnum(str, enum.Enum):
    user = "user"
    bot = "bot"


class ChatMessage(Base):
    __tablename__ = "chat_message"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("chat_session.id"), nullable=False)

    sender = Column(Enum(SenderEnum), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    session = relationship("ChatSession", back_populates="messages")

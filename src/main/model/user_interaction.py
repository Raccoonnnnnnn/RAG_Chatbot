from sqlalchemy import Column, Integer, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from src.main.model.base import Base


class ActionTypeEnum(str, enum.Enum):
    view = "view"
    click = "click"
    purchase = "purchase"
    like = "like"
    dislike = "dislike"
    search = "search"


class UserInteraction(Base):
    __tablename__ = "user_interaction"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    action_type = Column(Enum(ActionTypeEnum), nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    user = relationship("User", back_populates="interactions")

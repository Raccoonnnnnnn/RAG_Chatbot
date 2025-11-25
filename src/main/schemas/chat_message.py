from pydantic import BaseModel
from datetime import datetime

from src.main.model.chat_message import SenderEnum


class ChatMessageCreate(BaseModel):
    session_id: int
    sender: SenderEnum
    content: str


class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    sender: SenderEnum
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

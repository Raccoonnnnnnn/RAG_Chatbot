from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatSessionCreate(BaseModel):
    user_id: int
    session_title: Optional[str] = None


class ChatSessionResponse(BaseModel):
    id: int
    user_id: int
    session_title: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

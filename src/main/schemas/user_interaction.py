from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

from src.main.model.user_interaction import ActionTypeEnum


class UserInteractionCreate(BaseModel):
    user_id: int
    action_type: ActionTypeEnum
    meta_data: Optional[Any] = None


class UserInteractionResponse(BaseModel):
    id: int
    user_id: int
    action_type: ActionTypeEnum
    meta_data: Optional[Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

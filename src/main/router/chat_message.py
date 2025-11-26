from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.core.database import get_db
from src.main.schemas.chat_message import (
    ChatMessageCreate,
    ChatMessageResponse,
)
from src.main.crud.chat_message import (
    create_message,
    get_messages_by_session,
)

chat_message_router = APIRouter()


@chat_message_router.post("/", response_model=ChatMessageResponse)
async def create_message_route(
    data: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_message(db, data)


@chat_message_router.get(
    "/session/{session_id}", response_model=list[ChatMessageResponse]
)
async def fetch_messages_by_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_messages_by_session(db, session_id)
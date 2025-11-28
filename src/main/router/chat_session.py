from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.core.database import get_db
from src.main.schemas.chat_session import ChatSessionCreate, ChatSessionResponse
from src.main.crud.chat_session import (
    create_chat_session,
    get_sessions_by_user,
    get_session, update_session,
)

chat_session_router = APIRouter()


@chat_session_router.post("/", response_model=ChatSessionResponse)
async def create_chat_session_route(
    data: ChatSessionCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_chat_session(db, data)


@chat_session_router.get(
    "/user/{user_id}", response_model=list[ChatSessionResponse]
)
async def list_sessions_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_sessions_by_user(db, user_id)


@chat_session_router.get("/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session_route(
    session_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_session(db, session_id)

@chat_session_router.post("/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session_route(
        session_id: int,
        data: ChatSessionCreate,
        session: AsyncSession = Depends(get_db)
):
    return await update_session(session, session_id, data)
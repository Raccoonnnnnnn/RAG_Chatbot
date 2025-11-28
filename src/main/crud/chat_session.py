from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.main.model.chat_session import ChatSession
from src.main.schemas.chat_session import ChatSessionCreate
from datetime import datetime


async def create_chat_session(db: AsyncSession, data: ChatSessionCreate):
    session = ChatSession(
        user_id=data.user_id,
        session_title=data.session_title,
        created_at=datetime.utcnow(),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def get_sessions_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(ChatSession).where(ChatSession.user_id == user_id)
    )
    return result.scalars().all()


async def get_session(db: AsyncSession, session_id: int):
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    return result.scalar_one_or_none()

async def update_session(db: AsyncSession, session_id: int, data: ChatSessionCreate):
    chat_session = await get_session(db, session_id)
    chat_session.session_title = data.session_title
    db.add(chat_session)
    await db.commit()
    await db.refresh(chat_session)
    return chat_session
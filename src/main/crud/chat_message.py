from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from src.main.model.chat_message import ChatMessage
from src.main.schemas.chat_message import ChatMessageCreate


async def create_message(db: AsyncSession, data: ChatMessageCreate):
    msg = ChatMessage(
        session_id=data.session_id,
        sender=data.sender,
        content=data.content,
        created_at=datetime.utcnow(),
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def get_messages_by_session(db: AsyncSession, session_id: int):
    result = await db.execute(
        select(ChatMessage).where(ChatMessage.session_id == session_id)
    )
    return result.scalars().all()
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.main.model.user_interaction import UserInteraction
from src.main.schemas.user_interaction import UserInteractionCreate
from datetime import datetime


async def create_interaction(db: AsyncSession, data: UserInteractionCreate):
    interaction = UserInteraction(
        user_id=data.user_id,
        action_type=data.action_type,
        metadata=data.metadata,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(interaction)
    await db.commit()
    await db.refresh(interaction)
    return interaction


async def get_interactions_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(UserInteraction).where(UserInteraction.user_id == user_id)
    )
    return result.scalars().all()

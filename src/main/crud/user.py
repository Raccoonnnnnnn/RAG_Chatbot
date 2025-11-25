from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from datetime import datetime
from src.main.model.user import User
from src.main.schemas.user import UserCreate


async def create_user(db: AsyncSession, data: UserCreate):
    new_user = User(
        username=data.username,
        email=data.email,
        password=data.password,
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow()
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

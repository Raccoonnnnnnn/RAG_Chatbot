from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.main.core.database import get_db
from src.main.schemas.user import UserCreate, UserResponse
from src.main.crud.user import create_user, get_all_users, get_user

user_router = APIRouter()


@user_router.post("/", response_model=UserResponse)
async def create_user_route(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, data)


@user_router.get("/{user_id}", response_model=UserResponse)
async def fetch_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user(db, user_id)


@user_router.get("/", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.main.core.database import get_db
from src.main.core.jwt import create_access_token
from src.main.core.security import verify_password
from src.main.schemas.user import UserCreate, UserResponse, LoginResponse, LoginRequest
from src.main.crud.user import create_user, get_all_users, get_user, get_user_by_username

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

@user_router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Wrong password")

    token = create_access_token({"sub": user.username})

    return LoginResponse(access_token=token)
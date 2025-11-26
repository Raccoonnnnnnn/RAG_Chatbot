# src/main/api/user_interaction.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.core.database import get_db
from src.main.schemas.user_interaction import (
    UserInteractionCreate,
    UserInteractionResponse,
)
from src.main.crud.user_interaction import (
    create_interaction,
    get_interaction,
    get_all_interactions,
    get_interactions_by_user,
)

interaction_router = APIRouter()


@interaction_router.post("/", response_model=UserInteractionResponse)
async def create_interaction_route(
    data: UserInteractionCreate, db: AsyncSession = Depends(get_db)
):
    return await create_interaction(db, data)


@interaction_router.get("/{interaction_id}", response_model=UserInteractionResponse)
async def fetch_interaction(
    interaction_id: int, db: AsyncSession = Depends(get_db)
):
    return await get_interaction(db, interaction_id)


@interaction_router.get(
    "/user/{user_id}", response_model=list[UserInteractionResponse]
)
async def fetch_interactions_by_user(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    return await get_interactions_by_user(db, user_id)


@interaction_router.get("/", response_model=list[UserInteractionResponse])
async def list_interactions(db: AsyncSession = Depends(get_db)):
    return await get_all_interactions(db)

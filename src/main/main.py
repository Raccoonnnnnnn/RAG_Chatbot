from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from src.main.core.database import Base, engine
from src.main.router.user import user_router
from src.main.api import initialize_rag
from src.main.router.lightrag import lightrag_router
from src.main.model import user, user_interaction, chat_message, chat_session

# Tạo bảng database (sync, chỉ chạy 1 lần)
async def create_tables_if_not_exist():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def init_rag_bg():
    print("Initializing LightRAG in background...")
    await initialize_rag()
    print("LightRAG initialized!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context.
    LightRAG sẽ được load nền background để server start ngay.
    """

    # Tạo task async chạy background

    asyncio.create_task(create_tables_if_not_exist())
    asyncio.create_task(init_rag_bg())

    yield

    print("Shutting down...")


# Khởi tạo app
app = FastAPI(
    title="FastAPI + Postgres + LightRAG",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI + DB + LightRAG running successfully"}

# Routers
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(lightrag_router, prefix="/rag", tags=["LightRAG"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main.main:app", host="127.0.0.1", port=8000, reload=False)

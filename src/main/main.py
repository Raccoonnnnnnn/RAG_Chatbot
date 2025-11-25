from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.main.core.database import Base, engine
from src.main.router.user import user_router
from src.main.api import initialize_rag
from src.main.router.lightrag import lightrag_router

# Tạo bảng database
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing LightRAG...")
    await initialize_rag()
    print("LightRAG initialized!")
    yield
    # Shutdown
    print("Shutting down...")


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


@app.get("/")
def root():
    return {"message": "FastAPI + DB + LightRAG running successfully"}


# Routers
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(lightrag_router, prefix="/rag", tags=["LightRAG"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main.main:app", host="0.0.0.0", port=8000, reload=True)

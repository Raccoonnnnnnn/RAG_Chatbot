from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from src.main.router.chat_message import chat_message_router
from src.main.router.chat_session import chat_session_router
from src.main.router.user import user_router
from src.main.router.lightrag import lightrag_router, initialize_rag


app = FastAPI(
    title="FastAPI + Postgres + LightRAG",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root
@app.get("/")
def root():
    return {"message": "FastAPI + DB + LightRAG running successfully"}


# Routers
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(lightrag_router, prefix="/rag", tags=["LightRAG"])
app.include_router(chat_session_router, prefix="/chat-session", tags=["ChatSessions"])
app.include_router(chat_message_router, prefix="/chat-message", tags=["ChatMessages"])

if __name__ == "__main__":
    import uvicorn

    asyncio.run(initialize_rag())
    uvicorn.run("src.main.main:app", host="127.0.0.1", port=8001, reload=False)

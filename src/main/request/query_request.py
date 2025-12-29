from pydantic import BaseModel
import os

TOP_K = int(os.getenv("TOP_K", 5))
DEFAULT_QUERY_MODE = os.getenv("DEFAULT_QUERY_MODE", "local")


class QueryRequest(BaseModel):
    query: str
    mode: str = DEFAULT_QUERY_MODE
    conversation_history: list[dict[str, str]] = []
    top_k: int = TOP_K,
    user_id: int | None = None

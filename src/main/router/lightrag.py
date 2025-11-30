import asyncio
import os
import logging
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import pandas as pd

from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.operate import chunking_by_token_size
from lightrag.prompt import PROMPTS

from src.data_preprocessing.insert_custom_kg import create_custom_kg_for_batch
from src.main.request.insert_request import InsertRequest
from src.main.request.insert_custom_request import InsertCustomRequest
from src.main.request.delete_request import DeleteRequest
from src.main.request.query_request import QueryRequest

lightrag_router = APIRouter()

# =====================================================
# Environment & Configuration
# =====================================================
load_dotenv()

INSERT_BATCH_SIZE = int(os.getenv("INSERT_BATCH_SIZE", 20))
DEFAULT_QUERY_MODE = os.getenv("DEFAULT_QUERY_MODE", "local")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gemma2:9b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
MODEL_HOST = "http://localhost:11434"
LOG_FILE_MODE = os.getenv("LOG_FILE_MODE", "a")
WORKING_DIR = "./dickens_ollama"
LOG_FILE = "./logs/api_logs.log"
os.makedirs(WORKING_DIR, exist_ok=True)

# =====================================================
# Logging Setup
# =====================================================
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, mode=LOG_FILE_MODE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =====================================================
# Utility: Custom chunking
# =====================================================
def custom_chunking_wrapper(
        content,
        split_by_character=None,
        split_by_character_only=False,
        chunk_token_size=250,
        chunk_overlap_token_size=0,
        tiktoken_model_name="gpt-4o"
):
    return chunking_by_token_size(
        content=content,
        split_by_character="\n\n",
        split_by_character_only=False,
        overlap_token_size=50,
        max_token_size=512,
        tiktoken_model="gpt-4o"
    )


# =====================================================
# LightRAG Initialization
# =====================================================
rag = None
is_just_updated_KG = False


async def initialize_rag():
    """Initialize LightRAG instance asynchronously."""
    global rag
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name=LLM_MODEL_NAME,
        enable_llm_cache=False,
        llm_model_max_async=4,
        llm_model_max_token_size=8192,
        llm_model_kwargs={"host": MODEL_HOST, "options": {"num_ctx": 32768}},
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embed(
                texts, embed_model=EMBED_MODEL, host=MODEL_HOST
            ),
        ),
        chunking_func=custom_chunking_wrapper,
        max_parallel_insert=INSERT_BATCH_SIZE,
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()
    logger.info(f"LightRAG initialized with model: {LLM_MODEL_NAME}")


# =====================================================
# API Endpoints
# =====================================================

@lightrag_router.post("/insert")
async def insert_document(request: InsertRequest):
    if not rag:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")
    await rag.ainsert(request.content)
    return {"message": "Document inserted!"}


@lightrag_router.post("/insert_custom_kg")
async def insert_custom_kg(request: InsertCustomRequest):
    """Insert custom knowledge graph batches."""
    global is_just_updated_KG

    if not rag:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")

    try:
        custom_kgs, df = create_custom_kg_for_batch(request.path, batch_size=request.batch_size)
        total_batches = len(custom_kgs)

        for idx, custom_kg in enumerate(custom_kgs, start=1):
            try:
                await rag.ainsert_custom_kg(custom_kg)
                logger.info(f"Inserted batch {idx}/{total_batches}")
            except Exception as e:
                logger.error(f"Failed batch {idx}: {e}")
                raise HTTPException(status_code=500, detail=f"Error in batch {idx}: {e}")

        await rag.aclear_cache()
        is_just_updated_KG = True

        return JSONResponse(
            status_code=200,
            content={"message": f"Inserted {len(df)} records in {total_batches} batches"}
        )

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty or invalid")
    except Exception as e:
        logger.error(f"File processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")


@lightrag_router.post("/insert_batch")
async def insert_documents_batch(texts: list[str], ids: list[str] | None = None):
    if not rag:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")
    if len(texts) != len(ids):
        raise HTTPException(status_code=400, detail="Length of texts and ids must match")

    # Delete existing docs first
    for doc_id in ids:
        try:
            await rag.adelete_by_doc_id(doc_id)
        except Exception:
            continue

    logger.info(f"START inserting {len(texts)} docs")
    await rag.ainsert(texts, ids=ids)
    logger.info(f"END inserting {len(texts)} docs")

    return {"message": f"Inserted {len(texts)} documents after cleaning existing ones!"}


@lightrag_router.delete("/delete")
async def delete_document(request: DeleteRequest):
    if not rag:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")
    await rag.adelete_by_doc_id(request.doc_id)
    return {"message": "Document deleted!"}


@lightrag_router.post("/query")
async def query_rag(request: QueryRequest):
    global is_just_updated_KG
    if not rag:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")

    # Reset conversation history if KG was updated
    if is_just_updated_KG:
        request.conversation_history = []
        is_just_updated_KG = False

    response = await rag.aquery(
        request.query,
        param=QueryParam(
            mode=request.mode,
            top_k=request.top_k,
            conversation_history=request.conversation_history,
            history_turns=3,
        ),
        system_prompt=PROMPTS["custom"],
    )

    return {"query": request.query, "response": response}



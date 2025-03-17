import asyncio
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.operate import chunking_by_token_size
from lightrag.prompt import PROMPTS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
INSERT_BATCH_SIZE = int(os.getenv("INSERT_BATCH_SIZE", 20))
DEFAULT_QUERY_MODE = os.getenv("DEFAULT_QUERY_MODE", "local")
TOP_K = int(os.getenv("TOP_K", 5))

app = FastAPI()

WORKING_DIR = "./dickens_ollama"
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

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

class InsertRequest(BaseModel):
    content: str

class DeleteRequest(BaseModel):
    doc_id: str

class QueryRequest(BaseModel):
    query: str
    mode: str = DEFAULT_QUERY_MODE
    top_k: int = TOP_K

# init RAG instance
rag = None

async def initialize_rag():
    global rag
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="gemma2:9b",
        llm_model_max_async=4,
        llm_model_max_token_size=8192,
        llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 8192}},
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embed(
                texts, embed_model="nomic-embed-text", host="http://localhost:11434"
            ),
        ),
        chunking_func=custom_chunking_wrapper,
        max_parallel_insert = INSERT_BATCH_SIZE
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()
    logging.info("✅ LightRAG is ready!")

# API insert document to LightRAG
@app.post("/insert")
async def insert_document(request: InsertRequest):
    if rag is None:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")
    
    await rag.ainsert(request.content)
    return {"message": "✅ Document inserted!"}

# API to insert batch of documents with IDs
@app.post("/insert_batch")
async def insert_documents_batch(texts: list[str], ids: list[str]):
    if rag is None:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")
    if len(texts) != len(ids):
        raise HTTPException(status_code=400, detail="Length of texts and ids must match")
    
    # Step 1: Delete existing documents with the provided IDs
    for doc_id in ids:
        try:
            await rag.adelete_by_doc_id(doc_id)
            logging.info(f"Deleted existing document with ID: {doc_id}")
        except Exception as e:
            # Ignore if the document doesn't exist or deletion fails
            logging.warning(f"Failed to delete document ID {doc_id}: {e}")
            continue
    
    # Step 2: Insert batch of new documents
    await rag.ainsert(texts, ids=ids)
    return {"message": f"✅ Inserted {len(texts)} documents after deleting existing ones!"}

# API delete document from LightRAG
@app.delete("/delete")
async def delete_document(request: DeleteRequest):
    if rag is None:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")

    await rag.adelete_by_doc_id(request.doc_id)
    return {"message": "✅ Document deleted!"}

# API query from LightRAG
@app.post("/query")
async def query_rag(request: QueryRequest):
    if rag is None:
        raise HTTPException(status_code=500, detail="LightRAG is not initialized")

    response = await rag.aquery(
        request.query,
        param=QueryParam(mode=request.mode, top_k=request.top_k),
        system_prompt=PROMPTS["rag_response"]
    )
    return {"query": request.query, "response": response}


if __name__ == "__main__":
    import uvicorn
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_rag())
    uvicorn.run(app, host="0.0.0.0", port=8000)
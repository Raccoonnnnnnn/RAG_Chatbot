import asyncio
import nest_asyncio

nest_asyncio.apply()
import os
import inspect
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.operate import chunking_by_token_size
from lightrag.prompt import PROMPTS

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

async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="gemma2:9b",
        llm_model_max_async=4,
        llm_model_max_token_size=8192,
        # kv_storage="RedisKVStorage",
        # vector_storage="QdrantVectorDBStorage",
        # vector_db_storage_cls_kwargs={
        #     "cosine_better_than_threshold": 0.3  # Your desired threshold
        # },
        # graph_storage="Neo4JStorage",
        # doc_status_storage="MongoDocStatusStorage",
        llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 8192}},
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embed(
                texts, embed_model="nomic-embed-text", host="http://localhost:11434"
            ),
        ),
        chunking_func=custom_chunking_wrapper
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


async def print_stream(stream):
    async for chunk in stream:
        print(chunk, end="", flush=True)

async def delete(rag, doc_id):
    await rag.adelete_by_doc_id(doc_id)

def main():
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())


    # Insert example text
    with open("./data/tiki_books_json.txt", "r", encoding="utf-8") as f:
        rag.insert(f.read())
        

    input = "Tư vấn cho tôi 1 số sách được đánh giá 5 sao"
    print("\n\n🔎🔎🔎 QUERY: " + input + "\n\n")

    # Perform local search
    print("\n🔎 **Truy vấn mode `LOCAL`** ...")
    response = rag.query(input, param=QueryParam(mode="local", top_k=5, stream=True), system_prompt=PROMPTS["rag_response"])
    print("\n🟢 **Kết quả (mode `LOCAL`):**\n")

    if inspect.isasyncgen(response):
        asyncio.run(print_stream(response))
    else:
        print(response)


    # Perform hybrid search
    print("\n🔎 **Truy vấn mode `HYBRID`** ...")
    response = rag.query(input, param=QueryParam(mode="hybrid", top_k=5, stream=True), system_prompt=PROMPTS["rag_response"])
    print("\n🟢 **Kết quả (mode `HYBRID`):**\n")

    if inspect.isasyncgen(response):
        asyncio.run(print_stream(response))
    else:
        print(response)
    

if __name__ == "__main__":
    main()


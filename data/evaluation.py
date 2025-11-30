import json
import asyncio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import List, Dict

from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc


# ================================
# Load Ground Truth
# ================================
def load_ground_truth(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ================================
# Metric functions
# ================================
def recall_at_k(retrieved: List[str], relevant: List[str], k: int):
    retrieved_k = retrieved[:k]
    return len(set(retrieved_k) & set(relevant)) / len(relevant) if relevant else 0


def precision_at_k(retrieved: List[str], relevant: List[str], k: int):
    retrieved_k = retrieved[:k]
    return len(set(retrieved_k) & set(relevant)) / k if k else 0


def hit_at_k(retrieved: List[str], relevant: List[str], k: int):
    retrieved_k = retrieved[:k]
    return 1.0 if len(set(retrieved_k) & set(relevant)) > 0 else 0.0


def reciprocal_rank(retrieved: List[str], relevant: List[str]):
    for idx, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            return 1.0 / idx
    return 0.0


def ndcg_at_k(retrieved: List[str], relevant: List[str], k: int):
    dcg = 0.0
    for i, doc_id in enumerate(retrieved[:k]):
        if doc_id in relevant:
            dcg += 1 / np.log2(i + 2)
    ideal_dcg = sum([1 / np.log2(i + 2) for i in range(min(len(relevant), k))])
    return dcg / ideal_dcg if ideal_dcg != 0 else 0.0


# ================================
# Evaluate RAG
# ================================
async def evaluate_retrieval(groundtruth_path: str, rag: LightRAG, k=5):
    gts = load_ground_truth(groundtruth_path)
    results = []

    for sample in gts: # Sample every 10th for quicker evaluation
        query = sample["query"]
        relevant_ids = sample["expected_context_ids"]

        response = await rag.aquery(
            query,
            param=QueryParam(mode="hybrid", top_k=k),
        )

        if isinstance(response, str) or not isinstance(response, dict):
            print(f"⚠️ Warning: response for '{query}' invalid, skip.")
            continue

        contexts = response.get("contexts", [])
        if not isinstance(contexts, list):
            contexts = []

        retrieved_ids = []
        for c in contexts:
            if isinstance(c, dict) and "doc_id" in c:
                retrieved_ids.append(c["doc_id"])

        result = {
            "query": query,
            "hit@k": hit_at_k(retrieved_ids, relevant_ids, k),
            "precision@k": precision_at_k(retrieved_ids, relevant_ids, k),
            "recall@k": recall_at_k(retrieved_ids, relevant_ids, k),
            "mrr": reciprocal_rank(retrieved_ids, relevant_ids),
            "ndcg@k": ndcg_at_k(retrieved_ids, relevant_ids, k),
        }
        results.append(result)
        if len(results) == 10:
            break

    return results


# ================================
# Save results
# ================================
def save_results(results: List[Dict]):
    os.makedirs("evaluation_results", exist_ok=True)

    # JSON
    with open("evaluation_results/results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    # CSV + Excel
    df = pd.DataFrame(results)
    df.to_csv("evaluation_results/results.csv", index=False)
    df.to_excel("evaluation_results/results.xlsx", index=False)

    print("✅ Saved results to evaluation_results/")


# ================================
# Visualization
# ================================
def visualize_results(results: List[Dict]):
    df = pd.DataFrame(results)
    os.makedirs("evaluation_results", exist_ok=True)

    for col in ["precision@k", "recall@k", "hit@k", "mrr", "ndcg@k"]:
        if col not in df.columns:
            df[col] = 0.0

    # Histogram Precision
    plt.figure(figsize=(8, 6))
    plt.hist(df["precision@k"], bins=10)
    plt.title("Precision@K Histogram")
    plt.savefig("evaluation_results/precision_hist.png")
    plt.close()

    # Histogram Recall
    plt.figure(figsize=(8, 6))
    plt.hist(df["recall@k"], bins=10)
    plt.title("Recall@K Histogram")
    plt.savefig("evaluation_results/recall_hist.png")
    plt.close()

    # Histogram NDCG
    plt.figure(figsize=(8, 6))
    plt.hist(df["ndcg@k"], bins=10)
    plt.title("NDCG@K Histogram")
    plt.savefig("evaluation_results/ndcg_hist.png")
    plt.close()

    # Precision-Recall curve (trung bình)
    plt.figure(figsize=(8, 6))
    plt.plot(df["recall@k"], df["precision@k"], marker="o")
    plt.xlabel("Recall@K")
    plt.ylabel("Precision@K")
    plt.title("Precision-Recall Curve")
    plt.grid(True)
    plt.savefig("evaluation_results/pr_curve.png")
    plt.close()

    print("📊 Saved charts to evaluation_results/")


# ================================
# Main
# ================================
async def main():
    rag = LightRAG(
        working_dir="./dickens_ollama",
        llm_model_func=ollama_model_complete,
        llm_model_name="gemma2:9b",
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embed(
                texts, embed_model="nomic-embed-text", host="http://localhost:11434"
            ),
        )
    )
    await rag.initialize_storages()

    results = await evaluate_retrieval("./ground_truth_retrieval.json", rag, k=5)

    save_results(results)
    visualize_results(results)

    print("🎉 Evaluation completed!")


if __name__ == "__main__":
    asyncio.run(main())

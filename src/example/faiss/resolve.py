import os
import pickle

import faiss
import networkx as nx
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from src.data_preprocessing.insert_custom_kg import create_custom_kg_for_batch


def build_graph_from_kgs(custom_kgs):
    G = nx.DiGraph()
    for kg in custom_kgs:
        for e in kg["entities"]:
            G.add_node(
                e["entity_name"],
                type=e["entity_type"],
                description=e["description"],
                source_id=e["source_id"]
            )
        for r in kg["relationships"]:
            if r["src_id"] and r["tgt_id"]:
                G.add_edge(
                    r["src_id"],
                    r["tgt_id"],
                    description=r["description"],
                    relation_type=r["keywords"],
                    weight=r["weight"]
                )
    print(f"Graph có {G.number_of_nodes()} node và {G.number_of_edges()} cạnh.")
    return G


def build_faiss_index(csv_file, index_path="tiki_books.index", meta_path="tiki_books_meta.pkl"):
    # Nếu đã có index và metadata → bỏ qua build
    if os.path.exists(index_path) and os.path.exists(meta_path):
        print(f"Đã phát hiện file FAISS và metadata, đang load lại từ disk...")
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            data = pickle.load(f)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Load thành công FAISS + Metadata.")
        return index, model, data["graph"], data["df"]

    # Nếu chưa có → build mới
    print("🔹 Đang tạo Knowledge Graph và Embedding...")
    custom_kgs, df = create_custom_kg_for_batch(csv_file)

    G = build_graph_from_kgs(custom_kgs)
    all_chunks = [c for kg in custom_kgs for c in kg["chunks"]]
    print(f"Tổng số chunk: {len(all_chunks)}")

    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings = [model.encode(chunk["content"]) for chunk in tqdm(all_chunks, desc="Encoding chunks")]
    vectors = np.array(embeddings).astype("float32")

    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump({"chunks": all_chunks, "graph": G, "df": df}, f)

    print(f"Đã lưu FAISS index tại: {index_path}")
    print(f"Đã lưu metadata tại: {meta_path}")

    return index, model, G, df


def query_with_graph(query: str, model, index, meta_path, k=5):
    with open(meta_path, "rb") as f:
        data = pickle.load(f)

    all_chunks = data["chunks"]
    G = data["graph"]

    query_vector = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vector, k)

    print(f"\n Truy vấn: '{query}'\n")
    top_books = []
    for i, idx in enumerate(indices[0]):
        chunk = all_chunks[idx]
        print(f"Top {i + 1}:\n{chunk['content'][:300]}...\n{'-' * 80}")
        book_name = chunk["content"].split("\n")[0].replace("Book Name: ", "").strip()
        top_books.append(book_name)

    # Mở rộng từ graph
    related_info = []
    for book in top_books:
        if book in G:
            neighbors = list(G.successors(book))
            for n in neighbors[:3]:
                desc = G.nodes[n].get("description", "")
                related_info.append(f"{book} → {n}: {desc}")

    if related_info:
        print("\n Mối quan hệ liên quan:")
        for rel in related_info:
            print("-", rel)

    return top_books, related_info


if __name__ == "__main__":
    csv_file = "./data/faiss/books_data.csv"
    index, model, G, df = build_faiss_index(csv_file)
    query_with_graph("sách học thuật hay", model, index, "faiss_result/tiki_books_meta.pkl")

import os
import pandas as pd
from typing import Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
from tqdm import tqdm
import networkx as nx


# =====================
# 1. Tạo Custom KG từ CSV
# =====================
def create_custom_kg_for_batch(csv_file, batch_size: int = 100) -> list[Dict[str, Any]]:
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("❌ File not found:", csv_file)
        return [], []

    custom_kgs = []

    for start_idx in range(0, len(df), batch_size):
        batch_df = df.iloc[start_idx:start_idx + batch_size]
        custom_kg = {"chunks": [], "entities": [], "relationships": []}

        for _, row in batch_df.iterrows():
            book_data = row.to_dict()
            book_data = {k: str(v) if pd.notna(v) else "" for k, v in book_data.items()}
            source_id = f"book-{book_data['id']}"
            book_name = book_data["name"]

            # --- Chunk ---
            chunk_content = (
                f"Book Name: {book_data['name']}\n"
                f"Author: {book_data['authors']}\n"
                f"Publisher: {book_data['manufacturer']}\n"
                f"Category: {book_data['category']}\n"
                f"Seller: {book_data['seller_name']}\n"
                f"Link: {book_data['link']}\n"
                f"Current Price: {book_data['current_price']} VND\n"
                f"Original Price: {book_data['original_price']} VND\n"
                f"Discount Rate: {book_data['discount_rate']}%\n"
                f"Rating: {book_data['rating_average']} stars\n"
                f"Quantity Sold: {book_data['quantity_sold']}\n"
                f"Description: {book_data['short_description']}"
            )

            custom_kg["chunks"].append({"content": chunk_content, "source_id": source_id})

            # --- Entities ---
            entity_map = {
                "Book Name": book_name,
                "Author": book_data["authors"],
                "Seller Name": book_data["seller_name"],
                "Manufacturer": book_data["manufacturer"],
                "Current Price": book_data["current_price"],
                "Original Price": book_data["original_price"],
                "Discount": book_data["discount_rate"],
                "Sold Quantity": book_data["quantity_sold"],
                "Rating": book_data["rating_average"],
                "Category": book_data["category"],
                "Link": book_data["link"],
                "Description": book_data["short_description"]
            }

            for etype, name in entity_map.items():
                custom_kg["entities"].append({
                    "entity_name": name,
                    "entity_type": etype,
                    "description": f"{etype} of book '{book_name}': {name}",
                    "source_id": source_id
                })

            # --- Relationships ---
            for etype, name in entity_map.items():
                if etype != "Book Name" and name:
                    rel = {
                        "src_id": book_name,
                        "tgt_id": name,
                        "description": f"The book '{book_name}' has {etype.lower()} '{name}'.",
                        "keywords": etype.lower(),
                        "weight": 1.0,
                        "source_id": source_id
                    }
                    custom_kg["relationships"].append(rel)

        custom_kgs.append(custom_kg)

    return custom_kgs, df


# =====================
# 2. Xây dựng Knowledge Graph
# =====================
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
    print(f"✅ Graph có {G.number_of_nodes()} node và {G.number_of_edges()} cạnh.")
    return G


# =====================
# 3. Tạo hoặc Load FAISS Index
# =====================
def build_faiss_index(csv_file, index_path="tiki_books.index", meta_path="tiki_books_meta.pkl"):
    # Nếu đã có index và metadata → bỏ qua build
    if os.path.exists(index_path) and os.path.exists(meta_path):
        print(f"⚡ Đã phát hiện file FAISS và metadata, đang load lại từ disk...")
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            data = pickle.load(f)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Load thành công FAISS + Metadata.")
        return index, model, data["graph"], data["df"]

    # Nếu chưa có → build mới
    print("🔹 Đang tạo Knowledge Graph và Embedding...")
    custom_kgs, df = create_custom_kg_for_batch(csv_file)

    G = build_graph_from_kgs(custom_kgs)
    all_chunks = [c for kg in custom_kgs for c in kg["chunks"]]
    print(f"✅ Tổng số chunk: {len(all_chunks)}")

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


# =====================
# 4. Truy vấn RAG
# =====================
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


# =====================
# 5. Main
# =====================
if __name__ == "__main__":
    csv_file = "/data/books_data.csv"
    index, model, G, df = build_faiss_index(csv_file)
    query_with_graph("sách học thuật hay", model, index, "../faiss/tiki_books_meta.pkl")

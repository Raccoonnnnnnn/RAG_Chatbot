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
    print(f"Đồ thị có {G.number_of_nodes()} node và {G.number_of_edges()} cạnh.")
    return G


def build_faiss_index(csv_file, index_path="tiki_books.index", meta_path="tiki_books_meta.pkl"):
    print("Đang tạo knowledge graph và chunk...")
    custom_kgs, df = create_custom_kg_for_batch(csv_file)

    # Build graph
    G = build_graph_from_kgs(custom_kgs)

    # Lấy tất cả các chunk
    all_chunks = []
    for kg in custom_kgs:
        all_chunks.extend(kg["chunks"])
    print(f"Tổng số chunk: {len(all_chunks)}")

    # Khởi tạo model embedding
    print("Đang tạo embedding...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings = []
    for chunk in tqdm(all_chunks, desc="Encoding chunks"):
        emb = model.encode(chunk["content"])
        embeddings.append(emb)

    vectors = np.array(embeddings).astype("float32")

    # Tạo FAISS index
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    # Lưu
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump({"chunks": all_chunks, "graph": G, "df": df}, f)

    print(f"Đã lưu FAISS index tại: {index_path}")
    print(f"Đã lưu metadata + graph tại: {meta_path}")

    return index, model, G, df


def query_with_graph(query: str, model, index, meta_path, k=5):
    with open(meta_path, "rb") as f:
        data = pickle.load(f)

    all_chunks = data["chunks"]
    G = data["graph"]
    df = data["df"]

    query_vector = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vector, k)

    print(f"\n Kết quả truy vấn: '{query}'\n")
    top_books = []
    for i, idx in enumerate(indices[0]):
        chunk = all_chunks[idx]
        print(f"Top {i + 1}:\n{chunk['content'][:300]}...\n{'-' * 80}")
        # Trích tên sách từ chunk
        lines = chunk["content"].split("\n")
        if lines:
            book_name = lines[0].replace("Book Name: ", "").strip()
            top_books.append(book_name)

    # Mở rộng context qua graph
    related_info = []
    for book in top_books:
        if book in G:
            neighbors = list(G.successors(book))
            for n in neighbors[:3]:  # chỉ lấy 3 quan hệ gần nhất
                desc = G.nodes[n].get("description", "")
                related_info.append(f"{book} → {n}: {desc}")

    if related_info:
        print("\n📚 Các mối quan hệ liên quan:")
        for rel in related_info:
            print("-", rel)

    return top_books, related_info


if __name__ == "__main__":
    csv_file = "C:/Users/Admin/PycharmProjects/LightRAG/data/crawl_tiki_data/books_data.csv"

    # Tạo FAISS index + Graph
    index, model, G, df = build_faiss_index(csv_file)

    # Truy vấn thử
    query_with_graph("sách của Nguyễn Nhật Ánh về tuổi học trò", model, index, "tiki_books_meta.pkl")

#
# File FAISS được tạo: tiki_books.index
# File metadata chứa thông tin các chunk: tiki_books_meta.pkl

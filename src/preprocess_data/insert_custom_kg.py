import pandas as pd
from typing import Dict, Any

def create_custom_kg_for_batch(csv_file, batch_size: int = 100) -> list[Dict[str, Any]]:

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("File not found.")
        return [], []
    
    custom_kgs = []
    
    for start_idx in range(0, len(df), batch_size):
        batch_df = df.iloc[start_idx:start_idx + batch_size]
        custom_kg = {
            "chunks": [],
            "entities": [],
            "relationships": []
        }

        for index, row in batch_df.iterrows():
            book_data = row.to_dict()
            # Chuyển tất cả giá trị thành chuỗi và xử lý NaN
            book_data = {k: str(v) if pd.notna(v) else "" for k, v in book_data.items()}
            source_id = f"book-{book_data['id']}"
            book_name = book_data["name"]

            # Tạo nội dung chunk (giữ nguyên như trước)
            chunk_content = (
                f"{book_name} is a book written by {book_data['authors']} "
                f"published by {book_data['manufacturer']} under category {book_data['category']}. "
                f"It has a price of {book_data['current_price']} VND with a discount of {book_data['discount_rate']}%. "
                f"{book_data['short_description']}"
            )
            custom_kg["chunks"].append({
                "content": chunk_content,
                "source_id": source_id
            })

            # Tạo entities cho mỗi cột
            entities = [
                {
                    "entity_name": book_name,
                    "entity_type": "Book Name",
                    "description": f"The book '{book_name}', a published work categorized under '{book_data['category']}' with specific attributes like price, sales, and rating.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["authors"],
                    "entity_type": "Author",
                    "description": f"The author '{book_data['authors']}' who wrote the book '{book_name}'.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["seller_name"],
                    "entity_type": "Seller Name",
                    "description": f"The seller '{book_data['seller_name']}' offering the book '{book_name}' for purchase.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["manufacturer"],
                    "entity_type": "Manufacturer",
                    "description": f"The manufacturer '{book_data['manufacturer']}' responsible for publishing the book '{book_name}'.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["current_price"],
                    "entity_type": "Current Price",
                    "description": f"The Current Price of the book '{book_name}', set at {book_data['current_price']}.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["original_price"],
                    "entity_type": "Original Price",
                    "description": f"The Original Price of the book '{book_name}', set at {book_data['original_price']}.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["discount_rate"],
                    "entity_type": "Discount",
                    "description": f"The Discount of the book '{book_name}', set at {book_data['discount_rate']}.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["quantity_sold"],
                    "entity_type": "Sold Quantity",
                    "description": f"The Sold Quantity of the book '{book_name}', set at {book_data['quantity_sold']}.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["rating_average"],
                    "entity_type": "Rating",
                    "description": f"The Rating of the book '{book_name}', set at {book_data['rating_average']}.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["category"],
                    "entity_type": "Category",
                    "description": f"The book '{book_name}' belongs to the '{book_data['category']}' genre.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["link"],
                    "entity_type": "Link",
                    "description": f"The Link of the book '{book_name}', set at {book_data['link']}.",
                    "source_id": source_id
                },
                {
                    "entity_name": book_data["short_description"],
                    "entity_type": "Description",
                    "description": f"Summary of the book '{book_name}': {book_data['short_description']}.",
                    "source_id": source_id
                }
            ]
            custom_kg["entities"].extend(entities)

            # Tạo relationships giữa Book Name và các entity khác
            relationships = [
                {
                    "src_id": book_name,
                    "tgt_id": book_data["authors"],
                    "description": f"The book '{book_name}' was written by '{book_data['authors']}'.",
                    "keywords": "authorship",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["seller_name"],
                    "description": f"The book '{book_name}' is sold by '{book_data['seller_name']}'.",
                    "keywords": "sold by",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["manufacturer"],
                    "description": f"The book '{book_name}' was published by '{book_data['manufacturer']}'.",
                    "keywords": "published by",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["current_price"],
                    "description": f"The book '{book_name}' is currently priced at '{book_data['current_price']}'.",
                    "keywords": "has price",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["original_price"],
                    "description": f"The book '{book_name}' originally cost '{book_data['original_price']}'.",
                    "keywords": "originally priced",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["discount_rate"],
                    "description": f"The book '{book_name}' is available at a '{book_data['discount_rate']}' discount.",
                    "keywords": "has discount",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["quantity_sold"],
                    "description": f"The book '{book_name}' has sold '{book_data['quantity_sold']}' copies.",
                    "keywords": "has sold quantity",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["rating_average"],
                    "description": f"The book '{book_name}' has a rating of '{book_data['rating_average']}'.",
                    "keywords": "has rating",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["category"],
                    "description": f"The book '{book_name}' falls under the '{book_data['category']}' genre.",
                    "keywords": "belongs to category",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["link"],
                    "description": f"The book '{book_name}' is available at '{book_data['link']}'.",
                    "keywords": "has link",
                    "weight": 1.0,
                    "source_id": source_id
                },
                {
                    "src_id": book_name,
                    "tgt_id": book_data["short_description"],
                    "description": f"The book '{book_name}' summary: '{book_data['short_description']}'.",
                    "keywords": "has description",
                    "weight": 1.0,
                    "source_id": source_id
                }
            ]
            custom_kg["relationships"].extend(relationships)
        
        custom_kgs.append(custom_kg)
    
    return custom_kgs, df

# # Đọc dữ liệu từ CSV (giả lập 3000 sách)
# csv_data = """
# id,name,link,current_price,original_price,discount_rate,rating_average,quantity_sold,authors,seller_name,category,manufacturer,short_description
# 275861063,Walden Một Mình Sống Trong Rừng (Ấn Bản Bỏ Túi) - Bản Quyền,https://tiki.vn/product-p275861063.html?spid=275861064,151164,180000,16,5.0,55,Henry David Thoreau,Gooda Official,Du ký,Nhà Xuất Bản Tri Thức,"“Walden” là một hồi tưởng đầy chiêm nghiệm suy tư về quãng đời “hai năm hai tháng hai ngày” sống một mình trong một mảnh đất rừng bên cạnh đầm Walden, “Giọt nước của Trời”, “đáng yêu hơn kim cương” tr..."
# """
# df = pd.read_csv(pd.compat.StringIO(csv_data))
# # Giả lập 3000 sách bằng cách nhân bản dữ liệu (trong thực tế, bạn sẽ dùng file CSV thật)
# df = pd.concat([df] * 3000, ignore_index=True)

# # Tạo các batch custom_kg
# batch_size = 100  # Có thể điều chỉnh: 50, 200, 500 tùy hệ thống
# custom_kgs = create_custom_kg_for_batch(df, batch_size=batch_size)

# # Gọi insert_custom_kg cho từng batch
# for idx, custom_kg in enumerate(custom_kgs):
#     rag.insert_custom_kg(custom_kg, full_doc_id=f"batch-{idx}")
#     print(f"Inserted batch {idx + 1}/{len(custom_kgs)}")
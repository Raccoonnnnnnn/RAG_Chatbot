import json
import re

INPUT_FILE = "kv_store_full_docs.json"
OUTPUT_FILE = "ground_truth.json"


def extract_field(text, field_name):
    pattern = rf"{field_name}:\s*(.*)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def first_sentence(text):
    """Lấy câu đầu tiên từ Description để làm câu hỏi."""
    if not text:
        return None
    parts = re.split(r'[.!?]', text)
    return parts[0].strip()


def generate_questions(book_id, content):
    """
    Sinh 10 câu hỏi/1 sách.
    """

    name = extract_field(content, "Book Name")
    link = extract_field(content, "Link")
    price = extract_field(content, "Current Price")
    original_price = extract_field(content, "Original Price")
    discount = extract_field(content, "Discount")
    rating = extract_field(content, "Rating")
    sold = extract_field(content, "Sold Quantity")
    authors = extract_field(content, "Authors")
    seller = extract_field(content, "Seller Name")
    manufacturer = extract_field(content, "Manufacturer")
    category = extract_field(content, "Category")
    description = extract_field(content, "Description")

    samples = []

    # 1. Giá hiện tại
    if price:
        samples.append({
            "query": f"Giá hiện tại của sách {name} là bao nhiêu?",
            "gold_answer": f"Giá hiện tại của sách {name} là {price}.",
            "gold_passages": [f"Current Price: {price}"],
            "meta": {"source_id": book_id}
        })

    # 2. Giá gốc
    if original_price:
        samples.append({
            "query": f"Giá gốc ban đầu của sách {name} là bao nhiêu?",
            "gold_answer": f"Giá gốc của sách là {original_price}.",
            "gold_passages": [f"Original Price: {original_price}"],
            "meta": {"source_id": book_id}
        })

    # 3. Tỉ lệ giảm giá
    if discount:
        samples.append({
            "query": f"Sách {name} đang giảm giá bao nhiêu phần trăm?",
            "gold_answer": f"Sách đang giảm {discount}.",
            "gold_passages": [f"Discount: {discount}"],
            "meta": {"source_id": book_id}
        })

    # 4. Tác giả
    if authors and authors != "N/A":
        samples.append({
            "query": f"Ai là tác giả của sách {name}?",
            "gold_answer": f"Tác giả của sách là {authors}.",
            "gold_passages": [f"Authors: {authors}"],
            "meta": {"source_id": book_id}
        })

    # 5. Nhà xuất bản
    if manufacturer:
        samples.append({
            "query": f"Nhà xuất bản của sách {name} là gì?",
            "gold_answer": f"Nhà xuất bản của sách là {manufacturer}.",
            "gold_passages": [f"Manufacturer: {manufacturer}"],
            "meta": {"source_id": book_id}
        })

    # 6. Danh mục
    if category:
        samples.append({
            "query": f"Sách {name} thuộc thể loại nào?",
            "gold_answer": f"Sách thuộc thể loại {category}.",
            "gold_passages": [f"Category: {category}"],
            "meta": {"source_id": book_id}
        })

    # 7. Nhà bán hàng
    if seller:
        samples.append({
            "query": f"Sách {name} được bán bởi nhà bán hàng nào?",
            "gold_answer": f"Sách được bán bởi {seller}.",
            "gold_passages": [f"Seller Name: {seller}"],
            "meta": {"source_id": book_id}
        })

    # 8. Rating
    if rating:
        samples.append({
            "query": f"Sách {name} được đánh giá bao nhiêu sao?",
            "gold_answer": f"Sách được đánh giá {rating}.",
            "gold_passages": [f"Rating: {rating}"],
            "meta": {"source_id": book_id}
        })

    # 9. Số lượng bán
    if sold:
        samples.append({
            "query": f"Sách {name} đã bán được bao nhiêu bản?",
            "gold_answer": f"Sách đã bán {sold} bản.",
            "gold_passages": [f"Sold Quantity: {sold}"],
            "meta": {"source_id": book_id}
        })

    # 10. Câu hỏi dựa trên description
    if description:
        first = first_sentence(description)
        if first:
            samples.append({
                "query": f"Nội dung chính được nhắc tới đầu tiên trong mô tả của sách {name} là gì?",
                "gold_answer": first,
                "gold_passages": [f"Description: {description}"],
                "meta": {"source_id": book_id}
            })

    return samples


def main():
    with open(INPUT_FILE, "r", encoding="utf8") as f:
        data = json.load(f)

    dataset = []
    id_count = 1

    for book_id, item in data.items():
        content = item["content"]
        samples = generate_questions(book_id, content)

        for s in samples:
            s["id"] = id_count
            dataset.append(s)
            id_count += 1

    with open(OUTPUT_FILE, "w", encoding="utf8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

    print(f"Tạo xong dataset: {OUTPUT_FILE}, gồm {len(dataset)} câu hỏi.")


if __name__ == "__main__":
    main()

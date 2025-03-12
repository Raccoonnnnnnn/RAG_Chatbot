import pandas as pd
import json

# Đọc file Excel
try:
    df = pd.read_excel("books_full_details.xlsx", engine="openpyxl")
except FileNotFoundError:
    print("File không tồn tại.")
    exit()

# Hàm tạo mô tả sách dạng key-value
def generate_book_description(row):
    name = row["Name"] if pd.notna(row["Name"]) else ""
    price = str(row["Price (vnd)"]) + " VND" if pd.notna(row["Price (vnd)"]) else ""
    discount = str(row["Discount (%)"]) + "%" if pd.notna(row["Discount (%)"]) else ""
    sold = str(row["Sold"]) if pd.notna(row["Sold"]) else ""
    rating = str(row["Rating"]) if pd.notna(row["Rating"]) else ""
    publisher = ", ".join(eval(row["Publisher"])) if isinstance(row["Publisher"], str) and row["Publisher"] else ""
    manufacturer = ", ".join(eval(row["Manufacturer"])) if isinstance(row["Manufacturer"], str) and row["Manufacturer"] else ""
    authors = ", ".join(eval(row["Authors"])) if isinstance(row["Authors"], str) and row["Authors"] else ""
    link = row["Link"] if pd.notna(row["Link"]) else ""

    # Xử lý cột Other_sellers
    try:
        sellers_info = json.loads(row["Other_sellers"].replace("'", '"'))
        sellers = [{"name": s["name"], "price": s["price"], "link": s["link"]} for s in sellers_info]
    except:
        sellers = []

    # Tạo khối văn bản key-value
    book_info_lines = []
    if name:
        book_info_lines.append(f"Title: {name}")
    if authors:
        book_info_lines.append(f"Authors: {authors}")
    if publisher:
        book_info_lines.append(f"Publisher: {publisher}")
    if manufacturer:
        book_info_lines.append(f"Manufacturer: {manufacturer}")
    if price:
        book_info_lines.append(f"Price: {price}")
    if discount:
        book_info_lines.append(f"Discount: {discount}")
    if sold:
        book_info_lines.append(f"Sold: {sold}")
    if rating:
        book_info_lines.append(f"Rating: {rating}")
    if link:
        book_info_lines.append(f"Link: {link}")

    return "\n".join(book_info_lines)

# Chuyển đổi từng dòng thành mô tả văn bản
text_data = df.apply(generate_book_description, axis=1).tolist()

# Xuất ra file text để nạp vào LightRAG
output_file = "tiki_books_json_new.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n\n".join(text_data))

print(f"✅ Dữ liệu đã được ghi vào {output_file}")
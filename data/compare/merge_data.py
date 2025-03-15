import re

def parse_books_from_file(filename):
    """ Đọc file và trích xuất dữ liệu sách vào dictionary """
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Tách từng cuốn sách dựa trên khoảng trống giữa các entry
    books = content.split("\n\n")

    book_dict = {}
    for book in books:
        lines = book.strip().split("\n")
        title_match = re.match(r"Title:\s*(.*)", lines[0])
        if title_match:
            title = title_match.group(1).strip()
            book_dict[title] = "\n".join(lines)  # Lưu toàn bộ thông tin của sách

    return book_dict

def merge_books(file1, file2, output_file):
    """ Cập nhật thông tin sách từ file1 vào file2 và lưu vào output_file """
    books1 = parse_books_from_file(file1)
    books2 = parse_books_from_file(file2)

    # Cập nhật sách từ file1 vào file2
    updated_books = books2.copy()
    for title, content in books1.items():
        updated_books[title] = content  # Ghi đè hoặc thêm mới nếu chưa tồn tại

    # Ghi kết quả vào file mới với đúng định dạng
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(updated_books.values()) + "\n")

    print(f"✅ Đã cập nhật xong! Kết quả được lưu vào '{output_file}'.")

# Sử dụng hàm
file1 = "tiki_books_json_new.txt"  # File chứa thông tin mới
file2 = "tiki_books_json.txt"  # File cần cập nhật
output_file = "merged_books.txt"  # File kết quả

merge_books(file1, file2, output_file)

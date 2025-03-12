import pandas as pd
from tabulate import tabulate

def detect_changes(old_file, new_file):
    # Đọc dữ liệu từ file cũ và mới
    df_old = pd.read_excel(old_file)
    df_new = pd.read_excel(new_file)

    # Xác định khóa duy nhất (sử dụng "Name")
    key_column = 'Name'

    # Đảm bảo không có giá trị trùng lặp trong khóa chính
    df_old = df_old.drop_duplicates(subset=[key_column]).set_index(key_column)
    df_new = df_new.drop_duplicates(subset=[key_column]).set_index(key_column)

    # Tìm sách mới được thêm
    added_books = df_new.loc[~df_new.index.isin(df_old.index)].copy()
    added_books["Trạng thái"] = "Mới thêm"

    # Tìm sách có thay đổi dữ liệu
    common_keys = df_old.index.intersection(df_new.index)
    changed_rows = []
    changed_books_details = []

    for key in common_keys:
        old_row = df_old.loc[key]
        new_row = df_new.loc[key]

        # So sánh từng giá trị trong cùng một hàng
        changes = {}
        for col in df_old.columns:
            old_value = old_row[col] if isinstance(old_row, pd.Series) else old_row.iloc[0]
            new_value = new_row[col] if isinstance(new_row, pd.Series) else new_row.iloc[0]

            if old_value != new_value:
                changes[col] = f"{old_value} → {new_value}"  # Giá trị cũ -> Giá trị mới

        if changes:
            changed_rows.append({'Name': key, 'Thay đổi': changes, 'Trạng thái': 'Thay đổi thông tin'})
            book_details = new_row.to_dict()
            book_details['Name'] = key  # Đảm bảo cột 'Name' có trong dữ liệu chi tiết
            changed_books_details.append(book_details)

    # Chuyển danh sách thay đổi thành DataFrame
    changed_df = pd.DataFrame(changed_rows)

    # Gộp sách mới và sách thay đổi vào một file duy nhất
    all_updates = pd.concat([added_books.reset_index(), changed_df], ignore_index=True)

    # Lấy toàn bộ dữ liệu chi tiết của sách mới và sách có thay đổi từ file mới
    full_details_df = pd.DataFrame(changed_books_details)

    # Sắp xếp lại để "Name" là cột đầu tiên
    if not full_details_df.empty:
        cols = ['Name'] + [col for col in full_details_df.columns if col != 'Name']
        full_details_df = full_details_df[cols]

    # In kết quả tổng hợp
    print(f"\n📌 Tổng số sách mới thêm: {len(added_books)}")
    print(f"📌 Tổng số sách có thay đổi thông tin: {len(changed_df)}")

    # Hiển thị bảng trên terminal
    if not changed_df.empty or not added_books.empty:
        table_data = []
        for _, row in all_updates.iterrows():
            name = row["Name"]
            status = row["Trạng thái"]
            changes = row["Thay đổi"] if "Thay đổi" in row else "N/A"

            table_data.append([name, status, changes])

        headers = ["Tên Sách", "Trạng Thái", "Chi Tiết Thay Đổi"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    # Xuất dữ liệu ra file Excel
    output_file_summary = "books_update_report.xlsx"
    output_file_details = "books_full_details.xlsx"

    with pd.ExcelWriter(output_file_summary) as writer:
        all_updates.to_excel(writer, sheet_name="Books Update", index=False)

    with pd.ExcelWriter(output_file_details) as writer:
        full_details_df.to_excel(writer, sheet_name="Books Details", index=False)

    print(f"\n✅ Báo cáo tổng hợp đã được lưu vào '{output_file_summary}'")
    print(f"✅ Báo cáo chi tiết đã được lưu vào '{output_file_details}'")

    return all_updates, full_details_df

# Sử dụng hàm
old_file_path = "tiki_books_vn.xlsx"
new_file_path = "tiki_books_vn_generated.xlsx"

updates, full_details = detect_changes(old_file_path, new_file_path)

# Hiển thị dữ liệu trực quan hơn
print("\n📌 Tóm tắt các cập nhật:")
print(updates if not updates.empty else "Không có sách mới hoặc thay đổi")

print("\n📌 Chi tiết sách mới hoặc thay đổi:")
print(full_details if not full_details.empty else "Không có sách mới hoặc thay đổi")

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

    # Tìm các hàng có thay đổi dữ liệu
    common_keys = df_old.index.intersection(df_new.index)
    changed_rows = []

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
            changed_rows.append({'Name': key, 'Changes': changes})

    # Chuyển danh sách các thay đổi thành DataFrame
    changed_df = pd.DataFrame(changed_rows)

    # In kết quả
    print(f"\n📌 Số lượng sách thay đổi thông tin: {len(changed_df)}")

    # Hiển thị bảng trên terminal
    if not changed_df.empty:
        table_data = []
        for row in changed_rows:
            table_data.append([row["Name"], "\n".join([f"{k}: {v}" for k, v in row["Changes"].items()])])

        headers = ["Tên Sách", "Thay Đổi"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    # Xuất dữ liệu ra file Excel
    with pd.ExcelWriter("./data/changes_report.xlsx") as writer:
        if not changed_df.empty:
            changed_df.to_excel(writer, sheet_name="Changed Books", index=False)

    return changed_df

# Sử dụng hàm
old_file_path = "./data/tiki_books_vn.xlsx"
new_file_path = "./data/tiki_books_vn_new.xlsx"

changed = detect_changes(old_file_path, new_file_path)

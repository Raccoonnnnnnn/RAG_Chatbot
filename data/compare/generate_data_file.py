import pandas as pd
import random

def generate_modified_file(original_file, new_file):
    # Đọc dữ liệu từ file gốc
    df = pd.read_excel(original_file)

    # Copy DataFrame để chỉnh sửa
    df_new = df.copy()

    # Thực hiện một số thay đổi ngẫu nhiên
    num_rows = len(df_new)

    for _ in range(int(num_rows * 0.5)):  # Thay đổi 20% số sách ngẫu nhiên
        idx = random.randint(0, num_rows - 1)  # Chọn dòng ngẫu nhiên

        if 'Price (vnd)' in df_new.columns:
            df_new.at[idx, 'Price (vnd)'] *= random.uniform(0.9, 1.1)  # +/- 10% giá tiền
            df_new.at[idx, 'Price (vnd)'] = round(df_new.at[idx, 'Price (vnd)'], 2)

        if 'Discount (%)' in df_new.columns:
            df_new.at[idx, 'Discount (%)'] = random.randint(0, 50)  # Giảm giá ngẫu nhiên 0-50%

        if 'Sold' in df_new.columns:
            df_new.at[idx, 'Sold'] += random.randint(-10, 10)  # Điều chỉnh số lượng bán

    # Thêm một số sách mới (5% số sách hiện có)
    new_rows = df.sample(frac=0.05, replace=True).copy()
    new_rows['Name'] = new_rows['Name'] + " (New Edition)"  # Đổi tên sách để không trùng lặp
    df_new = pd.concat([df_new, new_rows], ignore_index=True)

    # Xóa một số sách ngẫu nhiên (5% số sách hiện có)
    df_new = df_new.drop(df_new.sample(frac=0.05).index)

    # Lưu file mới
    df_new.to_excel(new_file, index=False)
    print(f"File mới đã được tạo: {new_file}")


# Tạo file mới dựa trên file gốc
original_file = "tiki_books_vn.xlsx"
new_file = "tiki_books_vn_generated.xlsx"

generate_modified_file(original_file, new_file)

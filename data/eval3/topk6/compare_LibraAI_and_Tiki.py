import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

# Dữ liệu từ JSON
data = {
    "topk6": {
        "Comprehensiveness": [90.32, 9.68],
        "Diversity": [55.65, 44.35],
        "Empowerment": [81.45, 18.55],
        "Overall Winner": [84.68, 15.32]
    }
}

# Chuẩn bị dữ liệu cho biểu đồ
criteria = ['Tính toàn diện', 'Tính đa dạng', 'Khả năng trao quyền', 'Tổng thể']
libraai_scores = [data['topk6']['Comprehensiveness'][0], 
                  data['topk6']['Diversity'][0], 
                  data['topk6']['Empowerment'][0], 
                  data['topk6']['Overall Winner'][0]]
tiki_scores = [data['topk6']['Comprehensiveness'][1], 
               data['topk6']['Diversity'][1], 
               data['topk6']['Empowerment'][1], 
               data['topk6']['Overall Winner'][1]]

# Thiết lập thông số cho biểu đồ
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
bar_width = 0.35
index = np.arange(len(criteria))

# Vẽ cột cho LibraAI và Trợ lý AI của Tiki
bars1 = ax.bar(index, libraai_scores, bar_width, label='LibraAI', color='#1e88e5', alpha=0.85)
bars2 = ax.bar(index + bar_width, tiki_scores, bar_width, label='Trợ lý AI Tiki', color='#e53935', alpha=0.85)

# Thêm nhãn giá trị trên mỗi cột
for bar in bars1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.2f}%', 
            ha='center', va='bottom', fontsize=9, color='#1e88e5')
for bar in bars2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.2f}%', 
            ha='center', va='bottom', fontsize=9, color='#e53935')

# Tùy chỉnh biểu đồ
ax.set_xlabel('Tiêu chí đánh giá', fontsize=12)
ax.set_ylabel('Chất lượng phản hồi (%)', fontsize=12)
ax.set_title('So sánh chất lượng phản hồi giữa LibraAI và Trợ lý AI của Tiki (top-k = 6)', fontsize=14, pad=10)
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(criteria, fontsize=10)
ax.set_ylim(0, 100)  # Giới hạn trục y từ 0 đến 100%
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.3, color='gray')

# Điều chỉnh bố cục
plt.tight_layout()

# Tạo thư mục lưu trữ nếu chưa có
output_dir = './data/eval3/topk6'
os.makedirs(output_dir, exist_ok=True)

# Lưu biểu đồ dưới dạng PNG và pickle
plt.savefig(f'{output_dir}/comparison_libraai_tiki_topk6.png', dpi=300, bbox_inches='tight')
with open(f'{output_dir}/comparison_libraai_tiki_topk6.pkl', 'wb') as f:
    pickle.dump(fig, f)

# Đóng biểu đồ
plt.close()
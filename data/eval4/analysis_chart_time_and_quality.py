import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import numpy as np

# Định nghĩa đường dẫn đến các file thời gian
files = [
    'data/eval4/global/time_query_context_topk6.log',
    'data/eval4/hybrid/time_query_context_topk6.log',
    'data/eval4/local/time_query_context_topk6.log',
    'data/eval4/naive/time_query_context_topk6.log'
]

# Tên các chế độ tương ứng
modes = ['Global', 'Hybrid', 'Local', 'Naive']

# Ánh xạ chế độ sang màu (dùng cho các biểu đồ khác nếu cần)
mode_colors = {
    'Global': '#1e88e5',  # pastel green
    'Hybrid': '#e53935',  # soft orange
    'Local': '#43a047',   # soft blue
    'Naive': '#fb8c00'    # pastel pink
}

# Đọc và xử lý dữ liệu thời gian
data = []
for file, mode in zip(files, modes):
    df = pd.read_csv(file, sep='\t', header=None, names=['Unused', 'Time', 'Question'])
    df['Mode'] = mode
    data.append(df[['Time', 'Mode']])

# Gộp dữ liệu thời gian
all_data = pd.concat(data, ignore_index=True)

# Tính thống kê mô tả cho thời gian
stats = all_data.groupby('Mode')['Time'].agg(['mean', 'std', 'min', 'max']).reset_index()
stats = stats.round(3)
print("Thống kê thời gian phản hồi:")
print(stats)

# Vẽ biểu đồ cột so sánh thời gian trung bình
plt.figure(figsize=(10, 6))
palette = [mode_colors[mode] for mode in stats['Mode']]
barplot = sns.barplot(x='Mode', y='mean', hue='Mode', data=stats, palette=palette, legend=False)
plt.errorbar(x=stats['Mode'], y=stats['mean'], yerr=stats['std'], fmt='none', c='black', capsize=5)
for index, row in stats.iterrows():
    barplot.text(index, row['mean'] + 0.02, f"{row['mean']:.3f}", 
                 ha='center', va='bottom', fontsize=10)
plt.title('Thời gian phản hồi trung bình của các chế độ truy vấn (top_k=6)')
plt.xlabel('Chế độ truy vấn')
plt.ylabel('Thời gian trung bình (giây)')
plt.tight_layout()
plt.savefig('./data/eval4/response_time_comparison.png', dpi=300)
plt.show()

# Hàm đọc quality metrics
def load_quality_metrics(modes, eval_dir='eval4', topk=6):
    quality_metrics = []
    for mode in modes:
        metrics_path = f"./data/{eval_dir}/{mode.lower()}/{mode.lower()}_quality_metrics_topk{topk}.json"
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r', encoding='utf-8') as f:
                metrics = json.load(f)
                mode_metrics = metrics.get(mode.lower(), {})
                quality_metrics.append({
                    'Mode': mode,
                    'Comprehensiveness': mode_metrics.get('Comprehensiveness', {}).get('Mean', 0.0),
                    'Diversity': mode_metrics.get('Diversity', {}).get('Mean', 0.0),
                    # 'Empowerment': mode_metrics.get('Empowerment', {}).get('Mean', 0.0),
                    'Relevance': mode_metrics.get('Relevance', {}).get('Mean', 0.0),
                    'Overall Score': mode_metrics.get('Overall Score', {}).get('Mean', 0.0)
                })
        else:
            print(f"Warning: Quality metrics file for {mode} not found. Using default zeros.")
            quality_metrics.append({
                'Mode': mode,
                'Comprehensiveness': 0.0,
                'Diversity': 0.0,
                # 'Empowerment': 0.0,
                'Relevance': 0.0,
                'Overall Score': 0.0
            })
    return pd.DataFrame(quality_metrics)

# Đọc quality metrics
quality_df = load_quality_metrics(modes)
print("\nThống kê chất lượng phản hồi:")
print(quality_df)

# Vẽ biểu đồ cột so sánh chất lượng
plt.figure(figsize=(12, 6))
quality_melted = quality_df.melt(id_vars='Mode', 
                                 value_vars=['Comprehensiveness', 'Diversity', 
                                            #  'Empowerment', 
                                             'Relevance', 'Overall Score'],
                                 var_name='Criterion', value_name='Score')

# Custom palette: mỗi Mode có 1 màu duy nhất
custom_palette = [mode_colors[mode] for mode in quality_df['Mode']]

plt.figure(figsize=(12, 6))
sns.barplot(x='Mode', y='Score', hue='Criterion', data=quality_melted, palette='tab10')
for p in plt.gca().patches:
    height = p.get_height()
    if height > 0:
        plt.gca().text(p.get_x() + p.get_width()/2, height + 0.1, f'{height:.2f}', 
                       ha='center', va='bottom', fontsize=8)
plt.title('So sánh chất lượng phản hồi giữa các chế độ truy vấn (top_k=6)')
plt.xlabel('Chế độ truy vấn')
plt.ylabel('Điểm trung bình')
plt.legend(title='Tiêu chí', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('./data/eval4/quality_comparison.png', dpi=300)
plt.show()

# Vẽ biểu đồ cột đôi so sánh thời gian và chất lượng
merged_data = stats.merge(quality_df[['Mode', 'Overall Score']], on='Mode')
fig, ax1 = plt.subplots(figsize=(10, 6))

# Thiết lập vị trí cột
bar_width = 0.35
x = np.arange(len(merged_data['Mode']))

# Vẽ cột thời gian
color_time = '#1f77b4'  # green
bars1 = ax1.bar(x - bar_width/2, merged_data['mean'], bar_width, label='Thời gian (giây)', color=color_time)
ax1.set_xlabel('Chế độ truy vấn')
ax1.set_ylabel('Thời gian trung bình (giây)', color=color_time)
ax1.tick_params(axis='y', labelcolor=color_time)

# Vẽ cột chất lượng 
color_quality = '#ff7f0e'  # orange
ax2 = ax1.twinx()
bars2 = ax2.bar(x + bar_width/2, merged_data['Overall Score'], bar_width, label='Chất lượng tổng thể', color=color_quality)
ax2.set_ylabel('Điểm chất lượng tổng thể', color=color_quality)
ax2.tick_params(axis='y', labelcolor=color_quality)

# Thêm giá trị lên trên cột
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height + 0.02, f'{height:.3f}', 
             ha='center', va='bottom', fontsize=10)
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height + 0.1, f'{height:.2f}', 
             ha='center', va='bottom', fontsize=10)

# Thiết lập tiêu đề và nhãn trục x
plt.title('So sánh thời gian phản hồi và chất lượng tổng thể (top_k=6)')
ax1.set_xticks(x)
ax1.set_xticklabels(merged_data['Mode'])

# Thêm chú thích
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.savefig('./data/eval4/time_quality_dual_bar.png', dpi=300)
plt.show()
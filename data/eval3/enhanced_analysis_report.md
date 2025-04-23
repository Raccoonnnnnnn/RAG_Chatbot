
# Báo cáo phân tích phản hồi Chatbot nâng cao

## Tổng quan
Báo cáo này phân tích mối quan hệ giữa các giá trị top-k (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30), thời gian phản hồi và chất lượng câu trả lời cho hai chatbot. Thời gian phản hồi được trích xuất từ các file log (hoặc mô phỏng nếu thiếu), và các chỉ số chất lượng được lấy từ file JSON.

## Phân tích thời gian phản hồi
- **File log**: data/eval3/topk2/time_responses_topk2.log, data/eval3/topk4/time_responses_topk4.log, data/eval3/topk6/time_responses_topk6.log, data/eval3/topk8/time_responses_topk8.log, data/eval3/topk10/time_responses_topk10.log, data/eval3/topk12/time_responses_topk12.log, data/eval3/topk14/time_responses_topk14.log, data/eval3/topk16/time_responses_topk16.log, data/eval3/topk18/time_responses_topk18.log, data/eval3/topk20/time_responses_topk20.log, data/eval3/topk22/time_responses_topk22.log, data/eval3/topk24/time_responses_topk24.log, data/eval3/topk26/time_responses_topk26.log, data/eval3/topk28/time_responses_topk28.log, data/eval3/topk30/time_responses_topk30.log.
- **Thời gian phản hồi trung bình**: ['10.78', '15.65', '16.66', '19.59', '22.46', '25.80', '30.67', '33.54', '38.92', '42.11', '47.93', '51.72', '54.95', '57.65', '61.76'] giây.
- **Độ lệch chuẩn**: ['3.77', '6.14', '5.49', '6.26', '7.57', '7.98', '8.96', '9.62', '10.42', '10.30', '11.05', '12.77', '12.34', '13.39', '14.10'] giây.
- **Nhận xét**: Thời gian phản hồi tăng khi giá trị top-k cao hơn, phản ánh yêu cầu tính toán lớn hơn.

## Phân tích chất lượng

### Top-k = 2
- **Tính toàn diện**: Câu trả lời 1: 80.00%, Câu trả lời 2: 20.00%.
- **Đa dạng**: Câu trả lời 1: 56.00%, Câu trả lời 2: 44.00%.
- **Trao quyền**: Câu trả lời 1: 73.60%, Câu trả lời 2: 26.40%.
- **Người thắng tổng thể**: Câu trả lời 1: 77.60%, Câu trả lời 2: 22.40%.

### Top-k = 4
- **Tính toàn diện**: Câu trả lời 1: 81.60%, Câu trả lời 2: 18.40%.
- **Đa dạng**: Câu trả lời 1: 64.00%, Câu trả lời 2: 36.00%.
- **Trao quyền**: Câu trả lời 1: 76.00%, Câu trả lời 2: 24.00%.
- **Người thắng tổng thể**: Câu trả lời 1: 78.40%, Câu trả lời 2: 21.60%.

### Top-k = 6
- **Tính toàn diện**: Câu trả lời 1: 90.32%, Câu trả lời 2: 9.68%.
- **Đa dạng**: Câu trả lời 1: 55.65%, Câu trả lời 2: 44.35%.
- **Trao quyền**: Câu trả lời 1: 81.45%, Câu trả lời 2: 18.55%.
- **Người thắng tổng thể**: Câu trả lời 1: 84.68%, Câu trả lời 2: 15.32%.

### Top-k = 8
- **Tính toàn diện**: Câu trả lời 1: 87.90%, Câu trả lời 2: 12.10%.
- **Đa dạng**: Câu trả lời 1: 58.87%, Câu trả lời 2: 41.13%.
- **Trao quyền**: Câu trả lời 1: 81.45%, Câu trả lời 2: 18.55%.
- **Người thắng tổng thể**: Câu trả lời 1: 83.06%, Câu trả lời 2: 16.94%.

### Top-k = 10
- **Tính toàn diện**: Câu trả lời 1: 86.40%, Câu trả lời 2: 13.60%.
- **Đa dạng**: Câu trả lời 1: 57.60%, Câu trả lời 2: 42.40%.
- **Trao quyền**: Câu trả lời 1: 79.20%, Câu trả lời 2: 20.80%.
- **Người thắng tổng thể**: Câu trả lời 1: 83.20%, Câu trả lời 2: 16.80%.

### Top-k = 12
- **Tính toàn diện**: Câu trả lời 1: 89.60%, Câu trả lời 2: 10.40%.
- **Đa dạng**: Câu trả lời 1: 61.60%, Câu trả lời 2: 38.40%.
- **Trao quyền**: Câu trả lời 1: 81.60%, Câu trả lời 2: 18.40%.
- **Người thắng tổng thể**: Câu trả lời 1: 85.60%, Câu trả lời 2: 14.40%.

### Top-k = 14
- **Tính toàn diện**: Câu trả lời 1: 87.20%, Câu trả lời 2: 12.80%.
- **Đa dạng**: Câu trả lời 1: 64.00%, Câu trả lời 2: 36.00%.
- **Trao quyền**: Câu trả lời 1: 81.60%, Câu trả lời 2: 18.40%.
- **Người thắng tổng thể**: Câu trả lời 1: 83.20%, Câu trả lời 2: 16.80%.

### Top-k = 16
- **Tính toàn diện**: Câu trả lời 1: 88.00%, Câu trả lời 2: 12.00%.
- **Đa dạng**: Câu trả lời 1: 60.80%, Câu trả lời 2: 39.20%.
- **Trao quyền**: Câu trả lời 1: 83.20%, Câu trả lời 2: 16.80%.
- **Người thắng tổng thể**: Câu trả lời 1: 85.60%, Câu trả lời 2: 14.40%.

### Top-k = 18
- **Tính toàn diện**: Câu trả lời 1: 90.40%, Câu trả lời 2: 9.60%.
- **Đa dạng**: Câu trả lời 1: 69.60%, Câu trả lời 2: 30.40%.
- **Trao quyền**: Câu trả lời 1: 89.60%, Câu trả lời 2: 10.40%.
- **Người thắng tổng thể**: Câu trả lời 1: 88.80%, Câu trả lời 2: 11.20%.

### Top-k = 20
- **Tính toàn diện**: Câu trả lời 1: 92.80%, Câu trả lời 2: 7.20%.
- **Đa dạng**: Câu trả lời 1: 72.80%, Câu trả lời 2: 27.20%.
- **Trao quyền**: Câu trả lời 1: 84.00%, Câu trả lời 2: 16.00%.
- **Người thắng tổng thể**: Câu trả lời 1: 88.80%, Câu trả lời 2: 11.20%.

### Top-k = 22
- **Tính toàn diện**: Câu trả lời 1: 94.40%, Câu trả lời 2: 5.60%.
- **Đa dạng**: Câu trả lời 1: 67.20%, Câu trả lời 2: 32.80%.
- **Trao quyền**: Câu trả lời 1: 88.80%, Câu trả lời 2: 11.20%.
- **Người thắng tổng thể**: Câu trả lời 1: 92.80%, Câu trả lời 2: 7.20%.

### Top-k = 24
- **Tính toàn diện**: Câu trả lời 1: 91.20%, Câu trả lời 2: 8.80%.
- **Đa dạng**: Câu trả lời 1: 67.20%, Câu trả lời 2: 32.80%.
- **Trao quyền**: Câu trả lời 1: 88.00%, Câu trả lời 2: 12.00%.
- **Người thắng tổng thể**: Câu trả lời 1: 88.00%, Câu trả lời 2: 12.00%.

### Top-k = 26
- **Tính toàn diện**: Câu trả lời 1: 87.20%, Câu trả lời 2: 12.80%.
- **Đa dạng**: Câu trả lời 1: 64.80%, Câu trả lời 2: 35.20%.
- **Trao quyền**: Câu trả lời 1: 84.00%, Câu trả lời 2: 16.00%.
- **Người thắng tổng thể**: Câu trả lời 1: 84.00%, Câu trả lời 2: 16.00%.

### Top-k = 28
- **Tính toàn diện**: Câu trả lời 1: 89.60%, Câu trả lời 2: 10.40%.
- **Đa dạng**: Câu trả lời 1: 63.20%, Câu trả lời 2: 36.80%.
- **Trao quyền**: Câu trả lời 1: 84.80%, Câu trả lời 2: 15.20%.
- **Người thắng tổng thể**: Câu trả lời 1: 87.20%, Câu trả lời 2: 12.80%.

### Top-k = 30
- **Tính toàn diện**: Câu trả lời 1: 94.40%, Câu trả lời 2: 5.60%.
- **Đa dạng**: Câu trả lời 1: 65.60%, Câu trả lời 2: 34.40%.
- **Trao quyền**: Câu trả lời 1: 88.00%, Câu trả lời 2: 12.00%.
- **Người thắng tổng thể**: Câu trả lời 1: 89.60%, Câu trả lời 2: 10.40%.

## Tương quan
- **Tương quan Pearson** (Thời gian phản hồi vs. Chất lượng tổng thể): 0.796.
- **Giải thích**: Tương quan dương cho thấy chất lượng cao hơn có thể đi kèm với thời gian phản hồi tăng, dù xu hướng thay đổi theo top-k.

## Trực quan hóa
- **Loại biểu đồ**: Biểu đồ đường hai trục.
- **Trục trái**: Thời gian phản hồi trung bình với thanh lỗi (độ lệch chuẩn).
- **Trục phải**: Chất lượng tổng thể cho Câu trả lời 1.
- **File**: Lưu tại './data/eval3/enhanced_response_analysis.png', '.pdf', và '.pkl'.

## Khuyến nghị
- **Top-k tối ưu**: Top-k = 5 hoặc 10 mang lại sự cân bằng tốt giữa chất lượng và thời gian phản hồi.
- **Thu thập dữ liệu**: Đảm bảo tất cả file log và JSON được tạo và chứa dữ liệu hợp lệ.
- **Tối ưu hóa**: Khám phá xử lý song song hoặc lưu trữ đệm để giảm thời gian phản hồi cho top-k cao hơn.


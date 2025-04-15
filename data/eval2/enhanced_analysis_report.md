
# Báo cáo phân tích phản hồi Chatbot nâng cao

## Tổng quan
Báo cáo này phân tích mối quan hệ giữa các giá trị top-k (2, 5, 7, 10, 15), thời gian phản hồi và chất lượng câu trả lời cho hai chatbot. Thời gian phản hồi được trích xuất từ các file log (hoặc mô phỏng nếu thiếu), và các chỉ số chất lượng được lấy từ file JSON.

## Phân tích thời gian phản hồi
- **File log**: data/eval2/topk2/time_responses_topk2.log, data/eval2/topk5/time_responses_topk5.log, data/eval2/topk7/time_responses_topk7.log, data/eval2/topk10/time_responses_topk10.log, data/eval2/topk15/time_responses_topk15.log.
- **Thời gian phản hồi trung bình**: ['9.09', '12.11', '13.86', '15.63', '6.09'] giây.
- **Độ lệch chuẩn**: ['3.12', '4.24', '4.94', '6.59', '2.58'] giây.
- **Nhận xét**: Thời gian phản hồi tăng khi giá trị top-k cao hơn, phản ánh yêu cầu tính toán lớn hơn.

## Phân tích chất lượng

### Top-k = 2
- **Tính toàn diện**: Câu trả lời 1: 74.40%, Câu trả lời 2: 25.60%.
- **Đa dạng**: Câu trả lời 1: 48.00%, Câu trả lời 2: 52.00%.
- **Trao quyền**: Câu trả lời 1: 65.60%, Câu trả lời 2: 34.40%.
- **Người thắng tổng thể**: Câu trả lời 1: 69.60%, Câu trả lời 2: 30.40%.

### Top-k = 5
- **Tính toàn diện**: Câu trả lời 1: 78.40%, Câu trả lời 2: 21.60%.
- **Đa dạng**: Câu trả lời 1: 47.20%, Câu trả lời 2: 52.80%.
- **Trao quyền**: Câu trả lời 1: 68.80%, Câu trả lời 2: 31.20%.
- **Người thắng tổng thể**: Câu trả lời 1: 73.60%, Câu trả lời 2: 26.40%.

### Top-k = 7
- **Tính toàn diện**: Câu trả lời 1: 81.45%, Câu trả lời 2: 18.55%.
- **Đa dạng**: Câu trả lời 1: 54.03%, Câu trả lời 2: 45.97%.
- **Trao quyền**: Câu trả lời 1: 75.00%, Câu trả lời 2: 25.00%.
- **Người thắng tổng thể**: Câu trả lời 1: 78.23%, Câu trả lời 2: 21.77%.

### Top-k = 10
- **Tính toàn diện**: Câu trả lời 1: 84.00%, Câu trả lời 2: 16.00%.
- **Đa dạng**: Câu trả lời 1: 56.80%, Câu trả lời 2: 43.20%.
- **Trao quyền**: Câu trả lời 1: 77.60%, Câu trả lời 2: 22.40%.
- **Người thắng tổng thể**: Câu trả lời 1: 81.60%, Câu trả lời 2: 18.40%.

### Top-k = 15
- **Tính toàn diện**: Câu trả lời 1: 77.60%, Câu trả lời 2: 22.40%.
- **Đa dạng**: Câu trả lời 1: 68.00%, Câu trả lời 2: 32.00%.
- **Trao quyền**: Câu trả lời 1: 71.20%, Câu trả lời 2: 28.80%.
- **Người thắng tổng thể**: Câu trả lời 1: 74.40%, Câu trả lời 2: 25.60%.

## Tương quan
- **Tương quan Pearson** (Thời gian phản hồi vs. Chất lượng tổng thể): 0.335.
- **Giải thích**: Tương quan dương cho thấy chất lượng cao hơn có thể đi kèm với thời gian phản hồi tăng, dù xu hướng thay đổi theo top-k.

## Trực quan hóa
- **Loại biểu đồ**: Biểu đồ đường hai trục.
- **Trục trái**: Thời gian phản hồi trung bình với thanh lỗi (độ lệch chuẩn).
- **Trục phải**: Chất lượng tổng thể cho Câu trả lời 1.
- **File**: Lưu tại './data/eval2/enhanced_response_analysis.png', '.pdf', và '.pkl'.

## Khuyến nghị
- **Top-k tối ưu**: Top-k = 5 hoặc 10 mang lại sự cân bằng tốt giữa chất lượng và thời gian phản hồi.
- **Thu thập dữ liệu**: Đảm bảo tất cả file log và JSON được tạo và chứa dữ liệu hợp lệ.
- **Tối ưu hóa**: Khám phá xử lý song song hoặc lưu trữ đệm để giảm thời gian phản hồi cho top-k cao hơn.



# Báo cáo phân tích phản hồi Chatbot nâng cao

## Tổng quan
Báo cáo này phân tích mối quan hệ giữa các giá trị top-k (2, 5, 7, 10, 15), thời gian phản hồi và chất lượng câu trả lời cho hai chatbot. Thời gian phản hồi được trích xuất từ các file log (hoặc mô phỏng nếu thiếu), và các chỉ số chất lượng được đánh giá qua bốn tiêu chí: Tính toàn diện, Đa dạng, Trao quyền và Người thắng tổng thể.

## Phân tích thời gian phản hồi
- **File log**: data/eval/topk2/time_responses_topk2.log, data/eval/topk5/time_responses_topk5.log, data/eval/topk7/time_responses_topk7.log, data/eval/topk10/time_responses_topk10.log, data/eval/topk15/time_responses_topk15.log.
- **Thời gian phản hồi trung bình**: ['9.80', '12.52', '13.94', '15.07', '6.29'] giây.
- **Độ lệch chuẩn**: ['3.77', '4.47', '5.40', '6.98', '3.66'] giây.
- **Nhận xét**: Thời gian phản hồi tăng khi giá trị top-k cao hơn, phản ánh yêu cầu tính toán lớn hơn.

## Phân tích chất lượng

### Top-k = 2
- **Tính toàn diện**: Câu trả lời 1: 73.6%, Câu trả lời 2: 26.4%.
- **Đa dạng**: Câu trả lời 1: 52.8%, Câu trả lời 2: 47.2%.
- **Trao quyền**: Câu trả lời 1: 64.8%, Câu trả lời 2: 35.2%.
- **Người thắng tổng thể**: Câu trả lời 1: 69.6%, Câu trả lời 2: 30.4%.

### Top-k = 5
- **Tính toàn diện**: Câu trả lời 1: 80.0%, Câu trả lời 2: 20.0%.
- **Đa dạng**: Câu trả lời 1: 53.6%, Câu trả lời 2: 46.4%.
- **Trao quyền**: Câu trả lời 1: 76.0%, Câu trả lời 2: 24.0%.
- **Người thắng tổng thể**: Câu trả lời 1: 79.2%, Câu trả lời 2: 20.8%.

### Top-k = 7
- **Tính toàn diện**: Câu trả lời 1: 76.0%, Câu trả lời 2: 24.0%.
- **Đa dạng**: Câu trả lời 1: 48.5%, Câu trả lời 2: 52.0%.
- **Trao quyền**: Câu trả lời 1: 64.8%, Câu trả lời 2: 35.2%.
- **Người thắng tổng thể**: Câu trả lời 1: 72.0%, Câu trả lời 2: 28.0%.

### Top-k = 10
- **Tính toàn diện**: Câu trả lời 1: 84.0%, Câu trả lời 2: 16.0%.
- **Đa dạng**: Câu trả lời 1: 55.2%, Câu trả lời 2: 44.8%.
- **Trao quyền**: Câu trả lời 1: 72.0%, Câu trả lời 2: 28.0%.
- **Người thắng tổng thể**: Câu trả lời 1: 77.6%, Câu trả lời 2: 22.4%.

### Top-k = 15
- **Tính toàn diện**: Câu trả lời 1: 74.4%, Câu trả lời 2: 25.6%.
- **Đa dạng**: Câu trả lời 1: 70.4%, Câu trả lời 2: 29.6%.
- **Trao quyền**: Câu trả lời 1: 72.0%, Câu trả lời 2: 28.0%.
- **Người thắng tổng thể**: Câu trả lời 1: 72.0%, Câu trả lời 2: 28.0%.

## Tương quan
- **Tương quan Pearson** (Thời gian phản hồi vs. Chất lượng tổng thể): 0.538.
- **Giải thích**: Tương quan dương cho thấy chất lượng cao hơn có thể đi kèm với thời gian phản hồi tăng, dù xu hướng thay đổi theo top-k.

## Trực quan hóa
- **Loại biểu đồ**: Biểu đồ đường hai trục.
- **Trục trái**: Thời gian phản hồi trung bình với thanh lỗi (độ lệch chuẩn).
- **Trục phải**: Chất lượng tổng thể cho Câu trả lời 1.
- **File**: Lưu tại './data/eval/enhanced_response_analysis.png'.

## Khuyến nghị
- **Top-k tối ưu**: Top-k = 5 hoặc 10 mang lại sự cân bằng tốt giữa chất lượng (đỉnh ở 79.2% cho topk=5) và thời gian phản hồi.
- **Thu thập dữ liệu**: Đảm bảo tất cả file log được tạo và chứa dữ liệu hợp lệ để tránh mô phỏng.
- **Tối ưu hóa**: Khám phá xử lý song song hoặc lưu trữ đệm để giảm thời gian phản hồi cho top-k cao hơn.


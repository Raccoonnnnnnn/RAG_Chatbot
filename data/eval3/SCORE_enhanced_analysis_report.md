
# Báo cáo phân tích phản hồi Chatbot nâng cao

## Tổng quan
Báo cáo này phân tích mối quan hệ giữa các giá trị top-k (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30), thời gian phản hồi và chất lượng câu trả lời cho một chatbot. Thời gian phản hồi được trích xuất từ các file log (hoặc mô phỏng nếu thiếu), và các chỉ số chất lượng được lấy từ file JSON.

## Phân tích thời gian phản hồi
- **File log**: data/eval3/topk2/time_responses_topk2.log, data/eval3/topk4/time_responses_topk4.log, data/eval3/topk6/time_responses_topk6.log, data/eval3/topk8/time_responses_topk8.log, data/eval3/topk10/time_responses_topk10.log, data/eval3/topk12/time_responses_topk12.log, data/eval3/topk14/time_responses_topk14.log, data/eval3/topk16/time_responses_topk16.log, data/eval3/topk18/time_responses_topk18.log, data/eval3/topk20/time_responses_topk20.log, data/eval3/topk22/time_responses_topk22.log, data/eval3/topk24/time_responses_topk24.log, data/eval3/topk26/time_responses_topk26.log, data/eval3/topk28/time_responses_topk28.log, data/eval3/topk30/time_responses_topk30.log.
- **Thời gian phản hồi trung bình**: ['10.78', '15.65', '16.66', '19.59', '22.46', '25.80', '30.67', '33.54', '38.92', '42.11', '47.93', '51.72', '54.95', '57.65', '61.76'] giây.
- **Độ lệch chuẩn**: ['3.77', '6.14', '5.49', '6.26', '7.57', '7.98', '8.96', '9.62', '10.42', '10.30', '11.05', '12.77', '12.34', '13.39', '14.10'] giây.
- **Nhận xét**: Thời gian phản hồi tăng khi giá trị top-k cao hơn, phản ánh yêu cầu tính toán lớn hơn.

## Phân tích chất lượng

### Top-k = 2
- **Tính toàn diện**: Điểm trung bình: 7.20 (Std: 1.89).
- **Đa dạng**: Điểm trung bình: 4.01 (Std: 1.25).
- **Trao quyền**: Điểm trung bình: 6.60 (Std: 1.25).
- **Liên quan**: Điểm trung bình: 7.48 (Std: 2.27).
- **Tổng thể**: Điểm trung bình: 6.07 (Std: 1.26).

### Top-k = 4
- **Tính toàn diện**: Điểm trung bình: 7.66 (Std: 1.70).
- **Đa dạng**: Điểm trung bình: 4.35 (Std: 1.49).
- **Trao quyền**: Điểm trung bình: 6.93 (Std: 1.29).
- **Liên quan**: Điểm trung bình: 7.84 (Std: 2.49).
- **Tổng thể**: Điểm trung bình: 6.44 (Std: 1.40).

### Top-k = 6
- **Tính toàn diện**: Điểm trung bình: 7.72 (Std: 1.55).
- **Đa dạng**: Điểm trung bình: 4.35 (Std: 1.30).
- **Trao quyền**: Điểm trung bình: 7.00 (Std: 1.15).
- **Liên quan**: Điểm trung bình: 8.15 (Std: 2.26).
- **Tổng thể**: Điểm trung bình: 6.56 (Std: 1.15).

### Top-k = 8
- **Tính toàn diện**: Điểm trung bình: 7.72 (Std: 1.53).
- **Đa dạng**: Điểm trung bình: 4.33 (Std: 1.37).
- **Trao quyền**: Điểm trung bình: 6.88 (Std: 1.16).
- **Liên quan**: Điểm trung bình: 8.10 (Std: 2.24).
- **Tổng thể**: Điểm trung bình: 6.53 (Std: 1.22).

### Top-k = 10
- **Tính toàn diện**: Điểm trung bình: 7.65 (Std: 1.52).
- **Đa dạng**: Điểm trung bình: 4.42 (Std: 1.46).
- **Trao quyền**: Điểm trung bình: 6.89 (Std: 1.17).
- **Liên quan**: Điểm trung bình: 8.20 (Std: 2.11).
- **Tổng thể**: Điểm trung bình: 6.57 (Std: 1.13).

### Top-k = 12
- **Tính toàn diện**: Điểm trung bình: 7.70 (Std: 1.64).
- **Đa dạng**: Điểm trung bình: 4.44 (Std: 1.39).
- **Trao quyền**: Điểm trung bình: 6.93 (Std: 1.25).
- **Liên quan**: Điểm trung bình: 8.25 (Std: 2.10).
- **Tổng thể**: Điểm trung bình: 6.58 (Std: 1.23).

### Top-k = 14
- **Tính toàn diện**: Điểm trung bình: 7.84 (Std: 1.48).
- **Đa dạng**: Điểm trung bình: 4.66 (Std: 1.47).
- **Trao quyền**: Điểm trung bình: 6.99 (Std: 1.21).
- **Liên quan**: Điểm trung bình: 8.42 (Std: 1.96).
- **Tổng thể**: Điểm trung bình: 6.71 (Std: 1.19).

### Top-k = 16
- **Tính toàn diện**: Điểm trung bình: 7.78 (Std: 1.43).
- **Đa dạng**: Điểm trung bình: 4.61 (Std: 1.36).
- **Trao quyền**: Điểm trung bình: 7.04 (Std: 1.13).
- **Liên quan**: Điểm trung bình: 8.58 (Std: 1.91).
- **Tổng thể**: Điểm trung bình: 6.75 (Std: 1.08).

### Top-k = 18
- **Tính toàn diện**: Điểm trung bình: 7.90 (Std: 1.42).
- **Đa dạng**: Điểm trung bình: 4.81 (Std: 1.43).
- **Trao quyền**: Điểm trung bình: 7.15 (Std: 1.08).
- **Liên quan**: Điểm trung bình: 8.60 (Std: 1.98).
- **Tổng thể**: Điểm trung bình: 6.87 (Std: 1.16).

### Top-k = 20
- **Tính toàn diện**: Điểm trung bình: 7.91 (Std: 1.49).
- **Đa dạng**: Điểm trung bình: 4.68 (Std: 1.66).
- **Trao quyền**: Điểm trung bình: 7.17 (Std: 1.08).
- **Liên quan**: Điểm trung bình: 8.58 (Std: 1.95).
- **Tổng thể**: Điểm trung bình: 6.82 (Std: 1.17).

### Top-k = 22
- **Tính toàn diện**: Điểm trung bình: 7.81 (Std: 1.38).
- **Đa dạng**: Điểm trung bình: 4.62 (Std: 1.53).
- **Trao quyền**: Điểm trung bình: 7.05 (Std: 1.12).
- **Liên quan**: Điểm trung bình: 8.27 (Std: 2.16).
- **Tổng thể**: Điểm trung bình: 6.71 (Std: 1.12).

### Top-k = 24
- **Tính toàn diện**: Điểm trung bình: 7.95 (Std: 1.50).
- **Đa dạng**: Điểm trung bình: 4.78 (Std: 1.47).
- **Trao quyền**: Điểm trung bình: 7.15 (Std: 1.04).
- **Liên quan**: Điểm trung bình: 8.60 (Std: 1.99).
- **Tổng thể**: Điểm trung bình: 6.86 (Std: 1.14).

### Top-k = 26
- **Tính toàn diện**: Điểm trung bình: 7.85 (Std: 1.54).
- **Đa dạng**: Điểm trung bình: 4.60 (Std: 1.46).
- **Trao quyền**: Điểm trung bình: 6.98 (Std: 1.29).
- **Liên quan**: Điểm trung bình: 8.57 (Std: 1.92).
- **Tổng thể**: Điểm trung bình: 6.74 (Std: 1.23).

### Top-k = 28
- **Tính toàn diện**: Điểm trung bình: 7.69 (Std: 1.45).
- **Đa dạng**: Điểm trung bình: 4.38 (Std: 1.46).
- **Trao quyền**: Điểm trung bình: 6.86 (Std: 1.12).
- **Liên quan**: Điểm trung bình: 8.51 (Std: 1.78).
- **Tổng thể**: Điểm trung bình: 6.62 (Std: 1.14).

### Top-k = 30
- **Tính toàn diện**: Điểm trung bình: 7.85 (Std: 1.60).
- **Đa dạng**: Điểm trung bình: 4.67 (Std: 1.45).
- **Trao quyền**: Điểm trung bình: 7.06 (Std: 1.14).
- **Liên quan**: Điểm trung bình: 8.61 (Std: 1.84).
- **Tổng thể**: Điểm trung bình: 6.82 (Std: 1.22).

## Tương quan
- **Tương quan Pearson** (Thời gian phản hồi vs. Chất lượng trung bình): 0.719.
- **Giải thích**: Tương quan dương cho thấy chất lượng cao hơn có thể đi kèm với thời gian phản hồi tăng, dù xu hướng thay đổi theo top-k.

## Trực quan hóa
- **Biểu đồ 1**: Biểu đồ đường hai trục, so sánh thời gian phản hồi trung bình (giây) và chất lượng phản hồi trung bình (điểm 1-10).
- **Biểu đồ 2**: Biểu đồ đường hiển thị chất lượng phản hồi theo bốn tiêu chí (Tính toàn diện, Đa dạng, Trao quyền, Liên quan).
- **File**: Lưu tại './data/eval3/enhanced_response_analysis.pkl' và './data/eval3/criteria_quality_analysis.pkl'.

## Khuyến nghị
- **Top-k tối ưu**: Top-k = 5 hoặc 10 mang lại sự cân bằng tốt giữa chất lượng và thời gian phản hồi.
- **Thu thập dữ liệu**: Đảm bảo tất cả file log và JSON được tạo và chứa dữ liệu hợp lệ.
- **Tối ưu hóa**: Khám phá xử lý song song hoặc lưu trữ đệm để giảm thời gian phản hồi cho top-k cao hơn.

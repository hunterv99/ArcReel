# Tham chiếu Chế độ nội dung (Content Modes)

Chuyển đổi qua trường `content_mode` trong `project.json`. Các script của mỗi skill sẽ tự động đọc và áp dụng đặc tả tương ứng, không cần chỉ định tỷ lệ khung hình trong prompt.

| Tiêu chí | Kể chuyện + Hình ảnh (narration, mặc định) | Hoạt hình / Phim ngắn (drama) |
|------|---------------------------|-----------------|
| Cấu trúc dữ liệu | Mảng `segments` | Mảng `scenes` |
| Tỷ lệ khung hình | 9:16 Dọc | 16:9 Ngang |
| Thời lượng mặc định | 4 giây / đoạn | 8 giây / cảnh |
| Lựa chọn thời lượng | 4s / 6s / 8s | 4s / 6s / 8s |
| Nguồn đối thoại | Lồng tiếng sau (văn bản tiểu thuyết) | Đối thoại trực tiếp của diễn viên |
| Prompt Video | Chỉ bao gồm lời thoại nhân vật (nếu có), không có lời dẫn | Bao gồm lời thoại, lời dẫn, hiệu ứng âm thanh |
| Agent tiền xử lý | split-narration-segments | normalize-drama-script |

## Đặc tả Video

- **Độ phân giải**: Hình ảnh 1K, Video 1080p
- **Phương thức tạo**: Mỗi đoạn/cảnh được tạo độc lập, sử dụng ảnh phân cảnh làm khung hình bắt đầu
- **Cách ghép nối**: Sử dụng ffmpeg để ghép các đoạn độc lập, không dùng tính năng extend của Veo để nối cảnh
- **BGM (Nhạc nền)**: Được loại bỏ tự động qua tham số `negative_prompt` của API, sau đó thêm vào ở bước compose-video

## Lưu ý về Veo 3.1 extend

- Chỉ dùng để kéo dài **một** đoạn/cảnh đơn lẻ (mỗi lần +7 giây, tối đa 148 giây)
- **Chỉ hỗ trợ 720p**, độ phân giải 1080p không thể kéo dài
- Không thích hợp để nối các cảnh quay khác nhau

## Ngôn ngữ cho Prompt

- Prompt tạo hình ảnh/video nên sử dụng **tiếng Anh** (để đạt hiệu quả tốt nhất)
- Sử dụng mô tả kiểu tường thuật, không dùng liệt kê từ khóa

> Tham khảo `docs/google-genai-docs/nano-banana.md` từ dòng 365 về Hướng dẫn và chiến lược gợi ý (Prompting guide and strategies).

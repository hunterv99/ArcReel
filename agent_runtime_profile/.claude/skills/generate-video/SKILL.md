---
name: generate-video
description: Tạo các đoạn video từ các cảnh trong kịch bản. Sử dụng khi người dùng yêu cầu "tạo video", "biến ảnh phân cảnh thành video", muốn tạo lại video cho một cảnh cụ thể, hoặc khi quá trình tạo video bị gián đoạn và cần tiếp tục. Hỗ trợ các chế độ tạo hàng loạt theo tập, tạo từng cảnh, hoặc tiếp tục từ điểm dừng.
---

# Tạo Video

Sử dụng Veo 3.1 API để tạo video cho mỗi cảnh/đoạn, lấy ảnh phân cảnh (storyboard) làm khung hình bắt đầu.

> Các thông số như tỷ lệ khung hình, thời lượng, độ phân giải được script tự động thiết lập dựa trên `content_mode`, chi tiết xem tại `.claude/references/content-modes.md`.

## Cách dùng dòng lệnh

```bash
# Chế độ tiêu chuẩn: Tạo tất cả các cảnh đang chờ xử lý trong toàn tập (khuyên dùng)
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --episode {N}

# Tiếp tục từ điểm dừng: Tiếp tục từ vị trí bị gián đoạn trước đó
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --episode {N} --resume

# Từng cảnh riêng lẻ: Kiểm tra hoặc tạo lại một cảnh
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --scene E1S1

# Hàng loạt tự chọn: Chỉ định nhiều cảnh cụ thể
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --scenes E1S01,E1S05,E1S10

# Tất cả đang chờ xử lý
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --all
```

> Tất cả các tác vụ được gửi một lần vào hàng đợi tạo, Worker sẽ tự động điều phối dựa trên cấu hình đồng thời của từng nhà cung cấp (per-provider).

## Quy trình làm việc

1. **Tải dự án và kịch bản** — Xác nhận tất cả các cảnh đều có `storyboard_image`.
2. **Tạo video** — Script tự động xây dựng Prompt, gọi API và lưu điểm kiểm tra (checkpoint).
3. **Kiểm tra điểm chốt (Checkpoint)** — Hiển thị kết quả, người dùng có thể yêu cầu tạo lại các cảnh chưa ưng ý.
4. **Cập nhật kịch bản** — Tự động cập nhật đường dẫn `video_clip` và trạng thái cảnh quay.

## Xây dựng Prompt

Prompt được script tự động xây dựng bên trong, chọn chiến lược khác nhau tùy theo `content_mode`. Script đọc các trường sau từ kịch bản JSON:

**image_prompt** (dùng để tham chiếu ảnh phân cảnh): scene, composition (shot_type, lighting, ambiance).

**video_prompt** (dùng để tạo video): action, camera_motion, ambiance_audio, dialogue, narration (chỉ áp dụng cho drama).

- Chế độ kể chuyện (Narration): `novel_text` không tham gia vào việc tạo video (lồng tiếng sau này), `dialogue` chỉ bao gồm lời thoại của nhân vật trong nguyên tác.
- Chế độ phim ngắn (Drama): Bao gồm đầy đủ lời thoại, lời dẫn và hiệu ứng âm thanh.
- Negative prompt tự động loại bỏ nhạc nền (BGM).

## Kiểm tra trước khi tạo

- [ ] Tất cả các cảnh đều có ảnh phân cảnh đã được phê duyệt.
- [ ] Độ dài văn bản đối thoại phù hợp.
- [ ] Mô tả hành động rõ ràng và đơn giản.

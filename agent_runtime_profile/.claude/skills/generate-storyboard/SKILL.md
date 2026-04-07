---
name: generate-storyboard
description: Tạo hình ảnh phân cảnh (storyboard) cho các cảnh trong kịch bản. Sử dụng khi người dùng yêu cầu "tạo phân cảnh", "xem trước hình ảnh cảnh", muốn tạo lại một số hình ảnh phân cảnh, hoặc khi kịch bản thiếu hình ảnh phân cảnh. Tự động duy trì tính liên tục của nhân vật và hình ảnh.
---

# Tạo hình ảnh phân cảnh (Storyboard)

Tạo hình ảnh phân cảnh thông qua hàng đợi tạo (generation queue), tỷ lệ khung hình được thiết lập tự động dựa trên `content_mode`.

> Chi tiết về đặc tả chế độ nội dung xem tại `.claude/references/content-modes.md`.

## Cách dùng dòng lệnh

```bash
# Thêm tất cả các phân cảnh còn thiếu vào hàng đợi tạo (tự động phát hiện content_mode)
python .claude/skills/generate-storyboard/scripts/generate_storyboard.py script.json

# Tạo lại cho một cảnh duy nhất
python .claude/skills/generate-storyboard/scripts/generate_storyboard.py script.json --scene E1S05

# Tạo lại cho nhiều cảnh
python .claude/skills/generate-storyboard/scripts/generate_storyboard.py script.json --scene-ids E1S01 E1S02
```

> `--scene-ids` và `--segment-ids` là các tên gọi tương đương (cái sau thường dùng cho chế độ narration), có hiệu quả giống nhau. Dưới đây thống nhất dùng `--scene-ids`.

> **Quy tắc lựa chọn**: `--scene` tạo lại một cảnh; `--scene-ids` tạo lại nhiều cảnh; nếu không cung cấp tham số nào sẽ tạo tất cả các mục còn thiếu.

> **Lưu ý**: Script yêu cầu generation worker phải đang chạy (online), worker chịu trách nhiệm tạo hình ảnh thực tế và kiểm soát tốc độ.

## Quy trình làm việc

1. **Tải dự án và kịch bản** — Xác nhận tất cả các nhân vật đều có hình ảnh `character_sheet`.
2. **Tạo hình ảnh phân cảnh** — Script tự động phát hiện content_mode, liên kết các tác vụ dựa trên mối quan hệ liền kề.
3. **Kiểm tra điểm chốt (Checkpoint)** — Hiển thị từng hình ảnh phân cảnh, người dùng có thể chấp thuận hoặc yêu cầu tạo lại.
4. **Cập nhật kịch bản** — Cập nhật đường dẫn `storyboard_image` và trạng thái cảnh quay.

## Cơ chế nhất quán nhân vật

Script tự động xử lý các hình ảnh tham chiếu truyền vào, không cần chỉ định thủ công:
- **character_sheet**: Hình thiết kế của các nhân vật xuất hiện trong cảnh, giúp giữ ngoại hình nhất quán.
- **clue_sheet**: Hình thiết kế của các manh mối xuất hiện trong cảnh.
- **Hình phân cảnh trước đó**: Mặc định được tham chiếu cho các đoạn liền kề để tăng tính liên tục của hình ảnh.
- Khi một đoạn được đánh dấu `segment_break=true`, việc tham chiếu hình ảnh trước đó sẽ bị bỏ qua.

## Mẫu Prompt

Script đọc các trường sau từ kịch bản JSON để xây dựng prompt:

```
Storyboard cho cảnh [scene_id/segment_id]:

- Mô tả hình ảnh: [visual.description]
- Bố cục khung hình: [visual.shot_type]
- Điểm bắt đầu chuyển động camera: [visual.camera_movement]
- Điều kiện ánh sáng: [visual.lighting]
- Không khí hình ảnh: [visual.mood]
- Nhân vật: [characters_in_scene]
- Hành động: [action]

Yêu cầu phong cách: Phong cách hình ảnh phân cảnh điện ảnh, dựa trên thiết lập style của dự án.
Nhân vật phải hoàn toàn nhất quán với hình ảnh tham chiếu nhân vật được cung cấp.
```

> Tỷ lệ khung hình được thiết lập qua tham số API, không viết vào prompt.

## Kiểm tra trước khi tạo

- [ ] Tất cả nhân vật đều có hình ảnh `character_sheet` đã được chấp thuận.
- [ ] Mô tả hình ảnh cảnh quay đầy đủ.
- [ ] Hành động của nhân vật đã được chỉ định.

## Xử lý lỗi

- Lỗi ở một cảnh đơn lẻ không ảnh hưởng đến toàn bộ lô, ghi lại cảnh thất bại và tiếp tục.
- Kết thúc quá trình sẽ báo cáo tổng hợp tất cả các cảnh thất bại và nguyên nhân.
- Hỗ trợ tạo gia tăng (bỏ qua các cảnh đã tồn tại).
- Sử dụng `--scene-ids` để tạo lại các cảnh bị thất bại.

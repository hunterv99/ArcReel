---
name: generate-script
description: Sử dụng Gemini API để tạo kịch bản JSON. Được gọi bởi subagent create-episode-script. Đọc các tệp trung gian và project.json, gọi Gemini để tạo kịch bản JSON tuân thủ mô hình Pydantic.
user-invocable: false
---

# generate-script

Sử dụng Gemini API để tạo kịch bản JSON. Kỹ năng này được gọi bởi subagent `create-episode-script`, không dùng để tương tác trực tiếp với người dùng.

## Điều kiện tiên quyết

1. Thư mục dự án phải có tệp `project.json` (chứa style, overview, characters, clues).
2. Đã hoàn thành tiền xử lý Bước 1 (Step 1):
   - narration: `drafts/episode_N/step1_segments.md`
   - drama: `drafts/episode_N/step1_normalized_script.md`

## Cách dùng

```bash
# Tạo kịch bản cho tập phim cụ thể
python .claude/skills/generate-script/scripts/generate_script.py --episode {N}

# Tùy chỉnh đường dẫn đầu ra
python .claude/skills/generate-script/scripts/generate_script.py --episode {N} --output scripts/ep1.json

# Xem trước Prompt (không thực sự gọi API)
python .claude/skills/generate-script/scripts/generate_script.py --episode {N} --dry-run
```

## Quy trình tạo

Script bên trong hoàn thành các bước sau thông qua `ScriptGenerator`:

1. **Tải project.json** — Đọc content_mode, characters, clues, overview, style.
2. **Tải tệp trung gian Bước 1** — Chọn `step1_segments.md` (narration) hoặc `step1_normalized_script.md` (drama) tùy theo content_mode.
3. **Xây dựng Prompt** — Kết hợp nội dung sơ lược dự án, phong cách, nhân vật, manh mối và tệp trung gian thành một prompt hoàn chỉnh.
4. **Gọi Gemini API** — Sử dụng mô hình `gemini-3-flash-preview`, truyền Pydantic schema làm `response_schema` để ép kiểu định dạng đầu ra.
5. **Xác thực Pydantic** — Sử dụng `NarrationEpisodeScript` (narration) hoặc `DramaEpisodeScript` (drama) để kiểm tra tính hợp lệ của JSON trả về.
6. **Bổ sung siêu dữ liệu** — Ghi thêm episode, content_mode, số liệu thống kê (số đoạn/cảnh, tổng thời lượng), dấu thời gian.

## Định dạng đầu ra

Tệp JSON được tạo sẽ lưu vào `scripts/episode_N.json`, cấu trúc cốt lõi:

- `episode`, `content_mode`, `novel` (title, chapter, source_file).
- Chế độ narration: mảng `segments` (mỗi đoạn bao gồm visual, novel_text, duration_seconds, v.v.).
- Chế độ drama: mảng `scenes` (mỗi cảnh bao gồm visual, dialogue, action, duration_seconds, v.v.).
- `metadata`: total_segments/total_scenes, created_at, generator.
- `duration_seconds`: Tổng thời lượng của toàn tập (giây).

## Đầu ra của `--dry-run`

In ra toàn bộ nội dung prompt sẽ gửi tới Gemini, không gọi API, không ghi tệp. Dùng để kiểm tra chất lượng và độ dài của prompt.

> Chi tiết về đặc tả của hai chế độ được hỗ trợ xem tại `.claude/references/content-modes.md`.

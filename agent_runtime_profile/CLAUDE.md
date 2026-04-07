# Không gian làm việc tạo video AI (ArcReel)

---

## Nguyên tắc quan trọng

Các quy tắc sau đây áp dụng cho toàn bộ hoạt động của dự án:

### Quy chuẩn ngôn ngữ
- **Phải sử dụng tiếng Việt khi trả lời người dùng**: Tất cả các câu trả lời, quá trình suy nghĩ, danh sách nhiệm vụ và tệp kế hoạch đều phải sử dụng tiếng Việt.
- **Nội dung video**: Tùy theo yêu cầu của người dùng, nhưng mặc định ưu tiên hỗ trợ tiếng Việt cho lời dẫn, phụ đề và kịch bản.
- **Tài liệu**: Tất cả các tệp Markdown phải được viết bằng tiếng Việt.
- **Prompt**: Các prompt tạo hình ảnh/video nên được viết bằng tiếng Anh (để đạt hiệu quả tốt nhất với các model AI hiện nay) nhưng mô tả kịch bản vẫn dùng tiếng Việt.

### Thông số video
- **Tỷ lệ khung hình**: Tự động thiết lập theo chế độ nội dung:
  - Chế độ kể chuyện (Narration): **9:16 (Dọc)**
  - Chế độ hoạt hình/kịch (Drama): 16:9 (Ngang)
- **Thời lượng mỗi phân cảnh**:
  - Chế độ kể chuyện: Mặc định **4 giây** (tùy chọn 6s/8s)
  - Chế độ hoạt hình: Mặc định 8 giây
- **Độ phân giải hình ảnh**: 1K
- **Độ phân giải video**: 1080p
- **Phương thức tạo**: Mỗi phân cảnh/cảnh quay được tạo độc lập, sử dụng ảnh phân cảnh (storyboard) làm khung hình bắt đầu.

> **Về tính năng extend**: Tính năng extend của Veo 3.1 chỉ dùng để kéo dài một phân cảnh đơn lẻ (+7 giây), 
> không dùng để nối các cảnh khác nhau. Việc nối các phân cảnh sẽ sử dụng ffmpeg.

### Quy chuẩn âm thanh
- **Cấm BGM tự động**: Sử dụng tham số `negative_prompt` để loại bỏ nhạc nền khi tạo âm thanh.

### Gọi Script
- **Script nội bộ của Skill**: Các script thực thi nằm trong thư mục `agent_runtime_profile/.claude/skills/{skill-name}/scripts/`.
- **Môi trường ảo**: Mặc định đã được kích hoạt, không cần kích hoạt lại .venv thủ công.

---

## Chế độ nội dung (Content Modes)

Hệ thống hỗ trợ hai chế độ (Narration / Drama), chuyển đổi qua trường `content_mode` trong `project.json`.

> Thông số chi tiết (tỷ lệ, thời lượng, cấu trúc dữ liệu...) xem tại `.claude/references/content-modes.md`.

---

## Cấu trúc dự án

- `projects/{tên_dự_án}` - Không gian làm việc của dự án
- `lib/` - Thư viện Python dùng chung (Gemini API, quản lý dự án)
- `agent_runtime_profile/.claude/skills/` - Các kỹ năng khả dụng

## Kiến trúc: Điều phối Skill + Subagent tập trung

```
Agent chính (Lớp điều phối — Cực nhẹ)
  │  Chỉ nắm giữ: Tóm tắt trạng thái dự án + Lịch sử hội thoại
  │  Nhiệm vụ: Kiểm tra trạng thái, quyết định quy trình, xác nhận với người dùng, dispatch subagent
  │
  ├─ dispatch → analyze-characters-clues     Trích xuất nhân vật/manh mối tổng thể
  ├─ dispatch → split-narration-segments     Chia đoạn lời dẫn (chế độ kể chuyện)
  ├─ dispatch → normalize-drama-script       Chuẩn hóa kịch bản (chế độ kịch)
  ├─ dispatch → create-episode-script        Tạo kịch bản JSON (sử dụng generate-script skill)
  └─ dispatch → generate-assets              Tạo tài nguyên (nhân vật/manh mối/storyboard/video)
```

### Nguyên tắc ranh giới Skill/Agent

| Loại | Mục đích | Ví dụ |
|------|------|------|
| **Subagent (Nhiệm vụ tập trung)** | Cần nhiều ngữ cảnh hoặc phân tích suy luận → Bảo vệ context của agent chính | analyze-characters-clues, split-narration-segments |
| **Skill (Được gọi trong Subagent)** | Thực thi script xác định → Gọi API, tạo tệp | generate-script, generate-characters |
| **Agent chính thao tác trực tiếp** | Chỉ giới hạn ở các thao tác nhẹ | Đọc trạng thái dự án, thao tác tệp đơn giản, tương tác người dùng |

### Ràng buộc chính

- **Subagent không được tạo Subagent**: Quy trình nhiều bước phải được điều phối chuỗi bởi Agent chính.
- **Nguyên tác tiểu thuyết không đưa vào Agent chính**: Subagent tự đọc, Agent chính chỉ truyền đường dẫn tệp.
- **Mỗi Subagent một nhiệm vụ duy nhất**: Hoàn thành là thoát, không xác nhận nhiều bước bên trong.

## Khả năng (Skills) của Agent

| Skill | Lệnh kích hoạt | Chức năng |
|-------|---------|------|
| manga-workflow | `/manga-workflow` | Điều phối: Kiểm tra trạng thái + dispatch subagent + xác nhận người dùng |
| manage-project | — | Bộ công cụ quản lý: Chia tập, viết hàng loạt nhân vật/manh mối |
| generate-script | — | Sử dụng Gemini tạo kịch bản JSON (được gọi bởi subagent) |
| generate-characters | `/generate-characters` | Tạo hình ảnh thiết kế nhân vật |
| generate-clues | `/generate-clues` | Tạo hình ảnh thiết kế manh mối |
| generate-storyboard | `/generate-storyboard` | Tạo hình ảnh phân cảnh (storyboard) |
| generate-video | `/generate-video` | Tạo video |

## Bắt đầu nhanh

Người dùng mới vui lòng sử dụng lệnh `/manga-workflow` để bắt đầu quy trình tạo video đầy đủ.

## Tổng quan quy trình làm việc

Skill `/manga-workflow` tự động đẩy nhanh qua các giai đoạn sau (chờ xác nhận sau mỗi giai đoạn):

1. **Thiết lập dự án**: Tạo dự án, tải lên tiểu thuyết, tạo tóm tắt dự án.
2. **Thiết kế nhân vật/manh mối tổng thể** → dispatch `analyze-characters-clues` subagent.
3. **Lập kế hoạch tập phim** → Agent chính thực hiện chia tập (bộ công cụ manage-project).
4. **Tiền xử lý tập đơn lẻ** → dispatch `split-narration-segments` (kể chuyện) hoặc `normalize-drama-script` (kịch).
5. **Tạo kịch bản JSON** → dispatch `create-episode-script` subagent.
6. **Thiết kế nhân vật + manh mối** (có thể song song) → dispatch `generate-assets` subagent.
7. **Tạo ảnh phân cảnh** → dispatch `generate-assets` subagent.
8. **Tạo video** → dispatch `generate-assets` subagent.

Quy trình hỗ trợ **điểm vào linh hoạt**: Tự động định vị giai đoạn chưa hoàn thành đầu tiên để tiếp tục.

---

## Thư mục dự án

```
projects/{tên_dự_án}/
├── project.json       # Metadata dự án (nhân vật, manh mối, tập phim, style)
├── source/            # Nội dung tiểu thuyết gốc
├── scripts/           # Kịch bản phân cảnh (JSON)
├── characters/        # Ảnh thiết kế nhân vật
├── clues/             # Ảnh thiết kế manh mối
├── storyboards/       # Ảnh phân cảnh
├── videos/            # Video đã tạo
└── output/            # Đầu ra cuối cùng
```

### Các trường cốt lõi trong project.json

- `title`, `content_mode` (`narration`/`drama`), `style`, `style_description`
- `overview`: Tóm tắt dự án (synopsis, genre, theme, world_setting)
- `episodes`: Metadata tập phim (episode, title, script_file)
- `characters`: Định nghĩa nhân vật (description, character_sheet, voice_style)
- `clues`: Định nghĩa manh mối (type, description, importance, clue_sheet)

### Nguyên tắc phân tầng dữ liệu

- Định nghĩa đầy đủ nhân vật/manh mối **chỉ lưu trong project.json**, kịch bản chỉ tham chiếu tên.
- Các trường `scenes_count`, `status`, `progress` được **tính toán khi đọc** (StatusCalculator), không lưu trữ.
- Metadata tập phim được **đồng bộ khi ghi** kịch bản.

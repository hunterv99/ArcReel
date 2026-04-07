---
name: manage-project
description: Tập hợp các công cụ quản lý dự án. Các tình huống sử dụng: (1) Chia tập phim - phát hiện điểm chia và thực hiện chia tập, (2) Thêm hàng loạt nhân vật/manh mối vào project.json. Cung cấp quy trình chia tập lũy tiến peek (xem trước) + split (thực hiện), cũng như ghi hàng loạt nhân vật/manh mối.
user-invocable: false
---

# Tập hợp công cụ quản lý dự án

Cung cấp các công cụ dòng lệnh để quản lý tệp dự án, chủ yếu dùng để chia tập phim và ghi hàng loạt nhân vật/manh mối.

## Danh sách công cụ

| Script | Chức năng | Bên gọi |
|------|------|--------|
| `peek_split_point.py` | Phát hiện ngữ cảnh và điểm ngắt tự nhiên gần số chữ mục tiêu | Agent chính (Giai đoạn 2) |
| `split_episode.py` | Thực hiện chia tập, tạo episode_N.txt + _remaining.txt | Agent chính (Giai đoạn 2) |
| `add_characters_clues.py` | Thêm hàng loạt nhân vật/manh mối vào project.json | subagent |

## Quy trình chia tập phim

Việc chia tập phim sử dụng quy trình lũy tiến **peek → xác nhận của người dùng → split**, do agent chính thực hiện trực tiếp trong giai đoạn 2 của manga-workflow.

### Bước 1: Phát hiện điểm chia (Peek)

```bash
python .claude/skills/manage-project/scripts/peek_split_point.py --source {tệp nguồn} --target {số chữ mục tiêu}
```

**Tham số**:
- `--source`: Đường dẫn tệp nguồn (`source/novel.txt` hoặc `source/_remaining.txt`)
- `--target`: Số chữ hữu hiệu mục tiêu
- `--context`: Kích thước cửa sổ ngữ cảnh (mặc định 200 ký tự)

**Đầu ra** (JSON):
- `total_chars`: Tổng số chữ hữu hiệu
- `target_offset`: Độ lệch trong nguyên tác tương ứng với số chữ mục tiêu
- `context_before` / `context_after`: Ngữ cảnh trước và sau điểm chia
- `nearby_breakpoints`: Danh sách các điểm ngắt tự nhiên gần đó (sắp xếp theo khoảng cách, tối đa 10 điểm)

### Bước 2: Thực hiện chia tập (Split)

```bash
# Chạy thử (Dry run - chỉ xem trước)
python .claude/skills/manage-project/scripts/split_episode.py --source {tệp nguồn} --episode {N} --target {số chữ mục tiêu} --anchor "{văn bản neo}" --dry-run

# Thực hiện thực tế
python .claude/skills/manage-project/scripts/split_episode.py --source {tệp nguồn} --episode {N} --target {số chữ mục tiêu} --anchor "{văn bản neo}"
```

**Tham số**:
- `--source`: Đường dẫn tệp nguồn
- `--episode`: Số thứ tự tập phim
- `--target`: Số chữ hữu hiệu mục tiêu (nhất quán với bước peek)
- `--anchor`: Văn bản neo tại điểm chia (10-20 ký tự)
- `--context`: Kích thước cửa sổ tìm kiếm (mặc định 500 ký tự)
- `--dry-run`: Chỉ xem trước, không ghi tệp

**Cơ chế định vị**: Tính toán độ lệch xấp xỉ từ số chữ mục tiêu → tìm kiếm văn bản neo (anchor) trong phạm vi ±window → sử dụng kết quả khớp gần nhất.

**Tệp đầu ra**:
- `source/episode_{N}.txt`: Phần đầu
- `source/_remaining.txt`: Phần còn lại (tệp nguồn cho tập tiếp theo)

## Ghi hàng loạt nhân vật/manh mối

Thực hiện từ bên trong thư mục dự án, tự động phát hiện tên dự án:

⚠️ Phải viết trên một dòng duy nhất, JSON sử dụng định dạng nén (compact), không dùng `\` để xuống dòng:

```bash
python .claude/skills/manage-project/scripts/add_characters_clues.py --characters '{"Tên nhân vật": {"description": "...", "voice_style": "..."}}' --clues '{"Tên manh mối": {"type": "prop", "description": "...", "importance": "major"}}'
```

## Quy tắc thống kê số chữ

- Thống kê tất cả ký tự trong các dòng không trống (bao gồm cả dấu câu)
- Các dòng trống (chỉ chứa ký tự khoảng trắng) không được tính

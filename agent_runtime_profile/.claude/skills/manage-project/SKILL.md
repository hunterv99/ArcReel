---
name: manage-project
<<<<<<< HEAD
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
=======
description: 项目管理工具集。使用场景：(1) 分集切分——探测切分点并执行切分，(2) 批量添加角色/线索到 project.json。提供 peek（预览）+ split（执行）的渐进式切分工作流，以及角色/线索批量写入。
user-invocable: false
---

# 项目管理工具集

提供项目文件管理的命令行工具，主要用于分集切分和角色/线索批量写入。

## 工具一览

| 脚本 | 功能 | 调用者 |
|------|------|--------|
| `peek_split_point.py` | 探测目标字数附近的上下文和自然断点 | 主 agent（阶段 2） |
| `split_episode.py` | 执行分集切分，生成 episode_N.txt + _remaining.txt | 主 agent（阶段 2） |
| `add_characters_clues.py` | 批量添加角色/线索到 project.json | subagent |

## 分集切分工作流

分集切分采用 **peek → 用户确认 → split** 的渐进式流程，由主 agent 在 manga-workflow 阶段 2 直接执行。

### Step 1: 探测切分点

```bash
python .claude/skills/manage-project/scripts/peek_split_point.py --source {源文件} --target {目标字数}
```

**参数**：
- `--source`：源文件路径（`source/novel.txt` 或 `source/_remaining.txt`）
- `--target`：目标有效字数
- `--context`：上下文窗口大小（默认 200 字符）

**输出**（JSON）：
- `total_chars`：总有效字数
- `target_offset`：目标字数对应的原文偏移
- `context_before` / `context_after`：切分点前后上下文
- `nearby_breakpoints`：附近自然断点列表（按距离排序，最多 10 个）

### Step 2: 执行切分

```bash
# Dry run（仅预览）
python .claude/skills/manage-project/scripts/split_episode.py --source {源文件} --episode {N} --target {目标字数} --anchor "{锚点文本}" --dry-run

# 实际执行
python .claude/skills/manage-project/scripts/split_episode.py --source {源文件} --episode {N} --target {目标字数} --anchor "{锚点文本}"
```

**参数**：
- `--source`：源文件路径
- `--episode`：集数编号
- `--target`：目标有效字数（与 peek 一致）
- `--anchor`：切分点的锚点文本（10-20 字符）
- `--context`：搜索窗口大小（默认 500 字符）
- `--dry-run`：仅预览，不写文件

**定位机制**：target 字数计算大致偏移 → 在 ±window 范围内搜索 anchor → 使用距离最近的匹配

**输出文件**：
- `source/episode_{N}.txt`：前半部分
- `source/_remaining.txt`：后半部分（下一集的源文件）

## 角色/线索批量写入

从项目目录内执行，自动检测项目名称：

⚠️ 必须单行，JSON 使用紧凑格式，不可用 `\` 换行：

```bash
python .claude/skills/manage-project/scripts/add_characters_clues.py --characters '{"角色名": {"description": "...", "voice_style": "..."}}' --clues '{"线索名": {"type": "prop", "description": "...", "importance": "major"}}'
```

## 字数统计规则

- 统计非空行的所有字符（包括标点）
- 空行（仅含空白字符的行）不计入
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

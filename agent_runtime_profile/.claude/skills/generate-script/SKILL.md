---
name: generate-script
<<<<<<< HEAD
description: Sử dụng Gemini API để tạo kịch bản JSON. Được gọi bởi subagent create-episode-script. Đọc các tệp trung gian và project.json, gọi Gemini để tạo kịch bản JSON tuân thủ mô hình Pydantic.
=======
description: 使用 Gemini API 生成 JSON 剧本。由 create-episode-script subagent 调用。读取 step1 中间文件和 project.json，调用 Gemini 生成符合 Pydantic 模型的 JSON 剧本。
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
user-invocable: false
---

# generate-script

<<<<<<< HEAD
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
=======
使用 Gemini API 生成 JSON 剧本。此 skill 由 `create-episode-script` subagent 调用，不直接面向用户。

## 前置条件

1. 项目目录下存在 `project.json`（包含 style、overview、characters、clues）
2. 已完成 Step 1 预处理：
   - narration：`drafts/episode_N/step1_segments.md`
   - drama：`drafts/episode_N/step1_normalized_script.md`

## 用法

```bash
# 生成指定剧集的剧本
python .claude/skills/generate-script/scripts/generate_script.py --episode {N}

# 自定义输出路径
python .claude/skills/generate-script/scripts/generate_script.py --episode {N} --output scripts/ep1.json

# 预览 Prompt（不实际调用 API）
python .claude/skills/generate-script/scripts/generate_script.py --episode {N} --dry-run
```

## 生成流程

脚本内部通过 `ScriptGenerator` 完成以下步骤：

1. **加载 project.json** — 读取 content_mode、characters、clues、overview、style
2. **加载 Step 1 中间文件** — 根据 content_mode 选择 `step1_segments.md`（narration）或 `step1_normalized_script.md`（drama）
3. **构建 Prompt** — 将项目概述、风格、角色、线索和中间文件内容组合成完整 prompt
4. **调用 Gemini API** — 使用 `gemini-3-flash-preview` 模型，传入 Pydantic schema 作为 `response_schema` 约束输出格式
5. **Pydantic 验证** — 用 `NarrationEpisodeScript`（narration）或 `DramaEpisodeScript`（drama）校验返回 JSON
6. **补充元数据** — 写入 episode、content_mode、统计信息（片段/场景数、总时长）、时间戳

## 输出格式

生成的 JSON 文件保存至 `scripts/episode_N.json`，核心结构：

- `episode`、`content_mode`、`novel`（title、chapter、source_file）
- narration 模式：`segments` 数组（每个片段包含 visual、novel_text、duration_seconds 等）
- drama 模式：`scenes` 数组（每个场景包含 visual、dialogue、action、duration_seconds 等）
- `metadata`：total_segments/total_scenes、created_at、generator
- `duration_seconds`：全集总时长（秒）

## `--dry-run` 输出

打印将发送给 Gemini 的完整 prompt 文本，不调用 API、不写文件。用于检查 prompt 质量和长度。

> 支持的两种模式规格详见 `.claude/references/content-modes.md`。
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

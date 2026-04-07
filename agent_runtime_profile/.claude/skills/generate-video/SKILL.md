---
name: generate-video
<<<<<<< HEAD
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
=======
description: 为剧本场景生成视频片段。当用户说"生成视频"、"把分镜图变成视频"、想重新生成某个场景的视频、或视频生成中断需要续传时使用。支持整集批量、单场景、断点续传等模式。
---

# 生成视频

使用 Veo 3.1 API 为每个场景/片段创建视频，以分镜图作为起始帧。

> 画面比例、时长、分辨率等规格由脚本根据 content_mode 自动设置，详见 `.claude/references/content-modes.md`。

## 命令行用法

```bash
# 标准模式：生成整集所有待处理场景（推荐）
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --episode {N}

# 断点续传：从上次中断处继续
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --episode {N} --resume

# 单场景：测试或重新生成
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --scene E1S1

# 批量自选：指定多个场景
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --scenes E1S01,E1S05,E1S10

# 全部待处理
python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --all
```

> 所有任务一次性提交到生成队列，由 Worker 按 per-provider 并发配置自动调度。

## 工作流程

1. **加载项目和剧本** — 确认所有场景都有 `storyboard_image`
2. **生成视频** — 脚本自动构建 Prompt、调用 API、保存 checkpoint
3. **审核检查点** — 展示结果，用户可重新生成不满意的场景
4. **更新剧本** — 自动更新 `video_clip` 路径和场景状态

## Prompt 构建

Prompt 由脚本内部自动构建，根据 content_mode 选择不同策略。脚本从剧本 JSON 读取以下字段：

**image_prompt**（用于分镜图参考）：scene、composition（shot_type、lighting、ambiance）

**video_prompt**（用于视频生成）：action、camera_motion、ambiance_audio、dialogue、narration（仅 drama）

- 说书模式：`novel_text` 不参与视频生成（后期人工配音），`dialogue` 仅包含原文中的角色对话
- 剧集动画模式：包含完整的对话、旁白、音效
- Negative prompt 自动排除 BGM

## 生成前检查

- [ ] 所有场景都有已批准的分镜图
- [ ] 对话文本长度适当
- [ ] 动作描述清晰简单
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

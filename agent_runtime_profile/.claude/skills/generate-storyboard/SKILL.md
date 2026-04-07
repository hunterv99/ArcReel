---
name: generate-storyboard
<<<<<<< HEAD
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
=======
description: 为剧本场景生成分镜图。当用户说"生成分镜"、"预览场景画面"、想重新生成某些分镜图、或剧本中有场景缺少分镜图时使用。自动保持角色和画面连续性。
---

# 生成分镜图

通过生成队列创建分镜图，画面比例根据 content_mode 自动设置。

> 内容模式规格详见 `.claude/references/content-modes.md`。

## 命令行用法

```bash
# 提交所有缺失分镜图到生成队列（自动检测 content_mode）
python .claude/skills/generate-storyboard/scripts/generate_storyboard.py script.json

# 为单个场景重新生成
python .claude/skills/generate-storyboard/scripts/generate_storyboard.py script.json --scene E1S05

# 为多个场景重新生成
python .claude/skills/generate-storyboard/scripts/generate_storyboard.py script.json --scene-ids E1S01 E1S02
```

> `--scene-ids` 和 `--segment-ids` 是同义别名（后者为 narration 模式的习惯称呼），效果相同。以下统一使用 `--scene-ids`。

> **选择规则**：`--scene` 重生成一个；`--scene-ids` 重生成多个；未提供则提交所有缺失项。

> **注意**：脚本要求 generation worker 在线，worker 负责实际图像生成与速率控制。

## 工作流程

1. **加载项目和剧本** — 确认所有角色都有 `character_sheet` 图像
2. **生成分镜图** — 脚本自动检测 content_mode，按相邻关系串联依赖任务
3. **审核检查点** — 展示每张分镜图，用户可批准或要求重新生成
4. **更新剧本** — 更新 `storyboard_image` 路径和场景状态

## 角色一致性机制

脚本自动处理以下参考图传入，无需手动指定：
- **character_sheet**：场景中出场角色的设计图，保持外貌一致
- **clue_sheet**：场景中出现的线索设计图
- **上一张分镜图**：相邻片段默认引用，提升画面连续性
- 当片段标记 `segment_break=true` 时，跳过上一张分镜图参考

## Prompt 模板

脚本从剧本 JSON 读取以下字段构建 prompt：

```
场景 [scene_id/segment_id] 的分镜图：

- 画面描述：[visual.description]
- 镜头构图：[visual.shot_type]
- 镜头运动起点：[visual.camera_movement]
- 光线条件：[visual.lighting]
- 画面氛围：[visual.mood]
- 角色：[characters_in_scene]
- 动作：[action]

风格要求：电影分镜图风格，根据项目 style 设定。
角色必须与提供的角色参考图完全一致。
```

> 画面比例通过 API 参数设置，不写入 prompt。

## 生成前检查

- [ ] 所有角色都有已批准的 character_sheet 图像
- [ ] 场景视觉描述完整
- [ ] 角色动作已指定

## 错误处理

- 单场景失败不影响批次，记录失败场景后继续
- 生成结束后汇总报告所有失败场景和原因
- 支持增量生成（跳过已存在的场景图）
- 使用 `--scene-ids` 重新生成失败场景
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

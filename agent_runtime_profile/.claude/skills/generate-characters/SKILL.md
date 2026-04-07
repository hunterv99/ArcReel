---
name: generate-characters
<<<<<<< HEAD
description: Tạo hình ảnh tham chiếu thiết kế nhân vật (ba góc nhìn). Sử dụng khi người dùng yêu cầu "tạo hình nhân vật", "vẽ thiết kế nhân vật", muốn tạo hình tham chiếu cho nhân vật mới, hoặc khi nhân vật thiếu character_sheet. Đảm bảo ngoại hình nhân vật nhất quán trong toàn bộ video.
---

# Tạo hình ảnh thiết kế nhân vật

Sử dụng Gemini 3 Pro Image API để tạo hình ảnh thiết kế nhân vật, đảm bảo tính nhất quán về mặt hình ảnh trong toàn bộ video.

> Các nguyên tắc viết Prompt chi tiết xem tại chương "Ngôn ngữ cho Prompt" trong tài liệu `.claude/references/content-modes.md`.

## Hướng dẫn viết mô tả nhân vật

Khi viết mô tả (`description`) cho nhân vật, hãy sử dụng **phong cách tường thuật**, không liệt kê từ khóa.

**Khuyên dùng**:
> "Một cô gái ngoài đôi mươi, dáng người mảnh khảnh, khuôn mặt trái xoan với đôi mắt hạnh trong veo, đôi lông mày lá liễu hơi nhíu lại mang chút u buồn. Cô mặc bộ váy lụa thêu hoa màu xanh nhạt, thắt dải lụa cùng màu quanh eo, toát lên vẻ trang nghiêm mà không kém phần linh hoạt."

**Điểm mấu chốt**: Sử dụng các đoạn văn liền mạch để mô tả ngoại hình, trang phục, khí chất, bao gồm tuổi tác, vóc dáng, đặc điểm khuôn mặt và chi tiết trang phục.

## Cách dùng dòng lệnh

```bash
# Tạo cho tất cả các nhân vật đang chờ xử lý
python .claude/skills/generate-characters/scripts/generate_character.py --all

# Tạo cho một nhân vật cụ thể
python .claude/skills/generate-character/scripts/generate_character.py --character "{tên nhân vật}"

# Tạo cho nhiều nhân vật cụ thể
python .claude/skills/generate-character/scripts/generate_character.py --characters "{nhân vật 1}" "{nhân vật 2}" "{nhân vật 3}"

# Liệt kê các nhân vật đang chờ tạo
python .claude/skills/generate-character/scripts/generate_character.py --list
```

## Quy trình làm việc

1. **Tải dữ liệu dự án** — Tìm các nhân vật thiếu `character_sheet` từ project.json.
2. **Tạo thiết kế nhân vật** — Xây dựng prompt dựa trên mô tả, gọi script để tạo.
3. **Kiểm tra điểm chốt (Checkpoint)** — Hiển thị từng bản thiết kế, người dùng có thể phê duyệt hoặc yêu cầu tạo lại.
4. **Cập nhật project.json** — Cập nhật đường dẫn `character_sheet`.

## Mẫu Prompt

```
Một bản thiết kế nhân vật chuyên nghiệp, {style của dự án}.

Bản thiết kế ba góc nhìn cho nhân vật "[Tên nhân vật]". [Mô tả nhân vật - đoạn văn tường thuật]

Ba hình ảnh toàn thân cùng tỷ lệ được sắp xếp nằm ngang trên nền xám nhạt tinh khiết: bên trái là chính diện, ở giữa là góc ba phần tư, bên phải là góc nghiêng hoàn chỉnh. Ánh sáng studio mềm mại và đồng đều, không có bóng đổ mạnh.
```

> Phong cách nghệ thuật được quyết định bởi trường `style` của dự án, không sử dụng các mô tả cố định như "manga/anime".
=======
description: 生成角色设计参考图（三视图）。当用户说"生成角色图"、"画角色设计"、想为新角色创建参考图、或有角色缺少 character_sheet 时使用。确保视频中角色形象一致。
---

# 生成角色设计图

使用 Gemini 3 Pro Image API 创建角色设计图，确保整个视频中的视觉一致性。

> Prompt 编写原则详见 `.claude/references/content-modes.md` 的"Prompt 语言"章节。

## 角色描述编写指南

编写角色 `description` 时使用**叙事式写法**，不要罗列关键词。

**推荐**：
> "二十出头的女子，身材纤细，鹅蛋脸上有一双清澈的杏眼，柳叶眉微蹙时带着几分忧郁。身着淡青色绣花罗裙，腰间系着同色丝带，显得端庄而不失灵动。"

**要点**：用连贯段落描述外貌、服装、气质，包含年龄、体态、面部特征、服饰细节。

## 命令行用法

```bash
# 生成所有待处理的角色
python .claude/skills/generate-characters/scripts/generate_character.py --all

# 生成指定单个角色
python .claude/skills/generate-characters/scripts/generate_character.py --character "{角色名}"

# 生成指定多个角色
python .claude/skills/generate-characters/scripts/generate_character.py --characters "{角色1}" "{角色2}" "{角色3}"

# 列出待生成的角色
python .claude/skills/generate-characters/scripts/generate_character.py --list
```

## 工作流程

1. **加载项目数据** — 从 project.json 找出缺少 `character_sheet` 的角色
2. **生成角色设计** — 根据描述构建 prompt，调用脚本生成
3. **审核检查点** — 展示每张设计图，用户可批准或要求重新生成
4. **更新 project.json** — 更新 `character_sheet` 路径

## Prompt 模板

```
一张专业的角色设计参考图，{项目 style}。

角色「[角色名称]」的三视图设计稿。[角色描述 - 叙事式段落]

三个等比例全身像水平排列在纯净浅灰背景上：左侧正面、中间四分之三侧面、右侧纯侧面轮廓。柔和均匀的摄影棚照明，无强烈阴影。
```

> 画风由项目的 `style` 字段决定，不使用固定的"漫画/动漫"描述。
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

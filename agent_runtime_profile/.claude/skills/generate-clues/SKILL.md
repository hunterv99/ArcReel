---
name: generate-clues
<<<<<<< HEAD
description: Tạo hình ảnh thiết kế manh mối (đạo cụ/môi trường). Sử dụng khi người dùng yêu cầu "tạo hình manh mối", "vẽ thiết kế đạo cụ", muốn tạo hình tham chiếu cho vật phẩm hoặc bối cảnh quan trọng, hoặc khi manh mối chính thiếu clue_sheet. Đảm bảo tính nhất quán hình ảnh xuyên suốt các cảnh.
---

# Tạo hình ảnh thiết kế manh mối

Sử dụng Gemini 3 Pro Image API để tạo hình ảnh thiết kế manh mối, đảm bảo tính nhất quán về mặt hình ảnh của các vật phẩm và môi trường quan trọng trong toàn bộ video.

> Các nguyên tắc viết Prompt chi tiết xem tại chương "Ngôn ngữ cho Prompt" trong tài liệu `.claude/references/content-modes.md`.

## Phân loại manh mối

- **Đạo cụ (prop)**: Các vật phẩm quan trọng như tín vật, vũ khí, lá thư, đồ trang sức, v.v.
- **Môi trường (location)**: Các công trình mang tính biểu tượng, cây cối đặc biệt, địa điểm quan trọng, v.v.

## Hướng dẫn viết mô tả manh mối

Khi viết `description`, hãy sử dụng **phong cách tường thuật**, không liệt kê từ khóa.

**Ví dụ đạo cụ**:
> "Một miếng ngọc bội gia truyền màu xanh bích, kích thước khoảng bằng ngón tay cái, chất ngọc ấm áp và trong suốt. Bề mặt chạm khắc họa tiết hoa sen tinh xảo, các cánh hoa xòe ra từng lớp. Trên ngọc bội thắt một sợi dây lụa đỏ với nút thắt đồng tâm truyền thống."

**Ví dụ môi trường**:
> "Cây hòe cổ thụ trăm tuổi ở đầu làng, thân cây to lớn cần ba người ôm mới xuể, vỏ cây nứt nẻ dấu vết thời gian. Thân chính có một vết sẹo cháy xém rõ rệt do sét đánh, uốn lượn từ trên đỉnh xuống. Tán cây rậm rạp, tỏa bóng mát rượi trong những ngày hè."

**Điểm mấu chốt**: Sử dụng các đoạn văn liền mạch để mô tả hình dáng, chất liệu, chi tiết, làm nổi bật những đặc điểm độc đáo giúp nhận diện xuyên suốt các cảnh quay.

## Cách dùng dòng lệnh

```bash
# Tạo cho tất cả các manh mối đang chờ xử lý
python .claude/skills/generate-clues/scripts/generate_clue.py --all

# Tạo một manh mối cụ thể
python .claude/skills/generate-clues/scripts/generate_clue.py --clue "Ngọc bội"

# Tạo nhiều manh mối cụ thể
python .claude/skills/generate-clues/scripts/generate_clues.py --clues "Ngọc bội" "Cây hòe cổ thụ" "Mật thư"

# Liệt kê các manh mối đang chờ tạo
python .claude/skills/generate-clues/scripts/generate_clue.py --list
```

## Quy trình làm việc

1. **Tải siêu dữ liệu dự án** — Tìm các manh mối có `importance='major'` và thiếu `clue_sheet` từ project.json.
2. **Tạo thiết kế manh mối** — Chọn mẫu tương ứng theo loại (prop/location), gọi script để tạo.
3. **Kiểm tra điểm chốt (Checkpoint)** — Hiển thị từng bản thiết kế, người dùng có thể phê duyệt hoặc yêu cầu tạo lại.
4. **Cập nhật project.json** — Cập nhật đường dẫn `clue_sheet`.

## Mẫu Prompt

### Đạo cụ (prop)
```
Một bản thiết kế đạo cụ chuyên nghiệp, {style của dự án}.

Bản thiết kế đa góc nhìn cho đạo cụ "[Tên đạo cụ]". [Mô tả chi tiết - đoạn văn tường thuật]

Ba góc nhìn được sắp xếp nằm ngang trên nền xám nhạt tinh khiết: bên trái là cái nhìn tổng thể chính diện, ở giữa là góc nhìn nghiêng 45 độ để thể hiện khối, bên phải là đặc tả chi tiết quan trọng. Ánh sáng studio mềm mại và đồng đều, chất lượng hình ảnh cao, màu sắc chính xác.
```

### Môi trường (location)
```
Một bản thiết kế bối cảnh chuyên nghiệp, {style của dự án}.

Tham chiếu hình ảnh cho bối cảnh biểu tượng "[Tên bối cảnh]". [Mô tả chi tiết - đoạn văn tường thuật]

Hình ảnh chính chiếm ba phần tư không gian hiển thị tổng thể diện mạo và không khí môi trường, một hình ảnh nhỏ ở góc dưới bên phải là đặc tả chi tiết. Ánh sáng tự nhiên mềm mại.
```

## Kiểm tra chất lượng

- Đạo cụ: Ba góc nhìn rõ ràng và nhất quán, chi tiết khớp với mô tả, các kết cấu đặc biệt hiển thị rõ nét.
- Môi trường: Bố cục tổng thể và các đặc điểm nhận dạng nổi bật, không khí ánh sáng phù hợp, hình ảnh chi tiết rõ ràng.
=======
description: 生成线索设计参考图（道具/环境）。当用户说"生成线索图"、"画道具设计"、想为重要物品或场景创建参考图、或有 major 线索缺少 clue_sheet 时使用。确保跨场景视觉一致。
---

# 生成线索设计图

使用 Gemini 3 Pro Image API 创建线索设计图，确保整个视频中重要物品和环境的视觉一致性。

> Prompt 编写原则详见 `.claude/references/content-modes.md` 的"Prompt 语言"章节。

## 线索类型

- **道具类（prop）**：信物、武器、信件、首饰等关键物品
- **环境类（location）**：标志性建筑、特定树木、重要场所等

## 线索描述编写指南

编写 `description` 时使用**叙事式写法**，不要罗列关键词。

**道具示例**：
> "一块翠绿色的祖传玉佩，约拇指大小，玉质温润透亮。表面雕刻着精致的莲花纹样，花瓣层层舒展。玉佩上系着一根红色丝绳，打着传统的中国结。"

**环境示例**：
> "村口的百年老槐树，树干粗壮需三人合抱，树皮龟裂沧桑。主干上有一道明显的雷击焦痕，从顶部蜿蜒而下。树冠茂密，夏日里洒下斑驳的树影。"

**要点**：用连贯段落描述形态、质感、细节，突出能跨场景识别的独特特征。

## 命令行用法

```bash
# 生成所有待处理的线索
python .claude/skills/generate-clues/scripts/generate_clue.py --all

# 生成指定单个线索
python .claude/skills/generate-clues/scripts/generate_clue.py --clue "玉佩"

# 生成指定多个线索
python .claude/skills/generate-clues/scripts/generate_clue.py --clues "玉佩" "老槐树" "密信"

# 列出待生成的线索
python .claude/skills/generate-clues/scripts/generate_clue.py --list
```

## 工作流程

1. **加载项目元数据** — 从 project.json 找出 `importance='major'` 且缺少 `clue_sheet` 的线索
2. **生成线索设计** — 根据类型（prop/location）选择对应模板，调用脚本生成
3. **审核检查点** — 展示每张设计图，用户可批准或要求重新生成
4. **更新 project.json** — 更新 `clue_sheet` 路径

## Prompt 模板

### 道具类（prop）
```
一张专业的道具设计参考图，{项目 style}。

道具「[名称]」的多视角展示。[详细描述 - 叙事式段落]

三个视图水平排列在纯净浅灰背景上：左侧正面全视图、中间45度侧视图展示立体感、右侧关键细节特写。柔和均匀的摄影棚照明，高清质感，色彩准确。
```

### 环境类（location）
```
一张专业的场景设计参考图，{项目 style}。

标志性场景「[名称]」的视觉参考。[详细描述 - 叙事式段落]

主画面占据四分之三区域展示环境整体外观与氛围，右下角小图为细节特写。柔和自然光线。
```

## 质量检查

- 道具：三个视角清晰一致、细节符合描述、特殊纹理清晰可见
- 环境：整体构图和标志性特征突出、光线氛围合适、细节图清晰
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

---
name: generate-clues
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

---
name: generate-characters
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

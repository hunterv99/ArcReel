"""
_text_utils.py - Các hàm tiện ích dùng chung cho việc cắt tập con

Cung cấp chức năng đếm từ và chuyển đổi độ lệch ký tự, dùng chung cho peek_split_point.py và split_episode.py.

Quy tắc đếm: tính cả dấu câu, không tính dòng trống (dòng chỉ có khoảng trắng không được tính).
"""


def count_chars(text: str) -> int:
    """Tính số từ hợp lệ: tổng số ký tự trong các dòng không trống (tính cả dấu câu, không tính dòng trống)."""
    total = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped:  # Bỏ qua dòng trống
            total += len(stripped)
    return total


def find_char_offset(text: str, target_count: int) -> int:
    """Chuyển đổi số từ hợp lệ thành vị trí cắt bỏ so với văn bản gốc.

    Duyệt văn bản gốc, bỏ qua các ký tự trong dòng trống, khi số từ hợp lệ đạt đến target_count,
    trả về vị trí đoạn cắt đối với văn bản gốc (bắt đầu từ 0).

    Nếu target_count vượt quá tổng số lượng từ hợp lệ, trả về đoạn cắt ở cuối văn bản.
    """
    counted = 0
    lines = text.split("\n")
    pos = 0  # Vị trí ký tự trong văn bản gốc

    for line_idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            # Dòng trống: Bỏ qua toàn bộ dòng (bao gồm dấu xuống dòng)
            pos += len(line)
            if line_idx < len(lines) - 1:
                pos += 1  # Dấu xuống dòng
            continue

        # Dòng không trống: Đếm từng ký tự
        for char_idx, char in enumerate(line):
            if not char.strip():
                # Khoảng trắng đầu/cuối dòng không được tính vào số từ, nhưng tăng segment cắt
                pos += 1
                continue
            counted += 1
            if counted >= target_count:
                return pos
            pos += 1

        if line_idx < len(lines) - 1:
            pos += 1  # Dấu xuống dòng

    return pos


def find_natural_breakpoints(text: str, center_offset: int, window: int = 200) -> list[dict]:
    """Tìm các điểm ngắt tự nhiên (dấu chấm, ranh giới đoạn văn, v.v...) gần vị trí ngắt xác định.

    Trả về danh sách điểm cắt, mỗi điểm chứa:
    - offset: Vị trí ngắt văn bản gốc
    - char: Ký tự cắt
    - type: Loại cắt (sentence/paragraph)
    - distance: Khoảng cách so với số lượng ký tự center_offset
    """
    start = max(0, center_offset - window)
    end = min(len(text), center_offset + window)

    sentence_endings = {"。", "！", "？", "…"}
    breakpoints = []

    for i in range(start, end):
        ch = text[i]
        if ch == "\n" and i + 1 < len(text) and text[i + 1] == "\n":
            breakpoints.append(
                {
                    "offset": i + 1,
                    "char": "\\n\\n",
                    "type": "paragraph",
                    "distance": abs(i + 1 - center_offset),
                }
            )
        elif ch in sentence_endings:
            breakpoints.append(
                {
                    "offset": i + 1,  # Chia cắt sau dấu câu
                    "char": ch,
                    "type": "sentence",
                    "distance": abs(i + 1 - center_offset),
                }
            )

    # Sắp xếp theo khoảng cách
    breakpoints.sort(key=lambda bp: bp["distance"])
    return breakpoints

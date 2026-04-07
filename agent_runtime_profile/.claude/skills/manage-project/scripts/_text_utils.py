"""
<<<<<<< HEAD
_text_utils.py - Các hàm tiện ích dùng chung cho việc cắt tập con

Cung cấp chức năng đếm từ và chuyển đổi độ lệch ký tự, dùng chung cho peek_split_point.py và split_episode.py.

Quy tắc đếm: tính cả dấu câu, không tính dòng trống (dòng chỉ có khoảng trắng không được tính).
=======
_text_utils.py - 分集切分共享工具函数

提供字数计数和字符偏移转换功能，供 peek_split_point.py 和 split_episode.py 共享。

计数规则：含标点，不含空行（纯空白行不计入字数）。
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
"""


def count_chars(text: str) -> int:
<<<<<<< HEAD
    """Tính số từ hợp lệ: tổng số ký tự trong các dòng không trống (tính cả dấu câu, không tính dòng trống)."""
    total = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped:  # Bỏ qua dòng trống
=======
    """计算有效字数：所有非空行中的字符总数（含标点，不含空行）。"""
    total = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped:  # 跳过空行
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
            total += len(stripped)
    return total


def find_char_offset(text: str, target_count: int) -> int:
<<<<<<< HEAD
    """Chuyển đổi số từ hợp lệ thành vị trí cắt bỏ so với văn bản gốc.

    Duyệt văn bản gốc, bỏ qua các ký tự trong dòng trống, khi số từ hợp lệ đạt đến target_count,
    trả về vị trí đoạn cắt đối với văn bản gốc (bắt đầu từ 0).

    Nếu target_count vượt quá tổng số lượng từ hợp lệ, trả về đoạn cắt ở cuối văn bản.
    """
    counted = 0
    lines = text.split("\n")
    pos = 0  # Vị trí ký tự trong văn bản gốc
=======
    """将有效字数转换为原文字符偏移位置。

    遍历原文，跳过空行中的字符，当累计有效字数达到 target_count 时，
    返回对应的原文字符偏移（0-based）。

    如果 target_count 超过总有效字数，返回文本末尾偏移。
    """
    counted = 0
    lines = text.split("\n")
    pos = 0  # 原文中的字符位置
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

    for line_idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
<<<<<<< HEAD
            # Dòng trống: Bỏ qua toàn bộ dòng (bao gồm dấu xuống dòng)
            pos += len(line)
            if line_idx < len(lines) - 1:
                pos += 1  # Dấu xuống dòng
            continue

        # Dòng không trống: Đếm từng ký tự
        for char_idx, char in enumerate(line):
            if not char.strip():
                # Khoảng trắng đầu/cuối dòng không được tính vào số từ, nhưng tăng segment cắt
=======
            # 空行：跳过整行（含换行符）
            pos += len(line)
            if line_idx < len(lines) - 1:
                pos += 1  # 换行符
            continue

        # 非空行：逐字符计数
        for char_idx, char in enumerate(line):
            if not char.strip():
                # 行首/行尾空白不计入有效字数，但推进偏移
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
                pos += 1
                continue
            counted += 1
            if counted >= target_count:
                return pos
            pos += 1

        if line_idx < len(lines) - 1:
<<<<<<< HEAD
            pos += 1  # Dấu xuống dòng
=======
            pos += 1  # 换行符
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

    return pos


def find_natural_breakpoints(text: str, center_offset: int, window: int = 200) -> list[dict]:
<<<<<<< HEAD
    """Tìm các điểm ngắt tự nhiên (dấu chấm, ranh giới đoạn văn, v.v...) gần vị trí ngắt xác định.

    Trả về danh sách điểm cắt, mỗi điểm chứa:
    - offset: Vị trí ngắt văn bản gốc
    - char: Ký tự cắt
    - type: Loại cắt (sentence/paragraph)
    - distance: Khoảng cách so với số lượng ký tự center_offset
=======
    """在指定偏移附近查找自然断点（句号、段落边界等）。

    返回断点列表，每个断点包含：
    - offset: 原文字符偏移
    - char: 断点字符
    - type: 断点类型（sentence/paragraph）
    - distance: 距离 center_offset 的字符数
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
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
<<<<<<< HEAD
                    "offset": i + 1,  # Chia cắt sau dấu câu
=======
                    "offset": i + 1,  # 在标点之后切分
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
                    "char": ch,
                    "type": "sentence",
                    "distance": abs(i + 1 - center_offset),
                }
            )

<<<<<<< HEAD
    # Sắp xếp theo khoảng cách
=======
    # 按距离排序
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    breakpoints.sort(key=lambda bp: bp["distance"])
    return breakpoints

#!/usr/bin/env python3
"""
<<<<<<< HEAD
peek_split_point.py - Script dò tìm điểm cắt chia

Hiển thị nội dung xung quanh số từ mục tiêu, giúp agent và người dùng quyết định điểm ngắt tự nhiên.

Usage:
=======
peek_split_point.py - 切分点探测脚本

展示目标字数附近的上下文，帮助 agent 和用户决定自然断点。

用法:
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    python peek_split_point.py --source source/novel.txt --target 1000
    python peek_split_point.py --source source/novel.txt --target 1000 --context 300
"""

import argparse
import json
import sys
from pathlib import Path

<<<<<<< HEAD
# Import công cụ dùng chung
=======
# 导入共享工具
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
sys.path.insert(0, str(Path(__file__).parent))
from _text_utils import count_chars, find_char_offset, find_natural_breakpoints


def main():
<<<<<<< HEAD
    parser = argparse.ArgumentParser(description="Dò tìm nội dung xung quanh điểm cắt")
    parser.add_argument("--source", required=True, help="Đường dẫn tệp nguồn")
    parser.add_argument("--target", required=True, type=int, help="Số từ mục tiêu (số từ hợp lệ)")
    parser.add_argument("--context", default=200, type=int, help="Số từ ngữ cảnh hiển thị (mặc định 200)")
=======
    parser = argparse.ArgumentParser(description="探测切分点附近上下文")
    parser.add_argument("--source", required=True, help="源文件路径")
    parser.add_argument("--target", required=True, type=int, help="目标字数（有效字数）")
    parser.add_argument("--context", default=200, type=int, help="上下文字数（默认 200）")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    if not source_path.is_relative_to(Path.cwd().resolve()):
<<<<<<< HEAD
        print(f"Lỗi: Đường dẫn tệp nguồn nằm ngoài thư mục dự án hiện tại: {source_path}", file=sys.stderr)
        sys.exit(1)
    if not source_path.exists():
        print(f"Lỗi: Không tìm thấy tệp nguồn: {source_path}", file=sys.stderr)
=======
        print(f"错误：源文件路径超出当前项目目录: {source_path}", file=sys.stderr)
        sys.exit(1)
    if not source_path.exists():
        print(f"错误：源文件不存在: {source_path}", file=sys.stderr)
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        sys.exit(1)

    text = source_path.read_text(encoding="utf-8")
    total_chars = count_chars(text)

    if args.target >= total_chars:
<<<<<<< HEAD
        print(f"Lỗi: Số từ mục tiêu ({args.target}) bằng hoặc vượt quá tổng số lượng từ hợp lệ ({total_chars})", file=sys.stderr)
        sys.exit(1)

    # Xác định vị trí phân tách văn bản gốc tương ứng với số từ mục tiêu
    target_offset = find_char_offset(text, args.target)

    # Tìm các điểm ngắt tự nhiên ở gần đó
    breakpoints = find_natural_breakpoints(text, target_offset, window=args.context)

    # Trích xuất ngữ cảnh
=======
        print(f"错误：目标字数 ({args.target}) 超过或等于总有效字数 ({total_chars})", file=sys.stderr)
        sys.exit(1)

    # 定位目标字数对应的原文偏移
    target_offset = find_char_offset(text, args.target)

    # 查找附近的自然断点
    breakpoints = find_natural_breakpoints(text, target_offset, window=args.context)

    # 提取上下文
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    ctx_start = max(0, target_offset - args.context)
    ctx_end = min(len(text), target_offset + args.context)
    before_context = text[ctx_start:target_offset]
    after_context = text[target_offset:ctx_end]

<<<<<<< HEAD
    # Xuất kết quả
=======
    # 输出结果
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    result = {
        "source": str(source_path),
        "total_chars": total_chars,
        "target_chars": args.target,
        "target_offset": target_offset,
        "context_before": before_context,
        "context_after": after_context,
<<<<<<< HEAD
        "nearby_breakpoints": breakpoints[:10],  # Chỉ lấy 10 điểm gần nhất
=======
        "nearby_breakpoints": breakpoints[:10],  # 只取最近的 10 个
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

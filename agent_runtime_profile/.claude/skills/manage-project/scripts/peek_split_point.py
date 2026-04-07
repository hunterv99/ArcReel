#!/usr/bin/env python3
"""
peek_split_point.py - Script dò tìm điểm cắt chia

Hiển thị nội dung xung quanh số từ mục tiêu, giúp agent và người dùng quyết định điểm ngắt tự nhiên.

Usage:
    python peek_split_point.py --source source/novel.txt --target 1000
    python peek_split_point.py --source source/novel.txt --target 1000 --context 300
"""

import argparse
import json
import sys
from pathlib import Path

# Import công cụ dùng chung
sys.path.insert(0, str(Path(__file__).parent))
from _text_utils import count_chars, find_char_offset, find_natural_breakpoints


def main():
    parser = argparse.ArgumentParser(description="Dò tìm nội dung xung quanh điểm cắt")
    parser.add_argument("--source", required=True, help="Đường dẫn tệp nguồn")
    parser.add_argument("--target", required=True, type=int, help="Số từ mục tiêu (số từ hợp lệ)")
    parser.add_argument("--context", default=200, type=int, help="Số từ ngữ cảnh hiển thị (mặc định 200)")
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    if not source_path.is_relative_to(Path.cwd().resolve()):
        print(f"Lỗi: Đường dẫn tệp nguồn nằm ngoài thư mục dự án hiện tại: {source_path}", file=sys.stderr)
        sys.exit(1)
    if not source_path.exists():
        print(f"Lỗi: Không tìm thấy tệp nguồn: {source_path}", file=sys.stderr)
        sys.exit(1)

    text = source_path.read_text(encoding="utf-8")
    total_chars = count_chars(text)

    if args.target >= total_chars:
        print(f"Lỗi: Số từ mục tiêu ({args.target}) bằng hoặc vượt quá tổng số lượng từ hợp lệ ({total_chars})", file=sys.stderr)
        sys.exit(1)

    # Xác định vị trí phân tách văn bản gốc tương ứng với số từ mục tiêu
    target_offset = find_char_offset(text, args.target)

    # Tìm các điểm ngắt tự nhiên ở gần đó
    breakpoints = find_natural_breakpoints(text, target_offset, window=args.context)

    # Trích xuất ngữ cảnh
    ctx_start = max(0, target_offset - args.context)
    ctx_end = min(len(text), target_offset + args.context)
    before_context = text[ctx_start:target_offset]
    after_context = text[target_offset:ctx_end]

    # Xuất kết quả
    result = {
        "source": str(source_path),
        "total_chars": total_chars,
        "target_chars": args.target,
        "target_offset": target_offset,
        "context_before": before_context,
        "context_after": after_context,
        "nearby_breakpoints": breakpoints[:10],  # Chỉ lấy 10 điểm gần nhất
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

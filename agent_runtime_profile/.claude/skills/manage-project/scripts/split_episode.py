#!/usr/bin/env python3
"""
split_episode.py - Thực thi cắt tập con

Sử dụng số từ mục tiêu + văn bản neo để xác định vị trí cắt, chia tiểu thuyết thành episode_N.txt và _remaining.txt.
Số từ mục tiêu thu hẹp cửa sổ tìm kiếm, văn bản neo định vị chính xác.

Usage:
    # Chạy mô phỏng (Chỉ xem trước)
    python split_episode.py --source source/novel.txt --episode 1 --target 1000 --anchor "Anh ấy quay người rời đi." --dry-run

    # Thực thi thật
    python split_episode.py --source source/novel.txt --episode 1 --target 1000 --anchor "Anh ấy quay người rời đi."
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _text_utils import find_char_offset


def find_anchor_near_target(text: str, anchor: str, target_offset: int, window: int = 500) -> list[int]:
    """Tìm kiếm văn bản neo trong cửa sổ gần vị trí mục tiêu, trả về danh sách vị trí ngắt khi khớp cuối cùng (sắp xếp theo khoảng cách)."""
    search_start = max(0, target_offset - window)
    search_end = min(len(text), target_offset + window)
    search_region = text[search_start:search_end]

    positions = []
    start = 0
    while True:
        idx = search_region.find(anchor, start)
        if idx == -1:
            break
        abs_pos = search_start + idx + len(anchor)  # Vị trí ngắt tuyệt đối ở cuối neo
        positions.append(abs_pos)
        start = idx + 1

    # Sắp xếp theo khoảng cách đến target_offset
    positions.sort(key=lambda p: abs(p - target_offset))
    return positions


def main():
    parser = argparse.ArgumentParser(description="Thực thi cắt tập con")
    parser.add_argument("--source", required=True, help="Đường dẫn tệp nguồn")
    parser.add_argument("--episode", required=True, type=int, help="Số tập")
    parser.add_argument("--target", required=True, type=int, help="Số từ mục tiêu (giống với --target của peek)")
    parser.add_argument("--anchor", required=True, help="Đoạn văn bản trước điểm cắt (10-20 ký tự)")
    parser.add_argument("--context", default=500, type=int, help="Kích thước cửa sổ tìm kiếm (mặc định 500 ký tự)")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ xem trước điểm cắt, không ghi vào tệp")
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    if not source_path.is_relative_to(Path.cwd().resolve()):
        print(f"Lỗi: Đường dẫn tệp nguồn nằm ngoài thư mục dự án hiện tại: {source_path}", file=sys.stderr)
        sys.exit(1)
    if not source_path.exists():
        print(f"Lỗi: Không tìm thấy tệp nguồn: {source_path}", file=sys.stderr)
        sys.exit(1)

    text = source_path.read_text(encoding="utf-8")

    # Tính toán vị trí ngắt đại khái từ số từ mục tiêu
    target_offset = find_char_offset(text, args.target)

    # Tìm kiếm văn bản neo ở gần vị trí ngắt mục tiêu
    positions = find_anchor_near_target(text, args.anchor, target_offset, window=args.context)

    if len(positions) == 0:
        print(
            f'Lỗi: Không tìm thấy văn bản neo ở gần mục tiêu {args.target} từ (khoảng ± {args.context} từ): "{args.anchor}"',
            file=sys.stderr,
        )
        sys.exit(1)

    if len(positions) > 1:
        print(
            f"Cảnh báo: Tác giả tìm thấy {len(positions)} khớp neo trong phạm vi, sử dụng kết quả gần mục tiêu nhất.",
            file=sys.stderr,
        )
        for i, pos in enumerate(positions):
            ctx_start = max(0, pos - len(args.anchor) - 10)
            ctx_end = min(len(text), pos + 10)
            distance = abs(pos - target_offset)
            marker = " ← Đã chọn" if i == 0 else ""
            print(f"  Khớp {i + 1} (khoảng cách {distance}): ...{text[ctx_start:ctx_end]}...{marker}", file=sys.stderr)

    split_pos = positions[0]
    part_before = text[:split_pos]
    part_after = text[split_pos:]

    # Hiển thị xem trước điểm cắt
    preview_len = 50
    before_preview = part_before[-preview_len:] if len(part_before) > preview_len else part_before
    after_preview = part_after[:preview_len] if len(part_after) > preview_len else part_after

    print(f"Số từ mục tiêu: {args.target}, Độ lệch vị trí đoạn cắt: {target_offset}")
    print(f"Vị trí cắt: Tại ký tự thứ {split_pos}")
    print(f"Cuối đoạn trước: ...{before_preview}")
    print(f"Đầu đoạn sau: {after_preview}...")
    print(f"Nửa đầu: {len(part_before)} ký tự")
    print(f"Nửa phần sau: {len(part_after)} ký tự")

    if args.dry_run:
        print("\n[Dry Run] Không ghi vào tệp. Nếu đúng, vui lòng bỏ --dry-run và thực thi lại.")
        return

    # Ghi vào tệp thực tế
    output_dir = source_path.parent
    episode_file = output_dir / f"episode_{args.episode}.txt"
    remaining_file = output_dir / "_remaining.txt"

    episode_file.write_text(part_before, encoding="utf-8")
    remaining_file.write_text(part_after, encoding="utf-8")

    print("\nĐã tạo thành công:")
    print(f"  {episode_file} ({len(part_before)} ký tự)")
    print(f"  {remaining_file} ({len(part_after)} ký tự)")
    print(f"  Tệp gốc không thay đổi: {source_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
add_characters_clues.py - Thêm hàng loạt nhân vật/manh mối vào project.json

Usage (phải thực thi từ trong thư mục dự án, trên một dòng):
    python .claude/skills/manage-project/scripts/add_characters_clues.py --characters '{"Tên nhân vật": {"description": "...", "voice_style": "..."}}' --clues '{"Tên manh mối": {"type": "prop", "description": "...", "importance": "major"}}'
"""

import argparse
import json
import sys
from pathlib import Path

# Cho phép chạy script này trực tiếp từ bất kỳ thư mục làm việc nào trong repository
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # .claude/skills/manage-project/scripts -> repo root
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.data_validator import validate_project
from lib.project_manager import ProjectManager


def main():
    parser = argparse.ArgumentParser(
        description="Thêm hàng loạt nhân vật/manh mối vào project.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example (phải thực thi từ trong thư mục dự án, trên một dòng):
    %(prog)s --characters '{"Lý Bạch": {"description": "Kiếm khách áo trắng", "voice_style": "Hào phóng"}}'
    %(prog)s --clues '{"Ngọc bội": {"type": "prop", "description": "Ngọc trắng ấm áp", "importance": "major"}}'
        """,
    )

    parser.add_argument(
        "--characters",
        type=str,
        default=None,
        help="Dữ liệu nhân vật định dạng JSON",
    )
    parser.add_argument(
        "--clues",
        type=str,
        default=None,
        help="Dữ liệu manh mối định dạng JSON",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Đọc JSON từ stdin (chứa trường characters và/hoặc clues)",
    )

    args = parser.parse_args()

    characters = {}
    clues = {}

    if args.stdin:
        stdin_data = json.loads(sys.stdin.read())
        characters = stdin_data.get("characters", {})
        clues = stdin_data.get("clues", {})
    else:
        if args.characters:
            characters = json.loads(args.characters)
        if args.clues:
            clues = json.loads(args.clues)

    if not characters and not clues:
        print("❌ Chưa cung cấp dữ liệu nhân vật hoặc manh mối")
        sys.exit(1)

    pm, project_name = ProjectManager.from_cwd()

    # Thêm nhân vật
    chars_added = 0
    chars_skipped = 0
    if characters:
        project = pm.load_project(project_name)
        existing = project.get("characters", {})
        chars_skipped = sum(1 for name in characters if name in existing)
        chars_added = pm.add_characters_batch(project_name, characters)
        print(f"Nhân vật: Đã thêm mới {chars_added}, bỏ qua {chars_skipped} (đã tồn tại)")

    # Thêm manh mối
    clues_added = 0
    clues_skipped = 0
    if clues:
        project = pm.load_project(project_name)
        existing = project.get("clues", {})
        clues_skipped = sum(1 for name in clues if name in existing)
        clues_added = pm.add_clues_batch(project_name, clues)
        print(f"Manh mối: Đã thêm mới {clues_added}, bỏ qua {clues_skipped} (đã tồn tại)")

    # Xác thực dữ liệu
    result = validate_project(project_name, projects_root=str(pm.projects_root))
    if result.valid:
        print("✅ Dữ liệu hợp lệ")
    else:
        print("⚠️ Xác thực dữ liệu phát hiện vấn đề:")
        for error in result.errors:
            print(f"  Lỗi: {error}")
        for warning in result.warnings:
            print(f"  Cảnh báo: {warning}")
        sys.exit(1)

    # Tổng kết
    total_added = chars_added + clues_added
    if total_added > 0:
        print(f"\n✅ Hoàn tất: Tổng cộng đã thêm mới {total_added} dữ liệu")
    else:
        print("\nℹ️ Tất cả dữ liệu đã tồn tại, không có thêm mới")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
<<<<<<< HEAD
add_characters_clues.py - Thêm hàng loạt nhân vật/manh mối vào project.json

Usage (phải thực thi từ trong thư mục dự án, trên một dòng):
    python .claude/skills/manage-project/scripts/add_characters_clues.py --characters '{"Tên nhân vật": {"description": "...", "voice_style": "..."}}' --clues '{"Tên manh mối": {"type": "prop", "description": "...", "importance": "major"}}'
=======
add_characters_clues.py - 批量添加角色/线索到 project.json

用法（需从项目目录内执行，必须单行）:
    python .claude/skills/manage-project/scripts/add_characters_clues.py --characters '{"角色名": {"description": "...", "voice_style": "..."}}' --clues '{"线索名": {"type": "prop", "description": "...", "importance": "major"}}'
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
"""

import argparse
import json
import sys
from pathlib import Path

<<<<<<< HEAD
# Cho phép chạy script này trực tiếp từ bất kỳ thư mục làm việc nào trong repository
=======
# 允许从仓库任意工作目录直接运行该脚本
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # .claude/skills/manage-project/scripts -> repo root
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.data_validator import validate_project
from lib.project_manager import ProjectManager


def main():
    parser = argparse.ArgumentParser(
<<<<<<< HEAD
        description="Thêm hàng loạt nhân vật/manh mối vào project.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example (phải thực thi từ trong thư mục dự án, trên một dòng):
    %(prog)s --characters '{"Lý Bạch": {"description": "Kiếm khách áo trắng", "voice_style": "Hào phóng"}}'
    %(prog)s --clues '{"Ngọc bội": {"type": "prop", "description": "Ngọc trắng ấm áp", "importance": "major"}}'
=======
        description="批量添加角色/线索到 project.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例（需从项目目录内执行，必须单行）:
    %(prog)s --characters '{"李白": {"description": "白衣剑客", "voice_style": "豪放"}}'
    %(prog)s --clues '{"玉佩": {"type": "prop", "description": "温润白玉", "importance": "major"}}'
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        """,
    )

    parser.add_argument(
        "--characters",
        type=str,
        default=None,
<<<<<<< HEAD
        help="Dữ liệu nhân vật định dạng JSON",
=======
        help="JSON 格式的角色数据",
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    )
    parser.add_argument(
        "--clues",
        type=str,
        default=None,
<<<<<<< HEAD
        help="Dữ liệu manh mối định dạng JSON",
=======
        help="JSON 格式的线索数据",
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
<<<<<<< HEAD
        help="Đọc JSON từ stdin (chứa trường characters và/hoặc clues)",
=======
        help="从 stdin 读取 JSON（包含 characters 和/或 clues 字段）",
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
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
<<<<<<< HEAD
        print("❌ Chưa cung cấp dữ liệu nhân vật hoặc manh mối")
=======
        print("❌ 未提供角色或线索数据")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        sys.exit(1)

    pm, project_name = ProjectManager.from_cwd()

<<<<<<< HEAD
    # Thêm nhân vật
=======
    # 添加角色
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    chars_added = 0
    chars_skipped = 0
    if characters:
        project = pm.load_project(project_name)
        existing = project.get("characters", {})
        chars_skipped = sum(1 for name in characters if name in existing)
        chars_added = pm.add_characters_batch(project_name, characters)
<<<<<<< HEAD
        print(f"Nhân vật: Đã thêm mới {chars_added}, bỏ qua {chars_skipped} (đã tồn tại)")

    # Thêm manh mối
=======
        print(f"角色: 新增 {chars_added} 个，跳过 {chars_skipped} 个（已存在）")

    # 添加线索
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    clues_added = 0
    clues_skipped = 0
    if clues:
        project = pm.load_project(project_name)
        existing = project.get("clues", {})
        clues_skipped = sum(1 for name in clues if name in existing)
        clues_added = pm.add_clues_batch(project_name, clues)
<<<<<<< HEAD
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
=======
        print(f"线索: 新增 {clues_added} 个，跳过 {clues_skipped} 个（已存在）")

    # 数据验证
    result = validate_project(project_name, projects_root=str(pm.projects_root))
    if result.valid:
        print("✅ 数据验证通过")
    else:
        print("⚠️ 数据验证发现问题:")
        for error in result.errors:
            print(f"  错误: {error}")
        for warning in result.warnings:
            print(f"  警告: {warning}")
        sys.exit(1)

    # 汇总
    total_added = chars_added + clues_added
    if total_added > 0:
        print(f"\n✅ 完成: 共新增 {total_added} 条数据")
    else:
        print("\nℹ️ 所有数据已存在，无新增")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3


if __name__ == "__main__":
    main()

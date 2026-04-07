#!/usr/bin/env python3
"""
Clue Generator - Sử dụng Gemini API tạo ảnh thiết kế manh mối

Usage:
    python generate_clue.py --all
    python generate_clue.py --clue "Ngọc bội"
    python generate_clue.py --clues "Ngọc bội" "Cây hòe cổ thụ"
    python generate_clue.py --list

Example:
    python generate_clue.py --all
    python generate_clue.py --clue "Cây hòe cổ thụ"
"""

import argparse
import sys
from pathlib import Path

from lib.generation_queue_client import (
    BatchTaskResult,
    BatchTaskSpec,
    batch_enqueue_and_wait_sync,
)
from lib.generation_queue_client import (
    enqueue_and_wait_sync as enqueue_and_wait,
)
from lib.project_manager import ProjectManager


def generate_clue(clue_name: str) -> Path:
    """
    Tạo ảnh thiết kế cho một manh mối

    Args:
        clue_name: Tên manh mối

    Returns:
        Đường dẫn ảnh được tạo
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)

    # Lấy thông tin manh mối
    clue = pm.get_clue(project_name, clue_name)
    clue_type = clue.get("type", "prop")
    description = clue.get("description", "")

    if not description:
        raise ValueError(f"Mô tả của manh mối '{clue_name}' trống, vui lòng thêm mô tả trước")

    print(f"🎨 Đang tạo ảnh thiết kế manh mối: {clue_name}")
    print(f"   Loại: {clue_type}")
    print(f"   Mô tả: {description[:50]}..." if len(description) > 50 else f"   Mô tả: {description}")

    queued = enqueue_and_wait(
        project_name=project_name,
        task_type="clue",
        media_type="image",
        resource_id=clue_name,
        payload={"prompt": description},
        source="skill",
    )
    result = queued.get("result") or {}
    relative_path = result.get("file_path") or f"clues/{clue_name}.png"
    output_path = project_dir / relative_path
    version = result.get("version")
    version_text = f" (Phiên bản v{version})" if version is not None else ""
    print(f"✅ Ảnh thiết kế manh mối đã được lưu: {output_path}{version_text}")
    return output_path


def list_pending_clues() -> None:
    """
    Liệt kê các manh mối đang chờ tạo
    """
    pm, project_name = ProjectManager.from_cwd()
    pending = pm.get_pending_clues(project_name)

    if not pending:
        print(f"✅ Tất cả manh mối quan trọng trong dự án '{project_name}' đều đã có ảnh thiết kế")
        return

    print(f"\n📋 Manh mối chờ tạo ({len(pending)}):\n")
    for clue in pending:
        clue_type = clue.get("type", "prop")
        type_emoji = "📦" if clue_type == "prop" else "🏠"
        print(f"  {type_emoji} {clue['name']}")
        print(f"     Loại: {clue_type}")
        print(f"     Mô tả: {clue.get('description', '')[:60]}...")
        print()


def generate_batch_clues(
    clue_names: list[str] | None = None,
) -> tuple[int, int]:
    """
    Tạo ảnh thiết kế manh mối hàng loạt (tất cả vào hàng đợi, Worker xử lý song song)

    Args:
        clue_names: Danh sách tên manh mối được chỉ định. None tượng trưng cho tất cả các manh mối đang chờ xử lý.

    Returns:
        (Số lượng thành công, Số lượng thất bại)
    """
    pm, project_name = ProjectManager.from_cwd()
    project = pm.load_project(project_name)
    clues_dict = project.get("clues", {})

    if clue_names:
        names_to_process = []
        for name in clue_names:
            if name not in clues_dict:
                print(f"⚠️  Manh mối '{name}' không tồn tại trong project.json, bỏ qua")
                continue
            if not clues_dict[name].get("description"):
                print(f"⚠️  Manh mối '{name}' thiếu mô tả, bỏ qua")
                continue
            names_to_process.append(name)
    else:
        pending = pm.get_pending_clues(project_name)
        names_to_process = [c["name"] for c in pending]

    if not names_to_process:
        print("✅ Không có manh mối nào cần tạo")
        return (0, 0)
    specs = [
        BatchTaskSpec(
            task_type="clue",
            media_type="image",
            resource_id=name,
            payload={"prompt": clues_dict[name]["description"]},
        )
        for name in names_to_process
    ]

    total = len(specs)
    print(f"\n🚀 Nộp hàng loạt {total} yêu cầu tạo hình manh mối vào hàng đợi...\n")

    def on_success(br: BatchTaskResult) -> None:
        version = (br.result or {}).get("version")
        version_text = f" (Phiên bản v{version})" if version is not None else ""
        print(f"✅ Ảnh thiết kế manh mối: {br.resource_id} hoàn tất{version_text}")

    def on_failure(br: BatchTaskResult) -> None:
        print(f"❌ Ảnh thiết kế manh mối: {br.resource_id} thất bại - {br.error}")

    successes, failures = batch_enqueue_and_wait_sync(
        project_name=project_name,
        specs=specs,
        on_success=on_success,
        on_failure=on_failure,
    )

    print(f"\n{'=' * 40}")
    print("Tạo hoàn tất!")
    print(f"   ✅ Thành công: {len(successes)}")
    print(f"   ❌ Thất bại: {len(failures)}")
    print(f"{'=' * 40}")

    return (len(successes), len(failures))


def main():
    parser = argparse.ArgumentParser(description="Tạo ảnh thiết kế manh mối")
    parser.add_argument("--all", action="store_true", help="Tạo ảnh cho tất cả manh mối đang chờ xử lý")
    parser.add_argument("--clue", help="Chỉ định tên của một manh mối")
    parser.add_argument("--clues", nargs="+", help="Chỉ định tên của nhiều manh mối")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh sách các manh mối đang chờ tạo")

    args = parser.parse_args()

    try:
        if args.list:
            list_pending_clues()
        elif args.all:
            _, fail = generate_batch_clues()
            sys.exit(0 if fail == 0 else 1)
        elif args.clues:
            _, fail = generate_batch_clues(args.clues)
            sys.exit(0 if fail == 0 else 1)
        elif args.clue:
            output_path = generate_clue(args.clue)
            print(f"\n🖼️  Vui lòng xem ảnh đã tạo: {output_path}")
        else:
            parser.print_help()
            print("\n❌ Vui lòng chỉ định --all, --clues, --clue hoặc --list")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

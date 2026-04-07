#!/usr/bin/env python3
"""
Character Generator - Sử dụng Gemini API tạo ảnh thiết kế nhân vật

Usage:
    python generate_character.py --character "Trương Tam"
    python generate_character.py --characters "Trương Tam" "Lý Tứ"
    python generate_character.py --all
    python generate_character.py --list

Note:
    Ảnh tham chiếu sẽ tự động được đọc từ trường reference_image trong project.json
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


def generate_character(
    character_name: str,
) -> Path:
    """
    Tạo ảnh thiết kế cho một nhân vật

    Args:
        character_name: Tên nhân vật

    Returns:
        Đường dẫn ảnh được tạo
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)

    # Lấy thông tin nhân vật từ project.json
    project = pm.load_project(project_name)

    description = ""
    if "characters" in project and character_name in project["characters"]:
        char_info = project["characters"][character_name]
        description = char_info.get("description", "")

    if not description:
        raise ValueError(f"Mô tả của nhân vật '{character_name}' trống, vui lòng thêm mô tả trong project.json trước")

    print(f"🎨 Đang tạo ảnh thiết kế nhân vật: {character_name}")
    print(f"   Mô tả: {description[:50]}...")

    queued = enqueue_and_wait(
        project_name=project_name,
        task_type="character",
        media_type="image",
        resource_id=character_name,
        payload={"prompt": description},
        source="skill",
    )
    result = queued.get("result") or {}
    relative_path = result.get("file_path") or f"characters/{character_name}.png"
    output_path = project_dir / relative_path
    version = result.get("version")
    version_text = f" (Phiên bản v{version})" if version is not None else ""
    print(f"✅ Ảnh thiết kế nhân vật đã được lưu: {output_path}{version_text}")
    return output_path


def list_pending_characters() -> None:
    """Liệt kê các nhân vật đang chờ tạo ảnh thiết kế"""
    pm, project_name = ProjectManager.from_cwd()
    pending = pm.get_pending_characters(project_name)

    if not pending:
        print(f"✅ Tất cả nhân vật trong dự án '{project_name}' đều đã có ảnh thiết kế")
        return

    print(f"\n📋 Nhân vật chờ tạo ({len(pending)}):\n")
    for char in pending:
        print(f"  🧑 {char['name']}")
        desc = char.get("description", "")
        print(f"     Mô tả: {desc[:60]}..." if len(desc) > 60 else f"     Mô tả: {desc}")
        print()


def generate_batch_characters(
    character_names: list[str] | None = None,
) -> tuple[int, int]:
    """
    Tạo ảnh thiết kế nhân vật hàng loạt (tất cả vào hàng đợi, Worker xử lý song song)

    Args:
        character_names: Danh sách tên nhân vật được chỉ định. None tượng trưng cho tất cả các nhân vật đang chờ xử lý.

    Returns:
        (Số lượng thành công, Số lượng thất bại)
    """
    pm, project_name = ProjectManager.from_cwd()
    project = pm.load_project(project_name)

    if character_names:
        chars = project.get("characters", {})
        names_to_process = []
        for name in character_names:
            if name not in chars:
                print(f"⚠️  Nhân vật '{name}' không tồn tại trong project.json, bỏ qua")
                continue
            if not chars[name].get("description"):
                print(f"⚠️  Nhân vật '{name}' thiếu mô tả, bỏ qua")
                continue
            names_to_process.append(name)
    else:
        pending = pm.get_pending_characters(project_name)
        names_to_process = [c["name"] for c in pending]

    if not names_to_process:
        print("✅ Không có nhân vật nào cần tạo")
        return (0, 0)

    specs = [
        BatchTaskSpec(
            task_type="character",
            media_type="image",
            resource_id=name,
            payload={"prompt": project["characters"][name]["description"]},
        )
        for name in names_to_process
    ]

    total = len(specs)
    print(f"\n🚀 Nộp hàng loạt {total} yêu cầu tạo hình nhân vật vào hàng đợi...\n")

    def on_success(br: BatchTaskResult) -> None:
        version = (br.result or {}).get("version")
        version_text = f" (Phiên bản v{version})" if version is not None else ""
        print(f"✅ Ảnh thiết kế nhân vật: {br.resource_id} hoàn tất{version_text}")

    def on_failure(br: BatchTaskResult) -> None:
        print(f"❌ Ảnh thiết kế nhân vật: {br.resource_id} thất bại - {br.error}")

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
    parser = argparse.ArgumentParser(description="Tạo ảnh thiết kế nhân vật")
    parser.add_argument("--character", help="Chỉ định tên của một nhân vật")
    parser.add_argument("--characters", nargs="+", help="Chỉ định tên của nhiều nhân vật")
    parser.add_argument("--all", action="store_true", help="Tạo ảnh cho tất cả nhân vật đang chờ xử lý")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh sách các nhân vật đang chờ tạo")

    args = parser.parse_args()

    try:
        if args.list:
            list_pending_characters()
        elif args.all:
            _, fail = generate_batch_characters()
            sys.exit(0 if fail == 0 else 1)
        elif args.characters:
            _, fail = generate_batch_characters(args.characters)
            sys.exit(0 if fail == 0 else 1)
        elif args.character:
            output_path = generate_character(args.character)
            print(f"\n🖼️  Vui lòng xem ảnh đã tạo: {output_path}")
        else:
            parser.print_help()
            print("\n❌ Vui lòng chỉ định --all, --characters, --character hoặc --list")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

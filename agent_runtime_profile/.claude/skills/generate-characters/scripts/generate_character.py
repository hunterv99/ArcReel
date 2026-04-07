#!/usr/bin/env python3
"""
<<<<<<< HEAD
Character Generator - Sử dụng Gemini API tạo ảnh thiết kế nhân vật

Usage:
    python generate_character.py --character "Trương Tam"
    python generate_character.py --characters "Trương Tam" "Lý Tứ"
=======
Character Generator - 使用 Gemini API 生成角色设计图

Usage:
    python generate_character.py --character "张三"
    python generate_character.py --characters "张三" "李四"
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    python generate_character.py --all
    python generate_character.py --list

Note:
<<<<<<< HEAD
    Ảnh tham chiếu sẽ tự động được đọc từ trường reference_image trong project.json
=======
    参考图会自动从 project.json 中的 reference_image 字段读取
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
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
<<<<<<< HEAD
    Tạo ảnh thiết kế cho một nhân vật

    Args:
        character_name: Tên nhân vật

    Returns:
        Đường dẫn ảnh được tạo
=======
    生成单个角色设计图

    Args:
        character_name: 角色名称

    Returns:
        生成的图片路径
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)

<<<<<<< HEAD
    # Lấy thông tin nhân vật từ project.json
=======
    # 从 project.json 获取角色信息
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    project = pm.load_project(project_name)

    description = ""
    if "characters" in project and character_name in project["characters"]:
        char_info = project["characters"][character_name]
        description = char_info.get("description", "")

    if not description:
<<<<<<< HEAD
        raise ValueError(f"Mô tả của nhân vật '{character_name}' trống, vui lòng thêm mô tả trong project.json trước")

    print(f"🎨 Đang tạo ảnh thiết kế nhân vật: {character_name}")
    print(f"   Mô tả: {description[:50]}...")
=======
        raise ValueError(f"角色 '{character_name}' 的描述为空，请先在 project.json 中添加描述")

    print(f"🎨 正在生成角色设计图: {character_name}")
    print(f"   描述: {description[:50]}...")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

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
<<<<<<< HEAD
    version_text = f" (Phiên bản v{version})" if version is not None else ""
    print(f"✅ Ảnh thiết kế nhân vật đã được lưu: {output_path}{version_text}")
=======
    version_text = f" (版本 v{version})" if version is not None else ""
    print(f"✅ 角色设计图已保存: {output_path}{version_text}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    return output_path


def list_pending_characters() -> None:
<<<<<<< HEAD
    """Liệt kê các nhân vật đang chờ tạo ảnh thiết kế"""
=======
    """列出待生成设计图的角色"""
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    pm, project_name = ProjectManager.from_cwd()
    pending = pm.get_pending_characters(project_name)

    if not pending:
<<<<<<< HEAD
        print(f"✅ Tất cả nhân vật trong dự án '{project_name}' đều đã có ảnh thiết kế")
        return

    print(f"\n📋 Nhân vật chờ tạo ({len(pending)}):\n")
    for char in pending:
        print(f"  🧑 {char['name']}")
        desc = char.get("description", "")
        print(f"     Mô tả: {desc[:60]}..." if len(desc) > 60 else f"     Mô tả: {desc}")
=======
        print(f"✅ 项目 '{project_name}' 中所有角色都已有设计图")
        return

    print(f"\n📋 待生成的角色 ({len(pending)} 个):\n")
    for char in pending:
        print(f"  🧑 {char['name']}")
        desc = char.get("description", "")
        print(f"     描述: {desc[:60]}..." if len(desc) > 60 else f"     描述: {desc}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        print()


def generate_batch_characters(
    character_names: list[str] | None = None,
) -> tuple[int, int]:
    """
<<<<<<< HEAD
    Tạo ảnh thiết kế nhân vật hàng loạt (tất cả vào hàng đợi, Worker xử lý song song)

    Args:
        character_names: Danh sách tên nhân vật được chỉ định. None tượng trưng cho tất cả các nhân vật đang chờ xử lý.

    Returns:
        (Số lượng thành công, Số lượng thất bại)
=======
    批量生成角色设计图（全部入队，由 Worker 并行处理）

    Args:
        character_names: 指定的角色名称列表。None 表示所有待处理角色。

    Returns:
        (成功数, 失败数)
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    """
    pm, project_name = ProjectManager.from_cwd()
    project = pm.load_project(project_name)

    if character_names:
        chars = project.get("characters", {})
        names_to_process = []
        for name in character_names:
            if name not in chars:
<<<<<<< HEAD
                print(f"⚠️  Nhân vật '{name}' không tồn tại trong project.json, bỏ qua")
                continue
            if not chars[name].get("description"):
                print(f"⚠️  Nhân vật '{name}' thiếu mô tả, bỏ qua")
=======
                print(f"⚠️  角色 '{name}' 不存在于 project.json 中，跳过")
                continue
            if not chars[name].get("description"):
                print(f"⚠️  角色 '{name}' 缺少描述，跳过")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
                continue
            names_to_process.append(name)
    else:
        pending = pm.get_pending_characters(project_name)
        names_to_process = [c["name"] for c in pending]

    if not names_to_process:
<<<<<<< HEAD
        print("✅ Không có nhân vật nào cần tạo")
=======
        print("✅ 没有需要生成的角色")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
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
<<<<<<< HEAD
    print(f"\n🚀 Nộp hàng loạt {total} yêu cầu tạo hình nhân vật vào hàng đợi...\n")

    def on_success(br: BatchTaskResult) -> None:
        version = (br.result or {}).get("version")
        version_text = f" (Phiên bản v{version})" if version is not None else ""
        print(f"✅ Ảnh thiết kế nhân vật: {br.resource_id} hoàn tất{version_text}")

    def on_failure(br: BatchTaskResult) -> None:
        print(f"❌ Ảnh thiết kế nhân vật: {br.resource_id} thất bại - {br.error}")
=======
    print(f"\n🚀 批量提交 {total} 个角色设计图到生成队列...\n")

    def on_success(br: BatchTaskResult) -> None:
        version = (br.result or {}).get("version")
        version_text = f" (版本 v{version})" if version is not None else ""
        print(f"✅ 角色设计图: {br.resource_id} 完成{version_text}")

    def on_failure(br: BatchTaskResult) -> None:
        print(f"❌ 角色设计图: {br.resource_id} 失败 - {br.error}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

    successes, failures = batch_enqueue_and_wait_sync(
        project_name=project_name,
        specs=specs,
        on_success=on_success,
        on_failure=on_failure,
    )

    print(f"\n{'=' * 40}")
<<<<<<< HEAD
    print("Tạo hoàn tất!")
    print(f"   ✅ Thành công: {len(successes)}")
    print(f"   ❌ Thất bại: {len(failures)}")
=======
    print("生成完成!")
    print(f"   ✅ 成功: {len(successes)}")
    print(f"   ❌ 失败: {len(failures)}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    print(f"{'=' * 40}")

    return (len(successes), len(failures))


def main():
<<<<<<< HEAD
    parser = argparse.ArgumentParser(description="Tạo ảnh thiết kế nhân vật")
    parser.add_argument("--character", help="Chỉ định tên của một nhân vật")
    parser.add_argument("--characters", nargs="+", help="Chỉ định tên của nhiều nhân vật")
    parser.add_argument("--all", action="store_true", help="Tạo ảnh cho tất cả nhân vật đang chờ xử lý")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh sách các nhân vật đang chờ tạo")
=======
    parser = argparse.ArgumentParser(description="生成角色设计图")
    parser.add_argument("--character", help="指定单个角色名称")
    parser.add_argument("--characters", nargs="+", help="指定多个角色名称")
    parser.add_argument("--all", action="store_true", help="生成所有待处理的角色")
    parser.add_argument("--list", action="store_true", help="列出待生成的角色")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

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
<<<<<<< HEAD
            print(f"\n🖼️  Vui lòng xem ảnh đã tạo: {output_path}")
        else:
            parser.print_help()
            print("\n❌ Vui lòng chỉ định --all, --characters, --character hoặc --list")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Lỗi: {e}")
=======
            print(f"\n🖼️  请查看生成的图片: {output_path}")
        else:
            parser.print_help()
            print("\n❌ 请指定 --all、--characters、--character 或 --list")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 错误: {e}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        sys.exit(1)


if __name__ == "__main__":
    main()

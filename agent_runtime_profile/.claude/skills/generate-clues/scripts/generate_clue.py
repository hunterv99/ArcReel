#!/usr/bin/env python3
"""
<<<<<<< HEAD
Clue Generator - Sử dụng Gemini API tạo ảnh thiết kế manh mối

Usage:
    python generate_clue.py --all
    python generate_clue.py --clue "Ngọc bội"
    python generate_clue.py --clues "Ngọc bội" "Cây hòe cổ thụ"
=======
Clue Generator - 使用 Gemini API 生成线索设计图

Usage:
    python generate_clue.py --all
    python generate_clue.py --clue "玉佩"
    python generate_clue.py --clues "玉佩" "老槐树"
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    python generate_clue.py --list

Example:
    python generate_clue.py --all
<<<<<<< HEAD
    python generate_clue.py --clue "Cây hòe cổ thụ"
=======
    python generate_clue.py --clue "老槐树"
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


def generate_clue(clue_name: str) -> Path:
    """
<<<<<<< HEAD
    Tạo ảnh thiết kế cho một manh mối

    Args:
        clue_name: Tên manh mối

    Returns:
        Đường dẫn ảnh được tạo
=======
    生成单个线索设计图

    Args:
        clue_name: 线索名称

    Returns:
        生成的图片路径
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)

<<<<<<< HEAD
    # Lấy thông tin manh mối
=======
    # 获取线索信息
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    clue = pm.get_clue(project_name, clue_name)
    clue_type = clue.get("type", "prop")
    description = clue.get("description", "")

    if not description:
<<<<<<< HEAD
        raise ValueError(f"Mô tả của manh mối '{clue_name}' trống, vui lòng thêm mô tả trước")

    print(f"🎨 Đang tạo ảnh thiết kế manh mối: {clue_name}")
    print(f"   Loại: {clue_type}")
    print(f"   Mô tả: {description[:50]}..." if len(description) > 50 else f"   Mô tả: {description}")
=======
        raise ValueError(f"线索 '{clue_name}' 的描述为空，请先添加描述")

    print(f"🎨 正在生成线索设计图: {clue_name}")
    print(f"   类型: {clue_type}")
    print(f"   描述: {description[:50]}..." if len(description) > 50 else f"   描述: {description}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

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
<<<<<<< HEAD
    version_text = f" (Phiên bản v{version})" if version is not None else ""
    print(f"✅ Ảnh thiết kế manh mối đã được lưu: {output_path}{version_text}")
=======
    version_text = f" (版本 v{version})" if version is not None else ""
    print(f"✅ 线索设计图已保存: {output_path}{version_text}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    return output_path


def list_pending_clues() -> None:
    """
<<<<<<< HEAD
    Liệt kê các manh mối đang chờ tạo
=======
    列出待生成的线索
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    """
    pm, project_name = ProjectManager.from_cwd()
    pending = pm.get_pending_clues(project_name)

    if not pending:
<<<<<<< HEAD
        print(f"✅ Tất cả manh mối quan trọng trong dự án '{project_name}' đều đã có ảnh thiết kế")
        return

    print(f"\n📋 Manh mối chờ tạo ({len(pending)}):\n")
=======
        print(f"✅ 项目 '{project_name}' 中所有重要线索都已有设计图")
        return

    print(f"\n📋 待生成的线索 ({len(pending)} 个):\n")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    for clue in pending:
        clue_type = clue.get("type", "prop")
        type_emoji = "📦" if clue_type == "prop" else "🏠"
        print(f"  {type_emoji} {clue['name']}")
<<<<<<< HEAD
        print(f"     Loại: {clue_type}")
        print(f"     Mô tả: {clue.get('description', '')[:60]}...")
=======
        print(f"     类型: {clue_type}")
        print(f"     描述: {clue.get('description', '')[:60]}...")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        print()


def generate_batch_clues(
    clue_names: list[str] | None = None,
) -> tuple[int, int]:
    """
<<<<<<< HEAD
    Tạo ảnh thiết kế manh mối hàng loạt (tất cả vào hàng đợi, Worker xử lý song song)

    Args:
        clue_names: Danh sách tên manh mối được chỉ định. None tượng trưng cho tất cả các manh mối đang chờ xử lý.

    Returns:
        (Số lượng thành công, Số lượng thất bại)
=======
    批量生成线索设计图（全部入队，由 Worker 并行处理）

    Args:
        clue_names: 指定的线索名称列表。None 表示所有待处理线索。

    Returns:
        (成功数, 失败数)
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    """
    pm, project_name = ProjectManager.from_cwd()
    project = pm.load_project(project_name)
    clues_dict = project.get("clues", {})

    if clue_names:
        names_to_process = []
        for name in clue_names:
            if name not in clues_dict:
<<<<<<< HEAD
                print(f"⚠️  Manh mối '{name}' không tồn tại trong project.json, bỏ qua")
                continue
            if not clues_dict[name].get("description"):
                print(f"⚠️  Manh mối '{name}' thiếu mô tả, bỏ qua")
=======
                print(f"⚠️  线索 '{name}' 不存在于 project.json 中，跳过")
                continue
            if not clues_dict[name].get("description"):
                print(f"⚠️  线索 '{name}' 缺少描述，跳过")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
                continue
            names_to_process.append(name)
    else:
        pending = pm.get_pending_clues(project_name)
        names_to_process = [c["name"] for c in pending]

    if not names_to_process:
<<<<<<< HEAD
        print("✅ Không có manh mối nào cần tạo")
=======
        print("✅ 没有需要生成的线索")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
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
<<<<<<< HEAD
    print(f"\n🚀 Nộp hàng loạt {total} yêu cầu tạo hình manh mối vào hàng đợi...\n")

    def on_success(br: BatchTaskResult) -> None:
        version = (br.result or {}).get("version")
        version_text = f" (Phiên bản v{version})" if version is not None else ""
        print(f"✅ Ảnh thiết kế manh mối: {br.resource_id} hoàn tất{version_text}")

    def on_failure(br: BatchTaskResult) -> None:
        print(f"❌ Ảnh thiết kế manh mối: {br.resource_id} thất bại - {br.error}")
=======
    print(f"\n🚀 批量提交 {total} 个线索设计图到生成队列...\n")

    def on_success(br: BatchTaskResult) -> None:
        version = (br.result or {}).get("version")
        version_text = f" (版本 v{version})" if version is not None else ""
        print(f"✅ 线索设计图: {br.resource_id} 完成{version_text}")

    def on_failure(br: BatchTaskResult) -> None:
        print(f"❌ 线索设计图: {br.resource_id} 失败 - {br.error}")
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
    parser = argparse.ArgumentParser(description="Tạo ảnh thiết kế manh mối")
    parser.add_argument("--all", action="store_true", help="Tạo ảnh cho tất cả manh mối đang chờ xử lý")
    parser.add_argument("--clue", help="Chỉ định tên của một manh mối")
    parser.add_argument("--clues", nargs="+", help="Chỉ định tên của nhiều manh mối")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh sách các manh mối đang chờ tạo")
=======
    parser = argparse.ArgumentParser(description="生成线索设计图")
    parser.add_argument("--all", action="store_true", help="生成所有待处理的线索")
    parser.add_argument("--clue", help="指定单个线索名称")
    parser.add_argument("--clues", nargs="+", help="指定多个线索名称")
    parser.add_argument("--list", action="store_true", help="列出待生成的线索")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

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
<<<<<<< HEAD
            print(f"\n🖼️  Vui lòng xem ảnh đã tạo: {output_path}")
        else:
            parser.print_help()
            print("\n❌ Vui lòng chỉ định --all, --clues, --clue hoặc --list")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Lỗi: {e}")
=======
            print(f"\n🖼️  请查看生成的图片: {output_path}")
        else:
            parser.print_help()
            print("\n❌ 请指定 --all、--clues、--clue 或 --list")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 错误: {e}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        sys.exit(1)


if __name__ == "__main__":
    main()

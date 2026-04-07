#!/usr/bin/env python3
"""
<<<<<<< HEAD
generate_script.py - Sử dụng Gemini tạo kịch bản JSON

Usage:
=======
generate_script.py - 使用 Gemini 生成 JSON 剧本

用法:
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    python generate_script.py --episode <N>
    python generate_script.py --episode <N> --output <path>
    python generate_script.py --episode <N> --dry-run

<<<<<<< HEAD
Example:
=======
示例:
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    python generate_script.py --episode 1
    python generate_script.py --episode 1 --output scripts/ep1.json
"""

import argparse
import sys
from pathlib import Path

<<<<<<< HEAD
# Cho phép chạy script này trực tiếp từ bất kỳ thư mục làm việc nào trong repository
=======
# 允许从仓库任意工作目录直接运行该脚本
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # .claude/skills/generate-script/scripts -> repo root
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.project_manager import ProjectManager
from lib.script_generator import ScriptGenerator


def main():
    parser = argparse.ArgumentParser(
<<<<<<< HEAD
        description="Sử dụng Gemini tạo kịch bản JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
=======
        description="使用 Gemini 生成 JSON 剧本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    %(prog)s --episode 1
    %(prog)s --episode 1 --output scripts/ep1.json
    %(prog)s --episode 1 --dry-run
        """,
    )

<<<<<<< HEAD
    parser.add_argument("--episode", "-e", type=int, required=True, help="Số thứ tự tập")
=======
    parser.add_argument("--episode", "-e", type=int, required=True, help="剧集编号")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
<<<<<<< HEAD
        help="Đường dẫn tệp đầu ra (mặc định: scripts/episode_N.json)",
    )

    parser.add_argument("--dry-run", action="store_true", help="Chỉ hiển thị Prompt, không thực sự gọi API")

    args = parser.parse_args()

    # Xây dựng đường dẫn dự án
    pm, project_name = ProjectManager.from_cwd()
    project_path = pm.get_project_path(project_name)

    # Kiểm tra xem tệp trung gian có tồn tại không (xác định tên tệp dựa trên content_mode)
=======
        help="输出文件路径（默认: scripts/episode_N.json）",
    )

    parser.add_argument("--dry-run", action="store_true", help="仅显示 Prompt，不实际调用 API")

    args = parser.parse_args()

    # 构建项目路径
    pm, project_name = ProjectManager.from_cwd()
    project_path = pm.get_project_path(project_name)

    # 检查中间文件是否存在（根据 content_mode 确定文件名）
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    import json as _json

    project_json_path = project_path / "project.json"
    content_mode = "narration"
    if project_json_path.exists():
        try:
            content_mode = _json.loads(project_json_path.read_text(encoding="utf-8")).get("content_mode", "narration")
        except Exception:
<<<<<<< HEAD
            pass  # Sử dụng giá trị mặc định "narration" nếu đọc hoặc parse thất bại
=======
            pass  # 读取或解析失败时降级使用默认值 "narration"
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

    drafts_path = project_path / "drafts" / f"episode_{args.episode}"
    if content_mode == "drama":
        step1_path = drafts_path / "step1_normalized_script.md"
        step1_hint = "normalize_drama_script.py"
    else:
        step1_path = drafts_path / "step1_segments.md"
<<<<<<< HEAD
        step1_hint = "Chia đoạn (Step 1)"

    if not step1_path.exists():
        print(f"❌ Không tìm thấy tệp Step 1: {step1_path}")
        print(f"   Vui lòng hoàn thành {step1_hint} trước")
=======
        step1_hint = "片段拆分（Step 1）"

    if not step1_path.exists():
        print(f"❌ 未找到 Step 1 文件: {step1_path}")
        print(f"   请先完成 {step1_hint}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        sys.exit(1)

    try:
        if args.dry_run:
<<<<<<< HEAD
            # dry-run không cần client
            generator = ScriptGenerator(project_path)
            print("=" * 60)
            print("DRY RUN - Dưới đây là Prompt sẽ được gửi cho Gemini:")
=======
            # dry-run 不需要 client
            generator = ScriptGenerator(project_path)
            print("=" * 60)
            print("DRY RUN - 以下是将发送给 Gemini 的 Prompt:")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
            print("=" * 60)
            prompt = generator.build_prompt(args.episode)
            print(prompt)
            print("=" * 60)
            return

<<<<<<< HEAD
        # Thực sự tạo (Bất đồng bộ)
=======
        # 实际生成（异步）
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        import asyncio

        async def _run():
            generator = await ScriptGenerator.create(project_path)
            output_path = Path(args.output) if args.output else None
            return await generator.generate(
                episode=args.episode,
                output_path=output_path,
            )

        result_path = asyncio.run(_run())

<<<<<<< HEAD
        print(f"\n✅ Tạo kịch bản hoàn tất: {result_path}")

    except FileNotFoundError as e:
        print(f"❌ Lỗi tệp: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Tạo thất bại: {e}")
=======
        print(f"\n✅ 剧本生成完成: {result_path}")

    except FileNotFoundError as e:
        print(f"❌ 文件错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成失败: {e}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

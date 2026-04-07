#!/usr/bin/env python3
"""
normalize_drama_script.py - Sử dụng Gemini Pro tạo kịch bản chuẩn hóa

Chuyển đổi tiểu thuyết gốc trong source/ thành kịch bản chuẩn hóa định dạng Markdown (step1_normalized_script.md),
để generate_script.py sử dụng.

Usage:
    python normalize_drama_script.py --episode <N>
    python normalize_drama_script.py --episode <N> --source <file>
    python normalize_drama_script.py --episode <N> --dry-run
"""

import argparse
import sys
from pathlib import Path

# Cho phép chạy script này trực tiếp từ bất kỳ thư mục làm việc nào trong repository
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # .claude/skills/generate-script/scripts -> repo root
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asyncio

from lib.project_manager import ProjectManager
from lib.text_backends.base import TextGenerationRequest, TextTaskType
from lib.text_backends.factory import create_text_backend_for_task


def build_normalize_prompt(
    novel_text: str,
    project_overview: dict,
    style: str,
    characters: dict,
    clues: dict,
) -> str:
    """Xây dựng Prompt cho kịch bản chuẩn hóa"""

    char_list = "\n".join(f"- {name}" for name in characters.keys()) or "（Chưa có）"
    clue_list = "\n".join(f"- {name}" for name in clues.keys()) or "（Chưa có）"

    return f"""Nhiệm vụ của bạn là chuyển thể nội dung tiểu thuyết gốc thành bảng phân cảnh có cấu trúc (định dạng Markdown), để AI tiếp tục sử dụng để tạo video.

## Thông tin dự án

<overview>
{project_overview.get("synopsis", "")}

Thể loại：{project_overview.get("genre", "")}
Chủ đề cốt lõi：{project_overview.get("theme", "")}
Bối cảnh thế giới：{project_overview.get("world_setting", "")}
</overview>

<style>
{style}
</style>

<characters>
{char_list}
</characters>

<clues>
{clue_list}
</clues>

## Tiểu thuyết gốc

<novel>
{novel_text}
</novel>

## Yêu cầu đầu ra

Chuyển thể tiểu thuyết thành danh sách cảnh, sử dụng định dạng bảng Markdown:

| ID Cảnh | Mô tả cảnh | Thời lượng | Loại cảnh | segment_break |
|---------|---------|------|---------|---------------|
| E{{N}}S01 | Mô tả cảnh chi tiết... | 8 | Cốt truyện | Có |
| E{{N}}S02 | Mô tả cảnh chi tiết... | 8 | Hội thoại | Không |

Quy tắc：
- Định dạng ID Cảnh：E{{Số tập}}S{{Số thứ tự 2 chữ số}} (VD: E1S01, E1S02)
- Mô tả cảnh：Mô tả đã được kịch bản hóa, bao gồm hành động của nhân vật, hội thoại, môi trường, phù hợp để thể hiện bằng hình ảnh
- Thời lượng：4、6 hoặc 8 giây (mặc định 8 giây, hình ảnh đơn giản có thể dùng 4 hoặc 6 giây)
- Loại cảnh：Cốt truyện、Hành động、Hội thoại、Chuyển cảnh、Cảnh tĩnh
- segment_break：Đánh dấu "Có" tại điểm chuyển cảnh, "Không" cho cùng một cảnh liên tục
- Mỗi cảnh nên là một khung hình ảnh độc lập, có thể hoàn thành trong thời lượng quy định
- Tránh một cảnh chứa nhiều hành động khác nhau hoặc chuyển đồ cảnh

Chỉ xuất ra bảng Markdown, không bao gồm các văn bản giải thích bổ sung.
"""


def main():
    parser = argparse.ArgumentParser(
        description="Sử dụng Gemini Pro tạo kịch bản chuẩn hóa",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    %(prog)s --episode 1
    %(prog)s --episode 1 --source source/chapter1.txt
    %(prog)s --episode 1 --dry-run
        """,
    )

    parser.add_argument("--episode", "-e", type=int, required=True, help="Số thứ tự tập")
    parser.add_argument(
        "--source",
        "-s",
        type=str,
        default=None,
        help="Chỉ định đường dẫn tệp nguồn tiểu thuyết (mặc định lấy tất cả các tệp trong thư mục source/)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Chỉ hiển thị Prompt, không thực sự gọi API")

    args = parser.parse_args()

    # Xây dựng đường dẫn dự án
    pm, project_name = ProjectManager.from_cwd()
    project_path = pm.get_project_path(project_name)
    project = pm.load_project(project_name)

    # Đọc tiểu thuyết gốc
    if args.source:
        source_path = (project_path / args.source).resolve()
        if not source_path.is_relative_to(project_path.resolve()):
            print(f"❌ Đường dẫn vượt quá thư mục dự án: {source_path}")
            sys.exit(1)
        if not source_path.exists():
            print(f"❌ Không tìm thấy tệp nguồn: {source_path}")
            sys.exit(1)
        novel_text = source_path.read_text(encoding="utf-8")
    else:
        source_dir = project_path / "source"
        if not source_dir.exists() or not any(source_dir.iterdir()):
            print(f"❌ Thư mục source/ rỗng hoặc không tồn tại: {source_dir}")
            sys.exit(1)
        # Đọc tất cả các tệp văn bản theo thứ tự tên tệp
        texts = []
        for f in sorted(source_dir.iterdir()):
            if f.suffix in (".txt", ".md", ".text"):
                texts.append(f.read_text(encoding="utf-8"))
        novel_text = "\n\n".join(texts)

    if not novel_text.strip():
        print("❌ Tiểu thuyết gốc rỗng")
        sys.exit(1)

    # Xây dựng Prompt
    prompt = build_normalize_prompt(
        novel_text=novel_text,
        project_overview=project.get("overview", {}),
        style=project.get("style", ""),
        characters=project.get("characters", {}),
        clues=project.get("clues", {}),
    )

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN - Dưới đây là Prompt sẽ được gửi cho Gemini:")
        print("=" * 60)
        print(prompt)
        print("=" * 60)
        print(f"\nĐộ dài Prompt: {len(prompt)} ký tự")
        return

    # Gọi TextBackend
    async def _run():
        backend = await create_text_backend_for_task(TextTaskType.SCRIPT)
        print(f"Đang sử dụng {backend.model} để tạo kịch bản chuẩn hóa...")
        result = await backend.generate(TextGenerationRequest(prompt=prompt))
        return result.text

    response = asyncio.run(_run())

    # Lưu tệp
    drafts_dir = project_path / "drafts" / f"episode_{args.episode}"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    step1_path = drafts_dir / "step1_normalized_script.md"
    step1_path.write_text(response.strip(), encoding="utf-8")
    print(f"✅ Kịch bản chuẩn hóa đã được lưu: {step1_path}")

    # Thống kê tóm tắt
    lines = [
        line
        for line in response.split("\n")
        if line.strip().startswith("|") and "ID Cảnh" not in line and "---" not in line
    ]
    scene_count = len(lines)
    print(f"\n📊 Thống kê khởi tạo: {scene_count} cảnh")


if __name__ == "__main__":
    main()

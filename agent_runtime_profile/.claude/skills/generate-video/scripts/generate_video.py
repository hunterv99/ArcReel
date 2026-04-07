#!/usr/bin/env python3
"""
Video Generator - Sử dụng Veo 3.1 API tạo video phân cảnh

Usage:
    # Tạo theo từng tập (Khuyến nghị)
    python generate_video.py episode_N.json --episode N

    # Tiếp tục từ điểm dừng
    python generate_video.py episode_N.json --episode N --resume

    # Chế độ một cảnh
    python generate_video.py episode_N.json --scene SCENE_ID

    # Chế độ hàng loạt (Tạo độc lập từng cảnh)
    python generate_video.py episode_N.json --all

Mỗi cảnh tạo video độc lập, sử dụng ảnh phân cảnh làm khung hình bắt đầu, sau đó dùng ffmpeg để ghép lại.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from collections.abc import Callable
from datetime import datetime
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
from lib.prompt_utils import is_structured_video_prompt, video_prompt_to_yaml

# ============================================================================
# Xây dựng Prompt
# ============================================================================


def get_video_prompt(item: dict) -> str:
    """
    Lấy Prompt tạo video

    Hỗ trợ định dạng prompt có cấu trúc: Nếu video_prompt là dict, nó sẽ được chuyển sang định dạng YAML.

    Args:
        item: Dict chứa đoạn/cảnh

    Returns:
        chuỗi video_prompt (có thể là định dạng YAML hoặc chuỗi thông thường)
    """
    prompt = item.get("video_prompt")
    if not prompt:
        item_id = item.get("segment_id") or item.get("scene_id")
        raise ValueError(f"Đoạn/Cảnh thiếu trường video_prompt: {item_id}")

    # Kiểm tra xem có phải định dạng có cấu trúc không
    if is_structured_video_prompt(prompt):
        # Chuyển sang định dạng YAML
        return video_prompt_to_yaml(prompt)

    # Tránh truyền trực tiếp kiểu dict gây lỗi type
    if isinstance(prompt, dict):
        item_id = item.get("segment_id") or item.get("scene_id")
        raise ValueError(f"video_prompt của đoạn/cảnh là object nhưng định dạng không đúng chuẩn cấu trúc: {item_id}")

    if not isinstance(prompt, str):
        item_id = item.get("segment_id") or item.get("scene_id")
        raise TypeError(f"Loại video_prompt của đoạn/cảnh không hợp lệ (mong đợi str hoặc dict): {item_id}")

    return prompt


def get_items_from_script(script: dict) -> tuple:
    """
    Lấy danh sách cảnh/đoạn và các trường liên quan dựa trên chế độ nội dung

    Args:
        script: Dữ liệu kịch bản

    Returns:
        Tuple (items_list, id_field, char_field, clue_field)
    """
    content_mode = script.get("content_mode", "narration")
    if content_mode == "narration" and "segments" in script:
        return (script["segments"], "segment_id", "characters_in_segment", "clues_in_segment")
    return (script.get("scenes", []), "scene_id", "characters_in_scene", "clues_in_scene")


def parse_scene_ids(scenes_arg: str) -> list:
    """Parse danh sách ID cảnh được phân tách bằng dấu phẩy"""
    return [s.strip() for s in scenes_arg.split(",") if s.strip()]


def validate_duration(duration: int) -> str:
    """
    Xác thực và trả về tham số thời lượng hợp lệ

    Veo API chỉ hỗ trợ 4s/6s/8s

    Args:
        duration: Thời lượng đầu vào (giây)

    Returns:
        Chuỗi thời lượng hợp lệ
    """
    valid_durations = [4, 6, 8]
    if duration in valid_durations:
        return str(duration)
    # Làm tròn lên giá trị hợp lệ gần nhất
    for d in valid_durations:
        if d >= duration:
            return str(d)
    return "8"  # Giá trị tối đa


# ============================================================================
# Quản lý Checkpoint
# ============================================================================


def get_checkpoint_path(project_dir: Path, episode: int) -> Path:
    """Lấy đường dẫn tệp checkpoint"""
    return project_dir / "videos" / f".checkpoint_ep{episode}.json"


def load_checkpoint(project_dir: Path, episode: int) -> dict | None:
    """
    Tải checkpoint

    Returns:
        dict checkpoint hoặc None
    """
    checkpoint_path = get_checkpoint_path(project_dir, episode)
    if checkpoint_path.exists():
        with open(checkpoint_path, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_checkpoint(project_dir: Path, episode: int, completed_scenes: list, started_at: str):
    """Lưu checkpoint"""
    checkpoint_path = get_checkpoint_path(project_dir, episode)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

    checkpoint = {
        "episode": episode,
        "completed_scenes": completed_scenes,
        "started_at": started_at,
        "updated_at": datetime.now().isoformat(),
    }

    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)


def clear_checkpoint(project_dir: Path, episode: int):
    """Xóa checkpoint"""
    checkpoint_path = get_checkpoint_path(project_dir, episode)
    if checkpoint_path.exists():
        checkpoint_path.unlink()


# ============================================================================
# Ghép video bằng FFmpeg
# ============================================================================


def concatenate_videos(video_paths: list, output_path: Path) -> Path:
    """
    Sử dụng ffmpeg để ghép nhiều đoạn video

    Args:
        video_paths: Danh sách đường dẫn tệp video
        output_path: Đường dẫn đầu ra

    Returns:
        Đường dẫn video đầu ra
    """
    if len(video_paths) == 1:
        # Chỉ có một đoạn, sao chép trực tiếp
        import shutil

        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(video_paths[0], output_path)
        return output_path

    # Tạo danh sách tệp tạm thời
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for video_path in video_paths:
            f.write(f"file '{video_path}'\n")
        list_file = f.name

    try:
        # Sử dụng ffmpeg concat demuxer
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", str(output_path)]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Video đã được ghép: {output_path}")
        return output_path
    finally:
        Path(list_file).unlink()


# ============================================================================
# Hàm hỗ trợ tạo nhiệm vụ hàng loạt
# ============================================================================


def _build_video_specs(
    *,
    items: list,
    id_field: str,
    content_mode: str,
    script_filename: str,
    project_dir: Path,
    skip_ids: list[str] | None = None,
) -> tuple[list[BatchTaskSpec], dict[str, int]]:
    """
    从场景/片段列表构建 BatchTaskSpec 和 resource_id -> order_index 映射。

    Bỏ qua các mục thiếu ảnh phân cảnh hoặc prompt không hợp lệ, và in cảnh báo.

    Returns:
        (specs, order_map)  order_map: resource_id -> vị trí trong items gốc
    """
    item_type = "Đoạn" if content_mode == "narration" else "Cảnh"
    default_duration = 4 if content_mode == "narration" else 8
    skip_set = set(skip_ids or [])

    specs: list[BatchTaskSpec] = []
    order_map: dict[str, int] = {}

    for idx, item in enumerate(items):
        item_id = item.get(id_field) or item.get("scene_id") or item.get("segment_id") or f"item_{idx}"

        if item_id in skip_set:
            continue

        storyboard_image = (item.get("generated_assets") or {}).get("storyboard_image")
        if not storyboard_image:
            print(f"⚠️  {item_type} {item_id} không có ảnh phân cảnh, bỏ qua")
            continue
        storyboard_path = project_dir / storyboard_image
        if not storyboard_path.exists():
            print(f"⚠️  Ảnh phân cảnh không tồn tại: {storyboard_path}, bỏ qua")
            continue

        try:
            prompt = get_video_prompt(item)
        except Exception as e:
            print(f"⚠️  video_prompt của {item_type} {item_id} không hợp lệ, bỏ qua: {e}")
            continue

        duration = item.get("duration_seconds", default_duration)
        duration_str = validate_duration(duration)

        specs.append(
            BatchTaskSpec(
                task_type="video",
                media_type="video",
                resource_id=item_id,
                payload={
                    "prompt": prompt,
                    "script_file": script_filename,
                    "duration_seconds": int(duration_str),
                },
                script_file=script_filename,
            )
        )
        order_map[item_id] = idx

    return specs, order_map


def _scan_completed_items(
    items: list,
    id_field: str,
    item_type: str,
    completed_scenes: list[str],
    videos_dir: Path,
) -> tuple[list[Path | None], list[str]]:
    """Scan items for already-completed videos; return ordered paths and done IDs."""
    ordered_paths: list[Path | None] = [None] * len(items)
    already_done: list[str] = []
    for idx, item in enumerate(items):
        item_id = item.get(id_field, item.get("scene_id", f"item_{idx}"))
        video_output = videos_dir / f"scene_{item_id}.mp4"
        if item_id in completed_scenes and video_output.exists():
            print(f"  [{idx + 1}/{len(items)}] {item_type} {item_id} ✓ 已完成")
            ordered_paths[idx] = video_output
            already_done.append(item_id)
        elif item_id in completed_scenes:
            completed_scenes.remove(item_id)
    return ordered_paths, already_done


def _submit_and_wait_with_checkpoint(
    *,
    project_name: str,
    project_dir: Path,
    specs: list[BatchTaskSpec],
    order_map: dict[str, int],
    ordered_paths: list[Path | None],
    completed_scenes: list[str],
    save_fn: Callable[[], None],
    item_type: str,
) -> list[BatchTaskResult]:
    """Submit specs via batch_enqueue_and_wait_sync with checkpoint on each success."""
    print(f"\n🚀 Nộp hàng loạt {len(specs)} yêu cầu tạo video vào hàng đợi...\n")

    def on_success(br: BatchTaskResult) -> None:
        result = br.result or {}
        relative_path = result.get("file_path") or f"videos/scene_{br.resource_id}.mp4"
        output_path = project_dir / relative_path
        ordered_paths[order_map[br.resource_id]] = output_path
        completed_scenes.append(br.resource_id)
        save_fn()
        print(f"    ✅ Hoàn tất: {output_path.name}")

    def on_failure(br: BatchTaskResult) -> None:
        print(f"    ❌ {br.resource_id} thất bại: {br.error}")

    _, failures = batch_enqueue_and_wait_sync(
        project_name=project_name,
        specs=specs,
        on_success=on_success,
        on_failure=on_failure,
    )

    if failures:
        print(f"\n⚠️  {len(failures)} {item_type} tạo thất bại:")
        for f in failures:
            print(f"   - {f.resource_id}: {f.error}")
        print("    💡 Sử dụng cờ --resume để tiếp tục từ điểm này")
        raise RuntimeError(f"{len(failures)} {item_type} tạo thất bại")

    return failures


# ============================================================================
# Tạo video theo Episode (Tạo độc lập từng cảnh)
# ============================================================================


def generate_episode_video(
    script_filename: str,
    episode: int,
    resume: bool = False,
) -> list[Path]:
    """
    Tạo tệp video cho tất cả cảnh trong tập được chỉ định.

    Mỗi cảnh tạo video độc lập, sử dụng ảnh phân cảnh làm khung hình bắt đầu.
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)
    script = pm.load_script(project_name, script_filename)
    content_mode = script.get("content_mode", "narration")
    all_items, id_field, _, _ = get_items_from_script(script)

    episode_items = [s for s in all_items if s.get("episode", 1) == episode]
    if not episode_items:
        raise ValueError(f"Không tìm thấy cảnh/đoạn cho tập {episode}")

    item_type = "Đoạn" if content_mode == "narration" else "Cảnh"
    print(f"📋 Tập {episode} có tổng cộng {len(episode_items)} {item_type}")

    # Checkpoint
    completed_scenes: list[str] = []
    started_at = datetime.now().isoformat()
    if resume:
        checkpoint = load_checkpoint(project_dir, episode)
        if checkpoint:
            completed_scenes = checkpoint.get("completed_scenes", [])
            started_at = checkpoint.get("started_at", started_at)
            print(f"🔄 Khôi phục từ checkpoint, đã hoàn thành {len(completed_scenes)} cảnh")
        else:
            print("⚠️  Không tìm thấy checkpoint, tạo lại từ đầu")

    videos_dir = project_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

    ordered_video_paths, already_done_ids = _scan_completed_items(
        episode_items,
        id_field,
        item_type,
        completed_scenes,
        videos_dir,
    )
    specs, order_map = _build_video_specs(
        items=episode_items,
        id_field=id_field,
        content_mode=content_mode,
        script_filename=script_filename,
        project_dir=project_dir,
        skip_ids=already_done_ids,
    )

    if not specs and not any(ordered_video_paths):
        raise RuntimeError("Không có đoạn video nào để tạo")

    if specs:
        _submit_and_wait_with_checkpoint(
            project_name=project_name,
            project_dir=project_dir,
            specs=specs,
            order_map=order_map,
            ordered_paths=ordered_video_paths,
            completed_scenes=completed_scenes,
            save_fn=lambda: save_checkpoint(project_dir, episode, completed_scenes, started_at),
            item_type=item_type,
        )

    scene_videos = [p for p in ordered_video_paths if p is not None]
    if not scene_videos:
        raise RuntimeError("Không có đoạn video nào được tạo")

    clear_checkpoint(project_dir, episode)
    print(f"\n🎉 Tạo video tập {episode} hoàn tất, tổng cộng {len(scene_videos)} đoạn")
    return scene_videos


# ============================================================================
# Tạo một cảnh
# ============================================================================


def generate_scene_video(script_filename: str, scene_id: str) -> Path:
    """
    Tạo video cho một cảnh/đoạn

    Args:
        script_filename: Tên tệp kịch bản
        scene_id: ID cảnh/đoạn

    Returns:
        Đường dẫn video được tạo
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)

    # Tải kịch bản
    script = pm.load_script(project_name, script_filename)
    content_mode = script.get("content_mode", "narration")
    all_items, id_field, _, _ = get_items_from_script(script)

    # Tìm cảnh/đoạn được chỉ định
    item = None
    for s in all_items:
        if s.get(id_field) == scene_id or s.get("scene_id") == scene_id:
            item = s
            break

    if not item:
        raise ValueError(f"Cảnh/Đoạn '{scene_id}' không tồn tại")

    # Kiểm tra ảnh phân cảnh
    storyboard_image = item.get("generated_assets", {}).get("storyboard_image")
    if not storyboard_image:
        raise ValueError(f"Cảnh/Đoạn '{scene_id}' không có ảnh phân cảnh, vui lòng chạy generate-storyboard trước")

    storyboard_path = project_dir / storyboard_image
    if not storyboard_path.exists():
        raise FileNotFoundError(f"Ảnh phân cảnh không tồn tại: {storyboard_path}")

    # Trực tiếp dùng trường video_prompt
    prompt = get_video_prompt(item)

    # Lấy thời lượng (Chế độ kể chuyện mặc định 4s, hoạt hình nhiều tập mặc định 8s)
    default_duration = 4 if content_mode == "narration" else 8
    duration = item.get("duration_seconds", default_duration)
    duration_str = validate_duration(duration)

    print(f"🎬 Đang tạo video: Cảnh/Đoạn {scene_id}")
    print("   Thời gian đợi dự kiến: 1-6 phút")

    queued = enqueue_and_wait(
        project_name=project_name,
        task_type="video",
        media_type="video",
        resource_id=scene_id,
        payload={
            "prompt": prompt,
            "script_file": script_filename,
            "duration_seconds": int(duration_str),
        },
        script_file=script_filename,
        source="skill",
    )
    result = queued.get("result") or {}
    relative_path = result.get("file_path") or f"videos/scene_{scene_id}.mp4"
    output_path = project_dir / relative_path

    print(f"✅ Video đã được lưu: {output_path}")
    return output_path


def generate_all_videos(script_filename: str) -> list:
    """
    Tạo video cho tất cả các cảnh đang chờ xử lý (Chế độ độc lập)

    Returns:
        Danh sách đường dẫn video được tạo
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)

    # Tải kịch bản
    script = pm.load_script(project_name, script_filename)
    content_mode = script.get("content_mode", "narration")
    all_items, id_field, _, _ = get_items_from_script(script)

    pending_items = [item for item in all_items if not (item.get("generated_assets") or {}).get("video_clip")]

    if not pending_items:
        print("✨ Video cho tất cả cảnh/đoạn đều đã được tạo")
        return []

    item_type = "Đoạn" if content_mode == "narration" else "Cảnh"
    print(f"📋 Tổng cộng {len(pending_items)} {item_type} chờ tạo video")
    print("⚠️  Mỗi video có thể cần 1-6 phút, vui lòng kiên nhẫn chờ")
    print("💡 Khuyến nghị dùng chế độ --episode N để tự động ghép")

    specs, _ = _build_video_specs(
        items=pending_items,
        id_field=id_field,
        content_mode=content_mode,
        script_filename=script_filename,
        project_dir=project_dir,
    )

    if not specs:
        print("⚠️  Không có chức năng tạo nhiệm vụ video nào (chắc là thiếu ảnh phân cảnh hoặc prompt)")
        return []

    print(f"\n🚀 Nộp hàng loạt {len(specs)} video vào hàng đợi...\n")

    result_paths: list[Path] = []

    def on_success(br: BatchTaskResult) -> None:
        result = br.result or {}
        relative_path = result.get("file_path") or f"videos/scene_{br.resource_id}.mp4"
        output_path = project_dir / relative_path
        result_paths.append(output_path)
        print(f"✅ Hoàn tất: {output_path.name}")

    def on_failure(br: BatchTaskResult) -> None:
        print(f"❌ {br.resource_id} thất bại: {br.error}")

    _, failures = batch_enqueue_and_wait_sync(
        project_name=project_name,
        specs=specs,
        on_success=on_success,
        on_failure=on_failure,
    )

    if failures:
        print(f"\n⚠️  {len(failures)} {item_type} tạo thất bại:")
        for f in failures:
            print(f"   - {f.resource_id}: {f.error}")

    print(f"\n🎉 Tạo video hàng loạt hoàn tất, tổng cộng {len(result_paths)} cái")
    return result_paths


def generate_selected_videos(
    script_filename: str,
    scene_ids: list,
    resume: bool = False,
) -> list:
    """
    Tạo nhiều video được chỉ định

    Args:
        script_filename: Tên tệp kịch bản
        scene_ids: Danh sách ID cảnh
        resume: Có tiếp tục từ checkpoint không

    Returns:
        Danh sách đường dẫn video được tạo
    """
    import hashlib

    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)
    script = pm.load_script(project_name, script_filename)
    content_mode = script.get("content_mode", "narration")
    all_items, id_field, _, _ = get_items_from_script(script)

    # Lọc các cảnh được chỉ định
    items_by_id = {}
    for item in all_items:
        items_by_id[item.get(id_field, "")] = item
        if "scene_id" in item:
            items_by_id[item["scene_id"]] = item

    selected_items = []
    for scene_id in scene_ids:
        if scene_id in items_by_id:
            selected_items.append(items_by_id[scene_id])
        else:
            print(f"⚠️  Cảnh/Đoạn '{scene_id}' không tồn tại, bỏ qua")

    if not selected_items:
        raise ValueError("Không tìm thấy cảnh/đoạn hợp lệ nào")

    item_type = "Đoạn" if content_mode == "narration" else "Cảnh"
    print(f"📋 Tổng cộng đã chọn {len(selected_items)} {item_type}")

    # Checkpoint
    scenes_hash = hashlib.md5(",".join(scene_ids).encode()).hexdigest()[:8]
    checkpoint_path = project_dir / "videos" / f".checkpoint_selected_{scenes_hash}.json"
    completed_scenes: list[str] = []
    started_at = datetime.now().isoformat()

    if resume and checkpoint_path.exists():
        with open(checkpoint_path, encoding="utf-8") as f:
            checkpoint = json.load(f)
            completed_scenes = checkpoint.get("completed_scenes", [])
            started_at = checkpoint.get("started_at", started_at)
            print(f"🔄 Khôi phục từ checkpoint, đã hoàn tất {len(completed_scenes)} cảnh")

    videos_dir = project_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

    ordered_results, already_done_ids = _scan_completed_items(
        selected_items,
        id_field,
        item_type,
        completed_scenes,
        videos_dir,
    )
    specs, order_map = _build_video_specs(
        items=selected_items,
        id_field=id_field,
        content_mode=content_mode,
        script_filename=script_filename,
        project_dir=project_dir,
        skip_ids=already_done_ids,
    )

    if specs:

        def _save():
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            with open(checkpoint_path, "w", encoding="utf-8") as f_ckpt:
                json.dump(
                    {
                        "scene_ids": scene_ids,
                        "completed_scenes": completed_scenes,
                        "started_at": started_at,
                        "updated_at": datetime.now().isoformat(),
                    },
                    f_ckpt,
                    ensure_ascii=False,
                    indent=2,
                )

        _submit_and_wait_with_checkpoint(
            project_name=project_name,
            project_dir=project_dir,
            specs=specs,
            order_map=order_map,
            ordered_paths=ordered_results,
            completed_scenes=completed_scenes,
            save_fn=_save,
            item_type=item_type,
        )

    final_results = [p for p in ordered_results if p is not None]

    # Xóa checkpoint sau khi hoàn tất tất cả
    if checkpoint_path.exists():
        checkpoint_path.unlink()

    print(f"\n🎉 Tạo hàng loạt video hoàn tất, tổng cộng {len(final_results)} cái")
    return final_results


# ============================================================================
# Giao diện dòng lệnh (CLI)
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Tạo video phân cảnh",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  # Tạo theo từng tập (Khuyến nghị)
  python generate_video.py episode_1.json --episode 1

  # Tiếp tục từ điểm dừng
  python generate_video.py episode_1.json --episode 1 --resume

  # Chế độ tạo 1 cảnh
  python generate_video.py episode_1.json --scene E1S1

  # Chế độ hàng loạt tự chọn
  python generate_video.py episode_1.json --scenes E1S01,E1S05,E1S10

  # Chế độ hàng loạt (tạo độc lập)
  python generate_video.py episode_1.json --all
        """,
    )
    parser.add_argument("script", help="Tên tệp kịch bản")

    # Chọn chế độ
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--scene", help="Chỉ định ID cảnh (chế độ một cảnh)")
    mode_group.add_argument("--scenes", help="Chỉ định nhiều ID cảnh (ngăn cách bằng dấu phẩy), vd: E1S01,E1S05,E1S10")
    mode_group.add_argument("--all", action="store_true", help="Tạo video cho tất cả cảnh chờ xử lý (Chế độ độc lập)")
    mode_group.add_argument("--episode", type=int, help="Tạo và ghép theo tập (Khuyến nghị)")

    # Các lựa chọn khác
    parser.add_argument("--resume", action="store_true", help="Tiếp tục từ điểm ngắt trước")

    args = parser.parse_args()

    try:
        if args.scene:
            generate_scene_video(args.script, args.scene)
        elif args.scenes:
            scene_ids = parse_scene_ids(args.scenes)
            generate_selected_videos(
                args.script,
                scene_ids,
                resume=args.resume,
            )
        elif args.all:
            generate_all_videos(args.script)
        elif args.episode:
            generate_episode_video(
                args.script,
                args.episode,
                resume=args.resume,
            )
        else:
            print("Vui lòng chọn chế độ: --scene, --scenes, --all, hoặc --episode")
            print("Sử dụng --help để xem cú pháp")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

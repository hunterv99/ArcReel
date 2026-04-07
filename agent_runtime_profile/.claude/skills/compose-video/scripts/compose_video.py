#!/usr/bin/env python3
"""
Video Composer - Sử dụng ffmpeg để tổng hợp video cuối cùng

Usage:
    python compose_video.py <script_file> [--output OUTPUT] [--music MUSIC_FILE]

Example:
    python compose_video.py chapter_01_script.json --output chapter_01_final.mp4
    python compose_video.py chapter_01_script.json --music bgm.mp3
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from lib.project_manager import ProjectManager


def check_ffmpeg():
    """Kiểm tra xem ffmpeg có khả dụng không"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_video_duration(video_path: Path) -> float:
    """Lấy thời lượng video"""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        text=True,
    )

    return float(result.stdout.strip())


def concatenate_simple(video_paths: list, output_path: Path):
    """
    Ghép đơn giản (không có hiệu ứng chuyển cảnh)

    Sử dụng concat demuxer để ghép nhanh
    """
    # Tạo danh sách tệp tạm thời
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for path in video_paths:
            # Sử dụng đường dẫn tuyệt đối để tránh lỗi parse đường dẫn tương đối của ffmpeg
            abs_path = path.resolve()
            f.write(f"file '{abs_path}'\n")
        list_file = f.name

    try:
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", str(output_path)]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Lỗi ffmpeg: {result.stderr}")

    finally:
        Path(list_file).unlink()


def concatenate_with_transitions(
    video_paths: list, transitions: list, output_path: Path, transition_duration: float = 0.5
):
    """
    Ghép video có hiệu ứng chuyển cảnh

    Sử dụng filter xfade để thực hiện chuyển cảnh
    """
    if len(video_paths) < 2:
        # Sao chép trực tiếp một video duy nhất
        subprocess.run(["ffmpeg", "-y", "-i", str(video_paths[0]), "-c", "copy", str(output_path)])
        return

    # Xây dựng filter_complex
    inputs = []
    for i, path in enumerate(video_paths):
        inputs.extend(["-i", str(path)])

    # Lấy thời lượng của từng video
    durations = [get_video_duration(p) for p in video_paths]

    # Xây dựng chuỗi filter xfade
    filter_parts = []

    for i in range(len(video_paths) - 1):
        transition = transitions[i] if i < len(transitions) else "fade"

        # Ánh xạ loại xfade
        xfade_type = {
            "cut": None,  # Không sử dụng chuyển cảnh
            "fade": "fade",
            "dissolve": "dissolve",
            "wipe": "wipeleft",
        }.get(transition, "fade")

        if xfade_type is None:
            # Chuyển cảnh cut, không cần xfade
            continue

        if i == 0:
            prev_label = "[0:v]"
        else:
            prev_label = f"[v{i}]"

        next_label = f"[{i + 1}:v]"
        out_label = f"[v{i + 1}]" if i < len(video_paths) - 2 else "[vout]"

        # Tính toán độ lệch
        offset = sum(durations[: i + 1]) - transition_duration * (i + 1)

        filter_parts.append(
            f"{prev_label}{next_label}xfade=transition={xfade_type}:"
            f"duration={transition_duration}:offset={offset:.3f}{out_label}"
        )

    if filter_parts:
        # Âm thanh cũng cần được xử lý
        audio_filter = (
            ";".join([f"[{i}:a]" for i in range(len(video_paths))]) + f"concat=n={len(video_paths)}:v=0:a=1[aout]"
        )

        filter_complex = ";".join(filter_parts) + ";" + audio_filter

        cmd = [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex",
            filter_complex,
            "-map",
            "[vout]",
            "-map",
            "[aout]",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            str(output_path),
        ]
    else:
        # Tất cả đều là chuyển cảnh cut, sử dụng ghép đơn giản
        concatenate_simple(video_paths, output_path)
        return

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"⚠️  Hiệu ứng chuyển cảnh thất bại, thử ghép đơn giản: {result.stderr[:200]}")
        concatenate_simple(video_paths, output_path)


def add_background_music(video_path: Path, music_path: Path, output_path: Path, music_volume: float = 0.3):
    """
    Thêm nhạc nền

    Args:
        video_path: Tệp video
        music_path: Tệp nhạc
        output_path: Tệp đầu ra
        music_volume: Âm lượng nhạc nền (0-1)
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-i",
        str(music_path),
        "-filter_complex",
        f"[1:a]volume={music_volume}[bg];[0:a][bg]amix=inputs=2:duration=first[aout]",
        "-map",
        "0:v",
        "-map",
        "[aout]",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Thêm nhạc nền thất bại: {result.stderr}")


def compose_video(
    script_filename: str, output_filename: str = None, music_path: str = None, use_transitions: bool = True
) -> Path:
    """
    Tổng hợp video cuối cùng

    Args:
        script_filename: Tên tệp kịch bản
        output_filename: Tên tệp đầu ra
        music_path: Đường dẫn tệp nhạc nền
        use_transitions: Có sử dụng hiệu ứng chuyển cảnh không

    Returns:
        Đường dẫn video đầu ra
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)

    # Tải kịch bản
    script = pm.load_script(project_name, script_filename)

    # Thu thập các đoạn video
    video_paths = []
    transitions = []

    for scene in script["scenes"]:
        video_clip = scene.get("generated_assets", {}).get("video_clip")
        if not video_clip:
            raise ValueError(f"Cảnh {scene['scene_id']} thiếu đoạn video")

        video_path = project_dir / video_clip
        if not video_path.exists():
            raise FileNotFoundError(f"Tệp video không tồn tại: {video_path}")

        video_paths.append(video_path)
        transitions.append(scene.get("transition_to_next", "cut"))

    if not video_paths:
        raise ValueError("Không có đoạn video khả dụng")

    print(f"📹 Tổng cộng {len(video_paths)} đoạn video")

    # Xác định đường dẫn đầu ra
    if output_filename is None:
        chapter = script["novel"].get("chapter", "output").replace(" ", "_")
        output_filename = f"{chapter}_final.mp4"

    output_path = project_dir / "output" / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Tổng hợp video
    print("🎬 Đang tổng hợp video...")

    if use_transitions and any(t != "cut" for t in transitions):
        concatenate_with_transitions(video_paths, transitions, output_path)
    else:
        concatenate_simple(video_paths, output_path)

    print(f"✅ Tổng hợp video hoàn tất: {output_path}")

    # Thêm nhạc nền
    if music_path:
        music_file = Path(music_path)
        if not music_file.exists():
            music_file = project_dir / music_path

        if music_file.exists():
            print("🎵 Đang thêm nhạc nền...")
            final_output = output_path.with_stem(output_path.stem + "_with_music")
            add_background_music(output_path, music_file, final_output)
            output_path = final_output
            print(f"✅ Thêm nhạc nền hoàn tất: {output_path}")
        else:
            print(f"⚠️  Tệp nhạc nền không tồn tại: {music_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Tổng hợp video cuối cùng")
    parser.add_argument("script", help="Tên tệp kịch bản")
    parser.add_argument("--output", help="Tên tệp đầu ra")
    parser.add_argument("--music", help="Tệp nhạc nền")
    parser.add_argument("--no-transitions", action="store_true", help="Không sử dụng hiệu ứng chuyển cảnh")

    args = parser.parse_args()

    # Kiểm tra ffmpeg
    if not check_ffmpeg():
        print("❌ Lỗi: ffmpeg chưa được cài đặt hoặc không có trong PATH")
        print("   Vui lòng cài đặt ffmpeg: brew install ffmpeg (macOS/Linux) hoặc tải từ trang chủ cho Windows")
        sys.exit(1)

    try:
        output_path = compose_video(args.script, args.output, args.music, use_transitions=not args.no_transitions)

        print(f"\n🎉 Video cuối cùng: {output_path}")
        print("   Các đoạn riêng lẻ được giữ lại trong: videos/")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

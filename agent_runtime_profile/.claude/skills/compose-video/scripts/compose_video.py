#!/usr/bin/env python3
"""
<<<<<<< HEAD
Video Composer - Sử dụng ffmpeg để tổng hợp video cuối cùng
=======
Video Composer - 使用 ffmpeg 合成最终视频
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

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
<<<<<<< HEAD
    """Kiểm tra xem ffmpeg có khả dụng không"""
=======
    """检查 ffmpeg 是否可用"""
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_video_duration(video_path: Path) -> float:
<<<<<<< HEAD
    """Lấy thời lượng video"""
=======
    """获取视频时长"""
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
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
<<<<<<< HEAD
    Ghép đơn giản (không có hiệu ứng chuyển cảnh)

    Sử dụng concat demuxer để ghép nhanh
    """
    # Tạo danh sách tệp tạm thời
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for path in video_paths:
            # Sử dụng đường dẫn tuyệt đối để tránh lỗi parse đường dẫn tương đối của ffmpeg
=======
    简单拼接（无转场效果）

    使用 concat demuxer 进行快速拼接
    """
    # 创建临时文件列表
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for path in video_paths:
            # 使用绝对路径，避免 ffmpeg 解析相对路径出错
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
            abs_path = path.resolve()
            f.write(f"file '{abs_path}'\n")
        list_file = f.name

    try:
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", str(output_path)]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
<<<<<<< HEAD
            raise RuntimeError(f"Lỗi ffmpeg: {result.stderr}")
=======
            raise RuntimeError(f"ffmpeg 错误: {result.stderr}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

    finally:
        Path(list_file).unlink()


def concatenate_with_transitions(
    video_paths: list, transitions: list, output_path: Path, transition_duration: float = 0.5
):
    """
<<<<<<< HEAD
    Ghép video có hiệu ứng chuyển cảnh

    Sử dụng filter xfade để thực hiện chuyển cảnh
    """
    if len(video_paths) < 2:
        # Sao chép trực tiếp một video duy nhất
        subprocess.run(["ffmpeg", "-y", "-i", str(video_paths[0]), "-c", "copy", str(output_path)])
        return

    # Xây dựng filter_complex
=======
    使用转场效果拼接视频

    使用 xfade 滤镜实现转场
    """
    if len(video_paths) < 2:
        # 单个视频直接复制
        subprocess.run(["ffmpeg", "-y", "-i", str(video_paths[0]), "-c", "copy", str(output_path)])
        return

    # 构建 filter_complex
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    inputs = []
    for i, path in enumerate(video_paths):
        inputs.extend(["-i", str(path)])

<<<<<<< HEAD
    # Lấy thời lượng của từng video
    durations = [get_video_duration(p) for p in video_paths]

    # Xây dựng chuỗi filter xfade
=======
    # 获取每个视频的时长
    durations = [get_video_duration(p) for p in video_paths]

    # 构建 xfade 滤镜链
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    filter_parts = []

    for i in range(len(video_paths) - 1):
        transition = transitions[i] if i < len(transitions) else "fade"

<<<<<<< HEAD
        # Ánh xạ loại xfade
        xfade_type = {
            "cut": None,  # Không sử dụng chuyển cảnh
=======
        # xfade 类型映射
        xfade_type = {
            "cut": None,  # 不使用转场
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
            "fade": "fade",
            "dissolve": "dissolve",
            "wipe": "wipeleft",
        }.get(transition, "fade")

        if xfade_type is None:
<<<<<<< HEAD
            # Chuyển cảnh cut, không cần xfade
=======
            # cut 转场，不需要 xfade
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
            continue

        if i == 0:
            prev_label = "[0:v]"
        else:
            prev_label = f"[v{i}]"

        next_label = f"[{i + 1}:v]"
        out_label = f"[v{i + 1}]" if i < len(video_paths) - 2 else "[vout]"

<<<<<<< HEAD
        # Tính toán độ lệch
=======
        # 计算偏移量
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        offset = sum(durations[: i + 1]) - transition_duration * (i + 1)

        filter_parts.append(
            f"{prev_label}{next_label}xfade=transition={xfade_type}:"
            f"duration={transition_duration}:offset={offset:.3f}{out_label}"
        )

    if filter_parts:
<<<<<<< HEAD
        # Âm thanh cũng cần được xử lý
=======
        # 音频也需要处理
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
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
<<<<<<< HEAD
        # Tất cả đều là chuyển cảnh cut, sử dụng ghép đơn giản
=======
        # 全是 cut 转场，使用简单拼接
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        concatenate_simple(video_paths, output_path)
        return

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
<<<<<<< HEAD
        print(f"⚠️  Hiệu ứng chuyển cảnh thất bại, thử ghép đơn giản: {result.stderr[:200]}")
=======
        print(f"⚠️  转场效果失败，尝试简单拼接: {result.stderr[:200]}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        concatenate_simple(video_paths, output_path)


def add_background_music(video_path: Path, music_path: Path, output_path: Path, music_volume: float = 0.3):
    """
<<<<<<< HEAD
    Thêm nhạc nền

    Args:
        video_path: Tệp video
        music_path: Tệp nhạc
        output_path: Tệp đầu ra
        music_volume: Âm lượng nhạc nền (0-1)
=======
    添加背景音乐

    Args:
        video_path: 视频文件
        music_path: 音乐文件
        output_path: 输出文件
        music_volume: 背景音乐音量 (0-1)
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
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
<<<<<<< HEAD
        raise RuntimeError(f"Thêm nhạc nền thất bại: {result.stderr}")
=======
        raise RuntimeError(f"添加背景音乐失败: {result.stderr}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3


def compose_video(
    script_filename: str, output_filename: str = None, music_path: str = None, use_transitions: bool = True
) -> Path:
    """
<<<<<<< HEAD
    Tổng hợp video cuối cùng

    Args:
        script_filename: Tên tệp kịch bản
        output_filename: Tên tệp đầu ra
        music_path: Đường dẫn tệp nhạc nền
        use_transitions: Có sử dụng hiệu ứng chuyển cảnh không

    Returns:
        Đường dẫn video đầu ra
=======
    合成最终视频

    Args:
        script_filename: 剧本文件名
        output_filename: 输出文件名
        music_path: 背景音乐文件路径
        use_transitions: 是否使用转场效果

    Returns:
        输出视频路径
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    """
    pm, project_name = ProjectManager.from_cwd()
    project_dir = pm.get_project_path(project_name)

<<<<<<< HEAD
    # Tải kịch bản
    script = pm.load_script(project_name, script_filename)

    # Thu thập các đoạn video
=======
    # 加载剧本
    script = pm.load_script(project_name, script_filename)

    # 收集视频片段
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    video_paths = []
    transitions = []

    for scene in script["scenes"]:
        video_clip = scene.get("generated_assets", {}).get("video_clip")
        if not video_clip:
<<<<<<< HEAD
            raise ValueError(f"Cảnh {scene['scene_id']} thiếu đoạn video")

        video_path = project_dir / video_clip
        if not video_path.exists():
            raise FileNotFoundError(f"Tệp video không tồn tại: {video_path}")
=======
            raise ValueError(f"场景 {scene['scene_id']} 缺少视频片段")

        video_path = project_dir / video_clip
        if not video_path.exists():
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

        video_paths.append(video_path)
        transitions.append(scene.get("transition_to_next", "cut"))

    if not video_paths:
<<<<<<< HEAD
        raise ValueError("Không có đoạn video khả dụng")

    print(f"📹 Tổng cộng {len(video_paths)} đoạn video")

    # Xác định đường dẫn đầu ra
=======
        raise ValueError("没有可用的视频片段")

    print(f"📹 共 {len(video_paths)} 个视频片段")

    # 确定输出路径
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    if output_filename is None:
        chapter = script["novel"].get("chapter", "output").replace(" ", "_")
        output_filename = f"{chapter}_final.mp4"

    output_path = project_dir / "output" / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

<<<<<<< HEAD
    # Tổng hợp video
    print("🎬 Đang tổng hợp video...")
=======
    # 合成视频
    print("🎬 正在合成视频...")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

    if use_transitions and any(t != "cut" for t in transitions):
        concatenate_with_transitions(video_paths, transitions, output_path)
    else:
        concatenate_simple(video_paths, output_path)

<<<<<<< HEAD
    print(f"✅ Tổng hợp video hoàn tất: {output_path}")

    # Thêm nhạc nền
=======
    print(f"✅ 视频合成完成: {output_path}")

    # 添加背景音乐
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
    if music_path:
        music_file = Path(music_path)
        if not music_file.exists():
            music_file = project_dir / music_path

        if music_file.exists():
<<<<<<< HEAD
            print("🎵 Đang thêm nhạc nền...")
            final_output = output_path.with_stem(output_path.stem + "_with_music")
            add_background_music(output_path, music_file, final_output)
            output_path = final_output
            print(f"✅ Thêm nhạc nền hoàn tất: {output_path}")
        else:
            print(f"⚠️  Tệp nhạc nền không tồn tại: {music_path}")
=======
            print("🎵 正在添加背景音乐...")
            final_output = output_path.with_stem(output_path.stem + "_with_music")
            add_background_music(output_path, music_file, final_output)
            output_path = final_output
            print(f"✅ 背景音乐添加完成: {output_path}")
        else:
            print(f"⚠️  背景音乐文件不存在: {music_path}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

    return output_path


def main():
<<<<<<< HEAD
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
=======
    parser = argparse.ArgumentParser(description="合成最终视频")
    parser.add_argument("script", help="剧本文件名")
    parser.add_argument("--output", help="输出文件名")
    parser.add_argument("--music", help="背景音乐文件")
    parser.add_argument("--no-transitions", action="store_true", help="不使用转场效果")

    args = parser.parse_args()

    # 检查 ffmpeg
    if not check_ffmpeg():
        print("❌ 错误: ffmpeg 未安装或不在 PATH 中")
        print("   请安装 ffmpeg: brew install ffmpeg (macOS)")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        sys.exit(1)

    try:
        output_path = compose_video(args.script, args.output, args.music, use_transitions=not args.no_transitions)

<<<<<<< HEAD
        print(f"\n🎉 Video cuối cùng: {output_path}")
        print("   Các đoạn riêng lẻ được giữ lại trong: videos/")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
=======
        print(f"\n🎉 最终视频: {output_path}")
        print("   单独片段保留在: videos/")

    except Exception as e:
        print(f"❌ 错误: {e}")
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
        sys.exit(1)


if __name__ == "__main__":
    main()

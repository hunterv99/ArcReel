---
name: compose-video
<<<<<<< HEAD
description: Hậu kỳ và tổng hợp video. Sử dụng khi người dùng yêu cầu "thêm nhạc nền", "gộp video", "thêm đoạn đầu và đoạn cuối", muốn thêm BGM cho video thành phẩm, hoặc cần ghép nhiều tập video lại với nhau.
---

# Tổng hợp Video

Sử dụng ffmpeg để xử lý hậu kỳ video và tổng hợp nhiều đoạn phim.

## Các tình huống sử dụng

### 1. Thêm nhạc nền (BGM)
=======
description: 视频后期处理与合成。当用户说"加背景音乐"、"合并视频"、"加片头片尾"、想为成片添加 BGM、或需要将多集视频拼接时使用。
---

# 合成视频

使用 ffmpeg 进行视频后期处理和多片段合成。

## 使用场景

### 1. 添加背景音乐
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

```bash
python .claude/skills/compose-video/scripts/compose_video.py --episode {N} --music background_music.mp3 --music-volume 0.3
```

<<<<<<< HEAD
### 2. Gộp nhiều tập video
=======
### 2. 合并多集视频
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

```bash
python .claude/skills/compose-video/scripts/compose_video.py --merge-episodes 1 2 3 --output final_movie.mp4
```

<<<<<<< HEAD
### 3. Thêm đoạn giới thiệu và đoạn kết (Intro/Outro)
=======
### 3. 添加片头片尾
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

```bash
python .claude/skills/compose-video/scripts/compose_video.py --episode {N} --intro intro.mp4 --outro outro.mp4
```

<<<<<<< HEAD
### 4. Ghép nối dự phòng (Fallback)

Trong quy trình thông thường, video được Veo 3.1 tạo độc lập cho từng cảnh và cuối cùng cần được ghép lại thành một tập hoàn chỉnh. Khi việc ghép nối có hiệu ứng chuyển cảnh tiêu chuẩn (filter xfade) thất bại do tham số mã hóa không nhất quán, chế độ dự phòng sẽ sử dụng concat demuxer của ffmpeg để ghép nhanh không chuyển cảnh, đảm bảo ít nhất có thể xuất ra video hoàn chỉnh:
=======
### 4. 后备拼接

正常流程中视频由 Veo 3.1 逐场景独立生成，最终需要拼接成完整剧集。当标准的转场拼接（xfade 滤镜）因编码参数不一致而失败时，后备模式使用 ffmpeg concat demuxer 做无转场的快速拼接，确保至少能输出完整视频：
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

```bash
python .claude/skills/compose-video/scripts/compose_video.py --episode {N} --fallback-mode
```

<<<<<<< HEAD
## Quy trình làm việc

1. **Tải dự án và kịch bản** — Kiểm tra xem các tệp video có tồn tại hay không.
2. **Chọn chế độ xử lý** — Thêm BGM / Gộp nhiều tập / Thêm Intro, Outro / Ghép nối dự phòng.
3. **Thực thi xử lý** — Sử dụng ffmpeg để xử lý, giữ nguyên video gốc, xuất kết quả vào thư mục `output/`.

## Các loại chuyển cảnh (Chế độ dự phòng)

Dựa trên trường `transition_to_next` trong kịch bản:

| Loại | Filter ffmpeg |
|------|-------------|
| cut | Ghép trực tiếp |
=======
## 工作流程

1. **加载项目和剧本** — 检查视频文件是否存在
2. **选择处理模式** — 添加 BGM / 合并多集 / 添加片头片尾 / 后备拼接
3. **执行处理** — 使用 ffmpeg 处理，保持原始视频不变，输出到 `output/`

## 转场类型（后备模式）

根据剧本中的 `transition_to_next` 字段：

| 类型 | ffmpeg 滤镜 |
|------|-------------|
| cut | 直接拼接 |
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3
| fade | `xfade=transition=fade:duration=0.5` |
| dissolve | `xfade=transition=dissolve:duration=0.5` |
| wipe | `xfade=transition=wipeleft:duration=0.5` |

<<<<<<< HEAD
## Kiểm tra trước khi xử lý

- [ ] Các video cảnh quay tồn tại và có thể phát được.
- [ ] Độ phân giải video nhất quán (tỷ lệ khung hình do content_mode quyết định).
- [ ] Tệp nhạc nền / Intro / Outro tồn tại (nếu cần).
- [ ] ffmpeg đã được cài đặt và có trong PATH.
=======
## 处理前检查

- [ ] 场景视频存在且可播放
- [ ] 视频分辨率一致（由 content_mode 决定画面比例）
- [ ] 背景音乐 / 片头片尾文件存在（如需要）
- [ ] ffmpeg 已安装并在 PATH 中
>>>>>>> 7101250fbd452cd6228fdd93b27d061dd856a3e3

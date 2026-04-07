---
name: compose-video
description: Hậu kỳ và tổng hợp video. Sử dụng khi người dùng yêu cầu "thêm nhạc nền", "gộp video", "thêm đoạn đầu và đoạn cuối", muốn thêm BGM cho video thành phẩm, hoặc cần ghép nhiều tập video lại với nhau.
---

# Tổng hợp Video

Sử dụng ffmpeg để xử lý hậu kỳ video và tổng hợp nhiều đoạn phim.

## Các tình huống sử dụng

### 1. Thêm nhạc nền (BGM)

```bash
python .claude/skills/compose-video/scripts/compose_video.py --episode {N} --music background_music.mp3 --music-volume 0.3
```

### 2. Gộp nhiều tập video

```bash
python .claude/skills/compose-video/scripts/compose_video.py --merge-episodes 1 2 3 --output final_movie.mp4
```

### 3. Thêm đoạn giới thiệu và đoạn kết (Intro/Outro)

```bash
python .claude/skills/compose-video/scripts/compose_video.py --episode {N} --intro intro.mp4 --outro outro.mp4
```

### 4. Ghép nối dự phòng (Fallback)

Trong quy trình thông thường, video được Veo 3.1 tạo độc lập cho từng cảnh và cuối cùng cần được ghép lại thành một tập hoàn chỉnh. Khi việc ghép nối có hiệu ứng chuyển cảnh tiêu chuẩn (filter xfade) thất bại do tham số mã hóa không nhất quán, chế độ dự phòng sẽ sử dụng concat demuxer của ffmpeg để ghép nhanh không chuyển cảnh, đảm bảo ít nhất có thể xuất ra video hoàn chỉnh:

```bash
python .claude/skills/compose-video/scripts/compose_video.py --episode {N} --fallback-mode
```

## Quy trình làm việc

1. **Tải dự án và kịch bản** — Kiểm tra xem các tệp video có tồn tại hay không.
2. **Chọn chế độ xử lý** — Thêm BGM / Gộp nhiều tập / Thêm Intro, Outro / Ghép nối dự phòng.
3. **Thực thi xử lý** — Sử dụng ffmpeg để xử lý, giữ nguyên video gốc, xuất kết quả vào thư mục `output/`.

## Các loại chuyển cảnh (Chế độ dự phòng)

Dựa trên trường `transition_to_next` trong kịch bản:

| Loại | Filter ffmpeg |
|------|-------------|
| cut | Ghép trực tiếp |
| fade | `xfade=transition=fade:duration=0.5` |
| dissolve | `xfade=transition=dissolve:duration=0.5` |
| wipe | `xfade=transition=wipeleft:duration=0.5` |

## Kiểm tra trước khi xử lý

- [ ] Các video cảnh quay tồn tại và có thể phát được.
- [ ] Độ phân giải video nhất quán (tỷ lệ khung hình do content_mode quyết định).
- [ ] Tệp nhạc nền / Intro / Outro tồn tại (nếu cần).
- [ ] ffmpeg đã được cài đặt và có trong PATH.

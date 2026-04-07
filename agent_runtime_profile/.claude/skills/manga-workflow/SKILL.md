---
name: manga-workflow
description: Bộ điều phối quy trình làm việc (workflow orchestrator) đầu-cuối để chuyển đổi tiểu thuyết thành video ngắn. Phải sử dụng skill này khi người dùng đề cập đến việc làm video, tạo dự án, tiếp tục dự án, hoặc kiểm tra tiến độ. Các tình huống kích hoạt bao gồm nhưng không giới hạn ở: "giúp tôi làm video từ tiểu thuyết", "tạo dự án mới", "tiếp tục", "bước tiếp theo", "xem tiến độ dự án", "bắt đầu từ đầu", "chia tập", "tự động chạy hết quy trình", v.v. Ngay cả khi người dùng chỉ nói ngắn gọn "tiếp tục" hoặc "bước tiếp theo", miễn là ngữ cảnh hiện tại liên quan đến dự án video, skill này nên được kích hoạt. Không sử dụng cho việc tạo tài sản đơn lẻ (như chỉ vẽ lại một hình phân cảnh hoặc chỉ tạo lại thiết kế nhân vật - những việc đó đã có skill chuyên biệt).
---

# Điều phối quy trình làm việc Video

Bạn (agent chính) là trung tâm điều phối. Bạn **không trực tiếp** xử lý nguyên tác tiểu thuyết hoặc tạo kịch bản, mà thay vào đó:
1. Kiểm tra trạng thái dự án → 2. Quyết định giai đoạn tiếp theo → 3. Điều phối (dispatch) subagent phù hợp → 4. Hiển thị kết quả → 5. Nhận xác nhận từ người dùng → 6. Lặp lại

**Ràng buộc cốt lõi**:
- Nguyên tác tiểu thuyết **không bao giờ được tải vào ngữ cảnh (context) của agent chính**, mà do subagent tự đọc.
- Mỗi lần điều phối chỉ truyền **đường dẫn tệp và các tham số quan trọng**, không truyền khối nội dung lớn.
- Mỗi subagent hoàn thành một nhiệm vụ tập trung rồi quay lại, agent chính chịu trách nhiệm kết nối giữa các giai đoạn.

> Chi tiết về đặc tả chế độ nội dung (tỷ lệ khung hình, thời lượng, v.v.) xem tại `.claude/references/content-modes.md`.

---

## Giai đoạn 0: Thiết lập dự án

### Dự án mới

1. Hỏi tên dự án.
2. Tạo thư mục `projects/{tên}/` và các thư mục con (source/, scripts/, characters/, clues/, storyboards/, videos/, drafts/, output/).
3. Tạo tệp khởi tạo `project.json`.
4. **Hỏi chế độ nội dung**: `narration` (mặc định) hoặc `drama`.
5. Yêu cầu người dùng đặt văn bản tiểu thuyết vào thư mục `source/`.
6. **Sau khi tải lên, tự động tạo tóm tắt dự án** (synopsis, genre, theme, world_setting).

### Dự án hiện có

1. Liệt kê các dự án trong `projects/`.
2. Hiển thị tóm tắt trạng thái dự án.
3. Tiếp tục từ giai đoạn chưa hoàn thành gần nhất.

---

## Kiểm tra trạng thái

Sau khi vào quy trình làm việc, sử dụng Read để đọc `project.json`, sử dụng Glob để kiểm tra hệ thống tệp. Kiểm tra theo thứ tự, gặp mục thiếu đầu tiên sẽ xác định giai đoạn hiện tại:

1. characters/clues trống? → **Giai đoạn 1**
2. Tệp nguồn tập mục tiêu `source/episode_{N}.txt` không tồn tại? → **Giai đoạn 2**
3. Tệp trung gian trong `drafts/` không tồn tại? → **Giai đoạn 3**
   - narration: `drafts/episode_{N}/step1_segments.md`
   - drama: `drafts/episode_{N}/step1_normalized_script.md`
4. `scripts/episode_{N}.json` không tồn tại? → **Giai đoạn 4**
5. Có nhân vật thiếu `character_sheet`? → **Giai đoạn 5** (có thể song song với giai đoạn 6)
6. Có manh mối `importance=major` thiếu `clue_sheet`? → **Giai đoạn 6** (có thể song song với giai đoạn 5)
7. Có cảnh thiếu hình phân cảnh (storyboard)? → **Giai đoạn 7**
8. Có cảnh thiếu video? → **Giai đoạn 8**
9. Tất cả hoàn thành → Quy trình kết thúc, hướng dẫn người dùng xuất bản thảo Cắt Ảnh (Jianying) trên giao diện Web.

**Xác định số tập mục tiêu**: Nếu người dùng không chỉ định, tìm tập mới nhất chưa hoàn thành hoặc hỏi người dùng.

---

## Giao thức xác nhận giữa các giai đoạn

**Sau khi mỗi subagent quay lại**, agent chính thực hiện:

1. **Hiển thị tóm tắt**: Hiển thị tóm tắt do subagent trả về cho người dùng.
2. **Nhận xác nhận**: Sử dụng AskUserQuestion để cung cấp các tùy chọn:
   - **Tiếp tục giai đoạn tiếp theo** (khuyên dùng)
   - **Làm lại giai đoạn này** (thêm yêu cầu sửa đổi rồi điều phối lại)
   - **Bỏ qua giai đoạn này**
3. **Hành động dựa trên lựa chọn của người dùng**

---

## Giai đoạn 1: Thiết kế Nhân vật/Manh mối toàn cục

**Kích hoạt**: `characters` hoặc `clues` trong project.json trống.

**Điều phối subagent `analyze-characters-clues`**:

```
Tên dự án: {project_name}
Đường dẫn dự án: projects/{project_name}/
Phạm vi phân tích: {Toàn bộ tiểu thuyết / Phạm vi do người dùng chỉ định}
Nhân vật hiện có: {Danh sách tên nhân vật hiện có, hoặc "Không có"}
Manh mối hiện có: {Danh sách tên manh mối hiện có, hoặc "Không có"}

Hãy phân tích nguyên tác tiểu thuyết, trích xuất thông tin nhân vật và manh mối, ghi vào project.json và trả về tóm tắt.
```

---

## Giai đoạn 2: Lập kế hoạch phân tập

**Kích hoạt**: Tệp `source/episode_{N}.txt` của tập mục tiêu không tồn tại.

Mỗi lần chỉ chia tập cho tập hiện tại cần thực hiện. **Agent chính thực hiện trực tiếp** (không điều phối subagent):

1. Xác định tệp nguồn: Sử dụng `source/_remaining.txt` nếu có, nếu không thì dùng tệp tiểu thuyết gốc.
2. Hỏi người dùng số chữ mục tiêu (ví dụ: 1000 chữ/tập).
3. Gọi `peek_split_point.py` để hiển thị ngữ cảnh gần điểm chia:
   ```bash
   python .claude/skills/manage-project/scripts/peek_split_point.py --source {tệp nguồn} --target {số chữ mục tiêu}
   ```
4. Phân tích `nearby_breakpoints`, gợi ý các điểm ngắt tự nhiên.
5. Sau khi người dùng xác nhận, thực hiện dry run để kiểm tra:
   ```bash
   python .claude/skills/manage-project/scripts/split_episode.py --source {tệp nguồn} --episode {N} --target {số chữ mục tiêu} --anchor "{văn bản neo}" --dry-run
   ```
6. Thực hiện thực tế sau khi xác nhận không có sai sót (bỏ tham số `--dry-run`).

---

## Giai đoạn 3: Tiền xử lý tập phim

**Kích hoạt**: Tệp trung gian trong `drafts/` của tập mục tiêu không tồn tại.

Chọn subagent dựa trên `content_mode`:

- **narration** → điều phối `split-narration-segments`
- **drama** → điều phối `normalize-drama-script`

Prompt điều phối bao gồm: Tên dự án, đường dẫn dự án, số tập, đường dẫn tệp tiểu thuyết của tập này, danh sách tên nhân vật/manh mối.

---

## Giai đoạn 4: Tạo kịch bản JSON

**Kích hoạt**: `scripts/episode_{N}.json` không tồn tại.

**Điều phối subagent `create-episode-script`**: Truyền tên dự án, đường dẫn dự án, số tập.

---

## Giai đoạn 5+6: Thiết kế Nhân vật + Thiết kế Manh mối (Có thể song song)

Hai nhiệm vụ này không phụ thuộc lẫn nhau, **điều phối cùng lúc hai subagent `generate-assets`** (nếu cả hai đều cần thiết).

### subagent A — Thiết kế nhân vật

**Kích hoạt**: Có nhân vật thiếu `character_sheet`.

```
Điều phối subagent `generate-assets`:
  Loại nhiệm vụ: characters
  Tên dự án: {project_name}
  Đường dẫn dự án: projects/{project_name}/
  Các mục chờ tạo: {Danh sách tên nhân vật còn thiếu}
  Lệnh script:
    python .claude/skills/generate-characters/scripts/generate_character.py --all
  Phương thức xác minh: Đọc lại project.json, kiểm tra trường character_sheet của nhân vật tương ứng.
```

### subagent B — Thiết kế manh mối

**Kích hoạt**: Có manh mối `importance=major` thiếu `clue_sheet`.

```
Điều phối subagent `generate-assets`:
  Loại nhiệm vụ: clues
  Tên dự án: {project_name}
  Đường dẫn dự án: projects/{project_name}/
  Các mục chờ tạo: {Danh sách tên manh mối còn thiếu}
  Lệnh script:
    python .claude/skills/generate-clues/scripts/generate_clue.py --all
  Phương thức xác minh: Đọc lại project.json, kiểm tra trường clue_sheet của manh mối tương ứng.
```

Nếu chỉ một trong hai cần thực hiện, chỉ điều phối subagent tương ứng.
Sau khi cả hai subagent quay lại, hợp nhất tóm tắt để hiển thị cho người dùng và đi vào xác nhận giữa các giai đoạn.

---

## Giai đoạn 7: Tạo hình ảnh phân cảnh (Storyboard)

**Kích hoạt**: Có cảnh thiếu hình phân cảnh.

**Điều phối subagent `generate-assets`**:

```
Điều phối subagent `generate-assets`:
  Loại nhiệm vụ: storyboard
  Tên dự án: {project_name}
  Đường dẫn dự án: projects/{project_name}/
  Lệnh script:
    python .claude/skills/generate-storyboard/scripts/generate_storyboard.py episode_{N}.json
  Phương thức xác minh: Đọc lại scripts/episode_{N}.json, kiểm tra trường storyboard_image của các cảnh.
```

---

## Giai đoạn 8: Tạo video

**Kích hoạt**: Có cảnh thiếu video.

**Điều phối subagent `generate-assets`**:

```
Điều phối subagent `generate-assets`:
  Loại nhiệm vụ: video
  Tên dự án: {project_name}
  Đường dẫn dự án: projects/{project_name}/
  Lệnh script:
    python .claude/skills/generate-video/scripts/generate_video.py episode_{N}.json --episode {N}
  Phương thức xác minh: Đọc lại scripts/episode_{N}.json, kiểm tra trường video_clip của các cảnh.
```

---

## Cổng vào linh hoạt

Quy trình làm việc **không bắt buộc phải bắt đầu từ đầu**. Dựa trên kết quả kiểm tra trạng thái, hệ thống sẽ tự động bắt đầu từ giai đoạn chính xác:

- "Phân tích nhân vật tiểu thuyết" → Chỉ thực hiện giai đoạn 1.
- "Tạo kịch bản tập 2" → Bắt đầu từ giai đoạn 2 (nếu nhân vật đã có).
- "Tiếp tục" → Kiểm tra trạng thái để tìm mục thiếu đầu tiên.
- Chỉ định giai đoạn cụ thể (ví dụ: "Tạo hình phân cảnh") → Nhảy trực tiếp đến giai đoạn đó.

---

## Phân tầng dữ liệu

- Định nghĩa đầy đủ về Nhân vật/Manh mối **chỉ lưu trong project.json**, trong kịch bản chỉ tham chiếu bằng tên.
- Các trường thống kê (scenes_count, status, progress) được **tính toán khi đọc**, không lưu trữ.
- Siêu dữ liệu tập phim được **đồng bộ khi ghi** lúc lưu kịch bản.

# Benchmark Day 7

Sinh bằng `python -m src.prepare_data` từ hai nguồn:

- Benchmark Day 6: `benchmark/questions.jsonl` trong repo Day 6, gồm 21 câu.
- Các câu viết mới cho Day 7: [authored_questions.json](authored_questions.json).

Bộ câu hỏi được tạo và commit **trước khi chạy bất kỳ retrieval hay agent nào của Day 7**.

| File                    | Nội dung                                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `questions.json`        | Câu có đáp án theo schema [data/README.md](../data/README.md). Mỗi phần tử của `gold` là một evidence **thay thế**: chỉ cần một là đủ |
| `unanswerable.json`     | Câu thiếu bằng chứng (`search_and_abstain`), kèm `absence_reason` và `check_method`                                                   |
| `cases.json`            | `id`, `split`, `answerable`, dùng cho `starter/agent_metrics.py`                                                                      |
| `selection_criteria.md` | Tiêu chí chọn cấu hình, công bố trước khi chạy                                                                                        |

## Phân bố

| Split | Có đáp án | Thiếu bằng chứng | Tổng |
| ----- | --------: | ---------------: | ---: |
| dev   |        26 |                3 |   29 |
| test  |         8 |                3 |   11 |

### Dev (26 câu có đáp án)

| Nhóm                        | Câu                                                       |
| --------------------------- | --------------------------------------------------------- |
| Day 6 dev                   | `d01`–`d15` (giữ nguyên ID)                               |
| Day 6 test, chuyển sang dev | `d16`–`d21` (trước là `t01`–`t06`; ID gốc ghi ở `origin`) |
| Câu khó mới                 | `d22`–`d26`, diễn đạt xa nguồn hoặc có điều kiện          |
| Thiếu bằng chứng            | `ud01` FAT32, `ud02` Core i9, `ud03` Windows 11           |

### Test (8 câu có đáp án)

| Nhóm                    | Câu                                                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| Câu có đáp án, viết mới | `t01`–`t08`, lấy từ các trang chưa có câu dev nào: 210, 223, 229, 258, 268, 281, 286, 290 |
| Thiếu bằng chứng        | `ut01` Linux CFS, `ut02` Apple M2, `ut03` năm ra đời NTFS                                 |

## Vì sao làm bộ test mới

Bộ test Day 6 đã được chạy và phân tích lỗi trong báo cáo Day 6. Ví dụ, lỗi ở `t03` (journaling) được dùng làm lý do đề xuất thử BM25/hybrid. Các phương pháp Day 7 vì vậy có thể bị định hướng bởi chính bộ test đó.

Để đánh giá độc lập:

- 6 câu test Day 6 được chuyển sang dev.
- Bộ test Day 7 được viết mới từ các trang không có câu dev nào.

## Quy tắc

- Mỗi `evidence` phải là chuỗi con nguyên văn của trang PDF gốc. Trang ở đây là **số trang vật lý** của PDF, không phải số trang in trên sách. Mỗi evidence cũng phải nằm trọn trong **một chunk của index B**. `prepare_data` kiểm tra hai điều này bằng `starter/baseline.validate`.
- **Sửa dấu nháy:** câu Day 6 `d09` dùng dấu `'`, trong khi PDF dùng `’`. Evidence đã được thay bằng đúng chuỗi trong trang.
- **Kiểm tra câu thiếu bằng chứng:** tìm bằng regex trên toàn bộ 79 trang (`data/pages.jsonl` của Day 6). Kết quả ghi trong `check_method`. Không kết luận "thiếu thông tin" chỉ vì top-k không tìm thấy.
- **Câu gần chủ đề, dễ bị trả lời bừa:**
  - `ud02`: tài liệu nói chung chung "billions of transistors" nhưng không có số liệu của Core i9.
  - `ut01`: có ví dụ time slice 2 ms nhưng không nói gì về Linux CFS.

  Hai câu này dùng để thử xem agent có suy đoán không.

- **Filter `chapter`:** chỉ dùng khi người dùng tự nói phạm vi (`filter_context`). Có ở `d14`, `d15`, `d20`, `d21` (dev) và `t06` (test). Filter không bao giờ được suy ra từ gold.
- **Không lộ gold:** gold, `expected_answer` và `absence_reason` không bao giờ được đưa vào agent hay retriever. Runner chỉ truyền `question` và `filter`.
- **Giới hạn:**
  - Câu hỏi do AI (Claude) soạn từ text đã chuẩn hóa, sau đó được kiểm bằng script. Đa số câu dùng lại từ ngữ của nguồn, nên dễ hơn câu hỏi thật.
  - Mọi câu có đáp án chỉ cần **một** evidence, chưa có câu multi-hop bắt buộc nhiều đoạn.

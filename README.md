# Day 7 — Agentic RAG

**Bài cá nhân · Python 3.11+ · tiếp nối Day 6**

Dùng embedding và vector store từ Day 6 để xây một agent biết tìm bằng chứng, trả lời có nguồn và nhận biết khi không đủ thông tin. Bạn tự chọn kiến trúc, số tool và cách tổ chức retrieval.

> **Tùy chọn:** [Gợi ý dùng AI để lập trình](AGENT_SETUP.md) giúp bạn làm lab; phần này không bắt buộc và không tính điểm.

## Bài cần làm

![Agent tìm tài liệu trong kho Day 6 và trả lời có nguồn](assets/retrieval-pipeline.svg)

1. Kết nối dữ liệu, embedding và vector store Day 6.
2. Xây agent dùng model thật và ít nhất một khả năng truy xuất dữ liệu. Agent có thể dùng nhiều tool và nhiều lượt gọi.
3. Thử **ít nhất 3 phương pháp retrieval khác nhau**, trong đó có dense retrieval dùng vector store Day 6. Tự chọn các phương pháp còn lại; xem [gợi ý](GUIDE.md#2-thử-các-phương-pháp-retrieval).
4. Thử nhiều cấu hình, benchmark, phân tích lỗi và chọn cấu hình tốt trên **dev**; sau đó đánh giá trên **test**.

Benchmark tối thiểu có **24 câu**: dev gồm 15 câu có đáp án và 2 câu thiếu bằng chứng; test gồm 5 câu có đáp án và 2 câu thiếu bằng chứng. Xem [benchmark](BENCHMARK.md) và [rubric](RUBRIC.md).

## Thử thách nâng cao · +15 điểm

Index một tài liệu thực tế từ **100 trang** có bảng, ảnh và biểu đồ; xây agent truy xuất và trả lời các câu hỏi về nội dung đó. Hoàn thành [thử thách nâng cao](ADVANCED.md) và đạt **ít nhất 90% benchmark test** để nhận 15 điểm bonus. Phần cơ bản tối đa 85 điểm; toàn bài tối đa 100 điểm.

## Bắt đầu

1. Đọc [hướng dẫn](GUIDE.md), [rubric](RUBRIC.md) và [quy tắc](RULES.md).
2. Tạo repo cá nhân theo [cách nộp bài](SUBMISSION.md), chuẩn bị đầu ra Day 6 và model hỗ trợ tool calling.
3. Dùng hoặc thay thế [starter](starter/README.md); bạn cần kết nối model và vector store thật.
4. Chạy `python -m unittest discover -s tests -v`. Test mock chỉ kiểm tra code, không phải benchmark agent thật.

![Các bước thử nghiệm trên dev và đánh giá trên test](assets/experiment-loop.svg)

Nộp code, cách chạy, cấu hình, benchmark, trace và [báo cáo](report/individual/MSSV_HoTen.md). Thời gian ở [checkpoints](CHECKPOINTS.md) là gợi ý, có thể điều chỉnh theo lớp và phạm vi thử nghiệm.

---

## Bài làm

**Phạm Tuấn Cường · 2A202603584 · L3A.** Báo cáo: [report/individual/2A202603584_PhamTuanCuong.md](report/individual/2A202603584_PhamTuanCuong.md).

### Thành phần

- **Dữ liệu:** dùng lại Day 6 gồm corpus OpenStax _Introduction to Computer Science_ chương 5–6 (79 trang, giấy phép CC BY-NC-SA 4.0) và vector store PostgreSQL 16 + pgvector 0.8.7.
  - Index B có 323 chunk.
  - Embedding `intfloat/multilingual-e5-small`, 384 chiều, chạy trên CPU.
- **Agent:** `anthropic/claude-haiku-5.5` qua OpenRouter, có tool calling, `temperature=0`.
- **Retrieval:** 4 phương pháp:
  - dense (pgvector)
  - BM25
  - hybrid RRF
  - hybrid + cross-encoder `ms-marco-MiniLM-L-6-v2`
- **Benchmark:**
  - dev: 26 câu có đáp án + 3 câu thiếu evidence
  - test: 8 câu có đáp án + 3 câu thiếu evidence, viết mới
- **Cấu hình chọn trên dev:** `hybrid_combo`, gồm hybrid RRF, search đầu tiên dùng nguyên câu hỏi gốc và context budget 6.400 ký tự (mode truncate). Xem [results/comparison_dev.md](results/comparison_dev.md).

### Tái lập (Windows PowerShell)

```powershell
# 1. Day 6 phải chạy sẵn: container pgvector (docker compose -p day6_student_starter up -d) đã ingest index B.
#    Repo Day 6 (cách dựng lại vector store): https://github.com/Ptuancuong/K5-L3A-DAY06-PhamTuanCuong-2A202603584-DataIngestion
#    Chunk đã export sẵn ở data/day6/ (BM25 chạy được không cần DB; dense cần DB + model e5).
#    Có thể dùng lại venv của Day 6, hoặc tạo venv mới:
py -3.11 -m venv .venv; .venv\Scripts\Activate.ps1
pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# 2. File .env (đã có trong .gitignore, không commit):
#    OPENROUTER_API_KEY=...
#    DATABASE_URL=postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab
#    Nếu repo Day 6 không nằm ở ..\..\VinUni Lab Day06\..., đặt thêm DAY6_DIR=<đường dẫn repo Day 6>.

$env:PYTHONUTF8 = '1'           # Windows: test starter đọc file không chỉ rõ encoding
python -m unittest discover -s tests -v                  # 26 test offline

python -m src.prepare_data                               # export chunk + build benchmark (đã commit sẵn)
python -m src.eval_retrieval --configs dense bm25 hybrid hybrid_rerank dense_budget800 --split dev
python -m src.run_agent --config dense --split dev       # tương tự với các config khác trong configs/
python -m src.compare_answers --split dev --configs dense hybrid   # bảng đọc tay
python -m src.show_cited --split dev --configs dense hybrid        # chunk được cite nhưng không chứa gold
python -m src.labels --split dev                         # reviews.json + starter/agent_metrics.py
python -m src.select_config                              # áp tiêu chí -> configs/chosen.json

# Chỉ chạy sau khi đã commit chosen.json:
python -m src.eval_retrieval --configs dense chosen --split test
python -m src.run_agent --config dense --split test
python -m src.run_agent --config chosen --split test
python -m src.labels --split test
```

### Cấu trúc bài làm

| Đường dẫn                             | Nội dung                                                                                                                                                      |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/`                                | `retrieval.py` (dense/BM25/RRF/rerank), `context.py`, `agent.py`, `llm.py` (OpenRouter), `run_agent.py`, `eval_retrieval.py`, `labels.py`, `select_config.py` |
| `configs/`                            | Mỗi file JSON là một cấu hình thí nghiệm. `chosen.json` là cấu hình đã chốt, có kèm log chọn                                                                  |
| `benchmark/`                          | `questions.json`, `unanswerable.json`, `cases.json`, `authored_questions.json` và `selection_criteria.md`                                                     |
| `data/day6/`                          | Chunk A/B export từ pgvector Day 6                                                                                                                            |
| `results/retrieval/<config>/<split>/` | Trace và summary của retrieval-only                                                                                                                           |
| `results/agent/<config>/<split>/`     | `traces.json`, `summary.json`, `reviews.json` (nhãn), `agent_metrics.json`, `review_sheet.md`                                                                 |
| `plan.md`                             | Kế hoạch tổng hợp từ đề bài                                                                                                                                   |

# Code

Code bài làm Day 7. Chạy từ thư mục gốc của repo bằng `python -m src.<module>`.

| Module                                | Việc                                                                                                     |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `config.py`                           | Đường dẫn và `.env`; tham số chung: model, index B, đường dẫn Day 6                                      |
| `prepare_data.py`                     | Export chunk từ pgvector Day 6, chuyển và kiểm tra benchmark                                             |
| `retrieval.py`                        | `DenseRetriever` (pgvector, e5), `BM25Retriever`, `HybridRRF`, `CrossEncoderReranker`, `build_retriever` |
| `context.py`                          | `ContextBuilder`: context chỉ thêm không bớt, budget tính bằng ký tự, mode `skip` hoặc `truncate`        |
| `llm.py`                              | Client OpenRouter có tool calling; ghi token, chi phí, latency; retry khi gặp lỗi tạm thời               |
| `agent.py`                            | Vòng lặp agent: tool `search_documents` và `submit_answer`, giới hạn số lần search, kiểm tra citation    |
| `run_agent.py`                        | Chạy agent cho một config trên một split, lưu trace, summary và review sheet                             |
| `eval_retrieval.py`                   | Đánh giá retrieval-only trên câu hỏi gốc: Hit@1, Evidence Hit@3, MRR@10, CER                             |
| `metrics.py`                          | Định nghĩa hit và kiểm tra evidence trong context. Chỉ chạy **sau** khi agent chạy xong                  |
| `compare_answers.py`, `show_cited.py` | Công cụ hỗ trợ đọc và chấm tay                                                                           |
| `labels.py`                           | Nhãn chấm tay, xuất `reviews.json`, tổng hợp bằng `starter/agent_metrics.py`                             |
| `select_config.py`                    | Áp tiêu chí chọn đã công bố, tạo bảng dev và `configs/chosen.json`                                       |

Khung agent trong `starter/agentic.py` không được sửa. Module `agent.py` thay thế nó bằng kiến trúc gọi tool thật của LLM, nhưng vẫn giữ các quy tắc của starter:

- citation phải nằm trong context;
- có giới hạn số lần search;
- lỗi được báo ra, không thay bằng kết quả giả.

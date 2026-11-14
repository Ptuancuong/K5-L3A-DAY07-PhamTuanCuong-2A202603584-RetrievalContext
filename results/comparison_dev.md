# So sánh cấu hình trên dev (29 câu: 26 có đáp án + 3 thiếu evidence)

- **Retrieval:** Hit@1, Evidence Hit@3 và MRR@10 tính trên **câu hỏi gốc**, chạy retrieval một lần (`src.eval_retrieval`).
- **Agent:** các cột còn lại lấy từ lần chạy agent thật (`src.run_agent`), dùng `anthropic/claude-haiku-5.5` với `temperature=0`.
- **Nhãn:** đọc thủ công (`src.labels`), sau đó tổng hợp bằng `starter/agent_metrics.py`.

| Config | Hit@1 | Evidence Hit@3 | MRR@10 | Agent Context Evidence Rate | Grounded 0/1/2 (mean /2) | Citation hợp lệ | Abstention đúng | Từ chối nhầm | Lượt search TB | Median s/câu | Chi phí USD (29 câu) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dense | 20/26 | 24/26 | 0.849 | 24/26 | 1/1/24 (1.885) | 33/33 | 3/3 | 1/26 | 1.34 | 2.59 | 0.0159 |
| bm25 | 21/26 | 24/26 | 0.872 | 24/26 | 1/0/25 (1.923) | 29/29 | 3/3 | 1/26 | 1.28 | 2.44 | 0.0151 |
| hybrid | 23/26 | 24/26 | 0.913 | 25/26 | 0/0/26 (2.000) | 34/34 | 3/3 | 0/26 | 1.21 | 2.67 | 0.0147 |
| hybrid_rerank | 25/26 | 26/26 | 0.981 | 26/26 | 0/0/26 (2.000) | 31/31 | 3/3 | 0/26 | 1.21 | 3.21 | 0.0147 |
| dense_origfirst | 20/26 | 24/26 | 0.849 | 24/26 | 1/0/25 (1.923) | 30/30 | 3/3 | 1/26 | 1.31 | 1.55 | 0.0114 |
| dense_ctx6400 | 20/26 | 24/26 | 0.849 | 25/26 | 0/1/25 (1.962) | 34/34 | 3/3 | 0/26 | 1.28 | 2.67 | 0.0156 |
| dense_combo | 20/26 | 24/26 | 0.849 | 25/26 | 0/0/26 (2.000) | 32/32 | 3/3 | 0/26 | 1.28 | 1.65 | 0.0115 |
| hybrid_combo | 23/26 | 24/26 | 0.913 | 25/26 | 0/0/26 (2.000) | 29/29 | 3/3 | 0/26 | 1.24 | 1.62 | 0.0111 |
| hybrid_rerank_combo | 25/26 | 26/26 | 0.981 | 26/26 | 0/0/26 (2.000) | 32/32 | 3/3 | 0/26 | 1.21 | 2.35 | 0.0109 |

## Áp dụng tiêu chí chọn ([benchmark/selection_criteria.md](../benchmark/selection_criteria.md))

- 1. constraints pass: ['dense', 'bm25', 'hybrid', 'hybrid_rerank', 'dense_origfirst', 'dense_ctx6400', 'dense_combo', 'hybrid_combo', 'hybrid_rerank_combo']
- 2-3. best grounded sum 52, best context hits 26; within 1 question on both: ['hybrid', 'hybrid_rerank', 'dense_ctx6400', 'dense_combo', 'hybrid_combo', 'hybrid_rerank_combo']
- 5. tie-break by median latency, cost, simplicity: hybrid_combo (1620.8 ms, 0.01105 USD), dense_combo (1652.3 ms, 0.01145 USD), hybrid_rerank_combo (2349.9 ms, 0.01085 USD), dense_ctx6400 (2667.5 ms, 0.01563 USD), hybrid (2674.5 ms, 0.01473 USD), hybrid_rerank (3207.1 ms, 0.01471 USD)

**Cấu hình được chọn: `hybrid_combo`**: Hybrid RRF (dense + BM25) + improvements A and B.

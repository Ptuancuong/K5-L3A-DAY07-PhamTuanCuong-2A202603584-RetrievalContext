# Báo cáo Day 7 — Agentic RAG

**Phạm Tuấn Cường · 2A202603584 · L3A.** Chạy ngày 2026-11-14.

**Lệnh tái lập:** xem [README](../../README.md#bài-làm).

**Các mốc commit:**

| Commit    | Nội dung                                                  |
| --------- | --------------------------------------------------------- |
| `667c875` | Đóng băng benchmark và tiêu chí chọn, trước mọi lần chạy  |
| `85812f2` | Kết quả dev và `configs/chosen.json`, trước khi chạy test |
| `0e6bf9e` | Chạy test một lần                                         |

## Dữ liệu và benchmark

- **Nguồn, quyền sử dụng, số trang và số chunk**
  - **Nguồn:** OpenStax _Introduction to Computer Science_ (Rice University), chương 5–6. Giấy phép CC BY-NC-SA 4.0. Dùng nguyên corpus của Day 6, xem `data/manifest.json` trong repo Day 6.
  - **Phạm vi:** 79 trang nội dung, là trang PDF 204–294, bỏ trang mở chương, phần review và hai trang ít chữ (239, 265).
  - **Index:** dùng index **B** mà Day 6 đã chọn. Mỗi chunk là một đoạn, dài tối đa 1.000 ký tự và không vượt qua ranh giới trang. Có **323 chunk**: trung vị 768 ký tự, dài nhất 998 ký tự.
  - **Export:** `python -m src.prepare_data` xuất các chunk này từ pgvector ra [data/day6/chunks_B.json](../../data/day6/chunks_B.json). Index A (538 chunk) cũng được export nhưng không dùng trong thí nghiệm.
- **Vector store, embedding model, phiên bản và số chiều**
  - **Vector store:** PostgreSQL 16 + pgvector 0.8.7 (Docker của Day 6, `127.0.0.1:55433`), bảng `chunks`, `strategy='B'`, cosine exact search.
  - **Embedding:** `intfloat/multilingual-e5-small`, **384 chiều**, chạy trên CPU bằng sentence-transformers 6.3.0. Query được thêm tiền tố `query: ` và L2-normalize, giống cách Day 6 index document với tiền tố `passage: `.
  - **Kiểm tra tương thích:** `E5Embedder` báo lỗi nếu số chiều khác 384. Hai thông số trên cũng khớp với cột `model` và kiểu `vector(384)` trong bảng.
  - **Index không đổi:** không tạo index mới. BM25 và rerank chạy trên đúng 323 chunk và ID đó.
- **Agent model, cách chạy và phân chia dev/test**
  - **Model:** `anthropic/claude-haiku-5.5` qua OpenRouter (API OpenAI-compatible, tool calling), `temperature=0`, `max_tokens=700`.
  - **Model rerank:** `cross-encoder/ms-marco-MiniLM-L-6-v2`, chạy trên CPU.
  - **Phân chia:** **dev 26 câu có đáp án + 3 câu thiếu evidence**; **test 8 câu có đáp án + 3 câu thiếu evidence**.
  - **Vì sao làm test mới:** test Day 6 đã được chạy và phân tích lỗi trong báo cáo Day 6, nên 6 câu đó được chuyển sang dev (`d16`–`d21`). Bộ test Day 7 viết mới từ 8 trang không có câu dev nào. Test `test_day7.BenchmarkTests` kiểm tra rằng trang evidence của test và dev không trùng nhau.
- **Cách xác định câu có/thiếu evidence và tiêu chí chấm**
  - **Câu có đáp án:** evidence là chuỗi nguyên văn của trang, nằm trọn trong một chunk B. `prepare_data` kiểm tra điều này bằng `starter/baseline.validate`.
  - **Câu thiếu evidence:** kiểm tra bằng regex trên cả 79 trang. Kết quả ghi trong `check_method`. Hai câu được chọn vì rất gần chủ đề: `ud02` (tài liệu chỉ nói chung chung "billions of transistors") và `ut01` (tài liệu có ví dụ time slice 2 ms).
  - **Tiêu chí chọn cấu hình:** công bố trước trong [benchmark/selection_criteria.md](../../benchmark/selection_criteria.md). Thứ tự: ràng buộc abstention → grounded answer → Context Evidence Rate → Hit@3/Hit@1 → nếu chênh ≤ 1 câu thì xét latency, rồi chi phí.

## Retrieval và thử nghiệm

Hit@1 và Evidence Hit@3 tính trên **câu hỏi gốc**, chạy retrieval một lần (`src.eval_retrieval`, xuất cả top-10). **Context Evidence Rate (CER)** là câu có evidence gold trong **context cuối mà agent thật gửi cho LLM**. Trong ngoặc là CER của retrieval-only, khi đóng gói top-3 theo budget. Thời gian là median mỗi câu của agent. Chi phí là tổng USD do OpenRouter báo cho cả split. Mọi cấu hình đều dùng filter `chapter` cho 4 câu dev và 1 câu test mà người dùng tự nêu phạm vi, và tối đa 3 lượt search.

| Cấu hình                                         | Phương pháp, top-k, filter, rerank, context budget                        | Giả thuyết / thay đổi                                                     | Split    | Hit@1             | Evidence Hit@3   | Context Evidence Rate | Thời gian / chi phí    |
| ------------------------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------- | ----------------- | ---------------- | --------------------- | ---------------------- |
| Baseline `dense`                                 | Dense pgvector B, top-3, budget 3.200 ký tự (skip), LLM tự viết mọi query | Baseline bắt buộc trên vector store Day 6                                 | dev      | 20/26 (76,9%)     | 24/26 (92,3%)    | 24/26 (24/26)         | 2,59 s; 0,0159 USD     |
| Phương pháp 2 `bm25`                             | Okapi BM25 (k1=1,5; b=0,75; stopword tiếng Anh) trên cùng chunk           | Câu hỏi dùng lại từ ngữ của nguồn nên lexical có lợi                      | dev      | 21/26 (80,8%)     | 24/26 (92,3%)    | 24/26 (24/26)         | 2,44 s; 0,0151 USD     |
| Phương pháp 3 `hybrid`                           | RRF (k=60) của dense + BM25, mỗi bên 20 candidate                         | Hai cách tìm bổ sung nhau, tăng Hit@1                                     | dev      | 23/26 (88,5%)     | 24/26 (92,3%)    | 25/26 (24/26)         | 2,67 s; 0,0147 USD     |
| Phương pháp 4 `hybrid_rerank`                    | Hybrid lấy 20 candidate, cross-encoder xếp lại, giữ top-3                 | Rerank sửa các câu định nghĩa ngắn như d15 và d24                         | dev      | **25/26 (96,2%)** | **26/26 (100%)** | **26/26** (26/26)     | 3,21 s; 0,0147 USD     |
| Cải thiện 1 `dense_origfirst`                    | Baseline + **search 1 dùng nguyên câu hỏi gốc**                           | Câu viết lại của LLM làm mất từ khóa (d01, d19)                           | dev      | 20/26             | 24/26            | 24/26 (24/26)         | **1,55 s**; 0,0114 USD |
| Cải thiện 2 `dense_ctx6400`                      | Baseline + **budget 6.400 ký tự, mode truncate**                          | Budget đầy sau search 1 nên evidence tìm được ở search 2 bị bỏ (bm25 d09) | dev      | 20/26             | 24/26            | 25/26 (24/26)         | 2,67 s; 0,0156 USD     |
| `dense_combo`                                    | Baseline + cải thiện 1 + cải thiện 2                                      | Hai sửa đổi xử lý hai loại lỗi khác nhau                                  | dev      | 20/26             | 24/26            | 25/26 (24/26)         | 1,65 s; 0,0115 USD     |
| `hybrid_combo`                                   | Hybrid + cải thiện 1 + cải thiện 2                                        | Như trên, trên hybrid                                                     | dev      | 23/26             | 24/26            | 25/26 (24/26)         | **1,62 s; 0,0111 USD** |
| `hybrid_rerank_combo`                            | Hybrid rerank + cải thiện 1 + cải thiện 2                                 | Như trên, trên hybrid rerank                                              | dev      | 25/26             | 26/26            | 26/26 (26/26)         | 2,35 s; 0,0109 USD     |
| **Cấu hình đã chọn** (`chosen` = `hybrid_combo`) | Hybrid RRF, top-3, budget 6.400 truncate, câu hỏi gốc trước               | Chạy test 1 lần                                                           | **test** | 4/8 (50%)         | 7/8 (87,5%)      | **8/8** (7/8)         | **2,00 s; 0,0056 USD** |
| Baseline `dense`                                 | như trên                                                                  | Chạy test 1 lần                                                           | **test** | 5/8 (62,5%)       | 6/8 (75%)        | **8/8** (6/8)         | 3,52 s; 0,0063 USD     |

Thí nghiệm phụ `dense_budget800`: baseline với budget mặc định 800 ký tự của starter. CER retrieval-only chỉ đạt **5/26**, vì chunk B dài trung vị 768 ký tự, cộng thêm header thì gần như không chunk nào vừa budget. Đây là lý do baseline dùng budget 3.200.

**Một cấu hình vừa là phương pháp mới vừa là cải thiện:** `hybrid_rerank` là phương pháp retrieval thứ 4, đồng thời được đo như một cải thiện retrieval. Hit@1 tăng từ 20 lên 25/26 so với dense, và đây là phương pháp duy nhất tìm được d15 và d24 trong top-3. Hai cải thiện còn lại là thay đổi ở tầng agent và context, mỗi cái được đo riêng trên baseline dense, rồi mới kết hợp.

### Hai lỗi dev, nguyên nhân và cách thử

1. **Context budget đầy làm mất evidence.**
   - **Lỗi:** ở `bm25`/d09, search 1 thêm 3 chunk vào context, dùng hết 2.735/3.200 ký tự. Search 2 (`"THE operating system layers Dijkstra 1968"`) xếp gold `p264:c0` ở **hạng 1**, nhưng chunk bị `Not included (context budget full)`. Agent từ chối, nên câu này bị chấm 0.
   - **Lặp lại:** cùng lỗi xảy ra ở `dense_origfirst`/d24. Search 2 tìm được `p253:c0` ở hạng 1, nhưng context đã dùng 2.989/3.200 ký tự.
   - **Cách thử:** cải thiện 2 (budget 6.400 + truncate).
   - **Kết quả:** `dense_ctx6400` không còn từ chối nhầm (0/26), CER đạt 25/26. Tổ hợp `dense_combo` sửa được d24: search 2 lần này thêm được `p253:c0`.
   - **Đánh đổi:** context trung bình tăng từ 2.673 lên 2.937 ký tự, prompt dài hơn.
2. **Query do LLM viết lại kém hơn câu hỏi gốc.**
   - **Lỗi:**
     - Ở `dense`/d01, LLM search `"single 1 or 0 stored in a computer called"` và không lấy được `p205:c1`, trong khi câu hỏi gốc xếp chunk này **hạng 1**.
     - Ở `dense`/d19, query viết lại cũng không lấy được `p293:c2` (10 ms so với 100 µs). Câu trả lời chỉ đúng một phần (điểm 1) và còn nói sai rằng nguồn không có số liệu.
   - **Cách thử:** cải thiện 1 (search 1 luôn dùng câu hỏi gốc).
   - **Kết quả:**
     - `dense_origfirst` sửa được d01 và d19.
     - Nhưng d24 lại hỏng: câu gốc của d24 không có evidence trong top-3, và budget làm mất evidence ở search 2 (lỗi 1).
     - Chỉ khi kết hợp (`dense_combo`) thì cả ba câu đều đúng (26/26 điểm 2).
   - **Lợi ích phụ:** bỏ được một lượt gọi LLM, trung bình còn 1,28 lượt/câu so với 2,34. Nhờ vậy median latency giảm từ 2,59 s xuống 1,65 s và chi phí giảm khoảng 28%.

**Lỗi nhãn cần nêu:** d15 ("What does scheduling mean?"). Định nghĩa ở p274 ("determining which process in the ready state should be moved to the running state") tương đương với gold p272. Nhưng gold chỉ ghi p272, nên các metric retrieval và context tính nhiều cấu hình là trượt, dù câu trả lời đúng và được chấm 2. Đây là giới hạn của bộ gold.

**Lý do chọn cấu hình:** áp dụng máy móc theo tiêu chí đã công bố, bằng `python -m src.select_config` (kết quả ở [results/comparison_dev.md](../../results/comparison_dev.md)).

- **Ràng buộc:** cả 9 cấu hình đều đạt.
- **Grounded và CER:** 6 cấu hình nằm trong khoảng ≤ 1 câu so với tốt nhất ở cả grounded (tối đa 52/52 điểm) và CER (tối đa 26/26).
- **Tie-break theo median latency:** chọn `hybrid_combo` (1,62 s).

Cần nói rõ:

- `dense_combo` chỉ chậm hơn 31 ms, nằm trong sai số.
- `hybrid_rerank_combo` có retrieval tốt nhất nhưng chậm hơn khoảng 0,7 s/câu, do chạy cross-encoder trên CPU.
- Trên dev, `hybrid_combo` hơn `dense_combo` ở Hit@1 (23 so với 20).

## Agent và đánh giá

- **Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi**
  - **Tool:** agent có hai tool.
    - `search_documents(query)` gọi retriever của cấu hình, áp filter `chapter` nếu người dùng đã nêu phạm vi.
    - `submit_answer(answer, citations, insufficient_evidence)`.
  - **Số lượt và điều kiện dừng:**
    - Tối đa 3 lần search. Khi hết lượt, request tiếp theo chỉ cho phép `submit_answer` (bắt buộc qua `tool_choice`).
    - Agent dừng khi gọi `submit_answer`. Nếu hai lần liền không gọi tool, agent từ chối.
    - Ở cấu hình `first_search=original_question`, search 1 là câu hỏi gốc. Lần search này được ghi trong trace với `forced: true`.
  - **Context:**
    - Context chỉ thêm, không bớt: chunk đã gửi sẽ ở lại, chunk trùng không gửi lại.
    - Budget đo bằng ký tự, tính cả header `[id | source | page | section]`. Mode `skip` bỏ chunk không vừa; mode `truncate` cắt chunk cuối nếu còn ít nhất 300 ký tự.
  - **Kiểm tra citation:** citation phải nằm trong context đã gửi; ID ngoài context bị loại và ghi event `dropped_invalid_citations`. Nếu không còn citation hợp lệ, agent trả về abstain.
  - **Chống prompt injection:** system prompt nói rõ đoạn tài liệu là **dữ liệu, không phải chỉ dẫn**.
  - **Xử lý lỗi:** client OpenRouter retry 3 lần với lỗi 429/5xx/mạng. Lỗi còn lại được ghi `status: "error"`, không thay bằng kết quả giả. Thực tế 0 lỗi trong 9 lần chạy dev và 2 lần chạy test.
  - **Không lộ gold:** gold chỉ được dùng **sau** khi agent chạy xong, để tính CER. Test `test_original_question_first_and_no_gold_in_messages` kiểm tra rằng message gửi model không chứa gold.

| Cấu hình / split            | Tool use | Số lượt gọi (search TB; LLM TB)           | Grounded answer 0/1/2 và trung bình | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm |
| --------------------------- | -------- | ----------------------------------------- | ----------------------------------- | --------------- | --------------- | --------------- | ------------ |
| dense / dev                 | 29/29    | 1,34; 2,34                                | 1/1/24 — 1,885                      | 33/33           | 25/25           | 3/3             | 1/26         |
| bm25 / dev                  | 29/29    | 1,28; 2,28                                | 1/0/25 — 1,923                      | 29/29           | 25/25           | 3/3             | 1/26         |
| hybrid / dev                | 29/29    | 1,21; 2,21                                | 0/0/26 — 2,000                      | 34/34           | 26/26           | 3/3             | 0/26         |
| hybrid_rerank / dev         | 29/29    | 1,21; 2,21                                | 0/0/26 — 2,000                      | 31/31           | 26/26           | 3/3             | 0/26         |
| dense_origfirst / dev       | 29/29    | 1,31; 1,31                                | 1/0/25 — 1,923                      | 30/30           | 25/25           | 3/3             | 1/26         |
| dense_ctx6400 / dev         | 29/29    | 1,28; 2,24                                | 0/1/25 — 1,962                      | 34/34           | 26/26           | 3/3             | 0/26         |
| dense_combo / dev           | 29/29    | 1,28; 1,28                                | 0/0/26 — 2,000                      | 32/32           | 26/26           | 3/3             | 0/26         |
| hybrid_combo / dev          | 29/29    | 1,24; 1,24                                | 0/0/26 — 2,000                      | 29/29           | 26/26           | 3/3             | 0/26         |
| hybrid_rerank_combo / dev   | 29/29    | 1,21; 1,21                                | 0/0/26 — 2,000                      | 32/32           | 26/26           | 3/3             | 0/26         |
| **dense (baseline) / test** | 11/11    | 1,45; 2,45 (phân bố search 1:8, 2:1, 3:2) | 0/0/8 — 2,000                       | 9/10            | 8/8             | 3/3             | 0/8          |
| **chosen / test**           | 11/11    | 1,64; 1,64 (phân bố search 1:7, 2:1, 3:3) | 0/0/8 — 2,000                       | 9/9             | 8/8             | 3/3             | 0/8          |

**Context trên test (chấm tay, 0/1/2):** cả 8/8 câu có đáp án đều được điểm **2** ở cả hai cấu hình. Câu gold đầy đủ (gồm cả điều kiện ở t02 và t07) nằm trong context cuối, kèm id, nguồn và trang. Nhãn và lý do nằm trong `results/agent/{dense,chosen}/test/reviews.json`, trường `context_grade`.

| Query ID | Loại câu                         | Tool call và kết quả                                                                                                                                                                                                                                          | Câu trả lời và citation                                            | Nhãn, lý do                                                                                                                                                                    |
| -------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| t01      | paraphrase                       | **chosen:** câu gốc có gold `p210:c4` ở hạng 2. **dense:** retrieval-only với câu gốc xếp gold hạng 5. Trong agent, query 1 do LLM viết không có gold; query 2 (`"compiler translates high-level language to assembly language program"`) thêm được `p210:c4` | "A compiler… [p210:c4]" (cả hai)                                   | 2 / 2. Citation hỗ trợ. Agent nhiều lượt bù được chỗ retrieval một lượt trượt                                                                                                  |
| t02      | condition                        | Gold `p223:c2` ở hạng 1 (cả hai)                                                                                                                                                                                                                              | Address bus một chiều, data bus hai chiều, kèm lý do [p223:c2]     | 2 / 2                                                                                                                                                                          |
| t03      | direct                           | Gold `p229:c0`                                                                                                                                                                                                                                                | Năm tính chất [p229:c0]. **dense** thêm một câu chỉ cite `p228:c2` | 2 / 2. Citation `p228:c2` của dense bị chấm **không hỗ trợ** (chấm chặt): chunk chỉ nói "không công nghệ nào đạt cả năm", còn ý "kết hợp thành memory hierarchy" nằm ở p229:c0 |
| t05      | direct                           | **chosen:** câu gốc không có gold trong top-10; LLM search lần 2 (`"process consists of program counter, registers…"`) lấy được `p268:c1`. **dense:** LLM tự viết query và lấy được gold ở lượt 1                                                             | "address space, CPU state, set of OS resources [p268:c1]"          | 2 / 2. Ví dụ CER (8/8) cao hơn Hit@3 (7/8)                                                                                                                                     |
| t06      | metadata_filter (chương 6)       | Filter `chapter=6` do người dùng nêu; gold `p281:c3`                                                                                                                                                                                                          | TLB [p281:c3]                                                      | 2 / 2                                                                                                                                                                          |
| t07      | condition                        | Gold `p290:c2` ở hạng 2                                                                                                                                                                                                                                       | "khi đăng nhập từ trình duyệt/máy khác" [p290:c1][p290:c2]         | 2 / 2. `p290:c1` hỗ trợ ý về cookie                                                                                                                                            |
| ut01     | thiếu evidence (Linux CFS)       | 3 lần search, thấy round-robin và time slice chung chung                                                                                                                                                                                                      | Từ chối: "do not state the default time quantum… CFS"              | Từ chối đúng. Không lấy số 2 ms trong ví dụ để đoán                                                                                                                            |
| ut02     | thiếu evidence (Apple M2)        | dense 1 lần search, chosen 3 lần                                                                                                                                                                                                                              | Từ chối, chỉ nêu "up to three cache levels" [p234:c3]              | Từ chối đúng. Không có khẳng định vô căn cứ                                                                                                                                    |
| ut03     | thiếu evidence (năm ra đời NTFS) | 3 lần search, thấy MFT p285                                                                                                                                                                                                                                   | Từ chối: "do not state the year…"                                  | Từ chối đúng                                                                                                                                                                   |

(t04, t08: cả hai cấu hình đều trả lời đúng, cite gold ở hạng 1, điểm 2.)

- **Đường dẫn trace, nhãn, lệnh chạy, thời gian và chi phí**
  - **Trace:** `results/agent/<config>/<split>/traces.json`. Mỗi câu có toàn bộ event (`llm`: token, chi phí, ms; `search`: query, filter, kết quả kèm rank và score, chunk đã thêm, cắt hoặc bỏ), context cuối, câu trả lời và citation.
  - **Nhãn và tổng hợp:** `reviews.json` là nhãn; `agent_metrics.json` là kết quả của `starter/agent_metrics.py`; `summary.json` là metric tự động.
  - **Retrieval:** `results/retrieval/<config>/<split>/`.
  - **Lệnh chạy:** xem README.
  - **Chi phí:** toàn bộ thí nghiệm tốn **0,135 USD** theo OpenRouter: 9 cấu hình dev, 2 cấu hình test và 1 smoke test 3 câu đã xóa. Embedding, BM25 và rerank chạy local nên 0 USD.
  - **Thời gian khởi tạo retriever:** khoảng 15 s, chủ yếu do nạp model e5 (dòng `ready in …` của `run_agent`). Thời gian này không tính vào latency mỗi câu.
  - **Cách đo latency:** chạy song song 4 worker trên laptop CPU, gồm cả độ trễ mạng tới OpenRouter.
- **Kết quả trước/sau, đánh đổi và giới hạn**
  - **Trên test, cấu hình chọn so với baseline:**
    - Chất lượng câu trả lời **bằng nhau**: grounded 2,0, abstention 3/3, 0 từ chối nhầm, CER 8/8.
    - Cấu hình chọn **nhanh hơn**: median 2,00 s so với 3,52 s.
    - **Rẻ hơn khoảng 11%**: 0,0056 so với 0,0063 USD.
    - Citation **sạch hơn**: 9/9 so với 9/10.
  - **Retrieval một lượt không đồng nhất:**
    - Hybrid tốt hơn ở Hit@3 (7/8 so với 6/8) nhưng **kém hơn ở Hit@1** (4/8 so với 5/8).
    - Vậy hybrid không vượt trội ở mọi metric. Lợi ích chính trên test đến từ thiết kế agent: câu hỏi gốc trước, budget lớn hơn, và nhiều lượt search bù cho lần tìm đầu bị trượt (t01, t05).
  - **Giới hạn:**
    - **Test nhỏ:** 8 + 3 câu, mỗi câu tương ứng 12,5 điểm phần trăm. Cả hai cấu hình đều chạm trần ở grounded, nên test **không phân biệt được** chất lượng câu trả lời.
    - **Câu hỏi dễ:** benchmark do AI (Claude) soạn từ chính text nguồn, câu hỏi bám từ ngữ của nguồn nên dễ hơn câu hỏi thật.
    - **Ít câu khó:** không có câu multi-hop bắt buộc nhiều đoạn; chỉ có 3 câu thiếu evidence mỗi split.
    - **Gold chưa đầy đủ:** ví dụ d15.
    - **Không tất định:** LLM vẫn không tất định dù `temperature=0`. Ví dụ, d01 của `dense_ctx6400` đúng chỉ vì LLM viết query khác, không phải nhờ budget lớn hơn. Mỗi cấu hình chỉ chạy **một lần**, nên chênh lệch 1 câu nằm trong nhiễu.
    - **Nhãn do AI soạn nháp, tác giả duyệt:** AI (Claude) soạn nhãn sau khi đọc từng câu trả lời và từng chunk được cite. Tác giả đã duyệt lại toàn bộ và giữ nguyên, ghi `labeled_by = author-reviewed`. Người chấm cũng chính là tác giả, không có người chấm độc lập. Vì nhãn không bị sửa sau khi duyệt, có nguy cơ tác giả bị ảnh hưởng bởi bản nháp.
    - **Rerank:** cross-encoder MS MARCO chỉ hỗ trợ tiếng Anh, nên phù hợp với corpus và câu hỏi tiếng Anh này. Câu hỏi tiếng Việt chưa được thử.

## Thử thách nâng cao (nếu thực hiện)

Không thực hiện.

## Sử dụng AI

- **Đã dùng Claude Code (Claude Opus 5.5) để:**
  - viết toàn bộ code trong `src/` và `tests/test_day7.py`;
  - soạn 19 câu benchmark mới, kèm regex kiểm tra câu thiếu evidence;
  - chạy thí nghiệm;
  - soạn nhãn đánh giá;
  - viết báo cáo này.
- **Cách kiểm tra:**
  - Evidence được kiểm bằng script (`prepare_data` gọi `baseline.validate`).
  - Mọi số liệu trong báo cáo lấy từ file trong `results/`, do các lệnh đã chạy sinh ra.
  - Chi phí được đối chiếu với usage của OpenRouter.
  - Citation không chứa gold được đọc nguyên văn bằng `python -m src.show_cited`.
  - Tác giả đã duyệt toàn bộ nhãn trong `reviews.json` và giữ nguyên. Các override kèm lý do được liệt kê trong `src/labels.py`.

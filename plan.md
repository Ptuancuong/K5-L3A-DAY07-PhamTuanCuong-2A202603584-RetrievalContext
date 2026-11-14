# Kế hoạch làm Lab Day 7 — Agentic RAG

> Tổng hợp từ: README, GUIDE, BENCHMARK, RUBRIC, RULES, SUBMISSION, CHECKPOINTS, PSEUDOCODE, ADVANCED, REPORT_TEMPLATE, starter/README, data/README và code trong `starter/`.

## 0. Tóm tắt bài lab

**Mục tiêu:** dùng embedding và vector store **Day 6** để xây một **agent dùng LLM thật**. Agent tự gọi tool để tìm bằng chứng, trả lời **có citation**, và **từ chối** khi tài liệu không đủ thông tin.

**Điểm:** phần cơ bản 85 điểm, cộng tối đa 15 điểm bonus (thử thách nâng cao, chỉ được cộng khi đạt đủ điều kiện), tổng tối đa 100.

**Yêu cầu tối thiểu:**

| Hạng mục                 | Tối thiểu                                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Phương pháp retrieval    | **3 phương pháp khác nhau**, bắt buộc có **dense trên vector store Day 6**                                   |
| Cấu hình thử cải thiện   | **2 cấu hình**, mỗi cấu hình có giả thuyết và kết quả riêng                                                  |
| Benchmark                | **24 câu**: dev = 15 câu có đáp án + 2 câu thiếu bằng chứng; test = 5 câu có đáp án + 2 câu thiếu bằng chứng |
| Phân tích lỗi            | Đọc **ít nhất 2 lỗi trên dev**, nêu nguyên nhân, đo lại sau khi sửa                                          |
| Chấm tay                 | Đọc **5 câu test có đáp án + 2 câu test thiếu bằng chứng**, cho baseline và cấu hình đã chọn                 |
| Corpus (nếu tự chuẩn bị) | Ít nhất **30 trang** nội dung hợp lệ                                                                         |

---

## 1. Các bước cần làm (theo thứ tự)

### Bước 1 — Chuẩn bị môi trường và dữ liệu Day 6 (0:00–1:00)

- [ ] Dùng Python 3.11 trở lên, tạo `.venv`. Đặt API key trong `.env` (file này đã có trong `.gitignore`, **không commit**).
- [ ] Chọn một **LLM hỗ trợ tool calling** (API hoặc chạy trên máy đều được, không bắt buộc trả phí).
- [ ] Lấy lại từ Day 6: chunk, chunk ID, nguồn, trang, metadata, **vector store** và **embedding model**.
  - Ghi lại: tên và phiên bản embedding model, **số chiều**, cách kết nối vector store.
  - Query embedding phải **cùng model** với embedding đã dùng để index. Nếu đổi model, phải tạo lại index và ghi lại chi phí.
  - **Không dùng vector ngẫu nhiên** để đánh giá. Nếu chưa xong Day 6, phải hoàn thành phần embedding và vector store thật trước.
- [ ] Xuất chunk sang JSON array theo [data/README.md](data/README.md):
  - Chunk gồm `id`, `text`, `source_id`, `source`, `page`, `metadata`. ID phải duy nhất.
  - Nếu dữ liệu Day 6 có các trường `chunk_id`, `document_id`, `gold_source_id`, `gold_page`, `evidence_quote`, có thể dùng `starter/convert_day6.py`. Nếu không có, tự viết adapter.
- [ ] Chạy `python -m unittest discover -s tests -v` để kiểm tra code starter chạy được. Test này dùng mock, **không phải benchmark**.

### Bước 2 — Tạo benchmark và chia dev/test

- [ ] **Câu có đáp án** (dev ≥ 15, test ≥ 5): gồm `id`, `split`, `question`, `expected_answer`, `gold: [{source_id, page, evidence}]`.
  - Với schema mẫu, `evidence` phải **nằm trọn trong một chunk** đúng nguồn và đúng trang. `baseline.py` sẽ báo lỗi nếu không thỏa.
  - Nhiều phần tử trong `gold` được hiểu là các evidence **thay thế** nhau (chỉ cần một). Nếu có câu multi-hop cần nhiều đoạn, mở rộng schema và ghi rõ thế nào là "đủ evidence".
  - Có thể thêm `filter` nếu đó là thông tin **người dùng cung cấp trước**.
- [ ] **Câu thiếu bằng chứng** (dev ≥ 2, test ≥ 2): gồm `answerable: false`, `expected_behavior: "search_and_abstain"`, `absence_reason`.
  - Nên chọn câu **gần chủ đề** của tài liệu. Ghi lại đã kiểm tra trong tài liệu bằng cách nào để biết thông tin không có (không suy ra chỉ vì top-k không tìm thấy).
  - **Không** tính các câu này vào mẫu số của retrieval metrics.
- [ ] Tạo thêm file `cases.json` (gồm `id`, `split`, `answerable`) để dùng với `agent_metrics.py`.
- [ ] **Chia dev/test ngay từ đầu**, sau đó không đọc test khi đang chỉnh hệ thống.

### Bước 3 — Triển khai ít nhất 3 phương pháp retrieval (1:00–3:30)

Đề xuất (tự chọn được):

| #   | Phương pháp                      | Ghi chú                                                                                  |
| --- | -------------------------------- | ---------------------------------------------------------------------------------------- |
| 1   | **Dense** (bắt buộc)             | Embed query, tìm trong vector store Day 6; có thể thử metadata filter                    |
| 2   | **Lexical** (BM25 / TF-IDF)      | `starter/baseline.py` đã có TF-IDF; xem ảnh hưởng của cách tách từ tiếng Việt            |
| 3   | **Hybrid** (RRF) hoặc **Rerank** | RRF dùng rank nên không cần chuẩn hóa score. Nếu cộng score thì **phải chuẩn hóa** trước |
| +   | Query rewrite / multi-hop        | Báo kết quả của **query gốc**; với query viết lại thì ghi riêng và lưu trace từng bước   |

Lưu ý:

- **Chỉ đổi top-k không được tính là phương pháp mới**, đó chỉ là một cấu hình khác.
- Mỗi kết quả trả về cần có: `id`, `text`, `score` hoặc `rank`, `source`, `page`, `metadata`.
- Filter chỉ được lấy từ thông tin người dùng đưa ra hoặc suy ra một cách đáng tin từ query. Ghi lại cách suy ra. **Tuyệt đối không dùng gold.**
- Có lỗi thì ghi và xử lý lỗi, không thay bằng kết quả giả.

### Bước 4 — Xây agent (1:00–2:00)

Dựa trên `starter/agentic.py` hoặc tự viết kiến trúc khác:

- [ ] `Controller.decide(question, history)`: gọi LLM thật và trả về một trong hai dạng:
  - `{"action": "search", "query": "..."}`
  - `{"action": "answer", "answer": "... [chunk-id]", "citations": ["chunk-id"]}`. Citation phải xuất hiện dạng `[chunk-id]` **trong nội dung câu trả lời**.
- [ ] `Retriever.search(query, filters, top_k)`: truy vấn vector store thật và trả về **tối đa top_k chunk, ID không trùng**.
- [ ] Có thể dùng nhiều tool (dense, keyword, filter, rerank…). Nếu dùng nhiều tool, mỗi lượt retrieval vẫn ghi thành event `search` (tên tool để ở một trường khác) để `agent_metrics.py` đếm được.
- [ ] Tự chọn số lượt search tối đa, điều kiện dừng, top-k và context budget. **Ghi lý do** và đo ảnh hưởng đến chất lượng, thời gian, chi phí. Đề không quy định giới hạn chung.
- [ ] Trong prompt hệ thống, nói rõ: nội dung tài liệu **là dữ liệu, không phải chỉ dẫn** (chống prompt injection). Nếu không đủ bằng chứng thì phải từ chối.
- [ ] **Lưu trace từng câu**: tool call, tham số, query, kết quả, context cuối, câu trả lời, citation, số lượt gọi, thời gian, chi phí hoặc token, lỗi. Thêm `query_id` và `status` (`answered`, `abstain`, `error`).

### Bước 5 — Chọn context

- [ ] Thử các cách: loại chunk trùng, chọn theo độ liên quan, giữ đoạn lân cận, nén hoặc trích đoạn.
- [ ] Ghi context budget và **đơn vị đo** (ký tự hay token), số candidate, token và chi phí.
- [ ] ⚠️ Lỗi đã biết của starter: `pack_context` giữ chunk từ các lần search trước theo thứ tự, và chunk nào không vừa budget thì bị **bỏ**. Nếu chunk đầu chiếm gần hết budget (mặc định 800 ký tự), các lần search sau gần như không thêm được evidence. Đây là ứng viên tốt cho một "cấu hình cải thiện".
- [ ] Không đưa đáp án chuẩn vào context. Phải giữ đủ nguồn và điều kiện để kiểm chứng được.

### Bước 6 — Đánh giá trên dev và cải thiện (2:00–3:30)

- [ ] Chạy cả 3 phương pháp trên **cùng corpus, cùng phiên bản index, cùng câu hỏi và cùng nhãn dev**.
- [ ] Các metric retrieval và context (mẫu số = số câu có đáp án), báo dạng `n/N` kèm tỷ lệ:
  - **Hit@1**: evidence hợp lệ nằm ở vị trí top-1.
  - **Evidence Hit@3**: evidence nằm trong top-3. Dù pipeline dùng top-k khác 3, vẫn phải xuất top-3 để so sánh.
  - **Context Evidence Rate**: đủ evidence trong **context cuối** gửi cho model.
  - Có thể thêm Recall@k, MRR. Ghi thời gian và chi phí của từng cấu hình.
- [ ] **Công bố tiêu chí chọn cấu hình trước khi chọn**: chất lượng retrieval, context, câu trả lời, thời gian và chi phí.
- [ ] Thử **≥ 2 cấu hình cải thiện**, mỗi cái có giả thuyết, thay đổi và kết quả trước/sau. Không nhất thiết phải tăng điểm, nhưng **phải báo trung thực cả kết quả không cải thiện**.
  - Ví dụ: tăng top-k kèm rerank, đổi context budget hoặc cách đóng gói context, multi-turn search, hybrid RRF.
- [ ] Đọc ≥ 2 lỗi trên dev, tìm nguyên nhân, sửa, rồi đo lại.
- [ ] **Chốt cấu hình trước khi chạy test.**

### Bước 7 — Chạy test và chấm tay (3:30–4:00)

- [ ] Chạy **baseline** và **cấu hình đã chọn** trên cùng bộ test.
- [ ] Chấm context (≥ 5 câu test có đáp án, cho cả baseline và cấu hình chọn): **0** = không có evidence, **1** = có nhưng thiếu điều kiện hoặc nguồn, **2** = đủ evidence và nguồn. Ghi lý do và số câu ở từng mức.
- [ ] Chấm câu trả lời và tạo `reviews.json`:
  - `answer_grade` 0/1/2 cho câu có đáp án. Câu có đáp án mà agent từ chối thì chấm **0**.
  - `citation_support`: một giá trị true/false cho **mỗi citation**. Phải **đọc nguồn** để xác nhận nguồn thật sự hỗ trợ câu trả lời; ID đúng hoặc LLM verifier đồng ý là **chưa đủ**.
  - `abstention_correct` cho câu thiếu bằng chứng. Kiểm tra agent thật sự từ chối và không thêm khẳng định không có căn cứ.
- [ ] Tổng hợp bằng: `python starter/agent_metrics.py --cases ... --traces ... --reviews ... --split test --output ...`
  - Các chỉ số: Tool use, Grounded answer (phân bố 0/1/2 và trung bình), Citation hợp lệ, Câu trả lời có citation, Abstention đúng, Từ chối nhầm câu có đáp án. Lỗi model hoặc vector store **báo riêng**.

### Bước 8 — Báo cáo và nộp bài

- [ ] Sao chép `report/individual/MSSV_HoTen.md` thành `report/individual/2A202603584_PhamTuanCuong.md` và điền đủ các bảng:
  - Dữ liệu và benchmark: nguồn, quyền sử dụng, số trang, số chunk, vector store, embedding model và số chiều, agent model, cách chia dev/test.
  - Bảng retrieval: Baseline, PP2, PP3, Cải thiện 1, Cải thiện 2 (trên dev); Cấu hình chọn và Baseline (trên test).
  - Bảng đánh giá agent và bảng từng query (tool call, câu trả lời, citation, nhãn, lý do).
  - Hai lỗi dev, kết quả trước/sau, các đánh đổi và giới hạn.
- [ ] README hoặc hướng dẫn chạy: lệnh tái lập, model, dữ liệu, cách kết nối vector store.
- [ ] Trình bày tối thiểu: **một câu trả lời có bằng chứng, một câu thiếu bằng chứng và một lỗi**.
- [ ] `starter/data/` và `starter/results/` đang bị `.gitignore`. Nếu được phép chia sẻ thì dùng `git add -f <path>`, nếu không thì ghi cách tái tạo.
- [ ] Đảm bảo người chấm có quyền xem repo cá nhân. **Không push vào repo đề bài.**

---

## 2. Những điểm cần đặc biệt chú ý (dễ mất điểm)

1. **Không để gold lọt vào agent hay retrieval**: không dùng `gold`, `expected_answer` hay vùng evidence làm query, filter hoặc context.
2. **Không chỉnh hệ thống bằng test.** Nếu đã lỡ xem test để chỉnh thì phải **tạo bộ test mới** và ghi rõ trong báo cáo.
3. **Không dùng mock hay dữ liệu giả để báo kết quả.** Lỗi kết nối phải được báo (`status: "error"`), không thay bằng kết quả giả.
4. **Citation ID hợp lệ chưa có nghĩa là nguồn hỗ trợ câu trả lời.** Phải đọc nguồn để đối chiếu.
5. **Chỉ đổi top-k không được tính là phương pháp mới.**
6. **Không cộng thẳng score** của các retriever khác nhau nếu chưa chuẩn hóa. Dùng RRF hoặc min-max hoặc z-score.
7. **Báo kết quả của query gốc.** Kết quả của query viết lại hoặc multi-hop báo riêng, kèm trace từng bước.
8. **Trung thực**: điểm thấp vẫn được ghi nhận nếu thí nghiệm làm đúng và phân tích thật. Không bịa số liệu. Phải báo cả các cấu hình không cải thiện.
9. **Bảo mật**: không commit `.env`, API key, token hay dữ liệu mật hoặc cá nhân. Kiểm tra quyền sử dụng dữ liệu trước khi gửi lên dịch vụ ngoài.
10. **Câu thiếu bằng chứng không tính vào mẫu số** của Hit@1, Hit@3 và Context Evidence Rate.
11. **Context Evidence Rate có thể cao hơn Hit@3**, vì context có thể được ghép từ nhiều lượt search. Đây là hiện tượng bình thường.
12. **Ghi thời gian và chi phí** cho mọi cấu hình. Rubric có 3 điểm cho phần đánh đổi giữa chất lượng, thời gian và chi phí.
13. Đặt tên file kết quả khác nhau cho mỗi lần chạy, vì file cùng tên sẽ **bị ghi đè**.

---

## 3. Phân bổ điểm (để ưu tiên công sức)

| Hạng mục                | Điểm | Cần có                                                                                                      |
| ----------------------- | ---: | ----------------------------------------------------------------------------------------------------------- |
| Dữ liệu và benchmark    |   13 | Kết nối Day 6, embedding, nguồn (6); câu hỏi, evidence, split (7)                                           |
| Retrieval               |   17 | ≥ 3 phương pháp gồm dense (10); cấu hình, nguồn, score/rank, xử lý lỗi (7)                                  |
| Agent và context        |   17 | LLM thật, trace tool, điều kiện dừng (9); chọn context, citation, xử lý thiếu evidence (8)                  |
| Đánh giá                |   17 | Metric retrieval và context có thể kiểm chứng (9); đánh giá câu trả lời, citation, abstention, tool use (8) |
| Thử nghiệm và cải thiện |   13 | ≥ 2 cấu hình, giả thuyết, phân tích lỗi (5); chọn trên dev rồi chạy test (5); đánh đổi (3)                  |
| Tái lập và báo cáo      |    8 | Code, cách chạy, model, dữ liệu (5); kết luận, nguồn, giới hạn (3)                                          |

---

## 4. Thử thách nâng cao (tùy chọn, +15 điểm, không được cộng một phần)

Chỉ nên làm khi phần cơ bản đã xong. Phần này cần nhiều thời gian hơn lịch 4 giờ.

- **Tài liệu**: một tài liệu thực tế **≥ 100 trang** có text, bảng, ảnh và biểu đồ (ví dụ báo cáo thường niên hoặc báo cáo thống kê). Ghi nguồn, phiên bản, số trang, quyền sử dụng. Người chấm phải truy cập được bản gốc.
- **Index toàn bộ** nội dung hữu ích, không chỉ các trang có trong benchmark. Mỗi phần được index phải giữ liên kết tới trang gốc. Với bảng, ảnh, biểu đồ thì lưu vùng trang hoặc ảnh crop. Ghi rõ trang nào không xử lý được và lý do.
- **Pipeline đa phương thức** (tự chọn): OCR, phân tích layout, trích bảng, vision model hoặc caption, multimodal embedding… **Phải đối chiếu nội dung trích xuất với bản gốc.**
- **Benchmark riêng, chia dev/test trước khi thử nghiệm**:
  - Test ≥ **30 câu** = 24 câu có đáp án + 6 câu thiếu bằng chứng. Trong 24 câu có đáp án, tối thiểu: **Bảng 6, Ảnh/sơ đồ 5, Biểu đồ 5, Multi-hop 4, Text 4**. Mỗi câu chỉ thuộc **một nhóm chính**.
  - Dev ≥ 15 câu có đáp án + 3 câu thiếu bằng chứng.
  - Câu ở dev và test không được trùng nhau hoặc chỉ là cách diễn đạt khác của cùng một câu.
  - Mỗi câu ghi: ID, nhóm, câu hỏi, đáp án hoặc hành vi từ chối mong đợi, nguồn, lý do, evidence (trang, ô/hàng/cột hoặc vùng hình), đơn vị, phép tính.
- **Chấm đạt hoặc không đạt cho từng câu test**. Cần **≥ 90%** (30 câu thì cần **≥ 27/30**), không làm tròn.
  - Câu có đáp án chỉ đạt khi đúng và đủ, đúng đơn vị và phép tính, citation chỉ ra đúng trang và vùng evidence.
  - Lỗi hệ thống hoặc timeout tính là không đạt và vẫn nằm trong mẫu số.
  - Phải tự đọc và ghi nhãn **từng câu**. LLM judge chỉ được dùng để hỗ trợ.
- Báo `n/N` theo từng nhóm và toàn bộ, kèm số lỗi, thời gian, chi phí. Điền phần "Thử thách nâng cao" trong báo cáo.

---

## 5. Checklist nộp bài (theo SUBMISSION.md)

- [ ] Code agent, ≥ 3 phương pháp retrieval (gồm dense), test và hướng dẫn chạy
- [ ] Embedding model, vector store, cách kết nối, dữ liệu được phép chia sẻ hoặc cách tái tạo
- [ ] Benchmark ≥ 20 câu có evidence và ≥ 4 câu thiếu evidence, đã chia dev/test
- [ ] Kết quả từng query và tool call: context, câu trả lời, citation, lỗi, thời gian, chi phí
- [ ] ≥ 2 cấu hình cải thiện, bảng benchmark, nhãn, phân tích lỗi, lý do chọn cấu hình
- [ ] Báo cáo `report/individual/2A202603584_PhamTuanCuong.md`
- [ ] Repo cá nhân đã cấp quyền xem cho người chấm, không chứa `.env`, key hay token
- [ ] (Nếu làm nâng cao) nguồn tài liệu, thống kê index, benchmark có evidence theo trang và vùng, trace và nhãn toàn bộ test, bằng chứng đạt ≥ 90%

---

## 6. Gợi ý cấu trúc thư mục khi làm

```
src/
  retrievers/        dense.py, bm25.py, hybrid.py (RRF), rerank.py
  agent/             controller.py (LLM thật), tools.py, run_agent.py
  eval/              retrieval_eval.py (Hit@1, Hit@3, Context Evidence Rate), run_benchmark.py
configs/             baseline.yaml, improve1.yaml, improve2.yaml, chosen.yaml
benchmark/           questions.json, cases.json
results/<config>/<split>/   traces.json, summary.json, reviews.json
report/individual/2A202603584_PhamTuanCuong.md
```

Việc cần chuẩn bị ngay: **xác định vị trí dữ liệu và vector store Day 6** (repo này chưa có), và **chọn LLM có tool calling** để dùng cho agent.

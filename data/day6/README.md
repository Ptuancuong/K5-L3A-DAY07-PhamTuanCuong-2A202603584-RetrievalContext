# Chunk Day 6 (export từ pgvector)

`chunks_A.json` (538 chunk) và `chunks_B.json` (323 chunk) được export bằng `python -m src.prepare_data` từ bảng `chunks` của vector store Day 6:

- **Database:** PostgreSQL 16 + pgvector 0.8.7.
- **Embedding:** `intfloat/multilingual-e5-small`, 384 chiều.
- **Index A:** chunk cố định 500 ký tự, overlap 50.
- **Index B:** chunk theo đoạn, tối đa 1.000 ký tự. Day 6 chọn index B (cấu hình C = B + filter `chapter`).

Mỗi chunk theo schema `id, text, source_id, source, page, metadata`. `metadata` gồm `chapter`, `section`, `section_title`, `char_start`, `char_end`, `index` và `embedding_model`. `page` là số trang vật lý của PDF, đánh số từ 1.

**Nguồn:** OpenStax, _Introduction to Computer Science_, Rice University, chương 5–6. Giấy phép CC BY-NC-SA 4.0. Truy cập miễn phí tại openstax.org. Dữ liệu chỉ dùng cho mục đích học tập, phi thương mại, có ghi nguồn.

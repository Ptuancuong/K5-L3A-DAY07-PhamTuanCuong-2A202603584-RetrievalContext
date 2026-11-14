# Tiêu chí chọn cấu hình (công bố trước khi chạy)

Tiêu chí này được commit cùng benchmark, **trước** lần chạy retrieval hay agent đầu tiên. Chỉ dùng **dev** để chọn cấu hình. Test chỉ chạy **một lần** sau khi đã commit `configs/chosen.json`.

## Điều kiện so sánh

- **Giữ giống nhau cho mọi cấu hình:**
  - corpus: index B của Day 6, 323 chunk
  - câu hỏi và nhãn
  - LLM: `anthropic/claude-haiku-5.5` qua OpenRouter, `temperature=0`
  - system prompt
- **Chỉ thay đổi:** phương pháp retrieval, top-k, cách chọn context, context budget và số lượt search tối đa.
- **Đơn vị context budget:** ký tự, tính cả dòng header `[id | source | page]` của mỗi chunk.

## Thứ tự xét

1. **Ràng buộc:**
   - Abstention đúng trên dev phải đạt ít nhất **2/3** câu thiếu bằng chứng.
   - Số câu có đáp án bị từ chối nhầm trên dev không được vượt quá **3/26**.
2. **Grounded answer trung bình trên dev:** điểm 0/1/2 cho câu có đáp án.
3. **Context Evidence Rate của agent trên dev:** context cuối gửi model có chứa evidence gold.
4. **Retrieval trên dev:** Evidence Hit@3, rồi đến Hit@1. Chạy trên câu hỏi gốc với cùng cutoff 3.
5. **Chi phí và thời gian:**
   - Nếu hai cấu hình chênh nhau **≤ 1 câu** ở mục 2 và mục 3, chọn cấu hình có median latency mỗi câu thấp hơn. Nếu vẫn hòa thì chọn cấu hình rẻ hơn.
   - Nếu vẫn hòa, chọn cấu hình đơn giản hơn: ít thành phần hơn, không cần model phụ.

## Baseline

Baseline là **dense retrieval trên vector store Day 6**. Trên test chỉ chạy baseline và cấu hình đã chọn, với cùng LLM và prompt.

## Ghi nhãn

- **Tự động:** Hit@1, Hit@3 và Context Evidence Rate được tính bằng code, dựa trên việc chuỗi evidence xuất hiện trong chunk.
- **Thủ công:** answer grade, citation support và abstention được chấm bằng cách đọc câu trả lời và chunk được cite.
  - Nhãn nháp do AI đề xuất phải được tác giả duyệt.
  - Mỗi nhãn ghi rõ người chấm (`labeled_by`).
  - Một citation chỉ được tính là "hợp lệ" khi đọc chunk và thấy nó hỗ trợ câu trả lời.

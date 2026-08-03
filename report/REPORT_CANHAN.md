# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Vũ Đức Anh
**Nhóm:** [Tên nhóm]
**Ngày:** 03/08/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**

> Hai vector embedding hướng gần nhau trong không gian nhiều chiều, tức hai đoạn văn bản có ý nghĩa tương đồng hoặc dùng từ ngữ/cấu trúc tương tự. Giá trị gần 1 nghĩa là rất giống nhau về mặt ngữ nghĩa (theo mô hình embedding).

**Ví dụ có độ tương tự CAO:**

- Câu A: _Sinh viên đăng ký học phần trên cổng học vụ theo lịch học kỳ._
- Câu B: _Quy trình đăng ký môn học trực tuyến được thực hiện qua hệ thống học vụ._
- Tại sao tương đồng: Cùng chủ đề đăng ký học phần, cùng đối tượng sinh viên và bối cảnh học vụ.

**Ví dụ có độ tương tự THẤP:**

- Câu A: _Thư viện cung cấp dịch vụ mượn sách cho sinh viên._
- Câu B: _Đội bóng đá vừa thắng trận chung kết giải quốc gia._
- Tại sao khác: Hai câu thuộc lĩnh vực hoàn toàn khác nhau, không chia sẻ ngữ cảnh hay từ khóa liên quan.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**

> Embeddings thường được chuẩn hóa (normalized) nên độ dài vector không phản ánh mức độ liên quan ngữ nghĩa. Cosine đo góc giữa hai vector — tức hướng/ý nghĩa — thay vì khoảng cách tuyệt đối, phù hợp hơn khi so sánh văn bản có độ dài khác nhau.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**

> _Trình bày phép tính:_
> `step = chunk_size - overlap = 500 - 50 = 450`
> `số chunk = ⌈(10,000 - 50) / 450⌉ = ⌈9,950 / 450⌉ = ⌈22.11...⌉ = 23`
> _Đáp án:_ **23 chunks**

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**

> `step = 500 - 100 = 400` → `⌈(10,000 - 100) / 400⌉ = ⌈24.75⌉ = 25 chunks` — tăng thêm 2 chunk. Overlap lớn hơn giúp giữ ngữ cảnh ở ranh giới giữa các chunk (ví dụ một câu bị cắt đôi vẫn xuất hiện ở chunk kế tiếp), cải thiện khả năng truy xuất thông tin nằm ở biên đoạn văn.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:

> Dùng regex `(?<=[.!?])\s+|\.\n` để tách câu theo dấu chấm/hỏi/chấm than kèm khoảng trắng hoặc xuống dòng. Sau đó gom từng nhóm `max_sentences_per_chunk` câu liên tiếp thành một chunk. Xử lý edge case: chuỗi rỗng trả về `[]`, câu cuối không có dấu chấm vẫn được giữ lại nhờ strip whitespace.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:

> Thuật toán thử lần lượt các separator theo thứ tự ưu tiên (`\n\n` → `\n` → `. ` → ` `). Nếu đoạn vẫn dài hơn `chunk_size`, đệ quy sang separator tiếp theo; nếu hết separator thì fallback sang `FixedSizeChunker`. Base case: đoạn ≤ `chunk_size` thì trả về trực tiếp một chunk.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:

> Mỗi `Document` được embed qua `embedding_fn`, lưu thành record `{id, content, embedding, metadata}`. Với ChromaDB có sẵn thì dùng `collection.add()`; không thì lưu in-memory trong `self._store`. `search` embed câu hỏi, tính dot product với mọi embedding đã lưu (mock/local đã normalize nên dot product ≈ cosine), sắp xếp giảm dần và trả top-k.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:

> **Lọc trước, tìm sau:** duyệt `self._store`, giữ chunk có metadata khớp toàn bộ key-value trong `metadata_filter`, rồi gọi `_search_records` trên tập đã lọc. `delete_document` xóa mọi record có `metadata["doc_id"]` trùng, hoặc `id` trùng/khớp prefix `{doc_id}::` (hỗ trợ cả chunk lẫn document gốc).

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:

> Gọi `store.search(question, top_k)` lấy các chunk liên quan, ghép thành khối Context có đánh số `[1]`, `[2]`, … Prompt yêu cầu LLM chỉ trả lời dựa trên context và nói "không biết" nếu thiếu thông tin. Gọi `llm_fn(prompt)` và trả về chuỗi kết quả.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
python -m unittest tests.test_solution -v

test_chunker_classes_exist ... ok
test_mock_embedder_exists ... ok
test_counts_are_positive ... ok
test_each_strategy_has_count_and_avg_length ... ok
test_returns_three_strategies ... ok
test_identical_vectors_return_1 ... ok
test_opposite_vectors_return_minus_1 ... ok
test_orthogonal_vectors_return_0 ... ok
test_zero_vector_returns_0 ... ok
test_add_documents_increases_size ... ok
test_add_more_increases_further ... ok
test_initial_size_is_zero ... ok
test_search_results_have_content_key ... ok
test_search_results_have_score_key ... ok
test_search_results_sorted_by_score_descending ... ok
test_search_returns_at_most_top_k ... ok
test_search_returns_list ... ok
test_delete_reduces_collection_size ... ok
test_delete_returns_false_for_nonexistent_doc ... ok
test_delete_returns_true_for_existing_doc ... ok
test_filter_by_department ... ok
test_no_filter_returns_all_candidates ... ok
test_returns_at_most_top_k ... ok
test_chunks_respect_size ... ok
test_correct_number_of_chunks_no_overlap ... ok
test_empty_text_returns_empty_list ... ok
test_no_overlap_no_shared_content ... ok
test_overlap_creates_shared_content ... ok
test_returns_list ... ok
test_single_chunk_if_text_shorter ... ok
test_answer_non_empty ... ok
test_answer_returns_string ... ok
test_root_main_entrypoint_exists ... ok
test_src_package_exists ... ok
test_chunks_within_size_when_possible ... ok
test_empty_separators_falls_back_gracefully ... ok
test_handles_double_newline_separator ... ok
test_returns_list ... ok
test_chunks_are_strings ... ok
test_respects_max_sentences ... ok
test_returns_list ... ok
test_single_sentence_max_gives_many_chunks ... ok

----------------------------------------------------------------------
Ran 42 tests in 0.012s

OK
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

> _Ghi chú:_ Dự đoán dựa trên trực giác ngữ nghĩa. Điểm thực tế chạy bằng `MockEmbedder` (hash-based, không phản ánh ngữ nghĩa tiếng Việt). Với `EMBEDDING_PROVIDER=local` kết quả sẽ khác và phù hợp dự đoán hơn.

| Cặp | Câu A                                                  | Câu B                                               | Dự đoán | Điểm thực tế | Đúng? |
| --- | ------------------------------------------------------ | --------------------------------------------------- | ------- | ------------ | ----- |
| 1   | Sinh viên đăng ký học phần trên cổng học vụ.           | Quy trình đăng ký môn học trực tuyến cho sinh viên. | cao     | -0.079       | Không |
| 2   | Thư viện cho mượn sách và cung cấp không gian học tập. | Dịch vụ thư viện hỗ trợ mượn tài liệu.              | cao     | -0.036       | Không |
| 3   | Sinh viên đăng ký học phần theo lịch học kỳ.           | Thời tiết hôm nay nắng đẹp.                         | thấp    | 0.118        | Có    |
| 4   | Python là ngôn ngữ lập trình bậc cao.                  | Java cũng là ngôn ngữ lập trình phổ biến.           | cao     | -0.061       | Không |
| 5   | Khi trùng lịch, sinh viên điều chỉnh lớp học phần.     | Nếu bị trùng lịch học, cần đổi lớp trước hạn.       | cao     | -0.112       | Không |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**

> Cặp 3 (đăng ký học phần vs thời tiết) có điểm dương cao nhất (+0.118) dù dự đoán là thấp — điều này bất ngờ nhất. Nguyên nhân là MockEmbedder tạo vector từ hash MD5, không hiểu ngữ nghĩa; hai câu có thể trùng hash pattern ngẫu nhiên. Điều này cho thấy **chất lượng embedding phụ thuộc hoàn toàn vào mô hình** — mock chỉ phục vụ unit test, không dùng để đánh giá retrieval thực tế. Cần embedder đa ngôn ngữ (ví dụ `paraphrase-multilingual-MiniLM-L12-v2`) mới phản ánh đúng ý nghĩa văn bản.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân trong gói `src`. **Chiến lược chunking:** `RecursiveChunker(chunk_size=300)` trên `data/k3_university/`. **Embedder:** MockEmbedder (môi trường chưa cài `sentence-transformers`).

| #   | Câu hỏi (Query)                                                                  | Top-1 Chunk truy xuất được (tóm tắt)                                                             | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt)                                                                 |
| --- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------- | ------------------------------ | ----------------------------------------------------------------------------------------------- |
| 1   | Sinh viên đăng ký học phần ở đâu và theo lịch nào?                               | Đăng ký trên cổng học vụ theo lịch từng học kỳ; kiểm tra học phần tiên quyết trước khi xác nhận. | 0.240      | Có                             | Sinh viên đăng ký học phần qua cổng học vụ theo lịch học kỳ, cần kiểm tra điều kiện tiên quyết. |
| 2   | Khi gặp lỗi trùng lịch thì sinh viên cần làm gì?                                 | _(Top-1 là blockquote hướng dẫn metadata template — nhiễu)_                                      | 0.282      | Không                          | Agent không trả lời đúng vì chunk nhiễu được xếp hạng cao nhất.                                 |
| 3   | Thư viện cung cấp những dịch vụ gì?                                              | Mượn tài liệu và không gian học tập cho SV/GV/NV; cần thẻ định danh khi mượn.                    | 0.160      | Có                             | Thư viện cung cấp mượn tài liệu và không gian học tập.                                          |
| 4   | Cần mang gì khi sử dụng dịch vụ mượn tài liệu?                                   | _(Top-1 là blockquote template — nhiễu)_                                                         | 0.033      | Không                          | Agent không tìm được thông tin "mang thẻ định danh" ở top-1.                                    |
| 5   | Quy định đăng ký học phần dành cho sinh viên là gì? _(filter: audience=student)_ | Khi trùng lịch, điều chỉnh lớp trước hạn; yêu cầu ngoại lệ qua kênh học vụ chính thức.           | 0.045      | Một phần                       | Trả lời được phần xử lý trùng lịch nhưng chưa cover toàn bộ quy trình đăng ký.                  |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 3 / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**

> Dữ liệu sạch quan trọng không kém thuật toán chunking — blockquote/metadata template trong body làm nhiễu retrieval. Nhóm khác loại bỏ phần hướng dẫn trước khi nạp và dùng `RecursiveChunker` theo heading (`##`) cho kết quả ổn định hơn. Lọc `audience=student` giúp thu hẹp phạm vi nhưng vẫn cần chunk chất lượng cao mới trả lời đúng.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí                                        | Điểm tự đánh giá |
| ----------------------------------------------- | ---------------- |
| Khởi động (Warm-up)                             | 5 / 5            |
| Hướng tiếp cận của tôi (My Approach)            | 9 / 10           |
| Hoàn thiện code (Core Implementation — tests)   | 30 / 30          |
| Dự đoán độ tương tự (Similarity Predictions)    | 3 / 5            |
| Kết quả truy xuất của tôi (Competition Results) | 6 / 10           |
| **Tổng phần cá nhân**                           | **53 / 60**      |

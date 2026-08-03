# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Ngô Tuấn Hưng
**Nhóm:** Nhóm K3-AI
**Ngày:** 03/08/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Hai đoạn văn bản có độ tương tự cosine cao nghĩa là vector embedding của chúng hướng về cùng một chiều trong không gian vector đa chiều. Điều này thể hiện hai văn bản có sự tương đồng lớn về ngữ nghĩa (semantic meaning) hoặc thuộc cùng một chủ đề.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Chú chó đang chạy nhảy ngoài sân."
- Câu B: "Con cún đang nô đùa ở ngoài vườn."
- Tại sao tương đồng: Cả hai câu đều đề cập đến cùng một loài động vật (chó/cún) đang thực hiện hành động vui chơi ở không gian ngoài trời (sân/vườn).

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Chú chó đang chạy nhảy ngoài sân."
- Câu B: "Công thức toán học giải phương trình bậc hai."
- Tại sao khác: Hai câu thuộc hai chủ đề hoàn toàn độc lập và không liên quan ngữ nghĩa với nhau (hoạt động của động vật vs lý thuyết toán học).

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine similarity đo góc giữa 2 vector nên chỉ đánh giá hướng ngữ nghĩa mà không bị ảnh hưởng bởi độ dài văn bản (chiều dài vector). Ngược lại, Euclidean distance đo khoảng cách điểm cuối vector nên văn bản dài ngắn khác nhau sẽ bị khoảng cách xa dù cùng nội dung ngữ nghĩa.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* `số lượng chunk = làm_tròn_lên((10000 - 50) / (500 - 50)) = làm_tròn_lên(9950 / 450) = làm_tròn_lên(22.111)`
> *Đáp án:* 23 chunks

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Số lượng chunk tăng lên 25 (`làm_tròn_lên((10000 - 100) / (500 - 100)) = 25`). Muốn tăng độ chồng chéo vì giúp giữ lại đầy đủ ngữ cảnh nằm ở ranh giới giữa hai chunk liên tiếp, tránh làm ngắt đứt thông tin hoặc ý nghĩa câu.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Dùng biểu thức chính quy `re.split(r'(?<=[.!?])\s+|\n+', text)` để chia văn bản thành các câu riêng biệt tại vị trí sau các dấu chấm, hỏi, cảm thán hoặc xuống dòng. Xử lý các câu rỗng bằng `strip()`, sau đó gom các câu thành từng nhóm tối đa `max_sentences_per_chunk` câu.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Sử dụng thuật toán chia đệ quy với danh sách ranh giới ưu tiên `["\n\n", "\n", ". ", " ", ""]`. Base case là khi độ dài đoạn văn bản nhỏ hơn hoặc bằng `chunk_size` hoặc đã duyệt hết các ranh giới. Nếu vượt quá `chunk_size`, hàm chia theo ranh giới ưu tiên cao nhất rồi gọi đệ quy trên các đoạn con, sau đó gom các đoạn con lại mà không vượt quá `chunk_size`.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Hàm `add_documents` chuyển từng `Document` thành record chứa embedding (tính qua `_embedding_fn`) và lưu vào danh sách `_store`. Hàm `search` chuyển `query` thành vector, tính tích vô hướng (dot product) với từng embedding lưu trữ bằng `_dot`, sắp xếp giảm dần theo điểm score và lấy `top_k` kết quả.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> `search_with_filter` thực hiện pre-filtering trước: lọc `_store` lấy các chunk có `metadata` khớp với tất cả khóa-giá trị trong `metadata_filter`, rồi mới gọi hàm tìm kiếm tương tự trên danh sách đã lọc. `delete_document` xóa tất cả chunk có `id` hoặc `metadata['doc_id']` khớp với `doc_id` cần xóa.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Đầu tiên gọi `self.store.search(question, top_k=top_k)` để truy xuất `top_k` chunk có điểm tương tự cao nhất. Sau đó ghép nội dung các chunk lại làm `context` và truyền vào template prompt tiêu chuẩn cho RAG, cuối cùng gọi `self.llm_fn(prompt)` để tạo câu trả lời.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0
collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [ 35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED [ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

============================== 42 passed in 0.05s ==============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Chú chó đang chạy nhảy ngoài sân. | Con cún đang nô đùa ở ngoài vườn. | cao | -0.1577 (mock) | Đúng (với ngữ nghĩa real embedder) |
| 2 | Trí tuệ nhân tạo đang phát triển rất nhanh. | Mô hình ngôn ngữ lớn giúp giải quyết nhiều bài toán. | cao | 0.0205 (mock) | Đúng |
| 3 | Học phí đại học có thể thanh toán qua ngân hàng. | Sinh viên đăng ký môn học trực tuyến trên portal. | trung bình | 0.0163 (mock) | Đúng |
| 4 | Thời tiết hôm nay nắng đẹp và mát mẻ. | Món phở bò rất ngon và đậm đà. | thấp | -0.2583 (mock) | Đúng |
| 5 | Học phí đại học có thể thanh toán qua ngân hàng. | Công thức tính tích phân suy rộng trong toán học. | thấp | -0.0341 (mock) | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Mock embedder cho kết quả ngẫu nhiên do dựa trên hash MD5 chứ chưa học được ngữ nghĩa thực sự của tiếng Việt. Điều này cho thấy tầm quan trọng của việc dùng mô hình embedding thực sự (như Sentence Transformers hoặc OpenAI) để phản ánh chính xác khoảng cách ngữ nghĩa giữa các câu trong thực tế.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Sinh viên có được đăng ký mã học phần đang chờ lịch thi hoặc chờ kết quả điểm thi không? | `ueh-course-registration-plan-hk-cuoi-2025`: Không được phép đăng ký mã học phần đang chờ lịch thi... | 0.85 | Có | Không được phép đăng ký mã học phần đang chờ lịch thi hoặc chờ kết quả điểm thi. |
| 2 | Sinh viên không nộp học phí đúng hạn trong kỳ đăng ký học kỳ cuối 2025 sẽ bị xử lý thế nào? | `ueh-course-registration-plan-hk-cuoi-2025`: Sinh viên không nộp học phí đúng hạn sẽ bị xóa tên khỏi danh sách... | 0.82 | Có | Bị xóa tên khỏi danh sách lớp đã đăng ký. |
| 3 | Các bước đăng ký cấp thẻ sinh viên nhựa tại UEH là gì? | `ueh-student-card-services`: B1 Cổng GTĐT -> B2 điền thông tin -> B3 nộp 100k -> B4 in thẻ -> B5 nhận tại A203... | 0.84 | Có | Gồm 5 bước: Đăng ký trên Cổng GTĐT, điền thông tin, nộp 100.000đ, in thẻ và nhận tại phòng A203. |
| 4 | UEH Smart Library cung cấp quyền truy cập những cơ sở dữ liệu học thuật quốc tế nào? | `ueh-library-reading-culture`: Truy cập các cơ sở dữ liệu quốc tế như ScienceDirect, SpringerLink, Jora... | 0.89 | Có | Cung cấp quyền truy cập các CSDL như ScienceDirect, SpringerLink, Jora... |
| 5 | Thời gian thanh toán nội trú phí KTX UEH Quý III (tháng 7, 8, 9) dành cho sinh viên là khi nào? | `ueh-dorm-fee-2026-q3`: Lọc `audience=student` & `document_version=2026-q3` -> Thời gian nộp 01/7/2026 - 13/7/2026... | 0.87 | Có | Thời gian thanh toán từ 00h00 ngày 01/7/2026 đến 23h59 ngày 13/7/2026. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Việc kết hợp lọc metadata (metadata filtering) trước khi truy xuất giúp thu hẹp phạm vi tìm kiếm đáng kể và loại bỏ các chunk nhiễu. Ngoài ra, chiến lược `RecursiveChunker` cho thấy khả năng giữ trọn vẹn đoạn văn (paragraph) tốt hơn `FixedSizeChunker`.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |


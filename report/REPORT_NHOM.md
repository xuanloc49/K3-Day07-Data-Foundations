# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** DAY07 — UEH University Services
**Thành viên:** Vũ Đức Anh (`DAY07-2A202601191-VuDucAnh`), Ngô Tuấn Hưng (`DAY07-2A202601409-NgoTuanHung`), Trần Xuân Lộc (`DAY07-2A202601671-TranXuanLoc`), Đào Ngọc Bích (`DAY07-2A202601745-DaoNgocBich`)
**Ngày:** 2026-08-03

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Phạm vi bộ tài liệu (Scope)

**Chủ đề (cố định theo lớp K3):** Dịch vụ / quy định đại học (đăng ký môn, học phí, học bổng, thư viện, ký túc xá…).

**Phạm vi cụ thể nhóm tập trung:**
Dịch vụ và quy định dành cho sinh viên Đại học Kinh tế TP.HCM (UEH), bao gồm: đăng ký học phần, nội trú ký túc xá, học phí, chính sách học bổng, dịch vụ thẻ sinh viên và văn hóa đọc thư viện (nguồn công khai từ daotao.ueh.edu.vn và dsa.ueh.edu.vn).

### Danh sách tài liệu (Data Inventory)

| #   | Tên tài liệu                                                    | Nguồn (Source URL)                                                                                                                                                                | Ngày lấy / Phiên bản          | Số ký tự | Metadata đã gán                                                  |
| --- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | -------- | ---------------------------------------------------------------- |
| 1   | Quy định công tác tư vấn học tập đối với sinh viên ĐHCQ         | https://daotao.ueh.edu.vn/quy-dinh-cong-tac-tu-van-hoc-tap-doi-voi-sinh-vien-he-dai-hoc-chinh-quy/                                                                                | 2026-08-03 / 2016-10-24       | 12,993   | audience=faculty, dept=dao-tao, cat=course-registration, lang=vi |
| 2   | Thông báo hướng dẫn đăng ký học phần trực tuyến                 | https://daotao.ueh.edu.vn/thong-bao-huong-dan-dang-ky-hoc-phan-truc-tuyen-cho-sinh-vien-dhcq-ltdhcq-vb2dhcq/                                                                      | 2026-08-03 / not-stated       | 1,182    | audience=student, dept=dao-tao, cat=course-registration, lang=vi |
| 3   | Thông báo kế hoạch đăng ký học phần và nộp học phí HK cuối 2025 | https://daotao.ueh.edu.vn/thong-bao-ke-hoach-dang-ky-hoc-phan-va-nop-hoc-phi-hoc-ky-cuoi-nam-2025-doi-voi-sinh-vien-dai-hoc-chinh-quy-van-bang-2-lien-thong-dhcq-vua-lam-vua-hoc/ | 2026-08-03 / 2025-hoc-ky-cuoi | 7,137    | audience=student, dept=dao-tao, cat=course-registration, lang=vi |
| 4   | Thông báo Khung thời gian thu nội trú phí Ký túc xá năm 2025    | https://dsa.ueh.edu.vn/tin-tuc/thong-bao-khung-thoi-gian-thu-noi-tru-phi-ky-tuc-xa-ueh-nam-2025/                                                                                  | 2026-08-03 / 2025             | 1,547    | audience=student, dept=ktx, cat=dormitory, lang=vi               |
| 5   | Thông báo thu nội trú phí Ký túc xá Quý III/2026                | https://dsa.ueh.edu.vn/tin-tuc/thong-bao-ve-viec-thu-noi-tru-phi-ky-tuc-xa-quy-iii-2026-thang-789-nam-2026/                                                                       | 2026-08-03 / 2026-q3          | 1,293    | audience=student, dept=ktx, cat=dormitory, lang=vi               |
| 6   | Văn hóa đọc tại UEH: Khi tri thức trở thành “vốn liếng”         | https://dsa.ueh.edu.vn/tin-tuc/van-hoa-doc-tai-ueh-khi-tri-thuc-tro-thanh-von-lieng-cua-nhung-nha-lanh-dao-tuong-lai/                                                             | 2026-08-03 / not-stated       | 6,778    | audience=student, dept=thu-vien, cat=library, lang=vi            |
| 7   | Chính sách học bổng UEH                                         | https://dsa.ueh.edu.vn/tin-tuc/chinh-sach-hoc-bong/                                                                                                                               | 2026-08-03 / not-stated       | 12,732   | audience=student, dept=hoc-bong, cat=scholarship, lang=vi        |
| 8   | Quy định xét cấp học bổng khuyến khích học tập                  | https://daotao.ueh.edu.vn/quy-dinh-xet-cap-hoc-bong-khuyen-khich-hoc-tap-cho-sinh-vien-dai-hoc-chinh-quy/                                                                         | 2026-08-03 / not-stated       | 5,283    | audience=student, dept=hoc-bong, cat=scholarship, lang=vi        |
| 9   | THẺ SINH VIÊN – Ban Chăm sóc người học                          | https://dsa.ueh.edu.vn/chuyen-trang-ho-tro-dich-vu-tien-ich-ueh/the-sinh-vien/                                                                                                    | 2026-08-03 / not-stated       | 1,558    | audience=student, dept=dich-vu-sv, cat=student-services, lang=vi |
| 10  | Thông báo về mức học phí các hệ đào tạo năm học 2026-2027       | https://dsa.ueh.edu.vn/tin-tuc/thong-bao-ve-muc-hoc-phi-cac-he-dao-tao-nam-hoc-2026-2027-hoc-ky-cuoi-2026-hoc-ky-dau-2027-va-chinh-sach-ho-tro-hoc-phi-hoc-ky-cuoi-2026/          | 2026-08-03 / 2026-2027        | 1,076    | audience=student, dept=tai-chinh, cat=tuition, lang=vi           |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**

- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata    | Kiểu          | Ví dụ giá trị                            | Tại sao hữu ích cho truy xuất (retrieval)?                                                            |
| ------------------ | ------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `doc_id`           | string        | `ueh-dorm-fee-2026-q3`                   | Định danh duy nhất cho tài liệu, dùng để xóa/truy vết hoặc cập nhật các chunks của tài liệu.          |
| `title`            | string        | `THẺ SINH VIÊN – Ban Chăm sóc người học` | Hiển thị tên nguồn rõ ràng khi debug hoặc khi agent trả lời.                                          |
| `source_url`       | string (URL)  | `https://dsa.ueh.edu.vn/...`             | Giúp trích dẫn nguồn minh bạch (provenance) và hỗ trợ người dùng kiểm chứng thông tin.                |
| `retrieved_at`     | string (date) | `2026-08-03`                             | Theo dõi độ mới của dữ liệu thu thập.                                                                 |
| `document_version` | string        | `2026-q3`, `2016-10-24`                  | Phân biệt phiên bản quy định theo học kỳ/năm, lọc thông tin mới nhất tránh lấy dữ liệu cũ.            |
| `audience`         | string (enum) | `student`, `faculty`                     | Phân vai đối tượng áp dụng (sinh viên, cố vấn học tập / giảng viên), hỗ trợ `search_with_filter`.     |
| `department`       | string        | `ktx`, `dao-tao`, `hoc-bong`             | Lọc thông tin theo đơn vị quản lý chuyên trách (Ban Chăm sóc người học, Phòng Đào tạo...).            |
| `category`         | string        | `dormitory`, `scholarship`, `tuition`    | Giới hạn phạm vi tìm kiếm theo chủ đề nghiệp vụ, giảm bớt nhiễu từ các văn bản thuộc chuyên mục khác. |
| `language`         | string        | `vi`                                     | Phân loại ngôn ngữ tài liệu cho truy xuất tiếng Việt / tiếng Anh.                                     |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên 3 tài liệu đại diện (ngắn / trung bình / dài). **Đã bỏ front matter** bằng `parse_front_matter()` trước khi so sánh; `chunk_size=500` cho `fixed_size` và `recursive`; `SentenceChunker(max_sentences_per_chunk=3)` như trong `bench.py`.

| Tài liệu                                                                                      | Chiến lược (Strategy)            | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không?                                                     |
| --------------------------------------------------------------------------------------------- | -------------------------------- | -------------- | ----------------- | ---------------------------------------------------------------------------- |
| Kế hoạch đăng ký HK cuối 2025 (`ueh-course-registration-plan-hk-cuoi-2025`, 7.137 ký tự body) | FixedSizeChunker (`fixed_size`)  | 15             | 476               | Một phần — cắt theo ký tự, bảng lịch đăng ký có thể tách giữa dòng           |
|                                                                                               | SentenceChunker (`by_sentences`) | 15             | 474               | Khá — gom 3 câu/chunk, giữ câu trọn vẹn nhưng bullet dài vẫn gộp chung chunk |
|                                                                                               | RecursiveChunker (`recursive`)   | 20             | 360               | Tốt hơn — ưu tiên `\n\n` / `\n`, phù hợp thông báo nhiều mục                 |
| Chính sách học bổng (`ueh-scholarship-policy-overview`, 12.732 ký tự body)                    | FixedSizeChunker                 | 26             | 490               | Một phần — chunk đều nhưng dễ cắt giữa bảng điều kiện xét bổng               |
|                                                                                               | SentenceChunker                  | 20             | 634               | Khá — chunk dài hơn, giữ đoạn mô tả liền mạch; dễ trộn hai mục nếu câu ngắn  |
|                                                                                               | RecursiveChunker                 | 35             | 364               | Tốt — tách theo đoạn, chunk nhỏ hơn, dễ trúng mục cụ thể                     |
| Thẻ sinh viên (`ueh-student-card-services`, 1.558 ký tự body)                                 | FixedSizeChunker                 | 4              | 390               | Ổn — văn bản ngắn, ít mất ngữ cảnh                                           |
|                                                                                               | SentenceChunker                  | 2              | 777               | Tốt — gần như cả quy trình 5 bước nằm trong 1–2 chunk                        |
|                                                                                               | RecursiveChunker                 | 4              | 396               | Ổn — tách theo heading con, quy trình Bước 1–5 vẫn gần nhau                  |

**Nhận xét baseline:** Với thông báo/quy định UEH (nhiều mục, bảng, bullet), `recursive` thường tạo nhiều chunk hơn nhưng giữ cấu trúc đoạn tốt hơn. `by_sentences` phù hợp văn bản mô tả liền mạch (quy trình ngắn) nhưng dễ gộp nhiều ý không liên quan trên tài liệu dài.

### Chiến lược của từng thành viên

**Thành viên 1 — Vũ Đức Anh** (`DAY07-2A202601191-VuDucAnh`)

- **Loại chiến lược:** Sentence (`SentenceChunker`)
- **Mô tả & lý do chọn cho chủ đề này:** Chọn chia theo câu (tối đa 3 câu/chunk) vì nhiều thông báo UEH viết theo câu điều kiện / hậu quả / quy trình từng bước — giữ trọn câu tránh cắt giữa “Sinh viên … sẽ bị …”. Phù hợp câu hỏi dạng quy trình (#3) và điều kiện (#1–2); trade-off là tài liệu dài (học bổng) có thể gộp nhiều mục vào một chunk.
- **Tham số:** `SentenceChunker(max_sentences_per_chunk=3)` — chạy `python scripts/bench.py --chunker sentences`
- **Kết quả nạp corpus:** 135 chunk (`EMBEDDING_PROVIDER=local`, embedder `paraphrase-multilingual-MiniLM-L12-v2`)

**Thành viên 2 — Ngô Tuấn Hưng** (`DAY07-2A202601409-NgoTuanHung`)

- **Loại chiến lược:** Recursive (`RecursiveChunker`)
- **Mô tả & lý do chọn:** Thông báo UEH thường có cấu trúc đoạn/bullet rõ; `recursive` ưu tiên tách theo `\n\n`, `\n`, `. ` nên giữ mục con nguyên vẹn, chunk nhỏ hơn và dễ khớp câu hỏi cụ thể (ngoại lệ, số liệu theo quý).
- **Tham số:** `RecursiveChunker(chunk_size=500)` — chạy `python scripts/bench.py --chunker recursive`
- **Kết quả nạp corpus:** 136 chunk (cùng embedder local)

**Thành viên 3 — Trần Xuân Lộc** (`DAY07-2A202601671-TranXuanLoc`)

- **Loại chiến lược:** Custom (`HeadingChunker`)
- **Mô tả & lý do chọn:** Thiết kế chunker tùy chỉnh tách theo heading markdown (`#`–`####`) và cấu trúc quy định VN (Chương, Điều). Mỗi section thành một chunk, prefix heading cha để chunk tự chứa ngữ cảnh — phù hợp thông báo UEH có tiêu đề rõ; section dài > `max_chunk_size` thì tách tiếp theo sub-heading/đoạn.
- **Tham số:** `HeadingChunker(max_chunk_size=1500, include_parents=True)` — chạy trên nhánh `DAY07-2A202601671-TranXuanLoc`
- **Kết quả nạp corpus:** 63 chunk (ít nhất trong nhóm; top-3: 5/5, top-1: 4/5 với embedder local)
- **Code snippet:**

```python
class HeadingChunker:
    """Chia tài liệu theo heading: markdown (#/##) và pháp lý VN (Chương, Điều).

    Mỗi chunk = 1 section, kèm heading cha cho context.
    max_chunk_size=1500 đảm bảo không quá dài; section vượt giới hạn
    được split thêm theo paragraph.
    """
    _SPLIT_PATTERN = re.compile(
        r'^(?=#{1,4}\s|Chương\s+[IVXLCDM\d]|Điều\s+\d+\.)',
        re.MULTILINE | re.IGNORECASE,
    )

    def __init__(self, max_chunk_size=1500, include_parents=True): ...
    def chunk(self, text: str) -> list[str]: ...
```

**Thành viên 4 — Đào Ngọc Bích** (`DAY07-2A202601745-DaoNgocBich`)

- **Loại chiến lược:** Fixed-size (`FixedSizeChunker`)
- **Mô tả & lý do chọn:** Baseline chunk đều ~500 ký tự + overlap 50 — dễ triển khai, mật độ ổn định trên corpus đa chủ đề UEH; đồng thời phụ trách thu thập corpus và chuẩn hóa metadata/`sources.csv`.
- **Tham số:** `FixedSizeChunker(chunk_size=500, overlap=50)` — chạy `python scripts/bench.py --chunker fixed_size`
- **Kết quả nạp corpus:** 118 chunk (cùng embedder local)

### So Sánh Giữa Các Thành Viên

| Thành viên    | Chiến lược (Strategy)                          | Điểm truy xuất (/10) | Điểm mạnh                                                                        | Điểm yếu                                                                             |
| ------------- | ---------------------------------------------- | -------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Vũ Đức Anh    | SentenceChunker (`max_sentences_per_chunk=3`)  | 8/10                 | Top-3: 5/5; quy trình thẻ & thư viện top-1 tốt                                   | Câu #2 top-1 lệch sang `ueh-tuition-fee-2026-2027`; chunk dài trên tài liệu học bổng |
| Ngô Tuấn Hưng | RecursiveChunker (`chunk_size=500`)            | 9/10                 | Top-3: 5/5, top-1: 5/5; câu #1 có chunk chứa đúng câu “không được phép đăng ký…” | Nhiều chunk hơn → chi phí embed/index cao hơn                                        |
| Trần Xuân Lộc | HeadingChunker (custom, `max_chunk_size=1500`) | 8/10                 | Top-3: 5/5; chỉ 63 chunk — section gọn, có prefix heading                        | Câu #2 top-1 lệch doc học phí; cần heading rõ trong markdown crawl                   |
| Đào Ngọc Bích | FixedSizeChunker (`500/50`)                    | 8/10                 | Top-3: 5/5; câu #1 top-1 đúng doc; phụ trách corpus/metadata                     | Câu #2–3 top-1 đôi khi thiếu keyword; cắt giữa bullet/bảng                           |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**

> **RecursiveChunker** (Tuấn Hưng) cho top-1 tốt nhất (5/5). **HeadingChunker** (Lộc) đạt 5/5 top-3 với chỉ 63 chunk — mỗi chunk bám section + prefix heading, phù hợp quy định có cấu trúc. Sentence và Fixed-size (Anh, Bích) vẫn 5/5 top-3 nhưng dễ lệch top-1 ở câu học phí (#2) khi nhiều tài liệu cùng chủ đề.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng (ngoại lệ / điều kiện / quy trình / liệt kê / số liệu+filter), có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Bộ câu hỏi chung — **không đổi** sau khi thành viên đã chạy strategy. **Chạy:** `EMBEDDING_PROVIDER=local python scripts/bench.py` (query nằm trong `bench.py`).

| #   | Loại                                | Câu hỏi (Query)                                                                                                    | Câu trả lời chuẩn (Gold Answer)                                                                                                                             | Chunk / doc kỳ vọng                         |
| --- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| 1   | ngoại lệ                            | Sinh viên có được đăng ký mã học phần đang chờ lịch thi hoặc chờ kết quả điểm thi không?                           | Không được phép đăng ký mã học phần đang chờ lịch thi hoặc chờ kết quả điểm thi.                                                                            | `ueh-course-registration-plan-hk-cuoi-2025` |
| 2   | điều kiện                           | Sinh viên không nộp học phí đúng hạn trong kỳ đăng ký học kỳ cuối 2025 sẽ bị xử lý thế nào?                        | Bị xóa tên khỏi danh sách lớp đã đăng ký.                                                                                                                   | `ueh-course-registration-plan-hk-cuoi-2025` |
| 3   | quy trình                           | Các bước đăng ký cấp thẻ sinh viên nhựa tại UEH là gì?                                                             | B1 Cổng GTĐT → B2 điền thông tin → B3 thanh toán 100,000 đồng/1 thẻ → B4 CNTT in thẻ → B5 lấy thẻ A203 (chiều T3 / sáng T5).                                | `ueh-student-card-services`                 |
| 4   | liệt kê                             | UEH Smart Library cung cấp quyền truy cập những cơ sở dữ liệu học thuật quốc tế nào?                               | ScienceDirect, SpringerLink, Jora…                                                                                                                          | `ueh-library-reading-culture`               |
| 5   | số liệu + filter (audience & version) | Thời gian thanh toán nội trú phí KTX UEH Quý III (tháng 7, 8, 9) dành cho sinh viên là khi nào? | Từ 00h00 ngày 01/7/2026 đến 23h59 ngày 13/7/2026. | `ueh-dorm-fee-2026-q3` |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).
>
> Embedder: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (`EMBEDDING_PROVIDER=local`). Agent dùng demo LLM nên điểm agent chưa phản ánh đầy đủ; bảng dưới tập trung retrieval.

| #   | Câu hỏi                 | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3?  | Ghi chú                                                                                         |
| --- | ----------------------- | ------------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------- |
| 1   | ngoại lệ — chờ lịch thi | Recursive                       | Cả 3 chiến lược: **Có**          | Recursive top-1 chứa đúng câu cấm; Sentence/Fixed top-1 đúng doc nhưng chunk chưa có keyword rõ |
| 2   | trễ học phí             | Recursive                       | Cả 3: **Có** (doc đúng ở top-2+) | Sentence & Fixed: top-1 lệch `ueh-tuition-fee-2026-2027` (cùng chủ đề học phí)                  |
| 3   | quy trình thẻ nhựa      | Recursive                       | Cả 3: **Có**                     | Recursive score cao nhất (0.84); Fixed top-1 thiếu keyword B1–B5 trong preview                  |
| 4   | CSDL quốc tế            | Recursive                       | Cả 3: **Có**                     | Top-1 đều là `ueh-library-reading-culture`, score ~0.86–0.89                                    |
| 5   | KTX Quý III + filter    | Recursive / Fixed / Sentence    | Cả 3: **Có** (khi có filter)     | Bắt buộc `metadata_filter={"audience": "student", "document_version": "2026-q3"}` để loại bản 2025 và đảm bảo dành cho sinh viên |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**

> **Có**, rõ nhất ở **câu #5**: corpus có `ueh-dorm-fee-2025` và `ueh-dorm-fee-2026-q3` cùng mô tả Quý III (tháng 7–9) nhưng khác năm. Filter `document_version=2026-q3` loại bản 2025 trước khi search, top-1 luôn là thông báo 2026 với khung 01/7/2026–13/7/2026. Metadata `audience` cũng hữu ích khi corpus có bản đào tạo thư viện cho sinh viên vs giảng viên (doc #6 vs #7).

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**

> 1. **Chunk theo cấu trúc văn bản** (recursive) vượt fixed-size trên thông báo UEH nhiều mục — minh họa bằng câu #1: recursive top-1 chứa nguyên câu gold, fixed/sentence top-1 đúng doc nhưng chunk rộng hơn.
> 2. **Metadata filter là bắt buộc** khi nhiều phiên bản cùng chủ đề (KTX 2025 vs 2026-q3) — demo `search()` vs `search_with_filter()` trên câu #5.
> 3. **Mock embedder không dùng để kết luận chiến lược** — chỉ local/OpenAI mới phản ánh ngữ nghĩa tiếng Việt.

**Bài học rút ra khi so sánh trong nhóm:**

> Cùng corpus 11 tài liệu nhưng chiến lược chunk khác nhau cho mật độ và độ mạch lạc chunk khác nhau (118–136 chunk). Recursive tạo chunk nhỏ, bám đoạn → top-1 chính xác hơn trên câu điều kiện/ngoại lệ; Sentence gom câu → tốt với quy trình ngắn nhưng dễ “loãng” trên tài liệu dài. Câu hỏi về học phí (#2) là điểm yếu chung: tài liệu học phí 2026–2027 semantic gần câu hỏi nên cạnh tranh top-1.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**

> (1) Thêm metadata `academic_year` / `effective_date` rõ hơn trên mọi thông báo có phiên bản. (2) Cân nhắc chunk theo heading (custom chunker) cho tài liệu học bổng dài. (3) Chuẩn hóa tiêu đề section trong markdown crawl để recursive tách mục ổn định hơn.

**Failure case (phân tích lỗi):**

> **Câu #2** với Sentence/Fixed: top-1 là `ueh-tuition-fee-2026-2027` thay vì kế hoạch đăng ký HK 2025 — do embedding thấy “học phí” + “2025/2026” gần nhau. **Cải thiện:** filter `document_version=2025-hoc-ky-cuoi` hoặc `category=course-registration`, hoặc chunk nhỏ hơn quanh bullet “xóa tên khỏi danh sách lớp”.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí                                 | Điểm tự đánh giá |
| ---------------------------------------- | ---------------- |
| Lựa chọn tài liệu (Document Set Quality) | 9 / 10           |
| Thiết kế chiến lược (Strategy Design)    | 13 / 15          |
| Chất lượng truy xuất (Retrieval Quality) | 8 / 10           |
| Thuyết trình (Demo)                      | 4 / 5            |
| **Tổng phần nhóm**                       | **34 / 40**      |
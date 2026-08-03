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

| Thành viên | Chiến lược (Strategy) | Số chunk | Điểm truy xuất (top-3) | Điểm mạnh | Điểm yếu |
|-----------|----------|------|----------------------|-----------|----------|
| Vũ Đức Anh (TV1) | SentenceChunker (`max_sentences_per_chunk=3`) | 75 | 5/5 (real) / 0/5 (mock) | Giữ câu trọn vẹn; quy trình ngắn gom tốt; câu điều kiện–hậu quả không bị cắt | Tài liệu dài dễ gộp nhiều ý không liên quan; chunk dài không đều |
| Trần Xuân Lộc (TV2) | HeadingChunker (`max_chunk_size=1500, include_parents=True`) | 63 | 2/5 (mock) / 5/5 kỳ vọng (real) | Chunk = 1 Điều/section hoàn chỉnh, có heading context; ít chunk nhất → ít nhiễu | Tài liệu không có heading thành 1 chunk lớn; chunk dài hơn trung bình |
| Ngô Tuấn Hưng (TV3) | RecursiveChunker (`chunk_size=500`) | 88 | 4/5 (real) | Tự động hạ cấp phân tách linh hoạt; giữ được khối đoạn; phổ quát cho mọi loại tài liệu | Chunk nhỏ hơn, có thể ngắt ngữ cảnh giữa các đoạn dài; không nhận biết heading |
| Đào Ngọc Bích (TV4) | FixedSizeChunker (`chunk_size=500, overlap=50`) | 118 | 2/5 (mock) | Đơn giản, nhanh, dễ implement; overlap giảm mất thông tin tại biên; baseline tốt để so sánh | Không tôn trọng ranh giới ngữ nghĩa; dễ cắt giữa bảng/Điều; nhiều chunk nhất → nhiều nhiễu |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> Với bộ tài liệu dịch vụ và quy định đại học UEH, **HeadingChunker** (cho tài liệu có cấu trúc pháp lý Chương/Điều) kết hợp **SentenceChunker** (cho thông báo quy trình ngắn) là các chiến lược hiệu quả nhất. **RecursiveChunker** là giải pháp tổng quát linh hoạt (4/5 real). **FixedSizeChunker** tuy đơn giản nhưng phù hợp làm baseline — kết quả kém hơn trên tài liệu quy định vì cắt giữa ranh giới ngữ nghĩa.
>
> Nhận xét chung: Không có một chiến lược chunking duy nhất tối ưu cho mọi loại tài liệu — cần lựa chọn dựa trên cấu trúc cụ thể:
> - **Tài liệu pháp lý (Chương/Điều):** HeadingChunker vượt trội
> - **Thông báo quy trình (bước 1–5):** SentenceChunker giữ trọn vẹn nhất
> - **Văn bản hỗn hợp/tự do:** RecursiveChunker linh hoạt nhất
> - **Baseline/so sánh:** FixedSizeChunker đơn giản, dự đoán được

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng (ngoại lệ / điều kiện / quy trình / điều kiện+filter audience / số liệu+filter version), có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Bộ câu hỏi chung — **không đổi** sau khi thành viên đã chạy strategy. **Chạy:** `python bench.py` (query nằm trong `bench.py`).

| # | Loại | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk / doc kỳ vọng |
|---|------|-------|-------------------------------|--------------------------| 
| 1 | ngoại lệ | Sinh viên có được đăng ký mã học phần đang chờ lịch thi hoặc chờ kết quả điểm thi không? | Không được phép đăng ký mã học phần đang chờ lịch thi hoặc chờ kết quả điểm thi. | `ueh-course-registration-plan-hk-cuoi-2025` |
| 2 | điều kiện | Sinh viên không nộp học phí đúng hạn trong kỳ đăng ký học kỳ cuối 2025 sẽ bị xử lý thế nào? | Bị xóa tên khỏi danh sách lớp đã đăng ký. | `ueh-course-registration-plan-hk-cuoi-2025` |
| 3 | quy trình | Các bước đăng ký cấp thẻ sinh viên nhựa tại UEH là gì? | B1 Cổng GTĐT → B2 điền thông tin → B3 thanh toán 100,000 đồng/1 thẻ → B4 CNTT in thẻ → B5 lấy thẻ A203 (chiều T3 / sáng T5). | `ueh-student-card-services` |
| 4 | điều kiện + filter `audience=student` | Điều kiện để sinh viên UEH được xét cấp học bổng khuyến khích học tập là gì? | Đang trong thời gian 8 học kỳ chính; kết quả học tập và rèn luyện từ loại khá trở lên; không bị kỷ luật từ mức khiển trách trở lên; đạt từ 5 điểm trở lên tất cả học phần; số tín chỉ đăng ký >= số tín chỉ theo kế hoạch đào tạo. Không lọc `audience` dễ lấy nhầm tài liệu `ueh-academic-advising-regulation` (audience=faculty) vì cũng nhắc đến "đánh giá kết quả rèn luyện", "khen thưởng – kỷ luật". | `ueh-scholarship-regulation` |
| 5 | số liệu + filter `document_version=2026-q3` | Thời gian thanh toán nội trú phí KTX UEH Quý III (tháng 7, 8, 9) là khi nào? | Từ 00h00 ngày 01/7/2026 đến 23h59 ngày 13/7/2026. Không lọc dễ lẫn bản 2025: 01/7/2025–13/7/2025. | `ueh-dorm-fee-2026-q3` |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------| 
| 1 | ngoại lệ — chờ lịch thi | HeadingChunker / SentenceChunker | **Có** (Top-1, score 0.85) | Trích xuất chính xác quy định đăng ký HK cuối 2025 |
| 2 | trễ học phí | HeadingChunker / SentenceChunker | **Có** (Top-1, score 0.82) | Trích xuất chính xác chế tài xóa tên khỏi danh sách lớp |
| 3 | quy trình thẻ nhựa | SentenceChunker | **Có** (Top-1, score 0.88) | Giữ trọn vẹn quy trình 5 bước cấp lại thẻ sinh viên |
| 4 | điều kiện học bổng + filter `audience=student` | SentenceChunker / HeadingChunker | **Có** (Top-1, score 0.83) | Filter `audience=student` loại bỏ doc faculty (quy định tư vấn) vốn cũng nhắc đến "rèn luyện", "kỷ luật" |
| 5 | thời gian KTX + filter `document_version=2026-q3` | SentenceChunker + Filter `document_version=2026-q3` | **Có** (Top-1, score 0.81) | Filter giúp loại trừ bản 2025, lấy chính xác mốc 01/7/2026 |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> Metadata filtering hiệu quả ở **hai câu hỏi**:
> - **Câu #4 (`audience=student`):** Corpus chứa `ueh-academic-advising-regulation` (audience=faculty) — dù dành cho giảng viên/cố vấn, tài liệu này cũng nhắc đến "đánh giá kết quả rèn luyện", "khen thưởng – kỷ luật" gần nghĩa với điều kiện xét học bổng. Filter `audience=student` loại bỏ tài liệu faculty, đảm bảo chỉ truy xuất `ueh-scholarship-regulation` (student).
> - **Câu #5 (`document_version=2026-q3`):** Corpus chứa cả `ueh-dorm-fee-2025` và `ueh-dorm-fee-2026-q3` cùng đề cập đến phí KTX Quý III (tháng 7, 8, 9). Filter giúp lọc chính xác tài liệu năm 2026 thay vì bị lẫn bản 2025.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> 1. **Tầm quan trọng của Metadata Filtering:** Metadata filter phát huy hiệu quả ở hai trường hợp: (a) filter `audience=student` giúp loại bỏ tài liệu dành cho giảng viên/cố vấn (`ueh-academic-advising-regulation`) khi hỏi về điều kiện học bổng — dù tài liệu faculty cũng nhắc đến "rèn luyện", "kỷ luật" gần nghĩa; (b) filter `document_version=2026-q3` giúp phân biệt thông báo KTX 2025 vs 2026 cùng chủ đề Quý III.
> 2. **Sự phù hợp của từng loại Chunker:** `SentenceChunker` vượt trội khi xử lý câu hỏi quy trình ngắn; `HeadingChunker` thích hợp nhất cho tài liệu pháp lý/quy định học vụ có tiêu đề rõ ràng; `RecursiveChunker` là giải pháp tổng quát linh hoạt; `FixedSizeChunker` phù hợp làm baseline đối chứng, cho thấy rõ tầm quan trọng của việc tôn trọng ranh giới ngữ nghĩa khi chunking.
> 3. **Ảnh hưởng của Embedder:** Mock Embedder (dựa trên MD5) chỉ dùng phục vụ kiểm thử luồng chạy code; khi chuyển sang Real/Local Embedder (như SentenceTransformers), khả năng định vị khoảng cách ngữ nghĩa mới phát huy hiệu quả thực tế.
> 4. **So sánh 4 chiến lược — hình ảnh toàn cảnh:** FixedSize (118 chunk) → Recursive (88 chunk) → Sentence (75 chunk) → Heading (63 chunk). Càng tôn trọng cấu trúc tự nhiên, càng ít chunk nhưng mỗi chunk có chất lượng ngữ nghĩa cao hơn, giảm nhiễu khi retrieval.

**Bài học rút ra khi so sánh trong nhóm:**
> So sánh giữa 4 thành viên giúp nhóm nhận ra: (1) không có một phương pháp chunking đơn lẻ nào tối ưu cho toàn bộ corpus đại học; (2) FixedSizeChunker tuy đơn giản nhưng cho thấy rõ "baseline effect" — kết quả retrieval cải thiện đáng kể khi chuyển sang chiến lược tôn trọng ngữ cảnh (Sentence, Recursive, Heading); (3) việc lựa chọn chiến lược chia nhỏ cần linh hoạt dựa trên cấu trúc tự nhiên của từng nhóm tài liệu (văn bản quy định vs thông báo quy trình vs bài viết tự do).

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ áp dụng chiến lược **Hybrid Chunking** — tự động phát hiện cấu trúc tài liệu và chọn chunker phù hợp: HeadingChunker cho tài liệu quy định (có Chương/Điều), SentenceChunker cho thông báo quy trình ngắn, và RecursiveChunker cho văn bản tự do. Đồng thời chuẩn hóa và tự động hóa quy trình gán metadata ngay từ bước thu thập dữ liệu (data ingestion) để nâng cao độ chính xác khi truy xuất. Ngoài ra, sẽ tận dụng nhiều trường metadata filter hơn — `audience` (student/faculty), `category`, `document_version` — cho nhiều câu hỏi hơn để thu hẹp search space hiệu quả.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |

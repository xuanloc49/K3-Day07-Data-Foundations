# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** [Tên nhóm]
**Thành viên:** [Họ tên từng thành viên]
**Ngày:** [Ngày nộp]

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Phạm vi bộ tài liệu (Scope)

**Chủ đề (cố định theo lớp K3):** Dịch vụ / quy định đại học (đăng ký môn, học phí, học bổng, thư viện, ký túc xá…).

**Phạm vi cụ thể nhóm tập trung:**
Dịch vụ và quy định dành cho sinh viên Đại học Kinh tế TP.HCM (UEH), bao gồm: đăng ký học phần, nội trú ký túc xá, học phí, chính sách học bổng, dịch vụ thẻ sinh viên và văn hóa đọc thư viện.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Quy định công tác tư vấn học tập đối với sinh viên ĐHCQ | https://daotao.ueh.edu.vn/quy-dinh-cong-tac-tu-van-hoc-tap-doi-voi-sinh-vien-he-dai-hoc-chinh-quy/ | 2026-08-03 / 2016-10-24 | 12993 | audience=faculty, dept=dao-tao, cat=course-registration, lang=vi |
| 2 | Thông báo hướng dẫn đăng ký học phần trực tuyến | https://daotao.ueh.edu.vn/thong-bao-huong-dan-dang-ky-hoc-phan-truc-tuyen-cho-sinh-vien-dhcq-ltdhcq-vb2dhcq/ | 2026-08-03 / not-stated | 1182 | audience=student, dept=dao-tao, cat=course-registration, lang=vi |
| 3 | Thông báo kế hoạch đăng ký học phần và nộp học phí HK cuối 2025 | https://daotao.ueh.edu.vn/thong-bao-ke-hoach-dang-ky-hoc-phan-va-nop-hoc-phi-hoc-ky-cuoi-nam-2025-doi-voi-sinh-vien-dai-hoc-chinh-quy-van-bang-2-lien-thong-dhcq-vua-lam-vua-hoc/ | 2026-08-03 / 2025-hoc-ky-cuoi | 7137 | audience=student, dept=dao-tao, cat=course-registration, lang=vi |
| 4 | Thông báo Khung thời gian thu nội trú phí Ký túc xá năm 2025 | https://dsa.ueh.edu.vn/tin-tuc/thong-bao-khung-thoi-gian-thu-noi-tru-phi-ky-tuc-xa-ueh-nam-2025/ | 2026-08-03 / 2025 | 1547 | audience=student, dept=ktx, cat=dormitory, lang=vi |
| 5 | Thông báo thu nội trú phí Ký túc xá Quý III/2026 | https://dsa.ueh.edu.vn/tin-tuc/thong-bao-ve-viec-thu-noi-tru-phi-ky-tuc-xa-quy-iii-2026-thang-789-nam-2026/ | 2026-08-03 / 2026-q3 | 1293 | audience=student, dept=ktx, cat=dormitory, lang=vi |
| 6 | Văn hóa đọc tại UEH: Khi tri thức trở thành “vốn liếng” | https://dsa.ueh.edu.vn/tin-tuc/van-hoa-doc-tai-ueh-khi-tri-thuc-tro-thanh-von-lieng-cua-nhung-nha-lanh-dao-tuong-lai/ | 2026-08-03 / not-stated | 6778 | audience=student, dept=thu-vien, cat=library, lang=vi |
| 7 | Chính sách học bổng UEH | https://dsa.ueh.edu.vn/tin-tuc/chinh-sach-hoc-bong/ | 2026-08-03 / not-stated | 12732 | audience=student, dept=hoc-bong, cat=scholarship, lang=vi |
| 8 | Quy định xét cấp học bổng khuyến khích học tập | https://daotao.ueh.edu.vn/quy-dinh-xet-cap-hoc-bong-khuyen-khich-hoc-tap-cho-sinh-vien-dai-hoc-chinh-quy/ | 2026-08-03 / not-stated | 5283 | audience=student, dept=hoc-bong, cat=scholarship, lang=vi |
| 9 | THẺ SINH VIÊN – Ban Chăm sóc người học | https://dsa.ueh.edu.vn/chuyen-trang-ho-tro-dich-vu-tien-ich-ueh/the-sinh-vien/ | 2026-08-03 / not-stated | 1558 | audience=student, dept=dich-vu-sv, cat=student-services, lang=vi |
| 10 | Thông báo về mức học phí các hệ đào tạo năm học 2026-2027 | https://dsa.ueh.edu.vn/tin-tuc/thong-bao-ve-muc-hoc-phi-cac-he-dao-tao-nam-hoc-2026-2027-hoc-ky-cuoi-2026-hoc-ky-dau-2027-va-chinh-sach-ho-tro-hoc-phi-hoc-ky-cuoi-2026/ | 2026-08-03 / 2026-2027 | 1076 | audience=student, dept=tai-chinh, cat=tuition, lang=vi |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | string | `ueh-dorm-fee-2026-q3` | Định danh duy nhất cho tài liệu, dùng để xóa/truy vết hoặc cập nhật các chunks của tài liệu. |
| `source_url` | string | `https://dsa.ueh.edu.vn/...` | Giúp trích dẫn nguồn minh bạch (provenance) và hỗ trợ người dùng kiểm chứng thông tin. |
| `retrieved_at` | string | `2026-08-03` | Theo dõi độ mới của dữ liệu thu thập. |
| `document_version` | string | `2026-q3`, `2016-10-24` | Phân biệt phiên bản quy định theo học kỳ/năm, lọc thông tin mới nhất tránh lấy dữ liệu cũ. |
| `audience` | string | `student`, `faculty` | Phân vai đối tượng áp dụng (sinh viên, cố vấn học tập / giảng viên). |
| `department` | string | `ktx`, `dao-tao`, `hoc-bong` | Lọc thông tin theo đơn vị quản lý chuyên trách (Ban Chăm sóc người học, Phòng Đào tạo...). |
| `category` | string | `dormitory`, `scholarship`, `tuition` | Giới hạn phạm vi tìm kiếm theo chủ đề nghiệp vụ, giảm bớt nhiễu từ các văn bản thuộc chuyên mục khác. |
| `language` | string | `vi` | Phân loại ngôn ngữ tài liệu cho truy xuất tiếng Việt / tiếng Anh. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| | FixedSizeChunker (`fixed_size`) | | | |
| | SentenceChunker (`by_sentences`) | | | |
| | RecursiveChunker (`recursive`) | | | |

### Chiến lược của từng thành viên

> Mỗi thành viên điền một khối dưới đây (copy thêm nếu nhóm có nhiều hơn 3 người).

**Thành viên 1 — [Tên]**
- **Loại chiến lược:** [FixedSize / Sentence / Recursive / custom]
- **Mô tả & lý do chọn cho chủ đề này:** *(2-3 câu)*
- **Code snippet (nếu custom):**
```python
# Dán mã nguồn (implementation) vào đây
```

**Thành viên 2 — [Tên]**
- **Loại chiến lược:**
- **Mô tả & lý do chọn:**
- **Code snippet (nếu custom):**

**Thành viên 3 — [Tên]**
- **Loại chiến lược:**
- **Mô tả & lý do chọn:**
- **Code snippet (nếu custom):**

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| | | | | |
| | | | | |
| | | | | |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> *Viết 2-3 câu — đây là phần được đánh giá cao nhất (khả năng suy nghĩ & giải thích):*

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> *Viết 2-3 câu:*

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> *Liệt kê 2-3 ý:*

**Bài học rút ra khi so sánh trong nhóm:**
> *Viết 2-3 câu — cùng tài liệu nhưng chiến lược khác nhau dẫn tới khác biệt gì?*

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | / 10 |
| Thiết kế chiến lược (Strategy Design) | / 15 |
| Chất lượng truy xuất (Retrieval Quality) | / 10 |
| Thuyết trình (Demo) | / 5 |
| **Tổng phần nhóm** | **/ 40** |

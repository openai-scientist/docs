# Ánh xạ ID cũ → ID v3.0

Tệp này giúp tra ID cũ, ví dụ ID trong Report 7, sang ID v3.0. ID cũ đã bỏ không bao giờ được dùng lại. Từ v3.0 mọi ID là vĩnh viễn ([README §4](README.md)).

## Ánh xạ BRD

### Business problem

| ID cũ | ID mới | Ghi chú |
|---|---|---|
| BP-01 | BP-01 | Đổi lời. |
| BP-02 | BP-02 | Thêm SESOI, ngưỡng hiệu ứng. |
| BP-03 | BP-03 | Giữ. |
| BP-04 | BP-04 | Giữ. |
| BP-05 | BP-05 | Thêm chất lượng dữ liệu. |
| BP-06 | BP-06 | Bỏ phân loại cấu trúc; chia theo power. |
| BP-07 | BP-07 | Mở rộng sang p-hacking. |
| BP-08 | BP-08 | Giữ. |
| BP-09 | BP-09 | Giữ. |
| BP-10 | BP-10 | Giữ. |
| BP-11 | BP-11 | Giữ; JFE là Could. |
| BP-12 | BP-12 | Thêm con số không do code. |
| — | BP-13..BP-16 | Mới: hàng dữ liệu rời máy, run treo, kiểm soát toàn run quá thô, export chưa duyệt. |

### Business objective

| ID cũ | ID mới | Ghi chú |
|---|---|---|
| BO-01 | BO-01 | Giữ. |
| BO-02 | BO-02 | Thêm replay. |
| BO-03 | BO-03 | Nhánh `explore` bỏ; thay bằng release gate. |
| BO-04 | BO-04 | Thay "split policy tabular" bằng split theo power, Lock, envelope, tier. |
| BO-05 | BO-05 | Gate và PI escalation thay bằng preset, pinned, presence. |
| BO-06 | BO-06 | Giữ; thêm budget theo tháng. |
| BO-07 | BO-07 | Giữ. |
| BO-08 | BO-09 | Benchmark và seeded-flaw; bỏ so sánh AutoML và generic agent. |
| BO-09 | BO-12 | JFE, Could. |
| BO-10 | BO-10 | Giữ. |
| — | BO-08, BO-11 | Mới: run luôn kết thúc; export chỉ khi Dossier đã duyệt. |

### Business rule cũ (BR-01..BR-61)

| ID cũ | ID mới | Ghi chú |
|---|---|---|
| BR-01 | BR-01, BR-103 | Google sign-in là rule riêng (BR-103); chi tiết cấu hình thuộc implementation. |
| BR-02 | BR-02 | Bỏ mã HTTP. |
| BR-03 | BR-03 | |
| BR-04 | BR-04 | Bỏ giá trị mặc định (setting). |
| BR-05 | BR-05 | Webhook, SSE: chi tiết kỹ thuật, không ghi. |
| BR-06 | BR-07 | |
| BR-07 | Deprecated | Phân loại intent (`test`, `compare`, `explain`, `explore_dataset`) bỏ; research case không có intent kind. |
| BR-08 | Deprecated | Giới hạn độ dài là setting; trường hợp không có dataset do dataset stage xử lý (BR-08). |
| BR-09 | BR-07 | Giới hạn số lượng là setting. |
| BR-10 | BR-10 | Phần PI charter bỏ. |
| BR-11 | BR-10 | |
| BR-12 | BR-08 | Pipeline `default` Deprecated: thay bằng `dataset_first`. |
| BR-13 | BR-16 | |
| BR-14 | Deprecated | Danh sách định dạng và giới hạn kích thước là setting. |
| BR-15 | BR-17 | |
| BR-16 | BR-43 | Data card thay bằng DatasetSnapshot. |
| BR-17 | BR-22 | Nhánh `explore` bỏ; thay bằng BR-19. |
| BR-18 | BR-44 | `random_rows` thay bằng split theo power. |
| BR-19 | BR-28 | Gate thay bằng decision inbox. |
| BR-20 | BR-76 | Phân loại cấu trúc dữ liệu gộp vào BR-76. |
| BR-21 | BR-76, BR-43 | Unit và leakage risk nằm trong DatasetSnapshot. |
| BR-22 | BR-76, BR-44 | Split theo cấu trúc (BR-76); số phần theo power (BR-44). |
| BR-23 | BR-49 | Confirmatory chỉ mở qua envelope và unseal. |
| BR-24 | BR-47 | Protocol freeze thay bằng Lock. |
| BR-25 | BR-76 | Cấu trúc đặc biệt gộp vào BR-76. |
| BR-26 | BR-29 | Decision log ghi quyết định. |
| BR-27 | BR-42, BR-45 | |
| BR-28 | BR-42 | |
| BR-29 | BR-45 | |
| BR-30 | BR-28 | Review shortlist qua decision inbox; thiếu provider là lỗi thuộc message catalogue. |
| BR-31 | BR-46 | |
| BR-32 | BR-46 | |
| BR-33 | BR-46 | Validator thành contract check của AnalysisPlan. |
| BR-34 | BR-35, BR-47 | |
| BR-35 | BR-56 | |
| BR-36 | BR-08, BR-09, BR-13 | Gate, send back, rerun: Deprecated (glossary §11). |
| BR-37 | BR-24, BR-30 | Mode `light`/`auto` thay bằng preset và presence. |
| BR-38 | BR-27, BR-75 | Phần ghi giả định chuyển sang BR-75. |
| BR-39 | BR-14 | Pause, stop, abandon: Deprecated; thay bằng huỷ run (BR-77). |
| BR-40 | BR-31 | Charter, close, obligation: Deprecated; AI PI không kết thúc run. |
| BR-41 | BR-58, BR-61 | Giá trị mặc định là setting. |
| BR-42 | BR-23 | |
| BR-43 | BR-50 | |
| BR-44 | BR-57 | |
| BR-45 | BR-54, BR-55 | |
| BR-46 | BR-62, BR-63, BR-64 | |
| BR-47..BR-53 | BR-74 | JFE gộp thành một rule Could. |
| BR-54 | BR-66, BR-69 | |
| BR-55 | BR-66, BR-67 | |
| BR-56 | Deprecated | Tranh biện Toulmin/AIF thay bằng review loop (BR-35) với persona Skeptic và Reviewer 2. |
| BR-57 | Deprecated | Như BR-56 (ASPIC+). |
| BR-58 | BR-67 | |
| BR-59 | BR-74 | |
| BR-60 | BR-35, BR-66..BR-69 | |
| BR-61 | BR-64, BR-73 | |

### Rule cũ RULE-01..RULE-13 (mục 12 của v2.2)

| ID cũ | ID mới | Ghi chú |
|---|---|---|
| RULE-01 | BR-07, BR-10 | |
| RULE-02 | BR-16 | |
| RULE-03 | Deprecated | Gắn với `random_rows`; thay bằng BR-44. |
| RULE-04 | BR-41 | |
| RULE-05 | BR-42 | |
| RULE-06 | BR-38, BR-39 | Acceptance là action riêng (BR-25). |
| RULE-07 | BR-11 | |
| RULE-08 | BR-22 | |
| RULE-09 | Deprecated | Là rule về trạng thái triển khai; ngoài phạm vi tài liệu. |
| RULE-10 | Deprecated | Phân chia Platform và engine thuộc architecture. |
| RULE-11 | Deprecated | JFE là Could; xem BR-74. |
| RULE-12 | BR-56, BR-67 | |
| RULE-13 | BR-12 | |

## Ánh xạ PRD

### NFR cũ (PRD v2.2)

| ID cũ | ID mới | Ghi chú |
|---|---|---|
| NFR-01 | NFR-08, NFR-09 | Bỏ chi tiết kỹ thuật (session, CSRF, CORS, rate limit). |
| NFR-02 | NFR-12, NFR-14 | Nhánh `explore` bỏ; thay bằng release gate. |
| NFR-03 | Deprecated | Mô tả trạng thái triển khai ("current"). Thay bằng FR của execution stage. |
| NFR-04 | Deprecated | Mô tả roadmap ("next"). Thay bằng FR-41, FR-51, FR-53. |
| NFR-05 | NFR-26, NFR-25 | |
| NFR-06 | NFR-03, NFR-04 | |
| NFR-07 | NFR-01, NFR-02 | |
| NFR-08 | NFR-16 | |
| NFR-09 | NFR-20 | |
| NFR-10 | FR-106 | Quyền sử dụng nguồn thuộc JFE (Could). |
| NFR-11 | NFR-27, NFR-28, NFR-29 | |
| NFR-12 | Deprecated | Mô tả màn hình review. Nội dung duyệt thuộc FR-95, FR-99; màn hình thuộc Report III. |

### FE-16 cũ

| ID cũ | ID mới | Ghi chú |
|---|---|---|
| FE-16 | Deprecated | Không còn là feature riêng. Thay bằng execution stage FE-09 (FR-50, FR-51, FR-52, FR-54, FR-55, FR-57, FR-59) và split ở FE-06 (FR-40, FR-41, FR-42). Không dùng lại ID FE-16. |
| PR-33..PR-37 (planned) | Deprecated | Gộp vào FE-06 và FE-09. |

### FE-01..FE-15 của báo cáo capstone trước

| ID cũ | Tên cũ | ID mới | Ghi chú |
|---|---|---|---|
| FE-01 | Authentication and role-based access | FE-01 | |
| FE-02 | Project workspace management | FE-02 | |
| FE-03 | Dataset upload and validation | FE-03 | |
| FE-04 | Dataset profiling and Data Card | FE-06 | Data Card thay bằng DatasetSnapshot. |
| FE-05 | Data quality, cleaning, and versioning | FE-06, FE-03 | Chất lượng và cleaning ở FE-06; version ở FE-03. |
| FE-06 | Research question and hypothesis management | FE-04, FE-07 | Research case ở FE-04; hypothesis ở FE-07. |
| FE-07 | Research State and candidate directions | Deprecated | Research State là tên đã bỏ (glossary §11). Candidate thuộc FE-09 và decision inbox FE-05. |
| FE-08 | Ideation quality and structured gates | FE-11, FE-05 | Gate thay bằng decision inbox; chất lượng ý tưởng do review loop. |
| FE-09 | Experiment planning and Research Protocol | FE-08 | Protocol freeze thay bằng Lock. |
| FE-10 | Assumption checking and registered-capability execution | FE-09 | |
| FE-11 | Result validation and deterministic outcome management | FE-09 | Verdict do code. |
| FE-12 | Artifact-centered provenance, reproducibility, and reporting | FE-04, FE-09, FE-10, FE-14 | Hand-off object, replication, PaperPack, Dossier. |
| FE-13 | Evaluation, autonomy, and decision quality | FE-05, FE-11, FE-17 | Decision log, overturn, seeded-flaw bench, metric vận hành. |
| FE-14 | Knowledge, simulation, theory, campaign, and manuscript support | FE-07, FE-10 | Knowledge ở FE-07; manuscript ở FE-10. Simulation, theory, campaign: Deprecated (không có BR trong BRD v3.0). |
| FE-15 | Bounded tied-candidate confirmation batch | FE-09 | Candidate và confirmation tier (FR-57, FR-59); không còn feature riêng. |

### SRS cũ: feature F1–F7

| Feature cũ | ID mới | Ghi chú |
|---|---|---|
| F1 Research workspace khớp backend | FE-04, FE-05 | Mô tả màn hình thuộc Report III. |
| F2 Structure-aware data design | FE-06 | |
| F3 Independent model review có chọn lọc | FE-11 | Review chọn lọc Deprecated; review bắt buộc. |
| F4 Results review và dossier | FE-09, FE-14 | |
| F5 JFE | FE-18 | Could, sau MVP. |
| F6 Writing AIF trên stage `paper` | FE-10 | Writing AIF thay bằng paper stage. |
| F7 Evaluation và benchmark | §11.2 | Bench trong §11; so sánh human-only, AutoML, generic agent bỏ. |

### SRS cũ: SR-*

"Dropped" nghĩa là không có BR đỡ ở BRD v3.0, hoặc là chi tiết kỹ thuật, màn hình hay system rule thuộc Report III hoặc IV.

| ID cũ | ID mới | Ghi chú |
|---|---|---|
| SR-F1-01 | FR-13 | Tên field và giới hạn là system rule của Report III. `review_mode` và `interaction_mode`: Deprecated (thay bằng FR-25). |
| SR-F1-02 | Dropped | Rule form theo schema là system rule của Report III. |
| SR-F1-03 | FR-17 | |
| SR-F1-04 | FR-15 | Danh sách candidate dataset public: Dropped ở mức màn hình. Dataset public nay trong phạm vi (BR-08). |
| SR-F1-05 | FR-87 | Runner thành Local Node. |
| SR-F1-06 | FR-12 | |
| SR-F1-07 | FR-29 | Loại item theo BR-28. |
| SR-F1-08 | FR-31, FR-30 | Route trả lời: Dropped. |
| SR-F1-09 | Dropped | Mức màn hình; thuộc Report III và VI. |
| SR-F1-10 | NFR-16 | |
| SR-F1-11 | FR-35 | Directive và endorse: Dropped (không có BR). |
| SR-F1-12 | NFR-26 | Replay thành NFR. Export RO-Crate: Dropped (không có BR). |
| SR-F1-13 | Dropped | Chi tiết UI. |
| SR-F1-14 | Dropped | Kỹ thuật kiểm thử front end. |
| SR-F1-15 | Dropped | Message catalogue ở Report III (README §2). |
| SR-F2-01 | FR-40 | Phân loại năm loại cấu trúc và mức tin cậy: Dropped (BR-76 chỉ nêu group, thời gian, panel). |
| SR-F2-02 | FR-40 | Xác nhận cấu trúc là action pinned (BR-26, BR-76). Timing của biến và item `structure` ở `needs_you`: Dropped (chi tiết màn hình và field). |
| SR-F2-03 | FR-41 | Tên policy: Dropped. |
| SR-F2-04 | Dropped | Version digest là chi tiết kỹ thuật. |
| SR-F2-05 | Dropped | Chặn split khi cấu trúc `special` không có BR. |
| SR-F2-06 | Dropped | Phát hiện rò rỉ theo thời gian không có BR. |
| SR-F2-07 | FR-46 | Thành design diagnosis của AnalysisPlan. |
| SR-F2-08 | FR-37 | Manifest thành DatasetSnapshot. |
| SR-F2-09 | FR-30, FR-56 | |
| SR-F2-10 | Dropped | Không có BR cho analysis family dạng predictive. |
| SR-F2-11 | Dropped | Tương thích runner là chi tiết kỹ thuật (architecture). |
| SR-F3-01 | Deprecated | Review chọn lọc thay bằng review bắt buộc FR-71. |
| SR-F3-02 | FR-73, FR-74, FR-75 | |
| SR-F3-03 | FR-101 | |
| SR-F3-04 | FR-93 | |
| SR-F4-01 | FR-94 | |
| SR-F4-02 | FR-94, FR-60 | |
| SR-F4-03 | FR-54 | |
| SR-F4-04 | FR-55 | |
| SR-F4-05 | FR-54, FR-99 | Verdict, số, grade, ceiling do code; ghi chú của researcher là comment. |
| SR-F4-06 | FR-95 | |
| SR-F4-07 | FR-96 | |
| SR-F4-08 | FR-97 | Định dạng xuất theo review settings. |
| SR-F4-09 | Dropped | Dossier plan-only: không có Dossier khi chưa có PaperPack accepted (BR-62). |
| SR-F5-01 | FR-106 | Gợi ý tạp chí: Dropped. |
| SR-F5-02 | FR-106 | |
| SR-F5-03 | FR-106 | |
| SR-F5-04 | FR-107 | |
| SR-F5-05 | FR-107 | |
| SR-F5-06 | Dropped | Độ đồng thuận annotation không có BR. |
| SR-F5-07 | FR-106 | |
| SR-F5-08 | FR-108 | |
| SR-F5-09 | Dropped | Standalone run bỏ (ADR-13). |
| SR-F5-10 | FR-107 | |
| SR-F6-01 | FR-62 | |
| SR-F6-02 | Deprecated | Evidence ledger và statement theo Writing AIF; thay bằng contract PaperPack FR-64. |
| SR-F6-03 | Deprecated | Tranh biện và AIF graph bỏ (BR-56 cũ của BRD). |
| SR-F6-04 | Deprecated | ASPIC+ bỏ. Mức claim theo claim ceiling FR-64. |
| SR-F6-05 | Deprecated | Freeze claim set bỏ; claims theo contract. |
| SR-F6-06 | FR-108 | Publisher rules: Dropped. JFE là Could. |
| SR-F6-07 | FR-63 | |
| SR-F6-08 | FR-64, FR-65, FR-71 | |
| SR-F6-09 | FR-97 | |
| SR-F6-10 | FR-70 | |
| SR-F7-01 | Dropped | Bench structure detection không nằm trong §11.2. |
| SR-F7-02 | FR-77 | Seeded-flaw bench. |
| SR-F7-03 | Deprecated | So sánh human-only, AutoML, generic agent bỏ. |
| SR-F7-04 | Dropped | Thuộc §11.2 (paper reproduction bench) và SM-16. |

### PR-* cũ (PRD v2.2) và mục tiêu, nguyên tắc cũ

| ID cũ | ID mới | Ghi chú |
|---|---|---|
| PR-01 | FR-01 | |
| PR-02 | FR-04, FR-06 | |
| PR-03 | FR-05 | |
| PR-04 | FR-99, FR-100 | SSE và webhook là chi tiết kỹ thuật. |
| PR-05 | FR-07, FR-104 | |
| PR-06 | FR-09 | |
| PR-07, PR-08 | Dropped | Định dạng và giới hạn kích thước là system rule của Report III. |
| PR-09 | FR-10, FR-11 | |
| PR-10 | FR-09, FR-12 | |
| PR-11..PR-15 | FR-37, FR-39 | Data card thay bằng DatasetSnapshot; gate `data_card_review` và `question_choice`: Deprecated. |
| PR-16, PR-17 | Deprecated | `random_rows` và nhánh `explore` bỏ; thay bằng FR-42, FR-41. |
| PR-18..PR-21 | FR-43, FR-44, FR-45 | |
| PR-22..PR-26 | FR-46, FR-47, FR-48 | |
| PR-27 | FR-14, FR-16 | Pipeline `default` Deprecated. |
| PR-28 | FR-21, FR-22 | Gate, pause, resume, stop, abandon: Deprecated (thay bằng decision inbox, huỷ run). |
| PR-29 | FR-31, FR-32 | |
| PR-30 | FR-17 | |
| PR-31 | FR-88, FR-93 | Giá trị mặc định là setting. |
| PR-32 | FR-102 | |
| PR-38..PR-44 | FR-106, FR-107, FR-108 | |
| PR-45..PR-52 | FR-62, FR-63, FR-64, FR-70 | Writing AIF thay bằng paper stage. |
| G-01 | G-01 | |
| G-02 | G-02 | |
| G-03 | G-03 | Nhánh `explore` bỏ; thay bằng release gate. |
| G-04 | G-05 | Review có giới hạn thành review loop bắt buộc. |
| G-05 | G-05 | Accept, send-back, pause, stop, close: Deprecated; thay bằng preset, decision inbox, huỷ run. |
| G-06 | G-06 | Cấu hình model và integration thuộc FE-17. |
| G-07 | Deprecated | Chuẩn bị cho feature cũ; không còn cần. |
| G-08 | G-11 | JFE thành Could. |
| G-09 | G-10 | Approval trước export thành G-10; Writing AIF Deprecated. |
| PP-01 | FR-13 | ResearchCase thành research case. |
| PP-02 | PP-03 | |
| PP-03 | PP-09 | |
| PP-04 | FR-18 | |
| PP-05 | Deprecated | Phân biệt review, acceptance và close; close không còn. |
| PP-06 | Deprecated | `random_rows` bỏ. |
| PP-07 | Deprecated | Nhãn trạng thái triển khai ngoài phạm vi (README §3). |

## Ánh xạ architecture

### ADR (architecture.md)

ADR ID cũ lấy từ bản thiết kế trước. Từ v3.0 mọi ADR ID là vĩnh viễn.

| ADR cũ | Nội dung cũ | ADR mới | Lý do |
|---|---|---|---|
| ADR-01 | JFE là standalone run cấp project | Deprecated | JFE là năng lực Could sau MVP, gắn với paper stage. Không có standalone run (ADR-13). |
| ADR-02 | Writing là manuscript workspace đọc dossier approved | Deprecated | Paper là stage thứ năm của pipeline (ADR-01) và đọc EvidenceBundle trực tiếp. Không còn workspace riêng. |
| ADR-03 | Reviewer model có chọn lọc | ADR-06 | Đảo ngược: review độc lập bắt buộc cho mọi stage. |
| ADR-04 | Structure-aware inference split | ADR-09 | Mở rộng: split quyết định theo power; thêm tier xác nhận. |
| ADR-05 | Dossier do Platform dựng bằng code | ADR-12 | Đổi: Dossier là tham chiếu; Platform chỉ đánh version, kiểm hash, ghi approval. |
| ADR-06 | Một bảng verdict hiển thị trong contract | ADR-07 | Gộp vào nguyên tắc con số và verdict từ code. |
| ADR-07 | FE sinh type từ contract backend | Deprecated | Quyết định kỹ thuật thuộc repo code (ADR-16); không phải quyết định kiến trúc mức khái niệm. |
| ADR-08 | ASPIC+ tính bằng code | Deprecated | Argument map bị bỏ; nó thành góc nhìn theo hypothesis của evidence map. |
| ADR-09 | Rights record đi cùng mọi tài liệu nguồn | Deprecated | Đọc full text có paywall là non-goal; chỉ dùng full text open access. |
| ADR-10 | Standalone run dùng lại máy trạng thái của stage run | Deprecated | Không có standalone run (ADR-13). Run state dùng một mô hình (architecture.md mục 8.9). |

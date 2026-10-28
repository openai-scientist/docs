# capstone-project-docs

Tài liệu định nghĩa của **OpenAI-Scientist** (capstone FA26SE115).

> **Tài liệu định nghĩa hệ thống; code đi theo tài liệu.** Khi code khác tài liệu, đó là việc cần làm của code, hoặc là một thay đổi cần ghi vào tài liệu qua [changelog](changelog.md). Không sửa tài liệu chỉ để khớp code.

## 1. Bộ tài liệu

| Thứ tự đọc | Tài liệu | Trả lời câu hỏi | Chuẩn tham chiếu |
|---|---|---|---|
| 0 | [glossary.md](glossary.md) | Mỗi thuật ngữ nghĩa là gì? | Nguồn thuật ngữ duy nhất |
| — | [id-mapping.md](id-mapping.md) | ID cũ nay là ID nào? | Tra ID cũ → v3.0 |
| — | [traceability.md](traceability.md) | Rule nào sinh ra yêu cầu nào? | Ma trận BO → BR → FR, NFR, ADR |
| 1 | [BRD](BRD.md) | Vì sao làm, cho ai, rule nghiệp vụ nào? | BABOK (business requirements) |
| 2 | [PRD](PRD.md) | Sản phẩm có tính năng và hành trình nào, ưu tiên ra sao? | MoSCoW, user journey |
| 3 | [architecture.md](architecture.md) | Hệ thống được cấu trúc thế nào và vì sao? | arc42 + ADR |
| 4 | Report 7 (`report/`, sau giai đoạn C) | Bản nộp capstone: SRS, SDD, test, release | ISO/IEC/IEEE 29148, IEEE 1016, ISO/IEC/IEEE 29119-3, Diátaxis |

**Nội bộ và bàn giao.** glossary, BRD, PRD và architecture là **nguồn nội bộ** của team (văn bản giải thích bằng tiếng Việt). **Report 7 trên Google Docs là tài liệu cuối cùng** để nộp. Thư mục `report/` là bản staging bằng tiếng Anh, một file cho mỗi mục La Mã; team review qua git rồi chuyển vào Google Docs. Report không chép nguyên văn nguồn nội bộ: nó trình bày lại cho người đọc ngoài team và dùng ID đã chốt ở nguồn.

**Nguyên tắc nguồn.** Các tài liệu trong repo này định nghĩa hệ thống. Code và artefact của các team khác đi theo tài liệu. Giá trị kỹ thuật (tên setting, số mặc định, schema) thuộc về implementation.

**Luồng dẫn xuất.** glossary → BRD → PRD → architecture → Report. Tài liệu đứng sau không đặt ra rule mới; nó tham chiếu ID của tài liệu đứng trước. Khi Report cần một rule chưa có, thêm rule vào BRD hoặc PRD trước.

## 2. Mức chi tiết: tài liệu độc lập với code

Tài liệu ghi:
- hành vi, rule, trạng thái, quyền, ràng buộc chất lượng;
- khái niệm và quan hệ (logical data model: entity, thuộc tính chính, quan hệ, cardinality);
- contract ở mức khái niệm (hand-off object và các phần bắt buộc của nó).

Tài liệu **không** ghi:
- đường dẫn file, số dòng, tên class hoặc function;
- route REST, HTTP status code, tên biến môi trường, cổng;
- kiểu cột, nullable, khoá ngoại, tên migration;
- số lượng test, số commit, hoặc số liệu khác thay đổi theo từng commit.

Thông báo lỗi cho người dùng được định nghĩa dưới dạng **message catalogue** (ID, tình huống, nội dung), không gắn với HTTP code.

## 3. Nội dung bền và nội dung hay đổi

| Bền (ở trong tài liệu định nghĩa) | Hay đổi (ở ngoài, hoặc trong phụ lục có ngày) |
|---|---|
| Khái niệm, rule, ID requirement, trạng thái và chuyển trạng thái, quyền | Trạng thái triển khai, tiến độ sprint |
| Hand-off object và contract item | Tên setting và giá trị mặc định |
| Quality attribute và tiêu chí đo | Kết quả đo, số test, báo cáo lỗi |
| Quy trình cài đặt ở mức thành phần và bước | Lệnh, cổng, biến môi trường cụ thể (README của từng repo) |

## 4. Quy ước ID

| Tiền tố | Ý nghĩa | Tài liệu sở hữu |
|---|---|---|
| `BP-` | Business problem | BRD |
| `BO-` | Business objective | BRD |
| `BR-` | Business rule | BRD |
| `SM-` | Success metric | BRD |
| `G-` | Product goal (PRD §2) | PRD |
| `PP-` | Product principle (PRD §5) | PRD |
| `FE-` | Feature | PRD |
| `FR-` | Functional requirement mức sản phẩm (hành vi ổn định) | PRD |
| `BC-` | Benchmark case (project mẫu; PRD §11.2.1) | PRD |
| `NFR-` | Non-functional requirement (quality attribute) | PRD |
| `UC-` | Use case | Report III |
| `SR-` | System rule chi tiết của một UC (giới hạn, thời hạn, điều kiện), truy về FR | Report III |
| `ADR-` | Architecture decision record | architecture.md |
| `QS-` | Quality scenario (architecture §10) | architecture.md |
| `R-` | Risk (architecture §11) | architecture.md |
| `MSG-` | Message cho người dùng | Report III, phụ lục message catalogue |
| `CR-` | Common requirement áp dụng cho mọi UC | Report III §5.2 |
| `TC-` | Test case | Report V |

**Baseline v3.0.** Mọi ID được đánh số lại một lần ở v3.0. [id-mapping.md](id-mapping.md) ánh xạ ID cũ → ID mới (hoặc → Deprecated). Từ v3.0 trở đi áp dụng các quy tắc dưới đây.

Quy tắc:
1. ID là vĩnh viễn. Không đánh số lại, không dùng lại.
2. Requirement bị bỏ giữ nguyên dòng, ghi **Deprecated (ngày, lý do, thay bằng ID nào)**.
3. Mỗi ID chỉ được định nghĩa ở một tài liệu sở hữu; tài liệu khác chỉ tham chiếu.

## 5. Chuẩn theo loại tài liệu

**BRD.** Business problem → objective → stakeholder → scope (in/out) → business rule → success metric → risk, assumption, constraint. Mỗi BR là một rule kiểm được, truy về BO.

**PRD.** Feature theo MoSCoW (Must/Should/Could/Won't). Mỗi feature có: mục đích, actor, user journey ngắn, FR liên quan, tiêu chí chấp nhận. NFR có tiêu chí đo.

**Requirement (PRD và Report III, theo ISO/IEC/IEEE 29148).** Mỗi requirement có:

| Thuộc tính | Nội dung |
|---|---|
| ID | Bền vững, theo §4 |
| Statement | Một câu "The system shall …" (hoặc "Hệ thống phải …"), một ý, kiểm được |
| Rationale | Vì sao cần |
| Source | ID cha: BO cho BR, BR cho FR; BO, BR hoặc SM cho NFR (không dẫn ADR, QS, R hay PP) |
| Priority | Must / Should / Could |
| Verification | Test, Inspection, Analysis hoặc Demonstration |

Tránh từ mơ hồ: "nhanh", "thân thiện", "phù hợp", "v.v.", "nếu cần". NFR phải có ngưỡng đo (ví dụ "p95 dưới 2 giây cho trang danh sách run").

**Architecture và Report IV (arc42 + IEEE 1016).** Các viewpoint tối thiểu: context, logical (thành phần và trách nhiệm), information (logical data model), interaction (luồng chính), deployment, security. Mỗi quyết định lớn có một **ADR**: bối cảnh, quyết định, phương án đã cân nhắc, hệ quả.

**Report V (ISO/IEC/IEEE 29119-3, rút gọn).** Phạm vi, mức test, loại test, môi trường, tiêu chí vào/ra, rủi ro test, ma trận truy vết requirement → test case. Kết quả test có ngày và phiên bản build.

**Report VI (Diátaxis).** Tách bốn loại: tutorial (hành trình đầu tiên), how-to (từng nhiệm vụ), reference (màn hình, thông báo, quyền), explanation (khái niệm). Hướng dẫn cài đặt ở mức thành phần và bước; lệnh chi tiết dẫn tới README của repo.

**Truy vết.** Một ma trận BR → FR → UC → TC. Mỗi FR truy được về BR; mỗi Must FR có ít nhất một TC.

## 6. Văn phong

Viết gần ASD-STE100: câu ngắn, chủ động, một ý một câu, không từ mơ hồ. Thuật ngữ theo [glossary.md](glossary.md). Văn bản giải thích viết tiếng Việt; thuật ngữ, ID và tên trạng thái giữ tiếng Anh.

## 7. Quy trình thay đổi

Theo [AGENTS.md](AGENTS.md): cập nhật tài liệu nguồn trước, ghi [changelog.md](changelog.md) trong cùng đợt, kiểm tra link và `git diff --check`, rồi mới commit hoặc mở PR.

## 8. Diagram

Diagram editable nằm trong [`diagrams/`](diagrams/), dựng từ builder và source JSON. **Trạng thái: stale.** Chúng mô tả luồng cũ (gate, send-back, mode light/auto, pipeline ba stage) và sẽ được cập nhật ở một đợt riêng.

| Diagram | Lỗi thời ở điểm nào |
|---|---|
| Use case | Thiếu paper stage, decision inbox, duyệt Dossier; còn mode `light` |
| Context | Thiếu Local Node và paper stage |
| Activity | Luồng dựa trên gate; thiếu preset, presence, decision inbox, review loop |
| Sequence | Luồng dựa trên gate và runner; thiếu unseal, decision inbox, paper |
| ERD | Mô hình vật lý, còn entity gate; cần thành logical data model |

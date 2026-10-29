# Product Requirements Document (PRD)
## OpenAI-Scientist

**Document Type:** Product Requirements Document\
**Project:** OpenAI-Scientist (capstone FA26SE115)\
**Version:** 3.0 Draft (2026-10-29)\
**Status:** Draft — nguồn nội bộ\
**Liên quan:** [glossary](glossary.md) · [README](README.md) · [BRD](BRD.md) · [Architecture](architecture.md) · [Traceability](traceability.md) · [ID mapping](id-mapping.md) · [changelog](changelog.md)

Thuật ngữ theo [glossary.md](glossary.md).

> **Vai trò tài liệu.** PRD là nguồn nội bộ. PRD định nghĩa sản phẩm ở mức hành vi ổn định; code đi theo PRD. PRD không ghi trạng thái triển khai, màn hình, danh sách field hay giới hạn thuộc system rule của Report III.

---

# 1. Product Summary

OpenAI-Scientist là web app cho nhóm nghiên cứu làm việc trên dữ liệu dạng bảng. Researcher bắt đầu bằng một research case; dataset là tuỳ chọn. Hệ thống chạy pipeline `dataset_first` qua năm stage: dataset, hypothesis, experiment_design, execution và paper. Mỗi ranh giới stage có một hand-off object có kiểu, version và hash.

Máy làm phần việc kiểm tra được bằng code: con số, verdict, grade và claim ceiling. AI đề xuất và viết lời. Researcher giữ các quyết định pinned. Review độc lập là bắt buộc cho mọi object version. Hàng dữ liệu `local` ở lại máy user; Local Node chỉ release aggregate qua một release gate. Kết quả cuối là Dossier; chỉ Dossier đã duyệt mới được export ra ngoài project.

Hệ thống không hứa khoa học luôn đúng. Hệ thống hứa ba điều: **không có lỗi nào bị giấu, mọi claim có nguồn, mọi run có thể chạy lại**.

# 2. Product Goals

| ID | Mục tiêu sản phẩm | BO |
|---|---|---|
| G-01 | Researcher đi từ research case tới PaperPack trong một workspace, theo một pipeline cố định. | BO-01, BO-10 |
| G-02 | Mọi claim, citation, số liệu và quyết định truy được về record hoặc phép tính của code; mọi run replay được. | BO-02 |
| G-03 | Hàng dữ liệu không bao giờ rời nơi giữ dữ liệu; model và artifact chỉ thấy aggregate đã qua release gate. | BO-03 |
| G-04 | Kết quả xác nhận không thể p-hacking: split theo power, Lock, envelope, unseal, tried ledger và confirmation tier. | BO-04 |
| G-05 | Review độc lập bắt buộc ở mọi stage; user quyết định theo loại action (preset, pinned, presence). | BO-05 |
| G-06 | Chi tiêu có trần ở hai mức: token budget của run và budget tháng của project. | BO-06 |
| G-07 | Nhóm cộng tác an toàn trong project, quyền theo role. | BO-07 |
| G-08 | Mọi run kết thúc với kết quả rõ, kể cả `with_gaps`; không treo. | BO-08 |
| G-09 | Chất lượng từng stage và cả pipeline được đo bằng acceptance scenario, seeded-flaw bench, planted-truth bench và paper reproduction bench. | BO-09 |
| G-12 | (Should) Researcher thấy điều đã biết về mỗi claim key qua nhiều run: claim status, forecast score và replication run trên dữ liệu độc lập. | BO-02, BO-04, BO-10 |
| G-10 | Chỉ export ra ngoài project khi Dossier đã được duyệt. | BO-11 |
| G-11 | (Could, sau MVP) Researcher chọn tạp chí bằng profile có bằng chứng (JFE). | BO-12 |

# 3. Non-Goals

Nguồn: [BRD §7.2](BRD.md).

| Non-goal | Ghi chú |
|---|---|
| Dữ liệu không phải dạng bảng (ảnh, text corpus, tín hiệu) | Chỉ hỗ trợ dữ liệu bảng. |
| Thiết kế thu thập dữ liệu mới (thí nghiệm lab hoặc thực địa) | experiment_design chỉ lập kế hoạch phân tích dữ liệu bảng có sẵn. |
| Sản phẩm systematic review đầy đủ (đăng ký PROSPERO, GRADE đầy đủ, meta-analysis kết luận) | Hypothesis stage là rapid review có phương pháp. |
| Đọc full text sau paywall | Chỉ dùng metadata, abstract và full text open access. |
| Organization, multi-tenant, ma trận quyền tuỳ biến | Project là scope cao nhất. |
| Tự nộp bài cho publisher, bảo đảm tạp chí chấp nhận | Researcher quyết định nộp bài. |
| Tuyên bố causal chỉ từ plan hoặc hypothesis | Claim chỉ đến từ verdict và claim ceiling. |
| So sánh với human-only, AutoML hoặc generic agent | Ngoài phạm vi: sản phẩm không đánh giá chính OpenAI-Scientist so với các hệ thống này. Đề tài nghiên cứu của user vẫn trong phạm vi: user so sánh một phương pháp AutoML với baseline trên dữ liệu của mình bằng `method_comparison` (FE-19, Should, sau MVP). |
| Task family ranking, survival, forecasting, anomaly | Ngoài phạm vi; task family hỗ trợ là `binary`, `multiclass`, `regression`, `rare-event` (BR-83). |

# 4. Users and Roles

Định nghĩa role theo [glossary §1](glossary.md).

| Role | Loại | Phạm vi | Việc chính |
|---|---|---|---|
| Platform Admin | Role hệ thống | Toàn hệ thống | Quản lý user, model, key, engine settings, budget mặc định, audit, health. Xem metadata project; không xem nội dung nếu không là member. |
| Project Manager | Role project | Project được quản lý | Member, settings, budget, dataset, run; huỷ run; duyệt chi thêm; duyệt Dossier; mọi việc nghiên cứu của Researcher (BR-80). |
| Researcher | Role project | Project là member | Research case, run, decision inbox, acceptance, lock plan, paper. |
| Reviewer | Role project | Project là member | Đọc và bình luận mọi object; duyệt Dossier theo review settings. |
| AI PI | Connector persona; secondary actor trong use case | Run đang chạy | Tóm tắt, đề xuất next step, viết lab notebook, quyết tạm item không pinned khi `autopilot` và `away`, trong giới hạn thay mặt user. Không là member. |

## 4.1 Conceptual permission matrix

Ma trận này ở mức khái niệm. Chi tiết theo màn hình và thao tác thuộc Report III. Nếu Platform Admin là member của project, quyền trong project theo role project của người đó.

| Capability | Platform Admin | Project Manager | Researcher | Reviewer | AI PI |
|---|---|---|---|---|---|
| View | Chỉ metadata | Có | Có | Có | Run đang chạy |
| Comment | Không | Có | Có | Có | Không |
| Run (tạo và chạy) | Không | Có | Có | Không | Không |
| Answer inbox | Không | Có | Có | Không | Chỉ tentative decision cho item không pinned |
| Accept hand-off object | Không | Có | Có | Không | Chỉ tentative decision cho item không pinned |
| Lock plan | Không | Có | Có | Không | Không (pinned) |
| Cancel run | Không | Có | Có, với run mình tạo | Không | Không |
| Approve extra spend | Không | Có | Không | Không | Không |
| Approve Dossier | Không | Có [a] | Không | Có [a] | Không |
| Export | Không | Có | Có | Không | Không (pinned) |
| Administer | Hệ thống | Project | Không | Không | Không |

Chú thích:

- [a] Theo review settings của project: số approval, ai được duyệt, có cho tự duyệt không (BR-63).

Nguồn: BR-02, BR-06, BR-26, BR-80, BR-30, BR-31, BR-60, BR-63, BR-64, BR-77.

# 5. Product Principles

| ID | Nguyên tắc | Hệ quả cho sản phẩm |
|---|---|---|
| PP-01 | Mỗi object nghiên cứu có một module sở hữu. | Object liên kết với nhau chỉ bằng id và hash. |
| PP-02 | Một khái niệm, một tên. | UI, tài liệu và prompt dùng đúng tên trong glossary. |
| PP-03 | Con số đến từ code. | Text của model mang tham chiếu tới record, không mang số. |
| PP-04 | Truy vết được, không đòi hoàn hảo. | Code chỉ từ chối object khi provenance hoặc contract hỏng; vấn đề khác thành finding hoặc known risk. |
| PP-05 | Run kết thúc; không dừng treo. | Giới hạn kết thúc stage trên output tốt nhất, kèm gap. |
| PP-06 | Đối xứng giữa user và agent. | Action của user đi qua cùng tool, guard và check như agent. |
| PP-07 | Prompt và validator khớp nhau. | Mọi hard rule có ở cả hai nơi. |
| PP-08 | Code trước, agent cho phần cần phán đoán. | Dùng code thuần, rồi một lần gọi model, rồi mới đến agent loop. |
| PP-09 | Hàng dữ liệu không rời nơi giữ dữ liệu. | Chỉ aggregate rời đi, qua một release gate, và mỗi release có log. |
| PP-10 | Mỗi cơ chế phải có lý do tồn tại. | Persona, check hay loại biểu đồ chỉ có khi bench hoặc chuẩn biện minh. |


# 6. Feature List

MoSCoW: Must cho FE-01..FE-15 và FE-17; Should cho FE-19 (sau MVP); Could cho FE-18 (sau MVP). Cột BR liệt kê các BR mà FR của feature dẫn nguồn.

| FE | Name | MoSCoW | Purpose | Actors | BR |
|---|---|---|---|---|---|
| FE-01 | Account and access | Must | Cho user đăng nhập và bảo đảm mọi thao tác theo role. | Mọi user; Platform Admin | BR-01, BR-02, BR-06, BR-103 |
| FE-02 | Project workspace and members | Must | Cho nhóm làm việc trong một project có member, settings và audit log. | Project Manager; Researcher; Reviewer | BR-02, BR-03, BR-04, BR-05, BR-24, BR-59, BR-63, BR-80, BR-104 |
| FE-03 | Data management (dataset, version, connection, location) | Must | Quản lý dataset có version bất biến, nhập dữ liệu từ upload hoặc connection, và đặt data location. | Project Manager; Researcher | BR-16, BR-17, BR-18, BR-19, BR-102 |
| FE-04 | Research case and run management | Must | Bắt đầu run từ research case, điều phối năm stage, giữ run state, stale, huỷ run và next step. | Researcher; Project Manager; AI PI | BR-07, BR-08, BR-09, BR-10, BR-11, BR-12, BR-13, BR-14, BR-15, BR-41, BR-58, BR-77, BR-78, BR-104 |
| FE-05 | Human control | Must | Cho user kiểm soát run theo loại action: preset, presence, action pinned, decision inbox, decision log, overturn, AI PI và lab notebook. | Researcher; Project Manager; AI PI | BR-24, BR-25, BR-26, BR-27, BR-28, BR-29, BR-30, BR-31, BR-32, BR-33, BR-34, BR-49, BR-61, BR-75, BR-104 |
| FE-06 | Dataset stage | Must | Biến dữ liệu thành DatasetSnapshot: chất lượng, question map, split theo power và fitness. | Researcher; Persona (dataset) | BR-26, BR-41, BR-43, BR-44, BR-76, BR-84, BR-85, BR-86, BR-88, BR-89 |
| FE-07 | Hypothesis stage and Literature Base | Must | Rà soát literature có phương pháp và tạo HypothesisSet có evidence. | Researcher; Persona (hypothesis) | BR-41, BR-45, BR-54, BR-90, BR-91, BR-92, BR-99 |
| FE-08 | Experiment design stage and Lock | Must | Lập AnalysisPlan cho dữ liệu bảng có sẵn và khoá plan bằng Lock. | Researcher; Persona (experiment_design) | BR-26, BR-31, BR-46, BR-47, BR-50, BR-83, BR-86, BR-93, BR-94, BR-95, BR-96, BR-99 |
| FE-09 | Execution stage | Must | Chạy plan đã lock, giữ kết quả confirmatory trong envelope, unseal, và tính verdict, grade, claim ceiling bằng code. | Researcher; Persona (execution) | BR-11, BR-26, BR-48, BR-49, BR-50, BR-51, BR-52, BR-53, BR-54, BR-55, BR-56, BR-57, BR-86, BR-87, BR-105 |
| FE-10 | Paper stage | Must | Soạn PaperPack mà đội viết bài dùng được mà không phải dẫn xuất lại số liệu. | Researcher; Persona (paper) | BR-56, BR-65, BR-66, BR-67, BR-68, BR-69, BR-70, BR-71, BR-72, BR-73 |
| FE-11 | Independent review loop and personas | Must | Review độc lập bắt buộc cho mọi object version, với finding đã kiểm và tối đa hai vòng sửa. | Persona (guard); Researcher | BR-35, BR-36, BR-37, BR-38, BR-39, BR-40, BR-42, BR-97, BR-100, BR-101 |
| FE-12 | Local Node | Must | Giữ dữ liệu `local` trên máy user, chạy job cạnh dữ liệu và chỉ release aggregate qua release gate. | Researcher; Project Manager | BR-14, BR-16, BR-18, BR-19, BR-20, BR-21, BR-22, BR-27, BR-80, BR-81 |
| FE-13 | Budget and cost | Must | Kiểm soát token budget của run và budget tháng của project; run luôn kết thúc. | Project Manager; Platform Admin | BR-28, BR-58, BR-59, BR-60, BR-61, BR-78 |
| FE-14 | Dossier, approval and export | Must | Gom kết quả thành Dossier có version, duyệt theo review settings và chỉ cho export khi đã duyệt. | Reviewer; Project Manager; Researcher | BR-05, BR-62, BR-63, BR-64, BR-79 |
| FE-15 | Collaboration (comments, notifications) | Must | Cho member bình luận và nhận thông báo quanh cùng một run. | Mọi member | BR-05, BR-06, BR-28 |
| FE-17 | Administration and monitoring | Must | Cho Platform Admin quản lý user, model, key, audit và theo dõi vận hành. | Platform Admin | BR-02, BR-05, BR-14, BR-23, BR-29, BR-40 |
| FE-18 | Journal Fingerprint Extraction (JFE) | Could | Dựng profile tạp chí có bằng chứng để paper stage tham chiếu (sau MVP). | Researcher | BR-74 |
| FE-19 | Method comparison research | Should | So sánh các phương pháp ML trên cùng dữ liệu bằng claim type `method_comparison` (research pattern G–J, baseline policy F); sau MVP. | Researcher; Persona (experiment_design, execution) | BR-82, BR-83, BR-93, BR-96, BR-98, BR-99 |
| FE-20 | Claim ledger, forecast and replication | Should | Cho researcher thấy điều đã biết về mỗi claim key xuyên run, chấm độ chắc của model và nhân rộng claim trên dữ liệu độc lập; đo giá trị bằng planted-truth bench. | Researcher; AI PI; Persona (experiment_design) | BR-106, BR-107, BR-108, BR-109, BR-110 |

FE-16: Deprecated, không dùng lại để tránh nhầm với feature cũ. Nội dung của feature cũ thuộc execution stage (FE-09); xem [id-mapping.md](id-mapping.md#ánh-xạ-prd).

# 7. User Journeys

Mỗi journey ở mức khái niệm. Dòng "FR chính" liệt kê các requirement mà journey kiểm.

## J1 — Run đầu tiên chỉ từ một topic (chưa có dataset)

1. Researcher tạo research case chỉ có topic, mục tiêu, bối cảnh, ràng buộc, domain và tài liệu tham khảo.
2. Hệ thống kiểm project chưa có run active, rồi tạo run theo pipeline `dataset_first`.
3. Dataset stage tìm dataset trong project và dataset public. Nếu không có dataset dùng được, stage tạo một item question trong decision inbox.
4. Researcher chọn dataset có sẵn, upload dữ liệu, nhập từ data connection hoặc dùng Local Node. Hệ thống tạo dataset version.
5. Dataset stage xác định unit of observation và cấu trúc dữ liệu; Researcher xác nhận (action pinned) trước khi split được tạo. Dataset stage tạo DatasetSnapshot. Review loop chạy. Acceptance theo preset của stage.
6. Các stage sau chạy theo J2 và J3. Run kết thúc; AI PI đề xuất next step.

FR chính: FR-13, FR-14, FR-15, FR-16, FR-09, FR-40, FR-37, FR-29, FR-23.

## J2 — Decision inbox khi user present và khi away

**Present**

1. Agent gặp một action `must_ask` và tạo item trong decision inbox với option, option đề xuất và lý do.
2. Hệ thống hỏi ngay. Nếu không còn việc độc lập, run vào `waiting(decision)`.
3. User trả lời. Decision log ghi quyết định. Run quay lại `running`.

**Away (preset `autopilot`)**

1. User đặt presence `away`. Item `must_ask` xếp hàng; agent tiếp tục các action không phụ thuộc item.
2. AI PI quyết tạm các item không pinned. Mỗi quyết định thành một tentative decision.
3. Item pinned chờ. Khi không còn việc, stage kết thúc ở `ready_to_<action>` và run ở `waiting(decision)`; run không kết thúc vì item đó trước hạn chờ. Chỉ item pinned đang chặn và item `spending` mới gửi thông báo ngoài, kèm lời nhắc trước hạn.
4. User quay về, mở decision inbox, xác nhận hoặc lật lại từng tentative decision.
5. Nếu user lật, hệ thống hoàn tác phần phụ thuộc và đánh dấu object bị ảnh hưởng `stale`. Decision log ghi overturn. Hệ thống đề xuất nâng level theo overturn rate; user quyết định.
6. Nếu hạn chờ của item pinned hết mà user chưa trả lời, run kết thúc `ended(with_gaps)`. Item đóng ở trạng thái chưa trả lời và gap được liệt kê. AI PI và giá trị mặc định không quyết thay user.

FR chính: FR-28, FR-29, FR-30, FR-31, FR-32, FR-19, FR-36, FR-263, FR-264, FR-265, FR-266.

## J3 — Lock plan

1. Experiment_design stage chạy analysis program trên twin. Mọi check xanh. Review loop chạy.
2. Stage tạo item pinned "lock plan". Item này `must_ask` ở mọi preset.
3. Nếu user `present`, user đọc plan và quyết. Nếu user `away`, plan chờ lock tới hạn chờ của item; không ai lock thay user.
4. User lock. Platform ghi Lock; plan thành `locked` và bất biến.
5. Execution stage dựng từ Lock. Thay đổi thuật toán sau đó là deviation (pinned).

FR chính: FR-46, FR-47, FR-48, FR-49, FR-27, FR-56.

## J4 — Unseal, đọc verdict, grade và claim ceiling

1. Job confirmatory đưa kết quả vào envelope. Agent chỉ thấy done hoặc error.
2. Khi mọi check xanh, Platform unseal tự động (hoặc theo yêu cầu của user nếu user đã chọn unseal bằng tay). Platform mở mọi hypothesis cùng lúc và ghi thời điểm.
3. Code tính verdict, grade và claim ceiling. Interpretation row cho lời kết luận.
4. User đọc verdict của từng hypothesis, grade, claim ceiling, deviation log và candidate.
5. Candidate từ lane E vào decision inbox. User chọn; candidate không bao giờ là claim.
6. Paper stage không vượt claim ceiling.

FR chính: FR-51, FR-52, FR-53, FR-54, FR-55, FR-57, FR-58, FR-59.

## J5 — Chạy trên dữ liệu `local` qua Local Node

1. User cài Local Node (không cần Docker) và ghép với project bằng mã ghép.
2. Local Node đề xuất dataset từ thư mục nó theo dõi. Dataset version có data location `local`.
3. Job chạy cạnh dữ liệu. Kết quả đi qua release gate; chỉ aggregate rời máy. Mỗi release vào release log.
4. Nếu Local Node offline và job chặn việc, run vào `waiting(node_offline)`; việc khác tiếp tục; user nhận một thông báo gộp.
5. Ở disclosure `strict`, loại số chưa duyệt tạo item release review trong decision inbox. Researcher hoặc Project Manager của project trả lời.
6. Khi Local Node bị thu hồi, job cho dữ liệu `local` của Node bị từ chối và user được báo lý do. Object đã publish vẫn đọc được.

FR chính: FR-12, FR-79, FR-80, FR-81, FR-82, FR-85, FR-86, FR-87, FR-110.

## J6 — Budget chạm 100%

1. Hệ thống cảnh báo khi budget tháng của project chạm các ngưỡng.
2. Khi chạm 100%, hệ thống chặn run mới. Run đang chạy vào `waiting(budget_review)` và tạo item `spending` `must_ask`.
3. Project Manager nhận thông báo ngoài khi item `spending` được tạo và lời nhắc trước hạn trả lời.
4. Project Manager duyệt chi thêm (run chạy tiếp) hoặc để run kết thúc `with_gaps`.
5. Nếu hết hạn mà chưa có quyết định, run kết thúc `ended(with_gaps)` trên output tốt nhất; mọi contract item đỏ được liệt kê.

FR chính: FR-89, FR-90, FR-91, FR-92, FR-21.

## J7 — Duyệt và export Dossier

1. Khi PaperPack được accepted, Platform tạo Dossier version 1 từ các version EvidenceBundle và PaperPack đã accepted, và kiểm hash. Run kết thúc `with_gaps` hoặc `cancelled` trước khi có PaperPack accepted thì không có Dossier.
2. Reviewer và Project Manager đọc và bình luận.
3. Approval theo review settings. Khi đủ approval cho version hiện tại, Dossier thành approved.
4. Export là action pinned và cần Dossier đã duyệt. Mỗi export ghi vào audit log.
5. Nếu bundle hoặc pack có version accepted mới, Platform tạo Dossier version mới; version mới phải được duyệt lại.
6. Researcher quyết định nộp bài; hệ thống không tự nộp.

FR chính: FR-94, FR-95, FR-96, FR-97, FR-98, FR-99, FR-70.


# 8. Functional Requirements

Mỗi FR là một hành vi ổn định, kiểm được, ở mức sản phẩm. Mỗi FR chứa một requirement kiểm được độc lập. FR-146 trở đi được thêm sau khi ID đã chốt: FR-146 đến FR-150 là FR mới; các FR từ FR-151 tách ra từ FR cha và nằm ngay sau dòng cha, cùng priority và cùng BR nguồn. FR-263 trở đi là FR mới thêm sau khi ID đã chốt: hạn chờ item pinned (FR-263 đến FR-266), phần `method_comparison` tách khỏi FR Must (FR-267 đến FR-269), rule của vòng sửa (FR-270, FR-271), evidence rows và tích trên hàng độc lập (FR-272, FR-273, Must) và FE-20 (FR-274 đến FR-287, Should); chúng nằm trong feature của chúng. Giới hạn, thời hạn và điều kiện chi tiết là system rule (`SR-`) của Report III và truy về FR. Cột Verification: T = Test, I = Inspection, A = Analysis, D = Demonstration. Priority của FR lấy theo MoSCoW của feature.

## FE-01 — Account and access

**Mục đích:** Cho user đăng nhập và bảo đảm mọi thao tác theo role. **Actor:** Mọi user; Platform Admin. **Journey:** J1. **Tiêu chí chấp nhận:** Đăng nhập bằng email hoặc bằng tài khoản Google thành công; thao tác của member thiếu role bị từ chối; Platform Admin không mở nội dung project.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-01 | Hệ thống phải cho user đăng nhập bằng email, không dùng mật khẩu. | Bỏ rủi ro quản lý mật khẩu. | BR-01 | Must | T |
| FR-02 | Hệ thống phải kiểm role của user ở mọi thao tác và từ chối thao tác của member không có role phù hợp. | Quyền theo role là nền của mọi cộng tác. | BR-02 | Must | T |
| FR-151 | Hệ thống phải không tiết lộ sự tồn tại của project cho người không phải member. | Người ngoài project không biết project có tồn tại. | BR-02 | Must | T |
| FR-03 | Hệ thống phải cho Platform Admin xem metadata của mọi project (danh sách, member, usage, trạng thái run). | Người vận hành theo dõi vận hành của mọi project. | BR-06 | Must | T |
| FR-152 | Hệ thống phải không cho Platform Admin mở dataset, object hay bản thảo của project mà Platform Admin không là member. | Người vận hành không đọc nội dung nghiên cứu. | BR-06 | Must | T |
| FR-146 | Hệ thống phải cho user đăng nhập bằng tài khoản Google và nhận cùng một user khi email đã xác minh trùng với tài khoản đăng nhập bằng email. | User chọn cách đăng nhập quen thuộc mà không bị tách thành hai tài khoản. | BR-103 | Must | T |

## FE-02 — Project workspace and members

**Mục đích:** Cho nhóm làm việc trong một project có member, settings và audit log. **Actor:** Project Manager; Researcher; Reviewer. **Journey:** J7. **Tiêu chí chấp nhận:** Project luôn có Project Manager active; invitation hết hạn bị từ chối; project archive chỉ đọc.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-04 | Hệ thống phải bảo đảm mỗi project có ít nhất một Project Manager active và từ chối thao tác làm mất Project Manager cuối cùng. | Project luôn có người chịu trách nhiệm. | BR-03 | Must | T |
| FR-05 | Hệ thống phải cho user vào project qua invitation. | Kiểm soát ai vào project. | BR-04 | Must | T |
| FR-153 | Hệ thống phải từ chối invitation đã hết hạn theo access setting. | Invitation cũ không mở đường vào project. | BR-04 | Must | T |
| FR-06 | Hệ thống phải xử lý project đã archive là chỉ đọc. | Giữ nguyên hồ sơ khi project đóng. | BR-03 | Must | T |
| FR-07 | Hệ thống phải ghi mọi thay đổi quan trọng của project vào audit log chỉ-thêm. | Truy vết thay đổi. | BR-05 | Must | T |
| FR-08 | Hệ thống phải cho Project Manager đặt project settings gồm budget tháng, review settings, preset mặc định theo stage, notification và hạn chờ item pinned. | Mỗi project tự đặt mức kiểm soát và duyệt. | BR-24; BR-59; BR-63; BR-104 | Must | D |
| FR-111 | Hệ thống phải cho Project Manager làm mọi thao tác nghiên cứu của Researcher trong project (tạo run, trả lời decision inbox, accept object, lock plan, export), ngoài quyền quản lý của Project Manager. | Project Manager không cần thêm role Researcher để điều hành nghiên cứu. | BR-80; BR-02 | Must | T |

## FE-03 — Data management (dataset, version, connection, location)

**Mục đích:** Quản lý dataset có version bất biến, nhập dữ liệu từ upload hoặc connection, và đặt data location. **Actor:** Project Manager; Researcher. **Journey:** J1, J5. **Tiêu chí chấp nhận:** Mỗi lần upload tạo version mới có hash; dữ liệu `local` không có preview và download.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-09 | Hệ thống phải tạo một dataset version bất biến, có hash, cho mỗi lần upload hoặc import, và không ghi đè version cũ. | Replay cần dữ liệu không đổi. | BR-16 | Must | T |
| FR-154 | Hệ thống phải để mọi phân tích ghim một dataset version. | Replay biết chính xác dữ liệu đã dùng. | BR-16 | Must | T |
| FR-10 | Hệ thống phải chỉ import qua data connection từ nguồn user đã uỷ quyền. | Tránh import ngoài ý muốn. | BR-17 | Must | T |
| FR-155 | Hệ thống phải chặn data connection tới host nội bộ. | Tránh tấn công vào mạng nội bộ. | BR-17 | Must | T |
| FR-11 | Hệ thống phải không trả credential của data connection cho user. | Bảo vệ credential. | BR-17 | Must | T |
| FR-156 | Hệ thống phải không ghi credential của data connection vào log. | Log không lộ credential. | BR-17 | Must | T |
| FR-12 | Hệ thống phải gán cho mỗi dataset version một data location (`platform` hoặc `local`). | Mỗi dữ liệu có nơi giữ rõ ràng. | BR-18; BR-19 | Must | T |
| FR-157 | Hệ thống phải chỉ cho Local Node đọc dữ liệu `local`. | Dữ liệu `local` không đi qua đường khác. | BR-18; BR-19 | Must | T |
| FR-158 | Hệ thống phải không cho preview hay download hàng của dữ liệu `local`. | Hàng dữ liệu `local` không rời máy user. | BR-18; BR-19 | Must | T |
| FR-112 | Hệ thống phải cho upload nhận các định dạng dữ liệu bảng phổ biến, gồm Parquet. Danh sách đầy đủ là system rule của Report III. | Researcher đưa dữ liệu vào mà không phải đổi định dạng. | BR-102 | Must | T |

## FE-04 — Research case and run management

**Mục đích:** Bắt đầu run từ research case, điều phối năm stage, giữ run state, stale, huỷ run và next step. **Actor:** Researcher; Project Manager; AI PI. **Journey:** J1, J2. **Tiêu chí chấp nhận:** Run chạy hết năm stage hoặc kết thúc ở một trạng thái `ended`; run thứ hai bị từ chối khi đã có run active.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-13 | Hệ thống phải tạo run từ một research case gồm topic, mục tiêu, bối cảnh, ràng buộc, domain và tài liệu tham khảo; dataset là tuỳ chọn. | Researcher thường bắt đầu bằng câu hỏi, chưa có dataset. | BR-07 | Must | T |
| FR-14 | Hệ thống phải chạy mọi run theo pipeline `dataset_first`: dataset, hypothesis, experiment_design, execution, paper. | Một pipeline duy nhất; không rẽ nhánh theo dataset. | BR-08 | Must | T |
| FR-15 | Hệ thống phải để dataset stage, khi research case chưa có dataset, tìm dataset trong project, tìm dataset public (vai trò `enrichment` hoặc `validation`), hoặc hỏi user qua decision inbox. | Run bắt đầu được mà không cần dataset. | BR-08 | Must | T |
| FR-159 | Hệ thống phải xem việc join dữ liệu public vào dữ liệu riêng là action pinned. | Dữ liệu public không vào dữ liệu riêng khi chưa có quyết định. | BR-08 | Must | T |
| FR-16 | Hệ thống phải từ chối tạo run mới khi project đã có một run active. | Tránh tranh chấp dữ liệu, Literature Base, budget và inbox. | BR-09 | Must | T |
| FR-17 | Hệ thống phải chỉ cho đổi research case đã chốt qua amendment có lý do, version và event. | Mục tiêu không đổi ngầm giữa chừng. | BR-10 | Must | T |
| FR-160 | Hệ thống phải để stage đã bắt đầu giữ case version cũ. | Stage không đổi mục tiêu giữa chừng. | BR-10 | Must | T |
| FR-18 | Hệ thống phải bảo đảm mỗi ranh giới stage có đúng một hand-off object có kiểu, version và hash. | Truy vết cần object xác định. | BR-11 | Must | T |
| FR-161 | Hệ thống phải giữ hand-off object bất biến sau khi accepted và tạo version mới khi sửa. | Replay cần object cố định. | BR-11 | Must | T |
| FR-19 | Hệ thống phải đánh dấu `stale` mọi object downstream ghim một object upstream khi upstream có version mới. | Downstream biết upstream đã đổi. | BR-12 | Must | T |
| FR-162 | Hệ thống phải không tự cập nhật object `stale` và cho user chọn cập nhật qua acceptance. | Không có cập nhật ngầm. | BR-12 | Must | T |
| FR-20 | Hệ thống phải xem một stage là done khi mọi contract item xanh theo check bằng code. | Done có tiêu chí máy kiểm được. | BR-13 | Must | T |
| FR-163 | Hệ thống phải xem contract item đỏ là task tự sửa của agent. | Self-healing nhìn thấy được. | BR-13 | Must | T |
| FR-164 | Hệ thống phải chuyển contract item thành item `needs-you` khi item tiêu hết phần budget của nó. | Không có bộ đếm retry ẩn; user thấy item bị kẹt. | BR-13 | Must | T |
| FR-21 | Hệ thống phải giữ mỗi run ở đúng một run state (`running`; `waiting` với lý do `decision`, `node_offline` hoặc `budget_review`; `ended` với kết quả `complete`, `with_gaps`, `failed_technical` hoặc `cancelled`). | Trạng thái của run xác định. | BR-14 | Must | T |
| FR-165 | Hệ thống phải kết thúc mọi run: khi chạm giới hạn, stage kết thúc trên output tốt nhất và liệt kê mọi contract item đỏ. | Run kết thúc, không treo. | BR-14 | Must | T |
| FR-262 | Hệ thống phải chỉ kết thúc run `ended(with_gaps)` khi token budget của run cạn, item `spending` quá hạn hoặc item pinned quá hạn chờ; item pinned đang chờ không kết thúc run trước hạn chờ của nó. | Chờ user không làm mất run; chỉ giới hạn chi phí hoặc hạn trả lời mới kết thúc run. | BR-14; BR-58; BR-78; BR-104 | Must | T |
| FR-265 | Hệ thống phải kết thúc run `ended(with_gaps)` trên output tốt nhất khi hạn chờ của item pinned hết mà item chưa được trả lời, đóng item ở trạng thái chưa trả lời và liệt kê gap. | Run kết thúc, không treo, mà không ai quyết thay user. | BR-104; BR-14 | Must | T |
| FR-22 | Hệ thống phải cho Project Manager hoặc Researcher đã tạo run huỷ run từ mọi trạng thái trừ `ended`, và chuyển run sang `ended(cancelled)`. | User thoát khỏi run không còn cần. | BR-77 | Must | T |
| FR-166 | Hệ thống phải giữ object đã accepted khi huỷ run. | Huỷ run không làm mất kết quả đã chấp nhận. | BR-77 | Must | T |
| FR-167 | Hệ thống phải đóng mọi item đang chờ của run khi huỷ run. | Inbox không giữ item của run đã huỷ. | BR-77 | Must | T |
| FR-168 | Hệ thống phải ghi việc huỷ run vào audit log. | Truy vết ai huỷ run. | BR-77 | Must | T |
| FR-23 | Hệ thống phải để AI PI đề xuất next step sau run từ bộ cố định (`collect_more_data`, `explore_signal`, `replicate`, `write_paper`, `revise_plan`) và để user chọn. | Hướng dẫn bước tiếp theo bằng từ vựng chung. | BR-15 | Must | T |
| FR-24 | Hệ thống phải tính mọi con số bằng code. | Model không được bịa số. | BR-41 | Must | T |
| FR-169 | Hệ thống phải để text của model mang tham chiếu tới record và không mang con số. | Số trong text luôn truy được về record. | BR-41 | Must | T |

## FE-05 — Human control

**Mục đích:** Cho user kiểm soát run theo loại action: preset, presence, action pinned, decision inbox, decision log, overturn, AI PI và lab notebook. **Actor:** Researcher; Project Manager; AI PI. **Journey:** J2, J3. **Tiêu chí chấp nhận:** Action pinned luôn hỏi ở mọi preset; AI PI không quyết item pinned; overturn được ghi và hoàn tác.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-25 | Hệ thống phải cho mỗi stage một preset (`co_work`, `milestones` mặc định, `autopilot`). | Mức kiểm soát chỉnh theo từng stage. | BR-24 | Must | T |
| FR-170 | Hệ thống phải áp dụng việc đổi preset cho action tương lai và không tính lại quyết định đã qua. | Lịch sử quyết định không đổi. | BR-24 | Must | T |
| FR-171 | Hệ thống phải đánh giá lại item đang chờ khi đổi preset. | Item đang chờ theo mức kiểm soát mới. | BR-24 | Must | T |
| FR-26 | Hệ thống phải gán mỗi action vào đúng một action group và một level (`auto`, `do_then_review`, `must_ask`). | Quyền theo loại action, không theo công tắc toàn run. | BR-25 | Must | T |
| FR-172 | Hệ thống phải không cho override hạ level của action dưới floor. | Floor giữ mức kiểm soát tối thiểu. | BR-25 | Must | T |
| FR-27 | Hệ thống phải giữ action pinned luôn ở `must_ask` ở mọi preset: định nghĩa outcome và estimand; xác nhận unit of observation và cấu trúc dữ liệu trước khi split; chọn hypothesis (từ hai trở lên) và primary; join dữ liệu public vào dữ liệu riêng; lock plan; lệch khỏi thuật toán đã lock; dùng validation source; xuất ra ngoài project. | Quyết định chỉ researcher được sở hữu. | BR-26 | Must | T |
| FR-28 | Hệ thống phải hỏi ngay kèm option, option đề xuất và lý do với item `must_ask` khi user `present`. | Hỏi đúng lúc user có mặt. | BR-27 | Must | T |
| FR-173 | Hệ thống phải xếp item `must_ask` vào hàng chờ khi user `away` và để agent tiếp tục mọi action không phụ thuộc item. | Presence chỉ đổi cách item chờ. | BR-27 | Must | T |
| FR-29 | Hệ thống phải gom item của mọi stage vào một decision inbox duy nhất với tám loại item (question, review batch, tentative decision, deviation, candidate, needs-you, release review, spending). | Một nơi xử lý. | BR-28 | Must | T |
| FR-174 | Hệ thống phải chỉ gửi thông báo ngoài (mail, push) cho item pinned đang chặn và cho item `spending` (gửi Project Manager). | Giảm thông báo gây mệt mà người có thẩm quyền chi tiêu vẫn biết. | BR-28 | Must | T |
| FR-30 | Hệ thống phải ghi vào decision log mỗi quyết định (action type, level, phiên bản policy, ai quyết, presence, đã bị overturn hay chưa). | Quyết định truy vết được. | BR-29 | Must | T |
| FR-175 | Hệ thống phải tính overturn rate theo action type. | Đo chất lượng kiểm soát. | BR-29 | Must | T |
| FR-176 | Hệ thống phải chỉ đề xuất nâng level theo overturn rate và không tự nâng. | User giữ quyền đổi level. | BR-29 | Must | T |
| FR-31 | Hệ thống phải chỉ cho AI PI quyết tạm item không pinned khi preset là `autopilot` và user `away`, và tạo tentative decision để user xác nhận hoặc lật lại. | AI PI không quyết thay user ngoài phạm vi cho phép. | BR-30 | Must | T |
| FR-177 | Hệ thống phải hoàn tác phần phụ thuộc và đánh dấu object bị ảnh hưởng `stale` khi user lật một tentative decision. | User luôn sửa được quyết định tạm. | BR-30 | Must | T |
| FR-32 | Hệ thống phải không cho AI PI kết thúc run hay quyết item pinned; run chờ user tới hạn chờ của item (FR-263). | Quyết định pinned thuộc về user. | BR-31; BR-104 | Must | T |
| FR-178 | Hệ thống phải để stage kết thúc ở trạng thái `ready_to_<action>` và run ở `waiting(decision)` khi chỉ còn item pinned đang chờ; item đó không kết thúc run trước hạn chờ (FR-263). | Item pinned chờ user mà không làm run kết thúc trước hạn. | BR-31; BR-104 | Must | T |
| FR-33 | Hệ thống phải cho action của user trên UI đi qua cùng tool, guard và check như action của agent. | Không có đường tắt cho user hoặc agent. | BR-32 | Must | T |
| FR-179 | Hệ thống phải ghi vào decision log ai hành động. | Phân biệt quyết định của user, agent và AI PI. | BR-32 | Must | T |
| FR-34 | Hệ thống phải, ở preset `milestones`, đặt level của acceptance fitness theo verdict của code: `fit` là `auto` (ghi log), `fit_with_limits` là `do_then_review`, `not_fit` là `must_ask`. | Hỏi nhiều hơn khi dữ liệu kém phù hợp. | BR-33 | Must | T |
| FR-35 | Hệ thống phải để AI PI viết lab notebook cho run gồm tóm tắt, đề xuất, quyết định tạm và lý do. | User theo dõi run bằng văn bản đọc được. | BR-34 | Must | D |
| FR-36 | Hệ thống phải ghi vào decision log mỗi giả định của agent cùng phương án thay thế và lý do. | Giả định không biến thành quyết định ngầm. | BR-75 | Must | T |
| FR-180 | Hệ thống phải không coi giả định của agent là ý định của researcher. | Ý định của researcher chỉ đến từ researcher. | BR-75 | Must | T |
| FR-147 | Hệ thống phải đặt level của tám action group ở preset `co_work` như sau: `read_compute` là `auto`; `technical_fix` là `do_then_review`; `content_judgment`, `object_drafting`, `spending`, `acceptance` và `pinned` là `must_ask`; `unseal` là `auto` khi mọi check xanh. | Ở `co_work` user duyệt mọi quyết định nội dung. | BR-24; BR-25; BR-26; BR-49 | Must | T |
| FR-148 | Hệ thống phải đặt level của tám action group ở preset `milestones` như sau: `read_compute` và `technical_fix` là `auto`; `content_judgment` và `object_drafting` là `do_then_review`; `spending` và `pinned` là `must_ask`; `acceptance` theo verdict của code (FR-34); `unseal` là `auto` khi mọi check xanh. | Ở `milestones` user duyệt tại các mốc và theo độ phù hợp của dữ liệu. | BR-24; BR-25; BR-26; BR-33; BR-49 | Must | T |
| FR-149 | Hệ thống phải đặt level của tám action group ở preset `autopilot` như sau: `read_compute`, `technical_fix` và `content_judgment` là `auto` (`content_judgment` có ghi log); `object_drafting` và `acceptance` là `do_then_review`; `spending` là `auto` dưới mức trần chi tiêu và `must_ask` khi vượt mức trần (FR-92); `pinned` là `must_ask`; `unseal` là `auto` khi mọi check xanh. | Ở `autopilot` agent chạy tự động trong giới hạn của floor, action pinned và mức trần chi tiêu. | BR-24; BR-25; BR-26; BR-49; BR-61 | Must | T |
| FR-150 | Hệ thống phải đặt floor của action group `object_drafting` là `do_then_review` và floor của `pinned` là `must_ask`; mọi action group còn lại có floor `auto`. | Floor giới hạn mức hạ level của override. | BR-25; BR-26; BR-33 | Must | T |
| FR-263 | Hệ thống phải gán cho mỗi item pinned một hạn chờ trả lời; hạn chờ là project setting, mặc định 7 ngày, nhắc trước hạn 24 giờ. | Item pinned chờ user mà run không treo vô hạn. | BR-104 | Must | T |
| FR-264 | Hệ thống phải gửi thông báo ngoài (mail, push) nhắc người có quyền trả lời item pinned trước hạn chờ. | User biết hạn trước khi run kết thúc. | BR-104; BR-28 | Must | T |
| FR-266 | Hệ thống phải không để AI PI hay giá trị mặc định quyết item pinned thay user, kể cả khi hạn chờ hết. | Quyết định pinned chỉ đến từ user. | BR-104; BR-31 | Must | T |

## FE-06 — Dataset stage

**Mục đích:** Biến dữ liệu thành DatasetSnapshot: chất lượng, question map, split theo power và fitness. **Actor:** Researcher; Persona (dataset). **Journey:** J1. **Tiêu chí chấp nhận:** Acceptance scenario của dataset stage (§11.1) đạt; split đúng cấu trúc và power.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-37 | Hệ thống phải để dataset stage tạo DatasetSnapshot gồm nguồn, table model, profile năm chiều chất lượng, dictionary, cleaning recipe, question map (câu hỏi, yêu cầu dữ liệu, mức đáp ứng), split, vai trò nguồn và fitness. | Hand-off của dataset stage phải đủ để stage sau dùng mà không đoán. | BR-43 | Must | T |
| FR-38 | Hệ thống phải không cho cleaning của dataset stage dùng outcome; cleaning cần outcome thuộc AnalysisPlan. | Tránh cleaning chọn kết quả. | BR-43 | Must | T |
| FR-39 | Hệ thống phải để code kết luận fitness của dữ liệu với câu hỏi (`fit`, `fit_with_limits`, `not_fit`). | Kết luận phù hợp dữ liệu phải kiểm được. | BR-43; BR-41 | Must | T |
| FR-40 | Hệ thống phải để dataset stage xác định unit of observation và cấu trúc dữ liệu (group, thời gian, panel). | Split và phân tích đúng phụ thuộc giữa các hàng. | BR-76; BR-26 | Must | T |
| FR-181 | Hệ thống phải để Researcher xác nhận unit of observation và cấu trúc dữ liệu (action pinned) trước khi split được tạo. | Cấu trúc do người chịu trách nhiệm xác nhận. | BR-76; BR-26 | Must | T |
| FR-41 | Hệ thống phải không tạo split khi Researcher chưa xác nhận unit of observation và cấu trúc dữ liệu. | Tránh rò rỉ giữa các phần. | BR-76; BR-26 | Must | T |
| FR-182 | Hệ thống phải không để các hàng cùng group nằm ở hai phần khi chia. | Hàng cùng group phụ thuộc nhau; chia chúng gây rò rỉ. | BR-76; BR-26 | Must | T |
| FR-183 | Hệ thống phải chia dữ liệu có trật tự thời gian theo thời gian. | Tránh dùng dữ liệu tương lai để dự đoán quá khứ. | BR-76; BR-26 | Must | T |
| FR-42 | Hệ thống phải chọn split theo power: `three_way` khi n giữ power từ 0,8 và còn reserve; `two_way` khi không; `none` khi n dưới mức tối thiểu, kèm limitation. | Split theo power thật của câu hỏi. | BR-44 | Must | T |
| FR-113 | Hệ thống phải cho phép split phân tầng lặp lại (repeated stratified) cho dữ liệu IID có task family phân loại (`binary`, `multiclass`, `rare-event`). | Giữ tỷ lệ lớp ổn định giữa các phần, nhất là khi lớp positive hiếm. Phép lặp chỉ áp dụng trong phần exploration; phần confirmation dùng một lần (BR-86). | BR-84; BR-86 | Must | T |
| FR-114 | Hệ thống phải để dataset stage báo cáo riêng từng loại dataset shift: covariate shift, label shift và concept drift. | Ba loại shift cần xử lý khác nhau; gộp lại làm mờ nguyên nhân. | BR-85 | Must | T |
| FR-115 | Hệ thống phải để dictionary ghi thời điểm mỗi biến sẵn có. | Biết biến nào có mặt lúc triển khai. | BR-88 | Must | T |
| FR-184 | Hệ thống phải gắn cờ post-outcome cho biến được ghi sau outcome. | Biến ghi sau outcome gây leakage nhưng không có lúc triển khai. | BR-88 | Must | T |
| FR-116 | Hệ thống phải để dataset stage kiểm dòng trùng lặp giữa các phần split và báo cáo kết quả. | Dòng trùng làm kết quả lạc quan giả. | BR-88 | Must | T |
| FR-117 | Hệ thống phải để dataset stage gắn cờ tín hiệu dữ liệu (tỷ lệ positive thấp, categorical có cardinality cao, cột group hoặc thời gian, missingness cao). | Cờ tín hiệu giúp chọn pattern phù hợp dữ liệu. | BR-89; BR-26 | Must | T |
| FR-185 | Hệ thống phải để dataset stage gợi ý research pattern từ cờ tín hiệu, và để Researcher chọn pattern qua việc chọn hypothesis (FR-27). | AI gợi ý, người quyết định. | BR-89; BR-26 | Must | T |
| FR-118 | Hệ thống phải để prefilter của dataset stage chỉ dùng phân phối biên và không dùng quan hệ giữa biến và outcome. | Gợi ý không làm lộ kết quả; blind analysis được giữ. | BR-89 | Must | T |

## FE-07 — Hypothesis stage and Literature Base

**Mục đích:** Rà soát literature có phương pháp và tạo HypothesisSet có evidence. **Actor:** Researcher; Persona (hypothesis). **Journey:** J1. **Tiêu chí chấp nhận:** Acceptance scenario của hypothesis stage (§11.1) đạt; HypothesisSet có ít nhất hai hypothesis và một primary.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-43 | Hệ thống phải dựng và cập nhật Literature Base cấp project có version, từ metadata, abstract và full text open access, gồm protocol tìm kiếm, search log, quyết định sàng lọc, evidence card, evidence map do code dựng và BibTeX đã kiểm. | Evidence dùng chung cho mọi stage, có provenance. | BR-41 | Must | D |
| FR-186 | Hệ thống phải ghi lỗi theo nguồn, tiếp tục nguồn khác và ghi gap nếu mọi nguồn literature lỗi. | Một nguồn lỗi không dừng rà soát. | BR-41 | Must | T |
| FR-44 | Hệ thống phải để hypothesis stage tạo HypothesisSet gồm ít nhất hai hypothesis có claim key khác nhau và một primary. | Tránh khoá vào một giả thuyết duy nhất. | BR-45 | Must | T |
| FR-45 | Hệ thống phải yêu cầu mỗi hypothesis có estimand nháp, biến, confounder có nguồn, SESOI, câu bác bỏ, loại đóng góp và nguồn gốc. | Hypothesis kiểm được và bác bỏ được. | BR-45 | Must | T |
| FR-119 | Hệ thống phải yêu cầu mỗi hypothesis có comparator, primary metric khớp task family, hướng hoặc margin, phạm vi và decision rule. | Hypothesis kiểm được và bác bỏ được. | BR-90 | Must | T |
| FR-120 | Hệ thống phải trả về để sửa hypothesis không có comparator. | Mệnh đề "model tốt hơn" không có đối chứng không kiểm được. | BR-90; BR-99 | Must | T |
| FR-187 | Hệ thống phải không chấp nhận baseline cố ý yếu. | Baseline yếu làm kết quả lạc quan giả. | BR-90; BR-99 | Must | T |
| FR-121 | Hệ thống phải ánh xạ margin non-inferiority hoặc equivalence (δ) lên các vùng SESOI của verdict. | Equivalence cần margin định trước. | BR-91; BR-54 | Must | T |
| FR-122 | Hệ thống phải không kết luận equivalence từ p-value không có ý nghĩa thống kê. | Không có bằng chứng khác biệt không phải bằng chứng tương đương. | BR-91 | Must | T |
| FR-123 | Hệ thống phải giữ portfolio hypothesis gồm một primary và một số secondary không vượt giới hạn do project settings quy định (mặc định 3 secondary). | Giảm nhiễu từ nhiều so sánh. | BR-92 | Must | T |

## FE-08 — Experiment design stage and Lock

**Mục đích:** Lập AnalysisPlan cho dữ liệu bảng có sẵn và khoá plan bằng Lock. **Actor:** Researcher; Persona (experiment_design). **Journey:** J3. **Tiêu chí chấp nhận:** Acceptance scenario của experiment_design stage (§11.1) đạt; Lock ghi đủ hash.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-46 | Hệ thống phải để experiment_design stage tạo AnalysisPlan cho dữ liệu bảng có sẵn, gồm estimand, protocol theo loại claim, adjustment set, analysis program, fallback, decision rule, bảng diễn giải, robustness set, design diagnosis và cấu trúc họ giả thuyết. | Plan đủ để chạy và kiểm mà không quyết thêm. | BR-46 | Must | T |
| FR-47 | Hệ thống phải chạy analysis program trên twin dựng từ aggregate đã release trước khi plan được lock. | Sửa lỗi trước khi ai thấy ước lượng thật. | BR-50 | Must | T |
| FR-48 | Hệ thống phải để Platform ghi Lock khi user lock plan, gồm hash của spec, program và golden outputs, snapshot version, split digest, ai khoá và khi nào. | Plan cố định trước khi chạy confirmatory. | BR-47; BR-26 | Must | T |
| FR-188 | Hệ thống phải giữ object đã lock bất biến. | Thay đổi sau lock chỉ qua deviation. | BR-47; BR-26 | Must | T |
| FR-49 | Hệ thống phải giữ plan ở trạng thái chờ lock khi user `away`. | Lock là action pinned. | BR-26; BR-31 | Must | T |
| FR-189 | Hệ thống phải không cho ai lock thay user. | Quyết định lock thuộc về user. | BR-26; BR-31 | Must | T |
| FR-124 | Hệ thống phải ghi task family (`binary`, `multiclass`, `regression`, `rare-event`) vào AnalysisPlan. | Metric và protocol đúng với loại bài toán. | BR-83 | Must | T |
| FR-190 | Hệ thống phải dùng task family để chọn metric policy và protocol cho `prediction`. Phần `method_comparison`: FR-268 (FE-19, sau MVP). | Metric và protocol đúng với loại bài toán. | BR-83 | Must | T |
| FR-191 | Hệ thống phải dùng task family để chọn model family cho `association` và `causal`. | Model family đúng với loại outcome. | BR-83 | Must | T |
| FR-125 | Hệ thống phải giữ research pattern registry; mỗi pattern là một đơn vị có version gồm task family áp dụng, eligibility rule, cột bắt buộc, baseline policy, factor template, metric policy, chart template, statistical plan, failure mode và các action cần người (dùng lại action pinned, FR-27). | Pattern dùng lại được và kiểm được; không thêm điểm chặn mới. | BR-95; BR-26 | Must | T |
| FR-192 | Hệ thống phải để AnalysisPlan ghi research pattern đã chọn cùng version. | Plan truy được về pattern đã dùng. | BR-95; BR-26 | Must | T |
| FR-126 | Hệ thống phải cho `prediction` dùng pattern A–E và K–O. | Phạm vi pattern theo claim type. | BR-96 | Must | T |
| FR-193 | Hệ thống phải cho `prediction` dùng pattern F làm baseline policy. Phần `method_comparison`: FR-269 (FE-19, sau MVP). | `prediction` cần baseline. | BR-96 | Must | T |
| FR-127 | Hệ thống phải để AnalysisPlan ghi pipeline order: split trước; mọi bước học từ dữ liệu chỉ fit trong phần train; resampling chỉ trên phần train; calibration và threshold chọn trên phần validation; phần confirmation dùng một lần. | Chống leakage từ tiền xử lý. | BR-86 | Must | T |
| FR-128 | Hệ thống phải để AnalysisPlan của `prediction` có ba evidence family theo thứ tự: discrimination, reliability (calibration, stress, uncertainty), decision (threshold, cost, subgroup). Phần `method_comparison`: FR-267 (FE-19, sau MVP). | Một metric không đủ để kết luận. | BR-93 | Must | T |
| FR-129 | Hệ thống phải dùng, với task family `rare-event`, average precision (AP) hoặc precision tại recall cố định làm metric, không chỉ accuracy. | Accuracy che lỗi trên lớp hiếm. | BR-94 | Must | T |
| FR-130 | Hệ thống phải không so sánh AP giữa các tập có prevalence khác nhau. | AP phụ thuộc prevalence. | BR-94 | Must | T |
| FR-131 | Hệ thống phải dùng dữ liệu tách khỏi dữ liệu huấn luyện cho calibration. | Calibration trên dữ liệu huấn luyện cho kết quả lạc quan giả. | BR-94; BR-86 | Must | T |
| FR-132 | Hệ thống phải áp baseline policy (pattern F): baseline đơn giản chạy trước, trên cùng split. | So sánh công bằng. | BR-99 | Must | T |
| FR-195 | Hệ thống phải dùng cùng tuning budget cho baseline và phương pháp được so sánh. | Tuning budget khác nhau làm so sánh lệch. | BR-99 | Must | T |
| FR-196 | Hệ thống phải báo cáo runtime cùng điểm số của baseline. | Điểm số không đủ để so sánh chi phí. | BR-99 | Must | T |

## FE-09 — Execution stage

**Mục đích:** Chạy plan đã lock, giữ kết quả confirmatory trong envelope, unseal, và tính verdict, grade, claim ceiling bằng code. **Actor:** Researcher; Persona (execution). **Journey:** J4. **Tiêu chí chấp nhận:** Acceptance scenario của execution stage (§11.1) đạt; 0 ước lượng confirmatory trước unseal.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-50 | Hệ thống phải chạy execution trong sandbox. | Code của agent không chạm hệ thống ngoài sandbox. | BR-50 | Must | T |
| FR-197 | Hệ thống phải cho agent làm việc tự do trên twin và chỉ cho chạm dữ liệu thật qua aggregate hoặc chương trình đầy đủ. | Agent không thấy hàng thật. | BR-50 | Must | T |
| FR-198 | Hệ thống phải cho dry run trên dữ liệu thật chỉ trả số hàng, kiểu, missingness, hội tụ và thời gian, không trả ước lượng. | Agent không thấy ước lượng sớm. | BR-50 | Must | T |
| FR-51 | Hệ thống phải đưa kết quả confirmatory vào envelope ở Platform. | Kết quả confirmatory nằm ngoài tầm với của agent. | BR-49 | Must | T |
| FR-199 | Hệ thống phải chỉ cho agent thấy done hoặc error trước unseal. | Chặn p-hacking. | BR-49 | Must | T |
| FR-52 | Hệ thống phải unseal tự động khi mọi check xanh, trừ khi user đã chọn unseal bằng tay trước. | Mặc định không chặn run; user có quyền nâng mức. | BR-49 | Must | T |
| FR-53 | Hệ thống phải mở mọi hypothesis của một Lock cùng lúc khi unseal. | Không chọn hypothesis theo kết quả. | BR-49 | Must | T |
| FR-200 | Hệ thống phải ghi thời điểm unseal. | Truy vết thời điểm mở kết quả. | BR-49 | Must | T |
| FR-201 | Hệ thống phải từ chối unseal đến sớm hơn lần sửa lane C cuối. | Không mở kết quả khi còn sửa lane C. | BR-49 | Must | T |
| FR-54 | Hệ thống phải để code tính verdict của mỗi hypothesis theo decision rule đã lock (`supported`, `trivial`, `not_supported`, `insufficient`, `not_tested`). | Model không tạo verdict. | BR-54 | Must | T |
| FR-202 | Hệ thống phải lấy lời kết luận từ interpretation row tương ứng với verdict. | Lời kết luận khớp verdict. | BR-54 | Must | T |
| FR-55 | Hệ thống phải để code tính grade A–D từ diagnostics, robustness và deviation. | Mức tin cậy có nguồn tính toán. | BR-55; BR-56 | Must | T |
| FR-203 | Hệ thống phải để execution stage tính claim ceiling từ verdict, grade và confirmation tier. | Mức claim cho phép có nguồn tính toán. | BR-55; BR-56 | Must | T |
| FR-204 | Hệ thống phải không coi plan đã lock là claim đã được chứng minh. | Lock chỉ cố định plan, không chứng minh claim. | BR-55; BR-56 | Must | T |
| FR-56 | Hệ thống phải xem mọi thay đổi thuật toán đã lock là deviation và là action pinned. | Lệch khỏi plan phải do user quyết. | BR-48; BR-26 | Must | T |
| FR-205 | Hệ thống phải ghi mỗi deviation vào deviation log và tính vào grade. | Lệch khỏi plan phải thấy được. | BR-48; BR-26 | Must | T |
| FR-57 | Hệ thống phải giữ lane E chỉ trên exploration split, không chạm confirmatory split. | Khám phá không làm hỏng xác nhận. | BR-51 | Must | T |
| FR-206 | Hệ thống phải không dùng validation source trong lane E. | Validation source chỉ dùng khi user quyết. | BR-51 | Must | T |
| FR-207 | Hệ thống phải đưa mỗi candidate của lane E vào decision inbox để user chọn mà không đưa thẳng vào plan. | Candidate không bao giờ là claim. | BR-51 | Must | T |
| FR-58 | Hệ thống phải ghi mọi thủ tục tìm kiếm của lane E và của user vào tried ledger cùng ngưỡng nhiễu. | Càng tìm nhiều, ngưỡng càng cao. | BR-52 | Must | T |
| FR-208 | Hệ thống phải nâng ngưỡng cho candidate sau khi số thủ tục tìm kiếm tăng. | Tìm nhiều làm tăng kết quả đẹp do may rủi. | BR-52 | Must | T |
| FR-59 | Hệ thống phải gán cho mỗi candidate được xác nhận một confirmation tier (`replicated`, `reserve`, `unsealed_untouched`, `unsealed_touched`). | Mức xác nhận có thứ bậc. | BR-53 | Must | T |
| FR-209 | Hệ thống phải chỉ ghi evidence e-value vào claim ledger cho kết quả confirmatory và cho candidate ở tier `replicated` hoặc `reserve`. | Chỉ hàng chưa dùng để khám phá cho evidence e-value hợp lệ. | BR-53 | Must | T |
| FR-272 | Hệ thống phải gán evidence rows (`confirmatory`, `reserve` hoặc validation source theo hash) cho mỗi record có evidence e-value, bằng code. | Ledger cần biết hai record có dùng chung hàng hay không. | BR-53; BR-105 | Must | T |
| FR-273 | Hệ thống phải nhân evidence e-value của một claim key chỉ giữa các nhóm hàng độc lập, mỗi nhóm một record (record đầu tiên), và đánh dấu claim key `promoted` khi tích từ 1/α, với α là setting. | Cùng hàng đếm hai lần, hoặc chọn record lớn nhất, làm mất kiểm soát sai lầm. | BR-105 | Must | T |
| FR-60 | Hệ thống phải đưa replication package (code hash, environment, dữ liệu, seed, split) vào EvidenceBundle. | Replay cần đủ đầu vào. | BR-57 | Must | T |
| FR-210 | Hệ thống phải để replicator tái lập kết quả của EvidenceBundle. | Kết quả tái lập được. | BR-57 | Must | T |
| FR-211 | Hệ thống phải đánh đỏ item của bundle khi kết quả tái lập lệch. | Phát hiện lệch. | BR-57 | Must | T |
| FR-61 | Hệ thống phải để execution stage tạo EvidenceBundle gồm mười item có check: kết quả xác nhận, verdict và dòng diễn giải, grade, diagnostics, robustness, deviation log, tried ledger và candidate, bảng và hình, replication package, báo cáo replicator và envelope log. | Hand-off của execution phải đủ cho paper stage. | BR-11; BR-54; BR-55; BR-57 | Must | T |
| FR-133 | Hệ thống phải để guard của execution chặn vi phạm pipeline order (FR-127) trước khi chạy, hoặc ghi vi phạm là deviation. | Vi phạm không âm thầm vào kết quả. | BR-87; BR-86 | Must | T |

## FE-10 — Paper stage

**Mục đích:** Soạn PaperPack mà đội viết bài dùng được mà không phải dẫn xuất lại số liệu. **Actor:** Researcher; Persona (paper). **Journey:** J7. **Tiêu chí chấp nhận:** Acceptance scenario của paper stage (§11.1) đạt; 0 chữ số không phải tham chiếu.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-62 | Hệ thống phải để paper stage tạo PaperPack gồm mười item có check (reporting checklist, manuscript, claims, figures và tables, citations, limitations, reproducibility, declarations, review, formats) từ EvidenceBundle, AnalysisPlan và Lock, Literature Base, DatasetSnapshot và decision log. | Đội viết bài nhận gói đủ, không phải dẫn xuất lại. | BR-65 | Must | T |
| FR-63 | Hệ thống phải render mọi con số trong manuscript và trên hình từ record của EvidenceBundle. | Không có số do model viết. | BR-66; BR-71 | Must | T |
| FR-212 | Hệ thống phải đánh đỏ check khi text của model có chữ số không phải tham chiếu (trừ năm, số mục, số section). | Chữ số lạ bị bắt bằng máy. | BR-66; BR-71 | Must | T |
| FR-64 | Hệ thống phải ánh xạ mọi effect statement trong Abstract, Results và Discussion tới verdict và interpretation row. | Bản thảo không nói quá kết quả. | BR-67; BR-56 | Must | T |
| FR-213 | Hệ thống phải giữ từ chỉ mức claim khớp verdict. | Từ chỉ mức claim không mạnh hơn verdict. | BR-67; BR-56 | Must | T |
| FR-214 | Hệ thống phải không để claim vượt claim ceiling. | Claim ceiling là trần của bản thảo. | BR-67; BR-56 | Must | T |
| FR-65 | Hệ thống phải bảo đảm mọi citation nằm trong Literature Base. | Không có citation bịa. | BR-68 | Must | T |
| FR-215 | Hệ thống phải bảo đảm mọi citation có DOI đã resolve. | Citation tồn tại thật. | BR-68 | Must | T |
| FR-216 | Hệ thống phải bảo đảm mọi citation có trích dẫn hỗ trợ cho claim mà nó đỡ. | Không có citation lệch. | BR-68 | Must | T |
| FR-66 | Hệ thống phải bảo đảm limitations nêu mọi lý do grade, gap, known risk, deviation, kết quả negative control, power thấp và kết quả nhạy cảm với confounding. | Không giấu hạn chế. | BR-69 | Must | T |
| FR-217 | Hệ thống phải để code kiểm độ phủ của limitations. | Độ phủ kiểm được bằng máy. | BR-69 | Must | T |
| FR-67 | Hệ thống phải đặt các trường chỉ tác giả (authors, affiliation, ethics, funding, conflicts, CRediT) là placeholder "awaiting author". | Hệ thống không bịa thông tin của tác giả. | BR-70 | Must | T |
| FR-218 | Hệ thống phải lấy câu khai báo dùng AI từ decision log. | Khai báo dùng AI có nguồn. | BR-70 | Must | T |
| FR-68 | Hệ thống phải lập reporting checklist theo loại claim (STROBE + RECORD cho association và causal; TRIPOD cho prediction). | Báo cáo theo chuẩn của loại claim. | BR-71 | Must | T |
| FR-219 | Hệ thống phải để mỗi mục của reporting checklist trỏ tới anchor trong bài hoặc ghi "awaiting author" hay "not applicable" kèm lý do. | Mỗi mục checklist kiểm được. | BR-71 | Must | T |
| FR-220 | Hệ thống phải đưa vào PaperPack ít nhất ba hình chính. | Bản thảo có hình chính làm bằng chứng. | BR-71 | Must | T |
| FR-69 | Hệ thống phải áp writing rule theo ba loại: H (vi phạm là lỗi), M (vượt ngưỡng thành issue), G (nằm trong rubric reviewer). Nội dung từng rule: chưa xác định (Câu hỏi mở 2). | Văn phong kiểm được. | BR-72 | Must | I |
| FR-70 | Hệ thống phải để Researcher quyết định nộp bài và không tự nộp bài cho publisher. | Quyết định nộp bài thuộc người. | BR-73 | Must | I |

## FE-11 — Independent review loop and personas

**Mục đích:** Review độc lập bắt buộc cho mọi object version, với finding đã kiểm và tối đa hai vòng sửa. **Actor:** Persona (guard); Researcher. **Journey:** J2, J4. **Tiêu chí chấp nhận:** Review loop chạy một lần cho mỗi object version và dừng sau tối đa hai vòng sửa.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-71 | Hệ thống phải chạy review loop ở mọi stage, một lần cho mỗi object version, sau khi mọi check xanh. | Review độc lập bắt buộc. | BR-35 | Must | T |
| FR-72 | Hệ thống phải chạy reviewer với context mới và không cho reviewer thấy trace của tác giả. | Tránh reviewer cùng bias với tác giả. | BR-36 | Must | T |
| FR-221 | Hệ thống phải chạy các guard song song và không cho guard đọc nhau. | Guard độc lập với nhau. | BR-36 | Must | T |
| FR-73 | Hệ thống phải yêu cầu mỗi finding có category, severity (`blocking`, `major`, `minor`), anchor, evidence, failure scenario và cách sửa. | Finding kiểm được và sửa được. | BR-37 | Must | T |
| FR-222 | Hệ thống phải loại finding thiếu anchor hoặc evidence. | Finding không kiểm được không vào vòng sửa. | BR-37 | Must | T |
| FR-74 | Hệ thống phải kiểm mỗi finding bằng code hoặc verifier thứ hai (`confirmed`, `plausible`, `rejected`) trước khi sửa. | Không sửa theo finding sai. | BR-38 | Must | T |
| FR-223 | Hệ thống phải chỉ cho finding `blocking` đã `confirmed` vào vòng sửa. | Vòng sửa chỉ xử lý lỗi chắc chắn. | BR-38 | Must | T |
| FR-224 | Hệ thống phải ghi và hiển thị finding không vào vòng sửa. | Finding khác không bị giấu. | BR-38 | Must | T |
| FR-75 | Hệ thống phải giới hạn tối đa hai vòng sửa. | Review không kéo dài vô hạn. | BR-39 | Must | T |
| FR-225 | Hệ thống phải hiển thị finding còn lại sau hai vòng sửa là known risk, hoặc để user quyết định giữa hai phía. | Phần chưa giải quyết được thấy rõ. | BR-39 | Must | T |
| FR-76 | Hệ thống phải từ chối object chỉ khi provenance hoặc contract hỏng. | Traceable, không đòi hoàn hảo. | BR-42 | Must | T |
| FR-226 | Hệ thống phải thử lại vấn đề nội dung khác, rồi giữ như finding hoặc known risk. | Vấn đề nội dung không chặn run. | BR-42 | Must | T |
| FR-227 | Hệ thống phải không publish evidence không resolve được. | Không có evidence không truy được. | BR-42 | Must | T |
| FR-77 | Hệ thống phải đo precision của từng persona reviewer trên seeded-flaw bench. | Mỗi persona phải có giá trị đo được. | BR-40 | Must | A |
| FR-228 | Hệ thống phải hạ severity finding của reviewer có precision dưới mức tối thiểu. | Reviewer kém không chặn tiến độ. | BR-40 | Must | T |
| FR-229 | Hệ thống phải chỉ bật persona khi bench cho thấy nó bắt được điều persona khác bỏ sót. | Không thêm persona không có giá trị. | BR-40 | Must | A |
| FR-78 | Hệ thống phải cho user gọi mọi persona trên mọi object. | User chủ động kiểm tra. | BR-40 | Must | T |
| FR-134 | Hệ thống phải có negative test cho mỗi research pattern: ca cài sẵn lỗi mà pattern phải phát hiện. | Đo năng lực phát hiện lỗi của từng pattern. | BR-97 | Must | T |
| FR-135 | Hệ thống phải đưa red-team catalogue vào seeded-flaw bench, gồm ba nhóm lỗi cài sẵn: dữ liệu (cột post-outcome, trùng lặp giữa các phần split, nhãn positive sai, leakage theo thời gian, target encoding fit trên toàn dữ liệu, proxy của thuộc tính được bảo vệ), thí nghiệm (resampling trước split, tuning budget không bằng nhau, chọn feature bằng phần test, early stopping trên phần test, thiếu seed, chọn lọc run đẹp) và suy luận (equivalence từ p lớn hơn 0,05, causal claim từ feature attribution, so AP giữa các prevalence khác nhau, không báo cáo uncertainty). | Đo reviewer và guard trên lỗi khoa học có tên. | BR-100; BR-40 | Must | A |
| FR-136 | Hệ thống phải đo tỷ lệ phát hiện leakage cài sẵn (SM-17) trên seeded-flaw bench. | Leakage bị bỏ sót làm hỏng mọi kết luận sau đó. | BR-100 | Must | A |
| FR-137 | Hệ thống phải đo tỷ lệ chặn vi phạm pipeline order cài sẵn trước khi chạy (SM-18) trên seeded-flaw bench. | Guard phải chặn được lỗi có tên. | BR-100 | Must | A |
| FR-138 | Hệ thống phải có benchmark case catalogue gồm 60 project mẫu (PRD §11.2.1), mỗi project là một ca kiểm thử của research pattern, để Report V dẫn xuất test case. | Test case có nguồn; không có 60 flow riêng lẻ. | BR-101 | Must | I |
| FR-270 | Hệ thống phải chỉ chấp nhận finding `blocking` mới trên field không đổi sau một lần sửa khi evidence của finding là một fact tính mới. | Vòng sửa không kéo dài bằng finding không có bằng chứng mới. | BR-39; BR-37 | Must | T |
| FR-271 | Hệ thống phải review lại sau mỗi lần sửa chỉ trên finding đã sửa và field đã đổi. | Review lặp lại có phạm vi hẹp; vòng sửa không mở lại toàn object. | BR-39 | Must | T |

## FE-12 — Local Node

**Mục đích:** Giữ dữ liệu `local` trên máy user, chạy job cạnh dữ liệu và chỉ release aggregate qua release gate. **Actor:** Researcher; Project Manager. **Journey:** J5. **Tiêu chí chấp nhận:** Acceptance scenario của Local Node (§11.1) đạt; 0 hàng dữ liệu trong message ra ngoài.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-79 | Hệ thống phải cung cấp Local Node giữ dữ liệu `local` và chạy job cạnh dữ liệu. | Dữ liệu nhạy cảm ở lại máy chủ dữ liệu. | BR-18 | Must | D |
| FR-230 | Hệ thống phải không đòi user cài Docker để dùng Local Node. | User không cần kiến thức hạ tầng. | BR-18 | Must | D |
| FR-80 | Hệ thống phải không để hàng dữ liệu rời nơi giữ dữ liệu. | Hàng dữ liệu riêng không rời đi. | BR-19 | Must | T |
| FR-231 | Hệ thống phải chỉ cho aggregate (release) rời đi, qua một release gate duy nhất gồm ngưỡng ô nhỏ, làm tròn, kiểm tra differencing và probe budget. | Một điểm kiểm duy nhất cho privacy. | BR-19 | Must | T |
| FR-81 | Hệ thống phải ghi mọi release của một dataset version vào release log chỉ-thêm. | IT của đơn vị kiểm được mọi số đã rời đi. | BR-20 | Must | T |
| FR-232 | Hệ thống phải giữ bản Platform khớp với release log của Local Node. | Hai bên cùng một lịch sử release. | BR-20 | Must | T |
| FR-82 | Hệ thống phải cho release tự động trong policy ở disclosure `standard`. | Chủ dữ liệu chọn mức nghiêm. | BR-21; BR-80 | Must | T |
| FR-233 | Hệ thống phải ở disclosure `strict`, chỉ cho các loại số đã duyệt và tạo item release review trong decision inbox cho loại khác. | Chủ dữ liệu giữ quyền với loại số mới. | BR-21; BR-80 | Must | T |
| FR-234 | Hệ thống phải để Researcher hoặc Project Manager của project trả lời item release review. | Có người trả lời rõ ràng. | BR-21; BR-80 | Must | T |
| FR-83 | Hệ thống phải không gửi hàng dữ liệu cho model hay artifact đã publish; model chỉ nhận aggregate và profile do code tính. | Model không nhận dữ liệu riêng. | BR-22 | Must | T |
| FR-235 | Hệ thống phải chỉ trả loại lỗi, cột và số hàng ảnh hưởng cho exception từ dữ liệu thật. | Thông báo lỗi không làm lộ hàng dữ liệu. | BR-22 | Must | T |
| FR-84 | Hệ thống phải để Local Node kiểm hash của dataset version và từ chối job khi hash không khớp. | Job chỉ chạy trên dữ liệu đã ghim. | BR-16; BR-18 | Must | T |
| FR-236 | Hệ thống phải đề xuất version mới khi hash không khớp. | User biết bước tiếp theo. | BR-16; BR-18 | Must | T |
| FR-85 | Hệ thống phải đưa run vào `waiting(node_offline)` khi job local chặn việc và Local Node offline. | Run không treo vì máy user tắt. | BR-14; BR-27 | Must | T |
| FR-237 | Hệ thống phải tiếp tục việc không cần dữ liệu khi run ở `waiting(node_offline)`. | Chờ Node không làm dừng việc khác. | BR-14; BR-27 | Must | T |
| FR-238 | Hệ thống phải gửi một thông báo gộp khi run vào `waiting(node_offline)`. | Tránh thông báo lặp. | BR-14; BR-27 | Must | T |
| FR-86 | Hệ thống phải xử lý probe budget cạn của một dataset version là gap, không dừng run. | Giới hạn suy luận từ nhiều aggregate mà vẫn kết thúc run. | BR-19; BR-14 | Must | T |
| FR-239 | Hệ thống phải hiển thị mọi query bị từ chối cùng lý do. | User biết vì sao thiếu số. | BR-19; BR-14 | Must | T |
| FR-87 | Hệ thống phải cho user ghép Local Node với project bằng mã ghép. | User không cần cấu hình thủ công. | BR-18 | Must | D |
| FR-240 | Hệ thống phải đề xuất dataset từ thư mục mà Local Node theo dõi. | User không phải khai báo từng dataset. | BR-18 | Must | D |
| FR-110 | Hệ thống phải từ chối job cho dữ liệu `local` của Node khi Local Node bị thu hồi. | Node bị thu hồi không chạy job. | BR-81 | Must | T |
| FR-241 | Hệ thống phải báo user lý do khi từ chối job vì Node bị thu hồi. | User biết nguyên nhân. | BR-81 | Must | T |
| FR-242 | Hệ thống phải giữ object đã publish đọc được khi Local Node bị thu hồi. | Kết quả cũ không mất. | BR-81 | Must | T |

## FE-13 — Budget and cost

**Mục đích:** Kiểm soát token budget của run và budget tháng của project; run luôn kết thúc. **Actor:** Project Manager; Platform Admin. **Journey:** J6. **Tiêu chí chấp nhận:** Budget tháng 100% chặn run mới và tạo item `spending`; run vượt budget kết thúc `with_gaps`.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-88 | Hệ thống phải đặt cho mỗi run một token budget tính bằng token. | Chi phí run có trần. | BR-58 | Must | T |
| FR-243 | Hệ thống phải kết thúc run `ended(with_gaps)` trên output tốt nhất khi token budget của run hết. | Run không treo. | BR-58 | Must | T |
| FR-89 | Hệ thống phải cảnh báo ở các ngưỡng của budget tháng của project. | Chi phí project có trần. | BR-59 | Must | T |
| FR-244 | Hệ thống phải chặn run mới khi budget tháng của project chạm 100%. | Không chi vượt trần khi chưa có quyết định. | BR-59 | Must | T |
| FR-90 | Hệ thống phải chuyển run đang chạy sang `waiting(budget_review)` và tạo item `spending` `must_ask` khi project chạm 100% budget tháng. | Người có thẩm quyền quyết định chi thêm; không mất công việc. | BR-60 | Must | T |
| FR-245 | Hệ thống phải cho Project Manager duyệt chi thêm để run chạy tiếp, hoặc để run kết thúc `with_gaps`. | Project Manager quyết định chi tiêu. | BR-60 | Must | T |
| FR-91 | Hệ thống phải gán hạn trả lời cho item `spending`. | Run không treo chờ chi tiêu. | BR-78; BR-28 | Must | T |
| FR-246 | Hệ thống phải gửi thông báo ngoài (mail, push) cho Project Manager khi item `spending` được tạo và nhắc trước hạn. | Project Manager biết có item chờ. | BR-78; BR-28 | Must | T |
| FR-247 | Hệ thống phải kết thúc run `with_gaps` khi hạn trả lời hết mà chưa có quyết định. | Run kết thúc, không treo. | BR-78; BR-28 | Must | T |
| FR-92 | Hệ thống phải chặn chi tiêu `auto` vượt mức trần chi tiêu do Platform Admin đặt, ở mọi preset. | Không preset nào vượt trần. | BR-61 | Must | T |
| FR-248 | Hệ thống phải chỉ cho chi tiêu `auto` dưới mức trần ở preset `autopilot`. | Chi tiêu tự động có giới hạn. | BR-61 | Must | T |
| FR-93 | Hệ thống phải giữ usage và cost ledger theo run và theo project. | Chi phí truy vết được. | BR-61 | Must | T |

## FE-14 — Dossier, approval and export

**Mục đích:** Gom kết quả thành Dossier có version, duyệt theo review settings và chỉ cho export khi đã duyệt. **Actor:** Reviewer; Project Manager; Researcher. **Journey:** J7. **Tiêu chí chấp nhận:** Export bị từ chối khi Dossier chưa duyệt; Dossier version mới cần duyệt lại.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-94 | Hệ thống phải tạo Dossier khi run có PaperPack accepted (không tạo khi run kết thúc `with_gaps` hoặc `cancelled` trước khi có PaperPack accepted), gồm tham chiếu tới các version EvidenceBundle và PaperPack đã accepted. | Không có bản sao nội dung để lệch. | BR-62 | Must | T |
| FR-249 | Hệ thống phải kiểm hash của từng tham chiếu trong Dossier. | Dossier phát hiện tham chiếu bị đổi. | BR-62 | Must | T |
| FR-250 | Hệ thống phải chỉ đánh version, kiểm hash và ghi duyệt, và không đánh giá khoa học. | Platform không phán xét khoa học. | BR-62 | Must | T |
| FR-95 | Hệ thống phải ghi Approval của Reviewer hoặc Project Manager theo review settings: số approval, ai được duyệt, có cho tự duyệt không. | Quyền duyệt cấu hình theo project. | BR-63 | Must | T |
| FR-96 | Hệ thống phải tạo Dossier version mới khi EvidenceBundle hoặc PaperPack có version accepted mới. | Dossier theo kịp nội dung. | BR-79 | Must | T |
| FR-251 | Hệ thống phải gắn mỗi Approval với một Dossier version. | Approval không chuyển sang nội dung khác. | BR-79 | Must | T |
| FR-252 | Hệ thống phải yêu cầu duyệt lại Dossier version mới. | Nội dung mới cần người duyệt. | BR-79 | Must | T |
| FR-97 | Hệ thống phải chỉ cho export ra ngoài project khi Dossier đã được duyệt. | Kết quả không rời project khi chưa có người duyệt. | BR-64 | Must | T |
| FR-253 | Hệ thống phải xem export là action pinned. | Export luôn cần quyết định của user. | BR-64 | Must | T |
| FR-98 | Hệ thống phải ghi mỗi export vào audit log cùng version Dossier và định dạng. | Truy vết cái gì đã rời project. | BR-05; BR-64 | Must | T |

## FE-15 — Collaboration (comments, notifications)

**Mục đích:** Cho member bình luận và nhận thông báo quanh cùng một run. **Actor:** Mọi member. **Journey:** J7. **Tiêu chí chấp nhận:** Reviewer bình luận được mọi object; member nhận notification theo settings.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-99 | Hệ thống phải cho Reviewer đọc và bình luận mọi object của project. | Cộng tác quanh cùng một run. | BR-05; BR-06 | Must | T |
| FR-254 | Hệ thống phải cho Project Manager và Researcher bình luận theo role. | Cộng tác quanh cùng một run. | BR-05; BR-06 | Must | T |
| FR-100 | Hệ thống phải gửi notification cho member về sự kiện của project theo notification settings. | Member không bỏ lỡ việc cần làm. | BR-05; BR-28 | Must | T |
| FR-255 | Hệ thống phải chỉ gửi thông báo ngoài cho item pinned đang chặn và item `spending`. | Giảm thông báo gây mệt. | BR-05; BR-28 | Must | T |

## FE-17 — Administration and monitoring

**Mục đích:** Cho Platform Admin quản lý user, model, key, audit và theo dõi vận hành. **Actor:** Platform Admin. **Journey:** J6. **Tiêu chí chấp nhận:** Platform Admin quản lý được model và key mà key không xuất hiện trong log.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-101 | Hệ thống phải cho Platform Admin quản lý user, model profile theo model role (`stage`, `review`, `vision`), key, engine settings và budget mặc định. | Cấu hình tập trung ở Platform. | BR-02; BR-23 | Must | D |
| FR-102 | Hệ thống phải seal model key và secret tích hợp ở Platform. | Bảo vệ secret. | BR-23 | Must | T |
| FR-256 | Hệ thống phải không để model key và secret tích hợp xuất hiện trong prompt, log hoặc output. | Secret không rò qua đầu ra. | BR-23 | Must | T |
| FR-103 | Hệ thống phải kết thúc run `ended(failed_technical)` với lỗi rõ ràng khi thiếu model hoặc credential. | User biết cần cấu hình gì. | BR-14 | Must | T |
| FR-257 | Hệ thống phải không tạo output giả khi thiếu model hoặc credential. | Không có kết quả mẫu giả làm thật. | BR-14 | Must | T |
| FR-104 | Hệ thống phải cho Platform Admin xem audit log của hệ thống. | Vận hành và điều tra. | BR-05 | Must | D |
| FR-258 | Hệ thống phải cho Platform Admin xem health của các thành phần. | Vận hành phát hiện sự cố. | BR-05 | Must | D |
| FR-105 | Hệ thống phải báo cho mỗi run số question, thời gian bị chặn và overturn rate theo action type. | Đo chất lượng kiểm soát. | BR-29; BR-40 | Must | A |
| FR-259 | Hệ thống phải báo precision của persona trên seeded-flaw bench. | Đo chất lượng review. | BR-29; BR-40 | Must | A |

## FE-18 — Journal Fingerprint Extraction (JFE)

**Mục đích:** Dựng profile tạp chí có bằng chứng để paper stage tham chiếu (sau MVP). **Actor:** Researcher. **Journey:** J7. **Tiêu chí chấp nhận:** (Sau MVP) Mỗi feature của profile truy được về corpus snapshot và span.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-106 | Hệ thống phải dựng journal profile từ corpus được phép dùng, gồm nguồn, quyền sử dụng, độ bất định và version. | Profile có bằng chứng. | BR-74 | Could | T |
| FR-107 | Hệ thống phải truy mỗi feature của journal profile về corpus snapshot và span nguồn. | Tách cảm tính khỏi bằng chứng. | BR-74 | Could | T |
| FR-260 | Hệ thống phải phân biệt thông lệ quan sát được với quy định bắt buộc của publisher trong journal profile. | Researcher biết đâu là quy định. | BR-74 | Could | T |
| FR-108 | Hệ thống phải cho Researcher duyệt journal profile. | Researcher chịu trách nhiệm chọn tạp chí. | BR-74 | Could | T |
| FR-261 | Hệ thống phải để paper stage tham chiếu đúng version đã duyệt của journal profile. | Paper stage không dùng profile chưa duyệt. | BR-74 | Could | T |
| FR-109 | Hệ thống phải bảo đảm journal profile không thay đổi nội dung hay mức chắc chắn của claim. | Văn phong không làm đổi kết luận. | BR-74 | Could | I |

## FE-19 — Method comparison research

**Mục đích:** So sánh các phương pháp ML trên cùng dữ liệu bằng claim type `method_comparison`. **Actor:** Researcher; Persona (experiment_design, execution). **Journey:** J3, J4. **Tiêu chí chấp nhận:** (Sau MVP) Một so sánh có đủ so sánh theo cặp, nhiều seed, tuning budget bằng nhau, nested validation khi có tuning, hiệu chỉnh so sánh nhiều lần và kết quả negative được giữ. FE-19 là Should, sau MVP; MVP không đổi.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-139 | Hệ thống phải hỗ trợ claim type `method_comparison`: so sánh các phương pháp ML trên cùng dữ liệu, dùng pattern G (tối ưu hyperparameter), H (ensemble và stacking), I (ablation) và J (budget-aware), kèm baseline policy F. | Mở rộng từ nghiên cứu hiện tượng sang so sánh phương pháp. | BR-82; BR-96 | Should | T |
| FR-140 | Hệ thống phải so sánh theo cặp trên từng fold và seed trong `method_comparison`. | So sánh theo cặp loại phương sai giữa các fold. | BR-98 | Should | T |
| FR-141 | Hệ thống phải chạy nhiều seed trong `method_comparison`. | Một seed không đo được độ ổn định. | BR-98 | Should | T |
| FR-142 | Hệ thống phải dùng tuning budget bằng nhau cho mọi phương pháp trong `method_comparison`. | So sánh công bằng. | BR-98; BR-99 | Should | T |
| FR-143 | Hệ thống phải dùng nested validation khi `method_comparison` có tuning. | Tuning trên phần đánh giá làm kết quả lạc quan giả. | BR-98 | Should | T |
| FR-144 | Hệ thống phải hiệu chỉnh cho so sánh nhiều lần trong `method_comparison`. | Nhiều so sánh làm tăng dương tính giả. | BR-98 | Should | T |
| FR-145 | Hệ thống phải giữ kết quả negative của `method_comparison` trong EvidenceBundle. | Không giấu phương pháp thất bại. | BR-98 | Should | T |
| FR-194 | Hệ thống phải chỉ cho `method_comparison` dùng pattern G–J (FE-19, sau MVP). | Pattern G–J thuộc claim type so sánh phương pháp. | BR-96 | Should | T |
| FR-267 | Hệ thống phải để AnalysisPlan của `method_comparison` có ba evidence family theo thứ tự: discrimination, reliability (calibration, stress, uncertainty), decision (threshold, cost, subgroup) (FE-19, sau MVP). | Một metric không đủ để kết luận. | BR-93 | Should | T |
| FR-268 | Hệ thống phải dùng task family để chọn metric policy và protocol cho `method_comparison` (FE-19, sau MVP). | Metric và protocol đúng với loại bài toán. | BR-83 | Should | T |
| FR-269 | Hệ thống phải cho `method_comparison` dùng pattern F làm baseline policy (FE-19, sau MVP). | `method_comparison` cần baseline. | BR-96 | Should | T |

## FE-20 — Claim ledger, forecast and replication

**Mục đích:** Cho researcher thấy điều đã biết về mỗi claim key xuyên run, chấm độ chắc của model, nhân rộng claim trên dữ liệu độc lập và đo giá trị của hệ thống. **Actor:** Researcher; AI PI; Persona (experiment_design). **Journey:** J3, J4. **Tiêu chí chấp nhận:** (Should; vào MVP sau khi stage acceptance qua và planted-truth bench đo được nó, nếu không thì sau MVP) Trên Stack Overflow 2025 rồi 2026: mỗi hypothesis có verdict trên hai snapshot, tích evidence e-value và claim status; mỗi forecast có điểm; một báo cáo planted-truth bench có recall, phát hiện sai, hidden-error rate và attention budget.

| FR | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-274 | Hệ thống phải hiển thị claim ledger theo claim key: mọi record xuyên run (run, snapshot, evidence rows, verdict, evidence e-value), tích và `promoted`. | Điều đã biết nằm ở một chỗ, không rải trên các run. | BR-105 | Should | T |
| FR-275 | Hệ thống phải tính claim ledger chỉ từ hand-off object đã lưu, để replay cùng record cho cùng ledger. | Ledger không có chủ sở hữu thứ hai và không bị sửa tay. | BR-105 | Should | T |
| FR-276 | Hệ thống phải tính claim status cho mỗi claim key bằng code (`conjecture`, `testable`, `locked`, `tested`, `supported`, `refuted`, `unresolved`, `exploratory`, `established`, `contested`). | Một khái niệm xuyên run, cùng thang với claim ceiling. | BR-106 | Should | T |
| FR-277 | Hệ thống phải ghi trong claim ledger phần nào của luật `established` chưa có. | Không ngầm coi phần thiếu là đạt. | BR-106 | Should | T |
| FR-278 | Hệ thống phải để experiment_design stage ghi một forecast cho mỗi primary và secondary hypothesis trước khi lock plan: xác suất từ 0,01 tới 0,99 rằng verdict là `supported`, kèm một dòng lý do; contract check đỏ khi thiếu. | Độ chắc được ghi trước khi biết kết quả. | BR-107 | Should | T |
| FR-279 | Hệ thống phải giữ forecast trong Lock. | Forecast không sửa được sau khi thấy kết quả. | BR-107; BR-47 | Should | T |
| FR-280 | Hệ thống phải tính điểm Brier của mỗi forecast sau unseal và forecast score theo project. | Đo model có biết nó chắc tới đâu. | BR-107 | Should | T |
| FR-281 | Hệ thống phải hiển thị forecast với nhãn "model forecast" và không dùng nó cho verdict, grade, claim ceiling, claim status hay next step. | Xác suất của model không phải bằng chứng. | BR-108 | Should | T |
| FR-282 | Hệ thống phải mở replication run từ next step `replicate`: plan mới có program cùng hash với plan đã accepted, trên DatasetSnapshot độc lập có vai trò `validation`; check đỏ khi hash khác. | Nhân rộng đúng nghĩa: cùng phân tích, hàng mới. | BR-109 | Should | T |
| FR-283 | Hệ thống phải để researcher lock plan của replication run (action pinned). | Lock luôn là quyết định của user. | BR-109; BR-26 | Should | T |
| FR-284 | Hệ thống phải để paper stage dùng chữ "replicated" chỉ cho claim key `promoted` có record trên ít nhất hai snapshot. | Lời văn không vượt điều đã nhân rộng. | BR-109 | Should | T |
| FR-285 | Hệ thống phải chạy planted-truth bench từ dataset tới paper và đo recall của hiệu ứng thật, phát hiện sai và claim mạnh hơn verdict. | Đo giá trị bằng sự thật đã biết. | BR-110 | Should | A |
| FR-286 | Hệ thống phải tính hidden-error rate và attention budget cho mỗi run của planted-truth bench. | Đo lời hứa "không có lỗi nào bị giấu" và chi phí chú ý của người. | BR-110 | Should | A |
| FR-287 | Hệ thống phải chạy ablation của mỗi persona và mỗi tham số phán đoán trên planted-truth bench, nhiều lần mỗi cấu hình; luật toàn vẹn không bị ablation. | Chỉ giữ cơ chế làm tăng độ tin. | BR-110 | Should | A |

Ngoài FE-20, các năng lực sau là Could, sau MVP, và chưa có FR: rival explanation với dự đoán phân biệt; test stringency và negative knowledge; multiverse share; breaker trên model của provider khác cùng adversarial collaboration; winner's curse học từ replication; crux report; stakes theo câu hỏi; AI PI dựng lại trên hand-off object, chọn test tiếp theo theo giá trị thông tin; tree search trong exploration sau unseal.

# 9. Non-Functional Requirements

| NFR | Loại | Requirement | Tiêu chí đo | Source |
|---|---|---|---|---|
| NFR-01 | Performance | Hệ thống phải trả trang danh sách run và decision inbox cho project có tới 100 run. | p95 dưới 2 giây. Đo bằng load test trên môi trường staging. | — |
| NFR-02 | Performance | Hệ thống phải stream trace event từ engine tới web app. | p95 dưới 5 giây từ lúc event phát sinh đến lúc hiển thị. Đo bằng test có đồng hồ chung. | — |
| NFR-03 | Availability/reliability | Mọi run không ở trạng thái `waiting` phải đạt trạng thái `ended`; không run nào treo. | 100% run không ở `waiting` đạt `ended`; 0 run ở `waiting` mà không có item đang chờ hoặc Local Node offline; 0 run ở `waiting(decision)` quá hạn chờ của item pinned. Đo bằng audit run state theo project. | SM-01 |
| NFR-04 | Availability/reliability | Khi LLM gateway hoặc nguồn ngoài lỗi, hệ thống phải báo lỗi rõ, không tạo output giả và giữ object đã công bố đọc được. | 0 output giả trong test ngắt gateway; 100% object đã công bố đọc được sau lỗi. Đo bằng test chèn lỗi. | BR-14 |
| NFR-05 | Availability/reliability | Hệ thống phải giữ chi tiêu trong trần đã đặt. | 0 run vượt token budget mà không kết thúc `with_gaps`; 0 run chạm 100% budget tháng mà không có item `spending`. Đo bằng usage ledger và decision inbox. | SM-11 |
| NFR-06 | Availability/reliability | Platform phải sẵn sàng. | Từ 99% số phút của mỗi tháng lịch có health check đạt (đo trên cả tháng lịch, không thu hẹp theo giờ làm việc). Đo bằng giám sát health. | BO-08 |
| NFR-07 | Availability/reliability | Object đã accepted phải còn đọc được và giữ hash sau khi hệ thống khởi động lại. | 100% object accepted giữ nguyên hash sau khởi động lại. Đo bằng test khởi động lại. | BR-11 |
| NFR-08 | Security | Hệ thống phải kiểm quyền theo role và project ở mọi request và cô lập dữ liệu giữa các project. | 0 đường đọc dữ liệu, run, Literature Base, inbox hay audit của project khác. Đo bằng test hai project. | BR-02 |
| NFR-09 | Security | Hệ thống không được để key hoặc secret xuất hiện ngoài Platform. | 0 key hoặc secret trong prompt, log, trace và output. Đo bằng test cài key giả. | BR-23 |
| NFR-10 | Security | Hệ thống không được để agent thấy ước lượng confirmatory trước unseal. | 0 ước lượng confirmatory trong trace và workspace trước unseal; 100% yêu cầu unseal sớm hơn lần sửa lane C cuối bị từ chối. Đo bằng audit envelope log và unseal log. | SM-07 |
| NFR-11 | Security | Hệ thống phải ghi mọi thao tác quản trị và bảo mật vào audit log chỉ-thêm. | 100% thao tác được ghi; 0 thao tác sửa hoặc xoá bản ghi. Đo bằng test. | BR-05 |
| NFR-12 | Privacy | Hệ thống không được để hàng dữ liệu `local` rời Local Node. | 0 hàng dữ liệu `local` trong mọi message ra khỏi Local Node. Đo bằng packet capture trong acceptance scenario của Local Node. | SM-05 |
| NFR-13 | Privacy | Release log của Local Node phải khớp với bản Platform giữ. | 100% khớp. Đo bằng so sánh log trong acceptance scenario. | SM-06 |
| NFR-14 | Privacy | Release gate phải từ chối query làm lộ khác biệt dưới ngưỡng ô nhỏ. | 100% query như vậy bị từ chối và hiển thị lý do. Đo bằng test hai query khác tập hàng ít hơn ngưỡng. | BR-19 |
| NFR-15 | Usability | Người dùng mới phải tạo được run hợp lệ lần đầu. | Ít nhất 5 trên 5 người dùng thành công trong test 5 người. Đo bằng usability test. | BO-01 |
| NFR-16 | Usability | Giao diện phải cho người dùng phân biệt nguồn của thông tin: AI đề xuất, code tính, reviewer phát hiện, researcher duyệt, AI PI quyết định. | Từ 9/10 mục ngẫu nhiên được người dùng gán đúng nguồn. Đo bằng usability test. | BR-41; BR-30 |
| NFR-17 | Usability | Giao diện phải làm người dùng hiểu năm nhãn verdict. | Từ 4/5 nhãn được giải thích đúng không cần trợ giúp. Đo bằng usability test. | BR-54 |
| NFR-18 | Accessibility | Web app phải đạt WCAG 2.1 mức AA; decision inbox và bảng kết quả phải dùng được bằng bàn phím. | 0 lỗi mức A và AA trên các màn chính trong kiểm tra tự động và kiểm tra tay. Đo bằng audit accessibility. | — |
| NFR-19 | Localisation | Giao diện web app chỉ dùng tiếng Anh. | 100% chuỗi giao diện do hệ thống tạo bằng tiếng Anh. Đo bằng kiểm tra tự động chuỗi giao diện. | — |
| NFR-20 | Maintainability | Hệ thống phải dùng một harness cho cả năm engine; engine chỉ khác HarnessSpec. | 0 cơ chế guard, check, trace hay decision log riêng của một engine. Đo bằng inspection. | — |
| NFR-21 | Maintainability | Mỗi hard rule phải có ở cả prompt của bước liên quan và validator bằng code. | 0 rule chỉ có ở một phía. Đo bằng inspection. | — |
| NFR-22 | Maintainability | Tài liệu phải truy vết được BR, FR, UC và TC. | 100% FR truy được về BR; mỗi Must FR có ít nhất một TC. Đo bằng ma trận truy vết. | — |
| NFR-23 | Observability | Hệ thống phải phát một trace event cho mỗi action và mỗi thay đổi check, và ghi decision log đủ trường. | 100% action và thay đổi check có event; 100% quyết định có đủ trường của decision log. Đo bằng test. | BR-29 |
| NFR-24 | Observability | Hệ thống phải báo metric vận hành cho mỗi run. | Báo số question, thời gian bị chặn, overturn rate theo action type và tỷ lệ item `needs-you` cho 100% run; ngưỡng theo SM-02. | SM-02 |
| NFR-25 | Replayability | Replicator phải tái lập hash của EvidenceBundle. | 100% bundle accepted có replication package mà replicator tái lập hash; nếu không, item đỏ. Đo bằng báo cáo replicator. | SM-08 |
| NFR-26 | Replayability | Cùng object đã ghim, cùng Lock và cùng seed phải cho cùng hash. | 100% run trong bộ kiểm cho cùng hash khi chạy lại. Đo bằng chạy lại và so hash. | BO-02 |
| NFR-27 | Integrity và traceability | PaperPack không được chứa số không phải tham chiếu. | 0 chữ số ngoài danh sách cho phép (năm, số mục, số section) trong PaperPack accepted; 100% số tham chiếu được tới record. Đo bằng contract check ở mỗi version. | SM-03 |
| NFR-28 | Integrity và traceability | Mọi effect statement phải truy được về verdict và không vượt claim ceiling. | 100% effect statement trong Abstract, Results và Discussion ánh xạ tới verdict và interpretation row; 0 claim vượt claim ceiling. Đo bằng contract check claims. | SM-12 |
| NFR-29 | Integrity và traceability | Mọi citation phải nằm trong Literature Base với DOI đã resolve. | 100% citation. Đo bằng contract check citations. | SM-04 |
| NFR-30 | Integrity và traceability | Mọi object version accepted phải qua review loop với tối đa hai vòng sửa. | 100% object version accepted có review record; số vòng sửa mỗi object version không quá 2; 100% finding còn lại hiển thị trong PaperPack. Đo bằng đối chiếu review record. | SM-10 |
| NFR-31 | Integrity và traceability | AI PI không được quyết item pinned và mọi quyết định tạm phải hiện cho user. | 0 quyết định của AI PI trên item pinned; 100% quyết định tạm hiện trong decision inbox khi user quay về. Đo bằng test `autopilot` với user `away`. | BR-30; BR-31 |

# 10. Object Contracts Summary

Bảng này tóm tắt hand-off object và Dossier ở mức khái niệm. Định nghĩa đầy đủ: [glossary §6](glossary.md); quan hệ: [architecture §5.4](architecture.md). Mọi hand-off object có kiểu, version và hash, và bất biến sau khi accepted (FR-18).

| Object | Do ai tạo | Phần bắt buộc | Ghim | FR |
|---|---|---|---|---|
| DatasetSnapshot | Dataset stage | Nguồn; table model; profile năm chiều chất lượng; dictionary; cleaning recipe; question map; split; vai trò nguồn; fitness | Dataset version | FR-37 |
| HypothesisSet | Hypothesis stage | Ít nhất hai hypothesis có claim key khác nhau; một primary. Mỗi hypothesis có estimand nháp, biến, confounder có nguồn, SESOI, câu bác bỏ, loại đóng góp, nguồn gốc | DatasetSnapshot; Literature Base (version) | FR-44, FR-45 |
| AnalysisPlan | Experiment_design stage | Estimand; protocol theo loại claim; adjustment set; analysis program; fallback; decision rule; bảng diễn giải; robustness set; design diagnosis; cấu trúc họ giả thuyết; task family; research pattern đã chọn; pipeline order; evidence family (với `prediction` và `method_comparison`) | HypothesisSet | FR-46, FR-124..FR-128 |
| Lock | Platform | Hash của spec, program và golden outputs; snapshot version; split digest; ai khoá; khi nào | AnalysisPlan version | FR-48 |
| EvidenceBundle | Execution stage | Mười item: kết quả xác nhận; verdict và dòng diễn giải; grade; diagnostics; robustness; deviation log; tried ledger và candidate; bảng và hình; replication package; báo cáo replicator và envelope log. Kèm claim ceiling | AnalysisPlan (qua Lock) | FR-61 |
| PaperPack | Paper stage | Mười item: reporting checklist; manuscript; claims; figures và tables; citations; limitations; reproducibility; declarations; review; formats | EvidenceBundle | FR-62 |
| Dossier | Platform | Tham chiếu tới version EvidenceBundle và PaperPack đã accepted; hash; trạng thái duyệt; Approval theo version | EvidenceBundle và PaperPack (version accepted) | FR-94, FR-96 |

Literature Base không phải hand-off object. Nó là kho bằng chứng cấp project có version; mọi stage đọc theo version (FR-43).

# 11. Release and Acceptance Criteria

Benchmark chỉ chạy theo yêu cầu.

## 11.1 Stage acceptance scenario

Mỗi stage được chấp nhận riêng. Scenario chạy engine một mình với hand-off object upstream là fixture đã đóng băng, model thật và user theo kịch bản. Stage đạt khi **một** lần chạy live của scenario kết thúc với mọi hard check xanh. Hard check là check bằng code trên object tạo ra (số liệu cộng khớp, tham chiếu resolve, tier gắn đúng, hash bằng nhau). Kỳ vọng phụ thuộc phán đoán của model hoặc tín hiệu thật chỉ được báo cáo, không bắt buộc. Mỗi ngưỡng đếm của scenario cũng là một contract item; ngưỡng không đạt là gap của output, không phải run hỏng.

| Stage | Điều kiện chấp nhận (mức khái niệm) |
|---|---|
| harness | Contract item chuyển xanh; level theo preset đúng; user `away` không chặn run; review loop dừng sau hai vòng sửa. |
| dataset | DatasetSnapshot đủ mọi phần; các bất thường đã cài trong dữ liệu được tìm ra; cleaning chạm outcome chuyển sang plan; join trên khoá không hợp lệ bị từ chối; fitness `fit_with_limits` kèm lý do. |
| hypothesis | Luồng sàng lọc cộng khớp; evidence map có ít nhất một ô kiểm được với snapshot; HypothesisSet đủ hypothesis có loại đóng góp, estimand nháp và nguồn; mọi số trong evidence card nằm trong trích dẫn. |
| experiment_design | Mọi contract item xanh; twin phục hồi hiệu ứng đã cài và tỷ lệ dương tính giả của kiểm hoán vị nằm trong khoảng cho phép; Lock có golden outputs. |
| execution | Dry run khớp dữ liệu; kết quả confirmatory chỉ mở sau unseal; Holm và gatekeeping được áp dụng; tried ledger có ngưỡng nhiễu; candidate được xác nhận và gắn tier; hash của replicator bằng hash của bundle. |
| paper | Mười contract item xanh; ít nhất ba hình chính có số bằng record của bundle; không có chữ số không phải tham chiếu; bảng độ phủ reporting checklist đầy đủ. |
| Local Node | Ghép bằng mã; dataset được đề xuất từ thư mục; release log bằng bản Platform giữ; query differencing bị từ chối; 0 hàng dữ liệu trong message ra ngoài (bắt gói). |

Connection check giữa các stage chỉ chạy sau khi mọi stage đạt: object ghim và hash từ đầu đến cuối; đổi snapshot đánh dấu mọi object downstream `stale`; candidate của lane E quay lại decision inbox và vòng hai dùng reserve; user `away` qua đêm ở `milestones` với item pinned đang chờ (kết quả mong đợi: run ở `waiting(decision)` và chờ tới hạn chờ của item; việc không phụ thuộc item tiếp tục; item ở lại trong decision inbox; hệ thống gửi thông báo ngoài và lời nhắc trước hạn; hết hạn thì run `ended(with_gaps)`, item đóng ở trạng thái chưa trả lời và không ai quyết thay user); replication package tái lập hash của bundle.

## 11.2 Benchmark

Khả năng của bench là Must: hệ thống có seeded-flaw bench, red-team catalogue và cách đo precision của persona (FR-77, FR-135..FR-137), vì review loop dùng precision này. Việc chạy một đợt đánh giá đầy đủ trên seeded-flaw bench và paper reproduction bench là **Should** và chạy theo yêu cầu. Đợt đánh giá này không nằm trong điều kiện phát hành MVP (§11.3). SM-17 và SM-18 đo khi đợt đánh giá chạy.

| Bench | Mục đích | Chỉ số | Nguồn |
|---|---|---|---|
| Seeded-flaw bench | Đo precision của từng persona reviewer; đo phát hiện và chặn lỗi trong red-team catalogue (ba nhóm: dữ liệu, thí nghiệm, suy luận; BR-100, FR-135) | Precision không dưới mức tối thiểu của persona; dưới mức thì severity bị hạ. Tỷ lệ phát hiện leakage cài sẵn (SM-17) và tỷ lệ chặn vi phạm pipeline order (SM-18) đạt target của SM-17 (ít nhất 90%) và SM-18 (100%) | SM-09; SM-17; SM-18; BR-40; BR-100 |
| Paper reproduction bench | So kết quả của hệ thống với bài đã công bố có dữ liệu mở | Hướng và độ chồng khoảng của ước lượng chính; độ phủ checklist; lỗi lớn theo rubric Reviewer 2. Mục tiêu: không kém tỷ lệ bài không có lỗi lớn mà hệ thống data-to-paper báo cáo trên mục tiêu tương đương | SM-13 |

### 11.2.1 Benchmark case catalogue

Nguồn: BR-101; FR-138. 60 project mẫu là ca kiểm thử của research pattern, không phải 60 flow riêng. Cột ID là ID của benchmark case (`BC-`): C là classification, R là regression, I là imbalanced classification. Report V dẫn xuất test case từ bảng này (giai đoạn sau).

Cách đọc cột:

- **Pattern:** chữ cái của research pattern A–O (BR-96). Chữ cái là phép gán của tài liệu này theo mô tả project.
- **FE:** feature chạy ca. Ca có pattern G–J theo FE-19 (`method_comparison`, Should, sau MVP). Ca còn lại theo FE-09; việc chọn pattern nằm ở FE-08.
- **Priority:** đợt 1 gồm BC-C01, BC-C05, BC-C07; đợt 2 gồm BC-R01, BC-R06, BC-R08, BC-I01, BC-I08, BC-I18. Ca của đợt 1 và đợt 2 làm trước. Ca FE-09 của đợt 1 là Must: chúng là tập tối thiểu chứng minh nhánh tabular chạy được. Ca FE-09 từ đợt 2 trở đi là Should và chạy theo yêu cầu, cùng đợt đánh giá của bench (§11.2). Ca có pattern G–J theo priority của FE-19.

| BC ID | Tên ngắn | Task family | Pattern | FE | Priority |
|---|---|---|---|---|---|
| BC-C01 | So sánh thuật toán classification | binary / multiclass | F | FE-09 | Must, đợt 1 |
| BC-C02 | Độ ổn định của feature selection | binary / multiclass | C | FE-09 | Should, sau đợt 2 |
| BC-C03 | Thiếu dữ liệu và imputation | binary / multiclass | A | FE-09 | Should, sau đợt 2 |
| BC-C04 | Categorical encoding | binary / multiclass | C | FE-09 | Should, sau đợt 2 |
| BC-C05 | Scaling có thật sự cần | binary / multiclass | C | FE-09 | Must, đợt 1 |
| BC-C06 | Learning curve và sample efficiency | binary / multiclass | E | FE-09 | Should, sau đợt 2 |
| BC-C07 | Search budget và tối ưu hyperparameter | binary / multiclass | G | FE-19 | Should, sau MVP (đợt 1; xem Câu hỏi mở 5) |
| BC-C08 | Hiệu năng và giải thích | binary / multiclass | N | FE-09 | Should, sau đợt 2 |
| BC-C09 | Probability calibration | binary / multiclass | K | FE-09 | Should, sau đợt 2 |
| BC-C10 | Hiệu quả trên các phân nhóm | binary / multiclass | O | FE-09 | Should, sau đợt 2 |
| BC-C11 | Tối ưu decision threshold | binary / multiclass | K | FE-09 | Should, sau đợt 2 |
| BC-C12 | Ensemble và stacking | binary / multiclass | H | FE-19 | Should, sau MVP |
| BC-C13 | Label và feature noise robustness | binary / multiclass | B | FE-09 | Should, sau đợt 2 |
| BC-C14 | Class overlap và boundary | binary / multiclass | B | FE-09 | Should, sau đợt 2 |
| BC-C15 | Tương tác đặc trưng và ablation | binary / multiclass | C, I | FE-19 | Should, sau MVP |
| BC-C16 | Độ ổn định qua seed | binary / multiclass | F | FE-09 | Should, sau đợt 2 |
| BC-C17 | Predictive data drift | binary / multiclass | D | FE-09 | Should, sau đợt 2 |
| BC-C18 | Fairness-performance trade-off | binary / multiclass | O | FE-09 | Should, sau đợt 2 |
| BC-C19 | Out-of-distribution test | binary / multiclass | D | FE-09 | Should, sau đợt 2 |
| BC-C20 | AutoML với baseline khoa học | binary / multiclass | F, J | FE-19 | Should, sau MVP |
| BC-R01 | Benchmark linear và nonlinear | regression | F | FE-09 | Should, đợt 2 |
| BC-R02 | Scaling trong regression | regression | C | FE-09 | Should, sau đợt 2 |
| BC-R03 | Polynomial interactions | regression | C | FE-09 | Should, sau đợt 2 |
| BC-R04 | Regularization path | regression | N | FE-09 | Should, sau đợt 2 |
| BC-R05 | Ảnh hưởng của imputation | regression | A | FE-09 | Should, sau đợt 2 |
| BC-R06 | Robustness với outlier | regression | B | FE-09 | Should, đợt 2 |
| BC-R07 | Hiệu quả tối ưu hyperparameter trong regression | regression | G | FE-19 | Should, sau MVP |
| BC-R08 | Prediction interval coverage | regression | K | FE-09 | Should, đợt 2 |
| BC-R09 | Độ ổn định của feature selection | regression | C | FE-09 | Should, sau đợt 2 |
| BC-R10 | Học từ mẫu nhỏ | regression | E | FE-09 | Should, sau đợt 2 |
| BC-R11 | Stacking trong regression | regression | H | FE-19 | Should, sau MVP |
| BC-R12 | Heteroscedastic uncertainty | regression | K | FE-09 | Should, sau đợt 2 |
| BC-R13 | Nhiễu đo lường ở input | regression | B | FE-09 | Should, sau đợt 2 |
| BC-R14 | Feature interaction ablation | regression | I | FE-19 | Should, sau MVP |
| BC-R15 | Monotonic constrained learning | regression | C | FE-09 | Should, sau đợt 2 |
| BC-R16 | Cross-domain transfer | regression | D | FE-09 | Should, sau đợt 2 |
| BC-R17 | Biến đổi target | regression | C | FE-09 | Should, sau đợt 2 |
| BC-R18 | Explainability qua nhiều fold | regression | N | FE-09 | Should, sau đợt 2 |
| BC-R19 | Multi-output regression | regression | F | FE-09 | Should, sau đợt 2 |
| BC-R20 | AutoML regression suite | regression | F, J | FE-19 | Should, sau MVP |
| BC-I01 | Resampling benchmark | rare-event | L | FE-09 | Should, đợt 2 |
| BC-I02 | Các biến thể oversampling tổng hợp | rare-event | L | FE-09 | Should, sau đợt 2 |
| BC-I03 | Class weighting hay resampling | rare-event | L | FE-09 | Should, sau đợt 2 |
| BC-I04 | Extreme imbalance | rare-event | L | FE-09 | Should, sau đợt 2 |
| BC-I05 | Cost-sensitive learning | rare-event | L, O | FE-09 | Should, sau đợt 2 |
| BC-I06 | Threshold optimization | rare-event | K | FE-09 | Should, sau đợt 2 |
| BC-I07 | Precision-recall operating point | rare-event | K, L | FE-09 | Should, sau đợt 2 |
| BC-I08 | Calibration sau resampling | rare-event | K, L | FE-09 | Should, đợt 2 |
| BC-I09 | Số mẫu minority | rare-event | E, L | FE-09 | Should, sau đợt 2 |
| BC-I10 | Nhiễu nhãn ở lớp minority | rare-event | B, L | FE-09 | Should, sau đợt 2 |
| BC-I11 | Ensemble chuyên cho imbalance | rare-event | L | FE-09 | Should, sau đợt 2 |
| BC-I12 | Tối ưu sampling ratio | rare-event | L | FE-09 | Should, sau đợt 2 |
| BC-I13 | Feature selection khi imbalance | rare-event | C, L | FE-09 | Should, sau đợt 2 |
| BC-I14 | Synthetic hay duplicated minority | rare-event | L | FE-09 | Should, sau đợt 2 |
| BC-I15 | Imbalance kết hợp drift | rare-event | D, L | FE-09 | Should, sau đợt 2 |
| BC-I16 | Fairness khi imbalance | rare-event | L, O | FE-09 | Should, sau đợt 2 |
| BC-I17 | Anomaly detection hay supervised | rare-event | F, L | FE-09 | Should, sau đợt 2 |
| BC-I18 | Độ tin cậy thống kê đa dataset | rare-event | F, L | FE-09 | Should, đợt 2 |
| BC-I19 | Dịch chuyển phân phối feature của minority | rare-event | M, L | FE-09 | Should, sau đợt 2 |
| BC-I20 | Tự chọn chiến lược imbalance | rare-event | G, L | FE-19 | Should, sau MVP |

Ghi chú:

- BC-I17 so sánh với anomaly detection; BC-R19 là multi-output regression. Cả hai dùng task ngoài bốn task family (BR-83). Catalogue giữ chúng; xem Câu hỏi mở 6.
- BC-C20 và BC-R20 so sánh một AutoML với baseline khoa học như một đề tài nghiên cứu. Chúng không phải so sánh nền tảng này với AutoML (đã bỏ, §3). Ranh giới: đề tài nghiên cứu của user, trong đó user so sánh một phương pháp AutoML với baseline trên dữ liệu của mình bằng `method_comparison`, thuộc phạm vi (FE-19, Should). Đánh giá chính OpenAI-Scientist so với AutoML hoặc generic agent không thuộc phạm vi.
- BC-C01, BC-R01 và BC-I18 chỉ có pattern F (baseline policy) nên theo FE-09. Nội dung của chúng so sánh nhiều thuật toán; nếu chúng được xem là `method_comparison`, priority của chúng chuyển sang Should.

## 11.3 Điều kiện phát hành MVP

MVP gồm FE-01..FE-15 và FE-17. JFE (FE-18) và Method comparison research (FE-19) nằm sau MVP.

- Mọi stage và Local Node đạt acceptance scenario (§11.1), rồi connection check đạt.
- Mọi FR Must có ít nhất một test case đạt, theo ma trận truy vết.
- Mọi NFR có kết quả đo theo ngưỡng đã duyệt.
- 0 finding `blocking` còn mở trong tài liệu của release.

## 11.4 Definition of Done của một feature

1. Mọi FR Must của feature có test case đạt hoặc có inspection/analysis/demonstration được ghi.
2. NFR liên quan có kết quả đo.
3. Nếu feature là một stage: acceptance scenario của stage đạt.
4. FR, BR và ID liên quan khớp trong ma trận truy vết; tài liệu nguồn và [changelog](changelog.md) đã cập nhật trong cùng đợt.
5. Message cho người dùng của feature có trong message catalogue (Report III).
6. Không còn finding `blocking` đã `confirmed` của review loop; finding còn lại là known risk được ghi.

# 12. Open Questions

1. **Target của SM-02.** Cần ngưỡng cho số question mỗi run, thời gian bị chặn và overturn rate (BRD Câu hỏi mở 1). Đã đóng: ngưỡng ghi ở SM-02. Ảnh hưởng NFR-24.
2. **Writing rule.** BR-72 cần nội dung chi tiết của từng rule H, M và G (BRD Câu hỏi mở 2). Chưa xác định. Ảnh hưởng FR-69.
3. **Target của SM-17 và SM-18.** Cần ngưỡng cho tỷ lệ phát hiện leakage cài sẵn và tỷ lệ chặn vi phạm pipeline order (BRD Câu hỏi mở 3). Đã đóng: SM-17 ít nhất 90%, SM-18 là 100%. Ảnh hưởng FR-136, FR-137.
4. **Giới hạn secondary hypothesis.** Cần giá trị mặc định của project setting (BRD Câu hỏi mở 4). Đã đóng: mặc định 3 secondary. Ảnh hưởng FR-123.
5. **Priority của BC-C07.** BC-C07 thuộc đợt 1, nhưng pattern G của nó thuộc FE-19 (Should, sau MVP). Catalogue §11.2.1 ghi cả hai (BRD Câu hỏi mở 5). Hai lựa chọn: giữ Should, hoặc thay bằng ca khác trong đợt 1. Chưa xác định.
6. **Case có task nằm ngoài bốn task family.** BC-I17 (so sánh với anomaly detection) và BC-R19 (multi-output regression) dùng task ngoài bốn task family. Catalogue giữ chúng. Cần quyết định giữ hay bỏ. Chưa xác định.
7. **Giờ làm việc của NFR-06.** Không nguồn nào định nghĩa giờ làm việc. NFR-06 đo độ sẵn sàng trên cả tháng lịch. Đã đóng: đo trên cả tháng lịch, không thu hẹp. Ảnh hưởng NFR-06.

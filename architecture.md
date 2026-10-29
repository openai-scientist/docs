# Architecture — OpenAI-Scientist

**Phiên bản:** 3.0 (2026-10-29) · **Chuẩn:** arc42 + ADR, viewpoint theo IEEE 1016 · **Mức:** khái niệm
**Liên quan:** [README](README.md) · [Glossary](glossary.md) · [BRD](BRD.md) · [PRD](PRD.md) · [changelog](changelog.md)

Đây là **nguồn nội bộ** của Report IV (SDD). Report trên Google Docs là tài liệu cuối cùng; nó trình bày lại tài liệu này cho người đọc ngoài team. Tài liệu này không ghi đường dẫn, tên class, route, cổng, biến môi trường hay tên bảng. Giá trị kỹ thuật nằm trong plan của repo code (xem ADR-16). Thuật ngữ theo [glossary.md](glossary.md). Tài liệu này tham chiếu ADR ID. Ngoại lệ: nó dẫn BR-61 (mức trần chi tiêu), FR-22 (huỷ run) và FR-146 (Google sign-in), vì ba việc này chưa có ADR.

## Contents

1. [Introduction and goals](#1-introduction-and-goals)
2. [Constraints](#2-constraints)
3. [Context and scope](#3-context-and-scope)
4. [Solution strategy](#4-solution-strategy)
5. [Building block view](#5-building-block-view)
6. [Runtime view](#6-runtime-view)
7. [Deployment view](#7-deployment-view)
8. [Cross-cutting concepts](#8-cross-cutting-concepts)
9. [Architecture decisions](#9-architecture-decisions)
10. [Quality requirements](#10-quality-requirements)
11. [Risks and technical debt](#11-risks-and-technical-debt)
12. [Glossary](#12-glossary)

---

## 1. Introduction and goals

### 1.1 Mục đích

Hệ thống giúp một researcher đi từ một câu hỏi nghiên cứu và dữ liệu dạng bảng đến một gói bằng chứng sẵn sàng cho bài báo. Máy làm phần việc; researcher giữ các quyết định chỉ researcher mới sở hữu. Hệ thống **không hứa khoa học đúng**. Hệ thống hứa ba điều: không có lỗi bị giấu, mọi claim có nguồn, mọi run có thể replay.

### 1.2 Năm quality goal hàng đầu

| # | Quality goal | Nghĩa trong một dòng |
|---|---|---|
| 1 | Integrity | Không có lỗi bị giấu. Mọi con số và verdict do code tính, không do model viết. |
| 2 | Traceability | Mọi claim trỏ được về nguồn: record, version, hash, tài liệu, quyết định. |
| 3 | Replayability | Một run có thể chạy lại từ object đã ghim (pin) và cho cùng hash. |
| 4 | Data privacy | Hàng dữ liệu không bao giờ rời nơi giữ dữ liệu. Chỉ aggregate rời đi, qua một release gate. |
| 5 | Human control with progress | User giữ quyết định theo loại action. Run luôn kết thúc; không bao giờ treo vô hạn. |

### 1.3 Stakeholder

| Stakeholder | Kỳ vọng với kiến trúc |
|---|---|
| Researcher | Điều khiển được run; thấy mọi bước; không phải chờ vô hạn |
| Project Manager | Kiểm soát member, budget, duyệt chi thêm |
| Reviewer | Đọc mọi object; duyệt Dossier theo review settings |
| Platform Admin | Quản lý user, model, key, budget mặc định, audit |
| Paper team | Nhận PaperPack mà không phải dựng lại số liệu |
| IT của đơn vị giữ dữ liệu | Tin rằng hàng dữ liệu không rời máy; kiểm tra được mọi release |
| Hội đồng capstone | Kiến trúc có quyết định, lý do và cách đo |

---

## 2. Constraints

| Loại | Ràng buộc |
|---|---|
| Dữ liệu | Chỉ dữ liệu dạng bảng. |
| Non-goal | (1) Dữ liệu không phải bảng (ảnh, corpus văn bản, tín hiệu). (2) Thiết kế thu thập dữ liệu mới; experiment_design chỉ lập kế hoạch phân tích dữ liệu bảng có sẵn. (3) Systematic review đầy đủ (đăng ký PROSPERO, GRADE đầy đủ, meta-analysis kết luận). (4) Đọc full text có paywall. |
| LLM | Model do một **LLM gateway** bên ngoài cung cấp. Có ba model role: `stage`, `review`, `vision`. Key đi kèm request theo role. |
| Front end | Web app là sản phẩm tách riêng khỏi Platform. Hai bên giao tiếp qua giao diện đã định nghĩa; web app không giữ logic khoa học. |
| Pipeline | Pipeline luôn là `dataset_first`. Mỗi project có tối đa một run active. |
| Tài liệu | Tài liệu định nghĩa hệ thống; code đi theo tài liệu (ADR-16). |
| Team | Team sinh viên nhỏ, học kỳ cố định. Kiến trúc phải dùng lại một harness cho mọi engine (ADR-02) và tránh cơ chế riêng cho từng stage. |

---

## 3. Context and scope

### 3.1 Actor

Theo [glossary §1](glossary.md): Platform Admin, Project Manager, Researcher, Reviewer (người), AI PI (connector persona; secondary actor trong use case, hành động thay mặt user trong giới hạn của nó).

### 3.2 System context

```text
 Người dùng ──> Web app ──> Platform ──> Stage engines ──> LLM gateway
                               │   │            │
                               │   │            ├──> Literature sources
                               │   │            ├──> Public dataset sources
                               │   │            └──> Local Node (máy user, dữ liệu local)
                               │   ├──> AI PI ──> LLM gateway
                               │   ├──> Email
                               │   └──> Google sign-in; Google Sheets / Drive
```

Phạm vi hệ thống: Web app, Platform, Stage engines, AI PI, Local Node, thư viện dùng chung. Ngoài phạm vi: LLM gateway, nguồn literature, nguồn public dataset, email, Google.

### 3.3 External system

| External system | Vai trò | Hướng dữ liệu |
|---|---|---|
| LLM gateway | Cung cấp model theo role `stage`, `review`, `vision` | Prompt đi ra; text trả về. Không có hàng dữ liệu local trong prompt. |
| Literature sources | Tìm bài, metadata, abstract, full text open access | Query đi ra; metadata về |
| Public dataset sources | Tìm và đọc dataset public; header peek | Query đi ra; header và file public về |
| Email | Thông báo cho item pinned đang chặn và item `spending` | Đi ra |
| Google sign-in | Đăng nhập | Hai chiều |
| Google Sheets và Drive | Data connection do user uỷ quyền; import tạo dataset version | Dữ liệu về |

### 3.4 Business context

| Partner | Input | Output |
|---|---|---|
| Researcher, Project Manager | Research case, dataset, trả lời decision inbox, chấp nhận hand-off object | Dossier, PaperPack, Lab notebook |
| Reviewer | Bình luận, approval | Approval cho Dossier |
| Platform Admin | Model, key, budget mặc định, engine settings | Audit log, health |
| LLM gateway | Prompt có cấu trúc, schema output | Text và call có tool |
| Literature sources | Query theo protocol | Metadata, abstract, full text open access |
| Public dataset sources | Query, header peek | Dataset public, access card cho dữ liệu hạn chế |
| Email | Nội dung thông báo | Thông báo tới user |
| Google | Uỷ quyền của user | Danh tính; bảng từ Sheets và Drive |
| Paper team | PaperPack, replication package | Bản nộp tạp chí (ngoài hệ thống) |

---

## 4. Solution strategy

| # | Chiến lược | Quality goal | ADR |
|---|---|---|---|
| S1 | Pipeline năm stage; mỗi ranh giới có đúng một hand-off object có kiểu, version, hash, bất biến sau acceptance. | Traceability, Replayability | ADR-01 |
| S2 | Một harness chung cho mọi engine; engine khác nhau chỉ ở HarnessSpec. Mọi guard, check, trace và decision log nằm ở một chỗ. | Integrity, Traceability | ADR-02 |
| S3 | Platform sở hữu người, project, run, budget, key, audit, Lock, envelope, Dossier; Platform không đánh giá khoa học. | Integrity, Human control | ADR-03 |
| S4 | Quyền theo loại action: preset theo stage, presence, floor, action pinned. | Human control | ADR-04 |
| S5 | Một decision inbox cho mọi stage; theo dõi overturn; thông báo ngoài chỉ cho item pinned đang chặn và item `spending`. | Human control | ADR-05 |
| S6 | Review độc lập bắt buộc, persona, finding đã kiểm, tối đa hai vòng sửa. | Integrity | ADR-06 |
| S7 | Con số và verdict do code; text của model chỉ mang reference. | Integrity, Traceability | ADR-07 |
| S8 | Lock, envelope, unseal thực thi bằng đường code ở Platform; agent không có đường tới kết quả confirmatory. | Integrity | ADR-08, ADR-09 |
| S9 | Local Node giữ dữ liệu `local`; một release gate; release log chỉ-thêm; user không cần Docker. | Data privacy | ADR-10 |
| S10 | Một budget cho mỗi run; item hết budget thành needs-you; hết budget run thì `ended(with_gaps)`. Item `spending` và item pinned có hạn chờ; hết hạn thì `ended(with_gaps)`. Budget tháng của project chặn chi tiêu vượt mức. | Human control with progress | ADR-11, ADR-13, ADR-15 |
| S11 | Dossier chỉ tham chiếu version đã accepted; export cần approval. | Traceability, Integrity | ADR-12 |
| S12 | Dataset tuỳ chọn khi bắt đầu; dataset stage tìm hoặc hỏi. | Human control with progress | ADR-14 |
| S13 | Research pattern là đơn vị có version trong một registry; pipeline order chống leakage được guard chặn trước khi chạy; mỗi pattern có negative test. | Integrity | ADR-17 |
| S14 | Claim type `method_comparison` dùng cùng harness, Lock, envelope và verdict; chỉ thêm pattern G–J. Should, sau MVP. | Integrity, Traceability | ADR-18 |

---

## 5. Building block view

### 5.1 Level 1

```text
 Web app ──> Platform ──┬──> Dataset engine ────┐
                        ├──> Hypothesis engine  │   mỗi engine chạy trên Harness
                        ├──> Experiment design  │   (Executor trong engine)
                        ├──> Execution engine ──┼──> Local Node (Executor cạnh dữ liệu local)
                        ├──> Paper engine ──────┘
                        └──> AI PI
 Thư viện dùng chung: contract · analysis · tables · discovery
```

| Khối | Trách nhiệm | Không làm |
|---|---|---|
| Web app | Hiển thị workspace, decision inbox, trace; nhận hành động của user | Không chứa logic khoa học; không gọi engine trực tiếp |
| Platform | Người dùng, project, member, run, run state, budget, key, audit, presence, decision inbox tổng hợp, decision log chéo stage, Lock, envelope, unseal, Dossier, approval, thông báo | Không đánh giá nội dung khoa học |
| Stage engine ×5 (dataset, hypothesis, experiment_design, execution, paper) | Chạy một stage trên Harness theo HarnessSpec; tạo hand-off object | Không lưu người, project, key; không đọc kết quả envelope trước unseal |
| Harness | Runtime chung (xem 5.2) | Không biết khoa học của stage |
| AI PI | Connector persona: tóm tắt, đề xuất next step, ghi Lab notebook, quyết định tạm khi `autopilot` + `away` | Không kết thúc run; không quyết định item pinned |
| Executor | Chạy job phân tích. Hai nơi chạy: trong engine (cloud) hoặc trên Local Node. Cùng một thư viện phân tích | Không tạo đường riêng cho dữ liệu |
| Local Node | Giữ dữ liệu `local`; chạy job cạnh dữ liệu; release gate; release log; desktop app | Không gửi hàng dữ liệu; không yêu cầu Docker |
| Thư viện contract | Định nghĩa hand-off object, action type, giao thức job | — |
| Thư viện analysis | Registry thống kê, registry research pattern, firewall, disclosure, sandbox, bộ thực thi job | — |
| Thư viện tables | Table model, profile, split, cleaning recipe | — |
| Thư viện discovery | Tìm public dataset; header peek | Không tải dữ liệu hạn chế tự động |

### 5.2 Harness internals

| Thành phần | Trách nhiệm |
|---|---|
| Agent loop | Đọc contract status; chọn action tiếp; gọi một tool; quan sát kết quả |
| Action pipeline | Mọi action của agent hoặc user đi qua: guard → level → execute hoặc queue → recompute check → trace event → decision log |
| Workspace | Object có version, decision log, ghi chú tiến độ; bền theo engine và project, không theo run |
| Live trace | Mọi action và thay đổi check là một event, stream tới web app |
| Budget và exit | Token, thời gian, số job. Cạn budget thì run `ended(with_gaps)`: output tốt nhất, item đỏ được liệt kê. Hạn chờ của item `spending` và của item pinned cũng kết thúc run `with_gaps` |
| Contract và hand-off | Khi mọi contract item xanh (hoặc run kết thúc with_gaps), engine công bố một version hand-off object; acceptance theo bảng quyền |
| Built-ins | Workspace tool; `ask_human`; `record_gap`; `assume`; `run_job`; literature pack; discovery pack; guard (data firewall, numbers-only-from-tools, object đã lock bất biến, lọc secret); check dùng chung (schema, reference resolve, source mark theo attribute); review độc lập; hook cho seeded-flaw bench |

Phân chia trách nhiệm Engine và Platform trong action pipeline:

| Việc | Engine (Harness) | Platform |
|---|---|---|
| Level của action | Tính level trong từng action | Lưu policy (preset theo stage, override); gửi kèm request của run |
| Presence | Đọc từ request và từ sự kiện chuyển tiếp | Phát hiện (hoạt động UI, "away until"); chuyển tiếp thay đổi |
| Guard, check, trace, decision log | Chạy và phát event | Lưu event; dựng decision log chéo stage |
| Decision inbox | Phát item; hỏi ngay khi user `present` | Gộp item của mọi stage thành một inbox; chuyển câu trả lời về engine |
| Contract status | Tính và phát theo từng item | Hiển thị |
| Lock, envelope, unseal | Yêu cầu | Sở hữu và thực thi |

### 5.3 Object ownership

| Object | Module sở hữu | Liên kết bằng |
|---|---|---|
| DatasetSnapshot | Dataset engine | snapshot id + hash |
| Literature Base | Hypothesis engine | version id |
| HypothesisSet | Hypothesis engine | set id + claim key |
| AnalysisPlan | Experiment_design engine | spec hash, program hash |
| Lock | Platform (ghi theo yêu cầu của experiment_design) | spec hash, program hash |
| EvidenceBundle | Execution engine | bundle id + record id |
| PaperPack | Paper engine | pack id |
| Decision inbox, decision log, permission policy | Platform và Harness | item id |
| Release log | Local Node hoặc Executor trong engine; bản sao ở Platform | dataset version id |
| Tried ledger | Execution engine (workspace) | ledger entry id |
| ResearchPattern (registry) | Thư viện analysis; experiment_design engine đọc | pattern id + version |
| Envelope | Platform | lock id |

Object do Platform sở hữu (không thuộc engine nào):

| Object | Ghi chú |
|---|---|
| Project, Membership, Project settings | Người, role, budget, review settings, preset mặc định, notification |
| Run, StageRun | Run state; liên kết các hand-off object đã pin |
| Budget (run và tháng của project) | Số dư, ngưỡng cảnh báo, sổ chi tiêu |
| Model profile và key | Theo role; key không rời Platform ngoài request của run |
| Audit log | Chỉ-thêm |
| Lock, Envelope | Một Lock cho mỗi plan đã khoá; một Envelope cho mỗi Lock |
| Dossier, Approval | Platform chỉ đánh version, kiểm hash, ghi approval |
| Decision inbox và decision log tổng hợp | Gộp từ mọi stage |

### 5.4 Information view — logical data model

Bảng này mô tả khái niệm và quan hệ. Nó không ghi kiểu dữ liệu, khoá ngoại hay tên bảng. Cardinality đọc theo hướng "một dòng này có bao nhiêu dòng kia".

| Entity | Thuộc tính chính | Quan hệ (cardinality) |
|---|---|---|
| Project | tên, trạng thái, preset mặc định theo stage | 1 Project – N Membership; 1 – 1 ProjectSettings; 1 – N Dataset; 1 – N ResearchCase; 1 – N Run (tối đa 1 active); 1 – 1 LiteratureBase; 1 – N Dossier; 1 – N AuditEvent; 1 – 1 BudgetLedger (theo tháng) |
| Membership | role (Project Manager, Researcher, Reviewer), ngày thêm | N – 1 Project; N – 1 người dùng; 1 Membership – N Approval, Comment |
| ProjectSettings / ReviewSettings | budget tháng, ngưỡng cảnh báo, preset theo stage, số approval, ai được duyệt, cho tự duyệt không, định dạng xuất, notification | 1 – 1 Project |
| Dataset | tên, data location (`platform` hoặc `local`) | N – 1 Project; 1 – N DatasetVersion; 0..N – 1 DataConnection |
| DatasetVersion | hash, nguồn, thời điểm tạo, bất biến | N – 1 Dataset; 1 – N DatasetSnapshot ghim nó; 1 – 1 release log (nếu local) |
| DataConnection | nhà cung cấp (Google Sheets, Drive), phạm vi uỷ quyền | N – 1 Project; 1 – N Dataset |
| ResearchCase | topic, mục tiêu, bối cảnh, ràng buộc, domain, tài liệu tham khảo, dataset tuỳ chọn | N – 1 Project; 1 – N Run; 0..1 – N DatasetVersion (tuỳ chọn) |
| Run | run state, lý do chờ, kết quả kết thúc, token budget, pipeline | N – 1 ResearchCase; 1 – N StageRun; 1 – 0..N Lock (plan stale được lock lại trong cùng run); 1 – 0..N Dossier version |
| StageRun | stage, preset, presence tại lúc bắt đầu, trạng thái contract | N – 1 Run; 1 – 0..N hand-off object version; 1 – N DecisionInboxItem; 1 – N Finding |
| DatasetSnapshot | nguồn, table model, profile, dictionary, cleaning recipe, question map, split, vai trò nguồn, fitness; version, hash, trạng thái object | N – 1 DatasetVersion; N – 1 StageRun; 1 – N HypothesisSet ghim nó |
| HypothesisSet | ≥ 2 hypothesis (claim key khác nhau), 1 primary; version, hash | N – 1 DatasetSnapshot; N – 1 LiteratureBase (version); 1 – N AnalysisPlan ghim nó |
| AnalysisPlan | estimand, protocol, adjustment set, analysis program, fallback, decision rule, bảng diễn giải, robustness set, design diagnosis, family structure, task family, pipeline order, evidence family; version, hash | N – 1 HypothesisSet; N – M ResearchPattern (pattern đã chọn, version đã ghim); 1 – 0..1 Lock; 1 – N EvidenceBundle |
| ResearchPattern | pattern id, version, task family áp dụng, eligibility rule, cột bắt buộc, baseline policy, factor template, metric policy, chart template, statistical plan, failure mode, các action cần người (action pinned hiện có), ràng buộc thứ tự phối hợp, negative test | 1 – N version; N – M AnalysisPlan; 1 – N negative test |
| EvidenceBundle | mười item: kết quả xác nhận, verdict, grade, diagnostics, robustness, deviation log, tried ledger và candidate, bảng và hình, replication package, báo cáo replicator và envelope log; claim ceiling; version, hash | N – 1 AnalysisPlan (qua Lock); 1 – N PaperPack; 1 – 0..N Dossier tham chiếu |
| PaperPack | bản thảo, reporting checklist, claim, hình và bảng, citation, limitation, reproducibility, declaration, kết quả review, định dạng xuất; version, hash | N – 1 EvidenceBundle; 1 – 0..N Dossier tham chiếu |
| LiteratureBase | protocol, search log, quyết định screening, evidence card, evidence map, BibTeX đã kiểm; version | 1 – 1 Project; 1 – N version; stage khác đọc theo version |
| DecisionInboxItem | loại (question, review batch, tentative decision, deviation, candidate, needs-you, release review, spending), option, option đề xuất, lý do, trạng thái, thứ tự chặn | N – 1 StageRun; 1 – 0..1 DecisionLogEntry khi được quyết |
| DecisionLogEntry | action type, level, phiên bản policy, ai quyết (user, agent, AI PI), presence, đã overturn hay chưa | N – 1 Run; 0..1 – 1 DecisionInboxItem |
| Finding | category, severity, anchor (object + field), evidence, failure scenario, cách sửa, kết quả kiểm | N – 1 hand-off object version; N – 1 StageRun |
| Lock | hash spec, hash program, hash golden outputs, snapshot version, split digest, ai khoá, khi nào | N – 1 Run; 1 – 1 AnalysisPlan version; 1 – 1 Envelope |
| Envelope | kết quả confirmatory kín, trạng thái (sealed, unsealed), thời điểm unseal | 1 – 1 Lock |
| ReleaseLog / Release | danh sách chỉ-thêm các aggregate đã rời nơi giữ dữ liệu: loại số, lý do, job, thời điểm | 1 ReleaseLog – 1 DatasetVersion; 1 – N Release |
| Dossier | version, tham chiếu EvidenceBundle và PaperPack đã accepted, hash, trạng thái duyệt | N – 1 Run; 1 – N Approval; 1 – N Comment |
| Approval | quyết định, thời điểm, Dossier version | N – 1 Dossier; N – 1 Membership |
| Comment | nội dung, anchor | N – 1 Membership; N – 1 object bất kỳ của project |
| Notification | loại, người nhận, trạng thái | N – 1 người dùng; 0..1 – 1 DecisionInboxItem |
| AuditEvent | hành động quản trị hoặc bảo mật, ai, khi nào; chỉ-thêm | N – 1 Project (hoặc cấp hệ thống) |
| BudgetLedger | chi tiêu theo run và theo tháng, ngưỡng đã báo | 1 – 1 Project (theo tháng); 1 – N mục chi theo Run |
| ModelProfile | model role (`stage`, `review`, `vision`), model, key tham chiếu, đơn giá | N – 1 Platform; được StageRun dùng |

---

## 6. Runtime view

### 6.a Một run qua năm stage

1. Researcher tạo ResearchCase. Dataset không bắt buộc.
2. Platform kiểm tra project chưa có run active. Nếu đã có, Platform từ chối (ADR-13).
3. Platform tạo Run với pipeline `dataset_first` và gửi policy (preset theo stage), presence và key theo role cho engine đầu.
4. Dataset engine chạy prelude bằng code. Agent chỉ xử lý contract item đỏ. Nếu project không có dataset, engine tìm dataset trong project, tìm dataset public (vai trò `enrichment` hoặc `validation`) hoặc hỏi user qua decision inbox (ADR-14). Join dữ liệu public vào dữ liệu riêng là action pinned. Engine cũng chạy prefilter: gắn cờ tín hiệu dữ liệu (tỷ lệ positive thấp, categorical có cardinality cao, cột group hoặc thời gian, missingness cao) và gợi ý research pattern, chỉ bằng phân phối biên (ADR-17). Dictionary ghi thời điểm sẵn có của biến; biến post-outcome bị gắn cờ.
5. Engine xác định unit of observation và cấu trúc dữ liệu (group, thời gian, panel); Researcher xác nhận (action pinned) trước khi split được tạo (ADR-09). Engine kiểm dòng trùng lặp giữa các phần split và báo cáo dataset shift theo từng loại (covariate, label, concept). Engine công bố DatasetSnapshot. Review loop chạy (6.c). Acceptance theo preset. Với `milestones`, level theo fitness: `fit` là `auto`, `fit_with_limits` là `do_then_review`, `not_fit` là `must_ask`.
6. Hypothesis engine đọc DatasetSnapshot đã ghim và cập nhật Literature Base. Engine công bố HypothesisSet. Việc chọn hypothesis (≥ 2) và primary là action pinned.
7. Experiment_design engine đọc HypothesisSet. Engine ghi task family và chọn research pattern từ registry (ADR-17), rồi ghi pipeline order vào plan. Engine chạy program trên twin. Khi user lock plan (action pinned), Platform ghi Lock.
8. Execution engine chạy vòng đời đã định (6.d), rồi công bố EvidenceBundle.
9. Paper engine đọc EvidenceBundle, AnalysisPlan, Lock, Literature Base, DatasetSnapshot và decision log. Engine công bố PaperPack.
10. Khi mọi stage ở trạng thái accepted, Run `ended(complete)`. AI PI đề xuất next step. User chọn.
11. **Stale.** Nếu một object upstream có version mới, Platform đánh dấu mọi object downstream đã ghim version cũ là `stale`. Không có gì tự cập nhật. User cập nhật qua một acceptance. Khi user cập nhật, stage downstream chạy lại trên version mới.

### 6.b Item must_ask: present và away

1. Engine gặp action có level `must_ask`.
2. Engine tạo DecisionInboxItem với option, option đề xuất và lý do.
3. **Present:** Web app hỏi ngay. Run vào `waiting(decision)` nếu không còn việc độc lập. User trả lời; decision log ghi lại.
4. **Away:** item xếp hàng. Agent tiếp tục mọi action không phụ thuộc item. Item pinned đợi tới khi user quay về.
5. Nếu preset của stage là `autopilot` và user `away`, AI PI quyết định tạm các item không pinned. Mỗi quyết định tạm thành một item loại tentative decision. AI PI không bao giờ quyết định item pinned và không kết thúc run.
6. Khi user quay về, user xác nhận hoặc lật lại (overturn) từng tentative decision. Nếu lật, engine hoàn tác phần phụ thuộc và đánh dấu object bị ảnh hưởng là `stale`.
7. Decision log ghi ai quyết, presence và overturn. Hệ thống tính tỷ lệ overturn theo action type và **đề xuất** nâng level. Hệ thống không tự nâng.
8. Nếu stage không còn việc nào có thể làm mà item pinned vẫn chờ, stage dừng ở trạng thái "sẵn sàng cho action" cùng với item pinned đang chờ, và run ở `waiting(decision)`. Run không kết thúc vì item này trước hạn chờ. Đây không phải run state thứ tư.
9. Thông báo ngoài (email, push) chỉ gửi cho item pinned đang chặn và item `spending`. Item `spending` gửi Project Manager; item pinned gửi người có quyền trả lời item. Cả hai có lời nhắc trước hạn.
10. Mỗi item pinned có hạn chờ (project settings). Hết hạn mà item chưa được trả lời thì run chuyển `waiting(decision)` → `ended(with_gaps)`. Item đóng ở trạng thái chưa trả lời; gap được liệt kê. AI PI và giá trị mặc định không quyết thay user.

### 6.c Review loop

1. Mọi check của object version xanh.
2. Reviewer persona (guard) chạy song song với context mới; reviewer không thấy trace của tác giả.
3. Reviewer tạo finding. Code loại finding thiếu anchor hoặc evidence.
4. Mỗi finding được kiểm bằng code hoặc verifier thứ hai: `confirmed`, `plausible`, `rejected`.
5. Chỉ finding `blocking` đã `confirmed` vào vòng sửa. Finding `major` và `minor` được ghi và hiển thị.
6. Maker sửa. Check chạy lại. Review lại chỉ trên finding đã sửa và field đã đổi.
7. Một finding blocking mới trên field không đổi chỉ hợp lệ khi evidence của nó là một fact tính mới.
8. Tối đa hai vòng sửa. Finding còn lại thành **known risk**, hoặc user quyết định giữa hai phía (Facilitator hiển thị cả hai).
9. Reviewer có precision dưới ngưỡng trên seeded-flaw bench bị hạ severity finding blocking và major.

### 6.d Lock → dry run → envelope → unseal → judge → interpretation

1. Experiment_design yêu cầu action pinned "lock plan". User lock; Platform ghi Lock (hash spec, program, golden outputs, snapshot version, split digest, ai, khi nào). Nếu user `away`, plan dừng ở trạng thái chờ lock tới hạn chờ của item; không ai khoá thay user.
2. Execution dựng repo phân tích từ Lock. Phần đã lock bất biến. Guard kiểm pipeline order trước mọi lần chạy; vi phạm bị chặn hoặc được ghi là deviation (ADR-17).
3. **Rehearsal** trên twin: effect đã cài được phục hồi; kiểm hoán vị sạch.
4. **Dry run** trên dữ liệu thật: chạy toàn bộ program; chỉ trả số hàng, kiểu, missingness, hội tụ, thời gian. Không có ước lượng. Code so với twin (drift).
5. **Confirmatory job** mang cờ envelope. Executor gửi kết quả thẳng tới Platform. Agent chỉ thấy "done" hoặc "error" đã qua error firewall. Sửa và chạy lại được phép vì chưa ai thấy ước lượng.
6. Engine gửi yêu cầu unseal cùng contract status. Platform tự kiểm: có Lock; mọi confirmatory job của Lock đã xong; thời điểm yêu cầu sau lần sửa lane C cuối; level của `unseal` là `auto` hoặc user đã duyệt.
7. Platform mở **mọi** kết quả của Lock cùng lúc và ghi thời điểm unseal.
8. **Judge** bằng code: primary trước; Holm cho secondary; verdict ba vùng theo SESOI; kiểm hoán vị. Verdict là một trong năm giá trị.
9. Interpreter chọn một dòng của bảng diễn giải đã lock cho mỗi hypothesis. Lời văn kết luận lấy từ dòng đó. Code tính grade (A–D) và claim ceiling.
10. Lane D chạy post-hoc (gắn nhãn `post_hoc`); lane P đóng gói. Replicator chạy lại và so hash. Review loop chạy. Engine công bố EvidenceBundle.
11. Lane E chạy từ bước rehearsal, chỉ trên exploration split. Mỗi thủ tục ghi vào tried ledger. Tối đa số candidate cố định mỗi vòng vào decision inbox. Candidate không bao giờ là claim.

### 6.e Local job qua release gate

1. Platform định tuyến job của dataset version có location `local` tới Local Node.
2. Nếu Node offline và job chặn việc, Run vào `waiting(node_offline)`. Việc không cần dữ liệu (twin rehearsal, plan, bản nháp) vẫn tiếp tục. Platform gửi một thông báo gộp.
3. Node kiểm hash của dataset version. Không khớp thì từ chối job và đề xuất version mới.
4. Node chạy job trong sandbox của Node, không mạng, dữ liệu chỉ đọc, chỉ cột đã khai báo.
5. Kết quả đi qua **release gate** theo thứ tự: firewall (ngưỡng ô nhỏ; chỉ id và dạng lỗi cố định) → làm tròn → disclosure mode → kiểm differencing với release log của Node → probe budget của dataset version.
6. Probe budget cạn thì thành gap, không dừng run.
7. Release hợp lệ vào release log (chỉ-thêm). Platform nhận bản sao. Aggregate đi tiếp tới engine; hàng dữ liệu không bao giờ đi.
8. Ở disclosure `strict`, loại số chưa được duyệt tạo item release review trong decision inbox. Researcher hoặc Project Manager của project trả lời.
9. Query bị từ chối được hiển thị cùng lý do.
10. Khi Local Node bị thu hồi, Platform từ chối job cho dữ liệu `local` của Node đó và báo user lý do. Object đã publish vẫn đọc được.

### 6.f Budget

1. **Item.** Mỗi contract item có một phần cố định của token budget run. Khi item tiêu hết phần đó, Harness tạo item **needs-you** (`must_ask` ở mọi preset) với lỗi cuối và những gì đã thử. Run tiếp tục các việc khác.
2. **Run.** Khi token budget của run cạn, run `ended(with_gaps)`: output tốt nhất được công bố; mọi contract item đỏ được liệt kê. Item pinned đang chờ không kết thúc run trước hạn chờ của nó: run ở `waiting(decision)`. Huỷ run từ mọi trạng thái trừ `ended` cho `ended(cancelled)`.
3. **Project.** Hệ thống cảnh báo ở các ngưỡng của budget tháng.
4. Ở 100%, Platform chặn run mới. Run đang chạy vào `waiting(budget_review)` và tạo item `spending` loại `must_ask`.
5. Project Manager duyệt chi thêm (run chạy tiếp) hoặc để run kết thúc `with_gaps`. Item có hạn trả lời; Platform gửi thông báo ngoài (email, push) cho Project Manager khi item được tạo và nhắc trước hạn; hết hạn thì run kết thúc `with_gaps`.
6. **Item pinned.** Mỗi item pinned có hạn chờ (project settings). Platform nhắc trước hạn qua thông báo ngoài. Hết hạn mà item chưa được trả lời thì run `waiting(decision)` → `ended(with_gaps)`; item đóng ở trạng thái chưa trả lời và gap được liệt kê (6.b).

### 6.g Dossier

1. Khi PaperPack được accepted, Platform tạo Dossier version 1: tham chiếu tới EvidenceBundle (PaperPack đã tham chiếu nó) và PaperPack version đã accepted. Platform kiểm hash của từng tham chiếu. Run kết thúc `with_gaps` hoặc `cancelled` trước khi có PaperPack accepted thì không có Dossier.
2. Nếu bundle hoặc pack có version accepted mới, Platform tạo Dossier version mới; version cũ giữ nguyên. Approval của version cũ không chuyển sang version mới.
3. Reviewer và Project Manager đọc và bình luận. Approval theo review settings: số approval, ai được duyệt, có cho tự duyệt không.
4. Khi đủ approval cho version hiện tại, Dossier chuyển sang approved.
5. **Export** ra ngoài project là action pinned và cần Dossier approved. Platform chỉ ghi approval và kiểm hash; Platform không đánh giá khoa học.
6. Mỗi export ghi vào audit log với version Dossier và định dạng.

---

## 7. Deployment view

### 7.1 Node khái niệm

| Node | Chứa | Ghi chú |
|---|---|---|
| User browser | Web app | Không giữ secret dài hạn |
| Platform | Platform; database; object storage | Giữ người, project, run, key, audit, Lock, envelope, Dossier, file dataset `platform` |
| Engine workers | Năm stage engine; Executor (cloud) | Chạy trên Harness; không giữ dữ liệu `local` |
| AI PI | Dịch vụ connector persona | Chỉ nhận tóm tắt, không nhận hàng dữ liệu |
| LLM gateway | Model theo role | Dịch vụ ngoài; không nhận hàng dữ liệu `local` |
| Local Node (máy của user) | Service nền, desktop app, sandbox, release gate, release log | Giữ dữ liệu `local`; có thể chạy không giao diện cho IT |

### 7.2 Trust boundary

| Ranh giới | Giữa | Quy tắc |
|---|---|---|
| TB1 | Browser và Platform | Xác thực người dùng; kiểm quyền theo project ở mọi request |
| TB2 | Platform và Engine | Engine nhận key theo role và policy qua request; engine không có đường tới envelope |
| TB3 | Engine và LLM gateway | Chỉ text và schema; không hàng dữ liệu `local`; secret filter |
| TB4 | Platform/engine và Local Node | Node chỉ phát aggregate qua release gate; hàng dữ liệu không rời máy |
| TB5 | Agent code và dữ liệu thật | Agent chỉ thấy twin; dữ liệu thật qua probe và job; error firewall |
| TB6 | Project và project | Mỗi project cô lập dữ liệu và quyền |

---

## 8. Cross-cutting concepts

### 8.1 Vocabulary

Một khái niệm, một tên. Mọi tài liệu, UI và prompt dùng tên ở [glossary.md](glossary.md). Tên đã bỏ nằm ở glossary §11.

### 8.2 Permission model

| Khái niệm | Quy tắc |
|---|---|
| Action group | Tám nhóm: `read_compute`, `technical_fix`, `content_judgment`, `object_drafting`, `spending`, `acceptance`, `pinned`, `unseal`. Mỗi action type thuộc đúng một nhóm |
| Level | `auto`, `do_then_review`, `must_ask` |
| Preset | Chọn theo stage: `co_work`, `milestones` (mặc định), `autopilot`. Preset đặt level cho từng nhóm |
| Floor | Level thấp nhất của một action type. Override không hạ dưới floor |
| Override | User có thể đổi level của một action type. Level hiệu lực là level của override nếu có, nếu không là level của preset; kết quả không thấp hơn floor |
| Pinned | Luôn `must_ask` ở mọi preset: định nghĩa outcome và estimand; xác nhận unit of observation và cấu trúc dữ liệu trước khi split; chọn hypothesis (≥ 2) và primary; join dữ liệu public vào dữ liệu riêng; lock plan; lệch khỏi thuật toán đã lock; dùng validation source; xuất ra ngoài project |
| `spending` | Có mức trần do Platform Admin đặt (BR-61); không preset nào vượt trần |
| `unseal` | `auto` khi mọi check xanh ở mọi preset; user có thể nâng lên `must_ask` |
| `acceptance` | Ở `milestones`, level theo verdict của code (fitness: xem 6.a) |
| Đổi preset | Áp dụng cho action tương lai; item đang chờ được đánh giá lại; quyết định trong quá khứ không tính lại |
| Presence | `present` hoặc `away`; chỉ đổi cách item `must_ask` chờ; không phải mode |
| Đối xứng | Action của user và của agent đi qua cùng guard, level và check; decision log ghi ai làm |

Bảng level theo preset:

| Group | `co_work` | `milestones` | `autopilot` | Floor |
|---|---|---|---|---|
| `read_compute` | auto | auto | auto | không |
| `technical_fix` | do_then_review | auto | auto | không |
| `content_judgment` | must_ask | do_then_review | auto (có log) | không |
| `object_drafting` | must_ask | do_then_review | do_then_review | do_then_review |
| `spending` | must_ask | must_ask | auto trong trần | auto [1] |
| `acceptance` | must_ask | theo verdict | do_then_review | auto |
| `pinned` | must_ask | must_ask | must_ask | must_ask |
| `unseal` | auto khi mọi check xanh | như `co_work` | như `co_work` | auto [2] |

[1] `spending` có mức trần chi tiêu do Platform Admin đặt (BR-61). Chi tiêu vượt mức trần luôn `must_ask`. Không preset nào vượt trần.

[2] User có thể nâng level của `unseal` lên `must_ask`.

### 8.3 Numbers from code

Text của model chỉ mang reference tới record. Code render con số. Một chữ số trong text của model không phải reference thì fail check (năm, số mục và số phần được cho phép). Verdict, grade, claim ceiling và fitness do code tính. Chart đọc số từ EvidenceBundle và không fit lại model. (ADR-07)

### 8.4 Immutability, hash, version, stale

- Hand-off object có version, hash nội dung, bất biến sau acceptance.
- Object ghim version của upstream bằng id và hash.
- Dataset version bất biến; mọi phân tích ghim một dataset version.
- Lock bất biến. Thay đổi thuật toán đã lock là deviation (pinned) và vào deviation log.
- Version upstream mới đánh dấu downstream là `stale`. Không có cập nhật tự động.
- Replay: cùng object đã ghim, cùng Lock, cùng seed cho cùng hash; replicator so hash.

### 8.5 Self-healing và budget

Một check đỏ là một task cho agent loop. Trace hiển thị từng item: đỏ → action → xanh. Có một budget cho mỗi run và một phần budget cho mỗi item; không có bộ đếm retry riêng cho từng cơ chế. Hết phần của item thì needs-you. Hết budget run thì `ended(with_gaps)`. Lỗi kỹ thuật không phục hồi được thì `ended(failed_technical)`. Thiếu model hoặc credential thì run kết thúc `failed_technical` với lỗi rõ ràng; không có output giả. (ADR-11)

Bảng tình huống lỗi chéo stage:

| Tình huống | Hành vi |
|---|---|
| Model hoặc credential thiếu | Lỗi rõ ràng; `ended(failed_technical)`; không có output mẫu |
| Một nguồn literature ngừng | Ghi lỗi theo nguồn; tiếp tục nguồn khác; gap nếu mọi nguồn lỗi |
| Node offline và job chặn việc | `waiting(node_offline)`; việc khác tiếp tục; một thông báo gộp |
| File nguồn đổi giữa run | Job bị từ chối do hash không khớp; đề xuất version mới |
| File nguồn bị xoá | Run kết thúc ở job đó với gap; dữ liệu đã release giữ nguyên |
| Node bị thu hồi | Job local bị từ chối; object đã công bố vẫn đọc được |
| Budget item hết | Item needs-you; run tiếp tục việc khác |
| Item pinned quá hạn chờ | `ended(with_gaps)`; item đóng chưa trả lời; gap được liệt kê; không ai quyết thay user |
| Reviewer bất đồng sau hai vòng | Known risk hoặc user quyết định với hai phía |

Thông báo cho người dùng theo message catalogue (ở Report III), không theo mã kỹ thuật.

### 8.6 Review và persona

Review độc lập bắt buộc cho mọi stage. Persona là lens với mandate, taxonomy finding, skill, tool và precision đo được; có ba loại: maker, guard và connector. Guard chạy song song và không đọc nhau. Một persona chỉ bật khi seeded-flaw bench cho thấy nó bắt được điều persona khác bỏ sót. User gọi được persona bất kỳ trên object bất kỳ.

| Stage | Maker | Guard |
|---|---|---|
| dataset | Data Steward, Data Scout | Data Auditor, Privacy Officer, Domain Expert |
| hypothesis | Theorist, Librarian | Skeptic, Methodologist, Prior-art Checker |
| experiment_design | Trialist, Analyst | Methodologist, Skeptic, Domain Expert, Equity Reviewer, Code Auditor |
| execution | Engineer, Interpreter | Skeptic, Replicator, Code Auditor, Privacy Officer |
| paper | Scribe | Reporting Editor, Skeptic, Reviewer 2, Figure Reviewer |
| connector | AI PI, Explainer, Facilitator | — |

### 8.7 Security và privacy

| Chủ đề | Quy tắc |
|---|---|
| Authentication | Đăng nhập bằng email không mật khẩu hoặc Google sign-in (FR-146). Hai cách ánh xạ về cùng một user theo email đã xác minh |
| Authorization | Quyền theo role trong project (Platform Admin, Project Manager, Researcher, Reviewer). Mọi request kiểm quyền. Platform Admin chỉ thấy metadata của project (danh sách, member, usage, trạng thái run); không mở dataset, object hay bản thảo nếu không là member |
| Project isolation | Dữ liệu, run, Literature Base, inbox và audit của một project không đọc được từ project khác |
| Secrets | Key theo role đi kèm request; secret filter chặn key trong output và trace; key không vào object |
| Data firewall | Agent không thấy hàng dữ liệu thật. Chỉ aggregate, qua release gate. Exception từ dữ liệu thật được rút gọn thành loại lỗi, cột, số hàng ảnh hưởng và dòng code |
| Release gate | Một điểm duy nhất cho mọi release; mọi release vào release log |
| Envelope | Kết quả confirmatory chỉ qua đường code của Platform; agent không có đường tới |
| Join dữ liệu public vào dữ liệu riêng | Action pinned |
| Audit | Mọi thao tác quản trị và bảo mật vào audit log chỉ-thêm |
| Threat model | Platform và model được tin là không cần hàng dữ liệu và không bao giờ nhận. Node chỉ chạy code của Platform trong sandbox. Rủi ro còn lại chính là suy luận từ nhiều aggregate; được xử lý bằng ngưỡng ô nhỏ, làm tròn, kiểm differencing, probe budget và nhiễu trên probe thăm dò |

### 8.8 Observability

| Kênh | Nội dung |
|---|---|
| Trace event | Mọi action và thay đổi check, theo engine; stream tới web app |
| Decision log | Action type, level, phiên bản policy, ai quyết, presence, đã overturn hay chưa |
| Audit log | Thao tác quản trị và bảo mật |
| Release log | Mọi aggregate đã rời nơi giữ dữ liệu |
| Overturn metric | Tỷ lệ overturn theo action type; đề xuất nâng level (không tự nâng) |
| Metric vận hành | Số câu hỏi mỗi run, thời gian bị chặn, precision của persona trên seeded-flaw bench |
| Lab notebook | Tóm tắt, đề xuất, quyết định tạm của AI PI và lý do |

### 8.9 State models

Run state:

```text
running ─┬─> waiting(decision | node_offline | budget_review) ─> running
         └─> ended(complete | with_gaps | failed_technical)
waiting(budget_review) ─> ended(with_gaps)   (item spending quá hạn)
waiting(decision) ─> ended(with_gaps)        (item pinned quá hạn chờ)
bất kỳ trạng thái trừ ended ─> ended(cancelled)
```

| Run state | Điều kiện vào |
|---|---|
| `running` | Run bắt đầu hoặc tiếp tục |
| `waiting(decision)` | Item `must_ask` (kể cả item pinned) chặn mọi việc còn lại, khi user `present` hoặc `away`. Việc không phụ thuộc item vẫn tiếp tục. Item pinned có hạn chờ |
| `waiting(node_offline)` | Job local chặn việc và Node offline |
| `waiting(budget_review)` | Budget tháng của project chạm 100% |
| `ended(complete)` | Mọi stage accepted |
| `ended(with_gaps)` | Token budget của run cạn, item `spending` quá hạn, hoặc item pinned quá hạn chờ; output tốt nhất được công bố; item đỏ được liệt kê |
| `ended(failed_technical)` | Lỗi kỹ thuật không phục hồi được |
| `ended(cancelled)` | Project Manager hoặc Researcher đã tạo run huỷ run; object đã accepted được giữ, item đang chờ được đóng |

Từ `waiting(budget_review)`: item `spending` có hạn trả lời (project settings). Hết hạn, hoặc Project Manager để run kết thúc, thì `ended(with_gaps)`. Từ `waiting(decision)`: item pinned có hạn chờ (project settings). Hết hạn mà item chưa được trả lời thì `ended(with_gaps)` (FR-265); không ai quyết thay user (FR-266). Từ mọi trạng thái trừ `ended`, huỷ run đưa run tới `ended(cancelled)` (FR-22).

Object state:

```text
draft → checks_red ⇄ checks_green → in_review → ready → accepted → (locked)
bất kỳ trạng thái → stale
```

| Object state | Nghĩa |
|---|---|
| `draft` | Đang dựng |
| `checks_red` / `checks_green` | Có hoặc không còn contract item đỏ |
| `in_review` | Review loop đang chạy |
| `ready` | Review xong; chờ acceptance |
| `accepted` | Đã chấp nhận; bất biến |
| `locked` | Chỉ AnalysisPlan: đã có Lock |
| `stale` | Upstream đã ghim có version mới |

---

## 9. Architecture decisions

Mỗi ADR có Status, Context, Decision, Alternatives considered, Consequences. ID là vĩnh viễn từ v3.0. Ánh xạ ADR cũ → ADR mới nằm ở [id-mapping.md](id-mapping.md#ánh-xạ-architecture).

### ADR-01 — Pipeline theo stage với năm hand-off object có kiểu, version, bất biến

- **Status:** Accepted
- **Context:** Pipeline trước dùng ba stage và artifact không có hợp đồng chặt. Quality goal cần truy vết và replay.
- **Decision:** Pipeline có năm stage: dataset, hypothesis, experiment_design, execution, paper. Mỗi ranh giới có đúng một hand-off object có kiểu, version, hash và bất biến sau acceptance. Stage đọc version upstream đã ghim. Version upstream mới làm downstream `stale`.
- **Alternatives considered:** (a) Workflow tự do do agent định. (b) Một điều phối viên duy nhất giữ toàn bộ trạng thái.
- **Consequences:** Mỗi ranh giới có contract kiểm được. Truy vết và replay đơn giản. Đổi cấu trúc object cần đổi version contract. Không có cập nhật ngầm.

### ADR-02 — Một harness chung; engine chỉ khác HarnessSpec

- **Status:** Accepted
- **Context:** Bản trước có cơ chế riêng ở từng engine; luật nằm ở nhiều chỗ.
- **Decision:** Mọi engine chạy trên một harness: agent loop, action pipeline, workspace, live trace, budget và hand-off. Một engine khai báo HarnessSpec: contract, prelude, tool, skill, guard, action type, reviewer, budget, hand-off object.
- **Alternatives considered:** (a) Engine riêng cho từng stage với cơ chế riêng.
- **Consequences:** Guard, check, trace và decision log nằm một chỗ. Một engine có thể gần như không cần agent nếu prelude thoả contract. Thêm một cơ chế vào harness ảnh hưởng mọi engine; cần kiểm cho cả năm.

### ADR-03 — Platform sở hữu quản trị; Platform không đánh giá khoa học

- **Status:** Accepted
- **Context:** Cần một nơi duy nhất cho người, quyền, budget, key, audit và các cơ chế chống gian lận (Lock, envelope).
- **Decision:** Platform sở hữu người, project, run, budget, key, audit, Lock, envelope và Dossier. Platform không đánh giá nội dung khoa học. Engine làm khoa học và không lưu người, key hay project.
- **Alternatives considered:** (a) Mỗi engine tự quản trị quyền và budget.
- **Consequences:** Ranh giới rõ; engine thay được. Platform chỉ kiểm sự kiện của chính nó (Lock tồn tại, job đã xong, thời điểm). Platform trở thành điểm tin cậy; cần cô lập và audit chặt.

### ADR-04 — Kiểm soát của con người theo loại action

- **Status:** Accepted
- **Context:** Một công tắc chế độ cho toàn run và các điểm chặn cố định theo stage buộc user vào hai cực: hỏi mọi thứ hoặc không hỏi gì.
- **Decision:** Mỗi action type thuộc một trong tám action group. Preset theo stage (`co_work`, `milestones`, `autopilot`) đặt level cho từng nhóm. Presence (`present`, `away`) chỉ đổi cách item `must_ask` chờ. Floor và action pinned giới hạn những gì preset và override được làm. Level hiệu lực: override nếu có, nếu không là level của preset, và không thấp hơn floor.
- **Alternatives considered:** (a) Một công tắc chế độ cho toàn run (hai mức: hỏi nhiều hoặc tự chạy). (b) Điểm chặn cố định theo stage.
- **Consequences:** User chỉnh được theo từng loại việc. Có thêm bảng quyền cần thiết kế và kiểm. Quyết định có thể đo bằng overturn. Agent và user dùng cùng đường.

### ADR-05 — Một decision inbox chéo stage với theo dõi overturn

- **Status:** Accepted
- **Context:** Điểm chặn cố định theo stage làm user trả lời rải rác và bị chặn không cần thiết; một thông báo cho mỗi quyết định gây mệt.
- **Decision:** Một decision inbox cho mọi stage, tám loại item (gồm `spending`). Sắp xếp theo mức chặn và thời gian chặn. Review item của một object version được gộp. Thông báo ngoài chỉ cho item pinned đang chặn và item `spending`. Decision log ghi overturn; hệ thống đề xuất nâng level theo tỷ lệ overturn và không tự nâng.
- **Alternatives considered:** (a) Điểm chặn cố định theo stage. (b) Một thông báo cho mỗi quyết định.
- **Consequences:** User có một nơi để xử lý. Cần Platform gộp item của mọi engine. Tỷ lệ overturn là số đo vận hành.

### ADR-06 — Review độc lập bắt buộc, persona, finding đã kiểm, tối đa hai vòng sửa

- **Status:** Accepted
- **Context:** Self-review bỏ sót lỗi; review tuỳ chọn không bảo đảm. Check bằng code chỉ bắt lỗi có luật.
- **Decision:** Review loop chạy một lần cho mỗi object version sau khi mọi check xanh. Reviewer có context mới và không thấy trace của tác giả. Finding phải có anchor và evidence. Finding được kiểm trước khi sửa; chỉ blocking đã confirmed vào vòng sửa. Tối đa hai vòng; phần còn lại là known risk hoặc user quyết định. Precision đo bằng seeded-flaw bench.
- **Alternatives considered:** (a) Self-review của tác giả. (b) Reviewer tuỳ chọn. (c) Revision không giới hạn.
- **Consequences:** Chi phí model tăng cho mỗi object. Lỗi lọt qua check có cơ hội bị bắt. Vòng sửa có giới hạn nên run vẫn kết thúc.

### ADR-07 — Con số và verdict từ code

- **Status:** Accepted
- **Context:** Nếu model viết số, người đọc có thể tin đó là kết quả đã tính. Đây là lỗi nghiêm trọng nhất của hệ thống kiểu này.
- **Decision:** Mọi con số, verdict (năm giá trị), grade, claim ceiling, fitness và verdict bảng diễn giải do code tính. Text model chỉ mang reference tới record. Một chữ số không phải reference thì fail check. Chart đọc số từ bundle, không fit lại.
- **Alternatives considered:** (a) Model viết số và kiểm sau.
- **Consequences:** Integrity có cơ chế kiểm máy. Prompt phải nêu rõ luật. Mọi hiển thị số cần qua renderer của code. Text kém tự nhiên hơn.

### ADR-08 — Lock, envelope, unseal thực thi ở Platform bằng đường code

- **Status:** Accepted
- **Context:** Mối đe doạ là agent thấy ước lượng confirmatory trước khi phân tích xong và chỉnh theo đó (p-hacking).
- **Decision:** Platform ghi Lock. Job confirmatory gửi kết quả thẳng tới envelope ở Platform. Agent chỉ thấy "done" hoặc "error" đã rút gọn. Unseal do Platform kiểm: có Lock; mọi job đã xong; thời điểm sau lần sửa lane C cuối; level `auto` hoặc user đã duyệt. Mở mọi hypothesis cùng lúc và ghi thời điểm. Kết quả không mã hoá.
- **Alternatives considered:** (a) Tin agent không nhìn. (b) Mã hoá kết quả.
- **Consequences:** Kiểm soát truy cập bằng đường code đủ cho mối đe doạ này. Platform là điểm tin cậy. Hệ thống không chống được kẻ có quyền sửa code của Platform.

### ADR-09 — Chính sách split quyết định ở dataset stage; tier xác nhận; e-value chỉ trên hàng mới

- **Status:** Accepted
- **Context:** Split ngẫu nhiên ba phần cố định không xét power. Candidate từ khám phá cần cách xác nhận có thứ bậc.
- **Decision:** Dataset stage tính power cho hypothesis đã chọn. Nếu n giữ power đủ và còn phần dự trữ thì split ba phần (exploration / confirmation / reserve); nếu không thì hai phần; dưới n tối thiểu thì không split và ghi là limitation. Split tôn trọng unit of observation và cấu trúc dữ liệu: hàng cùng group không nằm ở hai phần; dữ liệu có trật tự thời gian chia theo thời gian. Researcher xác nhận unit và cấu trúc (action pinned) trước khi split được tạo. Tier xác nhận từ mạnh đến yếu: `replicated`, `reserve`, `unsealed_untouched`, `unsealed_touched`. Chỉ `replicated` và `reserve` ghi e-value vào ledger.
- **Alternatives considered:** (a) Split ngẫu nhiên ba phần cố định.
- **Consequences:** Split gắn với power thật của câu hỏi. Tích e-value chỉ hợp lệ trên hàng mới. Dataset stage cần hypothesis nháp sớm để tính power.

### ADR-10 — Local Node: hàng dữ liệu không rời máy; một release gate; không cần Docker

- **Status:** Accepted
- **Context:** Nhiều dữ liệu không được rời máy user, nhưng hệ thống vẫn phải tự làm việc.
- **Decision:** Local Node giữ dữ liệu `local` và chạy job cạnh dữ liệu. Chỉ aggregate rời đi, qua một release gate (ngưỡng ô nhỏ, làm tròn, disclosure, kiểm differencing, probe budget). Mỗi release vào release log chỉ-thêm. Disclosure `standard` hoặc `strict`. Node tự có isolation; user không cài Docker. Nếu máy không có isolation, Node chỉ chạy các family đã đăng ký và nói rõ trong manifest.
- **Alternatives considered:** (a) Upload mọi thứ lên Platform. (b) Sandbox Docker trên máy user.
- **Consequences:** Data privacy có điểm kiểm duy nhất. Cần twin dựng từ aggregate; dry run bắt drift. Mức isolation khác nhau theo OS và được khai báo.

### ADR-11 — Self-healing với một budget cho mỗi run; run kết thúc với gap

- **Status:** Accepted
- **Context:** Nhiều bộ đếm retry (thang heal, rerun, vòng, iteration) khó hiểu và có thể treo.
- **Decision:** Check đỏ là task của agent loop. Có một budget cho mỗi run; mỗi item có một phần cố định. Hết phần của item thì needs-you. Hết budget run thì `ended(with_gaps)` với output tốt nhất và item đỏ được liệt kê. Item pinned có hạn chờ; hết hạn mà chưa trả lời thì run cũng `ended(with_gaps)`, không ai quyết thay user. Không có bộ đếm riêng cho từng cơ chế.
- **Alternatives considered:** (a) Bộ đếm retry cho từng cơ chế. (b) Thang heal nhiều bậc. (c) Dừng treo chờ user.
- **Consequences:** Run luôn kết thúc; không có lỗi bị giấu. Cần chọn tỷ lệ phần của item; chọn sai làm item chuyển needs-you quá sớm hoặc quá muộn.

### ADR-12 — Dossier là tham chiếu; approval theo review settings; export cần approval

- **Status:** Accepted
- **Context:** Cần một gói để duyệt và chia sẻ mà không nhân đôi nội dung hay biến Platform thành người đánh giá khoa học.
- **Decision:** Dossier gồm tham chiếu tới version EvidenceBundle và PaperPack đã accepted, và chỉ được tạo khi run có PaperPack accepted. Platform đánh version Dossier, kiểm hash và ghi approval theo review settings của project. Export ra ngoài project cần Dossier approved.
- **Alternatives considered:** (a) Platform dựng nội dung. (b) Không có bước approval.
- **Consequences:** Không có bản sao nội dung để lệch. Approval gắn với một version cụ thể. Version mới cần approval mới.

### ADR-13 — Một run active cho mỗi project

- **Status:** Accepted
- **Context:** Run đồng thời cùng project tranh dữ liệu, Literature Base, budget và inbox.
- **Decision:** Mỗi project có tối đa một run active.
- **Alternatives considered:** (a) Nhiều run đồng thời cho một project.
- **Consequences:** Đơn giản hoá trạng thái, budget và inbox. Hạn chế thông lượng cho một project; project mới có thể giải quyết nhu cầu song song.

### ADR-14 — Dataset tuỳ chọn khi bắt đầu; pipeline luôn `dataset_first`

- **Status:** Accepted
- **Context:** Nhiều researcher bắt đầu bằng câu hỏi, chưa có dataset.
- **Decision:** Dataset không bắt buộc khi bắt đầu run. Pipeline luôn là `dataset_first`. Dataset stage tìm dataset trong project hoặc public (vai trò `enrichment` hoặc `validation`; join vào dữ liệu riêng là action pinned), hoặc hỏi user.
- **Alternatives considered:** (a) Bắt buộc có dataset. (b) Đổi pipeline theo việc có dataset hay không.
- **Consequences:** Một pipeline duy nhất. Dataset stage chịu cả hai điểm vào (question first, table first) và trường hợp không có dữ liệu.

### ADR-15 — Budget tháng của project có ngưỡng; ở 100% chặn run mới và chuyển run sang budget review

- **Status:** Accepted
- **Context:** Chi phí model là rủi ro lớn; dừng cứng làm mất việc, chỉ cảnh báo thì không kiểm soát.
- **Decision:** Project có budget tháng. Hệ thống cảnh báo ở các ngưỡng. Ở 100%, Platform chặn run mới; run đang chạy vào `waiting(budget_review)` và tạo item `spending` `must_ask`. Project Manager duyệt chi thêm hoặc để run `ended(with_gaps)`. Item `spending` có hạn trả lời; hết hạn thì run `ended(with_gaps)`, nên run không treo.
- **Alternatives considered:** (a) Dừng cứng ngay. (b) Chỉ cảnh báo. (c) Tự động pause.
- **Consequences:** Người có thẩm quyền quyết định chi thêm. Run không mất công việc. Cần thông báo đúng người khi item `spending` xuất hiện.

### ADR-16 — Tài liệu định nghĩa hệ thống ở mức khái niệm; code đi theo

- **Status:** Accepted
- **Context:** Tài liệu phản ánh code cũ bị lỗi thời mỗi commit và lẫn trạng thái triển khai.
- **Decision:** Tài liệu định nghĩa hệ thống ở mức khái niệm. Code theo tài liệu. Giá trị kỹ thuật (tên setting, số mặc định, schema, route, cổng) nằm trong plan của repo code. Khi code khác tài liệu, đó là việc cho code hoặc một thay đổi ghi qua changelog.
- **Alternatives considered:** (a) Tài liệu phản chiếu code.
- **Consequences:** Tài liệu bền. Cần kỷ luật đồng bộ qua changelog. Người đọc phải mở repo code để biết giá trị cụ thể.

### ADR-17 — Research pattern registry và pipeline order chống leakage

- **Status:** Accepted
- **Context:** Một workflow cho mỗi dataset hoặc mỗi đề tài không mở rộng được. Leakage thường đến từ thứ tự tiền xử lý sai (ví dụ resampling trước split), và reviewer bắt lỗi quá muộn.
- **Decision:** Hệ thống giữ một registry research pattern. Mỗi pattern có version và gồm task family áp dụng, eligibility rule, cột bắt buộc, baseline policy, factor template, metric policy, chart template, statistical plan, failure mode và các action cần người; các action này dùng lại action pinned, không thêm điểm chặn mới. Mỗi pattern có negative test. AnalysisPlan ghi pattern đã chọn, task family và pipeline order. Prefilter của dataset stage gợi ý pattern chỉ bằng phân phối biên; AI gợi ý, user chọn. Pipeline order bắt buộc: split trước; bước học từ dữ liệu chỉ fit trong phần train; resampling chỉ trên phần train; calibration và threshold chọn trên phần validation; phần confirmation dùng một lần. Guard của execution chặn vi phạm trước khi chạy, hoặc ghi vi phạm là deviation. Khi phối hợp nhiều pattern, ràng buộc thứ tự của registry quyết định thứ tự hợp lệ.
- **Alternatives considered:** (a) Một workflow cho mỗi dataset hoặc mỗi project mẫu. (b) Để agent tự quyết thứ tự tiền xử lý và để reviewer bắt lỗi sau.
- **Consequences:** Thêm pattern không đổi harness. 60 project mẫu thành ca kiểm thử của pattern. Registry cần bảo trì và version. Guard thứ tự phải được kiểm cho mọi pattern. Negative test là nguồn cho red-team catalogue.

### ADR-18 — Claim type `method_comparison` (Should, sau MVP)

- **Status:** Accepted
- **Context:** Hệ thống nghiên cứu hiện tượng trên dữ liệu bảng bằng claim type `association`, `causal` và `prediction`. Researcher cũng cần so sánh các phương pháp ML trên cùng dữ liệu với cùng mức chặt chẽ.
- **Decision:** Thêm claim type `method_comparison` bên cạnh `association`, `causal` và `prediction`. Nó dùng pattern G (tối ưu hyperparameter), H (ensemble và stacking), I (ablation), J (budget-aware), kèm baseline policy F. Nó cần so sánh theo cặp trên từng fold và seed, nhiều seed, tuning budget bằng nhau, nested validation khi có tuning, hiệu chỉnh so sánh nhiều lần và giữ kết quả negative. Nó chạy trên cùng harness, Lock, envelope và verdict. Priority Should, sau MVP; MVP không đổi.
- **Alternatives considered:** (a) Chỉ hỗ trợ nghiên cứu hiện tượng, không có `method_comparison`. (b) Đưa vào MVP. (c) Một engine riêng cho so sánh phương pháp.
- **Consequences:** Phạm vi rộng hơn. Không thêm cơ chế mới cho Lock, envelope hay verdict. Rủi ro phạm vi nằm ở R-14.

---

## 10. Quality requirements

### 10.1 Quality tree

| Quality goal | Thuộc tính | Cách bảo đảm (ADR) |
|---|---|---|
| Integrity | Không con số do model viết; không lỗi bị giấu; confirmatory không bị thấy sớm; leakage bị phát hiện hoặc chặn | ADR-06, ADR-07, ADR-08, ADR-11, ADR-17 |
| Traceability | Mọi claim và con số trỏ về record; object ghim version | ADR-01, ADR-07, ADR-12 |
| Replayability | Cùng input ghim cho cùng hash | ADR-01, ADR-08 |
| Data privacy | Hàng dữ liệu `local` không rời máy; mọi release có log | ADR-10 |
| Human control with progress | Quyền theo loại action; run luôn kết thúc; chi tiêu có trần | ADR-04, ADR-05, ADR-11, ADR-15 |

### 10.2 Quality scenario

| ID | Quality goal | Stimulus | Response | Measure |
|---|---|---|---|---|
| QS-01 | Integrity | Paper engine viết một đoạn có chữ số không phải reference | Check fail; đoạn quay lại Scribe | 0 chữ số ngoài danh sách cho phép (năm, số mục, số phần) trong PaperPack đã accepted; kiểm ở mỗi version |
| QS-02 | Integrity | Agent thử đọc kết quả confirmatory trước unseal | Platform không trả kết quả; agent chỉ thấy "done" hoặc "error" | 0 ước lượng confirmatory trong trace và workspace trước thời điểm unseal, kiểm trên mọi run |
| QS-03 | Integrity | Unseal được yêu cầu trước lần sửa lane C cuối | Platform từ chối | 100% yêu cầu unseal sớm hơn lần sửa cuối bị từ chối |
| QS-04 | Traceability | Reviewer chọn ngẫu nhiên một claim trong PaperPack | Claim trỏ tới verdict, dòng diễn giải và record trong bundle | 100% claim trong Abstract, Results và Discussion có verdict và dòng diễn giải |
| QS-05 | Replayability | Replicator chạy lại package của một EvidenceBundle | Hash kết quả bằng hash của bundle | 100% item có hash; replicator hash bằng hash bundle, nếu không item đỏ |
| QS-06 | Data privacy | Một job local chạy trọn một run | Chỉ aggregate rời Node | 0 hàng dữ liệu trong mọi message ra ngoài (kiểm bằng bắt gói của kịch bản test); số release trong release log bằng số release Platform giữ |
| QS-07 | Data privacy | Hai query có tập hàng khác nhau ít hơn ngưỡng ô nhỏ | Release gate từ chối query thứ hai | 100% query như vậy bị từ chối và hiển thị lý do |
| QS-08 | Human control with progress | Stage dùng hết phần budget của một item | Tạo item needs-you; run tiếp tục việc khác | 1 item needs-you cho mỗi item hết phần; 0 retry ngoài phần |
| QS-09 | Human control with progress | Budget run cạn khi còn item đỏ | Run `ended(with_gaps)` | 100% run kết thúc ở một trong bốn kết quả của `ended`; 0 run ở trạng thái chờ vô hạn không có item chờ user |
| QS-10 | Human control with progress | Budget tháng chạm 100% khi run đang chạy | Run vào `waiting(budget_review)`; tạo item `spending`; chặn run mới | 100% run mới bị chặn; 1 item `spending` cho mỗi run bị ảnh hưởng |
| QS-11 | Human control with progress | User `away` ở `autopilot`; có item pinned và không pinned | AI PI quyết tạm item không pinned; item pinned chờ | 0 quyết định của AI PI trên item pinned; 100% quyết định tạm xuất hiện trong inbox khi user quay về |
| QS-12 | Integrity | Review loop không giải quyết xong một finding blocking | Sau hai vòng sửa, finding thành known risk hoặc chờ user | Số vòng sửa mỗi object version không quá 2; 100% finding còn lại hiển thị trong PaperPack |
| QS-13 | Integrity | Dataset có cột post-outcome và dòng trùng giữa các phần split (cài sẵn trong red-team catalogue) | Dataset stage gắn cờ post-outcome và báo cáo dòng trùng trước khi DatasetSnapshot được accepted | Tỷ lệ phát hiện leakage cài sẵn trên seeded-flaw bench ít nhất 90% (SM-17) |
| QS-14 | Integrity | Plan hoặc agent fit một bước học từ dữ liệu (ví dụ resampling) trước split hoặc trên phần ngoài phần train | Guard của execution chặn trước khi chạy, hoặc ghi vi phạm là deviation | Tỷ lệ vi phạm pipeline order cài sẵn bị chặn trước khi chạy trên seeded-flaw bench là 100% (SM-18) |
| QS-15 | Human control with progress | User `away` quá hạn chờ của một item pinned | Platform nhắc trước hạn; hết hạn run `waiting(decision)` → `ended(with_gaps)`; item đóng chưa trả lời; gap được liệt kê | 100% item pinned quá hạn đóng chưa trả lời; 0 quyết định của AI PI hay giá trị mặc định trên item pinned; 0 run ở `waiting(decision)` quá hạn chờ |

---

## 11. Risks and technical debt

Các rủi ro dưới đây ở mức thiết kế. Trạng thái triển khai nằm ngoài tài liệu này.

| ID | Rủi ro | Tác động | Giảm thiểu |
|---|---|---|---|
| R-01 | Reviewer có lỗi tương quan với tác giả (cùng model) | Lỗi lọt qua review | Dùng model role `review` riêng; persona precision đo trên seeded-flaw bench; hạ severity khi dưới ngưỡng |
| R-02 | Suy luận từ nhiều aggregate rò thông tin cá nhân | Vi phạm data privacy | Ngưỡng ô nhỏ, làm tròn, kiểm differencing, probe budget, nhiễu trên probe thăm dò, release log kiểm được |
| R-03 | Twin lệch dữ liệu thật | Plan chạy tốt trên twin nhưng lỗi trên dữ liệu thật | Dry run so với twin; sửa trước envelope vì chưa ai thấy ước lượng |
| R-04 | Platform là điểm tin cậy duy nhất cho envelope | Kẻ sửa code Platform thấy kết quả sớm | Kiểm soát truy cập, audit log chỉ-thêm, review code; ghi rõ ADR-08 không chống được kẻ có quyền sửa Platform |
| R-05 | Chi phí model vượt kỳ vọng | Run hết budget sớm | Budget run; phần của item; budget tháng; thông báo ở ngưỡng; Project Manager duyệt chi thêm |
| R-06 | Phần của item đặt sai | Item chuyển needs-you quá sớm hoặc quá muộn | Đây là một setting đo được; theo dõi tỷ lệ needs-you trên metric vận hành |
| R-07 | Mệt mỏi vì approval ở `co_work` và `milestones` | User chấp nhận vô điều kiện | Gộp review item; tỷ lệ overturn; gợi ý nâng hoặc hạ level; không tự đổi |
| R-08 | Nguồn literature thiếu hoặc lỗi | Literature Base nghèo | Ghi lỗi theo nguồn; dùng nguồn khác; ghi gap; chỉ dùng full text open access |
| R-09 | Mức isolation của Local Node khác nhau theo OS | Không chạy được code do agent viết trên một số máy | Node khai báo khả năng trong manifest; fallback chạy family đã đăng ký; kế hoạch biết trước |
| R-10 | Giới hạn một run active làm chậm team | Thông lượng thấp trong một project | Chấp nhận có chủ ý (ADR-13); dùng nhiều project cho việc song song |
| R-11 | Tài liệu và code lệch | Hiểu sai hệ thống | Đồng bộ qua changelog; ADR-16 |
| R-12 | Phụ thuộc LLM gateway | Run lỗi khi gateway ngừng | Lỗi rõ ràng, `ended(failed_technical)`; không output mẫu; object đã công bố vẫn đọc được |
| R-13 | Team nhỏ, học kỳ cố định | Không đủ thời gian cho mọi persona và bench | Một harness (ADR-02); chỉ bật persona có giá trị đo được; JFE xếp Could |
| R-14 | Phạm vi mở rộng sang `method_comparison` và 60 case mẫu | Làm loãng MVP | Should, sau MVP; MVP không đổi (ADR-18); case có pattern G–J theo `method_comparison` |

---

## 12. Glossary

Xem [glossary.md](glossary.md). Tài liệu này không định nghĩa lại thuật ngữ.

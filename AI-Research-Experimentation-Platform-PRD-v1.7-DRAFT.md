# Product Requirements Document (PRD)
## AI Research Experimentation Platform

**Document Type:** Product Requirements Document\
**Version:** 2.2 Draft (2026-10-28)\
**Status:** Draft\
**Liên quan:** [BRD](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md) · [Architecture](architecture.md) · [changelog](changelog.md)

> **Implementation boundary:** Current release supports versioned tabular intake/profile, evidence-linked hypotheses and a reviewed/locked experiment-design plan. It does not yet execute experiments or produce statistical verdicts/dossiers. Structure-aware split policy is the next tabular increment (FE-16).

---

# 1. Product Summary

Web application cho nhóm nghiên cứu. Người dùng tạo project, upload/import dataset version (tuỳ chọn), tạo một `ResearchCase`, rồi theo dõi run qua các engine. Nếu có `dataset_version_id`, pipeline đi theo `dataset → hypothesis → experiment_design`; nếu không có dataset, pipeline là `hypothesis → experiment_design`. `explore_dataset` chỉ là intent đặc biệt để dataset stage đề xuất problem khi cần.

Current release tạo:

1. `dataset.data_card/v1` và `dataset.brief/v1` từ aggregates của dataset;
2. evidence, gaps và falsifiable hypotheses;
3. experiment plan, hoặc statistical analysis plan khi có data card, có critique/validation và lock.

FE-16/HGAR roadmap sau đó mới thêm structure classification, split policy, protocol freeze, sandbox execution, evidence results, verdict và dossier.

Phạm vi sản phẩm còn gồm **JFE (Journal Fingerprint Extraction)** để xây journal profile từ corpus có provenance và **Writing AIF (Argument Interchange Format) / ASW** để chuyển research outputs đã kiểm tra thành bản thảo có claim/evidence lineage. JFE profile có lifecycle độc lập và được Writing pin tại journal merge. Findings và kết luận trong bản thảo phải có evidence hợp lệ và được phê duyệt.

# 2. Product Goals

| ID | Mục tiêu |
|---|---|
| G-01 | Researcher có thể khởi tạo và theo dõi một run end-to-end trong platform. |
| G-02 | Case, dataset version, artifact, gate, finding, decision và chi phí đều có lineage/audit. |
| G-03 | Data-card path hỗ trợ profile/hypothesis mà không nhận raw rows; nhánh `explore` experimental có boundary riêng và đang tắt mặc định. |
| G-04 | Mỗi stage có review/validator và revision bounded; không publish provenance hỏng. |
| G-05 | Researcher hoặc PI xử lý accept/send-back, pause/resume/stop và budget theo authority; PI giữ quyền close. |
| G-06 | Cấu hình model, integration, engine settings và budget không cần sửa code/deploy. |
| G-07 | Chuẩn bị nền tảng khoa học cho FE-16 mà không ghi roadmap thành capability hiện tại. |
| G-08 | Researcher chọn journal từ đề xuất, duyệt corpus và sử dụng profile có version, uncertainty và evidence. |
| G-09 | Kiểm tra lập luận trước khi viết, giữ sentence-to-claim/evidence provenance và human approval trước export. |

# 3. Non-Goals

- Chạy model/experiment, sandbox execution, training, result calculation, scientific verdict hoặc publication dossier trong current release.
- Tự động tuyên bố causal effect, novelty đã chứng minh hoặc paper-ready conclusion.
- Upload raw rows vào LLM để tự khám phá khi chưa có consent/sandbox/policy.
- Organization/multi-tenant, custom roles, engine UI riêng hoặc hard delete lịch sử artifact.
- Ảnh, free text như nguồn phân tích chính, deep learning, federated learning, reinforcement learning và special structures không có adapter.

Giới hạn free text ở trên áp dụng cho input phân tích dataset của nhánh tabular; không loại trừ việc đọc paper hợp lệ trong JFE hoặc xử lý manuscript trong Writing. JFE/Writing không tự động nộp bài, không bảo đảm acceptance và không tạo research results thay cho execution.

# 4. Users & Roles

| Role | Phạm vi | Màn hình/chức năng chính |
|---|---|---|
| Platform Admin (`platform_admin`) | Toàn hệ thống | Users, projects, providers, settings, usage, logs, system. |
| Project Manager (`project_manager`) | Project được quản lý | Workspace, members, datasets, runs, budget, settings, archive/complete/abandon. |
| Researcher (`researcher`) | Project membership | Dataset/case, gates, hypotheses, plan; journal, corpus/profile, claims và bản thảo. |
| Reviewer (`reviewer`) | Project membership | Read artifact/finding, journal profile, argument graph, manuscript và comment. |
| AI PI (`oversight`) | Service decision boundary | Charter, stage outcome, failure, close, obligation, escalation. Không phải project member role. |

## 4.1 Permission rules

| Hành động | Admin | PM | Researcher | Reviewer |
|---|:-:|:-:|:-:|:-:|
| Đọc project/member/dataset/run/artifact/comment | ✓ | ✓ | ✓ | ✓ |
| Create/edit/archive/restore/complete/reopen project | ✓ | ✓ | – | – |
| Manage members/invitations | ✓ | ✓ | – | – |
| Upload/import/rename dataset; manage project files | ✓ | ✓ | ✓ | – |
| Create/test/browse/import connection | ✓ | ✓ | ✓ | – |
| Create/sync run, answer gate, accept/send-back | ✓ | ✓ | ✓ | – |
| Pause/resume/stop run | ✓ | ✓ | ✓ | – |
| Abandon run | ✓ | ✓ | – | – |
| Comment | ✓ | ✓ | ✓ | ✓ |
| Chọn journal; quản lý corpus và công việc JFE | ✓ | ✓ | ✓ | – |
| Duyệt journal profile, claims và bản thảo; export | ✓ | ✓ | ✓ | – |
| Project audit | ✓ | ✓ | – | – |
| System audit/admin | ✓ | – | – | – |

Non-member responses use `404`; insufficient role uses `403`/`ROLE_REQUIRED` according to Platform API behavior.

# 5. Product Principles

| ID | Nguyên tắc |
|---|---|
| PP-01 | `ResearchCase` là nguồn chính của intent/scope; không dùng lại `topic`/`objective` legacy làm contract chính. |
| PP-02 | Code/profiler/calculator tạo số; LLM chỉ diễn giải hoặc đề xuất, không được giả dạng sourced fact. |
| PP-03 | Data-card path không đưa raw rows vào model; artifact chỉ chứa aggregates, schema và provenance cần thiết. Nhánh `explore` experimental đang tắt mặc định. |
| PP-04 | Artifact immutable; amendment/revision/rerun tạo lineage mới. |
| PP-05 | Review pass, gate approval, stage acceptance và run close là các trạng thái khác nhau. |
| PP-06 | Current `random_rows` exploration/confirmation split không được gọi là structure-aware evaluation policy. |
| PP-07 | Mọi capability roadmap phải có trạng thái rõ (`planned`, `not implemented`) cho tới khi source và validator có thật. |

# 6. Current vs Next Release

| Capability | Current release | FE-16/HGAR next increment |
|---|---|---|
| Dataset | Versioned table intake/profile/data card/brief | Manifest có unit/group/time/structure và decision log mở rộng |
| Split | `random_rows`, seed, exploration/confirmation fraction | Group-disjoint, chronological/rolling-origin, panel entity+time, special adapter |
| Hypothesis | Literature/evidence/gap/hypothesis có review | Giữ nguyên, bổ sung structure-aware constraints |
| Plan | Experiment plan; data card → statistical analysis plan; review + lock | Protocol freeze trước execution |
| Execution | Chưa có execution engine/sandbox | Isolated sandbox, network off mặc định, checkpoint/resume/retry |
| Evidence | Plan/findings/gaps; chưa có result evidence | Effects, CIs, margins, verdict và dossier |
| Human control | Case/charter/gates/accept/send-back/amendment | Approval cho structure, protocol, holdout, spending và publication |

## 6.1 Backend capability vs frontend exposure

The Platform/engine source supports the dataset-first contract described above, but the current FE adapter is still feature-gated and hypothesis-oriented: the data stage is disabled in the run-studio feature configuration, and the start-run form does not yet submit `dataset_version_id` or expose `explore_dataset`. Therefore dataset-first is a current backend capability/contract and a planned end-user FE flow, not a claim that the current UI already exposes the full tabular journey.

# 7. Primary User Flows

## 7.1 Current platform flow — dataset-first backend contract

1. User tạo project và dataset version.
2. User mở Research flow và chọn `dataset_version_id`; `intent.kind=explore_dataset` là tùy chọn khi muốn dataset stage đề xuất problem, còn `test`/`compare`/`explain` có thể dùng problem đã biết.
3. Platform settle case; vì case có dataset, `dataset_first` bắt đầu `dataset` stage.
4. Dataset engine ingest/profile/describe; gate `data_card_review` cho researcher ở mode `light`.
5. Engine propose câu hỏi; gate `question_choice`; brief ghi objective/question/variables.
6. Nếu brief tạo problem `dataset_proposed`, Platform yêu cầu case/charter phù hợp trước stage kế tiếp khi PI flow cần nó.
7. Hypothesis engine tạo literature/evidence/gap/hypothesis; researcher/PI review và accept/send-back.
8. Experiment-design engine nhận hypothesis + data card/brief, tạo statistical analysis plan; resources/plan review và independent critique chạy theo engine contract.
9. Plan được lock/publish cùng finding/gap. Run close ghi obligation nếu có.

## 7.2 Current flow — case không có dataset

1. User cung cấp `intent`, `problem`, context, constraints, references và ít nhất một domain.
2. Platform chạy `default`: `hypothesis → experiment_design`.
3. Nếu PI bật, charter/clarification được xử lý theo `light`/`auto`; nếu PI không cấu hình hoặc charter bị skip, run vẫn tiếp tục theo case settled.
4. Kết quả cuối là evidence-linked hypotheses và reviewed/locked plan, không phải experiment result.

## 7.3 Case change flow

- Case đã settled chỉ được đổi qua `POST /projects/{project_id}/runs/{run_id}/case/amendments`.
- Amendment phải có fields + researcher reason; Platform tăng `case.version` và phát `case.amended`.
- Stage đã bắt đầu tiếp tục dùng case version cũ; stage kế tiếp nhận version mới.
- Researcher clarification là phần durable của case; PI không được ghi đè researcher intent.

## 7.4 Future flow — FE-16/HGAR

```text
dataset manifest → researcher confirms structure/target/unit/group/time
→ select matching split policy → freeze protocol/approval
→ sandbox preflight → execute tracked runs
→ scientific review → supported / not supported / inconclusive
→ researcher-approved dossier
```

Các bước này chưa được expose như current product flow.

## 7.5 Frontend exposure status

- Current FE exposes the existing project/research workspace and hypothesis-oriented run presentation.
- Dataset-first, `explore_dataset`, data-card gates and experiment-design scenes need FE integration before they can be presented as the default end-user journey.
- Run studio labels must distinguish backend plan/review capability from future execution/result capability.

## 7.6 JFE flow

1. Researcher xem journal đề xuất từ research context và metadata kho T3; chấp nhận hoặc chọn journal khác.
2. Researcher xác định phạm vi corpus, xem target/control papers, tiêu chí lựa chọn và quyền sử dụng, rồi phê duyệt corpus.
3. Hệ thống phân tích cấu trúc paper, gán rhetorical labels và đo features có liên kết tới nguồn.
4. Researcher/reviewer review annotation và kết quả phân tích; hệ thống tổng hợp đặc trưng journal cùng uncertainty và limitations.
5. Researcher phê duyệt và phát hành journal profile theo phiên bản để dùng cho Writing.

## 7.7 Writing AIF flow

1. Researcher chọn research outputs; hệ thống xác nhận nguồn, quyền sử dụng, evidence và giới hạn claim.
2. Hệ thống tổ chức evidence ledger, scientific statements và liên kết hypothesis/analysis/results.
3. Claims được tranh biện, phân rã Toulmin, biểu diễn bằng AIF và đánh giá bằng ASPIC+.
4. Researcher review và phê duyệt claims/argument graph.
5. Researcher chọn journal profile; hệ thống kết hợp publisher rules để tạo writing contract, outline và section/paragraph contracts.
6. Hệ thống tạo draft có sentence provenance, kiểm tra ngược với argument graph và hỗ trợ peer review/revision.
7. Researcher phê duyệt bản thảo cuối, disclosure và xuất PDF/DOCX/LaTeX.

# 8. ResearchCase Product Contract

| Field | Current rule |
|---|---|
| `version`, `status` | Bắt đầu version 1; `draft` hoặc `settled`; engine chỉ nhận case settled. |
| `intent` | `kind`: `test`, `compare`, `explain`, `explore_dataset`; text 12–2000 ký tự. |
| `problem` | 12–2000 ký tự; optional chỉ khi intent là `explore_dataset` và case còn draft. |
| `context` | Tối đa 4000 ký tự. |
| `constraints` | Tối đa 20 item; mỗi item tối đa 500 ký tự. |
| `references` | Tối đa 30 citation/note. |
| `domains` | Tối đa 10; run không có dataset phải có ít nhất một domain. |
| `dataset_version_id` | Optional cho test/compare/explain; bắt buộc cho `explore_dataset`. |
| `clarifications` | Câu hỏi PI và câu trả lời researcher; tối đa 10. |
| `amendments` | Version, changed fields, reason, timestamp; oldest-first. |
| `charter` | PI objectives, scope in/out, success/kill criteria, risk posture, assumptions, open questions, profile. |

`RunCreate` cũng nhận `review_mode` (`light`/`auto`), optional `interaction_mode`, `token_budget`, `problem`, `intent`, `context`, `constraints`, `references`, `dataset_version_id` và `domains`. Các legacy params không còn là nguồn chính.

# 9. Product Requirements

## 9.1 Authentication, project and collaboration

| ID | Requirement | Acceptance |
|---|---|---|
| PR-01 | Passwordless email login, optional Google sign-in, onboarding và account lifecycle. | User tạo được session; admin có thể lock/unlock theo API. |
| PR-02 | Project có PM, members, archive/restore/complete/reopen; archived read-only. | Role guard và state guard trả lỗi ổn định. |
| PR-03 | Invitation expiry theo access settings (default hiện tại 7 ngày, ceiling 720 giờ). | Invitation hết hạn không accept được; audit có actor/time. |
| PR-04 | Comments, notification, SSE và webhook cho run/project events. | Member xem đúng event theo project scope. |
| PR-05 | Audit log cho member, dataset, case, amendment, gate, run, budget và admin changes. | Record có actor, action, resource, timestamp và request context. |

## 9.2 Dataset intake

| ID | Requirement | Acceptance |
|---|---|---|
| PR-06 | Upload/import file table tạo immutable dataset version với original filename, size, SHA-256, row count và columns. | Upload version mới không overwrite version cũ. |
| PR-07 | Supported file format: CSV, TSV, XLSX, SAV, ZSAV, DTA, Parquet; zip có codebook/member. | Format hợp lệ được normalize nội bộ; format/size lỗi có error rõ. |
| PR-08 | Default max upload là 52,428,800 bytes (50 MiB). | Request vượt limit bị reject trước ingest. |
| PR-09 | Connection import hỗ trợ nguồn/table/view/SELECT và connector được đăng ký; secret không trả về. | Credential sealed; private/loopback host bị chặn. |
| PR-10 | Dataset version có preview/download/list versions theo project/member policy. | Dataset version id ổn định; delete không phá lineage đang dùng. |

## 9.3 Dataset stage

| ID | Requirement | Acceptance |
|---|---|---|
| PR-11 | Engine steps là `ingest`, `profile`, `describe`, optional `explore`, `propose`, `brief`. | Output step/resume manifest đúng contract. |
| PR-12 | Publish `dataset.data_card/v1`, markdown, `dataset.brief/v1`, markdown và optional explore report. | Artifact schema validate; primary artifact là brief. |
| PR-13 | Data card có source format/hash, unit, rows/columns, variables, measure/kind/role, missingness, flags, access, caveats, gaps, decisions. | Mọi field sourced/derived/LLM có source semantics phù hợp. |
| PR-14 | Model của data-card path chỉ đọc data card/aggregates; không copy raw row vào published output. Nhánh `explore` experimental phải được bật riêng. | Review artifact không có raw row; access record phản ánh rows `none`/`exploration`; mặc định `explore=false`. |
| PR-15 | `data_card_review` sau `describe`, `question_choice` sau `propose`; gates mở tối đa theo mode. | Light mode có researcher gate; auto mode dùng Platform/PI rule. |
| PR-16 | Current split chỉ là `Split.method=random_rows` với seed, exploration fraction, n_exploration, n_confirmation. | Tài liệu/UI không gọi đây là group/time/panel-safe split. |
| PR-17 | `explore` mặc định false. | Không bật raw-row exploration nếu chưa có sandbox/policy. |

## 9.4 Hypothesis stage

| ID | Requirement | Acceptance |
|---|---|---|
| PR-18 | Run literature/evidence workflow: understand, search, screen, extract, synthesize, hypothesize, critique, verify, lock. | Bounded loops, stage events và outputs hợp lệ. |
| PR-19 | Paper/evidence/gap/hypothesis có resolvable provenance; evidence scope được ghi. | Reference lỗi không publish; không fake fallback khi provider/model thiếu. |
| PR-20 | Hypothesis phải falsifiable; novelty report gắn heuristic label. | Reviewer kiểm tra criterion/claim/source. |
| PR-21 | Researcher review shortlist và hypotheses; approve, drop, comment hoặc request changes. | Gate response cập nhật artifact lineage/event. |

## 9.5 Experiment-design stage

| ID | Requirement | Acceptance |
|---|---|---|
| PR-22 | Steps là `understand → ground → design → critique → verify → lock`. | Step order/edges/max loops khớp engine spec. |
| PR-23 | Nếu có data card, workspace role là `analysis`; plan là statistical analysis plan cho dataset D1. | Plan dùng exact variable names/measurement levels từ card. |
| PR-24 | Validators kiểm tra variables, measurement fit, missing plan, confounding, multiplicity, split discipline, small cells và resampling seed. | Finding có category/severity/anchor; không tự tạo số bằng LLM. |
| PR-25 | Gates `resources_review` (khi cần) và `plan_review`; comment plan quay lại critique theo bound. | Reviewer/Researcher thấy open finding và revision diff. |
| PR-26 | Lock giữ byte/hash/approval/review state; publish không đồng nghĩa với execution/approval of result. | Rerun/revision không overwrite plan lineage. |

## 9.6 Orchestration, PI and budget

| ID | Requirement | Acceptance |
|---|---|---|
| PR-27 | Pipeline config hỗ trợ `default` và `dataset_first`; một active run/project. | Case có dataset route đúng dataset-first; case không có dataset route đúng default. |
| PR-28 | Run supports events, SSE, gates, pause/resume/stop, budget, sync, rerun/healing và abandon theo authority. | State transitions có audit/event và stable errors. |
| PR-29 | PI consults charter, stage outcome, failure và close; Critic stage review là config riêng. | PI action guard không accept blocking item thiếu known-risk reason. |
| PR-30 | Clarification/amendment durable; PI không thay intent researcher. | `case.amended` event + version visible trong run history. |
| PR-31 | Default run token budget 4,000,000; maximum 20,000,000; Platform có project budget/cost ledger. | Budget exhaustion giữ best artifact và ghi gap/reason. |
| PR-32 | BYOK/integration keys chỉ truyền trong request/memory. | Secret không xuất hiện trong artifact/log/event/API response. |

## 9.7 FE-16/HGAR requirements — planned

| ID | Requirement | Status |
|---|---|---|
| PR-33 | Classify independent/grouped/temporal/panel/special; researcher confirms target/unit/group/time/availability. | Planned; chưa có source implementation. |
| PR-34 | Registry maps structure to split policy; special requires adapter or out-of-scope result. | Planned; current contract chỉ có `random_rows`. |
| PR-35 | Freeze protocol: baselines, factors, split, metrics, seeds, statistics, budget, approval. | Planned; current lock chỉ lock plan artifact. |
| PR-36 | Sandbox preflight enforces no test-set access, train-only preprocessing/resampling, network policy, checkpoint/resume/retry. | Planned; chưa có execution engine. |
| PR-37 | Execute tracked runs and produce effect/CIs/margins/verdict/dossier. | Planned; current product không có result/verdict/dossier. |

## 9.8 JFE requirements

| ID | Requirement | Acceptance |
|---|---|---|
| PR-38 | Hệ thống đề xuất journal phù hợp với research context; người dùng có thể chấp nhận, tìm kiếm hoặc chọn journal khác. | Người dùng xem được lý do đề xuất và xác nhận journal mục tiêu. |
| PR-39 | Người dùng quản lý và phê duyệt corpus gồm target/control papers theo phạm vi nghiên cứu và quyền sử dụng. | Corpus thể hiện tiêu chí lựa chọn, papers được chọn/loại, nguồn, phạm vi và quyết định phê duyệt. |
| PR-40 | Hệ thống phân tích cấu trúc paper và duy trì liên kết về tài liệu nguồn. | Section, paragraph và sentence truy được về đúng document version và source span. |
| PR-41 | Hệ thống gán nhãn rhetorical features, đo đặc trưng và hỗ trợ reviewer xác nhận hoặc hiệu chỉnh annotation. | Feature có định nghĩa, đơn vị đo, giá trị, evidence và lịch sử review. |
| PR-42 | Hệ thống tổng hợp journal profile, thể hiện đặc trưng phổ biến và khác biệt so với control corpus. | Profile có số lượng mẫu, phân bố, độ bất định, dữ liệu thiếu và giới hạn phân tích. |
| PR-43 | Người dùng có thẩm quyền phê duyệt và phát hành journal profile theo phiên bản. | Profile có version, nguồn dữ liệu và approval record; phiên bản đã phát hành được bảo toàn. |
| PR-44 | Người dùng theo dõi tiến độ, lịch sử, tiếp tục hoặc hủy công việc JFE theo quyền trong project. | Trạng thái, tiến độ và hành động của người dùng được lưu và hiển thị nhất quán. |

## 9.9 Writing AIF requirements

| ID | Requirement | Acceptance |
|---|---|---|
| PR-45 | Hệ thống tiếp nhận research outputs, xác nhận quyền sử dụng và tổ chức evidence ledger cùng giới hạn claim. | Research outputs có nguồn, ownership, evidence links và phạm vi kết luận được phép. |
| PR-46 | Hệ thống quản lý scientific statements, tranh biện, rulings và phân rã Toulmin. | Mỗi statement có loại, trạng thái, căn cứ và liên kết lập luận; assumptions được phân biệt với findings. |
| PR-47 | Hệ thống biểu diễn lập luận bằng AIF và đánh giá bằng ASPIC+, kết hợp kiểm tra evidence và số liệu. | Graph thể hiện I/RA/CA/PA nodes, evidence mapping và kết quả đánh giá claim IN/OUT/undecided. |
| PR-48 | Người dùng phê duyệt và đóng băng claims/graph trước khi sử dụng để viết bài. | Bản thảo chỉ khẳng định claim được chấp nhận; claim undecided có qualifier phù hợp; thay đổi claim có approval record. |
| PR-49 | Hệ thống kết hợp journal profile với publisher rules để xác định yêu cầu cấu trúc và văn phong cho bản thảo. | Writing contract tham chiếu profile/rules version và giữ nguyên giới hạn claim đã duyệt. |
| PR-50 | Hệ thống tạo outline, section/paragraph contracts và draft có sentence provenance. | Người dùng truy được claim và evidence của từng câu có nội dung khoa học. |
| PR-51 | Hệ thống kiểm tra ngược bản thảo với AIF graph và hỗ trợ peer review về method, evidence và writing. | Báo cáo review chỉ rõ claim mới, scope widening, thiếu caveat, citation drift và mức độ phù hợp với journal. |
| PR-52 | Người dùng review revision, phê duyệt bản thảo cuối, disclosure và xuất tài liệu. | Bản xuất có đúng draft/graph/profile version, approval record và nội dung được phép sử dụng. |

# 10. API Surface (current)

> Tên route dưới đây là contract-level orientation; source `services/management` là authority khi path, error hoặc response thay đổi.

## 10.1 Dataset routes

| Method | Path | Mục đích |
|---|---|---|
| GET | `/projects/{project_id}/datasets` | List datasets. |
| POST | `/projects/{project_id}/datasets` | Upload/create dataset. |
| POST | `/projects/{project_id}/datasets/from-connection` | Import từ connection. |
| GET/PATCH/DELETE | `/projects/{project_id}/datasets/{dataset_id}` | Read/update/delete dataset metadata theo policy. |
| GET | `/projects/{project_id}/datasets/{dataset_id}/versions` | List immutable versions. |
| POST | `/projects/{project_id}/datasets/{dataset_id}/versions` | Upload version mới. |
| POST | `/projects/{project_id}/datasets/{dataset_id}/versions/from-connection` | Import version mới từ connection. |
| GET | `/projects/{project_id}/datasets/{dataset_id}/versions/{version_id}/download` | Download version. |
| GET | `/projects/{project_id}/datasets/{dataset_id}/versions/{version_id}/preview` | Preview rows theo masking/access policy. |

## 10.2 Research run routes

| Method | Path | Mục đích |
|---|---|---|
| GET | `/projects/{project_id}/runs` | List run. |
| POST | `/projects/{project_id}/runs` | Create/start run từ ResearchCase. |
| GET | `/projects/{project_id}/runs/{run_id}` | Run aggregate/state. |
| GET | `/projects/{project_id}/runs/{run_id}/events` | Paginated event history. |
| GET | `/projects/{project_id}/runs/{run_id}/events/stream` | SSE stream. |
| POST | `/projects/{project_id}/runs/{run_id}/gates/{gate_id}` | Submit gate answer. |
| POST | `/projects/{project_id}/runs/{run_id}/case/amendments` | Researcher amendment cho settled case. |
| POST | `/projects/{project_id}/runs/{run_id}/pause` | Pause. |
| POST | `/projects/{project_id}/runs/{run_id}/resume` | Resume với budget/credentials hợp lệ. |
| POST | `/projects/{project_id}/runs/{run_id}/stop` | Stop/cancel. |
| POST | `/projects/{project_id}/runs/{run_id}/budget` | Increase budget theo permission. |
| POST | `/projects/{project_id}/runs/{run_id}/sync` | Reconcile engine state/events. |
| POST | `/projects/{project_id}/runs/{run_id}/abandon` | PM/admin abandon run bị kẹt. |

Typical stable error boundaries include missing engine/config, problem required, dataset required, role/access, budget, credentials và contract mismatch. Error response không echo secret/submitted sensitive values.

# 11. Data and Artifact Contracts

| Area | Contract |
|---|---|
| Wire | `logos_contract` version `4.0.0`; schema ids and models are defined in `packages/contract`. |
| Dataset input | `platform.dataset/v1`; version id/source metadata passed to dataset stage. |
| Dataset output | `dataset.data_card/v1`, `dataset.data_card_markdown/v1`, `dataset.brief/v1`, `dataset.brief_markdown/v1`, optional `dataset.explore_report/v1`. |
| Hypothesis input/output | Hypothesis schemas and evidence resources from `logos-hypothesis`; exact IDs follow source contract. |
| Experiment design | `experiment_design.exp_plan/v1`; resources/index/review findings/revision artifacts as declared by engine. |
| JFE corpus | Journal identity, target/control papers, tiêu chí lựa chọn, quyền sử dụng và nguồn tài liệu. |
| JFE profile | Feature definitions/measurements, evidence, distributions, uncertainty, limitations, version và approval. |
| Writing evidence | Research output manifest, evidence ledger, scientific statements và claim ceiling. |
| Writing argument | Debate/rulings, Toulmin, AIF graph, evidence map, ASPIC+ labels và claim approval. |
| Writing manuscript | Journal writing contract, outline, section/paragraph contracts, draft, sentence provenance, review findings và revision history. |
| Writing export | Manuscript version, journal profile version, approved claims, disclosure và final approval record. |
| Run params | `inputs.params.case` contains settled ResearchCase; no parallel legacy topic/objective source. |
| Review categories | Includes leakage, baseline, control, statistics, reproducibility, evidence, metric validity, selective reporting, variable validity, measurement level, missing data, confounding, multiplicity, split discipline, effect size, small cells và other. |

# 12. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | **Security:** HttpOnly session, CSRF/CORS/rate limit, member isolation, sealed secrets, service keys, no secret in logs/artifacts. |
| NFR-02 | **Privacy:** Data-card path sends only allowed aggregates/data card to model; the opt-in experimental `explore` path has a separate exploration-row boundary; PII flags and access records are retained. |
| NFR-03 | **Scientific validity current:** Profiler/calculators are deterministic; plan validators enforce measurement/missing/split-discipline/small-cell/seed rules available in current card. |
| NFR-04 | **Scientific validity next:** Structure-aware split, train-only preprocess/resampling, holdout-once and sandbox preflight must be implemented before claiming execution validity. |
| NFR-05 | **Reproducibility:** Dataset SHA, case version, artifact hash, event/order, engine version, settings, seed and budget are retained where available. |
| NFR-06 | **Reliability:** Resume/checkpoint/idempotent event/artifact delivery; provider failures pause clearly and do not silently fabricate output. |
| NFR-07 | **Performance:** Long-running LLM/engine work is backgrounded; UI receives progress through event stream; budgets bound work. |
| NFR-08 | **Usability:** UI distinguishes AI proposed, code computed, reviewer found, researcher approved and PI decided. |
| NFR-09 | **Extensibility:** New stage must declare engine spec, settings, schemas, gates, events and verification; no cross-stage imports. |
| NFR-10 | **Source rights:** JFE/Writing kiểm tra quyền lưu, model processing, excerpt và export. Nếu nguồn bị thu hồi quyền, giữ metadata/audit theo policy nhưng ngừng cung cấp nội dung không còn được phép. |
| NFR-11 | **Claim fidelity:** Mỗi claim và số liệu trong bản thảo phải truy được về evidence đã được phê duyệt; bản thảo phải giữ nguyên scope, qualifiers và limitations của claim. |
| NFR-12 | **Review usability:** Người dùng xem được evidence, annotation cần review, claim status, revision diff và các quyết định phê duyệt. |

# 13. Release Status

| Capability | Status | Evidence/source |
|---|---|---|
| Auth/project/member/connection/dataset versioning | Current | `services/management` routes/models and FE workspace. |
| Contract and case model | Current | `packages/contract`, `ResearchCase`, contract 4.0.0. |
| `default` and `dataset_first` orchestration | Current | `management/research/orchestrator.py`, `deploy/.env.example`; routing phụ thuộc dataset presence. |
| Dataset data card/brief and gates | Current | `stages/dataset/engine.py`, dataset artifact contracts. |
| Literature hypothesis workflow | Current | `stages/hypothesis/engine.py` and contract schemas. |
| Analysis plan and independent review | Current | `stages/experiment-design/engine.py`, analysis pack/validators. |
| Structure detection + split policy registry (FE-16) | Planned | Current `Split.method` only `random_rows`. |
| Protocol freeze as execution gate | Planned | Current plan lock is artifact lock, not execution freeze. |
| Sandbox execution / model training | Not implemented | No execution engine in current pipeline. |
| Result statistics / verdict / dossier | Not implemented | Current run ends at plan/review/close. |

# 14. Acceptance Checklist

## 14.1 Current release

- [ ] User can create project, upload/import dataset version and see source/hash/version.
- [ ] User can create a settled ResearchCase with valid intent/problem/dataset/domain constraints.
- [ ] Dataset-first/default pipeline is selected correctly and one active run/project is enforced.
- [ ] Data card/brief artifacts validate; raw rows do not appear in published data-card artifacts, còn `explore` chỉ chạy khi được bật riêng.
- [ ] Hypothesis evidence refs and falsification criteria are present or surfaced as findings/gaps.
- [ ] Data-card plan uses variable names/measurement levels and current validators catch split/missing/small-cell/seed issues.
- [ ] Case amendment increments version and emits durable event.
- [ ] Budget, pause/resume, retry and missing credentials produce auditable state.

## 14.2 FE-16/HGAR gate before implementation claim

- [ ] Structure classifier benchmarked against expert labels.
- [ ] Split policy is selected from structure, researcher-confirmed and persisted with manifest/hash.
- [ ] Preprocessing/resampling and holdout access are enforced in code, not only prompt text.
- [ ] Sandbox has network/data permissions, checkpoint/resume/retry and immutable execution lineage.
- [ ] Effect/CI/margin/verdict output is code-generated and reviewed; dossier requires human approval.

# 15. References and Source of Truth

- **Methodology/design:** `docs/example/Booklet_HGAR_Tabular_Data_Science_Expanded_v2.pdf` and the current register/report in `docs/1.2/`.
- **Business intent:** project registration and report define the tabular/HGAR direction, five structure types and FE-16 as next increment.
- **Implementation truth:** `/Users/ngothanhdat/Documents/CODE/3. capstone/capstone-projects/projects/logos`, especially `packages/contract`, `services/management`, `stages/*`, `deploy/.env.example`; frontend contract surface is under `ai-research-platform-fe`.
- **Documentation links:** [BRD](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md) and [architecture](architecture.md) must keep current/planned labels aligned with this PRD.

- [JFE Complete PRD v2](../ai-research-platform-fe/docs/JFE_Deliverables_v2/JFE_v2/JFE_Complete_PRD_v2.md).
- [Yêu cầu dữ liệu kho T3](../ai-research-platform-fe/docs/jfe-t3-api-requirements.md).
- **Writing flow:** `ai-research-platform-fe/src/app/(main)/projects/[projectId]/_components/run-studio/writing/data/core.ts`.
- **JFE flow:** `ai-research-platform-fe/src/app/(main)/projects/[projectId]/_components/run-studio/writing/data/jfe.ts`.

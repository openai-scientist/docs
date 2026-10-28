# Business Requirements Document (BRD)
## AI Research Experimentation Platform

**Document Type:** Business Requirements Document\
**Project:** AI Research Experimentation Platform (`logos` + `ai-research-platform-fe`)\
**Version:** 2.2 Draft (2026-10-28)\
**Status:** Draft\
**Liên quan:** [PRD](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md) · [Architecture](architecture.md) · [changelog](changelog.md)

> **Ranh giới năng lực:** BRD này phân biệt rõ capability đang có trong source với increment tiếp theo. Bản hiện tại đã có intake/profile dữ liệu dạng bảng, data card/brief, hypothesis có evidence và experiment-design plan có review. FE-16 (nhận diện cấu trúc dữ liệu và enforcement split policy), sandbox execution, kết quả thống kê, verdict và dossier chưa được coi là capability đã triển khai.

---

# 1. Executive Summary

AI Research Experimentation Platform giúp researcher đi từ một **research case** hoặc một **dataset version** tới data card/research brief, hypothesis có bằng chứng và experiment plan được review. AI thực hiện phần công việc có thể kiểm tra bằng code; researcher hoặc AI Principal Investigator (PI) giữ quyền đối với mục tiêu, phạm vi, gate và quyết định accept/send-back.

Luồng hiện tại:

```text
ResearchCase
(intent + problem/context/constraints/references/domains; có thể gắn dataset)
        │
        ├─ có dataset_version_id ───────────────► dataset_first
        │                                         dataset → hypothesis → experiment_design
        │
        └─ không có dataset ────────────────────► default
                                                  hypothesis → experiment_design

dataset: ingest → profile → describe → [explore tắt mặc định] → propose → brief
        │              │                         │
        │              └─ data_card_review       └─ question_choice
        ▼
hypothesis: literature/evidence → gaps → falsifiable hypotheses → review
        ▼
experiment_design: resources → statistical analysis plan → independent critique → lock
        ▼
researcher / PI: gate, accept/send-back, pause/resume/stop; PI-controlled close
```

Định hướng tabular/HGAR của đề tài mở rộng luồng sau khi plan được lock:

```text
[FE-16 kế tiếp] cấu trúc dữ liệu → split policy phù hợp → protocol freeze
                → sandbox execution → evidence/statistical verdict → dossier
```

Đoạn sau là roadmap, không phải mô tả trạng thái source hiện tại.

Nhánh hỗ trợ công bố nghiên cứu bổ sung **JFE (Journal Fingerprint Extraction)** và **Writing AIF**: JFE xây profile đặc trưng của tạp chí từ corpus có quyền sử dụng; Writing tổ chức evidence thành lập luận kiểm tra được bằng AIF (Argument Interchange Format), rồi viết bản thảo trong giới hạn claim đã duyệt. Profile JFE được xây và phát hành độc lập, có thể tái sử dụng; Writing tham chiếu đúng phiên bản tại bước journal merge. Các findings và kết luận trong bản thảo phải được hỗ trợ bởi evidence đã được phê duyệt.

> Luồng dataset-first ở trên là capability của Platform/engine source. FE adapter hiện vẫn ưu tiên luồng hypothesis và chưa expose đầy đủ `dataset_version_id`, `explore_dataset` và dataset-stage UI; đây là phần FE integration cần hoàn thiện.

Ba giá trị kinh doanh:

1. **Traceability:** claim, evidence, data card, decision và artifact có provenance; con số phải đến từ code.
2. **Review độc lập:** mỗi stage có reviewer/validator riêng, revision có giới hạn và finding được lưu cùng artifact.
3. **Human control:** mode `light` để researcher xử lý gate; mode `auto` để PI quyết trong phạm vi charter và escalate khi có vấn đề integrity.

# 2. Business Context

Nghiên cứu trên dữ liệu bảng cần đồng thời hiểu dataset, đặt câu hỏi có thể trả lời, kiểm soát leakage và lập kế hoạch phân tích. Lỗi split là rủi ro đặc biệt quan trọng: các hàng có cùng entity, cùng panel hoặc có quan hệ thời gian không thể luôn được đối xử như IID rows. Bên cạnh đó, preprocess/resampling ngoài vòng validation hoặc dùng lại holdout có thể làm kết quả lạc quan giả.

LLM có thể hỗ trợ tìm literature, mô tả biến và soạn kế hoạch nhanh hơn, nhưng có rủi ro bịa nguồn/số, nhầm proxy với khái niệm, bỏ qua missingness/confounding hoặc trình bày giả định như kết luận. Nền tảng phải tách phần AI đề xuất, code kiểm tra và phần researcher phê duyệt.

# 3. Business Problems

| ID | Vấn đề |
|---|---|
| BP-01 | Tổng quan literature, sàng lọc evidence và tìm research gap tốn nhiều thời gian. |
| BP-02 | Hypothesis thường mơ hồ, không có biến, phép đo hoặc tiêu chí bác bỏ rõ. |
| BP-03 | Experiment/analysis plan có thể thiếu baseline, control, thống kê, missing-data plan hoặc kiểm soát leakage. |
| BP-04 | LLM có thể bịa citation, số liệu hoặc mức độ chắc chắn; khó audit nếu artifact không có provenance. |
| BP-05 | Dataset thực tế khó hiểu nhanh: kiểu biến, mã missing, cardinality, free text, PII và unit of observation. |
| BP-06 | Random row split không phù hợp với grouped, temporal, panel/longitudinal hoặc cấu trúc đặc biệt sẽ làm rò rỉ thông tin. |
| BP-07 | Preprocess/resampling và việc xem lại holdout có thể làm sai tính xác nhận của phân tích. |
| BP-08 | Một AI tự lập kế hoạch rồi tự chấp thuận dễ tự xác nhận chính nó; cần reviewer và human gate. |
| BP-09 | Token, model key và chi phí theo run/project cần được kiểm soát. |
| BP-10 | Nhóm nghiên cứu cần cộng tác, comment, notification và audit quanh cùng một run. |
| BP-11 | Chọn tạp chí và học cấu trúc bài viết thường dựa vào cảm tính; khó phân biệt thông lệ quan sát được với quy định bắt buộc của publisher. |
| BP-12 | Bản thảo có thể khuếch đại claim, bỏ caveat, lệch citation hoặc thêm kết luận không được evidence hỗ trợ. |

# 4. Business Objectives

| ID | Mục tiêu | Liên kết |
|---|---|---|
| BO-01 | Rút ngắn đường từ research case/dataset tới hypothesis có evidence và plan có thể review. | BP-01..BP-03 |
| BO-02 | Truy được claim, citation, biến, số liệu và quyết định về record hoặc phép tính của code. | BP-04, BP-05 |
| BO-03 | Profile dataset theo data-card path mà không đưa raw rows cho model; bảo vệ source, hash và version, đồng thời kiểm soát rõ nhánh `explore`. | BP-05 |
| BO-04 | Làm cho unit of observation, leakage risk và split policy trở thành phần bắt buộc của hướng tabular kế tiếp. | BP-06, BP-07 |
| BO-05 | Duy trì review độc lập, human gate, PI escalation và audit trail. | BP-08 |
| BO-06 | Kiểm soát token budget, model key và ngân sách project. | BP-09 |
| BO-07 | Hỗ trợ collaboration an toàn trong phạm vi project. | BP-10 |
| BO-08 | Đánh giá hệ thống bằng benchmark, seeded flaws và so sánh human-only/AutoML/generic agent/HGAR ở increment nghiên cứu. | BP-06, BP-08 |
| BO-09 | Hỗ trợ researcher chọn tạp chí và dùng profile có bằng chứng, control corpus, uncertainty và phiên bản rõ ràng. | BP-11 |
| BO-10 | Giữ lineage từ research record → evidence → claim/lập luận → câu trong bản thảo; researcher duyệt claim và bản xuất cuối. | BP-04, BP-12 |

# 5. Success Metrics

## 5.1 Đo được với capability hiện tại

| Metric | Cách đo |
|---|---|
| Run progress/completion | Tỉ lệ Platform run kết thúc với trạng thái và gap rõ; phân biệt `queued`, `running`, `paused`, `awaiting_review`, `completed`, `budget_exceeded`, `failed`, `stopped` và action abandon. |
| Stage completion | Tỉ lệ stage đạt `PENDING`, `RUNNING`, `COMPLETED`, `ACCEPTED`, `FAILED`, `STOPPED` hoặc `SUPERSEDED`, tách khỏi run-level status. |
| Traceability | Không publish artifact có evidence ref, schema id hoặc số liệu không resolve/không do code tạo. |
| Review quality | Finding blocking được phát hiện trong seeded-flaw bench; theo dõi revision và known risk. |
| Data safety | Data card có source hash/access record; data-card path không nhận raw row, còn `explore` là nhánh experimental đang tắt mặc định và có boundary riêng. |
| Budget compliance | Không stage nào vượt token budget; đo `budget_exceeded`, usage và cost ledger theo run/project. |
| Reliability | Tỉ lệ resume/healing thành công sau pause/provider failure; lỗi cần người có mã và hướng xử lý rõ. |

## 5.2 Metrics cho increment FE-16/HGAR

| Metric | Cách đo |
|---|---|
| RQ1 — structure detection | Độ chính xác phân loại independent/grouped/temporal/panel/special so với nhãn chuyên gia. |
| RQ2 — protocol validity | Tỉ lệ lỗi split, leakage, train-only preprocessing/resampling và holdout reuse được seeded test phát hiện trước khi chạy. |
| RQ3 — cycle quality | Tỉ lệ hoàn tất full cycle, verdict có evidence, thời gian và chi phí so với human-only, AutoML-only và generic agent. |
| Reproducibility | Dataset hash, case/protocol version, code/environment, seed, params và outputs đủ để tái lập run. |
| Human control | Mọi thay đổi protocol, holdout, spending và claim/publication đều có researcher approval/audit record. |

## 5.3 Metrics mục tiêu cho JFE và Writing AIF

| Metric | Cách đo |
|---|---|
| JFE provenance coverage | Feature/profile resolve được về corpus snapshot, document/span và extractor/registry version; công bố N, missing/N/A và uncertainty. |
| JFE review quality | Theo dõi parse failures, annotation disagreement, holdout validation và reviewer decisions. |
| Writing claim fidelity | Tỉ lệ câu có claim truy được về frozen graph/evidence; không xuất bản khi còn unsupported claim hoặc factual conflict blocking. |
| Writing efficiency & control | Đo thời gian, chi phí, revision và quyết định duyệt so với quy trình thủ công trên cùng record. |

# 6. Stakeholders

| Stakeholder | Role hệ thống | Mối quan tâm |
|---|---|---|
| System Administrator | `platform_admin` | Model/key, engine settings, budget mặc định, user, audit và vận hành. |
| Project Manager | `project_manager` | Project, member, dataset, run, budget và close/abandon. |
| Researcher / Data Analyst | `researcher` | Research case, dataset, gate, hypothesis, plan; chọn journal, duyệt corpus/profile, claims và bản thảo. |
| Reviewer / Stakeholder | `reviewer` | Đọc artifact, finding, journal profile, lập luận và bản thảo; comment trong phạm vi project. |
| Data/Methodology Reviewer | reviewer nghiệp vụ ở increment tương lai | Xác nhận unit, structure, split policy và protocol freeze. Chưa phải service/role riêng trong source hiện tại. |
| AI Principal Investigator | service `oversight` | Charter, stage outcome, failure, close, obligation và escalation. |

# 7. As-Is

Researcher tự tìm paper, ghi chú, kiểm tra dataset và viết plan trong các file rời. Quy tắc split/leakage có thể chỉ nằm trong kinh nghiệm cá nhân; reviewer khó biết model đã thấy gì; chi phí, quyết định và phiên bản dữ liệu không được nối thành một audit trail.

# 8. To-Be

- Một project workspace chứa dataset versions, files, members, runs, artifacts, comments, notifications và audit.
- Một run bắt đầu bằng `ResearchCase` có intent, problem hoặc dataset exploration, context, constraints, references và domains.
- Dataset stage tạo data card/research brief từ aggregates; data-card path không đưa raw rows vào model/artifact. Nhánh `explore` experimental tắt mặc định và phải có boundary riêng.
- Hypothesis stage tạo evidence-linked, falsifiable hypotheses; experiment-design stage tạo plan được critique và lock.
- Researcher/PI quyết định ở gate; mọi clarification/amendment/accept/send-back đều có version và event.
- FE-16 bổ sung structure-aware split policy và protocol controls; execution/verdict/dossier chỉ được mở sau khi có sandbox, provenance và validation tương ứng.
- JFE cung cấp journal profile có version và review; Writing AIF giữ claim/evidence, kiểm tra lập luận và kiểm tra ngược bản thảo trước human sign-off.

# 9. Scope

## 9.1 Trong phạm vi — đã có trong source hiện tại

| Nhóm | Nội dung |
|---|---|
| Tài khoản & quyền | Passwordless auth, onboarding, platform admin, project role `project_manager`/`researcher`/`reviewer`, member invitation và access control. |
| Project | Create/edit/archive/restore/complete/reopen; project là scope cao nhất, không organization layer. |
| Dataset | Versioned upload/import; CSV, TSV, XLSX, SAV, ZSAV, DTA, Parquet và zip/codebook theo dataset service; giới hạn mặc định 50 MiB. |
| Connections | Import table/view/SELECT từ connector được hỗ trợ; credential không trả về, host private bị chặn. |
| Research case | Intent `test`, `compare`, `explain`, `explore_dataset`; problem/context/constraints/references/domains; dataset version; charter, clarification và amendment. |
| Run orchestration | Pipeline `default` hoặc `dataset_first`; một active run/project; light/auto; gate, stage review, accept/send-back, pause/resume/stop/rerun/sync/abandon. |
| Dataset engine | `ingest → profile → describe → explore → propose → brief`; data card, brief, optional explore report; gates `data_card_review` và `question_choice`. |
| Hypothesis engine | Literature/evidence pipeline, gap, hypothesis, provenance, review và revision. |
| Experiment design | Resource grounding, plan, independent critique, validators/calculators, final check và locked plan. Với data card, plan là statistical analysis plan. |
| AI PI & governance | Charter, stage outcome, failure, close, directive, obligation, escalation; Critic có cờ cấu hình riêng. |
| Collaboration & admin | Comments, notifications/SSE, webhooks, audit, model/integration/engine settings, usage và cost ledger. |
| Evaluation | `logos_eval` bench và seeded-flaw evaluation theo source hiện tại. |

## 9.2 Increment tabular/HGAR — yêu cầu kế tiếp, chưa coi là đã triển khai

| Nhóm | Nội dung mục tiêu |
|---|---|
| Structure classification | Phân biệt independent, grouped, temporal, panel/longitudinal và special. Researcher xác nhận hoặc sửa. |
| Split policy registry | Chọn policy theo structure: repeated stratified k-fold cho independent; group-disjoint cho grouped; chronological/rolling-origin cho temporal; entity-disjoint + past-to-future cho panel; adapter riêng cho special. |
| Dataset manifest | Ghi hash, schema, license, target, unit, group/time, risks, access và quyết định structure. |
| Protocol freeze | Freeze baselines, factors, split, metrics, seeds, statistical plan, compute budget và approvals trước execution. |
| Sandbox execution | Chạy code cô lập, network off mặc định, preflight leakage, train-only preprocessing/resampling, checkpoint/resume/retry và immutable run. |
| Evidence & dossier | Lưu effect/CIs/practical margins, verdict supported/not supported/inconclusive và dossier được researcher duyệt. |

## 9.3 JFE và Writing AIF

| Nhóm | Nội dung |
|---|---|
| JFE | Đề xuất và lựa chọn journal; quản lý target/control corpus; phân tích cấu trúc, gán nhãn, đo đặc trưng; tổng hợp và phê duyệt journal profile. |
| Writing AIF / ASW | Quản lý evidence và scientific statements; tranh biện và đánh giá lập luận bằng Toulmin/AIF/ASPIC+; xây outline, soạn thảo, kiểm tra, review, phê duyệt và xuất bản thảo. |

# 10. Ngoài phạm vi

- Trong baseline hiện tại: model training, experiment execution, statistical result generation, verdict và publication dossier.
- Không tự động xử lý special structures nếu chưa có adapter/split policy riêng.
- Ảnh, free text như nguồn phân tích dataset chính của nhánh tabular, deep learning, federated learning và reinforcement learning. Giới hạn này không loại trừ paper text trong JFE hoặc manuscript trong Writing.
- Organization/multi-tenant, custom role/permission matrix và UI riêng của engine.
- Đưa raw rows vào LLM để “tự khám phá” khi chưa có sandbox/consent; `explore` hiện tắt mặc định.
- Tuyên bố causal effect hoặc kết luận publication chỉ từ plan/hypothesis.
- Tự động nộp bài cho publisher, bảo đảm journal acceptance, sao chép bài nguồn hoặc coi journal fit là xác nhận tính đúng khoa học.

# 11. Business Requirements

## 11.1 Truy cập và cộng tác

| ID | Yêu cầu |
|---|---|
| BR-01 | Người dùng đăng nhập bằng passwordless email; Google sign-in chỉ có khi được cấu hình. |
| BR-02 | Quyền dựa trên `platform_admin` và project role `project_manager`, `researcher`, `reviewer`; non-member nhận `404`, thiếu role nhận lỗi `403`. |
| BR-03 | Project có ít nhất một Project Manager active; project archived là read-only. |
| BR-04 | Member vào project qua invitation; expiry do access setting kiểm soát, mặc định hiện tại là 7 ngày và không vượt 720 giờ. |
| BR-05 | Thay đổi quan trọng có audit; comment, notification/SSE và webhook dùng để cộng tác. |

## 11.2 Research case và run

| ID | Yêu cầu |
|---|---|
| BR-06 | Tạo run phải nhận một `ResearchCase`, không dùng `topic`/`objective` legacy làm source chính. |
| BR-07 | `intent.kind` thuộc `test`, `compare`, `explain`, `explore_dataset`; intent text dài 12–2000 ký tự. |
| BR-08 | `problem` dài 12–2000 ký tự, bắt buộc khi case settled trừ `explore_dataset`; explore phải có dataset version. |
| BR-09 | Case lưu `context` (tối đa 4000), tối đa 20 constraints, 30 references và tối đa 10 domains; nếu không có dataset phải có ít nhất một domain. |
| BR-10 | Case được settled trước khi engine chạy; PI charter/clarification không được ghi đè phần researcher. |
| BR-11 | Sau khi settled, thay đổi chỉ qua researcher amendment có reason, version và event; stage đã bắt đầu vẫn giữ case version cũ. |
| BR-12 | Có `dataset_version_id` thì chạy `dataset_first`; không có dataset thì chạy `default`. `explore_dataset` là intent đặc biệt cho phép dataset stage đề xuất problem; pipeline hiện tại kết thúc ở reviewed/locked plan. |

## 11.3 Dataset và data card

| ID | Yêu cầu |
|---|---|
| BR-13 | Upload/import tạo dataset version bất biến; không ghi đè version cũ và lưu SHA-256/source metadata. |
| BR-14 | Dataset service nhận CSV, TSV, XLSX, SAV, ZSAV, DTA, Parquet và zip/codebook; giới hạn upload mặc định 50 MiB. |
| BR-15 | Data connection chỉ import nguồn/statement được phép; credential được seal, không trả về/log, private host bị chặn. |
| BR-16 | Dataset engine tạo data card gồm unit, rows/columns, variable type/measure/role/kind, missingness, cardinality, flags, access, caveats và decisions. |
| BR-17 | Mọi số trong data card do code tính; data-card path chỉ đưa aggregates/data card cho model, không copy raw row vào published artifact; `explore` là nhánh experimental đang tắt mặc định và category dưới `min_cell` không lộ count. |
| BR-18 | Data card hiện ghi split `random_rows` gồm exploration/confirmation rows với seed/fraction; đây là exploratory/confirmation split, chưa phải structure-aware evaluation split. |
| BR-19 | Researcher có thể review data card và chọn research question ở gate; mode auto dùng rule/PI theo cấu hình. |

## 11.4 Tabular scientific validity — FE-16 kế tiếp

| ID | Yêu cầu mục tiêu |
|---|---|
| BR-20 | Hệ thống nhận diện independent/grouped/temporal/panel/special và hiển thị lý do/độ tin cậy cho researcher. |
| BR-21 | Researcher xác nhận target, unit of observation, entity/group key, time/order, availability và leakage risk. |
| BR-22 | Hệ thống chọn hoặc yêu cầu researcher chọn split policy khớp structure; không cho plan ghi policy mâu thuẫn với manifest. |
| BR-23 | Preprocess và resampling phải nằm trong training fold; confirmation/holdout chỉ dùng theo protocol và một lần. |
| BR-24 | Protocol freeze ghi baselines, factors, split, metrics, seed, statistical plan, budget và human approval trước execution. |
| BR-25 | Special structure chỉ được chạy khi có adapter/policy được đăng ký; nếu không thì block hoặc đưa ra ngoài scope, không tự fallback random rows. |
| BR-26 | Mọi structure/split decision, amendment và exception phải có provenance/audit và đi cùng dataset hash. |

## 11.5 Hypothesis

| ID | Yêu cầu |
|---|---|
| BR-27 | Hypothesis engine tìm/sàng lọc literature và tạo evidence-linked research gap từ case hoặc dataset brief. |
| BR-28 | Mỗi paper/evidence card/gap/hypothesis có provenance; evidence không resolve thì không publish. |
| BR-29 | Hypothesis phải nêu variables/claim và falsification criterion cụ thể; novelty là heuristic, không phải chứng minh. |
| BR-30 | Researcher có thể review shortlist/hypothesis, drop/keep/comment hoặc yêu cầu revise; thiếu provider/model phải báo lỗi rõ, không fake output. |

## 11.6 Experiment design hiện tại

| ID | Yêu cầu |
|---|---|
| BR-31 | Từ hypothesis và data card/brief, engine tạo plan; khi có data card, plan phải là statistical analysis plan cho dataset đó. |
| BR-32 | Plan ghi measurement fit, missing-data handling, confounding, multiplicity, effect size/CI, split discipline và seed khi có resampling. |
| BR-33 | Validators phải kiểm tra variables tồn tại, measurement level, missing plan, current split discipline, small cells và resampling seed. |
| BR-34 | Critique/review độc lập, revision có giới hạn; plan lock theo hash khi hoàn tất bước lock. |
| BR-35 | Plan chưa được review đầy đủ vẫn phải mang gap/finding; “published/locked” không có nghĩa là experiment đã chạy hoặc claim đã được chứng minh. |

## 11.7 Điều phối, PI và chi phí

| ID | Yêu cầu |
|---|---|
| BR-36 | Mỗi project chỉ có một active run; stage phải đi theo pipeline, có gate/accept/send-back/rerun và bounded iteration. |
| BR-37 | Mode `light` để researcher xử lý gate; `auto` để PI quyết trong authority; integrity/charter conflict/cannot decide phải escalate. |
| BR-38 | Agent question không block run; default/assumption phải được ghi, không được coi là researcher intent. |
| BR-39 | Pause/resume/stop/abandon, provider retry và budget exhaustion phải giữ artifact tốt nhất cùng gap/reason. |
| BR-40 | PI tạo charter, stage outcome, failure, close và obligation; PI không trả lời engine gate và không tự biến plan thành kết quả. |
| BR-41 | Run có token budget mặc định 4.000.000, tối đa 20.000.000; project có usage/cost ledger và budget cảnh báo. |
| BR-42 | Model key/integration secret chỉ nằm trong memory/request, được seal ở Platform và không được engine đọc từ `.env`/file. |

## 11.8 Execution/evidence — sau FE-16

| ID | Yêu cầu mục tiêu |
|---|---|
| BR-43 | Chỉ execution service có sandbox, preflight và policy kiểm soát mới được chạy code/ML; engine plan hiện tại không cung cấp capability này. |
| BR-44 | Mọi execution phải lưu immutable run, code/env/seed/params, logs, artifacts và checkpoint/resume/retry. |
| BR-45 | Scientific reviewer tính paired effects, confidence intervals, practical margins và verdict supported/not supported/inconclusive từ outputs do code tạo. |
| BR-46 | Dossier chỉ được tạo sau evidence review và human approval; không tự suy ra publication claim từ LLM narrative. |

## 11.9 Journal Fingerprint Extraction (JFE)

| ID | Yêu cầu |
|---|---|
| BR-47 | Researcher nhận đề xuất journal theo research context và có thể chấp nhận, tìm kiếm hoặc chọn journal khác. |
| BR-48 | Researcher quản lý và phê duyệt corpus gồm bài từ journal mục tiêu và nhóm đối chứng theo tiêu chí lựa chọn rõ ràng. |
| BR-49 | Paper và kết quả phân tích từ kho T3 phải có nguồn gốc, phạm vi nội dung và quyền sử dụng rõ ràng. |
| BR-50 | Đặc trưng cấu trúc, rhetorical moves và văn phong của paper có định nghĩa, phép đo, evidence và review. |
| BR-51 | Journal profile thể hiện đặc trưng phổ biến, khác biệt so với nhóm đối chứng, độ bất định và giới hạn phân tích. |
| BR-52 | Journal profile được researcher phê duyệt, phát hành theo phiên bản và tái sử dụng cho nhiều bản thảo. |
| BR-53 | Researcher theo dõi tiến độ, lịch sử và quản lý công việc JFE trong phạm vi project. |

## 11.10 Writing AIF

| ID | Yêu cầu |
|---|---|
| BR-54 | Research outputs dùng để viết bài phải có nguồn, quyền sử dụng, evidence và phạm vi kết luận rõ ràng. |
| BR-55 | Claim trong bản thảo phải truy được về hypothesis, analysis, kết quả và evidence tương ứng. |
| BR-56 | Scientific statements được phân loại rõ; claim được tranh biện và review về phương pháp, thống kê, phạm vi và literature. |
| BR-57 | Lập luận được biểu diễn bằng Toulmin/AIF và đánh giá bằng ASPIC+ trước khi researcher phê duyệt claims. |
| BR-58 | Bản thảo chỉ khẳng định claims được chấp nhận; claim chưa xác định phải giữ qualifier phù hợp. |
| BR-59 | Cấu trúc và văn phong bản thảo phù hợp journal profile/publisher rules, không làm thay đổi nội dung hoặc mức độ chắc chắn của claim. |
| BR-60 | Bản thảo được kiểm tra tính nhất quán với lập luận đã duyệt, gồm evidence, citation, scope và limitations. |
| BR-61 | Researcher review revision, phê duyệt bản thảo cuối, disclosure và xuất tài liệu; việc nộp bài do researcher quyết định. |

# 12. Business Rules

| ID | Quy tắc |
|---|---|
| RULE-01 | `ResearchCase` là nguồn chính của intent/scope; settled case chỉ đổi qua researcher amendment. |
| RULE-02 | Data version bất biến; dataset hash và artifact provenance phải được giữ qua pipeline. |
| RULE-03 | `random_rows` hiện tại không được mô tả là group/time/panel split hoặc leakage-safe evaluation policy. |
| RULE-04 | Số liệu do code/calculator/profiler tạo; model không được viết số như sourced fact. |
| RULE-05 | Prompt và validator phải đồng bộ; lỗi nội dung chưa đủ để làm mất artifact nếu provenance/contract vẫn hợp lệ, nhưng phải thành finding/gap. |
| RULE-06 | Review pass khi không còn finding `blocking`; approve gate và accept stage là hai hành động riêng. |
| RULE-07 | Artifact immutable; sửa bằng revision/version/amendment, không overwrite lịch sử. |
| RULE-08 | Data-card path không đưa raw rows cho model; `explore` là nhánh experimental tắt mặc định vì ranh giới sandbox hiện chưa đáp ứng yêu cầu. |
| RULE-09 | Không được ghi nhận execution result/verdict/dossier là current capability cho tới khi sandbox, validator và evidence store tồn tại trong source. |
| RULE-10 | Platform quản lý data/access/run/audit; engine làm khoa học của stage; PI quyết định pipeline, không sở hữu run state. |
| RULE-11 | JFE profile publication và manuscript approval là hai gate riêng; profile completion không đồng nghĩa approval cho claim hay paper. |
| RULE-12 | Writing chỉ dùng evidence hợp lệ trong phạm vi đã duyệt. Graph validity/ASPIC+ IN không tự chứng minh một kết luận thực nghiệm là đúng. |
| RULE-13 | Profile version, frozen graph, draft revision và sentence provenance phải đi cùng nhau; sửa upstream làm downstream cần review lại, không âm thầm ghi đè. |

# 13. Assumptions & Constraints

- LLM gateway tương thích OpenAI, model role `stage` và `review` được cấu hình; thiếu credential phải báo lỗi/pause rõ.
- Literature provider công khai trả citation/evidence đủ provenance; abstract evidence không phải full-text validation.
- Platform hiện hỗ trợ CPU-friendly tabular workflow; các cấu trúc đặc biệt cần adapter riêng.
- PostgreSQL/storage/deployment là hạ tầng của source `logos`; chi tiết wire/config chuẩn nằm trong [architecture](architecture.md).
- Tên file BRD/PRD hiện giữ legacy để các link cũ tiếp tục hoạt động.

# 14. Risks & Mitigations

| Risk | Giảm thiểu |
|---|---|
| LLM bịa nguồn/số | Evidence ref, schema validation, calculator/profiler và reviewer độc lập. |
| Random split gây leakage | FE-16 structure detection + split registry; hiện phải ghi rõ limitation của `random_rows`. |
| Model thấy raw data | Data card aggregate-only, access record, explore off; execution sandbox phải có policy riêng. |
| Researcher đổi mục tiêu giữa chừng | Settled case, versioned amendment, stage lineage và audit. |
| Reviewer cùng bias với author | Model role `review`, Critic và seeded-flaw evaluation; vẫn phải theo dõi independence thực tế. |
| Auto mode quyết sai | Authority guard, escalation, obligation, light mode và audit. |
| Chi phí/provider outage | Per-run token budget, monthly budget, retry/pause/resume và usage ledger. |
| Roadmap bị hiểu là đã có | Mỗi requirement/roadmap section ghi trạng thái current/FE-16; PRD và architecture phải đồng bộ nhãn này. |

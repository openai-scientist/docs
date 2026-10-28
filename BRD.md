# Business Requirements Document (BRD)
## OpenAI-Scientist

**Document Type:** Business Requirements Document\
**Project:** OpenAI-Scientist (capstone FA26SE115)\
**Version:** 3.0 Draft (2026-10-29)\
**Status:** Draft — nguồn nội bộ\
**Liên quan:** [glossary](glossary.md) · [README](README.md) · [PRD](PRD.md) · [Architecture](architecture.md) · [Traceability](traceability.md) [ID mapping](id-mapping.md) · [changelog](changelog.md)

Thuật ngữ theo [glossary.md](glossary.md).

> **Vai trò tài liệu.** BRD là nguồn nội bộ. BRD định nghĩa hệ thống; code đi theo BRD. BRD không ghi trạng thái triển khai.

---

# 1. Executive Summary

OpenAI-Scientist giúp researcher đi từ một câu hỏi nghiên cứu và dữ liệu dạng bảng tới một gói bằng chứng sẵn sàng cho bài báo. Máy làm phần việc kiểm tra được bằng code. Researcher giữ các quyết định mà chỉ researcher được sở hữu.

**Chuẩn chất lượng:** hệ thống không hứa khoa học luôn đúng. Hệ thống hứa ba điều: **không có lỗi nào bị giấu, mọi claim có nguồn, mọi run có thể chạy lại**.

Pipeline luôn là `dataset_first`, gồm năm stage. Mỗi ranh giới stage có đúng một hand-off object, có kiểu, có version, có hash và bất biến sau khi accepted.

```text
research case (dataset là tuỳ chọn khi bắt đầu)
      │
      ▼
dataset ──DatasetSnapshot──► hypothesis ──HypothesisSet──► experiment_design
                                                               │
                                                      AnalysisPlan + Lock
                                                               ▼
              paper ◄──────────EvidenceBundle────────────── execution
                │
            PaperPack ──► Dossier (tham chiếu EvidenceBundle + PaperPack đã accepted)
                              │
                       duyệt (Approval) ──► export ra ngoài project
```

Ba giá trị kinh doanh:

1. **Truy vết:** claim, evidence, số liệu và quyết định có nguồn; con số đến từ code.
2. **Review độc lập bắt buộc:** mọi object version được review một lần, sau khi mọi check xanh.
3. **Human control theo loại action:** preset theo stage, action pinned luôn hỏi user, AI PI chỉ quyết tạm.

# 2. Business Context

Nghiên cứu trên dữ liệu bảng cần hiểu dataset, đặt câu hỏi trả lời được, tìm bằng chứng tài liệu, lập kế hoạch phân tích, chạy phân tích và viết bài. Mỗi bước có rủi ro riêng. Một agent AI có thể bịa nguồn hoặc số, nhầm proxy với khái niệm, thử nhiều phân tích rồi chỉ báo cáo kết quả đẹp, hoặc trình bày giả định như kết luận.

Dữ liệu nhạy cảm thường nằm trên máy của chủ dữ liệu và không được rời đi. Run dài thường chờ user trả lời và dễ bị treo. Chi phí model khó đoán.

Nền tảng tách ba phần: AI đề xuất và viết lời; code tính số, check và verdict; researcher giữ quyết định pinned. Platform quản lý dữ liệu, quyền, run, audit và Dossier. Platform không đánh giá khoa học.

# 3. Business Problems

| ID | Vấn đề |
|---|---|
| BP-01 | Tổng quan literature, sàng lọc evidence và tìm research gap tốn nhiều công sức. |
| BP-02 | Hypothesis thường mơ hồ: thiếu biến, phép đo, ngưỡng hiệu ứng hoặc tiêu chí bác bỏ. |
| BP-03 | Kế hoạch phân tích có thể thiếu baseline, kiểm soát confounding, xử lý missing data hoặc kiểm soát leakage. |
| BP-04 | LLM có thể bịa citation, số liệu hoặc mức chắc chắn; khó audit khi artifact không có provenance. |
| BP-05 | Dataset thực tế khó hiểu: kiểu biến, mã missing, cardinality, free text, PII, unit of observation và chất lượng. |
| BP-06 | Chia dữ liệu không đúng làm rò rỉ thông tin và làm kết quả lạc quan giả. |
| BP-07 | Nhìn kết quả xác nhận trước khi phân tích chốt, hoặc thử nhiều thủ tục rồi chọn kết quả đẹp (p-hacking), làm mất giá trị xác nhận. |
| BP-08 | Một AI tự lập kế hoạch rồi tự chấp thuận dễ tự xác nhận chính nó; cần reviewer độc lập và quyết định của người. |
| BP-09 | Token, model key và chi phí theo run và theo project cần được kiểm soát. |
| BP-10 | Nhóm nghiên cứu cần cộng tác, bình luận, thông báo và audit quanh cùng một run. |
| BP-11 | Chọn tạp chí và học cấu trúc bài viết thường dựa vào cảm tính; khó tách thông lệ quan sát được khỏi quy định bắt buộc. |
| BP-12 | Bản thảo có thể khuếch đại claim, bỏ caveat, lệch citation hoặc chứa con số không do code tạo. |
| BP-13 | Hàng dữ liệu riêng có thể rời khỏi máy giữ dữ liệu (tới model, log hoặc cloud). |
| BP-14 | Run có thể treo vô hạn khi chờ user, hết budget hoặc hết phần việc tự sửa. |
| BP-15 | Công tắc kiểm soát toàn run quá thô: user hoặc bị hỏi quá nhiều, hoặc mất quyền quyết định những việc chỉ user được quyết. |
| BP-16 | Kết quả có thể rời project mà chưa có người có thẩm quyền duyệt. |

# 4. Business Objectives

| ID | Mục tiêu | Liên kết |
|---|---|---|
| BO-01 | Rút ngắn đường từ research case tới hypothesis có evidence và kế hoạch phân tích có thể review. | BP-01..BP-03 |
| BO-02 | Truy được claim, citation, biến, số liệu và quyết định về record hoặc phép tính của code; mọi run replay được. | BP-04, BP-05 |
| BO-03 | Hàng dữ liệu không bao giờ rời nơi giữ dữ liệu; model và artifact chỉ thấy aggregate đã qua release gate. | BP-05, BP-13 |
| BO-04 | Làm cho kết quả xác nhận không thể p-hacking: split theo power, Lock, envelope, unseal, tried ledger và confirmation tier. | BP-06, BP-07 |
| BO-05 | Review độc lập bắt buộc cho mọi stage và quyền quyết định của người theo loại action (preset, pinned, presence). | BP-08, BP-15 |
| BO-06 | Kiểm soát token budget theo run và budget theo tháng của project. | BP-09 |
| BO-07 | Hỗ trợ cộng tác an toàn trong phạm vi project, với quyền theo role. | BP-10 |
| BO-08 | Mọi run kết thúc với kết quả rõ (kể cả `with_gaps`); không treo. | BP-14 |
| BO-09 | Đánh giá từng stage và cả pipeline bằng acceptance scenario, seeded-flaw bench và paper reproduction bench. | BP-06, BP-08 |
| BO-10 | Tạo PaperPack mà đội viết bài biến thành bản nộp mà không phải dẫn xuất lại; claim không vượt claim ceiling. | BP-04, BP-12 |
| BO-11 | Chỉ export ra ngoài project khi Dossier đã được duyệt. | BP-16 |
| BO-12 | (Could, sau MVP) Hỗ trợ chọn tạp chí bằng profile có bằng chứng, control corpus và version rõ (JFE). | BP-11 |

# 5. Success Metrics

| ID | Metric (định nghĩa) | Target | Cách đo | BO |
|---|---|---|---|---|
| SM-01 | Run ended: tỷ lệ run đạt trạng thái `ended` (`complete`, `with_gaps`, `failed_technical` hoặc `cancelled`) | 100%; không run nào ở `running` hoặc `waiting` mà không có item đang chờ | Audit run state theo project | BO-08 |
| SM-02 | Số question mỗi run, thời gian bị chặn, overturn rate theo action type | Báo cáo mỗi run. Ngưỡng tính trên các run ở preset `milestones` của một tháng: trung vị số question mỗi run không quá 15; trung vị thời gian bị chặn mỗi run không quá 24 giờ; overturn rate của mỗi action type không quá 10% (vượt ngưỡng thì xem lại level của action type đó) | Operating metrics từ decision log | BO-05 |
| SM-03 | Số trong object đã publish tham chiếu được tới record do code tạo | 100%; không còn chữ số nào không phải reference | Contract check của PaperPack và EvidenceBundle | BO-02, BO-10 |
| SM-04 | Citation nằm trong Literature Base với DOI đã resolve và trích dẫn hỗ trợ | 100% | Contract check citations | BO-02, BO-10 |
| SM-05 | Số hàng dữ liệu `local` có trong message gửi ra khỏi Local Node | 0 | Packet capture trong acceptance scenario của Local Node | BO-03 |
| SM-06 | Release log của Local Node khớp release mà Platform giữ | 100% khớp | So sánh log trong acceptance scenario | BO-03 |
| SM-07 | Run mà agent thấy ước lượng xác nhận trước unseal; run mà thời điểm unseal không sau lần sửa lane C cuối | 0 run | Audit envelope log và unseal log | BO-04 |
| SM-08 | EvidenceBundle có replication package mà replicator tái lập hash | 100% bundle accepted | Báo cáo replicator trong bundle | BO-02, BO-04 |
| SM-09 | Precision của từng persona reviewer trên seeded-flaw bench | Không dưới mức tối thiểu của persona; dưới mức thì severity bị hạ | Seeded-flaw bench | BO-05, BO-09 |
| SM-10 | Object version accepted đã qua review loop | 100% | Đối chiếu object version với review record | BO-05 |
| SM-11 | Run vượt token budget mà không kết thúc `with_gaps`; run đang chạy chạm 100% project budget mà không có item `spending` | 0 run | Usage ledger và decision inbox | BO-06 |
| SM-12 | Effect statement trong Abstract, Results, Discussion ánh xạ tới verdict và interpretation row; từ chỉ mức claim khớp verdict | 100% | Contract check claims | BO-10 |
| SM-13 | Paper reproduction bench: hướng và độ chồng khoảng của ước lượng chính so với bài đã công bố; độ phủ checklist | Không kém tỷ lệ bài không có lỗi lớn mà hệ thống data-to-paper báo cáo trên mục tiêu tương đương | Bench, chỉ chạy theo yêu cầu | BO-09, BO-10 |
| SM-14 | Stage acceptance: mỗi stage qua một lần chạy live của scenario riêng, mọi hard check xanh | 5/5 stage, thêm Local Node | Acceptance scenario | BO-09 |
| SM-15 | Export ra ngoài project có Dossier đã duyệt | 100% | Audit log export | BO-11 |
| SM-16 | (Sau MVP) Feature của journal profile truy được về corpus snapshot và span | 100% | Contract check của JFE | BO-12 |
| SM-17 | Tỷ lệ phát hiện leakage cài sẵn: phần lỗi leakage của red-team catalogue (BR-100) mà hệ thống phát hiện | Ít nhất 90% | Seeded-flaw bench | BO-09 |
| SM-18 | Tỷ lệ chặn vi phạm protocol: phần vi phạm pipeline order cài sẵn (BR-86) bị chặn trước khi chạy | 100% | Seeded-flaw bench | BO-09 |

# 6. Stakeholders và Roles

Định nghĩa role theo glossary §1.

| Stakeholder | Role | Mối quan tâm |
|---|---|---|
| Quản trị hệ thống | Platform Admin | User, model, key, engine settings, budget mặc định, audit, health. |
| Quản lý project | Project Manager | Member, settings, budget, dataset, run; huỷ run; duyệt chi thêm; duyệt Dossier; mọi quyền nghiên cứu của Researcher (BR-80). |
| Người nghiên cứu | Researcher | Research case, run, decision inbox, acceptance, paper. |
| Người review | Reviewer | Đọc và bình luận mọi object; duyệt Dossier theo review settings. |
| Hệ thống | AI PI (connector persona; secondary actor trong use case) | Hành động thay mặt user trong giới hạn của nó: tóm tắt, đề xuất next step, quyết tạm item không pinned khi `autopilot` và `away`. Không quyết item pinned, không kết thúc run. |
| Hệ thống | Persona (maker, guard, connector) | Tạo object (maker); review object (guard); nối run với user (connector, ví dụ AI PI). |

# 7. Scope

## 7.1 Trong phạm vi

**Năng lực theo stage**

| Stage | Năng lực nghiệp vụ |
|---|---|
| dataset | Tìm dataset trong project hoặc hỏi user; nhập dữ liệu từ upload (gồm Parquet), connection hoặc Local Node; profile chất lượng; dictionary có thời điểm sẵn có của biến; cờ leakage (biến post-outcome, trùng lặp giữa các phần split); báo cáo dataset shift; prefilter gợi ý research pattern; cleaning recipe; question map; quyết định split theo power; kết luận fitness. Tạo DatasetSnapshot. |
| hypothesis | Rapid review có phương pháp trên Literature Base; evidence map; HypothesisSet gồm ít nhất hai hypothesis và một primary; mỗi hypothesis kiểm được (comparator, primary metric, hướng hoặc margin, phạm vi, decision rule). |
| experiment_design | Lập AnalysisPlan cho dữ liệu bảng có sẵn: estimand, protocol theo loại claim, adjustment set, analysis program, decision rule, bảng diễn giải, robustness set; task family; research pattern từ registry; pipeline order; evidence family. Tạo Lock. |
| execution | Chạy chương trình đã lock trong sandbox; guard chặn vi phạm pipeline order; confirmatory vào envelope; unseal; verdict, grade và claim ceiling do code tính; khám phá có kiểm soát (lane E); replicator. Tạo EvidenceBundle. |
| paper | Soạn PaperPack theo contract: bản thảo IMRaD, reporting checklist, claims, hình và bảng, citation, limitations, reproducibility, declarations, review, định dạng xuất. |

**Phạm vi nghiên cứu.** Sản phẩm giữ nghiên cứu hiện tượng với claim type `association`, `causal` và `prediction`. Sản phẩm thêm lớp kiểm soát cho dữ liệu bảng: task family, research pattern, pipeline order, chống leakage, hypothesis kiểm được và red-team catalogue (BR-82..BR-101).

**Năng lực nền tảng**

| Nhóm | Nội dung |
|---|---|
| Tài khoản, project, quyền | Đăng nhập, role, project, member, invitation, audit log. |
| Dữ liệu | Dataset và dataset version có hash; data connection; data location `platform` hoặc `local`. |
| Điều phối run | Một run active mỗi project; run state; hand-off object; stale; next step. |
| Human control | Preset theo stage; action group, level, floor; action pinned; presence; decision inbox; decision log; overturn; AI PI; lab notebook. |
| Review độc lập | Review loop bắt buộc; personas; finding; seeded-flaw bench. |
| Budget | Token budget mỗi run; project budget theo tháng; ledger. |
| Cộng tác | Comment, notification, usage và cost ledger. |

**Local Node.** Service phía user giữ dữ liệu `local` và chạy job cạnh dữ liệu. Có release gate, release log và disclosure mode. User không cần Docker.

**Dossier.** Gói tham chiếu EvidenceBundle và PaperPack đã accepted; duyệt theo review settings; điều kiện để export.

**Could, sau MVP:** JFE (Journal Fingerprint Extraction): profile tạp chí từ corpus được phép dùng, paper stage tham chiếu.

**Should, sau MVP:** `method_comparison`: claim type so sánh các phương pháp ML trên cùng dữ liệu (research pattern G tối ưu hyperparameter, H ensemble và stacking, I ablation, J budget-aware, kèm baseline policy F). MVP không đổi (BR-82).

## 7.2 Ngoài phạm vi

| Non-goal | Ghi chú |
|---|---|
| Dữ liệu không phải dạng bảng (ảnh, text corpus, tín hiệu) | Chỉ hỗ trợ dữ liệu bảng. |
| Thiết kế thu thập dữ liệu mới (thí nghiệm lab hoặc thực địa) | experiment_design chỉ lập kế hoạch phân tích dữ liệu bảng có sẵn. |
| Sản phẩm systematic review đầy đủ (đăng ký PROSPERO, GRADE đầy đủ, meta-analysis kết luận) | Hypothesis stage là rapid review có phương pháp. |
| Đọc full text sau paywall | Chỉ dùng metadata, abstract và full text open access. |
| Organization, multi-tenant, ma trận quyền tuỳ biến | Project là scope cao nhất. |
| Tự nộp bài cho publisher, bảo đảm tạp chí chấp nhận | Researcher quyết định nộp bài. |
| Tuyên bố causal chỉ từ plan hoặc hypothesis | Claim chỉ đến từ verdict và claim ceiling. |
| So sánh với human-only, AutoML hoặc generic agent | Ngoài phạm vi là đánh giá chính OpenAI-Scientist so với các hệ thống này. Đề tài nghiên cứu của user vẫn trong phạm vi: user so sánh một phương pháp AutoML với baseline trên dữ liệu của mình bằng `method_comparison` (FE-19, Should, sau MVP). |
| Task family ngoài `binary`, `multiclass`, `regression`, `rare-event`: ranking, survival, forecasting, anomaly | BR-83. |

# 8. Business Rules

Cột "BO" ghi business objective (§4) mà rule phục vụ.

## 8.1 Truy cập và cộng tác

| ID | Rule | BO |
|---|---|---|
| BR-01 | User đăng nhập không mật khẩu bằng email. | BO-07 |
| BR-02 | Quyền dựa trên role hệ thống Platform Admin và role project Project Manager, Researcher, Reviewer. Người không phải member không thấy project tồn tại; member thiếu role bị từ chối thao tác. | BO-07 |
| BR-03 | Mỗi project có ít nhất một Project Manager active. Project đã archive chỉ đọc. | BO-07 |
| BR-04 | User vào project qua invitation; invitation hết hạn theo access setting. | BO-07 |
| BR-05 | Thay đổi quan trọng ghi vào audit log chỉ-thêm. Comment và notification dùng để cộng tác trong project. | BO-07 |
| BR-06 | Reviewer đọc và bình luận mọi object của project. Platform Admin xem metadata của mọi project (danh sách, member, usage, trạng thái run) nhưng không mở dataset, object hay bản thảo nếu không là member. | BO-07 |
| BR-80 | Project Manager có mọi quyền nghiên cứu của Researcher trong project (tạo run, trả lời decision inbox, accept object, lock plan, export), ngoài quyền quản lý của Project Manager. | BO-07 |
| BR-103 | User đăng nhập bằng email không mật khẩu hoặc bằng tài khoản Google. Hai cách đăng nhập ánh xạ về cùng một user theo email đã xác minh. | BO-07 |

## 8.2 Research case và run

| ID | Rule | BO |
|---|---|---|
| BR-07 | Mọi run bắt đầu từ một research case gồm topic, mục tiêu, bối cảnh, ràng buộc, domain và tài liệu tham khảo. Dataset là tuỳ chọn. | BO-01 |
| BR-08 | Pipeline luôn là `dataset_first`: dataset → hypothesis → experiment_design → execution → paper. Khi chưa có dataset, dataset stage tìm trong project, tìm dataset public, hoặc hỏi user. Dataset public có vai trò `enrichment` hoặc `validation`; join dữ liệu public vào dữ liệu riêng vẫn là action pinned (BR-26). | BO-01 |
| BR-09 | Mỗi project có tối đa một run active. | BO-07 |
| BR-10 | Sau khi research case được chốt, thay đổi chỉ qua amendment của researcher có lý do, version và event. Stage đã bắt đầu giữ case version cũ. | BO-02 |
| BR-11 | Mỗi ranh giới stage có đúng một hand-off object có kiểu, version và hash. Object bất biến sau khi accepted; sửa tạo version mới. | BO-02 |
| BR-12 | Khi object upstream mà object downstream ghim có version mới, object downstream thành `stale`. Không có gì tự cập nhật; user chọn cập nhật qua acceptance. | BO-02 |
| BR-13 | Mỗi stage có contract item, mỗi item có check bằng code. Stage "done" khi mọi item xanh. Item đỏ là việc tự sửa của agent; khi item tiêu hết phần budget thì thành item `needs-you`. | BO-08 |
| BR-14 | Run luôn kết thúc, không treo: `ended` với `complete`, `with_gaps`, `failed_technical` hoặc `cancelled`. Khi chạm giới hạn, stage kết thúc trên output tốt nhất và liệt kê mọi contract item đỏ. `with_gaps` chỉ có ba nguyên nhân: token budget của run cạn (BR-58), item `spending` quá hạn (BR-78), item pinned quá hạn chờ (BR-104). | BO-08 |
| BR-77 | Project Manager, hoặc Researcher đã tạo run, có thể huỷ run. Run kết thúc `ended(cancelled)`. Huỷ được từ mọi trạng thái trừ `ended`. Object đã accepted được giữ; mọi item đang chờ được đóng; thao tác ghi audit log. | BO-08 |
| BR-15 | Sau run, AI PI đề xuất next step từ bộ cố định: `collect_more_data`, `explore_signal`, `replicate`, `write_paper`, `revise_plan`. User chọn. | BO-01 |

## 8.3 Dữ liệu và quyền riêng tư

| ID | Rule | BO |
|---|---|---|
| BR-16 | Dataset version bất biến, có hash. Upload hoặc import tạo version mới; không ghi đè. Mọi phân tích ghim một dataset version. | BO-02 |
| BR-17 | Data connection chỉ import từ nguồn được uỷ quyền. Credential không trả lại, không ghi log; host nội bộ bị chặn. | BO-03 |
| BR-18 | Mỗi dataset version có data location `platform` hoặc `local`. Chỉ Local Node đọc được dữ liệu `local`. | BO-03 |
| BR-19 | Hàng dữ liệu không bao giờ rời nơi giữ dữ liệu. Chỉ aggregate (release) rời đi, qua một release gate duy nhất: ngưỡng ô nhỏ, làm tròn, kiểm tra differencing, probe budget. | BO-03 |
| BR-20 | Mọi release của một dataset version ghi vào release log chỉ-thêm. | BO-03 |
| BR-21 | Disclosure mode `standard` cho release tự động trong policy. Mode `strict` chỉ cho các loại số đã duyệt; loại khác thành item release review trong decision inbox. Researcher của project, hoặc Project Manager theo BR-80, trả lời item release review. | BO-03 |
| BR-22 | Model và artifact đã publish không nhận hàng dữ liệu; model chỉ nhận aggregate và profile do code tính. Exception từ dữ liệu thật chỉ trả loại lỗi, cột, số hàng ảnh hưởng. | BO-03 |
| BR-23 | Model key và secret tích hợp được seal ở Platform; không xuất hiện trong prompt, log hoặc output. | BO-06 |
| BR-81 | Khi Local Node bị thu hồi, job cho dữ liệu `local` của Node đó bị từ chối và user được báo lý do. Object đã publish vẫn đọc được. | BO-03 |
| BR-102 | Upload nhận các định dạng dữ liệu bảng phổ biến, gồm Parquet. Danh sách đầy đủ là system rule của Report III. | BO-01 |

## 8.4 Human control

| ID | Rule | BO |
|---|---|---|
| BR-24 | Mỗi stage có một preset: `co_work`, `milestones` (mặc định) hoặc `autopilot`. Đổi preset áp dụng cho action tương lai; item đang chờ được đánh giá lại; quyết định đã qua không tính lại. | BO-05 |
| BR-25 | Mỗi action thuộc đúng một trong tám action group và có level `auto`, `do_then_review` hoặc `must_ask`. Override có thể hạ level xuống floor, không thấp hơn. | BO-05 |
| BR-26 | Action pinned luôn `must_ask` ở mọi preset: định nghĩa outcome và estimand; xác nhận unit of observation và cấu trúc dữ liệu trước khi split; chọn hypothesis (từ hai trở lên) và primary; join dữ liệu public vào dữ liệu riêng; lock plan; lệch khỏi thuật toán đã lock; dùng validation source; xuất ra ngoài project. | BO-05 |
| BR-27 | Presence (`present` hoặc `away`) chỉ đổi cách item `must_ask` chờ. `present`: hỏi ngay, kèm option, option đề xuất và lý do. `away`: item xếp hàng, agent tiếp tục mọi action không phụ thuộc item. | BO-05 |
| BR-28 | Có một decision inbox duy nhất cho mọi stage, gồm tám loại item: question, review batch, tentative decision, deviation, candidate, needs-you, release review, spending. Thông báo ngoài (mail, push) chỉ cho item pinned đang chặn và cho item `spending`; cả hai có lời nhắc trước hạn (BR-78, BR-104). Item `spending` gửi Project Manager; item pinned gửi người có quyền trả lời item. | BO-05 |
| BR-29 | Decision log ghi mỗi quyết định: action type, level, phiên bản policy, ai quyết (user, agent, AI PI), presence, đã bị overturn hay chưa. Hệ thống tính overturn rate theo action type và chỉ **đề xuất** nâng level; không tự nâng. | BO-05 |
| BR-30 | AI PI chỉ quyết tạm item không pinned, và chỉ khi preset là `autopilot` và user `away`. Mỗi quyết định tạm thành tentative decision để user xác nhận hoặc lật lại. | BO-05 |
| BR-31 | AI PI không bao giờ kết thúc run và không bao giờ quyết item pinned. Item pinned chờ tới hạn chờ của nó (BR-104); stage kết thúc ở trạng thái `ready_to_<action>`. | BO-05 |
| BR-32 | Action của user trên UI đi qua cùng tool, guard và check như action của agent. Decision log ghi ai hành động. | BO-05 |
| BR-33 | Ở `milestones`, level của acceptance fitness theo verdict của code: `fit` là `auto` (ghi log); `fit_with_limits` là `do_then_review`; `not_fit` là `must_ask`. | BO-05 |
| BR-34 | AI PI viết lab notebook cho run: tóm tắt, đề xuất, quyết định tạm và lý do. | BO-05 |
| BR-75 | Khi agent dùng một giả định (ví dụ trong lúc item chờ user), giả định được ghi vào decision log cùng các phương án thay thế và lý do. Giả định không được coi là ý định của researcher. | BO-05 |
| BR-104 | Mỗi item pinned có hạn chờ do project settings quy định. Hệ thống nhắc người có quyền trả lời trước hạn bằng thông báo ngoài (mail, push), như với item `spending`. Hết hạn mà chưa trả lời thì run kết thúc `ended(with_gaps)`: item pinned đóng ở trạng thái chưa trả lời và gap được liệt kê. Không ai quyết thay user: không AI PI, không giá trị mặc định. Trước hạn, item pinned đang chờ không kết thúc run. | BO-05, BO-08 |

## 8.5 Review độc lập

| ID | Rule | BO |
|---|---|---|
| BR-35 | Review loop bắt buộc ở mọi stage. Nó chạy một lần cho mỗi object version, sau khi mọi check xanh. | BO-05 |
| BR-36 | Reviewer có context mới và không thấy trace của tác giả. Các guard chạy song song và không đọc nhau. | BO-05 |
| BR-37 | Finding có category, severity (`blocking`, `major`, `minor`), anchor, evidence, failure scenario và cách sửa. Code loại finding thiếu anchor hoặc evidence. | BO-05 |
| BR-38 | Trước khi sửa, finding được kiểm bằng code hoặc verifier thứ hai (`confirmed`, `plausible`, `rejected`). Chỉ finding `blocking` đã `confirmed` vào vòng sửa; finding khác được ghi và hiển thị. | BO-05 |
| BR-39 | Có tối đa hai vòng sửa. Sau mỗi lần sửa, review lại chỉ trên finding đã sửa và field đã đổi; finding `blocking` mới trên field không đổi chỉ hợp lệ khi evidence của nó là một fact tính mới. Finding còn lại thành known risk được hiển thị, hoặc user quyết định giữa hai phía. | BO-05 |
| BR-40 | Precision của reviewer đo trên seeded-flaw bench; reviewer dưới mức tối thiểu bị hạ severity finding. Một persona chỉ được bật khi bench cho thấy nó bắt được điều persona khác bỏ sót. User gọi được mọi persona trên mọi object. | BO-05, BO-09 |

## 8.6 Toàn vẹn khoa học

| ID | Rule | BO |
|---|---|---|
| BR-41 | Số do code tính. Text của model mang tham chiếu tới record, không mang con số. Model không viết số như một sự kiện đã tính. | BO-02 |
| BR-42 | Code chỉ từ chối object khi provenance hoặc contract hỏng. Vấn đề nội dung khác được thử lại, rồi giữ như finding hoặc known risk. Evidence không resolve được thì không publish. | BO-02 |
| BR-43 | DatasetSnapshot gồm nguồn, table model, profile năm chiều chất lượng, dictionary, cleaning recipe, question map, split, vai trò nguồn và fitness (`fit`, `fit_with_limits`, `not_fit`). Cleaning dùng outcome thuộc plan, không thuộc dataset stage. | BO-01 |
| BR-76 | Dataset stage xác định unit of observation và cấu trúc dữ liệu (group, thời gian, panel). Researcher xác nhận chúng (action pinned, BR-26) trước khi split được tạo. Split tôn trọng cấu trúc đó: các hàng cùng group không nằm ở hai phần; dữ liệu có trật tự thời gian được chia theo thời gian. Số phần của split vẫn theo BR-44. | BO-04 |
| BR-44 | Dataset stage quyết định split từ power: `three_way` nếu n giữ power từ 0,8 và còn reserve; `two_way` nếu không; `none` khi n dưới mức tối thiểu và ghi như limitation. | BO-04 |
| BR-45 | HypothesisSet gồm ít nhất hai hypothesis có claim key khác nhau và một primary. Mỗi hypothesis có estimand nháp, biến, confounder có nguồn, SESOI, câu bác bỏ, loại đóng góp và nguồn gốc. | BO-01 |
| BR-46 | AnalysisPlan chỉ lập kế hoạch phân tích dữ liệu bảng có sẵn, gồm estimand, protocol theo loại claim, adjustment set, analysis program, fallback, decision rule, bảng diễn giải, robustness set, design diagnosis và cấu trúc họ giả thuyết. | BO-01 |
| BR-47 | Lock là object riêng do Platform ghi: hash của spec, program và golden outputs, snapshot version, split digest, ai khoá, khi nào. Object đã lock bất biến. | BO-02, BO-04 |
| BR-48 | Thay đổi thuật toán đã lock là deviation: action pinned, ghi vào deviation log, ảnh hưởng grade, và phải xuất hiện trong limitations của paper. | BO-04 |
| BR-49 | Kết quả confirmatory vào envelope ở Platform. Trước unseal, agent chỉ thấy "done" hoặc "error". Unseal tự động khi mọi check xanh (user có thể chọn mở bằng tay trước; floor cho phép nâng lên `must_ask`). Mọi hypothesis mở cùng lúc; thời điểm unseal được ghi và phải sau lần sửa lane C cuối. | BO-04 |
| BR-50 | Execution chạy trong sandbox. Agent làm việc tự do trên twin; chạm dữ liệu thật chỉ qua aggregate hoặc chương trình đầy đủ. Dry run trên dữ liệu thật không trả ước lượng. | BO-04 |
| BR-51 | Lane E (exploration) chỉ dùng exploration split. Lane E không chạm confirmatory split, không dùng validation source, không đưa candidate thẳng vào plan. Candidate không phải claim; candidate vào decision inbox để user chọn. | BO-04 |
| BR-52 | Tried ledger ghi mọi thủ tục tìm kiếm ở lane E và ngưỡng nhiễu của nó. Càng tìm nhiều, ngưỡng cho candidate sau càng cao. Khám phá của user vào cùng ledger. | BO-04 |
| BR-53 | Mỗi candidate được xác nhận ở một confirmation tier: `replicated`, `reserve`, `unsealed_untouched`, `unsealed_touched`. Chỉ `replicated` và `reserve` ghi e-value vào ledger. | BO-04 |
| BR-54 | Verdict của mỗi hypothesis do code tính theo decision rule đã lock: `supported`, `trivial`, `not_supported`, `insufficient`, `not_tested`. Model không tạo verdict. | BO-10 |
| BR-55 | Grade A–D do code tính từ diagnostics, robustness và deviation. | BO-10 |
| BR-56 | Claim ceiling do execution stage tính từ verdict, grade và confirmation tier. Paper stage không vượt claim ceiling. "Plan đã lock" không có nghĩa claim đã được chứng minh. | BO-10 |
| BR-57 | EvidenceBundle có replication package (code hash, environment, dữ liệu, seed, split). Replicator tái lập kết quả. Lệch kết quả đánh đỏ item bundle và paper không dùng. | BO-02 |

## 8.7 Budget

| ID | Rule | BO |
|---|---|---|
| BR-58 | Mỗi run có token budget, đơn vị là token. Hết budget thì run kết thúc `ended(with_gaps)` trên output tốt nhất; item hết phần budget thì thành item `needs-you`. | BO-06, BO-08 |
| BR-59 | Project có budget theo tháng. Hệ thống cảnh báo ở các ngưỡng. Ở 100%, run mới bị chặn. | BO-06 |
| BR-60 | Khi project chạm 100%, run đang chạy chuyển sang `waiting(budget_review)` và tạo item `spending` `must_ask`. Project Manager duyệt chi thêm hoặc để run kết thúc `with_gaps`. | BO-06, BO-08 |
| BR-78 | Item `spending` có hạn trả lời do project settings quy định. Hệ thống nhắc Project Manager trước hạn bằng thông báo ngoài (mail, push), cũng như khi item được tạo. Hết hạn mà không có quyết định thì run kết thúc `with_gaps`. | BO-06, BO-08 |
| BR-61 | `spending` có mức trần chi tiêu do Platform Admin đặt. Mức trần là giới hạn tiền, không phải floor. Ở `autopilot`, chi tiêu chỉ `auto` dưới mức trần; vượt mức trần thì `must_ask`. Hệ thống giữ usage và cost ledger theo run và project. | BO-06 |

## 8.8 Quản trị kết quả

| ID | Rule | BO |
|---|---|---|
| BR-62 | Dossier gồm tham chiếu tới các version EvidenceBundle và PaperPack đã accepted. Platform chỉ đánh version, kiểm hash và ghi duyệt. Platform không đánh giá khoa học. Dossier chỉ được tạo khi run có PaperPack accepted (PaperPack đã tham chiếu EvidenceBundle). Run kết thúc `with_gaps` hoặc `cancelled` trước khi có PaperPack accepted thì không có Dossier. | BO-11 |
| BR-63 | Approval do Reviewer hoặc Project Manager thực hiện theo review settings: số approval, ai được duyệt, có cho tự duyệt không. | BO-11 |
| BR-64 | Export ra ngoài project cần Dossier đã duyệt. Export là action pinned. | BO-11 |
| BR-79 | Khi EvidenceBundle hoặc PaperPack có version accepted mới, Platform tạo Dossier version mới. Approval gắn với một Dossier version và không chuyển sang version mới; version mới phải được duyệt lại. | BO-11 |

## 8.9 Paper

| ID | Rule | BO |
|---|---|---|
| BR-65 | PaperPack gồm mười item có check: reporting checklist, manuscript, claims, figures và tables, citations, limitations, reproducibility, declarations, review, formats. Đầu vào: EvidenceBundle, AnalysisPlan và Lock, Literature Base, DatasetSnapshot, decision log. | BO-10 |
| BR-66 | Mọi số trong manuscript là tham chiếu tới record của bundle, do code render. Chữ số trong text model không phải tham chiếu thì check đỏ (năm, số mục, số section được miễn). | BO-02, BO-10 |
| BR-67 | Mọi effect statement trong Abstract, Results, Discussion ánh xạ tới verdict và interpretation row. Từ chỉ mức claim khớp verdict và không vượt claim ceiling. | BO-02, BO-10 |
| BR-68 | Mọi citation nằm trong Literature Base, có DOI đã resolve và trích dẫn hỗ trợ cho claim mà nó đỡ. | BO-02, BO-10 |
| BR-69 | Limitations nêu mọi lý do grade, gap, known risk, deviation, kết quả negative control, power thấp và kết quả nhạy cảm với confounding; code kiểm độ phủ. | BO-10 |
| BR-70 | Trường chỉ tác giả (authors, affiliation, ethics, funding, conflicts, CRediT) là placeholder "awaiting author". Câu khai báo dùng AI lấy từ decision log. | BO-10 |
| BR-71 | Reporting checklist theo loại claim: STROBE + RECORD cho association và causal; TRIPOD cho prediction. Mỗi mục trỏ tới anchor trong bài hoặc ghi "awaiting author" hay "not applicable" kèm lý do. Có ít nhất ba hình chính, mọi số trên hình bằng record của bundle. | BO-10 |
| BR-72 | Writing rule có ba loại: **H** (luật cứng, vi phạm là lỗi), **M** (chỉ số có ngưỡng, vượt ngưỡng thành issue), **G** (hướng dẫn, nằm trong rubric reviewer). Nội dung chi tiết từng rule: chưa xác định (Câu hỏi mở 2). | BO-10 |
| BR-73 | Researcher quyết định nộp bài. Hệ thống không tự nộp cho publisher. | BO-10 |
| BR-74 | (Could, sau MVP) JFE dựng profile tạp chí từ corpus được phép dùng, có nguồn, quyền sử dụng, độ bất định và version; Researcher duyệt profile; paper stage tham chiếu đúng version. Profile không thay đổi nội dung hay mức chắc chắn của claim. | BO-12 |

## 8.10 Research pattern và lớp kiểm soát nghiên cứu

Các rule này bổ sung cho BR-26, BR-43..BR-46 và BR-54; chúng không thay các rule đó.

| ID | Rule | BO |
|---|---|---|
| BR-82 | Claim type gồm `association`, `causal`, `prediction` (nghiên cứu hiện tượng) và `method_comparison` (so sánh các phương pháp ML trên cùng dữ liệu). `method_comparison` có priority Should, sau MVP; MVP không đổi. | BO-01 |
| BR-83 | Task family gồm `binary`, `multiclass`, `regression` và `rare-event` (nhị phân mất cân bằng). Với `prediction` và `method_comparison` (khi FE-19 có, sau MVP), task family chọn metric policy và protocol. Với `association` và `causal`, task family chọn model family. Ranking, survival, forecasting và anomaly nằm ngoài phạm vi. | BO-01 |
| BR-84 | Cấu trúc dữ liệu gồm IID, group, thời gian và panel (BR-76). Split của dữ liệu IID có thể là split phân tầng lặp lại (repeated stratified). | BO-04 |
| BR-85 | Dataset shift có ba loại: covariate shift, label shift và concept drift. Dataset stage báo cáo từng loại riêng. | BO-01 |
| BR-86 | Pipeline order chống leakage: split trước; mọi bước học từ dữ liệu (impute, scale, encode, chọn feature, resampling) chỉ fit trong phần train; resampling chỉ trên phần train; calibration và threshold chọn trên phần validation; phần confirmation chỉ dùng một lần. | BO-04 |
| BR-87 | Vi phạm pipeline order bị guard chặn trước khi chạy, hoặc được ghi là deviation. | BO-04 |
| BR-88 | Dictionary ghi thời điểm mỗi biến sẵn có. Biến được ghi sau outcome bị gắn cờ post-outcome. Dataset stage kiểm dòng trùng lặp giữa các phần split. | BO-04 |
| BR-89 | Dataset stage gắn cờ tín hiệu dữ liệu (tỷ lệ positive thấp, categorical có cardinality cao, cột group hoặc thời gian, missingness cao) và gợi ý research pattern. Prefilter chỉ dùng phân phối biên (tỷ lệ positive là phân phối biên của outcome), không dùng quan hệ với outcome, nên blind analysis được giữ. AI gợi ý; user chọn. | BO-01 |
| BR-90 | Mỗi hypothesis kiểm được: có comparator, primary metric khớp task family, hướng hoặc margin, phạm vi và decision rule. Mệnh đề "model tốt hơn" không có comparator bị trả về để sửa. Baseline cố ý yếu không được chấp nhận. | BO-01 |
| BR-91 | Margin non-inferiority hoặc equivalence (δ) ánh xạ lên các vùng SESOI của verdict. Hệ thống không kết luận equivalence từ p-value không có ý nghĩa thống kê. | BO-10 |
| BR-92 | Portfolio hypothesis gồm một primary và một số secondary có giới hạn. Giới hạn là project setting. | BO-04 |
| BR-93 | Với `prediction` và `method_comparison` (khi FE-19 có, sau MVP), bằng chứng gồm ba evidence family theo thứ tự: discrimination, reliability (calibration, stress, uncertainty), decision (threshold, cost, subgroup). | BO-01 |
| BR-94 | Với task family `rare-event`, metric gồm average precision (AP) hoặc precision tại recall cố định, không chỉ accuracy. AP không được so sánh giữa các tập có prevalence khác nhau. Calibration dùng dữ liệu tách khỏi dữ liệu huấn luyện. | BO-01 |
| BR-95 | Research pattern là đơn vị có version, gồm: task family áp dụng, eligibility rule, cột bắt buộc, baseline policy, factor template, metric policy, chart template, statistical plan, failure mode và các action cần người. Action cần người dùng lại action pinned hiện có; không thêm điểm chặn mới. | BO-01 |
| BR-96 | Với `prediction`, pattern gồm nhóm A–E (dữ liệu và feature) và nhóm K–O (reliability và trust). Pattern F là baseline policy cho `prediction` và `method_comparison` (khi FE-19 có, sau MVP). Pattern G–J chỉ dùng cho `method_comparison` (khi FE-19 có, sau MVP). | BO-01 |
| BR-97 | Mỗi research pattern có negative test: ca cài sẵn lỗi mà pattern phải phát hiện. | BO-09 |
| BR-98 | `method_comparison` (khi FE-19 có, sau MVP) cần: so sánh theo cặp trên từng fold và seed; nhiều seed; tuning budget bằng nhau; nested validation khi có tuning; hiệu chỉnh so sánh nhiều lần; giữ kết quả negative. | BO-04 |
| BR-99 | Baseline policy (pattern F): baseline đơn giản chạy trước; cùng split; cùng tuning budget; báo cáo runtime cùng điểm số. | BO-01 |
| BR-100 | Seeded-flaw bench có red-team catalogue gồm ba nhóm lỗi cài sẵn. Dữ liệu: cột post-outcome, trùng lặp giữa các phần split, nhãn positive sai, leakage theo thời gian, target encoding fit trên toàn dữ liệu, proxy của thuộc tính được bảo vệ. Thí nghiệm: resampling trước split, tuning budget không bằng nhau, chọn feature bằng phần test, early stopping trên phần test, thiếu seed, chọn lọc run đẹp. Suy luận: equivalence từ p lớn hơn 0,05, causal claim từ feature attribution, so AP giữa các prevalence khác nhau, không báo cáo uncertainty. | BO-09 |
| BR-101 | Benchmark case catalogue gồm 60 project mẫu: mỗi project là một ca kiểm thử của research pattern, không phải một flow riêng. Catalogue nằm ở PRD §11.2.1; ID của ca có tiền tố `BC-`. Report V dẫn xuất test case từ catalogue. | BO-09 |

# 9. Assumptions và Constraints

**Assumptions**

- Platform Admin cấu hình model gateway và key; thiếu cấu hình thì run báo lỗi rõ.
- Literature provider công khai trả metadata và abstract có provenance. Full text sau paywall nằm ngoài phạm vi.
- User có dữ liệu bảng cho câu hỏi của mình hoặc dùng được dataset trong project.
- User mở Local Node khi chạy job trên dữ liệu `local`.

**Constraints**

- Chỉ dữ liệu dạng bảng.
- Project là scope cao nhất; không có organization layer.
- Local Node không đòi user cài Docker.
- Một run active mỗi project.
- BRD không chứa giá trị kỹ thuật (tên setting, giá trị mặc định, schema).
- Diagram trong `diagrams/` chưa theo thiết kế này; cập nhật ở đợt riêng (README §8).

# 10. Risks và Mitigations

| Risk | Giảm thiểu |
|---|---|
| LLM bịa nguồn hoặc số | BR-41, BR-42, BR-66, BR-68; review loop BR-35. |
| P-hacking ở kết quả xác nhận | Split theo power (BR-44), Lock (BR-47), envelope và unseal (BR-49), tried ledger (BR-52), confirmation tier (BR-53). |
| Hàng dữ liệu rời máy giữ dữ liệu | Local Node, release gate, release log (BR-19..BR-21), BR-22. |
| Researcher đổi mục tiêu giữa chừng | Amendment có version (BR-10), stale (BR-12), decision log (BR-29). |
| Reviewer cùng bias với tác giả | Context mới, nhiều persona, precision trên seeded-flaw bench (BR-36, BR-40). |
| AI PI quyết sai | Chỉ quyết tạm, không item pinned, user lật lại; overturn đề xuất nâng level (BR-29..BR-31). |
| User bị hỏi quá nhiều hoặc không có mặt | Preset theo stage, batching, presence; thông báo ngoài chỉ cho item pinned đang chặn và item `spending` (BR-24, BR-27, BR-28); hạn chờ item pinned (BR-104). |
| Chi phí hoặc provider lỗi | Token budget, project budget, `ended(with_gaps)` (BR-58..BR-61); `failed_technical` khi lỗi kỹ thuật. |
| Local Node offline làm run chờ | Run chuyển `waiting(node_offline)`; item chờ không chặn việc khác (BR-27). |
| Object upstream đổi làm downstream sai | Stale (BR-12); user chọn cập nhật. |
| Thiếu rule viết bài chi tiết | BR-72 chưa có nội dung từng rule (Câu hỏi mở 2). |
| Phạm vi mở rộng sang `method_comparison` và 60 case mẫu | Should, sau MVP; MVP không đổi (BR-82). Case có pattern G–J theo `method_comparison` (BR-101). |
| Leakage trong pipeline tiền xử lý hoặc trong dữ liệu (biến post-outcome, trùng lặp giữa các phần split) | Pipeline order và guard (BR-86, BR-87), cờ leakage (BR-88), red-team catalogue và SM-17, SM-18 (BR-100). |

---

# Câu hỏi mở

1. **Target của SM-02.** Đã đóng. Ngưỡng ghi trong bảng SM.
2. **Writing rule.** BR-72 cần nội dung chi tiết của từng rule H, M và G. Chưa xác định.
3. **Target của SM-17 và SM-18.** Đã đóng. SM-17 ít nhất 90%; SM-18 là 100%, vì guard chặn theo luật cố định.
4. **Giới hạn secondary hypothesis.** Đã đóng. Giá trị mặc định là 3 secondary hypothesis; Project Manager đổi được trong project settings (BR-92).
5. **Priority của case mẫu có pattern G–J nằm trong đợt 1.** BC-C07 thuộc đợt 1 (làm đầu), nhưng pattern G của nó thuộc `method_comparison` (Should, sau MVP). PRD §11.2.1 ghi cả hai. Hai lựa chọn: giữ BC-C07 là Should, hoặc thay bằng ca khác trong đợt 1. Chưa xác định.

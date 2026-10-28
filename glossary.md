# Glossary — OpenAI-Scientist

**Phiên bản:** 1.0 (2026-10-29) · **Trạng thái:** Approved
**Liên quan:** [README](README.md) · [BRD](BRD.md) · [PRD](PRD.md) · [Architecture](architecture.md) · [changelog](changelog.md)

Đây là **nguồn duy nhất** cho thuật ngữ của dự án. BRD, PRD, architecture, Report 7 và UI dùng đúng tên ở đây. Tài liệu khác không định nghĩa lại thuật ngữ; chúng chỉ dẫn link về file này.

## Quy tắc

1. **Một khái niệm, một tên.** Không dùng từ đồng nghĩa trong tài liệu, UI, prompt hoặc code.
2. **Thuật ngữ giữ tiếng Anh.** Văn bản giải thích có thể viết tiếng Việt; tên khái niệm giữ nguyên tiếng Anh như cột "Term".
3. **Định nghĩa ở mức khái niệm.** Không ghi đường dẫn file, tên class, route hoặc kiểu cột.
4. **Tên đã bỏ** nằm ở §11. Tài liệu mới không dùng chúng, trừ khi giải thích lịch sử.
5. **Thêm thuật ngữ** bằng một dòng changelog. Không đổi nghĩa của thuật ngữ cũ mà không ghi vào §11.

---

## 1. Actor và role

| Term | Định nghĩa |
|---|---|
| Platform Admin | Người vận hành hệ thống. Quản lý user, model, key, engine settings, budget mặc định, audit và health. Không tham gia nội dung nghiên cứu của project nếu không là member. |
| Project Manager | Member có quyền quản lý project: member, settings, budget, dataset, run, và huỷ run. Project Manager cũng có mọi quyền nghiên cứu của Researcher trong project: tạo run, trả lời decision inbox, accept object, lock plan, export. |
| Researcher | Member làm nghiên cứu: tạo research case, chạy run, trả lời decision inbox, chấp nhận hand-off object. |
| Reviewer | Member đọc và bình luận mọi object của project. Reviewer duyệt **Dossier** theo review settings của project. |
| AI Principal Investigator (AI PI) | Connector persona phía hệ thống. Trong use case, AI PI là secondary actor, hành động thay mặt user trong giới hạn của nó: tóm tắt, đề xuất bước tiếp theo, và chỉ quyết định **tạm thời** các item không pinned khi preset là `autopilot` và user `away`. AI PI không bao giờ kết thúc run và không quyết định item pinned. |
| Persona | Một "lens" có mandate, phân loại finding riêng, skill, tool và precision đo được. Có ba loại: maker (tạo object), guard (review object) và connector (nối run với user; không tạo và không review object). Các persona cụ thể nằm ở các dòng ngay dưới. Persona khác với role: "Reviewer" là role của member; "Reviewer 2" là persona guard. |
| Data Steward | Maker của dataset stage. |
| Data Scout | Maker của dataset stage. |
| Data Auditor | Guard của dataset stage. |
| Privacy Officer | Guard của dataset stage và execution stage. |
| Domain Expert | Guard của dataset stage và experiment_design stage. |
| Theorist | Maker của hypothesis stage. |
| Librarian | Maker của hypothesis stage. |
| Skeptic | Guard của hypothesis, experiment_design, execution và paper stage. |
| Methodologist | Guard của hypothesis stage và experiment_design stage. |
| Prior-art Checker | Guard của hypothesis stage. |
| Trialist | Maker của experiment_design stage. |
| Analyst | Maker của experiment_design stage. |
| Equity Reviewer | Guard của experiment_design stage. |
| Code Auditor | Guard của experiment_design stage và execution stage. |
| Engineer | Maker của execution stage. Làm việc tự do trên twin. |
| Interpreter | Maker của execution stage. Chọn một dòng của bảng diễn giải đã lock cho mỗi hypothesis. |
| Replicator | Guard của execution stage. Chạy lại replication package và so hash với EvidenceBundle. |
| Scribe | Maker của paper stage. Viết text của bản thảo. |
| Reporting Editor | Guard của paper stage. |
| Reviewer 2 | Guard của paper stage. Rubric của nó đo lỗi lớn của bản thảo. |
| Figure Reviewer | Guard của paper stage. |
| Explainer | Connector. Mandate chi tiết: chưa xác định. |
| Facilitator | Connector. Hiển thị cả hai phía khi reviewer bất đồng sau hai vòng sửa. |

## 2. Project và dữ liệu

| Term | Định nghĩa |
|---|---|
| Project | Không gian làm việc chung của một nhóm. Chứa member, settings, dataset, research case, run, Literature Base, decision inbox và audit log. |
| Project settings | Cấu hình của project: budget, review settings, preset mặc định theo stage, notification, giới hạn số secondary hypothesis, hạn chờ item pinned. |
| Review settings | Phần của project settings quy định duyệt Dossier: số approval, ai được duyệt, có cho tự duyệt không, và định dạng xuất. |
| Dataset | Một tập dữ liệu dạng bảng trong project. Có một hoặc nhiều dataset version. |
| Dataset version | Một bản bất biến của dataset, có hash. Mọi phân tích ghim (pin) một dataset version. |
| Data connection | Nguồn dữ liệu bên ngoài được uỷ quyền (ví dụ Google Sheets, Drive). Import từ connection tạo dataset version mới. |
| Data location | Nơi dữ liệu nằm: `platform` (đã upload) hoặc `local` (nằm trên máy user, chỉ Local Node đọc được). |
| Research case | Ý định nghiên cứu của một run: topic, mục tiêu, bối cảnh, ràng buộc, domain, tài liệu tham khảo. Dataset là tuỳ chọn khi bắt đầu. |
| Literature Base | Kho bằng chứng tài liệu cấp project, có version. Gồm protocol tìm kiếm, search log, quyết định sàng lọc, evidence card, evidence map và BibTeX đã kiểm. Mọi stage dùng chung. |
| Data structure | Cấu trúc phụ thuộc giữa các hàng của dataset: IID, group, thời gian hoặc panel. Researcher xác nhận cấu trúc (action pinned) trước khi split được tạo. |
| Dataset shift | Sự khác nhau giữa các phần dữ liệu (ví dụ theo thời gian hoặc nguồn). Có ba loại, mỗi loại được báo cáo riêng: covariate shift (phân phối biến đầu vào đổi), label shift (phân phối outcome đổi) và concept drift (quan hệ giữa biến đầu vào và outcome đổi). |
| Post-outcome variable | Biến được ghi sau khi biết outcome. Dictionary ghi thời điểm mỗi biến sẵn có; dataset stage gắn cờ post-outcome cho biến này vì nó gây leakage. |
| Prefilter | Quy tắc bằng code của dataset stage: gắn cờ tín hiệu dữ liệu (tỷ lệ positive thấp, categorical có cardinality cao, cột group hoặc thời gian, missingness cao) và gợi ý research pattern. Chỉ dùng phân phối biên, không dùng quan hệ với outcome, nên blind analysis được giữ. AI gợi ý; user chọn. |

## 3. Run và pipeline

| Term | Định nghĩa |
|---|---|
| Run | Một lần thực thi pipeline cho một research case. Mỗi project có tối đa **một run active**. |
| Pipeline | Thứ tự stage của run. Pipeline chuẩn là `dataset_first`: dataset → hypothesis → experiment_design → execution → paper. |
| Stage | Một bước của pipeline: `dataset`, `hypothesis`, `experiment_design`, `execution`, `paper`. |
| Engine | Service chạy một stage. Mọi engine chạy trên cùng harness. |
| Web app | Giao diện web của user: hiển thị workspace, decision inbox và trace; nhận hành động của user. Không chứa logic khoa học. |
| Run state | `running`, `waiting` (lý do: `decision`, `node_offline`, `budget_review`), `ended` (kết quả: `complete`, `with_gaps`, `failed_technical`, `cancelled`). Item pinned đang chờ giữ run ở `waiting(decision)` cho tới hạn chờ item pinned; run không kết thúc vì item đó trước hạn. Run kết thúc `with_gaps` chỉ vì ba nguyên nhân: token budget của run cạn, item `spending` quá hạn, hoặc item pinned quá hạn chờ. Project Manager hoặc Researcher đã tạo run có thể huỷ run từ mọi trạng thái trừ `ended` (`cancelled`). |
| Ended with gaps | Run kết thúc vì một trong ba nguyên nhân: token budget của run cạn, item `spending` quá hạn, hoặc item pinned quá hạn chờ. Output tốt nhất được công bố; mọi contract item đỏ được liệt kê. Khi nguyên nhân là item pinned quá hạn, item đóng ở trạng thái chưa trả lời và gap được liệt kê. Run **kết thúc**, không **dừng treo**. |
| Token budget | Giới hạn token model cho một run. Đơn vị hợp đồng là token; UI có thể hiển thị chi phí ước tính. |
| Project budget | Giới hạn chi phí theo tháng của project. Hệ thống cảnh báo ở các ngưỡng. Khi chạm 100%: run mới bị chặn; run đang chạy chuyển sang `waiting(budget_review)` và tạo item `spending` `must_ask`. Project Manager duyệt chi thêm hoặc để run kết thúc `with_gaps`. Item có hạn trả lời; hết hạn thì run kết thúc `with_gaps`. |
| Stale | Trạng thái của object downstream khi object upstream mà nó ghim có version mới. Không có gì tự cập nhật; user chọn cập nhật qua acceptance. |
| Next step | Đề xuất sau một run, chọn từ một bộ từ vựng chung: `collect_more_data`, `explore_signal`, `replicate`, `write_paper`, `revise_plan`. AI PI đề xuất; user chọn. |

## 4. Harness và kiểm soát của con người

| Term | Định nghĩa |
|---|---|
| Harness | Runtime chung của mọi engine: agent loop, action pipeline, workspace, live trace, budget và hand-off. |
| HarnessSpec | Khai báo của một engine: contract, prelude, tool, skill, guard, action type, reviewer, budget, hand-off object. Engine khác nhau chỉ ở HarnessSpec. |
| Contract item | Một phần bắt buộc của output stage, có check bằng code. Stage "done" khi mọi item xanh. |
| Check | Code đánh dấu một contract item xanh hoặc đỏ, kèm lý do. |
| Prelude | Code xác định (deterministic) chạy trước agent loop. |
| Guard | Kiểm tra chặn trước một action: data firewall, numbers-only-from-tools, object đã lock là bất biến, lọc secret. |
| Self-healing | Một check đỏ là một task cho agent loop. Trace hiển thị theo item: đỏ → action → xanh. Hết phần budget của item thì item thành `needs-you`. |
| Action type | Một loại hành động engine khai báo. Thuộc đúng một action group. User và agent đi qua cùng action pipeline. |
| Action group | Một trong tám nhóm để đặt quyền: `read_compute`, `technical_fix`, `content_judgment`, `object_drafting`, `spending`, `acceptance`, `pinned`, `unseal`. |
| Level | Mức quyền của một action: `auto`, `do_then_review`, `must_ask`. |
| Floor | Mức thấp nhất một action type được phép có. Override không được hạ dưới floor. |
| Pinned action | Action luôn `must_ask` ở mọi preset: định nghĩa outcome và estimand; xác nhận unit of observation và cấu trúc dữ liệu trước khi split; chọn hypothesis (≥ 2) và primary; join dữ liệu public vào dữ liệu riêng; lock plan; lệch khỏi thuật toán đã lock; dùng validation source; xuất ra ngoài project. Mỗi item pinned có hạn chờ (Pinned wait deadline). |
| Pinned wait deadline | Hạn chờ trả lời của mỗi item pinned; là project setting. Trước hạn, hệ thống nhắc qua thông báo ngoài (mail, push). Hết hạn, item đóng ở trạng thái chưa trả lời và run `ended(with_gaps)`. Không ai quyết thay user: không AI PI, không giá trị mặc định. Gap được liệt kê. |
| Preset | Bộ level cho tám action group, chọn **theo stage**: `co_work`, `milestones` (mặc định), `autopilot`. Preset thay thế "mode" cũ. |
| Presence | User có liên lạc được ngay không: `present` hoặc `away`. Presence không phải mode; nó chỉ đổi cách item `must_ask` chờ. |
| Decision inbox | Hàng đợi duy nhất, cho mọi stage, của các item cần user. Có tám loại item: question, review batch, tentative decision, deviation, candidate, needs-you, release review, spending. Mỗi question có option, option đề xuất và lý do. Thông báo ngoài (mail, push) chỉ cho item pinned đang chặn và item `spending` (gửi Project Manager); cả hai có lời nhắc trước hạn. Item pinned có hạn chờ; hết hạn mà chưa trả lời thì run `ended(with_gaps)`. |
| Needs-you | Item inbox khi một contract item đã tiêu hết phần budget của nó. Item này `must_ask` ở mọi preset. |
| Tentative decision | Quyết định tạm của AI PI khi `autopilot` và user `away`. Trở thành item để user xác nhận hoặc lật lại khi quay về. |
| Overturn | User đảo một quyết định đã có. Decision log ghi lại; hệ thống tính tỷ lệ overturn theo action type và **đề xuất** nâng level, không tự nâng. |
| Decision log | Nhật ký mọi quyết định: action type, level, phiên bản policy, ai quyết (user, agent, AI PI), presence, đã bị overturn hay chưa. |
| Acceptance | Action chấp nhận một hand-off object version để stage sau dùng. Level của nó theo preset; ở `milestones` level theo verdict của code. |

## 5. Review độc lập

| Term | Định nghĩa |
|---|---|
| Review loop | Review độc lập bắt buộc, chạy một lần cho mỗi object version sau khi mọi check xanh. Reviewer có context mới, không thấy trace của tác giả. Tối đa hai vòng sửa. |
| Finding | Kết quả review: category, severity (`blocking`, `major`, `minor`), anchor (object + field), evidence, failure scenario, cách sửa. Finding thiếu anchor hoặc evidence bị loại. |
| Verification of finding | Trước khi sửa, finding được kiểm bằng code hoặc verifier thứ hai: `confirmed`, `plausible`, `rejected`. Chỉ finding `blocking` đã `confirmed` mới vào vòng sửa. |
| Known risk | Finding còn lại sau hai vòng sửa. Được ghi lại và hiển thị, hoặc user quyết định giữa hai phía. |
| Seeded-flaw bench | Bộ dữ liệu cài lỗi sẵn để đo precision của reviewer. Reviewer dưới ngưỡng bị hạ severity finding. Bench có red-team catalogue; nó cũng đo tỷ lệ phát hiện leakage cài sẵn và tỷ lệ chặn vi phạm pipeline order. |
| Red-team catalogue | Danh mục lỗi khoa học cài sẵn của seeded-flaw bench, ba nhóm. Dữ liệu: cột post-outcome, trùng lặp giữa các phần split, nhãn positive sai, leakage theo thời gian, target encoding fit trên toàn dữ liệu, proxy của thuộc tính được bảo vệ. Thí nghiệm: resampling trước split, tuning budget không bằng nhau, chọn feature bằng phần test, early stopping trên phần test, thiếu seed, chọn lọc run đẹp. Suy luận: equivalence từ p lớn hơn 0,05, causal claim từ feature attribution, so AP giữa các prevalence khác nhau, không báo cáo uncertainty. |
| Benchmark case catalogue | 60 project mẫu dùng làm ca kiểm thử của research pattern. Mỗi case có ID `BC-` (benchmark case, ví dụ `BC-C01`), tên ngắn, task family, pattern, FE và priority. Nằm ở PRD §11.2.1. Report V dẫn xuất test case từ đây. |

## 6. Hand-off object

| Term | Định nghĩa |
|---|---|
| Hand-off object | Output có kiểu, có version, có hash và bất biến sau khi accepted, của một stage. Mỗi ranh giới stage có đúng một loại. |
| DatasetSnapshot | Hand-off của dataset stage: nguồn, table model, profile năm chiều chất lượng, dictionary, cleaning recipe, question map, split, vai trò nguồn, fitness. |
| Fitness | Kết luận của code về độ phù hợp của dữ liệu với câu hỏi: `fit`, `fit_with_limits`, `not_fit`. |
| Question map | Ánh xạ câu hỏi → yêu cầu dữ liệu → mức đáp ứng (`exact`, `proxy`, `derived`, `gap`). |
| HypothesisSet | Hand-off của hypothesis stage: ít nhất hai hypothesis có claim key khác nhau, một primary. Mỗi hypothesis có estimand nháp, biến, confounder có nguồn, SESOI, câu bác bỏ, loại đóng góp và nguồn gốc. |
| Evidence map | Lưới exposure × outcome do code dựng từ evidence card của Literature Base. |
| AnalysisPlan | Hand-off của experiment_design stage: estimand, protocol theo loại claim, adjustment set, analysis program, fallback, decision rule, bảng diễn giải, robustness set, design diagnosis, cấu trúc họ giả thuyết, task family, research pattern đã chọn, pipeline order, evidence family (với `prediction` và `method_comparison`). Chỉ lập kế hoạch phân tích cho dữ liệu bảng có sẵn. |
| Lock | Object riêng ghi plan đã khoá: hash của spec, program và golden outputs, snapshot version, split digest, ai khoá, khi nào. Platform ghi Lock. |
| EvidenceBundle | Hand-off của execution stage, gồm mười item có check: kết quả xác nhận, verdict và dòng diễn giải, grade, diagnostics, robustness, deviation log, tried ledger và candidate, bảng và hình, replication package, báo cáo replicator và envelope log. |
| PaperPack | Hand-off của paper stage: bản thảo IMRaD, reporting checklist, claims, hình và bảng, citation, limitation, reproducibility, declaration, kết quả review, các định dạng xuất. |
| SESOI | Smallest effect size of interest: ngưỡng hiệu ứng nhỏ nhất có ý nghĩa, dùng để phân vùng verdict. |

## 7. Execution và bằng chứng

| Term | Định nghĩa |
|---|---|
| Split | Chia hàng dữ liệu thành phần: `none`, `two_way`, hoặc `three_way` (exploration / confirmation / reserve). Dataset stage quyết định dựa trên power. Split của dữ liệu IID có thể là split phân tầng lặp lại (repeated stratified). |
| Claim type | Loại claim của hypothesis và AnalysisPlan: `association`, `causal`, `prediction` (nghiên cứu hiện tượng) và `method_comparison` (Should, sau MVP). Protocol và reporting checklist theo claim type. |
| `method_comparison` | Claim type so sánh các phương pháp ML trên cùng dữ liệu. Dùng research pattern G (tối ưu hyperparameter), H (ensemble và stacking), I (ablation), J (budget-aware) và baseline policy F. Cần: so sánh theo cặp trên từng fold và seed, nhiều seed, tuning budget bằng nhau, nested validation khi có tuning, hiệu chỉnh so sánh nhiều lần, giữ kết quả negative. Priority Should, sau MVP. |
| Task family | Loại bài toán của outcome: `binary`, `multiclass`, `regression`, `rare-event` (nhị phân mất cân bằng). Với `prediction` và `method_comparison`, task family chọn metric policy và protocol; với `association` và `causal`, nó chọn model family. Ranking, survival, forecasting và anomaly nằm ngoài phạm vi. |
| Research pattern | Đơn vị nghiên cứu có version trong registry: task family áp dụng, eligibility rule, cột bắt buộc, baseline policy, factor template, metric policy, chart template, statistical plan, failure mode, các action cần người (dùng lại action pinned) và negative test. Nhóm A–E: dữ liệu và feature (A missingness, B noise và outlier, C feature engineering và selection, D drift, E data scarcity). Nhóm F–J: model và tối ưu (F baseline, G tối ưu hyperparameter, H ensemble và stacking, I ablation, J budget-aware). Nhóm K–O: reliability và trust (K calibration và threshold, L imbalance, M stress test, N explainability stability, O fairness và cost). |
| Baseline policy | Pattern F: baseline đơn giản chạy trước; cùng split; cùng tuning budget; báo cáo runtime cùng điểm số. Baseline cố ý yếu không được chấp nhận. |
| Pipeline order | Thứ tự chống leakage: split trước; mọi bước học từ dữ liệu (impute, scale, encode, chọn feature, resampling) chỉ fit trong phần train; resampling chỉ trên phần train; calibration và threshold chọn trên phần validation; phần confirmation dùng một lần. Phần train và phần validation nằm trong phần exploration của split. Vi phạm bị guard chặn trước khi chạy, hoặc được ghi là deviation. |
| Evidence family | Nhóm bằng chứng của `prediction` và `method_comparison`, theo thứ tự: discrimination, reliability (calibration, stress, uncertainty), decision (threshold, cost, subgroup). Với `rare-event`: AP hoặc precision tại recall cố định, không chỉ accuracy; không so AP giữa các prevalence khác nhau; calibration dùng dữ liệu tách khỏi dữ liệu huấn luyện. |
| Non-inferiority margin | Margin δ đặt trước cho kiểm định non-inferiority hoặc equivalence; ánh xạ lên các vùng SESOI của verdict. Không kết luận equivalence từ p-value không có ý nghĩa thống kê. |
| Lane | Vùng làm việc trong execution: C confirmatory, D diagnostics và robustness, E exploration, P packaging. Mỗi lane có việc được làm và cấm làm. |
| Twin | Bảng tổng hợp dựng chỉ từ aggregate đã release. Engineer làm việc tự do trên twin, không trên hàng thật. |
| Implanted effect | Hiệu ứng được cài vào twin với độ lớn đã biết. Rehearsal trên twin phải phục hồi được hiệu ứng này. |
| Clean permutation check | Kiểm hoán vị trên twin khi không còn hiệu ứng thật (outcome bị xáo trộn). Tỷ lệ dương tính giả phải nằm trong khoảng cho phép. |
| Golden outputs | Output của analysis program đã lock khi chạy trên twin. Là khoá hành vi: sửa kỹ thuật phải giữ nguyên golden outputs. |
| Dry run | Chạy toàn bộ program trên dữ liệu thật nhưng chỉ trả về số hàng, kiểu, missingness, hội tụ, thời gian; không trả ước lượng. |
| Envelope | Kho kín ở Platform giữ kết quả confirmatory cho tới khi unseal. Agent chỉ thấy "done" hoặc "error". |
| Unseal | Mở envelope. Tự động khi mọi check xanh; user có thể chọn trước là mở bằng tay. Mọi hypothesis mở cùng lúc; thời điểm unseal được ghi và phải sau lần sửa lane C cuối cùng. |
| Deviation | Thay đổi thuật toán đã lock. Là action pinned và được ghi vào deviation log. |
| Verdict | Kết luận do **code** tính cho mỗi hypothesis theo decision rule đã lock (vùng SESOI): `supported`, `trivial`, `not_supported`, `insufficient`, `not_tested`. Model không tạo verdict. |
| Holm correction | Hiệu chỉnh so sánh nhiều lần theo thủ tục step-down của Holm: kiểm p-value theo thứ tự tăng dần với ngưỡng nới dần, giữ xác suất có ít nhất một dương tính giả không vượt mức đặt trước. Judge áp dụng cho secondary hypothesis. |
| Gatekeeping | Kiểm định phân cấp: secondary chỉ được kiểm sau primary. |
| Interpretation row | Dòng của bảng diễn giải đã lock, tương ứng với verdict. Lời văn kết luận lấy từ dòng này. |
| Grade | Mức tin cậy A–D của bằng chứng, do code tính từ diagnostics, robustness và deviation. |
| Claim ceiling | Mức claim mạnh nhất được phép nói, do execution stage tính từ verdict, grade và confirmation tier. Paper stage không vượt mức này. |
| Tried ledger | Sổ ghi mọi thủ tục tìm kiếm ở lane E và ngưỡng nhiễu của nó. Càng tìm nhiều, ngưỡng cho candidate sau càng cao. |
| Candidate | Hypothesis do lane E đề xuất. Không bao giờ là claim. Vào decision inbox để user chọn. |
| Candidate cap per round | Số cố định, giới hạn số candidate lane E được đưa vào decision inbox trong mỗi vòng. |
| Confirmation tier | Cách một candidate được xác nhận, mạnh nhất trước: `replicated`, `reserve`, `unsealed_untouched`, `unsealed_touched`. |
| e-value | Giá trị bằng chứng tuần tự của một record xác nhận. Chỉ tier `replicated` và `reserve` ghi e-value vào ledger. |
| confounding E-value | Giá trị nhạy cảm với confounding không đo (VanderWeele và Ding). Khác hẳn e-value; không gọi chung một tên. |

## 8. Paper

| Term | Định nghĩa |
|---|---|
| Move | Một phần chức năng của bài báo (title, abstract, introduction, methods, results, discussion, limitations, conclusion), mỗi move có công thức viết riêng. |
| Claim level | Độ mạnh của lời khẳng định trong văn bản. Phải khớp verdict và claim ceiling. |
| Reporting checklist | Checklist chuẩn báo cáo theo loại claim (STROBE + RECORD cho association/causal, TRIPOD cho prediction). Mỗi mục trỏ tới một anchor trong bài hoặc ghi "awaiting author"/"not applicable" có lý do. |
| Writing rule | Luật văn phong của paper stage. Ba loại: **H** (luật cứng, vi phạm là lỗi), **M** (chỉ số có ngưỡng, vượt ngưỡng thành issue), **G** (hướng dẫn, nằm trong rubric reviewer). |
| Journal Fingerprint Extraction (JFE) | Năng lực **Could** sau MVP: dựng profile đặc trưng của một tạp chí từ corpus được phép dùng, để paper stage tham chiếu. |

## 9. Local execution

| Term | Định nghĩa |
|---|---|
| Local Node | Service phía user giữ dữ liệu `local` và chạy job cạnh dữ liệu. Có desktop app. User không cần cài Docker. |
| Executor | Nơi chạy job phân tích: trong engine (cloud) hoặc trên Local Node. Cùng một thư viện phân tích. |
| Release | Một aggregate rời khỏi nơi giữ dữ liệu. Hàng dữ liệu không bao giờ rời đi. |
| Release gate | Điểm kiểm tra duy nhất mọi release đi qua: ngưỡng ô nhỏ, làm tròn, kiểm tra differencing, probe budget. |
| Probe budget | Giới hạn số query thăm dò trên một dataset version, do release gate theo dõi để hạn chế suy luận từ nhiều aggregate. Cạn probe budget là gap, không dừng run. |
| Release log | Danh sách chỉ-thêm (append-only) mọi release của một dataset version. |
| Disclosure mode | Chính sách release của Local Node: `standard` (tự động trong policy) hoặc `strict` (chỉ các loại số đã duyệt; loại khác chờ release review do Researcher hoặc Project Manager của project trả lời). |

## 10. Quản trị kết quả

| Term | Định nghĩa |
|---|---|
| Dossier | Gói kết quả của run để duyệt và chia sẻ: tham chiếu tới các version EvidenceBundle và PaperPack đã accepted. Platform chỉ đánh version, kiểm hash và ghi duyệt theo review settings; Platform không đánh giá khoa học. Dossier chỉ được tạo khi run có PaperPack accepted; run kết thúc `with_gaps` hoặc `cancelled` trước đó không có Dossier. |
| Approval | Quyết định duyệt Dossier của Reviewer hoặc Project Manager, theo số approval và quy tắc tự duyệt trong review settings. Export ra ngoài project cần Dossier đã duyệt. |
| Lab notebook | Nhật ký đọc được của AI PI cho run: tóm tắt, đề xuất, quyết định tạm và lý do. |
| Audit log | Nhật ký chỉ-thêm của mọi thao tác quản trị và bảo mật trong project và hệ thống. |

## 11. Tên đã bỏ

| Tên cũ | Thay bằng | Ghi chú |
|---|---|---|
| Mode `light` / `auto`; review mode `copilot` / `full` | Preset theo stage + Presence | "Mode" toàn run không còn là khái niệm người dùng. |
| Gate, answer gate, gate kind | Decision inbox item | Item `must_ask` khi user `present` được hỏi ngay; khi `away` thì xếp hàng. |
| Send back | Acceptance bị từ chối + finding, hoặc overturn | Không còn vòng gửi trả riêng của AI PI. |
| Rerun stage, heal ladder, iteration/round limit | Self-healing + một budget mỗi run | |
| Independent Review and Revision Rounds (tuỳ chọn) | Review loop (bắt buộc) | |
| Pause tự động tại giới hạn chi tiêu | `waiting(budget_review)` + item `spending` do Project Manager quyết | |
| Research Brief, coordinator, Verify, Confirmation Contract, Research State, Research Graph, error plan | Research case, harness, Lock + envelope + unseal, hand-off object, decision log | Khái niệm của bản Report trước pipeline theo stage. |
| Research context (versioned) | Research case | |
| FE-16 / HGAR | Execution stage (split, Lock, envelope, verdict, grade) | Không còn là feature riêng. |
| Writing AIF, writing stage | Paper stage | |
| Pipeline `default` (bắt đầu từ hypothesis) | Pipeline `dataset_first`; dataset stage xử lý trường hợp chưa có dataset | |
| Runner (local runner + Docker sandbox) | Local Node | Local Node không yêu cầu Docker phía user. |
| novelty (như verdict), PipelineRecommendation, Suggestion | Next step | |

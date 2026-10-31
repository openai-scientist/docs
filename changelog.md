# Changelog

## 2026-10-30 — Slide Review 2

- 2026-10-31: Sửa icon node Dokploy trong
  [`diagrams/04-system-overview/System-Architecture-Diagram.drawio`](diagrams/04-system-overview/System-Architecture-Diagram.drawio):
  node này trước đó dùng nhầm logo Docker. Thay bằng logo chính thức của Dokploy
  (dokploy.com/icon.svg), tô màu `#111827` cho đọc được trên nền thẻ trắng và
  thêm `<title>Dokploy</title>` theo cách các icon khác trong file đang làm.
  Logo nhúng inline dạng data URI trong chính file `.drawio`, không có file ảnh
  rời. Regenerate `System-Architecture-Diagram.png` bằng draw.io CLI (`-x -f png
  -s 2`).
  Validation: xem lại vùng Delivery pipeline trong PNG, icon hiển thị đúng.

- 2026-10-31: Bỏ cột MoSCoW khỏi bảng trang Main features 2/2, chia lại độ rộng
  ba cột còn lại cho kín khổ. Thông tin ngoài phạm vi MVP vẫn giữ ở dòng cuối và
  ở dòng ghi chú dưới bảng.
  File: [`docs/slides/build_review2_slides.js`](docs/slides/build_review2_slides.js),
  `docs/slides/FA26SE115_Review2.pptx`.
  Validation: `validate.py` PASSED, render PDF kiểm tra trang 12 bằng mắt.

- 2026-10-31: Làm lại trang Proposed solution cho dễ đọc khi thuyết trình: mỗi
  stage kèm nghĩa tiếng Việt (hiểu dữ liệu, đặt giả thuyết, lập kế hoạch, chạy
  phân tích, viết bài) và có mũi tên nối; bỏ đánh số ở bốn thẻ ràng buộc để
  không lẫn với số stage; thay nhãn "Dossier: duyệt rồi mới được export" bằng
  câu đầy đủ; đưa Row, Lock/envelope/unseal, Local Node, verdict xuống speaker
  notes; rút tiêu đề còn một dòng. Nội dung nghiệp vụ không đổi.
  File: [`docs/slides/build_review2_slides.js`](docs/slides/build_review2_slides.js),
  `docs/slides/FA26SE115_Review2.pptx`.
  Validation: `validate.py` PASSED, render PDF kiểm tra trang 5 bằng mắt.

- 2026-10-31: Chỉnh văn trên slide theo bộ quy tắc humanizer
  (github.com/blader/humanizer): bỏ câu mở đầu đếm số ý ("Ba chuyện lặp đi lặp
  lại:") ở trang Problem, tách thành ba câu nêu thẳng sự việc; bỏ lặp "không ai"
  trong ý 1; sửa câu callout trang Proposed solution về cấu trúc tiếng Việt
  tự nhiên ("Không hệ nào trong năm hệ thống đã khảo sát có đủ cả..."). Nội dung
  nghiệp vụ không đổi, chỉ đổi cách diễn đạt.
  File: [`docs/slides/build_review2_slides.js`](docs/slides/build_review2_slides.js),
  `docs/slides/FA26SE115_Review2.pptx`.
  Validation: `validate.py` PASSED, đối chiếu lại chữ trang 3 bằng
  `slide_text.py`.

- 2026-10-31: Viết lại chữ trên hai trang Problem và Context bằng ngôn ngữ đời
  thường, bỏ mọi mã tài liệu (BRD, BP-01…BP-16) và thuật ngữ nội bộ khỏi mặt
  slide; phần ánh xạ sang mã BP, Lock/envelope, Local Node, Dossier chuyển hết
  vào speaker notes để trả lời khi hội đồng hỏi.
  Validation: `validate.py` PASSED, render PDF kiểm tra trang 3 và 4 bằng mắt.

- 2026-10-31: Rút gọn hai trang Problem và Context về dạng danh sách ba ý đánh
  số (theo mẫu slide tham chiếu), thay cho lưới card và hàng
  Input–Process–Output–Control. Nội dung lấy từ
  [`report/00-front-and-I-introduction.md`](report/00-front-and-I-introduction.md)
  §1.3, §2, §3.6, §4, §5. Thêm helper `numbered()` trong builder.
  Validation: `validate.py` PASSED, render PDF kiểm tra trang 3 và 4 bằng mắt.

- 2026-10-31: Cập nhật phiếu đăng ký thành
  `docs/1.2/register/FA26SE115_Phieu-dang-ky_v1.3.docx` cho khớp thiết kế hiện
  hành; bản v1.2 giữ nguyên làm baseline. Thay đổi: mục b bổ sung năm stage và
  hand-off object, Literature Base, Lock–envelope–unseal, claim ceiling, Local
  Node với release gate, Dossier và approval trước export; cấu trúc dữ liệu rút
  từ 5 xuống 4 loại, Type 5 chuyển sang mục ngoài phạm vi (EX-01, EX-08);
  mục c đổi vai trò theo Report I §1.3 (Platform Admin, Project Manager,
  Researcher, Reviewer, AI PI và personas); mục d bổ sung NFR về data
  residency, run luôn kết thúc, truy vết số liệu và trích dẫn; mục e, f cập
  nhật theo task family `binary`/`multiclass`/`regression`/`rare-event`;
  RQ3 bỏ so sánh với single-prompt LLM baseline vì trái EX-09; mục 4 ghi lại
  phạm vi, exclusion và quan hệ với baseline (workstream R4–R7 của Report II).
  Validation: `validate.py --original` PASSED, render PDF 7 trang kiểm tra bằng
  mắt. Không sửa `report/*.md`.

- 2026-10-31: Bỏ callout cuối trang Problems (phần diễn giải ngoài phạm vi đặc
  tả vấn đề) và bỏ hẳn trang "Data design · Conceptual ERD" theo yêu cầu của
  người dùng. Deck còn 19 slide; section "Workflow và demo" được khai báo lại
  tại trang Demo workflows vì khai báo cũ nằm trong khối đã xoá.
  Validation: `validate.py` PASSED, render PDF kiểm tra trang 3 và các trang
  sau vị trí xoá.

- 2026-10-31: Viết lại nội dung hai trang Problems và Context theo Report I
  ([`report/00-front-and-I-introduction.md`](report/00-front-and-I-introduction.md)
  §2 Product Background, §3.6 Comparison and Research Gap, §4 Business
  Opportunity) vì bản cũ viết tắt tới mức không hiểu được. Problems: mỗi ô nêu
  đủ hiện tượng và hệ quả thay vì nhãn cụt; callout nói rõ bốn nhóm rút từ 16
  business problem BP-01…BP-16. Context: ba cột đổi thành "Việc cần làm / Chỗ
  dễ sai / Khoảng trống của công cụ hiện có", khoảng trống mô tả theo bảng so
  sánh §3.6; hàng Input–Process–Output–Control viết thành câu đủ nghĩa và có
  nhãn dẫn. Speaker notes bổ sung nguồn và các BP chưa lên slide.
  Validation: `validate.py` PASSED, render PDF kiểm tra trang 3 và 4 bằng mắt.

- 2026-10-31: Slide bìa — vẽ lại panel "Pipeline 5 stage": spine dọc nối năm
  badge số, mỗi stage kèm hand-off object (DatasetSnapshot, HypothesisSet,
  AnalysisPlan + Lock, EvidenceBundle, PaperPack). Thanh cuối nói rõ ràng buộc
  phát hành thay vì chỉ gắn nhãn: "Dossier chốt kết quả của run / duyệt xong
  mới xuất ra ngoài project" (FE-14, BP-16, SM-15, ADR-12), có mũi tên cam từ
  stage `paper` xuống thanh gate để thể hiện pipeline kết thúc ở Dossier. Bỏ chip "Phiếu
  đăng ký baseline v1.x" ở hàng mã đề tài. Panel dựng bằng shape gốc của
  pptxgenjs nên sửa trực tiếp được trong PowerPoint; bản thử bằng ảnh PNG
  (`pipeline-panel.png` và script sinh ảnh) đã bỏ để không giữ artifact phẳng.
  Validation: `validate.py` PASSED, render PDF và kiểm tra trang bìa bằng mắt.

- 2026-10-31: Đổi vị trí hai logo trên header mọi slide: lockup sản phẩm
  (logo hệ thống + tên "OpenAI Scientist") chuyển sang mép trái, logo FPT
  University chuyển sang mép phải. Sửa trong `chrome()` của
  [`docs/slides/build_review2_slides.js`](docs/slides/build_review2_slides.js),
  build lại [`docs/slides/FA26SE115_Review2.pptx`](docs/slides/FA26SE115_Review2.pptx).
  Validation: `validate.py` PASSED, render PDF và kiểm tra trang 2 bằng mắt
  (không đè vào eyebrow hay hoạ tiết góc).

- 2026-10-31: Thay infinity mark ở góc phải bằng lockup sản phẩm: logo hệ thống
  cộng tên "OpenAI Scientist". Logo render từ
  `ai-research-platform-fe/public/brand/logo-mark.svg` của repo sản phẩm ra
  `docs/slides/assets/product-mark.png`. Validation: `validate.py` PASSED,
  render PDF kiểm tra bằng mắt.

- 2026-10-31: Theo quyết định của người dùng, bỏ bốn trang Logical ERD, State
  machines và Business workflows 1/2, 2/2 (diagram dọc, chữ quá nhỏ khi chiếu).
  Deck còn 20 slide; trang Agenda cập nhật theo. Lưu ý: guide §7.1 dòng 11–12,
  13 và 14–15 vẫn liệt kê các mục này, hiện chỉ còn Conceptual ERD đại diện cho
  Data Design. Asset `docs/slides/assets/activity/` giữ lại để dùng khi cần.
  Validation: `validate.py` PASSED, render PDF 20/20 slide.

- 2026-10-31: Trang Technology bổ sung thư viện front-end thực tế đọc từ
  `package.json` của repo sản phẩm (shadcn/ui, Radix UI, TanStack Query, Redux
  Toolkit, Zustand, React Hook Form, Zod, Axios) và nhóm hạ tầng · DevOps
  (Traefik, Dokploy, Docker Hub, GitHub, GitHub Actions, Vitest, Biome, Husky,
  Resend, Google sign-in). Logo Google thay bằng bản chính thống bốn màu;
  `docs/slides/assets/tech/` còn 28 file. Validation: `validate.py` PASSED,
  render PDF kiểm tra bằng mắt.

- 2026-10-31: Trang Technology đổi từ bảng chữ sang lưới hạng mục và logo công
  nghệ, theo mẫu người dùng cung cấp: sáu hàng Front-end, Back-end, Database ·
  storage, AI · literature, DevOps · dịch vụ, Môi trường. Logo dựng từ gói
  `simple-icons` ra `docs/slides/assets/tech/` (19 file); OpenAI, Dokploy và
  Crossref không có trong gói nên để nhãn chữ. Danh sách công nghệ lấy theo
  `diagrams/04-system-overview/System-Architecture-Diagram.png`. Validation:
  `validate.py` PASSED, render PDF kiểm tra bằng mắt.

- 2026-10-31: Hai trang Main features bỏ cột ID mã FE, thay bằng cột Mô tả; mã
  FE vẫn giữ trong BRD/PRD và speaker notes. File:
  `docs/slides/build_review2_slides.js`, `docs/slides/FA26SE115_Review2.pptx`.
  Validation: `validate.py` PASSED, render PDF kiểm tra bằng mắt.

- 2026-10-31: Bỏ hai trang actor AI PI và Persona (là engine và cơ chế bên
  trong, không phải main actor); còn bốn main actor. Hai trang Business
  workflows chuyển sang Activity Diagram có swimlane, export từ
  `diagrams/11-optional/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio`
  (trang Research Setup và Experiment Execution & Validation) ra
  `docs/slides/assets/activity/`; bản export rút chiều cao lane thừa, file
  diagram nguồn giữ nguyên. Deck còn 24 slide. Validation: `validate.py`
  PASSED, render PDF kiểm tra bằng mắt.

- 2026-10-31: Thêm bộ icon dựng từ react-icons (Feather) sang PNG tại
  `docs/slides/assets/icons/`: sáu icon cho sáu trang main actor và bốn icon cho
  hàng Input · Process · Output · Control ở trang Context. Script dựng icon nằm
  trong scratchpad phiên làm việc, không thêm vào repo. Validation:
  `validate.py` PASSED, render PDF kiểm tra bằng mắt.

- 2026-10-31: Thêm trang Agenda (slide 2). Trang Context đổi từ context diagram
  sang bối cảnh sản phẩm lấy từ Report I §2 Product Background và §4 Business
  Opportunity. Trang Main actors tách thành sáu trang, mỗi actor một trang theo
  mẫu người dùng cung cấp. Deck từ 20 lên 26 slide. File:
  `docs/slides/build_review2_slides.js`, `docs/slides/FA26SE115_Review2.pptx`;
  nguồn `report/00-front-and-I-introduction.md`. Validation: `validate.py`
  PASSED, render PDF kiểm tra bằng mắt.

- 2026-10-31: Bốn slide diagram (Context, System architecture, Logical ERD,
  State machines) chuyển sang bố cục chỉ tiêu đề và sơ đồ, theo mẫu người dùng
  cung cấp. Bỏ cột chú thích bên phải, phóng to sơ đồ và căn giữa khung nội
  dung; toàn bộ phần giải thích chuyển vào speaker notes. File:
  `docs/slides/build_review2_slides.js`, `docs/slides/FA26SE115_Review2.pptx`.
  Validation: `scripts/office/validate.py` PASSED, render PDF kiểm tra bằng mắt
  20/20 slide.

- Thêm bộ slide Review 2 [FA26SE115_Review2.pptx](docs/slides/FA26SE115_Review2.pptx) (20 slide) theo đúng bảng mục 7.1 của [hướng dẫn chuẩn bị Review](docs/example/Capstone_Huong-dan-chuan-bi-Review-va-Hoi-dong_v1.3.pdf): Title, Problem, Context, Proposed Solutions, Scope updates after Review 1, Main Actors, Main Features (2 slide), System Architecture, Technology, Data Design (Conceptual ERD và Logical ERD), State Machines, Business Workflows (2 slide), Demo Workflows for Committee 1.1, Progress & Team Contribution, Risks & Open Issues, Plan to Week 14, Thank you · Q&A. Kèm [builder](docs/slides/build_review2_slides.js) để tái tạo slide từ nguồn.
- Nội dung lấy từ [Report I](report/00-front-and-I-introduction.md), [Report II](report/02-project-management-plan.md), [Report III](report/03-software-requirements-specification.md), [Report IV](report/04-software-design-document.md), [Report V](report/05-software-testing-documentation.md) và diagram đã có ([system architecture](diagrams/04-system-overview/System-Architecture-Diagram.png), [context](diagrams/12-context/System-Context-Diagram-main-2.drawio.png), [database](diagrams/06-database/Database-Diagram.png), [state machine](diagrams/09-state-machine/04-Research-Run-Orchestration.png)). Slide chỉ trình bày lại nội dung đã có, không đặt requirement hoặc rule mới, nên không sửa BRD/PRD/Use Case Spec.
- Danh sách Demo Workflows (WF-01..WF-05) và người demo là **đề xuất**, còn chờ leader chốt theo [review2-gaps.md](review2-gaps.md); ba câu hỏi mở cho GV phản biện (staging vs production, re-baseline 240 person-days, danh sách workflow) được ghi thẳng trên slide 10, 16 và 19.
- Dựng lại toàn bộ slide theo style của [Review 1 - Capstone.pptx](docs/example/Review%201%20-%20Capstone.pptx): khổ 20″×11.25″, font Be Vietnam / Be Vietnam Ultra-Bold, bảng màu trung tính kèm accent cam, card bo góc, eyebrow in hoa + tiêu đề 42pt, logo FPT University và infinity mark cùng hoa văn góc trên mọi slide. Asset lấy từ chính file Review 1 và lưu tại `docs/slides/assets/`.
- Ngôn ngữ theo đúng Review 1: eyebrow và tiêu đề slide bằng tiếng Anh, nội dung bằng tiếng Việt, thuật ngữ kỹ thuật (hand-off object, Lock, envelope, with_gaps, FE-xx, WF-xx) giữ nguyên tiếng Anh. Cấu trúc 21 slide, các con số và các điểm còn mở không đổi.
- Bản dựng lại không thêm requirement, rule hay dữ liệu mới nên không sửa BRD/PRD/Use Case Spec.
- Gọn lại đúng yêu cầu bảng 7.1: bỏ slide Testing & quality (bảng không có mục này), Problem rút còn bốn vấn đề cốt lõi mỗi vấn đề một dòng kèm mã BP, hai slide Data Design đổi thành Conceptual ERD và Logical ERD, và bỏ các khối card bổ trợ ở slide Scope updates, Main Features 2/2, Business Workflows 2/2, Demo Workflows, Progress và Risks để mỗi slide chỉ còn đúng nội dung bảng yêu cầu. Tổng còn 20 slide.
- Viết lại nội dung theo hướng slide thuyết trình: mỗi slide chỉ giữ ý chốt, chữ cỡ lớn (tiêu đề 42pt, heading card 23–27pt, nội dung 17–20pt, bảng 18–19pt), bỏ câu dài và đoạn giải thích. Toàn bộ chi tiết (mã BP/FR/ADR, chuỗi bước workflow, danh sách entity planned, phân công RACI, mốc tuần) chuyển vào speaker notes của từng slide để người thuyết trình nói, không hiển thị trên màn chiếu.
- Rà ngôn ngữ slide và speaker notes bằng bộ pattern của skill [humanizer](https://github.com/blader/humanizer) (dựa trên Wikipedia "Signs of AI writing"): bỏ em dash dùng làm liên từ ở 20 vị trí, thay bằng dấu hai chấm, chấm phẩy hoặc ngoặc đơn; bỏ cấu trúc not-X-but-Y ("không bằng quy ước làm việc", "không phải gọi API", "sinh tự động, không vẽ tay"); bỏ câu phản bác không có đối tượng ("không giấu"); thay chuỗi mũi tên trang trí bằng câu thường. Lượt rà thứ hai sửa thêm: từ thổi phồng ("cốt lõi" thành "chính"), câu mất chủ ngữ ở ghi chú đóng góp, chú thích ảnh lặp lại tiêu đề card bên cạnh, con số "12 thực thể planned" không khớp danh sách liệt kê, và dòng Môi trường trong bảng Technology mâu thuẫn với callout về staging. Giữ nguyên mọi số liệu, mã ID và nội dung nghiệp vụ.
- Validation: `validate.py` đạt "All validations PASSED"; render toàn bộ 21 slide qua LibreOffice → PDF → ảnh và xem từng slide để kiểm tra tràn chữ, chồng lấn và lề; `slide_text.py` không còn placeholder text; sau khi đổi style đã render và xem lại toàn bộ slide, sửa các chỗ chữ tràn card và bảng bị dồn. Kiểm tra link changelog và `git diff --check`. Chưa commit/push.
## 2026-10-31 — Mở rộng luồng Activity theo tám nhóm

- Mở rộng từng tab trong [bộ editable](diagrams/10-activity/Activity-Diagrams.drawio) và tám PNG, đối chiếu [sequence flows](diagrams/08-sequence/sequence_flows.py); cập nhật [thuyết minh và phạm vi](diagrams/10-activity/Activity-Diagrams-design.md). Bổ sung bước và nhánh nghiệp vụ; AI PI chuyển sang quyết định tạm, Notifications sang điều kiện gửi thông báo. Không thay đổi requirement, BRD/PRD/Use Case Spec; sơ đồ không xác nhận runtime.
- Validation: validator draw.io strict 0 lỗi, 0 cảnh báo, score 0; xuất và xem tám PNG, kiểm tra cấu trúc và guard; `git diff --check`.

## 2026-10-31 — Activity Diagram theo tám nhóm Class

- Tạo [bộ editable tám tab](diagrams/10-activity/Activity-Diagrams.drawio), tám PNG và [thuyết minh phạm vi/nguồn](diagrams/10-activity/Activity-Diagrams-design.md); cập nhật [rule](diagrams/10-activity/rule.md) và [inventory](diagrams/README.md#10-activity). Mỗi nhóm chọn một luồng đại diện từ sequence; bộ này không thay thế năm main workflow Review 2. Không thay đổi requirement, BRD/PRD/Use Case Spec hoặc xác nhận runtime.
- Validation: kiểm tra tám tab, guard và kết nối, validator draw.io strict, xuất và xem tám PNG; `git diff --check`.

## 2026-10-31 — Chỉnh mẫu Activity Diagram theo góp ý

- Bỏ khung ngoài của [mẫu đăng nhập editable](diagrams/10-activity/Sign-In-With-Email-Code-example.drawio), đặt câu hỏi trong decision và ghi `[No]` / `[Yes]` trên hai nhánh; xuất lại [PNG](diagrams/10-activity/Sign-In-With-Email-Code-example.png) và đồng bộ [rule](diagrams/10-activity/rule.md). Đây là thay đổi trình bày, không thay đổi requirement hay BRD/PRD/Use Case Spec.
- Validation: validator draw.io strict, xuất và xem PNG, kiểm tra `git diff --check`.

## 2026-10-31 — Điều chỉnh rule Activity Diagram và ví dụ

- Cập nhật [rule](diagrams/10-activity/rule.md) theo hướng dẫn Visual Paradigm và draw.io: làm rõ decision/merge, fork/join, final, object flow và swimlane; giữ phạm vi main workflow Review 2. Thêm [ví dụ editable](diagrams/10-activity/Sign-In-With-Email-Code-example.drawio) và [PNG](diagrams/10-activity/Sign-In-With-Email-Code-example.png) dựa trên sequence và thuyết minh state hiện có. Đây là mẫu notation để duyệt, không thay đổi requirement hay xác nhận runtime; không cần sửa BRD/PRD/Use Case Spec.
- Validation: validator draw.io strict 0 lỗi, 0 cảnh báo, score 0; xuất và xem PNG; kiểm tra link mới và `git diff --check`. Activitylint main-flow không phù hợp ví dụ hai lane và hiểu thoi decision trống là merge; không coi kết quả đó là kiểm chứng ngữ nghĩa.

## 2026-10-31 — Giữ đúng tám state diagram chính

- Thu gọn [file editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio), [builder](diagrams/09-state-machine/build_state_diagrams.py), [Mermaid](diagrams/09-state-machine/State-Machine-Diagrams-Mermaid.md), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md) và [inventory](diagrams/README.md#09-state-machine) về tám vòng đời chính. Bỏ bốn tab và PNG phụ cùng ảnh/diagram đăng nhập standalone; giữ mã và ghi chú lịch sử. Các link lịch sử đến ảnh đã bỏ được ghi lại dạng văn bản.
- Xuất tám PNG và cập nhật tám hình state tương ứng trong `C:/Users/ADMIN/Downloads/FA26SE115_Report7 (1).md`; mục Research Run chỉ còn hình Run. Không đổi BRD/PRD/Use Case Spec, vì thay đổi phạm vi trình bày. Các giới hạn về state khái niệm và khác biệt Project trong thuyết minh vẫn còn.
- Validation: tái tạo builder; validator draw.io 0 lỗi, 0 cảnh báo, score 0; xuất và xem tám ảnh; kiểm tra số tab, hình trong report, liên kết và `git diff --check`.

## 2026-10-31 — Chọn vòng đời chính cho tám nhóm State Diagram

- Cập nhật [builder](diagrams/09-state-machine/build_state_diagrams.py), [draw.io](diagrams/09-state-machine/State-Machine-Diagrams.drawio), [Mermaid](diagrams/09-state-machine/State-Machine-Diagrams-Mermaid.md), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và [rule](diagrams/09-state-machine/rule.md): tám tab đầu lần lượt dùng Account, Project, Dataset, Run, Hand-off Object, Decision Item, in-app Notification và Monitoring Alert. Giữ Dossier, Email Code, Local Node pairing và notification email ở bốn tab riêng. Xuất PNG cho ba tab mới và ba tab được chuyển sang vị trí riêng.
- Cập nhật ảnh Account, Dataset, in-app Notification và bổ sung ảnh Run trong `C:/Users/ADMIN/Downloads/FA26SE115_Report7 (1).md`, giữ ảnh Dossier. Không đổi BRD/PRD/Use Case Spec: đây là cách trình bày vòng đời, không thay đổi requirement. Dataset available và unread/read là trạng thái khái niệm, không phải enum mới; Local Node và email retry vẫn là thiết kế dự kiến. Schema Project có status và archived_at khác với view lifecycle; chưa có quy tắc ánh xạ đầy đủ.
- Validation: chạy builder, validator draw.io score 0, xem PNG, kiểm tra ảnh nhúng và `git diff --check`; chưa xác nhận runtime.

## 2026-10-31 — Bổ sung sequence khớp nội dung report

- Đối chiếu Report7 mục III 3.7.1–3.7.3, III 3.8.2 và IV 3.6.2–3.6.4, 3.7.3. Bổ sung bốn tab và PNG trong [AI Principal Investigator](diagrams/08-sequence/06-ai-principal-investigator/Sequence-Diagrams-AI-Principal-Investigator.drawio) và [Notifications & Integrations](diagrams/08-sequence/07-notifications-integrations/Sequence-Diagrams-Notifications-Integrations.drawio); giữ các tab action policy, decision và inbox hiện hữu. Đồng bộ [flow source](diagrams/08-sequence/sequence_flows.py), [builder](diagrams/08-sequence/build_sequence_groups.py) và [inventory](diagrams/08-sequence/Sequence-Groups-design.md). Bốn ảnh được nhúng vào `C:/Users/ADMIN/Downloads/FA26SE115_Report7 (1).md` đúng caption; các bước nội bộ là đề xuất thiết kế, không xác nhận runtime. Không đổi BRD/PRD hoặc use case; report nêu mô tả màn hình tương ứng.
- Chưa giải quyết mâu thuẫn caption Pause/Resume/Stop/Abandon với FR-21/22 và mô hình state; không thêm hành vi chưa được thống nhất.
- Validation: tái tạo tám nhóm; validator hai file thay đổi 0 lỗi, 0 cảnh báo, score 0; xuất và xem bốn PNG; kiểm tra reference ảnh trong report và `git diff --check`.







## 2026-10-30 — Đồng bộ chỉnh sửa tay State Diagram

- Đồng bộ đường nối do người dùng chỉnh ở [Research Engines](diagrams/09-state-machine/05-Research-Engines.png) và [AI Principal Investigator](diagrams/09-state-machine/06-AI-Principal-Investigator.png) vào [builder](diagrams/09-state-machine/build_state_diagrams.py), xuất lại PNG từ [draw.io](diagrams/09-state-machine/State-Machine-Diagrams.drawio) hiện tại. Đây là điều chỉnh bố cục, không thay đổi requirement hoặc nội dung nghiệp vụ.
- Validation: validator strict 0 lỗi, 0 cảnh báo; chạy builder trong thư mục tạm và đối chiếu cell, style và geometry cả chín tab với file đã chỉnh; xem hai PNG; `git diff --check`.

## 2026-10-30 — Gom đường kết thúc AI Principal Investigator

- Bỏ các junction hiển thị trong [AI Principal Investigator](diagrams/09-state-machine/06-AI-Principal-Investigator.png); các transition hoàn tất dùng chung đường vẽ đến một final. Trong [draw.io](diagrams/09-state-machine/State-Machine-Diagrams.drawio), mỗi transition vẫn có source và target riêng. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và [rule](diagrams/09-state-machine/rule.md); không thay đổi requirement.
- Validation: builder chạy thành công; validator strict 0 lỗi, 0 cảnh báo; đã xem PNG, kiểm tra tái tạo và `git diff --check`. Các đoạn đường trùng nhau là chủ ý để tạo đường chung.

## 2026-10-30 — Gom final của AI Principal Investigator

- Chuyển trạng thái Closed do huỷ run sang bên phải, gom các nhánh hoàn tất bằng junction tới một final trong [AI Principal Investigator](diagrams/09-state-machine/06-AI-Principal-Investigator.png). Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [draw.io](diagrams/09-state-machine/State-Machine-Diagrams.drawio), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và [rule](diagrams/09-state-machine/rule.md). Đây là thay đổi trình bày, không thay đổi requirement.
- Validation: builder, validator strict 0 lỗi 0 cảnh báo, xuất và xem PNG, kiểm tra tái tạo và `git diff --check`.

## 2026-10-30 — Giảm kích thước mũi tên State Diagram

- Giảm kích thước đầu mũi tên từ 10 xuống 7 trong [diagram chín tab](diagrams/09-state-machine/State-Machine-Diagrams.drawio) và diagram đăng nhập (đã loại khỏi bộ hiện hành); cập nhật builder và xuất lại PNG. Đây là thay đổi trình bày, không đổi requirement.
- Validation: chạy hai builder; validator strict 0 lỗi, 0 cảnh báo cho cả hai file; xuất PNG từng tab và xem Research Engines, AI PI; `git diff --check`.

## 2026-10-30 — Chạy lại builder State Diagram

- Theo yêu cầu chạy builder, tái tạo [State Machine Diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio), bản đăng nhập (đã loại khỏi bộ hiện hành), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và PNG từ builder. Các chỉnh sửa thủ công chưa có trong builder không còn trong bản tái tạo; đã lưu bản trước khi chạy vào thư mục tạm. Không thay đổi requirement.
- Validation: hai builder chạy thành công; validator strict 0 lỗi, 0 cảnh báo cho hai draw.io; xuất và xem tổng quan chín PNG; `git diff --check`.

## 2026-10-30 — Đổi kiểu đầu mũi tên State Diagram

- Đổi transition sang đầu mũi tên mặc định có tô trong [diagram chín tab](diagrams/09-state-machine/State-Machine-Diagrams.drawio) và bản đăng nhập riêng (đã loại khỏi bộ hiện hành); xuất lại PNG và cập nhật kiểu trong builder cùng [rule](diagrams/09-state-machine/rule.md). Đây là thay đổi trình bày, không đổi requirement. Giữ nguyên chỉnh sửa thủ công hiện có; builder chưa đồng bộ các chỉnh sửa tay đó.
- Validation: so sánh XML xác nhận chỉ đổi thuộc tính kiểu đầu mũi tên; validator strict cho cả hai file 0 lỗi, 0 cảnh báo; xuất PNG và xem tab AI PI, Research Engines; `git diff --check`. Không chạy generator để tránh ghi đè chỉnh sửa tay.

## 2026-10-30 — Đồng bộ Mermaid vào tám tab Class Diagram

- Đối chiếu [tám khối Mermaid](diagrams/07-class/Class-Diagrams-Mermaid.md) với [diagram editable](diagrams/07-class/Class-Diagram-Authentication-Account.drawio); bổ sung năm composition User–AuthSession, Dataset–DatasetVersion, Run–StageRun, Dossier–Approval và Lock–Envelope vào [builder Authentication](diagrams/07-class/build_authentication_account.py) và [builder các nhóm](diagrams/07-class/class_diagram_pages.py). Project–ProjectSettings đã có sẵn; thoi đặc đặt phía toàn thể. Đồng bộ [thuyết minh](diagrams/07-class/Class-Diagrams-design.md), [Authentication](diagrams/07-class/Authentication-Account-design.md) và PNG bốn tab. Các composition bổ sung là lựa chọn thiết kế theo Mermaid, chưa xác nhận lifecycle khi xóa; không đổi requirement, BRD/PRD hay Use Case Spec.
- Validation: đối chiếu tám tab với Mermaid về 101 classifier, thành viên, 100 quan hệ, nhãn, multiplicity, loại và chiều; so sánh trước/sau chỉ năm style quan hệ đổi; Mermaid parse tám khối thành công, builder tái tạo byte-identical, validator 0 lỗi/0 cảnh báo, score 0; xuất và xem bốn PNG ảnh hưởng; `git diff --check`. Chưa xác nhận runtime hoặc in/chèn Word.





## 2026-10-30 — Thêm Mermaid cho State Diagram

- Thêm [Markdown Mermaid chín state diagram](diagrams/09-state-machine/State-Machine-Diagrams-Mermaid.md), dựa trên [draw.io](diagrams/09-state-machine/State-Machine-Diagrams.drawio) và liên kết tới [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md). Đây là định dạng trình bày bổ sung, không đổi requirement hoặc diagram gốc.
- Validation: Mermaid parse thành công cả chín khối; đối chiếu số transition từng tab với draw.io; kiểm tra `git diff --check`. Chưa kiểm tra ảnh render của từng Mermaid.

## 2026-10-30 — Tách mũi tên vào Stale

- Sắp xếp các transition vào Stale trong [Research Engines](diagrams/09-state-machine/05-Research-Engines.png) theo các hành lang vuông góc, tách điểm vào và nhãn. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [diagram editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio) và [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md); không đổi state hay requirement.
- Validation: validator strict 0 lỗi, 0 cảnh báo; xuất và xem PNG; kiểm tra tái tạo và `git diff --check`.

## 2026-10-30 — Tách đường nối State Diagram

- Đi lại các transition trong [Research Run](diagrams/09-state-machine/04-Research-Run-Orchestration.png) và [Research Engines](diagrams/09-state-machine/05-Research-Engines.png), tách các nhánh hạn chờ/chi tiêu và nhánh từ Draft sang Stale; giữ nguyên sự kiện, state và điều kiện trong metadata. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [diagram editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio) và [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md). Không thay đổi requirement.
- Validation: validator strict 0 lỗi, 0 cảnh báo; xuất và xem hai PNG, xem tổng quan chín tab; kiểm tra tái tạo và `git diff --check`.

## 2026-10-30 — Bỏ khung composite State Diagram

- Bỏ composite trong [Research Run](diagrams/09-state-machine/04-Research-Run-Orchestration.png) và [Research Engines](diagrams/09-state-machine/05-Research-Engines.png); thay transition kế thừa bằng transition riêng từ từng state tương ứng. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và [rule](diagrams/09-state-machine/rule.md). Không đổi requirement.
- Validation: validator strict 0 lỗi, 0 cảnh báo; xuất và xem hai PNG, kiểm tra tái tạo và `git diff --check`.

## 2026-10-30 — Bố cục Class Diagram trên xuống

- Sắp lại cả tám tab trong [Class Diagram editable](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): controller ở trên khi có, các service/interface trải ngang, entity và enum ở dưới theo cụm; đồng bộ [builder](diagrams/07-class/class_diagram_pages.py), [rule](diagrams/07-class/rule.md), [thuyết minh](diagrams/07-class/Class-Diagrams-design.md) và tám PNG. Chuyển Project–ProjectSettings thành composition dựa trên thiết kế cấu hình riêng project và code ProjectSetting; các cặp khác giữ nguyên do chưa đủ căn cứ lifecycle. Không đổi requirement, BRD/PRD hoặc Use Case Spec.
- Validation: so sánh tám tab giữ ID, text và source/target, chỉ thay loại quan hệ Project–ProjectSettings; builder tái tạo byte-identical, validator 0 errors/0 warnings, score 0; xuất và xem tám PNG, sửa đường xuyên hộp phát hiện khi xem; kiểm tra `git diff --check`. Chưa kiểm tra in/chèn Word hoặc runtime.




## 2026-10-30 — Rút gọn luồng chính Research Run

- Điều chỉnh [Research Run](diagrams/09-state-machine/04-Research-Run-Orchestration.png): đặt các transition sang Waiting trực tiếp trên trục dọc, giữ nhánh quay lại ở phải và transition chung từ composite. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [diagram editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio) và [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md). Không đổi requirement; các guard/effect đầy đủ vẫn lưu trong metadata.
- Validation: validator strict 0 lỗi, 0 cảnh báo; đã xuất và xem PNG; kiểm tra tái tạo và `git diff --check`. Validator hình học không chứng nhận đầy đủ ngữ nghĩa UML.

## 2026-10-30 — Bố cục dọc Research Run

- Sắp [Research Run](diagrams/09-state-machine/04-Research-Run-Orchestration.png) theo trục dọc; các nhánh chờ và tiếp tục đi hai bên, các nhánh kết thúc có hành lang riêng. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [diagram editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio) và [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md); không thay đổi requirement hoặc transition.
- Validation: validator strict 0 lỗi, 0 cảnh báo; xuất và xem PNG, kiểm tra tái tạo và `git diff --check`.

## 2026-10-30 — Gom transition chung của Research Run

- Theo đính chính của người dùng, thay khung ngoài ở [Research Run](diagrams/09-state-machine/04-Research-Run-Orchestration.png) bằng composite Active run chứa Running và Waiting. Ba transition cancel, technical failure và token exhaustion đi từ composite đến Ended; các nhánh theo từng state vẫn riêng. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [diagram editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và [rule](diagrams/09-state-machine/rule.md). Không đổi requirement.
- Validation: validator strict 0 lỗi, 0 cảnh báo; xuất và xem PNG, kiểm tra tái tạo và `git diff --check`.

## 2026-10-30 — Rút ngắn đường gấp Class Diagram

- Chuyển sáu đường gấp thành đường chéo trong [Class Diagram editable](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), gồm `checks platform rights`; cập nhật [builder](diagrams/07-class/class_diagram_pages.py), [thuyết minh](diagrams/07-class/Class-Diagrams-design.md) và PNG Authentication, Data, Administration. Điều chỉnh nhãn multiplicity của association chéo; ba tuyến gấp còn lại tránh class/đường trung gian. Đây là chỉnh trình bày, không đổi requirement hoặc BRD/PRD/Use Case Spec.
- Validation: so sánh nội dung và loại/chiều connector trước/sau, builder tái tạo ổn định, validator 0 errors/0 warnings, score 0; đã export và xem ba PNG, kiểm tra `git diff --check`. Chưa kiểm tra in hoặc chèn Word.


## 2026-10-30 — Sửa đường nối và thêm khung Research Run

- Đi lại các mũi tên vào choice trong [Research Engines](diagrams/09-state-machine/05-Research-Engines.png), thêm khung bao cho [Research Run](diagrams/09-state-machine/04-Research-Run-Orchestration.png); đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [diagram editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và [rule](diagrams/09-state-machine/rule.md). Khung là ranh giới trình bày, không thay đổi quan hệ state hay requirement.
- Validation: validator strict 0 lỗi, 0 cảnh báo; xuất và xem lại hai ảnh; kiểm tra tái tạo và `git diff --check`.

## 2026-10-30 — Đi dây Class Diagram tự nhiên hơn

- Đối chiếu trực tiếp bốn tab Class trong mẫu GreenLens và chỉnh 24 dependency thành các đường thẳng tỏa nhánh trên bảy tab của [diagram editable](diagrams/07-class/Class-Diagram-Authentication-Account.drawio); giữ tuyến gấp khúc nơi cần tránh hộp và giữ nguyên tab Research Engines. Đồng bộ [builder](diagrams/07-class/class_diagram_pages.py), [rule](diagrams/07-class/rule.md), [thuyết minh](diagrams/07-class/Class-Diagrams-design.md) và PNG bảy tab. Đây là thay đổi trình bày, không đổi requirement hay BRD/PRD/Use Case Spec.
- Validation: so sánh XML trước/sau giữ ID, nội dung, source/target, loại và chiều connector; builder tái tạo byte-identical; validator 0 errors/0 warnings, score 0; export và xem bảy PNG bị ảnh hưởng; `git diff --check` sạch. Chưa kiểm tra kích thước khi chèn Word.

## 2026-10-30 — Bổ sung contract connector cho Data Management

- Bổ sung `ConnectorFactory`, `Connector` và `GoogleSheetsConnector` vào [Class Diagram editable](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), kèm dependency và realization; đồng bộ [builder](diagrams/07-class/class_diagram_pages.py), [PNG Data Management](diagrams/07-class/Class-Diagram-Data-Management.png) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md). Contract dựa trên code backend và flow import trong [Report IV](report/04-software-design-document.md); không bổ sung repository khi chưa có căn cứ. Đây là chi tiết thiết kế, không đổi requirement nên không sửa BRD/PRD/Use Case Spec.
- Validation: builder tái tạo ổn định, validator 0 errors/0 warnings, score 0; export và xem PNG tab Data Management; kiểm tra link nguồn và `git diff --check`. Các class hiện tại còn lại không bị thay nội dung. Chưa xác nhận runtime hoặc khả năng đọc khi chèn Word.

## 2026-10-30 — Rà soát quan hệ Class Diagram

- [Builder Class](diagrams/07-class/class_diagram_pages.py) và [builder Authentication](diagrams/07-class/build_authentication_account.py) khai báo loại connector tường minh, hỗ trợ các ký hiệu UML trong [rule](diagrams/07-class/rule.md); giữ dependency/association khi nguồn chưa chứng minh loại khác. Trong [editable tám tab](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), sửa multiplicity đầu DecisionInboxItem thành `1` theo [Report IV §2.1.3](report/04-software-design-document.md), cập nhật [PNG AI PI](diagrams/07-class/Class-Diagram-AI-Principal-Investigator.png) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md). Không thay requirement hay BRD/PRD/Use Case Spec.
- Validation: builder tái tạo byte-identical; so sánh tám tab xác nhận giữ IDs, source/target và text ngoại trừ multiplicity nêu trên; validator 0 errors/0 warnings, score 0; xuất và xem PNG tab AI PI; kiểm tra `git diff --check`. Ký hiệu không đồng nghĩa xác nhận implementation/runtime.

## 2026-10-30 — Làm rõ cách chọn quan hệ Class Diagram

- Cập nhật [rule Class Diagram](diagrams/07-class/rule.md) để chọn loại quan hệ theo ngữ nghĩa và nguồn, quy định ký hiệu/chiều, và yêu cầu builder nhận loại tường minh thay vì suy từ multiplicity. Đối chiếu 33 tab Class trong file draw.io GreenLens do người dùng cung cấp và phần class specification trong report mẫu; phân biệt style trong mẫu với ngữ nghĩa cần xác minh. Đây là thay đổi quy tắc, không đổi requirement, BRD/PRD, nội dung diagram hoặc builder hiện tại.
- Kiểm kê 80 tab và thống kê style của 356 connector trong 33 tab Class từ XML; kiểm tra link nội bộ mới và `git diff --check`. Chưa render mẫu, chạy generator hay render diagram dự án vì không sửa diagram/builder.


## 2026-10-30 — Làm gọn State Machine Diagram

- Chỉnh ngăn tên composite Research Engines, rút gọn nhãn transition và bỏ tiêu đề/chú thích rời ngoài graph; giữ guard, effect, kết quả và phạm vi trong metadata và [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md). Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [quy tắc](diagrams/09-state-machine/rule.md), [diagram chín tab](diagrams/09-state-machine/State-Machine-Diagrams.drawio), bản đăng nhập riêng và PNG. Đây là thay đổi trình bày, không đổi requirement.
- Kiểm tra: validator draw.io strict cho cả hai file đạt 0 lỗi, 0 cảnh báo; xuất và xem chín tab, kiểm tra tái tạo và `git diff --check`. Không xác nhận runtime hoặc khả năng đọc khi chèn Word.

## 2026-10-30 — Hợp nhất lịch sử tài liệu

- Giữ các mục changelog của hai nhánh và cập nhật hai liên kết diagram đã chuyển vị trí; ghi đường dẫn tài liệu Review 2 không còn trong repository dưới dạng văn bản. Merge không thay đổi requirement hoặc workflow, nên không sửa BRD/PRD/Use Case Spec.
- Validation: builder [Package Diagram](diagrams/05-package/build_package_diagram.py) tái tạo [editable](diagrams/05-package/Package-Diagram.drawio) byte-identical với `PYTHONUTF8=1`; validator strict có 0 errors và lần lượt 61, 104, 59 warnings cho Package, [System Architecture](diagrams/04-system-overview/System-Architecture-Diagram.drawio), [Deployment](diagrams/04-system-overview/Deployment-Diagram-Production.drawio). Đã xem ba PNG hiện có; chưa render lại. Kiểm tra liên kết changelog và `git diff --check`.

## 2026-10-30 — Research Engines dùng composite state

- Theo lựa chọn mới, [Research Engines](diagrams/09-state-machine/05-Research-Engines.png) gom bảy state chưa stale vào composite Current version (not stale), Stale ở ngoài. Một transition upstreamVersionChanged từ state cha áp dụng cho mọi state con khi pinned upstream có version mới, thay cho bảy nhánh lặp và chuỗi junction. Có initial ngoài vào composite và initial trong vào Draft; giữ nguyên state, nhánh checks/review, giới hạn revision và khoảng cách đều.
- Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio), PNG tab 5, [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md), [review](diagrams/09-state-machine/State-Machine-Diagrams-review.md), [inventory](diagrams/README.md). Đây là đổi cấu trúc biểu diễn, không đổi requirement/business rule nên không sửa BRD/PRD/Use Case Spec; không sửa XML các tab khác.
- Validation: builder tái tạo ổn định; kiểm tra hierarchy, đủ bảy state con, một transition invalidation kế thừa, không junction, đúng initial và giữ guard/effect; validator --strict --score đạt 0 errors/0 warnings, score 0. Export PNG tab 5 scale 2/border 20 và mở xem; link nội bộ mới và git diff --check đạt. Chưa kiểm tra runtime hoặc in/chèn Word; không commit/push.

## 2026-10-30 — Chia đều khoảng cách và dùng junction cho Research Engines

- Theo yêu cầu mới, [Research Engines](diagrams/09-state-machine/05-Research-Engines.png) có state/choice cao 80, bước hàng 200 và khoảng trống dọc 120 trước scale. Sáu nhánh invalidation từ trục chính nằm ngang dài bằng nhau; dùng chuỗi junction nối từng đoạn riêng về junction trung tâm trước Stale, không chồng dây và không đồng bộ. Checks failed vẫn có nhánh ngoài vào junction thấp nhất; giữ đủ bảy nguồn invalidation và guard/effect hiện có.
- Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio), PNG tab 5, [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md), [review](diagrams/09-state-machine/State-Machine-Diagrams-review.md). Đây là chỉnh bố cục/ký pháp, không đổi requirement nên không sửa BRD/PRD/Use Case Spec; các tab khác giữ nguyên XML.
- Validation: validator --strict --score đạt 0 errors/0 warnings, score 0; kiểm tra khoảng cách bằng geometry và đường đi của cả bảy nguồn qua junction tới Stale, không có trigger mới trên đoạn continuation; builder tái tạo ổn định, link mới và git diff --check đạt. Export tab 5 scale 2/border 20 và mở xem PNG. Chưa kiểm tra in/chèn Word; không commit/push.

## 2026-10-30 — Làm rõ bố cục Research Engines

- Theo phản hồi hình bị rối, sửa riêng [Research Engines PNG](diagrams/09-state-machine/05-Research-Engines.png): luồng chính một trục dọc, tách đường hồi tiếp checks/revision, bỏ hai junction và các thân chung; đủ bảy đường độc lập tới Stale. Nhãn vòng revision rút gọn bằng round, đặc tả đầy đủ vẫn giữ trong metadata/bảng truy vết.
- Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md), [review](diagrams/09-state-machine/State-Machine-Diagrams-review.md). Không đổi requirement/state/business rule nên không sửa BRD/PRD/Use Case Spec; giữ nguyên XML các tab khác, kể cả tab Dossier riêng hiện có.
- Validation: builder tái tạo ổn định; validator --strict --score đạt 0 errors/0 warnings, score 0; đối chiếu XML các tab khác không thay đổi, đủ bảy nhánh Stale và guard giới hạn revision. Export riêng tab 5 scale 2/border 20, mở xem PNG sau sửa; kiểm tra link nội bộ mới và git diff --check. Chưa kiểm tra in/chèn Word; không commit/push.

## 2026-10-30 — Một junction cho các nhánh Stale

- Dùng một junction gom các transition thay thế tới Stale trong [diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio); giữ các trạng thái checks theo Report IV, Checks failed nối trực tiếp. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và [ảnh](diagrams/09-state-machine/05-Research-Engines.png). Thay đổi trình bày, không đổi BRD/PRD.
- Validator `--strict --score` 0 lỗi, 0 cảnh báo; ảnh đã xuất và xem.

## 2026-10-30 — Đi dây vuông góc các nhánh Stale

- Chuyển năm nhánh tới Stale sang đường vuông góc và các junction nối tiếp trong [diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio); giữ trigger từng nhánh, đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), và [ảnh](diagrams/09-state-machine/05-Research-Engines.png). Bố cục không thay đổi BRD/PRD.
- Đã xuất và xem ảnh; validator `--strict --score`: 0 lỗi, 0 cảnh báo.

## 2026-10-30 — Junction cho các nhánh vào Stale

- Gom năm nhánh thay thế vào Stale bằng junction trong [State Diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio); giữ trigger và nguồn từng nhánh, Draft và Checks failed giữ đường ngoài. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [rule](diagrams/09-state-machine/rule.md), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md) và [ảnh](diagrams/09-state-machine/05-Research-Engines.png). Chỉ đổi bố cục, không đổi BRD/PRD.
- Đã xem ảnh; validator `--strict --score` 0 lỗi, 0 cảnh báo.

## 2026-10-30 — Junction cho các nhánh revision

- Dùng junction gom hai nhánh revision về choice kiểm tra contract trong [State Diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio); giữ trigger, guard và effect riêng. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [rule](diagrams/09-state-machine/rule.md), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [README](diagrams/README.md) và [ảnh](diagrams/09-state-machine/05-Research-Engines.png). Bố cục không thay đổi requirement, không cần sửa BRD/PRD.
- Validator `--strict --score`: 0 lỗi, 0 cảnh báo; đã xem ảnh xuất.

## 2026-10-30 — Chỉnh mũi tên tại choice của Research Engines

- Tách điểm nối hai transition trở về choice và dịch nhãn tránh chồng đường trong [diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio); đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py) và [ảnh](diagrams/09-state-machine/05-Research-Engines.png). Chỉ thay bố cục, không đổi BRD/PRD hoặc flow.
- Validator `--strict --score` 0 lỗi/0 cảnh báo; ảnh đã xuất để kiểm tra.

## 2026-10-30 — Chỉnh trình bày Research Engines State Diagram

- Bỏ khối mô tả khỏi hình, giãn điểm nối của các transition vào Stale trong [State Diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio); giữ nội dung nghiệp vụ và thuyết minh trong [inventory](diagrams/09-state-machine/State-Machine-Diagrams-design.md). Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py) và [ảnh Research Engines](diagrams/09-state-machine/05-Research-Engines.png). Không cần sửa BRD/PRD vì chỉ đổi bố cục.
- Đã xem ảnh xuất; validator `--strict --score` đạt 0 lỗi, 0 cảnh báo.

## 2026-10-30 — Chỉnh nhãn vòng lặp Project

- Đưa nhãn `project updated` xuống dưới cạnh vòng lặp hẹp trong [State Diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio), đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py) và [ảnh Project](diagrams/09-state-machine/02-Project-Workspace.png). Đây là thay đổi bố cục, không đổi requirement.
- Validator `--strict --score`: 0 lỗi, 0 cảnh báo; đã xem ảnh xuất.

## 2026-10-30 — Tách vòng đời Dossier trong State Diagram

- Tách Dossier Version khỏi Project Workspace thành tab thứ chín trong [State Machine Diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio), giữ tám tab nhóm hiện có và graph/guard gốc. [Builder](diagrams/09-state-machine/build_state_diagrams.py), [inventory](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md) và [diagrams README](diagrams/README.md) được đồng bộ. ResearchRun và Hand-off Object Version đã có sẵn ở tab tương ứng.
- Xuất và xem [Project](diagrams/09-state-machine/02-Project-Workspace.png) và Dossier Version (đã loại khỏi bộ hiện hành). Validator draw.io `--strict --score`: 0 errors, 0 warnings, score 0. Không đổi BRD, PRD hoặc report: thay đổi chỉ tách view diagram, không đổi requirement.


Định dạng theo [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Mỗi phiên bản là một mốc tài liệu theo ngày. Đường dẫn là đường dẫn tương đối từ repository root.

## 2026-10-30 — Report 7 mục V: viết gọn theo mẫu SEP490

- Viết lại mục V của [Report 7 docx](deliverables/FA26SE115_Report7.docx) theo đúng khung của template `docs/example/2_SEP490/Report7_Final Project Report.docx` và bài mẫu GSU26SE41:
  - Mục 1–3 chỉ gồm bảng ngắn: Scope, Testing Types, Test Levels, Supporting Tools, Human Resources, Test Environment, Test Milestones.
  - Mục 4–5 gồm tên workbook Report 5 kèm ảnh chụp sheet và caption.
  - Mục V giảm từ khoảng 50 trang xuống 4 trang.
  - Bỏ 101 test case thiết kế "Not run", ma trận FR và catalogue benchmark.
- Nguồn nội dung là [S5 supplement](deliverables/supplements/S5-testing.md). Script [inject_report_v.py](deliverables/tests/inject_report_v.py) chèn nội dung vào docx và render ảnh từ workbook.
- Mục lục: đổi tên 4.1, 4.2, 5.1 và 5.2. Số trang cần update field trong Word.
- Không sửa [report/05-software-testing-documentation.md](report/05-software-testing-documentation.md) (leader). Mục V của docx giờ khác bản md này, cần báo leader.
- Unit Test workbook:
  - Sửa version Python từ 3.13 thành 3.12.
  - Dọn các hyperlink còn sót từ template ở sheet Functions và Statistics.
  - Thu hẹp cột N/A/B.
- Validation: render PDF bằng LibreOffice, xem lại các trang 175–179. Không còn hyperlink trỏ tới sheet không tồn tại.

## 2026-10-30 — Report 5: Unit Test và System Test Report

- Thêm [Unit Test workbook](<deliverables/FA26SE115_Report5_Unit Test.xlsx>) theo template SEP490: 40 function của management service, 330 UTCID (N 125 / A 113 / B 92). Spec nằm ở [unit_spec.py](deliverables/tests/unit_spec.py) và [unit_spec_more.py](deliverables/tests/unit_spec_more.py). Thêm nhóm 20 function thứ hai gồm Google sign-in, session, import dữ liệu, live view, integration, email/stream thông báo, settings và model admin, gate, send back, accept, replay, Local Node job và monitoring. Hai biểu đồ ở sheet Statistics được trỏ lại vào dòng Sub total và dời xuống dưới bảng. Kết quả P/F lấy từ JUnit của lần chạy pytest thật: `uv run --package management pytest -n 4 -m "not live and not bench"`, 1833 passed, 50 skipped, logos commit af201866. Tất cả 330 case đều Passed.
- Thêm [Test Report workbook](<deliverables/FA26SE115_Report5_Test Report.xlsx>): 8 feature, 58 system test case, chạy thật qua HTTP trên local docker stack 3 round (2026-10-30). Mỗi round đều ra 48 Passed, 1 Failed, 9 Pending. Hai lần chạy bị hỏng vì script không đăng nhập được (giới hạn số mã gửi cho mỗi email trong một giờ dẫn tới 401 dây chuyền). Đó là lỗi của script, không phải của app, nên không tính; kết quả được giữ ở `deliverables/tests/round*-aborted*.json`. Script đã được sửa để chờ mã mới tối đa 70 phút. Các case Pending là Research Run cần LLM provider (409 MODELS_NOT_CONFIGURED).
- Defect DEF-01 (ST-AD-03): Platform Admin không phải member vẫn đọc được dataset (HTTP 200), do `ProjectAccess.can_read_raw_data` trả True khi `is_admin`. Điều này mâu thuẫn với BR-06 / UC-02 trong [report/03](report/03-software-requirements-specification.md). Cần báo leader.
- Script sinh và dữ liệu ở [deliverables/tests/](deliverables/tests/). Không sửa BRD/PRD/Use Case Spec, vì đây là artifact kiểm thử.
- Validation: render cả hai workbook bằng LibreOffice, kiểm tra công thức thống kê ra 48/1/9/58 và 139 case.
## 2026-10-30 — Khôi phục State Diagram Data Management

- Theo yêu cầu mới, [tab Data Management](diagrams/09-state-machine/03-Data-Management.png) mô tả vòng đời một Local Node pairing với project: Unpaired, Paired online, Paired offline, Revoked. Nguồn UC-08/31 và FR-85/87/110/241/242; state là nhãn khái niệm, không khẳng định enum triển khai. Revocation từ online/offline chặn local jobs, nêu lý do và giữ published objects readable; final chỉ kết thúc pairing hiện tại, không tự thêm re-pairing.
- Khôi phục reason node_offline và hai transition local job blocked/Node reconnects trong [Run](diagrams/09-state-machine/04-Research-Run-Orchestration.png). Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), [editable](diagrams/09-state-machine/State-Machine-Diagrams.drawio), [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md), [review](diagrams/09-state-machine/State-Machine-Diagrams-review.md), [inventory](diagrams/README.md), ghi chú [Report IV](report/04-software-design-document.md#312-local-node-fe-12) và [Class](diagrams/07-class/Class-Diagrams-design.md). Giữ nguyên thiết kế Class editable. Đây là khôi phục view thiết kế của requirement đã có; BRD/PRD/Use Case Spec không thay đổi, không xác nhận chức năng Local Node đã triển khai.
- Validation: builder và kiểm tra tái tạo, graph/state/transition; validator `--strict --score` đạt 0 errors/0 warnings, score 0. Export lại hai tab thay đổi scale 2/border 20, mở xem cả hai PNG. Kiểm tra link nội bộ mới và git diff --check; doclint tài liệu State đạt 0 errors/4 warnings đường dẫn trong văn bản. Chưa kiểm chứng backend, runtime hoặc in/chèn Word; không commit/push.

## 2026-10-30 — Hiệu chỉnh State Diagram sau review

- Sửa [builder](diagrams/09-state-machine/build_state_diagrams.py) để giữ transition-spec trước relabel/style; khôi phục guard và effect AI PI, metadata confirm/overturn; nhánh kết thúc Run hiển thị result, Dossier export có effect export/audit.
- Research Engines dùng event revision checks completed sau khi có kết quả, guard và bộ đếm tối đa hai vòng revision theo IV 3.11; ghi rõ Under review bao gồm revision work. Làm rõ phạm vi một version và Stale giữ lịch sử, không tự refresh; không thêm transition phục hồi chưa chốt. Retry email ghi proposed, không dùng integration_deliveries để khẳng định email retry. Monitoring bỏ choice chỉ đọc status, nối trực tiếp Active → Resolved bằng resolution reported.
- Đồng bộ [editable tám tab](diagrams/09-state-machine/State-Machine-Diagrams.drawio), tám PNG, [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md), [trạng thái xử lý review](diagrams/09-state-machine/State-Machine-Diagrams-review.md#trạng-thái-sau-hiệu-chỉnh). Các thay đổi làm rõ thiết kế theo requirement hiện có, không đổi scope/actor/business rule nên không sửa BRD/PRD/Use Case Spec. Giữ các thay đổi Class/report/inventory có sẵn; Authentication không đổi model.
- Validation: builder chạy và tái tạo byte-identical; validator `--strict --score`: 0 errors/0 warnings, score 0. Kiểm tra graph/guard/effect, 8 tab/83 transition và final không outgoing. Export tám PNG scale 2/border 20 bằng draw.io CLI; mở xem sáu tab thay đổi. Doclint ba tài liệu: 0 errors/4 warnings đường dẫn trong văn bản; link nội bộ mới và `git diff --check` đạt. Quét toàn changelog phát hiện ba link cũ hỏng ngoài phạm vi: diagrams/11-optional/System-Context-Diagram.drawio, diagrams/11-optional/AI-Research-Experimentation-Platform-Use-Case.drawio và docs/example/SWP490_R2_Huong-dan-chuan-bi-Review-2_1.pdf; giữ nguyên và ghi nhận. Không kiểm chứng backend/runtime hoặc in A4/chèn Word; không commit/push.

## 2026-10-30 — Review học thuật bộ State Diagram

- Thêm [bản review State Diagram](diagrams/09-state-machine/State-Machine-Diagrams-review.md) theo góc nhìn giảng viên kỹ thuật phần mềm: ưu tiên lỗi mất guard/effect AI PI khi rút gọn nhãn, review loop chưa thể hiện giới hạn revision, identity/phục hồi sau Stale, cách trình bày reason/result Run và transition email retry còn là đề xuất.
- Chỉ bổ sung nhận xét và kế hoạch sửa; chưa thay đổi requirement, builder, editable hoặc PNG nên không sửa BRD/PRD/Use Case Spec và không chạy generator ghi đè artifact. Giữ nguyên thay đổi có sẵn.
- Validation: mở xem tám PNG hiện có; validator file chung `--strict --score` đạt 0 errors/0 warnings, score 0; kiểm tra trực tiếp XML 8 tab/85 transition và metadata AI PI. Kiểm tra link nội bộ mới và `git diff --check`; chưa kiểm chứng runtime, test case, đồng bộ pixel PNG/XML hoặc in/chèn Word. Nguồn ký pháp: [draw.io](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/).

## 2026-10-30 — Sửa phạm vi Local Node, điểm kết thúc và nhánh Stale

- Theo xác nhận của người dùng, Local Node chưa triển khai: [bộ State Diagram](diagrams/09-state-machine/State-Machine-Diagrams.drawio) giữ tám tab nhóm nhưng Data Management chỉ có ghi chú phạm vi; bỏ lifecycle Local Node và hai transition node_offline của Run, giữ decision/budget_review. Không bịa lifecycle thay thế. [Report IV](report/04-software-design-document.md#312-local-node-fe-12) và [thuyết minh Class](diagrams/07-class/Class-Diagrams-design.md) ghi rõ Local Node là thiết kế dự kiến; không tái sinh editable Class hoặc ghi đè các sửa đổi Class đang có. Đây là thu hẹp view theo phạm vi triển khai được người dùng xác nhận, không xóa requirement dự kiến trong BRD/PRD/Use Case Spec.
- Thêm completion tới final cho Archived, Superseded, sáu kết quả Decision Item, Sent/Skipped và Resolved alert. Mỗi nhánh có final riêng để tránh đường gom dài; lịch sử vẫn lưu. Không gắn final cho Stale/Accepted/Locked hoặc Failed vì còn invalidation/rework/retry. Giữ hai final Auth/Run.
- Đối chiếu IV 3.4.3 xác nhận mọi state object có thể stale; giữ bảy mũi tên độc lập tới một Stale, đổi năm đường gấp thành fan thẳng có thứ tự, giữ hai hành lang ngoài. Không có thân chung/junction hoặc state trùng. Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), tám PNG, [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md) và [inventory](diagrams/README.md#09-state-machine). Ký pháp đối chiếu [draw.io](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/) và [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/about-state-diagrams/).
- Validation: tám tab, 85 transition, 13 final không outgoing; Data Management không có state/transition; Run chỉ hai waiting reason; Object giữ bảy nhánh vào Stale. Repeat-build byte-identical editable/thuyết minh. Validator strict/score: 0 errors, 0 warnings, score 0; export tám PNG và xem contact sheet, mở riêng Object. Doclint bốn file State/rule/inventory/Report IV: 0 errors, 2 warnings đường dẫn builder. Thuyết minh Class có 3 lỗi tên cũ và 3 warnings trong nội dung có sẵn ngoài đoạn ghi chú mới; không sửa phần đó. Link entry mới và git diff --check đạt. Chưa kiểm tra runtime, A4 hoặc Word; không stage/commit/push.

## 2026-10-30 — Sửa nhãn Final trong bảng thuyết minh State Diagram

- Khi giải thích luồng cho người dùng, phát hiện formatter ghi mọi node tròn không nhãn là Initial. Sửa [builder](diagrams/09-state-machine/build_state_diagrams.py) và regenerate [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md): Ended → Final, không phải quay về Initial. Không đổi graph, geometry hoặc nghiệp vụ nên không sửa BRD/PRD/Use Case Spec.
- Validation: editable byte-identical trước/sau; kiểm tra bảng có Ended → Final và không còn Ended → Initial. Doclint thuyết minh: 0 errors/2 warnings đường dẫn builder; link entry mới và git diff --check đạt. Không cần export lại ảnh vì graph không đổi; không stage/commit/push.

## 2026-10-30 — Tham khảo hình State Diagram của report FI2M

- Đọc file mẫu `C:/Users/ADMIN/Downloads/Copy of 9927_HCM_SU26SE109_GSU41_HCM_GSU26SE41_FI2M_Report7_Final_Project_Report.docx.md`, giải mã và mở nguyên bản 12 ảnh State Diagram nhúng base64. [Bảng tham khảo](diagrams/09-state-machine/State-Machine-Diagrams-design.md#report-mẫu-tham-khảo-hình) ghi image ID/caption, SHA-256 và phạm vi áp dụng. Mẫu có cả lifecycle entity (Account/Audit/Maintenance/Disposal) và flow chức năng (Venue/Booking); dùng ảnh để chọn cách trình bày, không nhập nghiệp vụ thiết bị/venue hoặc lỗi caption/ảnh cắt của mẫu.
- Áp dụng profile compact chung: state/spacing gọn hơn, Arial state 12/transition 11, nhãn bằng lời như User cancels/Node reconnects/All stages accepted; chuyển toàn bộ nhánh stale thành đường vuông góc có hành lang riêng. Run giữ ba state, ba reason/bốn result và chín nhánh kết thúc; bỏ ô context kỹ thuật khỏi ảnh nhưng giữ field và trigger/guard/effect đầy đủ trong transition-spec/bảng nguồn. Không giảm transition hoặc đổi source/target để làm hình gọn.
- Đồng bộ [builder chung](diagrams/09-state-machine/build_state_diagrams.py), [builder Auth](diagrams/09-state-machine/build_email_code_state.py), [file tám tab](diagrams/09-state-machine/State-Machine-Diagrams.drawio), standalone Auth, chín PNG, [rule](diagrams/09-state-machine/rule.md) và [ghi chú Auth](diagrams/09-state-machine/Sign-In-With-Email-Code-design.md). Hai builder dùng chung profile, áp dụng idempotent tránh scale hai lần. Không đổi requirement/actor/business flow nên không sửa BRD/PRD/Use Case Spec hoặc Word; giữ thay đổi Class của người dùng.
- Validation: tám tên/thứ tự tab khớp Class; 83 transition/9 initial/2 final/8 choice có predicate, không mất state/nhánh Run/Object, không frame/composite/junction hoặc state lặp; các nhãn rút gọn giữ transition-spec đầy đủ. Builder tái tạo byte-identical model/inventory, standalone Auth khớp tab đầu. Validator `--strict --score` file chung và standalone: 0 errors/0 warnings, score 0. Export chín PNG scale 2/border 20 nền trắng; mở riêng Project/Run/Object và xem contact sheet tám tab sau áp dụng profile, kiểm tra lại nhãn stale cuối. Doclint bốn file rule/inventory/thuyết minh: 0 errors/3 warnings đường dẫn builder; link entry mới và `git diff --check` đạt. Chưa kiểm tra in A4/chèn Word hoặc runtime; không stage/commit/push.

## 2026-10-30 — Rà ký pháp và guard theo hai hướng dẫn UML

- Đối chiếu [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/about-state-diagrams/) và [draw.io](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/); bổ sung [bảng review và ánh xạ guard](diagrams/09-state-machine/State-Machine-Diagrams-design.md#review-uml-theo-hai-hướng-dẫn). Phân biệt yêu cầu UML với profile người dùng (tám tab, câu hỏi trong choice, trái/phải, không frame/composite/junction).
- Chuẩn hóa tám choice: nhãn [Yes]/[No] là tên ngắn của guard, có guard-expression boolean và bảng predicate, không phải trigger mới ở đường ra choice. Bổ sung guard Run trên ảnh; field reason/result chuyển sang UML comment với nét đứt không mũi tên, tên state thuần. AI PI dùng event userDecisionSubmitted trước choice confirm/overturn; email dùng dispatchRequested/deliveryResultReceived. Không để choice làm nơi chờ user/event.
- Đồng bộ [builder chung](diagrams/09-state-machine/build_state_diagrams.py), [builder Auth](diagrams/09-state-machine/build_email_code_state.py), [file tám tab](diagrams/09-state-machine/State-Machine-Diagrams.drawio), standalone Auth, chín PNG, [rule](diagrams/09-state-machine/rule.md), [ghi chú Auth](diagrams/09-state-machine/Sign-In-With-Email-Code-design.md) và [inventory](diagrams/README.md#09-state-machine). Auth giữ geometry/state/flow, chỉ chuẩn hóa guard. Không đổi requirement/actor/flow nghiệp vụ nên không sửa BRD/PRD/Use Case Spec hoặc Word; không chạm thay đổi Class của người dùng.
- Validation: audit tám tab/83 transition nét liền, chín initial đúng bậc vào/ra và không guard/trigger trên đường khởi tạo, hai final không outgoing, tám choice có predicate riêng; graph reachable và state không lặp. Hai comment link là nét đứt/không mũi tên và được loại khỏi transition audit. Builder tái tạo byte-identical editable/inventory; standalone và tab Auth khớp model. Validator `--strict --score` của file chung/standalone: 0 errors/0 warnings, score 0. Xuất chín PNG scale 2/border 20, xem ảnh Auth/Run/AI PI và contact sheet; tăng khoảng cách nhãn Run và xem lại sau sửa cuối. Doclint bốn file rule/inventory/thuyết minh: 0 errors/3 warnings đường dẫn builder; link entry mới và `git diff --check` đạt. Đây là review ký pháp/ngữ nghĩa thiết kế và kiểm tra cấu trúc/ảnh, không phải chứng nhận formal UML hoặc runtime test; các lifecycle đề xuất từ schema vẫn ghi rõ giới hạn nguồn. Không stage/commit/push.

## 2026-10-30 — Chuẩn hóa State Diagram thành vòng đời UML liền mạch

- Sửa [bộ tám tab](diagrams/09-state-machine/State-Machine-Diagrams.drawio) theo phản hồi người dùng: bỏ toàn bộ state bản sao và các cụm sự kiện rời; một state chỉ xuất hiện một lần trong cùng vòng đời, mọi state có đường tới từ initial. Giữ tám nhóm theo Class, không thêm frame ngoài/composite/junction.
- Research Run dùng ba state Running/Waiting/Ended theo FR-21 và RunState của Class; ba waiting reason và bốn ending result là field, không nhân thành state mới. Tách từng transition có trigger/guard/effect rõ và gán reason/result; Ended completion tới final, không hàm ý xóa record. Hand-off Object có một Stale duy nhất và đủ bảy transition trực tiếp từ các state áp dụng. Các đường chuyển trạng thái là nét liền, mũi tên mở; event/effect là nhãn thiết kế, không khẳng định tên API/event implementation.
- Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), tám PNG, [nguồn/transition mapping](diagrams/09-state-machine/State-Machine-Diagrams-design.md), [rule](diagrams/09-state-machine/rule.md) và [inventory](diagrams/README.md#09-state-machine). Đối chiếu [draw.io UML state machine](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/). Không đổi requirement/actor/business flow nên không sửa BRD/PRD/Use Case Spec hoặc Word; giữ nguyên model Auth đã duyệt và các thay đổi Class của người dùng.
- Validation: audit tám tên/thứ tự tab khớp Class, 83 transition; state không lặp, reachability theo cell thật không cần coalesce alias; final không có outgoing, không dashed transition hoặc chấm gom nhỏ. Run có đúng ba state/ba reason/bốn result/chín transition riêng vào Ended; Object có một Stale/bảy source. Model Auth giữ nguyên; TC reference tồn tại trong Report7. Builder tái tạo byte-identical editable/inventory. Validator `--strict --score`: 0 errors/0 warnings, score 0; export đủ tám PNG scale 2/border 20, mở riêng Run/Object và xem contact sheet cuối. Doclint ba file rule/inventory/thuyết minh: 0 errors/2 warnings đường dẫn builder; link entry mới và `git diff --check` đạt. Đây là kiểm tra cấu trúc, truy vết và ảnh, không phải chứng nhận formal UML hoặc runtime test; chưa kiểm tra in A4/chèn Word, không stage/commit/push.

## 2026-10-30 — State Diagram nối trực tiếp, bỏ chấm gom nhỏ

- Theo phản hồi người dùng, sửa [bộ tám tab](diagrams/09-state-machine/State-Machine-Diagrams.drawio): không còn junction/chấm gom nhỏ, khối lồng hoặc nhãn end event. Local Node, Dossier và Decision Item nối thẳng từ trạng thái nguồn đến đích. Run bỏ chuỗi câu hỏi phân loại kết thúc; mỗi mũi tên ghi sự kiện cụ thể.
- Tách các nhánh dùng chung của Run và Hand-off Object thành cụm tình huống có tiêu đề trong cùng tab; lặp lại state nguồn để đọc đường đi trực tiếp, có model-state ánh xạ về cùng một trạng thái nghiệp vụ. Nhãn như Waiting for Local Node, Under review, Ready for acceptance thay các code khó đọc; code nguồn và điều kiện/effect giữ trong [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md).
- Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), năm PNG bị ảnh hưởng, [rule](diagrams/09-state-machine/rule.md) và [inventory](diagrams/README.md#09-state-machine). Không thay requirement/actor/business flow nên không sửa BRD/PRD/Use Case Spec hoặc Word; giữ nguyên bản Authentication đã duyệt và các thay đổi Class Diagram của người dùng.
- Validation: audit tám tên/thứ tự tab khớp Class, model Auth giữ nguyên, 86 transition/8 choice Yes-No; không có vertex chấm nhỏ, frame/composite hoặc nhãn end event. Kiểm tra reachability theo model-state, đủ tám state Run và 13 nhánh kết thúc trực tiếp, đủ bảy nhánh object → stale; TC reference tồn tại trong nguồn. Builder tái tạo byte-identical editable/inventory; validator `--strict --score`: 0 errors/0 warnings, score 0. Export lại năm PNG scale 2/border 20 và mở xem; nhãn Run được kiểm tra lại sau sửa cuối. Doclint rule/inventory/thuyết minh: 0 errors/2 warnings đường dẫn builder; link entry mới và `git diff --check` đạt. Chưa kiểm chứng runtime, in A4 hoặc chèn Word; không stage/commit/push.

## 2026-10-30 — State Diagram theo tám nhóm, bỏ khối lồng

- Theo phản hồi người dùng, sửa [file chung](diagrams/09-state-machine/State-Machine-Diagrams.drawio) từ bảy tab theo entity sang tám tab đúng tên/thứ tự nhóm Class Diagram. Người dùng chọn giữ đầy đủ trạng thái và nhánh, bỏ khối lồng và rút ngắn nhãn. Authentication giữ nguyên model đã duyệt; Project và Dossier là hai vòng đời độc lập trong tab Project Workspace, Hand-off Object nằm ở Research Engines; sáu placeholder entity vẫn đủ.
- Trải phẳng toàn bộ composite, dùng junction nhỏ gom các đường end/stale/revocation có cùng nghĩa; các điều kiện/effect dài giữ trong metadata và [thuyết minh](diagrams/09-state-machine/State-Machine-Diagrams-design.md). Bổ sung Notifications & Integrations và Administration & Monitoring từ status schema/hành vi Report7; các transition suy ra còn là đề xuất, không khẳng định enum đủ chứng minh transition triển khai.
- Đồng bộ [builder](diagrams/09-state-machine/build_state_diagrams.py), tám PNG nhóm, [rule](diagrams/09-state-machine/rule.md) và [inventory](diagrams/README.md#09-state-machine). Không đổi BRD/PRD/Use Case Spec hoặc placeholder Word; đây là thay cách chia view và trình bày, không chốt thêm nghiệp vụ triển khai. Giữ thay đổi Class Diagram đang có của người dùng.
- Validation: tên/thứ tự 8 tab khớp Class Diagram; model Authentication giữ nguyên; 97 transition/11 choice có câu hỏi và Yes-No; mọi state có đường tới, không còn frame/composite. Kiểm tra đủ tám leaf state của Run, tám state Object và bảy nhánh stale, revocation từ cả hai state Node. Metadata source/test đầy đủ, TC ID tồn tại trong Report7. Builder tái tạo byte-identical editable/inventory; validator `--strict --score`: 0 errors/0 warnings, score 0. Xuất và mở xem tám PNG scale 2/border 20 nền trắng; thay bảy PNG cũ theo entity bằng tám PNG nhóm, giữ standalone Authentication đã duyệt. Doclint rule/inventory/thuyết minh: 0 errors/2 warnings đường dẫn builder; link entry mới và `git diff --check` đạt. Không kiểm chứng runtime, in A4/chèn Word; không stage/commit/push.

## 2026-10-30 — Bộ State Diagram chung bảy tab theo Report7

- Tạo [file draw.io chung](diagrams/09-state-machine/State-Machine-Diagrams.drawio) có bảy tab: Sign In With Email Code đã duyệt, Project, Local Node, Research Run, Hand-off Object, Dossier, Decision Item. Phủ đủ sáu placeholder State Machine của `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`; không tự thêm lifecycle cho các nhóm report ghi không có main entity. Bản Authentication standalone được giữ làm nguồn đã duyệt.
- Thêm [builder](diagrams/09-state-machine/build_state_diagrams.py), bảy PNG theo [inventory/nguồn/truy vết từng transition](diagrams/09-state-machine/State-Machine-Diagrams-design.md). Đồng bộ [rule](diagrams/09-state-machine/rule.md), [inventory chung](diagrams/README.md#09-state-machine) và [ghi chú bản thử](diagrams/09-state-machine/Sign-In-With-Email-Code-design.md). Mỗi diagram là một tab trong file chung; không có frame `stm`, choice có câu hỏi/Yes-No, nhãn trên đường nối nền trắng. Composite state gom transition nghiệp vụ áp dụng chung cho state con, không phải frame trang.
- Run có đủ ba waiting reason/bốn ended outcome; Hand-off Object có checks/review/acceptance/lock/stale; Dossier theo từng version, approvals không mang sang version mới; Decision Item phân biệt human answer, tentative confirm/overturn, pinned/spending timeout và đóng pending item khi cancel run. Các nhãn Project/Node/Decision Item suy ra từ mô tả hành vi được nêu rõ là thiết kế khái niệm, không khẳng định enum implementation.
- Không đổi requirement/actor/business rule hoặc flow sản phẩm nên không sửa BRD/PRD/Use Case Spec; chưa thay placeholder/chèn PNG vào Word. Không thêm reopen/restore/retry terminal state khi report chưa định nghĩa.
- Validation: builder tái tạo byte-identical cả editable/inventory; audit phủ 6/6 placeholder + Authentication, 7 tab/60 transition/5 choice có câu hỏi và Yes-No hai bên; model Authentication giữ nguyên bản đã duyệt, từng transition mới có source/test reference và các TC ID tồn tại trong nguồn. Validator `--strict --score`: 0 errors/0 warnings, score 0. Xuất đủ bảy PNG scale 2/border 20/nền trắng bằng draw.io CLI, mở từng diagram và xem contact sheet sau export cuối; sửa route/label ở Hand-off Object và Decision Item. Doclint bốn file rule/inventory/thuyết minh: 0 errors/3 warnings đường dẫn builder. Link trong entry mới và `git diff --check` đạt. Chưa kiểm tra runtime, in A4 hoặc chèn Word; test reference không phải kết quả thực thi. Không stage/commit/push.

## 2026-10-30 — Bỏ khung ngoài State Diagram

- Bỏ frame và tiêu đề `stm` ngoài cùng theo yêu cầu người dùng; giữ graph, nội dung và bố cục tương đối. Đồng bộ [builder](diagrams/09-state-machine/build_email_code_state.py), editable (đã loại khỏi bộ hiện hành), PNG (đã loại khỏi bộ hiện hành), [rule](diagrams/09-state-machine/rule.md) và [thuyết minh](diagrams/09-state-machine/Sign-In-With-Email-Code-design.md).
- Chỉ chỉnh trình bày, không đổi nghiệp vụ nên không sửa BRD/PRD/Use Case Spec. Validation: regenerate; validator `--strict --score`: 0 errors/0 warnings, score 0; export PNG scale 2/border 20 và đã xem trực quan. Doclint rule/thuyết minh: 0 errors, 1 warning đường dẫn builder; `git diff --check` sạch.

## 2026-10-30 — Đặt nhãn State Diagram trên đường mũi tên

- Theo yêu cầu người dùng, đặt text transition (gồm Yes/No) trực tiếp trên đường nối, dùng nền trắng phía sau chữ; giữ node và hướng nhánh. Đồng bộ [builder](diagrams/09-state-machine/build_email_code_state.py), editable (đã loại khỏi bộ hiện hành), PNG (đã loại khỏi bộ hiện hành), [rule](diagrams/09-state-machine/rule.md) và [thuyết minh](diagrams/09-state-machine/Sign-In-With-Email-Code-design.md).
- Chỉ chỉnh vị trí nhãn, không đổi nghiệp vụ nên không sửa BRD/PRD/Use Case Spec. Validation: regenerate; validator `--strict --score`: 0 errors/0 warnings, score 0; PNG scale 2/border 20 đã export và xem trực quan. Doclint rule/thuyết minh: 0 errors, 1 warning đường dẫn builder; `git diff --check` sạch.

## 2026-10-30 — Chốt hình thoi có câu hỏi và nhánh Yes/No

- Theo yêu cầu người dùng, sửa [rule State Diagram](diagrams/09-state-machine/rule.md): câu hỏi bắt buộc nằm trong hình thoi, hai nhánh `No`/`Yes` tách trái/phải; bỏ hướng dẫn cũ thay Yes/No bằng guard bên ngoài.
- Đồng bộ [builder bản thử](diagrams/09-state-machine/build_email_code_state.py), editable (đã loại khỏi bộ hiện hành), PNG (đã loại khỏi bộ hiện hành) và [thuyết minh](diagrams/09-state-machine/Sign-In-With-Email-Code-design.md). Câu hỏi là `Is code correct and unexpired?`; No quay lại chờ mã, Yes sang Signed in. Effect được giải thích trong thuyết minh để nhãn nhánh gọn như mẫu.
- Chỉ đổi quy ước trình bày, không đổi điều kiện hoặc nghiệp vụ nên không sửa BRD/PRD/Use Case Spec. Validation: regenerate; validator `--strict --score`: 0 errors/0 warnings, score 0; xuất PNG scale 2/border 20 và kiểm tra trực quan; doclint và `git diff --check` kiểm tra sau lần sửa cuối.

## 2026-10-30 — Vẽ thử State Diagram Sign In With Email Code

- Thêm editable (đã loại khỏi bộ hiện hành), PNG (đã loại khỏi bộ hiện hành), [builder](diagrams/09-state-machine/build_email_code_state.py) và [thuyết minh/truy vết](diagrams/09-state-machine/Sign-In-With-Email-Code-design.md), cập nhật [inventory](diagrams/README.md#09-state-machine). Nguồn là Report7 người dùng gửi, III §3.2.1 và IV §3.1/§2.2.4.
- Bản thử mô hình hóa một lần đăng nhập: Signed out → Awaiting email code → choice mã đúng/chưa hết hạn → Signed in → final. Mã sai/hết hạn quay lại chờ mã; account tạo lần đầu nằm trong effect resolve account. Final chỉ kết thúc lần đăng nhập, không đóng session. Nhãn state là thiết kế khái niệm từ mô tả report, không xác nhận enum triển khai.
- Không đổi requirement hoặc flow nghiệp vụ nên không sửa BRD/PRD/Use Case Spec; chưa thay placeholder/chèn ảnh vào report. Google, sign-out, session expiry và resend ngoài phạm vi bản thử.
- Validation: builder chạy; validator `--strict --score` đạt 0 errors/0 warnings, score 0; export PNG scale 2/border 20 nền trắng và xem trực quan. Builder tái tạo byte-identical; lint thuyết minh/inventory/rule: 0 errors, 1 warning do link builder là đường dẫn source. Link entry mới hợp lệ; `git diff --check` sạch. Không kiểm tra runtime hoặc in A4.

## 2026-10-30 — Dọn khối thừa trong IV 3.4 Research Run Orchestration

- Xoá trong [Report 7 docx](deliverables/FA26SE115_Report7.docx) khối nội dung cũ nằm giữa tiêu đề 3.4 và 3.4.1 Class Diagram: 3.4.1–3.4.3 viewpoint cũ, 3.13 Budget and Cost, 3.14 Dossier, 3.19 Cross-Cutting Behavior cùng Figure IV-5, IV-6, IV-7, IV-12, IV-13. Khối này trùng số với mục 3.4.1 của template SEP490. Bản prod đã được người dùng xoá tương ứng.
- Xoá 5 dòng hình tương ứng trong mục lục. Số trang trong mục lục cần refresh trong Word.
- Không sửa [report/04-software-design-document.md](report/04-software-design-document.md) (khung của leader) và không cần sửa BRD/PRD/Use Case Spec, vì đây là lỗi sắp xếp trong docx.
- Validation: render PDF bằng LibreOffice, kiểm tra 3.4 nối thẳng vào 3.4.1 Class Diagram và không còn caption IV-5/6/7/12/13.

## 2026-10-30 — Cập nhật rule State Machine Diagram

- Cập nhật [rule state machine](diagrams/09-state-machine/rule.md) theo [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/about-state-diagrams/), [draw.io](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/) và ảnh mẫu người dùng: bố cục dọc đen trắng, nhánh hai bên, phân biệt state với action/flowchart, trigger/guard/effect và choice.
- Sửa các ràng buộc cũ quá cứng: không bắt buộc final cho mọi vòng đời, không cấm fork/join hợp lệ, cho phép completion transition thiếu trigger, không ép event thì quá khứ hoặc effect theo tên code. Làm rõ initial/final, composite, mapping FR/test và kiểm tra ngữ nghĩa cùng ảnh export.
- Chỉ thay hướng dẫn vẽ và changelog; không đổi requirement, actor, rule nghiệp vụ hoặc flow sản phẩm nên không cần sửa BRD/PRD/Use Case Spec. Folder state machine hiện chỉ có rule, chưa có builder/editable/PNG cần regenerate.
- Validation: đối chiếu hai nguồn và bảng state Research Run/Hand-off Object trong [Software Design Document](report/04-software-design-document.md#342-state-viewpoint-run-state-machine); `python -I tools/doclint.py diagrams/09-state-machine/rule.md`: 0 errors/0 warnings; `git diff --check` sạch. Lint toàn bộ changelog còn 37 lỗi lịch sử (tên đã bỏ/link cũ), đã đối chiếu HEAD: không thêm lỗi mới; link trong entry mới hợp lệ. Không có thay đổi diagram để chạy render/validator.

## 2026-10-30 — Bổ sung Repository trong toàn bộ Sequence Diagram

- Theo yêu cầu người dùng, thêm một Repository giữa Service và Database trong 64 tab của tám file chính và bản Email Code standalone. Mỗi request dữ liệu có call Service → Repository → Database và reply ngược lại; không còn Service gọi trực tiếp Database. Tên Repository theo trách nhiệm service của từng page.
- Đồng bộ [builder chung](diagrams/08-sequence/build_sequence_groups.py), [định nghĩa flow](diagrams/08-sequence/sequence_flows.py), [builder Email Code](diagrams/08-sequence/build_sign_in_with_email_code.py), editable và PNG theo [inventory](diagrams/08-sequence/Sequence-Groups-design.md). Email Code dùng chung renderer/flow với tab đầu Authentication để tránh hai bản lệch nhau; luồng gửi mã, xác minh, tạo account lần đầu và mở session được giữ.
- Cập nhật [rule](diagrams/08-sequence/rule.md), [thuyết minh Email Code](diagrams/08-sequence/Sign-In-With-Email-Code-design.md) và [inventory chung](diagrams/README.md#08-sequence). Đây là bổ sung tầng thiết kế sequence, không đổi nghiệp vụ nên không sửa BRD/PRD/Use Case Spec; không sửa BE hoặc Class Diagram.
- Validation: regenerate đủ tám file/64 tab và standalone; kiểm tra từng page có đúng một Repository, mọi Database call/reply đi qua Repository, model Email Code standalone khớp tab đầu. Validator `--strict --score` trên chín file: 0 errors, 0 warnings, score 0. Xuất lại 65 PNG, xem contact sheet toàn bộ tab và mở riêng trang phức tạp. Bốn PNG dài (Local Job, Hypothesis, Independent Review, Execution) bị native exporter cắt cuối ở scale 2, đã xuất scale 1 và kiểm tra có đủ message cuối; các PNG còn lại scale 2, cùng border 20/nền trắng. `python -I tools/doclint.py`, link local và `git diff --check` đạt; không stage/commit/push.

## 2026-10-30 — Bộ Sequence Diagram theo tám nhóm chức năng

- Tạo tám folder, mỗi folder một file draw.io chính, mỗi sequence là một tab: [Authentication & Account](diagrams/08-sequence/01-authentication-account/Sequence-Diagrams-Authentication-Account.drawio) (5), [Project Workspace](diagrams/08-sequence/02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) (12), [Data Management](diagrams/08-sequence/03-data-management/Sequence-Diagrams-Data-Management.drawio) (10), [Research Run Orchestration](diagrams/08-sequence/04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) (13), [Research Engines](diagrams/08-sequence/05-research-engines/Sequence-Diagrams-Research-Engines.drawio) (6), [AI Principal Investigator](diagrams/08-sequence/06-ai-principal-investigator/Sequence-Diagrams-AI-Principal-Investigator.drawio) (5), [Notifications & Integrations](diagrams/08-sequence/07-notifications-integrations/Sequence-Diagrams-Notifications-Integrations.drawio) (4), [Administration & Monitoring](diagrams/08-sequence/08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) (9).
- Nguồn là `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`, đối chiếu [thiết kế class](diagrams/07-class/Class-Diagrams-design.md). Bộ 64 tab ánh xạ đủ 61 heading sequence ở IV 3.1–3.8, thêm Execution, Paper theo IV 3.5 và Local Job theo IV-12; Lock/Unseal của IV-10 nằm trong hai tab Experiment Design và Execution. [Inventory](diagrams/08-sequence/Sequence-Groups-design.md) có link từng PNG, vị trí nguồn, hash snapshot và ánh xạ caption cũ sang nghiệp vụ hiện hành; không khôi phục v3 flow đã bỏ.
- Thêm [builder](diagrams/08-sequence/build_sequence_groups.py) và [định nghĩa flow](diagrams/08-sequence/sequence_flows.py); cập nhật [rule sequence](diagrams/08-sequence/rule.md), [inventory chung](diagrams/README.md#08-sequence). Authentication đủ năm sequence; tab Email Code giữ nguyên model XML đã duyệt, bản standalone và builder cũ vẫn được giữ.
- Giữ phong cách người dùng chốt: không frame ngoài, nền trắng, tên actor tách chân, call/reply phân biệt, guard có hàng riêng, không activation lồng dài qua opt. Activation phủ đủ các reply thay thế theo cặp caller–callee. Các operation/persistence chưa chốt là đề xuất thiết kế; không tự định nghĩa endpoint hoặc xác nhận runtime. Không đổi requirement BRD/PRD/Use Case Spec hoặc placeholder Report7, nên không cần sửa các tài liệu nghiệp vụ đó.
- Luồng Google gồm mở consent, từ chối hoặc callback, xác minh identity và ánh xạ cùng verified email. Handle Must-Ask và Receive Notifications khởi tạo bởi event hệ thống trong context đã xác thực; user không cần mở UI để backend xử lý, chỉ nhận update khi connected và authorized.
- Validation: tái tạo ổn định tám file và inventory; ánh xạ đủ 61 heading sequence, 64 tab/64 PNG, mỗi folder đúng một draw.io chính; model XML Email Code khớp bản đã duyệt. Validator `--strict --score` trên tám file: 0 errors, 0 warnings, score 0. Xuất PNG từng tab bằng draw.io CLI scale 2/border 20 nền trắng; xem contact sheet của toàn bộ tab và mở riêng các trang có fragment phức tạp, kiểm tra lại hai trang event sau sửa cuối. `python -I tools/doclint.py`: 13 file, 0 errors/0 warnings; link local, whitespace file mới và `git diff --check` đạt. Chưa kiểm tra in A4/chèn Word hoặc runtime; giữ nguyên staged changes đã có, không stage/commit/push.

## 2026-10-29 — Kiến trúc hệ thống và deployment (IV 1.1)

- Vẽ lại [System Architecture Diagram](diagrams/04-system-overview/System-Architecture-Diagram.drawio) theo mẫu layered architecture: các tầng Users, Edge, Production VPS (gồm Application, Data, AI research) và External services, dải CI/CD bên dưới; dùng logo chính thức (Simple Icons), có tiêu đề, phiên bản, legend và line jump. Thay hình IV-1 cùng đoạn mô tả trong S4 và docx.
- Thêm [System Architecture Diagram](diagrams/04-system-overview/System-Architecture-Diagram.drawio) và [Deployment Diagram](diagrams/04-system-overview/Deployment-Diagram-Production.drawio) (UML 2.5: container Docker là node `«executionEnvironment»`, image là `«artifact»`). Nguồn: compose, workflow CI/CD của hai repo sản phẩm và thông tin hạ tầng do team cung cấp (1 Linux VPS + Dokploy, Cloudflare, LLM OpenAI/Gemini/OpenRouter). Theo yêu cầu dọn folder, chỉ giữ hai file `.drawio`; bỏ builder, PNG và các bản nháp Container/Component/CI-CD.
- Viết lại IV 1.1 trong [S4 supplement](deliverables/supplements/S4-design.md) và [Report 7 docx](deliverables/FA26SE115_Report7.docx):
  - Thu gọn từ 3 hình còn 2 hình: IV-1 System Architecture, IV-2 Deployment.
  - Đổi 1.1.4 thành 1.1.3.
  - Lùi số các hình IV phía sau xuống 1, tạo lại mục lục và sửa bảng viewpoint.
  - Không sửa `report/` (leader).
- Ghi nhận các giới hạn hiện tại: một VPS duy nhất, chưa có staging, chưa backup DB, chưa có giám sát bên ngoài.
- Nội dung khác với `report/` 1.1 cần báo leader:
  - Mục 1.1 mới mô tả hệ thống như đang chạy thật.
  - Engine `execution` và `paper` cùng Local Node chỉ được ghi là có trong thiết kế, chưa có trong bản phát hành hiện tại.
- Validation:
  - Builder chạy thành công.
  - Xuất PNG 200%, viền 20 px, kiểm tra bằng mắt không còn đường cắt hộp hay nhãn chồng.
  - Docx render qua LibreOffice; kiểm tra mục lục và các trang 115–119.

## 2026-10-29 — Vẽ thử Sequence Sign In With Email Code

- Chỉnh vùng bước 20–26 bị rối: bỏ activation lồng dài của `resolveUser`, mở rộng khung `opt`, rút gọn guard thành `[account not found]` và tăng khoảng cách trước message tạo tài khoản. Đồng bộ builder/editable/PNG và thuyết minh; regenerate, validator 0 errors/0 warnings, xem lại PNG và `git diff --check` đạt. Không đổi nghiệp vụ.

- Hạ nhãn actor `User` thêm 10 px theo phản hồi; đồng bộ builder/editable/PNG và thuyết minh. Regenerate, validator 0 errors/0 warnings, xuất PNG và kiểm tra trực quan; `git diff --check` đạt. Chỉ chỉnh trình bày, không đổi nghiệp vụ.

- Thêm [sequence editable](diagrams/08-sequence/Sequence-Diagram-Sign-In-With-Email-Code.drawio), [PNG](diagrams/08-sequence/Sequence-Diagram-Sign-In-With-Email-Code.png), [builder](diagrams/08-sequence/build_sign_in_with_email_code.py) và [thuyết minh/nguồn](diagrams/08-sequence/Sign-In-With-Email-Code-design.md) cho ô IV 3.1.2, dựa trên `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md` III 3.2.1 và IV 3.1; đối chiếu [thiết kế Authentication](diagrams/07-class/Authentication-Account-design.md).
- Bao phủ yêu cầu mã email, xác minh mã, `alt` mã sai/hết hạn và thành công, `opt` tạo tài khoản lần đầu, tiêu thụ mã và mở session. Tên operation theo Class Diagram đề xuất; chi tiết persistence là thiết kế khái niệm, không chốt endpoint hoặc cách truyền session. Không thay nghiệp vụ/BRD/PRD/Use Case Spec hoặc placeholder report; không đổi diagram khác.
- Validation: builder chạy thành công; validator cấu trúc 0 errors, 0 warnings, score 0; draw.io CLI xuất PNG zoom 200%, border 20 nền trắng, đã xem trực quan sau lần sửa cuối. `python -I tools/doclint.py` đạt; link local trong thuyết minh và entry này tồn tại; `git diff --check` sạch. Chưa kiểm tra in A4/chèn Word hoặc runtime backend.
- Theo phản hồi tiếp theo: bỏ khung `sd` ngoài cùng và tiêu đề của khung, giữ nguyên `alt`/`opt` và tương tác. Đồng bộ builder, editable, PNG và thuyết minh; regenerate, validator 0 errors/0 warnings, xuất lại PNG và xem trực quan; `git diff --check` đạt. Không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec.

## 2026-10-29 — Điều chỉnh rule Sequence Diagram theo hướng dẫn và ảnh mẫu

- Cập nhật [rule Sequence Diagram](diagrams/08-sequence/rule.md) theo [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-sequence-diagram/), [draw.io](https://www.drawio.com/docs/diagram-types/uml/sequence-diagrams/) và ảnh Admin/Audit Session người dùng gửi: bố cục actor–UI–controller–service–repository–database, call/reply, activation theo lần xử lý, đánh số message, fragment và checklist.
- Làm rõ khung `alt` phải bao cả nhánh lỗi và thành công, reply về caller trực tiếp, tên participant/API phải có nguồn; ảnh chỉ hướng dẫn phong cách. Giữ một file/một sequence và nguyên tắc gộp theo cấu trúc tương đương trong [inventory](diagrams/README.md#08-sequence).
- Phạm vi chỉ là quy tắc mô hình hóa, không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec. Folder `08-sequence` hiện chỉ có rule; không sửa hoặc regenerate diagram/builder, không có render check trong đợt này.
- Validation: đối chiếu hai hướng dẫn và quy tắc chung; `python -I tools/doclint.py` đạt (13 file, 0 errors, 0 warnings); kiểm tra link local trong rule và entry này, `git diff --check` đạt.

## 2026-10-29 — Co kích thước class theo nội dung

- Áp dụng chiều rộng theo tên lớp và thành viên cho cả tám tab trong [file draw.io chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), thay hộp rộng đồng loạt bằng entity/enum gọn và service/controller rộng theo nhu cầu. Đồng bộ [builder chính](diagrams/07-class/build_authentication_account.py), [helper đo Arial/Pillow](diagrams/07-class/class_diagram_pages.py), tám PNG trong [inventory](diagrams/07-class/Class-Diagrams-design.md), [thuyết minh Authentication](diagrams/07-class/Authentication-Account-design.md) và [rule](diagrams/07-class/rule.md). Giữ cỡ chữ, nội dung, tâm cụm và chiều cao theo dòng; cập nhật port/waypoint/nhãn sau đổi chiều rộng.
- Chỉ sửa trình bày nên không cần sửa BRD/PRD/Use Case Spec. Validation: graph 8 tab/98 classifier không đổi nội dung, builder tái tạo ổn định, validator 0 errors/0 warnings (score 0), kiểm tra tuyến/khung ngăn và xuất/xem tám PNG; kiểm tra link mới và `git diff --check`.

## 2026-10-29 — Điều chỉnh sáu Class Diagram còn lại theo cụm

- Thay lưới đều trên sáu tab Project Workspace, Data Management, Research Run Orchestration, AI Principal Investigator, Notifications & Integrations và Administration & Monitoring bằng bố cục riêng theo quan hệ; giữ hướng trái → phải, thu khoảng cách dọc và đặt nhánh hỗ trợ gần lớp sử dụng. Đồng bộ [file editable tám tab](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), [builder](diagrams/07-class/class_diagram_pages.py), sáu PNG và [thuyết minh/inventory](diagrams/07-class/Class-Diagrams-design.md), [rule](diagrams/07-class/rule.md).
- Chỉ đổi trình bày, không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec. Bảo toàn class/thành viên/nhãn/quan hệ của tám tab, giữ nguyên Authentication và Research Engines. Validation: builder tái tạo ổn định, validator 0 errors/0 warnings (score 0), kiểm tra tuyến không xuyên hộp khác, xuất và xem đủ sáu PNG, kiểm tra liên kết và `git diff --check`.

## 2026-10-29 — Bố trí Research Engines theo cụm quan hệ

- Chỉnh riêng tab Research Engines trong [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): thay lưới lặp bằng cụm dữ liệu/giả thuyết, thực thi/review và nhánh Harness–Lock–Envelope; phối hợp quan hệ ngang/dọc với cao độ khác nhau. Nhãn dài xuống dòng trong hành lang. Đồng bộ [builder](diagrams/07-class/class_diagram_pages.py), [PNG](diagrams/07-class/Class-Diagram-Research-Engines.png), [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md).
- Chỉ đổi trình bày, không đổi class/thành viên/quan hệ/nghiệp vụ; không cần sửa BRD/PRD/Use Case Spec. Validation: validator 0 errors/0 warnings, score 0; xuất và xem PNG, kiểm tra graph và bảy tab khác không đổi, builder tái tạo ổn định và `git diff --check`.

## 2026-10-29 — Kéo số sát đường association ngang

- Theo phản hồi, giảm offset dọc của multiplicity ngang từ 22 xuống 10 px trong [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), giữ vị trí gần hai endpoint. Đồng bộ [helper](diagrams/07-class/class_diagram_pages.py), bảy PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md). Chỉ đổi vị trí chữ, không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec.
- Validation: builder, validator 0 errors/0 warnings (score 0), export và xem PNG; bảo toàn nội dung graph, kiểm tra `git diff --check`.

## 2026-10-29 — Đặt multiplicity sát hai đầu association

- Theo phản hồi, đưa số về gần hai đầu nối trong [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): tâm số cách endpoint 20 px thay vì 38 px, vẫn nằm ngoài hộp. Giữ số dọc sát trái đường và tên quan hệ bên phải; không đổi nội dung hoặc quan hệ. Đồng bộ [helper](diagrams/07-class/class_diagram_pages.py), bảy PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md). Không đổi nghiệp vụ nên không sửa BRD/PRD/Use Case Spec.
- Validation: builder, validator 0 errors/0 warnings (score 0), export/xem các PNG bị ảnh hưởng và kiểm tra `git diff --check`.

## 2026-10-29 — Đưa multiplicity sát cạnh đường nối

- Điều chỉnh [Class Diagram chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): multiplicity dọc lệch trái 20 px thay vì 76 px, giữ cách endpoint 38 px; tên association chuyển sang bên phải đường để không chạm số. Đồng bộ [helper](diagrams/07-class/class_diagram_pages.py), bốn PNG bị ảnh hưởng, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md). Không đổi class/quan hệ/nghiệp vụ nên không sửa BRD/PRD/Use Case Spec.
- Validation: builder, validator 0 errors/0 warnings (score 0), export và xem PNG; bảo toàn nội dung tám tab và `git diff --check`.

## 2026-10-29 — Tách chữ khỏi viền entity và class trung gian

- Sửa vị trí multiplicity trên toàn bộ association trong [file Class Diagram chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): cách endpoint 38 px, lệch khỏi đường để không đè viền/stereotype hoặc nhãn giữa đường. Dịch `checks access` sang ngoài tuyến vòng bên trái, tránh AccountService. Giữ nguyên nội dung, class và tuyến đường; đồng bộ [builder Authentication](diagrams/07-class/build_authentication_account.py), [helper nhãn](diagrams/07-class/class_diagram_pages.py), bảy PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md).
- Chỉ sửa trình bày nên không cần cập nhật BRD/PRD/Use Case Spec. Validation: builder tái tạo, bảo toàn graph tám tab/98 classifier, validator 0 errors/0 warnings (score 0), export/xem các PNG bị ảnh hưởng và `git diff --check`.

## 2026-10-29 — Tách nhãn quan hệ khỏi các đường song song

- Sửa nhãn controller trên sáu tab trong [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): đặt phía trên đoạn ngang cuối trước class đích, giới hạn 130 px và xuống dòng; không đặt chữ giữa hai đường dọc gần nhau. Giữ nguyên nội dung nhãn, class và quan hệ. Đồng bộ [builder/layout](diagrams/07-class/class_diagram_pages.py), sáu PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md); không đổi nghiệp vụ nên không sửa BRD/PRD/Use Case Spec.
- Validation: builder tái tạo, validator 0 errors/0 warnings (score 0); xuất lại và xem PNG, kiểm tra bảo toàn graph tám tab và `git diff --check`.

## 2026-10-29 — Gom gọn Class Diagram theo chiều trái → phải

- Theo phản hồi mới nhất, bỏ bố cục tỏa bốn phía trên sáu tab; trở về thứ tự controller → service → entity/enum. Controller ở cột trái, căn giữa nhóm service theo chiều dọc; hàng/cột gần nhau hơn, đường chia nhánh ngắn lên/xuống để hạn chế song song dài và khoảng rỗng. Đồng bộ [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), [builder/layout](diagrams/07-class/class_diagram_pages.py), sáu PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md).
- Chỉ đổi bố cục, giữ toàn bộ class/thành viên/nhãn/quan hệ; không đổi requirement nên không cần sửa BRD/PRD/Use Case Spec. Validation: builder tái tạo, so sánh graph tám tab, validator 0 errors/0 warnings (score 0), export và xem sáu PNG; kiểm tra link và `git diff --check`.

## 2026-10-29 — Đặt class nhiều kết nối vào giữa cụm

- Theo phản hồi người dùng, bố trí lại sáu tab trong [file Class Diagram chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): controller ở giữa, chia nhánh lên/xuống và trái/phải, service/entity gần nhau; tách port để tránh dải đường song song hoặc đi chung đoạn. Authentication và Research Engines giữ nguyên bố cục. Đồng bộ [source layout](diagrams/07-class/class_diagram_pages.py), sáu PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md).
- Không đổi class, thành viên, loại/chiều quan hệ hoặc nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec. Validation: so sánh ID/value/source/target trước–sau cho cả tám tab; builder tái tạo; validator 0 errors/0 warnings, score 0; PNG đã export và xem trực quan; `git diff --check` sạch. Không thay placeholder report hoặc các thay đổi Use Case không liên quan.

## 2026-10-29 — Hoàn thiện bộ Class Diagram chung 8 tab

- Mở rộng [file draw.io đang dùng](diagrams/07-class/Class-Diagram-Authentication-Account.drawio) thành tám tab: Authentication & Account, Project Workspace, Data Management, Research Run Orchestration, Research Engines, AI Principal Investigator, Notifications & Integrations, Administration & Monitoring. Giữ nguyên graph Authentication đã duyệt, thêm bảy PNG riêng theo phong cách không frame, trải ngang, mũi tên lớn có nhãn và ít góc gấp.
- Đồng bộ [builder](diagrams/07-class/build_authentication_account.py), [source bảy tab mới](diagrams/07-class/class_diagram_pages.py), [thuyết minh/ánh xạ nguồn và validation](diagrams/07-class/Class-Diagrams-design.md), [rule](diagrams/07-class/rule.md), [inventory](diagrams/README.md) và ghi chú Authentication. Các lớp/signature vẫn là thiết kế đề xuất dựa trên Report7 người dùng gửi và Report III/IV, không phải reverse-engineering implementation; không đổi requirement nên BRD/PRD/Use Case Spec và placeholder report giữ nguyên.
- Validation: builder tái tạo; inventory tám tab/98 classifier, kiểm tra bảo toàn graph Authentication, ID/edge target/link và tính lặp lại; validator chung 0 errors/0 warnings, score 0. draw.io CLI xuất PNG từng tab mới, đã xem trực quan; `git diff --check` sạch. GreenLens full-package gate không phù hợp với bộ chỉ có Class, đã ghi rõ missing-family/unknown-page trong thuyết minh; không báo pass profile đó. Chưa kiểm tra in A4/chèn Word/runtime.

## 2026-10-29 — Vẽ thử Class Diagram Authentication & Account

- Làm gọn đường nối theo phản hồi: căn port cùng tọa độ cho đường thẳng ngang/dọc, bỏ các đoạn gấp nhỏ, đặt waypoint theo hành lang với tối thiểu góc gấp cần thiết. Giữ nhãn, đầu mũi tên lớn và nội dung class. Đồng bộ builder/editable/PNG/thuyết minh; validator 0 errors/0 warnings, score 0; đã xuất lại PNG bằng draw.io CLI, xem trực quan và kiểm tra `git diff --check`.
- Sửa đầu mũi tên vào class: pin trên cạnh, thêm đoạn tiếp cận vuông góc, tăng đầu mở lên size 16/nét 1.5; khôi phục nhãn quan hệ theo ảnh mẫu. Đồng bộ builder/editable/PNG/thuyết minh, giữ nguyên nội dung lớp. Builder và validator đạt 0 errors/0 warnings (score 0); đã xuất/xem PNG và chạy `git diff --check`.
- Bỏ khung ngoài và tiêu đề frame theo yêu cầu; giữ tọa độ class và đường nối. Đồng bộ builder/editable/PNG và thuyết minh; validator 0 errors/0 warnings, đã xem PNG và kiểm tra `git diff --check`. Không đổi nghiệp vụ.
- Điều chỉnh bản xem thử theo phản hồi: trải ngang canvas 2320 × 1300, tăng khoảng cách các cụm, bỏ ghi chú/legend/trạng thái và nhãn diễn giải ngoài class, giữ multiplicity và tiêu đề. Đồng bộ builder, editable, PNG và thuyết minh; nghiệp vụ và thành viên class không đổi. Regenerate và xuất lại PNG; validator 0 errors/0 warnings, score 0; đã xem trực quan và chạy `git diff --check`.
- Thêm [Class Diagram editable](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), [PNG preview](diagrams/07-class/Class-Diagram-Authentication-Account.png), [builder](diagrams/07-class/build_authentication_account.py) và [thuyết minh/ánh xạ nguồn](diagrams/07-class/Authentication-Account-design.md), dựa trên `xFA26SE115_Report7.md` người dùng gửi (III 3.2, IV 3.1) và đối chiếu [Report IV](report/04-software-design-document.md). Bao phủ passwordless email, Google sign-in, profile/onboarding, session/sign-out và quyền project/Platform Admin.
- Các lớp và signature là thiết kế đề xuất để duyệt vì slot IV 3.1.1 đang trống. Không thay placeholder/report hoặc BRD/PRD/Use Case Spec: không có thay đổi yêu cầu nghiệp vụ. Không sửa diagram khác hoặc các thay đổi Use Case đang có.
- Validation: chạy builder; validator báo 0 errors, 0 warnings, score 0; XML một page, 11 classifier; draw.io CLI xuất PNG scale 2/border 20 nền trắng và đã xem trực quan. Kiểm tra link local và `git diff --check`; chưa kiểm tra in A4/chèn Word hoặc runtime.

## 2026-10-29 — Điều chỉnh rule Class Diagram theo hướng dẫn và ảnh mẫu

- Cập nhật [rule Class Diagram](diagrams/07-class/rule.md) theo [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-class-diagram/), [draw.io](https://www.drawio.com/docs/diagram-types/uml/class-diagrams/) và hai ảnh tham chiếu: bố cục trái → phải, hộp UML trắng đen, signature, interface/abstract/enum, chiều quan hệ, role và multiplicity. Giữ 8 diagram theo nhóm feature; làm rõ ảnh không phải nguồn để thêm lớp hoặc công nghệ.
- Phạm vi chỉ là hướng dẫn mô hình hóa; không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec. Folder `07-class` hiện chỉ có rule, chưa có builder/diagram để regenerate hoặc render.
- Validation: đối chiếu rule với nguồn và quy tắc chung; kiểm tra link local và `git diff --check`. Chưa có validation/render của diagram.

## 2026-10-29 — Hoàn tác sửa diagram, bàn giao checklist tự vẽ

- Khôi phục [Use Case editable](diagrams/01-use-case/AI-Research-Experimentation-Platform-Use-Case.drawio) nguyên byte từ bản trước lần sửa diagram gần nhất; gỡ PNG được tạo trong lần sửa đó. Giữ quy tắc phong cách một trang đã được người dùng chốt và các thay đổi không liên quan.
- Thêm [checklist cập nhật Use Case](diagrams/01-use-case/use-case-update-checklist.md): ưu tiên, actor/quyền, ánh xạ nhãn cũ, chức năng cần bổ sung, quan hệ UML và danh sách đủ 41 UC có FE/FR theo [Report III](report/03-software-requirements-specification.md), [BRD](BRD.md), [PRD](PRD.md). Người dùng tự vẽ; không sửa requirement hoặc nội dung diagram.
- Chốt phạm vi view: 6 actor (User, Researcher, Project Manager, Reviewer, Platform Admin, AI Provider); không vẽ Persona/AI PI và tạm chưa đưa Local Node vào use case. Checklist/rule bỏ UC-08/30/31 khỏi lần vẽ này, còn 38 UC, giữ nguyên ID; kiểm tra bảng đủ 38 dòng, không còn association Persona/Local Node. Diagram và BRD/PRD/Report7 không đổi.
- Theo điều chỉnh mới của người dùng: checklist bỏ actor AI PI, giữ tên AI Provider và ba association hỗ trợ UC-19/20/25; giải thích khác biệt giữa provider, maker/guard persona và AI PI. Không chuyển quyền quyết định tạm sang provider; diagram và requirement nguồn chưa đổi.
- Đối chiếu thêm bản `xFA26SE115_Report7.md` người dùng gửi: bảng 41 UC/FE/FR khớp nguồn repo; chỉnh checklist dùng actor Persona cho maker/guard, User cho Sign in, bỏ LLM provider khỏi phương án mặc định và sửa tham chiếu validation upload về bước 2. Ghi nhận hai lỗi trình bày trong Report7 (thiếu heading UC-01 và chú thích approval `[a]` bị rơi); không sửa file Downloads hay diagram.
- Chi tiết hóa checklist thành thao tác cụ thể: 20 oval đổi tên, 21 oval thêm mới, danh sách oval/đường gốc cần xóa, bảng actor–UC cho đủ 41 UC, một generalization PM → Researcher và một include upload → validate; không đề xuất extend. Kiểm tra inventory oval khớp XML gốc, link local tồn tại và diagram không bị sửa.
- Theo yêu cầu người dùng, checklist không đề xuất actor Google/Email hoặc oval riêng cho từng phương thức đăng nhập; giữ UC-01 Sign in tổng quát, không thay đổi yêu cầu xác thực trong BRD/PRD.
- Validation: diagram khôi phục khớp byte bản sao lưu và có một page; checklist đủ 41 mã UC duy nhất; link local trong checklist và entry này tồn tại; `git diff --check` đạt. Không render lại vì sơ đồ được khôi phục nguyên bản.

## 2026-10-29 — Giữ cấu trúc Use Case một trang

- Cập nhật [quy tắc Use Case](diagrams/01-use-case/rule.md): giữ bố cục sơ đồ cũ trên một trang, không tách overview, module hoặc trang chi tiết. Quy tắc riêng này ưu tiên hơn hướng dẫn chung về tách diagram khi đông use case.
- Làm rõ phong cách theo ảnh người dùng: actor hai bên, cụm ellipse chính–phụ trong một khung dọc, nét mảnh/nền trắng; không dùng module box hay danh sách ellipse một cột. Ảnh chỉ là tham chiếu bố cục; ngữ nghĩa và quyền vẫn theo tài liệu nguồn.
- Hoàn tác bộ sơ đồ tám trang, builder và preview vừa tạo; khôi phục file editable từ bản sao lưu trước khi sửa. Không đổi requirement trong [BRD](BRD.md), [PRD](PRD.md) hay [Use Case Spec](report/03-software-requirements-specification.md).
- Validation: so sánh byte với bản sao lưu đạt; XML có đúng một page; `git diff --check` đạt. Không thay đổi nội dung hay hình học sơ đồ nên không cần render lại.

## 2026-10-29 — Hoàn tất merge Context diagram

- Hợp nhất [Context diagram](diagrams/12-context/System-Context-Diagram.drawio) (khi merge vào cấu trúc diagrams mới, file chuyển từ `diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio` sang `diagrams/11-optional/`, nội dung giữ nguyên): giữ bốn trang và bố cục hiện có, cập nhật metadata nguồn theo [BRD](BRD.md), [PRD](PRD.md) và context model `diagrams/context-diagrams/context_diagram.json` (đã gỡ cùng folder cũ). Không đổi requirement hay workflow.
- Kiểm tra: builder `diagrams/context-diagrams/build_context_diagram.py` chạy thành công vào file tạm; validator báo 0 lỗi, 2 cảnh báo đường nối giao nhau (score 20); draw.io xuất PDF thành công. `tools/doclint.py` và self-test đạt; kiểm tra link local trong changelog đạt. Không thay layout thủ công bằng output của builder.

## [Unreleased]

### Added

- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx): viết lại bối cảnh dự án ở I 1 Overview (câu mở đầu) và I 2 Product Background theo yêu cầu của team: sản phẩm hướng tới sinh viên và người mới muốn viết bài báo khoa học nhưng chưa biết lộ trình, xuất phát từ kinh nghiệm dự án RBL cùng cô Hương (khó khăn lớn nhất ở nghiên cứu dữ liệu dạng bảng); mục đích là bộ khung các giai đoạn nghiên cứu rõ ràng, từng bước, thay vì tự động hoá nghiên cứu cho người đã giỏi; sau đó dẫn sang hệ thống hiện tại (5 stage). Bảng BP và phần còn lại của mục 2 giữ nguyên. Nội dung ở [S1](deliverables/supplements/S1-introduction.md), thay cho mục tương ứng của `report/00` chỉ trong docx; `report/` không đổi.
  - Validation: build lại, đoạn cũ không còn trong docx; TOC 515 mục ổn định; render 236 trang, kiểm tra trực quan trang 19.
- Lõi khoa học xuyên run (quyết định của owner D1..D6, 2026-10-29; điều kiện của D1 là cổng kiểm tra, không phải thời gian còn lại). Mục đích: hệ thống là một quy trình suy luận, test và bằng chứng kiểm được, và giá trị của nó đo được bằng độ tin trên mỗi phút chú ý của con người.
  - [glossary.md](glossary.md) 1.1: Quy tắc 6 (nghĩa đã giữ chỗ của severity, calibration, forecasting); evidence e-value và evidence rows thay "e-value"; §7a mới: claim ledger, promoted, claim status, `established`, `refuted`, test stringency, forecast, forecast score, replication run, planted-truth bench, hidden-error rate, attention budget; §11 thêm tên đã bỏ "e-value" đứng một mình và "e-value ledger".
  - [BRD.md](BRD.md): §1 giá trị đo được và đích sau MVP; BO-09 thêm planted-truth bench; BR-53 làm rõ record nào vào claim ledger; BR-105 (Must: chỉ nhân giữa nhóm hàng độc lập, record đầu tiên, α là setting); BR-106..BR-110 (Should: claim status, forecast, xác suất của model không quyết định, replication run, planted-truth bench và ablation); SM-19..SM-22; §7.1 phạm vi Should và Could; hai rủi ro mới.
  - [PRD.md](PRD.md): G-12; FR-209 viết lại; FR-272, FR-273 (Must, FE-09); FE-20 mới (Should) với FR-274..FR-287; danh sách Could sau MVP không có FR.
  - [architecture.md](architecture.md): S15; AI PI đọc claim ledger; runtime view 6.h (vòng suy luận, test, bằng chứng); ADR-09 dùng evidence e-value; ADR-19 (evidence e-value chỉ nhân giữa nhóm hàng độc lập); ADR-20 (claim status là mức claim ceiling xuyên run).
  - [traceability.md](traceability.md): Matrix A, B, D, E; số đếm 110 BR, 287 FR (256 Must, 25 Should, 6 Could); gap G8: FR-272..FR-287 và BR-105..BR-110 chưa có UC và TC.
  - [Report I](report/00-front-and-I-introduction.md): FE-20 trong bảng feature; §6.3 Future Work. [Report IV](report/04-software-design-document.md): ADR-09 viết lại, ADR-19, ADR-20. [Report III](report/03-software-requirements-specification.md) và [Report V](report/05-software-testing-documentation.md): FR-209, BR-53 và luồng lane E dùng evidence e-value và claim ledger; UC và TC cho FR mới chưa viết (G8).
  - Không đổi: MVP vẫn là FE-01..FE-15 và FE-17; diagram trong `diagrams/` không đổi. [Report7.docx](deliverables/FA26SE115_Report7.docx) chưa được cập nhật theo các thay đổi của `report/` trong đợt này.
  - Validation: `python -I tools/doclint.py` (0 lỗi); `git diff --check` sạch; số BR, FR và priority đếm lại bằng script từ BRD §8 và PRD §8 (cùng script cho lại 104 BR, 271 FR, 254 Must trên bản trước).

- Khôi phục 5 diagram editable đã bị xoá trong [commit 151edf99](https://github.com/openai-scientist/capstone-project-docs/commit/151edf99e173c75ffc9433ed2c938ff15bcd3504) vào `diagrams/11-optional/`: [Activity](diagrams/11-optional/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio), [Context](diagrams/11-optional/AI-Research-Experimentation-Platform-Context.drawio), [ERD](diagrams/11-optional/AI-Research-Experimentation-Platform-ERD.drawio), [Sequence](diagrams/11-optional/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio) và [Use Case](diagrams/01-use-case/AI-Research-Experimentation-Platform-Use-Case.drawio). Nội dung nghiệp vụ, requirement và workflow không đổi; BRD, PRD và Use Case Spec không cần cập nhật.
  - Validation: `xmllint --noout` đạt trên cả 5 file; `git diff --check` và kiểm tra whitespace cho các file mới đạt.

- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx): lấp các mục chữ còn trống của Report III và IV; trong I–V chỉ còn ô diagram. Nội dung lấy từ code web app, backend và database script, viết ở [S3](deliverables/supplements/S3-requirements.md) và [S4](deliverables/supplements/S4-design.md); `report/` không đổi.
  - III: câu dẫn 2.2 và 3.; 3.1.2 Screen Descriptions; 3.1.3 Screen Authorization; 3.1.4 Non-Screen Functions; 3.1.5 Entity Descriptions; mô tả 63 chức năng ở 3.2–3.9; NFR chia theo thuộc tính ở 4.2.1–4.2.6.
  - IV 2.2.1–2.2.40: mô tả từng bảng sinh bằng [describe_tables.py](deliverables/database/describe_tables.py) từ [database script](deliverables/database/FA26SE115_database-script.sql).
  - Validation: placeholder giảm từ 249 xuống 136 (III 1 và IV 69 là ô diagram, VI 66); dòng leader chưa đặt chỉ là 6 dòng mở đầu supplement; TOC 515 mục ổn định; render 236 trang, kiểm tra trực quan trang 62 và 141.

- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx): mục I 3 Existing Systems dùng heading của leader thay cho KNIME/Orange của khung mẫu (3.1 Jupyter, 3.2 The AI Scientist, 3.3 AI co-scientist, 3.4 data-to-paper, 3.5 Kosmos, 3.6 Comparison and Research Gap); mỗi hệ thống nằm đúng heading, không còn placeholder ở Report I. `report/` không đổi.
  - Validation: build lại 360 heading; dòng leader chưa đặt chỉ còn 4 dòng mở đầu của supplement (như trước); TOC 515 mục ổn định; render 214 trang, kiểm tra trực quan trang 21.

- [Conceptual ERD](diagrams/03-conceptual-erd/Entity-Relationship-Diagram-Conceptual.drawio): 30 entity, 51 quan hệ, sinh bằng [build_erd.py](diagrams/03-conceptual-erd/build_erd.py) từ [database script](deliverables/database/FA26SE115_database-script.sql). Entity là bảng nghiệp vụ, đặt tên danh từ số ít PascalCase; bỏ 11 bảng kỹ thuật và các FK chỉ ghi người tạo/sửa/xác nhận. Bản số Crow's Foot suy từ FK (NOT NULL, FK là PK). [rule.md](diagrams/03-conceptual-erd/rule.md) cập nhật theo: nguồn entity, cách đặt tên, cách suy bản số, bố cục. Không đổi BRD/PRD/Use Case Spec vì không đổi requirement. Team chốt ERD theo database script; [review2-gaps.md](review2-gaps.md) ghi phần IV 2.1 cần leader cập nhật cho khớp.
  - Mọi entity cùng kích thước; đường nối do builder định tuyến trên lưới 20 px, không đường nào đi chung đoạn hoặc cắt qua entity.
  - Validation: builder kiểm tra bảng khớp layout và mọi quan hệ có động từ; draw.io CLI xuất PNG thành công; kiểm tra trực quan: không đường cắt qua entity, không nhãn chồng nhau.

### Changed

- [diagrams/03-conceptual-erd](diagrams/03-conceptual-erd/rule.md) (đổi tên từ `03-logical-erd`): team chốt vẽ ERD mức conceptual. Rule mới: entity chỉ ghi tên, quan hệ có tên và bản số Crow's Foot hai đầu, cho phép nhiều-nhiều trực tiếp, cấm thuộc tính/khoá/kiểu dữ liệu và entity kỹ thuật; ghi chú độ lệch với chữ "Logical ERD" của hướng dẫn Review 2. Cập nhật [README](diagrams/README.md) và [06-database](diagrams/06-database/rule.md).
- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx): bổ sung các mục Review 2 yêu cầu mà `report/` chưa có, nội dung lấy từ code `logos` và `ai-research-platform-fe` (ngày 2026-10-29), viết ở [deliverables/supplements/](deliverables/supplements/S4-design.md); `report/` không đổi.
  - II 6.2: repository, branch rules, Conventional Commits, CI của từng repo ([S2](deliverables/supplements/S2-project-management.md)); trả lời open item O-7.
  - IV 1.1: Technology Declaration (stack kèm version từ lock file, dịch vụ bên thứ ba với mục đích và dữ liệu gửi đi, AI tools) và Environments, Deployment and Rollback ([S4](deliverables/supplements/S4-design.md)).
  - IV 2.2: Database Script, kèm [database script](deliverables/database/FA26SE115_database-script.sql) sinh bằng cách chạy migration Alembic tới `20261022_0048` trên PostgreSQL 16 rồi `pg_dump --schema-only` (41 bảng, không dữ liệu).
  - V 4.2: thêm trường Execution (Automated/Manual theo level và method ở V 2.1) và Actual result cho 60 test case.
  - [review2-gaps.md](review2-gaps.md): các mục còn cần leader quyết định (workflow, state entity, ERD lệch script, staging, KNIME/Orange trong khung mẫu).
  - Validation: build lại theo khung 358 heading; 0 dòng nội dung leader bị sót; TOC 513 mục ổn định; field 514/514; render 214 trang và kiểm tra trực quan trang mới.
- [diagrams/](diagrams/README.md): dựng lại cấu trúc folder cho draw.io theo bộ diagram đã chốt (SEP490 template và hướng dẫn Review 2): `01-use-case` đến `10-activity` và `11-optional`, README có bảng folder, vị trí trong report, checklist tên file và quy tắc chung (file, frame UML, font, màu, export PNG). Mỗi folder có `rule.md` quy định ký hiệu, bố cục, điều cấm và checklist theo chuẩn: UML 2.5.1 (use case, class, sequence, state machine, activity, package, deployment), Crow's Foot (logical ERD, database), C4 (system overview, context), BPMN 2.0 (business process), mẫu SEP490 và hướng dẫn Review 2. Đã đối chiếu với nguồn online (OMG UML 2.5.1 và issue UMLR-670, Ambler *Elements of UML 2.0 Style*/agilemodeling.com, uml-diagrams.org, c4model.com, Camunda BPMN naming, draw.io crow's foot), sửa lại frame kind, hướng include/extend, quy ước tên (event thì quá khứ, guard không trùng, `name : Class`, reply chỉ khi cần, `[Container: tech]`, legend C4) và thêm mục Nguồn cho từng rule; 24 link nguồn đã kiểm tra trả về HTTP 200. Các folder diagram cũ (activity, context, erd, sequence, usecase) đã được dọn trước đó vì stale so với v3; link tới các file này trong các entry cũ đổi thành đường dẫn dạng text.
- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx) (bản track cho cả team; bản làm việc local vẫn ở `docs/1.2/report/`): dựng lại nội dung từ `report/00`–`06` nhưng **giữ nguyên khung Table of Contents của mẫu báo cáo đồ án** (358 heading cấp 1–4 cũ, đúng tên và thứ tự), cùng trang bìa và định dạng heading, bảng, bullet, ô ảnh, caption của bản docx cũ.
  - Nội dung leader được đặt vào heading cũ tương ứng theo một bảng ánh xạ, chữ giữ nguyên; heading con của markdown chuyển thành đoạn in đậm. Ví dụ: UC-01..41 vào III 2.2.2 Descriptions; FE-xx vào các nhóm III 3.2–3.9; Data Design vào IV 2. Database Design; Quality Scenarios, Risks and Technical Debt vào IV 1.1; các how-to Diátaxis vào nhóm User Manual tương ứng. Mục leader không có chỗ riêng trong khung cũ (Re-plan, Scope change log, Hand-off objects, Test risks, Users and Actors, các hệ thống AI Scientist/co-scientist/data-to-paper/Kosmos) được gộp vào heading gần nhất. Đã kiểm tra: 0 dòng nội dung leader bị bỏ sót (trừ các mục "Open items" nội bộ).
  - 259 heading của khung mẫu chưa có nội dung tương ứng trong `report/` (ví dụ KNIME, Orange, từng chức năng/sequence diagram cũ, Table Details từng bảng, Screens Flow) được giữ, kèm dòng `[CONTENT TO BE ADDED — …]`; 158 ô `[IMAGE TO BE ADDED — …]` cho hình theo khung cũ và hình của leader.
  - Caption hình và nội dung ô ảnh dùng tên diagram chuẩn BA/UML để người chuẩn bị biết cần vẽ gì: System Context Diagram, Use Case Diagram, Component, Deployment, Package Diagram, ERD, Screen Flow Diagram, `Class Diagram – <nhóm>`, `Sequence Diagram – <use case>`, `State Machine Diagram – <đối tượng>`, `Activity Diagram – <quy trình>`, `UI Screen – <chức năng>`. Chỉ đổi trong docx, `report/` giữ tên gốc.
  - Bộ sơ đồ đối chiếu hướng dẫn Review 2 (`docs/example/SWP490_R2_Huong-dan-chuan-bi-Review-2_1.pdf`, không còn trong repository) và report mẫu SEP490 (`docs/example/1_SEP490`, `docs/example/2_SEP490`). 14 ô ảnh đánh dấu "REQUIRED – Review 2": System Overview, Logical ERD, State machine cho Research Run, Hand-off Object, Project, Local Node, Dossier, Decision Item, và Activity diagram cho 5 luồng chính. 75 ô ảnh đánh dấu "REQUIRED – SEP490 template": Use Case, Screen Flow, Database Diagram (IV 2.2), Package, Class diagram theo feature, Sequence diagram. IV-2 đổi thành System Overview Diagram, IV-6 đổi thành Activity Diagram. Các ô State Diagram của khung mẫu mà nhóm không có thực thể có vòng đời thì ghi chú, không đặt ô ảnh.
  - TOC có link, gồm Heading 1–4 và caption hình (513 mục), số trang lấy từ bản render và đã ổn định; footer đổi sang "OpenAI-Scientist".
  - Không sửa file nào trong `report/`.
  - Validation: kiểm tra phủ nội dung 0 dòng thiếu; render bằng LibreOffice field TOC cân bằng (514 begin/514 end), kiểm tra trực quan trang TOC.

- Tên hệ thống: "AI Research Experimentation Platform" đổi thành **OpenAI-Scientist** (theo tên organization) trong `report/`, [glossary.md](glossary.md), [BRD.md](BRD.md), [PRD.md](PRD.md), [architecture.md](architecture.md), [README.md](README.md) và [traceability.md](traceability.md). Tên đề tài đã đăng ký giữ nguyên trên trang bìa. Các thuật ngữ thành phần Platform, engine và Local Node không đổi. Diagram chưa đổi tên (vẫn stale).
- `report/`: biên tập giọng văn để bỏ dấu hiệu văn bản máy viết, gồm đối lập giả, câu chốt, gạch ngang, chữ đậm trang trí và tự mô tả tài liệu. Nội dung, ID và bảng giữ nguyên.
- `report/`: biên tập lần hai về giọng văn, thuật ngữ, phạm vi và tính nhất quán theo một style sheet chung (tên vai trò, giá trị trong code span, "sign in", "dataset", không gạch ngang trong văn xuôi). ID và số dòng bảng giữ nguyên.
- FE-04 đổi tên thành "Research case and run management" trong [PRD.md](PRD.md), [traceability.md](traceability.md) và `report/`.
- Bench: khả năng của bench (seeded-flaw bench, red-team catalogue, đo precision của persona; FR-77, FR-135..FR-137) là Must. Chạy một đợt đánh giá đầy đủ là Should, chạy theo yêu cầu, không thuộc tiêu chí release MVP; SM-17 và SM-18 đo khi đợt đó chạy ([PRD.md](PRD.md) §11.2, [Report II](report/02-project-management-plan.md), [Report V](report/05-software-testing-documentation.md)).
- Ranh giới AutoML: BC-C20 và BC-R20 là chủ đề nghiên cứu của user dưới `method_comparison` (FE-19, Should). Non-goal chỉ loại việc đánh giá chính OpenAI-Scientist so với AutoML hoặc agent tổng quát ([BRD.md](BRD.md) §7.2, [PRD.md](PRD.md) §3 và §11.2.1, [Report I](report/00-front-and-I-introduction.md) EX-09).
- Huỷ run được từ mọi state trừ `ended` (BR-77, [architecture.md](architecture.md), [glossary.md](glossary.md)).
- BR-93, BR-96, BR-98 và các FR Must có hành vi `method_comparison` chỉ giữ phần MVP; phần `method_comparison` ghi "khi FE-19 có, sau MVP". FR-194 chuyển sang FE-19, Should.
- [Report II](report/02-project-management-plan.md): RACI theo R/A/C/I chuẩn; rủi ro 22 viết lại, bỏ tham chiếu ADR-16 và R-11 (không có trong Report IV).
- [Report I](report/00-front-and-I-introduction.md) §3: viết lại phần hệ thống hiện có. Giữ Jupyter làm mốc; bỏ KNIME và Orange; thêm The AI Scientist (Sakana AI), AI co-scientist (Google), data-to-paper (Technion) và Kosmos (Edison Scientific) theo trang và bài báo gốc của từng hệ thống; thêm bảng so sánh §3.6. Đánh lại số Table 2 đến Table 4. Review scope so với các hệ thống này: giữ nguyên MVP và claim type `causal`.
- Danh mục BC: ca FE-09 của đợt 1 (BC-C01, BC-C05; TC-62, TC-63) giữ Must; ca FE-09 từ đợt 2 trở đi và TC-65 đến TC-73 thành Should, chạy theo yêu cầu cùng đợt đánh giá bench ([PRD.md](PRD.md) §11.2.1, [Report V](report/05-software-testing-documentation.md)).
- Đóng câu hỏi mở bằng giá trị đề xuất: SM-02 (trung vị ≤ 15 question và ≤ 24 giờ bị chặn mỗi run, overturn rate ≤ 10% mỗi action type, tính trên run `milestones` trong tháng), SM-17 ≥ 90%, SM-18 = 100%, SR-06 mặc định 3 secondary, SR-08 mặc định 7 ngày và nhắc trước 24 giờ, SR-02 mặc định 1 GB mỗi file, NFR-06 đo trên cả tháng lịch ([BRD.md](BRD.md), [PRD.md](PRD.md), [architecture.md](architecture.md) QS-13/QS-14, `report/`).

### Removed

- Hai file tạm của draw.io trong `diagrams/context-diagrams/`; [.gitignore](.gitignore) bỏ qua mẫu `.$*.bkp` và `.$*.dtmp`.

### Added

- Hạn chờ của item pinned: BR-104, FR-263..FR-266, SR-08, MSG-59, MSG-60, TC-99, TC-100, QS-15. Hạn chờ là setting của project. Trước hạn, hệ thống nhắc Researcher đã tạo run và Project Manager. Hết hạn, run kết thúc `ended(with_gaps)`; item đóng mà không có câu trả lời, không ai quyết thay user. `with_gaps` có ba nguyên nhân (FR-262, BR-14).
- FR-267..FR-269: phần `method_comparison` tách khỏi FR Must (Should, FE-19). FR-270, FR-271: luật của review loop, gồm finding chặn mới trên field không đổi chỉ hợp lệ khi bằng chứng là fact mới tính.
- MSG-61: vi phạm thứ tự pipeline. TC-101 (Must): kiểm tra khả năng của seeded-flaw bench trên tập case tối thiểu.
- [glossary.md](glossary.md): Pinned wait deadline, Web app, Holm correction, Gatekeeping, Implanted effect, Clean permutation check, Candidate cap per round, Probe budget, Known risk; AI PI là connector persona, đóng vai secondary actor.

### Fixed

- [Report V](report/05-software-testing-documentation.md): FR-135..FR-137 (Must) trước chỉ có TC-58 (Should); nay có TC-101. [traceability.md](traceability.md) cập nhật BR-40, BR-100 và số TC (101).
- [Report VI](report/06-release-package-and-user-guides.md): sửa tham chiếu MSG-51 và MSG-25.

Validation: `python -I tools/doclint.py` (13 file, 0 lỗi), `--self-test` đạt, `git diff --check` sạch; script kiểm tra: 271/271 FR có UC trong Report III và có TC trong Report V, mọi TC được dẫn đều tồn tại, mọi ID BR/UC/MSG/SR/CR/QS/ADR/NFR/FE/SM trong `report/` có trong nguồn.

## [2026-10-29] — Giai đoạn C: Report 7 bằng tiếng Anh và dọn dẹp tài liệu cũ

### Added

- `report/`: bản staging tiếng Anh của Report 7, một file cho mỗi mục La Mã, dẫn xuất từ BRD, PRD, architecture và glossary; không gắn với trạng thái triển khai, không chứa thông tin nội bộ, không có diagram.
  - [I. Project Introduction](report/00-front-and-I-introduction.md), kèm front matter.
  - [II. Project Management Plan](report/02-project-management-plan.md): baseline gốc, re-plan, scope change log.
  - [III. SRS](report/03-software-requirements-specification.md) theo ISO/IEC/IEEE 29148: UC-01..UC-41, SR-01..SR-07, CR-01..CR-06, MSG-01..MSG-55; phủ 145/145 FR.
  - [IV. SDD](report/04-software-design-document.md) theo các viewpoint của IEEE 1016; data model chỉ ở mức logic.
  - [V. Testing](report/05-software-testing-documentation.md) theo ISO/IEC/IEEE 29119-3 bản rút gọn: TC-01..TC-94; mọi FR, NFR và BC đều có test case; trạng thái "Not run".
  - [VI. Release Package & User Guides](report/06-release-package-and-user-guides.md) theo Diátaxis.
  - Mỗi mục có phần "Open items" ghi những gì nguồn chưa định nghĩa.
- [README.md](README.md): thêm ID `CR-`.

### Changed

- Đổi tên file `AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md` → [BRD.md](BRD.md) và `AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md` → [PRD.md](PRD.md), vì số phiên bản trong tên file sai với nội dung v3.0. Đã sửa link trong mọi tài liệu và trong source của context diagram.
- [tools/doclint.py](tools/doclint.py): danh sách mặc định gồm BRD.md, PRD.md và `report/*.md`.
- [changelog.md](changelog.md): chuẩn hoá theo Keep a Changelog; bỏ đường dẫn code, repo khác, commit và tên tài liệu nội bộ.

### Fixed

- Sửa sau review độc lập (27 finding: 3 High, 10 Medium, 14 Low; theo luật tài liệu đứng trước thắng):
  - Item pinned đang chờ giữ run ở `waiting(decision)`. Run chỉ `ended(with_gaps)` khi hết token budget hoặc khi item `spending` quá hạn (FR-262). State model có thêm lối ra từ `waiting` và lối huỷ từ mọi state.
  - Floor của `acceptance` là `auto`. Mức trần chi tiêu là giới hạn tiền, không phải floor (BR-61, FR-92). Bảng level theo preset thành FR-147..FR-150.
  - Decision inbox có tám loại item, thêm `spending`.
  - Cardinality: Run 1 – 0..N Lock và 1 – 0..N Dossier version.
  - Cột nguồn của NFR chỉ còn BO/BR/SM. NFR-03, NFR-06, NFR-15 viết lại cho kiểm được. FR-113 thành dạng tuỳ chọn. Cột BR của bảng FE tính lại.
  - Persona có ba loại (maker, guard, connector), mỗi tên có một dòng trong glossary. Bỏ "đóng run".
  - Report: bỏ dẫn mục của tài liệu nội bộ, tên vendor/framework và ghi chú biên tập; sửa tham chiếu Open item, MSG-31, MSG-44, TC-01, TC-57..61, TC-90.
  - doclint: chỉ miễn trừ đúng heading lịch sử; bỏ miễn trừ cho dòng có "→"; thêm self-test.
- Đăng nhập bằng tài khoản Google: thêm BR-103, FR-146, MSG-56..MSG-58, TC-95..TC-98.
- Tách FR gộp nhiều yêu cầu: 111 FR mới (FR-151..FR-261). Phần đầu giữ ID cũ. Tổng 262 FR: 249 Must, 7 Should, 6 Could.
- [traceability.md](traceability.md): điền cột UC và TC cho cả 103 BR. 262/262 FR có UC và TC. Đóng gap G6.

### Removed

- Ảnh sơ đồ end-to-end cũ ở repo root: mô tả luồng có Decision Gate của bản BRD/PRD trước, mâu thuẫn với v3.0.

Kiểm tra (sau vòng sửa): doclint trên 13 file mặc định cho 0 lỗi, 0 cảnh báo; `--self-test` đạt 15 case; quét từ khoá rò rỉ nội bộ trên `report/` không có kết quả; mọi ID mà Report dẫn tới đều có ở nguồn hoặc ở Report III; `git diff --check` sạch. Diagram vẫn stale.

## [2026-10-29] — Giai đoạn B: BRD, PRD, architecture v3.0, lớp kiểm soát dữ liệu bảng, tài liệu độc lập

### Added

- [traceability.md](traceability.md): ma trận BO → BR, BR → FE → FR, NFR → BO/BR/QS, ADR → BR/FR, FE/SM; bảng coverage và gap.
- [id-mapping.md](id-mapping.md): ánh xạ ID cũ → v3.0 cho BRD, PRD, architecture (chuyển từ Appendix A của từng tài liệu).
- [tools/doclint.py](tools/doclint.py): kiểm link, anchor, tên đã bỏ, dấu hiệu gắn với code và dẫn nguồn quyết định; có `--self-test`.
- [glossary.md](glossary.md): thuật ngữ dữ liệu bảng (task family, research pattern, prefilter, dataset shift, pipeline order, evidence family, method comparison, red-team catalogue, benchmark case).
- Benchmark case catalogue `BC-*` (60 case) ở PRD §11.2.1, gắn priority theo FE.
- Claim type method comparison (pattern G–J, FE-19, Should, sau MVP); upload nhận Parquet.

### Changed

- [BRD](BRD.md) v3.0: đánh số lại BP, BO, SM, BR (BR-01..BR-102, SM-01..SM-18); cột nguồn của BR chỉ còn BO.
- [PRD](PRD.md) v3.0: FE-01..FE-19 (FE-16 deprecated), FR-01..FR-145, NFR-01..NFR-31, journey J1–J7; cột nguồn của FR chỉ còn BR.
- [architecture.md](architecture.md) v3.0 theo arc42: logical data model, runtime view, ADR-01..ADR-18, quality scenario, risk.
- [README.md](README.md): nguyên tắc "tài liệu định nghĩa hệ thống"; thêm `BC` vào bảng ID; thêm id-mapping và traceability vào bộ tài liệu.
- Hành vi đích theo thiết kế đích mới: run state thêm `ended(cancelled)`; item `spending` hết hạn thì `with_gaps`; Admin chỉ thấy metadata; Dossier chỉ tạo khi PaperPack accepted và version mới cần duyệt lại; Project Manager có mọi quyền nghiên cứu của Researcher; Researcher trả lời release review; thông báo ngoài cho item pinned và `spending`; dataset stage được tìm dataset public; xác nhận cấu trúc dữ liệu là action pinned; thu hồi rule Local Node; duyệt ngưỡng NFR.
- MVP = FE-01..FE-15 + FE-17; UI sản phẩm chỉ tiếng Anh.
- Dữ liệu bảng: thêm lớp kiểm soát (task family, panel, dataset shift, pipeline order, leakage, prefilter, hypothesis testability, evidence family, red-team catalogue, scorecard SM-17/SM-18), dựa trên tài liệu tham khảo về dữ liệu bảng; claim type method comparison là thay đổi có chủ đích so với thiết kế đích.
- Tài liệu độc lập: bỏ dẫn nguồn quyết định; truy vết chỉ lên ID cha; ánh xạ ID cũ gom vào id-mapping.md; tài liệu nội bộ viết tiếng Việt, chỉ `report/` viết tiếng Anh.
- Bỏ Appendix B "thay đổi so với v2.2" của BRD và PRD; lịch sử nằm ở changelog.

### Removed

- `specs/` (gap analysis, SRS, SDD, design brief): bản nháp chưa từng commit, đã gộp vào BRD, PRD, architecture.

Kiểm tra: doclint 7 file mặc định 0 lỗi, 0 cảnh báo, `--self-test` đạt; 102 BR đều có trong Matrix B; 145 FR đều có trong traceability, không FR nào thiếu BR nguồn; tập ID trước và sau lượt làm độc lập giống nhau; `git diff --check` sạch. Diagram trong `diagrams/` chưa cập nhật (stale theo kế hoạch).

## [2026-10-29] — Giai đoạn A: glossary duy nhất và chuẩn tài liệu

### Added

- [glossary.md](glossary.md): nguồn thuật ngữ duy nhất, 10 nhóm (actor, project và dữ liệu, run, harness và kiểm soát, review độc lập, hand-off object, execution, paper, Local Node, quản trị kết quả) và bảng **tên đã bỏ** (mode light/auto, gate, send-back, Research Brief/Verify, HGAR, Writing AIF, pipeline `default`, runner + Docker).

### Changed

- [README.md](README.md): thay dòng tiêu đề bằng chuẩn tài liệu: bộ tài liệu và thứ tự dẫn xuất (glossary → BRD → PRD → architecture → Report); mức chi tiết độc lập với code; tách nội dung bền và hay đổi; quy ước ID vĩnh viễn và deprecated; chuẩn theo loại tài liệu; văn phong ASD-STE100; trạng thái stale của `diagrams/`.
- Hành vi đích: preset theo stage + presence thay mode; decision inbox có overturn; review loop bắt buộc; dataset không bắt buộc khi bắt đầu run; một run active mỗi project; Reviewer duyệt Dossier; Platform chỉ version/hash/duyệt Dossier; HGAR tan vào execution; JFE là Could.
- Tài liệu ở mức khái niệm, không route/HTTP/kiểu cột. Paper stage theo thiết kế đích, chờ tài liệu writing.
- Diagram đánh dấu stale, cập nhật ở đợt riêng. BRD, PRD, architecture chưa sửa (giai đoạn B).

Kiểm tra: đối chiếu glossary với thiết kế đích và actor với BRD §6; kiểm stale của diagram; kiểm link nội bộ và `git diff --check`. Chuẩn tham chiếu: [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html), [IEEE 1016-2009](https://standards.ieee.org/ieee/1016/4502/), [ISO/IEC/IEEE 29119-3](https://www.iso.org/standard/79429.html), [arc42](https://arc42.org/), [ADR](https://adr.github.io/), [Diátaxis](https://diataxis.fr/), [ASD-STE100](https://www.asd-ste100.org/).

## [2026-10-28] — Chuẩn hoá tên entity và quy ước Crow's Foot của ERD

### Changed

- ERD editable (`diagrams/erd/AI-Research-Experimentation-Platform-ERD.drawio`) và model (`diagrams/erd/platform_erd.json`): dùng 40 danh từ số ít PascalCase làm tên hiển thị (`User`, `Project`, `DatasetVersion`, `PlatformAdminGrant`, `TokenUsageEntry`...); bảng mapping trong README (`diagrams/erd/README.md`) giữ liên kết 1:1 về 40 bảng gốc.
- Nhãn quan hệ là cụm động từ đọc từ parent sang child, là association dữ liệu chứ không phải flow. `ProjectMembership` là associative entity, không thêm đường N:M trùng giữa User và Project.
- Builder/validator (`diagrams/erd/build_platform_erd.py`): nét liền cho 3 quan hệ identifying, nét đứt cho 67 quan hệ non-identifying (biến thể IE ghi trong legend). Optionality/cardinality ở hai đầu nối, dựa trên constraint của schema.
- Mức chi tiết là entity-relationship overview, ẩn attributes theo mẫu report; không gọi là logical/physical model đầy đủ. Giữ 40 entity, 70 FK (54 hiển thị mặc định, 16 provenance trong layer bật được).
- Không đổi requirement, actor, scope, workflow hay schema; BRD/PRD không cần cập nhật.

Kiểm tra: regenerate và `--check` đạt (40 tên duy nhất, 70 FK, cardinality, identifying stroke, routing, rebuild khớp byte); export bằng draw.io và xem hình render; kiểm tra link và `git diff --check`. Nguồn quy tắc đặt tên: [ER/Studio](https://docwiki.embarcadero.com/ERStudioDA/193/en/Object_Name_Rules), [Microsoft Crow's Foot](https://support.microsoft.com/en-gb/visio/create-a-diagram-with-crow-s-foot-database-notation), [draw.io Crow's Foot](https://www.drawio.com/docs/tutorials/crows-foot-notation/); chi tiết ở ERD README (`diagrams/erd/README.md`).

## [2026-10-28] — ERD editable cho Report 7 mục III 3.1.5

### Added

- Report 7 ERD (`diagrams/erd/AI-Research-Experimentation-Platform-ERD.drawio`): 40 entity, 70 quan hệ FK theo schema Platform; ô chỉ ghi tên entity, đường nối có tên quan hệ và Crow's Foot; không liệt kê cột/PK/FK ở mức conceptual.
- ERD model (`diagrams/erd/platform_erd.json`), builder/validator (`diagrams/erd/build_platform_erd.py`), hướng dẫn (`diagrams/erd/README.md`): sinh từ metadata của schema, xác minh nullable/unique/PK/CHECK; 54 quan hệ chính hiển thị mặc định, 16 quan hệ provenance trong layer ẩn.
- Cardinality xét cả constraint kết hợp (OTP một purpose cùng unique theo user và purpose; settings là singleton). Không suy diễn FK từ JSON, tham chiếu đa hình hoặc context ID của monitoring/audit.

### Changed

- Ba ERD cũ đã xoá khỏi working tree trước task được giữ nguyên; link lịch sử tới chúng đổi thành tên file ghi rõ đã xoá, kèm link tới bộ ERD hiện tại.
- Không đổi requirement, scope, actor hay workflow; BRD/PRD không cần sửa.

Kiểm tra: build và `--check` đạt (40 entity, 70 FK, cardinality khớp, không chồng entity/nhãn, không đường xuyên entity, rebuild khớp byte); export draw.io và xem hình render; `git diff --check` sạch.

## [2026-10-28] — Bổ sung phạm vi JFE và Writing AIF vào BRD/PRD

### Changed

- [BRD v2.2 Draft](BRD.md): bổ sung business problems/objectives/metrics, stakeholder, scope JFE/Writing, BR-47–BR-61, business rules, phụ thuộc và rủi ro về corpus rights/claim fidelity.
- [PRD v2.2 Draft](PRD.md): bổ sung JFE/Writing vào bảng users/permissions, flow dạng bước, PR-38–PR-52, bảng data/artifact và non-functional requirements.
- JFE/Writing viết dưới dạng yêu cầu nghiệp vụ/sản phẩm và tiêu chí nghiệm thu, không ghi trạng thái triển khai. Giữ khung và số thứ tự có sẵn; giữ phạm vi tabular/FE-16.

Kiểm tra: 61 BR / 52 PR có ID duy nhất, liên tục; đủ flow journal → corpus → phân tích → profile, và evidence → lập luận → drafting → review/export; link, anchor, code fence và `git diff --check` đạt. Không chạy test hay generator vì chỉ đổi Markdown.

## [2026-10-28] — Đồng bộ BRD/PRD/architecture với contract hiện hành và hướng tabular

### Changed

- [BRD](BRD.md): bổ sung scope tabular, data-card boundary, năm loại cấu trúc dữ liệu, split-policy roadmap FE-16 và business requirements cho protocol freeze/execution/evidence.
- [PRD](PRD.md): đồng bộ research case, case amendment/charter, dataset format/limit, split hiện tại, validator của analysis plan và release status.
- [architecture](architecture.md): đồng bộ package ownership, pipeline, engine contract, hành vi dataset/hypothesis/experiment-design, PI authority, ranh giới frontend/platform và deployment settings.
- Ba tài liệu ghi rõ năng lực hiện tại dừng ở reviewed/locked plan; structure-aware split, sandbox execution, statistical result/verdict/dossier là increment kế tiếp (FE-16).
- Không sửa code, frontend hay diagram. Một số diagram lịch sử vẫn mô tả execution/Popper target; không dùng làm nguồn, cần migration riêng.

Kiểm tra: đối chiếu source và tài liệu tham khảo về dữ liệu bảng; kiểm link/cross-reference (link active trỏ tới file hiện hữu); `git diff --check` đạt. Không chạy test hay render diagram.

## [2026-10-27] — Định hướng lại phiếu đăng ký và report sang dữ liệu dạng bảng

### Changed

- Phiếu đăng ký (file local, không track): giữ định dạng, thông tin chung và tên đề tài; viết lại mục 3 và 4 theo hướng AI Scientist trên dữ liệu bảng do người dùng cung cấp. Bỏ hướng CRISP-DM và phạm vi ML/SE cũ.
- Liệt kê 5 kiểu cấu trúc dữ liệu kèm split policy: quan sát độc lập, có cấu trúc nhóm, theo thời gian, panel/longitudinal, cấu trúc đặc biệt cần adapter hoặc split policy riêng.
- Cập nhật functional/non-functional requirements, deliverables, task packages, research problems/questions/methodology theo hướng HGAR (protocol freeze, human gates, scientific reviewer).
- Report 7 (file local, không track): định vị lại theo dữ liệu bảng, giữ tên đề tài và phần mô tả hệ thống đã code. Viết lại Overview, Product Background, Existing Systems (thêm hàng Data structure, Leakage control), Business Opportunity, Vision, Scope; thêm FE-16 (increment kế tiếp), sửa LI-01, thêm EX-11, EX-12; thêm đoạn mở đầu cho 3.4 Data Management và NFR 4.2.6 Scientific Validity; dựng lại TOC (159 trang).
- BRD/PRD/architecture chưa sửa; cần đồng bộ hướng tabular và FE-16 ở đợt sau.

Kiểm tra: render phiếu (6 trang) và kiểm tra trực quan; `git diff --check` sạch.

## [2026-10-23] — Xoá các tài liệu handoff đã cũ

### Removed

- Ba handoff tạm (topic → hypothesis cho BE, cho engine, và event stream): hệ thống đã code xong. Contract hiện hành nằm trong [PRD](PRD.md) và [architecture](architecture.md).

### Fixed

- Link tới ba file đã xoá ở entry cũ đổi thành tên file kèm ghi chú "đã xoá". BRD/PRD không cần sửa vì không còn tham chiếu.

Kiểm tra: không còn link tới file đã xoá; `git diff --check` sạch.

## [2026-10-23] — Dựng lại Report 7 theo report mẫu và hệ thống đã code

### Changed

- Report 7 (file local, không track): dựng lại theo cấu trúc report mẫu gồm II. Project Management Plan, III. SRS, IV. SDD, V. Testing, VI. Release Package & User Guides, lấy nội dung từ [BRD](BRD.md), [PRD](PRD.md), [architecture](architecture.md) và hệ thống đã code.
- Phần đầu (bìa, Acknowledgement, Definition and Acronyms, I. Project Introduction) giữ chữ, chỉ trình bày lại theo report mẫu.
- Mục III có 62 đặc tả chức năng (33 mục viết mới từ các API của Platform, gồm quyền, business rule, mã lỗi); thêm use case Transfer Ownership, Delete Project, Configure Project Settings; Application Messages List có 135 mã lỗi.
- Mục IV: bảng PK/FK và bảng cột cho 40 bảng (421 cột); mỗi sequence diagram ghi API gọi và luồng chính. Mục V: số test case theo khu vực và kết quả chạy 2026-10-23 (4.063 passed, 9 failed, 53 skipped), Defect Report liệt kê 9 test fail. Mục VI: User Manual theo từng chức năng.
- Gộp Table of Figures vào một Table of Contents có hyperlink; ô ảnh và số liệu còn thiếu đánh dấu highlight vàng.

### Fixed

- Thời hạn lời mời theo cấu hình (mặc định 7 ngày, trần 720 giờ) thay vì 24 giờ; owner có thể xoá hẳn project. Hai điểm này cần đối chiếu lại trong BRD/PRD ở đợt sau.

Kiểm tra: render 159 trang; 632 mục TOC/hình đều có số trang ổn định qua hai lần render; `git diff --check` sạch.

## [2026-10-23] — Viết lại BRD, PRD, architecture theo hệ thống đã code (v2.0 DRAFT)

### Changed

- [BRD](BRD.md), [PRD](PRD.md), [architecture](architecture.md): viết lại thành v2.0. Bản cũ mô tả một "Popper target architecture" chưa từng được hiện thực (Understand ⇄ Ground ⇄ Discover ⇄ Verify ⇄ Communicate, Analysis Ledger, manuscript); bản mới bám hệ thống đang chạy.
- Phạm vi mới: Platform (auth không mật khẩu, project và 3 project role, dataset, data connection, run, stage, gate, accept/send-back, self-healing, token budget, BYOK, admin, webhook, audit); engine dataset, hypothesis, experiment_design; AI PI (charter, stage outcome, failure, close; Critic tắt mặc định; obligation); frontend (route, workspace, Run studio).
- Giữ tên file để không làm hỏng liên kết; version ghi trong header.

Kiểm tra: đối chiếu với README, contract, router, setting và route frontend của hệ thống; `git diff --check` sạch; liên kết giữa các tài liệu trỏ tới file có thật; không có diagram phải regenerate.

## [2026-10-06] — Event stream của research run và handoff topic → hypothesis (DRAFT)

Các tài liệu handoff dưới đây đã bị xoá ở entry 2026-10-23.

### Added

- Contract event stream cho research run (BE ↔ FE): endpoint SSE (resume bằng `Last-Event-ID`), lệnh trả lời gate, pause/resume, envelope event, danh mục event theo 7 stage, điểm dừng theo 4 review mode, ánh xạ với run/review/artifact hiện có. Lý do: FE đã dựng workspace từ event (dùng mock) nên BE và engine cần spec chung.
- Handoff cho team engine: ranh giới trách nhiệm với Platform BE; API engine cung cấp (tạo run idempotent, đọc trạng thái và event, trả lời gate, pause, resume, cancel); đẩy event về BE với số thứ tự và chính sách retry; danh mục event theo stage; gate; quy tắc chia nhỏ event; 10 tình huống lỗi; cách test.
- Handoff cho Platform BE: tạo run bằng `topic`, `domains`; đọc lại event; SSE; trả lời gate; pause, resume; endpoint nhận event từ engine; happy case, 15 unhappy case, migration, checklist.

### Changed

- Stage 1–8 thay cho Understand và Hypothesize: 5 stage `scope`, `search`, `screen`, `read`, `synthesize`; `hypothesize` sinh hypothesis qua tranh luận 3 góc nhìn, mỗi hypothesis có tiêu chí bác bỏ, kèm kiểm tra tính mới và khả thi. Khoá test plan chuyển sang step đầu của `experiment`. Gate `framing` đổi thành `scope`; thêm gate `screen` cho Copilot và Full.
- Run bắt đầu từ topic và domains do người dùng nhập, không còn dùng Research context; sub-question do hệ thống sinh ở stage 2. Tạm thời run chỉ đi từ topic tới hypothesis: ẩn chọn dataset, Check the data và review mode (mặc định Copilot); phần Experiment, Report, Paper vẫn giữ trong contract, bật lại bằng cờ.
- Tên artifact trong stage plan là tên cho người dùng đọc thay vì đường dẫn file; thêm trường `reads` tuỳ chọn. Màn hình run không còn lộ tên file hay tên cột dữ liệu; bỏ hiển thị skill trên UI.
- Bổ sung stage 1 (duyệt goal), stage 4 (bản ghi literature kèm nguồn, trích dẫn, DOI; thời điểm thu thập), stage 7 (overview và cơ hội nghiên cứu xếp ưu tiên).
- SSE tách khỏi endpoint đọc event JSON phân trang; dataset của `run.started` thành tuỳ chọn vì run từ topic không có dataset.
- FE nối sẵn API cho luồng này: chọn nguồn run bằng biến cấu hình (`mock` mặc định hoặc `api`), mở lại run sau reload, Experiment/Interpret/Report/Write hiện ở dạng khoá. Mock giữ lại cho tới khi BE qua checklist.
- BRD/PRD/ERD không sửa: contract nháp chưa đổi requirement.

Kiểm tra: typecheck, lint và test của frontend đạt (184 test pass, gồm test SSE mới); chạy trọn luồng bằng Playwright ở chế độ mock và api (happy case, pause/resume, reload giữa chừng, gate sau reload, run fail, mở lại run đã xong), desktop và điện thoại, không lỗi console.

## [2026-10-02] — Conceptual ERD chỉ vẽ cho Platform BE; bỏ Organization

### Changed

- Thay Conceptual ERD chung bằng ERD riêng cho Platform BE (13 entity, 19 relationship; các file lịch sử đã xoá, xem ERD hiện tại (`diagrams/erd/AI-Research-Experimentation-Platform-ERD.drawio`)). Lý do: Popper v2 thay kiến trúc cũ nên entity core của Popper v1 không còn khớp; sơ đồ chỉ gồm những gì Platform BE quản lý.
- Entity: `User`, `Role`, `Project`, `ProjectMember`, `Dataset`, `DatasetVersion`, `ResearchContext`, `Run`, `FrameReview`, `RunArtifact`, `Comment`, `Notification`, `AuditLog`. Mỗi khái niệm xuất hiện một lần, mọi relationship có tên và cardinality crow's-foot, không có thuộc tính hay khoá. `DatasetSnapshot` đổi tên thành `DatasetVersion` theo PRD.
- Bỏ `BillingAccount`, `PublicationRelease`, `PolicyVersion`, `DecisionRequest`, `EvaluationDecision`, `DatasetAssessment`, `UsageRecord` và entity core của Popper v1.
- Trước đó cùng ngày: bỏ `Organization` (42 entity, 69 relationship) vì BRD/PRD không định nghĩa organization hay workspace; project là ranh giới cách ly dữ liệu. Thêm `User owns Project` và `Project billed through BillingAccount`.
- Quyết định nghiệp vụ đi kèm: Reviewer chỉ đọc và bình luận, không có bước ký duyệt; dataset đợt này chỉ nhận CSV.
- BRD/PRD chưa sửa: vẫn tham chiếu kiến trúc Popper cũ, cần đồng bộ riêng.

Kiểm tra: builder báo 13 entity, 19 relationship, 0 crossing; export PNG bằng draw.io và kiểm tra bằng mắt, không có đường đè entity, marker chồng hay nhãn che nhau.

## [2026-10-01] — Điều chỉnh BRD/PRD theo kiến trúc Popper cập nhật

### Changed

- [BRD v1.10](BRD.md) và [PRD v1.9](PRD.md): giữ tên file, cấu trúc module, thứ tự và mọi mã requirement; không thêm module/BR/FR.
- Theo kiến trúc: problem-first brief, Understand ⇄ Ground ⇄ Discover ⇄ Verify ⇄ Communicate, coordinator với bounded playbook; worker/decision layer là tùy chọn.
- Sửa câu mâu thuẫn: agent được viết/chạy/debug code trong sandbox; Verify tùy chọn; reserve unread units không cần approval, pin/freeze cần recorded approval; primary look đã bắt đầu không được rerun để thay outcome.
- BR-79 / Module AI: passive durable exposure/recording, round-scoped contract, Lineage/Program Error Plan kế thừa qua run, không cấp α mới cho mỗi batch/run. BR-60/80/81/87 và Module AF/AJ: tiếp tục nghiên cứu trên non-reserved data sau Verify, giữ origin/history, feedback/steering, recovery.
- Đồng bộ summary, rules, acceptance criteria, provenance, risk, demo; run không Verify vẫn có exploratory figures, interpretation, code, sources, history.
- [architecture.md](architecture.md) giữ như bản tham chiếu cũ. Diagram cần đồng bộ ở đợt riêng trước commit/PR theo [AGENTS.md](AGENTS.md).

Kiểm tra: 150 mã requirement trong BRD và 197 trong PRD giữ nguyên danh sách và thứ tự; link, code fence, cross-reference ID đạt; `git diff HEAD --check` đạt. Không chạy generator vì không sửa diagram.

## [2026-09-30] — Thêm Conceptual ERD

### Added

- Conceptual ERD dạng `.drawio` editable (đã xoá): 43 entity, 70 relationship, crow's foot, connector vuông góc; hai khung Platform và Popper (nét đứt), đường cắt qua ranh giới là interface Platform ↔ Popper; record của Popper mà Platform dùng được tô riêng.
- Model JSON và builder (đã xoá); model ghi reference nguồn cho từng entity; builder có `--check` cho geometry connector và hỗ trợ khung nhóm.
- `.gitignore`: bỏ qua output build, file tạm Office, `.DS_Store`, `__pycache__/`; thêm cấu hình Live Server cho editor.
- Mức conceptual bỏ artifact envelope, events, traces và entity phụ (Construct, DataLead, Critique, Theory, Campaign, MethodLesson, Statement); các phần này thuộc logical ERD.
- File `.drawio` đã chỉnh tay sau khi build nên chạy lại builder sẽ ghi đè chỉnh sửa.
- BRD/PRD/Use Case Spec không cần sửa: ERD chỉ mô hình hoá dữ liệu đã có.

Kiểm tra: `--check` đạt, 0 lỗi, 24 điểm cắt đều có jump arc; render bằng draw.io viewer trên Chrome headless đạt; `git diff --check` đạt. Xem [architecture.md](architecture.md).

## [2026-09-28] — Đồng bộ BRD v1.9 / PRD v1.8 với kiến trúc đích Popper

### Added

- BRD: BR-82 Research Knowledge Layer, BR-83 Research Artifacts & Visibility (Must), BR-84 Publication Views & Integrity Audit (Must), BR-85 Simulation Lab, BR-86 Theory & Observable Implications, BR-87 Research Campaign; BRule-39 (policy settings có version, không được làm yếu bảo đảm), GA-17/18, R-33→36, acceptance criteria 59–63; BR-81 Research Program branches (Should).
- PRD: Module AK (Artifacts & Publication Views), AL (Knowledge Layer), AM (Simulation Lab); FR-STATE-06, FR-REFLOOP-06, FR-LOOP-09, FR-VALID-05/06, FR-PROV-04, FR-REPRO-04/05, FR-EVAL-06, FR-RQ-04; mở rộng NFR-02/03, acceptance criteria 61–66, entities, release plan, traceability.
- [PRD §53.1 Proposed Defaults](PRD.md): giá trị đề xuất cho open decision 5–7 và 14–24 (α = 0.05; deciding interval Bonferroni 1 − α/L, Holm chỉ để báo cáo, FDR chỉ cho exploration; margin theo summary measure; bảng cỡ mẫu; δ_F/δ_N cho pack `general` và software engineering; split 50/50; look budget 5; mode và threshold của decision point ở A1; margin evaluation; capability MVP). BRD KPI-28 trỏ tới α đề xuất. Đang chờ nhóm và supervisor duyệt.

### Changed

- [BRD v1.9](BRD.md) và [PRD v1.8](PRD.md) theo bảng mapping §7.10 của [architecture.md](architecture.md); giữ tên file.
- Research loop: agent loop trong giới hạn budget và invariant, giữ state machine cũ làm workflow floor (BR-80, Module AJ). Thêm exploration/confirmation split, Analysis Ledger, look budget, Research Protocol, confirmation batch (BR-79, Module AI).
- Evidence Sufficiency Gate deterministic: Finding / Negative Result / Inconclusive tính trên adjusted interval so với δ_F / δ_N (BR-59, Module AE). `NEED_MORE_EVIDENCE`, `TRY_ALTERNATIVE_METHOD`, `REPLICATE` thành next move (BR-60, Module AF); `NEED_HUMAN_REVIEW` thành escalation. Deterministic trigger là mức sàn; confidence của decision layer chỉ được thêm escalation (BR-61, BRule-28).
- BR-78: candidate ngang điểm vào cùng một confirmation batch trong look budget, không mở nhánh song song; bỏ `co_selected_with` và cap nhánh song song, thêm quan hệ `registered_in`; chuyển từ section 11 về section 10 (lỗi đặt sai có từ v1.7).
- Experiment chỉ chạy qua registered capabilities, bỏ `run_python`/`run_sql` (BR-22/23, Module L). BR-21 thành triangulation / bounded robustness. BR-65 thành Prior-Work Assessment giới hạn theo coverage, không có nhãn `novel`. BR-48 dùng origin do hệ thống gán.
- Mở rộng BR-27 (claim type / evidential status), BR-34 (reverse provenance), BR-40 (limitation theo validity type), BR-49 (dataset-scope looks), BR-55 (replay vs re-derivation, tombstone), BR-56 (các loại state), BR-58 (screens, admission gate, circuit breaker), BR-63 (champion/challenger), BR-80 (role profiles, context), BRule-07 (causal endorsement), NFR-02/07.
- Sửa mâu thuẫn còn lại: BR-07 / FR-PROFILE-04 (quan hệ hai biến chỉ trên exploration partition); BR-12 / FR-CLEAN-04 (cleaning sau split là protocol deviation); BR-41 / Module W (Negative Result và Inconclusive hiển thị ngang Finding); BR-42 (thêm confirmation batch, severity checks, claim level); BR-59 / Module AE (two-sided và directional); BRule-27 / PP-11 (bỏ "re-plan" khỏi technical retry); FR-EVAL-04 khớp BR-46; FR-VIZ-02 (chỉ registered chart capability); BR-25 (tách stability check khỏi replication); BR-16 / FR-RQ-01/02 (trường Research Brief, gap, intake trước khi đọc dữ liệu); BR-44/45 / FR-EVAL-02 (null / planted-signal ground truth, false-finding rate, power); FR-ADMIN-04 (settings có policy version).
- Tính lại phần định lượng §53.1: Holm thành simultaneous interval Bonferroni cho quyết định sufficiency (BR-49, FR-MTEST-02 làm rõ theo); số run evaluation từ 200 thành khoảng 655 mỗi arm cho margin 0.03 (khoảng 1.470 cho margin 0.02); thêm margin theo từng measure (d, r, β, OR, Cramér's V, η²) và bảng cỡ mẫu.
- [architecture.md](architecture.md): sửa link BRD/PRD hỏng thành link tới file DRAFT; phần "Proposed BRD/PRD changes" thành đã áp dụng, chờ supervisor sign-off.
- Diagram chưa đồng bộ: Activity/Sequence/Use Case/Context còn mô tả outcome cũ và luồng tuyến tính; cần cập nhật và regenerate ở đợt riêng theo [AGENTS.md](AGENTS.md).

Kiểm tra: kiểm tự động đạt (BR/BRule đúng thứ tự và section, MoSCoW và traceability đầy đủ, không tham chiếu ID không tồn tại, không FR trùng, acceptance criteria PRD liên tục 1–66, code fence cân bằng); `git diff --check` sạch. Còn tồn đọng có sẵn từ trước: architecture.md tham chiếu hai file chưa có trong repository. Chưa chạy diagram generator.

## [2026-09-24] — Chuẩn hóa tài liệu REQ-TOOL và cập nhật package diagram

### Added

- Bản chuẩn hóa [BRD](BRD.md) v1.8 và [PRD](PRD.md) v1.7 theo định dạng REQ-TOOL (đã xoá); giữ hai file DRAFT nguồn.

### Changed

- Cập nhật Use Case diagram, Activity và Sequence artifacts/builders theo các entry đồng bộ BRD/PRD.
- Backup Context draw.io là artifact kỹ thuật, không phải nguồn nội dung; Context model và builder là nguồn cho Context DFD Level 0.

Kiểm tra: `git diff --check` đạt; kết quả validation diagram nằm ở entry tương ứng. Diagram: Context (`diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio`), Activity (`diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio`), Sequence (`diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio`), Use Case (`diagrams/usecase-diagrams/AI-Research-Experimentation-Platform-Use-Case.drawio`).

## [2026-09-23] — System Context theo DFD Level 0

### Added

- Context — DFD Level 0 (`diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio`) dạng `.drawio` editable, kèm context model (`diagrams/context-diagrams/context_diagram.json`) và context builder (`diagrams/context-diagrams/build_context_diagram.py`): sáu external entity, một process trung tâm, 25 labeled data flow cấp cao theo BRD/PRD.
- Layout theo reference: Researcher ở trên, Project Manager/System Administrator bên trái, provider bên phải, Reviewer bên dưới; nới corridor để connector không chồng; nhãn flow sát làn mũi tên, rút gọn nhãn dài, tăng cỡ chữ.
- Loại module nội bộ và Secure Sandbox khỏi external boundary; AI/LLM Provider và Structured Decision Provider ở mức abstraction, không khóa vào vendor.

Kiểm tra: builder đạt (layout DFD Level 0 deterministic, không cần Graphviz); validator `--strict --score` 0 error, 0 warning, score 0; render draw.io 31.4.5 và kiểm tra trực quan; `git diff --check` đạt. Use Case, Activity, Sequence không đổi.

## [2026-09-22] — 30 Sequence UC, Activity theo BRD v1.8 / PRD v1.7

### Changed

- Activity — Main Flows (`diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio`) và builder (`diagrams/activity-diagrams/update_activity_diagram.py`): đồng bộ với BR-64/65/73-75/78 (Structured Idea Record/Reflection, optional novelty assessment, bounded tied candidates, immutable branch snapshots, sibling join, shared testing family, provenance/evaluation metadata, trang Final Outputs & Manuscript). Sửa thứ tự Hypothesis Selection Gate, đưa novelty về đúng lane, chuyển method-cap sang Experiment Planner / AI Agent, giới hạn reviewer override ở Researcher, cập nhật ownership của Evaluation, thêm nhánh Approved / Rejected–Revise–Automated Review cho Final Outputs.
- Sequence — Main Flows (`diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio`) và builder (`diagrams/sequence-diagrams/build_sequence_diagrams.py`): từ 24 lên 30 trang UC (UC-25–UC-30: Research Definition, Hypotheses, Experiments, Research Findings, Research Outputs, System Administration); đồng bộ UC-10–UC-16, UC-18–UC-24. UC-10: novelty có `opt [Novelty feature enabled]` và nhánh `SOURCE / NOT ASSESSED`; UC-11: human review optional, cho phép high-confidence auto-continue.
- Use Case diagram giữ nguyên; BRD/PRD không sửa vì là source input.

Kiểm tra: biên dịch hai builder đạt; Sequence sinh đúng 30 trang UC-01..UC-30; activitylint `--strict` và validator `--strict --score` của Activity, Sequence đạt (0 error, 0 warning, score 0); semantic QA đạt (0 lỗi message actor, return source, fragment parent); render draw.io 31.4.5 đạt trên các trang đã chọn; `git diff --check` đạt.

## [2026-09-22] — Refresh editable diagram package

### Added

- Backup kỹ thuật của diagram nằm trong phạm vi staged.

### Changed

- Cập nhật diagram editable Activity, Sequence, Use Case cùng builder source-backed tương ứng. BRD, PRD, Use Case Spec không đổi vì không đổi requirement.

### Removed

- Hai sequence artifact đã superseded.

Kiểm tra: activitylint `--strict` đạt; Activity validator 0 error, 1 cảnh báo crossing, score 10; Main Sequence đạt, score 0; Use Case 0 error, 56 cảnh báo geometry của system boundary/nested layout, score 355, giữ nguyên theo phạm vi yêu cầu; `git diff --cached --check` đạt.

## [2026-09-22] — Local tooling cleanup

### Removed

- Metadata và worktree local của các công cụ agent không còn dùng; rule/reference tương ứng trong [AGENTS.md](AGENTS.md) và registry này.

Kiểm tra: không có tài liệu canonical hay diagram editable nào bị xoá; local link và cross-reference kiểm tra lại.

## [2026-09-22] — Documentation governance

### Added

- [AGENTS.md](AGENTS.md) với documentation-first gate: cập nhật tài liệu và changelog trước khi commit hoặc PR.
- Registry tập trung liên kết toàn bộ tài liệu, flow reference, diagram editable và source builder. Task này không regenerate hay sửa nội dung diagram.

Kiểm tra: local link trong changelog và AGENTS.md đạt; `git diff --check` sạch.

### Gói tài liệu ban đầu

- Tài liệu nguồn: [BRD v1.8 Draft](BRD.md), [PRD v1.7 Draft](PRD.md). Use Case Specification không có file canonical; Use Case diagram giữ nguyên theo scope.
- Diagram: Context (`diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio`), Activity (`diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio`), Use Case (`diagrams/usecase-diagrams/AI-Research-Experimentation-Platform-Use-Case.drawio`), Sequence (`diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio`).
- Builder: Context model (`diagrams/context-diagrams/context_diagram.json`), Context builder (`diagrams/context-diagrams/build_context_diagram.py`), Use Case builder (`diagrams/usecase-diagrams/build_usecase_diagram.py`), Sequence builder (`diagrams/sequence-diagrams/build_sequence_diagrams.py`), [README](README.md), [AGENTS.md](AGENTS.md).
- Backup kỹ thuật của Use Case diagram (đã xoá) không phải source of truth.

### Quy ước registry

- BRD, PRD và Use Case Spec là nguồn nội dung nghiệp vụ/chức năng.
- File `.drawio`/`.xml` là artifact editable, giữ nguyên khả năng chỉnh sửa; PNG là flow reference trực quan.
- Builder là source-backed generator: khi flow hoặc quan hệ thay đổi, cập nhật builder và regenerate artifact.
- Metadata nội bộ của Git và file tạm của môi trường không thuộc documentation package canonical.

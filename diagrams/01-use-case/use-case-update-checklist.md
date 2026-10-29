# Các thao tác sửa Use Case — thêm, sửa, xóa và nối đường

Đối chiếu lại ngày 2026-10-29 với bản người dùng gửi `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md` (§III 2.1, 2.2.1–2.2.2, 3.1.3) và [BRD v3.0](../../BRD.md), [PRD v3.0](../../PRD.md) và [Report III §2.2](../../report/03-software-requirements-specification.md). Đây là phương án vẽ cụ thể; **chỉ cập nhật hướng dẫn, chưa sửa [diagram gốc](AI-Research-Experimentation-Platform-Use-Case.drawio)**.

## 1. Chốt cách đọc và loại đường

Giữ một trang, actor hai bên, ellipse theo cụm như ảnh của bạn. Không tạo overview, module box hoặc danh sách oval một cột. Đổi tên boundary từ `AI Research Experimentation Platform` thành **OpenAI-Scientist**.

| Ký hiệu trong tài liệu | Loại đường phải chọn trong draw.io | Hướng / nhãn |
|---|---|---|
| `Actor — UC` | **Association:** nét liền; Start Arrow = None, End Arrow = None | Không có chiều, không có nhãn |
| `PM —▷ Researcher` | **Generalization:** nét liền; Start Arrow = None, End Arrow = tam giác rỗng (Block, Fill tắt) | Tam giác chạm **Researcher**; không gắn nhãn include/extend |
| `UC A - -> UC B «include»` | Nét đứt; Start Arrow = None, End Arrow = Open | Mũi tên chạm UC B; nhãn `«include»` |
| `UC X - -> UC A «extend»` | Nét đứt; Start Arrow = None, End Arrow = Open | Mũi tên chạm UC A; nhãn `«extend»` và điều kiện |
| `Note …` | Hộp UML Note hoặc ghi chú text | Là điều kiện, không phải oval/use case mới; không vẽ thành mũi tên hành vi |

**Phương án bên dưới chỉ dùng association, một generalization actor và một include giữ lại. Không thêm extend.** Không cần cố thêm include/extend để sơ đồ trông giống hình mẫu.

## 2. Sửa, thêm và xóa actor

| Thao tác | Actor cũ | Actor cuối cùng | Đường cần xử lý |
|---|---|---|---|
| Giữ | Project Manager | Project Manager | Nối theo bảng §3 và thêm generalization tại §5 |
| Giữ | Researcher | Researcher | Nối theo bảng §3 |
| Thêm | Chưa có | User | Người truy cập trước khi đăng nhập, bao gồm guest; chỉ nối UC-01 bằng association. Đây là actor truy cập, không phải role project mới |
| Giữ | Reviewer | Reviewer | Nối theo bảng §3; không nối Lock/Export |
| Đổi tên | System Administrator | Platform Admin | Xóa association cũ, nối lại đúng bảng §3 |
| Xóa và thay vai trò | Decision Model Provider | AI PI | Xóa cả hai đường cũ tới Select Hypothesis và Evaluate Hypotheses. Tạo AI PI bên phải, chỉ nối UC-14 và UC-17 |
| Xóa và thay vai trò | AI Provider | Persona | Xóa ba association cũ của AI Provider. Thêm actor Persona theo Report III §2.1; nối UC-18, UC-19, UC-20, UC-22, UC-25, UC-27, UC-41. Chú thích maker/guard theo từng UC |
| Thêm | Chưa có | Local Node | Bên phải cụm dataset; nối UC-08, UC-30, UC-31 |
| Không tạo riêng | Persona (guard) | Dùng chung actor Persona ở dòng trên | UC-27 là guard; UC-18/19/20/22/25/41 là maker của stage tương ứng. Đây không phải Reviewer là người |

Không thêm Google hoặc Email vào bản vẽ này. Dùng một actor `User` cho UC-01 để bao phủ cả guest; dùng các role Researcher/Reviewer cho UC-38, PM kế thừa Researcher. Không cần thêm actor Any member. Dùng chung một actor `Persona` cho các persona được liệt kê trong mô tả UC để không làm sơ đồ đông hơn. Không vẽ generalization Persona → AI PI: tài liệu chỉ cần hai actor độc lập với phạm vi hành động rõ ràng.

Report III §2.1 liệt kê Persona nhưng không liệt kê LLM provider như actor của Use Case. Vì vậy bỏ LLM provider khỏi phương án mặc định; nhà cung cấp model vẫn có thể xuất hiện ở context/architecture. Local Node là supporting actor bổ sung suy ra từ UC-08/30/31 và scope Local Node, không phải role quyền mới hoặc một dòng có sẵn trong bảng actor §2.1.

## 3. Bảng thao tác cho từng oval và từng association

**Cách làm từng dòng:** đổi tên oval cũ hoặc thêm oval mới như cột 3; sau đó vẽ **một association riêng cho mỗi actor ở cột 4**, không nối các actor thành chuỗi. Tất cả đường trong cột 4 là **nét liền, không mũi tên**.

Ví dụ dòng UC-35: vẽ `Reviewer — UC-35` và `Project Manager — UC-35`, không vẽ `Reviewer — Project Manager — UC-35`.

Project Manager kế thừa toàn bộ association của Researcher qua generalization §5, nên không cần lặp các đường PM → upload, inbox, lock, export… Chỉ những quyền PM riêng hoặc điều kiện riêng mới nối thêm trong bảng.

| UC | Làm gì với oval hiện tại | Tên cuối cùng trên oval | Actor phải nối trực tiếp bằng association | Chỗ đặt gợi ý |
|---|---|---|---|---|
| UC-01 | **Thêm oval mới** | UC-01 Sign in | User | Gần cụm project ở trên trái |
| UC-02 | **Thêm oval mới** | UC-02 View project metadata | Platform Admin | Gần cụm quản trị ở trên phải |
| UC-03 | **Đổi tên** `Manage Members` | UC-03 Manage members | Project Manager | Gần cụm project ở trên trái |
| UC-04 | **Đổi tên** `Update Project` | UC-04 Configure project settings | Project Manager | Gần cụm project ở trên trái |
| UC-05 | **Đổi tên** `Monitor System` | UC-05 Review audit log, health and operating metrics | Platform Admin | Gần cụm quản trị ở trên phải |
| UC-06 | **Đổi tên** `Upload Dataset` | UC-06 Upload a dataset | Researcher | Gần cụm dataset hiện tại |
| UC-07 | **Thêm oval mới** | UC-07 Import from a data connection | Researcher | Gần cụm dataset hiện tại |
| UC-08 | **Thêm oval mới** | UC-08 Pair a Local Node and register local data | Researcher; Local Node | Gần cụm dataset hiện tại |
| UC-09 | **Đổi tên** `Manage Research Definition` | UC-09 Start a run from a research case | Researcher | Gần cụm research case/run hiện tại |
| UC-10 | **Đổi tên** `Define Research Question` | UC-10 Amend a research case | Researcher | Gần cụm research case/run hiện tại |
| UC-11 | **Thêm oval mới** | UC-11 Accept a hand-off object | Researcher | Gần cụm research case/run hiện tại |
| UC-12 | **Đổi tên** `View Research State` | UC-12 Monitor and recover a run | Researcher | Gần cụm research case/run hiện tại |
| UC-13 | **Thêm oval mới** | UC-13 Cancel a run | Researcher; Project Manager | Gần cụm research case/run hiện tại |
| UC-14 | **Thêm oval mới** | UC-14 Choose the next step | Researcher; AI PI | Gần cụm finding/collaboration hiện tại |
| UC-15 | **Thêm oval mới** | UC-15 Set preset and presence | Researcher | Gần cụm hypothesis/decision hiện tại |
| UC-16 | **Đổi tên** `Review Hypothesis Decision` | UC-16 Answer a decision inbox item | Researcher | Gần cụm hypothesis/decision hiện tại |
| UC-17 | **Thêm oval mới** | UC-17 Confirm or overturn a tentative decision | Researcher; AI PI | Gần cụm hypothesis/decision hiện tại |
| UC-18 | **Thêm oval mới** | UC-18 Run the dataset stage | Researcher; Persona  (maker) | Gần cụm dataset hiện tại |
| UC-19 | **Đổi tên** `Manage Hypotheses` | UC-19 Run the hypothesis stage | Researcher; Persona  (maker) | Gần cụm hypothesis/review hiện tại |
| UC-20 | **Đổi tên** `Create Experiment Plan` | UC-20 Run the experiment_design stage | Researcher; Persona  (maker) | Gần cụm experiment hiện tại |
| UC-21 | **Thêm oval mới** | UC-21 Lock a plan | Researcher | Gần cụm experiment hiện tại |
| UC-22 | **Đổi tên** `Run Experiment` | UC-22 Run the execution stage | Researcher; Persona  (maker) | Gần cụm experiment hiện tại |
| UC-23 | **Đổi tên** `Review Experiment Result` | UC-23 Read verdict, grade and claim ceiling | Researcher; Reviewer | Gần cụm experiment hiện tại |
| UC-24 | **Thêm oval mới** | UC-24 Triage exploration candidates | Researcher | Gần cụm experiment hiện tại |
| UC-25 | **Đổi tên** `Generate & Review Manuscript Draft` | UC-25 Run the paper stage | Researcher; Persona  (maker) | Gần cụm outputs/paper hiện tại |
| UC-26 | **Thêm oval mới** | UC-26 Decide on submission | Researcher | Gần cụm outputs/paper hiện tại |
| UC-27 | **Đổi tên** `Perform Automated Manuscript Review` | UC-27 Run the review loop | Researcher; Persona  (guard) | Gần cụm outputs/paper hiện tại |
| UC-28 | **Thêm oval mới** | UC-28 Invoke a persona on an object | Researcher | Gần cụm hypothesis/review hiện tại |
| UC-29 | **Đổi tên** `Run Benchmark` | UC-29 Run the benchmarks | Platform Admin | Gần cụm quản trị ở trên phải |
| UC-30 | **Thêm oval mới** | UC-30 Release an aggregate from local data | Researcher; Local Node | Gần cụm dataset hiện tại |
| UC-31 | **Thêm oval mới** | UC-31 Handle a Local Node that is offline or revoked | Researcher; Local Node | Gần cụm dataset hiện tại |
| UC-32 | **Thêm oval mới** | UC-32 Warn on and enforce budgets | Project Manager | Gần cụm project ở trên trái |
| UC-33 | **Thêm oval mới** | UC-33 Decide extra spend | Project Manager | Gần cụm project ở trên trái |
| UC-34 | **Đổi tên** `View Usage & Cost` | UC-34 Set the spending ceiling and read the ledger | Platform Admin; Project Manager | Gần cụm quản trị ở trên phải |
| UC-35 | **Đổi tên** `Approve Manuscript for External Use` | UC-35 Review and approve a Dossier | Reviewer; Project Manager | Gần cụm outputs/paper hiện tại |
| UC-36 | **Đổi tên** `Export Reproducibility Package` | UC-36 Export a Dossier | Researcher | Gần cụm outputs/paper hiện tại |
| UC-37 | **Thêm oval mới** | UC-37 Comment on an object | Researcher; Reviewer | Gần cụm finding/collaboration hiện tại |
| UC-38 | **Thêm oval mới** | UC-38 Receive notifications | Researcher; Reviewer | Gần cụm finding/collaboration hiện tại |
| UC-39 | **Đổi tên** `Manage Users & Roles` | UC-39 Manage users, models and keys | Platform Admin | Gần cụm quản trị ở trên phải |
| UC-40 | **Thêm oval mới** | UC-40 Build a journal profile (Could, after MVP) | Researcher | Gần cụm outputs/paper hiện tại |
| UC-41 | **Đổi tên** `Run Ablation Study` | UC-41 Compare methods (Should, after MVP) | Researcher; Persona  (maker) | Gần cụm hypothesis/review hiện tại |

Lưu ý cụ thể về các association:

- UC-01: chỉ vẽ `User — UC-01` bằng association. User bao gồm người chưa đăng nhập; không dùng riêng bốn role đã được cấp quyền để thay toàn bộ actor đăng nhập. Không nối Google/Email/Persona vào UC-01.
- UC-13: Researcher chỉ hủy run do mình tạo; PM hủy được run của project. Giữ cả hai association vì điều kiện khác nhau.
- UC-17: đường từ AI PI chỉ nói nó tạo quyết định tạm; **chỉ Researcher/PM xác nhận hoặc lật quyết định**. AI PI không có quyền tự xác nhận.
- UC-18/19/20/22/25/27/41: cùng nối actor `Persona`; chữ `(maker)`/`(guard)` trong bảng là ghi chú phạm vi, không yêu cầu thêm bảy actor. UC-27 có cả Researcher và Persona (guard), đúng mô tả chi tiết.
- UC-23: Reviewer được đọc verdict, grade và claim ceiling, nên có association riêng.
- UC-34: Admin đặt spending ceiling và xem ledger; PM đọc ledger của project. Không hiểu đường PM là quyền đặt system ceiling.
- UC-35: Reviewer và PM duyệt theo review settings. Researcher không có association duyệt riêng.
- UC-37/38: PM thừa hưởng đường Researcher; Reviewer có đường riêng. Platform Admin không có quyền comment/notification project chỉ vì là Admin.
- UC-40/41: giữ nguyên nhãn `Could, after MVP` / `Should, after MVP` như tên ở bảng. Không đưa thành điều kiện bắt buộc của MVP.

## 4. Xóa những oval nào

Sau khi đổi tên theo §3, **xóa toàn bộ các oval cũ dưới đây và tất cả đường chạm chúng**. Nội dung đã được gom vào UC tương ứng hoặc không còn là UC riêng trong danh mục hiện hành. Đây là phương án trình bày đủ 41 UC, không có nghĩa xóa chức năng khỏi sản phẩm.

- [ ] Xóa `Manage Research Project` và các đường nối vào/ra nó.
- [ ] Xóa `Define Initial Hypothesis` và các đường nối vào/ra nó.
- [ ] Xóa `Review Finding Dependencies` và các đường nối vào/ra nó.
- [ ] Xóa `View Experiment Plan` và các đường nối vào/ra nó.
- [ ] Xóa `View Dataset` và các đường nối vào/ra nó.
- [ ] Xóa `Generate Hypotheses` và các đường nối vào/ra nó.
- [ ] Xóa `Review Data Quality` và các đường nối vào/ra nó.
- [ ] Xóa `Generate Figures, Tables & Research Report` và các đường nối vào/ra nó.
- [ ] Xóa `Select Analysis Method` và các đường nối vào/ra nó.
- [ ] Xóa `View Research Outputs` và các đường nối vào/ra nó.
- [ ] Xóa `Review Research Finding` và các đường nối vào/ra nó.
- [ ] Xóa `Manage Dataset` và các đường nối vào/ra nó.
- [ ] Xóa `Manage Evaluation` và các đường nối vào/ra nó.
- [ ] Xóa `Select Hypothesis` và các đường nối vào/ra nó.
- [ ] Xóa `Manage Experiments` và các đường nối vào/ra nó.
- [ ] Xóa `Manage Research Findings` và các đường nối vào/ra nó.
- [ ] Xóa `Manage Research Outputs` và các đường nối vào/ra nó.
- [ ] Xóa `Evaluate Hypotheses` và các đường nối vào/ra nó.
- [ ] Xóa `Retry Experiment` và các đường nối vào/ra nó.
- [ ] Xóa `Review Evidence Decision` và các đường nối vào/ra nó.
- [ ] Xóa `View Evidence` và các đường nối vào/ra nó.
- [ ] Xóa `Select Validated Findings` và các đường nối vào/ra nó.
- [ ] Xóa `Resolve Conflicting Evidence` và các đường nối vào/ra nó.
- [ ] Xóa `View Project` và các đường nối vào/ra nó.
- [ ] Xóa `Create Project` và các đường nối vào/ra nó.
- [ ] Xóa `Archive Project` và các đường nối vào/ra nó.
- [ ] Xóa `View Data Card` và các đường nối vào/ra nó.
- [ ] Xóa `View Dataset Versions` và các đường nối vào/ra nó.
- [ ] Xóa `View Hypotheses` và các đường nối vào/ra nó.
- [ ] Xóa `Refine Hypothesis` và các đường nối vào/ra nó.
- [ ] Xóa `View Research Finding` và các đường nối vào/ra nó.
- [ ] Xóa `View Evaluation Results` và các đường nối vào/ra nó.
- [ ] Xóa `Manage AI Configuration` và các đường nối vào/ra nó.
- [ ] Xóa `Manage Evaluation Configuration` và các đường nối vào/ra nó.
- [ ] Xóa `View Users` và các đường nối vào/ra nó.
- [ ] Xóa `Manage Roles` và các đường nối vào/ra nó.
- [ ] Xóa `Assign Roles` và các đường nối vào/ra nó.
- [ ] Xóa `View Model Configuration` và các đường nối vào/ra nó.
- [ ] Xóa `Configure AI Model` và các đường nối vào/ra nó.
- [ ] Xóa `View System Logs` và các đường nối vào/ra nó.
- [ ] Xóa `View System Health` và các đường nối vào/ra nó.
- [ ] Xóa `Create Idea Record` và các đường nối vào/ra nó.
- [ ] Xóa `Check Assumptions` và các đường nối vào/ra nó.
- [ ] Xóa `Record Execution Trace` và các đường nối vào/ra nó.
- [ ] Xóa `Assess Idea Novelty` và các đường nối vào/ra nó.
- [ ] Xóa `Clean Dataset` và các đường nối vào/ra nó.

**Giữ duy nhất oval phụ `Validate Dataset`** ngoài danh sách 41 UC; không gán mã UC mới. Có thể sửa nhãn thành `Validate uploaded dataset` để phân biệt kiểm tra file nhập với đánh giá fitness của dataset stage. Đây là hành vi bắt buộc trong flow UC-06 (format, size, readable table), không phải một stage mới.

## 5. Nối giữa actor và giữa các oval: danh sách cuối cùng

### 5.1 Thêm đúng một generalization actor

`Project Manager —▷ Researcher`

- Nét liền, tam giác **rỗng** ở phía Researcher; không phải mũi tên Open của include/extend.
- Không nối ngược chiều. Không nối Reviewer hoặc Platform Admin kế thừa Researcher.
- Trong XML hiện có một đường generalization tới Researcher bị thiếu source. Xóa đường lỗi này, vẽ đường mới có đủ hai đầu PM và Researcher.

### 5.2 Giữ đúng một include

`UC-06 Upload a dataset - -> Validate uploaded dataset` với nhãn `«include»`.

- Dùng đường cũ `Upload Dataset → Validate Dataset`, cập nhật nhãn hai oval.
- Nét đứt, mũi tên **Open**, đầu nhọn chạm `Validate uploaded dataset`.
- Không vẽ chiều ngược lại; không nối Researcher trực tiếp tới helper này. UC-06 luôn kiểm tra file nhập, helper được tham gia thông qua include.
- Căn cứ: Report III UC-06 main flow bước 2; PRD FR-09 và FR-154. Helper không thay thế UC-18 Run the dataset stage.

### 5.3 Xóa toàn bộ các đường UC–UC còn lại trong diagram gốc

Bao gồm cả những đường tam giác rỗng hiện dùng để gom các oval nhỏ vào `Manage…`. Đó là **generalization hiện có**, không phải association. Trong phương án này không giữ generalization giữa các use case vì các thao tác view/upload/clean không được mô hình hóa như các biến thể thay thế của cùng một hành vi.

Bảng sau là danh sách đường gốc cần xóa; chiều được ghi chỉ để bạn tìm đúng đường, không phải hướng vẽ lại:

| Xóa đường gốc từ | Tới | Loại hiện tại |
|---|---|---|
| Define Initial Hypothesis | Manage Research Definition | Generalization: nét liền, tam giác rỗng |
| Review Finding Dependencies | Manage Research Findings | Generalization: nét liền, tam giác rỗng |
| Review Experiment Result | Manage Experiments | Generalization: nét liền, tam giác rỗng |
| View Experiment Plan | Manage Experiments | Generalization: nét liền, tam giác rỗng |
| Upload Dataset | Manage Dataset | Generalization: nét liền, tam giác rỗng |
| View Dataset | Manage Dataset | Generalization: nét liền, tam giác rỗng |
| Generate Hypotheses | Manage Hypotheses | Generalization: nét liền, tam giác rỗng |
| Define Research Question | Manage Research Definition | Generalization: nét liền, tam giác rỗng |
| Review Data Quality | Manage Dataset | Generalization: nét liền, tam giác rỗng |
| Generate Figures, Tables & Research Report | Manage Research Outputs | Generalization: nét liền, tam giác rỗng |
| Select Analysis Method | Manage Experiments | Generalization: nét liền, tam giác rỗng |
| View Research Outputs | Manage Research Outputs | Generalization: nét liền, tam giác rỗng |
| Review Research Finding | Manage Research Findings | Generalization: nét liền, tam giác rỗng |
| Run Experiment | Manage Experiments | Generalization: nét liền, tam giác rỗng |
| Create Experiment Plan | Manage Experiments | Generalization: nét liền, tam giác rỗng |
| View Research State | Manage Research Definition | Generalization: nét liền, tam giác rỗng |
| Select Hypothesis | Manage Hypotheses | Generalization: nét liền, tam giác rỗng |
| Retry Experiment | Run Experiment | Extend: nét đứt, mũi tên Open |
| Review Research Finding | View Evidence | Include: nét đứt, mũi tên Open |
| Resolve Conflicting Evidence | Review Research Finding | Extend: nét đứt, mũi tên Open |
| Generate Figures, Tables & Research Report | Select Validated Findings | Include: nét đứt, mũi tên Open |
| Export Reproducibility Package | Manage Research Outputs | Generalization: nét liền, tam giác rỗng |
| Generate & Review Manuscript Draft | Manage Research Outputs | Generalization: nét liền, tam giác rỗng |
| Approve Manuscript for External Use | Generate & Review Manuscript Draft | Extend: nét đứt, mũi tên Open |
| Perform Automated Manuscript Review | Generate & Review Manuscript Draft | Extend: nét đứt, mũi tên Open |
| View Project | Manage Research Project | Generalization: nét liền, tam giác rỗng |
| Create Project | Manage Research Project | Generalization: nét liền, tam giác rỗng |
| Update Project | Manage Research Project | Generalization: nét liền, tam giác rỗng |
| View Data Card | Manage Dataset | Generalization: nét liền, tam giác rỗng |
| View Dataset Versions | Manage Dataset | Generalization: nét liền, tam giác rỗng |
| Manage Members | Manage Research Project | Generalization: nét liền, tam giác rỗng |
| Archive Project | Manage Research Project | Generalization: nét liền, tam giác rỗng |
| View Hypotheses | Manage Hypotheses | Generalization: nét liền, tam giác rỗng |
| Evaluate Hypotheses | Manage Hypotheses | Generalization: nét liền, tam giác rỗng |
| Refine Hypothesis | Manage Hypotheses | Generalization: nét liền, tam giác rỗng |
| View Research Finding | Manage Research Findings | Generalization: nét liền, tam giác rỗng |
| Run Benchmark | Manage Evaluation | Generalization: nét liền, tam giác rỗng |
| View Evaluation Results | Manage Evaluation | Generalization: nét liền, tam giác rỗng |
| Run Ablation Study | Manage Evaluation | Generalization: nét liền, tam giác rỗng |
| View Users | Manage Users & Roles | Generalization: nét liền, tam giác rỗng |
| Assign Roles | Manage Users & Roles | Generalization: nét liền, tam giác rỗng |
| Manage Roles | Manage Users & Roles | Generalization: nét liền, tam giác rỗng |
| View Model Configuration | Manage AI Configuration | Generalization: nét liền, tam giác rỗng |
| Configure AI Model | Manage AI Configuration | Generalization: nét liền, tam giác rỗng |
| View System Logs | Monitor System | Generalization: nét liền, tam giác rỗng |
| View System Health | Monitor System | Generalization: nét liền, tam giác rỗng |
| View Usage & Cost | Monitor System | Generalization: nét liền, tam giác rỗng |
| Generate Hypotheses | Create Idea Record | Include: nét đứt, mũi tên Open |
| Select Analysis Method | Check Assumptions | Include: nét đứt, mũi tên Open |
| Run Experiment | Record Execution Trace | Include: nét đứt, mũi tên Open |
| Assess Idea Novelty | Generate Hypotheses | Extend: nét đứt, mũi tên Open |
| Review Evidence Decision | Review Experiment Result | Extend: nét đứt, mũi tên Open |
| Clean Dataset | Manage Dataset | Generalization: nét liền, tam giác rỗng |
| Review Hypothesis Decision | Select Hypothesis | Extend: nét đứt, mũi tên Open |

### 5.4 Xóa các association actor cũ, vẽ lại theo §3

Để không sót đường sai sau khi đổi nhãn: xóa các association actor–oval hiện tại rồi vẽ lại đúng cột actor của §3. Không giữ mặc định `Researcher — Manage Evaluation`: benchmark thuộc Platform Admin (UC-29). Không giữ `Decision Model Provider — Select Hypothesis/Evaluate Hypotheses`. Không thay ba đường của AI Provider bằng LLM provider: dùng các association của Persona theo §3.

Kết quả giữa các oval chỉ còn include UC-06 → Validate uploaded dataset; giữa các actor chỉ còn generalization PM → Researcher. Các đường còn lại đều là association actor–UC theo §3.

## 6. Những cặp tuyệt đối không nối bằng include/extend

| Không vẽ đường | Thay bằng note ở cạnh oval |
|---|---|
| UC-36 Export → UC-35 Approve bằng include | UC-36: `Precondition: current Dossier version approved; export requires a pinned user decision` |
| UC-11 Accept → UC-27 Review bằng include | UC-11: `Precondition: all contract checks green and independent review completed` |
| UC-21 Lock → UC-22 Execution để thể hiện bước sau | UC-22: `Precondition: a Lock exists`; không vẽ mũi tên thứ tự |
| UC-18 → UC-19 → UC-20 → UC-22 → UC-25 thành chuỗi include | Ghi text nhỏ: `dataset_first pipeline; order defined in activity diagram` |
| UC-18 include cả UC-06/07/08 | Ghi chú các cách lấy dữ liệu là lựa chọn theo trường hợp; không phải cả ba đều bắt buộc |
| UC-27 extend UC-25 | Review không phải tùy chọn của paper; review áp dụng cho object version của mọi stage |
| UC-35 extend UC-25 | Dossier approval là mục tiêu riêng, có actor và điều kiện riêng |

## 7. Note quyền cần đặt trên sơ đồ

Chỉ dùng text/UML Note, không biến các dòng sau thành oval mới:

1. `PM inherits Researcher capabilities (BR-80).`
2. Cạnh UC-13: `Researcher: own run only; PM: any project run.`
3. Cạnh AI PI/UC-17: `Tentative unpinned decisions only when autopilot + away; no pinned decisions or run termination.`
4. Cạnh Platform Admin: `Project metadata only unless also a project member.`
5. Cạnh UC-35: `Approvals bind one Dossier version and follow project review settings; new version requires new approval.`
6. Cạnh UC-34: `Admin sets system spending ceiling; PM reads project ledger.`
7. Cạnh UC-30: `Local rows stay on Local Node; only aggregates passing release gate may leave.`
8. Cạnh UC-26: `User decides submission; no automatic publisher submission.`

## 8. Trình tự thao tác và kiểm tra cuối

1. Sửa boundary và actor theo §1–2.
2. Xóa đường UC–UC ở §5.3 và association actor cũ ở §5.4; giữ include upload–validate.
3. Đổi tên 20 oval, thêm 21 oval theo §3; xóa các oval liệt kê ở §4. Không thêm module box.
4. Vẽ lại association actor–UC đúng từng dòng §3; thêm PM generalization và chỉnh include ở §5.
5. Đặt notes §6–7; giữ UC-40/41 có nhãn sau MVP.
6. Kiểm tra: đủ 41 mã UC duy nhất + một helper validate; actor ở ngoài, oval ở trong; không có Google/Email; đường chạm biên ellipse, không xuyên chữ/hình.
7. Lưu editable `.drawio`, xuất PNG và kiểm tra hình sau khi tự vẽ.

Phương án này không cần sửa BRD/PRD/Use Case Spec. Danh sách actor–UC là cách trình bày cụ thể dựa trên quyền và flow của tài liệu nguồn; không tạo role hoặc quyền mới.

## 9. Kết quả đối chiếu với xFA26SE115_Report7.md

Đây là rà soát phục vụ diagram/checklist; không phải audit toàn bộ hơn 690 KB của Report7. File Report7 trong Downloads và diagram không bị sửa.

| Nội dung kiểm tra | Kết quả / quyết định |
|---|---|
| Bảng UC-01–UC-41, tên, actor đại diện, FE và FR | Khớp 41/41 với bảng trong `report/03-software-requirements-specification.md`, sau khi chuẩn hóa escape Markdown như `experiment\_design` |
| Actor maker của stage | Checklist trước bỏ sót Persona của UC-18/19/20/22/25/41. Đã thêm một actor Persona dùng chung; UC-27 dùng vai trò guard của cùng actor |
| LLM provider | Là gợi ý mô hình hóa trước đó, không phải actor được liệt kê trong Report III §2.1. Bỏ khỏi phương án Use Case mặc định, dùng Persona theo report |
| UC-01 Sign in | Actor là any user; SC-01–03 cũng cho Guest truy cập. Checklist dùng một actor User để bao phủ người chưa đăng nhập; không cần Google/Email actor |
| UC-06 Validate uploaded dataset | Kiểm tra format/size/readable table ở main flow bước 2. Include là cách tách hành vi hỗ trợ do checklist đề xuất, không phải report có thêm một UC mang mã riêng |
| PM → Researcher | Có nguồn BR-80 và bảng actor/permission của Report III; giữ generalization |
| UC-13, UC-23, UC-34, UC-35, UC-37 | Phải dùng actor đầy đủ trong descriptions, không chỉ cột actor đại diện của bảng tổng hợp; checklist đã thể hiện |
| Điều kiện acceptance/export | Giữ precondition; Report không buộc phải vẽ include từ Accept tới Review hoặc Export tới Approve |
| Số oval và đường đề xuất xóa | Là phương án tinh gọn về 41 UC + helper validate, không phải yêu cầu xóa chức năng khỏi sản phẩm. Giữ bố cục cụm, chỉ bỏ tầng Manage/hành vi con không còn là UC độc lập |

Hai lỗi trình bày trong chính Report7 cần người dùng chỉnh khi hoàn thiện report:

1. Sau heading **III 2.2.2 Descriptions**, phần Sign in bắt đầu ngay bằng Goal, thiếu heading **UC-01 Sign in**. Thêm heading này trước Goal, tương tự UC-02–UC-41. Bảng tổng hợp vẫn có UC-01 nên không phải thiếu nội dung flow.
2. Sau permission matrix ở **III 2.1**, có ký tự `a` đứng riêng trong khi ô Approve Dossier dùng `[a]`. Nên thay bằng chú thích đầy đủ: `Approvals follow project review settings: required count, eligible approvers and whether self-approval is allowed (BR-63).`

Các màn SC-19 Decision providers hoặc chức năng gửi email trong phần screen/non-screen không tự động trở thành actor/use case mới. Chúng không phải lý do phục hồi Decision Model Provider như actor quyết hypothesis, hoặc đưa Google/Email trở lại diagram.

# Rule: Optional diagrams

## Expanded context — Report7 I/II

Theo yêu cầu ngày 2026-11-01, sửa trực tiếp tab `main-2` trong
`System-Context-Diagram.drawio`: giữ một ellipse OpenAI-Scientist ở giữa,
bốn vai trò và bốn đầu mối hệ thống bên ngoài theo bố cục gốc; mở rộng
canvas và khoảng cách để chứa đầy đủ mũi tên. Không dùng tab thẻ module.

- Nguồn: `C:\Users\ADMIN\Downloads\FA26SE115_Report7.md`, I §6.1 và II §1.1.
- Snapshot giữ nguyên 81 chức năng gốc; view tập trung nghiệp vụ nghiên cứu.
  `display_excluded_source_ids` bỏ FE-01 (login/access) và FE-15
  (comments/notifications) khỏi view, không xóa requirement nguồn.
- Gom 75 chức năng còn lại thành 49 luồng theo cùng actor, chiều trao đổi
  và ý nghĩa nghiệp vụ; thêm 20 trao đổi hỗ trợ, gồm quyết định duyệt hồ sơ
  của Project Manager theo FE-14.2. CRUD cùng đối tượng dùng
  `Manage …`; các quyết định lock, approval và export giữ riêng.
- Điều chỉnh cục bộ ngày 2026-11-02: chỉ tách các luồng của Literature &
  Evidence Sources (4), External Data Sources (6), Platform Administrator (8)
  và Large Language Model Provider (6). Tổng view 69 luồng; giữ nguyên các
  actor/luồng khác và ba tab còn lại. Metadata nguồn được giữ trên từng luồng
  tách; một chức năng nguồn có thể xuất hiện trên nhiều trao đổi cụ thể.
  Giữ input phía trên/output phía dưới; Admin cao 190 px để đủ chỗ nhãn,
  các cổng và hành lang nối chỉ điều chỉnh trong bốn actor này.
- Không hiện mã FE trên nhãn. `data-fe` giữ danh sách mã nguồn của mỗi luồng;
  `data-source-text` giữ nguyên văn chức năng, `data-wbs` giữ đối chiếu phần II.
- Snapshot chứa `compact_flows` định nghĩa tường minh cách gom; không gộp
  ngầm theo chuỗi chữ hoặc tự bỏ chức năng.
- [Snapshot và ánh xạ luồng](functional_scope.json),
  [builder](build_context_diagram.py),
  [PNG](System-Context-Diagram-main-2.drawio.png).
  Builder chỉ thay nội dung tab `main-2`, giữ ba tab còn lại.
- WBS phần II dùng đối chiếu phạm vi, không biến công việc thiết kế,
  frontend, testing/deployment thành actor hay chức năng nghiệp vụ mới.
- Trang mở rộng dùng ký pháp ellipse/rectangle theo ảnh mẫu thứ hai người
  dùng cung cấp ngày 2026-11-02, thay bố cục các hộp xếp cột. Không áp dụng
  ký pháp C4 Person/Software System của hướng dẫn cũ bên dưới.
- Ellipse trung tâm 800 × 650 px. Project Manager và Reviewer ở phía trên;
  Researcher bên trái; Literature/Data ở bên phải lệch x/y; Platform Admin
  dưới bên phải; AI/LLM Provider dưới bên phải, nối từ cạnh trái vào ellipse.
  Theo điều chỉnh mới nhất, Local Node chuyển sang dưới bên trái tại
  x=500, y=1680, nối cạnh phải qua các hành lang riêng lên đáy ellipse.
  Admin y=1280; AI/LLM tại x=2700, y=1680, ngang hàng Local Node,
  kéo vào trong 130 px. Cổng AI/LLM trên đáy ellipse tại x=1850–1880,
  tách khỏi cụm Admin x=1963–2012; giữ nguyên các actor còn lại.
- Nối theo mẫu: actor → đoạn ngang có nhãn → gấp vuông gần hệ thống →
  ellipse (hoặc chiều ngược lại). Cổng nằm trên cạnh hướng vào hệ thống;
  Researcher vẫn dùng trên/phải/dưới để chứa 27 luồng. Không bắt buộc chia
  đều ba cạnh cho các ô còn lại hoặc xếp các hộp thẳng hàng.
- Thứ tự luồng trên từng actor: input vào hệ thống ở trên, output hệ thống
  trả actor ở dưới; không xen kẽ. Sort ổn định theo chiều, giữ thứ tự nghiệp vụ
  trong cùng nhóm; giữa hai nhóm có khoảng đệm nhỏ. Researcher có 8 input
  nối cạnh trên, 10 output cạnh phải và 9 output cạnh dưới.
  Mười output cạnh phải nối ngang thẳng: cổng actor cùng y với đường nối,
  không thêm đoạn gấp nhỏ sát hộp.
- Bố cục thu hẹp ngang: ellipse x=1370, PM x=400; các actor phải dịch
  vào 470 px so với bản trước. Giữ kích thước hộp, ellipse và cỡ chữ;
  rút chiều dài đường ngang, không scale nhỏ toàn ảnh.
- Nhãn phải là cụm danh từ chỉ request, dữ liệu, quyết định hoặc kết quả;
  không dùng `Manage …` trên đường nối. Tránh viết tắt AI/PI/ML/LLM hoặc
  tên artifact CamelCase; dùng cách diễn đạt đầy đủ, dễ đọc tương đương.
  `actor_display_names` đổi tên hiển thị nhưng giữ actor key ổn định.
- `Confirmatory results and disclosure status` biểu diễn kết quả/trạng thái
  mở sau kiểm tra, không suy ra mọi lần mở đều cần duyệt. Review reports là
  báo cáo hệ thống gửi Reviewer; Project Manager có luồng quyết định duyệt
  research dossier theo chính sách dự án. Các quyền/requirement gốc không đổi.
- Đường 1.4 px, đầu classic tô đen cỡ 9; nhãn native cỡ 18 px, nền trắng
  vừa chữ, nằm giữa đoạn ngang. Metadata nguồn nằm trên chính edge.
- Canvas lớn phục vụ xem/zoom đầy đủ, không thu nhỏ để in A4. Nguồn và ánh
  xạ để trong metadata/tài liệu, không hiển thị ghi chú kỹ thuật trên ảnh.

Các diagram leader đã đặt trong `report/` nhưng không bắt buộc theo mẫu SEP490 hay Review 2. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## System Context Diagram (III 1, IV-1)
Chuẩn: C4 model mức 1 System Context.
- Tiêu đề `System Context diagram for OpenAI-Scientist`. Bắt buộc có legend.
- Hệ thống `OpenAI-Scientist` là **một** hộp duy nhất ở giữa, nền `#DAE8FC`, ghi `[Software System]` cùng mô tả.
- Xung quanh: người dùng (`C4 > Person`, ghi `[Person]`) và hệ thống ngoài (hộp nền xám, ghi `[Software System]`). Mỗi element có mô tả 1 câu.
- Mũi tên một chiều có nhãn là danh từ hoặc cụm danh từ chỉ dữ liệu, yêu cầu hoặc quyết định được trao đổi, ví dụ `Research cases`, `Model inference requests`, `Model responses`. Không dùng nhãn mơ hồ như `Data` hoặc `Uses`.
- Không vẽ thành phần bên trong hệ thống (đó là System Overview Diagram).

## Business Process Diagram – Research Pipeline (I 1.2)
Chuẩn: BPMN 2.0 (OMG), mức descriptive.
- Pool `OpenAI-Scientist`, lane theo actor (Researcher, AI PI, System).
- Task là hình bo góc, tên dạng **động từ nguyên mẫu + đối tượng**, ví dụ `Lock analysis plan`. Không dùng động từ mơ hồ như "Handle" hay "Process".
- Event: start event là vòng tròn viền mảnh, end event là vòng tròn viền đậm. Tên dạng **đối tượng + trạng thái**, ví dụ `Research case submitted`, `Paper approved`.
- Gateway là hình thoi (`X` exclusive, `+` parallel). Gateway exclusive đặt tên bằng câu hỏi, ví dụ `Checks green?`. Nhánh ra ghi câu trả lời.
- Data object (tờ giấy gập góc) cho 5 hand-off object giữa 5 stage: dataset, hypothesis, experiment_design, execution, paper.
- Sequence flow mũi tên liền; message flow giữa pool nét đứt.

## Deployment Diagram (IV-3)
Chuẩn: UML 2.5.1, mục 19 Deployments.
- Node là khối hộp 3D (`UML > Node`), stereotype `«device»` cho máy, `«executionEnvironment»` cho container/runtime. Ví dụ `«executionEnvironment» Docker`.
- Artifact (hình chữ nhật có biểu tượng tờ giấy, `«artifact»`) đặt trong node: `platform-api.jar`, `web-app`.
- Communication path giữa node là đường liền, nhãn giao thức `«HTTPS»`, `«WebSocket»`.
- Có node Local Node ở máy người dùng, tách khỏi node của server.
- Ghi môi trường (dev, staging, production) khớp Report 4.

## Process Diagram – Scrum Process (II 2.1)
- Vòng Scrum: Product Backlog → Sprint Planning → Sprint Backlog → Sprint (vòng lặp Daily Scrum) → Increment → Sprint Review → Sprint Retrospective.
- Ghi độ dài sprint và các buổi theo đúng II 2.1.

## Nguồn
- [C4 model: Notation](https://c4model.com/diagrams/notation).
- OMG, [BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/); Camunda, [Naming BPMN elements](https://docs.camunda.io/docs/components/best-practices/modeling/naming-bpmn-elements/).
- OMG UML 2.5.1, §19 Deployments; [uml-diagrams.org: Deployment Diagrams](https://www.uml-diagrams.org/deployment-diagrams.html).
- K. Schwaber, J. Sutherland, [The Scrum Guide 2020](https://scrumguides.org/scrum-guide.html).

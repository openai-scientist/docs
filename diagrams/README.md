# Diagrams

Source diagrams for [Report 7](../deliverables/FA26SE115_Report7.docx), drawn in draw.io.
Each slot in the report shows `IMAGE TO BE ADDED — <diagram name>`; the file name below matches that name.
Sources: SEP490 report template (T) and the SWP490 Review 2 guide (R2).

## Common rules (bắt buộc cho mọi diagram)

Mỗi folder có `rule.md` riêng cho loại diagram đó; các quy tắc dưới đây áp dụng thêm cho tất cả.

**File và tên**
- Mỗi `.drawio` chỉ chứa 1 diagram (1 page), trừ Screen Flow được gộp ba tab theo [rule riêng](02-screen-flow/rule.md). Tên `<Diagram-Type>-<Subject>.drawio`, ví dụ `Sequence-Diagram-Sign-In.drawio`.
- Export PNG cùng tên, cùng folder: `File > Export as > PNG`, Zoom 200%, Border 20 px, nền trắng, bỏ chọn "Transparent background". Report chỉ chèn PNG này.
- Nội dung theo `report/`: tên actor, UC, FE, entity, state, message lấy đúng chữ trong report (tiếng Anh). Code khác report thì báo leader, không tự vẽ theo code.

**Khung và tiêu đề**
- Diagram UML có frame theo UML 2.5.1: hình chữ nhật bao ngoài, góc trên trái là pentagon ghi `<kind> <name>`. Kind dạng viết tắt của spec: `uc` (use case), `sd` (interaction), `stm` (state machine), `act` (activity), `pkg` (package), `cmp` (component), `dep` (deployment). `class` không có dạng viết tắt nên ghi đủ. Ví dụ `sd Sign In`.
- Diagram không phải UML (C4, BPMN, ERD, Screen Flow) có tiêu đề nêu loại và phạm vi, ví dụ `Container diagram for OpenAI-Scientist` (khuyến nghị của C4).
- Không đặt caption "Figure …" trong ảnh vì report đã có caption.

**Style**
- Font Arial (Helvetica), chữ thường 11 pt, tên element 12 pt, tiêu đề frame 12 pt bold. Chữ trong ảnh không nhỏ hơn 10 pt khi in A4.
- Đường nối màu đen `#000000`, độ dày 1 pt. Element nền trắng, viền đen 1 pt.
- Chỉ dùng tối đa 1 màu nhấn, `#DAE8FC` viền `#6C8EBF` (blue nhạt của draw.io), để đánh dấu phần trọng tâm. Màu không được là cách duy nhất để phân biệt ý nghĩa.
- Đường nối dùng `orthogonalEdgeStyle` (vuông góc), không chéo nhau nếu tránh được, không đi xuyên qua element.
- Căn lưới: bật `Grid` 10 px, các element cùng hàng/cột phải thẳng hàng.
- Kích thước vừa 1 trang A4 dọc (rộng tối đa ~1600 px ở zoom 100%). Quá lớn thì tách diagram, không thu nhỏ chữ.
- Diagram có ký hiệu đặc biệt hoặc dùng màu phải có legend ở góc dưới phải. Riêng C4 thì luôn phải có legend.
- Màu dùng nhất quán giữa các diagram, và ảnh phải đọc được khi in đen trắng.

**Nguồn chung**
- OMG, [UML 2.5.1 specification](https://www.omg.org/spec/UML/) (formal/17-12-05). Frame kind lấy theo [OMG issue UMLR-670](https://issues.omg.org/issues/UMLR-670).
- Scott W. Ambler, *The Elements of UML 2.0 Style* (Cambridge University Press, 2005). Bản online là [agilemodeling.com/style](https://agilemodeling.com/style/).
- [uml-diagrams.org](https://www.uml-diagrams.org/), bản giải thích UML 2.5 theo từng mục của spec.

**Kiểm tra trước khi nộp**
- [ ] Tên file, frame, nội dung khớp `report/` và ô ảnh trong report.
- [ ] Đúng ký hiệu theo `rule.md` của folder.
- [ ] PNG đã export lại sau lần sửa cuối.
- [ ] Hướng dẫn Review 2 yêu cầu sơ đồ lưu dạng mã nguồn và nêu Mermaid hoặc PlantUML. Đã xác nhận với GVHD rằng draw.io được chấp nhận.

| Folder | Diagram | Count | Report slot | Source |
|---|---|---|---|---|
| [01-use-case](01-use-case/) | Use Case Diagram | 1–3 | III 2.2.1 | T |
| [02-screen-flow](02-screen-flow/) | Screen Flow Diagram | 1 | III 3.1.1 | T |
| [03-conceptual-erd](03-conceptual-erd/) | Entity Relationship Diagram (conceptual) | 1 | III 3.1.5, IV-5 | T, R2 |
| [04-system-overview](04-system-overview/) | System Overview Diagram | 1 | IV 1.1 (IV-2) | T, R2 |
| [05-package](05-package/) | Package Diagram | 1 | IV 1.2 (IV-4) | T |
| [06-database](06-database/) | Database Diagram (tables, matches the database script) | 1 | IV 2.2 | T, R2 |
| [07-class](07-class/) | Class Diagram, one per feature group | 8 | IV 3.1.1–3.8.1 | T |
| [08-sequence](08-sequence/) | Sequence Diagram, merged where the structure is the same | ~25–30 | IV 3.x.y | T |
| [09-state-machine](09-state-machine/) | State Machine Diagram, one per main entity | 6 | IV 3.2–3.6 | R2 |
| [10-activity](10-activity/) | Activity Diagram (swimlanes), one per main workflow | 5 | IV 3.4–3.6, VI 3 | R2 |
| [11-optional](11-optional/) | System Context, Business Process, Deployment, Scrum Process | 4 | I 1.2, II 2.1, III 1, IV 1.1 | report/ |

## File checklist

### 07-class
- [ ] `Class-Diagram-Authentication-Account.drawio`
- [ ] `Class-Diagram-Project-Workspace.drawio`
- [ ] `Class-Diagram-Data-Management.drawio`
- [ ] `Class-Diagram-Research-Run-Orchestration.drawio`
- [ ] `Class-Diagram-Research-Engines.drawio`
- [ ] `Class-Diagram-AI-Principal-Investigator.drawio`
- [ ] `Class-Diagram-Notifications-Integrations.drawio`
- [ ] `Class-Diagram-Administration-Monitoring.drawio`

### 08-sequence
One file per sequence; the report lists 63 template slots (IV 3.1–3.8). Features with the same
structure share one diagram (SEP490 template rule). The leader decides the merge list and the
six slots of removed v3 features (Answer Gate, Send Back, Charter, Consultations, Endorse, Reviewer Queue).
Already in `report/`:
- [ ] `Sequence-Diagram-Lock-Plan-and-Unseal-Results.drawio` (IV-10)
- [ ] `Sequence-Diagram-Execute-Local-Job-and-Release-Aggregate.drawio` (IV-12)

### 09-state-machine
- [ ] `State-Machine-Diagram-Research-Run.drawio` (IV-7)
- [ ] `State-Machine-Diagram-Hand-off-Object.drawio` (IV-8)
- [ ] `State-Machine-Diagram-Project.drawio` (IV 3.2.14)
- [ ] `State-Machine-Diagram-Local-Node.drawio` (IV 3.3.11)
- [ ] `State-Machine-Diagram-Dossier.drawio` (IV 3.4.15)
- [ ] `State-Machine-Diagram-Decision-Item.drawio` (IV 3.6.7)

### 10-activity
- [ ] `Activity-Diagram-Execute-Research-Run.drawio` (IV-6)
- [ ] `Activity-Diagram-Handle-Decision-Request.drawio` (IV-9)
- [ ] `Activity-Diagram-Independent-Review-Process.drawio` (IV-11)
- [ ] `Activity-Diagram-Budget-Control.drawio` (IV-13)
- [ ] `Activity-Diagram-Dossier-Approval-and-Export.drawio` (IV-14)

### 11-optional
- [ ] `System-Context-Diagram.drawio` (III 1, IV-1)
- [ ] `Business-Process-Diagram-Research-Pipeline.drawio` (I 1.2)
- [ ] `Deployment-Diagram.drawio` (IV-3)
- [ ] `Process-Diagram-Scrum-Process.drawio` (II 2.1)

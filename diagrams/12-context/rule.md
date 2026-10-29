# Rule: Optional diagrams

Các diagram leader đã đặt trong `report/` nhưng không bắt buộc theo mẫu SEP490 hay Review 2. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## System Context Diagram (III 1, IV-1)
Chuẩn: C4 model mức 1 System Context.
- Tiêu đề `System Context diagram for OpenAI-Scientist`. Bắt buộc có legend.
- Hệ thống `OpenAI-Scientist` là **một** hộp duy nhất ở giữa, nền `#DAE8FC`, ghi `[Software System]` cùng mô tả.
- Xung quanh: người dùng (`C4 > Person`, ghi `[Person]`) và hệ thống ngoài (hộp nền xám, ghi `[Software System]`). Mỗi element có mô tả 1 câu.
- Mũi tên một chiều có nhãn cụ thể dạng động từ + dữ liệu, ví dụ `Submits research case`, `Returns model completion`. Không dùng nhãn "Uses".
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

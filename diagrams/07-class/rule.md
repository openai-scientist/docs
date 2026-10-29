# Rule: Class Diagram

Chuẩn: UML 2.5.1, mục 9 Classification và 11 Structured Classifiers. Mẫu SEP490 Report 4 mục 3.x.1 (class diagram cho từng feature). Vị trí: IV 3.1.1 … IV 3.8.1. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện các class (controller, service, repository, model) tham gia vào một feature, cùng thuộc tính, phương thức chính và quan hệ giữa chúng.

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Class | `UML > Class` 3 ngăn | Ngăn 1: tên là **danh từ số ít, đầy đủ**, viết PascalCase, in đậm, căn giữa. Thêm stereotype nếu có, đặt phía trên tên (`«controller»`, `«service»`, `«repository»`, `«entity»`). Ngăn 2: thuộc tính. Ngăn 3: phương thức. |
| Thuộc tính | `visibility name : Type [multiplicity] = default` | Tên camelCase. Visibility: `+` public, `-` private, `#` protected, `~` package. Ví dụ `- status : RunState`, `- tags : String [0..*]`. |
| Phương thức | `visibility name(param : Type) : ReturnType` | Tên bắt đầu bằng **động từ mạnh**, camelCase. Ví dụ `+ cancelRun(runId : UUID) : void`. Thành viên static thì gạch chân. |
| Interface | Class có `«interface»` | Tên in nghiêng nếu abstract. |
| Enum | Class có `«enumeration»` | Liệt kê giá trị, ví dụ các state của RunState. |
| Association | Đường liền, multiplicity hai đầu (`1`, `0..1`, `*`, `1..*`) | Có tên vai trò nếu cần. |
| Aggregation | Đường liền, đầu thoi rỗng | Phần có thể tồn tại độc lập. |
| Composition | Đường liền, đầu thoi đặc | Phần chết theo toàn thể. |
| Generalization | Đường liền, tam giác rỗng | Kế thừa. |
| Realization | Nét đứt, tam giác rỗng | Class hiện thực interface. |
| Dependency | Nét đứt, đầu mũi tên mở | Dùng tạm thời (tham số, gọi hàm). |

## Bố cục
- Một diagram cho mỗi nhóm feature (8 file). Class dùng chung (User, Project) chỉ ghi ngăn tên, không lặp thuộc tính.
- Xếp theo tầng: controller trên, service giữa, repository/entity dưới.
- Mỗi class chỉ ghi thuộc tính và phương thức liên quan tới feature, tối đa khoảng 8 dòng mỗi ngăn.

## Không được
- Getter/setter, constructor, import.
- Dùng mũi tên association có hướng khi không cần chỉ hướng điều hướng.
- Class không có trong code hoặc thiết kế IV 3.

## Checklist
- [ ] Tên class và method khớp code (hoặc IV 3 nếu chưa code).
- [ ] Mọi association có multiplicity.
- [ ] Class xuất hiện trong Sequence Diagram của feature đó đều có trên Class Diagram.
- [ ] Multiplicity có giá trị min và max thì xem lại xem có thật sự đúng nghiệp vụ không.

## Nguồn
- OMG UML 2.5.1, §9 Classification, §11 Structured Classifiers.
- Ambler, [UML 2 Class Diagramming Guidelines](https://agilemodeling.com/style/classDiagram.htm).
- [uml-diagrams.org: Class Diagrams](https://www.uml-diagrams.org/class-diagrams-overview.html).

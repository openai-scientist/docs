# Rule: State Machine Diagram

Chuẩn: UML 2.5.1, mục 14 StateMachines (behavior state machine). Review 2: một state machine cho mỗi thực thể chính có vòng đời; prompt self-review kiểm tra state trong code thiếu trên diagram, transition không có FR kích hoạt, state không có lối ra. Vị trí: IV 3.2.14, 3.3.11, 3.4 (IV-7, IV-8), 3.4.15, 3.6.7. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện mọi trạng thái của một thực thể, sự kiện chuyển trạng thái và điều kiện, theo đúng bảng state trong report.

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Frame | `stm <Entity>` | Ví dụ `stm Research Run`. Mỗi file chỉ một entity. |
| Initial | Chấm tròn đen, đặt **góc trên trái** | Đúng một. State machine cấp cao nhất luôn có cả initial và final. |
| State | Hình chữ nhật bo góc | Tên ngắn gọn nhưng đủ nghĩa, đúng chữ trong report, kể cả dạng code: `running`, `waiting(decision)`, `ended(with_gaps)`. |
| Final | Chấm đen trong vòng tròn, đặt **góc dưới phải** | Sau các state kết thúc (`ended(...)`, `accepted`). |
| Composite state | State lớn chứa state con | Dùng khi nhiều state chung một lối ra, ví dụ `waiting` chứa `decision`, `node_offline`, `budget_review`; `ended` chứa 4 kết quả. |
| Transition | Mũi tên liền | Nhãn theo cú pháp UML `trigger [guard] / effect`, kèm FR. Event viết **thì quá khứ**: `user answered [item pinned] / resume run (FR-262)`. Effect của phần mềm dùng tên theo code (`resumeRun()`), effect do người làm viết văn xuôi. Không có trigger thì transition chạy khi state hoàn tất. |
| Guard | `[điều kiện]` | Guard trên các transition cùng event **không được trùng nhau**. Đặt tên guard nhất quán giữa các diagram. Guard không có tác dụng phụ. |
| Choice / Junction | Hình thoi / chấm đen nhỏ | Khi một event dẫn tới nhiều state theo điều kiện, để gom guard về một chỗ. |

## Bố cục
- Luồng chính đi trái sang phải hoặc trên xuống; state lỗi/huỷ đặt dưới.
- Nhãn transition đặt gần state nguồn: phía trên đường đi trái→phải, phía dưới đường đi phải→trái, bên phải đường đi xuống, bên trái đường đi lên.
- Transition dùng chung từ nhiều state (ví dụ cancel từ mọi state chưa ended) vẽ một lần từ composite state, không vẽ lặp.

## Không được
- State không có trong report/code, hoặc thiếu state có trong code.
- Transition không có nhãn event.
- State "hố đen" (có đường vào, không có lối ra, mà không phải state kết thúc) và state "phép màu" (có lối ra, không có đường vào, mà không phải initial).
- Dùng ký hiệu activity (action, fork) trong state machine.

## Checklist
- [ ] Đối chiếu từng dòng của bảng state trong IV 3.4.2/3.4.3 hoặc FR tương ứng.
- [ ] Mỗi transition có FR kích hoạt.
- [ ] Đủ một initial; mỗi state không final có ít nhất một lối ra.
- [ ] Mỗi transition có 1 test case (yêu cầu số test case của Review 2, mục 9.3).

## Nguồn
- OMG UML 2.5.1, §14 StateMachines.
- Ambler, [UML 2 State Machine Diagramming Guidelines](https://agilemodeling.com/style/stateChartDiagram.htm).
- [uml-diagrams.org: State Machine Diagrams](https://www.uml-diagrams.org/state-machine-diagrams.html).

# Rule: Sequence Diagram

Chuẩn: UML 2.5.1, mục 17 Interactions. Mẫu SEP490 Report 4 mục 3.x.y (feature có cùng cấu trúc thì vẽ một lần). Vị trí: IV 3.x.2 trở đi. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện thứ tự message giữa actor và các object/class để thực hiện **một** use case hoặc chức năng, gồm luồng chính và các nhánh lỗi quan trọng.

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Frame | `sd <Tên chức năng>` | Trùng tên file và tên ô ảnh trong report. |
| Actor | Stick figure + lifeline | Actor người và actor chủ động khởi tạo đặt **ngoài cùng bên trái**. Hệ thống ngoài chỉ phản hồi (LLM provider, email, Google) đặt **ngoài cùng bên phải**. Tên khớp Use Case Diagram. |
| Lifeline | `UML > Lifeline`, đường dọc nét đứt | Tên dạng `name : ClassName`. Có thể bỏ `name` thành `: ClassName`, nhưng phải ghi name khi message có nhắc tới object đó, hoặc khi có nhiều object cùng class. ClassName đúng class trên Class Diagram. Xếp theo tầng từ trái sang phải: Actor → UI → Controller/API → Service → Repository → Database/dịch vụ ngoài. |
| Activation | Thanh chữ nhật hẹp trên lifeline | Từ lúc nhận message tới lúc trả kết quả. |
| Synchronous message | Mũi tên liền, đầu **đặc** | Message phần mềm ghi **chữ ký hàm**: `startRun(caseId)`, ưu tiên tên tham số thay vì kiểu. Message từ người dùng ghi **văn xuôi**: `Clicks "Start run"`. Nhãn đặt cạnh đầu mũi tên. |
| Asynchronous message | Mũi tên liền, đầu **mở** | Event, queue, notification. |
| Reply | Mũi tên **nét đứt**, đầu mở | Chỉ vẽ khi giá trị trả về không hiển nhiên hoặc được dùng lại ở message sau. Ghi giá trị hoặc kiểu: `run`, `201 Created`. Có thể ghi thay trong message gốc: `run := startRun(caseId)`. |
| Create / Destroy | Message `«create»` tới đầu lifeline; `X` ở cuối lifeline | Khi object được tạo hoặc huỷ. |
| Combined fragment | Khung có nhãn góc trái | `alt` (điều kiện, chia bằng nét đứt, mỗi nhánh `[guard]`), `opt` (tuỳ chọn), `loop` (`loop [điều kiện]`), `par` (song song), `ref` (gọi diagram khác). |

## Bố cục
- Thời gian chạy từ trên xuống. Message không đi ngược lên. Message chính ưu tiên đi từ trái sang phải.
- Đánh số message `1`, `1.1`, `2` nếu diagram dài hơn 10 message.
- Nhánh lỗi chính (không đủ quyền MSG-01, dữ liệu sai) đặt trong `alt`; lỗi lặp lại ở mọi chức năng thì ghi chú, không vẽ lại.
- Quá ~20 message thì tách bằng `ref`.

## Gộp diagram
Chức năng có cùng cấu trúc (CRUD giống nhau, ví dụ Rename/Delete Dataset và Rename/Test/Delete Data Connection) dùng **một** diagram. Tên frame ghi chung, ví dụ `sd Manage Data Connection`, và ghi trong report rằng diagram áp dụng cho các chức năng nào.

## Không được
- Lifeline không có trên Class Diagram, hoặc tên message không có trong code/thiết kế.
- Dùng message nét liền cho reply.
- Vẽ chi tiết vòng lặp nội bộ của hàm.

## Checklist
- [ ] Reply chỉ vẽ khi cần, luôn là nét đứt.
- [ ] Guard của `alt`/`opt`/`loop` ghi trong `[ ]`.
- [ ] Lifeline và message khớp Class Diagram và code.

## Nguồn
- OMG UML 2.5.1, §17 Interactions (message sort, §17.4.4.1).
- Ambler, [UML 2 Sequence Diagramming Guidelines](https://agilemodeling.com/style/sequenceDiagram.htm).
- [uml-diagrams.org: Sequence Diagrams](https://www.uml-diagrams.org/sequence-diagrams.html).

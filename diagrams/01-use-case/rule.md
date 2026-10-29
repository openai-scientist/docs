# Rule: Use Case Diagram

Chuẩn: UML 2.5.1 (OMG), mục 18 Use Cases. Vị trí trong report: III 2.2.1. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện actor nào dùng chức năng (use case) nào của hệ thống, và quan hệ giữa các use case. Không thể hiện thứ tự hay luồng xử lý.

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Actor người | `UML > Actor` (stick figure) | Tên là **danh từ số ít chỉ vai trò**, không phải chức danh hay tên người. Đúng tên trong III 2.1 (Researcher, Project Manager, Reviewer, Platform Admin). |
| Actor hệ thống ngoài | Hình chữ nhật có stereotype `«system»` hoặc stick figure | Ví dụ AI PI, Local Node, Google, LLM provider. Đặt bên phải system boundary. |
| System boundary | Hình chữ nhật, tên `OpenAI-Scientist` ở trên | Mọi use case nằm trong; mọi actor nằm ngoài. |
| Use case | Ellipse | Tên **bắt đầu bằng động từ mạnh** + danh từ, dùng thuật ngữ nghiệp vụ, có mã: `UC-09 Start a run from a research case`. Đúng tên trong III 2.2. |
| Association | Đường liền, không mũi tên | Nối actor với use case họ khởi động. Spec cho phép mũi tên mở chỉ hướng khởi động, nhưng bộ diagram này không dùng. |
| Include | Mũi tên nét đứt, đầu mở, nhãn `«include»`, **từ use case gốc chỉ tới use case được include** | Chỉ dùng khi use case gốc **luôn** gọi use case kia. Use case được include đặt bên phải use case gốc. |
| Extend | Mũi tên nét đứt, đầu mở, nhãn `«extend»`, **từ use case mở rộng chỉ về use case gốc** | Chỉ dùng cho hành vi tuỳ chọn có điều kiện. Use case mở rộng đặt bên dưới use case gốc. |
| Generalization | Đường liền, đầu tam giác rỗng chỉ về phía tổng quát | Giữa actor (Project Manager → Researcher theo BR-80) hoặc giữa use case. |

## Bố cục
- Giữ cấu trúc sơ đồ cũ của người dùng trên đúng một trang trong một file `.drawio`. Không tách thành overview, module hoặc trang chi tiết theo nhóm FE. Khi cập nhật nghiệp vụ, sửa trực tiếp các actor, use case và quan hệ cần thiết trong bố cục hiện có; chỉ điều chỉnh vị trí cục bộ khi cần tránh chồng lấn.
- Phong cách theo ảnh tham chiếu của người dùng: một khung hệ thống lớn theo chiều dọc; Project Manager và Researcher ở bên trái, actor hỗ trợ và quản trị ở bên phải; các ellipse tạo thành cụm chức năng chính–phụ, rải quanh use case trung tâm của từng cụm. Giữ nền trắng, nét mảnh, chữ đen và bố cục tổng thể hiện có; không chuyển sang danh sách ellipse xếp đều thành một cột.
- Đường association từ actor tỏa tới use case liên quan, dừng ở biên ellipse; bố trí include/extend gần cụm tương ứng để tránh đi xuyên hình. Hình tham chiếu định hướng bố cục, không thay thế quy tắc ngữ nghĩa UML hoặc tên/quyền trong BRD, PRD và Report III.
- Actor chính và use case chính ở góc trên trái. Actor phụ và hệ thống ngoài bên phải.
- Use case thường xảy ra trước đặt cao hơn.
- Actor không nối trực tiếp với actor (ngoại trừ generalization).
- Use case cùng FE đặt gần nhau thành cụm trong cùng khung hệ thống; không thêm package/module box chia vùng.
- Khi có nhiều use case, mở rộng vùng vẽ và điều chỉnh khoảng cách trong cùng trang; không tự tách diagram theo nhóm FE hoặc tạo overview.

## Không được
- Vẽ luồng, thứ tự bước, hoặc nối use case với use case bằng đường liền.
- Dùng `«include»`/`«extend»` để chia nhỏ chức năng thành bước.
- Đặt màn hình, bảng dữ liệu hay tên API vào use case.

## Checklist
- [ ] Tất cả UC-01 … UC-41 trong III 2.2 có mặt (gồm cả use case *after MVP*, ghi chú `(after MVP)`).
- [ ] Mỗi use case có ít nhất một actor.
- [ ] Hướng mũi tên include/extend đúng.

## Nguồn
- OMG UML 2.5.1, §18 UseCases.
- Ambler, [UML 2 Use Case Diagramming Guidelines](https://agilemodeling.com/style/useCaseDiagram.htm).
- [uml-diagrams.org: Use Case Diagrams](https://www.uml-diagrams.org/use-case-diagrams.html).

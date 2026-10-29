# Rule: Sequence Diagram

Chuẩn: UML 2.5.1, mục 17 Interactions. Mẫu SEP490 Report 4 mục 3.x.y (feature có cùng cấu trúc thì vẽ một lần). Vị trí: IV 3.x.2 trở đi. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích và phạm vi
Thể hiện thứ tự tương tác để thực hiện **một** use case hoặc chức năng, gồm luồng chính và các nhánh lỗi quan trọng. Giữ một file editable `.drawio` / một page / một sequence và PNG cùng tên theo quy tắc chung; không tạo thêm overview hoặc bộ diagram khác khi chưa có yêu cầu.

- Nội dung nghiệp vụ, actor, quyền và flow lấy từ [Report III](../../report/03-software-requirements-specification.md); phạm vi thiết kế và ô ảnh lấy từ [Report IV](../../report/04-software-design-document.md). Đối chiếu [Class Diagram](../07-class/rule.md) khi đặt participant và operation.
- Phân biệt **system sequence** (Actor → System, nhìn từ ngoài) và **design sequence** (các participant bên trong). Các ô thiết kế IV 3.x.y mặc định dùng design sequence như ảnh tham chiếu; không trộn hai mức chi tiết trên cùng page.
- Ảnh người dùng gửi ngày 2026-10-29 là tham chiếu phong cách: nền trắng, nét mảnh, actor bên trái, các participant trải ngang, call liền và reply đứt. Không lấy Admin, Audit Session, endpoint, status code hoặc lớp trong ảnh làm requirement của dự án.
- Thứ tự ưu tiên: nội dung report → quy tắc riêng tại đây → quy tắc chung → phong cách ảnh mẫu. Không sao chép lỗi ký hiệu hoặc flow từ ảnh.

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Frame | `sd <Tên chức năng>` | Trùng tên file và tên ô ảnh trong report. |
| Actor | Stick figure + lifeline | Actor khởi tạo đặt **ngoài cùng bên trái**; tên khớp Use Case Diagram. Hệ thống ngoài chỉ phản hồi đặt về bên phải participant gọi nó. Không thêm actor chỉ vì có trong ảnh mẫu. |
| Lifeline | Header chữ nhật, đường dọc nét đứt | Object ghi `name : ClassName` hoặc `: ClassName`; nhiều instance cùng lớp phải có tên phân biệt. UI, database và hệ thống ngoài được ghi bằng tên vai trò rõ nghĩa, không bắt buộc là class phần mềm. |
| Activation | Thanh chữ nhật hẹp, nền trắng trên lifeline | Bắt đầu khi nhận call xử lý, kết thúc khi hoàn thành hoặc reply. Mỗi lần xử lý riêng dùng thanh riêng; self-call lồng nhau có thanh lệch nhẹ. Không kéo thanh toàn chiều cao chỉ vì participant tồn tại. |
| Synchronous message | Mũi tên liền, đầu tam giác **đặc** | Operation nội bộ ghi `operation(parameter)`; HTTP call ghi `METHOD /path` khi có nguồn hợp đồng. Actor ghi hành động như `Clicks "Start run"`. Nhãn nằm ngay trên đoạn message, không đè đầu mũi tên. |
| Asynchronous message | Mũi tên liền, đầu **mở** | Event, queue, notification. |
| Reply | Mũi tên **nét đứt**, đầu mở | Trả từ callee về **caller trực tiếp**, ghi kết quả/status có nguồn. Trong design sequence theo ảnh, thể hiện các reply chính để thấy kết quả quay lại UI; có thể bỏ reply nội bộ hiển nhiên. Không nối Service/Database thẳng về actor khi UI đang là caller. |
| Self-message | Mũi tên quay lại cùng lifeline | Chỉ dùng cho thao tác nội bộ cần thiết để hiểu flow; không bung từng bước thuật toán. |
| Create / Destroy | Message `«create»` tới header mới; `X` kết thúc lifeline | Chỉ khi tạo/hủy **participant**. Tạo/xóa một record không tự động có nghĩa là tạo/hủy Repository hoặc Database. |
| Combined fragment | Khung có tab operator góc trái | `alt`, `opt`, `loop`, `par`; `ref` tham chiếu interaction khác. Khung phủ toàn bộ participant và message thuộc phạm vi, guard nằm trong khung. |

## Participant và mức chi tiết
- Bố cục mặc định trái → phải: Actor → Browser/Web App → Controller/API → Service → Repository → Database. Authentication hoặc hệ thống ngoài đặt gần bên sử dụng. Đây là quy ước bố cục dự án, không phải số tầng bắt buộc của UML.
- Chỉ vẽ participant thực sự tham gia; không thêm Repository, Database hoặc AuthenticationService để đủ mẫu. Không cho actor thao tác thẳng database hay bỏ qua UI đã có trong flow.
- Operation và class nội bộ phải khớp thiết kế tương ứng. Nếu thiết kế còn thiếu, ghi rõ đề xuất và nguồn đối chiếu; không biến tên tự đặt thành tên đã có trong code. Boundary, store và hệ thống ngoài không cần ép thành class.
- Chỉ ghi endpoint, payload hoặc status cụ thể khi nguồn xác nhận. Khi report chưa chốt hợp đồng, dùng nhãn hành vi như `submit request` / `result`, không tự tạo API.
- Async event dùng mũi tên mở; phản hồi chấp nhận request không phải kết quả hoàn thành job. Callback/event sau đó phải thể hiện đúng sender/receiver, không giả làm reply đồng bộ.

## Fragment và luồng lỗi
- `alt`: các nhánh loại trừ nhau nằm **trọn trong cùng một khung**, ngăn bằng đường ngang nét đứt. Mỗi operand có guard `[condition]`; có thể dùng `[else]` cho nhánh còn lại.
- Với kiểm tra quyền: call kiểm tra trước `alt`; nhánh `[denied]` trả lỗi qua Controller → UI → Actor; nhánh `[allowed]` chứa xử lý được bảo vệ và các reply tương ứng. Không đặt luồng thành công bên dưới, ngoài khung, khiến nó vẫn chạy sau lỗi.
- Chỉ đưa message ra sau `alt` nếu message đó hợp lệ sau **mọi nhánh**. Nếu cần kết thúc interaction khi lỗi, phải biểu diễn việc dừng rõ ràng, chẳng hạn bằng fragment `break`; một nhãn lỗi riêng lẻ không tự chấm dứt flow.
- `opt [condition]` cho một nhánh tùy chọn; `loop [condition]` cho thao tác lặp, như nhiều lần scan/submit nếu nguồn yêu cầu; `par` chỉ khi flow thực sự đồng thời. Không ghép các lựa chọn khác nhau bằng dấu `/` vào một call.
- `ref <interaction name>` dùng khi tách quy trình con; dẫn tới file/page tồn tại. Lỗi chung có thể dẫn về flow xác thực dùng chung, nhưng không bỏ nhánh lỗi ảnh hưởng trực tiếp đến kết quả của chức năng.

## Bố cục
- Thời gian đọc từ trên xuống, biểu diễn **thứ tự**, không phải thời lượng theo khoảng cách. Call/reply thông thường nằm ngang; self-call có đoạn quay xuống. Chiều trái/phải phụ thuộc sender/receiver, không ép mọi call sang phải.
- Header cùng hàng, lifeline thẳng đứng, activation căn tâm. Dùng thư viện UML/UML 2.5 của draw.io, Arial/Helvetica và nét đen theo quy tắc chung; không dùng bóng, gradient, màu tầng hay icon trang trí.
- Message đi qua lifeline trung gian là bình thường; tránh đi xuyên header, activation không liên quan hoặc label. Đây là ngoại lệ cần thiết của quy tắc chung về đường nối không xuyên element. Dùng connector thẳng cho message giữa hai participant; chỉ dùng tuyến vuông góc cho self-call hoặc khi cần.
- Đánh số **tất cả** message theo thứ tự hiển thị `1:`, `2:`, `3:`… như ảnh tham chiếu, kể cả reply; tiếp tục số qua các operand để nhãn duy nhất trên page. Số thứ tự không có nghĩa mọi nhánh đều chạy. Không trộn kiểu số phân cấp trong cùng page.
- Chừa khoảng giữa các hàng đủ cho nhãn và guard; tăng khoảng cách participant theo nhãn dài nhất, không thu nhỏ chữ. Có thể lặp header ở chân hình dài để dễ đọc; đó là nhãn dẫn hướng, không phải participant mới hay sự kiện create.
- Giữ giới hạn đọc/in A4 của quy tắc chung. Khoảng 20 message là mốc rà soát, không phải ngưỡng UML: có thể giữ chuỗi dài hơn như ảnh nếu vẫn rõ một chức năng; nếu không đọc được thì tách bằng `ref`, không kéo rộng canvas hoặc giảm cỡ chữ để nhét đủ.

## Gộp diagram
Chức năng có cùng participant, thứ tự tương tác và điều kiện xử lý có thể dùng **một** diagram theo mẫu SEP490. Tên frame ghi chung, ví dụ `sd Manage Data Connection`, và ghi rõ trong report diagram áp dụng cho các chức năng nào. Không gộp chỉ vì cùng nhóm CRUD: Rename, Test và Delete chỉ dùng chung khi cấu trúc và nhánh quan trọng thực sự tương đương; nếu khác thì tách. Giữ danh sách gộp do leader chốt trong [inventory](../README.md#08-sequence), không tự thay số ô ảnh hoặc UC.

## Không được
- Thêm tầng, operation, API, actor hoặc business rule chỉ dựa vào ảnh mẫu.
- Dùng reply nét liền, trả sai caller, hoặc dùng activation dài thay cho lifeline.
- Vẽ `alt` thiếu cạnh bao, guard nằm ngoài hoặc luồng thành công vẫn tiếp tục sau nhánh từ chối.
- Vẽ chi tiết vòng lặp nội bộ của hàm hoặc sao chép chuỗi call không có nguồn.

## Checklist
- [ ] Tên file/frame/ô ảnh, actor, quyền và flow khớp report; operation nội bộ khớp Class Diagram hoặc được ghi rõ là đề xuất.
- [ ] Có trigger từ actor, UI boundary và kết quả hiển thị; chỉ chứa participant cần thiết.
- [ ] Call đồng bộ đầu đặc, async đầu mở; reply nét đứt về caller trực tiếp; số message duy nhất và nhất quán.
- [ ] Activation chỉ phủ thời gian xử lý, create/destroy đúng vòng đời participant.
- [ ] Guard nằm trong `[ ]`; khung fragment bao đủ message/participant, divider và cả nhánh thành công/lỗi; lỗi không rơi tiếp vào xử lý thành công.
- [ ] Không chồng nhãn, cắt chữ hoặc connector đâm vào activation không liên quan; PNG đọc được ở kích thước chèn report.
- [ ] Khi sửa artifact: giữ editable và builder/source đồng bộ, chạy generator nếu có, validator cấu trúc rồi export PNG và xem trực quan. Không coi syntax/XML pass là render pass.
- [ ] Cập nhật changelog, kiểm tra link và `git diff --check`; ghi đúng phạm vi validation đã chạy.

## Nguồn
- Visual Paradigm, [What is Sequence Diagram?](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-sequence-diagram/) — participant, activation, message và fragment.
- draw.io, [UML sequence diagrams](https://www.drawio.com/docs/diagram-types/uml/sequence-diagrams/) — thư viện shape, connector, guard và frame.
- Ảnh sequence Admin/Audit Session do người dùng gửi ngày 2026-10-29 — chỉ tham chiếu bố cục, không phải nguồn nghiệp vụ hoặc file editable của dự án.
- OMG UML 2.5.1, §17 Interactions (message sort, §17.4.4.1).
- Ambler, [UML 2 Sequence Diagramming Guidelines](https://agilemodeling.com/style/sequenceDiagram.htm).
- [uml-diagrams.org: Sequence Diagrams](https://www.uml-diagrams.org/sequence-diagrams.html).

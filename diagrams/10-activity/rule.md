# Rule: Activity Diagram

Chuẩn tham chiếu: UML 2.5.1 §15 Activities; áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram). Review 2 yêu cầu sơ đồ cho workflow nghiệp vụ chính, thể hiện trách nhiệm của actor và hệ thống, không mô tả chi tiết nội bộ ứng dụng. Mỗi main workflow (WF-xx) có một activity diagram; đối chiếu IV 3.4–3.6 và dùng lại trong VI 3 User Manual khi phù hợp. Theo yêu cầu tổ chức giống Class Diagram, bộ tám tab theo nhóm feature bổ sung mỗi nhóm một luồng đại diện; các tab này không tự nhận là đủ năm main workflow Review 2.

## Mục đích và phạm vi

- Diễn tả thứ tự hành động, điều kiện, kết quả và bên chịu trách nhiệm từ trigger đến kết thúc workflow. Activity khác sequence: không biến sơ đồ thành chuỗi message giữa class hoặc lời gọi API.
- Chọn workflow, actor, trạng thái và nhánh từ report, use case hoặc nguồn thiết kế liên quan; ghi rõ nguồn và giới hạn. Không suy ra tính năng đã chạy hay test đã pass từ diagram.
- Theo Review 2 mục 9.1, main workflow có ít nhất 2 actor hoặc đi qua ít nhất 3 tính năng bắt buộc, và làm đổi state của ít nhất 1 thực thể chính. Ví dụ minh họa notation có thể nhỏ hơn, nhưng phải ghi rõ không phải main workflow được duyệt.
- Ưu tiên luồng chính và các decision, loop cần hiểu quy trình. Thể hiện nhánh ngoại lệ chính khi có nguồn và phù hợp phạm vi; không tự đặt ngoại lệ, state hay hành vi.

## Ký hiệu và ngữ nghĩa

| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Frame | Khung UML bao ngoài | Không dùng khung ngoài cho bộ này; tên workflow đặt ở tên trang hoặc thuyết minh. |
| Activity partition / swimlane | Swimlane dọc hoặc ngang | Một lane cho mỗi actor hoặc hệ thống thật sự thực hiện bước, tên theo nguồn; không tạo lane database để mô tả xử lý nội bộ. Ưu tiên dưới 5 lane, chia sơ đồ khi cần. Mỗi action thuộc lane người/hệ thống thực hiện; đường nối được phép qua lane. |
| Initial node | Chấm đen | Điểm bắt đầu; profile dự án ưu tiên một initial, đặt tại nơi luồng bắt đầu. |
| Activity final | Chấm đen trong vòng tròn | Kết thúc toàn bộ activity và các nhánh còn hoạt động. Có thể dùng nhiều final tại các kết quả kết thúc khác nhau; không bắt buộc mọi kết quả phải có final riêng. |
| Flow final | Vòng tròn có dấu X | Chỉ kết thúc một luồng, không kết thúc toàn activity; dùng khi ngữ nghĩa đó cần thiết. |
| Action | Chữ nhật bo góc | Tên ngắn dạng động từ + đối tượng, ở mức nghiệp vụ, ví dụ `Approve extra spend`. |
| Decision | Hình thoi | Một luồng vào, từ hai luồng ra; viết câu hỏi ngắn bên trong hình thoi. Với câu hỏi hai kết quả, đặt `[No]` bên trái và `[Yes]` bên phải; câu hỏi xác định rõ ý nghĩa hai nhánh. Với nhiều kết quả, ghi guard cụ thể, không chồng lấn và bao phủ các khả năng trong phạm vi; dùng `[else]` khi thích hợp. |
| Merge | Hình thoi | Từ hai luồng thay thế đi vào, một luồng ra; không đồng bộ các nhánh song song. Không thêm merge một vào, một ra. |
| Fork / join | Thanh đen | Fork tách một luồng thành các luồng đồng thời; join đồng bộ các luồng song song theo join specification, mặc định chờ tất cả. Không dùng merge để thay join; không đặt guard lựa chọn trên nhánh ra fork. |
| Object node / object flow | Chữ nhật vuông / mũi tên nối object với action | Chỉ đưa object nghiệp vụ cần hiểu sự chuyển giao, ví dụ `AnalysisPlan [locked]`. Đặt tại lane thích hợp; không bắt buộc nằm trên đường phân cách. Phân biệt object flow với control flow bằng ngữ cảnh, nhãn và object node; không dựa riêng vào nét đứt. |
| Control flow | Đường liền có mũi tên | Chỉ thứ tự điều khiển; guard đặt trên nhánh ra decision. |

## Bố cục và trình bày

- Chọn nhất quán hướng đọc trong một diagram: từ trên xuống với lane dọc, hoặc từ trái sang phải với lane ngang. Sắp lane theo trách nhiệm và trình tự tương tác, giữ nhãn và mũi tên dễ đọc.
- Vẽ connector trực giao khi phù hợp, tránh xuyên action, chồng đường hoặc nhãn; để khoảng trống cho loop và đầu mũi tên. Không dùng màu, kích thước object hay vị trí lane làm điều kiện UML bắt buộc.
- Với main workflow, ghi trong thuyết minh hoặc góc sơ đồ các trường Actors, Trigger, kết quả nghiệp vụ, thay đổi state, FE liên quan và Owner theo Design Brief Phụ lục A, khi có nguồn.
- Trong draw.io bật thư viện UML / UML 2.5; giữ file `.drawio` editable và xuất PNG để review. Không thay source bằng ảnh phẳng.

## Checklist

- [ ] Scope, trigger, actor, kết quả và thay đổi state có nguồn; phân biệt main workflow với ví dụ.
- [ ] Tên, trạng thái và nhánh khớp report / use case / State Machine Diagram liên quan; khác biệt hoặc giả định được ghi rõ.
- [ ] Action có đường vào và ra phù hợp; mỗi decision có guard rõ, merge không nhầm join, nhánh song song đồng bộ đúng.
- [ ] Các kịch bản cần test được truy vết; chỉ ghi đã hiện thực hoặc đã test khi có bằng chứng.
- [ ] Kiểm tra XML / kết nối, chạy validator phù hợp và xem ảnh xuất, đặc biệt đầu mũi tên, guard, các đường cắt và tính dễ đọc.

## Bộ tám nhóm

Xem [thuyết minh phạm vi và nguồn](Activity-Diagrams-design.md), [file editable tám tab](Activity-Diagrams.drawio). Mỗi tab mô tả một luồng đại diện, không phải toàn bộ use case của nhóm.

## Ví dụ để duyệt

[Sign In With Email Code — editable](Sign-In-With-Email-Code-example.drawio) · [PNG](Sign-In-With-Email-Code-example.png). Ví dụ mô tả một lần đăng nhập và nhánh sai/hết hạn; đây là ví dụ notation, không nhận là main workflow Review 2 hoặc xác nhận runtime. Nguồn nghiệp vụ: [sequence flow](../08-sequence/sequence_flows.py), [thuyết minh state](../09-state-machine/Sign-In-With-Email-Code-design.md), FR-01 và report III 3.2.1 / IV 3.1.2. Ví dụ kết thúc lần thử sau khi báo lỗi; thao tác thử lại nằm ngoài phạm vi hình.

## Nguồn

- OMG UML 2.5.1, §15 Activities.
- [Visual Paradigm: What is Activity Diagram?](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-activity-diagram/).
- [draw.io: UML activity diagrams](https://www.drawio.com/docs/diagram-types/uml/activity-diagrams/).
- Ambler, [UML 2 Activity Diagramming Guidelines](https://agilemodeling.com/style/activityDiagram.htm).
- [uml-diagrams.org: Activity Diagrams](https://www.uml-diagrams.org/activity-diagrams.html).
- SWP490, Hướng dẫn chuẩn bị Review 2, mục 03 và 9.1.

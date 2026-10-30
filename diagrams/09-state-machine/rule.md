# Rule: State Machine Diagram

Chuẩn: UML 2.5.1, §14 StateMachines (behavior state machine). Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram). Quy tắc dưới đây dùng hai tài liệu Visual Paradigm/draw.io và ảnh mẫu người dùng cung cấp để làm rõ ký hiệu, ngữ nghĩa và bố cục.

## 1. Mục đích và phạm vi

- Thể hiện vòng đời của **một thực thể hoặc một hệ thống có phạm vi rõ ràng**: đang ở trạng thái nào, sự kiện nào làm đổi trạng thái, điều kiện và kết quả đi kèm.
- Bộ diagram hiện tại giữ một file/một page cho mỗi thực thể chính: Research Run, Hand-off Object, Project, Local Node, Dossier, Decision Item; vị trí report theo [inventory](../README.md#09-state-machine).
- Nguồn nghiệp vụ là bảng state và FR trong report được chốt. Đối chiếu implementation để phát hiện thiếu/lệch nhưng không tự thay report bằng code; ghi lại mâu thuẫn để xác nhận.
- Không tạo state cho từng bước CRUD hoặc từng màn hình nếu nguồn không mô tả vòng đời tương ứng. Luồng thao tác thuộc Activity/Sequence/Screen Flow.

## 2. Cách áp dụng ảnh mẫu

Giữ cách trình bày dễ đọc của ảnh: nền trắng, nét đen, state bo góc, initial phía trên, luồng chính đi xuống, nhánh phụ sang hai bên, final phía dưới khi vòng đời kết thúc. Caption nằm trong report, không nằm trong PNG.

Ảnh có những ô như `Build list for each URL` và hình thoi `Is ADMIN?`: đây là cách trình bày thiên về flowchart. Khi áp dụng vào state machine:

- Tên ô phải diễn tả trạng thái/điều kiện đang tồn tại, ví dụ `running`, thay vì lệnh thực hiện một bước. Một hoạt động đang diễn ra có thể là state nếu nguồn xác định nó là một trạng thái của đối tượng.
- Thao tác tức thời đặt trên transition dưới dạng effect; chỉ đưa vào `entry`, `do`, `exit` khi cần mô tả hành vi của state.
- Kiểm tra điều kiện dùng guard; chỉ thêm hình thoi choice khi thật sự cần phân nhánh transition. Không tự thêm chuỗi kiểm tra đăng nhập/quyền vào mọi vòng đời.
- `Unauthorized`, `failed` hay `created` chỉ là state nếu có nghĩa trong vòng đời đang mô hình hóa; không mặc định mọi response là một state.

## 3. Ký hiệu

| Element | Ký hiệu / nội dung | Quy tắc áp dụng |
|---|---|---|
| Frame | `stm <Entity>` | Theo quy tắc chung; tên xác định đúng đối tượng của page. |
| Initial pseudostate | Chấm tròn đen | Một initial cho region cần khởi tạo, đặt phía trên trục chính. Không có đường vào, đúng một đường ra; đường ra không có trigger hoặc guard, có thể có effect khởi tạo. |
| Simple state | Chữ nhật bo góc | Tên ngắn, đúng nguồn/report, kể cả `waiting(decision)` hay `ended(with_gaps)`. |
| State behavior | Ngăn nội dung tùy chọn | `entry / ...`, `do / ...`, `exit / ...`; không cần thì chỉ để tên state. |
| Transition | Đường liền, đầu mũi tên mở chỉ về đích | Gắn đúng source/target; nhãn theo mục 4. Self-transition được phép khi có sự kiện và ý nghĩa rõ ràng. |
| Choice | Hình thoi | Rẽ nhánh tức thời theo guard trên các đường ra. Dùng `[else]` cho trường hợp còn lại khi cần; không phải một state chờ. |
| Junction | Chấm tròn đen nhỏ | Nối/gom các đoạn transition có điều kiện; phân biệt với initial bằng vị trí và kết nối. Không cần thì nối trực tiếp. |
| Composite state | State lớn chứa state con | Chỉ dùng khi nguồn có phân cấp; không gom chỉ vì tên giống nhau. Xác định lối vào/ra và khởi tạo state con. |
| Final state | Chấm đen trong vòng tròn rỗng | Region bao nó đã hoàn tất; không có đường ra. Không bắt buộc thêm final cho hệ thống hoạt động liên tục hoặc vòng đời chưa kết thúc trong phạm vi. |
| Fork / Join | Thanh đen | Hợp lệ trong state machine cho các region đồng thời; không dùng để chia các nhánh điều kiện loại trừ nhau. |
| History / Regions | `H`, `H*` / vùng phân cách nét đứt trong composite | Chỉ dùng khi nguồn yêu cầu nhớ cấu hình con hoặc hoạt động đồng thời; phải giải thích trong legend. |

Các state kết thúc nghiệp vụ vẫn giữ tên và kết quả riêng trước final, nếu nguồn có mô tả. Không ép `accepted` thành kết thúc toàn bộ vòng đời: kiểm tra transition về `stale` hoặc sang `locked` theo loại object trong [bảng object states](../../report/04-software-design-document.md#343-state-viewpoint-object-states).

## 4. Nhãn transition và điều kiện

Cú pháp: `trigger [guard] / effect`. Chỉ ghi các phần có ý nghĩa; không chèn placeholder cho phần thiếu.

- **Trigger**: sự kiện gây chuyển trạng thái, tên nhất quán với nguồn; không bắt buộc thì quá khứ hoặc tên hàm trong code. Có thể là sự kiện người dùng, hệ thống hoặc thời gian.
- **Guard**: biểu thức boolean trong `[...]`, không có tác dụng phụ. Các nhánh cùng trigger cần phân biệt rõ và bao phủ trường hợp cần xử lý; quy ước của repo là dùng điều kiện loại trừ nhau để tránh mơ hồ.
- **Effect**: hành vi xảy ra khi transition được thực hiện; chỉ ghi khi nguồn xác định. Không bắt buộc đưa tên method triển khai vào ảnh.
- Transition không có trigger chỉ dùng khi đúng ngữ nghĩa completion hoặc là đoạn qua pseudostate. Completion của state xét cả hành vi/region con nếu có; không hiểu đơn giản là cứ vào state là lập tức đi tiếp.
- Đường ra từ choice dùng guard, không gắn thêm sự kiện phải chờ. Thay `Yes/No` đơn lẻ bằng `[valid]` / `[else]` hoặc điều kiện nghiệp vụ cụ thể.
- Ánh xạ transition với FR/UC/bảng state trong tài liệu đi kèm. Chỉ đưa mã FR lên ảnh khi cần truy vết trực tiếp và không làm nhãn rối; không bịa FR cho transition kỹ thuật.

Ví dụ định dạng từ [vòng đời Research Run](../../report/04-software-design-document.md#342-state-viewpoint-run-state-machine):

| Source | Nhãn | Target | Reference |
|---|---|---|---|
| `waiting(budget_review)` | `additional spending approved` | `running` | §3.4.2, FR liên quan theo report |
| `waiting(decision)` | `wait deadline reached [pinned item unanswered]` | `ended(with_gaps)` | FR-262, FR-265 |
| State chưa `ended` | `run cancelled [authorized requester]` | `ended(cancelled)` | FR-22 |

Nhãn minh họa là mô tả sự kiện nghiệp vụ, không xác nhận tên event/API trong implementation.

## 5. Bố cục và draw.io

- Bật thư viện **UML 2.5** trong More Shapes; dùng state/pseudostate đúng loại. Giữ element editable, không thay bằng ảnh.
- Ưu tiên trục chính trên → dưới như ảnh mẫu. Nhánh lỗi, từ chối, huỷ hoặc phục hồi đặt hai bên, giữ nhãn đủ khoảng trống. Không ép mọi nhánh về final nếu nguồn cho phép retry/resume.
- Initial/final căn theo luồng chính, không cố định ở hai góc đối diện như rule cũ. Final có thể có nhiều đường vào; chỉ thêm khi đúng nghĩa hoàn tất.
- Đường nối vuông góc, tránh đi xuyên ô, chữ hoặc cắt đường khác. Đường quay lại đi ở hành lang ngoài; đầu mũi tên phải chạm đúng biên state đích.
- Nhãn gần đoạn nguồn hoặc đoạn thẳng dễ đọc; guard ở sát nhánh ra tương ứng. Không để nhãn chồng hình thoi hoặc nhánh lân cận.
- Theo font, grid, A4 và export PNG của quy tắc chung. Đen trắng là mặc định; không thu nhỏ chữ để nhét thêm state.
- Chỉ gom transition chung lên composite nếu transition thực sự áp dụng cho mọi state con trong phạm vi đó. Đặc biệt kiểm tra ngoại lệ của cancel/retry/stale.

## 6. Không được

- Biến state machine thành chuỗi thao tác kiểu `Click button → Validate input → Save database`.
- Tự thêm state/transition, mất state theo nguồn, hoặc coi mọi enum triển khai là một state của đối tượng này.
- Dùng final như điểm gộp để tiếp tục luồng, dùng choice làm nơi chờ sự kiện, hoặc dùng fork thay choice.
- Cấm toàn bộ fork/join hoặc toàn bộ transition thiếu trigger: chúng hợp lệ khi dùng đúng ngữ nghĩa UML ở trên.
- Để state không thể tới được hoặc state có đường vào nhưng không có lối ra mà không giải thích đó là trạng thái terminal/chờ trong phạm vi. Không tự tạo đường ra chỉ để đạt checklist.

## 7. Checklist trước khi hoàn tất diagram

- [ ] Phạm vi một đối tượng rõ; đối chiếu đầy đủ state/transition với report và FR/UC liên quan, nêu chỗ lệch implementation nếu có.
- [ ] Tên state diễn tả trạng thái; action, trigger, guard, effect được phân biệt.
- [ ] Initial, final, choice, composite và concurrency đúng ngữ nghĩa; không bắt buộc final khi không có kết thúc.
- [ ] Guard không gây mơ hồ; retry, recovery, cancel và terminal theo đúng nguồn.
- [ ] Mỗi state có đường tới; state không có lối ra có lý do. Không còn transition đi ra từ final.
- [ ] Có ánh xạ transition với test case theo yêu cầu Review 2; không nhầm checklist này với bằng chứng test đã chạy.
- [ ] Nhãn và mũi tên rõ, không chồng/cắt; đọc được ở kích thước chèn report.
- [ ] Nếu tạo/sửa diagram: đồng bộ builder (nếu có), editable và PNG; chạy validator phù hợp và xem ảnh export. Syntax pass không thay thế review ngữ nghĩa hoặc kiểm tra trực quan.

## 8. Nguồn và mức áp dụng

- [Visual Paradigm — What is State Machine Diagram?](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/about-state-diagrams/): phân biệt state với activity, vòng đời đối tượng, composite và history.
- [draw.io — UML state machine diagram](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/): thư viện UML 2.5, hình dạng state/pseudostate, transition và regions.
- [OMG — UML 2.5.1](https://www.omg.org/spec/UML/2.5.1): §14 StateMachines, chuẩn ngữ nghĩa nền.
- Ảnh mẫu người dùng gửi ngày 2026-10-30: tham chiếu bố cục dọc, nét đen và nhánh hai bên; không phải nguồn nghiệp vụ Capstone hoặc chuẩn hóa toàn bộ ký hiệu trong ảnh.
- Các quy định một file/page/entity, style, mapping FR/test và export là quy ước repo/Review 2, không phải yêu cầu chung cho mọi state machine UML.

# Review State Diagram — góc nhìn giảng viên kỹ thuật phần mềm

Ngày review: 2026-10-30. Phạm vi: [file tám tab](State-Machine-Diagrams.drawio), tám PNG hiện có, [builder](build_state_diagrams.py), [thuyết minh](State-Machine-Diagrams-design.md), [rule](rule.md), Report III/IV và các phần schema/hành vi liên quan của `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`.

## Trạng thái sau hiệu chỉnh

Theo lựa chọn mới của người dùng, Research Engines chuyển sang composite Current version (not stale) chứa bảy state chưa stale; Stale ở ngoài, một transition upstreamVersionChanged trên state cha áp dụng cho mọi state con. Bỏ toàn bộ junction invalidation. Initial ngoài vào composite, initial trong vào Draft; nhánh checks/review, guard/effect và khoảng cách đều giữ nguyên. Đây là thay thế bố cục chuỗi junction của lượt trước; các tab khác không đổi XML.

Cập nhật theo yêu cầu mới: Data Management đã có lại thiết kế vòng đời Local Node pairing (Unpaired, Paired online/offline, Revoked) từ UC-08/31; Run khôi phục reason node_offline và hai transition chờ/reconnect. Đã đồng bộ ghi chú phạm vi trong Report IV, Class và inventory. Nhận xét cũ về tab chỉ ghi chú hoặc loại node_offline bên dưới là lịch sử bản review, không còn mô tả artifact hiện tại. Chưa xác nhận implementation Local Node.

Các phát hiện bên dưới ghi nhận **bản trước sửa**. Sau yêu cầu người dùng, đã cập nhật builder, editable, thuyết minh và PNG:

| ID | Kết quả xử lý |
|---|---|
| R1 | Giữ transition-spec trước relabel/style; AI PI có guard hiển thị và metadata. Timeout giữ no-answer/effect kết thúc run. Confirm/overturn có effect trong metadata và bảng truy vết. |
| R2 | Đổi event sang revision checks completed; Under review bao gồm công việc revision bất đồng bộ. Bộ đếm revision theo version khởi tạo 0, tăng khi revision checks hoàn tất từ review, guard dưới 2. Ghi chú kết quả sau hai vòng theo nguồn. |
| R3 | Ghi rõ scope một version và ghi chú Stale giữ lịch sử, không tự refresh; không thêm đường phục hồi chưa chốt. |
| R4 | Hiện result trên mọi nhánh vào Ended. Quy tắc nhiều blocker đồng thời vẫn là câu hỏi đặc tả, không tự thêm thuật toán ưu tiên. |
| R5 | Retry ghi proposed trên ảnh; reference chỉ rõ đây là đề xuất của email, không lấy integration delivery làm bằng chứng. Ghi rõ Failed có thể giữ nguyên, policy chưa chốt. |
| R6 | Bỏ choice đọc status; Active → Resolved qua resolution reported / record resolved_at, không chỉ định ai/thuật toán tự resolve. |

Đã tái tạo tám PNG và xem sáu tab thay đổi; Authentication/Data Management được giữ nội dung. Validator, kiểm tra metadata/graph, khả năng tái tạo và link tài liệu được ghi trong changelog. Không kiểm chứng backend hoặc in A4/chèn Word. Phần kết luận cũ bên dưới không phải trạng thái hiện tại của artifact.

## Kết luận

Bộ diagram có nền tảng tốt: state phần lớn mô tả tình trạng của đối tượng, luồng chính có nguồn, các vòng đời độc lập được tách rõ. Tuy nhiên, **chưa nên chốt là bản hoàn thiện để bảo vệ**: AI PI mất guard/effect trong quá trình rút gọn nhãn; review loop chưa thể hiện giới hạn lặp; xử lý sau Stale và một số transition suy từ schema còn cần làm rõ.

Đây là review thiết kế, không phải xác nhận implementation. Chưa sửa diagram, builder, PNG hoặc requirement. Các đề nghị bên dưới cần được đối chiếu và chốt trước khi cập nhật model.

## Phát hiện theo ưu tiên

P1: cần xử lý trước khi chốt diagram. P2: cần bổ sung hoặc giải thích rõ phạm vi. P3: cải thiện tính dễ đọc.

| ID | Mức | Vị trí | Nhận xét và tác động | Hướng xử lý |
|---|---|---|---|---|
| R1 | P1 | AI PI: Pending → Tentatively decided; timeout và answer | Guard và effect quan trọng đã bị mất khỏi XML khi rút gọn nhãn. Người đọc chỉ nhìn hình/model không biết giới hạn AI PI quyết định thay người dùng. | Giữ nguyên đặc tả transition trước khi đổi nhãn; hiển thị guard quan trọng trên ảnh; lưu đủ guard/effect vào metadata và bảng truy vết. |
| R2 | P1 | Research Engines: Under review → choice; vòng quay lại review | `revision requested` đi thẳng tới choice kiểm tra kết quả, trong khi yêu cầu sửa chưa đồng nghĩa sửa xong và checks đã chạy. Chu trình cũng chưa thể hiện tối đa hai vòng revision. | Chốt sự kiện hoàn tất sửa/check hoặc effect cần thiết trước choice; mô tả bộ đếm và điều kiện chuyển theo giới hạn hai vòng, không tự tạo thêm enum state. |
| R3 | P2 | Research Engines: Stale | Có bảy đường vào nhưng không có đường ra hay giải thích đủ rõ trên hình về việc xử lý bằng version mới. Thuyết minh nói còn acceptance/rework nhưng graph dừng tại đây. | Chốt identity là object hay object version. Nếu version cũ giữ stale, ghi chú việc tạo version mới; nếu cùng instance phục hồi, xác định transition từ nguồn trước khi thêm. |
| R4 | P2 | Run: Waiting/Ended | Giữ ba state là hợp lý, nhưng reason và result chỉ có trong metadata/thuyết minh. Hình đứng riêng không cho thấy kết quả Complete/With gaps/Failed/Cancelled được lưu thế nào. | Giữ ba state; thêm effect gán result vào nhánh kết thúc hoặc bảng transition đặt kèm hình. Làm rõ cách xử lý khi nhiều blocker cùng tồn tại. |
| R5 | P2 | Notifications: Failed → Pending | Retry email đang là đề xuất; reference của nhánh trỏ sang integration_deliveries. Schema của một loại delivery chưa đủ chứng minh transition của loại khác. | Giữ nhãn “đề xuất” ngay tại nơi trình bày; chốt chính sách retry/failure cho email, không tự đặt số lần thử hoặc timeout. |
| R6 | P3 | Monitoring: Active → choice → Active/Resolved | `Alert status updated` rồi hỏi status đã resolved chưa thiên về quan sát dữ liệu hơn là giải thích sự kiện gây chuyển trạng thái. Không phải lỗi ký pháp bắt buộc. | Khi nguồn xác định, dùng event có ý nghĩa nghiệp vụ như resolution được xác nhận; có thể bỏ choice nếu chỉ còn một chuyển trạng thái thực sự. |

### R1 — Guard/effect AI PI bị mất khi tạo artifact

Bằng chứng trực tiếp:

- `decision_item()` ban đầu có `AI PI decides [autopilot; away; non-pinned]`, `authorized user answers / record decision`, và timeout `[no answer] / end run with gaps`.
- `relabel()` ghi đè thuộc tính `value`; `flat_decision()` gọi hàm này trước `apply_reference_style()`.
- `apply_reference_style()` sau đó lưu `transition-spec` từ `value` đã rút gọn. XML hiện tại của `tentative-decision` chỉ còn `transition-spec="AI PI tentative decision"`, không có `guard-expression` cho giới hạn trên. `human-answer`, `pinned-timeout`, `spending-timeout` cũng mất phần guard/effect ban đầu.
- Thuyết minh mục 6 vẫn giải thích giới hạn AI PI. Vì vậy đây là **lệch giữa thuyết minh và artifact**, không phải toàn bộ tài liệu đều thiếu rule.

Đối chiếu [Report IV §3.5.2](../../report/04-software-design-document.md#352-interaction-viewpoint-a-must_ask-item-present-and-away): AI PI chỉ quyết định tạm thời khi autopilot, away và non-pinned; pinned timeout kết thúc run with gaps, không quyết định thay người dùng. Nhánh overturn cũng nên chỉ rõ effect undo dependent work, mark affected objects stale và ghi log; hiện bảng transition chỉ dẫn FR mà chưa thể hiện các effect này trên nhánh.

Nhãn gợi ý, chưa áp dụng: `AI PI decides [autopilot and away and not pinned]`. Với timeout, lưu riêng predicate item đúng loại/chưa được trả lời và effect kết thúc run with gaps. Không cần thêm hình thoi chỉ để biểu diễn từng guard.

### R2 — Phân biệt yêu cầu sửa với hoàn tất sửa

[Report IV §3.11](../../report/04-software-design-document.md#311-independent-review-loop-and-personas-fe-11) mô tả sửa, chạy lại checks, verify và tối đa hai vòng revision. Hình hiện tại cho phép vòng `Under review → choice → Checks passed → Under review` mà không biểu diễn giới hạn này.

Không kết luận choice là sai: choice phân nhánh ngay sau event là hợp lệ nếu kết quả checks đã có. Vấn đề là event `revision requested` chưa cung cấp kết quả đó. Có thể đổi thành event hoàn tất sửa/check có nguồn, hoặc mô tả hành vi thực hiện trước khi tới choice. Nếu quá trình sửa là bất đồng bộ, không coi nó là một effect tức thời mà bỏ qua trạng thái chờ thực tế.

Không tự nối sau hai vòng sang Ready vô điều kiện: nguồn còn phân biệt known risks hoặc người dùng quyết định. Nếu đây chỉ là sơ đồ vòng đời cấp cao, cần ghi rõ giới hạn được quản lý trong review loop, và dẫn sang đặc tả đó.

### R3 — Stale và identity của version

[Report IV §2.3](../../report/04-software-design-document.md) nêu không tự cập nhật upstream; người dùng cập nhật thông qua acceptance rồi chạy lại downstream trên version mới. Accepted object là immutable.

Không nên chữa bằng mũi tên `Stale → Accepted` hoặc `Stale → Draft` tùy ý. Cần xác định diagram theo một version hay toàn bộ logical object. Một stale version có thể được giữ nguyên để truy vết, còn version mới bắt đầu ở Draft; khi đó không có outgoing từ stale version có thể hợp lý, nhưng phải giải thích trên hình/caption. Không bắt buộc gắn final chỉ vì state không có outgoing.

### R4 — Run cần giải thích được khi đọc độc lập

[Report IV §3.4.2](../../report/04-software-design-document.md#342-state-viewpoint-run-state-machine) phân biệt waiting reason và ending outcome. Builder hiện có reason-values, result-values, result-value và transition-spec cho các nhánh Run; do đó không kết luận model thiếu các giá trị này.

Điểm cần sửa là cách trình bày: ảnh chỉ ghi `Ended` và event; khi chèn ảnh vào báo cáo cần mang theo kết quả tương ứng. Giữ state phẳng và ba enum hiện tại vẫn được. Có thể ghi `... / result := with_gaps` trên nhánh hoặc đặt bảng mapping ngay dưới hình.

Một câu hỏi đặc tả còn mở: run đang waiting(decision) thì ngân sách tháng chạm 100% xử lý thế nào? Sau khi trả lời decision, có được Running khi blocker ngân sách vẫn tồn tại không? Model chỉ có một reason, chưa mô tả cách ưu tiên/tái kiểm tra nhiều blocker. Đây là điểm cần chốt requirement, chưa phải bằng chứng triển khai sai.

## Đánh giá từng tab

| Tab | Đánh giá | Nhận xét |
|---|---|---|
| Authentication & Account | Đạt trong phạm vi lần đăng nhập | Có đường sai/hết hạn quay lại chờ mã; không mở session ở nhánh No. Final kết thúc lần đăng nhập, không phải kết thúc session. Resend, lỗi gửi, Google và session expiry đã được loại khỏi phạm vi trong thuyết minh; không tự coi là lỗi thiếu state. Caption nên nói rõ “Email-code sign-in attempt”. |
| Project Workspace | Cơ bản đạt | Project và Dossier version N có hai initial vì là hai máy độc lập, có tiêu đề riêng. Superseded mô tả version N; version N+1 là instance khác. `export authorized` nên làm rõ effect export/audit hoặc đổi tên nếu chỉ ghi nhận cấp phép. Completed là nhãn thiết kế cần giữ nguồn hành vi, không khẳng định là enum triển khai. |
| Data Management | Ghi chú phạm vi, không chấm như state machine | Local Node được loại theo phạm vi hiện tại; không cần thêm lifecycle để đủ tám tab. Không dùng ghi chú này để kết luận toàn bộ Data Management không có đối tượng có vòng đời. |
| Research Run Orchestration | Đạt luồng chính, cần R4 | Cancel từ Running/Waiting, các kết quả kết thúc và đường resume có nguồn. Không cần phục hồi sau Ended. Việc bỏ node_offline đã được ghi rõ trong Report IV theo phạm vi hiện tại. |
| Research Engines | Cần sửa R2, làm rõ R3 | Có đủ tám state và phân biệt Locked chỉ cho AnalysisPlan; fan vào Stale đọc được. Thiếu diễn giải xử lý stale và giới hạn review. |
| AI Principal Investigator | Ưu tiên sửa R1 | Confirm/overturn được nhận trước choice; các kết quả terminal tách rõ. Cần giữ guard AI PI và effect đồng bộ Run/object/log. Cần xác nhận item tentative là cùng entity hay một item mới có liên kết, vì report nói mỗi tentative decision trở thành một item. |
| Notifications & Integrations | Chấp nhận như thiết kế đề xuất | State có nguồn schema; Sent không chứng minh đến inbox. Chưa đủ cơ sở chốt retry. Caption cần nói rõ đây là notification email, không đại diện mọi integration delivery. |
| Administration & Monitoring | Cơ bản đạt, có thể gọn hơn | Acknowledged không bị nhầm thành Resolved. Resolved là kết thúc trong phạm vi hình; chưa có nguồn để tự thêm reopen. Cần cải thiện event theo R6 nếu đặc tả cho phép. |

## Ký pháp và trình bày

- Initial, state bo góc, choice và final được dùng nhất quán. Không phát hiện đường ra từ final qua kiểm tra XML ở lượt này.
- `[Yes]`/`[No]` là quy ước repo có mapping predicate, không nên chấm sai chỉ vì không viết predicate dài trên mỗi nhánh. Khi tách hình khỏi thuyết minh phải giữ câu hỏi và ngữ cảnh đủ rõ.
- Nhiều final hợp lệ khi là các kết quả kết thúc thay thế; hai initial trong Project Workspace cần được đọc là hai máy độc lập.
- Các ảnh đã xem không thấy lỗi che chữ hoặc dây xuyên state rõ ràng ở kích thước hiển thị. Run và Research Engines tương đối nhiều đường; chưa kiểm tra độ đọc khi thu nhỏ chèn Word/A4.
- Tên tab là nhóm chức năng, tên subject cần là entity/lifecycle. Không yêu cầu mỗi nhóm chức năng phải có một state machine.

Nguồn ký pháp: [draw.io — UML state machine diagram](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/) trình bày state, choice, final và nhãn `trigger [guard] / actions`. [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1) là chuẩn nền được repo viện dẫn; lượt này không kiểm chứng formal conformance với toàn bộ đặc tả OMG.

## Câu hỏi cần chốt trước khi sửa

1. Hand-off Object là một logical object hay một version bất biến? Sau stale sẽ tạo version mới hay phục hồi instance hiện tại?
2. Kết quả sau hai vòng review còn blocking finding chuyển tiếp thế nào trong vòng đời object?
3. Run xử lý đồng thời decision blocker và budget blocker theo thứ tự nào?
4. Retry email có nằm trong scope đã chốt? Điều gì kết thúc việc thử lại?
5. Tentative decision thay đổi cùng DecisionInboxItem hay tạo item mới liên kết item gốc? Hủy run có đóng cả yêu cầu review quyết định tạm thời không?

## Kế hoạch sửa và kiểm chứng

1. Sửa R1 trong builder trước; bảo toàn đặc tả gốc khi rút gọn nhãn. Đối chiếu XML, bảng transition và PNG để guard/effect thống nhất.
2. Chốt R2/R3 và identity, đồng bộ requirement bị ảnh hưởng nếu có; không tự bịa transition phục hồi.
3. Làm rõ R4/R5 bằng caption/bảng hoặc transition có nguồn; R6 là cải thiện tùy chọn.
4. Regenerate editable và PNG từ builder sau khi sửa; chạy validator, kiểm tra graph/guard/effect, xem lại ảnh và thử kích thước thực tế trong báo cáo. Đồng bộ changelog.

## Bằng chứng kiểm tra lượt review

- Đã kiểm tra inventory, Git status/diff stat và nội dung nguồn liên quan; giữ nguyên các thay đổi có sẵn.
- Đã mở xem tám PNG hiện tại; không tái export và chưa đối chiếu pixel để chứng minh PNG được sinh từ đúng revision XML hiện tại.
- Validator: `python C:/Users/ADMIN/.agents/skills/drawio-skill/scripts/validate.py diagrams/09-state-machine/State-Machine-Diagrams.drawio --strict --score` → 0 errors, 0 warnings, score 0.
- XML hiện tại có 8 tab, 85 transition; xác nhận trực tiếp metadata của các transition AI PI nêu trong R1. Structural pass không phủ nhận lỗi ngữ nghĩa/thiếu guard.
- Chưa chạy backend, chưa thực thi TC; test ID trong thuyết minh chỉ là truy vết kịch bản.

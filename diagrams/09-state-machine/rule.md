# Rule: State Machine Diagram

Chuẩn: UML 2.5.1, §14 StateMachines (behavior state machine). Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram). Quy tắc dưới đây dùng hai tài liệu Visual Paradigm/draw.io và ảnh mẫu người dùng cung cấp để làm rõ ký hiệu, ngữ nghĩa và bố cục.

## 1. Mục đích và phạm vi

- Thể hiện vòng đời của **một thực thể hoặc một hệ thống có phạm vi rõ ràng**: đang ở trạng thái nào, sự kiện nào làm đổi trạng thái, điều kiện và kết quả đi kèm. State biểu diễn tình trạng của đối tượng; không dùng action làm state chỉ để mô tả thứ tự thao tác.
- Theo yêu cầu người dùng, gom toàn bộ State Diagram vào **một file draw.io nhiều tab**, gồm **tám nhóm Class Diagram và một tab Dossier Version riêng**: Authentication & Account, Project Workspace, Data Management, Research Run Orchestration, Research Engines, AI Principal Investigator, Notifications & Integrations, Administration & Monitoring. File chính là [State-Machine-Diagrams.drawio](State-Machine-Diagrams.drawio). Dossier Version được tách thành tab thứ chín để xuất hình riêng; không trộn state của nhiều đối tượng thành một lifecycle. Đây là ngoại lệ của quy tắc một file/một page chung; xem [inventory và nguồn](State-Machine-Diagrams-design.md). File standalone Authentication được giữ làm nguồn đã duyệt.
- Nguồn nghiệp vụ là bảng state và FR trong report được chốt. Đối chiếu implementation để phát hiện thiếu/lệch nhưng không tự thay report bằng code; ghi lại mâu thuẫn để xác nhận.
- Không tạo state cho từng bước CRUD hoặc từng màn hình nếu nguồn không mô tả vòng đời tương ứng. Luồng thao tác thuộc Activity/Sequence/Screen Flow.

## 2. Cách áp dụng ảnh mẫu

Giữ cách trình bày dễ đọc của ảnh: nền trắng, nét đen, state bo góc, initial phía trên, luồng chính đi xuống, nhánh phụ sang hai bên, final phía dưới khi vòng đời kết thúc. Caption nằm trong report, không nằm trong PNG.

Ảnh có những ô như `Build list for each URL` và hình thoi `Is ADMIN?`: đây là cách trình bày thiên về flowchart. Khi áp dụng vào state machine:

- Tên ô phải diễn tả trạng thái/điều kiện đang tồn tại, ví dụ `running`, thay vì lệnh thực hiện một bước. Một hoạt động đang diễn ra có thể là state nếu nguồn xác định nó là một trạng thái của đối tượng.
- Thao tác tức thời đặt trên transition dưới dạng effect; chỉ đưa vào `entry`, `do`, `exit` khi cần mô tả hành vi của state.
- Hình thoi phân nhánh phải có **câu hỏi rõ ràng bên trong**, kết thúc bằng `?`; hai nhánh trả lời **`[Yes]` và `[No]`** tách sang hai bên như ảnh mẫu. Không để hình thoi rỗng. Không tự thêm chuỗi kiểm tra đăng nhập/quyền vào mọi vòng đời.
- `Unauthorized`, `failed` hay `created` chỉ là state nếu có nghĩa trong vòng đời đang mô hình hóa; không mặc định mọi response là một state.

Các yêu cầu về cách tổ chức tab, mỗi state một hình, câu hỏi trong hình thoi, hai nhánh trái/phải, không frame ngoài cùng là **profile trình bày của repo theo người dùng**, không phải hạn chế chung của UML. UML vẫn hỗ trợ composite, nhiều guard ra choice và junction khi mô hình cần.

## 3. Ký hiệu

| Element | Ký hiệu / nội dung | Quy tắc áp dụng |
|---|---|---|
| Khung ngoài | Khung bao trình bày tùy chọn | Không dùng khung bao riêng cho Research Run; composite Active run là một state thực sự chứa Running và Waiting. Phạm vi thể hiện trong tên page và thuyết minh. |
| Initial pseudostate | Chấm tròn đen | Một initial cho region cần khởi tạo, đặt phía trên trục chính. Không có đường vào, đúng một đường ra; đường ra không có trigger hoặc guard, có thể có effect khởi tạo. |
| Simple state | Chữ nhật bo góc | Tên ngắn, đúng nguồn/report, kể cả `waiting(decision)` hay `ended(with_gaps)`. |
| State behavior | Ngăn nội dung tùy chọn | `entry / ...`, `do / ...`, `exit / ...`; không cần thì chỉ để tên state. |
| Transition | Đường liền, đầu mũi tên mặc định có tô chỉ về đích | Gắn đúng source/target; nhãn theo mục 4. Self-transition được phép khi có sự kiện và ý nghĩa rõ ràng. |
| Choice | Hình thoi | Câu hỏi nằm trong hình thoi, ví dụ `Is code correct and unexpired?`; hai guard `[Yes]` / `[No]` của profile này sang hai bên. Đây là quy ước trình bày người dùng chốt; choice không phải state chờ. |
| Junction | Chấm tròn đen nhỏ | Được dùng để nối các nhánh thay thế có cùng phần tiếp theo; giữ trigger, guard và effect trên từng nhánh. Không dùng như join đồng bộ hay nhãn chung `end event`. |
| Composite state | Chữ nhật bo góc chứa state con | Research Engines dùng Current version (not stale), gồm bảy state chưa stale và Stale ở ngoài. Research Run dùng Active run chứa Running và Waiting; Ended ở ngoài. Transition từ biên state cha áp dụng cho mọi state con tương ứng; không hiểu là bảy state đồng thời. |
| Final state | Chấm đen trong vòng tròn rỗng | Region bao nó đã hoàn tất; không đồng nghĩa xóa object/record; không có đường ra. Không bắt buộc thêm final cho hệ thống hoạt động liên tục hoặc vòng đời chưa kết thúc trong phạm vi. |
| Fork / Join | Thanh đen | Hợp lệ trong state machine cho các region đồng thời; không dùng để chia các nhánh điều kiện loại trừ nhau. |
| History / Regions | `H`, `H*` / vùng phân cách nét đứt trong composite | Chỉ dùng khi nguồn yêu cầu nhớ cấu hình con hoặc hoạt động đồng thời; phải giải thích trong legend. |

Các state kết thúc nghiệp vụ vẫn giữ tên và kết quả riêng trước final, nếu nguồn có mô tả. Không ép `accepted` thành kết thúc toàn bộ vòng đời: kiểm tra transition về `stale` hoặc sang `locked` theo loại object trong [bảng object states](../../report/04-software-design-document.md#343-state-viewpoint-object-states).

## 4. Nhãn transition và điều kiện

Cú pháp: `trigger [guard] / effect`. Chỉ ghi các phần có ý nghĩa; không chèn placeholder cho phần thiếu.

- **Trigger**: sự kiện gây chuyển trạng thái, tên nhất quán với nguồn; không bắt buộc thì quá khứ hoặc tên hàm trong code. Có thể là sự kiện người dùng, hệ thống hoặc thời gian.
- **Guard**: biểu thức boolean trong `[...]`, không có tác dụng phụ, được đánh giá khi trigger xảy ra. Guard không tự chờ người dùng thao tác; input cần tới qua event trước khi vào choice. Các nhánh cùng trigger cần phân biệt rõ và bao phủ trường hợp cần xử lý; quy ước của repo là dùng điều kiện loại trừ nhau để tránh mơ hồ.
- **Effect**: hành vi xảy ra khi transition được thực hiện; chỉ ghi khi nguồn xác định. Không bắt buộc đưa tên method triển khai vào ảnh.
- Transition không có trigger chỉ dùng khi đúng ngữ nghĩa completion hoặc là đoạn qua pseudostate. Completion của state xét cả hành vi/region con nếu có; không hiểu đơn giản là cứ vào state là lập tức đi tiếp.
- Với choice nhị phân, chuyển điều kiện thành câu hỏi **bên trong hình thoi**; đường ra phải có **guard trong ngoặc vuông** và không có trigger mới. Trong profile người dùng chốt, hiển thị `[Yes]` / `[No]` là tên ngắn của hai guard trả lời câu hỏi; biểu thức boolean đầy đủ bắt buộc lưu ở `guard-expression` và bảng ánh xạ trong thuyết minh. Đây là alias hiển thị của bộ tài liệu, không phải tên event hoặc cú pháp đặc biệt do UML quy định. Khi không dùng profile này, ưu tiên `[điều kiện]` / `[else]`. Effect có thể đặt sau nhãn trả lời. Không gắn thêm sự kiện phải chờ lên đường ra choice. Nếu có nhiều kết quả, tách thành các câu hỏi nhị phân có nguồn, không ép mất trường hợp nghiệp vụ.
- Ánh xạ transition với FR/UC/bảng state trong tài liệu đi kèm. Chỉ đưa mã FR lên ảnh khi cần truy vết trực tiếp và không làm nhãn rối; không bịa FR cho transition kỹ thuật.

Ví dụ định dạng từ [vòng đời Research Run](../../report/04-software-design-document.md#342-state-viewpoint-run-state-machine):

| Source | Nhãn | Target | Reference |
|---|---|---|---|
| `waiting(budget_review)` | `additional spending approved` | `running` | §3.4.2, FR liên quan theo report |
| `waiting(decision)` | `wait deadline reached [pinned item unanswered]` | `ended(with_gaps)` | FR-262, FR-265 |
| State chưa `ended` | `run cancelled [authorized requester]` | `ended(cancelled)` | FR-22 |

Nhãn minh họa là mô tả sự kiện nghiệp vụ, không xác nhận tên event/API trong implementation.

## 5. Bố cục và draw.io

- Research Run và Research Engines dùng composite; các tab khác giữ cấu trúc hiện tại. Trải state theo trục dễ theo dõi, có thể dùng junction khi các nhánh thay thế có cùng phần tiếp theo. Mỗi vòng đời phải là một graph liền mạch; không lặp state hoặc tách thành các cụm minh họa sự kiện rời. Nếu source quy định field reason/result thì giữ là field, không tự nhân thành state mới. Không cắt bớt trạng thái hoặc nhánh để làm gọn. Nhãn trên ảnh ngắn; giữ điều kiện/effect và nguồn đầy đủ trong metadata/thuyết minh.
- Các field context như reason/result giữ trong metadata/thuyết minh; profile compact không đặt ô context dài bên cạnh state. Nếu thực sự cần note, note gắn bằng nét đứt không mũi tên và không được hiểu là transition. Không trộn danh sách field vào tên state hoặc coi là entry/do/exit.
- Export PNG riêng từng tab với tiền tố số thứ tự và tên tab, cùng folder với file chính.
- Bật thư viện **UML 2.5** trong More Shapes; dùng state/pseudostate đúng loại. Giữ element editable, không thay bằng ảnh.
- Ưu tiên trục chính trên → dưới như ảnh mẫu. Nhánh lỗi, từ chối, huỷ hoặc phục hồi đặt hai bên, giữ nhãn đủ khoảng trống. Không ép mọi nhánh về final nếu nguồn cho phép retry/resume.
- Initial/final căn theo luồng chính, không cố định ở hai góc đối diện như rule cũ. Final có thể có nhiều đường vào; chỉ thêm khi đúng nghĩa hoàn tất.
- Ưu tiên đường nối vuông góc; riêng cụm nhiều source cùng target có thể dùng đoạn thẳng nghiêng trực tiếp để dễ lần theo. Tránh đi xuyên ô, chữ hoặc cắt đường khác. Đường quay lại đi ở hành lang ngoài; đầu mũi tên phải chạm đúng biên state đích.
- Câu hỏi căn giữa hình thoi, tăng kích thước ô để đủ chữ. `[No]` đặt trực tiếp trên đường nhánh ra bên trái, `[Yes]` trên đường nhánh ra bên phải; nhãn transition cũng đặt đè lên đoạn đường thẳng tương ứng, dùng nền trắng để nét nối không xuyên chữ; đường có thể gấp vuông góc để tới state đích. Không để chữ chồng hình thoi hoặc nhánh lân cận.
- Theo hình lifecycle của report FI2M người dùng gửi: ô state gọn, nhãn sự kiện bằng lời; dùng Arial 12 cho state, 11 cho transition, 14 cho tiêu đề con. Giữ biểu thức UML đầy đủ trong transition-spec và thuyết minh khi nhãn ảnh rút gọn. Profile, caption/ảnh tham khảo và phạm vi áp dụng ghi trong [inventory](State-Machine-Diagrams-design.md#report-mẫu-tham-khảo-hình). Theo grid, A4 và export PNG của quy tắc chung. Đen trắng là mặc định; không thu nhỏ chữ để nhét thêm state.
- Mỗi mũi tên thể hiện đúng source/event/guard/target; không gộp nhiều cause thành nhãn mơ hồ. Giữ code nguồn trong metadata và thuyết minh. Run có running/waiting/ended; waiting reason và ended result thể hiện riêng trong state/transition, đúng FR-21 và Class Diagram. Nhánh stale phải có đường từ mọi state object áp dụng; cancel không được đổi một decision đã resolved.

## 6. Không được

- Biến state machine thành chuỗi thao tác kiểu `Click button → Validate input → Save database`.
- Tự thêm state/transition, mất state theo nguồn, hoặc coi mọi enum triển khai là một state của đối tượng này.
- Dùng final như điểm gộp để tiếp tục luồng, dùng choice làm nơi chờ sự kiện, hoặc dùng fork thay choice.
- Cấm toàn bộ fork/join hoặc toàn bộ transition thiếu trigger: chúng hợp lệ khi dùng đúng ngữ nghĩa UML ở trên.
- Để state không thể tới được hoặc state có đường vào nhưng không có lối ra mà không giải thích đó là trạng thái terminal/chờ trong phạm vi. Không tự tạo đường ra chỉ để đạt checklist.

## 7. Checklist trước khi hoàn tất diagram

- [ ] Phạm vi một đối tượng rõ; đối chiếu đầy đủ state/transition với report và FR/UC liên quan, nêu chỗ lệch implementation nếu có.
- [ ] Mỗi state chỉ có một hình trong cùng vòng đời, graph liền mạch từ initial; không dùng các bản sao state để tránh nối mũi tên.
- [ ] Tên state diễn tả trạng thái; action, trigger, guard, effect được phân biệt.
- [ ] Initial/final/choice đúng ngữ nghĩa; composite/initial và transition kế thừa có ngữ nghĩa rõ; không bắt buộc final khi không có kết thúc.
- [ ] Mỗi hình thoi có câu hỏi bên trong và hai guard `[Yes]` / `[No]` tách sang hai bên và có biểu thức boolean rõ ràng; câu trả lời ánh xạ rõ điều kiện đúng/phủ định, không có hình thoi rỗng.
- [ ] Guard không gây mơ hồ; retry, recovery, cancel và terminal theo đúng nguồn.
- [ ] Mỗi state có đường tới; state không có lối ra có lý do. Không còn transition đi ra từ final.
- [ ] Có ánh xạ transition với test case theo yêu cầu Review 2; không nhầm checklist này với bằng chứng test đã chạy.
- [ ] Nhãn nằm trực tiếp trên đường nối với nền trắng, không che đầu mũi tên, góc gấp hoặc hình thoi; đọc được ở kích thước chèn report.
- [ ] Nếu tạo/sửa diagram: đồng bộ builder (nếu có), editable và PNG; chạy validator phù hợp và xem ảnh export. Syntax pass không thay thế review ngữ nghĩa hoặc kiểm tra trực quan.

## 8. Nguồn và mức áp dụng

- [Visual Paradigm — What is State Machine Diagram?](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/about-state-diagrams/): phân biệt state với activity, vòng đời đối tượng, composite và history.
- [draw.io — UML state machine diagram](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/): thư viện UML 2.5, hình dạng state/pseudostate, transition và regions.
- [OMG — UML 2.5.1](https://www.omg.org/spec/UML/2.5.1): §14 StateMachines, chuẩn ngữ nghĩa nền.
- Ảnh mẫu người dùng gửi ngày 2026-10-30: tham chiếu bố cục dọc, nét đen và nhánh hai bên; không phải nguồn nghiệp vụ Capstone hoặc chuẩn hóa toàn bộ ký hiệu trong ảnh.
- Các quy định một file nhiều tab, một diagram/entity mỗi tab, style, câu hỏi trong hình thoi với hai nhánh Yes/No, mapping FR/test và export là quy ước repo/Review 2, không phải yêu cầu chung cho mọi state machine UML.

## 9. Phạm vi triển khai và các điểm kết thúc (2026-10-30)

- Theo yêu cầu mới, Research Engines dùng composite Current version (not stale) chứa bảy state chưa stale, Stale nằm ngoài; một transition upstreamVersionChanged kế thừa cho mọi state con thay thế các đường lặp/junction invalidation. Có initial ngoài vào composite và initial trong vào Draft. State/choice trên trục chính cao 80, bước hàng 200, khoảng trống dọc 120 trước scale. Giữ đầy đủ guard/effect và source-ref.

- Hiệu chỉnh sau review: rút gọn nhãn chỉ thay nội dung hiển thị; lưu `transition-spec` trước khi đổi nhãn, không ghi đè đặc tả gốc ở bước style. Guard/effect quan trọng phải xuất được trong bảng transition; guard giới hạn AI PI và result kết thúc Run được giữ đầy đủ trong metadata và bảng transition; ảnh dùng nhãn ngắn.
- Under review bao gồm công việc revision và chạy lại checks; nhánh tới choice chỉ xảy ra khi checks đã hoàn tất, không dùng event yêu cầu sửa để phân nhánh theo kết quả chưa có. Giới hạn hai vòng revision theo IV 3.11, findings còn lại thành known risks hoặc chờ người dùng; không tự kết luận mọi finding đều được chấp nhận sau hai vòng.
- Hand-off view theo một version; Stale giữ lịch sử và không tự refresh. Giải thích phạm vi version trong thuyết minh; không đặt chú thích rời ngoài hình hoặc tạo state/đường phục hồi chưa chốt. Email retry phải ghi proposed ngay trên ảnh; Failed có thể giữ nguyên khi chưa có policy. Monitoring có thể nối Active → Resolved bằng sự kiện ghi nhận resolution; không bắt buộc thêm choice đọc status.

- Theo yêu cầu mới của người dùng: khôi phục Local Node pairing trong Data Management và reason/transition node_offline của Run theo UC-08/31, FR-85/87/110/241/242. Đây là thiết kế dự kiến, không coi là bằng chứng implementation. Scope một pairing với project: Unpaired → Paired online, online ↔ offline, revocation từ cả hai trạng thái paired → Revoked → final. Final kết thúc pairing này; không tự thêm re-pairing/restore chưa chốt hoặc biến job/release thành state Node.
- Vòng đời trong phạm vi hình hoàn tất tại Archived (Project), Superseded (Dossier version), Answered/Confirmed/Overturned/Closed/Expired (Decision Item), Sent/Skipped (email delivery), Resolved (alert); nối tới final bằng completion transition không nhãn, final không có đường ra. Lịch sử vẫn được lưu. Decision Item vẽ các transition hoàn tất chung đường đến một final, không dùng junction; các view khác có thể dùng final riêng.
- Accepted/Locked còn có thể stale; Stale còn acceptance/rework; Failed còn retry. Không gắn final khiến mất các khả năng đó. Nếu report chưa chốt đường phục hồi, nêu giới hạn thay vì tự thêm transition.
- IV 3.4.3 cho phép mọi state object chuyển sang stale khi pinned upstream có version mới: trong Research Engines, quy tắc này được mô hình bằng transition từ composite chứa bảy state chưa stale tới Stale. Không cần bảy mũi tên riêng hoặc junction, không phải join đồng bộ.

## 10. Trình bày compact (2026-10-30)

- Composite dùng ngăn tên riêng và chứa region tuần tự; transition từ biên cha áp dụng cho các state con theo guard trong metadata.
- Bỏ các tiêu đề và chú thích rời ngoài graph; phạm vi và giả định nằm trong thuyết minh. Nhãn mũi tên dùng từ ngắn để phân biệt sự kiện; guard, effect, result và nguồn đầy đủ vẫn được lưu trong XML và bảng transition. Alias `eligible` của AI PI phải được đọc cùng guard đầy đủ trong bảng.

## 11. Cập nhật theo yêu cầu bỏ khung

Không dùng composite hoặc frame bao trong bộ hiện tại. Các transition trước đây kế thừa từ state cha được vẽ riêng từ từng state áp dụng; xem bảng transition trong thuyết minh.

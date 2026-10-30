# Authentication & Account — bản Class Diagram đề xuất

Bản thử để duyệt thiết kế và bố cục, chưa thay ảnh trong report. Sơ đồ thể hiện cấu trúc lớp của cả nhóm FE-01; không phải Sequence Diagram của riêng một lần sign-in.

File editable hiện được mở rộng thành **8 tab** theo yêu cầu mới: Authentication là tab đầu, giữ nguyên graph đã duyệt. Xem [inventory và nguồn của cả bộ](Class-Diagrams-design.md). Các ghi nhận một page bên dưới mô tả validation của bản Authentication ban đầu; validation hiện hành cho file chung là 8 tab.

Theo phản hồi tiếp theo về kích thước hộp: Authentication cũng dùng chiều rộng theo tên và thành viên, thay cho các cột hộp rộng gần bằng nhau. Giữ nguyên nội dung và chiều cao theo số dòng; giữ tâm hộp, cập nhật port/waypoint và nhãn khi cần. Đã xuất lại PNG và kiểm tra cùng tám tab; các ghi nhận giữ hình học bên dưới là lịch sử các lượt sửa trước đó.

Theo phản hồi về chữ đè lên class: giữ nguyên hình học class/đường nối, dịch `checks access` sang phía trái tuyến vòng ngoài và đặt multiplicity cách endpoint để không chạm viền hoặc nhãn giữa đường. PNG Authentication đã được export lại sau sửa vị trí nhãn.

Theo điều chỉnh của người dùng: bản preview trải ngang trên canvas 2320 × 1300, tăng khoảng cách giữa các cụm; bỏ dòng trạng thái bản nháp, khối ghi chú và legend. Nhãn quan hệ trên đường nối được giữ theo phản hồi mới nhất, gồm uses, verifies identity, sends code, issues / consumes, manages sessions, updates và các nhãn kiểm tra quyền. Mũi tên dependency dùng đầu mở kích thước 16, nét 1.5; pin vào cạnh class, có đoạn tiếp cận vuông góc tối thiểu 60–70 px để tránh đầu mũi tên chạy dọc cạnh hoặc trùng vạch chia ngăn. Các đường vào User dùng vị trí riêng để không trùng nhau. Theo phản hồi mới nhất, các quan hệ cùng hàng/cột đi thẳng; các đường khác dùng hành lang riêng với hai góc vuông, bỏ các đoạn lệch nhỏ do port/waypoint không cùng tọa độ. Đường AuthenticationService → AuthSession đi vòng hành lang trên/phải để tránh các class trung gian. Giữ nội dung class và multiplicity; bỏ khung ngoài cùng tiêu đề frame theo phản hồi tiếp theo của người dùng. Phần giải thích ký hiệu/ràng buộc nằm trong tài liệu này: nét liền là association, nét đứt với mũi tên mở là dependency; stereotype thể hiện vai trò của từng class. Bố cục ngang và việc bỏ legend/frame là ngoại lệ cho bản xem thử theo yêu cầu, chưa phải bố cục in A4 theo rule chung.

- [File editable](Class-Diagram-Authentication-Account.drawio)
- [PNG xem trước](Class-Diagram-Authentication-Account.png)
- [Builder](build_authentication_account.py)
- [Rule](rule.md)

## Nguồn và giới hạn

Nguồn chính: `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`, phần III 3.2 và IV 3.1. Phần IV 3.1.1 đang là placeholder, chưa có danh sách class hoặc chữ ký operation. Vì vậy tên controller/service, cách chia trách nhiệm, tên thuộc tính, kiểu dữ liệu và signature trong bản này là **đề xuất thiết kế**, không phải trích nguyên văn report hoặc sơ đồ reverse-engineer từ code.

Đối chiếu nội dung với [Report IV của repo](../../report/04-software-design-document.md) §3.1 và [Report III](../../report/03-software-requirements-specification.md). Có đọc giới hạn các model/service identity trong repo `logos` để kiểm tra khái niệm session, OTP và profile, nhưng không dùng cấu trúc code để thay hợp đồng nghiệp vụ. Code hiện có dùng router/hàm ở một số vị trí; các hộp controller/service trong bản vẽ là phân chia trách nhiệm thiết kế được đề xuất.

## Ánh xạ trách nhiệm

| Thành phần đề xuất | Trách nhiệm / căn cứ |
|---|---|
| AuthenticationController | Điểm vào cho email code, Google, profile/onboarding và sign-out; III 3.2.1–3.2.4. Kiểm tra quyền áp dụng cho mọi request được bảo vệ, không chỉ các operation trong hộp này. |
| AuthenticationService | Phát/xác minh challenge, xác minh Google identity, ánh xạ email đã xác minh về cùng User, mở/kiểm tra/thu hồi session; FR-01, FR-146; IV 3.1 bước 1–3; III 3.2.4–3.2.5. |
| AccountService | Hoàn tất onboarding và cập nhật display name/avatar; III 3.2.3. |
| AuthorizationService | Kiểm tra role theo project ở mọi action, ẩn sự tồn tại project với non-member, tách quyền metadata của Platform Admin; FR-02, FR-03, FR-151, FR-152; IV 3.1 bước 4–5. |
| User | Một danh tính tài khoản theo email; display name/avatar theo onboarding. `isPlatformAdmin` là biểu diễn rút gọn của quyền nền tảng trong view, không thay thế project role. |
| AuthSession | Session có hạn và có thể thu hồi; III 3.2.4–3.2.5. Các field UUID, expiresAt, revokedAt là lựa chọn thiết kế. |
| EmailChallenge | Challenge email có hạn và được tiêu thụ khi xác minh. `codeDigest`/`consumedAt` là đề xuất lưu trữ an toàn, không phải field được report quy định. Không có association tới User vì view không chốt việc tài khoản được tạo trước hay sau xác minh. |
| Membership | Liên kết user với project và project role; Report IV §2.1.1. Một user có thể có 0..* membership; mỗi membership thuộc 1 user. Project nằm ngoài view này, được tham chiếu qua projectId. |
| ProjectRole | Project Manager, Researcher, Reviewer; literal chữ hoa là cách đặt tên đề xuất, không khẳng định enum code hiện tại. |
| EmailDelivery / GoogleIdentityProvider | Dịch vụ ngoài hỗ trợ hai cách sign-in. Operation là contract khái niệm của view; không chốt nhà cung cấp email hoặc SDK. |

User liên kết với 0..* AuthSession; mỗi session xác thực một User. Theo [Mermaid](Class-Diagrams-Mermaid.md), quan hệ này được biểu diễn bằng composition với thoi đặc ở User như một lựa chọn mô hình hóa; không tự suy ra quy tắc xóa dữ liệu hoặc xác nhận toàn bộ vòng đời runtime. Các dependency nét đứt chỉ diễn tả sử dụng, không biểu diễn thứ tự gọi hoặc thứ tự xử lý.

Không thêm interface/implementation hoặc repository chưa được chốt chỉ để giống ảnh mẫu. Chi tiết persistence và DTO không nằm trong bản này. Các kiểu phụ được dùng trong signature:

| Kiểu | Ý nghĩa trong đề xuất |
|---|---|
| EmailCode | email và code người dùng nhập. |
| ProfileInput | display name và tham chiếu avatar của user đang đăng nhập. |
| Identity | email đã xác minh và subject nhận từ Google. |
| Action | Thao tác đang được kiểm tra quyền; tập giá trị theo policy, chưa liệt kê trong view này. |
| UUID, String, Boolean, DateTime | Kiểu thiết kế; không áp đặt ngôn ngữ lập trình. |

User/current session truyền ngầm qua request context ở các operation profile; việc update phải giới hạn đúng tài khoản đang đăng nhập. `canReadMetadata` chỉ là nhánh kiểm tra đặc quyền metadata của Platform Admin; các thành viên vẫn được kiểm tra quyền project qua `requireRole`. Membership là điều kiện cần để đọc nội dung, còn role/action quyết định quyền cụ thể. Session hết hạn bị từ chối và user quay lại sign-in theo III 3.2.5; điều hướng UI không được mô hình thành class.

## Tái tạo và kiểm tra

Từ repository root:

```powershell
python diagrams/07-class/build_authentication_account.py
python C:/Users/ADMIN/.agents/skills/drawio-skill/scripts/validate.py diagrams/07-class/Class-Diagram-Authentication-Account.drawio --score
& 'C:/Program Files/draw.io/draw.io.exe' -x -f png -s 2 -b 20 -o 'diagrams/07-class/Class-Diagram-Authentication-Account.png' 'diagrams/07-class/Class-Diagram-Authentication-Account.drawio'
```

Validation ngày 2026-10-29: validator báo **0 errors, 0 warnings**, score 0; XML có một page và 11 classifier. PNG đã xuất bằng draw.io CLI và được xem trực quan: không thấy chữ bị cắt, đường xuyên class hoặc nhãn chồng nhau. Đây là PNG preview nền trắng, scale 2, border 20, không nhúng XML; file `.drawio` riêng giữ khả năng chỉnh sửa. Chưa kiểm tra bản in A4 hoặc ảnh sau khi chèn vào Word, chưa có xác nhận thiết kế/implementation runtime.

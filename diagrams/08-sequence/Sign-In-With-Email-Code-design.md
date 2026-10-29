# Sign In With Email Code — bản sequence để duyệt

- [Editable](Sequence-Diagram-Sign-In-With-Email-Code.drawio)
- [PNG](Sequence-Diagram-Sign-In-With-Email-Code.png)
- [Builder](build_sign_in_with_email_code.py)
- [Rule](rule.md)

Nguồn chính: `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`, III 3.2.1 và IV 3.1, ô IV 3.1.2. Đối chiếu [Report III](../../report/03-software-requirements-specification.md), [Report IV](../../report/04-software-design-document.md) và [thiết kế Authentication & Account](../07-class/Authentication-Account-design.md). Đây là bản thiết kế đề xuất để xem trước, chưa thay placeholder hoặc chèn ảnh vào report.

## Phạm vi

Theo phản hồi người dùng, bỏ khung `sd` ngoài cùng và tiêu đề trong khung; giữ các fragment `alt`/`opt`. Đây là ngoại lệ trình bày cho bản xem thử này; nội dung và vị trí các tương tác không đổi.

Hạ nhãn actor `User` thêm 10 px theo phản hồi để tách tên khỏi chân hình người.

Sau lượt làm thoáng vùng `resolveUser`/`opt`, bản hiện tại dùng builder chung để bổ sung `AuthenticationRepository` giữa AuthenticationService và Database. Giữ guard có hàng riêng và không có activation lồng dài; số message thay đổi do tách request/reply qua Repository.

User nhập email tại SC-01, yêu cầu mã; hệ thống lưu challenge và yêu cầu gửi email. User nhập mã đã nhận tại SC-02. Mã sai hoặc hết hạn trả lỗi về UI, không tạo tài khoản/session. Mã hợp lệ tìm tài khoản theo email đã xác minh, tạo mới nếu đây là lần đầu, tiêu thụ mã một lần và mở session. `Delivery request accepted` chỉ xác nhận chấp nhận yêu cầu gửi email; không khẳng định email đã tới inbox. Hành động nhập mã giả định user đã nhận được mã.

Tên operation `requestEmailCode`, `signInWithCode`, `requestCode`, `verifyCode`, `sendCode` theo Class Diagram đề xuất hiện có. Theo yêu cầu mới của người dùng, request dữ liệu đi từ AuthenticationService → AuthenticationRepository → Database, reply theo chiều ngược lại. Repository là lớp thiết kế trong sequence, không khẳng định đã có trong BE hay Class Diagram. Message database là hành vi khái niệm, không phải tên SQL/API đã triển khai. Việc lưu digest/expiry và tiêu thụ challenge theo mô hình EmailChallenge hiện có; Report7 §IV 2.2.4 cũng mô tả digest và expiry của email_otps.

Thiết kế cần bảo đảm chỉ tạo session khi tiêu thụ mã hợp lệ thành công; `Consume code and create session atomically` biểu diễn thao tác logic nguyên tử, không chốt transaction/schema triển khai. Không quy định độ dài mã, TTL, retry limit, endpoint, HTTP status hoặc cách truyền token/cookie vì luồng nguồn chưa chốt các chi tiết này. Không đưa mã thật hoặc token vào sơ đồ.

Google sign-in, resend, lỗi nhà cung cấp email, onboarding và kiểm tra role trên request project sau đăng nhập nằm ngoài page này. FR-02 áp dụng khi truy cập chức năng được bảo vệ; không yêu cầu project role để người dùng bắt đầu đăng nhập.

## Validation

Chạy builder, validator cấu trúc và export PNG bằng draw.io CLI; xem PNG trước khi bàn giao. Kết quả thực tế được ghi trong changelog. Chưa kiểm tra in A4/chèn Word hoặc runtime backend.

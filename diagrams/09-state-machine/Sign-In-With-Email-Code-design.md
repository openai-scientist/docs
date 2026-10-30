# Sign In With Email Code — State Diagram để duyệt

Bản đã duyệt cũng nằm ở tab đầu [file State Diagram chung](State-Machine-Diagrams.drawio); file standalone và builder bên dưới được giữ làm nguồn gốc.

- [Editable draw.io](State-Machine-Diagram-Sign-In-With-Email-Code.drawio)
- [PNG xem trước](State-Machine-Diagram-Sign-In-With-Email-Code.png)
- [Builder](build_email_code_state.py)
- [Rule](rule.md)

Nguồn: `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`, III §3.2.1 (dòng 3133–3139), IV §3.1 (5675–5685), IV §2.2.4 (email_otps). Đối chiếu [sequence cùng nghiệp vụ](../08-sequence/Sign-In-With-Email-Code-design.md). Đây là bản thiết kế state machine đề xuất để duyệt; report mô tả hành vi nhưng chưa định nghĩa enum state cho lần đăng nhập này.

SHA-256 của file nguồn tại thời điểm vẽ: `8618eb8123e0a3d259c9e5f5ba97f9e29602534ae3503b2aaa25e0d2e5eb232d`.

Lượt đối chiếu UML với hai hướng dẫn đã chuẩn hóa guard `[Yes]`/`[No]`; giữ nguyên state/flow bản đã duyệt. Lượt tham khảo report FI2M dùng cùng profile compact của file tám tab; standalone và tab đầu có cùng model sau áp dụng style.

Theo yêu cầu người dùng, bỏ khung và tiêu đề `stm` ngoài cùng; giữ bố cục tương đối của toàn bộ state, nhãn và đường nối.

## Phạm vi và cách đọc

Đối tượng là **một lần đăng nhập bằng mã email**, không phải toàn bộ vòng đời account hoặc session. `Signed out`, `Awaiting email code`, `Signed in` là nhãn trạng thái khái niệm suy ra từ nguồn. Final nghĩa là lần đăng nhập thành công đã hoàn tất; session vẫn hoạt động. Không có đường từ nhánh sai/hết hạn đến `Signed in`.

Choice chứa câu hỏi **Is code correct and unexpired?**; `[No]` đi sang trái, `[Yes]` đi sang phải theo mẫu người dùng chốt. Các nhãn transition đặt trực tiếp trên đường nối, nền trắng ngắt nét bên dưới chữ để dễ đọc. `[Yes]` là guard alias cho mã đúng và chưa hết hạn; `[No]` cho mã sai hoặc hết hạn. Predicate lưu trong guard-expression và bảng review của bộ chung; chúng không phải event mới trên đường ra choice. Choice rẽ nhánh ngay sau sự kiện `code submitted`; không phải state chờ kiểm tra. Để giữ nhãn nhánh chỉ có `Yes`/`No`, các effect được mô tả trong thuyết minh này: nhánh No báo lỗi; nhánh Yes tiêu thụ mã, resolve account và mở session. `resolve account` nghĩa là tìm account theo email đã xác minh và tạo account nếu đăng nhập lần đầu. `consume code` biểu diễn tính dùng một lần; chỉ mở session sau khi mã được chấp nhận. Không xác định transaction, endpoint, token transport hoặc tên method triển khai.

Trở lại `Awaiting email code` sau lỗi nghĩa là lần đăng nhập chưa xác thực, cho phép người dùng sửa mã. Mã đã hết hạn không trở nên hợp lệ khi nhập lại. Yêu cầu mã mới, lỗi gửi mail, giới hạn số lần thử, Google, onboarding, sign-out và session expiry nằm ngoài bản thử này; không tự đặt TTL hoặc retry limit. Việc gửi mã không bảo đảm email đã tới inbox.

## Truy vết và kịch bản cần kiểm tra

| Transition | Nguồn | Kịch bản kiểm tra thiết kế |
|---|---|---|
| Initial → Signed out | III §3.2.1, actor any user | Bắt đầu lần đăng nhập chưa xác thực. |
| Signed out → Awaiting email code | FR-01, III §3.2.1 | Yêu cầu mã cho email; hệ thống gửi mã dùng một lần. |
| Awaiting email code → Choice | III §3.2.1 | Người dùng nộp mã để kiểm tra. |
| Choice → Awaiting email code | III §3.2.1; sequence đối chiếu | Mã sai hoặc hết hạn: báo lỗi, không mở session. |
| Choice → Signed in | FR-01, III §3.2.1, IV §2.2.4 | Mã đúng/chưa hết hạn: dùng mã một lần, resolve account, mở session; kiểm tra cả account có sẵn và lần đầu. |
| Signed in → Final | Ranh giới diagram đề xuất | Hoàn tất lần đăng nhập; không đồng nghĩa sign-out. |

Đây là các kịch bản review, chưa phải test runtime đã thực thi. FR-02 kiểm tra quyền trên hành động sau đăng nhập; không thêm choice quyền project vào luồng đăng nhập.

## Validation

Builder chạy thành công. Validator `--strict --score`: 0 errors, 0 warnings, score 0. PNG được export bằng draw.io CLI scale 2, border 20, nền trắng, không nhúng XML; đã mở xem và kiểm tra chữ, nhánh quay lại, đầu mũi tên và final. File draw.io riêng giữ mọi element editable. Chưa kiểm tra in A4/chèn Word hoặc backend runtime.

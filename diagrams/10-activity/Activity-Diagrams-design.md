# Activity Diagrams — tám nhóm feature

[File draw.io tám tab](Activity-Diagrams.drawio) theo thứ tự [Class Diagram](../07-class/Class-Diagrams-design.md). Mỗi tab chọn **một luồng đại diện**, không thể hiện toàn bộ chức năng của nhóm và không khẳng định đáp ứng định nghĩa main workflow Review 2. Đây là thiết kế để review, không xác nhận runtime hay kiểm thử thực tế. Nguồn nghiệp vụ chi tiết là [sequence flows](../08-sequence/sequence_flows.py) và [inventory sequence](../08-sequence/Sequence-Groups-design.md); có tham chiếu report và FR ở các mục tương ứng.

| Tab | Luồng và giới hạn | Nguồn sequence | Ảnh |
|---|---|---|---|
| Authentication & Account | Một lần đăng nhập email code; dừng sau báo lỗi hoặc mở session. Yêu cầu mã mới và thử lại nằm ngoài sơ đồ. | Sign In With Email Code, IV 3.1.2; FR-01 | [PNG](01-Authentication-Account.png) |
| Project Workspace | Tạo project và membership Project Manager cho người tạo. | Create Project, IV 3.2.2 | [PNG](02-Project-Workspace.png) |
| Data Management | Upload bảng hợp lệ và tạo phiên bản có hash; không mô hình hóa Local Node. | Upload Dataset, IV 3.3.2 | [PNG](03-Data-Management.png) |
| Research Run Orchestration | Kiểm tra ngân sách và active run, rồi tạo run và lên lịch stage đầu; không mô tả toàn vòng đời run. | Start Research Run, IV 3.4.2 | [PNG](04-Research-Run-Orchestration.png) |
| Research Engines | Dataset Stage từ pinned version, profile và xác nhận cấu trúc đến split, contract, review và snapshot chờ acceptance. Nhánh chờ xác nhận nằm ngoài phạm vi. | Dataset Stage, IV 3.5.2 | [PNG](05-Research-Engines.png) |
| AI Principal Investigator | Phân loại yêu cầu theo policy; AI quyết tạm chỉ khi away, autopilot và non-pinned. Người dùng xác nhận hoặc overturn; nhánh chờ người dùng kết thúc ở ranh giới sơ đồ. | Handle Must-Ask and Tentative Decisions; Confirm or Overturn Tentative Decision, IV 3.6; FR-25–36 | [PNG](06-AI-Principal-Investigator.png) |
| Notifications & Integrations | Tạo thông báo in-app; chỉ nhánh blocking pinned hoặc spending được chọn người nhận đủ quyền và yêu cầu gửi kênh ngoài đang bật. | Receive Notifications, IV 3.7.2; FR-29, FR-100, FR-264 | [PNG](07-Notifications-Integrations.png) |
| Administration & Monitoring | Kiểm tra và lưu engine settings, ghi audit; không đại diện mọi tác vụ monitoring. | Edit Platform and Engine Settings, IV 3.8.4 | [PNG](08-Administration-Monitoring.png) |

Các bước mở màn hình, hiển thị form và lỗi là cách trình bày tương tác khái quát từ luồng tương ứng; không khẳng định tên màn hình hoặc thông điệp UI cụ thể. Nút final kết thúc luồng trong phạm vi hình; nhánh chờ trong tab AI PI không có nghĩa inbox item đã được trả lời hay run đã kết thúc, và nhánh lỗi không ngăn người dùng thử lại. Gửi thông báo qua kênh ngoài là yêu cầu gửi khi kênh được bật, không bảo đảm đã tới người nhận. Một số luồng đại diện đơn giản không thỏa tiêu chí main workflow (ít nhất hai actor hoặc ba tính năng, có đổi state); danh sách năm workflow Review 2 vẫn được theo dõi riêng trong [inventory](../README.md#10-activity).

## Kiểm tra

Kiểm tra số tab, kết nối và guard; chạy validator draw.io strict và xem tám PNG sau export. Rule hai lane và nhánh ngoại lệ theo mẫu được duyệt khác profile activitylint 3–4 lane chỉ cho main flow; không lấy kết quả profile đó làm kiểm chứng UML. Không có builder cho file này: `.drawio` là bản editable nguồn; không chạy tái tạo tự động để tránh ghi đè chỉnh sửa tay.

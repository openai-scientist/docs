# Rule: Screen Flow Diagram

Screen flow của web app sử dụng dạng navigation map phân nhánh, tham khảo [Screen Flow Diagram](https://online.visual-paradigm.com/community/share/screen-flow-diagram-jrf06icih) và hình mẫu của team. Sơ đồ thể hiện khu vực giao diện, các màn hình, chức năng, tab và dialog chính của từng khu vực; không phải UML hay activity diagram.

## File và phạm vi

- Dùng một file editable `Screen-Flow-Diagram.drawio` với ba tab chi tiết: **Access**, **Project Workspace**, **Admin**, tab hợp nhất **Navigation Detail** và phiên bản **Navigation - No Labels**. Quy tắc này là ngoại lệ cho quy định một page mỗi file trong [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).
- Export một PNG riêng cho mỗi tab, cùng folder, border 20 px, nền trắng. Với tab quá lớn, cho phép export ảnh tổng thể theo chiều rộng phù hợp; tách hình khi đưa vào report để chữ đọc được.
- Nội dung dựa trên frontend hiện tại; đối chiếu report khi danh sách màn hình và phân quyền được bổ sung. Không coi sơ đồ frontend là xác nhận requirement hoặc runtime.

## Quy tắc hiện hành sau review

- Bỏ toàn bộ dialog và nhánh nội dung bên trong dialog trên mọi tab. Mỗi ô màn hình phải có hậu tố Page; không đổi tên nghiệp vụ hay nhãn preview. Các quy tắc dialog bên dưới chỉ mô tả phiên bản lịch sử và không áp dụng cho bản hiện tại.

## Ký hiệu và bố cục

- Đi từ trái sang phải: điểm vào → layout/nhóm điều hướng → màn hình → chức năng, tab, màn hình con hoặc dialog.
- Màn hình, layout và khu vực điều hướng: hình chữ nhật nền xám nhạt, viền xám; điểm vào có thể dùng nền vàng nhạt như hình mẫu. Tên và điều kiện nằm trong ô.
- Dialog, modal, drawer: ô bo tròn, ghi rõ loại trong nhãn. Nhánh của dialog nối từ màn hình hoặc khu vực mở nó.
- Mũi tên liền thể hiện quan hệ mở hoặc điều hướng. Có thể dùng đường nhánh chung như mẫu; tránh đường xuyên ô, giao cắt và nhãn chồng nhau. Không bắt buộc ghi hành động trên mọi mũi tên khi đích và ngữ cảnh đã rõ; điều kiện quyền hoặc điều hướng không hiển nhiên phải ghi rõ.
- Dùng node layout chung để thể hiện sidebar/header, không lặp layout ở từng màn hình. Đặt khu vực Platform Admin riêng trong tab Admin.
- Arial, nền trắng, kích thước chữ và bố cục phải đọc được khi xuất ảnh; không đặt caption Figure hoặc đoạn chú thích phía trên ảnh.
- Navigation Detail giữ ô 340 × 120 px, khoảng trống dọc 40 px và chữ 28/22 px khi thu gọn chiều cao.
- Riêng **Navigation Detail**: mỗi ô chữ nhật là một screen/view có UI thực, tên là danh từ tên màn hình; dialog/drawer thật dùng ô bo góc và ghi loại. Không tạo ô cho nút/hành động, trạng thái xử lý, card/tab nội dung, layout/sidebar/header. Inventory phải truy vết tới frontend bằng `data-source-file` và phân loại bằng `data-kind`; không nhập máy móc mọi node của ba tab cũ.
- **Navigation Detail** giữ nền kem `#fffbed`, viền/mũi tên cam `#f29b31`; nhãn hành động/điều kiện chữ tối 22 px, căn giữa trên nét nối (`y=0`, `align=center`, `verticalAlign=middle`, `spacing=2`, nền trắng ngắt nét). Không dùng nền cam cho nhãn. Mỗi nguồn có corridor riêng; đóng dialog trở lại màn mở.
- Bản rút gọn giữ màn danh sách, màn chi tiết và dialog chính; lược CRUD, xác nhận xóa, drawer/activity/review, mode/tab phụ và vòng lặp thao tác tại chỗ. Chỉ gom các view thuộc cùng màn hình/flow thực, không tạo ô nhóm chức năng giả. Research Run giữ đủ 7 stage view đang mở; Writing chỉ giữ workspace và Manuscript, đánh dấu example preview. Data ẩn và Experiment/Interpret/Report đang khóa được ghi chú. Không coi việc lược ô là xóa chức năng hay thay requirement. Builder chỉ cập nhật Navigation Detail; giữ nguyên ba tab cũ.

- Phiên bản **Navigation - No Labels** phải clone đúng hình học, màn hình và cạnh của Navigation Detail; chỉ xóa nhãn hiển thị trên cạnh, giữ hành động trong metadata. Không sửa bản có nhãn khi tạo bản này; không tự đổi bố cục hoặc rút bớt ô.
- Hai bản **Navigation Detail - B&W** và **Navigation No Labels - B&W** chỉ đổi palette của bản tương ứng: fill/label background trắng, chữ/viền/mũi tên đen. Giữ nguyên ô, cạnh, nhãn, metadata, hình học và cỡ chữ; không sửa các tab nguồn khi tạo phiên bản.
- **Screen Flow - Vertical B&W** là bản bố cục theo ảnh mẫu: xác thực phía trên, 5 cột chính, màn con xếp dọc theo nhánh bên trái, Members/Project Settings ở hàng dưới. Được đổi geometry/ports/waypoints để bố trí, nhưng giữ nguyên node, loại màn/dialog, nhãn, metadata và endpoint của toàn bộ 41 cạnh từ bản B&W không nhãn. Giữ ô 340 × 120 px, chữ 28 px; không thêm nhóm chức năng hay Landing/Register/Forgot password nếu source chưa có. Không sửa bảy tab cũ khi tạo phiên bản này.

## Không được

- Vẽ xử lý server hoặc lời gọi API như màn hình.
- Dùng ảnh chụp thay cho node có thể chỉnh sửa.
- Khẳng định đầy đủ theo III 3.1.2/3.1.3 khi danh sách hoặc bảng phân quyền chưa có.

## Checklist

- [ ] Mỗi tab có điểm vào, phân nhánh rõ và các màn hình/dialog có nguồn frontend.
- [ ] Điều kiện role và nhánh đăng nhập thể hiện đúng; ngoại lệ hoặc đường chưa vẽ được ghi chú.
- [ ] PNG của từng tab bị sửa được export lại từ đúng tab sau lần sửa cuối; tab giữ nguyên không cần export lại.
- [ ] Khi report có screen descriptions và authorization, đối chiếu tên, độ bao phủ và role trước khi đưa vào report.

Bản Vertical B&W hiện dùng bố cục compact: cột cách 440 px, hàng cách 140 px; 7 stage Research Run chia hai cột trong vùng giữa, Admin chia hai cột, Members/Settings dùng vùng trống dưới Library. Giữ 35 Page/34 cạnh, chữ 28 px và các phiên bản khác.

Các bản ngang hiện cũng được thu gọn: khoảng cách cột 480 → 360 px, khoảng trống hàng 40 → 20 px, nhãn cạnh wrap trong 240 px để không đè ô. Bản màu/đen trắng/có nhãn/không nhãn và ảnh Research Run xuất lại cùng đợt; ba tab gốc thu bớt khoảng dọc dư sau khi bỏ dialog. Nội dung và cỡ chữ giữ nguyên.

Nhãn cạnh dùng hành động cụ thể và đúng đối tượng, không lặp Select + tên trang: Browse research runs, Inspect dataset details, Review screening results, Read evidence cards, Explore research gaps, Review proposed hypotheses, Read the signed manuscript. Đây là thao tác mở/xem màn hình tương ứng, không mô tả việc người dùng tự chạy thuật toán. Bản không nhãn giữ các mô tả này trong metadata.

Theo review mới nhất, bỏ dòng [example preview] khỏi nhãn ô Writing workspace Page và Manuscript Page trên mọi phiên bản. Phần giải thích dữ liệu ví dụ giữ trong README; thay nhãn trình bày không thay đổi trạng thái tích hợp hay hành vi frontend.

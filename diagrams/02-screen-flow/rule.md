# Rule: Screen Flow Diagram

Screen flow của web app sử dụng dạng navigation map phân nhánh, tham khảo [Screen Flow Diagram](https://online.visual-paradigm.com/community/share/screen-flow-diagram-jrf06icih) và hình mẫu của team. Sơ đồ thể hiện khu vực giao diện, các màn hình, chức năng, tab và dialog chính của từng khu vực; không phải UML hay activity diagram.

## File và phạm vi

- Dùng một file editable `Screen-Flow-Diagram.drawio` với ba tab: **Access**, **Project Workspace**, **Admin**. Quy tắc này là ngoại lệ cho quy định một page mỗi file trong [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).
- Export một PNG riêng cho mỗi tab, cùng folder, border 20 px, nền trắng. Với tab quá lớn, cho phép export ảnh tổng thể theo chiều rộng phù hợp; tách hình khi đưa vào report để chữ đọc được.
- Nội dung dựa trên frontend hiện tại; đối chiếu report khi danh sách màn hình và phân quyền được bổ sung. Không coi sơ đồ frontend là xác nhận requirement hoặc runtime.

## Ký hiệu và bố cục

- Đi từ trái sang phải: điểm vào → layout/nhóm điều hướng → màn hình → chức năng, tab, màn hình con hoặc dialog.
- Màn hình, layout và khu vực điều hướng: hình chữ nhật nền xám nhạt, viền xám; điểm vào có thể dùng nền vàng nhạt như hình mẫu. Tên và điều kiện nằm trong ô.
- Dialog, modal, drawer: ô bo tròn, ghi rõ loại trong nhãn. Nhánh của dialog nối từ màn hình hoặc khu vực mở nó.
- Mũi tên liền thể hiện quan hệ mở hoặc điều hướng. Có thể dùng đường nhánh chung như mẫu; tránh đường xuyên ô, giao cắt và nhãn chồng nhau. Không bắt buộc ghi hành động trên mọi mũi tên khi đích và ngữ cảnh đã rõ; điều kiện quyền hoặc điều hướng không hiển nhiên phải ghi rõ.
- Dùng node layout chung để thể hiện sidebar/header, không lặp layout ở từng màn hình. Đặt khu vực Platform Admin riêng trong tab Admin.
- Arial, nền trắng, kích thước chữ và bố cục phải đọc được khi xuất ảnh; không đặt caption Figure trong ảnh.

## Không được

- Vẽ xử lý server hoặc lời gọi API như màn hình.
- Dùng ảnh chụp thay cho node có thể chỉnh sửa.
- Khẳng định đầy đủ theo III 3.1.2/3.1.3 khi danh sách hoặc bảng phân quyền chưa có.

## Checklist

- [ ] Mỗi tab có điểm vào, phân nhánh rõ và các màn hình/dialog có nguồn frontend.
- [ ] Điều kiện role và nhánh đăng nhập thể hiện đúng; ngoại lệ hoặc đường chưa vẽ được ghi chú.
- [ ] Ba PNG được export lại từ đúng tab sau lần sửa cuối.
- [ ] Khi report có screen descriptions và authorization, đối chiếu tên, độ bao phủ và role trước khi đưa vào report.

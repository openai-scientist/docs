# Rule: System Overview v2

- Nội dung lấy từ code và file deploy production; không vẽ service, kết nối hay dịch vụ ngoài không có nguồn.
- Giữ bố cục và style v1. Không thêm note.
- Deployment: ký hiệu UML 2.5 nhưng node là hình chữ nhật phẳng, không dùng khối 3D (`«device»`, `«executionEnvironment»`, `«artifact»`), mọi communication path ghi giao thức.
- System Architecture: mọi mũi tên có nhãn động từ; không đường nào xuyên qua card.
- Vai trò người dùng dùng đúng 5 tên trong spec LOGOS.
- Sau mỗi lần sửa: chạy builder, `xmllint --noout`, export PNG và xem hình.

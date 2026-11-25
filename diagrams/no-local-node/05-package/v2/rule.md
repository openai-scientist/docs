# Rule: Package Diagram v2

- Chuẩn: UML 2.5.1 package diagram, style v1 (khung `pkg`, folder package, nền trắng, viền đen, Arial, dependency nét đứt đầu mở). Không có note, title hay chú thích thêm trên canvas.
- Package và dependency chỉ lấy từ code: thư mục `src`, các `pyproject.toml` và contract import-linter của `management`. Không thêm package theo spec mà code chưa có.
- Khung là namespace thật (`services`, `stages`, `packages`); không dùng `«layer»` hay nhóm tự đặt. Python import ghi `«use»`, không ghi `«import»`.
- Trong `management`, mỗi hàng là một lớp và chỉ vẽ dependency giữa hai lớp liền kề.
- Đường nối vuông góc, không xuyên package, chạm đúng package đích.
- Sau mỗi lần sửa: chạy builder, `xmllint --noout`, export PNG và xem hình.

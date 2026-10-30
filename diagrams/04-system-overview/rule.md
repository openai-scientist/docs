# Rule: System Overview Diagram

Chuẩn: C4 model (Simon Brown), mức 2 Container. Thoả yêu cầu SEP490 Report 4 mục 1.1 (sub-system, external system, kết nối) và Review 2 (thành phần, dịch vụ ngoài, luồng dữ liệu chính). Vị trí: Report 7 IV 1.1 chỉ dùng System Architecture Diagram (layered, IV-1) và Deployment Diagram (IV-2). Chỉ giữ file `.drawio`. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Cho người đọc thấy hệ thống gồm những khối chạy riêng nào, nói chuyện với nhau và với dịch vụ ngoài ra sao.

## Ký hiệu bắt buộc
| Element | Ký hiệu | Quy tắc |
|---|---|---|
| Tiêu đề | Text trên cùng | `Container diagram for OpenAI-Scientist`. Diagram C4 không dùng frame UML. |
| Người dùng | `C4 > Person` | 3 dòng: **Tên**, `[Person]`, mô tả 1 câu về vai trò. |
| Container của hệ thống | Hình chữ nhật, nền `#DAE8FC` | 3 dòng: **Tên**, `[Container: <công nghệ>]`, mô tả trách nhiệm 1 câu. Ví dụ `Platform API` / `[Container: FastAPI, Python 3.12]` / `Owns runs, objects and decisions`. Mọi container phải ghi công nghệ. |
| Kho dữ liệu | Hình trụ (cylinder) | `[Container: PostgreSQL 16]`, object storage… Theo C4, kho dữ liệu cũng là container. |
| Dịch vụ bên thứ ba | Hình chữ nhật nền xám `#F5F5F5` | `[Software System]` + mô tả. Google OAuth, LLM provider, email… Đúng bảng khai báo công nghệ của Report 4. |
| System boundary | Khung nét đứt quanh các container | Nhãn `OpenAI-Scientist [Software System]`. Local Node đặt ngoài boundary nếu chạy ở máy người dùng. |
| Luồng dữ liệu | Mũi tên **một chiều** | Nhãn cụ thể theo hướng mũi tên: **động từ + dữ liệu**, dòng dưới ghi `[giao thức]`. Ví dụ `Sends run commands` / `[HTTPS/JSON]`. Giữa các container bắt buộc ghi giao thức. |

## Bố cục
- Người dùng trên cùng, container ở giữa, kho dữ liệu dưới, dịch vụ ngoài bên phải.
- **Bắt buộc có legend** giải thích hình, màu, kiểu viền và kiểu đường. Viết tắt phải giải thích trong legend.
- Container trong C4 là ứng dụng hoặc kho dữ liệu chạy riêng, không có nghĩa là Docker container.

## Không được
- Đi vào class, bảng, hàm (đó là Package/Class Diagram).
- Mũi tên không nhãn hoặc nhãn chung chung như "uses".
- Thiếu dịch vụ ngoài có trong code (prompt self-review của Review 2 sẽ phát hiện).

## Checklist
- [ ] Mọi container và dịch vụ ngoài trong code và Report 4 đều có mặt, và ngược lại.
- [ ] Mọi mũi tên có nhãn và giao thức.
- [ ] Mọi element ghi rõ loại (`[Person]`, `[Container: …]`, `[Software System]`) và có mô tả.

## Nguồn
- Simon Brown, [C4 model: Notation](https://c4model.com/diagrams/notation) và [Container](https://c4model.com/abstractions/container).

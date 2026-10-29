# Rule: Screen Flow Diagram

Chuẩn: mẫu SEP490 Report 3, mục 3.1.1 Screens Flow (không thuộc UML; dùng quy ước wireflow/navigation map). Vị trí: III 3.1.1. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện các màn hình của web app và đường điều hướng giữa chúng. Màn hình nào được mở từ màn hình nào, bằng hành động gì.

## Ký hiệu bắt buộc
| Element | Ký hiệu | Quy tắc |
|---|---|---|
| Màn hình | Hình chữ nhật bo góc, 160×60 | Tên màn hình đúng như mục III 3.1.2 Screen Descriptions, kèm mã nếu có (`SC-03 Project Overview`). |
| Điểm vào | Hình tròn đen nhỏ | Điểm bắt đầu, thường nối tới Sign In. |
| Điều hướng | Mũi tên liền, đầu mũi tên đặc | Nhãn là hành động người dùng: `click "New run"`, `submit`. |
| Điều hướng có điều kiện | Mũi tên + nhãn `[điều kiện]` | Ví dụ `[role = Platform Admin]`. |
| Popup/dialog | Hình chữ nhật nét đứt | Gắn với màn hình cha. |
| Nhóm theo vai trò/khu vực | Container (swimlane hoặc group) | Ví dụ "Project workspace", "Run studio", "Admin console". |

## Bố cục
- Luồng đi từ trái sang phải hoặc trên xuống dưới, bắt đầu từ Sign In.
- Màn hình chung (header, navigation) không vẽ lặp; ghi chú "Global navigation available from all screens".
- Màn hình chỉ Platform Admin thấy đặt riêng một nhóm.

## Không được
- Vẽ logic xử lý phía server hay lời gọi API.
- Dùng ảnh chụp màn hình thay cho ô chữ nhật. Ảnh chụp đặt ở các mục `UI Screen` riêng.

## Checklist
- [ ] Mọi màn hình trong III 3.1.2 đều có mặt và có ít nhất một đường vào.
- [ ] Màn hình phân quyền khớp III 3.1.3 Screen Authorization.

## Nguồn
- Mẫu SEP490 Report 3, mục 3.1 System Functional Overview. Screen flow không có chuẩn quốc tế, nên rule này theo mẫu của trường.

# Rule: Package Diagram

Chuẩn: UML 2.5.1, mục 12 Packages. Mẫu SEP490 Report 4 mục 1.2 (package diagram cho mỗi sub-system kèm bảng Package Descriptions). Vị trí: IV 1.2 (IV-4). Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện cách code của từng sub-system (web app, Platform, engines) chia thành package/module và package nào phụ thuộc package nào.

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Package | `UML > Package` (folder có tab) | Tên đúng tên thư mục/namespace trong code hoặc module trong IV 1.2. |
| Sub-system | Package lớn chứa package con | Một khung cho mỗi sub-system. |
| Dependency | Mũi tên nét đứt, đầu mở `-->` | Từ package dùng tới package được dùng. Có thể ghi `«use»`, `«import»`. |

## Bố cục
- Xếp theo tầng: presentation/API trên, domain/service giữa, data/infrastructure dưới. Dependency chỉ đi xuống.
- Dưới diagram có bảng **Package Descriptions**: `No | Package | Description` (đúng mẫu SEP490).

## Không được
- Vòng phụ thuộc (A → B → A). Nếu code có thì báo leader và ghi trong Known Gaps.
- Vẽ class bên trong package (để Class Diagram).

## Checklist
- [ ] Package khớp cấu trúc thư mục code thật.
- [ ] Mọi package có dòng mô tả trong bảng.

## Nguồn
- OMG UML 2.5.1, §12 Packages.
- Ambler, [UML 2 Package Diagramming Guidelines](https://agilemodeling.com/style/packageDiagram.htm).
- [uml-diagrams.org: Package Diagrams](https://www.uml-diagrams.org/package-diagrams.html).

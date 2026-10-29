# Rule: Database Diagram

Chuẩn: ER mức vật lý, ký hiệu Crow's Foot. Mẫu SEP490 Report 4 mục 2 (table relationship và Table Descriptions). Review 2 yêu cầu khớp database script. Vị trí: IV 2.2. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện đúng các bảng trong database script: cột, kiểu, khoá, ràng buộc và quan hệ FK.

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Bảng | `Entity Relation > Table` | Tên đúng tên bảng trong migration/script (snake_case, ví dụ `research_runs`). |
| Cột | Mỗi dòng: `ký hiệu khoá` · `tên_cột` · `KIỂU` | Khoá ghi `PK`, `FK`, `UK`. Kiểu đúng DBMS (`UUID`, `TEXT`, `TIMESTAMPTZ`, `JSONB`…). Cột NOT NULL ghi `NN` hoặc in đậm, chọn một cách và giữ nguyên. |
| Quan hệ FK | Đường liền Crow's Foot | Nối từ cột FK tới cột PK của bảng được tham chiếu. Bản số ở hai đầu. |

## Bố cục
- Cùng cách gom nhóm như Logical ERD để dễ đối chiếu.
- Bảng nhiều cột có thể chỉ ghi cột khoá và cột nghiệp vụ chính, các cột còn lại ghi trong Table Descriptions.
- Diagram quá lớn thì tách theo nhóm, mỗi file `Database-Diagram-<Group>.drawio`.

## Không được
- Bảng hoặc cột không có trong script, hoặc ngược lại.
- Dùng tên entity PascalCase của bản logical.

## Checklist
- [ ] Đối chiếu từng bảng với database script; không lệch tên, cột, FK.
- [ ] Mỗi bảng có mục Table Descriptions trong IV 2.2.

## Nguồn
- draw.io, [Crow's foot notation for ER diagrams](https://www.drawio.com/blog/crows-foot-notation).
- Mẫu SEP490 Report 4, mục 2 Database Design; SWP490, Hướng dẫn chuẩn bị Review 2, mục 03.

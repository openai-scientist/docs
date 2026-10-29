# Rule: Entity Relationship Diagram (conceptual)

Chuẩn: ký hiệu Crow's Foot (Information Engineering, James Martin), mức conceptual. Vị trí: III 3.1.5 và IV 2.1 (IV-5). Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện các khái niệm nghiệp vụ chính và quan hệ giữa chúng, cho người đọc không cần biết kỹ thuật. Không có thuộc tính, khoá hay kiểu dữ liệu. Bảng, cột và FK nằm ở [06-database](../06-database/rule.md).

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Entity | Hình chữ nhật một ngăn (`Entity Relation > Entity`) | Chỉ ghi tên: danh từ số ít, PascalCase, đúng tên trong IV 2.1 (ResearchRun, Dataset, Project…). |
| Quan hệ | Đường liền, đầu Crow's Foot (`ERmandOne`, `ERzeroToOne`, `ERoneToMany`, `ERzeroToMany`) | Mỗi đầu gồm 2 ký hiệu. Ký hiệu **trong** (gần đường) là min: vòng tròn = 0 (tuỳ chọn), vạch = 1 (bắt buộc). Ký hiệu **ngoài** (sát entity) là max: vạch = 1, chân chim = nhiều. Ví dụ `\|\|` một và chỉ một, `o\|` không hoặc một, `\|<` một hoặc nhiều, `o<` không hoặc nhiều. |
| Tên quan hệ | Nhãn động từ giữa đường | Đọc từ trái sang phải hoặc trên xuống: `Project owns Dataset`. |

## Bố cục
- Gom entity theo nhóm như IV 2.1: Identity & project, Data, Run & stages, Hand-off objects, Local release & governance. Mỗi nhóm một vùng.
- Entity trung tâm (Project, ResearchRun) đặt giữa. Đường nối ngắn nhất có thể, không chéo nhau.
- Quan hệ nhiều-nhiều được phép vẽ trực tiếp (`>o—o<`). Không cần entity trung gian, trừ khi bản thân quan hệ là một khái niệm nghiệp vụ (ví dụ ProjectMembership mang vai trò).

## Không được
- Ghi thuộc tính, `PK`, `FK`, kiểu dữ liệu hoặc tên bảng snake_case (đó là mức logical/vật lý).
- Trộn ký hiệu Chen (hình thoi, hình elip) với Crow's Foot.
- Vẽ entity kỹ thuật không phải khái niệm nghiệp vụ (log, session, bảng monitoring, `alembic_version`).
- Vẽ entity không có trong report.

## Checklist
- [ ] Mọi entity nghiệp vụ trong IV 2.1 có mặt; không thừa entity.
- [ ] Mỗi quan hệ có tên và bản số ở **cả hai đầu**.
- [ ] Entity có bảng tương ứng trong database script, hoặc được ghi là "planned" trong report.
- [ ] Không trộn multiplicity kiểu UML (`0..*`) với ký hiệu Crow's Foot.

## Lưu ý Review 2
Hướng dẫn Review 2 ghi "Logical ERD". Team chọn vẽ mức conceptual; bảng thuộc tính của từng entity nằm ở phần Entity Descriptions (III 3.1.5, IV 2.1) và chi tiết bảng ở Database Diagram, nên hội đồng vẫn đối chiếu được với database script.

## Nguồn
- J. Martin, Information Engineering. Ký hiệu crow's foot do G. Everest đề xuất.
- draw.io, [Crow's foot notation for ER diagrams](https://www.drawio.com/blog/crows-foot-notation).
- Creately, [Crow's Foot Notation guide](https://creately.com/guides/crows-foot-notation/).
- Lucidchart, [Conceptual, logical and physical data models](https://www.lucidchart.com/pages/er-diagrams#section_3).

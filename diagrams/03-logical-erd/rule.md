# Rule: Entity Relationship Diagram (logical)

Chuẩn: ký hiệu Crow's Foot (Information Engineering, James Martin). Mức logical. Vị trí: III 3.1.5 và IV 2.1 (IV-5). Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện các entity nghiệp vụ, thuộc tính chính và quan hệ, độc lập với DBMS. Bản vật lý (bảng, kiểu dữ liệu) nằm ở [06-database](../06-database/rule.md).

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Entity | `Entity Relation > Table` | Tên danh từ số ít, PascalCase, đúng tên trong IV 2.1 (ResearchRun, Dataset, AnalysisPlan…). |
| Thuộc tính | Dòng trong entity | Ghi khoá chính `PK` và khoá ngoại `FK`, sau đó vài thuộc tính nghiệp vụ chính. Không ghi kiểu dữ liệu. |
| Quan hệ | Đường liền, đầu Crow's Foot (`ERmandOne`, `ERzeroToOne`, `ERoneToMany`, `ERzeroToMany`) | Mỗi đầu gồm 2 ký hiệu. Ký hiệu **trong** (gần đường) là min: vòng tròn = 0 (tuỳ chọn), vạch = 1 (bắt buộc). Ký hiệu **ngoài** (sát entity) là max: vạch = 1, chân chim = nhiều. Ví dụ `\|\|` một và chỉ một, `o\|` không hoặc một, `\|<` một hoặc nhiều, `o<` không hoặc nhiều. |
| Tên quan hệ | Nhãn động từ giữa đường | Đọc từ trái sang phải hoặc trên xuống: `Project owns Dataset`. |

## Bố cục
- Gom entity theo nhóm như IV 2.1: Identity & project, Data, Run & stages, Hand-off objects, Local release & governance. Mỗi nhóm một vùng.
- Entity trung tâm (Project, ResearchRun) đặt giữa. Đường nối ngắn nhất có thể, không chéo nhau.
- Quan hệ nhiều-nhiều phải tách thành entity trung gian (ví dụ ProjectMembership).

## Không được
- Trộn ký hiệu Chen (hình thoi) với Crow's Foot.
- Ghi kiểu dữ liệu, index, tên bảng snake_case (đó là mức vật lý).
- Vẽ entity không có trong report.

## Checklist
- [ ] Mọi entity trong IV 2.1 có mặt; không thừa entity.
- [ ] Mỗi quan hệ có bản số ở **cả hai đầu**.
- [ ] Khớp với Database Diagram và database script (yêu cầu Review 2).
- [ ] Không trộn multiplicity kiểu UML (`0..*`) với ký hiệu Crow's Foot.

## Nguồn
- J. Martin, Information Engineering. Ký hiệu crow's foot do G. Everest đề xuất.
- draw.io, [Crow's foot notation for ER diagrams](https://www.drawio.com/blog/crows-foot-notation).
- Creately, [Crow's Foot Notation guide](https://creately.com/guides/crows-foot-notation/).

# Rule: Activity Diagram

Chuẩn: UML 2.5.1, mục 15 Activities, có activity partition (swimlane). Review 2: activity diagram cho các luồng nghiệp vụ chính, thể hiện sự tham gia của actor, không mô tả xử lý chi tiết bên trong ứng dụng; mỗi main workflow (WF-xx) ứng với một activity diagram. Vị trí: IV 3.4–3.6 (IV-6, IV-9, IV-11, IV-13, IV-14), dùng lại trong VI 3 User Manual. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích
Thể hiện một workflow nghiệp vụ trọn vẹn, từ hành động khởi đầu của actor tới kết quả nghiệp vụ, ai làm bước nào.

## Ký hiệu bắt buộc
| Element | Ký hiệu draw.io | Quy tắc |
|---|---|---|
| Frame | `act <Tên workflow>` | Kèm mã: `act WF-01 Execute Research Run`. |
| Swimlane (partition) | `Container > Swimlane` **ngang** (khuyến nghị cho quy trình nghiệp vụ) | Chỉ tạo lane cho actor **thật sự tham gia** workflow đó, chọn trong Researcher, Project Manager, Reviewer, AI PI, System. Nên dưới 5 lane; vượt quá thì tách diagram. Sắp lane theo thứ tự xuất hiện. Bước nằm trong lane của người/hệ thống thực hiện. |
| Initial / Final | Chấm đen ở **góc trên trái** / chấm đen trong vòng tròn | Một initial, và **luôn có** activity final. Final đặt sau mỗi kết quả nghiệp vụ. Activity final kết thúc cả activity; flow final (vòng tròn có dấu X) chỉ dừng một nhánh. |
| Action | Hình chữ nhật bo góc | **Động từ + danh từ**, mức nghiệp vụ: `Approve extra spend`, không ghi `call POST /budget`. |
| Decision / Merge | Hình thoi, **không ghi nhãn** | Câu hỏi quyết định đã thể hiện qua action đứng trước. Mỗi nhánh ra **bắt buộc** có guard `[điều kiện]`. Các guard không trùng nhau và phải bao phủ đủ mọi trường hợp; dùng `[otherwise]` cho nhánh còn lại. Không thêm decision thừa. |
| Fork / Join | Thanh đen dày | Cho các bước song song. Join chờ mọi nhánh. |
| Object node | Hình chữ nhật thường, **nhỏ hơn action** | Chỉ vẽ hand-off object quan trọng giữa các bước (DatasetSpec, AnalysisPlan, EvidenceBundle…). Object xuất hiện nhiều lần thì ghi state theo vòng đời: `AnalysisPlan [locked]`. Object dùng chung giữa hai lane đặt trên đường phân cách lane. |
| Control flow | Mũi tên liền | Không nhãn trừ guard. |

## Bố cục
- Luồng chạy từ trên xuống (lane dọc) hoặc trái sang phải (lane ngang); giữ một hướng cho cả bộ.
- Mỗi workflow ghi ở góc dưới: Actors, Trigger, kết quả nghiệp vụ, state entity thay đổi (ví dụ `Research Run: running → ended(complete)`), FE liên quan, Owner. Đây là các trường Design Brief Phụ lục A yêu cầu.
- Có ít nhất một nhánh ngoại lệ chính, ứng với kịch bản demo ngoại lệ (DS-xxb).

## Không được
- Chi tiết bên trong ứng dụng: lời gọi API, query, class (để Sequence Diagram).
- Action không nằm trong lane nào.
- Decision không có guard, hoặc guard trùng nhau.
- Action "hố đen" (có đường vào, không có đường ra) hoặc action "phép màu" (có đường ra, không có đường vào).
- Guard trên nhánh ra của fork.

## Checklist
- [ ] Workflow có ít nhất 2 actor hoặc đi qua ít nhất 3 tính năng bắt buộc, và làm đổi state của ít nhất 1 thực thể chính (định nghĩa main workflow của Review 2, mục 9.1).
- [ ] Mọi bước có test hoặc được hiện thực trong code (prompt self-review kiểm tra).
- [ ] Tên workflow, actor, state khớp report và State Machine Diagram.

## Nguồn
- OMG UML 2.5.1, §15 Activities.
- Ambler, [UML 2 Activity Diagramming Guidelines](https://agilemodeling.com/style/activityDiagram.htm).
- [uml-diagrams.org: Activity Diagrams](https://www.uml-diagrams.org/activity-diagrams.html).
- SWP490, Hướng dẫn chuẩn bị Review 2, mục 03 và 9.1.

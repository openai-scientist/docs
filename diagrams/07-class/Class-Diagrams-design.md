# Class Diagrams — 8 tab theo nhóm feature

## Artifact

File editable chung: [Class-Diagram-Authentication-Account.drawio](Class-Diagram-Authentication-Account.drawio). Giữ tên artifact đã dùng để người dùng tiếp tục mở cùng file; nội dung hiện có cả tám nhóm, không chỉ Authentication. Mỗi tab là một Class Diagram, không phải Sequence hoặc Activity Diagram.


| Tab                              | PNG riêng                                           | Classifier | Nguồn chính trong Report7                                                                   |
| -------------------------------- | --------------------------------------------------- | ----------: | ------------------------------------------------------------------------------------------- |
| Authentication &amp; Account     | [PNG](Class-Diagram-Authentication-Account.png)     | 11         | IV 3.1; III 3.2; [thuyết minh chi tiết](Authentication-Account-design.md)                   |
| Project Workspace                | [PNG](Class-Diagram-Project-Workspace.png)          | 12         | IV 3.2, §2.1.1; III 3.3; FR-04–08, FR-111, FR-153, FR-263                                   |
| Data Management                  | [PNG](Class-Diagram-Data-Management.png)            | 15         | IV 3.3 và phần Local Node FE-12; III Data Management; FR-09–12, FR-80–87, FR-110, FR-112    |
| Research Run Orchestration       | [PNG](Class-Diagram-Research-Run-Orchestration.png) | 13         | IV 3.4, Budget FE-13, Dossier FE-14, Cross-Cutting Behavior; FR-13–24, FR-88–98, FR-262–266 |
| Research Engines                 | [PNG](Class-Diagram-Research-Engines.png)           | 15         | IV 3.5 và phần FE-07–11; FR-37–78, FR-113–137, FR-270                                       |
| AI Principal Investigator        | [PNG](Class-Diagram-AI-Principal-Investigator.png)  | 12         | IV 3.6; FR-25–36, FR-147–150, FR-262–266                                                    |
| Notifications &amp; Integrations | [PNG](Class-Diagram-Notifications-Integrations.png) | 12         | IV 3.7; III Notifications/Project settings; FR-29, FR-99–100, FR-264                        |
| Administration &amp; Monitoring  | [PNG](Class-Diagram-Administration-Monitoring.png)  | 11         | IV 3.8; FR-101–105; NFR-09, NFR-24                                                          |


Nguồn chính là `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md` do người dùng cung cấp, snapshot SHA256 `8618EB8123E0A3D259C9E5F5BA97F9E29602534AE3503B2AAA25E0D2E5EB232D`. Đối chiếu [Report IV trong repo](../../report/04-software-design-document.md) về entity, quan hệ và flow; [Report III](../../report/03-software-requirements-specification.md) về requirement. Không sửa file trong Downloads hoặc placeholder của report.

## Cách đọc và phạm vi đề xuất

Các slot Class Diagram trong Report7 còn trống. Controller/service, một số entity phụ, tên field, chữ ký operation và kiểu dữ liệu là **thiết kế đề xuất để duyệt**, không phải tên lớp hoặc API đã xác nhận trong implementation. Không suy ra runtime, deployment hoặc kiểm thử nghiệp vụ từ sơ đồ.

- `«controller»`: điểm vào, đại diện trách nhiệm điều phối request.
- `«service»`: logic nghiệp vụ hoặc trách nhiệm xử lý.
- `«entity»`: đối tượng dữ liệu trong view thiết kế. Audit/health/metric snapshot và các cấu hình phụ là biểu diễn đề xuất từ hành vi report, không khẳng định có bảng tương ứng.
- `«external»`: dịch vụ ngoài; không chốt SDK hoặc nhà cung cấp cụ thể.
- `«enumeration»`: tập giá trị. RunState gồm `running`, `waiting`, `ended`; lý do chờ và kết quả kết thúc nằm ở field riêng. Không biến từng waiting reason thành một state cấp cao khác.
- Nét đứt, mũi tên mở: dependency từ bên sử dụng tới bên được dùng. Nhãn mô tả trách nhiệm, không phải thứ tự xử lý. Nét liền: association hoặc composition, kèm multiplicity hai đầu; thoi đặc nằm ở phía toàn thể. Nét đứt, tam giác rỗng: realization hướng tới interface. Composition được mô hình hóa theo [Mermaid](Class-Diagrams-Mermaid.md) và các giả định bên dưới.
- Entity dùng chung chỉ hiện phần liên quan từng nhóm; tên và ý nghĩa không đổi giữa các tab. HandOffObject là tên view chung cho các object có version/hash/state, không khẳng định implementation có một superclass hoặc một bảng dùng chung.
- DTO/value type trong signature được lược khỏi hộp để giữ trọng tâm: `*Input`, `*Ref`, `Map`, `Table`, `CheckResult`, `Secret`, `Aggregate`, `Action`, v.v. Chúng là kiểu khái niệm, chưa phải schema API. Các kiểu domain như LiteratureBase/ResearchPattern được nhắc qua operation hoặc version reference, không mở thêm tab ngoài tám nhóm yêu cầu.
- Các class phụ được đề xuất gồm Invitation, Document, ProjectIntegration, NotificationPreference, SealedSecret, HealthSnapshot, OperatingMetrics và Export. Chúng cụ thể hóa hành vi đã mô tả, không bổ sung quyền hoặc chức năng nghiệp vụ mới.

## Quan hệ và ký hiệu — 2026-10-30

Theo yêu cầu mới về bố cục trên xuống và trải ngang, cả tám tab đã được sắp lại: controller ở trên khi tab có controller, các service/interface dàn ngang bên dưới, entity và enum đặt ở vùng dưới theo cụm liên quan. Research Engines không có controller nên bắt đầu bằng hàng service; một số adapter hoặc entity phụ nằm gần lớp liên quan để không bịa thêm tầng. Các đường dài được đi vòng khi cần tránh class, các nhánh còn lại ưu tiên nối thẳng.

Theo [Mermaid](Class-Diagrams-Mermaid.md), diagram dùng sáu composition: User–AuthSession, Project–ProjectSettings, Dataset–DatasetVersion, Run–StageRun, Dossier–Approval và Lock–Envelope; thoi đặc ở đầu toàn thể. Đây là các lựa chọn mô hình hóa đề xuất về sở hữu/vòng đời, không phải yêu cầu xóa cascade. Report chưa xác định đầy đủ vòng đời khi xóa cho mọi cặp; DatasetVersion và StageRun hiện có `RESTRICT` trong backend và lịch sử/version cần được bảo toàn. `DecisionInboxItem`–`DecisionLogEntry` vẫn là association vì vai trò lịch sử/audit chưa chốt. Project–ProjectSettings có thêm căn cứ từ Report IV §2.1.1 và model `ProjectSetting` của backend.

Sau khi xem trực tiếp bốn tab Class của mẫu GreenLens, bảy tab Authentication, Project, Data, Run, AI PI, Notifications và Administration dùng một số dependency chéo thẳng để các nhánh tỏa tự nhiên, thay cho hành lang vuông lặp lại. Các đường còn lại giữ tuyến thẳng hoặc gấp khúc theo không gian và tránh hộp; Research Engines giữ bố cục hiện có. Chỉ thay đường và vị trí nhãn, không đổi class, nội dung hay loại/chiều quan hệ.

Điều chỉnh tiếp sáu đường gấp tại Authentication, Data và Administration thành đường chéo, gồm `checks platform rights` theo ảnh phản hồi; đặt lại multiplicity cho association chéo User–AuthSession. Ba tuyến vòng còn lại tránh class hoặc các nhánh trung gian. Không đổi nội dung hoặc ngữ nghĩa của các đường.

Builder khai báo tường minh loại cho từng connector, không suy loại từ multiplicity. Các đường controller/service và tác vụ đọc, tạo hoặc xử lý được giữ là dependency ở mức thiết kế đề xuất; chúng không chứng minh implementation giữ hay không giữ tham chiếu. Khi thiết kế chi tiết xác nhận liên kết cấu trúc hoặc ownership/vòng đời, cần đối chiếu lại trước khi đổi ký hiệu.

Tab Data Management bổ sung `ConnectorFactory` và `Connector` dưới dạng interface, cùng `GoogleSheetsConnector` đại diện một implementation. `GoogleSheetsConnector` → `Connector` là realization cấu trúc (Python `Protocol`, không đòi kế thừa tường minh); factory trả về contract, còn `DataService` dùng factory trong flow import. Report IV 3.3 mô tả import từ kết nối được ủy quyền nhưng không quy định tên các class này: đây là chi tiết thiết kế bổ sung đối chiếu code, không phải thay đổi requirement. Nguồn code: [Connector protocol](../../../logos/services/management/src/management/connections/connectors/base.py), [factory](../../../logos/services/management/src/management/connections/connectors/__init__.py), [Google Sheets implementation](../../../logos/services/management/src/management/connections/connectors/google_sheets.py) và [dataset service](../../../logos/services/management/src/management/datasets/service.py). Chữ ký được biểu diễn ở mức UML, chuyển snake_case sang camelCase và `AsyncContext` là cách rút gọn kiểu async context manager; không coi đó là API public. Không thêm repository riêng vì phần service được khảo sát dùng SQLAlchemy `AsyncSession` trực tiếp, chưa có repository tương ứng cần biểu diễn. Các connector khác được lược khỏi view, không có nghĩa chỉ hỗ trợ Google Sheets.

Trong tab AI Principal Investigator, association `DecisionInboxItem`–`DecisionLogEntry` đặt `1` ở đầu inbox và `0..1` ở đầu log: một inbox item có tối đa một log khi đã quyết định, còn log được nối theo quan hệ này gắn với một inbox item. Căn cứ [Report IV §2.1.3](../../report/04-software-design-document.md). Điều này mô tả association đang vẽ, không khẳng định mọi log hệ thống đều thuộc một inbox item.

Tab Authentication giữ nguyên class, thành viên, ID và nhãn đã được người dùng duyệt. Kích thước hộp được cập nhật cùng toàn bộ tám tab theo yêu cầu mới dưới đây.

Kích thước class không còn dùng chung một chiều rộng: builder đo tên/stereotype bằng Arial Bold 19 và các dòng thành viên bằng Arial 17; chừa tổng đệm 48 px cho header, 32 px cho thành viên, làm tròn chiều rộng lên 10 px và giữ tối thiểu 190 px. Chiều cao vẫn theo số dòng, giữ nguyên nội dung và cách xuống dòng. Entity/enum ít nội dung gọn hơn service/controller. Khi thay chiều rộng, giữ tâm hộp để bảo toàn cụm, cập nhật chiều rộng các ngăn, port trên/dưới, waypoint liên quan và vị trí nhãn/multiplicity. Thay đổi này áp dụng cả Authentication và Research Engines; cả tám PNG được xuất lại.

Sáu tab Project Workspace, Data Management, Research Run Orchestration, AI Principal Investigator, Notifications &amp; Integrations và Administration &amp; Monitoring giữ hướng đọc gọn trái → phải nhưng dùng tọa độ riêng theo từng cụm quan hệ, thay lưới hàng/cột cách đều. Project/Membership và Dataset/Version giữ các entity dùng chung gần nhau; Invitation/Document, local execution/release, proposal/metrics được đặt thành cụm có cao độ và khoảng cách khác nhau. BudgetLedger nằm dưới BudgetService, NotificationChannel dưới IntegrationService; EngineSettings và ba kết quả monitoring tách thành các nhánh riêng. Khoảng cách dọc được thu lại sau render để tránh tăng khoảng rỗng. Canvas tự vừa phạm vi hộp; port và waypoint được tính lại theo tọa độ mới. Nhánh controller vẫn có nhãn trên đoạn ngang cuối, không đặt chữ giữa hai hành lang song song.

Authentication và Research Engines giữ nguyên trong lượt chỉnh sáu tab này. Research Engines đã có bố cục riêng theo cụm: HypothesisSet dưới HypothesisEngine, review sát PaperPack và nhánh Harness–Lock–Envelope phía dưới. Chỉ giữ căn thẳng tại nơi giúp nối trực tiếp, không xê dịch ngẫu nhiên từng hộp. So sánh trước/sau cho cả tám tab xác nhận ID, tên class, thành viên, nhãn, source/target và chiều quan hệ giữ nguyên; chỉ đổi hình học/port/waypoint/kiểu nhãn trên sáu tab được yêu cầu.

## Quy tắc nghiệp vụ giữ khi đọc thiết kế

Các nhánh từ controller đặt nhãn phía trên đoạn ngang cuối trước class nhận, không tự căn giữa toàn bộ polyline. Nhãn rộng 130–140 px và có thể xuống dòng, tâm nhãn lệch lên 28 px; tránh che hai hành lang dọc gần nhau. Nhãn dài trên các quan hệ ngang khác rộng 140 px, lệch lên 25 px. PNG được export lại sau mỗi thay đổi bố cục để kiểm tra vị trí thực tế.

Điều chỉnh tiếp theo cho chữ sát entity: multiplicity của toàn bộ association được neo cách endpoint 20 px thay vì tỷ lệ cố định theo tổng chiều dài; với đường ngang lệch xuống 10 px, đường dọc lệch trái 20 px để số nằm sát cạnh đường. Tên quan hệ của association dọc đặt bên phải đường để không đụng số; không đẩy multiplicity ngang quá xa. Trong Authentication, `checks access` được dịch sang trái tuyến vòng ngoài để không che AccountService. Chỉ thay vị trí nhãn, giữ nguyên class, đường nối và nội dung multiplicity. Authentication vì vậy giữ hình học class/edge đã duyệt nhưng vị trí nhãn được cập nhật theo phản hồi mới này. Đã export lại bảy PNG bị ảnh hưởng; tab Administration không có multiplicity nên không cần export lại.

- **Project:** không xóa PM hoạt động cuối cùng; archived là read-only; thay đổi quan trọng có audit; invitation hết hạn bị từ chối. ProjectSettings giữ review policy, monthly budget, preset và pinned wait deadline. Document là phần quản lý tài liệu của workspace, không thay PaperPack hay Dossier.
- **Data:** mỗi lần upload/import tạo version bất biến có hash; không preview/download raw local data. Local jobs cần kiểm hash và isolation. Release gate theo thứ tự firewall → rounding → disclosure → differencing → probe budget; release log append-only. Credential chỉ biểu diễn bằng SecretRef.
- **Run:** tối đa một active run/project; pipeline dataset_first; thay case đã xác nhận tạo amendment. Cancel từ mọi state trừ ended; upstream version mới làm downstream stale. Dossier chỉ tham chiếu accepted versions; approval không mang sang version mới; export phải có approved Dossier và pinned authorization. HandOffObject/Export trong tab là view rút gọn, không chứng minh toàn bộ reference graph.
- **Engines:** đủ năm engine và năm output chính. Split phải chờ người dùng xác nhận; lựa chọn hypothesis/primary và lock là pinned. Verdict/fitness/grade/claim ceiling do code tính. Envelope chỉ unseal khi đủ điều kiện; review độc lập và tối đa hai vòng. Harness/IndependentReviewService là trách nhiệm dùng chung dù chỉ vẽ một số dependency đại diện để tránh dày đường; không có nghĩa các engine khác được bỏ check/review. `requestUserLock` và `requestUnseal` là yêu cầu, không phải engine tự quyết thay user.
- **AI PI:** floor/override/preset/ceiling cùng áp dụng; AI PI chỉ quyết tạm non-pinned khi đúng điều kiện autopilot/away, không quyết pinned và không tự kết thúc run. Hết pinned deadline thì DecisionService đóng unanswered và kết thúc with_gaps. Overturn kéo theo undo dependent work và stale; metric chỉ đề xuất nâng level, không tự thay policy. Operation trong class không thay thế các guard này.
- **Notifications:** external notice chỉ dành cho blocking pinned và spending; recipient phải có quyền trả lời. Reminder pinned tới Researcher tạo run và PM; spending tới PM. Preference không nới rộng ngoại lệ thông báo ngoài. Comment luôn có anchor và quyền project.
- **Admin:** metadata của project không đồng nghĩa quyền đọc nghiên cứu. Secret không xuất hiện trong prompt/log/output. Thiếu model/key kết thúc failed_technical, không sinh sample output. Metric availability chưa có được giữ là unknown, không hiểu là zero chỉ vì field có kiểu số.

Các caption Sequence cũ như Answer Gate/Charter/Consultations/Reviewer Queue trong file xuất không được dùng để khôi phục flow đã bỏ khi không khớp requirement và phần thiết kế hiện hành. FE-18 JFE (Could, after MVP) và FE-19 method comparison (Should, after MVP) vẫn là phạm vi tương lai theo snapshot nguồn, không được đưa thành chức năng MVP qua các tab này.

## Tái tạo và export

[build_authentication_account.py](build_authentication_account.py) giữ phần Authentication đã duyệt và gọi [class_diagram_pages.py](class_diagram_pages.py) để thêm bảy tab. Builder nhỏ dùng chung hàm dựng class/connector giữa các tab, không tạo thêm tầng interface/repository không cần thiết.

Builder cần Python với Pillow và font Windows `C:/Windows/Fonts/arial.ttf`, `arialbd.ttf` để đo chiều rộng theo font thực tế trước khi ghi XML.

```powershell
python diagrams/07-class/build_authentication_account.py
python C:/Users/ADMIN/.agents/skills/drawio-skill/scripts/validate.py diagrams/07-class/Class-Diagram-Authentication-Account.drawio --score
```

Để xuất một tab, dùng draw.io CLI `-p <index>` với index từ **1 đến 8** theo bảng trên; PNG scale 2, border 20, nền trắng. Ví dụ tab 2:

```powershell
Start-Process -FilePath 'C:/Program Files/draw.io/draw.io.exe' -ArgumentList @('-x','-f','png','-s','2','-b','20','-p','2','-o','C:/Users/ADMIN/Desktop/Capstone/capstone-project-docs/diagrams/07-class/Class-Diagram-Project-Workspace.png','C:/Users/ADMIN/Desktop/Capstone/capstone-project-docs/diagrams/07-class/Class-Diagram-Authentication-Account.drawio') -WindowStyle Hidden -Wait
```

## Validation — 2026-10-29

- Sau lượt co chiều rộng theo nội dung: bảo toàn graph 8 tab/98 classifier và toàn bộ text; builder tái tạo ổn định, validator 0 errors/0 warnings (score 0). Xuất và xem lại tám PNG; kiểm tra ngăn vừa hộp, chữ đủ khoảng đệm, tuyến không xuyên hộp không liên quan và multiplicity vẫn gần endpoint.
- Sau lượt bỏ lưới đều trên sáu tab: builder tái tạo ổn định; validator 0 errors/0 warnings, score 0. Đã xuất và xem đủ sáu PNG, kiểm tra tuyến vuông góc không xuyên hộp class không liên quan, bảo toàn nội dung graph 98 classifier; Authentication và Research Engines giống hệt trước lượt sửa này.
- Builder tái tạo file 8 tab, 98 classifier, không placeholder rỗng. Kiểm tra page ID/cell ID, source/target, nhãn quan hệ, geometry và tính lặp lại của builder.
- Validator chung: **0 errors, 0 warnings, score 0** cho file nhiều tab.
- Đã xuất và xem PNG riêng của cả bảy tab mới; ảnh Authentication đã duyệt giữ nguyên. Kiểm tra chữ không bị cắt, port/đường nối, nhãn và overlap; không chỉ dựa vào XML syntax.
- Sau lần chỉnh bố cục trái → phải gọn hơn: xuất lại và kiểm tra trực quan sáu PNG bị ảnh hưởng; validator chung tiếp tục báo 0 errors/0 warnings, score 0. So sánh danh sách cell/value/source/target trước và sau layout xác nhận không thay nội dung hoặc loại bỏ quan hệ; file vẫn đủ tám tab/98 classifier. Controller dùng port theo từng nhánh; các đoạn đi lên và đi xuống dùng phần hành lang tách nhau, không gộp các quan hệ.
- Đã thử GreenLens `--package --strict`: profile này đòi đủ ERD/architecture/Use Case/Sequence/Class và nhận diện tên tab theo convention riêng; nó báo missing-family/unknown-page cho bộ chỉ có Class với tên nhóm feature. Không coi đây là kết quả pass; không áp dụng gate full GreenLens package cho artifact này. Dùng inventory 8 tab/class vocabulary và validator chung để kiểm tra phạm vi thực tế, không thêm các diagram khác chỉ để đáp ứng profile không phù hợp.
- Link local và `git diff --check` được kiểm tra. Chưa chèn ảnh vào Word, chưa kiểm tra in A4 hoặc xác nhận implementation/runtime. Khổ ngang, không frame/legend là lựa chọn người dùng đã chốt để xem diagram.

## Phạm vi Local Node trong phiên bản hiện tại (2026-10-30)

Theo xác nhận của người dùng, Local Node chưa triển khai. `LocalNode`, `LocalNodeService` và các quan hệ local work trong tab Data Management hiện mô tả thiết kế dự kiến từ Report7, không phải phần đã giao. Việc chúng xuất hiện trong Class không bắt buộc phải có State Diagram. Theo yêu cầu mới, bộ [State Diagram hiện tại](../09-state-machine/State-Machine-Diagrams-design.md) khôi phục vòng đời Local Node pairing và nhánh chờ node_offline của Run dưới dạng thiết kế dự kiến, không xác nhận chức năng đã triển khai. Ghi chú này không tái sinh hay sửa các lớp/quan hệ trong editable Class và không ghi đè nội dung Class đang được chỉnh sửa.

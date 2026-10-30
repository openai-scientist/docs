# Rule: Class Diagram

Chuẩn: UML 2.5.1, §7 Common Structure, §9 Classification, §10 Simple Classifiers và §11 Structured Classifiers. Vị trí trong report: IV 3.1.1 … IV 3.8.1, một diagram cho mỗi nhóm feature. Áp dụng thêm [quy tắc chung](../README.md#common-rules-bắt-buộc-cho-mọi-diagram).

## Mục đích và phạm vi

- Thể hiện cấu trúc thiết kế của feature: class, interface, enum, thuộc tính, phương thức chính và quan hệ. Đây là design class diagram; không chỉ liệt kê entity như ERD và không mô tả thứ tự gọi như Sequence Diagram.
- Theo yêu cầu người dùng, gộp 8 Class Diagram vào một file editable [Class-Diagram-Authentication-Account.drawio](Class-Diagram-Authentication-Account.drawio), mỗi nhóm feature một tab theo [danh mục diagram](../README.md#07-class). Giữ tên file đang dùng để tiếp tục mở cùng artifact. Không đổi sang một tab cho mỗi UC.
- Nội dung nghiệp vụ và tên gọi theo [Report IV](../../report/04-software-design-document.md), đối chiếu requirement trong [Report III](../../report/03-software-requirements-specification.md). Code dùng để kiểm chứng thiết kế; nếu khác report thì ghi nhận để leader chốt, không tự thay nội dung theo code.
- Chỉ đưa controller, service, repository, entity/model, helper/strategy, configuration/security hoặc external adapter vào khi có trong thiết kế và liên quan trực tiếp đến feature. Không bắt buộc đủ các tầng trong mọi diagram.
- Interface và lớp triển khai chỉ xuất hiện khi thiết kế có contract đó. SOLID không có nghĩa là mỗi service phải có thêm interface; tránh lớp, pattern và abstraction không cần thiết theo DRY, KISS, YAGNI.

## Phong cách theo hai ảnh tham chiếu

- Dùng hộp UML chữ nhật, nền trắng, viền mảnh, chữ đen; tên class in đậm, căn giữa; nội dung căn trái. Theo phong cách người dùng đã duyệt, không có frame ngoài, tiêu đề frame, legend hoặc ghi chú rời trong ảnh; tên tab xác định phạm vi. Đây là ngoại lệ có chủ đích so với quy tắc chung; giải thích ký hiệu nằm trong [thuyết minh](Class-Diagrams-design.md).
- Ảnh 1 tham chiếu cách tổ chức service/helper, interface/strategy, entity và enum. Ảnh 2 tham chiếu cách thể hiện controller, service interface/implementation, repository, entity và dịch vụ ngoài. Chỉ học cách trình bày; không sao chép tên lớp, công nghệ hoặc quan hệ của hệ thống trong ảnh vào dự án.
- Ưu tiên bố cục trái → phải: điểm vào ở trái, service/logic ở giữa, repository và entity ở phải hoặc phía dưới; enum đặt gần lớp sử dụng. Có thể xếp trên → dưới nếu ít giao cắt hơn. Không ép mọi diagram vào một cột dọc.
- Interface đặt gần implementation; lớp cha ở phía trên lớp con khi thuận bố cục. Chừa khoảng trống cho đường realization/generalization và nhãn.
- Không sao chép chữ quá nhỏ, nét quá nhạt hoặc phần bị cắt ở mép ảnh mẫu. Theo yêu cầu trải rộng để xem, các tab dùng canvas ngang, không ép vừa A4 bằng cách thu nhỏ chữ. Export PNG riêng từng tab ở scale 2, border 20, nền trắng. Chưa coi preview là bản in A4 đã kiểm chứng.

## Hộp class và thành viên

Trong draw.io, bật **More Shapes > Software > UML và UML 2.5**. Dùng shape class có các ngăn editable; không dùng ảnh chụp hoặc một text box giả toàn bộ diagram.

| Thành phần | Quy tắc |
|---|---|
| Class | Ba ngăn: tên, thuộc tính, phương thức. Tên PascalCase, danh từ số ít hoặc tên vai trò đầy đủ. Ngăn không có nội dung có thể để trống hoặc ẩn; không suy ra rằng class không có thành viên. |
| Stereotype | Đặt trên tên, trong `«…»`. `«interface»`, `«enumeration»` phân biệt loại phần tử; `«controller»`, `«service»`, `«repository»`, `«entity»`, `«external»` là quy ước vai trò của dự án, được giải thích trong thuyết minh thay cho legend trên ảnh. Không dùng stereotype để khẳng định framework chưa có. |
| Thuộc tính | `visibility name : Type [multiplicity] = default`. Ví dụ minh họa: `- status : RunState`, `- tags : String [0..*]`. Tên camelCase; chỉ thêm multiplicity/default khi đã xác định. |
| Phương thức | `visibility name(parameterName : Type) : ReturnType`. Ví dụ minh họa: `+ cancelRun(runId : UUID) : void`. Tên camelCase, diễn tả hành động; ghi kiểu tham số và kiểu trả về ở mức thiết kế chi tiết. |
| Visibility | `+` public, `-` private, `#` protected, `~` package. Dùng đúng thiết kế; không mặc định mọi thuộc tính private hoặc mọi phương thức public chỉ vì ảnh mẫu dùng như vậy. |
| Abstract class / operation | In nghiêng tên class hoặc operation trừu tượng; có thể thêm `{abstract}` để dễ nhận biết. Không đánh dấu concrete class là abstract. |
| Static member | Gạch chân thuộc tính/phương thức static; instance member không gạch chân. |
| Derived attribute | Dấu `/` trước tên, ví dụ `/remainingBudget : Decimal`, chỉ khi giá trị được tính từ dữ liệu khác trong thiết kế. |
| Interface | Hộp có `«interface»` và danh sách operation của contract. Không dùng chữ nghiêng làm dấu hiệu duy nhất để phân biệt interface; realization thể hiện lớp hiện thực contract. |
| Enum | Hộp có `«enumeration»`, tên enum và ngăn liệt kê literal đúng nguồn. Không thêm `+`/`-` hoặc coi literal là phương thức. Không cần ngăn phương thức trống. |

Giữ cú pháp UML `name : Type`, không trộn với `Type name` trong ảnh 1. Dùng nhất quán kiểu dữ liệu theo thiết kế; không tự chuyển thành kiểu Java chỉ vì ảnh mẫu có `UUID` hoặc `OffsetDateTime`.

## Quan hệ và chiều ký hiệu

Ký hiệu phải thể hiện đúng ngữ nghĩa trước khi chỉnh đường nối cho đẹp. Đầu connector bám vào viền hộp class, không bám vào dòng thuộc tính/phương thức.

| Quan hệ | Nét và đầu nối | Chiều / điều kiện dùng |
|---|---|---|
| Association | Nét liền; có thể không có mũi tên | Liên kết cấu trúc giữa các instance, như một đối tượng giữ tham chiếu tới đối tượng khác. Khi thể hiện navigability, dùng mũi tên mở tại lớp có thể được truy cập từ lớp nguồn. Không có mũi tên nghĩa là không chỉ rõ navigability trong view, không tự kết luận hai chiều. |
| Aggregation | Nét liền, thoi rỗng ở phía **toàn thể** | Quan hệ whole–part cho phép phần tồn tại độc lập. Nếu thiết kế chỉ chứng minh một liên kết thông thường thì dùng association. |
| Composition | Nét liền, thoi đặc ở phía **toàn thể** | Phần thuộc tối đa một composite tại một thời điểm và vòng đời chịu quản lý của composite. Chỉ dùng khi có bằng chứng về ownership/vòng đời; có FK hoặc cascade trong database chưa đủ để tự suy ra composition. |
| Generalization | Nét liền, tam giác rỗng tại **lớp cha** | Lớp con → lớp cha, nghĩa là “is a”. Không dùng để nối service tới repository. |
| Realization | Nét đứt, tam giác rỗng tại **interface** | Implementation → interface. Khác dependency ở đầu tam giác rỗng, không phải mũi tên mở. |
| Dependency | Nét đứt, mũi tên mở tại **phần tử được dùng** | Lớp phụ thuộc → lớp được dùng, chẳng hạn kiểu tham số, kiểu trả về hoặc sử dụng tạm thời. Không dùng nét đứt thay cho mọi association. |

### Nhãn, role và multiplicity

- Tên quan hệ đặt giữa đường khi cần làm rõ ý nghĩa, ví dụ `uses`, `manages`, `persists`; role đặt sát đầu liên quan, ví dụ `requester`, `details`. Nhãn không thay thế ký hiệu quan hệ.
- Với association, aggregation, composition giữa các instance, ghi multiplicity hai đầu: `1`, `0..1`, `0..*` (hoặc `*`), `1..*`. Giá trị ở đầu B là số instance B liên quan đến **một** instance A; kiểm tra cả chiều ngược lại.
- Không gắn multiplicity lên dependency, realization hoặc generalization. Một đường dùng kiểu enum thông thường là dependency; không tự thêm cardinality vào enum.
- Không suy cardinality từ tên số nhiều hoặc từ một bản ghi ví dụ. Nếu nguồn chưa đủ, ghi note “Multiplicity TBD” và đưa vào mục cần chốt; chưa coi diagram hoàn tất.
- Một cặp class có thể có nhiều association khi role khác nhau; phải ghi role rõ. Tránh vẽ đồng thời association và dependency chỉ để lặp lại cùng một liên kết.
- Mũi tên navigability không phải mũi tên thứ tự xử lý, request/response hoặc luồng dữ liệu. Class Diagram không dùng message đánh số như Sequence Diagram.

## Mức chi tiết và bố cục

- Chỉ hiện thành viên phục vụ feature: dữ liệu chính, operation nghiệp vụ, contract và helper cần giải thích. Bỏ getter/setter, constructor và import thông thường; chỉ nêu operation kỹ thuật nếu nó quyết định thiết kế đang mô tả.
- Không giới hạn cứng 8 dòng mỗi ngăn. Chiều rộng theo tên lớp và dòng thành viên dài nhất, chiều cao theo số dòng; không ép các hộp cùng chiều rộng hoặc chiều cao. Đo theo đúng font/size hiển thị, chừa đệm cho tên in đậm và nội dung; entity/enum ít thành viên gọn hơn service nhiều phương thức. Không thu nhỏ chữ hoặc thay nội dung để làm hộp bằng nhau. Nếu quá dày, lược thành viên ngoài phạm vi và dẫn tới thiết kế chi tiết.
- Class dùng chung có thể chỉ hiện tên và stereotype nếu chỉ làm ngữ cảnh. Khi thuộc tính/phương thức của nó cần cho feature, hiện phần liên quan; dùng cùng tên và chữ ký nhất quán giữa các diagram.
- Giữ thứ tự đọc trái → phải, gom service và entity thành các hàng gần nhau. Controller nhiều kết nối vẫn ở cột trái nhưng căn theo giữa nhóm service về chiều dọc để chia nhánh ngắn lên/xuống; không trải các cụm ra bốn phía tạo khoảng rỗng lớn. Giảm khoảng cách hàng/cột, dùng port riêng và hành lang ngắn để tránh dải đường dài song song. Không gộp dependency thành bus hoặc xóa quan hệ để làm thưa đường.
- Không ép mọi nhóm vào lưới có khoảng cách đều nhau. Áp dụng bố cục riêng theo quan hệ cho từng tab: gom entity dùng chung, tách nhánh hỗ trợ, cho phép cụm lệch cao độ và entity/external ở dưới service. Ví dụ BudgetLedger dưới BudgetService, NotificationChannel dưới IntegrationService và các kết quả monitoring thành ba nhánh. Giữ khoảng trống có mục đích, đường ngắn và nhãn rõ; không dịch hộp ngẫu nhiên chỉ để phá căn hàng. Thu khoảng cách theo nội dung và tính lại port/waypoint sau khi di chuyển hộp.
- Căn port cùng tọa độ để nối thẳng khi các class cùng hàng/cột. Đường khác dùng hành lang riêng, ưu tiên hai góc vuông; chỉ đi vòng ngoài khi cần tránh class trung gian. Đầu mũi tên dependency mở size 16, nét 1.5; đoạn cuối đi vuông góc vào cạnh class. Nhãn quan hệ ngắn đặt sát đường, giữ multiplicity tại hai đầu association.
- Khi các đường có đoạn song song gần nhau, không đặt nhãn giữa dải đường. Ưu tiên nhãn phía trên đoạn ngang cuối hướng vào class đích, giới hạn chiều rộng và xuống dòng khi cần; giữ khoảng trống với cả đường lân cận lẫn hộp class. Không dùng nền nhãn trắng để che một đường khác.
- Multiplicity không bám sát viền hoặc đè lên stereotype/entity: đặt tâm chữ cách đầu nối 20 px dọc theo đường, lệch xuống 10 px với đường ngang, lệch 20 px sang trái với đường dọc; tên quan hệ dọc đặt bên phải đường để không chạm số. Không đẩy số ra xa đường để tránh nhãn giữa. Kiểm tra riêng cả đầu source và target sau render, nhất là association dọc ngắn. Nhãn trên tuyến vòng ngoài phải nằm phía ngoài các class trung gian, không chèn vào vùng hộp để tiết kiệm lề.
- Tránh đường cắt hộp, nhãn đè lên cạnh, nhiều đường trùng đoạn hoặc tam giác/thoi bị che. Giao nhau không có nghĩa là nối; không tạo điểm nối ngoài ý muốn. Không thêm mọi loại quan hệ vào diagram chỉ để đủ bộ ký hiệu.

## Không được

- Biến diagram thành database schema với PK/FK, Crow's Foot hoặc toàn bộ cột bảng; FK không thay thế association.
- Bịa class, method, interface, enum literal hoặc quan hệ chỉ để giống ảnh mẫu. Thành phần mới phải có căn cứ trong thiết kế IV 3 trước khi đưa vào diagram.
- Suy inheritance từ tên gần giống nhau; suy composition từ “has a”; đảo đầu thoi hoặc đầu tam giác.
- Ép mọi lifeline trong Sequence Diagram thành class: actor, instance và dịch vụ ngoài cần được phân biệt với classifier nội bộ.
- Vẽ trực tiếp dịch vụ ngoài như entity/repository của hệ thống; nếu cần ngữ cảnh, đánh dấu `«external»` và chỉ hiện contract liên quan.

## Checklist

- [ ] Đủ 8 tab, đúng nhóm feature và slot IV 3.x.1; không đổi requirement để khớp ảnh.
- [ ] Class, thành viên và kiểu có căn cứ; khác biệt giữa report và code được ghi nhận.
- [ ] Các ngăn đúng vai trò; signature thống nhất `name : Type`; abstract/static/interface/enum phân biệt rõ.
- [ ] Mỗi quan hệ đúng loại, đúng chiều, đúng đầu mũi tên/thoi; multiplicity và role đúng nguồn.
- [ ] Class nội bộ tham gia Sequence Diagram của feature được đối chiếu; operation gọi tới tồn tại trên receiver hoặc contract tương ứng. Actor/external không bị biến thành class nội bộ.
- [ ] Không có thành viên trùng hoặc abstraction thừa; không có multiplicity TBD chưa chốt.
- [ ] Không cắt hộp/chữ, đường xuyên class, nhãn chồng nhau; đọc được ở kích thước chèn report.
- [ ] File `.drawio` còn editable và có đúng 8 tab; sau khi sửa diagram, chạy validator hiện hành, export lại PNG của tab bị ảnh hưởng và kiểm tra trực quan. Kiểm tra Markdown của rule không thay thế validation/render diagram.

## Nguồn

- [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/): chuẩn ngữ nghĩa; ưu tiên khi hướng dẫn công cụ hoặc ảnh minh họa giản lược ký hiệu.
- [Visual Paradigm — What is Class Diagram?](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-class-diagram/): tham khảo cấu trúc class, thuộc tính/operation, visibility, quan hệ và multiplicity.
- [draw.io — UML class diagrams](https://www.drawio.com/docs/diagram-types/uml/class-diagrams/): thư viện UML/UML 2.5, ngăn class và thao tác connector editable.
- Hai ảnh người dùng cung cấp ngày 2026-10-29: tham chiếu bố cục và phong cách trắng đen, không phải nguồn requirement hoặc định nghĩa UML.

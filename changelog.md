# Changelog

Định dạng theo [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Mỗi phiên bản là một mốc tài liệu theo ngày. Đường dẫn là đường dẫn tương đối từ repository root.

## 2026-10-30 — Bổ sung Repository trong toàn bộ Sequence Diagram

- Theo yêu cầu người dùng, thêm một Repository giữa Service và Database trong 64 tab của tám file chính và bản Email Code standalone. Mỗi request dữ liệu có call Service → Repository → Database và reply ngược lại; không còn Service gọi trực tiếp Database. Tên Repository theo trách nhiệm service của từng page.
- Đồng bộ [builder chung](diagrams/08-sequence/build_sequence_groups.py), [định nghĩa flow](diagrams/08-sequence/sequence_flows.py), [builder Email Code](diagrams/08-sequence/build_sign_in_with_email_code.py), editable và PNG theo [inventory](diagrams/08-sequence/Sequence-Groups-design.md). Email Code dùng chung renderer/flow với tab đầu Authentication để tránh hai bản lệch nhau; luồng gửi mã, xác minh, tạo account lần đầu và mở session được giữ.
- Cập nhật [rule](diagrams/08-sequence/rule.md), [thuyết minh Email Code](diagrams/08-sequence/Sign-In-With-Email-Code-design.md) và [inventory chung](diagrams/README.md#08-sequence). Đây là bổ sung tầng thiết kế sequence, không đổi nghiệp vụ nên không sửa BRD/PRD/Use Case Spec; không sửa BE hoặc Class Diagram.
- Validation: regenerate đủ tám file/64 tab và standalone; kiểm tra từng page có đúng một Repository, mọi Database call/reply đi qua Repository, model Email Code standalone khớp tab đầu. Validator `--strict --score` trên chín file: 0 errors, 0 warnings, score 0. Xuất lại 65 PNG, xem contact sheet toàn bộ tab và mở riêng trang phức tạp. Bốn PNG dài (Local Job, Hypothesis, Independent Review, Execution) bị native exporter cắt cuối ở scale 2, đã xuất scale 1 và kiểm tra có đủ message cuối; các PNG còn lại scale 2, cùng border 20/nền trắng. `python -I tools/doclint.py`, link local và `git diff --check` đạt; không stage/commit/push.

## 2026-10-30 — Bộ Sequence Diagram theo tám nhóm chức năng

- Tạo tám folder, mỗi folder một file draw.io chính, mỗi sequence là một tab: [Authentication & Account](diagrams/08-sequence/01-authentication-account/Sequence-Diagrams-Authentication-Account.drawio) (5), [Project Workspace](diagrams/08-sequence/02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) (12), [Data Management](diagrams/08-sequence/03-data-management/Sequence-Diagrams-Data-Management.drawio) (10), [Research Run Orchestration](diagrams/08-sequence/04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) (13), [Research Engines](diagrams/08-sequence/05-research-engines/Sequence-Diagrams-Research-Engines.drawio) (6), [AI Principal Investigator](diagrams/08-sequence/06-ai-principal-investigator/Sequence-Diagrams-AI-Principal-Investigator.drawio) (5), [Notifications & Integrations](diagrams/08-sequence/07-notifications-integrations/Sequence-Diagrams-Notifications-Integrations.drawio) (4), [Administration & Monitoring](diagrams/08-sequence/08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) (9).
- Nguồn là `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`, đối chiếu [thiết kế class](diagrams/07-class/Class-Diagrams-design.md). Bộ 64 tab ánh xạ đủ 61 heading sequence ở IV 3.1–3.8, thêm Execution, Paper theo IV 3.5 và Local Job theo IV-12; Lock/Unseal của IV-10 nằm trong hai tab Experiment Design và Execution. [Inventory](diagrams/08-sequence/Sequence-Groups-design.md) có link từng PNG, vị trí nguồn, hash snapshot và ánh xạ caption cũ sang nghiệp vụ hiện hành; không khôi phục v3 flow đã bỏ.
- Thêm [builder](diagrams/08-sequence/build_sequence_groups.py) và [định nghĩa flow](diagrams/08-sequence/sequence_flows.py); cập nhật [rule sequence](diagrams/08-sequence/rule.md), [inventory chung](diagrams/README.md#08-sequence). Authentication đủ năm sequence; tab Email Code giữ nguyên model XML đã duyệt, bản standalone và builder cũ vẫn được giữ.
- Giữ phong cách người dùng chốt: không frame ngoài, nền trắng, tên actor tách chân, call/reply phân biệt, guard có hàng riêng, không activation lồng dài qua opt. Activation phủ đủ các reply thay thế theo cặp caller–callee. Các operation/persistence chưa chốt là đề xuất thiết kế; không tự định nghĩa endpoint hoặc xác nhận runtime. Không đổi requirement BRD/PRD/Use Case Spec hoặc placeholder Report7, nên không cần sửa các tài liệu nghiệp vụ đó.
- Luồng Google gồm mở consent, từ chối hoặc callback, xác minh identity và ánh xạ cùng verified email. Handle Must-Ask và Receive Notifications khởi tạo bởi event hệ thống trong context đã xác thực; user không cần mở UI để backend xử lý, chỉ nhận update khi connected và authorized.
- Validation: tái tạo ổn định tám file và inventory; ánh xạ đủ 61 heading sequence, 64 tab/64 PNG, mỗi folder đúng một draw.io chính; model XML Email Code khớp bản đã duyệt. Validator `--strict --score` trên tám file: 0 errors, 0 warnings, score 0. Xuất PNG từng tab bằng draw.io CLI scale 2/border 20 nền trắng; xem contact sheet của toàn bộ tab và mở riêng các trang có fragment phức tạp, kiểm tra lại hai trang event sau sửa cuối. `python -I tools/doclint.py`: 13 file, 0 errors/0 warnings; link local, whitespace file mới và `git diff --check` đạt. Chưa kiểm tra in A4/chèn Word hoặc runtime; giữ nguyên staged changes đã có, không stage/commit/push.

## 2026-10-29 — Vẽ thử Sequence Sign In With Email Code

- Chỉnh vùng bước 20–26 bị rối: bỏ activation lồng dài của `resolveUser`, mở rộng khung `opt`, rút gọn guard thành `[account not found]` và tăng khoảng cách trước message tạo tài khoản. Đồng bộ builder/editable/PNG và thuyết minh; regenerate, validator 0 errors/0 warnings, xem lại PNG và `git diff --check` đạt. Không đổi nghiệp vụ.

- Hạ nhãn actor `User` thêm 10 px theo phản hồi; đồng bộ builder/editable/PNG và thuyết minh. Regenerate, validator 0 errors/0 warnings, xuất PNG và kiểm tra trực quan; `git diff --check` đạt. Chỉ chỉnh trình bày, không đổi nghiệp vụ.

- Thêm [sequence editable](diagrams/08-sequence/Sequence-Diagram-Sign-In-With-Email-Code.drawio), [PNG](diagrams/08-sequence/Sequence-Diagram-Sign-In-With-Email-Code.png), [builder](diagrams/08-sequence/build_sign_in_with_email_code.py) và [thuyết minh/nguồn](diagrams/08-sequence/Sign-In-With-Email-Code-design.md) cho ô IV 3.1.2, dựa trên `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md` III 3.2.1 và IV 3.1; đối chiếu [thiết kế Authentication](diagrams/07-class/Authentication-Account-design.md).
- Bao phủ yêu cầu mã email, xác minh mã, `alt` mã sai/hết hạn và thành công, `opt` tạo tài khoản lần đầu, tiêu thụ mã và mở session. Tên operation theo Class Diagram đề xuất; chi tiết persistence là thiết kế khái niệm, không chốt endpoint hoặc cách truyền session. Không thay nghiệp vụ/BRD/PRD/Use Case Spec hoặc placeholder report; không đổi diagram khác.
- Validation: builder chạy thành công; validator cấu trúc 0 errors, 0 warnings, score 0; draw.io CLI xuất PNG zoom 200%, border 20 nền trắng, đã xem trực quan sau lần sửa cuối. `python -I tools/doclint.py` đạt; link local trong thuyết minh và entry này tồn tại; `git diff --check` sạch. Chưa kiểm tra in A4/chèn Word hoặc runtime backend.
- Theo phản hồi tiếp theo: bỏ khung `sd` ngoài cùng và tiêu đề của khung, giữ nguyên `alt`/`opt` và tương tác. Đồng bộ builder, editable, PNG và thuyết minh; regenerate, validator 0 errors/0 warnings, xuất lại PNG và xem trực quan; `git diff --check` đạt. Không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec.

## 2026-10-29 — Điều chỉnh rule Sequence Diagram theo hướng dẫn và ảnh mẫu

- Cập nhật [rule Sequence Diagram](diagrams/08-sequence/rule.md) theo [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-sequence-diagram/), [draw.io](https://www.drawio.com/docs/diagram-types/uml/sequence-diagrams/) và ảnh Admin/Audit Session người dùng gửi: bố cục actor–UI–controller–service–repository–database, call/reply, activation theo lần xử lý, đánh số message, fragment và checklist.
- Làm rõ khung `alt` phải bao cả nhánh lỗi và thành công, reply về caller trực tiếp, tên participant/API phải có nguồn; ảnh chỉ hướng dẫn phong cách. Giữ một file/một sequence và nguyên tắc gộp theo cấu trúc tương đương trong [inventory](diagrams/README.md#08-sequence).
- Phạm vi chỉ là quy tắc mô hình hóa, không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec. Folder `08-sequence` hiện chỉ có rule; không sửa hoặc regenerate diagram/builder, không có render check trong đợt này.
- Validation: đối chiếu hai hướng dẫn và quy tắc chung; `python -I tools/doclint.py` đạt (13 file, 0 errors, 0 warnings); kiểm tra link local trong rule và entry này, `git diff --check` đạt.

## 2026-10-29 — Co kích thước class theo nội dung

- Áp dụng chiều rộng theo tên lớp và thành viên cho cả tám tab trong [file draw.io chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), thay hộp rộng đồng loạt bằng entity/enum gọn và service/controller rộng theo nhu cầu. Đồng bộ [builder chính](diagrams/07-class/build_authentication_account.py), [helper đo Arial/Pillow](diagrams/07-class/class_diagram_pages.py), tám PNG trong [inventory](diagrams/07-class/Class-Diagrams-design.md), [thuyết minh Authentication](diagrams/07-class/Authentication-Account-design.md) và [rule](diagrams/07-class/rule.md). Giữ cỡ chữ, nội dung, tâm cụm và chiều cao theo dòng; cập nhật port/waypoint/nhãn sau đổi chiều rộng.
- Chỉ sửa trình bày nên không cần sửa BRD/PRD/Use Case Spec. Validation: graph 8 tab/98 classifier không đổi nội dung, builder tái tạo ổn định, validator 0 errors/0 warnings (score 0), kiểm tra tuyến/khung ngăn và xuất/xem tám PNG; kiểm tra link mới và `git diff --check`.

## 2026-10-29 — Điều chỉnh sáu Class Diagram còn lại theo cụm

- Thay lưới đều trên sáu tab Project Workspace, Data Management, Research Run Orchestration, AI Principal Investigator, Notifications & Integrations và Administration & Monitoring bằng bố cục riêng theo quan hệ; giữ hướng trái → phải, thu khoảng cách dọc và đặt nhánh hỗ trợ gần lớp sử dụng. Đồng bộ [file editable tám tab](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), [builder](diagrams/07-class/class_diagram_pages.py), sáu PNG và [thuyết minh/inventory](diagrams/07-class/Class-Diagrams-design.md), [rule](diagrams/07-class/rule.md).
- Chỉ đổi trình bày, không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec. Bảo toàn class/thành viên/nhãn/quan hệ của tám tab, giữ nguyên Authentication và Research Engines. Validation: builder tái tạo ổn định, validator 0 errors/0 warnings (score 0), kiểm tra tuyến không xuyên hộp khác, xuất và xem đủ sáu PNG, kiểm tra liên kết và `git diff --check`.

## 2026-10-29 — Bố trí Research Engines theo cụm quan hệ

- Chỉnh riêng tab Research Engines trong [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): thay lưới lặp bằng cụm dữ liệu/giả thuyết, thực thi/review và nhánh Harness–Lock–Envelope; phối hợp quan hệ ngang/dọc với cao độ khác nhau. Nhãn dài xuống dòng trong hành lang. Đồng bộ [builder](diagrams/07-class/class_diagram_pages.py), [PNG](diagrams/07-class/Class-Diagram-Research-Engines.png), [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md).
- Chỉ đổi trình bày, không đổi class/thành viên/quan hệ/nghiệp vụ; không cần sửa BRD/PRD/Use Case Spec. Validation: validator 0 errors/0 warnings, score 0; xuất và xem PNG, kiểm tra graph và bảy tab khác không đổi, builder tái tạo ổn định và `git diff --check`.

## 2026-10-29 — Kéo số sát đường association ngang

- Theo phản hồi, giảm offset dọc của multiplicity ngang từ 22 xuống 10 px trong [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), giữ vị trí gần hai endpoint. Đồng bộ [helper](diagrams/07-class/class_diagram_pages.py), bảy PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md). Chỉ đổi vị trí chữ, không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec.
- Validation: builder, validator 0 errors/0 warnings (score 0), export và xem PNG; bảo toàn nội dung graph, kiểm tra `git diff --check`.

## 2026-10-29 — Đặt multiplicity sát hai đầu association

- Theo phản hồi, đưa số về gần hai đầu nối trong [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): tâm số cách endpoint 20 px thay vì 38 px, vẫn nằm ngoài hộp. Giữ số dọc sát trái đường và tên quan hệ bên phải; không đổi nội dung hoặc quan hệ. Đồng bộ [helper](diagrams/07-class/class_diagram_pages.py), bảy PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md). Không đổi nghiệp vụ nên không sửa BRD/PRD/Use Case Spec.
- Validation: builder, validator 0 errors/0 warnings (score 0), export/xem các PNG bị ảnh hưởng và kiểm tra `git diff --check`.

## 2026-10-29 — Đưa multiplicity sát cạnh đường nối

- Điều chỉnh [Class Diagram chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): multiplicity dọc lệch trái 20 px thay vì 76 px, giữ cách endpoint 38 px; tên association chuyển sang bên phải đường để không chạm số. Đồng bộ [helper](diagrams/07-class/class_diagram_pages.py), bốn PNG bị ảnh hưởng, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md). Không đổi class/quan hệ/nghiệp vụ nên không sửa BRD/PRD/Use Case Spec.
- Validation: builder, validator 0 errors/0 warnings (score 0), export và xem PNG; bảo toàn nội dung tám tab và `git diff --check`.

## 2026-10-29 — Tách chữ khỏi viền entity và class trung gian

- Sửa vị trí multiplicity trên toàn bộ association trong [file Class Diagram chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): cách endpoint 38 px, lệch khỏi đường để không đè viền/stereotype hoặc nhãn giữa đường. Dịch `checks access` sang ngoài tuyến vòng bên trái, tránh AccountService. Giữ nguyên nội dung, class và tuyến đường; đồng bộ [builder Authentication](diagrams/07-class/build_authentication_account.py), [helper nhãn](diagrams/07-class/class_diagram_pages.py), bảy PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md).
- Chỉ sửa trình bày nên không cần cập nhật BRD/PRD/Use Case Spec. Validation: builder tái tạo, bảo toàn graph tám tab/98 classifier, validator 0 errors/0 warnings (score 0), export/xem các PNG bị ảnh hưởng và `git diff --check`.

## 2026-10-29 — Tách nhãn quan hệ khỏi các đường song song

- Sửa nhãn controller trên sáu tab trong [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): đặt phía trên đoạn ngang cuối trước class đích, giới hạn 130 px và xuống dòng; không đặt chữ giữa hai đường dọc gần nhau. Giữ nguyên nội dung nhãn, class và quan hệ. Đồng bộ [builder/layout](diagrams/07-class/class_diagram_pages.py), sáu PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md); không đổi nghiệp vụ nên không sửa BRD/PRD/Use Case Spec.
- Validation: builder tái tạo, validator 0 errors/0 warnings (score 0); xuất lại và xem PNG, kiểm tra bảo toàn graph tám tab và `git diff --check`.

## 2026-10-29 — Gom gọn Class Diagram theo chiều trái → phải

- Theo phản hồi mới nhất, bỏ bố cục tỏa bốn phía trên sáu tab; trở về thứ tự controller → service → entity/enum. Controller ở cột trái, căn giữa nhóm service theo chiều dọc; hàng/cột gần nhau hơn, đường chia nhánh ngắn lên/xuống để hạn chế song song dài và khoảng rỗng. Đồng bộ [file chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), [builder/layout](diagrams/07-class/class_diagram_pages.py), sáu PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md).
- Chỉ đổi bố cục, giữ toàn bộ class/thành viên/nhãn/quan hệ; không đổi requirement nên không cần sửa BRD/PRD/Use Case Spec. Validation: builder tái tạo, so sánh graph tám tab, validator 0 errors/0 warnings (score 0), export và xem sáu PNG; kiểm tra link và `git diff --check`.

## 2026-10-29 — Đặt class nhiều kết nối vào giữa cụm

- Theo phản hồi người dùng, bố trí lại sáu tab trong [file Class Diagram chung](diagrams/07-class/Class-Diagram-Authentication-Account.drawio): controller ở giữa, chia nhánh lên/xuống và trái/phải, service/entity gần nhau; tách port để tránh dải đường song song hoặc đi chung đoạn. Authentication và Research Engines giữ nguyên bố cục. Đồng bộ [source layout](diagrams/07-class/class_diagram_pages.py), sáu PNG, [rule](diagrams/07-class/rule.md) và [thuyết minh](diagrams/07-class/Class-Diagrams-design.md).
- Không đổi class, thành viên, loại/chiều quan hệ hoặc nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec. Validation: so sánh ID/value/source/target trước–sau cho cả tám tab; builder tái tạo; validator 0 errors/0 warnings, score 0; PNG đã export và xem trực quan; `git diff --check` sạch. Không thay placeholder report hoặc các thay đổi Use Case không liên quan.

## 2026-10-29 — Hoàn thiện bộ Class Diagram chung 8 tab

- Mở rộng [file draw.io đang dùng](diagrams/07-class/Class-Diagram-Authentication-Account.drawio) thành tám tab: Authentication & Account, Project Workspace, Data Management, Research Run Orchestration, Research Engines, AI Principal Investigator, Notifications & Integrations, Administration & Monitoring. Giữ nguyên graph Authentication đã duyệt, thêm bảy PNG riêng theo phong cách không frame, trải ngang, mũi tên lớn có nhãn và ít góc gấp.
- Đồng bộ [builder](diagrams/07-class/build_authentication_account.py), [source bảy tab mới](diagrams/07-class/class_diagram_pages.py), [thuyết minh/ánh xạ nguồn và validation](diagrams/07-class/Class-Diagrams-design.md), [rule](diagrams/07-class/rule.md), [inventory](diagrams/README.md) và ghi chú Authentication. Các lớp/signature vẫn là thiết kế đề xuất dựa trên Report7 người dùng gửi và Report III/IV, không phải reverse-engineering implementation; không đổi requirement nên BRD/PRD/Use Case Spec và placeholder report giữ nguyên.
- Validation: builder tái tạo; inventory tám tab/98 classifier, kiểm tra bảo toàn graph Authentication, ID/edge target/link và tính lặp lại; validator chung 0 errors/0 warnings, score 0. draw.io CLI xuất PNG từng tab mới, đã xem trực quan; `git diff --check` sạch. GreenLens full-package gate không phù hợp với bộ chỉ có Class, đã ghi rõ missing-family/unknown-page trong thuyết minh; không báo pass profile đó. Chưa kiểm tra in A4/chèn Word/runtime.

## 2026-10-29 — Vẽ thử Class Diagram Authentication & Account

- Làm gọn đường nối theo phản hồi: căn port cùng tọa độ cho đường thẳng ngang/dọc, bỏ các đoạn gấp nhỏ, đặt waypoint theo hành lang với tối thiểu góc gấp cần thiết. Giữ nhãn, đầu mũi tên lớn và nội dung class. Đồng bộ builder/editable/PNG/thuyết minh; validator 0 errors/0 warnings, score 0; đã xuất lại PNG bằng draw.io CLI, xem trực quan và kiểm tra `git diff --check`.
- Sửa đầu mũi tên vào class: pin trên cạnh, thêm đoạn tiếp cận vuông góc, tăng đầu mở lên size 16/nét 1.5; khôi phục nhãn quan hệ theo ảnh mẫu. Đồng bộ builder/editable/PNG/thuyết minh, giữ nguyên nội dung lớp. Builder và validator đạt 0 errors/0 warnings (score 0); đã xuất/xem PNG và chạy `git diff --check`.
- Bỏ khung ngoài và tiêu đề frame theo yêu cầu; giữ tọa độ class và đường nối. Đồng bộ builder/editable/PNG và thuyết minh; validator 0 errors/0 warnings, đã xem PNG và kiểm tra `git diff --check`. Không đổi nghiệp vụ.
- Điều chỉnh bản xem thử theo phản hồi: trải ngang canvas 2320 × 1300, tăng khoảng cách các cụm, bỏ ghi chú/legend/trạng thái và nhãn diễn giải ngoài class, giữ multiplicity và tiêu đề. Đồng bộ builder, editable, PNG và thuyết minh; nghiệp vụ và thành viên class không đổi. Regenerate và xuất lại PNG; validator 0 errors/0 warnings, score 0; đã xem trực quan và chạy `git diff --check`.
- Thêm [Class Diagram editable](diagrams/07-class/Class-Diagram-Authentication-Account.drawio), [PNG preview](diagrams/07-class/Class-Diagram-Authentication-Account.png), [builder](diagrams/07-class/build_authentication_account.py) và [thuyết minh/ánh xạ nguồn](diagrams/07-class/Authentication-Account-design.md), dựa trên `xFA26SE115_Report7.md` người dùng gửi (III 3.2, IV 3.1) và đối chiếu [Report IV](report/04-software-design-document.md). Bao phủ passwordless email, Google sign-in, profile/onboarding, session/sign-out và quyền project/Platform Admin.
- Các lớp và signature là thiết kế đề xuất để duyệt vì slot IV 3.1.1 đang trống. Không thay placeholder/report hoặc BRD/PRD/Use Case Spec: không có thay đổi yêu cầu nghiệp vụ. Không sửa diagram khác hoặc các thay đổi Use Case đang có.
- Validation: chạy builder; validator báo 0 errors, 0 warnings, score 0; XML một page, 11 classifier; draw.io CLI xuất PNG scale 2/border 20 nền trắng và đã xem trực quan. Kiểm tra link local và `git diff --check`; chưa kiểm tra in A4/chèn Word hoặc runtime.

## 2026-10-29 — Điều chỉnh rule Class Diagram theo hướng dẫn và ảnh mẫu

- Cập nhật [rule Class Diagram](diagrams/07-class/rule.md) theo [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-class-diagram/), [draw.io](https://www.drawio.com/docs/diagram-types/uml/class-diagrams/) và hai ảnh tham chiếu: bố cục trái → phải, hộp UML trắng đen, signature, interface/abstract/enum, chiều quan hệ, role và multiplicity. Giữ 8 diagram theo nhóm feature; làm rõ ảnh không phải nguồn để thêm lớp hoặc công nghệ.
- Phạm vi chỉ là hướng dẫn mô hình hóa; không đổi nghiệp vụ nên không cần sửa BRD/PRD/Use Case Spec. Folder `07-class` hiện chỉ có rule, chưa có builder/diagram để regenerate hoặc render.
- Validation: đối chiếu rule với nguồn và quy tắc chung; kiểm tra link local và `git diff --check`. Chưa có validation/render của diagram.

## 2026-10-29 — Hoàn tác sửa diagram, bàn giao checklist tự vẽ

- Khôi phục [Use Case editable](diagrams/01-use-case/AI-Research-Experimentation-Platform-Use-Case.drawio) nguyên byte từ bản trước lần sửa diagram gần nhất; gỡ PNG được tạo trong lần sửa đó. Giữ quy tắc phong cách một trang đã được người dùng chốt và các thay đổi không liên quan.
- Thêm [checklist cập nhật Use Case](diagrams/01-use-case/use-case-update-checklist.md): ưu tiên, actor/quyền, ánh xạ nhãn cũ, chức năng cần bổ sung, quan hệ UML và danh sách đủ 41 UC có FE/FR theo [Report III](report/03-software-requirements-specification.md), [BRD](BRD.md), [PRD](PRD.md). Người dùng tự vẽ; không sửa requirement hoặc nội dung diagram.
- Chốt phạm vi view: 6 actor (User, Researcher, Project Manager, Reviewer, Platform Admin, AI Provider); không vẽ Persona/AI PI và tạm chưa đưa Local Node vào use case. Checklist/rule bỏ UC-08/30/31 khỏi lần vẽ này, còn 38 UC, giữ nguyên ID; kiểm tra bảng đủ 38 dòng, không còn association Persona/Local Node. Diagram và BRD/PRD/Report7 không đổi.
- Theo điều chỉnh mới của người dùng: checklist bỏ actor AI PI, giữ tên AI Provider và ba association hỗ trợ UC-19/20/25; giải thích khác biệt giữa provider, maker/guard persona và AI PI. Không chuyển quyền quyết định tạm sang provider; diagram và requirement nguồn chưa đổi.
- Đối chiếu thêm bản `xFA26SE115_Report7.md` người dùng gửi: bảng 41 UC/FE/FR khớp nguồn repo; chỉnh checklist dùng actor Persona cho maker/guard, User cho Sign in, bỏ LLM provider khỏi phương án mặc định và sửa tham chiếu validation upload về bước 2. Ghi nhận hai lỗi trình bày trong Report7 (thiếu heading UC-01 và chú thích approval `[a]` bị rơi); không sửa file Downloads hay diagram.
- Chi tiết hóa checklist thành thao tác cụ thể: 20 oval đổi tên, 21 oval thêm mới, danh sách oval/đường gốc cần xóa, bảng actor–UC cho đủ 41 UC, một generalization PM → Researcher và một include upload → validate; không đề xuất extend. Kiểm tra inventory oval khớp XML gốc, link local tồn tại và diagram không bị sửa.
- Theo yêu cầu người dùng, checklist không đề xuất actor Google/Email hoặc oval riêng cho từng phương thức đăng nhập; giữ UC-01 Sign in tổng quát, không thay đổi yêu cầu xác thực trong BRD/PRD.
- Validation: diagram khôi phục khớp byte bản sao lưu và có một page; checklist đủ 41 mã UC duy nhất; link local trong checklist và entry này tồn tại; `git diff --check` đạt. Không render lại vì sơ đồ được khôi phục nguyên bản.

## 2026-10-29 — Giữ cấu trúc Use Case một trang

- Cập nhật [quy tắc Use Case](diagrams/01-use-case/rule.md): giữ bố cục sơ đồ cũ trên một trang, không tách overview, module hoặc trang chi tiết. Quy tắc riêng này ưu tiên hơn hướng dẫn chung về tách diagram khi đông use case.
- Làm rõ phong cách theo ảnh người dùng: actor hai bên, cụm ellipse chính–phụ trong một khung dọc, nét mảnh/nền trắng; không dùng module box hay danh sách ellipse một cột. Ảnh chỉ là tham chiếu bố cục; ngữ nghĩa và quyền vẫn theo tài liệu nguồn.
- Hoàn tác bộ sơ đồ tám trang, builder và preview vừa tạo; khôi phục file editable từ bản sao lưu trước khi sửa. Không đổi requirement trong [BRD](BRD.md), [PRD](PRD.md) hay [Use Case Spec](report/03-software-requirements-specification.md).
- Validation: so sánh byte với bản sao lưu đạt; XML có đúng một page; `git diff --check` đạt. Không thay đổi nội dung hay hình học sơ đồ nên không cần render lại.

## 2026-10-29 — Hoàn tất merge Context diagram

- Hợp nhất [Context diagram](diagrams/11-optional/System-Context-Diagram.drawio) (khi merge vào cấu trúc diagrams mới, file chuyển từ `diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio` sang `diagrams/11-optional/`, nội dung giữ nguyên): giữ bốn trang và bố cục hiện có, cập nhật metadata nguồn theo [BRD](BRD.md), [PRD](PRD.md) và context model `diagrams/context-diagrams/context_diagram.json` (đã gỡ cùng folder cũ). Không đổi requirement hay workflow.
- Kiểm tra: builder `diagrams/context-diagrams/build_context_diagram.py` chạy thành công vào file tạm; validator báo 0 lỗi, 2 cảnh báo đường nối giao nhau (score 20); draw.io xuất PDF thành công. `tools/doclint.py` và self-test đạt; kiểm tra link local trong changelog đạt. Không thay layout thủ công bằng output của builder.

## [Unreleased]

### Added

- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx): viết lại bối cảnh dự án ở I 1 Overview (câu mở đầu) và I 2 Product Background theo yêu cầu của team: sản phẩm hướng tới sinh viên và người mới muốn viết bài báo khoa học nhưng chưa biết lộ trình, xuất phát từ kinh nghiệm dự án RBL cùng cô Hương (khó khăn lớn nhất ở nghiên cứu dữ liệu dạng bảng); mục đích là bộ khung các giai đoạn nghiên cứu rõ ràng, từng bước, thay vì tự động hoá nghiên cứu cho người đã giỏi; sau đó dẫn sang hệ thống hiện tại (5 stage). Bảng BP và phần còn lại của mục 2 giữ nguyên. Nội dung ở [S1](deliverables/supplements/S1-introduction.md), thay cho mục tương ứng của `report/00` chỉ trong docx; `report/` không đổi.
  - Validation: build lại, đoạn cũ không còn trong docx; TOC 515 mục ổn định; render 236 trang, kiểm tra trực quan trang 19.
- Lõi khoa học xuyên run (quyết định của owner D1..D6, 2026-10-29; điều kiện của D1 là cổng kiểm tra, không phải thời gian còn lại). Mục đích: hệ thống là một quy trình suy luận, test và bằng chứng kiểm được, và giá trị của nó đo được bằng độ tin trên mỗi phút chú ý của con người.
  - [glossary.md](glossary.md) 1.1: Quy tắc 6 (nghĩa đã giữ chỗ của severity, calibration, forecasting); evidence e-value và evidence rows thay "e-value"; §7a mới: claim ledger, promoted, claim status, `established`, `refuted`, test stringency, forecast, forecast score, replication run, planted-truth bench, hidden-error rate, attention budget; §11 thêm tên đã bỏ "e-value" đứng một mình và "e-value ledger".
  - [BRD.md](BRD.md): §1 giá trị đo được và đích sau MVP; BO-09 thêm planted-truth bench; BR-53 làm rõ record nào vào claim ledger; BR-105 (Must: chỉ nhân giữa nhóm hàng độc lập, record đầu tiên, α là setting); BR-106..BR-110 (Should: claim status, forecast, xác suất của model không quyết định, replication run, planted-truth bench và ablation); SM-19..SM-22; §7.1 phạm vi Should và Could; hai rủi ro mới.
  - [PRD.md](PRD.md): G-12; FR-209 viết lại; FR-272, FR-273 (Must, FE-09); FE-20 mới (Should) với FR-274..FR-287; danh sách Could sau MVP không có FR.
  - [architecture.md](architecture.md): S15; AI PI đọc claim ledger; runtime view 6.h (vòng suy luận, test, bằng chứng); ADR-09 dùng evidence e-value; ADR-19 (evidence e-value chỉ nhân giữa nhóm hàng độc lập); ADR-20 (claim status là mức claim ceiling xuyên run).
  - [traceability.md](traceability.md): Matrix A, B, D, E; số đếm 110 BR, 287 FR (256 Must, 25 Should, 6 Could); gap G8: FR-272..FR-287 và BR-105..BR-110 chưa có UC và TC.
  - [Report I](report/00-front-and-I-introduction.md): FE-20 trong bảng feature; §6.3 Future Work. [Report IV](report/04-software-design-document.md): ADR-09 viết lại, ADR-19, ADR-20. [Report III](report/03-software-requirements-specification.md) và [Report V](report/05-software-testing-documentation.md): FR-209, BR-53 và luồng lane E dùng evidence e-value và claim ledger; UC và TC cho FR mới chưa viết (G8).
  - Không đổi: MVP vẫn là FE-01..FE-15 và FE-17; diagram trong `diagrams/` không đổi. [Report7.docx](deliverables/FA26SE115_Report7.docx) chưa được cập nhật theo các thay đổi của `report/` trong đợt này.
  - Validation: `python -I tools/doclint.py` (0 lỗi); `git diff --check` sạch; số BR, FR và priority đếm lại bằng script từ BRD §8 và PRD §8 (cùng script cho lại 104 BR, 271 FR, 254 Must trên bản trước).

- Khôi phục 5 diagram editable đã bị xoá trong [commit 151edf99](https://github.com/openai-scientist/capstone-project-docs/commit/151edf99e173c75ffc9433ed2c938ff15bcd3504) vào `diagrams/11-optional/`: [Activity](diagrams/11-optional/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio), [Context](diagrams/11-optional/AI-Research-Experimentation-Platform-Context.drawio), [ERD](diagrams/11-optional/AI-Research-Experimentation-Platform-ERD.drawio), [Sequence](diagrams/11-optional/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio) và [Use Case](diagrams/11-optional/AI-Research-Experimentation-Platform-Use-Case.drawio). Nội dung nghiệp vụ, requirement và workflow không đổi; BRD, PRD và Use Case Spec không cần cập nhật.
  - Validation: `xmllint --noout` đạt trên cả 5 file; `git diff --check` và kiểm tra whitespace cho các file mới đạt.

- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx): lấp các mục chữ còn trống của Report III và IV; trong I–V chỉ còn ô diagram. Nội dung lấy từ code web app, backend và database script, viết ở [S3](deliverables/supplements/S3-requirements.md) và [S4](deliverables/supplements/S4-design.md); `report/` không đổi.
  - III: câu dẫn 2.2 và 3.; 3.1.2 Screen Descriptions; 3.1.3 Screen Authorization; 3.1.4 Non-Screen Functions; 3.1.5 Entity Descriptions; mô tả 63 chức năng ở 3.2–3.9; NFR chia theo thuộc tính ở 4.2.1–4.2.6.
  - IV 2.2.1–2.2.40: mô tả từng bảng sinh bằng [describe_tables.py](deliverables/database/describe_tables.py) từ [database script](deliverables/database/FA26SE115_database-script.sql).
  - Validation: placeholder giảm từ 249 xuống 136 (III 1 và IV 69 là ô diagram, VI 66); dòng leader chưa đặt chỉ là 6 dòng mở đầu supplement; TOC 515 mục ổn định; render 236 trang, kiểm tra trực quan trang 62 và 141.

- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx): mục I 3 Existing Systems dùng heading của leader thay cho KNIME/Orange của khung mẫu (3.1 Jupyter, 3.2 The AI Scientist, 3.3 AI co-scientist, 3.4 data-to-paper, 3.5 Kosmos, 3.6 Comparison and Research Gap); mỗi hệ thống nằm đúng heading, không còn placeholder ở Report I. `report/` không đổi.
  - Validation: build lại 360 heading; dòng leader chưa đặt chỉ còn 4 dòng mở đầu của supplement (như trước); TOC 515 mục ổn định; render 214 trang, kiểm tra trực quan trang 21.

- [Conceptual ERD](diagrams/03-conceptual-erd/Entity-Relationship-Diagram-Conceptual.drawio): 30 entity, 51 quan hệ, sinh bằng [build_erd.py](diagrams/03-conceptual-erd/build_erd.py) từ [database script](deliverables/database/FA26SE115_database-script.sql). Entity là bảng nghiệp vụ, đặt tên danh từ số ít PascalCase; bỏ 11 bảng kỹ thuật và các FK chỉ ghi người tạo/sửa/xác nhận. Bản số Crow's Foot suy từ FK (NOT NULL, FK là PK). [rule.md](diagrams/03-conceptual-erd/rule.md) cập nhật theo: nguồn entity, cách đặt tên, cách suy bản số, bố cục. Không đổi BRD/PRD/Use Case Spec vì không đổi requirement. Team chốt ERD theo database script; [review2-gaps.md](review2-gaps.md) ghi phần IV 2.1 cần leader cập nhật cho khớp.
  - Mọi entity cùng kích thước; đường nối do builder định tuyến trên lưới 20 px, không đường nào đi chung đoạn hoặc cắt qua entity.
  - Validation: builder kiểm tra bảng khớp layout và mọi quan hệ có động từ; draw.io CLI xuất PNG thành công; kiểm tra trực quan: không đường cắt qua entity, không nhãn chồng nhau.

### Changed

- [diagrams/03-conceptual-erd](diagrams/03-conceptual-erd/rule.md) (đổi tên từ `03-logical-erd`): team chốt vẽ ERD mức conceptual. Rule mới: entity chỉ ghi tên, quan hệ có tên và bản số Crow's Foot hai đầu, cho phép nhiều-nhiều trực tiếp, cấm thuộc tính/khoá/kiểu dữ liệu và entity kỹ thuật; ghi chú độ lệch với chữ "Logical ERD" của hướng dẫn Review 2. Cập nhật [README](diagrams/README.md) và [06-database](diagrams/06-database/rule.md).
- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx): bổ sung các mục Review 2 yêu cầu mà `report/` chưa có, nội dung lấy từ code `logos` và `ai-research-platform-fe` (ngày 2026-10-29), viết ở [deliverables/supplements/](deliverables/supplements/S4-design.md); `report/` không đổi.
  - II 6.2: repository, branch rules, Conventional Commits, CI của từng repo ([S2](deliverables/supplements/S2-project-management.md)); trả lời open item O-7.
  - IV 1.1: Technology Declaration (stack kèm version từ lock file, dịch vụ bên thứ ba với mục đích và dữ liệu gửi đi, AI tools) và Environments, Deployment and Rollback ([S4](deliverables/supplements/S4-design.md)).
  - IV 2.2: Database Script, kèm [database script](deliverables/database/FA26SE115_database-script.sql) sinh bằng cách chạy migration Alembic tới `20261022_0048` trên PostgreSQL 16 rồi `pg_dump --schema-only` (41 bảng, không dữ liệu).
  - V 4.2: thêm trường Execution (Automated/Manual theo level và method ở V 2.1) và Actual result cho 60 test case.
  - [review2-gaps.md](review2-gaps.md): các mục còn cần leader quyết định (workflow, state entity, ERD lệch script, staging, KNIME/Orange trong khung mẫu).
  - Validation: build lại theo khung 358 heading; 0 dòng nội dung leader bị sót; TOC 513 mục ổn định; field 514/514; render 214 trang và kiểm tra trực quan trang mới.
- [diagrams/](diagrams/README.md): dựng lại cấu trúc folder cho draw.io theo bộ diagram đã chốt (SEP490 template và hướng dẫn Review 2): `01-use-case` đến `10-activity` và `11-optional`, README có bảng folder, vị trí trong report, checklist tên file và quy tắc chung (file, frame UML, font, màu, export PNG). Mỗi folder có `rule.md` quy định ký hiệu, bố cục, điều cấm và checklist theo chuẩn: UML 2.5.1 (use case, class, sequence, state machine, activity, package, deployment), Crow's Foot (logical ERD, database), C4 (system overview, context), BPMN 2.0 (business process), mẫu SEP490 và hướng dẫn Review 2. Đã đối chiếu với nguồn online (OMG UML 2.5.1 và issue UMLR-670, Ambler *Elements of UML 2.0 Style*/agilemodeling.com, uml-diagrams.org, c4model.com, Camunda BPMN naming, draw.io crow's foot), sửa lại frame kind, hướng include/extend, quy ước tên (event thì quá khứ, guard không trùng, `name : Class`, reply chỉ khi cần, `[Container: tech]`, legend C4) và thêm mục Nguồn cho từng rule; 24 link nguồn đã kiểm tra trả về HTTP 200. Các folder diagram cũ (activity, context, erd, sequence, usecase) đã được dọn trước đó vì stale so với v3; link tới các file này trong các entry cũ đổi thành đường dẫn dạng text.
- [deliverables/FA26SE115_Report7.docx](deliverables/FA26SE115_Report7.docx) (bản track cho cả team; bản làm việc local vẫn ở `docs/1.2/report/`): dựng lại nội dung từ `report/00`–`06` nhưng **giữ nguyên khung Table of Contents của mẫu báo cáo đồ án** (358 heading cấp 1–4 cũ, đúng tên và thứ tự), cùng trang bìa và định dạng heading, bảng, bullet, ô ảnh, caption của bản docx cũ.
  - Nội dung leader được đặt vào heading cũ tương ứng theo một bảng ánh xạ, chữ giữ nguyên; heading con của markdown chuyển thành đoạn in đậm. Ví dụ: UC-01..41 vào III 2.2.2 Descriptions; FE-xx vào các nhóm III 3.2–3.9; Data Design vào IV 2. Database Design; Quality Scenarios, Risks and Technical Debt vào IV 1.1; các how-to Diátaxis vào nhóm User Manual tương ứng. Mục leader không có chỗ riêng trong khung cũ (Re-plan, Scope change log, Hand-off objects, Test risks, Users and Actors, các hệ thống AI Scientist/co-scientist/data-to-paper/Kosmos) được gộp vào heading gần nhất. Đã kiểm tra: 0 dòng nội dung leader bị bỏ sót (trừ các mục "Open items" nội bộ).
  - 259 heading của khung mẫu chưa có nội dung tương ứng trong `report/` (ví dụ KNIME, Orange, từng chức năng/sequence diagram cũ, Table Details từng bảng, Screens Flow) được giữ, kèm dòng `[CONTENT TO BE ADDED — …]`; 158 ô `[IMAGE TO BE ADDED — …]` cho hình theo khung cũ và hình của leader.
  - Caption hình và nội dung ô ảnh dùng tên diagram chuẩn BA/UML để người chuẩn bị biết cần vẽ gì: System Context Diagram, Use Case Diagram, Component, Deployment, Package Diagram, ERD, Screen Flow Diagram, `Class Diagram – <nhóm>`, `Sequence Diagram – <use case>`, `State Machine Diagram – <đối tượng>`, `Activity Diagram – <quy trình>`, `UI Screen – <chức năng>`. Chỉ đổi trong docx, `report/` giữ tên gốc.
  - Bộ sơ đồ đối chiếu [hướng dẫn Review 2](docs/example/SWP490_R2_Huong-dan-chuan-bi-Review-2_1.pdf) và report mẫu SEP490 (`docs/example/1_SEP490`, `docs/example/2_SEP490`). 14 ô ảnh đánh dấu "REQUIRED – Review 2": System Overview, Logical ERD, State machine cho Research Run, Hand-off Object, Project, Local Node, Dossier, Decision Item, và Activity diagram cho 5 luồng chính. 75 ô ảnh đánh dấu "REQUIRED – SEP490 template": Use Case, Screen Flow, Database Diagram (IV 2.2), Package, Class diagram theo feature, Sequence diagram. IV-2 đổi thành System Overview Diagram, IV-6 đổi thành Activity Diagram. Các ô State Diagram của khung mẫu mà nhóm không có thực thể có vòng đời thì ghi chú, không đặt ô ảnh.
  - TOC có link, gồm Heading 1–4 và caption hình (513 mục), số trang lấy từ bản render và đã ổn định; footer đổi sang "OpenAI-Scientist".
  - Không sửa file nào trong `report/`.
  - Validation: kiểm tra phủ nội dung 0 dòng thiếu; render bằng LibreOffice field TOC cân bằng (514 begin/514 end), kiểm tra trực quan trang TOC.

- Tên hệ thống: "AI Research Experimentation Platform" đổi thành **OpenAI-Scientist** (theo tên organization) trong `report/`, [glossary.md](glossary.md), [BRD.md](BRD.md), [PRD.md](PRD.md), [architecture.md](architecture.md), [README.md](README.md) và [traceability.md](traceability.md). Tên đề tài đã đăng ký giữ nguyên trên trang bìa. Các thuật ngữ thành phần Platform, engine và Local Node không đổi. Diagram chưa đổi tên (vẫn stale).
- `report/`: biên tập giọng văn để bỏ dấu hiệu văn bản máy viết, gồm đối lập giả, câu chốt, gạch ngang, chữ đậm trang trí và tự mô tả tài liệu. Nội dung, ID và bảng giữ nguyên.
- `report/`: biên tập lần hai về giọng văn, thuật ngữ, phạm vi và tính nhất quán theo một style sheet chung (tên vai trò, giá trị trong code span, "sign in", "dataset", không gạch ngang trong văn xuôi). ID và số dòng bảng giữ nguyên.
- FE-04 đổi tên thành "Research case and run management" trong [PRD.md](PRD.md), [traceability.md](traceability.md) và `report/`.
- Bench: khả năng của bench (seeded-flaw bench, red-team catalogue, đo precision của persona; FR-77, FR-135..FR-137) là Must. Chạy một đợt đánh giá đầy đủ là Should, chạy theo yêu cầu, không thuộc tiêu chí release MVP; SM-17 và SM-18 đo khi đợt đó chạy ([PRD.md](PRD.md) §11.2, [Report II](report/02-project-management-plan.md), [Report V](report/05-software-testing-documentation.md)).
- Ranh giới AutoML: BC-C20 và BC-R20 là chủ đề nghiên cứu của user dưới `method_comparison` (FE-19, Should). Non-goal chỉ loại việc đánh giá chính OpenAI-Scientist so với AutoML hoặc agent tổng quát ([BRD.md](BRD.md) §7.2, [PRD.md](PRD.md) §3 và §11.2.1, [Report I](report/00-front-and-I-introduction.md) EX-09).
- Huỷ run được từ mọi state trừ `ended` (BR-77, [architecture.md](architecture.md), [glossary.md](glossary.md)).
- BR-93, BR-96, BR-98 và các FR Must có hành vi `method_comparison` chỉ giữ phần MVP; phần `method_comparison` ghi "khi FE-19 có, sau MVP". FR-194 chuyển sang FE-19, Should.
- [Report II](report/02-project-management-plan.md): RACI theo R/A/C/I chuẩn; rủi ro 22 viết lại, bỏ tham chiếu ADR-16 và R-11 (không có trong Report IV).
- [Report I](report/00-front-and-I-introduction.md) §3: viết lại phần hệ thống hiện có. Giữ Jupyter làm mốc; bỏ KNIME và Orange; thêm The AI Scientist (Sakana AI), AI co-scientist (Google), data-to-paper (Technion) và Kosmos (Edison Scientific) theo trang và bài báo gốc của từng hệ thống; thêm bảng so sánh §3.6. Đánh lại số Table 2 đến Table 4. Review scope so với các hệ thống này: giữ nguyên MVP và claim type `causal`.
- Danh mục BC: ca FE-09 của đợt 1 (BC-C01, BC-C05; TC-62, TC-63) giữ Must; ca FE-09 từ đợt 2 trở đi và TC-65 đến TC-73 thành Should, chạy theo yêu cầu cùng đợt đánh giá bench ([PRD.md](PRD.md) §11.2.1, [Report V](report/05-software-testing-documentation.md)).
- Đóng câu hỏi mở bằng giá trị đề xuất: SM-02 (trung vị ≤ 15 question và ≤ 24 giờ bị chặn mỗi run, overturn rate ≤ 10% mỗi action type, tính trên run `milestones` trong tháng), SM-17 ≥ 90%, SM-18 = 100%, SR-06 mặc định 3 secondary, SR-08 mặc định 7 ngày và nhắc trước 24 giờ, SR-02 mặc định 1 GB mỗi file, NFR-06 đo trên cả tháng lịch ([BRD.md](BRD.md), [PRD.md](PRD.md), [architecture.md](architecture.md) QS-13/QS-14, `report/`).

### Removed

- Hai file tạm của draw.io trong `diagrams/context-diagrams/`; [.gitignore](.gitignore) bỏ qua mẫu `.$*.bkp` và `.$*.dtmp`.

### Added

- Hạn chờ của item pinned: BR-104, FR-263..FR-266, SR-08, MSG-59, MSG-60, TC-99, TC-100, QS-15. Hạn chờ là setting của project. Trước hạn, hệ thống nhắc Researcher đã tạo run và Project Manager. Hết hạn, run kết thúc `ended(with_gaps)`; item đóng mà không có câu trả lời, không ai quyết thay user. `with_gaps` có ba nguyên nhân (FR-262, BR-14).
- FR-267..FR-269: phần `method_comparison` tách khỏi FR Must (Should, FE-19). FR-270, FR-271: luật của review loop, gồm finding chặn mới trên field không đổi chỉ hợp lệ khi bằng chứng là fact mới tính.
- MSG-61: vi phạm thứ tự pipeline. TC-101 (Must): kiểm tra khả năng của seeded-flaw bench trên tập case tối thiểu.
- [glossary.md](glossary.md): Pinned wait deadline, Web app, Holm correction, Gatekeeping, Implanted effect, Clean permutation check, Candidate cap per round, Probe budget, Known risk; AI PI là connector persona, đóng vai secondary actor.

### Fixed

- [Report V](report/05-software-testing-documentation.md): FR-135..FR-137 (Must) trước chỉ có TC-58 (Should); nay có TC-101. [traceability.md](traceability.md) cập nhật BR-40, BR-100 và số TC (101).
- [Report VI](report/06-release-package-and-user-guides.md): sửa tham chiếu MSG-51 và MSG-25.

Validation: `python -I tools/doclint.py` (13 file, 0 lỗi), `--self-test` đạt, `git diff --check` sạch; script kiểm tra: 271/271 FR có UC trong Report III và có TC trong Report V, mọi TC được dẫn đều tồn tại, mọi ID BR/UC/MSG/SR/CR/QS/ADR/NFR/FE/SM trong `report/` có trong nguồn.

## [2026-10-29] — Giai đoạn C: Report 7 bằng tiếng Anh và dọn dẹp tài liệu cũ

### Added

- `report/`: bản staging tiếng Anh của Report 7, một file cho mỗi mục La Mã, dẫn xuất từ BRD, PRD, architecture và glossary; không gắn với trạng thái triển khai, không chứa thông tin nội bộ, không có diagram.
  - [I. Project Introduction](report/00-front-and-I-introduction.md), kèm front matter.
  - [II. Project Management Plan](report/02-project-management-plan.md): baseline gốc, re-plan, scope change log.
  - [III. SRS](report/03-software-requirements-specification.md) theo ISO/IEC/IEEE 29148: UC-01..UC-41, SR-01..SR-07, CR-01..CR-06, MSG-01..MSG-55; phủ 145/145 FR.
  - [IV. SDD](report/04-software-design-document.md) theo các viewpoint của IEEE 1016; data model chỉ ở mức logic.
  - [V. Testing](report/05-software-testing-documentation.md) theo ISO/IEC/IEEE 29119-3 bản rút gọn: TC-01..TC-94; mọi FR, NFR và BC đều có test case; trạng thái "Not run".
  - [VI. Release Package & User Guides](report/06-release-package-and-user-guides.md) theo Diátaxis.
  - Mỗi mục có phần "Open items" ghi những gì nguồn chưa định nghĩa.
- [README.md](README.md): thêm ID `CR-`.

### Changed

- Đổi tên file `AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md` → [BRD.md](BRD.md) và `AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md` → [PRD.md](PRD.md), vì số phiên bản trong tên file sai với nội dung v3.0. Đã sửa link trong mọi tài liệu và trong source của context diagram.
- [tools/doclint.py](tools/doclint.py): danh sách mặc định gồm BRD.md, PRD.md và `report/*.md`.
- [changelog.md](changelog.md): chuẩn hoá theo Keep a Changelog; bỏ đường dẫn code, repo khác, commit và tên tài liệu nội bộ.

### Fixed

- Sửa sau review độc lập (27 finding: 3 High, 10 Medium, 14 Low; theo luật tài liệu đứng trước thắng):
  - Item pinned đang chờ giữ run ở `waiting(decision)`. Run chỉ `ended(with_gaps)` khi hết token budget hoặc khi item `spending` quá hạn (FR-262). State model có thêm lối ra từ `waiting` và lối huỷ từ mọi state.
  - Floor của `acceptance` là `auto`. Mức trần chi tiêu là giới hạn tiền, không phải floor (BR-61, FR-92). Bảng level theo preset thành FR-147..FR-150.
  - Decision inbox có tám loại item, thêm `spending`.
  - Cardinality: Run 1 – 0..N Lock và 1 – 0..N Dossier version.
  - Cột nguồn của NFR chỉ còn BO/BR/SM. NFR-03, NFR-06, NFR-15 viết lại cho kiểm được. FR-113 thành dạng tuỳ chọn. Cột BR của bảng FE tính lại.
  - Persona có ba loại (maker, guard, connector), mỗi tên có một dòng trong glossary. Bỏ "đóng run".
  - Report: bỏ dẫn mục của tài liệu nội bộ, tên vendor/framework và ghi chú biên tập; sửa tham chiếu Open item, MSG-31, MSG-44, TC-01, TC-57..61, TC-90.
  - doclint: chỉ miễn trừ đúng heading lịch sử; bỏ miễn trừ cho dòng có "→"; thêm self-test.
- Đăng nhập bằng tài khoản Google: thêm BR-103, FR-146, MSG-56..MSG-58, TC-95..TC-98.
- Tách FR gộp nhiều yêu cầu: 111 FR mới (FR-151..FR-261). Phần đầu giữ ID cũ. Tổng 262 FR: 249 Must, 7 Should, 6 Could.
- [traceability.md](traceability.md): điền cột UC và TC cho cả 103 BR. 262/262 FR có UC và TC. Đóng gap G6.

### Removed

- Ảnh sơ đồ end-to-end cũ ở repo root: mô tả luồng có Decision Gate của bản BRD/PRD trước, mâu thuẫn với v3.0.

Kiểm tra (sau vòng sửa): doclint trên 13 file mặc định cho 0 lỗi, 0 cảnh báo; `--self-test` đạt 15 case; quét từ khoá rò rỉ nội bộ trên `report/` không có kết quả; mọi ID mà Report dẫn tới đều có ở nguồn hoặc ở Report III; `git diff --check` sạch. Diagram vẫn stale.

## [2026-10-29] — Giai đoạn B: BRD, PRD, architecture v3.0, lớp kiểm soát dữ liệu bảng, tài liệu độc lập

### Added

- [traceability.md](traceability.md): ma trận BO → BR, BR → FE → FR, NFR → BO/BR/QS, ADR → BR/FR, FE/SM; bảng coverage và gap.
- [id-mapping.md](id-mapping.md): ánh xạ ID cũ → v3.0 cho BRD, PRD, architecture (chuyển từ Appendix A của từng tài liệu).
- [tools/doclint.py](tools/doclint.py): kiểm link, anchor, tên đã bỏ, dấu hiệu gắn với code và dẫn nguồn quyết định; có `--self-test`.
- [glossary.md](glossary.md): thuật ngữ dữ liệu bảng (task family, research pattern, prefilter, dataset shift, pipeline order, evidence family, method comparison, red-team catalogue, benchmark case).
- Benchmark case catalogue `BC-*` (60 case) ở PRD §11.2.1, gắn priority theo FE.
- Claim type method comparison (pattern G–J, FE-19, Should, sau MVP); upload nhận Parquet.

### Changed

- [BRD](BRD.md) v3.0: đánh số lại BP, BO, SM, BR (BR-01..BR-102, SM-01..SM-18); cột nguồn của BR chỉ còn BO.
- [PRD](PRD.md) v3.0: FE-01..FE-19 (FE-16 deprecated), FR-01..FR-145, NFR-01..NFR-31, journey J1–J7; cột nguồn của FR chỉ còn BR.
- [architecture.md](architecture.md) v3.0 theo arc42: logical data model, runtime view, ADR-01..ADR-18, quality scenario, risk.
- [README.md](README.md): nguyên tắc "tài liệu định nghĩa hệ thống"; thêm `BC` vào bảng ID; thêm id-mapping và traceability vào bộ tài liệu.
- Hành vi đích theo thiết kế đích mới: run state thêm `ended(cancelled)`; item `spending` hết hạn thì `with_gaps`; Admin chỉ thấy metadata; Dossier chỉ tạo khi PaperPack accepted và version mới cần duyệt lại; Project Manager có mọi quyền nghiên cứu của Researcher; Researcher trả lời release review; thông báo ngoài cho item pinned và `spending`; dataset stage được tìm dataset public; xác nhận cấu trúc dữ liệu là action pinned; thu hồi rule Local Node; duyệt ngưỡng NFR.
- MVP = FE-01..FE-15 + FE-17; UI sản phẩm chỉ tiếng Anh.
- Dữ liệu bảng: thêm lớp kiểm soát (task family, panel, dataset shift, pipeline order, leakage, prefilter, hypothesis testability, evidence family, red-team catalogue, scorecard SM-17/SM-18), dựa trên tài liệu tham khảo về dữ liệu bảng; claim type method comparison là thay đổi có chủ đích so với thiết kế đích.
- Tài liệu độc lập: bỏ dẫn nguồn quyết định; truy vết chỉ lên ID cha; ánh xạ ID cũ gom vào id-mapping.md; tài liệu nội bộ viết tiếng Việt, chỉ `report/` viết tiếng Anh.
- Bỏ Appendix B "thay đổi so với v2.2" của BRD và PRD; lịch sử nằm ở changelog.

### Removed

- `specs/` (gap analysis, SRS, SDD, design brief): bản nháp chưa từng commit, đã gộp vào BRD, PRD, architecture.

Kiểm tra: doclint 7 file mặc định 0 lỗi, 0 cảnh báo, `--self-test` đạt; 102 BR đều có trong Matrix B; 145 FR đều có trong traceability, không FR nào thiếu BR nguồn; tập ID trước và sau lượt làm độc lập giống nhau; `git diff --check` sạch. Diagram trong `diagrams/` chưa cập nhật (stale theo kế hoạch).

## [2026-10-29] — Giai đoạn A: glossary duy nhất và chuẩn tài liệu

### Added

- [glossary.md](glossary.md): nguồn thuật ngữ duy nhất, 10 nhóm (actor, project và dữ liệu, run, harness và kiểm soát, review độc lập, hand-off object, execution, paper, Local Node, quản trị kết quả) và bảng **tên đã bỏ** (mode light/auto, gate, send-back, Research Brief/Verify, HGAR, Writing AIF, pipeline `default`, runner + Docker).

### Changed

- [README.md](README.md): thay dòng tiêu đề bằng chuẩn tài liệu: bộ tài liệu và thứ tự dẫn xuất (glossary → BRD → PRD → architecture → Report); mức chi tiết độc lập với code; tách nội dung bền và hay đổi; quy ước ID vĩnh viễn và deprecated; chuẩn theo loại tài liệu; văn phong ASD-STE100; trạng thái stale của `diagrams/`.
- Hành vi đích: preset theo stage + presence thay mode; decision inbox có overturn; review loop bắt buộc; dataset không bắt buộc khi bắt đầu run; một run active mỗi project; Reviewer duyệt Dossier; Platform chỉ version/hash/duyệt Dossier; HGAR tan vào execution; JFE là Could.
- Tài liệu ở mức khái niệm, không route/HTTP/kiểu cột. Paper stage theo thiết kế đích, chờ tài liệu writing.
- Diagram đánh dấu stale, cập nhật ở đợt riêng. BRD, PRD, architecture chưa sửa (giai đoạn B).

Kiểm tra: đối chiếu glossary với thiết kế đích và actor với BRD §6; kiểm stale của diagram; kiểm link nội bộ và `git diff --check`. Chuẩn tham chiếu: [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html), [IEEE 1016-2009](https://standards.ieee.org/ieee/1016/4502/), [ISO/IEC/IEEE 29119-3](https://www.iso.org/standard/79429.html), [arc42](https://arc42.org/), [ADR](https://adr.github.io/), [Diátaxis](https://diataxis.fr/), [ASD-STE100](https://www.asd-ste100.org/).

## [2026-10-28] — Chuẩn hoá tên entity và quy ước Crow's Foot của ERD

### Changed

- ERD editable (`diagrams/erd/AI-Research-Experimentation-Platform-ERD.drawio`) và model (`diagrams/erd/platform_erd.json`): dùng 40 danh từ số ít PascalCase làm tên hiển thị (`User`, `Project`, `DatasetVersion`, `PlatformAdminGrant`, `TokenUsageEntry`...); bảng mapping trong README (`diagrams/erd/README.md`) giữ liên kết 1:1 về 40 bảng gốc.
- Nhãn quan hệ là cụm động từ đọc từ parent sang child, là association dữ liệu chứ không phải flow. `ProjectMembership` là associative entity, không thêm đường N:M trùng giữa User và Project.
- Builder/validator (`diagrams/erd/build_platform_erd.py`): nét liền cho 3 quan hệ identifying, nét đứt cho 67 quan hệ non-identifying (biến thể IE ghi trong legend). Optionality/cardinality ở hai đầu nối, dựa trên constraint của schema.
- Mức chi tiết là entity-relationship overview, ẩn attributes theo mẫu report; không gọi là logical/physical model đầy đủ. Giữ 40 entity, 70 FK (54 hiển thị mặc định, 16 provenance trong layer bật được).
- Không đổi requirement, actor, scope, workflow hay schema; BRD/PRD không cần cập nhật.

Kiểm tra: regenerate và `--check` đạt (40 tên duy nhất, 70 FK, cardinality, identifying stroke, routing, rebuild khớp byte); export bằng draw.io và xem hình render; kiểm tra link và `git diff --check`. Nguồn quy tắc đặt tên: [ER/Studio](https://docwiki.embarcadero.com/ERStudioDA/193/en/Object_Name_Rules), [Microsoft Crow's Foot](https://support.microsoft.com/en-gb/visio/create-a-diagram-with-crow-s-foot-database-notation), [draw.io Crow's Foot](https://www.drawio.com/docs/tutorials/crows-foot-notation/); chi tiết ở ERD README (`diagrams/erd/README.md`).

## [2026-10-28] — ERD editable cho Report 7 mục III 3.1.5

### Added

- Report 7 ERD (`diagrams/erd/AI-Research-Experimentation-Platform-ERD.drawio`): 40 entity, 70 quan hệ FK theo schema Platform; ô chỉ ghi tên entity, đường nối có tên quan hệ và Crow's Foot; không liệt kê cột/PK/FK ở mức conceptual.
- ERD model (`diagrams/erd/platform_erd.json`), builder/validator (`diagrams/erd/build_platform_erd.py`), hướng dẫn (`diagrams/erd/README.md`): sinh từ metadata của schema, xác minh nullable/unique/PK/CHECK; 54 quan hệ chính hiển thị mặc định, 16 quan hệ provenance trong layer ẩn.
- Cardinality xét cả constraint kết hợp (OTP một purpose cùng unique theo user và purpose; settings là singleton). Không suy diễn FK từ JSON, tham chiếu đa hình hoặc context ID của monitoring/audit.

### Changed

- Ba ERD cũ đã xoá khỏi working tree trước task được giữ nguyên; link lịch sử tới chúng đổi thành tên file ghi rõ đã xoá, kèm link tới bộ ERD hiện tại.
- Không đổi requirement, scope, actor hay workflow; BRD/PRD không cần sửa.

Kiểm tra: build và `--check` đạt (40 entity, 70 FK, cardinality khớp, không chồng entity/nhãn, không đường xuyên entity, rebuild khớp byte); export draw.io và xem hình render; `git diff --check` sạch.

## [2026-10-28] — Bổ sung phạm vi JFE và Writing AIF vào BRD/PRD

### Changed

- [BRD v2.2 Draft](BRD.md): bổ sung business problems/objectives/metrics, stakeholder, scope JFE/Writing, BR-47–BR-61, business rules, phụ thuộc và rủi ro về corpus rights/claim fidelity.
- [PRD v2.2 Draft](PRD.md): bổ sung JFE/Writing vào bảng users/permissions, flow dạng bước, PR-38–PR-52, bảng data/artifact và non-functional requirements.
- JFE/Writing viết dưới dạng yêu cầu nghiệp vụ/sản phẩm và tiêu chí nghiệm thu, không ghi trạng thái triển khai. Giữ khung và số thứ tự có sẵn; giữ phạm vi tabular/FE-16.

Kiểm tra: 61 BR / 52 PR có ID duy nhất, liên tục; đủ flow journal → corpus → phân tích → profile, và evidence → lập luận → drafting → review/export; link, anchor, code fence và `git diff --check` đạt. Không chạy test hay generator vì chỉ đổi Markdown.

## [2026-10-28] — Đồng bộ BRD/PRD/architecture với contract hiện hành và hướng tabular

### Changed

- [BRD](BRD.md): bổ sung scope tabular, data-card boundary, năm loại cấu trúc dữ liệu, split-policy roadmap FE-16 và business requirements cho protocol freeze/execution/evidence.
- [PRD](PRD.md): đồng bộ research case, case amendment/charter, dataset format/limit, split hiện tại, validator của analysis plan và release status.
- [architecture](architecture.md): đồng bộ package ownership, pipeline, engine contract, hành vi dataset/hypothesis/experiment-design, PI authority, ranh giới frontend/platform và deployment settings.
- Ba tài liệu ghi rõ năng lực hiện tại dừng ở reviewed/locked plan; structure-aware split, sandbox execution, statistical result/verdict/dossier là increment kế tiếp (FE-16).
- Không sửa code, frontend hay diagram. Một số diagram lịch sử vẫn mô tả execution/Popper target; không dùng làm nguồn, cần migration riêng.

Kiểm tra: đối chiếu source và tài liệu tham khảo về dữ liệu bảng; kiểm link/cross-reference (link active trỏ tới file hiện hữu); `git diff --check` đạt. Không chạy test hay render diagram.

## [2026-10-27] — Định hướng lại phiếu đăng ký và report sang dữ liệu dạng bảng

### Changed

- Phiếu đăng ký (file local, không track): giữ định dạng, thông tin chung và tên đề tài; viết lại mục 3 và 4 theo hướng AI Scientist trên dữ liệu bảng do người dùng cung cấp. Bỏ hướng CRISP-DM và phạm vi ML/SE cũ.
- Liệt kê 5 kiểu cấu trúc dữ liệu kèm split policy: quan sát độc lập, có cấu trúc nhóm, theo thời gian, panel/longitudinal, cấu trúc đặc biệt cần adapter hoặc split policy riêng.
- Cập nhật functional/non-functional requirements, deliverables, task packages, research problems/questions/methodology theo hướng HGAR (protocol freeze, human gates, scientific reviewer).
- Report 7 (file local, không track): định vị lại theo dữ liệu bảng, giữ tên đề tài và phần mô tả hệ thống đã code. Viết lại Overview, Product Background, Existing Systems (thêm hàng Data structure, Leakage control), Business Opportunity, Vision, Scope; thêm FE-16 (increment kế tiếp), sửa LI-01, thêm EX-11, EX-12; thêm đoạn mở đầu cho 3.4 Data Management và NFR 4.2.6 Scientific Validity; dựng lại TOC (159 trang).
- BRD/PRD/architecture chưa sửa; cần đồng bộ hướng tabular và FE-16 ở đợt sau.

Kiểm tra: render phiếu (6 trang) và kiểm tra trực quan; `git diff --check` sạch.

## [2026-10-23] — Xoá các tài liệu handoff đã cũ

### Removed

- Ba handoff tạm (topic → hypothesis cho BE, cho engine, và event stream): hệ thống đã code xong. Contract hiện hành nằm trong [PRD](PRD.md) và [architecture](architecture.md).

### Fixed

- Link tới ba file đã xoá ở entry cũ đổi thành tên file kèm ghi chú "đã xoá". BRD/PRD không cần sửa vì không còn tham chiếu.

Kiểm tra: không còn link tới file đã xoá; `git diff --check` sạch.

## [2026-10-23] — Dựng lại Report 7 theo report mẫu và hệ thống đã code

### Changed

- Report 7 (file local, không track): dựng lại theo cấu trúc report mẫu gồm II. Project Management Plan, III. SRS, IV. SDD, V. Testing, VI. Release Package & User Guides, lấy nội dung từ [BRD](BRD.md), [PRD](PRD.md), [architecture](architecture.md) và hệ thống đã code.
- Phần đầu (bìa, Acknowledgement, Definition and Acronyms, I. Project Introduction) giữ chữ, chỉ trình bày lại theo report mẫu.
- Mục III có 62 đặc tả chức năng (33 mục viết mới từ các API của Platform, gồm quyền, business rule, mã lỗi); thêm use case Transfer Ownership, Delete Project, Configure Project Settings; Application Messages List có 135 mã lỗi.
- Mục IV: bảng PK/FK và bảng cột cho 40 bảng (421 cột); mỗi sequence diagram ghi API gọi và luồng chính. Mục V: số test case theo khu vực và kết quả chạy 2026-10-23 (4.063 passed, 9 failed, 53 skipped), Defect Report liệt kê 9 test fail. Mục VI: User Manual theo từng chức năng.
- Gộp Table of Figures vào một Table of Contents có hyperlink; ô ảnh và số liệu còn thiếu đánh dấu highlight vàng.

### Fixed

- Thời hạn lời mời theo cấu hình (mặc định 7 ngày, trần 720 giờ) thay vì 24 giờ; owner có thể xoá hẳn project. Hai điểm này cần đối chiếu lại trong BRD/PRD ở đợt sau.

Kiểm tra: render 159 trang; 632 mục TOC/hình đều có số trang ổn định qua hai lần render; `git diff --check` sạch.

## [2026-10-23] — Viết lại BRD, PRD, architecture theo hệ thống đã code (v2.0 DRAFT)

### Changed

- [BRD](BRD.md), [PRD](PRD.md), [architecture](architecture.md): viết lại thành v2.0. Bản cũ mô tả một "Popper target architecture" chưa từng được hiện thực (Understand ⇄ Ground ⇄ Discover ⇄ Verify ⇄ Communicate, Analysis Ledger, manuscript); bản mới bám hệ thống đang chạy.
- Phạm vi mới: Platform (auth không mật khẩu, project và 3 project role, dataset, data connection, run, stage, gate, accept/send-back, self-healing, token budget, BYOK, admin, webhook, audit); engine dataset, hypothesis, experiment_design; AI PI (charter, stage outcome, failure, close; Critic tắt mặc định; obligation); frontend (route, workspace, Run studio).
- Giữ tên file để không làm hỏng liên kết; version ghi trong header.

Kiểm tra: đối chiếu với README, contract, router, setting và route frontend của hệ thống; `git diff --check` sạch; liên kết giữa các tài liệu trỏ tới file có thật; không có diagram phải regenerate.

## [2026-10-06] — Event stream của research run và handoff topic → hypothesis (DRAFT)

Các tài liệu handoff dưới đây đã bị xoá ở entry 2026-10-23.

### Added

- Contract event stream cho research run (BE ↔ FE): endpoint SSE (resume bằng `Last-Event-ID`), lệnh trả lời gate, pause/resume, envelope event, danh mục event theo 7 stage, điểm dừng theo 4 review mode, ánh xạ với run/review/artifact hiện có. Lý do: FE đã dựng workspace từ event (dùng mock) nên BE và engine cần spec chung.
- Handoff cho team engine: ranh giới trách nhiệm với Platform BE; API engine cung cấp (tạo run idempotent, đọc trạng thái và event, trả lời gate, pause, resume, cancel); đẩy event về BE với số thứ tự và chính sách retry; danh mục event theo stage; gate; quy tắc chia nhỏ event; 10 tình huống lỗi; cách test.
- Handoff cho Platform BE: tạo run bằng `topic`, `domains`; đọc lại event; SSE; trả lời gate; pause, resume; endpoint nhận event từ engine; happy case, 15 unhappy case, migration, checklist.

### Changed

- Stage 1–8 thay cho Understand và Hypothesize: 5 stage `scope`, `search`, `screen`, `read`, `synthesize`; `hypothesize` sinh hypothesis qua tranh luận 3 góc nhìn, mỗi hypothesis có tiêu chí bác bỏ, kèm kiểm tra tính mới và khả thi. Khoá test plan chuyển sang step đầu của `experiment`. Gate `framing` đổi thành `scope`; thêm gate `screen` cho Copilot và Full.
- Run bắt đầu từ topic và domains do người dùng nhập, không còn dùng Research context; sub-question do hệ thống sinh ở stage 2. Tạm thời run chỉ đi từ topic tới hypothesis: ẩn chọn dataset, Check the data và review mode (mặc định Copilot); phần Experiment, Report, Paper vẫn giữ trong contract, bật lại bằng cờ.
- Tên artifact trong stage plan là tên cho người dùng đọc thay vì đường dẫn file; thêm trường `reads` tuỳ chọn. Màn hình run không còn lộ tên file hay tên cột dữ liệu; bỏ hiển thị skill trên UI.
- Bổ sung stage 1 (duyệt goal), stage 4 (bản ghi literature kèm nguồn, trích dẫn, DOI; thời điểm thu thập), stage 7 (overview và cơ hội nghiên cứu xếp ưu tiên).
- SSE tách khỏi endpoint đọc event JSON phân trang; dataset của `run.started` thành tuỳ chọn vì run từ topic không có dataset.
- FE nối sẵn API cho luồng này: chọn nguồn run bằng biến cấu hình (`mock` mặc định hoặc `api`), mở lại run sau reload, Experiment/Interpret/Report/Write hiện ở dạng khoá. Mock giữ lại cho tới khi BE qua checklist.
- BRD/PRD/ERD không sửa: contract nháp chưa đổi requirement.

Kiểm tra: typecheck, lint và test của frontend đạt (184 test pass, gồm test SSE mới); chạy trọn luồng bằng Playwright ở chế độ mock và api (happy case, pause/resume, reload giữa chừng, gate sau reload, run fail, mở lại run đã xong), desktop và điện thoại, không lỗi console.

## [2026-10-02] — Conceptual ERD chỉ vẽ cho Platform BE; bỏ Organization

### Changed

- Thay Conceptual ERD chung bằng ERD riêng cho Platform BE (13 entity, 19 relationship; các file lịch sử đã xoá, xem ERD hiện tại (`diagrams/erd/AI-Research-Experimentation-Platform-ERD.drawio`)). Lý do: Popper v2 thay kiến trúc cũ nên entity core của Popper v1 không còn khớp; sơ đồ chỉ gồm những gì Platform BE quản lý.
- Entity: `User`, `Role`, `Project`, `ProjectMember`, `Dataset`, `DatasetVersion`, `ResearchContext`, `Run`, `FrameReview`, `RunArtifact`, `Comment`, `Notification`, `AuditLog`. Mỗi khái niệm xuất hiện một lần, mọi relationship có tên và cardinality crow's-foot, không có thuộc tính hay khoá. `DatasetSnapshot` đổi tên thành `DatasetVersion` theo PRD.
- Bỏ `BillingAccount`, `PublicationRelease`, `PolicyVersion`, `DecisionRequest`, `EvaluationDecision`, `DatasetAssessment`, `UsageRecord` và entity core của Popper v1.
- Trước đó cùng ngày: bỏ `Organization` (42 entity, 69 relationship) vì BRD/PRD không định nghĩa organization hay workspace; project là ranh giới cách ly dữ liệu. Thêm `User owns Project` và `Project billed through BillingAccount`.
- Quyết định nghiệp vụ đi kèm: Reviewer chỉ đọc và bình luận, không có bước ký duyệt; dataset đợt này chỉ nhận CSV.
- BRD/PRD chưa sửa: vẫn tham chiếu kiến trúc Popper cũ, cần đồng bộ riêng.

Kiểm tra: builder báo 13 entity, 19 relationship, 0 crossing; export PNG bằng draw.io và kiểm tra bằng mắt, không có đường đè entity, marker chồng hay nhãn che nhau.

## [2026-10-01] — Điều chỉnh BRD/PRD theo kiến trúc Popper cập nhật

### Changed

- [BRD v1.10](BRD.md) và [PRD v1.9](PRD.md): giữ tên file, cấu trúc module, thứ tự và mọi mã requirement; không thêm module/BR/FR.
- Theo kiến trúc: problem-first brief, Understand ⇄ Ground ⇄ Discover ⇄ Verify ⇄ Communicate, coordinator với bounded playbook; worker/decision layer là tùy chọn.
- Sửa câu mâu thuẫn: agent được viết/chạy/debug code trong sandbox; Verify tùy chọn; reserve unread units không cần approval, pin/freeze cần recorded approval; primary look đã bắt đầu không được rerun để thay outcome.
- BR-79 / Module AI: passive durable exposure/recording, round-scoped contract, Lineage/Program Error Plan kế thừa qua run, không cấp α mới cho mỗi batch/run. BR-60/80/81/87 và Module AF/AJ: tiếp tục nghiên cứu trên non-reserved data sau Verify, giữ origin/history, feedback/steering, recovery.
- Đồng bộ summary, rules, acceptance criteria, provenance, risk, demo; run không Verify vẫn có exploratory figures, interpretation, code, sources, history.
- [architecture.md](architecture.md) giữ như bản tham chiếu cũ. Diagram cần đồng bộ ở đợt riêng trước commit/PR theo [AGENTS.md](AGENTS.md).

Kiểm tra: 150 mã requirement trong BRD và 197 trong PRD giữ nguyên danh sách và thứ tự; link, code fence, cross-reference ID đạt; `git diff HEAD --check` đạt. Không chạy generator vì không sửa diagram.

## [2026-09-30] — Thêm Conceptual ERD

### Added

- Conceptual ERD dạng `.drawio` editable (đã xoá): 43 entity, 70 relationship, crow's foot, connector vuông góc; hai khung Platform và Popper (nét đứt), đường cắt qua ranh giới là interface Platform ↔ Popper; record của Popper mà Platform dùng được tô riêng.
- Model JSON và builder (đã xoá); model ghi reference nguồn cho từng entity; builder có `--check` cho geometry connector và hỗ trợ khung nhóm.
- `.gitignore`: bỏ qua output build, file tạm Office, `.DS_Store`, `__pycache__/`; thêm cấu hình Live Server cho editor.
- Mức conceptual bỏ artifact envelope, events, traces và entity phụ (Construct, DataLead, Critique, Theory, Campaign, MethodLesson, Statement); các phần này thuộc logical ERD.
- File `.drawio` đã chỉnh tay sau khi build nên chạy lại builder sẽ ghi đè chỉnh sửa.
- BRD/PRD/Use Case Spec không cần sửa: ERD chỉ mô hình hoá dữ liệu đã có.

Kiểm tra: `--check` đạt, 0 lỗi, 24 điểm cắt đều có jump arc; render bằng draw.io viewer trên Chrome headless đạt; `git diff --check` đạt. Xem [architecture.md](architecture.md).

## [2026-09-28] — Đồng bộ BRD v1.9 / PRD v1.8 với kiến trúc đích Popper

### Added

- BRD: BR-82 Research Knowledge Layer, BR-83 Research Artifacts & Visibility (Must), BR-84 Publication Views & Integrity Audit (Must), BR-85 Simulation Lab, BR-86 Theory & Observable Implications, BR-87 Research Campaign; BRule-39 (policy settings có version, không được làm yếu bảo đảm), GA-17/18, R-33→36, acceptance criteria 59–63; BR-81 Research Program branches (Should).
- PRD: Module AK (Artifacts & Publication Views), AL (Knowledge Layer), AM (Simulation Lab); FR-STATE-06, FR-REFLOOP-06, FR-LOOP-09, FR-VALID-05/06, FR-PROV-04, FR-REPRO-04/05, FR-EVAL-06, FR-RQ-04; mở rộng NFR-02/03, acceptance criteria 61–66, entities, release plan, traceability.
- [PRD §53.1 Proposed Defaults](PRD.md): giá trị đề xuất cho open decision 5–7 và 14–24 (α = 0.05; deciding interval Bonferroni 1 − α/L, Holm chỉ để báo cáo, FDR chỉ cho exploration; margin theo summary measure; bảng cỡ mẫu; δ_F/δ_N cho pack `general` và software engineering; split 50/50; look budget 5; mode và threshold của decision point ở A1; margin evaluation; capability MVP). BRD KPI-28 trỏ tới α đề xuất. Đang chờ nhóm và supervisor duyệt.

### Changed

- [BRD v1.9](BRD.md) và [PRD v1.8](PRD.md) theo bảng mapping §7.10 của [architecture.md](architecture.md); giữ tên file.
- Research loop: agent loop trong giới hạn budget và invariant, giữ state machine cũ làm workflow floor (BR-80, Module AJ). Thêm exploration/confirmation split, Analysis Ledger, look budget, Research Protocol, confirmation batch (BR-79, Module AI).
- Evidence Sufficiency Gate deterministic: Finding / Negative Result / Inconclusive tính trên adjusted interval so với δ_F / δ_N (BR-59, Module AE). `NEED_MORE_EVIDENCE`, `TRY_ALTERNATIVE_METHOD`, `REPLICATE` thành next move (BR-60, Module AF); `NEED_HUMAN_REVIEW` thành escalation. Deterministic trigger là mức sàn; confidence của decision layer chỉ được thêm escalation (BR-61, BRule-28).
- BR-78: candidate ngang điểm vào cùng một confirmation batch trong look budget, không mở nhánh song song; bỏ `co_selected_with` và cap nhánh song song, thêm quan hệ `registered_in`; chuyển từ section 11 về section 10 (lỗi đặt sai có từ v1.7).
- Experiment chỉ chạy qua registered capabilities, bỏ `run_python`/`run_sql` (BR-22/23, Module L). BR-21 thành triangulation / bounded robustness. BR-65 thành Prior-Work Assessment giới hạn theo coverage, không có nhãn `novel`. BR-48 dùng origin do hệ thống gán.
- Mở rộng BR-27 (claim type / evidential status), BR-34 (reverse provenance), BR-40 (limitation theo validity type), BR-49 (dataset-scope looks), BR-55 (replay vs re-derivation, tombstone), BR-56 (các loại state), BR-58 (screens, admission gate, circuit breaker), BR-63 (champion/challenger), BR-80 (role profiles, context), BRule-07 (causal endorsement), NFR-02/07.
- Sửa mâu thuẫn còn lại: BR-07 / FR-PROFILE-04 (quan hệ hai biến chỉ trên exploration partition); BR-12 / FR-CLEAN-04 (cleaning sau split là protocol deviation); BR-41 / Module W (Negative Result và Inconclusive hiển thị ngang Finding); BR-42 (thêm confirmation batch, severity checks, claim level); BR-59 / Module AE (two-sided và directional); BRule-27 / PP-11 (bỏ "re-plan" khỏi technical retry); FR-EVAL-04 khớp BR-46; FR-VIZ-02 (chỉ registered chart capability); BR-25 (tách stability check khỏi replication); BR-16 / FR-RQ-01/02 (trường Research Brief, gap, intake trước khi đọc dữ liệu); BR-44/45 / FR-EVAL-02 (null / planted-signal ground truth, false-finding rate, power); FR-ADMIN-04 (settings có policy version).
- Tính lại phần định lượng §53.1: Holm thành simultaneous interval Bonferroni cho quyết định sufficiency (BR-49, FR-MTEST-02 làm rõ theo); số run evaluation từ 200 thành khoảng 655 mỗi arm cho margin 0.03 (khoảng 1.470 cho margin 0.02); thêm margin theo từng measure (d, r, β, OR, Cramér's V, η²) và bảng cỡ mẫu.
- [architecture.md](architecture.md): sửa link BRD/PRD hỏng thành link tới file DRAFT; phần "Proposed BRD/PRD changes" thành đã áp dụng, chờ supervisor sign-off.
- Diagram chưa đồng bộ: Activity/Sequence/Use Case/Context còn mô tả outcome cũ và luồng tuyến tính; cần cập nhật và regenerate ở đợt riêng theo [AGENTS.md](AGENTS.md).

Kiểm tra: kiểm tự động đạt (BR/BRule đúng thứ tự và section, MoSCoW và traceability đầy đủ, không tham chiếu ID không tồn tại, không FR trùng, acceptance criteria PRD liên tục 1–66, code fence cân bằng); `git diff --check` sạch. Còn tồn đọng có sẵn từ trước: architecture.md tham chiếu hai file chưa có trong repository. Chưa chạy diagram generator.

## [2026-09-24] — Chuẩn hóa tài liệu REQ-TOOL và cập nhật package diagram

### Added

- Bản chuẩn hóa [BRD](BRD.md) v1.8 và [PRD](PRD.md) v1.7 theo định dạng REQ-TOOL (đã xoá); giữ hai file DRAFT nguồn.

### Changed

- Cập nhật Use Case diagram, Activity và Sequence artifacts/builders theo các entry đồng bộ BRD/PRD.
- Backup Context draw.io là artifact kỹ thuật, không phải nguồn nội dung; Context model và builder là nguồn cho Context DFD Level 0.

Kiểm tra: `git diff --check` đạt; kết quả validation diagram nằm ở entry tương ứng. Diagram: Context (`diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio`), Activity (`diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio`), Sequence (`diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio`), Use Case (`diagrams/usecase-diagrams/AI-Research-Experimentation-Platform-Use-Case.drawio`).

## [2026-09-23] — System Context theo DFD Level 0

### Added

- Context — DFD Level 0 (`diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio`) dạng `.drawio` editable, kèm context model (`diagrams/context-diagrams/context_diagram.json`) và context builder (`diagrams/context-diagrams/build_context_diagram.py`): sáu external entity, một process trung tâm, 25 labeled data flow cấp cao theo BRD/PRD.
- Layout theo reference: Researcher ở trên, Project Manager/System Administrator bên trái, provider bên phải, Reviewer bên dưới; nới corridor để connector không chồng; nhãn flow sát làn mũi tên, rút gọn nhãn dài, tăng cỡ chữ.
- Loại module nội bộ và Secure Sandbox khỏi external boundary; AI/LLM Provider và Structured Decision Provider ở mức abstraction, không khóa vào vendor.

Kiểm tra: builder đạt (layout DFD Level 0 deterministic, không cần Graphviz); validator `--strict --score` 0 error, 0 warning, score 0; render draw.io 31.4.5 và kiểm tra trực quan; `git diff --check` đạt. Use Case, Activity, Sequence không đổi.

## [2026-09-22] — 30 Sequence UC, Activity theo BRD v1.8 / PRD v1.7

### Changed

- Activity — Main Flows (`diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio`) và builder (`diagrams/activity-diagrams/update_activity_diagram.py`): đồng bộ với BR-64/65/73-75/78 (Structured Idea Record/Reflection, optional novelty assessment, bounded tied candidates, immutable branch snapshots, sibling join, shared testing family, provenance/evaluation metadata, trang Final Outputs & Manuscript). Sửa thứ tự Hypothesis Selection Gate, đưa novelty về đúng lane, chuyển method-cap sang Experiment Planner / AI Agent, giới hạn reviewer override ở Researcher, cập nhật ownership của Evaluation, thêm nhánh Approved / Rejected–Revise–Automated Review cho Final Outputs.
- Sequence — Main Flows (`diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio`) và builder (`diagrams/sequence-diagrams/build_sequence_diagrams.py`): từ 24 lên 30 trang UC (UC-25–UC-30: Research Definition, Hypotheses, Experiments, Research Findings, Research Outputs, System Administration); đồng bộ UC-10–UC-16, UC-18–UC-24. UC-10: novelty có `opt [Novelty feature enabled]` và nhánh `SOURCE / NOT ASSESSED`; UC-11: human review optional, cho phép high-confidence auto-continue.
- Use Case diagram giữ nguyên; BRD/PRD không sửa vì là source input.

Kiểm tra: biên dịch hai builder đạt; Sequence sinh đúng 30 trang UC-01..UC-30; activitylint `--strict` và validator `--strict --score` của Activity, Sequence đạt (0 error, 0 warning, score 0); semantic QA đạt (0 lỗi message actor, return source, fragment parent); render draw.io 31.4.5 đạt trên các trang đã chọn; `git diff --check` đạt.

## [2026-09-22] — Refresh editable diagram package

### Added

- Backup kỹ thuật của diagram nằm trong phạm vi staged.

### Changed

- Cập nhật diagram editable Activity, Sequence, Use Case cùng builder source-backed tương ứng. BRD, PRD, Use Case Spec không đổi vì không đổi requirement.

### Removed

- Hai sequence artifact đã superseded.

Kiểm tra: activitylint `--strict` đạt; Activity validator 0 error, 1 cảnh báo crossing, score 10; Main Sequence đạt, score 0; Use Case 0 error, 56 cảnh báo geometry của system boundary/nested layout, score 355, giữ nguyên theo phạm vi yêu cầu; `git diff --cached --check` đạt.

## [2026-09-22] — Local tooling cleanup

### Removed

- Metadata và worktree local của các công cụ agent không còn dùng; rule/reference tương ứng trong [AGENTS.md](AGENTS.md) và registry này.

Kiểm tra: không có tài liệu canonical hay diagram editable nào bị xoá; local link và cross-reference kiểm tra lại.

## [2026-09-22] — Documentation governance

### Added

- [AGENTS.md](AGENTS.md) với documentation-first gate: cập nhật tài liệu và changelog trước khi commit hoặc PR.
- Registry tập trung liên kết toàn bộ tài liệu, flow reference, diagram editable và source builder. Task này không regenerate hay sửa nội dung diagram.

Kiểm tra: local link trong changelog và AGENTS.md đạt; `git diff --check` sạch.

### Gói tài liệu ban đầu

- Tài liệu nguồn: [BRD v1.8 Draft](BRD.md), [PRD v1.7 Draft](PRD.md). Use Case Specification không có file canonical; Use Case diagram giữ nguyên theo scope.
- Diagram: Context (`diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio`), Activity (`diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio`), Use Case (`diagrams/usecase-diagrams/AI-Research-Experimentation-Platform-Use-Case.drawio`), Sequence (`diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio`).
- Builder: Context model (`diagrams/context-diagrams/context_diagram.json`), Context builder (`diagrams/context-diagrams/build_context_diagram.py`), Use Case builder (`diagrams/usecase-diagrams/build_usecase_diagram.py`), Sequence builder (`diagrams/sequence-diagrams/build_sequence_diagrams.py`), [README](README.md), [AGENTS.md](AGENTS.md).
- Backup kỹ thuật của Use Case diagram (đã xoá) không phải source of truth.

### Quy ước registry

- BRD, PRD và Use Case Spec là nguồn nội dung nghiệp vụ/chức năng.
- File `.drawio`/`.xml` là artifact editable, giữ nguyên khả năng chỉnh sửa; PNG là flow reference trực quan.
- Builder là source-backed generator: khi flow hoặc quan hệ thay đổi, cập nhật builder và regenerate artifact.
- Metadata nội bộ của Git và file tạm của môi trường không thuộc documentation package canonical.

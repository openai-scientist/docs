# Rule: Context Diagram v2 — Whole Product

## Phạm vi

Bản v2 là context view một page cho toàn bộ product FE–BE–LOGOS. Mức trừu tượng
là context, không phải package, component hoặc use case. Hệ thống trung tâm bao
gồm frontend, Platform API/backend và Scientific Core/LOGOS; các lớp này chỉ
được ghi trong mô tả của ellipse, không tách thành các node nội bộ.

## Nguồn bắt buộc

- FE product surface: `ai-research-platform-fe/src/app`, `src/lib/api`,
  `src/lib/realtime`, `src/lib/auth`.
- Backend/runtime: `logos/services/management`, `services/oversight`,
  `services/runner`, `stages/*`, `packages/*`.
- Role, boundary và authority đích: `LOGOS_Platform/01-san-pham`,
  `02-kien-truc`, `05-xuyen-he-thong`, `06-kiem-chung`, `08-ban-giao`.
- Style/layout baseline: `diagrams/12-context/System-Context-Diagram.drawio`
  page `main-2`; không sửa file legacy.

## Quy tắc style và nội dung

- Giữ grammar v1: một ellipse trung tâm, participant/external system là
  rectangle, tên đậm, line đen và route vuông góc.
- Hệ thống trung tâm phải thể hiện đủ FE, Platform API/backend và Scientific
  Core/LOGOS trong description.
- Role đích gồm Platform Operator, Tenant Admin, Project Manager, Researcher
  (Student) và Reviewer.
- External context gồm Literature & Evidence Services, External Data Sources,
  Local Node và AI Model Providers.
- Giữ đủ 69 trao đổi source-backed của page `main-2` v1; không tự rút gọn
  thành bộ flow mới. Chỉ sửa label/role cần thiết cho vocabulary đích; không đưa
  route FE, package, class hoặc mã requirement lên hình.
- Mỗi connector label là tiếng Anh, mô tả request, data, decision hoặc result;
  không dùng nhãn mơ hồ như `Data`, `Uses` hoặc `Process`.
- Mũi tên một chiều theo hướng trao đổi; nếu có hai chiều thì dùng hai cạnh
  riêng với nhãn riêng.
- Mỗi endpoint phải attach đúng rectangle/ellipse; không dangling, không đi
  xuyên participant khác, không đè route. Tenant Admin là node bổ sung nên phải
  dùng lane riêng phía trên trái, tách khỏi Project Manager và Researcher.
  Giữ khoảng cách đủ để label đọc được.
- Không có title/label chung ở góc trái canvas.
- Một page và một PNG export duy nhất trong `v2/`.

## Validation tối thiểu

- `python3 -m py_compile build_context_diagram.py`
- `python3 build_context_diagram.py`
- `xmllint --noout System-Context-Diagram.drawio`
- Export PNG bằng Draw.io sau lần sinh cuối và kiểm tra trực quan.
- Extractor xác nhận một page, 10 node (1 system + 9 participants), 69 edge,
  0 dangling edge và không có nhãn mã FE/M01–M12.
- Kiểm tra route xác nhận không có edge cắt/đè edge khác và không có route đi
  xuyên node ngoài endpoint; kiểm tra render thủ công và `git diff --check`.

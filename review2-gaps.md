# Review 2 – Nội dung còn thiếu (Report 1–5, mục I–V)

Đối chiếu `report/*.md` và [Report 7 docx](deliverables/FA26SE115_Report7.docx) với `docs/example/SWP490_R2_Huong-dan-chuan-bi-Review-2_1.pdf`.
Diagram đang được vẽ, sẽ chèn vào sau nên không liệt kê ở đây.

## Đã bổ sung vào docx (2026-10-29)

Nội dung lấy từ code (`logos`, `ai-research-platform-fe`), viết ở [deliverables/supplements/](deliverables/supplements/); `report/` không đổi.

- [x] II 6.2: repository, branch rules, Conventional Commits, CI của backend và web app (trả lời O-7: web app đã có CI).
- [x] IV 1.1 → 1.4 Technology Declaration: stack kèm version, dịch vụ bên thứ ba (mục đích, dữ liệu gửi đi), AI tools.
- [x] IV 1.1 → 1.5 Environments, Deployment and Rollback.
- [x] IV 2.2 → 2.4 Database Script: [FA26SE115_database-script.sql](deliverables/database/FA26SE115_database-script.sql) (41 bảng, Alembic `20261022_0048`).
- [x] V 4.2: thêm trường Execution (Automated/Manual, suy từ level và method theo V 2.1) và Actual result cho 60 TC.

## Cần leader quyết định / cung cấp

### Report 1 – Introduction
- [ ] I 3.2 KNIME và I 3.3 Orange: khung mẫu còn 2 heading này nhưng leader đã bỏ KNIME/Orange (changelog). Chọn: đổi tên heading thành 2 hệ thống AI Scientist, hay để trống?
- [ ] Các mục còn `[CONTENT TO BE ADDED]` (251 chỗ trong docx).

### Report 2 – Project Management Plan
- [ ] Danh sách main workflow (tối thiểu 4, đề xuất WF-01..05), mỗi workflow có 1 người phụ trách.
- [ ] Demo script cho mỗi workflow: 1 ca chính + 1 ca ngoại lệ, chạy trên staging, seed data nạp bằng script.

### Report 3 – SRS
- [ ] Bảng trạng thái cho Project, Local Node, Dossier, Decision Item (hiện mới có Run và Hand-off Object).
- [ ] Rà acceptance criteria của các feature bắt buộc: đo được, test được.
- [ ] Mô tả từng main workflow (bước, actor, ngoại lệ) để gắn activity diagram.

### Report 4 – SDD
- [ ] **ERD lệch database script.** Review 2 yêu cầu ERD khớp script. IV 2.1 (thiết kế v3) có entity chưa có bảng trong build hiện tại (ví dụ Dossier, Local Node, hand-off objects); script có bảng không có trong IV 2.1 (ví dụ `monitoring_*`, `integration_*`, `pi_consultations`). Chọn: ERD vẽ theo script hiện tại, hay ghi rõ phần v3 là "planned"?
- [ ] **Chưa có môi trường staging** (code có `APP_ENV=staging` nhưng chưa deploy). Review 2 yêu cầu demo trên staging: dựng staging hay xin demo trên production?
- [ ] AI tools: xác nhận model cụ thể team dùng (Claude Code, Codex) để ghi vào bảng.

### Report 5 – Test
- [ ] Đủ số TC tối thiểu: 3/feature bắt buộc + 1/workflow + 1/state transition + 1/NFR (thiếu TC theo workflow và transition; phụ thuộc 2 mục trên).
- [ ] Chạy test, ghi Actual result (hiện tất cả "Not run").

## Ưu tiên
1. Danh sách workflow, entity có state machine, ERD theo script hay v3, staging.
2. Đủ số TC tối thiểu, demo script, chạy test.
3. Placeholder còn lại.

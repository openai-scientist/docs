# Review 2 – Nội dung còn thiếu (Report 1–5, mục I–V)

Đối chiếu `report/*.md` và [Report 7 docx](deliverables/FA26SE115_Report7.docx) với `docs/example/SWP490_R2_Huong-dan-chuan-bi-Review-2_1.pdf`.
Mục đã xong được gỡ khỏi file này; lịch sử nằm trong [changelog](changelog.md).

## Gắn diagram vào docx
- [ ] `[CONTENT TO BE ADDED]` còn lại trong I–V chỉ là ô diagram: III 3.1.1 Screens Flow và IV 3.1–3.8 (8 Class Diagram, 61 Sequence Diagram). Gắn ảnh rồi xoá dòng placeholder. Ảnh UI Screen của III 3.2–3.9 và ERD (III 3.1.5) cũng gắn vào ô có sẵn. VI (66 chỗ) để sau Review 2.

## Cần leader quyết định / cung cấp

### Report 2 – Project Management Plan
- [ ] Danh sách main workflow (tối thiểu 4, đề xuất WF-01..05), mỗi workflow có 1 người phụ trách.
- [ ] Demo script cho mỗi workflow: 1 ca chính + 1 ca ngoại lệ, chạy trên staging, seed data nạp bằng script.

### Report 3 – SRS
- [ ] Bảng trạng thái cho Project, Local Node, Dossier, Decision Item (hiện mới có Run và Hand-off Object).
- [ ] Rà acceptance criteria của các feature bắt buộc: đo được, test được.
- [ ] Mô tả từng main workflow (bước, actor, ngoại lệ) để gắn activity diagram.
- [ ] Rà mô tả 63 chức năng III 3.2–3.9 ([S3](deliverables/supplements/S3-requirements.md)) với hành vi thực tế của app, nhất là Pause/Resume/Stop/Abandon/Sync run và Charter/Directives của AI PI.

### Report 4 – SDD
- [ ] IV 2.1 (thiết kế v3) cần leader cập nhật theo database script (ERD đã chốt vẽ theo script): ghi "planned" cho entity chưa có bảng (LiteratureBase, Finding, DatasetSnapshot, HypothesisSet, AnalysisPlan, ResearchPattern, EvidenceBundle, PaperPack, Lock, Envelope, ReleaseLog/Release, Dossier, Approval); bổ sung entity có bảng nhưng chưa mô tả (PlatformRole, ProjectFile, ProjectIntegration, IntegrationDelivery, SpendingAlert, NotificationEmail, NotificationPreference, GoogleConnectionGrant, FrameReview, RunArtifact, RunEvent, PIConsultation, PINote); thống nhất tên (Membership → ProjectMembership, Run → ResearchRun, ResearchCase → ResearchContext…).
- [ ] **Chưa có môi trường staging** (code có `APP_ENV=staging` nhưng chưa deploy). Review 2 yêu cầu demo trên staging: dựng staging hay xin demo trên production?
- [ ] AI tools: xác nhận model cụ thể team dùng (Claude Code, Codex) để ghi vào bảng.

### Report 5 – Test
- [ ] Đủ số TC tối thiểu: 3/feature bắt buộc + 1/workflow + 1/state transition + 1/NFR (thiếu TC theo workflow và transition; phụ thuộc 2 mục trên).
- [ ] Chạy test, ghi Actual result (hiện tất cả "Not run").

## Ưu tiên
1. Danh sách workflow, entity có state machine, cập nhật IV 2.1 theo script, staging.
2. Đủ số TC tối thiểu, demo script, chạy test.
3. Gắn diagram và ảnh màn hình.

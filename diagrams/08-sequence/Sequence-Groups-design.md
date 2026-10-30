# Sequence Diagrams — 8 nhóm Authentication đến Administration

Mỗi folder có một file draw.io chính; mỗi tab là một sequence riêng. PNG được xuất theo tab.

Nguồn: `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`, SHA256 `8618eb8123e0a3d259c9e5f5ba97f9e29602534ae3503b2aaa25e0d2e5eb232d`. Nội dung theo III và IV của snapshot này; đối chiếu [Report III](../../report/03-software-requirements-specification.md), [Report IV](../../report/04-software-design-document.md) và [thiết kế class](../07-class/Class-Diagrams-design.md).

Đây là thiết kế đề xuất để duyệt, không phải reverse-engineering hoặc xác nhận runtime. Operation có trên Class Diagram được dùng lại; nhãn hành vi chưa có operation được giữ ở mức khái niệm, không tự tạo endpoint, DTO hoặc HTTP status. Theo yêu cầu người dùng, mọi tương tác dữ liệu đi qua Repository: Service → Repository → Database, reply theo chiều ngược lại. Repository là phân tách trách nhiệm thiết kế của bộ sequence này, không khẳng định đã có trong BE hoặc Class Diagram hiện tại. Không đổi Class Diagram hay BE trong đợt sửa này.

Email Code trong tab đầu Authentication và bản standalone dùng cùng model có Repository; giữ luồng nghiệp vụ đã duyệt. Không khung ngoài, nền trắng, actor bên trái, tên actor hạ cách chân, reply nét đứt về caller, guard có hàng riêng; không dùng activation lồng dài qua opt. Khổ preview theo nội dung, chưa chứng minh phù hợp in A4/Word.

## Xử lý caption cũ và giới hạn

- Caption Answer Gate được ánh xạ sang Answer Decision Inbox Item (FR-28–30).
- Caption Accept/Send Back/Rerun được thể hiện bằng acceptance, revision và version mới; không mở lại accepted object để sửa.
- Pause/Resume/Stop/Abandon dùng Cancel and Synchronize Run theo state model IV 3.4; không tạo state paused hoặc resurrect ended run.
- Charter/Directives → Configure Action Policy; Consultations → Handle Must-Ask and Tentative Decisions; Endorse/Retry → Confirm or Overturn Tentative Decision theo IV 3.6.
- Reviewer Queue → View Actionable Decision Inbox, không khôi phục queue nghiệp vụ riêng đã bỏ.
- Execution và Paper thêm theo IV 3.5 (FE-09/10); Local Job thêm theo Figure IV-12. Experiment Design và Execution cùng đối chiếu Figure IV-10.
- Các lựa chọn dùng alt riêng; không ghép Rename/Test/Delete thành một message có dấu /. Read không biến thành write, lỗi không rơi tiếp vào nhánh thành công.
- Quyền project được kiểm tra trước khi đọc/ghi; Sign In/Invitation và Platform Admin dùng đúng scope. Admin project list chỉ trả metadata. Secret chỉ trả reference; không đưa khóa vào log/output.
- Engine pages mô tả lifecycle dưới một request điều phối, không quy định giao thức HTTP chờ job hoàn thành. Run Start trả Run trước, stage chạy nền và kết quả theo dõi ở tab Monitor; event bất đồng bộ dùng đầu mở.
- Handle Must-Ask và Receive Notifications bắt đầu từ event hệ thống trong context run/project đã được xác thực, không phụ thuộc user đang mở UI. UI chỉ nhận update khi connected và authorized; quyền trả lời được kiểm tra riêng trong tab answer/confirm.
- Không thêm FE-18/19 sau MVP hoặc tự giải quyết các khác biệt requirement chưa được chốt. Placeholder Report7 và requirement gốc không sửa.

## Tái tạo

`python diagrams/08-sequence/build_sequence_groups.py` (Python stdlib). Nguồn flow: [sequence_flows.py](sequence_flows.py); layout: [builder](build_sequence_groups.py). Export PNG bằng draw.io CLI `-x -f png -s 2 -b 20 -p <tab 1-based> -o <PNG> <drawio>`.

Ngoại lệ export: Execute Local Job and Release Aggregate, Hypothesis Stage, Independent Review and Revision Rounds, Execution Stage and Unseal Results dùng `-s 1` (100%). Các ảnh này bị cắt phần cuối khi native exporter xuất ở scale 2; scale 1 đã kiểm tra đủ nội dung. Giữ nguyên geometry/cỡ chữ trong editable.

## Inventory

| Nhóm / file | Tab | Sequence / PNG | Nguồn Report7 |
|---|---:|---|---|
| [Authentication & Account](01-authentication-account/Sequence-Diagrams-Authentication-Account.drawio) | 1 | [Sign In With Email Code](01-authentication-account/01-Sign-In-With-Email-Code.png) | IV 3.1.2; III 3.2.1; FR-01 |
| [Authentication & Account](01-authentication-account/Sequence-Diagrams-Authentication-Account.drawio) | 2 | [Sign In With Google](01-authentication-account/02-Sign-In-With-Google.png) | IV 3.1.3; III 3.2.2; FR-146 |
| [Authentication & Account](01-authentication-account/Sequence-Diagrams-Authentication-Account.drawio) | 3 | [Complete Onboarding and Update Profile](01-authentication-account/03-Complete-Onboarding-and-Update-Profile.png) | IV 3.1.4; III 3.2.3 |
| [Authentication & Account](01-authentication-account/Sequence-Diagrams-Authentication-Account.drawio) | 4 | [Sign Out](01-authentication-account/04-Sign-Out.png) | IV 3.1.5; III 3.2.4 |
| [Authentication & Account](01-authentication-account/Sequence-Diagrams-Authentication-Account.drawio) | 5 | [View Unauthorized and Session Expired Pages](01-authentication-account/05-View-Unauthorized-and-Session-Expired-Pages.png) | IV 3.1.6; III 3.2.5; FR-02, FR-151 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 1 | [Create Project](02-project-workspace/01-Create-Project.png) | IV 3.2.2; III 3.3.1; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 2 | [View Project List and Overview](02-project-workspace/02-View-Project-List-and-Overview.png) | IV 3.2.3; III 3.3.2; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 3 | [Update Archive or Complete Project](02-project-workspace/03-Update-Archive-or-Complete-Project.png) | IV 3.2.4; III 3.3.3; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 4 | [Manage Members and Invitations](02-project-workspace/04-Manage-Members-and-Invitations.png) | IV 3.2.5; III 3.3.4; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 5 | [Manage Documents](02-project-workspace/05-Manage-Documents.png) | IV 3.2.6; III 3.3.5; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 6 | [Manage Project Integrations and Preferences](02-project-workspace/06-Manage-Project-Integrations-and-Preferences.png) | IV 3.2.7; III 3.3.6; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 7 | [Accept or Decline Invitation](02-project-workspace/07-Accept-or-Decline-Invitation.png) | IV 3.2.8; III 3.3.7; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 8 | [Resend or Cancel Invitation](02-project-workspace/08-Resend-or-Cancel-Invitation.png) | IV 3.2.9; III 3.3.8; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 9 | [Transfer Ownership](02-project-workspace/09-Transfer-Ownership.png) | IV 3.2.10; III 3.3.9; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 10 | [Delete Project](02-project-workspace/10-Delete-Project.png) | IV 3.2.11; III 3.3.10; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 11 | [View Project Activity and Audit Log](02-project-workspace/11-View-Project-Activity-and-Audit-Log.png) | IV 3.2.12; III 3.3.11; IV 3.2 |
| [Project Workspace](02-project-workspace/Sequence-Diagrams-Project-Workspace.drawio) | 12 | [Configure Project Settings and Monthly Budget](02-project-workspace/12-Configure-Project-Settings-and-Monthly-Budget.png) | IV 3.2.13; III 3.3.12; IV 3.2 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 1 | [Upload Dataset](03-data-management/01-Upload-Dataset.png) | IV 3.3.2; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 2 | [View Dataset Detail](03-data-management/02-View-Dataset-Detail.png) | IV 3.3.3; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 3 | [Manage Data Connection and Import](03-data-management/03-Manage-Data-Connection-and-Import.png) | IV 3.3.4; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 4 | [Rename or Delete Dataset](03-data-management/04-Rename-or-Delete-Dataset.png) | IV 3.3.5; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 5 | [Upload New Dataset Version](03-data-management/05-Upload-New-Dataset-Version.png) | IV 3.3.6; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 6 | [Download or Preview Dataset Version](03-data-management/06-Download-or-Preview-Dataset-Version.png) | IV 3.3.7; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 7 | [Browse and Preview Connection Source](03-data-management/07-Browse-and-Preview-Connection-Source.png) | IV 3.3.8; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 8 | [Rename Test or Delete Data Connection](03-data-management/08-Rename-Test-or-Delete-Data-Connection.png) | IV 3.3.9; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 9 | [Connect Google Sheets and Drive](03-data-management/09-Connect-Google-Sheets-and-Drive.png) | IV 3.3.10; III 3.4; IV 3.3; FR-09–12 |
| [Data Management](03-data-management/Sequence-Diagrams-Data-Management.drawio) | 10 | [Execute Local Job and Release Aggregate](03-data-management/10-Execute-Local-Job-and-Release-Aggregate.png) | Figure IV-12; III 3.4; IV 3.3; FR-09–12 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 1 | [Start Research Run](04-research-run-orchestration/01-Start-Research-Run.png) | IV 3.4.2; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 2 | [Monitor Run in Run Studio](04-research-run-orchestration/02-Monitor-Run-in-Run-Studio.png) | IV 3.4.3; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 3 | [Answer Decision Inbox Item](04-research-run-orchestration/03-Answer-Decision-Inbox-Item.png) | IV 3.4.4; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 4 | [Accept Revise or Rerun Stage Version](04-research-run-orchestration/04-Accept-Revise-or-Rerun-Stage-Version.png) | IV 3.4.5; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 5 | [Cancel and Synchronize Run](04-research-run-orchestration/05-Cancel-and-Synchronize-Run.png) | IV 3.4.6; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 6 | [Raise Token Budget](04-research-run-orchestration/06-Raise-Token-Budget.png) | IV 3.4.7; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 7 | [View Review Rounds Diffs and Artifacts](04-research-run-orchestration/07-View-Review-Rounds-Diffs-and-Artifacts.png) | IV 3.4.8; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 8 | [Comment On Run](04-research-run-orchestration/08-Comment-On-Run.png) | IV 3.4.9; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 9 | [View Run List](04-research-run-orchestration/09-View-Run-List.png) | IV 3.4.10; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 10 | [View Recovery State](04-research-run-orchestration/10-View-Recovery-State.png) | IV 3.4.11; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 11 | [Download and Compare Artifacts](04-research-run-orchestration/11-Download-and-Compare-Artifacts.png) | IV 3.4.12; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 12 | [View Iteration Summary](04-research-run-orchestration/12-View-Iteration-Summary.png) | IV 3.4.13; III 3.5; IV 3.4 |
| [Research Run Orchestration](04-research-run-orchestration/Sequence-Diagrams-Research-Run-Orchestration.drawio) | 13 | [Edit or Delete Comment](04-research-run-orchestration/13-Edit-or-Delete-Comment.png) | IV 3.4.14; III 3.5; IV 3.4 |
| [Research Engines](05-research-engines/Sequence-Diagrams-Research-Engines.drawio) | 1 | [Dataset Stage](05-research-engines/01-Dataset-Stage.png) | IV 3.5.2; IV 3.5; FE-06–11; FR-37–78 |
| [Research Engines](05-research-engines/Sequence-Diagrams-Research-Engines.drawio) | 2 | [Hypothesis Stage](05-research-engines/02-Hypothesis-Stage.png) | IV 3.5.3; IV 3.5; FE-06–11; FR-37–78 |
| [Research Engines](05-research-engines/Sequence-Diagrams-Research-Engines.drawio) | 3 | [Experiment Design Stage and Lock](05-research-engines/03-Experiment-Design-Stage-and-Lock.png) | IV 3.5.4 / Figure IV-10; IV 3.5; FE-06–11; FR-37–78 |
| [Research Engines](05-research-engines/Sequence-Diagrams-Research-Engines.drawio) | 4 | [Independent Review and Revision Rounds](05-research-engines/04-Independent-Review-and-Revision-Rounds.png) | IV 3.5.5; IV 3.5; FE-06–11; FR-37–78 |
| [Research Engines](05-research-engines/Sequence-Diagrams-Research-Engines.drawio) | 5 | [Execution Stage and Unseal Results](05-research-engines/05-Execution-Stage-and-Unseal-Results.png) | IV 3.5 / FE-09 / Figure IV-10; IV 3.5; FE-06–11; FR-37–78 |
| [Research Engines](05-research-engines/Sequence-Diagrams-Research-Engines.drawio) | 6 | [Paper Stage](05-research-engines/06-Paper-Stage.png) | IV 3.5 / FE-10; IV 3.5; FE-06–11; FR-37–78 |
| [AI Principal Investigator](06-ai-principal-investigator/Sequence-Diagrams-AI-Principal-Investigator.drawio) | 1 | [Configure Action Policy](06-ai-principal-investigator/01-Configure-Action-Policy.png) | IV 3.6.2; IV 3.6; FR-25–36, FR-262–266 |
| [AI Principal Investigator](06-ai-principal-investigator/Sequence-Diagrams-AI-Principal-Investigator.drawio) | 2 | [Handle Must-Ask and Tentative Decisions](06-ai-principal-investigator/02-Handle-Must-Ask-and-Tentative-Decisions.png) | IV 3.6.3; IV 3.6; FR-25–36, FR-262–266 |
| [AI Principal Investigator](06-ai-principal-investigator/Sequence-Diagrams-AI-Principal-Investigator.drawio) | 3 | [Confirm or Overturn Tentative Decision](06-ai-principal-investigator/03-Confirm-or-Overturn-Tentative-Decision.png) | IV 3.6.4; IV 3.6; FR-25–36, FR-262–266 |
| [AI Principal Investigator](06-ai-principal-investigator/Sequence-Diagrams-AI-Principal-Investigator.drawio) | 4 | [View Lab Notebook](06-ai-principal-investigator/04-View-Lab-Notebook.png) | IV 3.6.5; IV 3.6; FR-25–36, FR-262–266 |
| [AI Principal Investigator](06-ai-principal-investigator/Sequence-Diagrams-AI-Principal-Investigator.drawio) | 5 | [View PI Overview and Close Report](06-ai-principal-investigator/05-View-PI-Overview-and-Close-Report.png) | IV 3.6.6; IV 3.6; FR-25–36, FR-262–266 |
| [Notifications & Integrations](07-notifications-integrations/Sequence-Diagrams-Notifications-Integrations.drawio) | 1 | [Receive Notifications](07-notifications-integrations/01-Receive-Notifications.png) | IV 3.7.2; IV 3.7; FR-29, FR-100, FR-255, FR-264 |
| [Notifications & Integrations](07-notifications-integrations/Sequence-Diagrams-Notifications-Integrations.drawio) | 2 | [View Actionable Decision Inbox](07-notifications-integrations/02-View-Actionable-Decision-Inbox.png) | IV 3.7.3; IV 3.6; FR-28; ADR-05 |
| [Notifications & Integrations](07-notifications-integrations/Sequence-Diagrams-Notifications-Integrations.drawio) | 3 | [Set Notification Preferences](07-notifications-integrations/03-Set-Notification-Preferences.png) | IV 3.7.4; III 3.8.3; IV 3.7 |
| [Notifications & Integrations](07-notifications-integrations/Sequence-Diagrams-Notifications-Integrations.drawio) | 4 | [Mark Notifications as Read](07-notifications-integrations/04-Mark-Notifications-as-Read.png) | IV 3.7.5; III 3.8.4 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 1 | [Manage Users](08-administration-monitoring/01-Manage-Users.png) | IV 3.8.2; III 3.9; IV 3.8; FE-17 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 2 | [Configure Models and Decision Provider](08-administration-monitoring/02-Configure-Models-and-Decision-Provider.png) | IV 3.8.3; III 3.9; IV 3.8; FE-17 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 3 | [Edit Platform and Engine Settings](08-administration-monitoring/03-Edit-Platform-and-Engine-Settings.png) | IV 3.8.4; III 3.9; IV 3.8; FE-17 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 4 | [View Usage Audit Log and Log Monitoring](08-administration-monitoring/04-View-Usage-Audit-Log-and-Log-Monitoring.png) | IV 3.8.5; III 3.9; IV 3.8; FE-17 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 5 | [View Admin Overview](08-administration-monitoring/05-View-Admin-Overview.png) | IV 3.8.6; III 3.9; IV 3.8; FE-17 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 6 | [View and Edit User Detail](08-administration-monitoring/06-View-and-Edit-User-Detail.png) | IV 3.8.7; III 3.9; IV 3.8; FE-17 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 7 | [View All Projects](08-administration-monitoring/07-View-All-Projects.png) | IV 3.8.8; III 3.9; IV 3.8; FE-17 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 8 | [Grant or Revoke Platform Admin](08-administration-monitoring/08-Grant-or-Revoke-Platform-Admin.png) | IV 3.8.9; III 3.9; IV 3.8; FE-17 |
| [Administration & Monitoring](08-administration-monitoring/Sequence-Diagrams-Administration-Monitoring.drawio) | 9 | [View System Health and Acknowledge Alerts](08-administration-monitoring/09-View-System-Health-and-Acknowledge-Alerts.png) | IV 3.8.10; III 3.9; IV 3.8; FE-17 |

## Validation

Kết quả chạy thực tế ghi trong changelog. Validator XML/geometry không thay thế export và xem PNG. Chưa chèn vào Word, chưa kiểm tra in A4 hoặc runtime nghiệp vụ.

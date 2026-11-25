# Diagram cho bản Report 7 không có Local Node

Bản sao các diagram dùng cho [FA26SE115_Report7_No-Local-Node.docx](../../deliverables/FA26SE115_Report7_No-Local-Node.docx). Dữ liệu được lưu và xử lý trên Platform; không có Local Node, Release Gate, release log hay runner. Diagram gốc trong `diagrams/` giữ nguyên.

| Diagram | Nguồn sửa | Ảnh |
|---|---|---|
| System Context | `12-context/v2/System-Context-Diagram.drawio` | `12-context/v2/System-Context-Diagram.png` |
| Use Case | `01-use-case/AI-Research-Experimentation-Platform-Use-Case.drawio` | `01-use-case/Use case.png` |
| Screen Flow (bỏ SC-30) | `02-screen-flow/v2/build_role_tabs.py` | `02-screen-flow/v2/Screen-Flow-*.png` |
| System Architecture, Deployment | `04-system-overview/v2/*.drawio` | `04-system-overview/v2/*.png` |
| AI research tier | `04-system-overview/System-Architecture-v3-ai-tier.html` | `04-system-overview/System-Architecture-v3-ai-tier.png` |
| Package | `05-package/v2/Package-Diagram.drawio` | `05-package/v2/Package-Diagram.png` |
| Database | `06-database/Database-Diagram.drawio` | `06-database/Database-Diagram.png` |
| Class | `07-class/v2/Class-Diagram-Authentication-Account.drawio` (+ `class_model.py` cho bản Mermaid) | `07-class/v2/Class-Diagram-*.png` |
| Sequence Data Management | `08-sequence/sequence_flows.py` → `build_sequence_groups.py` | `08-sequence/03-data-management/*.png` |

Các file `.drawio` là nguồn chính. Builder của context, architecture, deployment, package và database không được chép sang vì builder gốc vẫn sinh Local Node.

Công cụ:

- `rm_cells.py <file.drawio> <id>...`: xoá cell kèm cell con và cạnh nối.
- `export_page.py <file.drawio> "<tên trang>" <out.png> [scale]`: xuất đúng một trang (cờ `-p` của draw.io CLI không ổn định).

# System Overview v2 — LOGOS

Bản v2 của hai hình Report 7 IV 1.1: System Architecture Diagram (IV-1) và Deployment Diagram (IV-2). Giữ bố cục và style của bản v1 ở thư mục cha, chỉ sửa nội dung cho khớp code. Bản v1 giữ nguyên.

## Nguồn

- `logos/deploy/docker-compose.prod.yml` (commit 94eb2492): các service, volume, mạng `capstone-net`.
- `ai-research-platform-fe/docker/docker-compose.prod.yml` (commit 43de0a2): service `fe`.
- `logos/services/runner`: runner ở Local Node gọi Platform API qua HTTPS để nhận job và trả kết quả.
- `logos/services/management/core/config.py`: production dùng `storage_backend=r2`.
- Vai trò: `LOGOS_Platform/01-san-pham/02-vai-tro-va-persona.md`.

## System Architecture — thay đổi so với v1

| Mục | v1 | v2 |
|---|---|---|
| Khung VPS | OpenAI-Scientist on a Linux VPS | LOGOS on a Linux VPS |
| Người dùng | 4 vai trò, có Platform Admin | 5 vai trò LOGOS: Researcher (student), Project Manager, Reviewer, Tenant Admin, Platform Operator |
| Engine thứ 5 | Paper Engine | Writing Engine (service `writing`) |
| Local Node | Mũi tên vào AI research tier | Mũi tên tới Cloudflare: runner gọi Platform API để nhận job và trả kết quả |
| Cloudflare R2 | Viền nét đứt (tuỳ chọn) | Viền liền: production bắt buộc dùng R2 |

## Deployment — thay đổi so với v1

| Mục | v1 | v2 |
|---|---|---|
| Frame | `dep OpenAI-Scientist production` | `dep LOGOS production` |
| Engine | 5 node, thiếu `writing` | 6 node: oversight, dataset, hypothesis, experiment-design, execution, writing |
| Backup | Không có | Node `backup` (TCP 5432 tới `db`) và cloud service off-site backup storage (rclone remote) |
| Local Node | Không có | «device» Local Node, «artifact» logos-runner, HTTPS tới Cloudflare |
| Note | Có một note | Bỏ, diagram không có note |

## Ký hiệu

- Deployment theo UML 2.5 nhưng vẽ node bằng hình chữ nhật phẳng thay cho khối 3D (theo yêu cầu); loại node do stereotype thể hiện: `«device»` cho phần cứng, `«executionEnvironment»` cho môi trường chạy phần mềm, `«artifact»` cho thứ được triển khai. Communication path là đường liền, nhãn ghi giao thức. `«cloud service»` là stereotype tự định nghĩa cho dịch vụ bên ngoài.
- System Architecture giữ style card và icon của v1, không theo đủ ký hiệu C4. C4 yêu cầu mỗi phần tử ghi loại và công nghệ, và mỗi hình có legend. Hai điểm này chưa áp dụng để giữ style hiện tại.

## Sinh lại

```bash
python3 build_system_architecture.py
python3 build_deployment_diagram.py
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -s 2 --border 20 -o System-Architecture-Diagram.png System-Architecture-Diagram.drawio
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -s 2 --border 20 -o Deployment-Diagram-Production.png Deployment-Diagram-Production.drawio
```

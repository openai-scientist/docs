# Context Diagram v2 — Whole Product

Bản v2 là bản redraw có kiểm soát từ page `main-2` của v1, không phải một layout
mới. Bản v1 ở thư mục cha giữ nguyên; v2 giữ nguyên ellipse, rectangle, vị trí,
kích thước, typography, canvas và routing của v1, sau đó chỉ sửa phần tên/phạm
vi cần thiết cho toàn hệ thống FE–Platform API–Scientific Core/LOGOS.

## Artifact

- Source-backed repos:
  - `/Users/ngothanhdat/Documents/CODE/3. capstone/capstone-projects/projects/ai-research-platform-fe`
  - `/Users/ngothanhdat/Documents/CODE/3. capstone/capstone-projects/projects/logos`
- Business semantics: `/Users/ngothanhdat/Documents/CODE/3. capstone/capstone-projects/docs/LOGOS_Platform`
- Builder: [`build_context_diagram.py`](build_context_diagram.py)
- Editable source: [`System-Context-Diagram.drawio`](System-Context-Diagram.drawio)
- PNG duy nhất: [`System-Context-Diagram.png`](System-Context-Diagram.png)

## Phạm vi hệ thống trung tâm

Ellipse trung tâm là **AI Research Experimentation Platform**, gồm ba lớp dưới
đây. Theo chuẩn context diagram (DFD mức 0), hệ thống là một process duy nhất nên
ellipse chỉ ghi tên, không liệt kê thành phần bên trong:

- AI Research Platform FE
- Platform API/backend
- Scientific Core / LOGOS

Context diagram không bung các package nội bộ FE/BE/LOGOS thành node riêng; phần
đó đã thuộc Package/Architecture Diagram. Bộ 69 luồng source-backed của page v1
được giữ lại để không làm mất nội dung; chỉ sửa tên hệ thống, tên external/role
và mapping quản trị cần thiết.

## Delta so với v1

| Thành phần | v1 | v2 |
|---|---|---|
| System label | OpenAI-Scientist | AI Research Experimentation Platform |
| System description | Tabular-data scientific research platform | Bỏ; ellipse chỉ ghi tên hệ thống |
| Platform Admin | Một actor hiện trạng | Tách thành Platform Operator và Tenant Admin theo vocabulary đích |
| External names | Large Language Model Provider; Literature & Evidence Sources | AI Model Providers; Literature & Evidence Services |
| Layout/style | `main-2`, ellipse 800×650, các box và route v1 | Giữ nguyên; chỉ thêm node Tenant Admin cần cho mapping role |
| Routing correction | Chưa có Tenant Admin | Tenant Admin có hai lane thẳng phía trên Project Manager, vào đỉnh ellipse giữa bó Project Manager và bó Reviewer; không đường nào cắt nhau, nhãn không đè lên box |
| Exchanges | 69 | 69, không rút gọn thành 19 |

## Participants và external systems

| Nhóm | Node | Trao đổi chính |
|---|---|---|
| Role | Platform Operator | Governance/service requests; operational status and audit |
| Role | Tenant Admin | Tenant and policy administration; usage and audit views |
| Role | Project Manager | Project and budget decisions; activity and resource reports |
| Role | Researcher (student) | Research cases, datasets, run decisions, stage outputs, evidence and decision inbox |
| Role | Reviewer | Review findings, approval decisions, assignments and dossiers |
| External | Literature & Evidence Services | Literature/evidence queries and bibliographic evidence |
| External | External Data Sources | Data discovery/import requests and source metadata/version data |
| External | Local Node | Local analysis/release, approved aggregates and node status |
| External | AI Model Providers | Inference/generation requests and model responses/review findings |

Các role trên dùng vocabulary đích của `LOGOS_Platform`. Code hiện tại còn có
`System Admin`/`Platform Admin`; mapping sang `Platform Operator` và `Tenant
Admin` được ghi là transition/mismatch trong handoff, không được hiểu là đã
migrate chỉ từ tên actor trên hình.

## Style giữ nguyên từ v1

- Một ellipse hệ thống ở giữa, participant/external system là rectangle đậm.
- Nền trắng, viền đen, font Arial, đường nối đen vuông góc.
- Giữ geometry v1: ellipse tại `(1370, 675)` kích thước `800×650`; các actor
  hiện hữu giữ nguyên vị trí và kích thước của page `main-2`.
- Connector label là tiếng Anh, dùng cụm danh từ mô tả request, decision, data
  hoặc result.
- Một page và một PNG duy nhất.
- Không có title/label chung ở góc trái canvas.
- Không đưa mã FE, M01–M12, route, class hoặc package implementation lên hình.

## Sinh lại

```bash
python3 build_context_diagram.py
/Applications/draw.io.app/Contents/MacOS/draw.io --disable-update --export \
  --format png --page-index 1 --size diagram --border 20 \
  --output System-Context-Diagram.png System-Context-Diagram.drawio
```

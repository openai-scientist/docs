# Package Diagram v2 — LOGOS (theo code)

Package diagram UML vẽ theo cấu trúc code thật của hai repo sản phẩm. Style giữ như v1 ở thư mục cha. Bản v2 cũ (bản chuyển tiếp) đã được xoá.

## Nguồn

| Khung (namespace thật) | Package | Nguồn |
|---|---|---|
| `ai-research-platform-fe` | app, components, hooks, server, stores, lib, types | `ai-research-platform-fe/src` (commit 43de0a2) |
| `services` | `management`, `logos_oversight`, `logos_runner` | `logos/services/*` (commit 94eb2492) |
| `services::management` | 14 module, mỗi hàng một lớp; `db`, `core`, `infra` là lớp thấp nhất | contract import-linter "Feature layering" trong `services/management/pyproject.toml` |
| `stages` | dataset, hypothesis, experiment_design, execution, writing | `logos/stages/*` |
| `packages` | discovery, recompute, analysis, engine, tables, contract | dependency trong `pyproject.toml` của từng package |

`research` (orchestrator) gọi `logos_oversight` và từng stage qua HTTP; `runners` gọi `logos_runner`. `audit` dùng `core`, `db`; `access` dùng `core`. `packages/connectors` không được vẽ vì thư mục này không có file nào được git theo dõi.

## Quy ước tên và ký hiệu (UML 2.5.1)

- Khung ngoài `pkg LOGOS`: `pkg` là viết tắt chuẩn của frame kind package, theo sau là tên phần tử.
- Package có vẽ phần tử con bên trong thì tên nằm ở tab; package không có con thì tên nằm giữa thân.
- Tên package dùng đúng tên thư mục hoặc tên package Python trong code. Không dùng nhóm tự đặt hay stereotype ngoài chuẩn.
- Python import là dependency sử dụng, ghi `«use»`. Không dùng `«import»`, vì trong UML từ khoá này là public package import (gộp namespace). Lời gọi giữa các service ghi `«use» HTTP`.

## Sinh lại

```bash
python3 build_package_diagram.py Package-Diagram.drawio
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -s 2 -o Package-Diagram.png Package-Diagram.drawio
```

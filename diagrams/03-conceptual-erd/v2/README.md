# Conceptual ERD v2 — LOGOS Platform

- Nguồn: `capstone-projects/docs/LOGOS_Platform/visual/model.py` (`ENT`, `REL`) — 91 thực thể, 108 quan hệ, khớp `04-du-lieu/02-erd-khai-niem.md`.
- Một hình duy nhất, style v1: box trắng 160 × 40, Arial, đường đen vuông góc, Crow's Foot hai đầu, nhãn tiếng Anh, không thuộc tính/PK/FK.
- Bố cục theo module: mỗi module (M01…M12, CORE) là một khối, xếp trái→phải theo thứ tự phụ thuộc trong `CONTEXTS` (4 khối mỗi hàng); trong khối, Graphviz `dot` (trên xuống) đặt entity theo quan hệ nội bộ, snap lưới 20 px; đường nối do router A* lưới 10 px của builder (cùng luật v1): vuông góc, không xuyên entity, không đi chung đoạn với đường khác, mỗi điểm nối trên cạnh entity chỉ một đường.

Bản số: `1:N` → `||—o<`, `N:1` → `>o—||`, `1:1` → `||—||`, `1:0..1` → `||—o|`, `N:0..1` → `>o—o|`, `N:N` → `>o—o<`.

## Sinh lại

```bash
brew install graphviz   # cần lệnh dot
python3 build_erd.py
/Applications/draw.io.app/Contents/MacOS/draw.io --disable-update --export --format png \
  --size diagram --border 20 --output Entity-Relationship-Diagram-Conceptual.png \
  Entity-Relationship-Diagram-Conceptual.drawio
xmllint --noout Entity-Relationship-Diagram-Conceptual.drawio
```

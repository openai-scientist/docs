# Rule: Conceptual ERD v2 — LOGOS Platform

Kế thừa ký hiệu và điều cấm của [rule v1](../rule.md) (Crow's Foot, mức conceptual, không thuộc tính/PK/FK). Khác v1 ở nguồn và bố cục:

- Nguồn: `LOGOS_Platform/visual/model.py` (`ENT`, `REL`), đủ 91 thực thể và 108 quan hệ như [`04-du-lieu/02-erd-khai-niem.md`]; không suy entity từ database script.
- Một hình duy nhất; style v1: box trắng 160 × 40, Arial, đường đen vuông góc, nhãn quan hệ tiếng Anh, không title, lane, màu hay legend.
- Bản số theo `REL`: `1:N` `||—o<`, `N:1` `>o—||`, `1:1` `||—||`, `1:0..1` `||—o|`, `N:0..1` `>o—o|`, `N:N` `>o—o<`.
- Đường nối: không xuyên entity, không đi chung đoạn với đường khác, mỗi điểm nối một đường; được phép cắt nhau.
- Chỉ sửa qua [`build_erd.py`](build_erd.py), rồi export lại PNG (lệnh trong [README](README.md)).

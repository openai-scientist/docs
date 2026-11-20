"""Build the LOGOS conceptual ERD (v2) as one draw.io page in the v1 style.

Usage:
    python3 build_erd.py [MODEL.py] [OUTPUT.drawio]

Source of truth: LOGOS_Platform/visual/model.py (ENT, REL), all entities and
relations. Graphviz `dot` (splines=ortho) computes node positions and
orthogonal routes; this script only converts them to draw.io cells with
white 160x40 boxes, black lines, Arial and Crow's Foot ends.
"""

from __future__ import annotations

import argparse
import heapq
import importlib.util
import json
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve()
DEFAULT_MODEL = ROOT.parents[4] / "capstone-projects" / "docs" / "LOGOS_Platform" / "visual" / "model.py"
DEFAULT_OUTPUT = ROOT.parent / "Entity-Relationship-Diagram-Conceptual.drawio"
W, H, MARGIN = 160, 40, 40

# (start marker at REL source, end marker at REL target)
ENDS = {
    "1:N": ("ERmandOne", "ERzeroToMany"), "N:1": ("ERzeroToMany", "ERmandOne"),
    "1:1": ("ERmandOne", "ERmandOne"), "1:0..1": ("ERmandOne", "ERzeroToOne"),
    "N:0..1": ("ERzeroToMany", "ERzeroToOne"), "N:N": ("ERzeroToMany", "ERzeroToMany"),
}

EN_LABELS = {
    "bật cờ": "enables feature flag", "bị giới hạn": "limits", "bị giữ": "is under legal hold",
    "bị yêu cầu xóa": "requests deletion for", "cho phép": "permits", "chuyển giao": "hands over",
    "chạy": "runs", "chặn": "blocks", "chọn": "selects", "chốt cấu hình": "snapshots config",
    "chứa": "contains", "cung cấp": "provides", "có": "has", "có Case": "has case",
    "có Inquiry": "has inquiry", "có dòng thời gian": "has timeline", "có giá": "has rate card",
    "có giá trị": "defines value", "có hoạt động": "has activity", "có kế hoạch": "has plan", "có phiên bản": "has version",
    "có phương án": "has option", "có thành viên": "has member", "có việc": "has task",
    "căn cứ": "bases", "cấp lease": "leases", "cấp quyền": "grants share",
    "cần duyệt (phát hành)": "requires release approval", "cần duyệt (tài nguyên)": "requires resource approval",
    "cần hỗ trợ": "requests support", "cần phê duyệt": "requires approval", "cần quyết định": "requires decision",
    "cần đối chiếu": "requires reconciliation", "dùng cho": "used for", "dùng key": "uses credential",
    "dùng model": "uses model", "dẫn xuất": "derives", "dựng": "builds", "dựng bản thảo": "drafts manuscript",
    "giao": "assigns", "giao cho Core qua": "sends to Core via", "giữ": "holds", "giữ chỗ": "reserves",
    "giữ suất": "leases capacity", "gửi": "sends", "gửi qua": "delivers via", "hạch toán": "posts to ledger",
    "khai báo": "declares conflict", "khởi tạo": "creates", "kiểm quyền dữ liệu": "checks data access",
    "kết nối": "connects", "là reviewer": "reviews", "là tác nhân": "acts as actor", "lưu bởi": "stored by",
    "mang vai trò": "carries role", "mời": "invites", "ngoại lệ": "exempts", "nhận": "receives",
    "nhận phiếu": "receives vote", "nhận sự kiện": "receives event", "nằm trong": "belongs to",
    "phát hành": "releases", "phát sinh": "generates usage", "quyết toán": "settles", "ref": "references",
    "ref + digest": "references with digest", "sinh": "produces", "sinh việc (sự kiện)": "creates task from event",
    "thuộc": "belongs to", "thử": "attempts", "trên phiên bản": "for version", "trình bày": "presents",
    "tạo kết quả": "produces result", "viết": "writes", "xin vượt": "requests exception", "xác thực": "authenticates",
    "ánh xạ qua command ID": "maps by command ID", "áp dụng": "applies", "đánh dấu": "bookmarks",
    "đăng nhập": "signs in", "đăng nhập qua": "signs in via", "được chiếu": "is projected", "được cấp": "is granted",
    "được dùng": "is used by", "được ghi bởi": "recorded by", "được gắn": "binds", "được kiểm tra": "is reviewed",
    "được lập chỉ mục": "is indexed", "được nhận": "is admitted", "được niêm phong": "is sealed",
    "được phân loại": "is classified", "được phản biện": "is reviewed by", "được thảo luận": "is discussed",
    "được trả lời": "is answered", "được đọc qua": "is read through", "đặt": "sets", "ủy quyền": "delegates",
}


def load_model(path: Path):
    spec = importlib.util.spec_from_file_location("logos_visual_model", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def layout(entities, relations) -> dict:
    """Run graphviz dot and return its JSON layout (points, y-up)."""
    lines = ['digraph G {', 'graph [splines=ortho, nodesep=0.8, ranksep=2.0, rankdir=LR];',
             f'node [shape=box, fixedsize=true, width={W / 72}, height={H / 72}];']
    lines += [f'"{e[0]}";' for e in entities]
    lines += [f'"{s}" -> "{d}" [id="r{i}", arrowhead=none];' for i, (s, d, _, _) in enumerate(relations)]
    lines.append('}')
    out = subprocess.run(["dot", "-Tjson"], input="\n".join(lines), capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


G = 10  # routing grid (px); lines keep 10 px apart


class Router:
    """Grid A* router (same rules as the v1 builder): lines are orthogonal, never cross an
    entity, never share a segment with another line, and each port on an entity edge is
    used by one line only. Crossing another line is allowed but costs extra, as do bends."""

    STEP = {"E": (G, 0, "h"), "W": (-G, 0, "h"), "S": (0, G, "v"), "N": (0, -G, "v")}
    AXIS = {"N": "v", "S": "v", "E": "h", "W": "h"}

    def __init__(self, boxes, maxx, maxy):
        self.boxes, self.maxx, self.maxy = boxes, maxx, maxy
        self.blocked = {(gx, gy) for x, y, w, h in boxes.values()
                        for gx in range(x - G, x + w + G + 1, G) for gy in range(y - G, y + h + G + 1, G)}
        self.used, self.ports_taken = {}, set()

    def ports(self, t):
        x, y, w, h = self.boxes[t]
        out = []
        for gx in range(x + 2 * G, x + w - 2 * G + 1, G):
            out += [((gx, y - 2 * G), ((gx - x) / w, 0), "N"), ((gx, y + h + 2 * G), ((gx - x) / w, 1), "S")]
        for gy in range(y + G, y + h - G + 1, G):
            out += [((x - 2 * G, gy), (0, (gy - y) / h), "W"), ((x + w + 2 * G, gy), (1, (gy - y) / h), "E")]
        return [p for p in out if p[0] not in self.ports_taken and not self.used.get(p[0])]

    def route(self, src, dst):
        goals = {p[0]: p for p in self.ports(dst)}
        tx, ty, tw, th = self.boxes[dst]
        hd = lambda p: (max(tx - p[0], 0, p[0] - tx - tw) + max(ty - p[1], 0, p[1] - ty - th)) / G
        heap, best, prev = [], {}, {}
        for pt, rel, d in self.ports(src):
            st = (pt, d)
            best[st], prev[st] = 0, None
            heapq.heappush(heap, (hd(pt), 0, st, rel))
        while heap:
            _, cost, st, rel0 = heapq.heappop(heap)
            if cost > best.get(st, 1e18):
                continue
            pt, d = st
            if pt in goals and self.STEP[d][:2] == tuple(-v for v in self.STEP[goals[pt][2]][:2]):
                path = [st]
                while prev[path[-1]] is not None:
                    path.append(prev[path[-1]])
                path = [q for q, _ in reversed(path)]
                self._take(path)
                return path, rel0, goals[pt][1]
            for nd, (dx, dy, ax) in self.STEP.items():
                if (dx, dy) == tuple(-v for v in self.STEP[d][:2]):
                    continue
                q = (pt[0] + dx, pt[1] + dy)
                if not (0 <= q[0] <= self.maxx and 0 <= q[1] <= self.maxy):
                    continue
                if (q in self.blocked and q not in goals) or q in self.ports_taken:
                    continue
                if ax in self.used.get(pt, ()) or ax in self.used.get(q, ()):
                    continue
                c = cost + 1 + (6 if nd != d else 0) + (20 if self.used.get(q) else 0)
                ns = (q, nd)
                if c < best.get(ns, 1e18):
                    best[ns], prev[ns] = c, st
                    heapq.heappush(heap, (c + hd(q), c, ns, rel0))
        raise SystemExit(f"no route {src} -> {dst}")

    def _take(self, path):
        for a, b in zip(path, path[1:]):
            ax = "h" if a[1] == b[1] else "v"
            self.used.setdefault(a, set()).add(ax)
            self.used.setdefault(b, set()).add(ax)
        self.ports_taken.update((path[0], path[-1]))


def bends(path):
    """End points plus every corner of a grid path."""
    return [p for i, p in enumerate(path) if i in (0, len(path) - 1)
            or (path[i - 1][0] == p[0]) != (p[0] == path[i + 1][0])]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("model", nargs="?", type=Path, default=DEFAULT_MODEL)
    ap.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args()

    model = load_model(args.model.resolve())
    entities, relations = list(model.ENT), list(model.REL)
    missing = sorted({r[3] for r in relations} - set(EN_LABELS))
    if missing:
        raise SystemExit(f"missing English labels: {missing}")

    g = layout(entities, relations)
    top = float(g["bb"].split(",")[3])
    tx = lambda x: round(float(x) + MARGIN)
    ty = lambda y: round(top - float(y) + MARGIN)

    snap = lambda v: int(round(v / (2 * G)) * 2 * G)
    nodes = [n for n in g["objects"] if "pos" in n]
    boxes = {}
    for n in nodes:
        x, y = n["pos"].split(",")
        boxes[n["name"]] = (snap(tx(x) - W / 2), snap(ty(y) - H / 2), W, H)
    maxx = max(x + w for x, _, w, _ in boxes.values()) + MARGIN
    maxy = max(y + h for _, y, _, h in boxes.values()) + MARGIN
    router = Router(boxes, maxx, maxy)

    cells = [f'<mxCell id="{t}" value="{t}" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;'
             f'strokeColor=#000000;fontSize=11;fontFamily=Arial;" vertex="1" parent="1">'
             f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
             for t, (x, y, w, h) in boxes.items()]

    # Short relations first: they get the straightest lines and nearest ports.
    def span(i):
        a, b = boxes[relations[i][0]], boxes[relations[i][1]]
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    for i in sorted(range(len(relations)), key=span):
        s, d, card, verb = relations[i]
        start, end = ENDS[card]
        path, (ex, ey), (nx, ny) = router.route(s, d)
        pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in bends(path))
        cells.append(f'<mxCell id="r{i}" value="{escape(EN_LABELS[verb])}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                     f'exitX={ex:.4f};exitY={ey:.4f};exitDx=0;exitDy=0;entryX={nx:.4f};entryY={ny:.4f};entryDx=0;entryDy=0;'
                     f'startArrow={start};endArrow={end};startFill=0;endFill=0;startSize=8;endSize=8;'
                     f'strokeColor=#000000;fontSize=9;fontFamily=Arial;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" '
                     f'source="{s}" target="{d}"><mxGeometry relative="1" as="geometry"><Array as="points">{pts}'
                     '</Array></mxGeometry></mxCell>')

    xml = ('<mxfile host="drawio"><diagram id="erd" name="Conceptual ERD"><mxGraphModel grid="1" gridSize="10" '
           'page="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) +
           '</root></mxGraphModel></diagram></mxfile>')
    args.output.write_text(xml, encoding="utf-8")
    print(f"{len(nodes)} entities, {len(relations)} relations -> {args.output}")


if __name__ == "__main__":
    main()

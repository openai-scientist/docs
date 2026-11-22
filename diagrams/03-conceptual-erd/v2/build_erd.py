"""Build the LOGOS conceptual ERD (v2) as one draw.io page in the v1 style.

Usage:
    python3 build_erd.py [MODEL.py] [OUTPUT.drawio]

Source of truth: LOGOS_Platform/visual/model.py (ENT, REL), all entities and
relations. Entities are grouped by module (graphviz dot inside each block); the grid router draws
orthogonal lines; this script converts them to draw.io cells with
white 160x40 boxes, black lines, Arial and Crow's Foot ends.
"""

from __future__ import annotations

import argparse
import heapq
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve()
DEFAULT_MODEL = ROOT.parents[4] / "capstone-projects" / "docs" / "LOGOS_Platform" / "visual" / "model.py"
DEFAULT_OUTPUT = ROOT.parent / "Entity-Relationship-Diagram-Conceptual.drawio"
W, H, MARGIN = 160, 40, 40
WIDE, WIDE_DEGREE = 240, 8   # entities with more relations get a wider box (more ports)

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


def width(name, relations):
    return WIDE if sum(name in r[:2] for r in relations) > WIDE_DEGREE else W


def layout(entities, relations, contexts) -> dict:
    """Group entities by module (M01..M12, CORE) in the dependency order of CONTEXTS.
    Each module is laid out on its own with graphviz dot (top-down, internal relations only);
    module blocks are then placed left to right, BLOCKS_PER_ROW per row, so the figure reads
    in a fixed order: identity and projects first, results and operations last."""
    order = [k for k, _ in sorted(contexts.items(), key=lambda kv: kv[1][2])] + ["CORE"]
    mod = {e[0]: e[1] for e in entities}
    blocks = []
    for m in order:
        names = [e[0] for e in entities if e[1] == m]
        if not names:
            continue
        lines = ['digraph G {', f'graph [nodesep={NODESEP}, ranksep={RANKSEP}, rankdir=TB];',
                 f'node [shape=box, fixedsize=true, width={W / 72}, height={H / 72}];']
        lines += [f'"{n}" [width={width(n, relations) / 72}];' for n in names]
        lines += [f'"{s}" -> "{d}";' for s, d, _, _ in relations if mod[s] == m and mod[d] == m]
        lines.append('}')
        out = json.loads(subprocess.run(["dot", "-Tjson"], input="\n".join(lines), capture_output=True,
                                        text=True, check=True).stdout)
        bw, bh = (float(v) for v in out["bb"].split(",")[2:])
        pos = {n["name"]: tuple(float(v) for v in n["pos"].split(",")) for n in out["objects"] if "pos" in n}
        blocks.append((bw, bh, {k: (x, bh - y) for k, (x, y) in pos.items()}))
    rows, x0 = [[]], 0.0
    for i, b in enumerate(blocks):
        wrap = x0 and x0 + b[0] > MAX_WIDTH if MAX_WIDTH else i and i % BLOCKS_PER_ROW == 0
        if wrap:
            rows.append([]); x0 = 0.0
        rows[-1].append(b); x0 += b[0] + BLOCK_GAP
    # with --max-width, spread each row's blocks over the full figure width and centre them
    # vertically in the row, so short or narrow blocks do not leave holes at the row's end
    full = max(sum(b[0] for b in r) + BLOCK_GAP * (len(r) - 1) for r in rows)
    placed, y0 = {}, 0.0
    for r in rows:
        rowh = max(b[1] for b in r)
        spare = full - sum(b[0] for b in r) - BLOCK_GAP * (len(r) - 1)
        step = BLOCK_GAP + (spare / (len(r) - 1) if MAX_WIDTH and len(r) > 1 else 0)
        x0 = spare / 2 if MAX_WIDTH and len(r) == 1 else 0.0
        for bw, bh, pos in r:
            dy = (rowh - bh) / 2 if MAX_WIDTH else 0.0
            for k, (x, y) in pos.items():
                placed[k] = (x0 + x, y0 + dy + y)
            x0 += bw + step
        y0 += rowh + BLOCK_GAP
    return placed


BLOCKS_PER_ROW, BLOCK_GAP = 4, 90
NODESEP, RANKSEP = 0.8, 0.95   # graphviz spacing inside a block (inches)
MAX_WIDTH = 0   # when set, blocks fill each row up to this width instead of a fixed count


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
        for gx in range(x + 2 * G, x + w - 2 * G + 1, 2 * G):
            out += [((gx, y - 2 * G), ((gx - x) / w, 0), "N"), ((gx, y + h + 2 * G), ((gx - x) / w, 1), "S")]
        for gy in range(y + G, y + h - G + 1, 2 * G):
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


def full_path(pts, ext, ent, a, b):
    """Polyline as drawn: box edge point, the routed bends, box edge point."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return [(ax + ext[0] * aw, ay + ext[1] * ah)] + list(pts) + [(bx + ent[0] * bw, by + ent[1] * bh)]


def label_size(text):
    return len(text) * 5.6 + 8, 14   # Arial 10 px, white background with a small margin


def hit(r, q):
    return r[0] < q[2] and q[0] < r[2] and r[1] < q[3] and q[1] < r[3]


def seg_rect(p, q, pad=0):
    return (min(p[0], q[0]) - pad, min(p[1], q[1]) - pad, max(p[0], q[0]) + pad, max(p[1], q[1]) + pad)


END_ZONE = 22   # last stretch of a line that holds the crow's foot


def place_labels(relations, routes, boxes):
    """Pick, for each relation, a spot on its own line where the label touches no entity,
    no other label, no other line and no crow's foot. Returns draw.io relative x (-1..1)."""
    polys = {i: full_path(p, e, n, boxes[relations[i][0]], boxes[relations[i][1]]) for i, (p, e, n) in routes.items()}
    segs = [(i, seg_rect(a, b)) for i, pl in polys.items() for a, b in zip(pl, pl[1:])]
    ends = [(i, seg_rect(pl[k], pl[k + 1 if k == 0 else k - 1], 7)) for i, pl in polys.items() for k in (0, len(pl) - 1)]
    taken, out = [], {}
    for i, pl in sorted(polys.items(), key=lambda kv: -len(EN_LABELS[relations[kv[0]][3]])):
        w, h = label_size(EN_LABELS[relations[i][3]])
        lens = [abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pl, pl[1:])]
        total = sum(lens) or 1
        best = None
        pos = 0
        for (a, b), ln in zip(zip(pl, pl[1:]), lens):
            for t in range(0, int(ln) + 1, 2):
                s_ = pos + t
                if s_ < END_ZONE + w / 2 * (a[1] == b[1]) or total - s_ < END_ZONE + w / 2 * (a[1] == b[1]):
                    continue
                f = t / ln if ln else 0
                cx, cy = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
                vertical = a[0] == b[0]
                # on the line first; beside it (4, 12 or 20 px gap) when the line has no room
                shifts = [(0, 0)] + [d for g in (4, 12, 20) for d in
                                     ([(-(w / 2 + g), 0), (w / 2 + g, 0)] if vertical else [(0, -(h / 2 + g)), (0, h / 2 + g)])]
                for k, (dx, dy) in enumerate(shifts):
                    r = (cx + dx - w / 2, cy + dy - h / 2, cx + dx + w / 2, cy + dy + h / 2)
                    bad = sum(hit(r, (x - 2, y - 2, x + bw + 2, y + bh + 2)) for x, y, bw, bh in boxes.values()) * 100
                    bad += sum(hit(r, q) for q in taken) * 100
                    bad += sum(hit(r, q) for j, q in segs if j != i) * 10
                    bad += sum(hit(r, q) for j, q in ends) * 10
                    score = (bad, k, abs(s_ - total / 2))
                    if best is None or score < best[0]:
                        best = (score, s_, r, (dx, dy))
            pos += ln
        if best is None:   # very short line: centre it
            best = ((0, 0, 0), total / 2, (0, 0, 0, 0), (0, 0))
        if best[0][0]:
            print(f"label clash: {EN_LABELS[relations[i][3]]} ({relations[i][0]} - {relations[i][1]})")
        taken.append(best[2])
        out[i] = (2 * best[1] / total - 1, best[3])
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("model", nargs="?", type=Path, default=DEFAULT_MODEL)
    ap.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--nodesep", type=float, default=NODESEP)
    ap.add_argument("--ranksep", type=float, default=RANKSEP)
    ap.add_argument("--gap", type=float, default=BLOCK_GAP, help="space between module blocks")
    ap.add_argument("--max-width", type=float, default=0, help="wrap blocks by row width (points)")
    ap.add_argument("--per-row", type=int, default=BLOCKS_PER_ROW,
                    help="module blocks per row (2 gives a portrait figure for the report)")
    args = ap.parse_args()
    globals()['BLOCKS_PER_ROW'] = args.per_row
    globals()['MAX_WIDTH'] = args.max_width
    globals().update(NODESEP=args.nodesep, RANKSEP=args.ranksep, BLOCK_GAP=args.gap)

    model = load_model(args.model.resolve())
    entities, relations = list(model.ENT), list(model.REL)
    missing = sorted({r[3] for r in relations} - set(EN_LABELS))
    if missing:
        raise SystemExit(f"missing English labels: {missing}")

    placed = layout(entities, relations, model.CONTEXTS)
    snap = lambda v: int(round(v / (2 * G)) * 2 * G)
    boxes = {k: (snap(x + MARGIN - width(k, relations) / 2), snap(y + MARGIN - H / 2), width(k, relations), H)
             for k, (x, y) in placed.items()}
    nodes = list(boxes)
    maxx = max(x + w for x, _, w, _ in boxes.values()) + MARGIN
    maxy = max(y + h for _, y, _, h in boxes.values()) + MARGIN
    router = Router(boxes, maxx, maxy)

    cells = [f'<mxCell id="{t}" value="{t}" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;'
             f'strokeColor=#000000;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">'
             f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
             for t, (x, y, w, h) in boxes.items()]

    # Short relations first: they get the straightest lines and nearest ports.
    def span(i):
        a, b = boxes[relations[i][0]], boxes[relations[i][1]]
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    routes = {}
    for i in sorted(range(len(relations)), key=span):
        path, ext, ent = router.route(relations[i][0], relations[i][1])
        routes[i] = (bends(path), ext, ent)
    labels = place_labels(relations, routes, boxes)
    for i, (pts_, (ex, ey), (nx, ny)) in routes.items():
        s, d, card, verb = relations[i]
        start, end = ENDS[card]
        pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts_)
        cells.append(f'<mxCell id="r{i}" value="{escape(EN_LABELS[verb])}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                     f'exitX={ex:.4f};exitY={ey:.4f};exitDx=0;exitDy=0;entryX={nx:.4f};entryY={ny:.4f};entryDx=0;entryDy=0;'
                     f'startArrow={start};endArrow={end};startFill=0;endFill=0;startSize=8;endSize=8;'
                     f'strokeColor=#000000;fontSize=10;fontFamily=Arial;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" '
                     f'source="{s}" target="{d}"><mxGeometry x="{labels[i][0]:.4f}" relative="1" as="geometry"><Array as="points">{pts}'
                     f'</Array><mxPoint x="{labels[i][1][0]:.1f}" y="{labels[i][1][1]:.1f}" as="offset"/></mxGeometry></mxCell>')

    xml = ('<mxfile host="drawio"><diagram id="erd" name="Conceptual ERD"><mxGraphModel grid="1" gridSize="10" '
           'page="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) +
           '</root></mxGraphModel></diagram></mxfile>')
    args.output.write_text(xml, encoding="utf-8")
    print(f"{len(nodes)} entities, {len(relations)} relations -> {args.output}")


if __name__ == "__main__":
    main()

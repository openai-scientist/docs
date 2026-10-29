#!/usr/bin/env python3
"""Build an editable conceptual ERD from the Platform's live SQLAlchemy metadata.

No database connection, application startup or environment file is needed. Geometry and
business descriptions live in platform_erd.json; relationship cardinalities come from code.
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parents[1]
DEFAULT_SOURCE = DOCS.parent / "capstone-projects/projects/logos"
OUTPUT = HERE / "AI-Research-Experimentation-Platform-ERD.drawio"
GRID = 10

METADATA_SCRIPT = '''
import inspect, json
import management.db.models_registry
from management.db.base import Base
from sqlalchemy import CheckConstraint, UniqueConstraint
models = {m.local_table.name: m.class_ for m in Base.registry.mappers}
result = {"entities": {}, "relationships": []}
for table in sorted(Base.metadata.tables.values(), key=lambda t: t.name):
    cls = models[table.name]
    path = inspect.getsourcefile(cls)
    result["entities"][table.name] = {
        "source": path[path.index("services/management/"):],
        "line": inspect.getsourcelines(cls)[1],
        "columns": [c.name for c in table.columns],
    }
    unique_sets = [{c.name for c in table.primary_key.columns}]
    unique_sets += [{c.name for c in u.columns} for u in table.constraints
                    if isinstance(u, UniqueConstraint)]
    unique_sets += [{c.name for c in ix.columns} for ix in table.indexes
                    if ix.unique and ix.dialect_options["postgresql"].get("where") is None
                    and ix.dialect_options["sqlite"].get("where") is None]
    result["entities"][table.name]["unique_sets"] = sorted([sorted(x) for x in unique_sets])
    result["entities"][table.name]["checks"] = sorted(str(c.sqltext) for c in table.constraints
                                                     if isinstance(c, CheckConstraint))
    for fk in sorted(table.foreign_keys, key=lambda f: f.parent.name):
        col = fk.parent
        result["relationships"].append({
            "key": table.name + "." + col.name,
            "parent": fk.column.table.name, "child": table.name,
            "column": col.name, "target_column": fk.column.name,
            "optional_parent": col.nullable,
            "single_child": bool(col.unique or {col.name} in unique_sets),
            "identifying": bool(col.primary_key),
        })
print(json.dumps(result, sort_keys=True))
'''


def metadata(source: Path) -> dict:
    python = source / ".venv/bin/python"
    if not python.is_file():
        raise SystemExit(f"Missing source workspace Python: {python}")
    import os

    env = os.environ.copy()
    env["PYTHONPATH"] = str(source / "services/management/src")
    run = subprocess.run([str(python), "-c", METADATA_SCRIPT], cwd=source,
                         env=env, capture_output=True, text=True, check=True)
    return json.loads(run.stdout)


def intersects(a, b, margin=0):
    return (a[0] < b[0] + b[2] + margin and a[0] + a[2] > b[0] - margin
            and a[1] < b[1] + b[3] + margin and a[1] + a[3] > b[1] - margin)


def simplify(points):
    result = []
    for p in points:
        if result and p == result[-1]:
            continue
        while len(result) > 1:
            a, b = result[-2:]
            if (a[0] == b[0] == p[0]) or (a[1] == b[1] == p[1]):
                result.pop()
            else:
                break
        result.append(p)
    return result


def ports(boxes, relations):
    requests = defaultdict(list)
    sides = {}
    normals = {"left": (-1, 0), "right": (1, 0), "top": (0, -1), "bottom": (0, 1)}
    for r in sorted(relations, key=lambda item: (item["layer"] != "core", item["key"])):
        for end, name, other in (("start", r["parent"], r["child"]),
                                 ("end", r["child"], r["parent"])):
            x, y, w, h = boxes[name]
            ox, oy, ow, oh = boxes[other]
            dx, dy = ox + ow / 2 - x - w / 2, oy + oh / 2 - y - h / 2
            if name == other:
                side = "right" if end == "start" else "top"
            elif abs(dx) > abs(dy) * 1.4:
                side = "right" if dx > 0 else "left"
            else:
                side = "bottom" if dy > 0 else "top"
            preferred = side
            # Spread high-degree entities across their perimeter so Crow's Foot markers
            # do not share an endpoint and appear to form a single ambiguous relationship.
            opposite = {"left": "right", "right": "left", "top": "bottom", "bottom": "top"}
            candidates = []
            for candidate in normals:
                length = w - 40 if candidate in ("top", "bottom") else h - 20
                capacity = max(1, int(length // 20))
                count = len(requests[(name, candidate)])
                if count >= capacity:
                    continue
                penalty = 0 if candidate == preferred else 200 if candidate == opposite[preferred] else 100
                candidates.append((penalty + count * 3, candidate))
            if not candidates:
                raise ValueError(f"Not enough marker space on {name}")
            side = min(candidates)[1]
            requests[(name, side)].append((r["key"], end, ox if side in ("top", "bottom") else oy))
    for (name, side), items in requests.items():
        x, y, w, h = boxes[name]
        items.sort(key=lambda i: (i[2], i[0], i[1]))
        for k, (key, end, _) in enumerate(items):
            fraction = (k + 1) / (len(items) + 1)
            if side in ("top", "bottom"):
                pos = (round((x + 20 + (w - 40) * fraction) / GRID) * GRID,
                       y if side == "top" else y + h)
            else:
                pos = (x if side == "left" else x + w,
                       round((y + 10 + (h - 20) * fraction) / GRID) * GRID)
            n = normals[side]
            outside = (pos[0] + n[0] * 30, pos[1] + n[1] * 30)
            sides[(key, end)] = (pos, outside, ((pos[0] - x) / w, (pos[1] - y) / h))
    return sides


def route_edges(model, boxes, relations):
    occupied, blocked = defaultdict(int), set()
    maxx, maxy = model["width"] // GRID, 198
    for x, y, w, h in boxes.values():
        for gx in range((x - 10) // GRID, (x + w + 10) // GRID + 1):
            for gy in range((y - 10) // GRID, (y + h + 10) // GRID + 1):
                blocked.add((gx, gy))
    anchors = ports(boxes, relations)
    # Route short structural edges first; hidden provenance never influences the visible page.
    def priority(r):
        a, b = boxes[r["parent"]], boxes[r["child"]]
        return (r["layer"] != "core", abs(a[0] - b[0]) + abs(a[1] - b[1]), r["key"])

    for r in sorted(relations, key=priority):
        src, start, source_port = anchors[(r["key"], "start")]
        dst, goal, target_port = anchors[(r["key"], "end")]
        start, goal = (start[0] // GRID, start[1] // GRID), (goal[0] // GRID, goal[1] // GRID)
        initial = (start[0], start[1], -1)
        queue, best, came = [(0, 0, initial)], {initial: 0}, {}
        finish = None
        while queue:
            _, cost, state = heapq.heappop(queue)
            x, y, direction = state
            if cost != best.get(state):
                continue
            if (x, y) == goal:
                finish = state
                break
            for nd, (dx, dy) in enumerate(((1, 0), (0, 1), (-1, 0), (0, -1))):
                nx, ny = x + dx, y + dy
                if not (2 <= nx <= maxx - 2 and 9 <= ny <= maxy):
                    continue
                if (nx, ny) in blocked:
                    continue
                edge_key = tuple(sorted(((x, y), (nx, ny))))
                reuse = occupied[edge_key] if r["layer"] == "core" else 0
                new_cost = cost + 10 + (45 if direction >= 0 and nd != direction else 0) + reuse * 75
                ns = (nx, ny, nd)
                if new_cost < best.get(ns, math.inf):
                    best[ns], came[ns] = new_cost, state
                    heuristic = (abs(nx - goal[0]) + abs(ny - goal[1])) * 10
                    heapq.heappush(queue, (new_cost + heuristic, new_cost, ns))
        if finish is None:
            raise ValueError(f"No route for {r['key']}")
        path, state = [], finish
        while True:
            path.append((state[0] * GRID, state[1] * GRID))
            if state == initial:
                break
            state = came[state]
        path.reverse()
        if r["layer"] == "core":
            for a, b in zip(path, path[1:]):
                occupied[tuple(sorted(((a[0] // GRID, a[1] // GRID),
                                       (b[0] // GRID, b[1] // GRID))))] += 1
        r.update(points=simplify([src, *path, dst]), source_port=source_port, target_port=target_port)


def label_position(r, boxes, labels, marker_boxes):
    points, width, height = r["points"], max(54, len(r["label"]) * 7 + 10), 20
    segments = [(a, b, abs(a[0] - b[0]) + abs(a[1] - b[1])) for a, b in zip(points, points[1:])]
    total = sum(s[2] for s in segments)
    candidates, travelled = [], 0
    for a, b, length in segments:
        for f in (0.5, 0.33, 0.67, 0.2, 0.8):
            cx, cy = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            offsets = ((0, 0), (0, -24), (0, 24)) if a[1] == b[1] else ((0, 0), (-(width / 2 + 12), 0), ((width / 2 + 12), 0))
            for dx, dy in offsets:
                rect = (cx + dx - width / 2, cy + dy - height / 2, width, height)
                if any(intersects(rect, box, 10) for box in boxes.values()):
                    continue
                if any(intersects(rect, marker) for marker in marker_boxes):
                    continue
                overlap = sum(intersects(rect, old, 8) for old in labels)
                score = overlap * 10000 + (0 if a[1] == b[1] else 500) - min(length, width + 20)
                score += 40 if dx or dy else 0
                if length < (width + 20 if a[1] == b[1] else 50):
                    score += 1000
                candidates.append((score, travelled + length * f, rect, (dx, dy)))
        travelled += length
    if not candidates:
        raise ValueError(f"No label space: {r['key']}")
    _, distance, rect, offset = min(candidates)
    labels.append(rect)
    return 2 * distance / total - 1, rect, offset


def vertex(root, key, value, box, style, parent="1", **extra):
    cell = ET.SubElement(root, "mxCell", id=key, value=value, vertex="1", parent=parent,
                         style=style, **extra)
    x, y, w, h = box
    ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})
    return cell


def build(model, schema):
    entities = {e["name"]: e for e in model["entities"]}
    if set(entities) != set(schema["entities"]):
        raise ValueError(f"Model/source entity mismatch: {set(entities) ^ set(schema['entities'])}")
    names = model["entity_names"]
    assert set(names) == set(entities), "Missing entity/table naming mapping"
    assert len(set(names.values())) == len(names), "Entity display names must be unique"
    assert all(re.fullmatch(r"[A-Z][A-Za-z0-9]*", value) for value in names.values()), "Use explicit PascalCase noun names"
    schema["entity_names"] = names
    w, h = model["entity_width"], model["entity_height"]
    boxes = {name: (e["x"], e["y"], w, h) for name, e in entities.items()}
    relations = schema["relationships"]
    for r in relations:
        if override := model.get("cardinality_overrides", {}).get(r["key"]):
            entity = schema["entities"][r["child"]]
            assert override["requires_check"] in entity["checks"], f"Missing CHECK for {r['key']}"
            assert sorted(override["requires_unique"]) in entity["unique_sets"], f"Missing unique key for {r['key']}"
            r["single_child"] = override["single_child"]
        hidden = r["column"] in model["provenance_columns"] and r["key"] not in model["core_overrides"]
        r["layer"] = "provenance" if hidden else "core"
        r["label"] = model["relationship_labels"].get(r["key"], "last updates" if r["column"] == "updated_by_user_id" else "creates")
    route_edges(model, boxes, relations)
    mxfile = ET.Element("mxfile", host="app.diagrams.net", type="device", version="31.5.3")
    diagram = ET.SubElement(mxfile, "diagram", id="platform-conceptual-erd", name="Report 3.1.5 ERD",
                            **{"data-source": "logos/services/management SQLAlchemy metadata; Alembic head 20261022_0048",
                               "data-level": "Entity-relationship overview derived from the implemented schema; attributes suppressed",
                               "data-notation": "Crow's Foot (IE variant): solid identifying, dashed non-identifying; endpoint markers show min/max"})
    graph = ET.SubElement(diagram, "mxGraphModel", grid="1", gridSize="10", page="1", pageScale="1",
                         pageWidth=str(model["width"]), pageHeight=str(model["height"]),
                         background="#ffffff", math="0", shadow="0", tooltips="1")
    root = ET.SubElement(graph, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0", value="Entities and core relationships")
    ET.SubElement(root, "mxCell", id="2", parent="0", value="Technical provenance relationships", visible="0")
    text_style = "text;html=0;align=center;verticalAlign=middle;fontFamily=Helvetica;fontColor=#000000;strokeColor=none;fillColor=none;"
    vertex(root, "title", model["title"] + " — " + model["subtitle"], (0, 18, model["width"], 38), text_style + "fontSize=26;fontStyle=1;")
    node_style = "rounded=0;whiteSpace=wrap;html=0;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.5;fontColor=#000000;fontFamily=Helvetica;fontSize=20;spacing=7;"
    for name, box in boxes.items():
        source = schema["entities"][name]
        vertex(root, name, names[name], box, node_style, **{"data-table": name,
               "data-source": f"{source['source']}:{source['line']}", "data-description": entities[name]["description"]})
    labels = []
    marker_boxes = [(x - 28, y - 28, 56, 56) for r in relations if r["layer"] == "core"
                    for x, y in (r["points"][0], r["points"][-1])]
    for r in sorted(relations, key=lambda r: (r["layer"] != "core", r["key"])):
        key = "rel_" + r["key"].replace(".", "_")
        start = "ERzeroToOne" if r["optional_parent"] else "ERmandOne"
        end = "ERzeroToOne" if r["single_child"] else "ERzeroToMany"
        sx, sy = r["source_port"]
        tx, ty = r["target_port"]
        style = ("edgeStyle=none;rounded=0;html=0;strokeColor=#000000;strokeWidth=1.3;"
                 "fontFamily=Helvetica;fontSize=14;fontColor=#000000;labelBackgroundColor=#ffffff;"
                 f"startArrow={start};startFill=0;startSize=14;endArrow={end};endFill=0;endSize=14;"
                 "jumpStyle=arc;jumpSize=8;"
                 f"exitX={sx};exitY={sy};entryX={tx};entryY={ty};exitPerimeter=0;entryPerimeter=0;")
        style += "dashed=0;" if r["identifying"] else "dashed=1;dashPattern=8 5;"
        if r["layer"] == "provenance":
            style += "strokeColor=#777777;fontColor=#555555;"
        cell = ET.SubElement(root, "mxCell", id=key, value=r["label"], edge="1",
                             parent="1" if r["layer"] == "core" else "2", source=r["parent"], target=r["child"],
                             style=style, **{"data-fk": r["key"], "data-target-column": r["target_column"],
                                             "data-identifying": str(r["identifying"]).lower(),
                                             "data-route": json.dumps(r["points"]),
                                             "data-cardinality": ("0..1" if r["optional_parent"] else "1") + ":" + ("0..1" if r["single_child"] else "0..*")})
        own_markers = [(x - 28, y - 28, 56, 56) for x, y in (r["points"][0], r["points"][-1])]
        lx, rect, offset = label_position(r, boxes, labels if r["layer"] == "core" else [], marker_boxes + own_markers)
        cell.set("data-label-box", json.dumps(rect))
        geom = ET.SubElement(cell, "mxGeometry", relative="1", x=str(round(lx, 6)), y="0", **{"as": "geometry"})
        ET.SubElement(geom, "mxPoint", x=str(offset[0]), y=str(offset[1]), **{"as": "offset"})
        array = ET.SubElement(geom, "Array", **{"as": "points"})
        for x, y in r["points"][1:-1]:
            ET.SubElement(array, "mxPoint", x=str(x), y=str(y))
    visible = sum(r["layer"] == "core" for r in relations)
    legend = (f"{len(entities)} entities | {visible} core relationships | {len(relations) - visible} technical provenance relationships in hidden layer\n"
              "Crow's Foot: || exactly one; o| zero or one; o< zero or many. Read each verb from parent to child.\n"
              "IE convention: solid = identifying (parent key is part of child primary key); dashed = non-identifying.\n"
              "Standalone telemetry and ledger records have no declared foreign keys; no relationship is invented from context IDs.")
    vertex(root, "legend", legend, (90, 2250, model["width"] - 180, 110), text_style + "fontSize=17;whiteSpace=wrap;")
    ET.indent(mxfile, space="  ")
    return ET.tostring(mxfile, encoding="utf-8", xml_declaration=True) + b"\n"


def validate(data, schema):
    root = ET.fromstring(data)
    cells = root.findall(".//mxCell")
    entities = {c.attrib["id"]: c for c in cells if "data-description" in c.attrib}
    edges = [c for c in cells if c.get("edge") == "1"]
    assert set(entities) == set(schema["entities"]), "Entity coverage mismatch"
    assert all(c.get("data-table") == key and c.get("value") == schema["entity_names"][key]
               for key, c in entities.items()), "Entity/table naming mismatch"
    assert {c.attrib["data-fk"] for c in edges} == {r["key"] for r in schema["relationships"]}, "FK coverage mismatch"
    # These are semantic consequences of CHECK + UNIQUE/PK, not of a single FK index.
    constrained = {e.get("data-fk"): e for e in edges}
    for key in ("email_otps.user_id", "platform_settings.updated_by_user_id"):
        assert "endArrow=ERzeroToOne;" in constrained[key].get("style"), f"Singleton constraint lost: {key}"
    boxes = {}
    for name, cell in entities.items():
        g = cell.find("mxGeometry")
        boxes[name] = tuple(float(g.attrib[k]) for k in ("x", "y", "width", "height"))
    for name, a in boxes.items():
        for other, b in boxes.items():
            if name < other:
                assert not intersects(a, b), f"Entities overlap: {name}, {other}"
    for edge in edges:
        relationship = next(r for r in schema["relationships"] if r["key"] == edge.get("data-fk"))
        expected_start = "ERzeroToOne" if relationship["optional_parent"] else "ERmandOne"
        expected_end = "ERzeroToOne" if relationship["single_child"] else "ERzeroToMany"
        assert f"startArrow={expected_start};" in edge.get("style"), "Incorrect parent cardinality"
        assert f"endArrow={expected_end};" in edge.get("style"), "Incorrect child cardinality"
        assert edge.get("source") == relationship["parent"] and edge.get("target") == relationship["child"]
        identifying = relationship["identifying"]
        assert edge.get("data-identifying") == str(identifying).lower(), "Incorrect identity dependency"
        assert f"dashed={0 if identifying else 1};" in edge.get("style"), "Incorrect identifying/non-identifying stroke"
        points = json.loads(edge.attrib["data-route"])
        for a, b in zip(points, points[1:]):
            assert a[0] == b[0] or a[1] == b[1], f"Non-orthogonal: {edge.get('data-fk')}"
            for name, box in boxes.items():
                # Strict interior intersection: terminal stubs may touch the entity border.
                x, y, w, h = box
                if a[0] == b[0]:
                    hit = x < a[0] < x + w and max(min(a[1], b[1]), y) < min(max(a[1], b[1]), y + h)
                else:
                    hit = y < a[1] < y + h and max(min(a[0], b[0]), x) < min(max(a[0], b[0]), x + w)
                assert not hit, f"Edge crosses entity: {edge.get('data-fk')} -> {name}"
    terminals = defaultdict(list)
    for edge in edges:
        points = json.loads(edge.attrib["data-route"])
        terminals[(edge.get("source"), tuple(points[0]))].append(edge.get("data-fk"))
        terminals[(edge.get("target"), tuple(points[-1]))].append(edge.get("data-fk"))
    assert all(len(items) == 1 for items in terminals.values()), "Ambiguous shared entity port"
    label_boxes = []
    marker_boxes = [(x - 28, y - 28, 56, 56) for e in edges if e.get("parent") == "1"
                    for x, y in (json.loads(e.attrib["data-route"])[0], json.loads(e.attrib["data-route"])[-1])]
    for edge in edges:
        rect = json.loads(edge.attrib["data-label-box"])
        assert not any(intersects(rect, b) for b in boxes.values()), "Relationship label overlaps entity"
        if edge.get("parent") == "1":
            assert not any(intersects(rect, old) for old in label_boxes), "Core relationship labels overlap"
            assert not any(intersects(rect, marker) for marker in marker_boxes), "Core relationship label overlaps cardinality marker"
            label_boxes.append(rect)
    n_identifying = sum(r["identifying"] for r in schema["relationships"])
    print(f"PASS entities={len(entities)} unique_names={len(entities)} foreign_keys={len(edges)} identifying={n_identifying} cardinalities=source entity_overlaps=0 edge_entity_intersections=0 duplicate_ports=0 core_label_overlaps=0")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true", help="Validate source, geometry and byte-for-byte rebuild without writing")
    args = parser.parse_args()
    model = json.loads((HERE / "platform_erd.json").read_text())
    schema = metadata(args.source_root.resolve())
    data = build(model, schema)
    validate(data, schema)
    if args.check:
        assert args.output.read_bytes() == data, "Draw.io artifact is stale; rebuild it"
        print("PASS deterministic rebuild")
    else:
        args.output.write_bytes(data)
        print(args.output)


if __name__ == "__main__":
    main()

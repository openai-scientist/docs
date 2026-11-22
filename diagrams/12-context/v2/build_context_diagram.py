"""Build Context Diagram v2 from the v1 main-2 geometry and source flows.

The v1 context page is the visual baseline. This builder keeps its ellipse,
rectangle sizes, placements, orthogonal routing and source-backed exchanges,
then applies only the product-scope and role-name corrections required by the
current handoff.
"""

from __future__ import annotations

import html
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path


HERE = Path(__file__).resolve().parent
LEGACY_DIR = HERE.parent
SCOPE_PATH = LEGACY_DIR / "functional_scope.json"
DEFAULT_OUTPUT = HERE / "System-Context-Diagram.drawio"

BASE_STYLE = (
    "html=1;whiteSpace=wrap;fontFamily=Arial;fontColor=#111827;"
    "strokeColor=#111827;fillColor=#FFFFFF;"
)
EDGE_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#111827;"
    "strokeWidth=1.4;endArrow=classic;endFill=1;endSize=9;fontFamily=Arial;"
    "fontSize=18;align=center;verticalAlign=middle;labelBackgroundColor=#FFFFFF;spacing=2;"
)

X, Y, W, H = 1290, 640, 960, 720
CX, CY = X + W / 2, Y + H / 2


def ellipse_y(x: float, bottom: bool = True) -> float:
    dy = H / 2 * math.sqrt(max(0.0, 1.0 - ((x - CX) / (W / 2)) ** 2))
    return CY + dy if bottom else CY - dy


def ellipse_x(y: float, right: bool = False) -> float:
    dx = W / 2 * math.sqrt(max(0.0, 1.0 - ((y - CY) / (H / 2)) ** 2))
    return CX + dx if right else CX - dx


def add_box(
    root: ET.Element,
    key: str,
    label: str,
    x: int,
    y: int,
    width: int,
    height: int,
    style: str,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        id=key,
        value=label,
        parent="1",
        vertex="1",
        style=BASE_STYLE + style,
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        x=str(x),
        y=str(y),
        width=str(width),
        height=str(height),
        attrib={"as": "geometry"},
    )


def normalize_flow(flow: dict) -> dict:
    """Correct only the v1 Platform Admin split required by the target roles."""
    normalized = dict(flow)
    actor = normalized["actor"]
    label = normalized["label"]
    if actor == "Platform Admin":
        if label == "Platform settings and default resource limits":
            normalized["actor"] = "Tenant Admin"
            normalized["label"] = "Tenant settings and default resource limits"
        elif label == "Resource usage reports":
            normalized["actor"] = "Tenant Admin"
            normalized["label"] = "Tenant usage and cost reports"
        else:
            normalized["actor"] = "Platform Operator"
    return normalized


def load_groups() -> dict[str, list[dict]]:
    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    actor_order = [
        "Project Manager",
        "Researcher",
        "AI / LLM Provider",
        "Local Node",
        "Reviewer",
        "Literature & Evidence Sources",
        "External Data Sources",
        "Platform Operator",
        "Tenant Admin",
    ]
    groups = {actor: [] for actor in actor_order}
    excluded = set(scope["display_excluded_source_ids"])
    source_flows = [
        flow
        for flow in scope["compact_flows"]
        if not excluded.intersection(flow["source_ids"])
    ]
    source_flows.extend(
        dict(flow, id=flow.get("id", f"support-{index}"))
        for index, flow in enumerate(scope["extra_flows"])
    )
    for source_flow in source_flows:
        flow = normalize_flow(source_flow)
        groups[flow["actor"]].append(flow)

    # Keep the v1 Local Node direction correction.
    for flow in groups["Local Node"]:
        flow["direction"] = "in" if flow["id"] == "FE-12.2" else "out"
    for flows in groups.values():
        flows.sort(key=lambda flow: flow["direction"] == "out")
    return groups


def add_flow(
    root: ET.Element,
    flow: dict,
    actor_key: str,
    source: str,
    target: str,
    route: list[tuple[float, float]],
    actor_port: tuple[float, float],
    system_port: tuple[float, float],
    label_segment: int = 0,
) -> None:
    outgoing = flow["direction"] == "out"
    actor_style = f"exitX={actor_port[0]};exitY={actor_port[1]};exitPerimeter=0;"
    system_style = f"entryX={system_port[0]};entryY={system_port[1]};entryPerimeter=0;"
    if outgoing:
        actor_style = actor_style.replace("exit", "entry")
        system_style = system_style.replace("entry", "exit")
    cell = ET.SubElement(
        root,
        "mxCell",
        id=f"flow-{flow['id']}",
        parent="1",
        edge="1",
        source=source,
        target=target,
        value=html.escape(flow["label"]),
        style=EDGE_STYLE + actor_style + system_style,
    )
    lengths = [
        abs(x2 - x1) + abs(y2 - y1)
        for (x1, y1), (x2, y2) in zip(route, route[1:])
    ]
    fraction = (sum(lengths[:label_segment]) + lengths[label_segment] / 2) / sum(lengths)
    if outgoing:
        fraction = 1 - fraction
    geometry = ET.SubElement(
        cell,
        "mxGeometry",
        relative="1",
        x=str(2 * fraction - 1),
        y="0",
        attrib={"as": "geometry"},
    )
    points = list(route[1:-1])
    if outgoing:
        points.reverse()
    array = ET.SubElement(geometry, "Array", attrib={"as": "points"})
    for point_x, point_y in points:
        ET.SubElement(array, "mxPoint", x=str(point_x), y=str(point_y))
    cell.set("data-fe", ",".join(flow.get("source_ids", [flow["id"]])))
    cell.set("data-source-text", flow.get("text", flow["label"]))
    cell.set("data-wbs", flow.get("wbs", ""))


def build(output: Path) -> None:
    groups = load_groups()
    root = ET.Element("root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    # Exact v1 main-2 system geometry and typography, with corrected scope.
    add_box(
        root,
        "platform",
        "<b>AI Research Experimentation Platform</b>",
        X,
        Y,
        W,
        H,
        "ellipse;fontSize=28;align=center;verticalAlign=middle;strokeWidth=2.4;",
    )

    placements = {
        "Project Manager": (400, 300, 320, 300),
        "Researcher": (50, 990, 320, 260),
        "AI / LLM Provider": (2700, 1660, 340, 230),
        "Local Node": (500, 1680, 340, 170),
        "Reviewer": (2800, 360, 340, 240),
        "Literature & Evidence Sources": (2850, 740, 370, 180),
        "External Data Sources": (2970, 960, 330, 220),
        "Platform Operator": (2580, 1290, 340, 240),
        "Tenant Admin": (50, 50, 320, 190),
    }
    display_names = {
        "Researcher": "Researcher (student)",
        "AI / LLM Provider": "AI Model Providers",
        "Literature & Evidence Sources": "Literature & Evidence Services",
    }
    for index, actor in enumerate(groups):
        ax, ay, aw, ah = placements[actor]
        add_box(
            root,
            f"actor-{index}",
            html.escape(display_names.get(actor, actor)),
            ax,
            ay,
            aw,
            ah,
            "fontSize=23;fontStyle=1;align=center;verticalAlign=middle;strokeWidth=1.5;",
        )

    for index, (actor, flows) in enumerate(groups.items()):
        ax, ay, aw, ah = placements[actor]
        actor_key = f"actor-{index}"
        input_count = sum(flow["direction"] == "in" for flow in flows)
        middle_count = (len(flows) - input_count + 1) // 2
        for flow_index, flow in enumerate(flows):
            t = (flow_index + 0.5 + (0.6 if flow_index >= input_count else 0)) / (
                len(flows) + 0.6
            )
            label_segment = 0
            if actor == "Project Manager":
                yy = ay + ah * t
                sx = 1740 - 30 * flow_index
                sy = ellipse_y(sx, False)
                route = [(ax + aw, yy), (sx, yy), (sx, sy)]
                actor_port = (1, t)
                system_port = ((sx - X) / W, (sy - Y) / H)
            elif actor == "Reviewer":
                yy = ay + ah * t
                sx = 1830 + 30 * flow_index
                sy = ellipse_y(sx, False)
                route = [(ax, yy), (sx, yy), (sx, sy)]
                actor_port = (0, t)
                system_port = ((sx - X) / W, (sy - Y) / H)
            elif actor == "Researcher":
                if flow_index < input_count:
                    yy = 690 + flow_index * 34
                    apx = ax + 35 + flow_index * (aw - 70) / max(input_count - 1, 1)
                    sx = ellipse_x(yy)
                    sy = yy
                    route = [(apx, ay), (apx, yy), (sx, yy)]
                    actor_port = ((apx - ax) / aw, 0)
                    system_port = ((sx - X) / W, (sy - Y) / H)
                    label_segment = 1
                elif flow_index < input_count + middle_count:
                    relative_index = flow_index - input_count
                    yy = 1000 + relative_index * 27
                    sx = ellipse_x(yy)
                    sy = yy
                    route = [(ax + aw, yy), (sx, yy)]
                    actor_port = (1, (yy - ay) / ah)
                    system_port = ((sx - X) / W, (sy - Y) / H)
                else:
                    relative_index = flow_index - input_count - middle_count
                    count = len(flows) - input_count - middle_count
                    yy = 1310 + relative_index * 30
                    apx = ax + aw - 35 - relative_index * (aw - 70) / max(count - 1, 1)
                    sx = 1480 + relative_index * 28
                    sy = ellipse_y(sx)
                    route = [(apx, ay + ah), (apx, yy), (sx, yy), (sx, sy)]
                    actor_port = ((apx - ax) / aw, 1)
                    system_port = ((sx - X) / W, (sy - Y) / H)
                    label_segment = 1
            elif actor in ("Literature & Evidence Sources", "External Data Sources"):
                yy = ay + ah * (0.1 + 0.8 * t)
                sx = ellipse_x(yy, True)
                sy = yy
                route = [(ax, yy), (sx, yy)]
                actor_port = (0, (yy - ay) / ah)
                system_port = ((sx - X) / W, (sy - Y) / H)
            elif actor == "AI / LLM Provider":
                yy = ay + ah * (0.08 + 0.84 * t)
                sx = 2012 - flow_index * 28
                sy = ellipse_y(sx)
                route = [(ax, yy), (sx, yy), (sx, sy)]
                actor_port = (0, (yy - ay) / ah)
                system_port = ((sx - X) / W, (sy - Y) / H)
            elif actor == "Local Node":
                yy = ay + ah * (0.15 + 0.7 * t)
                sx = 1760 + flow_index * 28
                sy = ellipse_y(sx)
                route = [(ax + aw, yy), (sx, yy), (sx, sy)]
                actor_port = (1, (yy - ay) / ah)
                system_port = ((sx - X) / W, (sy - Y) / H)
            elif actor == "Tenant Admin":
                # straight lane above Project Manager, entering the ellipse top between
                # the Project Manager and Reviewer bundles so no route is crossed
                yy = 110 if flow["direction"] == "in" else 170
                sx = 1800 if flow["direction"] == "in" else 1770
                sy = ellipse_y(sx, False)
                route = [(ax + aw, yy), (sx, yy), (sx, sy)]
                actor_port = (1, (yy - ay) / ah)
                system_port = ((sx - X) / W, (sy - Y) / H)
            else:
                yy = ay + ah * (0.03 + 0.94 * t)
                sx = 2180 - flow_index * 28
                sy = ellipse_y(sx)
                route = [(ax, yy), (sx, yy), (sx, sy)]
                actor_port = (0, (yy - ay) / ah)
                system_port = ((sx - X) / W, (sy - Y) / H)

            outgoing = flow["direction"] == "out"
            add_flow(
                root,
                flow,
                actor_key,
                "platform" if outgoing else actor_key,
                actor_key if outgoing else "platform",
                route,
                actor_port,
                system_port,
                label_segment,
            )

    mxfile = ET.Element("mxfile", host="Electron", agent="Codex drawio-skill", pages="1")
    diagram = ET.SubElement(
        mxfile,
        "diagram",
        id="context-v2",
        name="main-2",
        **{
            "data-source": "v1 main-2 geometry + functional_scope.json; LOGOS_Platform role and product-scope correction",
            "data-model": "Whole-product context: FE, Platform API/backend, Scientific Core/LOGOS and external contexts.",
        },
    )
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        dx="2151",
        dy="1269",
        grid="1",
        gridSize="10",
        guides="1",
        tooltips="1",
        connect="1",
        arrows="1",
        fold="1",
        page="0",
        pageScale="1",
        pageWidth="1900",
        pageHeight="1300",
        background="#ffffff",
        math="0",
        shadow="0",
    )
    model.append(root)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(mxfile).write(output, encoding="utf-8", xml_declaration=True)
    flow_count = sum(len(flows) for flows in groups.values())
    print(f"generated {output}")
    print("baseline: v1 main-2 geometry, typography, routing and monochrome grammar")
    print(f"scope: whole product FE -> Platform API -> Scientific Core / LOGOS; flows: {flow_count}")
    print("nodes: 1 platform, 9 participants; canvas title: none; page: one")


if __name__ == "__main__":
    build(DEFAULT_OUTPUT)

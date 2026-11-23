"""Build the editable System Architecture Diagram v2 of LOGOS (Report 7, IV 1.1.1, Figure IV-1).

v2 keeps the v1 card style on a left-to-right layout and corrects the content against the code:
logos/deploy/docker-compose.prod.yml, ai-research-platform-fe/docker/docker-compose.prod.yml,
logos/services/runner (the Local Node runner polls the Platform API) and the five LOGOS roles.

Source: deliverables/FA26SE115_Report7.docx, IV 1.1.1 (diagram text, actor and
external system tables), 1.1.2 (deployment nodes) and 1.5 (delivery pipeline).
Icons: Simple Icons (CC0) and Dashboard Icons (Dokploy, kept in its own colours) for brands, Tabler Icons (MIT) for generic symbols,
stored in ./icons and embedded in the .drawio so the file stays self-contained.
Run: python3 build_system_architecture.py
"""
from base64 import b64encode
from html import escape
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
OUT = HERE / "System-Architecture-Diagram.drawio"
FONT = "fontFamily=Arial;fontColor=#000000;"
INK, GREY = "#000000", "#4D4D4D"
# AWS Architecture Icons group palette: white groups with a coloured border and matching title.
AWS = {"cloud": "#232F3E", "public": "#7AA116", "private": "#00A4A6", "ai": "#8C4FFF", "generic": "#7D8998"}
CARD_LINE, LINE = "#B6BEC9", "#545B64"

cells, ids = [], {}


def icon_uri(name, color):
    """Read an SVG icon, set its colour and return a draw.io data URI."""
    svg = (HERE.parent / "icons" / f"{name}.svg").read_text()
    if name.startswith("tb-"):
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    elif name.startswith("si-"):
        svg = re.sub(r"<svg ", f'<svg fill="{color}" ', svg, count=1)
    return "data:image/svg+xml," + b64encode(svg.encode()).decode()


def add(cid, value, style, x, y, w, h):
    cells.append(f'<mxCell id="{cid}" value="{escape(value)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    ids[cid] = (x, y, w, h)


def group(cid, title, x, y, w, h, fill="#FFFFFF", dashed=False, color=None):
    """Group in AWS style: white fill, coloured border, title in the same colour at the top left."""
    color = color or AWS["generic"]
    add(cid, f"<b>{title}</b>",
        f"rounded=0;html=1;whiteSpace=wrap;{FONT}fontColor={color};fontSize=15;fillColor={fill};"
        f"strokeColor={color};strokeWidth=1.5;dashed={1 if dashed else 0};verticalAlign=top;align=left;"
        "spacingLeft=12;spacingTop=6;container=0;", x, y, w, h)


def tier(text, x, y, w=300):
    add(f"t{len(cells)}", text, f"text;html=1;{FONT}fontSize=11;fontStyle=1;fontColor={GREY};align=left;verticalAlign=middle;",
        x, y, w, 20)


def node(cid, name, kind, desc, ico, color, x, y, w, h=72, fill="#FFFFFF", dashed=False):
    """Card with an icon on the left: name, [type: technology] and one line of description."""
    label = f"<b style='font-size:16px'>{name}</b><br><span style='font-size:13px'>{desc}</span>"
    add(cid, label,
        f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=11;fillColor={fill};strokeColor={CARD_LINE};"
        f"strokeWidth=1;dashed={1 if dashed else 0};align=left;verticalAlign=middle;spacingLeft=56;spacingRight=6;",
        x, y, w, h)
    add(cid + "_i", "", f"shape=image;html=1;imageAspect=1;aspect=fixed;image={icon_uri(ico, color)};",
        x + 12, y + h / 2 - 16, 32, 32)


def edge(src, tgt, label="", pts=(), sx=None, sy=None, tx=None, ty=None, dashed=False, lx=0):
    style = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;{FONT}fontSize=13;strokeColor={LINE};strokeWidth=1.25;"
             f"endArrow=block;endFill=1;labelBackgroundColor=#FFFFFF;dashed={1 if dashed else 0};")
    for k, v in (("exitX", sx), ("exitY", sy), ("entryX", tx), ("entryY", ty)):
        if v is not None:
            style += f"{k}={v};"
    if sx is not None or sy is not None:
        style += "exitDx=0;exitDy=0;"
    if tx is not None or ty is not None:
        style += "entryDx=0;entryDy=0;"
    geo = "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in pts)
    geo = f'<Array as="points">{geo}</Array>' if geo else ""
    cells.append(f'<mxCell id="e{len(cells)}" value="{escape(label.replace(chr(10), "<br>"))}" style="{style}" edge="1" parent="1" '
                 f'source="{src}" target="{tgt}"><mxGeometry x="{lx}" relative="1" as="geometry">{geo}</mxGeometry></mxCell>')


# Layout reads left to right along the request path: users -> browser -> Cloudflare -> Traefik
# -> Web App / Platform API; data sits under the API, the AI research tier at the bottom,
# external services on the right with one straight lane per flow.
H = 80
group("g_vps", "OpenAI-Scientist on a Linux VPS", 860, 90, 1070, 990, color=AWS["cloud"])
group("g_ext", "External services", 1970, 90, 310, 990, dashed=True)

roles = ["Researcher (student)", "Project Manager", "Reviewer", "Tenant Admin", "Platform Operator"]
add("users", "<b style='font-size:16px'>Users</b><br><span style='font-size:13px'>" + "<br>".join(roles) + "</span>",
    f"rounded=1;arcSize=6;html=1;whiteSpace=wrap;{FONT}fontSize=13;fillColor=#FFFFFF;strokeColor={CARD_LINE};"
    "align=left;verticalAlign=middle;spacingLeft=56;", 500, 70, 260, 180)
add("users_i", "", f"shape=image;html=1;imageAspect=1;aspect=fixed;image={icon_uri('tb-user', INK)};", 512, 144, 32, 32)
node("browser", "Web browser", "", "Opens the app", "tb-world-www", INK, 500, 280, 260, H)
node("cf", "Cloudflare", "", "DNS, HTTPS, proxy", "si-cloudflare", "#F38020", 500, 410, 260, H)
node("local", "Local Node", "", "Runs jobs next to the owner's data", "tb-device-laptop", INK, 500, 560, 260, 90)

# inside the VPS
node("traefik", "Traefik", "", "Routes requests", "si-traefikproxy", "#24A1C1", 890, 410, 200, H)
node("web", "Web App", "", "Next.js website", "si-nextdotjs", INK, 1130, 160, 250, H)
node("api", "Platform API", "", "FastAPI: accounts, projects, runs", "si-fastapi", "#009688", 1130, 390, 250, 120)
node("r2", "Cloudflare R2", "", "Datasets and files", "si-cloudflare", "#F38020", 890, 600, 210, H)
node("db", "Platform Database", "", "PostgreSQL 16", "si-postgresql", "#4169E1", 1430, 600, 230, H)
node("worker", "Integration Worker", "", "Exports to Drive", "tb-cloud-upload", INK, 1690, 600, 220, H)

group("g_ai", "AI research tier", 890, 740, 1020, 320, color=AWS["ai"])
node("aipi", "AI PI Service", "", "AI reviewer that advises at every stage", "tb-brain", AWS["ai"], 910, 785, 980, 64)
STAGES = [("e_ds", "Dataset", "Prepares the data"), ("e_hy", "Hypothesis", "Proposes hypotheses"),
          ("e_xd", "Experiment Design", "Plans the analysis"), ("e_ex", "Execution", "Runs the analysis"),
          ("e_wr", "Writing", "Writes the paper")]
EW, EG = 180, 20
for i, (cid, n, out) in enumerate(STAGES):
    x = 910 + i * (EW + EG)
    add(cid, f"<b style='font-size:15px'>{i + 1}. {n}</b><br><span style='font-size:13px'>{out}</span>",
        f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=13;fillColor=#FFFFFF;strokeColor={CARD_LINE};"
        "align=center;verticalAlign=top;spacingTop=40;", x, 910, EW, 120)
    add(cid + "_i", "", f"shape=image;html=1;imageAspect=1;aspect=fixed;image={icon_uri('tb-robot', AWS['ai'])};",
        x + EW / 2 - 15, 918, 30, 30)
    edge("aipi", cid, "Advises" if i == 2 else "", sx=(i * (EW + EG) + EW / 2) / 980, sy=1, tx=0.5, ty=0, dashed=True)
for a_, b_ in zip(STAGES, STAGES[1:]):
    edge(a_[0], b_[0])

# external services, each at the height of its lane
node("gid", "Google Identity", "", "Google sign-in", "si-google", "#4285F4", 1990, 290, 270, H)
node("resend", "Resend", "", "Sign-in codes by email", "si-resend", INK, 1990, 390, 270, H)
node("extdb", "External data sources", "", "Project databases", "tb-database-import", INK, 1990, 490, 270, H)
node("drive", "Google Drive", "", "Receives results", "si-googledrive", "#1FA463", 1990, 600, 270, H)
node("llm", "LLM providers", "", "OpenAI, Gemini, OpenRouter", "si-openai", INK, 1990, 790, 270, H)
node("lit", "Literature APIs", "", "OpenAlex, arXiv", "tb-books", INK, 1990, 930, 270, H)

# delivery pipeline
group("g_cicd", "Delivery pipeline (CI/CD)", 500, 1120, 1430, 130)
node("gha", "GitHub Actions", "", "Tests and builds", "si-githubactions", "#2088FF", 530, 1155, 220, H)
node("hub", "Docker Hub", "", "Stores images", "si-docker", "#2496ED", 900, 1155, 220, H)
node("dokploy", "Dokploy", "", "Deploys to the VPS", "di-dokploy", INK, 1270, 1155, 240, H)

# ---------- flows: request path first, then data, AI, externals, delivery ----------
edge("users", "browser", "Use")
edge("browser", "cf", "HTTPS")
edge("cf", "traefik", "Forwards")
edge("traefik", "web", "", pts=[(990, 200)], sx=0.5, sy=0, tx=0, ty=0.5)
edge("traefik", "api", "")
edge("web", "api", "Calls")
edge("local", "cf", "Polls for jobs")
edge("api", "r2", "Stores files", pts=[(1150, 640)], sx=0.08, sy=1, tx=1, ty=0.5)
edge("api", "db", "Reads, writes", pts=[(1350, 640)], sx=0.88, sy=1, tx=0, ty=0.5)
edge("worker", "db", "Reads")
edge("api", "aipi", "Starts each stage", sx=0.5, sy=1, tx=(1255 - 910) / 980, ty=0)
edge("api", "gid", "Signs in", pts=[(1700, 420), (1700, 330)], sx=1, sy=0.25, tx=0, ty=0.5)
edge("api", "resend", "Sends email", pts=[(1800, 450), (1800, 430)], sx=1, sy=0.5, tx=0, ty=0.5)
edge("api", "extdb", "Imports tables", pts=[(1880, 480), (1880, 530)], sx=1, sy=0.75, tx=0, ty=0.5)
edge("worker", "drive", "Uploads")
edge("g_ai", "llm", "Asks models", sx=1, sy=(830 - 740) / 320, tx=0, ty=0.5)
edge("g_ai", "lit", "Searches", sx=1, sy=(970 - 740) / 320, tx=0, ty=0.5)
edge("gha", "hub", "Pushes images", dashed=True)
edge("hub", "dokploy", "Pulls images", dashed=True)
edge("dokploy", "g_vps", "Rolls out", sx=0.5, sy=0, tx=(1390 - 860) / 1070, ty=1, dashed=True)

xml = ('<mxfile host="drawio"><diagram id="sys-arch" name="System Architecture">'
       '<mxGraphModel dx="1640" dy="1040" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       'fold="1" page="1" pageScale="1" pageWidth="2300" pageHeight="1270" background="#FFFFFF" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
OUT.write_text(xml)
print("written", OUT)

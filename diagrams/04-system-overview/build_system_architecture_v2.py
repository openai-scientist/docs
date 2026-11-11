"""Build version 2 of the editable System Architecture Diagram (Report 7, IV 1.1.1, Figure IV-1).

Source: deliverables/FA26SE115_Report7.docx, IV 1.1.1 (diagram text, actor and
external system tables), 1.1.2 (deployment nodes) and 1.5 (delivery pipeline).
Icons: Simple Icons (CC0) and Dashboard Icons (Dokploy, kept in its own colours) for brands, Tabler Icons (MIT) for generic symbols,
stored in ./icons and embedded in the .drawio so the file stays self-contained.
Run: python3 build_system_architecture_v2.py
"""
from base64 import b64encode
from html import escape
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
OUT = HERE / "System-Architecture-Diagram-v2.drawio"  # version 1 stays in build_system_architecture.py
FONT = "fontFamily=Arial;fontColor=#000000;"
INK, GREY = "#000000", "#4D4D4D"
# AWS Architecture Icons group palette: white groups with a coloured border and matching title.
AWS = {"cloud": "#232F3E", "public": "#7AA116", "private": "#00A4A6", "ai": "#8C4FFF", "generic": "#7D8998"}
CARD_LINE, LINE = "#B6BEC9", "#545B64"

cells, ids = [], {}


def icon_uri(name, color):
    """Read an SVG icon, set its colour and return a draw.io data URI."""
    svg = (HERE / "icons" / f"{name}.svg").read_text()
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
        f"rounded=0;html=1;whiteSpace=wrap;{FONT}fontColor={color};fontSize=12;fillColor={fill};"
        f"strokeColor={color};strokeWidth=1.5;dashed={1 if dashed else 0};verticalAlign=top;align=left;"
        "spacingLeft=12;spacingTop=6;container=0;", x, y, w, h)


def tier(text, x, y, w=300):
    add(f"t{len(cells)}", text, f"text;html=1;{FONT}fontSize=11;fontStyle=1;fontColor={GREY};align=left;verticalAlign=middle;",
        x, y, w, 20)


def node(cid, name, kind, desc, ico, color, x, y, w, h=72, fill="#FFFFFF", dashed=False):
    """Card with an icon on the left: name, [type: technology] and one line of description."""
    label = f"<b style='font-size:13px'>{name}</b><br><span style='font-size:11px'>{desc}</span>"
    add(cid, label,
        f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=11;fillColor={fill};strokeColor={CARD_LINE};"
        f"strokeWidth=1;dashed={1 if dashed else 0};align=left;verticalAlign=middle;spacingLeft=52;spacingRight=6;",
        x, y, w, h)
    add(cid + "_i", "", f"shape=image;html=1;imageAspect=1;aspect=fixed;image={icon_uri(ico, color)};",
        x + 12, y + h / 2 - 15, 30, 30)


def edge(src, tgt, label="", pts=(), sx=None, sy=None, tx=None, ty=None, dashed=False, lx=0, ly=0):
    style = (f"edgeStyle=orthogonalEdgeStyle;rounded=1;arcSize=12;html=1;{FONT}fontSize=10;strokeColor={LINE};strokeWidth=1.25;"
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
    if ly:  # lift the label off a short line so the arrow stays visible
        geo += f'<mxPoint y="{ly}" as="offset"/>'
    cells.append(f'<mxCell id="e{len(cells)}" value="{escape(label.replace(chr(10), "<br>"))}" style="{style}" edge="1" parent="1" '
                 f'source="{src}" target="{tgt}"><mxGeometry x="{lx}" relative="1" as="geometry">{geo}</mxGeometry></mxCell>')


# ---------- title ----------

# ---------- layout ----------
# Read left to right: people and their browser, the request path into the VPS, the three tiers
# inside it, then the external services each tier talks to. CI/CD and the legend sit below.

# People (the four roles of Report 7) and how they reach the platform
group("g_users", "Users", 40, 20, 260, 270)
for i, (cid, n, d, ico) in enumerate([
        ("researcher", "Researcher", "Runs research cases", "tb-user"),
        ("pm", "Project Manager", "Manages the project and team", "tb-user-cog"),
        ("reviewer", "Reviewer", "Reviews and approves results", "tb-user-check"),
        ("admin", "Platform Admin", "Operates the platform", "tb-user-shield")]):
    node(cid, n, "Person", d, ico, INK, 50, 52 + i * 58, 240, 50)
node("browser", "Web browser", "Software", "Where users open the app", "tb-world-www", INK, 80, 330, 180, 60)
node("cf", "Cloudflare", "DNS, proxy, TLS", "Domain, HTTPS, protection", "si-cloudflare", "#F38020",
     80, 440, 180, 60)

# Local Node runs outside the platform, on the data holder's machine
group("g_holder", "At the data holder", 40, 510, 260, 110, dashed=True)
node("local", "Local Node", "Container: Python", "Analyses data where it lives", "tb-device-laptop", INK,
     55, 542, 230, 60)

# The platform on the VPS
group("g_vps", "OpenAI-Scientist on a Linux VPS", 360, 20, 940, 650, color=AWS["cloud"])
node("traefik", "Traefik", "Reverse proxy", "Routes each request", "si-traefikproxy", "#24A1C1", 380, 85, 180, 60)

group("g_app", "Application tier", 590, 50, 690, 128, color=AWS["public"])
node("web", "Web App", "Container: Next.js 16, React 19", "The website users work in", "si-nextdotjs",
     INK, 605, 80, 170, 70)
node("api", "Platform API", "Container: FastAPI, Python 3.12", "Accounts, projects and runs",
     "si-fastapi", "#009688", 830, 80, 210, 70)
node("worker", "Integration Worker", "Container: Python 3.12", "Sends results to Drive",
     "tb-cloud-upload", INK, 1070, 80, 195, 70)

group("g_data", "Data tier", 590, 220, 690, 112, color=AWS["private"])
node("r2", "Cloudflare R2", "Object storage, S3 API", "Datasets and files",
     "si-cloudflare", "#F38020", 605, 252, 195, 64, dashed=True)
node("db", "Platform Database", "Container: PostgreSQL 16", "Users, projects, history", "si-postgresql",
     "#4169E1", 1070, 252, 195, 64)

group("g_ai", "AI research tier", 380, 380, 900, 265, color=AWS["ai"])
# AI PI on top advises every engine. The engines run in stage order: the Platform API starts
# the next engine after the user accepts the result (Report 7, IV 1.1.1 and FE-06 to FE-10).
node("aipi", "AI PI Service", "Container: Python", "AI reviewer that advises the researcher at every stage",
     "tb-brain", AWS["ai"], 400, 420, 860, 56)
STAGES = [("e_ds", "Dataset Engine", "Prepares the data"), ("e_hy", "Hypothesis Engine", "Proposes hypotheses"),
          ("e_xd", "Experiment Design Engine", "Plans the analysis"), ("e_ex", "Execution Engine", "Runs the analysis"),
          ("e_pa", "Paper Engine", "Writes the paper")]
EW, EG, EX = 148, 30, 400
for i, (cid, n, out) in enumerate(STAGES):
    x = EX + i * (EW + EG)
    add(cid, f"<b style='font-size:12px'>{i + 1}. {n}</b><br><span style='font-size:11px'>{out}</span>",
        f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=11;fillColor=#FFFFFF;strokeColor={CARD_LINE};"
        "strokeWidth=1;align=center;verticalAlign=top;spacingTop=38;", x, 522, EW, 100)
    add(cid + "_i", "", f"shape=image;html=1;imageAspect=1;aspect=fixed;image={icon_uri('tb-robot', AWS['ai'])};",
        x + EW / 2 - 14, 528, 28, 28)
    edge("aipi", cid, "Advises" if i == 2 else "", sx=(i * (EW + EG) + EW / 2) / 860, sy=1, tx=0.5, ty=0,
         dashed=True)
for a_, b_ in zip(STAGES, STAGES[1:]):
    edge(a_[0], b_[0], "")

# External services, each placed next to the part of the platform that uses it
group("g_ext", "External services", 1360, 20, 240, 650, dashed=True)
node("gid", "Google Identity", "Software System", "Google sign-in", "si-google", "#4285F4", 1375, 52, 210, 56)
node("resend", "Resend", "Software System", "Sign-in codes by email", "si-resend", INK, 1375, 116, 210, 56)
node("drive", "Google Drive", "Software System", "Files in, results out", "si-googledrive", "#1FA463",
     1375, 180, 210, 56)
node("extdb", "External data sources", "Software System", "Project databases", "tb-database-import", INK,
     1375, 328, 210, 56)
node("llm", "LLM providers", "Software System", "OpenAI, Gemini", "si-openai", INK, 1375, 420, 210, 56)
node("lit", "Literature APIs", "Software System", "Research papers", "tb-books", INK, 1375, 544, 210, 56)

# Delivery pipeline (Report 7, IV 1.5)
group("g_cicd", "Delivery pipeline (CI/CD)", 360, 700, 940, 100)
node("gha", "GitHub Actions", "CI", "Tests and builds the code", "si-githubactions", "#2088FF",
     380, 730, 260, 56)
node("hub", "Docker Hub", "Image registry", "Stores built images", "si-docker", "#2496ED", 700, 730, 260, 56)
node("dokploy", "Dokploy", "Deployment", "Deploys to the VPS", "di-dokploy", INK, 1020, 730, 260, 56)


# ---------- flows ----------
edge("g_users", "browser", "Use", sx=0.5, sy=1, tx=0.5, ty=0)
edge("browser", "cf", "Opens", sx=0.5, sy=1, tx=0.5, ty=0)
edge("cf", "traefik", "Forwards", pts=[(325, 470), (325, 115)], sx=1, sy=0.5, tx=0, ty=0.5)
edge("traefik", "web", "", sx=1, sy=0.5, tx=0, ty=0.5)
edge("traefik", "api", "", pts=[(470, 166), (850, 166)], sx=0.5, sy=1, tx=0.095, ty=1)
edge("web", "api", "Calls")
edge("api", "r2", "Stores files", pts=[(870, 284)], sx=0.19, sy=1, tx=1, ty=0.5)
edge("api", "db", "Reads, writes", pts=[(1020, 284)], sx=0.905, sy=1, tx=0, ty=0.5, lx=0.6)
edge("worker", "db", "Reads", sx=0.5, sy=1, tx=0.5, ty=0, lx=0.6)
edge("api", "aipi", "Asks for advice", sx=0.38, sy=1, tx=(910 - 400) / 860, ty=0, lx=0.5)
edge("api", "g_ai", "Starts each stage", sx=0.62, sy=1, tx=(960 - 380) / 900, ty=0, lx=-0.45)
# Each external link gets its own lane in the gap between the VPS and the external column,
# so no two lines share a segment or cross.
edge("api", "gid", "Signs in", pts=[(1000, 30), (1345, 30), (1345, 80)], sx=(1000 - 830) / 210, sy=0,
     tx=0, ty=0.5, lx=-0.3)
edge("api", "resend", "Sends email", pts=[(1020, 42), (1330, 42), (1330, 144)], sx=(1020 - 830) / 210, sy=0,
     tx=0, ty=0.5, lx=-0.1)
edge("worker", "drive", "Uploads", pts=[(1315, 115), (1315, 208)], sx=1, sy=0.5, tx=0, ty=0.5, lx=0.6)
edge("api", "extdb", "Imports tables", pts=[(990, 356)], sx=(990 - 830) / 210, sy=1,
     tx=0, ty=0.5, lx=0.3)
edge("aipi", "llm", "Asks models", sx=1, sy=0.5, tx=0, ty=0.5)
edge("g_ai", "lit", "Searches", sx=1, sy=(572 - 380) / 265, tx=0, ty=0.5)
edge("local", "g_ai", "Sends\nsummaries", ly=-34, sx=1, sy=0.5, tx=0,
     ty=(572 - 380) / 265)
edge("gha", "hub", "Pushes images", dashed=True)
edge("hub", "dokploy", "Pulls images", dashed=True)
edge("dokploy", "g_vps", "Rolls out", sx=0.5, sy=0, tx=(1150 - 360) / 940, ty=1, dashed=True)

xml = ('<mxfile host="drawio"><diagram id="sys-arch" name="System Architecture">'
       '<mxGraphModel dx="1640" dy="1040" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       'fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="830" background="#FFFFFF" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
OUT.write_text(xml)
print("written", OUT)

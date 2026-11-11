"""Build the editable System Architecture Diagram (Report 7, IV 1.1.1, Figure IV-1).

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


def group(cid, title, x, y, w, h, fill="#FBFBFC", dashed=False):
    """Tier or boundary band with its title at the top left."""
    add(cid, f"<b>{title}</b>",
        f"rounded=1;arcSize=2;html=1;whiteSpace=wrap;{FONT}fontSize=12;fillColor={fill};"
        f"strokeColor={INK};strokeWidth=1;dashed={1 if dashed else 0};verticalAlign=top;align=left;"
        "spacingLeft=12;spacingTop=6;container=0;", x, y, w, h)


def tier(text, x, y, w=300):
    add(f"t{len(cells)}", text, f"text;html=1;{FONT}fontSize=11;fontStyle=1;fontColor={GREY};align=left;verticalAlign=middle;",
        x, y, w, 20)


def node(cid, name, kind, desc, ico, color, x, y, w, h=72, fill="#FFFFFF", dashed=False):
    """Card with an icon on the left: name, [type: technology] and one line of description."""
    label = f"<b style='font-size:13px'>{name}</b><br><span style='font-size:11px'>{desc}</span>"
    add(cid, label,
        f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=11;fillColor={fill};strokeColor={INK};"
        f"strokeWidth=1;dashed={1 if dashed else 0};align=left;verticalAlign=middle;spacingLeft=52;spacingRight=6;",
        x, y, w, h)
    add(cid + "_i", "", f"shape=image;html=1;imageAspect=1;aspect=fixed;image={icon_uri(ico, color)};",
        x + 12, y + h / 2 - 15, 30, 30)


def edge(src, tgt, label="", pts=(), sx=None, sy=None, tx=None, ty=None, dashed=False, lx=0):
    style = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;{FONT}fontSize=10;strokeColor={INK};strokeWidth=1;"
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


# ---------- title ----------

# ---------- columns ----------
group("g_users", "Users and data holders", 20, 90, 240, 780)
group("g_edge", "Edge", 280, 90, 170, 780)
group("g_vps", "OpenAI-Scientist on a Linux VPS", 470, 90, 890, 740,
      fill="#FFFFFF", dashed=True)
group("g_ext", "External services", 1380, 90, 250, 780, fill="#FBFBFC")

# Users: the four roles of Report 7, then the browser and the Local Node
for i, (cid, n, d, ico) in enumerate([
        ("researcher", "Researcher", "Runs research cases", "tb-user"),
        ("pm", "Project Manager", "Manages the project and team", "tb-user-cog"),
        ("reviewer", "Reviewer", "Reviews and approves results", "tb-user-check"),
        ("admin", "Platform Admin", "Operates the platform", "tb-user-shield")]):
    node(cid, n, "Person", d, ico, INK, 35, 125 + i * 84, 210)
node("browser", "Web browser", "Software", "Where users open the app", "tb-world-www", INK, 35, 476, 210)
node("local", "Local Node", "Container: Python", "Analyses data on the owner's machine",
     "tb-device-laptop", INK, 35, 760, 210, 84)

# Edge
node("cf", "Cloudflare", "DNS, proxy, TLS", "Domain, HTTPS and protection", "si-cloudflare", "#F38020", 290, 476, 150)

# VPS: ingress, application tier, data tier, AI research tier
node("traefik", "Traefik", "Reverse proxy, :443", "Sends each request to the right service",
     "si-traefikproxy", "#24A1C1", 490, 128, 850, 60)
group("g_app", "Application tier", 480, 196, 870, 116)
node("web", "Web App", "Container: Next.js 16, React 19", "The website users work in", "si-nextdotjs",
     INK, 490, 224, 225, 76)
node("api", "Platform API", "Container: FastAPI, Python 3.12", "Handles accounts, projects and runs",
     "si-fastapi", "#009688", 785, 224, 260, 76)
node("worker", "Integration Worker", "Container: Python 3.12", "Sends results to Google Drive",
     "tb-cloud-upload", INK, 1080, 224, 260, 76)
group("g_data", "Data tier", 480, 324, 870, 112)
node("r2", "Cloudflare R2", "Object storage, S3 API", "Stores datasets and files",
     "si-cloudflare", "#F38020", 490, 354, 260, 72, dashed=True)
node("db", "Platform Database", "Container: PostgreSQL 16", "Stores users, projects and history", "si-postgresql",
     "#4169E1", 1080, 354, 260, 72)

group("g_ai", "AI research tier", 480, 448, 870, 362, fill="#FBFBFC")
# Five stage engines in pipeline order. The arrows show stage order: the Platform API starts
# the next engine after the user accepts the result (Report 7, IV 1.1.1 and FE-06 to FE-10).
# The AI PI sits above the engines and advises each of them at its decision gate.
STAGES = [("e_ds", "Dataset Engine", "Prepares the data"), ("e_hy", "Hypothesis Engine", "Proposes hypotheses"),
          ("e_xd", "Experiment Design Engine", "Plans the analysis"), ("e_ex", "Execution Engine", "Runs the analysis"),
          ("e_pa", "Paper Engine", "Writes the paper")]
EW, EG = 136, 32.5
for i, (cid, n, out) in enumerate(STAGES):
    x = 510 + i * (EW + EG)
    add(cid, f"<b style='font-size:12px'>{i + 1}. {n}</b><br><span style='font-size:11px'>{out}</span>",
        f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=11;fillColor=#FFFFFF;strokeColor={INK};"
        "strokeWidth=1;align=center;verticalAlign=top;spacingTop=38;", x, 600, EW, 100)
    add(cid + "_i", "", f"shape=image;html=1;imageAspect=1;aspect=fixed;image={icon_uri('tb-robot', INK)};",
        x + EW / 2 - 14, 606, 28, 28)
add("runtime", "<b>AI Engine runtime</b>: built into every engine, same core with a different configuration",
    f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=12;fillColor=#DAE8FC;strokeColor=#6C8EBF;"
    "strokeWidth=1;align=center;verticalAlign=middle;", 510, 730, 810, 40)
node("aipi", "AI PI Service", "Container: Python", "AI reviewer that advises the researcher at every stage",
     "tb-brain", INK, 510, 500, 810, 60)
for i, (cid, _, _) in enumerate(STAGES):
    edge("aipi", cid, "Advises" if i == 2 else "", sx=(i * (EW + EG) + EW / 2) / 810, sy=1, tx=0.5, ty=0, dashed=True)
for a_, b_ in zip(STAGES, STAGES[1:]):
    edge(a_[0], b_[0], "")

# External services (Report 7, IV 1.1.1 external system table)
node("gid", "Google Identity", "Software System", "Google sign-in", "si-google", "#4285F4", 1392, 124, 228)
node("resend", "Resend", "Software System", "Sends sign-in codes by email", "si-resend", INK, 1392, 204, 228)
node("drive", "Google Drive", "Software System", "Imports files, receives results", "si-googledrive", "#1FA463",
     1392, 284, 228)
node("extdb", "External data sources", "Software System", "Project databases to import",
     "tb-database-import", INK, 1392, 398, 228)
node("llm", "LLM providers", "Software System", "AI models: OpenAI, Gemini", "si-openai", INK, 1392, 542, 228)
node("lit", "Literature APIs", "Software System", "Finds research papers", "tb-books", INK,
     1392, 715, 228)

# Delivery pipeline (Report 7, IV 1.5)
group("g_cicd", "Delivery pipeline (CI/CD)", 20, 890, 1340, 120)
node("gha", "GitHub Actions", "CI", "Tests and builds the code", "si-githubactions", "#2088FF",
     40, 925, 300, 70)
node("hub", "Docker Hub", "Image registry", "Stores built images", "si-docker", "#2496ED",
     420, 925, 300, 70)
node("dokploy", "Dokploy", "Deployment", "Deploys to the VPS", "di-dokploy", INK, 800, 925, 300, 70)

# Legend
add("legend", "<b>Legend</b><br>Solid arrow: request or data flow<br>"
    "Dashed arrow: build and deploy<br>Dashed card: managed service outside the VPS<br>"
    "Arrow between engines: stage order 1 to 5. The<br>Platform API starts the next stage after the user<br>accepts the result. Dashed: AI PI advice<br>AI PI: AI Principal Investigator",
    f"rounded=1;arcSize=4;html=1;whiteSpace=wrap;{FONT}fontSize=10;fillColor=#FFFFFF;strokeColor={INK};"
    "align=left;verticalAlign=top;spacing=8;", 1380, 890, 250, 140)

# ---------- flows ----------
edge("browser", "cf", "Opens")
edge("cf", "traefik", "Forwards", pts=[(365, 158)], sx=0.5, sy=0, tx=0, ty=0.5)
edge("traefik", "web", "", sx=0.14, sy=1, tx=0.5, ty=0)
edge("traefik", "api", "", sx=0.49, sy=1, tx=0.5, ty=0)
edge("web", "api", "Calls")
edge("api", "r2", "Stores files", pts=[(798, 390)], sx=0.05, sy=1, tx=1, ty=0.5)
edge("api", "db", "Reads, writes", pts=[(1015, 390)], sx=0.88, sy=1, tx=0, ty=0.5)
edge("worker", "db", "Reads", sx=0.5, sy=1, tx=0.5, ty=0, lx=0.6)
edge("api", "g_ai", "Starts each stage", sx=0.5, sy=1, tx=0.5, ty=0)
edge("api", "gid", "Signs in", pts=[(1000, 204), (1365, 204), (1365, 160)], sx=0.83, sy=0, tx=0,
     ty=0.5, lx=-0.35)
edge("api", "resend", "Sends email", pts=[(1030, 214), (1365, 214), (1365, 240)], sx=0.94, sy=0, tx=0,
     ty=0.5, lx=0.45)
edge("worker", "drive", "Uploads", pts=[(1365, 290), (1365, 320)], sx=1, sy=0.86, tx=0, ty=0.5)
edge("api", "extdb", "Imports tables", pts=[(960, 442), (1365, 442), (1365, 434)], sx=0.67, sy=1,
     tx=0, ty=0.5)
edge("g_ai", "llm", "Asks models", sx=1, sy=0.337, tx=0, ty=0.5)
edge("g_ai", "lit", "Searches", sx=1, sy=0.83, tx=0, ty=0.5)
edge("api", "aipi", "Asks for advice", sx=0.2, sy=1, tx=(837 - 510) / 810, ty=0, lx=0.62)
edge("local", "g_ai", "Sends summary results", sx=1, sy=0.5, tx=0, ty=0.894)
edge("gha", "hub", "Pushes images", dashed=True)
edge("hub", "dokploy", "Pulls images", dashed=True)
edge("dokploy", "g_vps", "Rolls out", sx=0.5, sy=0, tx=0.618, ty=1, dashed=True)

xml = ('<mxfile host="drawio"><diagram id="sys-arch" name="System Architecture">'
       '<mxGraphModel dx="1640" dy="1040" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       'fold="1" page="1" pageScale="1" pageWidth="1660" pageHeight="1050" background="#FFFFFF" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
OUT.write_text(xml)
print("written", OUT)

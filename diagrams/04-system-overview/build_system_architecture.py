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


def group(cid, title, x, y, w, h, fill="#F7F8FA", dashed=False):
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
    label = (f"<b style='font-size:12px'>{name}</b><br><span style='font-size:10px;color:{GREY}'>[{kind}]</span>"
             f"<br><span style='font-size:11px'>{desc}</span>")
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
add("title", "<b>System Architecture of OpenAI-Scientist</b><br><span style='font-size:11px;color:#4D4D4D'>"
    "Production: scientist.beyond8.io.vn (web), api-scientist.beyond8.io.vn (API)</span>",
    f"text;html=1;{FONT}fontSize=18;align=left;verticalAlign=middle;", 20, 14, 900, 50)

# ---------- columns ----------
group("g_users", "Users and data holders", 20, 90, 240, 780)
group("g_edge", "Edge", 280, 90, 170, 780)
group("g_vps", "OpenAI-Scientist  [Software System]  Linux VPS, Docker Engine (Dokploy)", 470, 90, 890, 740,
      fill="#FFFFFF", dashed=True)
group("g_ext", "External services  [Software System]", 1380, 90, 250, 780, fill="#F5F5F5")

# Users: the four roles of Report 7, then the browser and the Local Node
for i, (cid, n, d, ico) in enumerate([
        ("researcher", "Researcher", "Runs research cases and answers pinned decisions", "tb-user"),
        ("pm", "Project Manager", "Members, data, budget and runs", "tb-user-cog"),
        ("reviewer", "Reviewer", "Reads, comments, approves the Dossier", "tb-user-check"),
        ("admin", "Platform Admin", "Users, models, keys, health", "tb-user-shield")]):
    node(cid, n, "Person", d, ico, INK, 35, 125 + i * 84, 210)
node("browser", "Web browser", "Software", "Used by all four roles", "tb-world-www", INK, 35, 476, 210)
node("local", "Local Node", "Container: Python", "Runs at the data holder, releases aggregates only",
     "tb-device-laptop", INK, 35, 760, 210, 84)

# Edge
node("cf", "Cloudflare", "DNS, proxy, TLS", "Public entry point", "si-cloudflare", "#F38020", 290, 476, 150)

# VPS: ingress, application tier, data tier, AI research tier
node("traefik", "Traefik", "Reverse proxy, :443", "Routes the web host and the API host to their containers",
     "si-traefikproxy", "#24A1C1", 490, 128, 850, 60)
tier("APPLICATION TIER", 490, 200)
node("web", "Web App", "Container: Next.js 16, React 19", "User interface, no scientific logic", "si-nextdotjs",
     INK, 490, 224, 225, 76)
node("api", "Platform API", "Container: FastAPI, Python 3.12", "Runs, objects, decisions, REST and run events",
     "si-fastapi", "#009688", 785, 224, 260, 76)
node("worker", "Integration Worker", "Container: Python 3.12", "Delivers run results to integrations",
     "tb-cloud-upload", INK, 1080, 224, 260, 76)
tier("DATA TIER", 490, 318)
node("r2", "Cloudflare R2", "Object storage, S3 API", "Datasets, project files, artifacts (managed)",
     "si-cloudflare", "#F38020", 490, 342, 260, 76, dashed=True)
node("db", "Platform Database", "Container: PostgreSQL 16", "People, projects, runs, audit log", "si-postgresql",
     "#4169E1", 1080, 342, 260, 76)

group("g_ai", "AI research tier", 490, 460, 850, 350, fill="#F7F8FA")
# Five stage engines in pipeline order. Engines do not call each other: the Platform API
# hands each accepted artifact to the next stage (Report 7, IV 1.1.1 and FE-06 to FE-10).
add("order", "Stage order, dataset first. The Platform API hands each accepted artifact to the next engine.",
    f"text;html=1;{FONT}fontSize=11;fontColor={GREY};align=left;verticalAlign=middle;", 510, 488, 800, 22)
STAGES = [("e_ds", "Dataset Engine", "DatasetSnapshot"), ("e_hy", "Hypothesis Engine", "HypothesisSet"),
          ("e_xd", "Experiment Design Engine", "AnalysisPlan, Lock"), ("e_ex", "Execution Engine", "EvidenceBundle"),
          ("e_pa", "Paper Engine", "PaperPack")]
EW, EG = 136, 32.5
for i, (cid, n, out) in enumerate(STAGES):
    x = 510 + i * (EW + EG)
    add(cid, f"<b style='font-size:12px'>{n}</b><br><span style='font-size:10px;color:{GREY}'>[Container]</span>"
        f"<br><span style='font-size:11px'>Outputs<br><b>{out}</b></span>",
        f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=11;fillColor=#FFFFFF;strokeColor={INK};"
        "strokeWidth=1;align=center;verticalAlign=top;spacingTop=40;", x, 516, EW, 116)
    add(cid + "_i", "", f"shape=image;html=1;imageAspect=1;aspect=fixed;image={icon_uri('tb-robot', INK)};",
        x + EW / 2 - 14, 524, 28, 28)
for a_, b_ in zip(STAGES, STAGES[1:]):
    edge(a_[0], b_[0], "")
add("runtime", "<b>AI Engine runtime</b> shared by the five stage engines: "
    "agent loop, guards, checks, live trace, budget",
    f"rounded=1;arcSize=8;html=1;whiteSpace=wrap;{FONT}fontSize=12;fillColor=#DAE8FC;strokeColor=#6C8EBF;"
    "strokeWidth=1;align=center;verticalAlign=middle;", 510, 648, 810, 40)
node("aipi", "AI PI Service", "Container: Python", "Advises at gates, reviews runs, records forecasts",
     "tb-brain", INK, 510, 708, 380, 72)
add("ai_note", "Each AI service runs in its own container with its own run volume.",
    f"text;html=1;{FONT}fontSize=11;fontColor={GREY};align=left;verticalAlign=middle;", 910, 732, 410, 24)

# External services (Report 7, IV 1.1.1 external system table)
node("gid", "Google Identity", "Software System", "Sign in with Google", "si-google", "#4285F4", 1392, 124, 228)
node("resend", "Resend", "Software System", "One-time passwords and notifications", "si-resend", INK, 1392, 204, 228)
node("drive", "Google Drive", "Software System", "File import and result delivery", "si-googledrive", "#1FA463",
     1392, 284, 228)
node("extdb", "External data sources", "Software System", "Databases connected to a project",
     "tb-database-import", INK, 1392, 398, 228)
node("llm", "LLM providers", "Software System", "OpenAI, Google Gemini, OpenRouter", "si-openai", INK, 1392, 542, 228)
node("lit", "Literature APIs", "Software System", "OpenAlex, arXiv, Semantic Scholar, Crossref", "tb-books", INK,
     1392, 715, 228)

# Delivery pipeline (Report 7, IV 1.5)
group("g_cicd", "Delivery pipeline (CI/CD)", 20, 890, 1340, 120)
node("gha", "GitHub Actions", "CI", "Lint, contract checks, tests, image build", "si-githubactions", "#2088FF",
     40, 925, 300, 70)
node("hub", "Docker Hub", "Image registry", "Images tagged latest and commit SHA", "si-docker", "#2496ED",
     420, 925, 300, 70)
node("dokploy", "Dokploy", "Deployment", "Redeploy, migrate, health checks", "di-dokploy", INK, 800, 925, 300, 70)

# Legend
add("legend", "<b>Legend</b><br>Solid arrow: request, label names the data and [protocol]<br>"
    "Dashed arrow: build and deployment flow<br>White card: container or person<br>"
    "Dashed card: managed service outside the VPS<br>Grey band: tier or external group<br>"
    "Blue band: shared AI Engine runtime<br>AI PI: AI Principal Investigator",
    f"rounded=1;arcSize=4;html=1;whiteSpace=wrap;{FONT}fontSize=10;fillColor=#FFFFFF;strokeColor={INK};"
    "align=left;verticalAlign=top;spacing=8;", 1380, 890, 250, 140)

# ---------- flows ----------
edge("browser", "cf", "[HTTPS]")
edge("cf", "traefik", "[HTTPS]", pts=[(365, 158)], sx=0.5, sy=0, tx=0, ty=0.5)
edge("traefik", "web", "[HTTPS]", sx=0.14, sy=1, tx=0.5, ty=0)
edge("traefik", "api", "[HTTPS]", sx=0.49, sy=1, tx=0.5, ty=0)
edge("web", "api", "Calls\n[REST, SSE]")
edge("api", "r2", "Stores files\n[S3 API]", pts=[(815, 380)], sx=0.12, sy=1, tx=1, ty=0.5)
edge("api", "db", "Reads, writes\n[SQL]", pts=[(1015, 380)], sx=0.88, sy=1, tx=0, ty=0.5)
edge("worker", "db", "[SQL]", sx=0.5, sy=1, tx=0.5, ty=0)
edge("api", "g_ai", "Starts stage work\n[HTTP/JSON]", sx=0.5, sy=1, tx=0.5, ty=0)
edge("api", "gid", "Signs in [OAuth 2.0]", pts=[(1000, 204), (1365, 204), (1365, 160)], sx=0.83, sy=0, tx=0,
     ty=0.5, lx=-0.35)
edge("api", "resend", "Sends email [HTTPS]", pts=[(1030, 214), (1365, 214), (1365, 240)], sx=0.94, sy=0, tx=0,
     ty=0.5, lx=0.45)
edge("worker", "drive", "Uploads\n[HTTPS]", pts=[(1365, 290), (1365, 320)], sx=1, sy=0.86, tx=0, ty=0.5)
edge("api", "extdb", "Imports tables [SQL, read-only]", pts=[(960, 440), (1365, 440), (1365, 434)], sx=0.67, sy=1,
     tx=0, ty=0.5)
edge("g_ai", "llm", "Prompts\n[HTTPS]", sx=1, sy=0.337, tx=0, ty=0.5)
edge("g_ai", "lit", "Searches\n[HTTPS]", sx=1, sy=0.83, tx=0, ty=0.5)
edge("local", "g_ai", "Aggregates only [HTTPS]", sx=1, sy=0.5, tx=0, ty=0.894)
edge("gha", "hub", "Pushes images", dashed=True)
edge("hub", "dokploy", "Pulls images", dashed=True)
edge("dokploy", "g_vps", "Rolls out", sx=0.5, sy=0, tx=0.618, ty=1, dashed=True)

xml = ('<mxfile host="drawio"><diagram id="sys-arch" name="System Architecture">'
       '<mxGraphModel dx="1640" dy="1040" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       'fold="1" page="1" pageScale="1" pageWidth="1660" pageHeight="1050" background="#FFFFFF" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
OUT.write_text(xml)
print("written", OUT)

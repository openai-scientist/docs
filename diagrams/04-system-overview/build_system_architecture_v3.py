"""Build the System Architecture diagrams, version 3 (diagram-design style).

Two slide-sized (1280x720) HTML figures with inline SVG:
  * System-Architecture-v3-overview.html  - the whole production system
  * System-Architecture-v3-ai-tier.html   - a zoom into the AI research tier

Facts come from Report 7, chapter IV 1.1 (System Architecture, Deployment Diagram,
Trust Boundaries) and the non-screen functions NS-01 to NS-05. Colours follow the AWS
architecture palette already used by versions 1 and 2. Every coordinate is placed by
hand on a 4px grid so connectors stay orthogonal and labels never sit on a line.
"""
from base64 import b64encode
from html import escape
from pathlib import Path
import re

HERE = Path(__file__).parent

# ---------- tokens (AWS palette mapped to diagram-design roles) ----------
PAPER, INK, MUTED, SOFT = "#FFFFFF", "#232F3E", "#545B64", "#5F6B7A"
RULE = "#B6BEC9"
ACCENT, ACCENT_TINT = "#C7511F", "rgba(199,81,31,0.07)"   # focal only, 1-2 per figure
LINK = "#2E73B8"                                        # calls that leave the VPS
TIER = {  # stroke colour, label colour (darkened so 8px text clears 4.5:1)
    "vps": ("#232F3E", "#232F3E"),
    "app": ("#7AA116", "#4D6B0B"),
    "data": ("#00A4A6", "#00787A"),
    "ai": ("#8C4FFF", "#6B2FD6"),
    "ext": ("#7D8998", "#5F6B7A"),
}
FONTS = ("https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1"
         "&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap")
SANS, MONO = "Geist, system-ui, sans-serif", "'Geist Mono', ui-monospace, monospace"


def icon_uri(name, color):
    """Inline SVG icon from icons/ as a data URI, tinted to colour (same loader as version 2)."""
    svg = (HERE / "icons" / f"{name}.svg").read_text()
    if name.startswith("tb-"):
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    elif name.startswith("si-"):
        svg = re.sub(r"<svg ", f'<svg fill="{color}" ', svg, count=1)
    return "data:image/svg+xml;base64," + b64encode(svg.encode()).decode()


# icon per node name: (file, colour)
ICONS = {
    "Users": ("tb-user", INK), "Cloudflare": ("si-cloudflare", "#F38020"),
    "Traefik": ("si-traefikproxy", "#24A1C1"), "Web App": ("si-nextdotjs", INK),
    "Platform API": ("si-fastapi", "#009688"), "Integration\nWorker": ("tb-cloud-upload", INK),
    "Cloudflare R2": ("si-cloudflare", "#F38020"), "Platform DB": ("si-postgresql", "#4169E1"),
    "AI PI Service + 5 stage engines": ("tb-brain", "#8C4FFF"), "AI PI Service": ("tb-brain", "#8C4FFF"),
    "Local Node": ("tb-device-laptop", INK), "Google Identity": ("si-google", "#4285F4"),
    "Resend": ("si-resend", INK), "Google Drive": ("si-googledrive", "#1FA463"),
    "Team chat": ("tb-messages", INK), "External DBs": ("tb-database-import", INK),
    "LLM providers": ("si-openai", INK), "Literature APIs": ("tb-books", INK),
    "GitHub Actions": ("si-githubactions", "#2088FF"), "Docker Hub": ("si-docker", "#2496ED"),
    "Dokploy": ("di-dokploy", INK), "Release Gate": ("tb-shield-lock", INK),
    "Dataset": ("tb-robot", "#8C4FFF"), "Hypothesis": ("tb-robot", "#8C4FFF"),
    "Experiment\nDesign": ("tb-robot", "#8C4FFF"), "Execution": ("tb-robot", "#8C4FFF"),
    "Paper": ("tb-robot", "#8C4FFF"),
}


class Figure:
    """Collects SVG layers in z-order: zones, then arrows, then nodes, then labels."""

    def __init__(self):
        self.zones, self.arrows, self.nodes, self.labels = [], [], [], []

    # zone: tier or trust boundary, eyebrow label on a paper mask over the border
    def zone(self, x, y, w, h, label, tier, dashed=False):
        stroke, text = TIER[tier]
        dash = ' stroke-dasharray="5,4"' if dashed else ""
        self.zones.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" '
                          f'stroke="{stroke}" stroke-width="1.2"{dash}/>')
        lw = len(label) * 6 + 12
        self.zones.append(f'<rect x="{x + 12}" y="{y - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>'
                          f'<text x="{x + 18}" y="{y + 3}" fill="{text}" font-size="8" font-family="{MONO}" '
                          f'font-weight="500" letter-spacing="0.14em">{escape(label.upper())}</text>')

    # node: opaque mask, box, name (sans 600) and a technical sublabel (mono)
    def node(self, x, y, w, h, name, sub="", kind="svc"):
        stroke, fill, dash = RULE, PAPER, ""
        if kind == "focal":
            stroke, fill = ACCENT, ACCENT_TINT
        elif kind == "managed":
            dash = ' stroke-dasharray="4,3"'
        elif kind == "ext":
            stroke, dash = "#9AA4B1", ' stroke-dasharray="4,3"'
        cx = x + w / 2
        lines = name.split("\n")
        top = y + h / 2 - (len(lines) - 1) * 10 - (6 if sub else -6)
        icon = ICONS.get(name)
        img = ""
        if icon:
            uri = icon_uri(*icon)
            if h >= 72:   # tall box: icon centred above the text
                top = y + 52
                img = f'<image href="{uri}" x="{cx - 12}" y="{y + 12}" width="24" height="24"/>'
            else:         # short box: icon at the left, text centred in the remaining width
                s_, pad = (20, 10) if h <= 56 else (24, 12)
                img = f'<image href="{uri}" x="{x + pad}" y="{y + (h - s_) / 2}" width="{s_}" height="{s_}"/>'
                cx = x + pad + s_ + (w - pad - s_) / 2
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
               f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" '
               f'stroke-width="{1.4 if kind == "focal" else 1}"{dash}/>']
        if img:
            out.append(img)
        for i, ln in enumerate(lines):
            out.append(f'<text x="{cx}" y="{top + i * 20}" fill="{INK}" font-size="16" font-weight="600" '
                       f'font-family="{SANS}" text-anchor="middle">{escape(ln)}</text>')
        if sub:
            out.append(f'<text x="{cx}" y="{top + (len(lines) - 1) * 20 + 18}" fill="{MUTED}" font-size="12" '
                       f'font-family="{MONO}" text-anchor="middle">{escape(sub)}</text>')
        self.nodes.append("".join(out))

    # arrow: orthogonal polyline with r=8 rounded corners, or a raw path string
    def arrow(self, pts=None, d=None, color=MUTED, dashed=False):
        if d is None:
            d = rounded(pts)
        marker = {MUTED: "arrow", LINK: "arrow-link", ACCENT: "arrow-accent"}[color]
        dash = ' stroke-dasharray="4,3"' if dashed else ""
        self.arrows.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{1 if dashed else 1.3}"'
                           f'{dash} marker-end="url(#{marker})"/>')

    # label beside a segment: side "above" a horizontal line or "right"/"left" of a vertical one
    def label(self, x, y, text, side="above"):
        text = text.upper()
        w = len(text) * 7.4 + 8
        if side == "above":
            mx, my, tx, ty, anchor = x - w / 2, y - 24, x, y - 13, "middle"
        elif side == "right":
            mx, my, tx, ty, anchor = x + 8, y - 8, x + 12, y + 4, "start"
        else:
            mx, my, tx, ty, anchor = x - 8 - w, y - 8, x - 12, y + 4, "end"
        self.labels.append(f'<rect x="{mx:.0f}" y="{my}" width="{w:.0f}" height="16" rx="2" fill="{PAPER}"/>'
                           f'<text x="{tx}" y="{ty}" fill="{MUTED}" font-size="12" font-family="{MONO}" '
                           f'text-anchor="{anchor}" letter-spacing="0.04em">{escape(text)}</text>')

    def callout(self, x, y, text):
        self.labels.append(f'<text x="{x}" y="{y}" fill="{SOFT}" font-size="16" font-style="italic" '
                           f'font-family="\'Instrument Serif\', serif">{escape(text)}</text>')

    def svg(self, slug, title, desc, legend):
        defs = "".join(
            f'<marker id="{mid}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">'
            f'<polygon points="0 0, 8 3, 0 6" fill="{c}"/></marker>'
            for mid, c in (("arrow", MUTED), ("arrow-link", LINK), ("arrow-accent", ACCENT)))
        return (f'<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" role="img" '
                f'aria-labelledby="{slug}-title {slug}-desc">'
                f'<title id="{slug}-title">{escape(title)}</title><desc id="{slug}-desc">{escape(desc)}</desc>'
                f'<defs>{defs}</defs><rect width="1280" height="720" fill="{PAPER}"/>'
                + "".join(self.zones + self.arrows + self.nodes + self.labels)
                + "</svg>")


def rounded(pts, r=8):
    """Orthogonal path through pts with quadratic r=8 corners."""
    d = [f"M{pts[0][0]},{pts[0][1]}"]
    for (x0, y0), (x1, y1), (x2, y2) in zip(pts, pts[1:], pts[2:]):
        dx1, dy1 = (x1 > x0) - (x1 < x0), (y1 > y0) - (y1 < y0)
        dx2, dy2 = (x2 > x1) - (x2 < x1), (y2 > y1) - (y2 < y1)
        d.append(f"L{x1 - dx1 * r},{y1 - dy1 * r} Q{x1},{y1} {x1 + dx2 * r},{y1 + dy2 * r}")
    d.append(f"L{pts[-1][0]},{pts[-1][1]}")
    return " ".join(d)


def legend_strip(items):
    """Horizontal legend in the bottom 60px safe area."""
    out, x = [f'<line x1="40" y1="672" x2="1240" y2="672" stroke="{RULE}" stroke-width="0.8"/>'], 40
    for kind, text in items:
        if kind in ("solid", "link", "dashed"):
            color = LINK if kind == "link" else MUTED
            dash = ' stroke-dasharray="4,3"' if kind == "dashed" else ""
            out.append(f'<line x1="{x}" y1="696" x2="{x + 28}" y2="696" stroke="{color}" stroke-width="1.3"{dash}/>')
        else:
            stroke = {"focal": ACCENT, "managed": RULE, "ext": "#9AA4B1"}[kind]
            dash = "" if kind == "focal" else ' stroke-dasharray="4,3"'
            out.append(f'<rect x="{x}" y="688" width="28" height="16" rx="3" fill="{PAPER}" stroke="{stroke}"{dash}/>')
        out.append(f'<text x="{x + 36}" y="700" fill="{MUTED}" font-size="12" font-family="{MONO}">{escape(text)}</text>')
        x += 36 + len(text) * 7.4 + 32
    return "".join(out)


def page(slug, eyebrow, title, svg):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link href="{FONTS}" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: {SANS}; background: {PAPER}; color: {INK}; min-height: 100vh;
           }}
    .frame {{ max-width: 1280px; width: 100%; }}
    .diagram-container {{ width: 100%; overflow-x: auto; }}
    .eyebrow {{ font-family: {MONO}; font-size: 0.66rem; font-weight: 500; letter-spacing: 0.18em;
               text-transform: uppercase; color: {MUTED}; margin-bottom: 0.5rem; }}
    h1 {{ font-family: 'Instrument Serif', serif; font-size: 2rem; font-weight: 400;
          letter-spacing: -0.02em; line-height: 1.15; margin-bottom: 1.5rem; }}
    svg {{ width: 100%; min-width: 1280px; display: block; }}
    @media print {{ .diagram-container {{ overflow-x: visible; }} svg {{ min-width: 0; }} }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="diagram-container" id="{slug}">{svg}</div>
  </div>
</body>
</html>
"""


# =====================================================================================
# Figure 1 - overview of the production system
# =====================================================================================
def overview():
    f = Figure()
    # zones
    f.zone(232, 60, 768, 488, "Linux VPS · Dokploy · Docker", "vps")
    f.zone(420, 92, 220, 328, "Application tier", "app")
    f.zone(660, 92, 200, 240, "Data tier", "data")
    f.zone(420, 440, 560, 96, "AI research tier", "ai")
    f.zone(32, 452, 176, 96, "Data holder", "ext", dashed=True)
    f.zone(1032, 60, 208, 340, "Platform services", "ext", dashed=True)
    f.zone(1032, 420, 208, 128, "AI services", "ext", dashed=True)
    f.zone(232, 564, 768, 84, "Delivery · CI/CD", "ext")

    # arrows (drawn before nodes)
    f.arrow([(120, 168), (120, 232)])                                   # users -> cloudflare
    f.arrow([(200, 260), (252, 260)])                                   # cloudflare -> traefik
    f.arrow([(320, 232), (320, 152), (436, 152)])                       # traefik -> web app
    f.arrow([(388, 260), (436, 260)])                                   # traefik -> api
    f.arrow([(530, 180), (530, 232)])                                   # web app -> api (REST)
    # routed so that no two connectors cross: no hops needed
    f.arrow([(604, 232), (604, 204), (760, 204), (760, 180)])           # api -> R2
    f.arrow([(624, 260), (676, 260)])                                   # api -> db
    f.arrow([(436, 276), (404, 276), (404, 484), (436, 484)])           # api -> ai tier
    f.arrow([(624, 356), (760, 356), (760, 288)])                       # worker -> db
    f.arrow([(624, 380), (1032, 380)], color=LINK)                      # worker -> team services
    f.arrow([(624, 246), (652, 246), (652, 216), (1032, 216)], color=LINK)  # api -> platform services
    f.arrow([(964, 490), (1032, 490)], color=LINK)                      # ai tier -> ai services
    f.arrow([(200, 508), (436, 508)], dashed=True)                      # local node -> ai tier
    f.arrow([(448, 608), (500, 608)], dashed=True)                      # actions -> hub
    f.arrow([(700, 608), (752, 608)], dashed=True)                      # hub -> dokploy
    f.arrow([(852, 584), (852, 548)], dashed=True)                      # dokploy -> vps

    # nodes
    f.node(40, 112, 160, 56, "Users", "4 project roles")
    f.node(40, 232, 160, 56, "Cloudflare", "DNS·TLS·proxy", "managed")
    f.node(252, 232, 136, 56, "Traefik", ":80 · :443")
    f.node(436, 124, 188, 56, "Web App", "Next.js 16")
    f.node(436, 232, 188, 56, "Platform API", "FastAPI · Python", "focal")
    f.node(436, 340, 188, 56, "Integration\nWorker", "", "svc")
    f.node(676, 124, 168, 56, "Cloudflare R2", "S3 API · files", "managed")
    f.node(676, 232, 168, 56, "Platform DB", "PostgreSQL 16", "svc")
    f.node(436, 472, 528, 52, "AI PI Service + 5 stage engines", "shared AI Engine runtime · fig. 2", "focal")
    f.node(44, 482, 156, 52, "Local Node", "aggregates only")
    for i, (n, s) in enumerate([("Google Identity", "OAuth 2.0 sign-in"), ("Resend", "OTP · notices"),
                                ("Google Drive", "import · results"), ("Team chat", "Slack·Teams·Discord"),
                                ("External DBs", "read-only import")]):
        f.node(1048, (92, 148, 208, 264, 320)[i], 176, 48, n, s, "ext")
    f.node(1048, 436, 176, 48, "LLM providers", "OpenAI · Gemini", "ext")
    f.node(1048, 492, 176, 48, "Literature APIs", "OpenAlex · arXiv", "ext")
    f.node(248, 584, 200, 48, "GitHub Actions", "build · test", "ext")
    f.node(500, 584, 200, 48, "Docker Hub", "image registry", "ext")
    f.node(752, 584, 200, 48, "Dokploy", "deploy on VPS", "svc")

    # labels
    f.label(120, 212, "HTTPS", "right")
    f.label(530, 216, "REST", "right")
    f.label(940, 216, "Auth · email")
    f.label(404, 400, "HTTP", "left")
    f.label(900, 380, "Delivery")
    f.label(318, 508, "Aggregates")
    f.label(852, 566, "Deploy", "right")

    legend = [("focal", "focal component"), ("managed", "managed / outside VPS"),
              ("solid", "request"), ("link", "leaves the VPS"), ("dashed", "async / deploy")]
    desc = ("Users reach Cloudflare and Traefik on one Linux VPS, which routes to the Web App and the Platform "
            "API; the API uses PostgreSQL, Cloudflare R2 and the AI research tier, the Integration Worker "
            "delivers results, the Local Node sends only aggregates, and Dokploy deploys images from Docker Hub.")
    return page("sysarch-v3-overview", "Architecture · OpenAI-Scientist · Figure 1",
                "System architecture",
                f.svg("sysarch-v3-overview", "OpenAI-Scientist system architecture", desc, legend))


# =====================================================================================
# Figure 2 - the AI research tier in detail
# =====================================================================================
def ai_tier():
    f = Figure()
    f.zone(232, 72, 768, 360, "AI research tier · on the VPS", "ai")
    f.zone(248, 220, 736, 196, "Shared AI Engine runtime · one container per engine", "ai", dashed=True)
    f.zone(232, 480, 560, 120, "Data holder · Local Node", "ext", dashed=True)
    f.zone(1032, 180, 208, 252, "AI services", "ext", dashed=True)

    EX, EW, EG, EY, EH = 264, 124, 24, 268, 100
    stages = [("Dataset", "DatasetSnapshot"), ("Hypothesis", "HypothesisSet"),
              ("Experiment\nDesign", "AnalysisPlan"), ("Execution", "EvidenceBundle"), ("Paper", "PaperPack")]

    # arrows
    f.arrow([(200, 318), (264, 318)])                                   # api -> engines (HTTP)
    f.arrow([(120, 272), (120, 140), (264, 140)])                       # api -> ai pi (consult)
    f.arrow([(264, 164), (176, 164), (176, 272)], dashed=True)          # ai pi -> api (advice)
    for i in range(4):
        x = EX + i * (EW + EG) + EW
        f.arrow([(x, EY + EH / 2), (x + EG, EY + EH / 2)])
    f.arrow([(968, 152), (1200, 152), (1200, 220)], color=LINK)         # ai pi -> llm
    f.arrow([(984, 290), (1040, 290)], color=LINK)                      # engines -> llm
    f.arrow([(984, 380), (1040, 380)], color=LINK)                      # engines -> literature
    f.arrow([(460, 416), (460, 516)], dashed=True)                      # engines -> local node (jobs)
    f.arrow([(520, 540), (568, 540)])                                   # local node -> release gate
    f.arrow([(680, 516), (680, 416)])                                   # release gate -> engines

    # nodes
    f.node(40, 272, 160, 64, "Platform API", "runs the stages", "focal")
    f.node(264, 120, 704, 64, "AI PI Service", "oversight · advises at stage end, failure and close", "focal")
    for i, (n, art) in enumerate(stages):
        f.node(EX + i * (EW + EG), EY, EW, EH, n, art)
    f.node(248, 516, 272, 48, "Local Node", "runs jobs next to the data")
    f.node(568, 516, 208, 48, "Release Gate", "small-cell · rounding")
    f.node(1040, 220, 192, 88, "LLM providers", "OpenAI·Gemini·OpenRouter", "ext")
    f.node(1040, 336, 192, 88, "Literature APIs", "OpenAlex · arXiv · …", "ext")

    # labels
    f.label(120, 200, "Consult", "left")
    f.label(176, 200, "Advice", "right")
    f.label(1036, 152, "Prompts")
    f.label(452, 456, "Jobs", "left")
    f.label(688, 456, "Aggregates", "right")
    f.callout(808, 556, "Data rows never leave the node.")
    f.callout(808, 468, "Only text and schemas reach models.")

    legend = [("focal", "focal component"), ("ext", "outside the VPS"),
              ("solid", "call"), ("link", "HTTPS to a provider"), ("dashed", "async")]
    desc = ("The Platform API runs five stage engines on a shared AI Engine runtime and consults the AI PI "
            "Service; engines call LLM providers and literature APIs, and send jobs to the Local Node, whose "
            "aggregates return only through the Release Gate.")
    return page("sysarch-v3-ai-tier", "Architecture · OpenAI-Scientist · Figure 2",
                "AI research tier",
                f.svg("sysarch-v3-ai-tier", "OpenAI-Scientist AI research tier", desc, legend))


if __name__ == "__main__":
    for name, html in (("System-Architecture-v3-overview.html", overview()),
                       ("System-Architecture-v3-ai-tier.html", ai_tier())):
        (HERE / name).write_text(html)
        print("written", HERE / name)

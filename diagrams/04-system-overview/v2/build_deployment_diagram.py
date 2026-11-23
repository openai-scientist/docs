"""Deployment Diagram v2 of LOGOS production (Report 7, IV 1.1.2, Figure IV-2).

usage: python3 build_deployment_diagram.py

Sources: logos/deploy/docker-compose.prod.yml (services, volumes, network capstone-net),
ai-research-platform-fe/docker/docker-compose.prod.yml (fe) and logos/services/runner
(the Local Node runner calls the Platform API over HTTPS).
UML 2.5 deployment notation with flat boxes: the stereotype names the node kind.
No notes on the canvas.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'Deployment-Diagram-Production.drawio'
FONT = 'fontFamily=Arial;fontColor=#000000;'
BOX = f'rounded=0;html=1;whiteSpace=wrap;{FONT}fontSize=13;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#000000;'
FRAME = f'rounded=0;html=1;whiteSpace=wrap;{FONT}fontSize=14;align=left;verticalAlign=top;spacingLeft=12;spacingTop=6;fillColor=none;strokeColor=#000000;'
EDGE = f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;{FONT}fontSize=12;strokeColor=#000000;labelBackgroundColor=#ffffff;endArrow=none;'
cells = []


def label(kind, name, *lines):
    extra = ''.join(f'<br>{escape(l)}' for l in lines)
    return f'«{kind}»<br><b style="font-size:15px">{escape(name)}</b>{extra}'


def box(id_, value, x, y, w, h, style=BOX):
    cells.append(f'<mxCell id="{id_}" value="{escape(value)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def path(a, b, text='', exit_=None, entry=None, pts=()):
    st = EDGE
    if exit_:
        st += f'exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;'
    if entry:
        st += f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;'
    arr = ''.join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in pts)
    arr = f'<Array as="points">{arr}</Array>' if arr else ''
    cells.append(f'<mxCell id="p{len(cells)}" value="{escape(text)}" style="{st}" edge="1" parent="1" source="{a}" '
                 f'target="{b}"><mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')


# --- outside the VPS: the runner next to the owner's data, the browser and the edge
box('local', label('device', 'Local Node', '«artifact» capstone-runner'), 100, 70, 300, 100)
box('browser', label('device', 'User browser'), 470, 70, 300, 100)
box('cf', label('cloud service', 'Cloudflare', 'DNS, proxy, TLS'), 470, 240, 300, 100)
path('browser', 'cf', 'HTTPS')
path('local', 'cf', 'HTTPS', (0.5, 1), (0, 0.5), [(250, 290)])

# --- the VPS and its Docker engine
VPS = (40, 410, 1200, 1020)
box('vps', '«device»<br><b>Linux VPS</b>', *VPS, style=FRAME)
box('docker', '«executionEnvironment»<br><b>Docker Engine</b> (Dokploy, network capstone-net)', 70, 480, 1140, 920,
    style=FRAME)

box('traefik', label('executionEnvironment', 'traefik', '«artifact» Dokploy reverse proxy :80 / :443'),
    470, 560, 300, 100)
box('fe', label('executionEnvironment', 'fe', '«artifact» capstone-fe, Next.js :3000'), 180, 730, 300, 100)
box('api', label('executionEnvironment', 'api', '«artifact» capstone-be, FastAPI :8080'), 700, 730, 300, 100)
box('migrate', label('executionEnvironment', 'migrate', '«artifact» capstone-be, Alembic'), 100, 900, 250, 100)
box('worker', label('executionEnvironment', 'integration-worker', '«artifact» capstone-be'), 385, 900, 225, 100)
box('db', label('executionEnvironment', 'db', '«artifact» postgres:16-alpine', 'volume platform_db_data'),
    700, 900, 300, 100)
box('backup', label('executionEnvironment', 'backup', '«artifact» capstone-be, rclone', 'volume backup_work'),
    700, 1060, 300, 100)

path('cf', 'traefik', 'HTTPS', (0.5, 1), (0.5, 0))
path('traefik', 'fe', 'HTTP :3000', (0.25, 1), (0.5, 0), [(545, 695), (330, 695)])
path('traefik', 'api', 'HTTP :8080', (0.75, 1), (0.5, 0), [(695, 695), (850, 695)])
path('fe', 'api', 'HTTP')
path('api', 'db', 'TCP 5432')
path('worker', 'db', 'TCP 5432')
path('migrate', 'db', 'TCP 5432', (0.5, 1), (0.15, 1), [(225, 1030), (745, 1030)])
path('db', 'backup', 'TCP 5432', (0.7, 1), (0.7, 0))

# stage engines and the AI PI, one row fed by one HTTP fan from the api
ENG = [('oversight', 'oversight_runs'), ('dataset', 'dataset_runs'), ('hypothesis', 'hypothesis_runs'),
       ('experiment-design', 'experiment_design_runs'), ('execution', 'execution_runs'), ('writing', 'writing_runs')]
EW, EG = 172, 14
for i, (name, vol) in enumerate(ENG):
    x = 100 + i * (EW + EG)
    box(f'eng{i}', f'«executionEnvironment»<br><b style="font-size:15px">{name}</b><br>«artifact»<br>capstone-{name}'
        f'<br>volume {vol}', x, 1240, EW, 130, BOX.replace('fontSize=13', 'fontSize=12'))
    path('api', f'eng{i}', 'HTTP' if i == 5 else '', (1, 0.5), (0.5, 0), [(1170, 780), (1170, 1200), (x + EW / 2, 1200)])

# --- external services, one communication path each from the VPS
EXT = [('hub', 'Docker Hub', '', 'HTTPS, pulls images'), ('r2', 'Cloudflare R2', 'object storage', 'HTTPS, S3 API (api)'),
       ('google', 'Google APIs', 'sign-in, Drive', 'HTTPS (api, worker)'), ('resend', 'Resend', 'email', 'HTTPS (api)'),
       ('llm', 'LLM providers', 'OpenAI, Gemini, OpenRouter', 'HTTPS (engines, oversight)'),
       ('lit', 'Literature APIs', 'OpenAlex, arXiv', 'HTTPS (hypothesis)'),
       ('offsite', 'Off-site backup storage', 'rclone remote', 'HTTPS (backup)')]
for i, (id_, name, desc, proto) in enumerate(EXT):
    y = 440 + i * 135
    box(id_, label('cloud service', name, *([desc] if desc else [])), 1460, y, 320, 95)
    path('vps', id_, proto, (1, round((y + 47.5 - VPS[1]) / VPS[3], 4)), (0, 0.5))

cells.insert(0, f'<mxCell id="frame" value="dep OpenAI-Scientist production" style="shape=umlFrame;whiteSpace=wrap;html=1;width=300;'
             f'height=32;{FONT}fontSize=14;fontStyle=1;strokeColor=#000000;fillColor=none;" vertex="1" parent="1">'
             '<mxGeometry x="10" y="10" width="1810" height="1450" as="geometry"/></mxCell>')
OUT.write_text('<mxfile><diagram name="Deployment-Diagram-Production"><mxGraphModel grid="1" gridSize="10" '
               'background="#ffffff"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + ''.join(cells)
               + '</root></mxGraphModel></diagram></mxfile>')
print('written', OUT)

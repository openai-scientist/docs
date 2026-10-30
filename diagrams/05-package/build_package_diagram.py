"""Package diagram (.drawio) of OpenAI-Scientist, from the code layout of the two product repos.

usage: build_package_diagram.py out.drawio

Sources:
- web app: ai-research-platform-fe/src (Next.js)
- Platform: logos/services/management/src/management; the layers follow the import-linter
  contract "Feature layering" in services/management/pyproject.toml
- engines and shared libraries: logos/services/oversight, logos/stages/*, logos/packages/*
Dependencies point from the user to the used package. Inside a layered frame only adjacent
layers are drawn; a higher layer may use any lower one.
"""
import sys
from html import escape

out = sys.argv[1]
cells = []
# black and white like the SEP490 sample and diagrams/README.md: names only, descriptions go in the table
PKG = ('shape=folder;tabWidth={tw};tabHeight=22;tabPosition=left;html=1;whiteSpace=wrap;verticalAlign={va};'
       'align=center;spacingTop={st};fontFamily=Arial;fontSize=12;fontStyle=1;fillColor=#ffffff;strokeColor=#000000;')


def pkg(id_, name, x, y, w, h, note='', frame=False, fill=None, stroke=None):
    # UML: a package drawn with its members carries its name in the tab, otherwise in the body
    style = PKG.format(tw=80, va='middle', st=18)
    if frame:
        style = PKG.format(tw=min(w - 20, 8 * len(name) + 20), va='top', st=2).replace('align=center', 'align=left;spacingLeft=6')
    cells.append(f'<mxCell id="{id_}" value="{escape(name)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def dep(a, b, label='', exit_=None, entry=None):
    pts = ''
    if exit_:
        pts += f'exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;'
    if entry:
        pts += f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;'
    cells.append(f'<mxCell id="d_{a}_{b}" value="{escape(label)}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;'
                 f'html=1;dashed=1;endArrow=open;endFill=0;strokeColor=#000000;fontFamily=Arial;fontSize=11;labelBackgroundColor=#ffffff;{pts}" '
                 f'edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')


BW, BH = 200, 70  # package box

# --- Web App (Next.js)
pkg('fe', 'ai-research-platform-fe', 40, 80, 1460, 470, frame=True, fill='#f5f9ff', stroke='#6c8ebf')
pkg('fe_app', 'app', 670, 130, BW, BH, 'routes: (main), (external), api')
row = [('fe_components', 'components', 'shared UI, shadcn/ui'), ('fe_hooks', 'hooks', 'TanStack Query hooks'),
       ('fe_server', 'server', 'server actions, auth'), ('fe_stores', 'stores', 'client preferences')]
for i, (id_, n, note) in enumerate(row):
    pkg(id_, n, 250 + i * 280, 260, BW, BH, note)
    dep('fe_app', id_)
pkg('fe_lib', 'lib', 670, 380, BW, BH, 'API client, auth, realtime, run-stream')
for id_, *_ in row:
    dep(id_, 'fe_lib', exit_=(0.5, 1), entry=(0.5, 0))
pkg('fe_types', 'types', 1100, 380, BW, BH, 'API models, enums')
dep('fe_lib', 'fe_types')

# --- Platform: management service (FastAPI)
pkg('mg', 'management', 40, 610, 900, 1080, frame=True, fill='#f7fbf3', stroke='#82b366')
layers = [
    [('mg_monitoring', 'monitoring', 'health, alerts'), ('mg_research', 'research', 'runs, stages, PI, budget, reviews')],
    [('mg_datasets', 'datasets', 'datasets, versions')],
    [('mg_connections', 'connections', 'external data sources')],
    [('mg_projects', 'projects', 'projects, members, settings')],
    [('mg_integrations', 'integrations', 'Google, project integrations')],
    [('mg_identity', 'identity', 'sign-in, OTP, sessions'), ('mg_notifications', 'notifications', 'in-app, email')],
    [('mg_audit', 'audit', 'audit events'), ('mg_access', 'access', 'platform roles, guards')],
]
y = 690
prev = []
for layer in layers:
    xs = [390] if len(layer) == 1 else [230, 550]
    for (id_, n, note), x in zip(layer, xs):
        pkg(id_, n, x, y, BW, BH, note)
    ids = [l[0] for l in layer]
    for a in prev:
        for b in ids:
            if len(prev) == 2 and len(ids) == 2 and prev.index(a) != ids.index(b):
                continue  # parallel pairs: draw straight down only
            dep(a, b)
    prev = ids
    y += 120
# foundation layer: core : db : infra are siblings in one layer
pkg('mg_found', '«layer» foundation', 120, y, 740, 140, frame=True, fill='#ffffff', stroke='#82b366')
for i, (id_, n, note) in enumerate([('mg_core', 'core', 'config, errors, service client'),
                                    ('mg_db', 'db', 'SQLAlchemy session, Alembic'),
                                    ('mg_infra', 'infra', 'email, file store (R2), secret box')]):
    pkg(id_, n, 150 + i * 240, y + 55, BW, BH, note)
for a in prev:
    dep(a, 'mg_found')

# --- Engines (separate HTTP services)
pkg('en', 'engines', 1000, 610, 500, 640, frame=True, fill='#fffaf0', stroke='#d6b656')
for i, (id_, n, note) in enumerate([('en_oversight', 'logos_oversight', 'AI PI: consult, findings'),
                                    ('en_dataset', 'logos_dataset', 'stage dataset'),
                                    ('en_hypothesis', 'logos_hypothesis', 'stage hypothesis, literature'),
                                    ('en_design', 'logos_experiment_design', 'stage experiment-design')]):
    pkg(id_, n, 1110, 700 + i * 140, 280, BH + 10, note)

# --- Shared libraries
pkg('sh', 'packages', 1000, 1360, 500, 380, frame=True, fill='#f9f4fb', stroke='#9673a6')
pkg('sh_engine', 'logos_engine', 1110, 1420, 280, BH + 10, 'Harness runtime, testing kit')
pkg('sh_contract', 'logos_contract', 1110, 1620, 280, BH + 10, 'hand-off artifacts, activity, API paths')
dep('sh_engine', 'sh_contract')
dep('en', 'sh_engine', '«import»', exit_=(0.3, 1), entry=(0.2, 0))

# --- cross sub-system dependencies
dep('fe_lib', 'mg', '«use» HTTP REST / SSE', exit_=(0.5, 1), entry=(0.6, 0))
dep('mg_research', 'en', '«use» HTTP', exit_=(1, 0.25), entry=(0, 0.1))
dep('mg_research', 'sh_contract', '«import»', exit_=(1, 0.8), entry=(0, 0.5))
dep('en', 'sh_contract', '«import»', exit_=(1, 0.95), entry=(1, 0.5))

# UML frame "pkg <name>" around the whole diagram
cells.insert(0, '<mxCell id="frame" value="pkg OpenAI-Scientist" style="shape=umlFrame;whiteSpace=wrap;html=1;'
             'width=190;height=28;fontFamily=Arial;fontSize=12;fontStyle=1;strokeColor=#000000;fillColor=none;" '
             'vertex="1" parent="1"><mxGeometry x="10" y="20" width="1520" height="1770" as="geometry"/></mxCell>')
xml = ('<mxfile><diagram name="Package Diagram"><mxGraphModel grid="1" gridSize="10"><root><mxCell id="0"/>'
       '<mxCell id="1" parent="0"/>' + ''.join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open(out, 'w').write(xml)

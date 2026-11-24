"""Package diagram (.drawio) of LOGOS, from the code layout of the two product repos.

usage: build_package_diagram.py out.drawio

Sources:
- web app: ai-research-platform-fe/src (Next.js)
- Platform: logos/services/management/src/management; the layers follow the import-linter
  contract "Feature layering" in services/management/pyproject.toml
- engines, data job runner and shared libraries: logos/services/oversight, logos/stages/*,
  logos/services/runner, logos/packages/*; package dependencies from each pyproject.toml
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
    if id_.startswith('fe_'):
        x += 145  # centre the web app packages in the widened frame
    style = PKG.format(tw=80, va='middle', st=18)
    if frame:
        style = PKG.format(tw=min(w - 20, 8 * len(name) + 20), va='top', st=2).replace('align=center', 'align=left;spacingLeft=6')
    cells.append(f'<mxCell id="{id_}" value="{escape(name)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def dep(a, b, label='', exit_=None, entry=None, via=None):
    pts = ''
    if exit_:
        pts += f'exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;'
    if entry:
        pts += f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;'
    cells.append(f'<mxCell id="d_{a}_{b}" value="{escape(label)}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;'
                 f'html=1;dashed=1;endArrow=open;endFill=0;strokeColor=#000000;fontFamily=Arial;fontSize=11;labelBackgroundColor=#ffffff;{pts}" '
                 f'edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry">'
                 + (('<Array as="points">' + ''.join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in via) + '</Array>') if via else '')
                 + '</mxGeometry></mxCell>')


BW, BH = 200, 70  # package box

# --- Web App (Next.js)
pkg('fe', 'ai-research-platform-fe', 40, 80, 1750, 470, frame=True, fill='#f5f9ff', stroke='#6c8ebf')
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

# --- services: the three deployable services of logos/services
pkg('sv', 'services', 40, 610, 1250, 1200, frame=True)

# management (FastAPI), layered by the import-linter contract "Feature layering"
pkg('mg', 'management', 60, 660, 900, 1120, frame=True)
layers = [
    [('mg_monitoring', 'monitoring'), ('mg_research', 'research')],
    [('mg_datasets', 'datasets'), ('mg_runners', 'runners')],
    [('mg_connections', 'connections')],
    [('mg_projects', 'projects')],
    [('mg_integrations', 'integrations')],
    [('mg_identity', 'identity'), ('mg_notifications', 'notifications')],
    [('mg_audit', 'audit'), ('mg_access', 'access')],
]
y = 740
prev = []
for layer in layers:
    xs = [410] if len(layer) == 1 else [250, 570]
    for (id_, n), x in zip(layer, xs):
        pkg(id_, n, x, y, BW, BH)
    ids = [l[0] for l in layer]
    for a in prev:
        for b in ids:
            if len(prev) == 2 and len(ids) == 2 and prev.index(a) != ids.index(b):
                continue  # parallel pairs: draw straight down only
            dep(a, b)
    prev = ids
    y += 120
# core : db : infra are independent siblings of the lowest layer (no package of their own)
for id_, n, x in [('mg_db', 'db', 170), ('mg_core', 'core', 410), ('mg_infra', 'infra', 650)]:
    pkg(id_, n, x, y + 20, BW, BH)
dep('mg_audit', 'mg_db', exit_=(0.3, 1), entry=(0.7, 0))
dep('mg_audit', 'mg_core', exit_=(1, 0.5), entry=(0.5, 0))
dep('mg_access', 'mg_core', exit_=(0.5, 1), entry=(0.75, 0))

pkg('sv_oversight', 'oversight', 1025, 740, 210, BH)
pkg('sv_runner', 'runner', 1025, 1000, 210, BH)

# --- stages: the five stage engines (separate HTTP services)
pkg('st', 'stages', 1330, 610, 460, 400, frame=True)
for i, (id_, n) in enumerate([('st_dataset', 'dataset'), ('st_hypothesis', 'hypothesis'),
                              ('st_design', 'experiment_design'), ('st_execution', 'execution'),
                              ('st_writing', 'writing')]):
    x = 1455 if i == 4 else 1345 + (i % 2) * 225
    pkg(id_, n, x, 670 + (i // 2) * 110, 210, BH)

# --- packages: shared libraries; logos_recompute has no package dependency
pkg('sh', 'packages', 1330, 1060, 460, 460, frame=True)
for id_, n, x, y_ in [('sh_discovery', 'discovery', 1345, 1120), ('sh_recompute', 'recompute', 1490, 1120),
                      ('sh_analysis', 'analysis', 1635, 1120), ('sh_engine', 'engine', 1345, 1250),
                      ('sh_tables', 'tables', 1635, 1250), ('sh_contract', 'contract', 1490, 1400)]:
    pkg(id_, n, x, y_, 140, BH)
dep('sh_discovery', 'sh_engine')
dep('sh_analysis', 'sh_tables')
dep('sh_engine', 'sh_contract', exit_=(0.5, 1), entry=(0.2, 0))
dep('sh_tables', 'sh_contract', exit_=(0.5, 1), entry=(0.8, 0))

# --- cross-package dependencies (Python imports are plain usage, not UML «import»)
dep('fe_lib', 'mg', '«use» HTTP REST / SSE', exit_=(0.5, 1), entry=(0.6, 0))
dep('mg_research', 'sv_oversight', '«use» HTTP', exit_=(1, 0.5), entry=(0, 0.5))
dep('mg_research', 'st', '«use» HTTP', exit_=(0.8, 0), entry=(0, 0.075), via=[(730, 640)])
dep('mg_runners', 'sv_runner', '«use» HTTP', exit_=(1, 0.5), entry=(0, 0.5))
dep('mg', 'sh_contract', '«use»', exit_=(1, 0.85), entry=(0.5, 1))
dep('sv_oversight', 'sh', '«use»', exit_=(1, 0.5), entry=(0, 0.3), via=[(1300, 775), (1300, 1198)])
dep('sv_runner', 'sh', '«use»', exit_=(1, 0.5), entry=(0, 0.1), via=[(1265, 1035), (1265, 1106)])
dep('st', 'sh', '«use»', exit_=(0.5, 1), entry=(0.5, 0))

# UML frame "pkg <name>" around the whole diagram
cells.insert(0, '<mxCell id="frame" value="pkg OpenAI-Scientist" style="shape=umlFrame;whiteSpace=wrap;html=1;'
             'width=170;height=28;fontFamily=Arial;fontSize=12;fontStyle=1;strokeColor=#000000;fillColor=none;" '
             'vertex="1" parent="1"><mxGeometry x="10" y="20" width="1810" height="1820" as="geometry"/></mxCell>')
xml = ('<mxfile><diagram name="Package Diagram"><mxGraphModel grid="1" gridSize="10"><root><mxCell id="0"/>'
       '<mxCell id="1" parent="0"/>' + ''.join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open(out, 'w').write(xml)

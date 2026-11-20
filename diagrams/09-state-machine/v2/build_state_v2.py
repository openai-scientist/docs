"""State Machine Diagrams v2: redraws the Project, Research Run and AI PI tabs from the LOGOS code.

usage: python3 build_state_v2.py   (reads ../State-Machine-Diagrams.drawio, writes ./State-Machine-Diagrams.drawio)

Sources (logos/services/management/src/management):
- Project: projects/project_status.py (derived status), projects/router/projects.py (complete, reopen,
  archive, restore)
- Research run: research/models.py, research/stage_runs.py, research/orchestrator.py (budget, stop, reopen)
- AI PI consultation: research/pi/service.py, research/pi/apply.py
Other tabs are copied from v1; tab 7 only loses the "(proposed)" mark on the retry.
"""
import xml.etree.ElementTree as E
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = 'html=1;fontFamily=Arial;fontColor=#000000;strokeColor=#000000;fillColor=#ffffff;strokeWidth=1;'
STATE = BASE + 'rounded=1;absoluteArcSize=1;arcSize=10;whiteSpace=wrap;fontSize=12;'
START = BASE + 'ellipse;fillColor=#000000;fontSize=12;'
END = BASE + 'ellipse;shape=endState;fillColor=#000000;fontSize=12;'
EDGE = (BASE + 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;endArrow=classic;'
        'endSize=7;endFill=1;dashed=0;labelBackgroundColor=#ffffff;fontSize=12;')
W, H = 170, 50


class Page:
    def __init__(self):
        self.root = E.Element('root')
        E.SubElement(self.root, 'mxCell', id='0')
        E.SubElement(self.root, 'mxCell', id='1', parent='0')
        self.n = 0

    def node(self, id_, text, x, y, style=STATE, w=W, h=H):
        c = E.SubElement(self.root, 'mxCell', id=id_, value=text, style=style, vertex='1', parent='1')
        E.SubElement(c, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as': 'geometry'})

    def start(self, x, y):
        self.node('start', '', x - 9, y, START, 18, 18)

    def end(self, id_, x, y):
        self.node(id_, '', x - 11, y, END, 22, 22)

    def edge(self, a, b, text='', exit_=None, entry=None, pts=()):
        st = EDGE
        if exit_:
            st += f'exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;'
        if entry:
            st += f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;'
        self.n += 1
        c = E.SubElement(self.root, 'mxCell', id=f'e{self.n}', value=text, style=st, edge='1', parent='1',
                         source=a, target=b)
        g = E.SubElement(c, 'mxGeometry', relative='1', **{'as': 'geometry'})
        if pts:
            arr = E.SubElement(g, 'Array', **{'as': 'points'})
            for px, py in pts:
                E.SubElement(arr, 'mxPoint', x=str(px), y=str(py))


def project():
    p = Page()
    cx = 300  # centre column
    p.start(cx, 40)
    p.node('draft', 'Draft', cx - W / 2, 100)
    p.node('ready', 'Data ready', cx - W / 2, 240)
    p.node('researching', 'Researching', cx - W / 2, 380)
    p.node('review', 'Needs review', 560, 380)
    p.node('completed', 'Completed', 560, 240)
    p.node('archived', 'Archived\n(read-only)', 560, 100)
    p.edge('start', 'draft')
    p.edge('draft', 'ready', 'dataset version added')
    p.edge('ready', 'researching', 'run started', (0.3, 1), (0.3, 0))
    p.edge('researching', 'ready', 'run ended', (0.7, 0), (0.7, 1))
    p.edge('researching', 'review', 'stage awaits review', (1, 0.3), (0, 0.3))
    p.edge('review', 'researching', 'review answered', (0, 0.7), (1, 0.7))
    p.edge('ready', 'completed', 'marked complete\n[no active run]', (1, 0.3), (0, 0.3))
    p.edge('completed', 'ready', 'reopened', (0, 0.7), (1, 0.7))
    p.edge('completed', 'archived', 'archived', (0.3, 0), (0.3, 1))
    p.edge('archived', 'completed', 'restored', (0.7, 1), (0.7, 0))
    return p


def run():
    p = Page()
    p.node('start', '', 152, 256, START, 18, 18)
    p.node('queued', 'Queued', 240, 240)
    p.node('running', 'Running', 515, 240)
    p.node('review', 'Awaiting review', 820, 240)
    p.node('paused', 'Paused', 240, 90)
    p.node('budget', 'Budget exceeded', 820, 90)
    p.node('stopped', 'Stopped', 240, 370)
    p.node('failed', 'Failed', 515, 470)
    p.node('completed', 'Completed', 820, 470)
    p.edge('start', 'queued')
    p.edge('queued', 'running', 'stage started')
    p.edge('running', 'review', 'gate opened', (1, 0.3), (0, 0.3))
    p.edge('review', 'running', 'reviewer decided', (0, 0.7), (1, 0.7))
    p.edge('running', 'paused', 'paused', (0.15, 0), (1, 0.8), [(540.5, 130)])
    p.edge('paused', 'running', 'resumed', (1, 0.4), (0.35, 0), [(574.5, 110)])
    p.edge('running', 'budget', 'budget used up', (0.85, 0), (0, 0.8), [(659.5, 130)])
    p.edge('budget', 'running', 'budget raised', (0, 0.4), (0.65, 0), [(625.5, 110)])
    p.edge('running', 'stopped', 'run stopped', (0.2, 1), (1, 0.5), [(549, 395)])
    p.edge('running', 'failed', 'stage failed')
    p.edge('review', 'completed', 'last stage accepted')
    for s, x, y in (('stopped', 325, 470), ('failed', 600, 570), ('completed', 905, 570)):
        p.end(f'{s}-end', x, y)
        p.edge(s, f'{s}-end')
    return p


def pi():
    p = Page()
    p.start(300, 40)
    p.node('queued', 'Queued', 215, 100)
    p.node('sent', 'Sent to AI PI', 215, 230)
    p.node('decided', 'Decided', 20, 380)
    p.node('awaiting', 'Awaiting researcher', 410, 380)
    p.node('failed', 'Failed', 600, 230)
    p.node('applied', 'Applied', 20, 540)
    p.node('stale', 'Stale', 215, 540)
    p.node('endorsed', 'Endorsed', 410, 540)
    p.node('overridden', 'Overridden', 600, 540)
    p.edge('start', 'queued')
    p.edge('queued', 'sent', 'request sent')
    p.edge('sent', 'decided', 'PI decides', (0.3, 1), (0.5, 0), [(266, 330), (105, 330)])
    p.edge('sent', 'awaiting', 'PI hands over', (0.7, 1), (0.5, 0), [(334, 330), (495, 330)])
    p.edge('sent', 'failed', 'PI cannot decide')
    p.edge('decided', 'applied', 'decision applied')
    p.edge('decided', 'stale', 'run moved on', (1, 0.8), (0.5, 0), [(300, 420)])
    p.edge('awaiting', 'endorsed', 'researcher endorses')
    p.edge('awaiting', 'overridden', 'researcher overrides', (1, 0.5), (0.3, 0), [(651, 405)])
    p.edge('failed', 'overridden', 'researcher decides', (0.7, 1), (0.7, 0))
    for s, x in (('applied', 105), ('stale', 300), ('endorsed', 495), ('overridden', 685)):
        p.end(f'{s}-end', x, 650)
        p.edge(s, f'{s}-end')
    return p


tree = E.parse(HERE.parent / 'State-Machine-Diagrams.drawio')
pages = tree.getroot().findall('diagram')
for idx, fn in ((1, project), (3, run), (5, pi)):
    model = pages[idx].find('mxGraphModel')
    model.remove(model.find('root'))
    model.append(fn().root)
for c in pages[6].iter('mxCell'):
    if c.get('value') and '(proposed)' in c.get('value'):
        c.set('value', c.get('value').replace(' (proposed)', '').replace('(proposed)', '').strip())
out = HERE / 'State-Machine-Diagrams.drawio'
tree.write(out, encoding='utf-8', xml_declaration=True)
print('written', out)

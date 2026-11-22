"""Build one Screen Flow tab per role, following the LOGOS screen list (SC-01..SC-30).
Each tab starts at a UML start node and enters Sign In; boxes read "SC-xx Name" so they
match the Screen Descriptions table row for row. Layout is a compact tree computed here.
usage: python3 build_role_tabs.py   (run inside diagrams/02-screen-flow/v2)"""
import xml.etree.ElementTree as ET

FILE = 'Screen-Flow-Diagram.drawio'
W, H = 200, 56
SCREENS = {
    1: 'Sign In', 2: 'Verify Code', 3: 'Onboarding', 4: 'Unauthorized',
    5: 'Project List', 6: 'Project Overview', 7: 'Project Settings', 8: 'Documents',
    9: 'Research Case', 10: 'Datasets', 11: 'Dataset Detail', 12: 'Data Connections',
    13: 'Hypothesis Workspace', 14: 'Design Workspace', 15: 'Run Studio',
    16: 'Results & Dossier', 17: 'Manuscript', 18: 'Task Inbox', 19: 'Review Workspace',
    20: 'Admin Overview', 21: 'Users', 22: 'User Detail', 23: 'All Projects',
    24: 'Models & Keys', 25: 'Policies & Settings', 26: 'Usage & Budget',
    27: 'Operations Dashboard', 28: 'Incidents & Support Access', 29: 'Audit Log', 30: 'Local Nodes',
}
SIGN_IN = [('start', 1), (1, 2), (2, 3)]            # first sign-in goes through onboarding
CASE = [(6, 9), (6, 8), (6, 12), (6, 30), (6, 10), (10, 11),
        (9, 13), (9, 14), (9, 15), (9, 16), (16, 17)]
ROLES = {
    'Researcher': SIGN_IN + [(3, 5), (5, 4), (5, 6), (5, 18)] + CASE,
    'Project Manager': SIGN_IN + [(3, 5), (5, 4), (5, 6), (5, 18), (6, 7)] + CASE,
    'Reviewer': SIGN_IN + [(3, 5), (5, 4), (5, 6), (5, 18), (18, 19)],
    'Tenant Admin': SIGN_IN + [(3, 20), (20, 21), (21, 22), (20, 23), (20, 24), (20, 25), (20, 26), (20, 18)],
    'Platform Operator': SIGN_IN + [(3, 27), (27, 28), (27, 29), (27, 18)],
}
BOX = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=13;'
START = 'ellipse;html=1;fillColor=#000000;strokeColor=#000000;'
EDGE = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;'
        'strokeColor=#000000;exitX=0.5;exitY=1;entryX=0.5;entryY=0;')


IND = 30   # indent of a stacked leaf column, leaving room for its trunk line


def layout(edges, gx=30, gy=40):
    """Compact tree. Leaf children stack in one indented column under their parent
    (joined by a trunk line); children with their own children spread side by side.
    Each subtree keeps its own column band, so connector lines never share a segment.
    Returns ({node: (centre x, centre y)}, {(parent, child): stacked?})."""
    kids = {}
    for a, b in edges:
        kids.setdefault(a, []).append(b)
    leaves = lambda n: [c for c in kids.get(n, []) if c not in kids]
    inner = lambda n: [c for c in kids.get(n, []) if c in kids]
    def stack(n):    # leaves of n stack when they are more than one, or sit next to inner children
        return len(leaves(n)) > 1 or (leaves(n) and inner(n))
    def size(n):
        if n not in kids: return W, H
        parts = [size(c) for c in inner(n)] + ([(IND + W, len(leaves(n)) * (H + gy) - gy)] if stack(n) else
                                               [size(c) for c in leaves(n)])
        w = max(W, sum(p[0] for p in parts) + gx * (len(parts) - 1))
        return w, H + gy + max(p[1] for p in parts)
    pos, stacked = {}, {}
    def place(n, left, top):
        w, _ = size(n)
        if n not in kids:
            pos[n] = (left + W / 2, top + H / 2); return
        x = left
        parts = (['STACK'] if stack(n) else []) + inner(n) + ([] if stack(n) else leaves(n))
        tw = sum((IND + W) if p == 'STACK' else size(p)[0] for p in parts) + gx * (len(parts) - 1)
        x = left + (w - tw) / 2
        pos[n] = (x + W / 2 if stack(n) else left + w / 2, top + H / 2)
        for p in parts:
            if p == 'STACK':
                for i, c in enumerate(leaves(n)):
                    pos[c] = (x + IND + W / 2, top + H + gy + i * (H + gy) + H / 2); stacked[(n, c)] = True
                x += IND + W + gx
            else:
                place(p, x, top + H + gy); x += size(p)[0] + gx
    place('start', 20, 20)
    return pos, stacked


tree = ET.parse(FILE); mx = tree.getroot()
model_attrs = next(mx.iter('mxGraphModel')).attrib
for role, edges in ROLES.items():
    name = f'Screen Flow - {role}'
    for d in [d for d in mx.iter('diagram') if d.get('name') == name]: mx.remove(d)
    pos, stacked = layout(edges)
    d = ET.SubElement(mx, 'diagram', {'id': 'role-' + role.lower().replace(' ', '-'), 'name': name})
    root = ET.SubElement(ET.SubElement(d, 'mxGraphModel', dict(model_attrs)), 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'}); ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    for n, (x, y) in pos.items():
        w, h = (30, 30) if n == 'start' else (W, H)
        label = '' if n == 'start' else f'SC-{int(n):02d}<br><b>{SCREENS[int(n)]}</b>'
        c = ET.SubElement(root, 'mxCell', {'id': f'n{n}', 'value': label, 'style': START if n == 'start' else BOX,
                                           'vertex': '1', 'parent': '1'})
        ET.SubElement(c, 'mxGeometry', {'x': f'{x - w / 2:.0f}', 'y': f'{y - h / 2:.0f}',
                                        'width': str(w), 'height': str(h), 'as': 'geometry'})
    for i, (a, b) in enumerate(edges):
        style = EDGE.replace('exitX=0.5;', f'exitX={IND / 2 / W};').replace('entryX=0.5;entryY=0;', 'entryX=0;entryY=0.5;') \
            if stacked.get((a, b)) else EDGE
        e = ET.SubElement(root, 'mxCell', {'id': f'e{i}', 'edge': '1', 'parent': '1', 'style': style,
                                           'source': f'n{a}', 'target': f'n{b}'})
        ET.SubElement(e, 'mxGeometry', {'relative': '1', 'as': 'geometry'})
    print(name, len(pos) - 1, 'screens', len(edges), 'links')
tree.write(FILE, encoding='utf-8', xml_declaration=False)

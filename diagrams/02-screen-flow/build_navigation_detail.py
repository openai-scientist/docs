"""Build a screen map: rectangles are screens; rounded boxes are real overlays."""
from pathlib import Path
import argparse
import copy
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
TARGET = HERE / "Screen-Flow-Diagram.drawio"
PAGE_ID = "navigation-detail"
NO_LABELS_ID = "navigation-no-edge-labels"
VERTICAL_ID = "navigation-vertical-bw"
BW_VARIANTS = [
    (PAGE_ID, 'navigation-detail-bw', 'Navigation Detail - B&W'),
    (NO_LABELS_ID, 'navigation-no-edge-labels-bw', 'Navigation No Labels - B&W'),
]
FRONTEND = HERE.parents[2] / 'ai-research-platform-fe' / 'src/app/(main)'
WORK = 'projects/[projectId]/_components/'
AUTH = '(sign-in)/'
NODE_WIDTH = 340
NODE_HEIGHT = 120
VERTICAL_GAP = 20
NODE_FONT = 28
EDGE_FONT = 22
# Explicit screen inventory. Actions and layout containers cannot become nodes.
SCREENS = [
    ('login', 'Sign in', 'screen', AUTH+'auth/login/page.tsx'),
    ('code', 'Email verification', 'screen', AUTH+'auth/_components/email-code-form.tsx'),
    ('link', 'Sign-in link confirmation', 'screen', AUTH+'auth/verify/page.tsx'),
    ('onboarding', 'Onboarding', 'screen', AUTH+'onboarding/page.tsx'),
    ('projects', 'Projects', 'screen', 'projects/(list)/page.tsx'),
    ('invitations', 'Project invitations', 'dialog', 'projects/_components/workspace-projects.tsx'),
    ('new-project', 'New project', 'dialog', 'projects/_components/create-project-dialog.tsx'),
    ('overview', 'Project Overview', 'screen', 'projects/[projectId]/page.tsx'),
    ('research', 'Research flow', 'screen', 'projects/[projectId]/experiments/page.tsx'),
    ('run-form', 'Research run setup', 'dialog', WORK+'run-studio/start-run-dialog.tsx'),
    ('studio', 'Research run workspace', 'screen', WORK+'run-studio/run-workspace.tsx'),
    ('jfe', 'Journal fingerprints', 'dialog', WORK+'run-studio/jfe-workspace.tsx'),
    ('datasets', 'Datasets', 'screen', WORK+'datasets-section.tsx'),
    ('import', 'Connection import', 'dialog', WORK+'dataset-connection-import.tsx'),
    ('dataset', 'Dataset details', 'screen', 'projects/[projectId]/datasets/[datasetId]/page.tsx'),
    ('connections', 'Data Connections', 'screen', WORK+'data-connections/connections-section.tsx'),
    ('connection', 'Source connection setup', 'dialog', WORK+'data-connections/connection-flow.tsx'),
    ('documents', 'Documents', 'screen', WORK+'project-files-section.tsx'),
    ('document', 'Document preview', 'dialog', WORK+'project-file-preview.tsx'),
    ('members', 'Members', 'screen', WORK+'member-directory.tsx'),
    ('settings', 'Project Settings', 'screen', WORK+'settings-section.tsx'),
    ('admin', 'Admin Overview', 'screen', 'admin/page.tsx'),
    ('users', 'Users', 'screen', 'admin/users/page.tsx'),
    ('user', 'User details', 'screen', 'admin/users/[userId]/page.tsx'),
    ('admin-projects', 'Projects (Admin)', 'screen', 'admin/projects/page.tsx'),
    ('admin-project', 'Project details (Admin)', 'screen', 'admin/projects/[projectId]/page.tsx'),
    ('providers', 'Models & Providers', 'screen', 'admin/providers/page.tsx'),
    ('decisions', 'Decision Providers', 'screen', 'admin/decision-providers/page.tsx'),
    ('usage', 'Usage & Cost', 'screen', 'admin/usage/page.tsx'),
    ('health', 'System Health', 'screen', 'admin/system/page.tsx'),
    ('audit', 'Audit Log', 'screen', 'admin/logs/page.tsx'),
    ('monitor', 'Log Monitoring', 'screen', 'admin/log-monitoring/page.tsx'),
    ('admin-settings', 'Settings (Admin)', 'screen', 'admin/settings/page.tsx'),
]
TRANSITIONS = [
    ('login', 'code', 'Enter email / Continue'),
    ('login', 'link', 'Open sign-in email link'),
    ('login', 'onboarding', 'Sign in [first time]'),
    ('login', 'projects', 'Sign in [onboarded User]'),
    ('login', 'admin', 'Sign in [onboarded Admin]'),
    ('projects', 'invitations', 'Review project invitations'),
    ('projects', 'new-project', 'Create a project'),
    ('projects', 'overview', 'Open project workspace'),
    ('overview', 'research', 'Browse research runs'),
    ('research', 'run-form', 'Configure a research run'),
    ('research', 'studio', 'Open a current or saved run'),
    ('research', 'jfe', 'Open journal fingerprints'),
    ('overview', 'datasets', 'Browse project datasets'),
    ('datasets', 'import', 'Import from connection [write]'),
    ('datasets', 'dataset', 'Inspect dataset details'),
    ('overview', 'connections', 'Browse connected data sources'),
    ('connections', 'connection', 'Connect a data source'),
    ('overview', 'documents', 'Browse reference documents'),
    ('documents', 'document', 'Preview a document'),
    ('overview', 'members', 'View project members [non-manager]'),
    ('overview', 'settings', 'Configure project [Project Manager]'),
    ('admin', 'users', 'Browse platform users'),
    ('users', 'user', 'Inspect user account'),
    ('admin', 'admin-projects', 'Browse platform projects'),
    ('admin-projects', 'admin-project', 'Inspect project details'),
    ('admin', 'providers', 'Inspect AI models and providers'),
    ('admin', 'decisions', 'Inspect decision providers'),
    ('admin', 'usage', 'Review usage and spending'),
    ('admin', 'health', 'Inspect system health'),
    ('admin', 'audit', 'Review platform audit events'),
    ('admin', 'monitor', 'Monitor technical events'),
    ('admin', 'admin-settings', 'Configure platform settings'),
]
# Selectable stage views, not the internal processing steps within each stage.
RUN = WORK+'run-studio/'
RUN_STAGES = [
    ('scope', 'Scope', 'scope-scene.tsx'),
    ('search', 'Literature search', 'search-scene.tsx'),
    ('screen', 'Paper screening', 'screen-scene.tsx'),
    ('read', 'Evidence reading', 'read-scene.tsx'),
    ('synthesize', 'Gap synthesis', 'synthesize-scene.tsx'),
    ('hypothesize', 'Hypotheses', 'hypothesize-scene.tsx'),
    ('map', 'Research map', 'map-scene.tsx'),
]
for key, title, filename in RUN_STAGES:
    SCREENS.append(('run-'+key, title, 'screen', RUN+'scenes/'+filename))
    action = {'scope': 'Review research scope', 'search': 'Browse retrieved papers',
              'screen': 'Review screening results', 'read': 'Read evidence cards',
              'synthesize': 'Explore research gaps', 'hypothesize': 'Review proposed hypotheses',
              'map': 'Explore the argument map'}[key]
    TRANSITIONS.append(('studio', 'run-'+key, action))
SCREENS += [
    ('writing', 'Writing workspace', 'screen', RUN+'writing-preview.tsx'),
    ('writing-paper', 'Manuscript', 'screen', RUN+'writing/paper.tsx'),
]
TRANSITIONS += [
    ('studio', 'writing', 'Open writing preview'),
    ('writing', 'writing-paper', 'Read the signed manuscript'),
]


def build():
    original = TARGET.read_text(encoding="utf-8")
    nodes = {}
    screens = [row for row in SCREENS if row[2] == 'screen']
    kept = {row[0] for row in screens}
    transitions = [row for row in TRANSITIONS if row[0] in kept and row[1] in kept]
    for key, title, kind, path in screens:
        assert (FRONTEND / path).is_file(), path
        nodes[key] = ET.Element('mxCell', value=title, kind=kind, path=path)
    edges = [(f'{a}-to-{b}', a, b, ET.Element('mxCell', value=label)) for a, b, label in transitions]

    # A navigation tree gets contiguous subtree bands. This keeps unrelated
    # screens' branches apart even when one workspace has dozens of views.
    children = {key: [] for key in nodes}
    incoming = set()
    for _, a, b, _ in edges:
        assert b not in incoming, f'Duplicate parent for {b}'
        incoming.add(b)
        children[a].append(b)
    roots = set(nodes)-incoming
    assert roots == {'login'}, roots
    positions = {}
    next_leaf = 0

    def place(key, depth):
        nonlocal next_leaf
        for child in children[key]:
            place(child, depth+1)
        if children[key]:
            y = round((positions[children[key][0]][1]+positions[children[key][-1]][1])/20)*10
        else:
            y = 20+next_leaf*(NODE_HEIGHT+VERTICAL_GAP)
            next_leaf += 1
        positions[key] = (40+depth*(NODE_WIDTH+360), y)

    place('login', 0)
    assert positions.keys() == nodes.keys()

    page = ET.Element('diagram', id=PAGE_ID, name='Navigation Detail')
    model = ET.SubElement(page, 'mxGraphModel', grid='1', gridSize='10', page='0', background='#ffffff')
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', id='0')
    ET.SubElement(root, 'mxCell', id='1', parent='0')
    for key, source in nodes.items():
        title = source.get('value', '')
        parts = title.split('\n', 1)
        title = parts[0] + ('' if parts[0].endswith(' Page') else ' Page') + ('\n'+parts[1] if len(parts)>1 else '')
        kind = source.get('kind')
        if kind != 'screen':
            title += f'\n({kind})'
        style = (f'rounded={int(kind != "screen")};arcSize=15;whiteSpace=wrap;html=1;fillColor=#fffbed;strokeColor=#f29b31;'
                 f'strokeWidth=1.5;fontColor=#754314;fontFamily=Arial;fontSize={NODE_FONT};spacing=8;')
        cell = ET.SubElement(root, 'mxCell', id=key, value=title, style=style, vertex='1', parent='1',
                             **{'data-kind': kind, 'data-source-file': source.get('path')})
        x, y = positions[key]
        ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(NODE_WIDTH), height=str(NODE_HEIGHT), **{'as': 'geometry'})

    # Different screens keep separate vertical corridors; only a screen's own
    # branches share a trunk. Otherwise nearby review dialogs look conflated.
    columns = {}
    for a in dict.fromkeys(a for _, a, _, _ in edges):
        columns.setdefault(positions[a][0], []).append(a)
    bends = {}
    for x, sources in columns.items():
        for index, a in enumerate(sorted(sources, key=lambda key: positions[key][1])):
            bends[a] = x + NODE_WIDTH + 40 + index*6
    for key, a, b, source in edges:
        sx, sy = positions[a]
        tx, ty = positions[b]
        label = source.get('value')
        style = ('edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;'
                 'html=1;endArrow=block;endFill=1;strokeColor=#f29b31;strokeWidth=1.5;'
                 f'fontFamily=Arial;fontSize={EDGE_FONT};fontColor=#333333;labelBackgroundColor=#FFFFFF;'
                 'align=center;verticalAlign=middle;spacing=2;whiteSpace=wrap;labelWidth=240;'
                 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
        cell = ET.SubElement(root, 'mxCell', id=key, value=label, style=style, edge='1', parent='1',
                             source=a, target=b)
        geometry = ET.SubElement(cell, 'mxGeometry', relative='1', y='0', **{'as': 'geometry'})
        bend_x = bends[a]
        lengths = [bend_x-sx-NODE_WIDTH, abs(ty-sy), tx-bend_x]
        geometry.set('x', str(1 - lengths[-1] / sum(lengths)))
        array = ET.SubElement(geometry, 'Array', **{'as': 'points'})
        for x, y in [(bend_x, sy+NODE_HEIGHT/2), (bend_x, ty+NODE_HEIGHT/2)]:
            ET.SubElement(array, 'mxPoint', x=str(x), y=str(y))


    xml = ET.tostring(page, encoding='unicode')
    pattern = r'<diagram\b[^>]*\bid="(?:navigation-overview|navigation-detail)"[^>]*>.*?</diagram>'
    if re.search(pattern, original, flags=re.S):
        updated = re.sub(pattern, lambda _: xml, original, flags=re.S)
    else:
        updated = original.replace('</mxfile>', xml + '</mxfile>')
    for old in re.findall(r'<diagram\b.*?</diagram>', original, flags=re.S):
        if 'id="navigation-' not in old:
            assert old in updated
    TARGET.write_text(updated, encoding='utf-8', newline='')
    print(f'Updated {PAGE_ID}: {len(nodes)} screens/overlays, {len(edges)} navigation edges')
    if f'id="{NO_LABELS_ID}"' in original:
        build_no_labels()
    if any(f'id="{target}"' in original for _, target, _ in BW_VARIANTS):
        build_bw()


def build_variant(source_id, target_id, name, hide_labels=False, monochrome=False):
    """Clone current editable geometry, changing only requested presentation."""
    original = TARGET.read_text(encoding='utf-8')
    page = ET.fromstring(original).find(f"diagram[@id='{source_id}']")
    assert page is not None, f'{source_id} must exist first'
    variant = copy.deepcopy(page)
    variant.set('id', target_id)
    variant.set('name', name)
    for cell in variant.findall('.//mxCell'):
        if hide_labels and cell.get('edge') == '1':
            cell.set('data-action', cell.get('value', ''))
            cell.set('value', '')
        if monochrome and cell.get('style'):
            cell.set('style', re.sub(
                r'(fillColor|strokeColor|fontColor|labelBackgroundColor)=([^;]+)',
                lambda m: m.group(1)+'='+('none' if m.group(2)=='none' else
                    '#FFFFFF' if m.group(1) in ('fillColor', 'labelBackgroundColor') else '#000000'),
                cell.get('style')))
    save_variant(original, variant)


def save_variant(original, variant):
    target_id = variant.get('id')
    xml = ET.tostring(variant, encoding='unicode')
    pattern = rf'<diagram\b[^>]*\bid="{target_id}"[^>]*>.*?</diagram>'
    if re.search(pattern, original, flags=re.S):
        updated = re.sub(pattern, lambda _: xml, original, flags=re.S)
    else:
        updated = original.replace('</mxfile>', xml+'</mxfile>')
    for old in re.findall(r'<diagram\b.*?</diagram>', original, flags=re.S):
        if f'id="{target_id}"' not in old:
            assert old in updated
    TARGET.write_text(updated, encoding='utf-8', newline='')
    print(f'Updated {target_id}')


def build_no_labels():
    build_variant(PAGE_ID, NO_LABELS_ID, 'Navigation - No Labels', hide_labels=True)


def build_bw():
    for source, target, name in BW_VARIANTS:
        build_variant(source, target, name, monochrome=True)


def build_vertical():
    """Project the same screen tree into the reference's vertical columns."""
    original = TARGET.read_text(encoding='utf-8')
    source = ET.fromstring(original).find("diagram[@id='navigation-no-edge-labels-bw']")
    assert source is not None, 'Create the black-and-white no-label page first'
    page = copy.deepcopy(source)
    page.set('id', VERTICAL_ID)
    page.set('name', 'Screen Flow - Vertical B&W')
    page.set('data-source-page', 'navigation-no-edge-labels-bw')
    cells = {cell.get('id'): cell for cell in page.findall('.//mxCell')}
    children = {key: [] for key, cell in cells.items() if cell.get('vertex') == '1'}
    for cell in cells.values():
        if cell.get('edge') == '1':
            children[cell.get('source')].append(cell.get('target'))
    width, height, step, indent = NODE_WIDTH, NODE_HEIGHT, 140, 20
    secondary = [key for key in children['overview'] if key in ('members', 'settings')]
    columns = [key for key in children['overview'] if key not in secondary] + ['admin']
    center = 60 + (len(columns)-2)*440/2 + width/2
    middle = center-width/2
    positions = {
        'login': (middle, 20), 'code': (middle-440, 20),
        'link': (middle+440, 20), 'onboarding': (middle, 180),
        'projects': (middle, 340), 'overview': (middle, 500),
    }

    def place_column(key, base, level, row):
        positions[key] = (base+level*indent, 650+row*step)
        next_row = row+1
        for child in children[key]:
            next_row = place_column(child, base, level+1, next_row)
        return next_row

    for index, key in enumerate(columns):
        place_column(key, 60+index*440, 0, 0)
    for index, key in enumerate(secondary):
        place_column(key, 60+(index+1)*440, 0, 2)
    # Fill the empty center with run views and split the Admin list in two.
    positions['writing'] = (100, 930)
    positions['writing-paper'] = (120, 1070)
    stage_keys = [key for key in children['studio'] if key.startswith('run-')]
    for index, key in enumerate(stage_keys):
        positions[key] = (500+(index % 2)*440, 1250+(index//2)*140)
    admin_children = children['admin']
    for base, subset in [(1380, admin_children[:5]), (1820, admin_children[5:])]:
        row = 1
        for key in subset:
            row = place_column(key, base, 0, row)
    assert set(positions) == set(children), 'Every source screen needs a slot'
    for key, (x, y) in positions.items():
        geometry = cells[key].find('mxGeometry')
        geometry.set('x', str(x))
        geometry.set('y', str(y))

    for cell in cells.values():
        if cell.get('edge') != '1':
            continue
        a, b = cell.get('source'), cell.get('target')
        sx, sy = positions[a]
        tx, ty = positions[b]
        points = []
        if a == 'login':
            if b == 'code':
                ports = (0, .5, 1, .5)
            elif b == 'link':
                ports = (1, .5, 0, .5)
            elif b == 'onboarding':
                ports = (.5, 1, .5, 0)
            elif b == 'projects':
                ports = (.8, 1, .8, 0)
                bypass = sx+width+60
                points = [(sx+width*.8, 170), (bypass, 170),
                          (bypass, 310), (tx+width*.8, 310)]
            else:
                assert b == 'admin'
                ports = (.95, 1, .5, 0)
                outer = 60+len(columns)*440
                points = [(sx+width*.95, 160), (outer, 160),
                          (outer, 630), (tx+width/2, 630)]
        elif a == 'projects':
            ports = {'invitations': (0, .5, 1, .5),
                     'new-project': (1, .5, 0, .5),
                     'overview': (.5, 1, .5, 0)}[b]
        elif a == 'overview':
            if b in secondary:
                ports = (.5, 1, 0, .5)
                points = [(sx+width/2, 630), (tx-40, 630), (tx-40, ty+height/2)]
            else:
                ports = (.5, 1, .5, 0)
                points = [(sx+width/2, 630), (tx+width/2, 630)]
        elif a == 'admin':
            ports = (.5, 1, 0, .5)
            points = [(sx+width/2, 780), (tx-20, 780), (tx-20, ty+height/2)]
        elif a == 'studio' and b.startswith('run-'):
            ports = (0, .5, 0, .5)
            points = [(sx-20, sy+height/2), (sx-20, 1210),
                      (tx-20, 1210), (tx-20, ty+height/2)]
        else:
            ports = (0, .5, 0, .5)
            points = [(sx-20, sy+height/2), (sx-20, ty+height/2)]
        style = re.sub(r'(?:exit|entry)[XY]=[^;]+;', '', cell.get('style'))
        style = re.sub(r'rounded=[^;]+;', 'rounded=0;', style)
        ex, ey, ix, iy = ports
        cell.set('style', style+f'exitX={ex};exitY={ey};entryX={ix};entryY={iy};')
        cell.remove(cell.find('mxGeometry'))
        geometry = ET.SubElement(cell, 'mxGeometry', relative='1', **{'as': 'geometry'})
        if points:
            array = ET.SubElement(geometry, 'Array', **{'as': 'points'})
            for x, y in points:
                ET.SubElement(array, 'mxPoint', x=str(x), y=str(y))
    save_variant(original, page)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--no-edge-labels', action='store_true', help='Clone the current detail page without edge labels')
    mode.add_argument('--black-white', action='store_true', help='Clone both existing variants in black and white')
    mode.add_argument('--vertical', action='store_true', help='Create the reference-style vertical black-and-white layout')
    args = parser.parse_args()
    if args.vertical:
        build_vertical()
    elif args.no_edge_labels:
        build_no_labels()
        if any(f'id="{target}"' in TARGET.read_text(encoding='utf-8') for _, target, _ in BW_VARIANTS):
            build_bw()
    elif args.black_white:
        build_bw()
    else:
        build()
    if not args.vertical and f'id="{VERTICAL_ID}"' in TARGET.read_text(encoding='utf-8'):
        build_vertical()

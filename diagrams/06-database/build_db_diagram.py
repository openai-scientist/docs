"""Physical database diagram (.drawio) from a psql dump of information_schema.

usage: build_db_diagram.py cols.txt keys.txt out.drawio
cols.txt: table|column|type|nullable   keys.txt: table|column|PRIMARY KEY or FOREIGN KEY|ref_table

Tables sit in columns by business area. Lines run on a 20 px grid from the FK row to the referenced
table, never through a table and never along a segment another line already uses (A* router, as in
diagrams/03-conceptual-erd/build_erd.py).
"""
import heapq
import sys
from collections import defaultdict
from html import escape

cols, keys, out = sys.argv[1:4]
tables = defaultdict(list)
nullable = {}
for line in open(cols):
    t, c, ty, nul = line.rstrip('\n').split('|')
    tables[t].append((c, ty))
    nullable[(t, c)] = nul == 'YES'
pk, fk, edges = set(), set(), []
for line in open(keys):
    t, c, kind, ref = line.rstrip('\n').split('|')
    if kind == 'PRIMARY KEY':
        pk.add((t, c))
    elif (t, c, ref) not in edges:
        fk.add((t, c))
        edges.append((t, c, ref))

# columns of the layout, by business area, top to bottom
LAYOUT = [  # four tall columns, so the page is portrait like the report
    ['auth_sessions', 'email_otps', 'user_platform_roles', 'google_connection_grants', 'audit_events',
     'platform_settings', 'integration_secrets', 'engine_settings', 'model_profiles',
     'monitoring_events', 'monitoring_alerts', 'monitoring_capture_gaps', 'monitoring_worker_states'],
    ['projects', 'project_memberships', 'project_settings', 'notification_preferences', 'spending_alerts',
     'datasets', 'dataset_versions', 'data_connections', 'project_files', 'project_integrations', 'integration_deliveries'],
    ['users', 'research_contexts', 'research_runs', 'comments', 'cost_entries', 'cost_ledger_start',
     'notifications', 'notification_emails'],
    ['stage_runs', 'stage_decisions', 'run_gates', 'frame_reviews', 'run_events', 'run_artifacts',
     'pi_consultations', 'pi_notes'],
]
placed = [t for c in LAYOUT for t in c]
missing = set(tables) ^ set(placed)
if missing:
    sys.exit(f'layout and database disagree: {sorted(missing)}')

# HEAD + ROW / 2 is a multiple of G, so every row centre lies on the routing grid
G, W, ROW, HEAD, GAPX, GAPY, M = 20, 300, 20, 30, 400, 160, 60
TOP = 400  # free lanes above the tables
# heavily referenced tables are wider, so every incoming line gets its own point on the top or bottom side
WIDE = {'users': 700, 'projects': 420, 'research_runs': 560, 'stage_runs': 420}
boxes, x = {}, M
for column in LAYOUT:
    y, cw = TOP, max(WIDE.get(t, W) for t in column)
    for t in column:
        h = HEAD + ROW * len(tables[t])
        boxes[t] = (x, y, WIDE.get(t, W), h)
        y += (h + GAPY + G - 1) // G * G  # keep table tops on the grid
    x += cw + GAPX
MAXX = x + M
MAXY = max(y + h for _, y, _, h in boxes.values()) + 400  # free lanes below the tables


blocked = set()
for x, y, w, h in boxes.values():
    for gx in range(x - G, x + w + G + 1, G):
        for gy in range(y - G, y + h + G + 1, G):
            blocked.add((gx, gy))
used, taken, reserved = {}, set(), set()
STEP = {'E': (G, 0, 'h'), 'W': (-G, 0, 'h'), 'S': (0, G, 'v'), 'N': (0, -G, 'v')}
OPP = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}


def src_ports(t, c):
    """Both ends of the FK row, two grid cells outside the table."""
    x, y, w, h = boxes[t]
    ry = y + HEAD + ROW // 2 + [k for k, _ in tables[t]].index(c) * ROW
    out = [((x - 2 * G, ry), (0, (ry - y) / h), 'W'), ((x + w + 2 * G, ry), (1, (ry - y) / h), 'E')]
    return [p for p in out if p[0] not in taken and not used.get(p[0])]


def dst_ports(t):
    """Grid points along the top and bottom sides of the referenced table, so a line never seems to point at a column."""
    x, y, w, h = boxes[t]
    out = []
    for gx in range(x + G, x + w - G + 1, G):
        out.append(((gx, y - 2 * G), ((gx - x) / w, 0), 'N'))
        out.append(((gx, y + h + 2 * G), ((gx - x) / w, 1), 'S'))
    return [p for p in out if p[0] not in taken and not used.get(p[0]) and p[0] not in reserved]


def route(t, c, r, share=False):
    starts, goals = src_ports(t, c), {p[0]: p for p in dst_ports(r)}
    own = {p[0] for p in starts}
    tx, ty, tw, th = boxes[r]

    def hdist(p):
        return (max(tx - p[0], 0, p[0] - tx - tw) + max(ty - p[1], 0, p[1] - ty - th)) / G

    heap, best, prev = [], {}, {}
    for pt, rel, d in starts:
        best[(pt, d)] = 0
        prev[(pt, d)] = None
        heapq.heappush(heap, (hdist(pt), 0, (pt, d), rel))
    while heap:
        _, cost, st, rel0 = heapq.heappop(heap)
        if cost > best.get(st, 1e18):
            continue
        pt, d = st
        # arrive moving into the side of the goal port (opposite of its outward direction)
        if pt in goals and prev[st] is not None and d == OPP[goals[pt][2]]:
            path = [st]
            while prev[path[-1]] is not None:
                path.append(prev[path[-1]])
            return [p for p, _ in reversed(path)], rel0, goals[pt][1]
        for nd, (dx, dy, ax) in STEP.items():
            if nd == OPP[d]:
                continue
            q = (pt[0] + dx, pt[1] + dy)
            if not (0 <= q[0] <= MAXX and 0 <= q[1] <= MAXY) or (q in blocked and q not in goals):
                continue
            if q in taken or (q in reserved and q not in own):
                continue
            overlap = ax in used.get(pt, ()) or ax in used.get(q, ())
            if overlap and not share:
                continue
            nc = cost + 1 + (4 if nd != d else 0) + (12 if used.get(q) else 0) + (60 if overlap else 0)
            ns = (q, nd)
            if nc < best.get(ns, 1e18):
                best[ns] = nc
                prev[ns] = st
                heapq.heappush(heap, (nc + hdist(q), nc, ns, rel0))
    if not share:
        print(f'shared lane: {t}.{c} -> {r}')
        return route(t, c, r, share=True)
    sys.exit(f'no route {t}.{c} -> {r}')


def take(path):
    for a, b in zip(path, path[1:]):
        ax = 'h' if a[1] == b[1] else 'v'
        used.setdefault(a, set()).add(ax)
        used.setdefault(b, set()).add(ax)
    taken.update((path[0], path[-1]))


SHORT = {'character varying': 'varchar', 'timestamp with time zone': 'timestamptz',
         'timestamp without time zone': 'timestamp', 'double precision': 'float8'}
cells = []
for t, (x, y, w, h) in boxes.items():
    cells.append(f'<mxCell id="t_{t}" value="{t}" style="shape=table;startSize={HEAD};container=1;collapsible=0;'
                 f'childLayout=tableLayout;fontStyle=1;align=center;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=13;" '
                 f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    for n, (c, ty) in enumerate(tables[t]):
        tag = 'PK' if (t, c) in pk else 'FK' if (t, c) in fk else ''
        ty = SHORT.get(ty, ty) + ('' if nullable[(t, c)] else ' NN')
        style = 'fontStyle=1;' if tag == 'PK' else 'fontStyle=2;' if tag == 'FK' else ''
        rid = f'r_{t}_{c}'
        cells.append(f'<mxCell id="{rid}" value="" style="shape=tableRow;horizontal=0;startSize=0;fillColor=none;'
                     f'collapsible=0;dropTarget=0;top=0;left=0;right=0;bottom=0;" vertex="1" parent="t_{t}">'
                     f'<mxGeometry y="{HEAD + n * ROW}" width="{w}" height="{ROW}" as="geometry"/></mxCell>')
        for k, (val, cx, cw) in enumerate(((tag, 0, 34), (escape(c), 34, 150), (escape(ty), 184, w - 184))):
            cells.append(f'<mxCell id="{rid}_{k}" value="{val}" style="shape=partialRectangle;connectable=0;fillColor=none;'
                         f'top=0;left=0;bottom=0;right=0;align=left;spacingLeft=4;fontSize=11;{style}" vertex="1" '
                         f'parent="{rid}"><mxGeometry x="{cx}" width="{cw}" height="{ROW}" as="geometry">'
                         f'<mxRectangle width="{cw}" height="{ROW}" as="alternateBounds"/></mxGeometry></mxCell>')


def span(e):
    a, b = boxes[e[0]], boxes[e[2]]
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


reserved = {p[0] for t, c, _ in edges for p in src_ports(t, c)}
# FK rows' ports are kept free, so destination ports never sit on them
# short links first, so they get the direct lanes; each FK row exits on its own grid point
for n, (t, c, r) in enumerate(sorted(edges, key=span)):
    path, (ex, ey), (nx, ny) = route(t, c, r)
    take(path)
    bends = [p for i, p in enumerate(path) if i in (0, len(path) - 1)
             or (path[i - 1][0] == p[0]) != (p[0] == path[i + 1][0])]
    one = 'ERzeroToOne' if nullable[(t, c)] else 'ERmandOne'
    cells.append(f'<mxCell id="e{n}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                 f'exitX={ex:.4f};exitY={ey:.4f};exitDx=0;exitDy=0;entryX={nx:.4f};entryY={ny:.4f};entryDx=0;entryDy=0;'
                 f'startArrow=ERmany;endArrow={one};startFill=0;endFill=0;strokeColor=#555555;" edge="1" parent="1" '
                 f'source="t_{t}" target="t_{r}"><mxGeometry relative="1" as="geometry"><Array as="points">'
                 + ''.join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in bends) + '</Array></mxGeometry></mxCell>')
cells.append('<mxCell id="title" value="Database Diagram – OpenAI-Scientist (PostgreSQL, schema public)" '
             'style="text;html=1;fontSize=20;fontStyle=1;align=left;" vertex="1" parent="1">'
             f'<mxGeometry x="{M}" y="20" width="900" height="40" as="geometry"/></mxCell>')
xml = ('<mxfile><diagram name="Database Diagram"><mxGraphModel grid="1" gridSize="10"><root><mxCell id="0"/>'
       '<mxCell id="1" parent="0"/>' + ''.join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open(out, 'w').write(xml)
print(len(tables), 'tables', len(edges), 'foreign keys')

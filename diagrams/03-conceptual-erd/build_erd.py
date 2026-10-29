"""Conceptual ERD (crow's foot) of the tables in deliverables/database/FA26SE115_database-script.sql.

usage: build_erd.py SCRIPT.sql OUT.drawio
Every business table is an entity, named as a conceptual entity (singular PascalCase noun);
technical tables (sessions, one-time codes, monitoring, system settings, migration marker) are left out. every foreign key is a relationship, except the
"created by", "last updated by" and "acknowledged by" columns, which record who touched a row rather than a
business relationship. Cardinality comes from the script: NOT NULL foreign key -> mandatory one,
nullable -> zero or one; a foreign key that is the primary key -> one-to-one, otherwise many.
"""
import heapq
import re
import sys
from xml.sax.saxutils import escape

W, H, PX, PY, G = 160, 40, 240, 160, 20

NAME = {
    'users': 'User', 'projects': 'Project', 'project_memberships': 'ProjectMembership',
    'project_settings': 'ProjectSetting', 'user_platform_roles': 'PlatformRole', 'audit_events': 'AuditEvent',
    'project_files': 'ProjectFile', 'project_integrations': 'ProjectIntegration',
    'integration_deliveries': 'IntegrationDelivery', 'spending_alerts': 'SpendingAlert',
    'notifications': 'Notification', 'notification_emails': 'NotificationEmail',
    'notification_preferences': 'NotificationPreference', 'data_connections': 'DataConnection',
    'google_connection_grants': 'GoogleConnectionGrant', 'datasets': 'Dataset', 'dataset_versions': 'DatasetVersion',
    'research_contexts': 'ResearchContext', 'research_runs': 'ResearchRun', 'cost_entries': 'CostEntry',
    'stage_runs': 'StageRun', 'stage_decisions': 'StageDecision', 'run_gates': 'RunGate',
    'pi_consultations': 'PIConsultation', 'pi_notes': 'PINote', 'frame_reviews': 'FrameReview',
    'comments': 'Comment', 'run_artifacts': 'RunArtifact', 'run_events': 'RunEvent', 'model_profiles': 'ModelProfile',
}
TECHNICAL = {'alembic_version', 'auth_sessions', 'email_otps', 'monitoring_events', 'monitoring_alerts',
             'monitoring_capture_gaps', 'monitoring_worker_states', 'cost_ledger_start', 'platform_settings',
             'engine_settings', 'integration_secrets'}
# (column, row) of each entity; every entity has the same size
POS = {
    'project_settings': (0, 0), 'project_files': (1, 0), 'project_integrations': (2, 0),
    'integration_deliveries': (3, 0), 'spending_alerts': (4, 0), 'data_connections': (5, 0), 'model_profiles': (9, 0),
    'datasets': (6, 0), 'projects': (2.5, 1.5), 'research_contexts': (4, 1.5), 'cost_entries': (5, 1.5),
    'pi_consultations': (7, 1.5), 'pi_notes': (8.5, 1.5),
    'dataset_versions': (6, 1.5), 'project_memberships': (1, 3), 'google_connection_grants': (2, 3),
    'notification_preferences': (3, 3), 'research_runs': (4.5, 3), 'stage_runs': (6.5, 3),
    'notifications': (3, 4.5), 'stage_decisions': (7.5, 4), 'notification_emails': (1, 4.5),
    'frame_reviews': (0, 4.5), 'comments': (4, 4.5), 'run_artifacts': (5, 4.5), 'run_events': (6, 4.5),
    'run_gates': (8.5, 5.5), 'users': (2, 5.5), 'user_platform_roles': (1, 7), 'audit_events': (3, 7),
}
SKIP_COLS = {'created_by_user_id', 'updated_by_user_id', 'acknowledged_by_user_id', 'actor_user_id'}
KEEP = {('audit_events', 'actor_user_id')}
# verb read from the referenced (parent) table to the child table
VERB = {
    ('projects', 'owner_user_id'): 'owns', ('project_memberships', 'user_id'): 'joins',
    ('project_memberships', 'project_id'): 'has', ('project_memberships', 'created_by_user_id'): 'invites',
    ('project_settings', 'project_id'): 'is configured by', ('user_platform_roles', 'user_id'): 'has role',
    ('auth_sessions', 'user_id'): 'opens', ('email_otps', 'user_id'): 'requests',
    ('datasets', 'project_id'): 'owns', ('datasets', 'created_by_user_id'): 'uploads',
    ('dataset_versions', 'dataset_id'): 'has', ('dataset_versions', 'created_by_user_id'): 'creates',
    ('data_connections', 'project_id'): 'has', ('data_connections', 'created_by_user_id'): 'connects',
    ('google_connection_grants', 'project_id'): 'grants', ('google_connection_grants', 'user_id'): 'authorizes',
    ('research_contexts', 'project_id'): 'has', ('research_contexts', 'created_by_user_id'): 'writes',
    ('research_runs', 'project_id'): 'runs', ('research_runs', 'created_by_user_id'): 'starts',
    ('research_runs', 'dataset_version_id'): 'is analyzed in', ('research_runs', 'research_context_id'): 'frames',
    ('stage_runs', 'research_run_id'): 'consists of', ('stage_runs', 'prior_stage_run_id'): 'precedes',
    ('stage_runs', 'origin_decision_id'): 'starts', ('stage_decisions', 'stage_run_id'): 'records',
    ('stage_decisions', 'decided_by_user_id'): 'decides', ('run_gates', 'run_id'): 'waits at',
    ('run_gates', 'stage_run_id'): 'opens', ('run_gates', 'answered_by_user_id'): 'answers',
    ('run_events', 'run_id'): 'emits', ('run_events', 'stage_run_id'): 'emits',
    ('run_artifacts', 'run_id'): 'produces', ('run_artifacts', 'stage_run_id'): 'produces',
    ('comments', 'run_id'): 'has', ('comments', 'artifact_id'): 'is commented in', ('comments', 'author_user_id'): 'writes',
    ('frame_reviews', 'run_id'): 'is reviewed in', ('frame_reviews', 'submitted_by_user_id'): 'submits',
    ('cost_entries', 'project_id'): 'is charged', ('cost_entries', 'run_id'): 'costs',
    ('spending_alerts', 'project_id'): 'raises', ('pi_consultations', 'research_run_id'): 'consults',
    ('pi_consultations', 'stage_run_id'): 'consults', ('pi_consultations', 'applied_decision_id'): 'is applied by',
    ('pi_notes', 'research_run_id'): 'has', ('pi_notes', 'consultation_id'): 'writes',
    ('notifications', 'project_id'): 'sends', ('notifications', 'recipient_user_id'): 'receives',
    ('notifications', 'run_id'): 'notifies', ('notification_emails', 'project_id'): 'sends',
    ('notification_emails', 'recipient_user_id'): 'receives', ('notification_emails', 'run_id'): 'notifies',
    ('notification_preferences', 'project_id'): 'sets', ('notification_preferences', 'user_id'): 'sets',
    ('project_files', 'project_id'): 'stores', ('project_files', 'created_by_user_id'): 'uploads',
    ('project_integrations', 'project_id'): 'integrates', ('project_integrations', 'created_by_user_id'): 'adds',
    ('integration_deliveries', 'integration_id'): 'delivers', ('audit_events', 'actor_user_id'): 'performs',
    ('users', 'created_by_user_id'): 'creates',
}

sql = open(sys.argv[1]).read()
tables = [t for t in re.findall(r'CREATE TABLE public\.(\w+)', sql) if t not in TECHNICAL]
notnull = {}
for t, body in re.findall(r'CREATE TABLE public\.(\w+) \((.*?)\n\);', sql, re.S):
    for line in body.splitlines():
        m = re.match(r'\s+(\w+) ', line)
        if m:
            notnull[(t, m[1])] = 'NOT NULL' in line
pk = {(t, c) for t, c in re.findall(r'ALTER TABLE ONLY public\.(\w+)\s+ADD CONSTRAINT \w+ PRIMARY KEY \((\w+)\)', sql)}
fks = re.findall(r'ALTER TABLE ONLY public\.(\w+)\s+ADD CONSTRAINT \w+ FOREIGN KEY \((\w+)\) REFERENCES public\.(\w+)\(', sql)

missing = (set(tables) ^ set(POS)) | (set(tables) ^ set(NAME))
if missing:
    sys.exit(f'layout and script disagree: {sorted(missing)}')


def box(t):
    c, r = POS[t]
    return round(40 + c * PX), round(80 + r * PY), W, H


rels = []
for child, col, parent in fks:
    if child in TECHNICAL or parent in TECHNICAL:
        continue
    if col in SKIP_COLS and (child, col) not in KEEP:
        continue
    verb = VERB.get((child, col))
    if verb is None:
        sys.exit(f'no verb for {child}.{col}')
    rels.append((child, col, parent, verb))

# Grid router: lines run on a 20 px grid, never through an entity, never along a segment another line
# already uses; crossing another line is allowed but costs extra, and so does each bend.
boxes = {t: box(t) for t in tables}
blocked = set()
for x, y, w, h in boxes.values():
    for gx in range(x - G, x + w + G + 1, G):
        for gy in range(y - G, y + h + G + 1, G):
            blocked.add((gx, gy))
used = {}  # grid point -> axes ('h', 'v') already taken by a line
taken_ports = set()
MAXX, MAXY = 2400, 1300
STEP = {'E': (G, 0, 'h'), 'W': (-G, 0, 'h'), 'S': (0, G, 'v'), 'N': (0, -G, 'v')}


def ports(t):
    """Grid points 2 cells outside each side, one per grid cell along it, with the side's relative coordinate and outward direction."""
    x, y, w, h = boxes[t]
    out = []
    for gx in range(x + G, x + w - G + 1, G):
        out.append(((gx, y - 2 * G), ((gx - x) / w, 0), 'N'))
        out.append(((gx, y + h + 2 * G), ((gx - x) / w, 1), 'S'))
    for gy in range(y + G, y + h - G + 1, G):
        out.append(((x - 2 * G, gy), (0, (gy - y) / h), 'W'))
        out.append(((x + w + 2 * G, gy), (1, (gy - y) / h), 'E'))
    return [p for p in out if p[0] not in taken_ports and not used.get(p[0])]


def route(src, dst):
    starts, goals = ports(src), {p[0]: p for p in ports(dst)}
    tx, ty, tw, th = boxes[dst]

    def hdist(p):
        return max(tx - p[0], 0, p[0] - tx - tw) + max(ty - p[1], 0, p[1] - ty - th)

    heap, best, prev = [], {}, {}
    for pt, rel, d in starts:
        st = (pt, d)
        best[st] = 0
        prev[st] = None
        heapq.heappush(heap, (hdist(pt), 0, st, rel))
    while heap:
        _, cost, st, rel0 = heapq.heappop(heap)
        if cost > best.get(st, 1e18):
            continue
        pt, d = st
        if pt in goals and (src != dst or prev[st] is not None) and STEP[d][2] == {'N': 'v', 'S': 'v', 'E': 'h', 'W': 'h'}[goals[pt][2]] and \
                (STEP[d][0], STEP[d][1]) == (-STEP[goals[pt][2]][0], -STEP[goals[pt][2]][1]):
            path = [st]
            while prev[path[-1]] is not None:
                path.append(prev[path[-1]])
            return [p for p, _ in reversed(path)], rel0, goals[pt][1]
        for nd, (dx, dy, ax) in STEP.items():
            if (dx, dy) == (-STEP[d][0], -STEP[d][1]):
                continue
            q = (pt[0] + dx, pt[1] + dy)
            if not (0 <= q[0] <= MAXX and 0 <= q[1] <= MAXY) or (q in blocked and q not in goals):
                continue
            if ax in used.get(pt, ()) or ax in used.get(q, ()):
                continue
            if q in taken_ports:
                continue
            c = cost + 1 + (4 if nd != d else 0) + (15 if used.get(q) else 0)
            ns = (q, nd)
            if c < best.get(ns, 1e18):
                best[ns] = c
                prev[ns] = st
                heapq.heappush(heap, (c + hdist(q) / G, c, ns, rel0))
    sys.exit(f'no route {src} -> {dst}')


def take(path):
    for a, b in zip(path, path[1:]):
        ax = 'h' if a[1] == b[1] else 'v'
        used.setdefault(a, set()).add(ax)
        used.setdefault(b, set()).add(ax)
    taken_ports.update((path[0], path[-1]))


def centre_dist(r):
    a, b = boxes[r[2]], boxes[r[0]]
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


cells = []
for t in tables:
    x, y, w, h = boxes[t]
    cells.append(f'<mxCell id="{t}" value="{NAME[t]}" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;'
                 f'strokeColor=#000000;fontSize=11;fontFamily=Arial;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
for n, (child, col, parent, verb) in enumerate(sorted(rels, key=centre_dist)):
    path, (ex, ey), (nx, ny) = route(parent, child)
    take(path)
    bends = [p for i, p in enumerate(path) if i in (0, len(path) - 1)
             or (path[i - 1][0] == p[0]) != (p[0] == path[i + 1][0])]
    parent_end = 'ERmandOne' if notnull[(child, col)] else 'ERzeroToOne'
    child_end = 'ERzeroToOne' if (child, col) in pk else 'ERzeroToMany'
    cells.append(f'<mxCell id="r{n}" value="{escape(verb)}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                 f'exitX={ex:.4f};exitY={ey:.4f};exitDx=0;exitDy=0;entryX={nx:.4f};entryY={ny:.4f};entryDx=0;entryDy=0;'
                 f'startArrow={parent_end};endArrow={child_end};startFill=0;endFill=0;startSize=8;endSize=8;'
                 f'strokeColor=#000000;fontSize=9;fontFamily=Arial;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" '
                 f'source="{parent}" target="{child}"><mxGeometry relative="1" as="geometry"><Array as="points">'
                 + ''.join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in bends) + '</Array></mxGeometry></mxCell>')
cells.append('<mxCell id="title" value="Conceptual Entity Relationship Diagram – OpenAI-Scientist" style="text;html=1;fontSize=16;'
             'fontStyle=1;fontFamily=Arial;align=left;" vertex="1" parent="1">'
             '<mxGeometry x="40" y="10" width="600" height="30" as="geometry"/></mxCell>')
xml = ('<mxfile host="drawio"><diagram id="erd" name="ERD"><mxGraphModel dx="1600" dy="1200" grid="1" gridSize="10" '
       'guides="1" page="1" pageWidth="2400" pageHeight="1300" math="0" shadow="0"><root><mxCell id="0"/>'
       '<mxCell id="1" parent="0"/>' + ''.join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open(sys.argv[2], 'w').write(xml)
print(len(tables), 'entities,', len(rels), 'relationships')

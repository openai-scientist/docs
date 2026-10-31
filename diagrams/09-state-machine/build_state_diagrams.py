"""Build eight flat feature-group views from Report7 and the approved Authentication page."""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as E

OUT = Path(__file__).resolve().parent
NAME = 'State-Machine-Diagrams'
BASE = 'html=1;fontFamily=Arial;fontSize=14;fontColor=#000000;strokeColor=#000000;fillColor=#ffffff;strokeWidth=1;'


class Page:
    def __init__(self, name, key):
        self.page = E.Element('diagram', name=name, id=key)
        model = E.SubElement(self.page, 'mxGraphModel', grid='1', gridSize='10', page='1', pageWidth='1600', pageHeight='1600', background='#ffffff')
        self.root = E.SubElement(model, 'root')
        E.SubElement(self.root, 'mxCell', id='0')
        E.SubElement(self.root, 'mxCell', id='1', parent='0')

    def node(self, key, text, x, y, w=220, h=70, kind='state', parent='1'):
        styles = {
            'state': 'rounded=1;absoluteArcSize=1;arcSize=10;whiteSpace=wrap;',
            'choice': 'rhombus;whiteSpace=wrap;',
            'initial': 'ellipse;fillColor=#000000;',
            'final': 'ellipse;shape=endState;fillColor=#000000;',
            'text': 'text;strokeColor=none;fillColor=none;fontStyle=1;fontSize=18;align=left;',
            'note': 'shape=note;size=15;whiteSpace=wrap;align=left;spacing=10;',
            'composite': 'swimlane;rounded=1;arcSize=4;startSize=40;horizontal=1;container=1;collapsible=0;pointerEvents=0;align=left;spacingLeft=12;fontStyle=1;whiteSpace=wrap;',
        }
        cell = E.SubElement(self.root, 'mxCell', id=key, value=text, style=BASE + styles[kind], vertex='1', parent=parent)
        E.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), attrib={'as': 'geometry'})
        if kind == 'composite':
            self.node('scope-start', '', x + w / 2 - 12, y - 100, 24, 24, 'initial')
            self.edge('scope-entry', 'scope-start', key, ref='Diagram scope entry; see page source', test='Design entry check')

    def edge(self, key, source, target, text='', ports=(.5, 1, .5, 0), points=(), parent='1', pos=0, ref='', test=''):
        sx, sy, tx, ty = ports
        style = BASE + f'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;endArrow=classic;endSize=7;endFill=1;dashed=0;labelBackgroundColor=#ffffff;align=center;verticalAlign=middle;exitX={sx};exitY={sy};entryX={tx};entryY={ty};exitPerimeter=1;entryPerimeter=1;'
        cell = E.SubElement(self.root, 'mxCell', id=key, value=text, style=style, edge='1', parent=parent, source=source, target=target)
        cell.set('source-ref', ref)
        cell.set('test-ref', test)
        geo = E.SubElement(cell, 'mxGeometry', x=str(pos), relative='1', attrib={'as': 'geometry'})
        if points:
            arr = E.SubElement(geo, 'Array', attrib={'as': 'points'})
            for x, y in points:
                E.SubElement(arr, 'mxPoint', x=str(x), y=str(y))
        return cell


def project():
    p = Page('Project', 'project')
    p.node('start', '', 418, 30, 24, 24, 'initial')
    p.node('active', 'Active', 320, 130)
    p.node('completed', 'Completed', 320, 390)
    p.node('archived', 'Archived\n(read-only)', 320, 650)
    p.edge('created', 'start', 'active', ref='III 3.3.1; FR-04', test='TC-03')
    p.edge('complete', 'active', 'completed', 'project marked completed\n/ write audit entry', ref='III 3.3.3; FR-07', test='TC-03; TC-05')
    p.edge('archive-completed', 'completed', 'archived', 'project archived\n/ write audit entry', ref='III 3.3.3; FR-06; FR-07', test='TC-03; TC-05')
    p.edge('archive-active', 'active', 'archived', 'project archived\n/ make read-only; audit', ports=(1, .5, 1, .5), points=((790, 165), (790, 685)), ref='III 3.3.3; FR-06; FR-07', test='TC-03; TC-05')
    p.edge('edit', 'active', 'active', 'project updated\n/ write audit entry', ports=(0, .7, 0, .3), points=((80, 179), (80, 151)), ref='III 3.3.3; FR-07', test='TC-03; TC-05')
    return p.page


def handoff():
    p = Page('Hand-off Object', 'hand-off-object')
    p.node('version', 'Hand-off object version', 40, 30, 1100, 1220, 'composite')
    p.node('start', '', 538, 60, 24, 24, 'initial', 'version')
    p.node('draft', 'draft', 440, 130, 220, 70, parent='version')
    p.node('checks', 'Are all contract\nitems green?', 415, 290, 270, 100, 'choice', 'version')
    p.node('red', 'checks_red', 70, 305, 220, 70, parent='version')
    p.node('green', 'checks_green', 800, 305, 220, 70, parent='version')
    p.node('review', 'in_review', 800, 510, 220, 70, parent='version')
    p.node('ready', 'ready', 800, 710, 220, 70, parent='version')
    p.node('accepted', 'accepted\n(immutable)', 800, 910, 220, 80, parent='version')
    p.node('locked', 'locked\n(AnalysisPlan only)', 800, 1110, 220, 80, parent='version')
    p.node('stale', 'stale', 1270, 600, 220, 80)
    p.edge('create', 'start', 'draft', parent='version', ref='IV 3.4.3', test='TC-11')
    p.edge('check', 'draft', 'checks', 'checks completed', parent='version', ref='IV 3.4.3', test='TC-11; TC-27')
    p.edge('red-branch', 'checks', 'red', 'No', ports=(0, .5, 1, .5), parent='version', ref='IV 3.4.3', test='TC-11; TC-27')
    p.edge('green-branch', 'checks', 'green', 'Yes', ports=(1, .5, 0, .5), parent='version', ref='IV 3.4.3', test='TC-11; TC-27')
    p.edge('repair', 'red', 'checks', 'object revised; checks rerun', ports=(.5, 1, .5, 1), points=((180, 440), (550, 440)), parent='version', ref='IV 3.4.3; IV review loop', test='TC-27')
    p.edge('regression', 'green', 'checks', 'contract check changed', ports=(.3, 0, .7, 0), points=((866, 240), (604, 240)), parent='version', ref='IV 3.4.3', test='TC-11; TC-27')
    p.edge('review-start', 'green', 'review', 'review started', parent='version', ref='IV 3.4.3; IV review loop', test='TC-27')
    p.edge('revise-review', 'review', 'checks', 'maker revises\n/ checks run again', ports=(0, .5, .7, 1), points=((660, 545), (660, 470), (604, 470)), parent='version', ref='IV review loop step 6', test='TC-27')
    p.edge('review-done', 'review', 'ready', 'review completed', parent='version', ref='IV 3.4.3', test='TC-27')
    p.edge('accept', 'ready', 'accepted', 'object accepted\n/ freeze version and hash', parent='version', ref='IV 3.4.3; FR-161', test='TC-11')
    p.edge('lock', 'accepted', 'locked', 'plan locked\n[AnalysisPlan only]', parent='version', ref='IV 3.4.3; IV 3.8', test='TC-21')
    p.edge('invalidate', 'version', 'stale', 'pinned upstream\nversion changed', ports=(1, .5, 0, .5), ref='IV 3.4.3; FR-19', test='TC-11')
    return p.page


def dossier():
    p = Page('Dossier', 'dossier')
    p.node('version', 'Dossier version N', 40, 30, 1100, 730, 'composite')
    p.node('start', '', 538, 60, 24, 24, 'initial', 'version')
    p.node('pending', 'Version N, not approved', 420, 150, 260, 80, parent='version')
    p.node('enough', 'Enough eligible\napprovals?', 415, 340, 270, 110, 'choice', 'version')
    p.node('approved', 'Version N, approved', 800, 540, 260, 80, parent='version')
    p.node('superseded', 'Superseded\n(approval history retained)', 430, 960, 320, 80)
    p.edge('create', 'start', 'pending', '/ check reference hashes', parent='version', ref='IV 3.14 step 1; FR-94; FR-249', test='TC-35')
    p.edge('approval-recorded', 'pending', 'enough', 'eligible approval recorded', parent='version', ref='IV 3.14; FR-95', test='TC-35')
    p.edge('not-enough', 'enough', 'pending', 'No', ports=(0, .5, 0, .5), points=((180, 395), (180, 190)), parent='version', pos=-.75, ref='IV 3.14; FR-95', test='TC-35')
    p.edge('enough-approvals', 'enough', 'approved', 'Yes', ports=(1, .5, .5, 0), points=((930, 395),), parent='version', pos=-.75, ref='IV 3.14 step 4; FR-95', test='TC-35')
    p.edge('export', 'approved', 'approved', 'pinned export authorized\n/ export; audit version + format', ports=(.5, 1, 0, .5), points=((930, 680), (730, 680), (730, 580)), parent='version', ref='IV 3.14 steps 5-6; FR-97; FR-98', test='TC-36')
    p.edge('supersede', 'version', 'superseded', 'new accepted EvidenceBundle / PaperPack version\n/ create version N+1, not approved;\nkeep old approvals as history', ref='IV 3.14 step 2; FR-96; FR-251; FR-252', test='TC-35')
    return p.page


def decision_item():
    p = Page('Decision Item', 'decision-item')
    p.node('open', 'Decision item lifecycle', 40, 40, 1280, 900, 'composite')
    p.node('start', '', 448, 60, 24, 24, 'initial', 'open')
    p.node('pending', 'Pending user decision', 320, 150, 280, 80, parent='open')
    p.node('tentative', 'Tentatively decided\n(awaiting user review)', 870, 150, 320, 80, parent='open')
    p.node('confirms', 'Does the user\nconfirm?', 895, 420, 270, 110, 'choice', 'open')
    p.node('confirmed', 'Confirmed', 1000, 700, 220, 80, parent='open')
    p.node('overturned', 'Overturned', 600, 700, 240, 80, parent='open')
    p.node('answered', 'Answered', 70, 480, 240, 80, parent='open')
    p.node('unanswered', 'Closed unanswered\n(pinned wait deadline)', 370, 480, 260, 80, parent='open')
    p.node('spending-expired', 'Expired unanswered\n(spending deadline)', 70, 720, 260, 80, parent='open')
    p.node('closed-cancelled', 'Closed\n(run cancelled)', 520, 1120, 320, 80)
    p.edge('create', 'start', 'pending', ref='IV 3.5.2; FR-28', test='TC-16', parent='open')
    p.edge('human-answer', 'pending', 'answered', 'authorized user answers\n/ record decision', ports=(0, .6, .5, 0), points=((190, 198),), parent='open', ref='IV 3.5.2 step 3; FR-28', test='TC-16')
    p.edge('tentative-decision', 'pending', 'tentative', 'AI PI decides\n[autopilot; away; non-pinned]', ports=(1, .5, 0, .5), parent='open', ref='IV 3.5.2 step 5; FR-31', test='TC-17')
    p.edge('user-review', 'tentative', 'confirms', 'user reviews decision', parent='open', ref='IV 3.5.2 step 6; FR-31', test='TC-17')
    p.edge('confirmed-branch', 'confirms', 'confirmed', 'Yes', ports=(1, .5, .5, 0), points=((1240, 475), (1240, 640), (1110, 640)), parent='open', pos=-.8, ref='IV 3.5.2 step 6; FR-31', test='TC-17')
    p.edge('overturned-branch', 'confirms', 'overturned', 'No', ports=(0, .5, .5, 0), points=((720, 475),), parent='open', pos=-.8, ref='IV 3.5.2 step 6; FR-31', test='TC-17')
    p.edge('pinned-timeout', 'pending', 'unanswered', 'pinned wait deadline passed\n[no answer]\n/ end run with gaps', ports=(.7, 1, .5, 0), points=((516, 340), (500, 340)), parent='open', ref='IV 3.5.2 step 4; FR-265', test='TC-98; TC-100')
    p.edge('spending-timeout', 'pending', 'spending-expired', 'spending deadline passed\n[no answer]\n/ end run with gaps', ports=(0, .3, .5, 0), points=((20, 174), (20, 650), (200, 650)), parent='open', pos=.75, ref='IV 3.13; FR-91', test='TC-33')
    p.edge('cancel-pending', 'open', 'closed-cancelled', 'run cancelled\n[an item is still pending]', ref='IV 3.4.1 alternative flow; FR-22', test='TC-13')
    return p.page


def flat_page(diagram, name):
    """Remove composites; callers rebuild shared exits as direct transitions."""
    p = Page.__new__(Page)
    p.page = diagram
    p.page.set('name', name)
    p.root = diagram.find('./mxGraphModel/root')
    cells = {c.get('id'): c for c in p.root}
    composites = {k for k, c in cells.items() if 'container=1' in c.get('style', '')}
    for cell in list(p.root):
        if cell.get('id') in composites | {'scope-start', 'scope-entry'} or cell.get('source') in composites or cell.get('target') in composites:
            p.root.remove(cell)
            continue
        parent = cells.get(cell.get('parent'))
        if parent is not None and parent.get('id') in composites:
            box = parent.find('mxGeometry')
            dx, dy = float(box.get('x')), float(box.get('y'))
            geo = cell.find('mxGeometry')
            if cell.get('vertex') == '1':
                geo.set('x', str(float(geo.get('x', '0')) + dx))
                geo.set('y', str(float(geo.get('y', '0')) + dy))
            for pt in geo.findall('./Array/mxPoint'):
                pt.set('x', str(float(pt.get('x')) + dx))
                pt.set('y', str(float(pt.get('y')) + dy))
            cell.set('parent', '1')
    return p


def box(p, key, x, y, w=None, h=None):
    cell = p.root.find(f"mxCell[@id='{key}']")
    geo = cell.find('mxGeometry')
    geo.set('x', str(x)); geo.set('y', str(y))
    if w is not None: geo.set('width', str(w))
    if h is not None: geo.set('height', str(h))


def relabel(p, labels):
    for key, text in labels.items():
        cell = p.root.find(f"mxCell[@id='{key}']")
        if cell.get('edge') == '1' and 'transition-spec' not in cell.attrib:
            cell.set('transition-spec', cell.get('value', ''))
        cell.set('value', text)


def drop_edges(p):
    for cell in list(p.root):
        if cell.get('edge') == '1': p.root.remove(cell)


def state(p, key, text, logical_id, x, y, w=260, h=80):
    p.node(key, text, x, y, w, h)
    p.root.find(f"mxCell[@id='{key}']").set('model-state', logical_id)


def account_lifecycle():
    p = Page('Authentication & Account', 'authentication-account')
    p.node('start', '', 428, 30, 24, 24, 'initial')
    state(p, 'active', 'Active account', 'active', 320, 150, 240, 80)
    state(p, 'suspended', 'Suspended account', 'suspended', 320, 500, 240, 80)
    p.edge('created', 'start', 'active', ref='III 3.2.1; IV 2.2.1 users; initial active is a design interpretation', test='Design entry check')
    p.edge('suspend', 'active', 'suspended', 'admin suspends account', ports=(.3,1,.3,0), ref='III 3.9.1; IV 2.2.1 users status active/suspended', test='Design transition check')
    p.edge('reactivate', 'suspended', 'active', 'admin reactivates account', ports=(1,.5,1,.5), points=((800,540),(800,190)), ref='III 3.9.1; IV 2.2.1 users status active/suspended', test='Design transition check')
    return p.page


def dataset_lifecycle():
    p = Page('Data Management', 'data-management-dataset')
    p.node('start', '', 428, 30, 24, 24, 'initial')
    state(p, 'available', 'Dataset available', 'conceptual_available', 320, 180, 240, 80)
    p.node('end', '', 428, 650, 30, 30, 'final')
    p.edge('created', 'start', 'available', '/ create first version with hash', ref='III 3.4.1; FR-09; IV 3.3; upload or import; conceptual lifecycle not a status enum', test='Design entry check')
    p.edge('version', 'available', 'available', 'new version\n/ retain prior versions', ports=(1,.2,1,.8), points=((900,110),(900,350)), ref='III 3.4.5; FR-09; immutable DatasetVersion', test='Design transition check')
    p.edge('delete', 'available', 'end', 'authorized deletion confirmed', ref='III 3.4.4; deletion constraints unspecified', test='Design transition check')
    return p.page


def notification_lifecycle():
    p = Page('Notifications & Integrations', 'notifications-in-app')
    p.node('start', '', 428, 30, 24, 24, 'initial')
    state(p, 'unread', 'Unread', 'read_at is null', 320, 160, 240, 80)
    state(p, 'read', 'Read', 'read_at is set', 320, 500, 240, 80)
    p.edge('created', 'start', 'unread', ref='IV 2.2.14 notifications read_at; conceptual lifecycle', test='Design entry check')
    p.edge('mark-read', 'unread', 'read', 'recipient marks as read\n/ record read_at', ref='III 3.8.4; IV 2.2.14 notifications', test='Design transition check')
    return p.page


def data_management():
    """Project pairing lifecycle, independent of jobs and dataset versions."""
    p = Page('Data Management', 'data-management')
    p.page.set('scope-status', 'planned-design')
    p.page.set('scope', 'One Local Node pairing with a project; conceptual states inferred from UC-08/31, not implementation enums')
    p.node('scope', 'Local Node — project pairing lifecycle (planned design)', 100, 0, 1000, 40, 'text')
    p.node('start', '', 418, 80, 24, 24, 'initial')
    state(p, 'unpaired', 'Unpaired', 'unpaired', 320, 180, 220, 80)
    state(p, 'online', 'Paired\n(online)', 'paired_online', 320, 420, 220, 80)
    state(p, 'offline', 'Paired\n(offline)', 'paired_offline', 880, 420, 220, 80)
    state(p, 'revoked', 'Revoked', 'revoked', 600, 800, 240, 80)
    p.edge('begin', 'start', 'unpaired', ref='UC-08 precondition: installed Node before project pairing', test='TC-08')
    p.edge('paired', 'unpaired', 'online', 'pairing succeeds\n[valid project pairing code]', ref='UC-08; FR-87; conceptual connected pairing outcome', test='TC-08')
    p.edge('disconnected', 'online', 'offline', 'connection lost', ports=(1,.3,0,.3), ref='UC-31; FR-85; connection status independent of local job status', test='TC-31')
    p.edge('reconnected', 'offline', 'online', 'Node reconnects', ports=(0,.7,1,.7), ref='UC-31 alternative flow; IV 3.4.2 waiting(node_offline)', test='TC-31')
    for key, sx, corridor in [('online', .2, 364), ('offline', .8, 1056)]:
        p.edge(key+'-revoked', key, 'revoked', 'pairing revoked\n/ reject local jobs; explain reason;\nkeep published objects readable', ports=(sx,1,sx,0),
               points=((corridor,680),(600+sx*240,680)),
               ref='UC-31; FR-110; FR-241; FR-242; end of this pairing, not deletion of Node or results',test='TC-31')
    finish_at(p, 'revoked', 705, 1030)
    p.node('scope-note', 'States describe one pairing, not job execution or dataset processing.\nA lost connection does not revoke the pairing. Re-pairing is outside this lifecycle.\nDesign view only; no implementation verification implied.', 100, 1150, 1250, 100, 'text')
    return p.page


def finish_at(p, source, x, y):
    key = source + '-final'
    p.node(key, '', x, y, 30, 30, 'final')
    p.edge(source + '-complete', source, key,
           ref='UML completion within the depicted lifecycle scope; history remains stored',
           test='Design completion check')


def labelled_route(p, key, source, target, text, ports, points, label_segment, ref, test):
    edge = p.edge(key, source, target, text, ports=ports, points=points, ref=ref, test=test)
    def endpoint(node_id, rx, ry):
        g = p.root.find(f"mxCell[@id='{node_id}']/mxGeometry")
        return float(g.get('x')) + rx * float(g.get('width')), float(g.get('y')) + ry * float(g.get('height'))
    route = [endpoint(source, *ports[:2]), *points, endpoint(target, *ports[2:])]
    lengths = [abs(b[0]-a[0]) + abs(b[1]-a[1]) for a,b in zip(route,route[1:])]
    distance = sum(lengths[:label_segment]) + lengths[label_segment] / 2
    edge.find('mxGeometry').set('x', str(2 * distance / sum(lengths) - 1))
    return edge


def flat_run():
    p = Page('Research Run Orchestration', 'research-run')
    p.node('start', '', 638, 30, 24, 24, 'initial')
    state(p, 'running', 'Running', 'running', 500, 180, 300, 160)
    state(p, 'waiting', 'Waiting', 'waiting', 1100, 500, 400, 160)
    state(p, 'ended', 'Ended', 'ended', 400, 1000, 400, 220)
    p.root.find("mxCell[@id='waiting']").set('reason-values', 'decision,node_offline,budget_review')
    p.root.find("mxCell[@id='ended']").set('result-values', 'complete,with_gaps,failed_technical,cancelled')
    p.node('final', '', 585, 1320, 30, 30, 'final')
    p.edge('begin', 'start', 'running', ref='IV 3.4.1; FR-14; FR-21', test='TC-09')
    # Distinct transitions carry their own trigger, guard and effect.
    for key, trigger, reason, sy, tx, x, ref, tests in [
        ('decision-blocked', 'decisionBlocked', 'decision', .2, .85, 1440, 'FR-262; no independent work; user present or pinned', 'TC-16; TC-98'),
        ('local-job-blocked', 'localJobBlocked', 'node_offline', .5, .5, 1300, 'FR-85; FR-237; FR-238; offline Node and blocking local job; independent work continues; one combined notice', 'TC-31'),
        ('monthly-limit', 'monthlyBudgetReached', 'budget_review', .8, .15, 1160, 'FR-90; monthly budget 100%; create spending item', 'TC-33')]:
        y = 180 + sy * 160
        labelled_route(p, key, 'running', 'waiting', f'{trigger}' + {'decision': ' [present or pinned]', 'node_offline': ' [Node offline]', 'budget_review': ' [usage >= 100%]'}[reason] + f' /\nreason := {reason}',
                       (1, sy, tx, 0), ((x,y),), 0, 'IV 3.4.2; ' + ref, tests)
    for key, trigger, reason, sy, target_x, corridor_x, corridor_y, test in [
        ('decision-answered', 'answerReceived', 'decision', .25, .7, 950, 400, 'TC-16'),
        ('node-returned', 'nodeReconnected', 'node_offline', .5, .5, 900, 430, 'TC-31'),
        ('spend-approved', 'extraSpendApproved', 'budget_review', .75, .3, 850, 460, 'TC-33')]:
        y = 500 + sy * 160
        x = 500 + target_x * 300
        labelled_route(p, key, 'waiting', 'running', f'{trigger} [reason = {reason}]',
                       (0, sy, target_x, 1), ((corridor_x,y),(corridor_x,corridor_y),(x,corridor_y)), 2,
                       'IV 3.4.2; corresponding waiting reason resumes running', test)
    running_ends = [
        ('finished', 'allStagesAccepted /\nresult := complete', 'complete', 100, 940, .2, .2, 'IV 3.4.1 step 10', 'TC-09'),
        ('cancel-running', 'cancel [authorized] /\nresult := cancelled', 'cancelled', 180, 860, .4, .4, 'FR-22; Project Manager or creating Researcher; close pending items; audit', 'TC-13'),
        ('fatal-running', 'fatalError /\nresult := failed_technical', 'failed_technical', 260, 780, .6, .6, 'FR-103; unrecoverable error or missing model/credential; no sample output', 'TC-12'),
        ('budget-running', 'tokenBudgetExhausted /\nresult := with_gaps', 'with_gaps', 340, 700, .8, .8, 'FR-262; publish best output with gaps', 'TC-32'),
    ]
    for key, text, result, corridor_x, corridor_y, sy, tx, ref, test in running_ends:
        y, x = 180 + sy * 160, 400 + tx * 400
        edge = labelled_route(p,key,'running','ended',text,(0,sy,tx,0),
                              ((corridor_x,y),(corridor_x,corridor_y),(x,corridor_y)),2,'IV 3.4.2; '+ref,test)
        edge.set('result-value', result)
    waiting_ends = [
        ('cancel-waiting', 'cancel [authorized] /\nresult := cancelled', 'cancelled', 'FR-22', 'TC-13'),
        ('budget-waiting', 'tokenBudgetExhausted /\nresult := with_gaps', 'with_gaps', 'FR-262; any waiting reason', 'TC-32'),
        ('pinned-expired', 'waitDeadlinePassed [reason = decision and pinned item unanswered] /\nresult := with_gaps', 'with_gaps', 'FR-262; FR-265; close pinned item unanswered', 'TC-98; TC-100'),
        ('spending-closed', 'spendingDeclinedOrExpired [reason = budget_review] /\nresult := with_gaps', 'with_gaps', 'FR-245; FR-91', 'TC-33'),
        ('fatal-waiting', 'fatalError /\nresult := failed_technical', 'failed_technical', 'FR-103; unrecoverable error or missing model/credential', 'TC-12'),
    ]
    for i,(key,text,result,ref,test) in enumerate(waiting_ends):
        sx, ty = .1 + i*.2, .12 + i*.19
        x, y = 1100 + sx*400, 1000 + ty*220
        edge = labelled_route(p,key,'waiting','ended',text,(sx,1,1,ty),((x,y),),1,'IV 3.4.2; '+ref,test)
        edge.set('result-value', result)
    p.edge('lifecycle-complete', 'ended', 'final', ref='Completion of Run lifecycle; result remains stored; no record deletion', test='Design completion check')
    # Running and Waiting form one active region. Only events valid in both
    # substates are inherited from its boundary; reason-specific exits stay local.
    p.node('active-run', 'Active run', 450, -60, 1120, 760, 'composite')
    composite = p.root.find("mxCell[@id='active-run']")
    composite.set('uml-kind', 'composite')
    p.root.remove(composite)
    p.root.insert(2, composite)
    for key in ('start', 'running', 'waiting'):
        cell = p.root.find(f"mxCell[@id='{key}']")
        cell.set('parent', 'active-run')
        geo = cell.find('mxGeometry')
        geo.set('x', str(float(geo.get('x')) - 450))
        geo.set('y', str(float(geo.get('y')) + 60))
    import re
    for key, redundant, y, x, target_x, end_y in [
        ('cancel-running', 'cancel-waiting', 240, 180, 560, 900),
        ('fatal-running', 'fatal-waiting', 360, 260, 640, 840),
        ('budget-running', 'budget-waiting', 480, 340, 720, 780),
    ]:
        p.root.remove(p.root.find(f"mxCell[@id='{redundant}']"))
        edge = p.root.find(f"mxCell[@id='{key}']")
        edge.set('source', 'active-run')
        edge.set('source-ref', edge.get('source-ref') + '; applies in Running and Waiting')
        style = edge.get('style')
        for attr, value in (('exitX', 0), ('exitY', (y + 60) / 760)):
            style = re.sub(rf'{attr}=[^;]+;', f'{attr}={value};', style)
        edge.set('style', style)
        geo = edge.find('mxGeometry')
        for child in list(geo): geo.remove(child)
        points = E.SubElement(geo, 'Array', attrib={'as': 'points'})
        for px, py in ((x, y), (x, end_y), (target_x, end_y)):
            E.SubElement(points, 'mxPoint', x=str(px), y=str(py))
    # Vertical presentation: blocked events on the left, resumes on the right.
    box(p, 'active-run', 100, 0, 1400, 900)
    box(p, 'scope-start', 788, -100)
    box(p, 'start', 728, 90)  # coordinates relative to the composite
    box(p, 'running', 600, 200, 280, 100)
    box(p, 'waiting', 600, 540, 280, 100)
    box(p, 'ended', 700, 1280, 280, 120)
    box(p, 'final', 825, 1510, 30, 30)
    def reroute(key, ports, points, label_pos=0):
        edge = p.root.find(f"mxCell[@id='{key}']")
        style = edge.get('style')
        for attr, value in zip(('exitX', 'exitY', 'entryX', 'entryY'), ports):
            style = re.sub(rf'{attr}=[^;]+;', f'{attr}={value};', style)
        edge.set('style', style)
        geo = edge.find('mxGeometry')
        geo.set('x', str(label_pos))
        for child in list(geo): geo.remove(child)
        if points:
            arr = E.SubElement(geo, 'Array', attrib={'as': 'points'})
            for x, y in points:
                E.SubElement(arr, 'mxPoint', x=str(x), y=str(y))
    for key, port, label_pos in [
        ('decision-blocked', .2, -.65),
        ('local-job-blocked', .5, 0),
        ('monthly-limit', .8, .65),
    ]:
        reroute(key, (port, 1, port, 0), (), label_pos)
    for key, sy, ty, corridor in [
        ('decision-answered', .8, .2, 1400),
        ('node-returned', .5, .5, 1300),
        ('spend-approved', .2, .8, 1200),
    ]:
        reroute(key, (1, sy, 1, ty), ((corridor, 540 + sy*100), (corridor, 200 + ty*100)), -.68)
    reroute('finished', (0, .05, .1, 0), ((-120, 205), (-120, 1220), (728, 1220)), .3)
    for key, y, corridor, bottom, target in [
        ('cancel-running', 380, -30, 1160, 784),
        ('fatal-running', 480, 10, 1100, 840),
        ('budget-running', 580, 50, 1040, 896),
    ]:
        reroute(key, (0, y/900, (target-700)/280, 0), ((corridor, y), (corridor, bottom), (target, bottom)), .45)
    for key, sx, target_y, corridor, turn_y in [
        ('pinned-expired', .95, .7, 1160, 740),
        ('spending-closed', .8, .3, 1100, 820),
    ]:
        reroute(key, (sx, 1, 1, target_y), ((700 + sx*280, turn_y), (corridor, turn_y), (corridor, 1280 + target_y*120)), .45)
    p.page.set('scope', 'One Run; Active run is a sequential composite with Running and Waiting; Ended is outside')
    return p.page


def composite_handoff():
    p = flat_page(handoff(), 'Research Engines')
    revision = p.root.find("mxCell[@id='revise-review']")
    revision.set('value', 'revision checks completed [revision rounds < 2]\n/ revision rounds += 1')
    revision.set('source-ref', 'IV 3.11 steps 6-8; FR-75; completed revision and checks, at most two revision rounds per version')
    relabel(p, {'draft': 'Draft', 'red': 'Checks failed', 'green': 'Checks passed',
                'review': 'Under review', 'ready': 'Ready for acceptance',
                'accepted': 'Accepted', 'locked': 'Locked (AnalysisPlan)', 'stale': 'Stale',
                'repair': 'Checks rerun', 'revise-review': 'Revision checked [round < 2]\n/ round += 1',
                'accept': 'Object accepted', 'lock': 'Plan locked [AnalysisPlan]'})
    p.root.find("mxCell[@id='create']").set('value', '/ round := 0')
    p.root.find("mxCell[@id='create']").set('transition-spec', '/ revision rounds := 0')
    codes = {'draft': 'draft', 'red': 'checks_red', 'green': 'checks_green', 'review': 'in_review',
             'ready': 'ready', 'accepted': 'accepted', 'locked': 'locked', 'stale': 'stale'}
    for key, code in codes.items():
        p.root.find(f"mxCell[@id='{key}']").set('model-state', code)
    positions = [('start', 898, 65, 24, 24), ('draft', 800, 150, 220, 80),
                 ('checks', 760, 350, 300, 80), ('red', 160, 350, 220, 80),
                 ('green', 800, 550, 220, 80), ('review', 800, 750, 220, 80),
                 ('ready', 800, 950, 220, 80), ('accepted', 800, 1150, 220, 80),
                 ('locked', 800, 1350, 220, 80), ('stale', 1580, 950, 220, 80)]
    for args in positions: box(p, *args)
    # Equal 200-unit row pitch and 80-unit node heights keep main gaps at 120 units.
    def route(key, ports=(.5,1,.5,0), points=(), pos=0):
        import re
        cell = p.root.find(f"mxCell[@id='{key}']")
        style = cell.get('style')
        for attr, value in zip(('exitX','exitY','entryX','entryY'), ports):
            style = re.sub(rf'{attr}=[^;]+;', f'{attr}={value};', style)
        cell.set('style', style)
        geo = cell.find('mxGeometry')
        geo.set('x',str(pos))
        for child in list(geo): geo.remove(child)
        if points:
            arr = E.SubElement(geo,'Array',attrib={'as':'points'})
            for x,y in points: E.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    for key in ('create','check','review-start','review-done','accept','lock'): route(key)
    route('red-branch',(0,.5,1,.5),pos=-.4)
    route('green-branch',(1,.5,.8,0),((1130,390),(1130,490),(976,490)),pos=-.65)
    route('repair',(.5,0,.2,.2),((270,250),(820,250),(820,310)),pos=-.6)
    route('revise-review',(0,.5,.5,1),((560,790),(560,470),(910,470)),pos=-.25)
    route('regression',(1,.2,.8,.2),((1260,566),(1260,270),(1000,270),(1000,310)),pos=.3)
    p.page.set('scope', 'One hand-off object version; round aliases revision rounds; no automatic refresh of stale versions')
    p.root.find("mxCell[@id='review']").set('state-behavior', 'Includes asynchronous revision work and checks; at most two revision rounds; remaining findings become known risks or await user decision (IV 3.11)')
    # One inherited invalidation transition replaces seven identical leaf transitions.
    p.node('current-version', 'Current version (not stale)', 80, 0, 1280, 1490, 'composite')
    container = p.root.find("mxCell[@id='current-version']")
    container.set('uml-kind','composite')
    p.root.remove(container)
    p.root.insert(2,container)
    for cell in list(p.root):
        if cell.get('id') in {'0','1','current-version','scope-start','scope-entry','stale'}:
            continue
        if cell.get('parent') != '1': continue
        cell.set('parent','current-version')
        geo = cell.find('mxGeometry')
        if cell.get('vertex')=='1':
            geo.set('x',str(float(geo.get('x','0'))-80))
        for point in geo.findall('./Array/mxPoint'):
            point.set('x',str(float(point.get('x','0'))-80))
    box(p,'stale',1580,750,220,80)
    p.edge('version-invalidated','current-version','stale',
           'upstreamVersionChanged',ports=(1,790/1490,0,.5),
           ref='IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes',
           test='TC-11')
    p.root.find("mxCell[@id='version-invalidated']").set('guard-expression','pinned upstream object has a new version')
    p.page.set('scope','One hand-off object version; seven non-stale states inside one composite; upstreamVersionChanged exits the composite to stale')
    return p.page


def flat_decision():
    p = flat_page(decision_item(), 'AI Principal Investigator')
    relabel(p, {'human-answer': 'authorized user answers',
                'tentative-decision': 'AI PI decides\n[autopilot; away; non-pinned]',
                'pinned-timeout': 'pinned deadline passed\n[no answer]',
                'spending-timeout': 'spending deadline passed\n[no answer]'})
    p.root.find("mxCell[@id='user-review']").set('value', 'userDecisionSubmitted')
    for key, guard in [('tentative-decision', 'autopilot and away and not pinned'),
                       ('pinned-timeout', 'pinned item and no answer'),
                       ('spending-timeout', 'spending item and no answer')]:
        p.root.find(f"mxCell[@id='{key}']").set('guard-expression', guard)
    p.root.find("mxCell[@id='confirmed-branch']").set('effect', 'record confirmation in decision log')
    p.root.find("mxCell[@id='overturned-branch']").set('effect', 'undo dependent work; mark affected objects stale; record overturn in decision log')
    box(p, 'closed-cancelled', 1550, 700, 320, 80)
    p.edge('pending-cancelled', 'pending', 'closed-cancelled', 'run cancelled', ports=(.85, 0, 1, .5),
           points=((598, 60), (1950, 60), (1950, 740)),
           ref='IV 3.4.1 alternative flow; FR-22; still pending', test='TC-13')
    p.edge('tentative-cancelled', 'tentative', 'closed-cancelled', 'run cancelled', ports=(1, .3, 0, .5),
           points=((1450, 214), (1450, 740)),
           ref='IV 3.4.1 alternative flow; FR-22; awaiting user review', test='TC-13')
    # Explicit completion transitions share their final route visually.
    p.node('decision-final', '', 745, 1320, 30, 30, 'final')
    for key, x in [('answered', 390), ('spending-expired', 240),
                   ('unanswered', 540), ('overturned', 760),
                   ('confirmed', 1150), ('closed-cancelled', 1710)]:
        ports = (1, .5, .5, 0) if key == 'answered' else (.5, 1, .5, 0)
        points = [(390, 560)] if key == 'answered' else []
        points += [(x, 1100)]
        if x != 760: points.append((760, 1100))
        p.edge(key + '-complete', key, 'decision-final', ports=ports, points=points,
               ref='Completion of Decision Item lifecycle; history remains stored',
               test='Design completion check')
    return p.page


def notifications():
    p = Page('Notifications & Integrations', 'notifications-integrations')
    for key, text, x, y in [('pending', 'Pending', 400, 130), ('sending', 'Sending', 850, 480),
                            ('skipped', 'Skipped', 40, 480), ('sent', 'Sent', 1120, 1030), ('failed', 'Failed', 570, 1030)]:
        p.node(key, text, x, y, 240, 80)
    p.node('start', '', 508, 30, 24, 24, 'initial')
    p.node('allowed', 'Should the email\nbe sent?', 385, 310, 270, 110, 'choice')
    p.node('success', 'Was delivery\nsuccessful?', 835, 740, 270, 110, 'choice')
    p.edge('queue', 'start', 'pending', ref='IV 2.2.16 notification_emails; IV 3.7', test='TC-38')
    p.edge('dispatch', 'pending', 'allowed', 'dispatchRequested', ref='IV 2.2.16; FR-100; notification settings', test='TC-38')
    p.edge('skip', 'allowed', 'skipped', 'No', ports=(0, .5, .5, 0), points=((160, 365),), pos=-.7, ref='IV 2.2.16 skipped; suppression condition proposed from settings', test='TC-38')
    p.edge('send', 'allowed', 'sending', 'Yes', ports=(1, .5, .5, 0), points=((970, 365),), pos=-.7, ref='IV 2.2.16 sending; FR-100', test='TC-38')
    p.edge('delivery-result', 'sending', 'success', 'deliveryResultReceived', ref='IV 2.2.16', test='TC-38')
    p.edge('delivery-no', 'success', 'failed', 'No', ports=(0, .5, .5, 0), points=((690, 795),), pos=-.7, ref='IV 2.2.16 failed', test='TC-38')
    p.edge('delivery-yes', 'success', 'sent', 'Yes', ports=(1, .5, .5, 0), points=((1240, 795),), pos=-.7, ref='IV 2.2.16 sent; provider accepted, not inbox proof', test='TC-38')
    p.edge('retry', 'failed', 'pending', 'retry scheduled\n(proposed)', ports=(.5, 1, 0, .5), points=((690, 1210), (-100, 1210), (-100, 170)), pos=.3, ref='Design proposal for notification_emails; IV 2.2.16 attempts does not establish retry policy; no confirmed retry limit or terminal failure rule', test='Design retry check')
    p.node('scope-heading', 'Notification email (proposed delivery lifecycle)', 40, -30, 1250, 35, 'text')
    p.node('retry-scope', 'Email retry policy is not specified. Failed can remain failed.\nThis view does not define webhook or integration delivery states.', 40, 1290, 1250, 70, 'text')
    finish_at(p, 'skipped', 145, 660)
    finish_at(p, 'sent', 1225, 1180)
    return p.page


def monitoring():
    p = Page('Administration & Monitoring', 'administration-monitoring')
    p.node('start', '', 468, 30, 24, 24, 'initial')
    p.node('active', 'Active alert', 360, 130, 240, 80)
    p.node('resolved', 'Resolved alert', 820, 650, 240, 80)
    p.edge('raised', 'start', 'active', ref='IV 2.2.38 monitoring_alerts active; FR-104', test='TC-05')
    p.edge('acknowledged', 'active', 'active', 'acknowledged', ports=(1, .3, 1, .7), points=((930, 154), (930, 186)), ref='III 3.9.9; IV 2.2.38 acknowledged_at; acknowledgement does not resolve status', test='TC-05')
    p.edge('resolution-reported', 'active', 'resolved', 'resolution reported\n/ record resolved_at', points=((480, 470), (940, 470)), ref='IV 2.2.38 status resolved; resolved_at; design event abstraction, no resolver or automatic resolution algorithm specified', test='TC-05')
    finish_at(p, 'resolved', 925, 830)
    return p.page


def project_workspace():
    p = flat_page(project(), 'Project Workspace')
    relabel(p, {'complete': 'marked completed', 'archive-completed': 'archived', 'archive-active': 'archived', 'edit': 'project updated'})
    p.node('project-heading', 'Project', 320, -30, 250, 30, 'text')
    finish_at(p, 'archived', 415, 830)
    d = flat_page(dossier(), 'Dossier')
    drop_edges(d)
    for args in [('start', 1208, 30), ('pending', 1100, 130, 240, 80),
                 ('enough', 1085, 330, 270, 110), ('approved', 1500, 540, 240, 80),
                 ('superseded', 1100, 1030, 240, 80)]:
        box(d, *args)
    relabel(d, {'pending': 'Not approved', 'approved': 'Approved', 'superseded': 'Superseded'})
    d.node('heading', 'Dossier version N', 1100, -30, 300, 30, 'text')
    d.edge('create', 'start', 'pending', ref='IV 3.14; FR-94; FR-249; accepted PaperPack and EvidenceBundle, check hashes', test='TC-35')
    d.edge('approval', 'pending', 'enough', 'approval recorded', ref='IV 3.14; FR-95; eligible approver under review settings', test='TC-35')
    d.edge('not-enough', 'enough', 'pending', 'No', ports=(0, .5, 0, .5), points=((950, 385), (950, 170)), pos=-.7, ref='FR-95; fewer eligible approvals than required', test='TC-35')
    d.edge('approval-yes', 'enough', 'approved', 'Yes', ports=(1, .5, .5, 0), points=((1620, 385),), pos=-.7, ref='FR-95; enough eligible approvals', test='TC-35')
    d.edge('export', 'approved', 'approved', 'pinned export authorized\n/ export; audit version + format', ports=(.3, 1, 0, .5), points=((1572, 760), (1430, 760), (1430, 580)), ref='FR-97; FR-98; pinned export approval, audit version and format', test='TC-36')
    d.edge('pending-superseded', 'pending', 'superseded', 'new accepted version', ports=(1, .25, 1, .8), points=((1840, 150), (1840, 1094)), ref='FR-96; FR-251; FR-252; new accepted EvidenceBundle or PaperPack; N+1 needs new approvals', test='TC-35')
    d.edge('approved-superseded', 'approved', 'superseded', 'new accepted version', ports=(.8, 1, 1, .2), points=((1692, 1046),), ref='FR-96; FR-251; FR-252; old approvals retained as history', test='TC-35')
    finish_at(d, 'superseded', 1205, 1220)
    for cell in list(d.root):
        if cell.get('id') in {'0', '1'}: continue
        cell.set('id', 'dossier-' + cell.get('id'))
        for attr in ('source', 'target'):
            if cell.get(attr): cell.set(attr, 'dossier-' + cell.get(attr))
        p.root.append(cell)
    return p.page


def normalize_choice_guards(page):
    conditions = {
        'checks': ('all contract items green', 'at least one contract item red'),
        'dossier-enough': ('eligible approvals meet review settings', 'eligible approvals below requirement'),
        'confirms': ('submitted decision is confirm', 'submitted decision is overturn'),
        'allowed': ('external notice allowed by policy and preferences', 'external notice disallowed by policy or preferences'),
        'success': ('provider accepted delivery', 'delivery failed'),
        'resolved-question': ('alert status is resolved', 'alert status is active'),
    }
    cells = {c.get('id'): c for c in page.findall('.//mxCell')}
    for edge in cells.values():
        if edge.get('edge') != '1' or edge.get('value') not in {'Yes', 'No'}: continue
        answer = edge.get('value')
        predicate = conditions[edge.get('source')][0 if answer == 'Yes' else 1]
        edge.set('value', f'[{answer}]')
        edge.set('branch-answer', answer)
        edge.set('guard-expression', predicate)
        cells[edge.get('source')].set('guard-' + answer.lower(), predicate)


def apply_reference_style(page):
    """FI2M lifecycle-image profile; preserve all state/transition semantics."""
    if page.get('reference-style') == 'fi2m-lifecycle-v1': return
    scale = .72
    labels = {
        'request-code': 'Code requested',
        'paired': 'Pairing succeeds',
        'online-revoked': 'Pairing revoked',
        'offline-revoked': 'Pairing revoked',
        'decision-blocked': 'Decision blocks work',
        'monthly-limit': 'Monthly budget reached',
        'local-job-blocked': 'Node offline',
        'node-returned': 'Node reconnects',
        'decision-answered': 'Decision answered',
        'spend-approved': 'Extra spend approved',
        'finished': 'All stages accepted',
        'cancel-running': 'Run cancelled',
        'cancel-waiting': 'Run cancelled',
        'fatal-running': 'Technical failure',
        'fatal-waiting': 'Technical failure',
        'budget-running': 'Token budget exhausted',
        'budget-waiting': 'Token budget exhausted',
        'pinned-expired': 'Pinned wait expires',
        'spending-closed': 'Spending declined or expired',
        'user-review': 'Decision submitted',
        'tentative-decision': 'AI PI decides [eligible]',
        'pinned-timeout': 'Pinned deadline expires',
        'spending-timeout': 'Spending deadline expires',
        'revise-review': 'Revision checked [round < 2]',
        'dossier-export': 'Export authorized',
        'resolution-reported': 'Resolution reported',
        'retry': 'Retry scheduled (proposed)',
        'dispatch': 'Dispatch requested',
        'delivery-result': 'Delivery result received',
        'status-update': 'Alert status updated',
    }
    for cell in page.findall('.//mxCell'):
        if cell.get('vertex') != '1' and cell.get('edge') != '1': continue
        style = dict(item.split('=',1) for item in cell.get('style','').split(';') if '=' in item)
        if cell.get('vertex') == '1':
            if 'uml-kind' not in cell.attrib:
                kind = 'text' if ';text;' in cell.get('style','') else 'choice' if 'rhombus;' in cell.get('style','') else 'final' if style.get('shape') == 'endState' else 'initial' if not cell.get('value') and 'ellipse;' in cell.get('style','') else 'state'
                cell.set('uml-kind',kind)
            size = 14 if style.get('fontStyle') == '1' else 12
        else:
            size = 11
            full = cell.get('value','')
            if full:
                if 'transition-spec' not in cell.attrib:
                    cell.set('transition-spec',full)
            value = labels.get(cell.get('id'),full)
            value = value.replace('upstreamVersionChanged','New upstream version')
            cell.set('value',value)
        # Keep non-key shape prefixes (rhombus / ellipse / text) intact.
        pieces = [item for item in cell.get('style','').split(';') if item and not item.startswith('fontSize=')]
        cell.set('style',';'.join(pieces) + f';fontSize={size};')
        geo = cell.find('mxGeometry')
        if cell.get('vertex') == '1':
            for key in ('x','y','width','height'):
                if geo.get(key) is not None: geo.set(key,str(round(float(geo.get(key))*scale,3)))
        for point in geo.findall('.//mxPoint'):
            for key in ('x','y'):
                if point.get(key) is not None: point.set(key,str(round(float(point.get(key))*scale,3)))
    page.set('reference-style','fi2m-lifecycle-v1')


def remove_composite_frames(page):
    """Replace inherited exits with explicit leaf transitions."""
    name = page.get('name')
    if name not in {'Research Run Orchestration', 'Research Engines'}:
        return page
    cells = {c.get('id'): c for c in page.findall('.//mxCell')}
    if name == 'Research Run Orchestration':
        inherited = [(deepcopy(cells[key]), source) for key in ('cancel-running', 'fatal-running', 'budget-running') for source in ('running', 'waiting')]
    else:
        inherited = [(deepcopy(cells['version-invalidated']), source) for source in ('draft', 'red', 'green', 'review', 'ready', 'accepted', 'locked')]
    p = flat_page(page, name)
    if name == 'Research Engines':
        box(p, 'stale', 1700, 750, 220, 160)
    import re
    for edge, source in inherited:
        original = edge.get('id')
        edge.set('id', original + '-' + source)
        edge.set('source', source)
        edge.set('parent', '1')
        edge.set('transition-spec', edge.get('transition-spec', edge.get('value', '')))
        if name == 'Research Run Orchestration':
            labels = {'cancel-running': 'Run cancelled', 'fatal-running': 'Technical failure', 'budget-running': 'Token budget exhausted'}
            edge.set('value', labels[original])
            idx = ('cancel-running', 'fatal-running', 'budget-running').index(original)
            if source == 'running':
                sx, sy, tx, ty = 0, (.25 + .25*idx), 0, (.7 - .25*idx)
                x = (-80, -30, 20)[idx]
                y = 1280 + ty*120
                points = ((x, 200 + sy*100), (x, y))
            else:
                sx, sy, tx, ty = (.15 + .2*idx), 1, (.15 + .2*idx), 0
                points = ()
            style = BASE + f'edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endSize=7;endFill=1;labelBackgroundColor=#ffffff;exitX={sx};exitY={sy};entryX={tx};entryY={ty};exitPerimeter=1;entryPerimeter=1;'
        else:
            edge.set('value', 'New upstream version')
            sx, sy, tx, ty = 1, .5, 0, (.1 + .12 * ('draft', 'red', 'green', 'review', 'ready', 'accepted', 'locked').index(source))
            lanes = {'green': (1080, 590, 770), 'review': (1080, 790, 800),
                     'ready': (1150, 990, 830), 'accepted': (1250, 1190, 860),
                     'locked': (1350, 1390, 890)}
            style = BASE + 'edgeStyle=none;endArrow=classic;endSize=7;endFill=1;labelBackgroundColor=#ffffff;'
            points = ()
            if source in lanes:
                x, from_y, to_y = lanes[source]
                entry = (to_y - 750) / 160
                style = BASE + f'edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endSize=7;endFill=1;labelBackgroundColor=#ffffff;exitX=1;exitY=.5;entryX=0;entryY={entry};exitPerimeter=1;entryPerimeter=1;'
                points = ((x, from_y), (x, to_y))
            if source == 'draft':
                style = BASE + 'edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endSize=7;endFill=1;labelBackgroundColor=#ffffff;exitX=1;exitY=.5;entryX=.5;entryY=0;'
                points = ((1950,190), (1950,700), (1810,700))
            if source == 'red':
                style = BASE + 'edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endSize=7;endFill=1;labelBackgroundColor=#ffffff;exitX=0;exitY=.5;entryX=.5;entryY=1;'
                points = ((-40,390), (-40,1510), (1810,1510))
        edge.set('style', style)
        geo = edge.find('mxGeometry')
        if name == 'Research Run Orchestration':
            geo.set('x', '0.75' if source == 'running' else str((-.65, 0, .65)[idx]))
        else:
            geo.set('x', '0.5' if source in {'green', 'review', 'ready', 'accepted', 'locked'} else '-0.55')
        for child in list(geo): geo.remove(child)
        if points:
            arr = E.SubElement(geo, 'Array', attrib={'as': 'points'})
            for x, y in points: E.SubElement(arr, 'mxPoint', x=str(x), y=str(y))
        p.root.append(edge)
    if name == 'Research Run Orchestration':
        edge = p.root.find("mxCell[@id='finished']")
        edge.set('style', re.sub(r'entryX=[^;]+;entryY=[^;]+;', 'entryX=0;entryY=0.95;', edge.get('style')))
        geo = edge.find('mxGeometry')
        for child in list(geo): geo.remove(child)
        arr = E.SubElement(geo, 'Array', attrib={'as': 'points'})
        for x, y in ((-150,205), (-150,1394)):
            E.SubElement(arr, 'mxPoint', x=str(x), y=str(y))
    p.page.set('scope', 'Flat lifecycle; formerly inherited exits are explicit transitions from each applicable state')
    return p.page


def build():
    mx = E.Element('mxfile', host='drawio', version='26.0.0')
    combined = project_workspace()
    root = combined.find('./mxGraphModel/root')
    for cell in list(root):
        if cell.get('id', '').startswith('dossier-'):
            root.remove(cell)
    pages = [account_lifecycle(), combined, dataset_lifecycle(), flat_run(), composite_handoff(), flat_decision(), notification_lifecycle(), monitoring()]
    for page in pages:
        page = remove_composite_frames(page)
        # Scope and explanatory notes belong in the companion design, not on the image.
        root = page.find('./mxGraphModel/root')
        for cell in list(root):
            if cell.get('vertex') == '1' and ';text;' in cell.get('style', ''):
                root.remove(cell)
        normalize_choice_guards(page)
        apply_reference_style(page)
        if page.get('name') == 'Research Engines':
            geometry = page.find(".//mxCell[@id='check']/mxGeometry")
            E.SubElement(geometry, 'mxPoint', x='0', y='-20', attrib={'as': 'offset'})
        if page.get('name') == 'Project Workspace':
            geometry = page.find(".//mxCell[@id='edit']/mxGeometry")
            geometry.set('x', '-0.5')
            E.SubElement(geometry, 'mxPoint', x='0', y='14', attrib={'as': 'offset'})
        coordinates = [(float(g.get('x', '0')), float(g.get('y', '0')))
                       for g in page.findall('.//mxCell[@vertex="1"]/mxGeometry')]
        coordinates += [(float(g.get('x', '0')), float(g.get('y', '0')))
                        for g in page.findall('.//mxCell[@edge="1"]/mxGeometry/Array/mxPoint')]
        dx = max(0, 40 - min(x for x, y in coordinates))
        dy = max(0, 40 - min(y for x, y in coordinates))
        for cell in page.findall('.//mxCell'):
            if cell.get('parent') != '1':
                continue
            geo = cell.find('mxGeometry')
            if geo is None:
                continue
            if cell.get('vertex') == '1':
                geo.set('x', str(float(geo.get('x', '0')) + dx))
                geo.set('y', str(float(geo.get('y', '0')) + dy))
            else:
                for point in geo.findall('./Array/mxPoint'):
                    point.set('x', str(float(point.get('x', '0')) + dx))
                    point.set('y', str(float(point.get('y', '0')) + dy))
        # Store all edge routes in root coordinates, matching the validator's
        # absolute-waypoint contract while preserving nested state geometry.
        cells = {cell.get('id'): cell for cell in page.findall('.//mxCell')}
        for cell in cells.values():
            if cell.get('edge') != '1' or cell.get('parent') == '1':
                continue
            parent = cells[cell.get('parent')]
            parent_geo = parent.find('mxGeometry')
            dx, dy = float(parent_geo.get('x', '0')), float(parent_geo.get('y', '0'))
            for point in cell.findall('./mxGeometry/Array/mxPoint'):
                point.set('x', str(float(point.get('x', '0')) + dx))
                point.set('y', str(float(point.get('y', '0')) + dy))
            cell.set('parent', '1')
        # Preserve the hand-adjusted routes in the editable diagram.
        manual_routes = {
            'Research Engines': {
                'regression': [(976.0, 407.5), (976.0, 194.38), (778.0, 194.38)],
                'repair': [(263.19, 180.0), (670.0, 180.0)],
                'version-invalidated-draft': [(1372.0, 136.78)],
            },
            'AI Principal Investigator': {
                'pending-cancelled': [(430.59, 110.06), (1231.18, 110.06)],
            },
        }
        for key, points in manual_routes.get(page.get('name'), {}).items():
            edge = page.find(f".//mxCell[@id='{key}']")
            geo = edge.find('mxGeometry')
            for arr in geo.findall("Array[@as='points']"):
                geo.remove(arr)
            arr = E.SubElement(geo, 'Array', attrib={'as': 'points'})
            for x, y in points:
                E.SubElement(arr, 'mxPoint', x=str(x), y=str(y))
            if key == 'pending-cancelled':
                style = edge.get('style').replace('entryX=1;', 'entryX=0.5;').replace('entryY=0.5;', 'entryY=0;').replace('entryPerimeter=1;', '')
                edge.set('style', style + 'entryDx=0;entryDy=0;')
        mx.append(page)
    E.indent(mx, space='  ')
    target = OUT / f'{NAME}.drawio'
    E.ElementTree(mx).write(target, encoding='utf-8', xml_declaration=True)
    write_design(mx)
    print(target)


def write_design(mx):
    inventory = [
        ('Authentication-Account', 'III 3.9.1; IV 2.2.1', 'Vòng đời account active/suspended; initial active là diễn giải thiết kế, không xác nhận runtime.'),
        ('Project-Workspace', 'III 3.3.1–3.3.3; IV 3.2.14', 'Vòng đời khái niệm Project gồm Active, Completed, Archived; Archived là read-only. Schema IV 2.2.6 dùng status draft/data_ready/researching/needs_review/completed và archived_at; quan hệ giữa hai cách biểu diễn chưa được đặc tả. Không coi Active/Archived là enum schema. Dossier không thuộc tám hình chính.'),
        ('Data-Management', 'III 3.4.1, 3.4.4, 3.4.5; FR-09', 'Vòng đời Dataset ở mức khái niệm: tồn tại, thêm version immutable và kết thúc khi xóa được cho phép. Available không phải enum schema; điều kiện xóa chưa được đặc tả đầy đủ.'),
        ('Research-Run-Orchestration', 'IV 3.4.2, Figure IV-7; IV 3.13', 'Một state machine liền mạch, chỉ ba state Running/Waiting/Ended theo enum RunState của Class Diagram và FR-21. Waiting có reason decision/node_offline/budget_review; node_offline khi Node offline và local job chặn việc; reconnect đưa về running, independent work và một combined notice theo FR-237/238; Ended có result complete/with_gaps/failed_technical/cancelled. Đây là field của state, không phải nhiều state trùng tên. Bố cục dọc đặt Running trên Waiting; các transition sang Waiting đi thẳng xuống và các nhánh tiếp tục đi bên phải. Không dùng composite; cancel, fatal error và token exhaustion có transition riêng từ Running và Waiting. Các nhánh chỉ áp dụng Running hoặc Waiting giữ riêng. Metadata và bảng giữ đầy đủ điều kiện và phép gán reason/result. Từ running: all stages accepted, token exhaustion, cancel, technical failure; từ waiting(decision): pinned deadline unanswered, token exhaustion, cancel, technical failure; từ waiting(budget_review): spending decline/expiry, token exhaustion, cancel, technical failure. Không lặp state hay tách các cụm tình huống rời; mỗi transition là nét liền có trigger [guard] / effect khi cần. Tên event/effect là ký hiệu thiết kế từ hành vi, không chốt event/API implementation. Chỉ complete khi tất cả stage accepted. Cancel chỉ bởi Project Manager hoặc creating Researcher. Pinned item không hết hạn trước wait deadline. Khôi phục nhánh node_offline theo yêu cầu mới như thiết kế dự kiến; không khẳng định Local Node đã triển khai.'),
        ('Research-Engines', 'IV 3.4.3, Figure IV-8; IV 3.11; IV 3.8', 'Một version của Hand-off Object gồm draft, checks_red, checks_green, in_review, ready, accepted, locked và stale. Mỗi state chưa stale có transition riêng sang Stale khi pinned upstream có version mới; không dùng composite. Locked chỉ áp dụng AnalysisPlan. Revision tối đa hai vòng; Stale giữ lịch sử, không tự phục hồi. Điều kiện, effect và nguồn đầy đủ nằm trong metadata và bảng transition.'),
        ('AI-Principal-Investigator', 'IV 3.6.7; IV 3.5.2; IV 3.13; FR-22/28/31/91/265', 'Đủ nhánh human answer, AI PI tentative decision, user confirm/overturn, pinned timeout, spending timeout, cancel khi còn pending/awaiting user review. AI PI chỉ được tentative ở autopilot + away + non-pinned. Overturn undo dependent work, đánh dấu affected objects stale và ghi decision log. Confirm cũng ghi log. Timeout pinned đóng unanswered, end run with gaps, không ai quyết định thay user. Closed khi run cancelled nằm bên phải; các transition hoàn tất dùng chung đường vẽ tới một final, không có junction. Nhãn Pending/Answered/Confirmed/Overturned/Closed là thiết kế từ hành vi, không khẳng định enum implementation.'),
        ('Notifications-Integrations', 'III 3.8.4; IV 2.2.14', 'Vòng đời notification trong ứng dụng theo read_at: unread và read là diễn giải, không phải enum. Email delivery không thuộc tám hình chính.'),
        ('Administration-Monitoring', 'III 3.9.9; IV 2.2.38 monitoring_alerts; IV 3.8; FR-104', 'Vòng đời một monitoring alert: active/resolved theo schema. Acknowledge là self-transition ghi acknowledged_at/by, không đồng nghĩa resolve. Resolution reported là event thiết kế cho việc ghi nhận resolved và resolved_at; nối trực tiếp Active tới Resolved, không thêm choice chỉ để đọc status. Không khẳng định ai hoặc thuật toán nào tự resolve. Không tự thêm reopen resolved alert; sự cố mới có thể là alert mới nhưng nguồn chưa chốt identity rule.'),
    ]
    lines = [
        '# State Machine Diagrams — các vòng đời theo nhóm chức năng', '',
        '- [File draw.io chung tám tab](State-Machine-Diagrams.drawio)',
        '- [Builder](build_state_diagrams.py)', '- [Rule](rule.md)', '',
        'Nguồn: `C:/Users/ADMIN/Downloads/FA26SE115_Report7 (1).md`. Cách chia tab theo [Class Diagram](../07-class/Class-Diagrams-design.md), không suy từ số entity lifecycle. Đối chiếu [Report IV](../../report/04-software-design-document.md).', '',
        '## Inventory', '', '| Tab | PNG | Nguồn |', '|---|---|---|',
    ]
    for i, (page, (slug, source, _)) in enumerate(zip(mx.findall('diagram'), inventory), 1):
        lines.append(f'| {i}. {page.get("name")} | [{slug}]({i:02d}-{slug}.png) | {source} |')
    lines += ['', '## Report mẫu tham khảo hình', '',
        'File tham khảo: `C:/Users/ADMIN/Downloads/Copy of 9927_HCM_SU26SE109_GSU41_HCM_GSU26SE41_FI2M_Report7_Final_Project_Report.docx.md`. SHA-256 file mẫu: `6ea83525979bbee6a8282c3122615a421b0cabf2174b32a5e5045f29f3428b74`. Các ảnh nhúng base64 đã được mở xem ở độ phân giải gốc; dùng để chọn cách trình bày, không nhập nghiệp vụ thiết bị/venue vào dự án.', '',
        '| Ảnh nhúng | Caption / mục trong report mẫu | Cách áp dụng |', '|---|---|---|',
        '| image118 | IV 3.1.4, Borrow Request (caption ghi Class Diagram nhưng nội dung là lifecycle) | Tên state ngắn, luồng chính và nhánh phụ; không sao chép lỗi caption/ảnh nhỏ. |',
        '| image128 | Figure 4.3.3.5.1 Lecturer Account Lifecycle | Sự kiện bằng lời, guard đặt trên đường, vòng quay lại ở ngoài. |',
        '| image131 | Figure 4.3.4.3.1 Equipment SKU Lifecycle | Một state một ô, nhiều transition có nguồn/đích rõ; không thu chữ nhỏ như ảnh gốc. |',
        '| image135 | Figure 4.3.5.4.1 Inventory Audit Session Lifecycle | Trục dọc, nhánh completed/cancelled rõ, initial/final tối giản. |',
        '| image144–147 | Figure 4.3.7.3.1–4 Venue | Phân biệt nhóm luồng chức năng có câu hỏi/Yes-No với lifecycle entity; chỉ dùng bố cục choice đã chốt. |',
        '| image150 | Figure 4.3.8.3.1 Create a booking | Nhánh kiểm tra/ngoại lệ ở hai bên; không mang CRUD/HTTP lỗi sang state của dự án. |',
        '| image153 | Figure 4.3.9.3.1 Penalty & Credibility | Tham khảo cách ghi điều kiện; không sao chép điểm gom/ký hiệu không cần. |',
        '| image157 | Figure 4.3.10.3.1 Maintenance | State gọn và sự kiện ngắn, initial → state → final. |',
        '| image161 | Figure 4.3.11.3.1 Disposal | Bố cục ngắn, nhãn nghiệp vụ dễ đọc. |', '',
        'Profile áp dụng: Arial state 12/transition 11, cùng tỉ lệ bố cục compact; tiêu đề con 14. Nhãn hiển thị bằng lời như User cancels/Node reconnects/All stages accepted. transition-spec giữ trigger/guard/effect gốc; bảng bên dưới ghi cả nhãn ảnh và biểu thức đầy đủ. Không bỏ trạng thái, transition, reason/result hoặc predicate để làm hình gọn. Giữ nền trắng, state bo góc theo UML, không sao chép viền vuông/cắt ảnh/chữ quá nhỏ từ report mẫu.', '',
    ]
    lines += ['', '## Cách đọc và mức thiết kế', '',
        'Giữ đầy đủ trạng thái và nhánh; Research Engines và Research Run dùng state phẳng, các transition chung được vẽ riêng từ từng state; các view khác giữ bố cục hiện có. Câu hỏi trong hình thoi, guard [No] trái/[Yes] phải; Yes/No là alias của biểu thức guard ở bảng dưới, không phải event. Nhãn ngắn nằm trực tiếp trên đường nối nền trắng; điều kiện, effect và reference đầy đủ ở bảng dưới. Research Engines có transition riêng từ từng state tới Stale; các nhánh revision giữ đường riêng; không dùng nhãn chung end event. Mỗi vòng đời là một graph liền mạch, mỗi state chỉ xuất hiện một lần; không tách các cụm sự kiện rồi vẽ lại state. Các transition dùng nét liền và đầu mũi tên mặc định có tô. Nhãn theo trigger [guard] / effect; choice chỉ phân nhánh tức thời theo guard; không đợi event ở đường ra. Event userDecisionSubmitted phải tới trước choice confirm/overturn. Reason/result là field context, giá trị và phép gán đầy đủ ở metadata/bảng transition; không cần ô chú thích kỹ thuật riêng trên ảnh theo profile report mẫu. model-state trong XML ánh xạ nhãn dễ đọc về state code nguồn. Đường chính/hồi tiếp vuông góc; transition tới Stale áp dụng khi pinned upstream có version mới. Final đánh dấu kết thúc phạm vi mô tả; tác động lưu trữ phải đọc theo transition và nguồn của từng đối tượng.', '',
        'Tám tab thể hiện một đối tượng chính cho mỗi nhóm. Dataset available và notification unread/read là cách diễn giải vòng đời, không phải enum xác nhận trong schema. Nhánh Local Node trong Run vẫn là thiết kế dự kiến.', '',
        'Các status lấy từ nguồn nhưng một enum không tự xác nhận đầy đủ transition. Những nhãn hay transition diễn giải được chỉ rõ trong từng mục. Không đổi nghiệp vụ BRD/PRD/Use Case Spec; không thay placeholder Word. Final UML đánh dấu hoàn tất vòng đời/region; với Dataset, transition vào final là xóa được cho phép, còn ý nghĩa lưu trữ sau xóa chưa được đặc tả. Run có completion từ Ended tới final, result vẫn lưu; Email Code Sign-In kết thúc một lần đăng nhập. Archived và Superseded kết thúc vòng đời trong phạm vi hình, không kết luận record bị xóa hoặc hệ thống không bao giờ có chức năng khôi phục. Các Decision Item đã trả lời/đóng, email Sent/Skipped và alert Resolved đều nối final. Decision Item gom đường vẽ các transition hoàn tất về một final chung; các view khác có thể dùng final riêng. Stale giữ lịch sử version; acceptance/rerun upstream-downstream không phải tự sửa version cũ. Không thêm final/transition phục hồi chưa chốt. Failed có thể giữ nguyên; retry email là đề xuất, không bảo đảm luôn retry.', '',
        'Test ID trong metadata/bảng là tham chiếu kịch bản, không phải kết quả test runtime. Design routing/retry check là kiểm tra thiết kế còn cần bổ sung, không bịa TC ID.', '',
    ]
    lines += ['## Hiệu chỉnh sau review 2026-10-30', '', 'Bảo toàn transition-spec trước khi rút gọn nhãn. Nhãn AI PI [eligible] là alias của guard autopilot and away and not pinned; guard đầy đủ, timeout và effect confirm/overturn lưu trong metadata và bảng. Result của Run được giữ trong metadata và bảng. Review bao gồm revision work; sự kiện hoàn tất checks có guard tối đa hai vòng. Phạm vi stale version được ghi trong thuyết minh; email retry ghi proposed. Monitoring dùng resolution reported trực tiếp.', '', 'Giới hạn chưa chốt: cách ưu tiên nhiều blocker đồng thời của Run; identity/liên kết item tentative; chính sách retry và kết thúc failure email. Không tự thêm thuật toán hoặc transition cho các điểm này.', '']
    for i, (page, (_, source, note)) in enumerate(zip(mx.findall('diagram'), inventory), 1):
        lines += [f'## {i}. {page.get("name")}', '', source + '.', '', note, '']
        cells = {c.get('id'): c for c in page.findall('.//mxCell')}
        lines += ['| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |', '|---|---|---|---|']
        for c in cells.values():
            if c.get('edge') != '1' or c.get('semantic-kind') == 'comment-link': continue
            src, dst = cells[c.get('source')], cells[c.get('target')]
            def label(cell):
                if cell.get('value'):
                    code = cell.get('model-state')
                    return cell.get('value') + (f' ({code})' if code and code != cell.get('value') else '')
                return 'Junction' if cell.get('uml-kind') == 'junction' else 'Final' if cell.get('uml-kind') == 'final' or 'shape=endState' in cell.get('style','') else 'Initial'
            row = [label(src) + ' → ' + label(dst), c.get('value') or '(nối đường)', ('UML: ' + c.get('transition-spec') + '; ' if c.get('transition-spec') else '') + ('effect: ' + c.get('effect') + '; ' if c.get('effect') else '') + (c.get('source-ref') or '') + ('; guard: ' + c.get('guard-expression') if c.get('guard-expression') else ''), c.get('test-ref')]
            lines.append('| ' + ' | '.join((v or '').replace('\n', '<br>').replace('|', '\\|') for v in row) + ' |')
        lines.append('')
    lines += ['## Review UML theo hai hướng dẫn', '',
        'Đối chiếu [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/about-state-diagrams/) về trạng thái đối tượng, sự kiện và guard; đối chiếu [draw.io](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/) về shape, initial/final/choice và nhãn transition.', '',
        'Đã sửa: Yes/No trần thành guard alias [Yes]/[No] có predicate; điều kiện Run được lưu trong metadata và bảng transition; input confirm/overturn tới trước choice; field reason/result giữ ở context/metadata/thuyết minh, giữ tên state thuần và không thêm ô context lên ảnh compact. Initial không có incoming và chỉ một outgoing không guard/trigger; final không có outgoing. Câu hỏi trong hình thoi và trái/phải là profile người dùng; Research Engines dùng bảy transition invalidation riêng, không phải hạn chế chung của UML.', '',
        '| Tab / choice | [Yes] tương ứng | [No] tương ứng |', '|---|---|---|']
    for page in mx.findall('diagram'):
        cells = {c.get('id'): c for c in page.findall('.//mxCell')}
        for choice in cells.values():
            if 'rhombus' not in choice.get('style',''): continue
            branches = {e.get('branch-answer'): e.get('guard-expression') for e in cells.values() if e.get('source') == choice.get('id')}
            row = [page.get('name') + ' / ' + choice.get('value'), branches['Yes'], branches['No']]
            lines.append('| ' + ' | '.join(v.replace('\n','<br>').replace('|','\\|') for v in row) + ' |')
    lines += ['', 'Các hướng dẫn là nguồn ký pháp, không xác nhận nghiệp vụ project. Notifications/Monitoring và các transition đề xuất vẫn có giới hạn nguồn như từng mục; validator XML không phải chứng nhận formal UML hoặc runtime test.', '', '## Validation', '', 'Tái tạo bằng `python diagrams/09-state-machine/build_state_diagrams.py`; export từng tab scale 2, border 20, nền trắng. Kết quả kiểm tra thực tế ghi trong changelog; không suy ra runtime, in A4 hoặc chèn Word từ validator XML.', '']
    (OUT / 'State-Machine-Diagrams-design.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    build()

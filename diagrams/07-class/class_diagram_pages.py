"""Proposed FE-group class views, based on Report7 III/IV (not code extraction)."""

from html import escape, unescape
from math import ceil
import re
import textwrap
import xml.etree.ElementTree as E

BASE = 'html=1;fontFamily=Arial;fontSize=17;fontColor=#000000;strokeColor=#000000;strokeWidth=1;fillColor=#FFFFFF;'


def fit_class_widths(mx):
    """Fit displayed content in Arial while preserving class centres and routes."""
    from PIL import ImageFont

    body = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 17)
    heading = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 19)
    for diagram in mx.findall('diagram'):
        root = diagram.find('mxGraphModel/root')
        cells = {c.get('id'): c for c in root.findall('mxCell')}
        bounds = {}
        for name, cell in cells.items():
            if cell.get('vertex') != '1' or cell.get('parent') != '1':
                continue
            geometry = cell.find('mxGeometry')
            x, y, w, h = (float(geometry.get(k, '0')) for k in ['x','y','width','height'])
            title = [unescape(re.sub('<[^>]+>', '', line)) for line in cell.get('value').split('<br>')]
            members = [unescape(line) for child in cells.values() if child.get('parent') == name
                       for line in child.get('value', '').split('<br>')]
            width = max(190, ceil(max([heading.getlength(t)+48 for t in title]
                                     + [body.getlength(t)+32 for t in members])/10)*10)
            left = x+(w-width)/2
            bounds[name] = (x, y, w, h, left, width)
            geometry.set('x', str(left))
            geometry.set('width', str(width))
            for child in cells.values():
                if child.get('parent') == name:
                    child.find('mxGeometry').set('width', str(width))
        for cell in cells.values():
            if cell.get('edge') != '1':
                continue
            style = cell.get('style')
            props = dict(v.split('=',1) for v in style.split(';') if '=' in v)
            geometry = cell.find('mxGeometry')
            waypoints = geometry.findall('Array/mxPoint')
            ends = []
            for endpoint, prefix in [('source','exit'),('target','entry')]:
                x, y, w, h, left, width = bounds[cell.get(endpoint)]
                px, py = float(props[prefix+'X']), float(props[prefix+'Y'])
                if py in (0,1) and 0 < px < 1:
                    old_x = x+w*px
                    new_x = min(max(old_x,left+18),left+width-18)
                    px = (new_x-left)/width
                    style = re.sub(rf'{prefix}X=[^;]*;',f'{prefix}X={px};',style)
                    if waypoints:
                        point = waypoints[0 if endpoint == 'source' else -1]
                        if abs(float(point.get('x'))-old_x) < .01:
                            point.set('x', str(new_x))
                ends.append((left+width*px,y+h*py))
            cell.set('style',style)
            path = [ends[0], *[(float(p.get('x')),float(p.get('y'))) for p in waypoints], ends[1]]
            if 'labelWidth=' in style and cell.get('source').endswith('Controller') and waypoints:
                lengths = [abs(b[0]-a[0])+abs(b[1]-a[1]) for a,b in zip(path,path[1:])]
                geometry.set('x',str(1-lengths[-1]/sum(lengths)))


def space_endpoint_labels(mx):
    """Keep multiplicities a fixed distance from the box, independent of edge length."""
    for diagram in mx.findall('diagram'):
        root = diagram.find('mxGraphModel/root')
        cells = {cell.get('id'): cell for cell in root.findall('mxCell')}
        for edge in cells.values():
            if edge.get('edge') != '1':
                continue
            style = dict(item.split('=',1) for item in edge.get('style').split(';') if '=' in item)
            path = []
            for endpoint, prefix in [('source','exit'),('target','entry')]:
                geometry = cells[edge.get(endpoint)].find('mxGeometry')
                x, y, w, h = (float(geometry.get(k,'0')) for k in ['x','y','width','height'])
                port = (float(style.get(prefix+'X',.5)),float(style.get(prefix+'Y',.5)))
                point = (x+w*port[0],y+h*port[1])
                if endpoint == 'source':
                    path.append(point)
                    path.extend((float(p.get('x')),float(p.get('y'))) for p in edge.findall('mxGeometry/Array/mxPoint'))
                else:
                    path.append(point)
            path = [p for i,p in enumerate(path) if i==0 or p != path[i-1]]
            total = sum(abs(b[0]-a[0])+abs(b[1]-a[1]) for a,b in zip(path,path[1:]))
            if all(abs(p[0]-path[0][0]) < .01 for p in path) and cells.get(edge.get('id')+'-source') is not None:
                # Put the association name on the right; multiplicities stay close on the left.
                offset = edge.find("mxGeometry/mxPoint[@as='offset']")
                offset.set('x',str(len(edge.get('value',''))*4.5+14))
                offset.set('y','0')
            for suffix, first, last in [('source',path[0],path[1]),('target',path[-2],path[-1])]:
                label = cells.get(edge.get('id')+'-'+suffix)
                if label is None:
                    continue
                geometry = label.find('mxGeometry')
                geometry.set('x',str(-1+40/total if suffix=='source' else 1-40/total))
                geometry.set('y','0')
                for child in list(geometry):
                    geometry.remove(child)
                horizontal = abs(first[1]-last[1]) < .01
                E.SubElement(geometry,'mxPoint',x='0' if horizontal else '-20',
                             y='10' if horizontal else '0',attrib={'as':'offset'})


class Page:
    def __init__(self, mx, slug, name):
        self.diagram = E.SubElement(mx, 'diagram', id=slug, name=name)
        model = E.SubElement(self.diagram, 'mxGraphModel', grid='1', gridSize='10', page='1', pageWidth='3000', pageHeight='2150', background='#FFFFFF')
        self.root = E.SubElement(model, 'root')
        E.SubElement(self.root, 'mxCell', id='0')
        E.SubElement(self.root, 'mxCell', id='1', parent='0')
        self.boxes = {}
        self.edges = 0
        self.fanout = {}

    def vertex(self, id, value, x, y, w, h, style, parent='1'):
        c = E.SubElement(self.root, 'mxCell', id=id, value=value, style=BASE+style, vertex='1', parent=parent)
        E.SubElement(c, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), attrib={'as': 'geometry'})

    def node(self, name, role, col, row, attrs=(), methods=(), literals=()):
        x, y, w = 60 + col*760, 100 + row*520, 520
        def lines(items):
            return [part for item in items for part in textwrap.wrap(item, width=58, subsequent_indent='    ', break_long_words=False, break_on_hyphens=False)]
        al, ml = lines(literals or attrs), lines(methods)
        ah, mh = max(24, len(al)*26+16), len(ml)*28+16 if ml else 0
        h = 56+ah+mh
        self.boxes[name] = (x, y, w, h, col, row)
        self.vertex(name, f'«{role}»<br><b>{escape(name)}</b>', x, y, w, h,
                    'swimlane;startSize=56;horizontal=1;collapsible=0;container=1;align=center;fontSize=19;')
        self.vertex(name+'-attributes', '<br>'.join(escape(s) for s in al), 0, 56, w, ah,
                    'text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;', name)
        if ml:
            self.vertex(name+'-operations', '<br>'.join(escape(s) for s in ml), 0, 56+ah, w, mh,
                        'rounded=0;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;', name)

    def link(self, source, target, label, mult=None, route=None):
        sx, sy, sw, sh, sc, sr = self.boxes[source]
        tx, ty, tw, th, tc, tr = self.boxes[target]
        self.edges += 1
        key = f'edge-{self.edges}'
        points = []
        label_x = 0
        if route:
            ports, points = route
        elif sr == tr:
            ports = (1, 28/sh, 0, 28/th) if sc < tc else (0, 28/sh, 1, 28/th)
        elif sc == tc:
            ports = (.5, 1, .5, 0) if sr < tr else (.5, 0, .5, 1)
        else:
            # Controller fan-out: nested corridors, with low branches nearest the source.
            n = self.fanout.get(source, 0)
            self.fanout[source] = n+1
            source_y = sy+110+n*50
            corridor = sx+sw+180-n*35
            ports = (1, (source_y-sy)/sh, 0, 28/th)
            points = [(corridor, source_y), (corridor, ty+28)]
            label_x = -80
        ex, ey, ix, iy = ports
        style = BASE+'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;strokeWidth=1.5;endSize=16;labelBackgroundColor=#FFFFFF;spacing=5;'
        style += 'endArrow=none;' if mult else 'dashed=1;endArrow=open;endFill=0;'
        style += f'exitX={ex};exitY={ey};entryX={ix};entryY={iy};exitPerimeter=0;entryPerimeter=0;'
        cell = E.SubElement(self.root, 'mxCell', id=key, value=label, style=style, edge='1', parent='1', source=source, target=target)
        g = E.SubElement(cell, 'mxGeometry', relative='1', attrib={'as': 'geometry'})
        if points:
            a = E.SubElement(g, 'Array', attrib={'as': 'points'})
            for x,y in points:
                E.SubElement(a, 'mxPoint', x=str(x), y=str(y))
        E.SubElement(g, 'mxPoint', x=str(label_x), y='-15', attrib={'as': 'offset'})
        if mult:
            for suffix, value, pos in [('source', mult[0], -.88), ('target', mult[1], .88)]:
                c = E.SubElement(self.root, 'mxCell', id=key+'-'+suffix, value=value, style='edgeLabel;html=1;fontFamily=Arial;fontSize=17;labelBackgroundColor=#FFFFFF;', vertex='1', connectable='0', parent=key)
                E.SubElement(c, 'mxGeometry', x=str(pos), y='-18', relative='1', attrib={'as': 'geometry'})

    def compact_left_to_right(self):
        """Keep the reading direction while shortening the controller fan-out."""
        if self.diagram.get('id') == 'research-engines':
            self.group_research_engines()
            return
        cells = {c.get('id'): c for c in self.root.findall('mxCell')}
        hub = next(name for name in self.boxes if name.endswith('Controller'))
        layouts = {
            'project-workspace': {
                'ProjectController': (60,472), 'ProjectService': (880,48),
                'Project': (1620,80), 'ProjectSettings': (2320,144),
                'MembershipService': (880,392), 'Membership': (1620,408), 'User': (2320,472),
                'InvitationService': (1000,744), 'Invitation': (1740,776),
                'DocumentService': (860,1096), 'Document': (1580,1128), 'AuditLogEntry': (60,976),
            },
            'data-management': {
                'DataController': (60,464), 'DataService': (880,48), 'Dataset': (1640,80),
                'DataConnection': (2340,80), 'DataLocation': (2340,336),
                'DatasetVersionService': (880,408), 'DatasetVersion': (1640,408),
                'LocalNodeService': (1020,760), 'LocalNode': (1760,792), 'ReleaseLog': (2460,856),
                'ReleaseGate': (860,1096), 'Release': (1600,1144),
            },
            'research-run-orchestration': {
                'RunController': (60,456), 'ResearchCase': (60,48),
                'RunOrchestrator': (880,48), 'Run': (1640,80), 'RunState': (2340,144),
                'BudgetService': (880,408), 'StageRun': (1640,432), 'BudgetLedger': (880,680),
                'DossierService': (880,968), 'Dossier': (1640,968), 'Approval': (2340,1032),
                'HandOffObject': (1640,1272), 'Export': (2340,1304),
            },
            'ai-principal-investigator': {
                'DecisionController': (60,472), 'DecisionService': (880,48),
                'DecisionInboxItem': (1640,80), 'DecisionLogEntry': (2340,112),
                'ActionPolicyService': (880,416), 'ActionPolicy': (1640,440),
                'ActionLevel': (2340,528), 'AIPrincipalInvestigator': (1020,792),
                'LabNotebookEntry': (1760,824), 'Presence': (2460,920),
                'OverturnMetricService': (860,1168), 'Run': (1600,1168),
            },
            'notifications-integrations': {
                'CollaborationController': (60,480), 'NotificationService': (880,48),
                'Notification': (1640,80), 'DecisionInboxItem': (2340,128),
                'IntegrationService': (880,456), 'ProjectIntegration': (1640,440),
                'NotificationChannel': (880,720), 'CommentService': (1040,992),
                'Comment': (1780,1024), 'Membership': (2480,1088),
                'NotificationPreferenceService': (860,1328), 'NotificationPreference': (1620,1360),
            },
            'administration-monitoring': {
                'AdministrationController': (60,520), 'User': (60,48),
                'AdministrationService': (880,48), 'ModelProfile': (1640,80),
                'EngineSettings': (1640,368), 'SecretService': (880,648), 'SealedSecret': (1640,680),
                'MonitoringService': (880,1000), 'AuditLogEntry': (1640,1024),
                'HealthSnapshot': (2340,904), 'OperatingMetrics': (2340,1208),
            },
        }
        for name, (_, _, w, h, col, row) in self.boxes.items():
            x, y = layouts[self.diagram.get('id')][name]
            self.boxes[name] = (x,y,w,h,col,row)
            geometry = cells[name].find('mxGeometry')
            geometry.set('x',str(x))
            geometry.set('y',str(y))
        branches = sorted([c for c in self.root.findall('mxCell')
                           if c.get('edge') == '1' and c.get('source') == hub
                           and self.boxes[c.get('target')][0] != self.boxes[hub][0]],
                          key=lambda c:self.boxes[c.get('target')][1])
        ranks = {c.get('id'): i for i,c in enumerate(branches)}
        for cell in self.root.findall('mxCell'):
            if cell.get('edge') != '1':
                continue
            source, target = cell.get('source'), cell.get('target')
            sx,sy,sw,sh,_,_ = self.boxes[source]
            tx,ty,tw,th,_,_ = self.boxes[target]
            points = []
            if cell.get('id') in ranks:
                rank = ranks[cell.get('id')]
                fraction = ([.15,.35,.65,.85] if len(branches)==4 else [.2,.5,.8])[rank]
                source_y = sy+sh*fraction
                # Short upper/lower branches use separate parts of two corridors.
                corridor = 700 if abs(ty-source_y)<350 else 650
                ports = (1,fraction,0,28/th)
                points = [(corridor,source_y),(corridor,ty+28)]
            elif sx == tx:
                ports = (.5,1,.5,0) if sy < ty else (.5,0,.5,1)
            elif source == 'Dataset' and target == 'DataLocation':
                ports = (.8,1,.5,0)
                points = [(sx+sw*.8,sy+sh+50),(tx+tw*.5,sy+sh+50)]
            elif source == 'AdministrationService' and target == 'EngineSettings':
                ports = (1,.8,0,.5)
                points = [(1500,sy+sh*.8),(1500,ty+th*.5)]
            elif source == 'MonitoringService' and target == 'HealthSnapshot':
                ports = (.75,0,0,.5)
                points = [(sx+sw*.75,ty+th*.5)]
            elif source == 'MonitoringService' and target == 'OperatingMetrics':
                ports = (.5,1,0,.5)
                points = [(sx+sw*.5,ty+th*.5)]
            elif max(sy,ty)+28 < min(sy+sh,ty+th):
                line_y = max(sy,ty)+28
                ports = (1,(line_y-sy)/sh,0,(line_y-ty)/th) if sx < tx else (0,(line_y-sy)/sh,1,(line_y-ty)/th)
            else:
                ports = (1,.8,0,28/th)
                corridor = (sx+sw+tx)/2
                points = [(corridor,sy+sh*.8),(corridor,ty+28)]
            ex,ey,ix,iy = ports
            style = cell.get('style')
            for prop,value in [('exitX',ex),('exitY',ey),('entryX',ix),('entryY',iy)]:
                style = re.sub(rf'{prop}=[^;]*;',f'{prop}={value};',style)
            if cell.get('id') in ranks:
                style += 'labelWidth=130;whiteSpace=wrap;'
            cell.set('style',style)
            geometry = cell.find('mxGeometry')
            for child in list(geometry):
                geometry.remove(child)
            if points:
                arr=E.SubElement(geometry,'Array',attrib={'as':'points'})
                for x,y in points:
                    E.SubElement(arr,'mxPoint',x=str(x),y=str(y))
            vertical = ex == ix and sx == tx and not points
            wrap_label = not vertical and len(cell.get('value','')) > 18
            if wrap_label:
                cell.set('style',cell.get('style')+'labelWidth=140;whiteSpace=wrap;')
            label_y = -25 if wrap_label else -15
            label_dx = len(cell.get('value',''))*4.5+14 if vertical else 0
            if vertical:
                label_y = 0
            if cell.get('id') in ranks:
                path = [(sx+sw*ex,sy+sh*ey), *points, (tx+tw*ix,ty+th*iy)]
                lengths = [abs(b[0]-a[0])+abs(b[1]-a[1]) for a,b in zip(path,path[1:])]
                total = sum(lengths)
                # Anchor on the final horizontal segment, clear of both vertical lanes.
                geometry.set('x',str(1-lengths[-1]/total))
                geometry.set('y','0')
                label_y = -28
                label_dx = 0
            E.SubElement(geometry,'mxPoint',x=str(label_dx),y=str(label_y),attrib={'as':'offset'})
        self.diagram.find('mxGraphModel').set('pageWidth',str(max(b[0]+b[2] for b in self.boxes.values())+80))
        self.diagram.find('mxGraphModel').set('pageHeight',str(max(b[1]+b[3] for b in self.boxes.values())+80))

    def group_research_engines(self):
        """Place related objects around their users rather than repeating a grid."""
        positions = {
            'DatasetEngine': (60, 60), 'DatasetSnapshot': (740, 100),
            'HypothesisEngine': (1420, 60), 'HypothesisSet': (1420, 370),
            'ExperimentDesignEngine': (60, 650), 'AnalysisPlan': (740, 650),
            'ExecutionEngine': (1420, 730), 'EvidenceBundle': (2100, 730),
            'PaperEngine': (60, 1080), 'PaperPack': (740, 1120),
            'IndependentReviewService': (1420, 1160), 'Finding': (2100, 1220),
            'Harness': (300, 1500), 'Lock': (1040, 1530), 'Envelope': (1780, 1570),
        }
        cells = {c.get('id'): c for c in self.root.findall('mxCell')}
        for name, (x, y) in positions.items():
            _, _, w, h, col, row = self.boxes[name]
            self.boxes[name] = (x, y, w, h, col, row)
            geometry = cells[name].find('mxGeometry')
            geometry.set('x', str(x))
            geometry.set('y', str(y))
        for cell in cells.values():
            if cell.get('edge') != '1':
                continue
            sx, sy, sw, sh, _, _ = self.boxes[cell.get('source')]
            tx, ty, tw, th, _, _ = self.boxes[cell.get('target')]
            # A shared horizontal level keeps close neighbours connected directly.
            if abs(sy-ty) < min(sh, th)-35 and sx != tx:
                line_y = max(sy, ty)+28
                ports = (1, (line_y-sy)/sh, 0, (line_y-ty)/th) if sx < tx else (0, (line_y-sy)/sh, 1, (line_y-ty)/th)
            else:
                # Vertical relations use the overlapping footprint of their boxes.
                line_x = (max(sx, tx)+min(sx+sw, tx+tw))/2
                ports = ((line_x-sx)/sw, 1, (line_x-tx)/tw, 0)
            style = cell.get('style')
            for prop, value in zip(['exitX','exitY','entryX','entryY'], ports):
                style = re.sub(rf'{prop}=[^;]*;', f'{prop}={value};', style)
            vertical = ports[1] == 1 and ports[3] == 0
            wrap_label = not vertical and len(cell.get('value')) > 18
            if wrap_label:
                style += 'labelWidth=140;whiteSpace=wrap;'
            cell.set('style', style)
            geometry = cell.find('mxGeometry')
            for child in list(geometry):
                geometry.remove(child)
            E.SubElement(geometry, 'mxPoint', x=str(len(cell.get('value'))*4.5+14) if vertical else '0',
                         y='0' if vertical else '-25' if wrap_label else '-15', attrib={'as':'offset'})
        model = self.diagram.find('mxGraphModel')
        model.set('pageWidth', '2700')
        model.set('pageHeight', '1900')


def add_feature_pages(mx):
    pages = []
    p = Page(mx, 'project-workspace', 'Project Workspace')
    pages.append(p)
    p.node('ProjectController', 'controller', 0, 0, methods=[
        '+ create(input : ProjectInput) : Project', '+ update(projectId : UUID, input : ProjectInput) : void',
        '+ archive(projectId : UUID) : void', '+ manageMembers(projectId : UUID) : void',
        '+ manageInvitations(projectId : UUID) : void', '+ manageDocuments(projectId : UUID) : void',
        '+ configure(projectId : UUID, settings : ProjectSettings) : void'])
    p.node('ProjectService', 'service', 1, 0, methods=[
        '+ create(input : ProjectInput) : Project', '+ update(projectId : UUID, input : ProjectInput) : void',
        '+ archive(projectId : UUID) : void', '+ configure(settings : ProjectSettings) : void',
        '+ recordChange(action : String) : void'])
    p.node('Project', 'entity', 2, 0, attrs=['- id : UUID', '- name : String', '- status : String'])
    p.node('ProjectSettings', 'entity', 3, 0, attrs=['- monthlyBudget : Decimal', '- defaultPresetPerStage : Map',
        '- reviewSettings : ReviewSettings', '- notificationChoices : Map', '- pinnedWaitDeadline : Duration'])
    p.node('MembershipService', 'service', 1, 1, methods=['+ changeRole(memberId : UUID, role : ProjectRole) : void',
        '+ remove(memberId : UUID) : void', '+ transferOwnership(projectId : UUID, userId : UUID) : void',
        '- requireActiveManager(projectId : UUID) : void'])
    p.node('Membership', 'entity', 2, 1, attrs=['- projectId : UUID', '- role : ProjectRole', '- dateAdded : DateTime'])
    p.node('User', 'entity', 3, 1, attrs=['- id : UUID', '- email : String'])
    p.node('InvitationService', 'service', 1, 2, methods=['+ invite(projectId : UUID, email : String) : Invitation',
        '+ accept(invitationId : UUID) : Membership', '+ decline(invitationId : UUID) : void',
        '+ resend(invitationId : UUID) : void', '+ cancel(invitationId : UUID) : void', '- rejectExpired(invitation : Invitation) : void'])
    p.node('Invitation', 'entity', 2, 2, attrs=['- id : UUID', '- projectId : UUID', '- email : String',
        '- role : ProjectRole', '- expiresAt : DateTime', '- status : String'])
    p.node('DocumentService', 'service', 1, 3, methods=['+ add(projectId : UUID, input : DocumentInput) : Document',
        '+ update(documentId : UUID, input : DocumentInput) : void', '+ list(projectId : UUID) : Document [0..*]'])
    p.node('Document', 'entity', 2, 3, attrs=['- id : UUID', '- projectId : UUID', '- name : String', '- version : Integer'])
    p.node('AuditLogEntry', 'entity', 0, 3, attrs=['- action : String', '- actorId : UUID', '- projectId : UUID [0..1]', '- time : DateTime'])
    for service, label in [('ProjectService','uses'), ('MembershipService','manages members'), ('InvitationService','manages invitations'), ('DocumentService','manages documents')]:
        p.link('ProjectController', service, label)
    for service, entity, label in [('ProjectService','Project','manages'), ('MembershipService','Membership','maintains'),
        ('InvitationService','Invitation','issues / resolves'), ('DocumentService','Document','versions')]:
        p.link(service, entity, label)
    p.link('Project','ProjectSettings','settings', ('1','1'))
    p.link('Membership','User','member', ('0..*','1'))
    p.link('Project','Membership','memberships', ('1','0..*'))
    p.link('ProjectController','AuditLogEntry','reads project activity')

    p = Page(mx, 'data-management', 'Data Management')
    pages.append(p)
    p.node('DataController','controller',0,0,methods=['+ upload(input : UploadInput) : DatasetVersion',
        '+ importData(connectionId : UUID) : DatasetVersion', '+ preview(versionId : UUID) : TablePreview',
        '+ pairNode(code : String) : LocalNode', '+ runLocal(job : LocalJob) : Release'])
    p.node('DataService','service',1,0,methods=['+ createDataset(input : DatasetInput) : Dataset',
        '+ importData(connection : DataConnection) : DatasetVersion', '- requireAuthorizedSource(uri : String) : void',
        '- blockInternalHosts(uri : String) : void', '- rejectLocalPreview(dataset : Dataset) : void'])
    p.node('Dataset','entity',2,0,attrs=['- id : UUID','- projectId : UUID','- name : String','- location : DataLocation'])
    p.node('DataConnection','entity',3,0,attrs=['- id : UUID','- provider : String','- authorizationScope : String','- credentialRef : SecretRef'])
    p.node('DatasetVersionService','service',1,1,methods=['+ create(datasetId : UUID, source : String) : DatasetVersion',
        '+ verifyHash(version : DatasetVersion) : Boolean', '- preventOverwrite(versionId : UUID) : void'])
    p.node('DatasetVersion','entity',2,1,attrs=['- id : UUID','- contentHash : String','- source : String','- createdAt : DateTime'])
    p.node('DataLocation','enumeration',3,1,literals=['platform','local'])
    p.node('LocalNodeService','service',1,2,methods=['+ pair(projectId : UUID, code : String) : LocalNode',
        '+ route(job : LocalJob) : void','+ revoke(nodeId : UUID) : void','- rejectUnavailableNode(nodeId : UUID) : void'])
    p.node('LocalNode','entity',2,2,attrs=['- id : UUID','- projectId : UUID','- status : String','- isolationManifest : String'])
    p.node('ReleaseLog','entity',3,2,attrs=['- datasetVersionId : UUID','- appendOnly : Boolean'])
    p.node('ReleaseGate','service',1,3,methods=['+ check(job : LocalJob, result : Aggregate) : Release',
        '- applyFirewall(result : Aggregate) : void','- round(result : Aggregate) : Aggregate',
        '- checkDisclosure(result : Aggregate) : void','- checkDifferencing(result : Aggregate) : void','- checkProbeBudget(versionId : UUID) : void'])
    p.node('Release','entity',2,3,attrs=['- id : UUID','- jobId : UUID','- kind : String','- reason : String','- time : DateTime'])
    for service, label in [('DataService','uses'),('DatasetVersionService','versions data'),('LocalNodeService','routes local work'),('ReleaseGate','checks aggregates')]:
        p.link('DataController',service,label)
    p.link('DataService','Dataset','manages')
    p.link('Dataset','DataConnection','imports from',('0..*','0..1'))
    p.link('Dataset','DatasetVersion','versions',('1','0..*'))
    p.link('DatasetVersionService','DatasetVersion','creates / verifies')
    p.link('Dataset','DataLocation','uses location type', route=((.8,1,.5,0),[(1996,540),(2600,540)]))
    p.link('LocalNodeService','LocalNode','pairs / revokes')
    p.link('LocalNode','ReleaseLog','appends locally')
    p.link('ReleaseGate','Release','approves release')

    p = Page(mx,'research-run-orchestration','Research Run Orchestration')
    pages.append(p)
    p.node('RunController','controller',0,0,methods=['+ start(caseId : UUID) : Run','+ amendCase(input : Amendment) : ResearchCase',
        '+ cancel(runId : UUID) : void','+ acceptObject(objectId : UUID) : void','+ reviewSpending(itemId : UUID, approve : Boolean) : void',
        '+ approveDossier(dossierId : UUID) : Approval','+ export(dossierId : UUID, format : String) : Export'])
    p.node('RunOrchestrator','service',1,0,methods=['+ start(caseId : UUID) : Run','+ advance(runId : UUID) : StageRun',
        '+ cancel(runId : UUID) : void','+ markDownstreamStale(objectId : UUID) : void',
        '- requireNoActiveRun(projectId : UUID) : void'])
    p.node('Run','entity',2,0,attrs=['- id : UUID','- state : RunState','- waitingReason : String [0..1]',
        '- endingOutcome : String [0..1]','- tokenBudget : Integer','- researchCaseRef : VersionRef','- pipeline : String = dataset_first'])
    p.node('ResearchCase','entity',0,1,attrs=['- id : UUID','- projectId : UUID','- version : Integer','- objective : String',
        '- constraints : String','- datasetVersionId : UUID [0..1]'])
    p.node('BudgetService','service',1,1,methods=['+ recordUsage(runId : UUID, amount : Decimal) : void',
        '+ checkLimits(runId : UUID) : void','+ approveSpending(itemId : UUID) : void',
        '+ expireSpending(itemId : UUID) : void','- endWithGaps(runId : UUID) : void'])
    p.node('StageRun','entity',2,1,attrs=['- id : UUID','- stage : String','- preset : String', '- presenceAtStart : String','- contractStatus : String'])
    p.node('BudgetLedger','entity',3,1,attrs=['- projectId : UUID','- month : String','- spending : Decimal','- notifiedThresholds : Decimal [0..*]'])
    p.node('DossierService','service',1,2,methods=['+ createFromAccepted(packId : UUID) : Dossier',
        '+ approve(dossierId : UUID) : Approval','+ exportApproved(dossierId : UUID, format : String) : Export',
        '- verifyReferenceHashes(dossierId : UUID) : void','- requirePinnedExportApproval(dossierId : UUID) : void'])
    p.node('Dossier','entity',2,2,attrs=['- id : UUID','- version : Integer','- evidenceBundleRef : VersionRef',
        '- paperPackRef : VersionRef','- approvalState : String'])
    p.node('Approval','entity',3,2,attrs=['- membershipId : UUID','- dossierVersion : Integer','- decision : String','- time : DateTime'])
    p.node('RunState','enumeration',3,0,literals=['running','waiting','ended'])
    p.node('HandOffObject','entity',2,3,attrs=['- id : UUID','- version : Integer','- contentHash : String',
        '- state : String','- upstreamRefs : VersionRef [0..*]'])
    p.node('Export','entity',3,3,attrs=['- dossierVersion : Integer','- format : String','- approvedActionRef : UUID','- auditEntryRef : UUID'])
    p.link('RunController','RunOrchestrator','uses')
    p.link('RunController','BudgetService','reviews spending')
    p.link('RunController','DossierService','approves / exports')
    p.link('RunOrchestrator','Run','orchestrates')
    p.link('Run','RunState','uses state type')
    p.link('RunController','ResearchCase','amends case version')
    p.link('Run','StageRun','stages',('1','0..*'))
    p.link('BudgetService','StageRun','checks stage share')
    p.link('BudgetService','BudgetLedger','records usage',route=((.5,1,.5,1),[(1080,1000),(2600,1000)]))
    p.link('DossierService','Dossier','versions / checks')
    p.link('Dossier','Approval','approvals',('1','0..*'))
    p.link('Dossier','HandOffObject','references accepted versions')
    p.link('Export','HandOffObject','reads accepted references')

    p = Page(mx,'research-engines','Research Engines')
    pages.append(p)
    p.node('DatasetEngine','service',0,0,methods=['+ profile(versionId : UUID) : DatasetSnapshot',
        '+ assessFitness(snapshot : DatasetSnapshot) : Fitness','+ splitAfterConfirmation(input : SplitInput) : void'])
    p.node('DatasetSnapshot','entity',1,0,attrs=['- versionRef : VersionRef','- qualityProfile : QualityProfile',
        '- dictionary : Dictionary','- split : SplitSpec','- fitness : Fitness'])
    p.node('HypothesisEngine','service',2,0,methods=['+ updateLiterature(projectId : UUID) : LiteratureBase',
        '+ propose(snapshot : DatasetSnapshot) : HypothesisSet','+ selectPrimary(input : Selection) : void'])
    p.node('HypothesisSet','entity',3,0,attrs=['- snapshotRef : VersionRef','- literatureVersionRef : VersionRef',
        '- hypotheses : Hypothesis [2..*]','- primaryClaimKey : String'])
    p.node('ExperimentDesignEngine','service',0,1,methods=['+ build(set : HypothesisSet) : AnalysisPlan',
        '+ rehearseOnTwin(plan : AnalysisPlan) : CheckResult','+ requestUserLock(planId : UUID) : void'])
    p.node('AnalysisPlan','entity',1,1,attrs=['- hypothesisSetRef : VersionRef','- patternRefs : VersionRef [0..*]',
        '- taskFamily : String','- pipelineOrder : String [1..*]','- interpretationTable : Table'])
    p.node('ExecutionEngine','service',2,1,methods=['+ execute(lock : Lock) : EvidenceBundle','+ dryRun(lock : Lock) : Diagnostics',
        '+ requestUnseal(lockId : UUID) : void','+ computeVerdicts(input : EvidenceInput) : Verdict [1..*]'])
    p.node('EvidenceBundle','entity',3,1,attrs=['- analysisPlanRef : VersionRef','- verdicts : Verdict [1..*]',
        '- grade : String','- claimCeiling : String','- replicationHash : String'])
    p.node('PaperEngine','service',0,2,methods=['+ draft(input : PaperInput) : PaperPack',
        '+ renderNumbers(bundle : EvidenceBundle) : void','+ validateClaimsAndCitations(pack : PaperPack) : CheckResult'])
    p.node('PaperPack','entity',1,2,attrs=['- evidenceBundleRef : VersionRef','- manuscript : String',
        '- reportingChecklist : Checklist','- limitations : String [0..*]','- authorDeclarations : Declaration [0..*]'])
    p.node('IndependentReviewService','service',2,2,methods=['+ review(object : HandOffObject) : Finding [0..*]',
        '+ verify(finding : Finding) : String','+ reviseConfirmedBlockers(objectId : UUID) : void',
        '- enforceTwoRounds(round : Integer) : void'])
    p.node('Finding','entity',3,2,attrs=['- anchor : ObjectFieldRef','- evidence : EvidenceRef','- severity : String',
        '- verificationResult : String','- proposedFix : String'])
    p.node('Harness','service',0,3,methods=['+ checkContract(object : HandOffObject) : CheckResult',
        '+ enforcePipelineOrder(plan : AnalysisPlan) : void','+ checkItemBudget(itemId : UUID) : void',
        '+ renderNumbers(records : Record [0..*]) : String'])
    p.node('Lock','entity',1,3,attrs=['- analysisPlanRef : VersionRef','- specHash : String','- programHash : String',
        '- splitDigest : String','- lockedBy : UUID','- lockedAt : DateTime'])
    p.node('Envelope','entity',2,3,attrs=['- lockId : UUID','- state : String','- sealedResults : Result [0..*]', '- unsealedAt : DateTime [0..1]'])
    for a,b,label in [('DatasetEngine','DatasetSnapshot','publishes'),('HypothesisEngine','HypothesisSet','publishes'),
        ('ExperimentDesignEngine','AnalysisPlan','publishes'),('ExecutionEngine','EvidenceBundle','publishes'),
        ('PaperEngine','PaperPack','publishes'),('IndependentReviewService','Finding','verifies')]:
        p.link(a,b,label)
    p.link('HypothesisEngine','DatasetSnapshot','reads pinned snapshot')
    p.link('ExecutionEngine','AnalysisPlan','reads locked plan')
    p.link('IndependentReviewService','PaperPack','reviews object version')
    p.link('PaperEngine','Harness','runs checks')
    p.link('ExecutionEngine','IndependentReviewService','reviews evidence')
    p.link('Harness','Lock','checks locked plan')
    p.link('Lock','Envelope','sealed results',('1','1'))

    p = Page(mx,'ai-principal-investigator','AI Principal Investigator')
    pages.append(p)
    p.node('DecisionController','controller',0,0,methods=['+ answer(itemId : UUID, option : String) : void',
        '+ confirmTentative(itemId : UUID) : void','+ overturn(itemId : UUID, reason : String) : void',
        '+ changePolicy(input : PolicyInput) : void','+ setPresence(value : Presence) : void'])
    p.node('DecisionService','service',1,0,methods=['+ createRequest(input : DecisionInput) : DecisionInboxItem',
        '+ answer(itemId : UUID, option : String) : void','+ overturn(itemId : UUID, reason : String) : void',
        '+ expirePinnedItem(itemId : UUID) : void','- closeUnansweredAndEndWithGaps(itemId : UUID) : void'])
    p.node('DecisionInboxItem','entity',2,0,attrs=['- id : UUID','- kind : String','- options : String [1..*]',
        '- proposedOption : String','- status : String','- pinned : Boolean','- waitDeadline : DateTime [0..1]'])
    p.node('DecisionLogEntry','entity',3,0,attrs=['- actionType : String','- level : ActionLevel','- policyVersion : Integer',
        '- decidedBy : String','- presence : Presence','- overturned : Boolean'])
    p.node('ActionPolicyService','service',1,1,methods=['+ effectiveLevel(actionType : String) : ActionLevel',
        '+ updatePreset(stage : String, preset : String) : void','+ setOverride(actionType : String, level : ActionLevel) : void',
        '- enforceFloorAndCeiling(actionType : String) : void','- reevaluateWaitingItems() : void'])
    p.node('ActionPolicy','entity',2,1,attrs=['- version : Integer','- presetPerStage : Map','- overrides : Map',
        '- floors : Map','- spendingCeiling : Decimal'])
    p.node('ActionLevel','enumeration',3,1,literals=['auto','do_then_review','must_ask'])
    p.node('AIPrincipalInvestigator','service',1,2,methods=['+ propose(item : DecisionInboxItem) : String',
        '+ decideTentatively(item : DecisionInboxItem) : void','+ proposeNextStep(runId : UUID) : String',
        '- rejectPinnedDecision(item : DecisionInboxItem) : void'])
    p.node('LabNotebookEntry','entity',2,2,attrs=['- runId : UUID','- summary : String','- proposal : String [0..1]',
        '- tentativeDecisionRef : UUID [0..1]','- reason : String','- presence : Presence'])
    p.node('Presence','enumeration',3,2,literals=['present','away'])
    p.node('OverturnMetricService','service',1,3,methods=['+ compute(actionType : String) : Decimal',
        '+ proposeHigherLevel(actionType : String) : ActionLevel'])
    p.node('Run','entity',2,3,attrs=['- id : UUID','- state : RunState','- endingOutcome : String [0..1]'])
    for s,l in [('DecisionService','answers / overturns'),('ActionPolicyService','sets policy'),('AIPrincipalInvestigator','requests proposals'),('OverturnMetricService','reads measured outcomes')]:
        p.link('DecisionController',s,l)
    p.link('DecisionService','DecisionInboxItem','creates / resolves')
    p.link('DecisionInboxItem','DecisionLogEntry','decided record',('0..1','0..1'))
    p.link('ActionPolicyService','ActionPolicy','versions')
    p.link('ActionPolicy','ActionLevel','uses level type')
    p.link('AIPrincipalInvestigator','LabNotebookEntry','writes proposals')
    p.link('LabNotebookEntry','Presence','records context type')
    p.link('OverturnMetricService','Run','measures decisions by run')
    p.link('DecisionInboxItem','ActionPolicy','evaluated under')

    p = Page(mx,'notifications-integrations','Notifications & Integrations')
    pages.append(p)
    p.node('CollaborationController','controller',0,0,methods=['+ listNotifications() : Notification [0..*]',
        '+ markRead(notificationId : UUID) : void','+ setPreferences(input : PreferencesInput) : void',
        '+ configureIntegration(input : IntegrationInput) : void','+ comment(input : CommentInput) : Comment'])
    p.node('NotificationService','service',1,0,methods=['+ create(event : ProjectEvent) : Notification',
        '+ listForUser(userId : UUID) : Notification [0..*]','+ markRead(notificationId : UUID) : void',
        '- allowExternalNotice(item : DecisionInboxItem) : Boolean','- selectAuthorizedRecipients(item : DecisionInboxItem) : UUID [0..*]'])
    p.node('Notification','entity',2,0,attrs=['- id : UUID','- recipientId : UUID','- kind : String','- status : String','- decisionItemId : UUID [0..1]'])
    p.node('DecisionInboxItem','entity',3,0,attrs=['- id : UUID','- kind : String','- pinned : Boolean','- blocking : Boolean','- waitDeadline : DateTime [0..1]'])
    p.node('IntegrationService','service',1,1,methods=['+ configure(input : IntegrationInput) : ProjectIntegration',
        '+ deliver(notificationId : UUID, channel : String) : void','- resolveSealedCredential(ref : SecretRef) : void'])
    p.node('ProjectIntegration','entity',2,1,attrs=['- projectId : UUID','- provider : String','- credentialRef : SecretRef','- enabled : Boolean'])
    p.node('NotificationChannel','external',3,1,methods=['+ deliver(recipient : String, message : String) : void'])
    p.node('CommentService','service',1,2,methods=['+ add(input : CommentInput) : Comment',
        '+ list(objectRef : ObjectRef) : Comment [0..*]','- requireProjectRole(actorId : UUID) : void'])
    p.node('Comment','entity',2,2,attrs=['- id : UUID','- membershipId : UUID','- text : String','- anchor : ObjectFieldRef'])
    p.node('Membership','entity',3,2,attrs=['- projectId : UUID','- role : ProjectRole'])
    p.node('NotificationPreferenceService','service',1,3,methods=['+ update(input : PreferencesInput) : NotificationPreference',
        '+ resolveForProject(projectId : UUID) : NotificationPreference'])
    p.node('NotificationPreference','entity',2,3,attrs=['- projectId : UUID','- userId : UUID','- eventChoices : Map','- channels : String [0..*]'])
    for s,l in [('NotificationService','receives / reads'),('IntegrationService','configures channels'),('CommentService','comments on objects'),('NotificationPreferenceService','sets preferences')]:
        p.link('CollaborationController',s,l)
    p.link('NotificationService','Notification','creates / marks read')
    p.link('Notification','DecisionInboxItem','decision context',('0..*','0..1'))
    p.link('IntegrationService','ProjectIntegration','configures')
    p.link('IntegrationService','NotificationChannel','delivers through',route=((.5,0,.5,0),[(1080,560),(2600,560)]))
    p.link('CommentService','Comment','anchors comments')
    p.link('Comment','Membership','author',('0..*','1'))
    p.link('NotificationPreferenceService','NotificationPreference','updates')

    p = Page(mx,'administration-monitoring','Administration & Monitoring')
    pages.append(p)
    p.node('AdministrationController','controller',0,0,methods=['+ manageUsers(input : UserAdminInput) : void',
        '+ configureModel(input : ModelInput) : void','+ configureEngine(input : EngineInput) : void',
        '+ viewAudit(filter : AuditFilter) : AuditLogEntry [0..*]','+ viewHealth() : HealthSnapshot',
        '+ viewMetrics(runId : UUID) : OperatingMetrics'])
    p.node('AdministrationService','service',1,0,methods=['+ updateUser(input : UserAdminInput) : User',
        '+ configureModel(input : ModelInput) : ModelProfile','+ configureEngine(input : EngineInput) : EngineSettings',
        '+ setDefaultBudget(amount : Decimal) : void','- requirePlatformAdmin(userId : UUID) : void'])
    p.node('ModelProfile','entity',2,0,attrs=['- id : UUID','- modelRole : String','- model : String','- keyRef : SecretRef','- unitPrice : Decimal'])
    p.node('EngineSettings','entity',3,0,attrs=['- engineId : String','- enabled : Boolean','- configuration : Map'])
    p.node('SecretService','service',1,1,methods=['+ seal(value : String) : SecretRef','+ rotate(ref : SecretRef, value : String) : void',
        '+ resolveForExecution(ref : SecretRef) : Secret','- preventSecretDisclosure() : void'])
    p.node('SealedSecret','entity',2,1,attrs=['- id : UUID','- encryptedValue : Bytes','- keyVersion : String','- updatedAt : DateTime'])
    p.node('User','entity',0,1,attrs=['- id : UUID','- email : String','- status : String','- isPlatformAdmin : Boolean'])
    p.node('MonitoringService','service',1,2,methods=['+ readAudit(filter : AuditFilter) : AuditLogEntry [0..*]',
        '+ health() : HealthSnapshot','+ metrics(runId : UUID) : OperatingMetrics',
        '+ requireModelsAndCredentials(runId : UUID) : void'])
    p.node('AuditLogEntry','entity',2,2,attrs=['- action : String','- actorId : UUID','- projectId : UUID [0..1]','- time : DateTime'])
    p.node('HealthSnapshot','entity',3,2,attrs=['- collectedAt : DateTime','- componentStates : Map'])
    p.node('OperatingMetrics','entity',2,3,attrs=['- runId : UUID','- questionCount : Integer','- blockedTime : Duration',
        '- overturnRates : Map','- personaPrecision : Map'])
    for s,l in [('AdministrationService','configures platform'),('SecretService','manages sealed secrets'),('MonitoringService','reads operation')]:
        p.link('AdministrationController',s,l)
    p.link('AdministrationService','ModelProfile','configures model roles')
    p.link('AdministrationService','EngineSettings','configures engines',route=((.6,0,.5,0),[(1132,40),(2600,40)]))
    p.link('AdministrationController','User','manages user accounts')
    p.link('SecretService','SealedSecret','seals / rotates')
    p.link('MonitoringService','AuditLogEntry','reads append-only log')
    p.link('MonitoringService','HealthSnapshot','reads component health',route=((.5,0,.5,0),[(1080,1080),(2600,1080)]))
    p.link('MonitoringService','OperatingMetrics','computes run metrics')

    for page in pages:
        page.compact_left_to_right()

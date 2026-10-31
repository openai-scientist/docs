from pathlib import Path
import xml.etree.ElementTree as E
from html import escape
from class_diagram_pages import add_feature_pages, fit_class_widths, straighten_controller_fanout, top_down_project, top_down_remaining, top_down_engines, space_endpoint_labels, relation_style

OUT = Path(__file__).resolve().parent
NAME = 'Class-Diagram-Authentication-Account'
mx = E.Element('mxfile', host='drawio', version='26.0.0')
diagram = E.SubElement(mx, 'diagram', id='authentication-account', name='Authentication & Account')
model = E.SubElement(diagram, 'mxGraphModel', dx='2320', dy='1300', grid='1', gridSize='10', page='1', pageWidth='2320', pageHeight='1300', background='#FFFFFF')
root = E.SubElement(model, 'root')
E.SubElement(root, 'mxCell', id='0')
E.SubElement(root, 'mxCell', id='1', parent='0')
BASE = 'html=1;fontFamily=Arial;fontSize=17;fontColor=#000000;strokeColor=#000000;strokeWidth=1;fillColor=#FFFFFF;'
def vertex(id, value, x, y, w, h, style='', parent='1'):
    if parent == '1':
        x, y = x * 1.5, y * 0.85
    cell = E.SubElement(root, 'mxCell', id=id, value=value, style=BASE+style, vertex='1', parent=parent)
    E.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), attrib={'as':'geometry'})
    return cell

def cls(id, name, role, x, y, w, attrs=(), methods=(), literals=()):
    header = 56
    ah = max(24, len(attrs)*26+16) if not literals else len(literals)*26+16
    mh = len(methods)*28+16 if methods else 0
    h = header+ah+mh
    vertex(id, f'«{role}»<br><b>{escape(name)}</b>', x,y,w,h,
        'swimlane;startSize=56;horizontal=1;collapsible=0;container=1;align=center;fontSize=19;')
    content = literals or attrs
    vertex(id+'-attributes', '<br>'.join(escape(a) for a in content),0,header,w,ah,
        'text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;whiteSpace=wrap;',id)
    if methods:
        vertex(id+'-operations', '<br>'.join(escape(a) for a in methods),0,header+ah,w,mh,
            'rounded=0;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;whiteSpace=wrap;',id)

cls('controller','AuthenticationController','controller',50,120,420, methods=[
 '+ requestEmailCode(email : String) : void',
 '+ signInWithCode(input : EmailCode) : AuthSession',
 '+ signInWithGoogle(code : String) : AuthSession',
 '+ completeOnboarding(input : ProfileInput) : User',
 '+ updateProfile(input : ProfileInput) : User',
 '+ signOut(sessionId : UUID) : void'])
cls('auth','AuthenticationService','service',560,120,420,methods=[
 '+ requestCode(email : String) : void',
 '+ verifyCode(input : EmailCode) : AuthSession',
 '+ signInGoogle(code : String) : AuthSession',
 '+ validateSession(token : String) : User',
 '+ revokeSession(sessionId : UUID) : void',
 '- resolveUser(email : String) : User'])
cls('google','GoogleIdentityProvider','external',1080,120,400,methods=[
 '+ verifyIdentity(code : String) : Identity'])
cls('email','EmailDelivery','external',1080,390,400,methods=[
 '+ sendCode(email : String, code : String) : void'])
cls('account','AccountService','service',50,580,420,methods=[
 '+ completeOnboarding(input : ProfileInput) : User',
 '+ updateProfile(input : ProfileInput) : User'])
cls('user','User','entity',560,580,420,attrs=[
 '- id : UUID','- email : String','- displayName : String [0..1]',
 '- avatarUrl : String [0..1]','- isPlatformAdmin : Boolean'])
cls('challenge','EmailChallenge','entity',1080,680,400,attrs=[
 '- id : UUID','- email : String','- codeDigest : String',
 '- expiresAt : DateTime','- consumedAt : DateTime [0..1]'])
cls('access','AuthorizationService','service',50,980,420,methods=[
 '+ requireRole(user : User, projectId : UUID,',
 '    action : Action) : void',
 '+ canReadMetadata(user : User) : Boolean'])
cls('membership','Membership','entity',560,980,420,attrs=[
 '- projectId : UUID','- role : ProjectRole'])
cls('session','AuthSession','entity',1080,1080,400,attrs=[
 '- id : UUID','- expiresAt : DateTime','- revokedAt : DateTime [0..1]'])
cls('role','ProjectRole','enumeration',560,1280,420,literals=[
 'PROJECT_MANAGER','RESEARCHER','REVIEWER'])

def edge(id, source, target, label='', points=(), ports=(1,.5,0,.5), mult=None, *, kind):
    ex,ey,ix,iy=ports
    style = BASE+'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;endSize=16;strokeWidth=1.5;labelBackgroundColor=#FFFFFF;spacing=5;'
    style += relation_style(kind, mult)
    style+=f'exitX={ex};exitY={ey};entryX={ix};entryY={iy};entryPerimeter=0;exitPerimeter=0;'
    cell=E.SubElement(root,'mxCell',id=id,value=label,style=style,edge='1',parent='1',source=source,target=target)
    geo=E.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
    routed = points
    arr=E.SubElement(geo,'Array',attrib={'as':'points'})
    for x,y in routed:
        E.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    if label:
        if id in ('auth-email', 'auth-challenge'):
            geo.set('x', '-0.65')
        E.SubElement(geo, 'mxPoint', x='0', y='-15', attrib={'as':'offset'})
    if mult:
        for suffix, val, pos in [('source',mult[0],-.85),('target',mult[1],.85)]:
            child=E.SubElement(root,'mxCell',id=id+'-'+suffix,value=val,style='edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;labelBackgroundColor=#FFFFFF;fontFamily=Arial;fontSize=17;',vertex='1',connectable='0',parent=id)
            g=E.SubElement(child,'mxGeometry',x=str(pos),y='-15',relative='1',attrib={'as':'geometry'})
            E.SubElement(g,'mxPoint',x='0',y='0',attrib={'as':'offset'})

edge('controller-auth','controller','auth','uses',ports=(1,28/264,0,28/264), kind='dependency')
edge('controller-account','controller','account','updates profile',ports=(.5,1,.5,0), kind='dependency')
edge('controller-access','controller','access','checks access',points=[(40,234),(40,861)],ports=(0,.5,0,28/180), kind='dependency')
edge('auth-google','auth','google','verifies identity',ports=(1,28/264,0,28/124), kind='dependency')
edge('auth-email','auth','email','sends code',points=[(1550,256),(1550,359.5)],ports=(1,154/264,0,28/124), kind='dependency')
edge('auth-user','auth','user','resolves verified email',ports=(.35,1,.35,0), kind='dependency')
edge('auth-challenge','auth','challenge','issues / consumes',points=[(1500,326),(1500,606)],ports=(1,224/264,0,28/202), kind='dependency')
edge('auth-session','auth','session','manages sessions',points=[(1180.2,60),(2140,60),(2140,946)],ports=(.81,0,1,28/150), kind='dependency')
edge('account-user','account','user','updates',ports=(1,28/152,0,28/202), kind='dependency')
edge('access-user','access','user','checks platform rights',points=[(720,861),(720,654.6)],ports=(1,28/180,0,.8), kind='dependency')
edge('access-membership','access','membership','checks project role',ports=(1,.5,0,90/124), kind='dependency')
edge('user-membership','user','membership','memberships',ports=(.5,1,.5,0),mult=('1','0..*'), kind='association')
edge('user-session','user','session','sessions',points=[(1500,664.7),(1500,1038)],ports=(1,.85,0,.8),mult=('1','0..*'), kind='composition')
edge('membership-role','membership','role','uses type',ports=(.5,1,.5,0), kind='dependency')

add_feature_pages(mx)
fit_class_widths(mx)
straighten_controller_fanout(mx)
top_down_project(mx)
top_down_remaining(mx)
top_down_engines(mx)
space_endpoint_labels(mx)
access_label = root.find("mxCell[@id='controller-access']/mxGeometry")
access_label.find("mxPoint[@as='offset']").set('x','-90')
E.indent(mx)
E.ElementTree(mx).write(OUT/(NAME+'.drawio'),encoding='utf-8',xml_declaration=True)
print(OUT/(NAME+'.drawio'))

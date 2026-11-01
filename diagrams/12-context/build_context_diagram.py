"""Expand the existing context page from the Report7 I/II snapshot."""
import html,json,math
from pathlib import Path
import xml.etree.ElementTree as E
HERE=Path(__file__).resolve().parent

def build():
 d=json.loads((HERE/'functional_scope.json').read_text(encoding='utf-8'))
 p=HERE/'System-Context-Diagram.drawio'; tree=E.parse(p); file=tree.getroot()
 for page in list(file):
  if page.get('id')=='report7-full-functional-scope': file.remove(page)
 page=next(p for p in file if p.get('name')=='main-2')
 model=page.find('mxGraphModel'); root=model.find('root'); layer=root[1].get('id')
 for cell in list(root)[2:]: root.remove(cell)
 model.set('page','0'); model.set('background','#ffffff')
 page.set('data-source','FA26SE115_Report7.md: I 6.1 (19 FE groups, 81 functions); II 1.1 (WBS)')
 base='html=1;whiteSpace=wrap;fontFamily=Arial;fontColor=#111827;strokeColor=#111827;fillColor=#FFFFFF;'
 def box(key,label,x,y,w,h,style=''):
  c=E.SubElement(root,'mxCell',id=key,value=label,parent=layer,vertex='1',style=base+style)
  E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
  return c
 groups={a:[] for a in ['Project Manager','Researcher','AI / LLM Provider','Local Node','Reviewer','Literature & Evidence Sources','External Data Sources','Platform Admin']}
 excluded=set(d['display_excluded_source_ids'])
 for f in d['compact_flows']:
  if not excluded.intersection(f['source_ids']):
   groups[f['actor']].append(f)
 for i,f in enumerate(d['extra_flows']): groups[f['actor']].append(dict(f,id=f.get('id','support-'+str(i))))
 # Fix Local Node directions: outgoing analysis/policy requests, incoming aggregates.
 for f in groups['Local Node']: f['direction']='in' if f['id']=='FE-12.2' else 'out'
 # Inputs to the platform first; outputs from the platform below. Stable order
 # retains each business group's relative order within its direction.
 for flows in groups.values():
  flows.sort(key=lambda f:f['direction']=='out')
 # Reference layout: staggered boxes around an ellipse, with short labelled
 # horizontal exchanges and nested right-angle turns close to the system.
 X,Y,W,H=1370,675,800,650
 cx,cy=X+W/2,Y+H/2
 box('platform','<b>OpenAI-Scientist</b><br>Tabular-data scientific research platform',X,Y,W,H,'ellipse;fontSize=28;align=center;verticalAlign=middle;strokeWidth=2.4;')
 def ellipse_y(x,bottom=True):
  dy=H/2*math.sqrt(max(0,1-((x-cx)/(W/2))**2))
  return cy+dy if bottom else cy-dy
 def ellipse_x(y,right=False):
  dx=W/2*math.sqrt(max(0,1-((y-cy)/(H/2))**2))
  return cx+dx if right else cx-dx
 placements={
  'Project Manager':(400,350,320,220),
  'Researcher':(50,990,320,260),
  'Reviewer':(2800,390,340,190),
  'Literature & Evidence Sources':(2850,790,370,150),
  'External Data Sources':(2970,1080,330,160),
  'Platform Admin':(2580,1280,340,190),
  'AI / LLM Provider':(2700,1680,340,170),
  'Local Node':(500,1680,340,170),
 }
 for idx,(actor,flows) in enumerate(groups.items()):
  ax,ay,aw,ah=placements[actor];n=len(flows);key='actor-'+str(idx)
  input_count=sum(f['direction']=='in' for f in flows)
  middle_count=(n-input_count+1)//2
  box(key,html.escape(d.get('actor_display_names',{}).get(actor,actor)),ax,ay,aw,ah,'fontSize=23;fontStyle=1;align=center;verticalAlign=middle;strokeWidth=1.5;')
  for i,f in enumerate(flows):
   t=(i+.5+(.6 if i>=input_count else 0))/(n+.6);label_segment=0
   if actor=='Project Manager':
    yy=ay+ah*t;sx=1760-140*i/max(n-1,1);sy=ellipse_y(sx,False)
    route=[(ax+aw,yy),(sx,yy),(sx,sy)];px,py=1,t
   elif actor=='Reviewer':
    yy=ay+ah*t;sx=1780+140*i/max(n-1,1);sy=ellipse_y(sx,False)
    route=[(ax,yy),(sx,yy),(sx,sy)];px,py=0,t
   elif actor=='Researcher':
    if i<input_count:
     yy=720+i*28;apx=ax+35+i*(aw-70)/max(input_count-1,1);sx=ellipse_x(yy);sy=yy
     route=[(apx,ay),(apx,yy),(sx,yy)];px,py=(apx-ax)/aw,0;label_segment=1
    elif i<input_count+middle_count:
     j=i-input_count;yy=1000+j*24
     sx=ellipse_x(yy);sy=yy
     route=[(ax+aw,yy),(sx,yy)];px,py=1,(yy-ay)/ah;label_segment=0
    else:
     j=i-input_count-middle_count;count=n-input_count-middle_count;yy=1300+j*28;apx=ax+aw-35-j*(aw-70)/max(count-1,1);sx=1550+j*180/max(count-1,1);sy=ellipse_y(sx)
     route=[(apx,ay+ah),(apx,yy),(sx,yy),(sx,sy)];px,py=(apx-ax)/aw,1;label_segment=1
   elif actor in ('Literature & Evidence Sources','External Data Sources'):
    yy=ay+ah*(.1+.8*t);sx=ellipse_x(yy,True);sy=yy
    route=[(ax,yy),(sx,yy)];px,py=0,(yy-ay)/ah
   elif actor=='AI / LLM Provider':
    yy=ay+ah*(.08+.84*t);sx=1880-i*6;sy=ellipse_y(sx)
    route=[(ax,yy),(sx,yy),(sx,sy)];px,py=0,(yy-ay)/ah
   elif actor=='Local Node':
    yy=ay+ah*(.15+.7*t);sx=1770+i*18;sy=ellipse_y(sx)
    route=[(ax+aw,yy),(sx,yy),(sx,sy)];px,py=1,(yy-ay)/ah
   else:
    yy=ay+ah*(.03+.94*t);sx=2012-i*7;sy=ellipse_y(sx)
    route=[(ax,yy),(sx,yy),(sx,sy)];px,py=0,(yy-ay)/ah
   outgoing=f['direction']=='out'
   actor_port=f'exitX={px};exitY={py};exitPerimeter=0;'
   system_port=f'entryX={(sx-X)/W};entryY={(sy-Y)/H};entryPerimeter=0;'
   if outgoing:
    actor_port=actor_port.replace('exit','entry');system_port=system_port.replace('entry','exit')
   c=E.SubElement(root,'mxCell',id='flow-'+f['id'],parent=layer,edge='1',source='platform' if outgoing else key,target=key if outgoing else 'platform',value=html.escape(f['label']),style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#111827;strokeWidth=1.4;endArrow=classic;endFill=1;endSize=9;fontFamily=Arial;fontSize=18;align=center;verticalAlign=middle;labelBackgroundColor=#FFFFFF;spacing=2;'+actor_port+system_port)
   lengths=[abs(x2-x1)+abs(y2-y1) for (x1,y1),(x2,y2) in zip(route,route[1:])]
   fraction=(sum(lengths[:label_segment])+lengths[label_segment]/2)/sum(lengths)
   if outgoing:fraction=1-fraction
   g=E.SubElement(c,'mxGeometry',relative='1',x=str(2*fraction-1),y='0',attrib={'as':'geometry'})
   points=route[1:-1]
   if outgoing:points.reverse()
   arr=E.SubElement(g,'Array',attrib={'as':'points'})
   for x,z in points:E.SubElement(arr,'mxPoint',x=str(x),y=str(z))
   c.set('data-fe',','.join(f.get('source_ids',[f['id']])));c.set('data-source-text',f.get('text',f['label']));c.set('data-wbs',f.get('wbs',''))
 tree.write(p,encoding='utf-8',xml_declaration=True)
 print(f"Updated main-2: {sum(len(g) for g in groups.values())} flows; Researcher: {len(groups['Researcher'])}; peripheral flows omitted")
if __name__=='__main__': build()

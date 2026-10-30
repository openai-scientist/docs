"""Build the review draft of one email-code sign-in attempt (Report7 III 3.2.1)."""
from pathlib import Path
import xml.etree.ElementTree as E

OUT = Path(__file__).resolve().parent
NAME = 'State-Machine-Diagram-Sign-In-With-Email-Code'
BASE = 'html=1;fontFamily=Arial;fontSize=14;fontColor=#000000;strokeColor=#000000;fillColor=#ffffff;strokeWidth=1;'


def build():
    mx = E.Element('mxfile', host='drawio', version='26.0.0')
    page = E.SubElement(mx, 'diagram', id='email-code-attempt', name='Sign In With Email Code')
    model = E.SubElement(page, 'mxGraphModel', grid='1', gridSize='10', page='1', pageWidth='850', pageHeight='1100', background='#ffffff')
    root = E.SubElement(model, 'root')
    E.SubElement(root, 'mxCell', id='0')
    E.SubElement(root, 'mxCell', id='1', parent='0')

    def node(key, text, x, y, w, h, style, parent='1'):
        cell = E.SubElement(root, 'mxCell', id=key, value=text, style=BASE + style, vertex='1', parent=parent)
        E.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), attrib={'as': 'geometry'})
        return cell

    def edge(key, source, target, text='', ports=(.5, 1, .5, 0), points=(), offset=(0, 0)):
        sx, sy, tx, ty = ports
        style = BASE + f'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;endArrow=open;endSize=10;endFill=0;labelBackgroundColor=#ffffff;align=center;verticalAlign=middle;exitX={sx};exitY={sy};entryX={tx};entryY={ty};exitPerimeter=1;entryPerimeter=1;'
        answer = text if source == 'valid-code' and text in {'Yes', 'No'} else None
        cell = E.SubElement(root, 'mxCell', id=key, value=f'[{answer}]' if answer else text, style=style, edge='1', parent='1', source=source, target=target)
        if answer:
            cell.set('branch-answer', answer)
            cell.set('guard-expression', 'code correct and unexpired' if answer == 'Yes' else 'code incorrect or expired')
        geo = E.SubElement(cell, 'mxGeometry', relative='1', attrib={'as': 'geometry'})
        if source == 'valid-code':
            geo.set('x', '-0.85')
        if points:
            arr = E.SubElement(geo, 'Array', attrib={'as': 'points'})
            for x, y in points:
                E.SubElement(arr, 'mxPoint', x=str(x), y=str(y))
        E.SubElement(geo, 'mxPoint', x=str(offset[0]), y=str(offset[1]), attrib={'as': 'offset'})

    node('initial', '', 368, 65, 24, 24, 'ellipse;fillColor=#000000;')
    node('signed-out', 'Signed out', 280, 130, 200, 54, 'rounded=1;arcSize=15;whiteSpace=wrap;')
    node('awaiting-code', 'Awaiting email code', 280, 300, 200, 54, 'rounded=1;arcSize=15;whiteSpace=wrap;')
    node('valid-code', 'Is code correct\nand unexpired?', 260, 430, 240, 100, 'rhombus;whiteSpace=wrap;')
    node('signed-in', 'Signed in', 540, 640, 200, 54, 'rounded=1;arcSize=15;whiteSpace=wrap;')
    node('final', '', 365, 740, 30, 30, 'ellipse;shape=endState;fillColor=#000000;')
    edge('begin', 'initial', 'signed-out')
    edge('request-code', 'signed-out', 'awaiting-code', 'email code requested\n/ send one-time code', offset=(0, 0))
    edge('submit-code', 'awaiting-code', 'valid-code', 'code submitted', offset=(0, 0))
    edge('invalid-code', 'valid-code', 'awaiting-code', 'No', ports=(0, .5, 0, .5), points=((100, 480), (100, 327)), offset=(0, 0))
    edge('accept-code', 'valid-code', 'signed-in', 'Yes', ports=(1, .5, .5, 0), points=((640, 480),), offset=(0, 0))
    edge('complete-attempt', 'signed-in', 'final', ports=(.5, 1, 1, .5), points=((640, 755),))
    from build_state_diagrams import apply_reference_style
    apply_reference_style(page)
    E.indent(mx, space='  ')
    path = OUT / f'{NAME}.drawio'
    E.ElementTree(mx).write(path, encoding='utf-8', xml_declaration=True)
    print(path)


if __name__ == '__main__':
    build()

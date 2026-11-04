"""Build the 8 IV.3 class diagrams (draw.io) and their Mermaid copy from class_model.py.

Layout: one row per layer (controller, services, helpers, entities). Edges between rows
leave the bottom of the upper box and enter the top of the lower box through a private
lane in the gap; edges that skip a row go down a free corridor between boxes.
Requires Pillow and the Windows Arial fonts to size boxes.
"""
from html import escape
from math import ceil
from pathlib import Path
import re
import textwrap
import xml.etree.ElementTree as E

from PIL import ImageFont

from class_model import PAGES

OUT = Path(__file__).resolve().parent
DRAWIO = OUT / 'Class-Diagram-Authentication-Account.drawio'
MERMAID = OUT / 'Class-Diagrams-Mermaid.md'

BASE = 'html=1;fontFamily=Arial;fontSize=17;fontColor=#000000;strokeColor=#000000;strokeWidth=1;fillColor=#FFFFFF;'
EDGE_KIND = {
    'dependency': 'dashed=1;endArrow=open;endFill=0;',
    'association': 'endArrow=none;',
    'composition': 'startArrow=diamondThin;startFill=1;startSize=16;endArrow=none;',
    'realization': 'dashed=1;endArrow=block;endFill=0;',
}
BODY = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 17)
HEAD = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 19)
H_GAP, LANE, MARGIN, LEFT, TOP, LINE = 160, 22, 70, 60, 60, 21


def wrap(items):
    return [part for item in items for part in
            textwrap.wrap(item, width=84, subsequent_indent='    ', break_long_words=False, break_on_hyphens=False)]


def text(line):
    """Escape a member line and keep the indent of a wrapped continuation."""
    body = line.lstrip(' ')
    return '&nbsp;' * (len(line) - len(body)) + escape(body)


def measure(c):
    first = c['literals'] or c['attrs']
    c['first'], c['second'] = wrap(first), wrap(c['ops'])
    texts = [HEAD.getlength(f'«{c["stereo"]}»') + 48, HEAD.getlength(c['name']) + 48]
    texts += [BODY.getlength(t) + 32 for t in c['first'] + c['second']]
    c['w'] = max(190, ceil(max(texts) / 10) * 10)
    c['h1'] = max(24, len(c['first']) * LINE + 18)
    c['h2'] = len(c['second']) * LINE + 18 if c['second'] else 0
    c['h'] = 56 + c['h1'] + c['h2']


def layout(page):
    classes = {c['name']: c for c in page['classes']}
    for c in classes.values():
        measure(c)
    rows = {}
    for c in page['classes']:
        rows.setdefault(c['row'], []).append(c)
    order = sorted(rows)
    widths = {r: sum(c['w'] for c in rows[r]) + H_GAP * (len(rows[r]) - 1) for r in order}
    full = max(widths.values())
    neighbours = {n: [] for n in classes}
    for rel in page['relations']:
        neighbours[rel['source']].append(rel['target'])
        neighbours[rel['target']].append(rel['source'])

    def place():
        for r in order:
            x = LEFT + (full - widths[r]) / 2
            for c in rows[r]:
                c['x'], c['ri'] = x, order.index(r)
                x += c['w'] + H_GAP

    place()
    # Barycentre ordering (down, then up) so that each class sits under its users.
    for sweep in (order[1:], order[-2::-1], order[1:]):
        for r in sweep:
            def key(c):
                linked = [classes[n] for n in neighbours[c['name']] if classes[n]['row'] != r]
                if not linked:
                    return c['x'] + c['w'] / 2
                return sum(o['x'] + o['w'] / 2 for o in linked) / len(linked)
            rows[r].sort(key=key)
            place()
    return classes, [rows[r] for r in order], full


def plan_edges(page, classes, rows):
    """Decide ports, lanes and corridors; returns per-edge geometry once row y is known."""
    sides = {}  # (class, 'top'|'bottom') -> list of (edge index, other x)
    plans = []
    for i, rel in enumerate(page['relations']):
        s, t = classes[rel['source']], classes[rel['target']]
        if s['ri'] == t['ri']:
            row = rows[s['ri']]
            a, b = sorted((row.index(s), row.index(t)))
            if b - a == 1:
                plans.append(dict(kind='side'))
                continue
            plans.append(dict(kind='under', gap=s['ri']))
            sides.setdefault((s['name'], 'bottom'), []).append((i, t['x']))
            sides.setdefault((t['name'], 'bottom'), []).append((i, s['x']))
            continue
        up, low = (s, t) if s['ri'] < t['ri'] else (t, s)
        plans.append(dict(kind='down', up=up['name'], low=low['name'], gap=up['ri'], gap2=low['ri'] - 1))
        sides.setdefault((up['name'], 'bottom'), []).append((i, low['x'] + low['w'] / 2))
        sides.setdefault((low['name'], 'top'), []).append((i, up['x'] + up['w'] / 2))
    port = {}
    for (name, side), items in sides.items():
        items.sort(key=lambda e: e[1])
        for k, (i, _) in enumerate(items):
            port[(i, name, side)] = (k + 1) / (len(items) + 1)
    lanes = {}
    for i, p in enumerate(plans):
        if p['kind'] in ('under', 'down'):
            lanes.setdefault(p['gap'], []).append((i, 'a'))
        if p['kind'] == 'down' and p['gap2'] != p['gap']:
            lanes.setdefault(p['gap2'], []).append((i, 'b'))
    return plans, port, lanes


def place_rows(rows, lanes):
    y = TOP
    tops, bottoms = [], []
    for ri, row in enumerate(rows):
        tops.append(y)
        bottom = y + max(c['h'] for c in row)
        bottoms.append(bottom)
        for c in row:
            c['y'] = y
        y = bottom + 2 * MARGIN + LANE * len(lanes.get(ri, []))
    return tops, bottoms, y


def corridor(rows, lo, hi, want, used):
    """Free x between boxes in rows lo..hi (exclusive) nearest to want."""
    spans = [(c['x'] - 30, c['x'] + c['w'] + 30) for r in rows[lo + 1:hi] for c in r]
    candidates = {want} | {a - 1 for a, _ in spans} | {b + 1 for _, b in spans}
    for base in sorted(candidates, key=lambda v: abs(v - want)):
        step = -14 if base in {a - 1 for a, _ in spans} else 14
        x = base + step * used.get(round(base), 0)
        if not any(a < x < b for a, b in spans):
            used[round(base)] = used.get(round(base), 0) + 1
            return x
    return want


def build_page(mx, page):
    classes, rows, full = layout(page)
    plans, port, lanes = plan_edges(page, classes, rows)
    tops, bottoms, height = place_rows(rows, lanes)
    lane_y = {}

    def span(key):
        i, part = key
        rel, plan = page['relations'][i], plans[i]
        s, t = classes[rel['source']], classes[rel['target']]
        if plan['kind'] == 'under':
            return abs((s['x'] + s['w'] * port[i, s['name'], 'bottom']) - (t['x'] + t['w'] * port[i, t['name'], 'bottom']))
        up, low = classes[plan['up']], classes[plan['low']]
        ux = up['x'] + up['w'] * port[i, up['name'], 'bottom']
        lx = low['x'] + low['w'] * port[i, low['name'], 'top']
        return abs(ux - lx)
    for gap, items in lanes.items():
        items.sort(key=lambda e: -span(e))
        for k, key in enumerate(items):
            lane_y[key[0], key[1]] = bottoms[gap] + MARGIN + LANE * k
    diagram = E.SubElement(mx, 'diagram', id=page['id'], name=page['name'])
    model = E.SubElement(diagram, 'mxGraphModel', grid='1', gridSize='10', page='1', background='#FFFFFF',
                         pageWidth=str(int(full + 2 * LEFT)), pageHeight=str(int(height)))
    root = E.SubElement(model, 'root')
    E.SubElement(root, 'mxCell', id='0')
    E.SubElement(root, 'mxCell', id='1', parent='0')

    def vertex(id, value, x, y, w, h, style, parent='1'):
        cell = E.SubElement(root, 'mxCell', id=id, value=value, style=BASE + style, vertex='1', parent=parent)
        E.SubElement(cell, 'mxGeometry', x=str(round(x, 1)), y=str(round(y, 1)), width=str(w), height=str(h),
                     attrib={'as': 'geometry'})

    for c in page['classes']:
        vertex(c['name'], f'«{c["stereo"]}»<br><b>{escape(c["name"])}</b>', c['x'], c['y'], c['w'], c['h'],
               'swimlane;startSize=56;horizontal=1;collapsible=0;container=1;align=center;fontSize=19;')
        vertex(c['name'] + '-attributes', '<br>'.join(text(s) for s in c['first']), 0, 56, c['w'], c['h1'],
               'text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;',
               c['name'])
        if c['second']:
            vertex(c['name'] + '-operations', '<br>'.join(text(s) for s in c['second']), 0, 56 + c['h1'], c['w'],
                   c['h2'], 'rounded=0;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;', c['name'])

    used = {}
    for i, (rel, plan) in enumerate(zip(page['relations'], plans)):
        s, t = classes[rel['source']], classes[rel['target']]
        points = []
        if plan['kind'] == 'side':
            y = max(s['y'], t['y']) + 28
            right = s['x'] < t['x']
            ports = (1 if right else 0, (y - s['y']) / s['h'], 0 if right else 1, (y - t['y']) / t['h'])
        elif plan['kind'] == 'under':
            ly = lane_y[i, 'a']
            ps, pt = port[i, s['name'], 'bottom'], port[i, t['name'], 'bottom']
            points = [(s['x'] + s['w'] * ps, ly), (t['x'] + t['w'] * pt, ly)]
            ports = (ps, 1, pt, 1)
        else:
            up, low = classes[plan['up']], classes[plan['low']]
            pu, pl = port[i, up['name'], 'bottom'], port[i, low['name'], 'top']
            ux, lx = up['x'] + up['w'] * pu, low['x'] + low['w'] * pl
            ya = lane_y[i, 'a']
            if plan['gap2'] == plan['gap']:
                path = [(ux, ya), (lx, ya)]
            else:
                cx = corridor(rows, up['ri'], low['ri'], (ux + lx) / 2, used)
                yb = lane_y[i, 'b']
                path = [(ux, ya), (cx, ya), (cx, yb), (lx, yb)]
            if up is s:
                points, ports = path, (pu, 1, pl, 0)
            else:
                points, ports = path[::-1], (pl, 0, pu, 1)
        style = BASE + ('edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;endSize=16;'
                        'strokeWidth=1.5;labelBackgroundColor=#FFFFFF;spacing=5;')
        style += EDGE_KIND[rel['kind']]
        style += 'exitX={};exitY={};entryX={};entryY={};exitPerimeter=0;entryPerimeter=0;'.format(
            *(round(v, 4) for v in ports))
        eid = f'{page["id"]}-e{i + 1}'
        cell = E.SubElement(root, 'mxCell', id=eid, value=escape(rel['label']), style=style, edge='1', parent='1',
                            source=s['name'], target=t['name'])
        geo = E.SubElement(cell, 'mxGeometry', relative='1', attrib={'as': 'geometry'})
        if points:
            arr = E.SubElement(geo, 'Array', attrib={'as': 'points'})
            for x, y in points:
                E.SubElement(arr, 'mxPoint', x=str(round(x, 1)), y=str(round(y, 1)))
        E.SubElement(geo, 'mxPoint', x='0', y='-12', attrib={'as': 'offset'})
        if rel['mult']:
            for suffix, value, pos in (('source', rel['mult'][0], -0.85), ('target', rel['mult'][1], 0.85)):
                label = E.SubElement(root, 'mxCell', id=f'{eid}-{suffix}', value=value, vertex='1', connectable='0',
                                     parent=eid, style='edgeLabel;html=1;fontFamily=Arial;fontSize=17;'
                                                       'labelBackgroundColor=#FFFFFF;')
                g = E.SubElement(label, 'mxGeometry', x=str(pos), y='-16', relative='1', attrib={'as': 'geometry'})
                E.SubElement(g, 'mxPoint', x='0', y='0', attrib={'as': 'offset'})


WHITE = ("%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', "
         "'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', "
         "'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', "
         "'fontFamily': 'Arial'}}}%%")


def mermaid(pages):
    arrow = {'dependency': '..>', 'association': '--', 'composition': '*--', 'realization': '..|>'}
    out = ['# Class Diagrams — Mermaid', '',
           'Xuất từ [class_model.py](class_model.py) bằng [build_class_diagrams.py](build_class_diagrams.py), '
           'cùng nội dung với file draw.io; mỗi khối đặt nền trắng, chữ và nét đen. Class chỉ có tên '
           '(không ngăn thành viên) thuộc nhóm khác và được vẽ lại để thể hiện phụ thuộc. '
           'Chạy lại builder sẽ ghi đè các chỉnh tay trong file này.', '']
    for n, page in enumerate(pages, 1):
        out += [f'## {n}. {page["name"]}', '', '```mermaid', WHITE, 'classDiagram']
        for c in page['classes']:
            out.append(f'    class {c["name"]} {{')
            out.append(f'        <<{c["stereo"]}>>')
            for line in c['literals'] + c['attrs'] + c['ops']:
                line = re.sub(r'<([^<>]+)>', r'~\1~', line)
                # Mermaid prints "name(args) : Type" itself from "name(args) Type".
                line = re.sub(r'^([-+#~]) (.*\)) : (.*)$', r'\1\2 \3', line)
                # Mermaid reads "*" as abstract/italic and "__" as bold inside members.
                line = line.replace('*', '∗').replace('_', '#95;')
                out.append('        ' + line)
            out.append('    }')
        for r in page['relations']:
            mult = r['mult'] or ('', '')
            left = f' "{mult[0]}"' if mult[0] else ''
            right = f'"{mult[1]}" ' if mult[1] else ''
            out.append(f'    {r["source"]}{left} {arrow[r["kind"]]} {right}{r["target"]} : {r["label"]}')
        out += ['```', '']
    return '\n'.join(out)


def check(pages):
    for page in pages:
        names = [c['name'] for c in page['classes']]
        assert len(names) == len(set(names)), page['id']
        for r in page['relations']:
            assert r['source'] in names and r['target'] in names, (page['id'], r)


def main(argv=()):
    """Write the Mermaid copy. Since 2026-11-03 the draw.io file is edited by hand (imported from
    Mermaid and re-laid out by the user); it is only regenerated with --drawio, which discards that layout."""
    check(PAGES)
    MERMAID.write_text(mermaid(PAGES), encoding='utf-8')
    print(MERMAID, sum(len(p['classes']) for p in PAGES), 'classes')
    if '--drawio' in argv:
        mx = E.Element('mxfile', host='app.diagrams.net')
        for page in PAGES:
            build_page(mx, page)
        E.indent(mx)
        E.ElementTree(mx).write(DRAWIO, encoding='utf-8', xml_declaration=True)
        print(DRAWIO, 'regenerated (hand layout replaced)')


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

"""Remove draw.io cells by id, plus their child cells and every edge attached to them.

Usage: python3 rm_cells.py <file.drawio> <id> [<id> ...]
"""
import sys
import xml.etree.ElementTree as ET

path, ids = sys.argv[1], set(sys.argv[2:])
tree = ET.parse(path)
removed = 0
for model in tree.getroot().iter('root'):
    cells = list(model)
    drop = set(ids)
    changed = True
    while changed:  # children and attached edges, transitively
        changed = False
        for c in cells:
            cid = c.get('id')
            inner = c if c.tag == 'mxCell' else c.find('mxCell')
            if cid in drop or inner is None:
                continue
            if inner.get('parent') in drop or inner.get('source') in drop or inner.get('target') in drop:
                drop.add(cid); changed = True
    for c in cells:
        if c.get('id') in drop:
            model.remove(c); removed += 1
tree.write(path, encoding='utf-8', xml_declaration=False)
print(f'{path}: removed {removed} cells')

"""Replace section V of the Report 7 docx with S5-testing.md (short SEP490 form).

usage: inject_v.py REPORT.docx S5.md TESTS_DIR
Paragraph and table formatting is cloned from the existing section V, so the docx keeps its styles.
"""
import collections
import json
import re
import sys
from copy import deepcopy
from pathlib import Path

import docx
from docx.oxml.ns import qn

doc_path, md_path, tests = sys.argv[1], sys.argv[2], Path(sys.argv[3])
d = docx.Document(doc_path)
body = d.element.body
W = lambda tag: qn('w:' + tag)


def text_of(el):
    return ''.join(t.text or '' for t in el.iter(W('t')))


def style_of(el):
    s = el.find(W('pPr') + '/' + W('pStyle'))
    return s.get(W('val')) if s is not None else None


# --- locate section V in the body
els = list(body.iterchildren())
h1 = d.styles['Heading 1'].style_id
start = next(i for i, e in enumerate(els) if e.tag == W('p') and style_of(e) == h1 and text_of(e).startswith('V.'))
end = next(i for i, e in enumerate(els) if i > start and e.tag == W('p') and style_of(e) == h1)
old = els[start + 1:end]
if old and any(b.get(W('type')) == 'page' for b in old[-1].iter(W('br'))):
    old = old[:-1]  # keep the page break before section VI

# prototypes from the old section
ids = {d.styles[n].style_id: n for n in ('Heading 2', 'Heading 3', 'Normal') if n in [s.name for s in d.styles]}
proto = {}
for e in old:
    if e.tag == W('p') and text_of(e).strip():
        name = ids.get(style_of(e), 'Normal') if style_of(e) else 'Normal'
        key = 'bullet' if text_of(e).startswith('•') else name
        proto.setdefault(key, e)
    if e.tag == W('tbl') and 'tbl' not in proto and text_of(e).startswith('Member'):
        proto['tbl'] = e


def unbold(el):
    for rpr in el.iter(W('rPr')):
        for b in rpr.findall(W('b')) + rpr.findall(W('bCs')):
            rpr.remove(b)
    return el


def para(kind, text):
    p = deepcopy(proto[kind])
    if kind in ('Normal', 'bullet'):
        unbold(p)
    runs = p.findall(W('r'))
    for r in runs[1:]:
        p.remove(r)
    for x in list(p):
        if x.tag not in (W('pPr'), W('r')):
            p.remove(x)
    r = runs[0]
    for x in list(r):
        if x.tag != W('rPr'):
            r.remove(x)
    t = r.makeelement(W('t'), {})
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r.append(t)
    return p


def cell(tc_proto, text, width):
    tc = deepcopy(tc_proto)
    tc.find(W('tcPr') + '/' + W('tcW')).set(W('w'), str(width)) if tc.find(W('tcPr') + '/' + W('tcW')) is not None else None
    ps = tc.findall(W('p'))
    for p in ps[1:]:
        tc.remove(p)
    p = ps[0]
    runs = p.findall(W('r'))
    for r in runs[1:]:
        p.remove(r)
    for x in list(runs[0]):
        if x.tag != W('rPr'):
            runs[0].remove(x)
    t = runs[0].makeelement(W('t'), {})
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    runs[0].append(t)
    return tc


def table(rows):
    src = proto['tbl']
    tbl = deepcopy(src)
    trs = tbl.findall(W('tr'))
    head_tr, body_tr = trs[0], trs[1]
    head_tc, body_tc = head_tr.find(W('tc')), body_tr.find(W('tc'))
    total = sum(int(g.get(W('w'))) for g in tbl.find(W('tblGrid')))
    n = len(rows[0])
    grid = tbl.find(W('tblGrid'))
    for g in list(grid):
        grid.remove(g)
    # column width follows the longest word and the amount of text in the column
    weight = [3 + max(max(len(w) for r in rows for w in (r[j] or 'x').split()) * 1.0,
                  min(22, sum(len(r[j]) for r in rows) / len(rows))) for j in range(n)]
    widths = [int(total * w / sum(weight)) for w in weight]
    for w in widths:
        grid.append(grid.makeelement(W('gridCol'), {W('w'): str(w)}))
    for tr in trs:
        tbl.remove(tr)
    for k, row in enumerate(rows):
        tr = deepcopy(head_tr if k == 0 else body_tr)
        for tc in tr.findall(W('tc')):
            tr.remove(tc)
        for v in row:
            c = cell(head_tc if k == 0 else body_tc, v, widths[len(tr.findall(W('tc')))])
            tr.append(c if k == 0 else unbold(c))
        tbl.append(tr)
    return tbl


# --- values computed from the result files
def unit_types():
    sys.path.insert(0, str(tests))
    from unit_spec import FUNCTIONS
    from unit_spec_more import MORE
    FUNCTIONS = FUNCTIONS + MORE
    c = collections.Counter(case[1] for f in FUNCTIONS for case in f['cases'])
    return {'unit_n': str(c['N']), 'unit_a': str(c['A']), 'unit_b': str(c['B'])}


rounds = [json.load(open(tests / f'round{k}.json')) for k in (1, 2, 3) if (tests / f'round{k}.json').exists()]
KINDS = ('Passed', 'Failed', 'Pending')


def system_rounds():
    rows = [['Round', 'Test date', 'Passed', 'Failed', 'Pending', 'Total']]
    for k, r in enumerate(rounds, 1):
        c = collections.Counter(x['result'] for x in r)
        rows.append([f'Round {k}', r[0]['date'], *(str(c[x]) for x in KINDS), str(len(r))])
    return rows


def system_features():
    last = rounds[-1]
    rows = [['No', 'Feature', 'Passed', 'Failed', 'Pending', 'Number of test cases']]
    for i, f in enumerate(dict.fromkeys(x['feature'] for x in last), 1):
        c = collections.Counter(x['result'] for x in last if x['feature'] == f)
        rows.append([str(i), f, *(str(c[x]) for x in KINDS), str(sum(c.values()))])
    c = collections.Counter(x['result'] for x in last)
    rows.append(['', 'Sub total', *(str(c[x]) for x in KINDS), str(len(last))])
    return rows


# --- images of the Report 5 workbooks (one sheet each, rendered by LibreOffice, white margin cut)
import subprocess
import tempfile

import openpyxl
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm
from PIL import Image, ImageChops

BOOKS = {'unit-cases': ('FA26SE115_Report5_Unit Test.xlsx', 'create_project'),
         'unit-statistics': ('FA26SE115_Report5_Unit Test.xlsx', 'Statistics'),
         'system-cases': ('FA26SE115_Report5_Test Report.xlsx', 'Test Cases'),
         'system-statistics': ('FA26SE115_Report5_Test Report.xlsx', 'Test Statistics')}
tmp = Path(tempfile.mkdtemp())


def sheet_image(key):
    book, sheet = BOOKS[key]
    # keep every sheet so cross-sheet formulas resolve; hide the others and fit the sheet to one page
    wb = openpyxl.load_workbook(tests.parent / book)
    for ws in wb.worksheets:
        ws.sheet_state = 'visible' if ws.title == sheet else 'hidden'
    wb.active = wb.sheetnames.index(sheet)
    ws = wb[sheet]
    last = max(c.row for r in ws.iter_rows() for c in r if c.value not in (None, ''))
    ws.print_area = f'A1:{openpyxl.utils.get_column_letter(ws.max_column)}{last}'  # table only, not the template charts
    ws.page_setup.orientation = 'landscape'
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 1
    x = tmp / f'{key}.xlsx'
    wb.save(x)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(tmp), str(x)], capture_output=True)
    subprocess.run(['pdftoppm', '-png', '-r', '150', '-f', '1', '-l', '1', '-singlefile', str(tmp / f'{key}.pdf'), str(tmp / key)])
    im = Image.open(tmp / f'{key}.png').convert('RGB')
    box = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
    # drop the page footer of the template: keep content above the last 8% of the page
    im = im.crop((box[0], box[1], box[2], min(box[3], int(im.height * 0.9))))
    box = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
    im.crop(box).save(tmp / f'{key}-cut.png')
    return tmp / f'{key}-cut.png'


def image(key, caption):
    holder = d.add_paragraph()
    holder.alignment = WD_ALIGN_PARAGRAPH.CENTER
    holder.add_run().add_picture(str(sheet_image(key)), width=Cm(16))
    cap = para('Normal', caption)
    docx.text.paragraph.Paragraph(cap, d).alignment = WD_ALIGN_PARAGRAPH.CENTER
    return [holder._p, cap]


values = unit_types()
special = {
    '{{system_rounds}}': lambda: [para('Normal', 'Results by round (workbook sheets of each feature):'),
                                  table(system_rounds())],
    '{{system_features}}': lambda: [para('Normal', f'Results of Round {len(rounds)} by feature:'), table(system_features())],
}

# --- markdown to elements (the first heading and its intro are notes, not report text)
new, rows = [], []
lines = Path(md_path).read_text().split('\n')
lines = lines[next(i for i, l in enumerate(lines) if l.startswith('## ')):]
for line in lines + ['']:
    for k, v in values.items():
        line = line.replace('{{' + k + '}}', v)
    if line.startswith('|'):
        cells = [c.strip().replace('`', '') for c in line.strip('|').split('|')]
        if not set(''.join(cells)) <= set('-: '):
            rows.append(cells)
        continue
    if rows:
        new.append(table(rows))
        rows = []
    s = line.strip()
    if not s:
        continue
    if s in special:
        new += special[s]()
    elif s.startswith('!['):
        cap, key = re.match(r'!\[(.*)\]\((.*)\)', s).groups()
        new += image(key, cap)
    elif s.startswith('### '):
        new.append(para('Heading 3', s[4:]))
    elif s.startswith('## '):
        new.append(para('Heading 2', s[3:]))
    elif s.startswith('- '):
        new.append(para('bullet', '• ' + s[2:].replace('`', '')))
    else:
        new.append(para('Normal', s.replace('`', '')))

anchor = els[end]
for e in old:
    body.remove(e)
for e in new:
    anchor.addprevious(e)

# --- table of contents lines of section V
TOC = {'4.1 Test Case Summary': '4.1 Unit Test Cases', '4.2 Sample Test Cases': '4.2 System Test Cases',
       '5.1 Test Summary Report': '5.1 Unit Test Report', '5.2 Defect Report': '5.2 System Test Report'}
toc_v = False
for p in d.paragraphs[:600]:
    tx = p.text
    if tx.startswith('V. Software Testing'):
        toc_v = True
    elif tx.startswith('VI. '):
        break
    if toc_v:
        for a, b in TOC.items():
            if tx.startswith(a):
                for t in p._p.iter(W('t')):
                    if a.split(' ', 1)[1] in (t.text or ''):
                        t.text = t.text.replace(a.split(' ', 1)[1], b.split(' ', 1)[1])
d.save(doc_path)
print('removed', len(old), 'elements; inserted', len(new), '; rounds', len(rounds))

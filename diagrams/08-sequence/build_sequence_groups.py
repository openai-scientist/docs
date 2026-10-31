"""Build source-backed, editable sequence groups and an explicit inventory."""
from html import escape
from pathlib import Path
import hashlib
import textwrap
import xml.etree.ElementTree as E
from sequence_flows import GROUPS

OUT = Path(__file__).resolve().parent
REPORT = Path('C:/Users/ADMIN/Downloads/FA26SE115_Report7 (1).md')
BASE = ('html=1;fontFamily=Arial;fontSize=12;fontColor=#000000;'
        'strokeColor=#000000;strokeWidth=1;fillColor=#FFFFFF;')
ROW = 54


def flatten(items):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def repository_interactions(items):
    """Make the requested data-access boundary explicit before layout."""
    result = []
    for item in flatten(items):
        if 'branches' in item:
            result.append({**item, 'branches': [(guard, repository_interactions(body))
                                                for guard, body in item['branches']]})
        elif 'body' in item:
            result.append({**item, 'body': repository_interactions(item['body'])})
        elif item.get('to') == 'd' and not item.get('reply'):
            result.extend([{**item, 'to': 'repo'},
                           {**item, 'from': 'repo', 'label': 'Read / persist requested data'}])
        elif item.get('from') == 'd' and item.get('reply'):
            result.extend([{**item, 'to': 'repo'}, {**item, 'from': 'repo'}])
        else:
            result.append(item)
    return result


def draw_page(flow, page_id):
    repository = flow['service'].removesuffix('Service').removesuffix('Engine')
    repository = {'RunOrchestrator': 'Run', 'IndependentReview': 'Review',
                  'AIPrincipalInvestigator': 'Decision'}.get(repository, repository)
    names = {'u': flow['actor'], 'w': 'Web App', 'c': ': ' + flow['controller'],
             'a': ': AuthenticationService' if flow.get('session_only') else ': AuthorizationService',
             's': ': ' + flow['service'],
             'repo': ': ' + flow.get('repository', repository + 'Repository'), 'd': 'Database'}
    names.update(flow.get('participants', {}))
    # Only show participants which actually send/receive a message.
    access_label = 'validateSession(session)' if flow.get('session_only') else 'requireRole(user, project, action)'
    if flow['actor'] == 'Platform Admin':
        names['a'] = ': AdministrationService'
        access_label = 'requirePlatformAdmin(userId)'
    if flow.get('public'):
        names.pop('a')
        prelude = []
    else:
        prelude = [{'from': 'c', 'to': 'a', 'label': access_label},
                   {'from': 'a', 'to': 'c', 'label': 'Access check result', 'reply': True}]
    completion = [] if flow.get('terminal_branches') else [
        {'from': 's', 'to': 'c', 'label': flow.get('result', 'Operation result'), 'reply': True},
        {'from': 'c', 'to': 'w', 'label': 'Result or domain validation error', 'reply': True},
        {'from': 'w', 'to': 'u', 'label': flow.get('display', 'Show result or error'), 'reply': True},
    ]
    main = [
        {'from': 'c', 'to': 's', 'label': flow['operation']},
        *flatten(flow['steps']),
        *completion,
    ]
    if prelude:
        execution = [{'branches': [
            ('[access denied or session invalid]', [
                {'from': 'c', 'to': 'w', 'label': 'Access rejected', 'reply': True},
                {'from': 'w', 'to': 'u', 'label': 'Show unavailable / sign-in required', 'reply': True}]),
            ('[else: access allowed]', main)]}]
    else:
        execution = main
    tree = [
        {'from': 'u', 'to': 'w', 'label': flow['trigger']},
        {'from': 'w', 'to': 'c', 'label': flow.get('entry', flow['operation'])},
        *prelude, *execution,
    ]
    if flow.get('google_consent'):
        tree = [
            {'from': 'u', 'to': 'w', 'label': 'Choose Sign in with Google'},
            {'from': 'w', 'to': 'g', 'label': 'Open Google account and consent screen'},
            {'from': 'g', 'to': 'w', 'label': 'Authorization callback: code or denial', 'reply': True},
            {'branches': [
                ('[consent denied]', [{'from': 'w', 'to': 'u', 'label': 'Show sign-in cancelled', 'reply': True}]),
                ('[authorization code returned]', [
                    {'from': 'w', 'to': 'c', 'label': 'signInWithGoogle(code)'}, *main])]},
        ]
    if flow.get('system_trigger'):
        names = {'t': flow['system_trigger'], **names}
        tree = [
            {'from': 't', 'to': 's', 'label': flow['operation'], 'async': True},
            *flatten(flow['steps']),
            {'kind': 'opt', 'guard': '[user connected and authorized]', 'body': [
                {'from': 's', 'to': 'c', 'label': 'Publish authorized inbox update', 'async': True},
                {'from': 'c', 'to': 'w', 'label': 'Deliver in-app update', 'async': True},
                {'from': 'w', 'to': 'u', 'label': 'Show notification / decision status', 'async': True}]},
        ]
    if flow.get('custom_tree'):
        tree = flow['custom_tree']
    tree = repository_interactions(tree)
    messages, fragments = [], []
    cursor = 160

    def layout(items, depth=0):
        nonlocal cursor
        for item in flatten(items):
            if 'branches' in item or item.get('kind') in ('loop', 'opt', 'par'):
                start = cursor
                cursor += 26
                branch_data = item.get('branches', [(item['guard'], item['body'])]) if 'branches' not in item else item['branches']
                guards, dividers = [], []
                indices = []
                for i, (guard, body) in enumerate(branch_data):
                    if i:
                        dividers.append(cursor)
                        cursor += 12
                    guards.append((cursor, guard))
                    cursor += 70
                    before = len(messages)
                    layout(body, depth+1)
                    indices.extend(range(before, len(messages)))
                    cursor += 10
                fragments.append({'kind': item.get('kind', 'alt'), 'top': start,
                                  'bottom': cursor, 'guards': guards, 'dividers': dividers,
                                  'indices': indices, 'depth': depth})
                cursor += 48
            else:
                messages.append({**item, 'y': cursor, 'number': len(messages)+1})
                cursor += ROW
    layout(tree)
    if names.get('a') == names.get('s'):
        for message in messages:
            for key in ('from', 'to'):
                if message[key] == 'a':
                    message[key] = 's'
        del names['a']
    used = {m[k] for m in messages for k in ('from', 'to')}
    names = {k: v for k, v in names.items() if k in used}
    origin = 130 if flow.get('system_trigger') else 80
    xs = {key: origin + i*290 for i, key in enumerate(names)}
    width, height = max(xs.values())+150, cursor+35
    page = E.Element('diagram', id=page_id, name=flow['title'])
    model = E.SubElement(page, 'mxGraphModel', grid='1', gridSize='10', page='1',
                         pageWidth=str(width), pageHeight=str(height), background='#FFFFFF')
    root = E.SubElement(model, 'root')
    E.SubElement(root, 'mxCell', id='0')
    E.SubElement(root, 'mxCell', id='1', parent='0')

    def vertex(id, value, x, y, w, h, style, parent='1'):
        cell = E.SubElement(root, 'mxCell', id=id, value=value, style=BASE+style,
                            parent=parent, vertex='1')
        E.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w),
                     height=str(h), attrib={'as': 'geometry'})

    def line(id, x1, y1, x2, y2):
        cell = E.SubElement(root, 'mxCell', id=id, value='', edge='1', parent='1',
                            style=BASE+'dashed=1;endArrow=none;')
        geo = E.SubElement(cell, 'mxGeometry', relative='1', attrib={'as': 'geometry'})
        for name, x, y in [('sourcePoint', x1, y1), ('targetPoint', x2, y2)]:
            E.SubElement(geo, 'mxPoint', x=str(x), y=str(y), attrib={'as': name})

    # Transparent frames sit behind lifelines; guards have their own row.
    for i, frame in enumerate(sorted(fragments, key=lambda f: f['depth'])):
        involved = {messages[n][key] for n in frame['indices'] for key in ('from', 'to')}
        if frame['depth'] == 0:
            left, right = 20, width-20
        else:
            left = min(xs[k] for k in involved)-95 + frame['depth']*5
            right = max(xs[k] for k in involved)+95 - frame['depth']*5
        vertex(f'fragment_{i}', frame['kind'], left, frame['top'], right-left,
               frame['bottom']-frame['top'],
               'shape=umlFrame;fillColor=none;pointerEvents=0;container=0;'
               'width=55;height=25;align=left;verticalAlign=top;spacingLeft=8;spacingTop=5;')
        guard_left = max(left+70, min(xs[k] for k in involved)+24) if involved else left+70
        for j, (y, guard) in enumerate(frame['guards']):
            vertex(f'fragment_{i}_guard{j}', escape(guard), guard_left, y, right-guard_left-15, 30,
                   'text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;')
        for j, y in enumerate(frame['dividers']):
            line(f'fragment_{i}_divider{j}', left, y, right, y)

    for key, label in names.items():
        if key == 'u':
            vertex(key, label, xs[key]-15, 45, 30, height-70,
                   'shape=umlLifeline;participant=umlActor;size=60;'
                   'perimeter=lifelinePerimeter;container=1;verticalAlign=bottom;spacingBottom=-20;')
        else:
            vertex(key, label, xs[key]-110, 55, 220, height-80,
                   'shape=umlLifeline;size=44;perimeter=lifelinePerimeter;'
                   'container=1;whiteSpace=wrap;')

    intervals = {key: [] for key in names}
    if flow.get('system_trigger'):
        intervals['s'].append((messages[0]['y'], messages[-1]['y']))
    # A caller can receive alternative replies in different operands. Its
    # execution covers the whole alternative, not only the first drawn reply.
    requests = [m for m in messages if not m.get('reply') and not m.get('async')]
    for m in requests:
        next_y = min((n['y'] for n in requests if n['from'] == m['from']
                      and n['to'] == m['to'] and n['y'] > m['y']), default=height)
        replies = [n['y'] for n in messages if n.get('reply')
                   and n['from'] == m['to'] and n['to'] == m['from']
                   and m['y'] < n['y'] < next_y]
        end = max(replies) if replies else messages[-1]['y']+10
        intervals[m['to']].append((m['y'], end))
    bars = {}
    for key, values in intervals.items():
        if key == 'u':
            continue
        merged = []
        for start, end in sorted(values):
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
            else:
                merged.append((start, max(start+12, end)))
        for n, (start, end) in enumerate(merged):
            id = f'activation_{key}_{n}'
            vertex(id, '', 106, start-55, 8, end-start, '', parent=key)
            bars[id] = (key, start, end)

    def anchor(key, y, right):
        for id, (owner, start, end) in bars.items():
            if key == owner and start <= y <= end:
                return id, (1 if right else 0), (y-start)/(end-start)
        top, h = (45, height-70) if key == 'u' else (55, height-80)
        return key, .5, (y-top)/h

    for m in messages:
        sender, receiver, y = m['from'], m['to'], m['y']
        source, ex, ey = anchor(sender, y, xs[receiver] > xs[sender])
        target, ix, iy = anchor(receiver, y, xs[sender] > xs[receiver])
        max_width = abs(xs[sender]-xs[receiver])-24
        # Wrap long operation labels instead of hiding arrowheads or shrinking text.
        label = f"{m['number']}: {m['label']}"
        wrapped = '<br>'.join(escape(t) for t in textwrap.wrap(label, max(26, int(max_width/6.6)),
                                                            break_long_words=False))
        arrow = ('dashed=1;endArrow=open;endFill=0;' if m.get('reply') else
                 'endArrow=open;endFill=0;' if m.get('async') else 'endArrow=block;endFill=1;')
        cell = E.SubElement(root, 'mxCell', id=f"m{m['number']}", value=wrapped,
                            edge='1', parent='1', source=source, target=target,
                            style=BASE+'edgeStyle=none;rounded=0;endSize=9;'+arrow+
                            'labelBackgroundColor=#FFFFFF;verticalAlign=bottom;spacingBottom=5;'
                            f'exitX={ex};exitY={ey};entryX={ix};entryY={iy};'
                            'exitPerimeter=0;entryPerimeter=0;')
        E.SubElement(cell, 'mxGeometry', relative='1', attrib={'as': 'geometry'})
    return page


def build():
    rows = []
    for group in GROUPS:
        folder = OUT / group['folder']
        folder.mkdir(exist_ok=True)
        file = folder / f"Sequence-Diagrams-{group['slug']}.drawio"
        mx = E.Element('mxfile', host='drawio', version='26.0.0')
        for i, flow in enumerate(group['flows'], 1):
            page = draw_page(flow, f"{group['folder']}-{i}")
            page.set('id', f"{group['folder']}-{i}")
            mx.append(page)
            png = f"{i:02d}-{flow['slug']}.png"
            rows.append((group, i, flow, file.relative_to(OUT).as_posix(), png))
        E.indent(mx, space='  ')
        E.ElementTree(mx).write(file, encoding='utf-8', xml_declaration=True)
        print(f"{group['folder']}: {len(group['flows'])} tabs")
    digest = hashlib.sha256(REPORT.read_bytes()).hexdigest()
    lines = [
        '# Sequence Diagrams — 8 nhóm Authentication đến Administration', '',
        'Mỗi folder có một file draw.io chính; mỗi tab là một sequence riêng. PNG được xuất theo tab.', '',
        f'Nguồn: `{REPORT.as_posix()}`, SHA256 `{digest}`. Nội dung theo III và IV của snapshot này; '
        'đối chiếu [Report III](../../report/03-software-requirements-specification.md), '
        '[Report IV](../../report/04-software-design-document.md) và '
        '[thiết kế class](../07-class/Class-Diagrams-design.md).', '',
        'Đây là thiết kế đề xuất để duyệt, không phải reverse-engineering hoặc xác nhận runtime. '
        'Operation có trên Class Diagram được dùng lại; nhãn hành vi chưa có operation được giữ ở mức khái niệm, '
        'không tự tạo endpoint, DTO hoặc HTTP status. Theo yêu cầu người dùng, mọi tương tác dữ liệu đi qua '
        'Repository: Service → Repository → Database, reply theo chiều ngược lại. Repository là phân tách trách nhiệm '
        'thiết kế của bộ sequence này, không khẳng định đã có trong BE hoặc Class Diagram hiện tại. '
        'Không đổi Class Diagram hay BE trong đợt sửa này.', '',
        'Email Code trong tab đầu Authentication và bản standalone dùng cùng model có Repository; giữ luồng nghiệp vụ đã duyệt. '
        'Không khung ngoài, nền trắng, actor bên trái, tên actor hạ cách chân, reply nét đứt về caller, guard có hàng riêng; '
        'không dùng activation lồng dài qua opt. Khổ preview theo nội dung, chưa chứng minh phù hợp in A4/Word.', '',
        '## Xử lý caption cũ và giới hạn', '',
        '- Caption Answer Gate được ánh xạ sang Answer Decision Inbox Item (FR-28–30).',
        '- Caption Accept/Send Back/Rerun được thể hiện bằng acceptance, revision và version mới; không mở lại accepted object để sửa.',
        '- Pause/Resume/Stop/Abandon dùng Cancel and Synchronize Run theo state model IV 3.4; không tạo state paused hoặc resurrect ended run.',
        '- Charter/Directives, Stage Outcome/Failure/Close Consultations và Endorse/Retry Consultation có tab riêng theo III 3.7.1–3.7.3; không đồng nhất với action policy hoặc tentative decision.',
        '- Reviewer Queue có tab riêng theo III 3.8.2 và SC-13; không đồng nhất với Decision Inbox. Các bước nội bộ là đề xuất thiết kế.',
        '- Execution và Paper thêm theo IV 3.5 (FE-09/10); Local Job thêm theo Figure IV-12. Experiment Design và Execution cùng đối chiếu Figure IV-10.',
        '- Các lựa chọn dùng alt riêng; không ghép Rename/Test/Delete thành một message có dấu /. Read không biến thành write, lỗi không rơi tiếp vào nhánh thành công.',
        '- Quyền project được kiểm tra trước khi đọc/ghi; Sign In/Invitation và Platform Admin dùng đúng scope. Admin project list chỉ trả metadata. Secret chỉ trả reference; không đưa khóa vào log/output.',
        '- Engine pages mô tả lifecycle dưới một request điều phối, không quy định giao thức HTTP chờ job hoàn thành. Run Start trả Run trước, stage chạy nền và kết quả theo dõi ở tab Monitor; event bất đồng bộ dùng đầu mở.',
        '- Handle Must-Ask và Receive Notifications bắt đầu từ event hệ thống trong context run/project đã được xác thực, không phụ thuộc user đang mở UI. UI chỉ nhận update khi connected và authorized; quyền trả lời được kiểm tra riêng trong tab answer/confirm.',
        '- Không thêm FE-18/19 sau MVP hoặc tự giải quyết các khác biệt requirement chưa được chốt. Placeholder Report7 và requirement gốc không sửa.', '',
        '## Tái tạo', '',
        '`python diagrams/08-sequence/build_sequence_groups.py` (Python stdlib). '
        'Nguồn flow: [sequence_flows.py](sequence_flows.py); layout: [builder](build_sequence_groups.py). '
        'Export PNG bằng draw.io CLI `-x -f png -s 2 -b 20 -p <tab 1-based> -o <PNG> <drawio>`.', '',
        'Ngoại lệ export: Execute Local Job and Release Aggregate, Hypothesis Stage, Independent Review and Revision Rounds, '
        'Execution Stage and Unseal Results dùng `-s 1` (100%). Các ảnh này bị cắt phần cuối khi native exporter xuất '
        'ở scale 2; scale 1 đã kiểm tra đủ nội dung. Giữ nguyên geometry/cỡ chữ trong editable.', '',
        '## Inventory', '',
        '| Nhóm / file | Tab | Sequence / PNG | Nguồn Report7 |',
        '|---|---:|---|---|',
    ]
    for g, i, f, file, png in rows:
        lines.append(f"| [{g['title']}]({file}) | {i} | [{f['title']}]({g['folder']}/{png}) | {f['source']} |")
    lines += ['', '## Validation', '',
              'Kết quả chạy thực tế ghi trong changelog. Validator XML/geometry không thay thế export và xem PNG. '
              'Chưa chèn vào Word, chưa kiểm tra in A4 hoặc runtime nghiệp vụ.', '']
    (OUT/'Sequence-Groups-design.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'{len(GROUPS)} groups; {len(rows)} sequence tabs')


if __name__ == '__main__':
    build()

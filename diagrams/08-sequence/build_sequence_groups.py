"""Build source-backed, editable sequence groups and an explicit inventory."""
from html import escape
from pathlib import Path
import hashlib
import re
import textwrap
import xml.etree.ElementTree as E
from sequence_flows import GROUPS

OUT = Path(__file__).resolve().parent
REPORT = Path('C:/Users/ADMIN/Downloads/FA26SE115_Report7 (1).md')
BASE = ('html=1;fontFamily=Arial;fontSize=12;fontColor=#000000;'
        'strokeColor=#000000;strokeWidth=1;fillColor=#FFFFFF;')
# Vertical spacing (px). NORMAL is the original layout; a tab that would exceed one
# A4 portrait page (A4_RATIO) falls back to COMPACT.
NORMAL = dict(ROW=54, LINE=15, GUARD=70, FRAME_TOP=26, FRAME_BOTTOM=48, DIVIDER=12, OPERAND_END=10)
COMPACT = dict(ROW=32, LINE=15, GUARD=38, FRAME_TOP=16, FRAME_BOTTOM=26, DIVIDER=4, OPERAND_END=2)
GAP = 290         # distance between lifelines


def flatten(items):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


WRITE_VERBS = {'accept', 'add', 'append', 'apply', 'archive', 'ask', 'block', 'build', 'cancel',
               'change', 'close', 'complete', 'confirm', 'consume', 'create', 'decline', 'delete',
               'disclose', 'draft', 'end', 'grant', 'import', 'invite', 'issue', 'keep', 'lift',
               'mark', 'overturn', 'persist', 'pin', 'publish', 'queue', 'record', 'register',
               'remove', 'rename', 'resend', 'revoke', 'save', 'set', 'store', 'transfer',
               'update', 'write'}


def database_label(service_label):
    """One unambiguous Repository -> Database action instead of a combined read/write label.
    A clause writes when its leading verb writes ("Query append-only audit" only reads)."""
    for clause in re.split(r';| and ', service_label):
        verb = re.match(r'\s*([A-Za-z][a-z]*)', clause)
        if verb and verb.group(1).lower() in WRITE_VERBS:
            return 'Write records'
    return 'Query records'


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
                           {**item, 'from': 'repo', 'label': database_label(item['label'])}])
        elif item.get('from') == 'd' and item.get('reply'):
            result.extend([{**item, 'to': 'repo'}, {**item, 'from': 'repo'}])
        else:
            result.append(item)
    return result


def rejection(guard):
    reason = guard.strip('[]').removeprefix('else: ')
    return [{'from': 's', 'to': 'c', 'label': f'Rejected: {reason}', 'reply': True},
            {'from': 'c', 'to': 'w', 'label': 'Domain validation error', 'reply': True},
            {'from': 'w', 'to': 'u', 'label': 'Show error message', 'reply': True}]


def distribute(items, success):
    """Return the result inside every operand of a final alt, so an error branch never
    ends empty and never falls through to the success reply (rule.md, Fragment và luồng lỗi)."""
    items = flatten(items)
    last = items[-1] if items else {}
    if 'branches' not in last or last.get('kind', 'alt') != 'alt':
        return items + success
    return items[:-1] + [{**last, 'branches': [
        (guard, distribute(body, success) if flatten(body) else rejection(guard))
        for guard, body in last['branches']]}]


def interaction(flow):
    """Return (participants, interaction tree) for one flow; shared by builder and review checks."""
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
    def completion(to='s', result=None, display=None):
        if flow.get('terminal_branches'):
            return []
        return [
            {'from': to, 'to': 'c', 'label': result or flow.get('result', 'Operation result'), 'reply': True},
            {'from': 'c', 'to': 'w', 'label': 'Result or domain validation error', 'reply': True},
            {'from': 'w', 'to': 'u', 'label': display or flow.get('display', 'Show result or error'), 'reply': True},
        ]

    def run_part(operation, steps, to='s', result=None, display=None):
        main = [{'from': 'c', 'to': to, 'label': operation},
                *distribute(steps, completion(to, result, display))]
        if not prelude:
            return main
        return [{'branches': [
            ('[access denied or session invalid]', [
                {'from': 'c', 'to': 'w', 'label': 'Access rejected', 'reply': True},
                {'from': 'w', 'to': 'u', 'label': 'Show unavailable or sign-in required', 'reply': True}]),
            ('[else: access allowed]', main)]}]

    main = run_part(flow['operation'], flow['steps'])[-1]['branches'][1][1] if prelude else         run_part(flow['operation'], flow['steps'])
    tree = [
        {'from': 'u', 'to': 'w', 'label': flow['trigger']},
        {'from': 'w', 'to': 'c', 'label': flow.get('entry', flow['operation'])},
        *prelude, *run_part(flow['operation'], flow['steps']),
    ]
    if flow.get('choices'):
        # One operand per user choice; each calls its own controller and service operation.
        tree = [{'from': 'u', 'to': 'w', 'label': flow['trigger']}, {'branches': [
            (ch['guard'], [{'from': 'w', 'to': 'c', 'label': ch['entry']}, *prelude,
                           *run_part(ch['operation'], ch.get('steps', []), ch.get('to', 's'),
                                     ch.get('result'), ch.get('display'))])
            for ch in flow['choices']]}]
    if flow.get('google_consent'):
        tree = [
            {'from': 'u', 'to': 'w', 'label': 'Choose Sign in with Google'},
            {'from': 'w', 'to': 'g', 'label': 'authorize(clientId, scope)'},
            {'from': 'g', 'to': 'w', 'label': 'Authorization callback: code or denial', 'reply': True},
            {'branches': [
                ('[consent denied]', [{'from': 'w', 'to': 'u', 'label': 'Show sign-in cancelled', 'reply': True}]),
                ('[authorization code returned]', [
                    {'from': 'w', 'to': 'c', 'label': 'signInWithGoogle(code)'}, *main])]},
        ]
    if flow.get('system_trigger'):
        # The actor stays leftmost; the system trigger lifeline comes right after it.
        names = {'u': names['u'], 't': flow['system_trigger'], **names}
        tree = [
            {'from': 't', 'to': 's', 'label': flow['operation'], 'async': True},
            *flatten(flow['steps']),
            {'kind': 'opt', 'guard': '[user connected and authorized]', 'body': [
                {'from': 's', 'to': 'c', 'label': 'pushUpdate(event)', 'async': True},
                {'from': 'c', 'to': 'w', 'label': 'Deliver in-app update', 'async': True},
                {'from': 'w', 'to': 'u', 'label': flow.get('display', 'Show notification and decision status'),
                 'async': True}]},
        ]
    if flow.get('custom_tree'):
        tree = flow['custom_tree']
    return names, repository_interactions(tree)


def walk(items):
    for item in flatten(items):
        if 'branches' in item:
            for _, body in item['branches']:
                yield from walk(body)
        elif 'body' in item:
            yield from walk(item['body'])
        else:
            yield item


def wrap_label(text, sender, receiver, xs):
    width = abs(xs[sender] - xs[receiver]) - 24
    return textwrap.wrap(text, max(26, int(width / 6.6)), break_long_words=False)


def draw_page(flow, page_id, gap=GAP, sp=NORMAL):
    names, tree = interaction(flow)
    if names.get('a') == names.get('s'):
        for message in walk(tree):
            for key in ('from', 'to'):
                if message[key] == 'a':
                    message[key] = 's'
        del names['a']
    used = {m[k] for m in walk(tree) for k in ('from', 'to')}
    names = {k: v for k, v in names.items() if k in used}
    # An actor figure is narrow; a box lifeline (system trigger first) needs more room.
    origin = 80 if next(iter(names), None) == 'u' else 130
    xs = {key: origin + i*gap for i, key in enumerate(names)}
    messages, fragments = [], []
    cursor = 150

    def layout(items, depth=0):
        nonlocal cursor
        for item in flatten(items):
            if 'branches' in item or item.get('kind') in ('loop', 'opt', 'par'):
                start = cursor
                cursor += sp['FRAME_TOP']
                branch_data = item.get('branches', [(item['guard'], item['body'])]) if 'branches' not in item else item['branches']
                guards, dividers = [], []
                indices = []
                for i, (guard, body) in enumerate(branch_data):
                    if i:
                        dividers.append(cursor)
                        cursor += sp['DIVIDER']
                    guards.append((cursor, guard))
                    cursor += sp['GUARD']
                    before = len(messages)
                    layout(body, depth+1)
                    indices.extend(range(before, len(messages)))
                    cursor += sp['OPERAND_END']
                fragments.append({'kind': item.get('kind', 'alt'), 'top': start,
                                  'bottom': cursor, 'guards': guards, 'dividers': dividers,
                                  'indices': indices, 'depth': depth})
                cursor += sp['FRAME_BOTTOM']
            else:
                number = len(messages) + 1
                lines = wrap_label(f"{number}: {item['label']}", item['from'], item['to'], xs)
                cursor += sp['LINE'] * (len(lines) - 1)   # room for a wrapped label above its arrow
                messages.append({**item, 'y': cursor, 'number': number, 'lines': lines})
                cursor += sp['ROW']
    layout(tree)
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
            # Nested frames stay inside the outer frame (20 .. width-20).
            left = max(20 + frame['depth']*8, min(xs[k] for k in involved)-95 + frame['depth']*5)
            right = min(width-20 - frame['depth']*8, max(xs[k] for k in involved)+95 - frame['depth']*5)
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
        # Wrap long operation labels instead of hiding arrowheads or shrinking text.
        wrapped = '<br>'.join(escape(t) for t in m['lines'])
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


A4_RATIO = 1.41  # height / width of an A4 portrait page; every tab must fit one page


def ratio(page):
    model = page.find('mxGraphModel')
    return int(model.get('pageHeight')) / int(model.get('pageWidth'))


def tabs(group):
    """Pages of one group in report order: (report index, flow, page, PNG name); one page per flow."""
    out = []
    for i, flow in enumerate(group['flows'], 1):
        page_id = f"{group['folder']}-{i}"
        page = draw_page(flow, page_id)
        if ratio(page) > A4_RATIO:
            # Only a tab taller than A4 is compacted, then widened (fewer wrapped labels) until it fits.
            for gap in range(GAP, 481, 10):
                page = draw_page(flow, page_id, gap, COMPACT)
                if ratio(page) <= A4_RATIO:
                    break
        out.append((i, flow, page, f"{i:02d}-{flow['slug']}.png"))
    return out


def build():
    rows = []
    for group in GROUPS:
        folder = OUT / group['folder']
        folder.mkdir(exist_ok=True)
        file = folder / f"Sequence-Diagrams-{group['slug']}.drawio"
        mx = E.Element('mxfile', host='drawio', version='26.0.0')
        for i, flow, page, png in tabs(group):
            mx.append(page)
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
        '- Không thêm FE-18/19/20 sau MVP hoặc tự giải quyết các khác biệt requirement chưa được chốt. Placeholder Report7 và requirement gốc không sửa.',
        '- Bổ sung 2026-11-03 theo `C:/Users/ADMIN/Downloads/FA26SE115_Report7 (3).md` (Phần III đã tái cấu trúc ở bản (2)): '
        'Pair a Local Node, Handle an Offline or Revoked Local Node, Approve Additional Spending, Review and Approve a Research Dossier, '
        'Export a Research Dossier. Cột nguồn của các tab này ghi "Report7 (3)"; các tab khác vẫn theo snapshot hash bên trên. '
        'Local Node và Dossier là thiết kế đề xuất, chưa có bảng tương ứng trong Database Design của report.',
        '- Execution Stage dùng thuật ngữ disclosure của Report7 (2)/(3) thay cho unseal/envelope; nội dung luồng không đổi.',
        '- Rà soát 2026-11-03 theo rule.md: Repository → Database ghi `Query records` hoặc `Write records` theo động từ đầu mệnh đề, '
        'không còn nhãn ghép "Read / persist"; mỗi operand lỗi của `alt` cuối trả lỗi riêng về UI thay cho operand rỗng; '
        'ghi log quyết định chỉ còn trong nhánh thành công (Accept/Revise/Rerun, Confirm/Overturn). '
        'Các stage engine, Independent Review và Execute Local Job bắt đầu từ trigger hệ thống, khớp Start Research Run, FR-14, FR-71.',
        '- Bổ sung 2026-11-03 (phương án a: FE-18/19/20 giữ sau MVP, không vẽ): 5 tab cho use case Must chưa có sequence — '
        'Amend a Research Case (UC-28), Build Literature Base (UC-38), Lock an Analysis Plan and Request a Deviation (UC-40), '
        'Triage Exploration Candidates (UC-43), Run Reviewer Benchmark (UC-65). Slot IV giả định report đã áp FIX-01…FIX-19.',
        '- Đồng bộ class 2026-11-03: mọi message gọi vào controller/service là operation có trong [class model](../07-class/class_model.py). '
        'Tab có nhiều lựa chọn dùng `choices`: mỗi operand gọi operation riêng của controller và service. Luồng hệ thống đẩy cập nhật bằng `pushUpdate(event)`. '
        'Tab sắp theo số mục IV 3.x.y nên PNG số n ứng với mục 3.x.(n+1). Đổi tên: Answer Gate, Accept Send Back or Rerun Stage, Experiment Design Stage, '
        'View Decision Inbox, Manage Project Integrations and Notification Preferences; AI PI thêm slot 3.6.7–3.6.9, Decision Inbox là 3.7.6.',
        '- Vừa trang A4 2026-11-03: mỗi sequence là một hình duy nhất, tỉ lệ cao/rộng ≤ 1.41 (A4 dọc). '
        'Sequence vừa A4 giữ khoảng dòng gốc (message 54 px, guard 70 px, viền fragment 26/48 px); chỉ 22 tab vượt A4 mới nén '
        '(message 32 px, guard 38 px, viền fragment 16/26 px), vẫn vượt thì giãn khoảng cách lifeline (290 → tối đa 480 px). Nhãn dài xuống dòng (+15 px mỗi dòng); '
        'không tách hình, không bỏ nhánh. Update/Archive/Complete gộp lưu và ghi audit thành một lần ghi.', '',
        '## Tái tạo', '',
        '`python diagrams/08-sequence/build_sequence_groups.py` (Python stdlib). '
        'Nguồn flow: [sequence_flows.py](sequence_flows.py); layout: [builder](build_sequence_groups.py). '
        'Export PNG bằng draw.io CLI `-x -f png -s 2 -b 20 -p <tab 1-based> -o <PNG> <drawio>`.', '',
        'Ngoại lệ export: tab có `pageHeight` lớn hơn 2700 px dùng `-s 1` (100%), vì native exporter cắt phần cuối '
        'khi xuất trang dài ở scale 2; các tab còn lại dùng `-s 2`. Kiểm tra trực quan đến message cuối. '
        'Giữ nguyên geometry/cỡ chữ trong editable.', '',
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

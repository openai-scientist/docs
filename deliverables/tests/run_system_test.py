"""System test round against the local stack (docker compose dev, API on :8080).

usage: run_system_test.py OUT.json
Each case runs real HTTP calls and records Passed/Failed with what the server answered.
Sign-in codes are read from the management log (the local email sender writes mail to the log).
"""
import io
import json
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime

import requests

API = 'http://127.0.0.1:8080/api/v1'
ORIGIN = 'http://localhost:3000'
TAG = uuid.uuid4().hex[:6]
CASES, RESULTS = [], []


def case(cid, feature, function, desc, procedure, expected, pre):
    def wrap(fn):
        CASES.append(dict(id=cid, feature=feature, function=function, desc=desc, procedure=procedure,
                          expected=expected, pre=pre, fn=fn))
        return fn
    return wrap


class User:
    def __init__(self, email):
        self.email, self.s, self.csrf = email, requests.Session(), None
        self.s.headers['Origin'] = ORIGIN

    def call(self, method, path, **kw):
        h = kw.pop('headers', {})
        if self.csrf and method != 'GET':
            h['X-CSRF-Token'] = self.csrf
        return self.s.request(method, API + path, headers=h, timeout=60, **kw)

    def start(self):
        return self.call('POST', '/auth/email/start', json={'email': self.email})

    def sign_in(self):
        # within the resend cooldown or the hourly per-email code cap no new code is sent, so keep
        # asking for up to 70 minutes (the cap window) before giving up
        deadline = time.time() + 70 * 60
        while time.time() < deadline:
            st = self.start()
            if st.status_code == 429:  # the sign-in rate limit of the test machine, not a result
                time.sleep(int(st.headers.get('Retry-After', 20)))
                continue
            try:
                r = self.verify(code_for(self.email, tries=10))
            except RuntimeError:
                time.sleep(60)
                continue
            if r.ok:
                return r
            time.sleep(60)
        raise RuntimeError(f'could not sign in {self.email}')

    def verify(self, code):
        r = self.call('POST', '/auth/email/verify', json={'email': self.email, 'code': code})
        if r.ok:
            self.csrf = self.call('GET', '/auth/csrf-token').json()['data'].get('csrf_token')
        return r


def code_for(email, tries=20):
    for _ in range(tries):
        log = subprocess.run(['docker', 'logs', '--since', '75m', 'logos-management-1'], capture_output=True, text=True)
        text = log.stdout + log.stderr
        hits = [m.end() for m in re.finditer(re.escape(f'to {email}'), text)]
        if hits:
            m = re.search(r'\b(\d{6})\b', text[hits[-1]:hits[-1] + 1500])
            if m:
                return m.group(1)
        time.sleep(0.5)
    raise RuntimeError(f'no code in the log for {email}')


def data(r):
    return r.json().get('data')


def expect(r, *codes):
    ok = r.status_code in codes
    return ok, f'HTTP {r.status_code}' + ('' if ok else f' {r.text[:160]}')


CSV = b'id,group,age,score\n' + b''.join(f'{i},{"ab"[i % 2]},{20 + i % 30},{i * 1.5}\n'.encode() for i in range(1, 61))
ctx = {}
pm = User(f'pm.{TAG}@example.com')
rs = User(f'researcher.{TAG}@example.com')
out = User(f'outsider.{TAG}@example.com')
admin = User('admin@example.com')

# ---------------- Authentication & Account
F_AUTH = 'Authentication & Account'


@case('ST-AUTH-01', F_AUTH, 'Sign in with email code', 'Start sign-in for a new email address',
      '1. POST /auth/email/start with a new email', 'Answer 200; a 6-digit code and link are emailed', 'Email address has no account')
def _():
    r = pm.start()
    ok, note = expect(r, 200)
    return ok and bool(code_for(pm.email)), note + ', code found in mail log'


@case('ST-AUTH-02', F_AUTH, 'Sign in with email code', 'Sign in with a wrong code',
      '1. POST /auth/email/verify with code 000000', 'Request refused; no session', 'Sign-in started')
def _():
    r = pm.verify('000000')
    return expect(r, 400, 401, 422)


@case('ST-AUTH-03', F_AUTH, 'Sign in with email code', 'Sign in with the emailed code',
      '1. Read the code from the email\n2. POST /auth/email/verify\n3. GET /auth/me',
      'Session opens; /auth/me returns the user; no password asked', 'Sign-in started')
def _():
    r = pm.verify(code_for(pm.email))
    me = pm.call('GET', '/auth/me')
    return r.ok and me.ok and data(me)['user']['email'] == pm.email, f'verify HTTP {r.status_code}, me HTTP {me.status_code}'


@case('ST-AUTH-04', F_AUTH, 'Sign in with email code', 'Reuse a code that was already used',
      '1. POST /auth/email/verify again with the same code', 'Request refused', 'Code used once')
def _():
    u = User(pm.email)
    return expect(u.verify(code_for(pm.email)), 400, 401, 422)


@case('ST-AUTH-05', F_AUTH, 'Sign in with email code', 'Start sign-in from a site that is not allowed',
      '1. POST /auth/email/start with Origin http://evil.example', 'Request refused (403)', 'None')
def _():
    r = requests.post(API + '/auth/email/start', json={'email': f'x.{TAG}@example.com'},
                      headers={'Origin': 'http://evil.example'}, timeout=30)
    return expect(r, 403)


@case('ST-AUTH-06', F_AUTH, 'Session', 'Open the profile without a session',
      '1. GET /auth/me without cookie', 'Request refused (401)', 'Not signed in')
def _():
    return expect(requests.get(API + '/auth/me', timeout=30), 401)


@case('ST-AUTH-07', F_AUTH, 'Complete onboarding and update profile', 'Set the display name',
      '1. PATCH /auth/me with display_name\n2. GET /auth/me', 'Name saved and returned', 'Signed in')
def _():
    r = pm.call('PATCH', '/auth/me', json={'display_name': 'Test Manager'})
    me = data(pm.call('GET', '/auth/me'))['user']
    return r.ok and me.get('display_name') == 'Test Manager', f'HTTP {r.status_code}'


@case('ST-AUTH-08', F_AUTH, 'Sign out', 'Sign out ends the session',
      '1. Sign in a second browser session\n2. POST /auth/logout\n3. GET /auth/me', '/auth/me answers 401 after logout', 'Signed in')
def _():
    u = User(f'logout.{TAG}@example.com')
    u.sign_in()
    r = u.call('POST', '/auth/logout')
    me = u.call('GET', '/auth/me')
    return r.ok and me.status_code == 401, f'logout HTTP {r.status_code}, me HTTP {me.status_code}'


# ---------------- Project Workspace
F_PRJ = 'Project Workspace'


@case('ST-PRJ-01', F_PRJ, 'Create project', 'Create a project',
      '1. POST /projects with name, description, domain', 'Project created; creator is Project Manager', 'Signed in')
def _():
    rs.sign_in(); out.sign_in()
    r = pm.call('POST', '/projects', json={'name': f'System test {TAG}', 'description': 'Round 1', 'domain': 'health'})
    if r.ok:
        ctx['pid'] = data(r)['id']
    return expect(r, 200, 201)


@case('ST-PRJ-02', F_PRJ, 'Create project', 'Create a project without a name',
      '1. POST /projects with empty name', 'Validation error (422)', 'Signed in')
def _():
    return expect(pm.call('POST', '/projects', json={'name': ''}), 422)


@case('ST-PRJ-03', F_PRJ, 'View project list and overview', 'A user sees only own projects',
      '1. As outsider GET /projects', 'The new project is not listed', 'Project exists')
def _():
    r = out.call('GET', '/projects')
    ids = [p['id'] for p in (data(r) or [])] if r.ok else []
    return r.ok and ctx['pid'] not in ids, f'HTTP {r.status_code}, {len(ids)} projects'


@case('ST-PRJ-04', F_PRJ, 'View project list and overview', 'A non-member opens a project',
      '1. As outsider GET /projects/{id}', 'Refused (403/404); nothing revealed', 'Project exists')
def _():
    return expect(out.call('GET', f"/projects/{ctx['pid']}"), 403, 404)


@case('ST-PRJ-05', F_PRJ, 'Manage members and invitations', 'Invite a member as Researcher',
      '1. POST /projects/{id}/members with email and role researcher\n2. GET members', 'Invitation saved as pending', 'Signed in as Project Manager')
def _():
    r = pm.call('POST', f"/projects/{ctx['pid']}/members", json={'email': rs.email, 'role': 'researcher'})
    if r.ok:
        ctx['mid'] = data(r)['id']
    return expect(r, 200, 201)


@case('ST-PRJ-06', F_PRJ, 'Manage members and invitations', 'Invite with a role that does not exist',
      '1. POST members with role owner', 'Validation error (422)', 'Signed in as Project Manager')
def _():
    return expect(pm.call('POST', f"/projects/{ctx['pid']}/members", json={'email': out.email, 'role': 'owner'}), 422)


@case('ST-PRJ-07', F_PRJ, 'Accept or decline invitation', 'Invitee accepts the invitation',
      '1. As invitee list invitations\n2. Accept the invitation\n3. GET the project', 'Invitee becomes a member and opens the project', 'Invitation pending')
def _():
    inv = rs.call('GET', '/invitations')
    items = data(inv) or [] if inv.ok else []
    mine = [i for i in items if i.get('project_id') == ctx['pid'] or i.get('project', {}).get('id') == ctx['pid']]
    if not mine:
        return False, f'invitations HTTP {inv.status_code}, none for the project'
    a = rs.call('POST', f"/invitations/{mine[0]['id']}/accept")
    g = rs.call('GET', f"/projects/{ctx['pid']}")
    return a.ok and g.ok, f'accept HTTP {a.status_code}, project HTTP {g.status_code}'


@case('ST-PRJ-08', F_PRJ, 'Configure project settings', 'Read defaults and save one section',
      '1. GET /projects/{id}/settings\n2. PATCH settings/{section} with the version', 'Section saved; version increases', 'Signed in as Project Manager')
def _():
    g = pm.call('GET', f"/projects/{ctx['pid']}/settings")
    snap = data(g)
    ctx['settings'] = snap
    sec = next(iter(snap['sections'])) if isinstance(snap.get('sections'), dict) else None
    if not sec:
        return False, f'settings shape: {list(snap)[:6]}'
    sec = 'general'
    tz = 'UTC' if snap['sections'][sec].get('timezone') != 'UTC' else 'Asia/Bangkok'
    values = dict(snap['sections'][sec], timezone=tz)
    p = pm.call('PATCH', f"/projects/{ctx['pid']}/settings/{sec}", json={'version': snap['version'], 'values': values})
    ctx['sec'] = sec
    new = (data(p) or {}).get('version')
    return p.ok and new == snap['version'] + 1, f"HTTP {p.status_code}, version {snap['version']}->{new}"


@case('ST-PRJ-09', F_PRJ, 'Configure project settings', 'Save with a stale version',
      '1. PATCH settings with the old version number', 'Conflict (409); old values kept', 'Settings saved once')
def _():
    snap, sec = ctx['settings'], ctx['sec']
    body = snap['sections'][sec]
    return expect(pm.call('PATCH', f"/projects/{ctx['pid']}/settings/{sec}",
                          json={'version': snap['version'], 'values': body.get('values', body)}), 409)


@case('ST-PRJ-10', F_PRJ, 'Configure project settings', 'A Researcher tries to change settings',
      '1. As Researcher PATCH settings', 'Refused (403)', 'Researcher is a member')
def _():
    snap = data(rs.call('GET', f"/projects/{ctx['pid']}/settings")) or ctx['settings']
    sec = ctx['sec']
    body = snap['sections'][sec]
    return expect(rs.call('PATCH', f"/projects/{ctx['pid']}/settings/{sec}",
                          json={'version': snap['version'], 'values': body.get('values', body)}), 403)


@case('ST-PRJ-11', F_PRJ, 'View project activity and audit log', 'Changes appear in the activity log',
      '1. GET /projects/{id}/activity', 'Entries for project creation, invitation and settings', 'Changes made')
def _():
    r = pm.call('GET', f"/projects/{ctx['pid']}/activity")
    n = len(data(r) or []) if r.ok else 0
    return r.ok and n >= 2, f'HTTP {r.status_code}, {n} entries'


# ---------------- Data Management
F_DS = 'Data Management'


@case('ST-DS-01', F_DS, 'Upload dataset', 'Upload a valid CSV file',
      '1. POST /projects/{id}/datasets with name and a 60-row CSV', 'Dataset and version 1 created', 'Signed in as Researcher')
def _():
    r = rs.call('POST', f"/projects/{ctx['pid']}/datasets", data={'name': f'patients-{TAG}'},
                files={'file': ('patients.csv', io.BytesIO(CSV), 'text/csv')})
    if r.ok:
        d = data(r)
        ctx['did'] = d.get('id') or d.get('dataset', {}).get('id')
    return expect(r, 200, 201)


@case('ST-DS-02', F_DS, 'Upload dataset', 'Upload a file in an unsupported format',
      '1. POST datasets with a binary .exe file', 'Upload refused; nothing stored', 'Signed in as Researcher')
def _():
    r = rs.call('POST', f"/projects/{ctx['pid']}/datasets", data={'name': f'bad-{TAG}'},
                files={'file': ('tool.exe', io.BytesIO(b'MZ\x90\x00' * 64), 'application/octet-stream')})
    return expect(r, 400, 415, 422)


@case('ST-DS-03', F_DS, 'Upload new dataset version', 'Upload a second version',
      '1. POST /datasets/{id}/versions with a new CSV\n2. GET versions', 'Two versions; version 1 unchanged', 'Dataset exists')
def _():
    r = rs.call('POST', f"/projects/{ctx['pid']}/datasets/{ctx['did']}/versions",
                files={'file': ('patients-v2.csv', io.BytesIO(CSV + b'61,a,40,91.5\n'), 'text/csv')})
    v = rs.call('GET', f"/projects/{ctx['pid']}/datasets/{ctx['did']}/versions")
    vs = data(v) or []
    ctx['vid'] = vs[-1]['id'] if vs else None
    return r.ok and len(vs) >= 2, f'HTTP {r.status_code}, {len(vs)} versions'


@case('ST-DS-04', F_DS, 'View dataset detail', 'Preview a dataset version',
      '1. GET /datasets/{id}/versions/{v}/preview', 'Columns and first rows shown', 'Version exists')
def _():
    return expect(rs.call('GET', f"/projects/{ctx['pid']}/datasets/{ctx['did']}/versions/{ctx['vid']}/preview"), 200)


@case('ST-DS-05', F_DS, 'View dataset detail', 'Download a dataset version',
      '1. GET /versions/{v}/download', 'File downloads as attachment', 'Version exists')
def _():
    r = rs.call('GET', f"/projects/{ctx['pid']}/datasets/{ctx['did']}/versions/{ctx['vid']}/download")
    return r.ok and b'id,group' in r.content, f'HTTP {r.status_code}, {len(r.content)} bytes'


@case('ST-DS-06', F_DS, 'Upload dataset', 'A non-member uploads a dataset',
      '1. As outsider POST datasets', 'Refused (403/404)', 'Project exists')
def _():
    return expect(out.call('POST', f"/projects/{ctx['pid']}/datasets", data={'name': 'outsider-data'},
                           files={'file': ('a.csv', io.BytesIO(CSV), 'text/csv')}), 403, 404)


@case('ST-DS-07', F_DS, 'Rename or delete dataset', 'Rename a dataset',
      '1. PATCH /datasets/{id} with a new name', 'Name saved', 'Dataset exists')
def _():
    return expect(rs.call('PATCH', f"/projects/{ctx['pid']}/datasets/{ctx['did']}", json={'name': f'patients-renamed-{TAG}'}), 200)


# ---------------- Data connections and integrations
F_CN = 'Data Connections & Integrations'


@case('ST-CN-01', F_CN, 'Manage data connection and import', 'Connect to a reachable PostgreSQL',
      '1. POST /connections kind postgres, host db, valid credentials', 'Connection tested and saved', 'Project Manager; local PostgreSQL running')
def _():
    r = pm.call('POST', f"/projects/{ctx['pid']}/connections", json={
        'name': f'local-pg-{TAG}', 'kind': 'postgres',
        'config': {'host': 'db', 'port': 5432, 'database': 'platform', 'username': 'platform', 'ssl': 'disable'},
        'secret': {'password': 'platform-local-only'}})
    if r.ok:
        ctx['cid'] = data(r)['id']
    return expect(r, 200, 201)


@case('ST-CN-02', F_CN, 'Manage data connection and import', 'Connect with a wrong password',
      '1. POST /connections with a wrong password', 'Error shown; nothing saved', 'Project Manager')
def _():
    before = len(data(pm.call('GET', f"/projects/{ctx['pid']}/connections")) or [])
    r = pm.call('POST', f"/projects/{ctx['pid']}/connections", json={
        'name': f'bad-pg-{TAG}', 'kind': 'postgres',
        'config': {'host': 'db', 'port': 5432, 'database': 'postgres', 'username': 'platform', 'ssl': 'disable'},
        'secret': {'password': 'wrong'}})
    after = len(data(pm.call('GET', f"/projects/{ctx['pid']}/connections")) or [])
    return (not r.ok) and after == before, f'HTTP {r.status_code}, connections {before}->{after}'


@case('ST-CN-03', F_CN, 'Manage data connection and import', 'Paste text into the host field',
      '1. POST /connections with host "db; DROP TABLE x"', 'Validation error; nothing saved', 'Project Manager')
def _():
    r = pm.call('POST', f"/projects/{ctx['pid']}/connections", json={
        'name': f'paste-{TAG}', 'kind': 'postgres',
        'config': {'host': 'db; DROP TABLE x', 'database': 'platform', 'username': 'platform'},
        'secret': {'password': 'x'}})
    return expect(r, 400, 422)


@case('ST-CN-04', F_CN, 'Manage data connection and import', 'Browse tables of a connection',
      '1. GET /connections/{id}/tables', 'Tables of the source listed', 'Connection saved')
def _():
    return expect(pm.call('GET', f"/projects/{ctx['pid']}/connections/{ctx['cid']}/tables", params={'schema': 'public'}), 200)


@case('ST-CN-05', F_CN, 'Manage data connection and import', 'The response never shows the password',
      '1. GET /connections/{id}\n2. Search the body for the password', 'Password not in any response', 'Connection saved')
def _():
    r = pm.call('GET', f"/projects/{ctx['pid']}/connections/{ctx['cid']}")
    return r.ok and 'platform-local-only' not in r.text, f'HTTP {r.status_code}'


@case('ST-CN-06', F_CN, 'Manage project integrations', 'Add a Slack webhook',
      '1. POST /integrations provider slack with a hooks.slack.com URL', 'Integration saved', 'Project Manager')
def _():
    r = pm.call('POST', f"/projects/{ctx['pid']}/integrations", json={
        'provider': 'slack', 'name': 'Team channel', 'webhook_url': 'https://hooks.slack.com/services/T000/B000/XXXXXXXX',
        'events': ['run.finished'], 'enabled': False})
    return expect(r, 200, 201)


@case('ST-CN-07', F_CN, 'Manage project integrations', 'Add a webhook to an unknown host',
      '1. POST /integrations with https://evil.example/hook', 'Validation error (422)', 'Project Manager')
def _():
    r = pm.call('POST', f"/projects/{ctx['pid']}/integrations", json={
        'provider': 'slack', 'name': 'Bad', 'webhook_url': 'https://evil.example/hook', 'events': ['run.completed']})
    return expect(r, 400, 422)


@case('ST-CN-08', F_CN, 'Manage data connection and import', 'Delete a connection',
      '1. DELETE /connections/{id}', 'Connection removed', 'Connection saved')
def _():
    return expect(pm.call('DELETE', f"/projects/{ctx['pid']}/connections/{ctx['cid']}"), 200, 204)


# ---------------- Local Node
F_LN = 'Local Node'


@case('ST-LN-01', F_LN, 'Pair a Local Node', 'Create a runner and read its token once',
      '1. POST /runners with a name\n2. GET /runners', 'Token returned once; list does not show it', 'Project Manager')
def _():
    r = pm.call('POST', f"/projects/{ctx['pid']}/runners", json={'name': f'lab-pc-{TAG}'})
    d = data(r) or {}
    tok = d.get('token') or d.get('pairing_token')
    ctx['rid'] = (d.get('runner') or d).get('id')
    lst = pm.call('GET', f"/projects/{ctx['pid']}/runners")
    return r.ok and bool(tok) and tok not in lst.text, f'HTTP {r.status_code}, list HTTP {lst.status_code}'


@case('ST-LN-02', F_LN, 'Pair a Local Node', 'A non-member creates a runner',
      '1. As outsider POST /runners', 'Refused (403/404)', 'Project exists')
def _():
    return expect(out.call('POST', f"/projects/{ctx['pid']}/runners", json={'name': 'outsider-pc'}), 403, 404)


@case('ST-LN-03', F_LN, 'Pair a Local Node', 'Revoke a runner',
      '1. DELETE /runners/{id}', 'Runner revoked', 'Runner exists')
def _():
    return expect(pm.call('DELETE', f"/projects/{ctx['pid']}/runners/{ctx['rid']}"), 200, 204)


@case('ST-LN-04', F_LN, 'Pair a Local Node', 'Revoke an unknown runner',
      '1. DELETE /runners/{random id}', 'runner_not_found (404)', 'None')
def _():
    return expect(pm.call('DELETE', f"/projects/{ctx['pid']}/runners/{uuid.uuid4()}"), 404)


# ---------------- Research Run
F_RUN = 'Research Run Orchestration'
NO_MODEL = ('Pending: no LLM provider is configured on the local stack (/admin/models stage and review are null), '
            'so no run can start; needs a provider key set by the Platform Admin')


@case('ST-RUN-01', F_RUN, 'Start research run', 'Start a run with an invalid intent',
      '1. POST /runs with intent kind "guess"', 'Validation error (422)', 'Researcher; dataset exists')
def _():
    return expect(rs.call('POST', f"/projects/{ctx['pid']}/runs", json={'intent': {'kind': 'guess', 'text': 'x'}}), 422)


@case('ST-RUN-02', F_RUN, 'Start research run', 'Start a run before the Platform Admin set the models',
      '1. POST /runs with intent explore_dataset and the dataset version',
      'Refused (409 MODELS_NOT_CONFIGURED); no run created', 'Researcher; dataset exists; no stage or review model set')
def _():
    r = rs.call('POST', f"/projects/{ctx['pid']}/runs", json={
        'intent': {'kind': 'explore_dataset', 'text': 'Which factors relate to the score?'},
        'dataset_version_id': ctx['vid'], 'review_mode': 'light'})
    runs = data(rs.call('GET', f"/projects/{ctx['pid']}/runs")) or []
    code = (r.json().get('error') or {}).get('code')
    return r.status_code == 409 and code == 'MODELS_NOT_CONFIGURED' and not runs, f'HTTP {r.status_code} {code}, {len(runs)} runs'


def pending(cid, function, desc, procedure, expected, pre):
    case(cid, F_RUN, function, desc, procedure, expected, pre)(lambda: (None, NO_MODEL))


pending('ST-RUN-03', 'Start research run', 'Start a run that explores a dataset',
        '1. POST /runs with intent explore_dataset and the dataset version\n2. GET the run',
        'Run created in state running; dataset stage starts', 'Models configured; no active run')
pending('ST-RUN-04', 'Start research run', 'Start a second run while one is active',
        '1. POST /runs again', 'Refused (409); one active run per project', 'A run is active')
pending('ST-RUN-05', 'Monitor run in Run Studio', 'Read the run, its stages and events',
        '1. GET /runs/{id}\n2. GET /runs/{id}/stages\n3. GET /runs/{id}/events', 'One run state; stages and events returned', 'Run exists')
pending('ST-RUN-06', 'Answer gate', 'Answer a gate of a stage',
        '1. Wait for a gate\n2. POST /stages/{s}/gates/{g} with an option', 'Gate closed; stage continues', 'Stage waits at a gate')
pending('ST-RUN-07', 'Accept, send back or rerun stage', 'Accept a stage and send a later stage back',
        '1. POST /stages/{s}/accept\n2. POST /stages/{s2}/send-back', 'Stage accepted; iteration 2 created', 'Stage completed')
pending('ST-RUN-08', 'Amend a research case', 'Amend the case with an empty reason',
        '1. POST /case/amendments with reason ""', 'Refused; case unchanged', 'Run exists')
pending('ST-RUN-09', 'Comment on run', 'Comment on a run',
        '1. POST /runs/{id}/comments\n2. GET comments', 'Comment saved and listed', 'Run exists')
pending('ST-RUN-10', 'Pause, resume, stop run', 'Stop the run',
        '1. POST /runs/{id}/stop with a reason\n2. GET the run', 'Run stopped; accepted objects kept', 'Run active')
pending('ST-RUN-11', 'Download and compare artifacts', 'Export an ended run',
        '1. GET /runs/{id}/artifacts/export', 'ZIP with every file and its hash', 'Run ended')


# ---------------- Notifications
F_NT = 'Notifications'


@case('ST-NT-01', F_NT, 'Notification preferences', 'Read and change own preferences',
      '1. GET notification-preferences/me\n2. PATCH with the version', 'Preferences saved', 'Member of the project')
def _():
    g = rs.call('GET', f"/projects/{ctx['pid']}/notification-preferences/me")
    v = (data(g) or {}).get('version')
    p = rs.call('PATCH', f"/projects/{ctx['pid']}/notification-preferences/me", json={'version': v, 'events': {'comments': {'in_app': False}}})
    return expect(p, 200)


@case('ST-NT-02', F_NT, 'View notifications', 'Read the unread count and mark all read',
      '1. GET /notifications/unread-count\n2. POST /notifications/read-all\n3. GET unread-count', 'Count is 0 after read-all', 'Signed in')
def _():
    a = rs.call('GET', '/notifications/unread-count')
    b = rs.call('POST', '/notifications/read-all')
    c = rs.call('GET', '/notifications/unread-count')
    n = (data(c) or {}).get('unread_count')
    return a.ok and b.ok and n == 0, f'{a.status_code}/{b.status_code}/{c.status_code}, count={n}'


# ---------------- Administration
F_AD = 'Administration'


@case('ST-AD-01', F_AD, 'Review health and operating metrics', 'Platform Admin opens the overview',
      '1. Sign in as admin@example.com\n2. GET /admin/overview', 'Overview returned', 'Default admin account')
def _():
    admin.sign_in()
    return expect(admin.call('GET', '/admin/overview'), 200)


@case('ST-AD-02', F_AD, 'Review health and operating metrics', 'A normal user opens the admin overview',
      '1. As Researcher GET /admin/overview', 'Refused (403)', 'Signed in')
def _():
    return expect(rs.call('GET', '/admin/overview'), 403)


@case('ST-AD-03', F_AD, 'View project metadata', 'Platform Admin reads project usage without content',
      '1. As admin GET /admin/usage/projects\n2. As admin GET a dataset of the project', 'Usage listed; dataset refused', 'Admin is not a member')
def _():
    a = admin.call('GET', '/admin/usage/projects')
    b = admin.call('GET', f"/projects/{ctx['pid']}/datasets/{ctx['did']}")
    return a.ok and b.status_code in (403, 404), f'usage {a.status_code}, dataset {b.status_code}'


@case('ST-AD-04', F_AD, 'Manage platform settings', 'Read the platform settings schema',
      '1. As admin GET /admin/settings and /admin/settings/schema', 'Settings and schema returned', 'Signed in as admin')
def _():
    a = admin.call('GET', '/admin/settings')
    b = admin.call('GET', '/admin/settings/schema')
    return a.ok and b.ok, f'{a.status_code}/{b.status_code}'


# ---------------- Project lifecycle (last: it changes the project)
@case('ST-PRJ-12', F_PRJ, 'Update, archive, complete project', 'Archive the project; it is read-only',
      '1. POST /archive\n2. PATCH a setting\n3. POST /restore', 'Change refused while archived; restore works', 'Project Manager')
def _():
    a = pm.call('POST', f"/projects/{ctx['pid']}/archive")
    snap = data(pm.call('GET', f"/projects/{ctx['pid']}/settings"))
    sec = ctx['sec']
    body = snap['sections'][sec]
    p = pm.call('PATCH', f"/projects/{ctx['pid']}/settings/{sec}", json={'version': snap['version'], 'values': body.get('values', body)})
    r = pm.call('POST', f"/projects/{ctx['pid']}/restore")
    return a.ok and p.status_code in (403, 409, 423) and r.ok, f'archive {a.status_code}, patch {p.status_code}, restore {r.status_code}'


@case('ST-PRJ-13', F_PRJ, 'Transfer ownership', 'Hand the project to an active member',
      '1. POST /transfer-ownership with the Researcher id', 'Owner changed', 'Researcher is an active member')
def _():
    me = data(rs.call('GET', '/auth/me'))['user']
    return expect(pm.call('POST', f"/projects/{ctx['pid']}/transfer-ownership", json={'new_owner_user_id': me['id']}), 200)


@case('ST-PRJ-14', F_PRJ, 'Delete project', 'Delete the project',
      '1. As new owner DELETE /projects/{id}\n2. GET the project', 'Project and its data removed', 'Caller is owner')
def _():
    d = rs.call('DELETE', f"/projects/{ctx['pid']}")
    g = rs.call('GET', f"/projects/{ctx['pid']}")
    return d.ok and g.status_code == 404, f'delete {d.status_code}, get {g.status_code}'


for c in CASES:
    try:
        ok, note = c['fn']()
    except Exception as exc:  # a broken step is a failed case, with the reason kept
        ok, note = False, f'{type(exc).__name__}: {exc}'[:200]
    res = 'Pending' if ok is None else 'Passed' if ok else 'Failed'
    RESULTS.append({k: v for k, v in c.items() if k != 'fn'} | {'result': res, 'note': note,
                                                                 'date': datetime.now().strftime('%Y-%m-%d')})
    print(f"{c['id']:12} {res:8} {note}")
json.dump(RESULTS, open(sys.argv[1], 'w'), indent=1)

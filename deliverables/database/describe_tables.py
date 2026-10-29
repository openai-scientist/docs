"""Markdown description of every table in the database script: usage tables.py SCRIPT.sql > out.md"""
import re
import sys

PURPOSE = {
    'users': 'A person with an account on the Platform.',
    'user_platform_roles': 'The platform-level role of a user (Platform Admin); one row per user at most.',
    'auth_sessions': 'A signed-in browser session; the token is stored only as a digest.',
    'email_otps': 'A one-time sign-in code sent by email; stored as a digest with an expiry and attempt count.',
    'google_connection_grants': 'A Google authorization that a user gives to a project for Sheets and Drive import.',
    'projects': 'The shared workspace of a team.',
    'project_memberships': 'The membership of a user in a project, with a role and an invitation state.',
    'project_settings': 'The configuration of one project (budget, presets, notifications, access settings).',
    'project_files': 'A document uploaded to a project.',
    'project_integrations': 'A chat tool (Slack, Microsoft Teams, Discord) that receives project notifications.',
    'integration_deliveries': 'One message queued for, or sent to, a project integration, with retry state.',
    'integration_secrets': 'The encrypted webhook secret of a project integration.',
    'comments': 'A remark of a member on a run or on an artifact of a run.',
    'notifications': 'An in-app notification for a user.',
    'notification_preferences': 'Which notification groups a user receives in a project.',
    'notification_emails': 'A notification email queued for a member, sent after commit by the dispatch loop.',
    'data_connections': 'An authorized external data source of a project; the credential is stored encrypted.',
    'datasets': 'A tabular dataset of a project.',
    'dataset_versions': 'An immutable version of a dataset, with its content hash and storage key.',
    'research_contexts': 'The research case of a project: topic, goals, context and constraints.',
    'research_runs': 'One execution of the research pipeline for a research case.',
    'stage_runs': 'One execution of one stage in a run.',
    'stage_decisions': 'A decision on the outcome of a stage run (accept, send back, rerun).',
    'run_events': 'A trace event that an engine or the Platform emits during a run.',
    'run_gates': 'A question of a run that waits for a person to answer.',
    'run_artifacts': 'A file that a stage run produces (hand-off object, report, figure).',
    'frame_reviews': 'A review of the research frame of a run, submitted by a member.',
    'pi_consultations': 'A consultation of the AI PI about a run or a stage, with its result.',
    'pi_notes': 'An entry of the lab notebook that the AI PI writes for a run.',
    'cost_entries': 'An increase of model token usage and cost, by project, run and model role.',
    'cost_ledger_start': 'The time from which the cost ledger is complete; one row.',
    'spending_alerts': 'A budget alert raised for a project in a month.',
    'model_profiles': 'The model configuration of a model role (model, key reference, unit price).',
    'platform_settings': 'Platform-wide settings that a Platform Admin edits; one row.',
    'engine_settings': 'Settings of one stage engine that a Platform Admin edits.',
    'audit_events': 'An append-only record of an administrative or security action.',
    'monitoring_events': 'A captured log event of a service, for log monitoring.',
    'monitoring_alerts': 'An alert raised from monitoring events, with its acknowledgement.',
    'monitoring_capture_gaps': 'A period in which log capture of a service was incomplete.',
    'monitoring_worker_states': 'The last heartbeat and state of a background worker.',
}

sql = open(sys.argv[1]).read()
cols, checks = {}, {}
for t, body in re.findall(r'CREATE TABLE public\.(\w+) \((.*?)\n\);', sql, re.S):
    cols[t] = []
    for line in body.splitlines():
        m = re.match(r'\s+(\w+) (.+?)(,)?$', line)
        if not m or m[1] == 'CONSTRAINT':
            c = re.search(r'CHECK \(+\(?(\w+)\)?(?:::text)? = ANY \(+ARRAY\[(.*?)\]', line)
            if c:
                checks[(t, c[1])] = ', '.join(re.findall(r"'([^']*)'", c[2]))
            continue
        typ = re.sub(r" DEFAULT .*| NOT NULL", '', m[2])
        typ = typ.replace('character varying', 'varchar').replace('timestamp with time zone', 'timestamptz')
        cols[t].append((m[1], typ, 'NOT NULL' in m[2]))
keys = {}
for t, kind, c, ref in re.findall(r'ALTER TABLE ONLY public\.(\w+)\s+ADD CONSTRAINT \w+ (PRIMARY KEY|UNIQUE|FOREIGN KEY) \(([\w, ]+)\)(?: REFERENCES public\.(\w+))?', sql):
    for col in c.split(', '):
        keys.setdefault((t, col), []).append({'PRIMARY KEY': 'PK', 'UNIQUE': 'Unique', 'FOREIGN KEY': f'FK → {ref}'}[kind])

n = 0
for t in PURPOSE:  # the order of the headings in the report frame
    if t == 'alembic_version':
        continue
    n += 1
    print(f'### 2.2.{n} {t}\n\n{PURPOSE[t]}\n\n| Column | Type | Required | Key | Allowed values |\n| ----- | ----- | ----- | ----- | ----- |')
    for c, typ, nn in cols[t]:
        print(f"| `{c}` | {typ} | {'Yes' if nn else 'No'} | {', '.join(keys.get((t, c), []))} | {checks.get((t, c), '')} |")
    print()

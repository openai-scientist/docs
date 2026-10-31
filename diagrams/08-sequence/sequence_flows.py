"""Reviewable interaction definitions; Report7 III/IV are the business source."""
import re


def slug(title):
    return re.sub(r'[^A-Za-z0-9]+', '-', title).strip('-')


def call(sender, receiver, label, result):
    return [{'from': sender, 'to': receiver, 'label': label},
            {'from': receiver, 'to': sender, 'label': result, 'reply': True}]


def db(label, result='Stored result'):
    return call('s', 'd', label, result)


def alt(*branches):
    return {'branches': list(branches)}


def opt(guard, body):
    return {'kind': 'opt', 'guard': guard, 'body': body}


def loop(guard, body):
    return {'kind': 'loop', 'guard': guard, 'body': body}


def event(sender, receiver, label):
    return {'from': sender, 'to': receiver, 'label': label, 'async': True}


def finish(result, display):
    return [{'from': 's', 'to': 'c', 'label': result, 'reply': True},
            {'from': 'c', 'to': 'w', 'label': result, 'reply': True},
            {'from': 'w', 'to': 'u', 'label': display, 'reply': True}]


def flow(title, slot, source, actor, controller, service, operation, steps, **kw):
    return dict(title=title, slug=slug(title), slot=slot, source=f'{slot}; {source}',
                actor=actor, controller=controller, service=service, operation=operation,
                trigger=kw.pop('trigger', title), steps=steps, **kw)


def project(title, slot, operation, steps, actor='Project Manager', service='ProjectService', **kw):
    return flow(title, slot, f'III 3.3.{int(slot.split(".")[-1])-1}; IV 3.2', actor,
                'ProjectController', service, operation, steps, **kw)


def data(title, slot, operation, steps, actor='Researcher', service='DataService', **kw):
    return flow(title, slot, 'III 3.4; IV 3.3; FR-09–12', actor,
                'DataController', service, operation, steps, **kw)


def run(title, slot, operation, steps, actor='Researcher', service='RunOrchestrator', **kw):
    return flow(title, slot, 'III 3.5; IV 3.4', actor,
                'RunController', service, operation, steps, **kw)


def pi(title, slot, operation, steps, actor='Researcher', service='DecisionService', **kw):
    return flow(title, slot, 'IV 3.6; FR-25–36, FR-262–266', actor,
                'DecisionController', service, operation, steps, **kw)


def admin(title, slot, operation, steps, service='AdministrationService', **kw):
    return flow(title, slot, 'III 3.9; IV 3.8; FE-17', 'Platform Admin',
                'AdministrationController', service, operation, steps, **kw)


GROUPS = [
    dict(folder='01-authentication-account', slug='Authentication-Account',
         title='Authentication & Account', flows=[
        flow('Sign In With Email Code', 'IV 3.1.2', 'III 3.2.1; FR-01', 'User',
             'AuthenticationController', 'AuthenticationService', 'requestEmailCode(email)', [],
             public=True, participants={'e': ': EmailDelivery'}, custom_tree=[
                 {'from': 'u', 'to': 'w', 'label': 'Enter email and request code'},
                 {'from': 'w', 'to': 'c', 'label': 'requestEmailCode(email)'},
                 {'from': 'c', 'to': 's', 'label': 'requestCode(email)'},
                 db('Store code digest and expiry', 'Challenge stored'),
                 call('s', 'e', 'sendCode(email, code)', 'Delivery request accepted'),
                 finish('Request completed', 'Show Verify code (SC-02)'),
                 {'from': 'u', 'to': 'w', 'label': 'Enter code received by email'},
                 {'from': 'w', 'to': 'c', 'label': 'signInWithCode(input)'},
                 {'from': 'c', 'to': 's', 'label': 'verifyCode(input)'},
                 db('Load email challenge', 'Challenge'),
                 alt(('[code invalid or expired]', finish('Verification rejected', 'Show invalid / expired code')),
                     ('[else: code valid and not expired]', [
                         db('Find user by verified email', 'User or no account'),
                         opt('[account not found]', [db('Create first-sign-in account', 'User created')]),
                         db('Consume code and create session atomically', 'AuthSession'),
                         finish('AuthSession', 'Show signed-in state')]))]),
        flow('Sign In With Google', 'IV 3.1.3', 'III 3.2.2; FR-146', 'User',
             'AuthenticationController', 'AuthenticationService', 'signInWithGoogle(code)', [
                 call('s', 'g', 'verifyIdentity(code)', 'Verified identity or rejection'),
                 alt(('[identity invalid]', [db('Record sign-in rejection', 'Rejected; no session')]),
                     ('[verified email available]', [
                         db('Find user by verified email', 'User or no account'),
                         opt('[first sign-in]', [db('Create account for verified email', 'User')]),
                         db('Create session for same user identity', 'AuthSession')]))],
             public=True, google_consent=True, participants={'g': ': GoogleIdentityProvider'},
             trigger='Complete Google authorization and return code'),
        flow('Complete Onboarding and Update Profile', 'IV 3.1.4', 'III 3.2.3', 'User',
             'AuthenticationController', 'AccountService', 'Update own profile(input)', [
                 db('Load current user profile', 'Current user'),
                 alt(('[first onboarding]', [db('completeOnboarding(input)', 'Profile completed')]),
                     ('[profile update]', [db('updateProfile(input)', 'Own profile updated')]))], session_only=True),
        flow('Sign Out', 'IV 3.1.5', 'III 3.2.4', 'User',
             'AuthenticationController', 'AuthenticationService', 'revokeSession(sessionId)', [
                 db('Revoke current session', 'Session ended')], session_only=True,
             display='Return to sign-in page'),
        flow('View Unauthorized and Session Expired Pages', 'IV 3.1.6', 'III 3.2.5; FR-02, FR-151',
             'User', 'AuthenticationController', 'AuthenticationService', 'validateSession(token)', [
                 db('Read session and current access context', 'Session / role status'),
                 alt(('[session expired or missing]', finish('Session expired', 'Show sign-in required')),
                     ('[authenticated but action denied]', finish('Unavailable / permission denied', 'Show unavailable without project disclosure')),
                     ('[session and permission valid]', finish('Access allowed', 'Continue to authorized page')))], public=True, terminal_branches=True,
             display='Show sign-in / unavailable page or continue', trigger='Open a protected page'),
    ]),
    dict(folder='02-project-workspace', slug='Project-Workspace', title='Project Workspace', flows=[
        project('Create Project', 'IV 3.2.2', 'create(input)', [
            db('Validate name and description', 'Input validation'),
            alt(('[input invalid]', []), ('[input valid]', [
                db('Create project and creator PM membership', 'Project and membership'),
                db('recordChange(project created)', 'Audit entry')]))], actor='User', session_only=True),
        project('View Project List and Overview', 'IV 3.2.3', 'Read accessible projects', [
            db('List only projects with user membership', 'Project list'),
            opt('[project selected]', [db('Read authorized project overview', 'Project overview')])], actor='User', session_only=True),
        project('Update Archive or Complete Project', 'IV 3.2.4', 'Apply project change(input)', [
            db('Read current project state', 'Project state'),
            alt(('[archived: write blocked]', []), ('[writable project]', [
                alt(('[edit selected]', [db('update(projectId, input)', 'Project updated')]),
                    ('[archive selected]', [db('archive(projectId)', 'Read-only archived project')]),
                    ('[complete selected]', [db('Mark project completed', 'Completed project')])),
                db('recordChange(action)', 'Audit entry')]))]),
        project('Manage Members and Invitations', 'IV 3.2.5', 'Manage project access', [
            db('Read project state and active managers', 'Access context'),
            alt(('[archived or last PM removal]', []), ('[change permitted]', [
                alt(('[invite]', [db('invite(projectId, email, role)', 'Pending invitation')]),
                    ('[change role]', [db('changeRole(memberId, role)', 'Role updated')]),
                    ('[remove member]', [db('remove(memberId)', 'Member removed')])),
                db('Append access change audit', 'Audit entry')]))], service='MembershipService'),
        project('Manage Documents', 'IV 3.2.6', 'Manage project documents', [
            db('Load document and project state', 'Document context'),
            alt(('[download]', [db('Read authorized document', 'Document bytes or reference')]),
                ('[writable project: upload]', [db('add(projectId, input)', 'Document stored')]),
                ('[writable project: delete confirmed]', [db('Delete document and append audit', 'Document removed')]),
                ('[else: write forbidden or not confirmed]', []))], actor='Researcher', service='DocumentService'),
        project('Manage Project Integrations and Preferences', 'IV 3.2.7', 'Manage project delivery settings', [
            db('Check project writable state', 'Write permission'),
            alt(('[project archived]', []), ('[project writable]', [
                alt(('[connect channel]', [call('s', 'x', 'configure(input)', 'Integration with sealed secret reference')]),
                    ('[test channel]', [call('s', 'x', 'Test configured channel', 'Delivery test result')]),
                    ('[remove channel]', [db('Remove project integration', 'Integration removed')]),
                    ('[set notification groups]', [db('Save project notification preferences', 'Preferences saved')])),
                db('Append settings change audit', 'Audit entry')]))], participants={'x': ': IntegrationService'}),
        project('Accept or Decline Invitation', 'IV 3.2.8', 'Respond to own invitation', [
            db('Load invitation and verify recipient', 'Invitation and expiry'),
            alt(('[expired or recipient mismatch]', []), ('[valid invitation]', [
                alt(('[accept]', [db('accept(invitationId)', 'Membership with invited role')]),
                    ('[decline]', [db('decline(invitationId)', 'Invitation declined')])),
                db('Append invitation response audit', 'Audit entry')]))],
                actor='User', service='InvitationService', session_only=True),
        project('Resend or Cancel Invitation', 'IV 3.2.9', 'Manage pending invitation', [
            db('Read pending invitation and project state', 'Pending / writable status'),
            alt(('[not pending or project archived]', []), ('[pending and writable]', [
                alt(('[resend]', [db('resend(invitationId)', 'Invitation delivery requested')]),
                    ('[cancel]', [db('cancel(invitationId)', 'Invitation cancelled')])),
                db('Append invitation change audit', 'Audit entry')]))], service='InvitationService'),
        project('Transfer Ownership', 'IV 3.2.10', 'transferOwnership(projectId, userId)', [
            db('Check caller ownership and target active membership', 'Transfer eligibility'),
            alt(('[not owner, archived or inactive target]', []), ('[transfer eligible]', [
                db('Transfer ownership; retain an active PM', 'New owner'),
                db('Append ownership transfer audit', 'Audit entry')]))], service='MembershipService'),
        project('Delete Project', 'IV 3.2.11', 'Delete project after confirmation', [
            db('Verify project owner and confirmation', 'Deletion eligibility'),
            alt(('[not owner or not confirmed]', []), ('[confirmed by owner]', [
                db('Record deletion audit and delete project', 'Deletion recorded')]))]),
        project('View Project Activity and Audit Log', 'IV 3.2.12', 'Read project activity(filter)', [
            db('Query project-scoped append-only audit', 'Authorized activity entries')], actor='Researcher'),
        project('Configure Project Settings and Monthly Budget', 'IV 3.2.13', 'configure(settings)', [
            db('Validate settings and writable project', 'Validation result'),
            alt(('[invalid or archived]', []), ('[valid and writable]', [
                db('Save monthly budget, thresholds and access settings', 'Project settings'),
                call('s', 'x', 'updatePreset(stage, preset)', 'Future actions and waiting items reevaluated'),
                db('Save pinned deadline and append change audit', 'Settings saved')]))],
                participants={'x': ': ActionPolicyService'}),
    ]),
]

GROUPS += [
    dict(folder='03-data-management', slug='Data-Management', title='Data Management', flows=[
        data('Upload Dataset', 'IV 3.3.2', 'upload(input)', [
            db('Validate format, size and readable table', 'SR-01 / SR-02 / SR-07 result'),
            alt(('[file invalid]', []), ('[valid tabular file]', [
                call('s', 'v', 'create(datasetId, source)', 'Immutable version with content hash'),
                db('Save dataset and platform location', 'Dataset with first version')]))],
             participants={'v': ': DatasetVersionService'}),
        data('View Dataset Detail', 'IV 3.3.3', 'Read dataset detail(versionId)', [
            db('Read dataset versions and location', 'Immutable versions and location'),
            db('Read code-computed profile and columns', 'Metadata only; no local rows')], actor='Researcher'),
        data('Manage Data Connection and Import', 'IV 3.3.4', 'importData(connection)', [
            call('s', 'k', 'seal(credential)', 'SecretRef only'),
            db('Save connection with sealed reference', 'DataConnection'),
            call('s', 'x', 'Read authorized source; block internal hosts', 'Source validation result'),
            alt(('[unauthorized or internal host]', []), ('[authorized source]', [
                call('s', 'x', 'Import selected table', 'Imported table'),
                call('s', 'v', 'create(datasetId, source)', 'New immutable version and hash'),
                db('Save version with platform location', 'Imported version')]))],
             participants={'k': ': SecretService', 'x': 'Authorized Data Source', 'v': ': DatasetVersionService'}),
        data('Rename or Delete Dataset', 'IV 3.3.5', 'Manage selected dataset', [
            db('Read dataset and writable project', 'Dataset context'),
            alt(('[project archived]', []), ('[rename selected]', [db('Rename dataset metadata', 'Name updated')]),
                ('[delete confirmed]', [db('Delete dataset according to references', 'Deletion result')]),
                ('[else: not confirmed]', []))]),
        data('Upload New Dataset Version', 'IV 3.3.6', 'Upload next version(input)', [
            db('Validate writable project and uploaded table', 'Validation result'),
            alt(('[invalid or archived]', []), ('[valid upload]', [
                call('s', 'v', 'create(datasetId, source)', 'New version; old versions unchanged'),
                db('Persist version and content hash', 'New immutable version')]))],
             participants={'v': ': DatasetVersionService'}),
        data('Download or Preview Dataset Version', 'IV 3.3.7', 'Read dataset version content', [
            db('Read pinned version and data location', 'Version location'),
            alt(('[location local]', []),
                ('[platform location: preview]', [db('Read authorized preview rows', 'TablePreview')]),
                ('[platform location: download]', [db('Read authorized version file', 'Download content')]))]),
        data('Browse and Preview Connection Source', 'IV 3.3.8', 'Browse authorized connection', [
            db('Load connection secret reference', 'DataConnection without credentials'),
            call('s', 'x', 'Validate authorized source and host', 'Source eligibility'),
            alt(('[source rejected]', []), ('[source authorized]', [
                call('s', 'x', 'List available tables and files', 'Source list'),
                opt('[source selected]', [call('s', 'x', 'Preview selected source', 'Table preview')])]))],
             participants={'x': 'Authorized Data Source'}),
        data('Rename Test or Delete Data Connection', 'IV 3.3.9', 'Manage data connection', [
            db('Read connection and project state', 'Connection context'),
            alt(('[project archived: write rejected]', []),
                ('[rename]', [db('Rename connection', 'Updated metadata')]),
                ('[test]', [call('s', 'x', 'Test authorized source connection', 'Connection test result')]),
                ('[delete confirmed]', [db('Delete connection and sealed reference', 'Connection removed')]))],
             participants={'x': 'Authorized Data Source'}),
        data('Connect Google Sheets and Drive', 'IV 3.3.10', 'Authorize Google source for project', [
            call('s', 'g', 'Request project-scoped authorization', 'Authorization outcome'),
            alt(('[consent denied]', []), ('[consent granted]', [
                db('Store sealed grant reference for project', 'Grant reference only'),
                call('s', 'g', 'List authorized sheets and files', 'Source list'),
                call('s', 'g', 'Read selected authorized source', 'Imported table'),
                db('Create immutable dataset version and hash', 'DatasetVersion')]))],
             participants={'g': 'Google Sheets / Drive'}),
        data('Execute Local Job and Release Aggregate', 'Figure IV-12', 'runLocal(job)', [
            db('Read pinned version and Node status', 'Local job eligibility'),
            alt(('[Node revoked]', []),
                ('[Node offline and job blocks work]', [db('Set waiting(node_offline); retain other work', 'Wait state and one combined notice')]),
                ('[Node online]', [
                    call('s', 'n', 'route(job); verify pinned hash', 'Hash check result'),
                    alt(('[hash mismatch]', [db('Record rejection; propose new version', 'Mismatch reason')]),
                        ('[hash matches]', [
                            {'from': 's', 'to': 'n', 'label': 'Run isolated job; keep raw result local'},
                            call('n', 'r', 'check(job, aggregate) locally', 'Firewall, rounding, disclosure, differencing, probe checks'),
                            alt(('[probe exhausted or release rejected]', [
                                    {'from': 'n', 'to': 's', 'label': 'Sanitized rejection; no aggregate', 'reply': True},
                                    db('Record gap and rejection reason', 'Run may continue other work')]),
                                ('[strict mode: new number kind]', [
                                    {'from': 'n', 'to': 's', 'label': 'Release approval required; no raw result', 'reply': True},
                                    db('Create release review item', 'Await Researcher or PM approval')]),
                                ('[release allowed]', [
                                    call('n', 'r', 'Append local release log', 'Release reference'),
                                    {'from': 'n', 'to': 's', 'label': 'Released aggregate only', 'reply': True},
                                    db('Store copy of approved release', 'Released aggregate')]))]))]))],
             participants={'n': 'Local Node', 'r': ': ReleaseGate (Local Node)'}),
    ]),
    dict(folder='04-research-run-orchestration', slug='Research-Run-Orchestration',
         title='Research Run Orchestration', flows=[
        run('Start Research Run', 'IV 3.4.2', 'start(caseId)', [
            db('Check monthly budget and active run atomically', 'Start eligibility'),
            alt(('[budget blocked or active run exists]', []), ('[start allowed]', [
                db('Create Run with dataset_first and pinned case', 'Run created'),
                event('s', 'e', 'Schedule first stage with policy and keys by role')]))],
             participants={'e': ': DatasetEngine'}, result='Run or start rejection', display='Show Run Studio or start error'),
        run('Monitor Run in Run Studio', 'IV 3.4.3', 'Read authorized run snapshot', [
            db('Read run state, stages and artifacts', 'Current snapshot'),
            loop('[while authorized monitoring is open]', [
                event('t', 's', 'Committed run event'),
                event('s', 'c', 'Authorized event projection'),
                event('c', 'w', 'Stream state / trace / artifact update')])],
             participants={'t': 'Run Event Stream'}, display='Show latest run state'),
        run('Answer Decision Inbox Item', 'IV 3.4.4', 'Answer waiting decision(itemId, option)', [
            call('s', 'q', 'answer(itemId, option)', 'Decision result'),
            alt(('[not eligible or item no longer pending]', []), ('[decision accepted]', [
                db('Append decision log and recheck blocked work', 'Decision recorded'),
                opt('[no other blocking item]', [db('Return waiting run to running', 'Run may continue')])]))],
             participants={'q': ': DecisionService'}),
        run('Accept Revise or Rerun Stage Version', 'IV 3.4.5', 'Review stage version(action)', [
            db('Read version checks and current acceptance policy', 'Stage eligibility'),
            alt(('[checks or policy reject action]', []),
                ('[accept eligible version]', [db('Accept version; keep accepted content immutable', 'Accepted version')]),
                ('[request revision]', [db('Record reason and create draft successor', 'New draft version')]),
                ('[rerun requested]', [db('Create next version; mark downstream stale', 'Versioned rerun scheduled')])),
            db('Append action decision record', 'Decision log')]),
        run('Cancel and Synchronize Run', 'IV 3.4.6', 'Apply run control(action)', [
            db('Check creator-or-PM rights and run state', 'Control eligibility'),
            alt(('[read synchronization]', [db('Read authoritative run and engine state', 'Current state')]),
                ('[cancel requested and not ended]', [db('cancel(runId); keep accepted objects', 'ended(cancelled)'),
                    db('Close pending items and append audit', 'Cancellation recorded')]),
                ('[else: cancel not permitted]', []))]),
        run('Raise Token Budget', 'IV 3.4.7', 'Adjust run token allowance(input)', [
            db('Check run not ended and proposed allowance', 'Budget adjustment validation'),
            alt(('[invalid or ended]', []), ('[active and allowed]', [
                db('Save increased run token budget; append audit', 'Updated token allowance'),
                db('Read independent monthly spending restriction', 'Project spend approval still required if blocked')]))],
             actor='Project Manager', service='BudgetService'),
        run('View Review Rounds Diffs and Artifacts', 'IV 3.4.8', 'Read stage review history', [
            db('Read authorized versioned review rounds', 'Findings and revision history'),
            db('Read version diffs and artifact references', 'Review details')]),
        run('Comment On Run', 'IV 3.4.9', 'Add anchored comment(input)', [
            {'from': 's', 'to': 'x', 'label': 'add(input with object anchor)'},
            {'from': 'x', 'to': 'd', 'label': 'Persist authorized comment with anchor'},
            {'from': 'd', 'to': 'x', 'label': 'Comment', 'reply': True},
            {'from': 'x', 'to': 's', 'label': 'Comment or permission error', 'reply': True}],
             participants={'x': ': CommentService'}, repository='CommentRepository'),
        run('View Run List', 'IV 3.4.10', 'Read project runs(filter)', [
            db('List runs of authorized project', 'Runs and current states')]),
        run('View Recovery State', 'IV 3.4.11', 'Read recovery status(runId)', [
            db('Read failed checks, budget and recovery trace', 'Recovery state and reason'),
            alt(('[repair within item budget]', [db('Read system repair progress', 'Retrying details')]),
                ('[item share exhausted]', [db('Read needs-you item and prior attempts', 'Human action required')]),
                ('[unrecoverable or missing model / key]', [db('Read failed_technical reason', 'No sample output')]))]),
        run('Download and Compare Artifacts', 'IV 3.4.12', 'Read artifact versions(action)', [
            db('Verify project access and version references', 'Authorized artifacts'),
            alt(('[download]', [db('Read selected immutable artifact', 'Artifact content')]),
                ('[compare]', [db('Read two authorized artifact versions', 'Version differences')]))]),
        run('View Iteration Summary', 'IV 3.4.13', 'Read iteration summary(stageId)', [
            db('Read stage versions, reasons and review events', 'What changed and why')]),
        run('Edit or Delete Comment', 'IV 3.4.14', 'Modify own comment(action)', [
            db('Check comment author and project state', 'Ownership and writable status'),
            alt(('[not author or project archived]', []),
                ('[edit]', [db('Save own comment edit', 'Updated comment')]),
                ('[delete confirmed]', [db('Delete own comment', 'Comment removed')]))]),
    ]),
]


def engine(title, slot, service, operation, steps, **kw):
    return flow(title, slot, 'IV 3.5; FE-06–11; FR-37–78', 'Researcher',
                'RunController', service, operation, steps, **kw)


GROUPS += [
    dict(folder='05-research-engines', slug='Research-Engines', title='Research Engines', flows=[
        engine('Dataset Stage', 'IV 3.5.2', 'DatasetEngine', 'profile(versionId)', [
            db('Read dataset metadata and pinned version', 'Dataset context'),
            call('s', 'h', 'Compute profile, dictionary and fitness in code', 'Snapshot draft and checks'),
            call('s', 'q', 'createRequest(confirm observation unit and structure)', 'Pinned decision status'),
            alt(('[confirmation pending]', [db('Persist draft; no split before user confirmation', 'Waiting for pinned answer')]),
                ('[confirmed by user]', [
                    call('s', 'h', 'Create power-based split; check duplicates / shift', 'Split digest and check results'),
                    call('s', 'h', 'checkContract(snapshot)', 'Contract result'),
                    alt(('[contract red]', [db('Record repair tasks; respect item budget', 'Draft with checks_red')]),
                        ('[contract green]', [call('s', 'r', 'review(snapshot)', 'Verified review findings'),
                            db('Publish DatasetSnapshot version for acceptance', 'Snapshot with fitness and known risks')]))]))],
               participants={'h': ': Harness', 'q': ': DecisionService', 'r': ': IndependentReviewService'}),
        engine('Hypothesis Stage', 'IV 3.5.3', 'HypothesisEngine', 'propose(snapshot)', [
            db('Read accepted pinned DatasetSnapshot', 'Snapshot'),
            call('s', 'l', 'Search eligible scholarly sources', 'Sources, prior art and source failures'),
            db('Update LiteratureBase with source provenance', 'LiteratureBase version'),
            db('Draft hypotheses with comparator and rule', 'Portfolio draft'),
            call('s', 'h', 'Check comparator, baseline and hypothesis limits', 'Portfolio validation'),
            alt(('[invalid hypothesis or weak baseline]', [db('Record repair need', 'Not accepted')]),
                ('[portfolio valid]', [call('s', 'q', 'createRequest(select hypotheses and primary)', 'Pinned selection status'),
                    alt(('[selection pending]', [db('Keep selection waiting', 'No automatic primary choice')]),
                        ('[user selected at least two and primary]', [db('Publish selected HypothesisSet version', 'Selected portfolio')]))]))],
               participants={'l': 'Scholarly Sources', 'h': ': Harness', 'q': ': DecisionService'}),
        engine('Experiment Design Stage and Lock', 'IV 3.5.4 / Figure IV-10',
               'ExperimentDesignEngine', 'build(hypothesisSet)', [
            db('Read pinned hypotheses and snapshot', 'Accepted input versions'),
            db('Draft plan, pattern versions and pipeline order', 'AnalysisPlan draft'),
            call('s', 'h', 'enforcePipelineOrder(plan)', 'Pipeline guard result'),
            call('s', 'h', 'Rehearse on released-aggregate twin', 'Golden outputs and contract checks'),
            alt(('[checks red]', [db('Keep plan draft for repairs', 'No Lock written')]),
                ('[checks green]', [call('s', 'q', 'createRequest(lock plan)', 'Pinned lock decision'),
                    alt(('[user away or decision pending]', [db('Keep plan waiting for user', 'Nobody locks for user')]),
                        ('[user approves lock]', [db('Write hashes, split digest, actor and lock time', 'Immutable Lock')]))]))],
               participants={'h': ': Harness', 'q': ': DecisionService'}),
        engine('Independent Review and Revision Rounds', 'IV 3.5.5',
               'IndependentReviewService', 'review(objectVersion)', [
            call('s', 'h', 'checkContract(objectVersion)', 'Contract status'),
            alt(('[contract red]', [db('Record contract repair tasks', 'Not ready for independent review')]),
                ('[contract green]', [
                    loop('[initial review, or confirmed blockers remain and revision round < 2]', [
                        {'kind': 'par', 'branches': [
                            ('[guard A: fresh isolated context]', call('s', 'g1', 'Review assigned version and fields', 'Anchored findings')),
                            ('[guard B: fresh isolated context]', call('s', 'g2', 'Review independently', 'Anchored findings'))]},
                        call('s', 'h', 'Drop unanchored findings; verify evidence', 'Confirmed / plausible / rejected'),
                        alt(('[confirmed blockers and round available]', [
                            call('s', 'm', 'Revise confirmed blockers only', 'Repaired version'),
                            call('s', 'h', 'Recheck changed fields; new unchanged-field blocker needs new computed fact', 'New contract result')]),
                            ('[no confirmed blocker or round limit reached]', [db('Record major / minor findings and known risks', 'Review outcome')]))]),
                    db('Publish review record; unresolved evidence withheld', 'Version ready for acceptance policy')]))],
               participants={'h': ': Harness', 'g1': 'Guard Persona A', 'g2': 'Guard Persona B', 'm': 'Maker Persona'}),
        engine('Execution Stage and Unseal Results', 'IV 3.5 / FE-09 / Figure IV-10',
               'ExecutionEngine', 'execute(lock)', [
            db('Read immutable Lock and pinned inputs', 'Locked program and split'),
            call('s', 'h', 'enforcePipelineOrder(plan)', 'Pipeline check'),
            alt(('[pipeline violates Lock]', [db('Block run or request pinned deviation', 'No silent algorithm change')]),
                ('[locked pipeline valid]', [
                    call('s', 'x', 'Twin rehearsal and permutation check', 'Twin diagnostics'),
                    call('s', 'x', 'Dry run on real data without estimates', 'Counts, types, missingness, convergence, time'),
                    call('s', 'x', 'Confirmatory job; write sealed envelope', 'Done / filtered error only to agent'),
                    call('s', 'h', 'Check Lock, jobs complete and last lane-C repair', 'Unseal eligibility'),
                    alt(('[unseal checks fail]', [db('Record rejection; keep envelope sealed', 'No estimates exposed')]),
                        ('[manual unseal and user has not approved]', [db('Keep pinned unseal request pending', 'Envelope remains sealed')]),
                        ('[checks green and auto or user approved]', [
                            db('Unseal all hypotheses of Lock; record time', 'Unsealed results'),
                            call('s', 'h', 'Compute verdict, grade and claim ceiling in code', 'Evidence records and interpretation rows'),
                            db('Publish EvidenceBundle with replication package', 'Versioned EvidenceBundle')]))]))],
               participants={'h': ': Harness', 'x': 'Isolated Executor'}),
        engine('Paper Stage', 'IV 3.5 / FE-10', 'PaperEngine', 'draft(input)', [
            db('Read accepted bundle, plan, Lock, literature and log', 'Pinned input references'),
            call('s', 'h', 'renderNumbers(bundle records)', 'Code-rendered tables and figures'),
            db('Build claims and manuscript within claim ceiling', 'PaperPack draft'),
            call('s', 'h', 'Validate claims, citations and reporting checklist', 'Paper contract result'),
            alt(('[invalid claim or unresolved citation]', [db('Record repairs; do not publish invalid content', 'Draft with checks_red')]),
                ('[contract green]', [call('s', 'r', 'review(paperPack)', 'Independent findings and known risks'),
                    db('Publish PaperPack for acceptance', 'PaperPack version; no automatic submission')]))],
               participants={'h': ': Harness', 'r': ': IndependentReviewService'}),
    ]),
    dict(folder='06-ai-principal-investigator', slug='AI-Principal-Investigator',
         title='AI Principal Investigator', flows=[
        pi('Configure Action Policy', 'IV 3.6.2', 'changePolicy(input)', [
            call('s', 'p', 'Check floors and spending ceiling', 'Policy validation'),
            alt(('[override below floor or invalid]', []), ('[valid preset or override]', [
                call('s', 'p', 'updatePreset(stage, preset)', 'Future actions use updated effective level'),
                db('Save overrides and append policy change log', 'New policy version'),
                call('s', 'p', 'Reevaluate waiting items; retain past decisions', 'Waiting item evaluation')]))],
           participants={'p': ': ActionPolicyService'}),
        pi('Handle Must-Ask and Tentative Decisions', 'IV 3.6.3', 'Handle action decision(input)', [
            call('s', 'p', 'effectiveLevel(actionType)', 'Level with floor and ceiling'),
            db('Create inbox item with options and reason', 'DecisionInboxItem'),
            alt(('[present: must_ask]', [db('Ask user; wait only if all work blocked', 'Pending decision')]),
                ('[away: pinned]', [db('Keep waiting until deadline; continue independent work', 'No AI or default answer'),
                    opt('[deadline passed without answer]', [db('Close unanswered and end with_gaps', 'Gap and unanswered item')])]),
                ('[away: autopilot and non-pinned]', [call('s', 'i', 'decideTentatively(item)', 'Tentative decision with reason'),
                    db('Record tentative decision for user review', 'Decision log and notebook')]),
                ('[else: no tentative authority]', [db('Queue item; continue independent work', 'Pending user decision')]))],
           participants={'p': ': ActionPolicyService', 'i': ': AIPrincipalInvestigator'},
           system_trigger=': RunOrchestrator'),
        pi('Confirm or Overturn Tentative Decision', 'IV 3.6.4', 'Review tentative item(action)', [
            db('Read tentative item and user authority', 'Tentative decision'),
            alt(('[item not tentative or no longer actionable]', []),
                ('[confirm]', [db('Confirm tentative decision; append log', 'Confirmed decision')]),
                ('[overturn with reason]', [db('overturn(itemId, reason)', 'Overturn recorded'),
                    call('s', 'r', 'Undo dependent work; mark affected objects stale', 'Dependent work invalidated')])),
            call('s', 'm', 'compute(actionType)', 'Overturn rate and suggested higher level'),
            db('Record proposal only; do not auto-change policy', 'Metrics and policy suggestion')],
           participants={'r': ': RunOrchestrator', 'm': ': OverturnMetricService'}),
        pi('View Lab Notebook', 'IV 3.6.5', 'Read lab notebook(runId)', [
            db('Read authorized run notebook', 'Summaries, proposals and tentative reasons'),
            db('Read assumptions with alternatives and actor', 'Assumptions remain distinct from user intent')]),
        pi('View PI Overview and Close Report', 'IV 3.6.6', 'Read PI overview(runId)', [
            db('Read run progress, decisions and notebook', 'PI overview'),
            opt('[run ended]', [call('s', 'i', 'proposeNextStep(runId)', 'Proposal from fixed allowed set'),
                db('Read close report and remaining gaps', 'User chooses next step; PI never ends run')])],
           participants={'i': ': AIPrincipalInvestigator'}),
        flow('Charter and Directives', 'IV 3.6.2', 'III 3.7.1; FR-31, FR-32', 'Researcher / Project Manager',
             'DecisionController', 'DecisionService', 'Submit run goals, limits and questions', [
                 db('Read run context and existing charter', 'Current charter'),
                 alt(('[invalid input or unauthorized change]', []), ('[valid charter and directives]', [
                     db('Record goals, limits and questions for this run', 'Charter and directives recorded'),
                     db('Record user action in decision log', 'Action recorded')]))]),
        flow('Stage Outcome Failure and Close Consultations', 'IV 3.6.3', 'III 3.7.2; NS-03; FR-31, FR-35', 'Project member',
             'DecisionController', 'DecisionService', 'Request background consultation for stage outcome, failure or run close', [
                 db('Record consultation and event context', 'Queued consultation'),
                 call('s', 'i', 'Consult AI PI with authorized run context', 'Advice or consultation failure'),
                 alt(('[consultation failed]', [db('Record failure for the consultation', 'Failure recorded')]),
                     ('[advice returned]', [db('Record advice and notebook entry', 'Consultation result'),
                         db('Keep pinned actions for user decision', 'No pinned decision by AI PI')]))],
             participants={'i': ': AIPrincipalInvestigator'}, system_trigger=': RunOrchestrator'),
        flow('Endorse or Retry Consultation', 'IV 3.6.4', 'III 3.7.3; FR-30, FR-177', 'Researcher / Project Manager',
             'DecisionController', 'DecisionService', 'Review consultation advice(action)', [
                 db('Read consultation and check action eligibility', 'Consultation context'),
                 alt(('[not eligible or result unavailable]', []),
                     ('[endorse advice]', [db('Record endorsement and user action', 'Endorsement recorded')]),
                     ('[request new consultation]', [db('Record user override and queue new consultation', 'New consultation queued')]))]),
    ]),
    dict(folder='07-notifications-integrations', slug='Notifications-Integrations',
         title='Notifications & Integrations', flows=[
        flow('Receive Notifications', 'IV 3.7.2', 'IV 3.7; FR-29, FR-100, FR-255, FR-264', 'Researcher',
             'CollaborationController', 'NotificationService', 'create(event)', [
                     call('s', 'p', 'resolveForProject(projectId)', 'Effective notification settings'),
                     db('Create authorized in-app notification', 'Notification'),
                     alt(('[blocking pinned or spending item]', [
                         db('Select recipients authorized to answer', 'Researcher + PM for pinned; PM for spending'),
                         call('s', 'i', 'deliver(notificationId, enabledChannel)', 'External notice delivery result')]),
                         ('[other event]', []))],
             participants={'p': ': NotificationPreferenceService', 'i': ': IntegrationService'},
             system_trigger='Project Event Stream'),
        flow('View Actionable Decision Inbox', 'IV 3.7.3', 'IV 3.6; FR-28; ADR-05', 'Researcher',
             'CollaborationController', 'DecisionService', 'Read own actionable inbox', [
                 db('Filter items by answer authority and membership', 'Authorized pending items'),
                 db('Sort by blocking level then blocking time', 'Single decision inbox')]),
        flow('Set Notification Preferences', 'IV 3.7.4', 'III 3.8.3; IV 3.7', 'Researcher',
             'CollaborationController', 'NotificationPreferenceService', 'update(input)', [
                 db('Validate notification groups and writable project', 'Preference eligibility'),
                 alt(('[invalid or archived]', []), ('[valid preferences]', [
                     db('Save current user project preferences', 'NotificationPreference'),
                     db('Retain external-notice eligibility restriction', 'Preferences do not widen event eligibility')]))]),
        flow('Mark Notifications as Read', 'IV 3.7.5', 'III 3.8.4', 'Researcher',
             'CollaborationController', 'NotificationService', 'markRead(notificationId)', [
                 db('Check current user owns notification', 'Notification scope'),
                 alt(('[not recipient]', []), ('[one notice]', [db('Mark own notification read', 'Read state')]),
                     ('[all own notices]', [db('Mark current user notices read', 'Own read states')]))],
             session_only=True),
        flow('View Reviewer Queue', 'IV 3.7.3', 'III 3.8.2; SC-13; FE-15', 'Project member',
             'CollaborationController', 'ReviewService', 'Read review items across projects', [
                 db('Find projects where the user is a member', 'Authorized memberships'),
                 db('Read items awaiting review for this user across those projects', 'Authorized review items'),
                 db('Return project and item references', 'Reviewer queue')], session_only=True,
             display='Show items awaiting the user review'),
    ]),
    dict(folder='08-administration-monitoring', slug='Administration-Monitoring',
         title='Administration & Monitoring', flows=[
        admin('Manage Users', 'IV 3.8.2', 'manageUsers(input)', [
            db('Read selected users and validate action', 'User admin context'),
            alt(('[input invalid]', []), ('[permitted user update]', [
                db('updateUser(input)', 'Updated User'), db('Append admin action audit', 'Audit entry')]))]),
        admin('Configure Models and Decision Provider', 'IV 3.8.3', 'configureModel(input)', [
            call('s', 'k', 'seal(key)', 'SecretRef; never raw key in result'),
            db('Save model role, provider and sealed key reference', 'ModelProfile'),
            opt('[test requested]', [call('s', 'x', 'Test configured model using sealed reference', 'Sanitized capability result')]),
            db('Append configuration audit without secret', 'Audit entry')],
              participants={'k': ': SecretService', 'x': 'Model Provider'}),
        admin('Edit Platform and Engine Settings', 'IV 3.8.4', 'configureEngine(input)', [
            db('Validate platform limits and engine settings', 'Settings validation'),
            alt(('[invalid settings]', []), ('[valid settings]', [
                db('Save platform settings, engine defaults and budget', 'Updated settings'),
                db('Append settings audit', 'Audit entry')]))]),
        admin('View Usage Audit Log and Log Monitoring', 'IV 3.8.5', 'Read operating records(filter)', [
            alt(('[usage]', [db('Read scoped usage and cost ledger', 'Usage metrics with availability')]),
                ('[audit]', [db('readAudit(filter)', 'Append-only audit entries')]),
                ('[captured service logs]', [db('Read captured logs with secret filtering', 'Log entries and capture gaps')])),
            opt('[monitoring remains open]', [event('t', 's', 'New authorized monitoring projection'),
                event('s', 'c', 'Filtered monitoring update'), event('c', 'w', 'Update monitoring view')])],
              service='MonitoringService', participants={'t': 'Monitoring Event Stream'}),
        admin('View Admin Overview', 'IV 3.8.6', 'Read platform overview', [
            db('Read usage, health and recent audit activity', 'Overview with availability / missing reasons')],
              service='MonitoringService'),
        admin('View and Edit User Detail', 'IV 3.8.7', 'Manage selected user detail', [
            db('Read user profile and project metadata', 'User detail without research content'),
            opt('[profile edit requested and valid]', [db('updateUser(input)', 'Updated profile'),
                db('Append profile admin change audit', 'Audit entry')])]),
        admin('View All Projects', 'IV 3.8.8', 'Read all project metadata', [
            db('Read project list, members, usage and run states', 'Metadata only; no datasets or manuscripts')]),
        admin('Grant or Revoke Platform Admin', 'IV 3.8.9', 'Change platform role(input)', [
            db('Validate target user and role action', 'Role action eligibility'),
            alt(('[invalid target or action]', []),
                ('[grant]', [db('Grant Platform Admin role; append audit', 'Role granted')]),
                ('[revoke]', [db('Revoke Platform Admin role; append audit', 'Role revoked')]))]),
        admin('View System Health and Acknowledge Alerts', 'IV 3.8.10', 'Read health and alerts', [
            db('Read component and worker health with availability', 'HealthSnapshot and alerts'),
            opt('[acknowledge selected alert]', [db('Validate alert and record acknowledgement', 'Alert acknowledgement audit')])],
              service='MonitoringService'),
    ]),
]

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


# Tabs added 2026-11-03 from FA26SE115_Report7 (3).md (III restructured in Report7 (2)).
LOCAL_SOURCE = 'Report7 (3) III 3.8; FR-79–87, FR-110, FR-230–242'


def denied():
    return [{'from': 'c', 'to': 'w', 'label': 'Access rejected', 'reply': True},
            {'from': 'w', 'to': 'u', 'label': 'Show unavailable', 'reply': True}]


def choice(guard, entry, operation, steps=(), **kw):
    """One user choice: its own controller entry and service operation (class model)."""
    return dict(guard=guard, entry=entry, operation=operation, steps=list(steps), **kw)


def guarded(action, body):
    """Permission check before the protected body, per rule.md (Fragment và luồng lỗi)."""
    return [{'from': 'c', 'to': 'a', 'label': f'requireRole(user, project, {action})'},
            {'from': 'a', 'to': 'c', 'label': 'Access check result', 'reply': True},
            alt(('[access denied]', denied()), ('[else: access allowed]', body))]


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
             'AuthenticationController', 'AuthenticationService', 'signInGoogle(code)', [
                 call('s', 'g', 'verifyIdentity(code)', 'Verified identity or rejection'),
                 alt(('[identity invalid]', [db('Record sign-in rejection', 'Rejected; no session')]),
                     ('[verified email available]', [
                         db('Find user by verified email', 'User or no account'),
                         opt('[first sign-in]', [db('Create account for verified email', 'User')]),
                         db('Create session for same user identity', 'AuthSession')]))],
             public=True, google_consent=True, participants={'g': ': GoogleIdentityProvider'},
             trigger='Complete Google authorization and return code'),
        flow('Complete Onboarding and Update Profile', 'IV 3.1.4', 'III 3.2.3', 'User',
             'AuthenticationController', 'AccountService', 'updateProfile(input)', [], session_only=True,
             trigger='Submit display name and profile', choices=[
                 choice('[first onboarding]', 'completeOnboarding(input)', 'completeOnboarding(input)',
                        [db('Save display name and avatar of signed-in user', 'Profile completed')]),
                 choice('[profile update]', 'updateProfile(input)', 'updateProfile(input)',
                        [db('Save own profile', 'Own profile updated')])]),
        flow('Sign Out', 'IV 3.1.5', 'III 3.2.4', 'User',
             'AuthenticationController', 'AuthenticationService', 'revokeSession(sessionId)', entry='signOut(sessionId)', steps=[
                 db('Revoke current session', 'Session ended')], session_only=True,
             display='Return to sign-in page'),
        flow('View Unauthorized and Session Expired Pages', 'IV 3.1.6', 'III 3.2.5; FR-02, FR-151',
             'User', 'AuthenticationController', 'AuthenticationService', 'validateSession(token)', entry='currentSession(token)', steps=[
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
        project('View Project List and Overview', 'IV 3.2.3', 'listForUser(userId)', [], actor='User', session_only=True,
                trigger='Open projects', choices=[
                    choice('[project list]', 'listProjects()', 'listForUser(userId)',
                           [db('List only projects with user membership and pending invitations', 'Project list')]),
                    choice('[project selected]', 'getOverview(projectId)', 'getOverview(projectId)',
                           [db('Read authorized project overview', 'Project overview')])]),
        project('Update Archive or Complete Project', 'IV 3.2.4', 'update(projectId, input)', [],
                trigger='Edit, archive or complete project', choices=[
                    choice('[edit selected]', 'update(projectId, input)', 'update(projectId, input)', [
                        db('Read current project state', 'Project state'),
                        alt(('[archived: write blocked]', []), ('[writable project]', [
                            db('Save project information; record change in audit log', 'Project updated')]))]),
                    choice('[archive selected]', 'archive(projectId)', 'archive(projectId)', [
                        db('Read current project state', 'Project state'),
                        alt(('[already archived]', []), ('[else: not archived]', [
                            db('Set project archived (read-only); record change in audit log', 'Archived project')]))]),
                    choice('[complete selected]', 'complete(projectId)', 'complete(projectId)', [
                        db('Read current project state', 'Project state'),
                        alt(('[archived: write blocked]', []), ('[writable project]', [
                            db('Set project completed; record change in audit log', 'Completed project')]))])]),
        project('Manage Members and Invitations', 'IV 3.2.5', 'changeRole(memberId, role)', [], service='MembershipService',
                participants={'i': ': InvitationService'}, trigger='Invite, change role or remove member', choices=[
                    choice('[invite]', 'inviteMember(projectId, email, role)', 'invite(projectId, email, role)',
                           to='i', result='Pending invitation or rejection'),
                    choice('[change role]', 'changeRole(memberId, role)', 'changeRole(memberId, role)', [
                        db('Read project state and active managers', 'Access context'),
                        alt(('[archived or last active PM loses role]', []), ('[change permitted]', [
                            db('Save member role; append audit', 'Role updated')]))]),
                    choice('[remove member]', 'removeMember(memberId)', 'remove(memberId)', [
                        db('Read project state and active managers', 'Access context'),
                        alt(('[archived or last active PM]', []), ('[removal permitted]', [
                            db('Remove membership; append audit', 'Member removed')]))])]),
        project('Manage Documents', 'IV 3.2.6', 'list(projectId)', [], actor='Researcher', service='DocumentService',
                trigger='Upload, download or delete document', choices=[
                    choice('[upload]', 'uploadDocument(projectId, input)', 'add(projectId, input)', [
                        db('Read project state', 'Writable status'),
                        alt(('[project archived]', []), ('[writable project]', [db('Store document; append audit', 'Document stored')]))]),
                    choice('[download]', 'downloadDocument(documentId)', 'download(documentId)', [
                        db('Read authorized document', 'Document file')]),
                    choice('[delete confirmed]', 'deleteDocument(documentId)', 'delete(documentId)', [
                        db('Read project state', 'Writable status'),
                        alt(('[project archived]', []), ('[writable project]', [db('Delete document; append audit', 'Document removed')]))])]),
        project('Manage Project Integrations and Notification Preferences', 'IV 3.2.7', 'configure(input)', [], service='IntegrationService',
                participants={'p': ': NotificationPreferenceService', 'x': ': NotificationChannel'},
                trigger='Change delivery channel or notification groups', choices=[
                    choice('[connect channel]', 'configureIntegration(projectId, input)', 'configure(input)', [
                        db('Read project state', 'Writable status'),
                        alt(('[project archived]', []), ('[project writable]', [
                            db('Save integration with sealed secret reference; append audit', 'ProjectIntegration')]))]),
                    choice('[test channel]', 'testIntegration(integrationId)', 'test(integrationId)', [
                        db('Read integration and sealed reference', 'ProjectIntegration'),
                        call('s', 'x', 'deliver(recipient, message)', 'Delivery test result')]),
                    choice('[remove channel]', 'removeIntegration(integrationId)', 'remove(integrationId)', [
                        db('Read project state', 'Writable status'),
                        alt(('[project archived]', []), ('[project writable]', [
                            db('Remove integration and sealed reference; append audit', 'Integration removed')]))]),
                    choice('[set notification groups]', 'setNotificationPreferences(projectId, input)', 'update(input)',
                           to='p', result='NotificationPreference')]),
        project('Accept or Decline Invitation', 'IV 3.2.8', 'accept(invitationId)', [],
                actor='User', service='InvitationService', session_only=True, trigger='Respond to invitation', choices=[
                    choice('[accept]', 'acceptInvitation(invitationId)', 'accept(invitationId)', [
                        db('Load invitation and verify recipient', 'Invitation and expiry'),
                        alt(('[expired, cancelled or recipient mismatch]', []), ('[valid invitation]', [
                            db('Create membership with invited role; append audit', 'Membership')]))]),
                    choice('[decline]', 'declineInvitation(invitationId)', 'decline(invitationId)', [
                        db('Load invitation and verify recipient', 'Invitation and expiry'),
                        alt(('[expired, cancelled or recipient mismatch]', []), ('[valid invitation]', [
                            db('Close invitation as declined; append audit', 'Invitation declined')]))])]),
        project('Resend or Cancel Invitation', 'IV 3.2.9', 'resend(invitationId)', [], service='InvitationService',
                trigger='Resend or cancel pending invitation', choices=[
                    choice('[resend]', 'resendInvitation(invitationId)', 'resend(invitationId)', [
                        db('Read pending invitation and project state', 'Pending and writable status'),
                        alt(('[not pending or project archived]', []), ('[pending and writable]', [
                            db('Renew expiry; record resend; append audit', 'Invitation resent')]))]),
                    choice('[cancel]', 'cancelInvitation(invitationId)', 'cancel(invitationId)', [
                        db('Read pending invitation and project state', 'Pending and writable status'),
                        alt(('[not pending or project archived]', []), ('[pending and writable]', [
                            db('Close invitation as cancelled; append audit', 'Invitation cancelled')]))])]),
        project('Transfer Ownership', 'IV 3.2.10', 'transferOwnership(projectId, userId)', [
            db('Check caller ownership and target active membership', 'Transfer eligibility'),
            alt(('[not owner, archived or inactive target]', []), ('[transfer eligible]', [
                db('Transfer ownership; retain an active PM', 'New owner'),
                db('Append ownership transfer audit', 'Audit entry')]))], service='MembershipService'),
        project('Delete Project', 'IV 3.2.11', 'delete(projectId)', entry='deleteProject(projectId, confirmation)',
                trigger='Confirm project deletion', steps=[
            db('Verify project owner and confirmation', 'Deletion eligibility'),
            alt(('[not owner or not confirmed]', []), ('[confirmed by owner]', [
                db('Record deletion audit and delete project', 'Deletion recorded')]))]),
        project('View Project Activity and Audit Log', 'IV 3.2.12', 'listActivity(projectId, filter)', trigger='Open activity log', steps=[
            db('Query project-scoped append-only audit', 'Authorized activity entries')], actor='Researcher'),
        project('Configure Project Settings and Monthly Budget', 'IV 3.2.13', 'configure(settings)',
                entry='configure(projectId, settings)', trigger='Save project settings', steps=[
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
        data('Upload Dataset', 'IV 3.3.2', 'createDataset(input)', entry='upload(input)', trigger='Upload tabular file', steps=[
            db('Validate format, size and readable table', 'SR-01 / SR-02 / SR-07 result'),
            alt(('[file invalid]', []), ('[valid tabular file]', [
                call('s', 'v', 'create(datasetId, source)', 'Immutable version with content hash'),
                db('Save dataset and platform location', 'Dataset with first version')]))],
             participants={'v': ': DatasetVersionService'}),
        data('View Dataset Detail', 'IV 3.3.3', 'getDetail(datasetId)', entry='getDataset(datasetId)', trigger='Open dataset', steps=[
            db('Read dataset versions and location', 'Immutable versions and location'),
            db('Read code-computed profile and columns', 'Metadata only; no local rows')], actor='Researcher'),
        data('Manage Data Connection and Import', 'IV 3.3.4', 'importData(connection)', entry='importData(connectionId)',
             trigger='Save connection and import table', steps=[
            call('s', 'k', 'seal(credential)', 'SecretRef only'),
            db('Save connection with sealed reference', 'DataConnection'),
            call('s', 'x', 'test()', 'Source validation result; internal hosts blocked'),
            alt(('[unauthorized or internal host]', []), ('[authorized source]', [
                call('s', 'x', 'openRows(source, maxRows)', 'Row stream of selected table'),
                call('s', 'v', 'create(datasetId, source)', 'New immutable version and hash'),
                db('Save version with platform location', 'Imported version')]))],
             participants={'k': ': SecretService', 'x': ': Connector', 'v': ': DatasetVersionService'}),
        data('Rename or Delete Dataset', 'IV 3.3.5', 'rename(datasetId, name)', [],
             trigger='Rename or delete dataset', choices=[
                 choice('[rename]', 'renameDataset(datasetId, name)', 'rename(datasetId, name)', [
                     db('Read dataset and writable project', 'Dataset context'),
                     alt(('[project archived]', []), ('[writable project]', [db('Save dataset name; append audit', 'Name updated')]))]),
                 choice('[delete confirmed]', 'deleteDataset(datasetId)', 'delete(datasetId)', [
                     db('Read dataset references and writable project', 'Deletion context'),
                     alt(('[archived or accepted artifact depends on dataset]', []), ('[else: deletion allowed]', [
                         db('Delete dataset; append audit', 'Dataset deleted')]))])]),
        data('Upload New Dataset Version', 'IV 3.3.6', 'addVersion(datasetId, input)', entry='uploadVersion(datasetId, input)',
             trigger='Upload new file for dataset', steps=[
            db('Validate writable project and uploaded table', 'Validation result'),
            alt(('[invalid or archived]', []), ('[valid upload]', [
                call('s', 'v', 'create(datasetId, source)', 'New version; old versions unchanged'),
                db('Persist version and content hash', 'New immutable version')]))],
             participants={'v': ': DatasetVersionService'}),
        data('Download or Preview Dataset Version', 'IV 3.3.7', 'preview(versionId)', [],
             trigger='Preview or download version', choices=[
                 choice('[preview]', 'preview(versionId)', 'preview(versionId)', [
                     db('Read pinned version and data location', 'Version location'),
                     alt(('[location local]', []), ('[platform location]', [db('Read authorized preview rows', 'TablePreview')]))]),
                 choice('[download]', 'download(versionId)', 'download(versionId)', [
                     db('Read pinned version and data location', 'Version location'),
                     alt(('[location local]', []), ('[platform location]', [db('Read authorized version file', 'Version file')]))])]),
        data('Browse and Preview Connection Source', 'IV 3.3.8', 'browse(connectionId, schema)', [],
             participants={'x': ': Connector'}, trigger='Browse or preview source', choices=[
                 choice('[browse]', 'browseConnection(connectionId, schema)', 'browse(connectionId, schema)', [
                     db('Load connection secret reference', 'DataConnection without credentials'),
                     call('s', 'x', 'test()', 'Source eligibility'),
                     alt(('[source rejected]', []), ('[source authorized]', [
                         call('s', 'x', 'listTables(schema, search, limit)', 'Tables and files')]))]),
                 choice('[preview selected source]', 'previewSource(connectionId, source)', 'previewSource(connectionId, source)', [
                     db('Load connection secret reference', 'DataConnection without credentials'),
                     call('s', 'x', 'openRows(source, maxRows)', 'Preview rows')])]),
        data('Rename Test or Delete Data Connection', 'IV 3.3.9', 'testConnection(connectionId)', [],
             participants={'x': ': Connector'}, trigger='Rename, test or delete connection', choices=[
                 choice('[rename]', 'renameConnection(connectionId, name)', 'renameConnection(connectionId, name)', [
                     db('Read connection and project state', 'Connection context'),
                     alt(('[project archived]', []), ('[writable project]', [db('Save connection name', 'Updated metadata')]))]),
                 choice('[test]', 'testConnection(connectionId)', 'testConnection(connectionId)', [
                     db('Load connection secret reference', 'DataConnection without credentials'),
                     call('s', 'x', 'test()', 'Connection test result')]),
                 choice('[delete confirmed]', 'deleteConnection(connectionId)', 'deleteConnection(connectionId)', [
                     db('Read connection and project state', 'Connection context'),
                     alt(('[project archived]', []), ('[writable project]', [
                         db('Delete connection and sealed reference', 'Connection removed')]))])]),
        data('Connect Google Sheets and Drive', 'IV 3.3.10', 'authorizeGoogle(projectId)', entry='connectGoogle(projectId)',
             trigger='Connect Google Sheets or Drive', steps=[
            call('s', 'g', 'authorize(clientId, scope)', 'Authorization outcome'),
            alt(('[consent denied]', []), ('[consent granted]', [
                db('Store sealed grant reference for project', 'Grant reference only'),
                call('s', 'x', 'listTables(schema, search, limit)', 'Authorized sheets and files'),
                call('s', 'x', 'openRows(source, maxRows)', 'Rows of selected source'),
                db('Create immutable dataset version and hash', 'DatasetVersion')]))],
             participants={'g': ': GoogleIdentityProvider', 'x': ': GoogleSheetsConnector'}),
        flow('Pair a Local Node and Register Local Data', 'IV 3.3.11', LOCAL_SOURCE, 'Researcher',
             'DataController', 'LocalNodeService', 'pair(projectId, code)', [],
             participants={'n': ': LocalNodeAgent'}, custom_tree=[
                 {'from': 'u', 'to': 'w', 'label': 'Open Local Node page; request pairing code'},
                 {'from': 'w', 'to': 'c', 'label': 'requestPairingCode(projectId)'},
                 guarded('pair node', [
                     {'from': 'c', 'to': 's', 'label': 'issuePairingCode(projectId)'},
                     db('Store pairing code digest and expiry', 'Pairing code'),
                     finish('Pairing code', 'Show pairing code'),
                     {'from': 'u', 'to': 'n', 'label': 'Enter pairing code in Local Node app'},
                     {'from': 'n', 'to': 'c', 'label': 'pairNode(code)'},
                     {'from': 'c', 'to': 's', 'label': 'pair(projectId, code)'},
                     db('Verify code; register Node with token digest', 'LocalNode or rejection'),
                     alt(('[code invalid or expired]', [
                             {'from': 's', 'to': 'c', 'label': 'Pairing rejected', 'reply': True},
                             {'from': 'c', 'to': 'n', 'label': 'Pairing rejected', 'reply': True}]),
                         ('[code valid]', [
                             {'from': 's', 'to': 'c', 'label': 'Paired LocalNode', 'reply': True},
                             {'from': 'c', 'to': 'n', 'label': 'Node token; Platform keeps digest only', 'reply': True},
                             event('c', 'w', 'Node paired update'),
                             event('w', 'u', 'Show MSG-17: Local Node paired'),
                             opt('[datasets found in monitored folder]', [
                                 {'from': 'n', 'to': 'c', 'label': 'proposeDatasets(nodeId, manifests)'},
                                 {'from': 'c', 'to': 's', 'label': 'registerDatasets(nodeId, manifests)'},
                                 db('Create local DatasetVersions; no rows stored', 'Local DatasetVersions'),
                                 {'from': 's', 'to': 'c', 'label': 'Registered datasets', 'reply': True},
                                 {'from': 'c', 'to': 'n', 'label': 'Proposals recorded', 'reply': True}])]))])]),
        flow('Execute Local Job and Release Aggregate', 'IV 3.3.12', LOCAL_SOURCE + '; Figure IV-12', 'Researcher',
             'DataController', 'LocalNodeService', 'route(job)', [
            db('Read pinned version and Node status', 'Local job eligibility'),
            alt(('[Node revoked]', [db('Record job rejection: Node revoked', 'Rejection reason (MSG-19)')]),
                ('[Node offline and job blocks work]', [db('Set waiting(node_offline); retain other work', 'Wait state and one combined notice')]),
                ('[Node online]', [
                    {'from': 's', 'to': 'n', 'label': 'runJob(job)'},
                    alt(('[pinned hash mismatch]', [
                            {'from': 'n', 'to': 's', 'label': 'Rejected: hash mismatch', 'reply': True},
                            db('Record rejection; propose new version', 'Mismatch reason')]),
                        ('[hash matches: raw result stays local]', [
                            call('n', 'r', 'check(job, result)', 'Firewall, rounding, disclosure, differencing, probe checks'),
                            alt(('[probe exhausted or release rejected]', [
                                    {'from': 'n', 'to': 's', 'label': 'Sanitized rejection; no aggregate', 'reply': True},
                                    db('Record gap and rejection reason', 'Run may continue other work')]),
                                ('[strict mode: new number kind]', [
                                    {'from': 'n', 'to': 's', 'label': 'Release approval required; no raw result', 'reply': True},
                                    db('Create release review item', 'Await Researcher or PM approval')]),
                                ('[release allowed]', [
                                    call('n', 'r', 'recordRelease(release)', 'Release reference'),
                                    {'from': 'n', 'to': 's', 'label': 'Released aggregate only', 'reply': True},
                                    db('Store copy of approved release', 'Released aggregate')]))]))]))],
             participants={'n': ': LocalNodeAgent', 'r': ': ReleaseGate'},
             system_trigger=': ExecutionEngine', display='Show released aggregate, gap or wait state'),
        flow('Handle an Offline or Revoked Local Node', 'IV 3.3.13', LOCAL_SOURCE, 'Project Manager',
             'DataController', 'LocalNodeService', 'revoke(nodeId)', [],
             participants={'t': ': RunOrchestrator', 'n': ': LocalNodeAgent', 'p': ': NotificationService', 'e': ': ExecutionEngine'},
             custom_tree=[
                 {'from': 'e', 'to': 's', 'label': 'route(job)'},
                 db('Read Node status and last seen', 'Node status'),
                 alt(('[Node revoked]', [
                         db('Record job rejection and reason', 'Rejection'),
                         {'from': 's', 'to': 'e', 'label': 'Job rejected: Node revoked (MSG-19)', 'reply': True}]),
                     ('[Node offline]', [
                         db('Set run waiting(node_offline); keep other work', 'Waiting run'),
                         event('s', 'p', 'create(nodeOfflineEvent) (MSG-18)'),
                         {'from': 's', 'to': 'e', 'label': 'Job queued until Node returns', 'reply': True}]),
                     ('[Node online]', [
                         call('s', 'n', 'runJob(job)', 'Job accepted'),
                         {'from': 's', 'to': 'e', 'label': 'Job routed', 'reply': True}])),
                 opt('[offline Node reconnects]', [
                     event('n', 's', 'heartbeat(nodeId)'),
                     db('Mark Node online; release queued job', 'Queued job released'),
                     event('s', 't', 'resume(runId)')]),
                 {'from': 'u', 'to': 'w', 'label': 'Revoke Local Node'},
                 {'from': 'w', 'to': 'c', 'label': 'revokeNode(nodeId)'},
                 guarded('revoke node', [
                     {'from': 'c', 'to': 's', 'label': 'revoke(nodeId)'},
                     db('Set revoked_at; reject pending local jobs', 'Node revoked; published artifacts unchanged'),
                     finish('Node revoked', 'Show Node revoked; published artifacts stay readable')])]),
    ]),
    dict(folder='04-research-run-orchestration', slug='Research-Run-Orchestration',
         title='Research Run Orchestration', flows=[
        run('Start Research Run', 'IV 3.4.2', 'start(caseId)', [
            db('Check monthly budget and active run atomically', 'Start eligibility'),
            alt(('[budget blocked or active run exists]', []), ('[start allowed]', [
                db('Create Run with dataset_first and pinned case', 'Run created'),
                event('s', 'e', 'profile(versionId)')]))],
             participants={'e': ': DatasetEngine'}, result='Run or start rejection', display='Show Run Studio or start error'),
        run('Monitor Run in Run Studio', 'IV 3.4.3', 'getSnapshot(runId)', entry='getRun(runId)', trigger='Open run in Run Studio', steps=[
            db('Read run state, stages and artifacts', 'Current snapshot'),
            loop('[while authorized monitoring is open]', [
                event('t', 's', 'onRunEvent(event)'),
                event('s', 'c', 'pushUpdate(event)'),
                event('c', 'w', 'Stream state, trace and artifact updates')])],
             participants={'t': 'Run Event Stream'}, display='Show latest run state'),
        flow('Answer Gate', 'IV 3.4.4', 'III 3.2.3.3; FR-28–30', 'Researcher',
             'DecisionController', 'DecisionService', 'answer(itemId, option)', [
            db('Read item status and answer authority', 'Answer eligibility'),
            alt(('[not eligible or item no longer pending]', []), ('[decision accepted]', [
                db('Record answer; append decision log', 'Decision recorded'),
                opt('[no other blocking item]', [call('s', 't', 'resume(runId)', 'Run running')])]))],
             participants={'t': ': RunOrchestrator'}, trigger='Answer waiting item'),
        run('Accept Send Back or Rerun Stage', 'IV 3.4.5', 'acceptVersion(objectId)', [],
            trigger='Accept, send back or rerun stage', choices=[
                choice('[accept]', 'acceptObject(objectId)', 'acceptVersion(objectId)', [
                    db('Read version checks and acceptance policy', 'Stage eligibility'),
                    alt(('[checks or policy reject action]', []), ('[accept eligible version]', [
                        db('Accept version; keep accepted content immutable; append decision log', 'Accepted version')]))]),
                choice('[send back with reason]', 'requestRevision(objectId, reason)', 'requestRevision(objectId, reason)', [
                    db('Read version state', 'Stage eligibility'),
                    alt(('[version not reviewable]', []), ('[else: reviewable]', [
                        db('Record reason and create draft successor; append decision log', 'New draft version')]))]),
                choice('[rerun]', 'rerunStage(stageRunId)', 'rerunStage(stageRunId)', [
                    db('Read stage state and budget', 'Rerun eligibility'),
                    alt(('[run ended or budget blocked]', []), ('[else: rerun allowed]', [
                        db('Create next version; mark downstream stale; append decision log', 'Versioned rerun scheduled')]))])]),
        run('Cancel and Synchronize Run', 'IV 3.4.6', 'cancel(runId)', [], trigger='Cancel or sync run', choices=[
            choice('[sync]', 'syncRun(runId)', 'syncRun(runId)', [
                db('Read authoritative run and engine state', 'Current state')]),
            choice('[cancel]', 'cancel(runId)', 'cancel(runId)', [
                db('Check creator-or-PM rights and run state', 'Control eligibility'),
                alt(('[run ended or caller not creator or PM]', []), ('[else: cancel allowed]', [
                    db('End run as cancelled; keep accepted objects', 'ended(cancelled)'),
                    db('Close waiting items and append audit', 'Cancellation recorded')]))])]),
        run('Raise Token Budget', 'IV 3.4.7', 'raiseRunBudget(runId, amount)', entry='raiseTokenBudget(runId, amount)',
            trigger='Raise run token budget', steps=[
            db('Read run state, waiting reason and new amount', 'Budget review context'),
            alt(('[run not waiting for budget review or amount invalid]', []), ('[else: waiting for budget review]', [
                db('Save increased token budget; append audit', 'Updated token budget'),
                db('Read monthly project spending restriction', 'Monthly budget status'),
                alt(('[monthly budget blocked]', [db('Keep run waiting for spending approval', 'Run waiting')]),
                    ('[else: monthly budget available]', [call('s', 't', 'resume(runId)', 'Run running')]))]))],
             actor='Project Manager', service='BudgetService', participants={'t': ': RunOrchestrator'}),
        run('View Review Rounds Diffs and Artifacts', 'IV 3.4.8', 'getReviewHistory(stageRunId)', trigger='Open review rounds', steps=[
            db('Read authorized versioned review rounds', 'Findings and revision history'),
            db('Read version diffs and artifact references', 'Review details')]),
        run('Comment On Run', 'IV 3.4.9', 'add(input)', entry='addComment(input)', trigger='Write comment', steps=[
            db('Read project state and object anchor', 'Comment context'),
            alt(('[archived or anchor invalid]', []), ('[else: comment allowed]', [
                db('Save comment with anchor', 'Comment')]))],
             service='CommentService', repository='CommentRepository'),
        run('View Run List', 'IV 3.4.10', 'listRuns(projectId, filter)', trigger='Open run list', steps=[
            db('List runs of authorized project', 'Runs and current states')]),
        run('View Recovery State', 'IV 3.4.11', 'getRecoveryState(runId)', trigger='Open recovery state', steps=[
            db('Read failed checks, budget and recovery trace', 'Recovery state and reason'),
            alt(('[repair within item budget]', [db('Read system repair progress', 'Retrying details')]),
                ('[item share exhausted]', [db('Read needs-you item and prior attempts', 'Human action required')]),
                ('[unrecoverable or missing model / key]', [db('Read failed_technical reason', 'No sample output')]))]),
        run('Download and Compare Artifacts', 'IV 3.4.12', 'downloadArtifact(versionId)', [],
            trigger='Download or compare artifact', choices=[
                choice('[download]', 'downloadArtifact(versionId)', 'downloadArtifact(versionId)', [
                    db('Read selected immutable artifact version', 'Artifact file')]),
                choice('[compare]', 'compareArtifacts(versionA, versionB)', 'compareArtifacts(versionA, versionB)', [
                    db('Read two artifact versions of the same object', 'Version differences')])]),
        run('View Iteration Summary', 'IV 3.4.13', 'getIterationSummary(stageRunId)', trigger='Open iteration summary', steps=[
            db('Read stage versions, reasons and review events', 'What changed and why')]),
        run('Edit or Delete Comment', 'IV 3.4.14', 'edit(commentId, text)', [], service='CommentService',
            repository='CommentRepository', trigger='Edit or delete own comment', choices=[
                choice('[edit]', 'editComment(commentId, text)', 'edit(commentId, text)', [
                    db('Check comment author and project state', 'Ownership and writable status'),
                    alt(('[not author or project archived]', []), ('[else: author]', [db('Save own comment edit', 'Updated comment')]))]),
                choice('[delete confirmed]', 'deleteComment(commentId)', 'delete(commentId)', [
                    db('Check comment author and project state', 'Ownership and writable status'),
                    alt(('[not author or project archived]', []), ('[else: author]', [db('Delete own comment', 'Comment removed')]))])]),
        flow('Approve Additional Spending', 'IV 3.4.15',
             'Report7 (3) III 3.2.6; FR-88–93, FR-243–248; SR-03, SR-04', 'Project Manager',
             'RunController', 'BudgetService', 'approveSpending(itemId)', [],
             participants={'t': ': RunOrchestrator', 'p': ': NotificationService'}, custom_tree=[
                 {'from': 't', 'to': 's', 'label': 'recordUsage(runId, amount)'},
                 db('Append cost entry; read monthly spend', 'Spend against thresholds'),
                 alt(('[budget limit reached]', [
                         db('Block new AI work; create spending item with deadline', 'Spending item'),
                         event('s', 'p', 'create(spendingRequestedEvent)'),
                         {'from': 's', 'to': 't', 'label': 'Run waits for spending decision', 'reply': True}]),
                     ('[warning threshold reached]', [
                         db('Create budget_warning alert', 'Spending alert'),
                         event('s', 'p', 'create(budgetWarningEvent)'),
                         {'from': 's', 'to': 't', 'label': 'Continue with warning', 'reply': True}]),
                     ('[else: within budget]', [
                         {'from': 's', 'to': 't', 'label': 'Continue', 'reply': True}])),
                 alt(('[Project Manager decides before deadline]', [
                         {'from': 'u', 'to': 'w', 'label': 'Open spending item; approve or reject'},
                         {'from': 'w', 'to': 'c', 'label': 'reviewSpending(itemId, approve)'},
                         {'from': 'c', 'to': 'a', 'label': 'requireRole(user, project, approve spending)'},
                         {'from': 'a', 'to': 'c', 'label': 'Project Manager check result', 'reply': True},
                         alt(('[not a Project Manager]', denied()),
                             ('[approve]', [
                                 {'from': 'c', 'to': 's', 'label': 'approveSpending(itemId)'},
                                 db('Record approval; lift budget block', 'Approved item'),
                                 event('s', 't', 'resume(runId)'),
                                 finish('Spending approved', 'Show work resumed')]),
                             ('[reject]', [
                                 {'from': 'c', 'to': 's', 'label': 'rejectSpending(itemId)'},
                                 db('Close item as rejected', 'Rejected item'),
                                 event('s', 't', 'endWithGaps(runId, reason)'),
                                 finish('Spending rejected', 'Show run ended with gaps')]))]),
                     ('[deadline passes without decision]', [
                         {'from': 't', 'to': 's', 'label': 'expireSpending(itemId)'},
                         db('Close item unanswered', 'Expired item'),
                         {'from': 's', 'to': 't', 'label': 'End run with gaps; no placeholder output', 'reply': True}]))]),
        flow('Review and Approve a Research Dossier', 'IV 3.4.16',
             'Report7 (3) III 3.7; FR-94–96, FR-249–251; BR-62, BR-63, BR-79', 'Reviewer',
             'RunController', 'DossierService', 'approve(dossierId)', [],
             participants={'t': ': RunOrchestrator'}, custom_tree=[
                 {'from': 't', 'to': 's', 'label': 'createFromAccepted(packId)'},
                 db('Pin accepted EvidenceBundle and PaperPack versions with hashes', 'Dossier version awaiting approval'),
                 opt('[earlier Dossier version exists]', [
                     db('Mark earlier version superseded; approvals not carried over', 'Superseded version')]),
                 {'from': 's', 'to': 't', 'label': 'New Dossier version (MSG-54)', 'reply': True},
                 {'from': 'u', 'to': 'w', 'label': 'Open Dossier and approve'},
                 {'from': 'w', 'to': 'c', 'label': 'approveDossier(dossierId)'},
                 guarded('approve dossier', [
                     {'from': 'c', 'to': 's', 'label': 'approve(dossierId)'},
                     db('Read approval policy, author and version state', 'Approval context'),
                     alt(('[self-approval not allowed or version superseded]',
                          finish('Approval rejected', 'Show MSG-52 or superseded notice')),
                         ('[approval policy satisfied]', [
                             db('Record Approval for this version; append audit', 'Approval'),
                             finish('Approval', 'Show Dossier approved')]))])]),
        flow('Export a Research Dossier', 'IV 3.4.17',
             'Report7 (3) III 3.7; FR-97, FR-98; BR-64', 'Researcher',
             'RunController', 'DossierService', 'exportApproved(dossierId, format)', [],
             participants={'q': ': DecisionService'}, custom_tree=[
                 {'from': 'u', 'to': 'w', 'label': 'Export Dossier(format)'},
                 {'from': 'w', 'to': 'c', 'label': 'export(dossierId, format)'},
                 guarded('export dossier', [
                     {'from': 'c', 'to': 's', 'label': 'exportApproved(dossierId, format)'},
                     db('Read approval state and reference hashes', 'Dossier version'),
                     alt(('[version not approved]', finish('Export rejected', 'Show MSG-55: approval needed')),
                         ('[reference hash mismatch]', finish('Export blocked', 'Show integrity error')),
                         ('[approved and hashes valid]', [
                             call('s', 'q', 'createRequest(pinned export)', 'Pinned decision status'),
                             alt(('[export not confirmed yet]',
                                  finish('Export pending', 'Show MSG-39: confirm pinned export')),
                                 ('[user confirmed export]', [
                                     db('Build package; append export history and audit', 'Export package'),
                                     finish('Export package', 'Download Dossier package')]))]))])]),
        # 2026-11-03: Must use cases of Report7 III without a sequence (option a review).
        flow('Amend a Research Case', 'IV 3.4.18', 'III 3.2.3; UC-28; FR-17', 'Researcher',
             'RunController', 'ResearchCaseService', 'amend(caseId, change, reason)', entry='amendCase(input)', steps=[
            db('Read case version and confirmation state', 'Case context'),
            alt(('[input invalid or reason missing]', []),
                ('[case not confirmed yet]', [db('Update draft case', 'Updated draft case')]),
                ('[else: case confirmed]', [
                    db('Store new case version with reason; append amendment event', 'Amended case version'),
                    db('Keep earlier runs pinned to their case version', 'Pinned runs unchanged')]))],
            repository='ResearchCaseRepository', trigger='Submit case change with reason',
            result='Case version', display='Show amended case or error'),
    ]),
]


def engine(title, slot, service, operation, steps, **kw):
    # Stages and the review loop are scheduled by the orchestrator (Start Research Run, FR-14,
    # FR-71), not started by a user click; the user only sees the published result.
    kw.setdefault('system_trigger', ': RunOrchestrator')
    kw.setdefault('display', 'Show stage result and pending decisions')
    return flow(title, slot, 'IV 3.5; FE-06–11; FR-37–78', 'Researcher',
                'RunController', service, operation, steps, **kw)


GROUPS += [
    dict(folder='05-research-engines', slug='Research-Engines', title='Research Engines', flows=[
        engine('Dataset Stage', 'IV 3.5.2', 'DatasetEngine', 'profile(versionId)', [
            db('Read dataset metadata and pinned version', 'Dataset context'),
            call('s', 'h', 'computeProfile(versionId)', 'Profile, dictionary and fitness computed in code'),
            call('s', 'q', 'createRequest(confirm observation unit and structure)', 'Pinned decision status'),
            alt(('[confirmation pending]', [db('Persist draft; no split before user confirmation', 'Waiting for pinned answer')]),
                ('[confirmed by user]', [
                    call('s', 'h', 'createSplit(snapshotId, policy)', 'Power-based split; duplicate and shift checks'),
                    call('s', 'h', 'checkContract(snapshot)', 'Contract result'),
                    alt(('[contract red]', [db('Record repair tasks; respect item budget', 'Draft with checks_red')]),
                        ('[contract green]', [call('s', 'r', 'review(snapshot)', 'Verified review findings'),
                            db('Publish DatasetSnapshot version for acceptance', 'Snapshot with fitness and known risks')]))]))],
               participants={'h': ': Harness', 'q': ': DecisionService', 'r': ': IndependentReviewService'}),
        engine('Hypothesis Stage', 'IV 3.5.3', 'HypothesisEngine', 'propose(snapshot)', [
            db('Read accepted pinned DatasetSnapshot', 'Snapshot'),
            call('s', 'l', 'search(query)', 'Sources, prior art and source failures'),
            db('Update LiteratureBase with source provenance', 'LiteratureBase version'),
            db('Draft hypotheses with comparator and rule', 'Portfolio draft'),
            call('s', 'h', 'validatePortfolio(set)', 'Comparator, baseline and limit checks'),
            alt(('[invalid hypothesis or weak baseline]', [db('Record repair need', 'Not accepted')]),
                ('[portfolio valid]', [call('s', 'q', 'createRequest(select hypotheses and primary)', 'Pinned selection status'),
                    alt(('[selection pending]', [db('Keep selection waiting', 'No automatic primary choice')]),
                        ('[user selected at least two and primary]', [db('Publish selected HypothesisSet version', 'Selected portfolio')]))]))],
               participants={'l': ': ScholarlySource', 'h': ': Harness', 'q': ': DecisionService'}),
        engine('Experiment Design Stage', 'IV 3.5.4 / Figure IV-10',
               'ExperimentDesignEngine', 'build(hypothesisSet)', [
            db('Read pinned hypotheses and snapshot', 'Accepted input versions'),
            db('Draft plan, pattern versions and pipeline order', 'AnalysisPlan draft'),
            call('s', 'h', 'enforcePipelineOrder(plan)', 'Pipeline guard result'),
            call('s', 'h', 'rehearseOnTwin(plan)', 'Golden outputs and contract checks'),
            alt(('[checks red]', [db('Keep plan draft for repairs', 'No Lock written')]),
                ('[checks green]', [call('s', 'q', 'createRequest(lock plan)', 'Pinned lock request'),
                    db('Publish AnalysisPlan version waiting for the user to lock it', 'Plan waiting for lock; nobody locks for user')]))],
               participants={'h': ': Harness', 'q': ': DecisionService'}),
        engine('Independent Review and Revision Rounds', 'IV 3.5.7',
               'IndependentReviewService', 'review(objectVersion)', [
            call('s', 'h', 'checkContract(objectVersion)', 'Contract status'),
            alt(('[contract red]', [db('Record contract repair tasks', 'Not ready for independent review')]),
                ('[contract green]', [
                    loop('[initial review, or confirmed blockers remain and revision round < 2]', [
                        {'kind': 'par', 'branches': [
                            ('[guard A: fresh isolated context]', call('s', 'g1', 'review(object, fields)', 'Anchored findings')),
                            ('[guard B: fresh isolated context]', call('s', 'g2', 'review(object, fields)', 'Anchored findings'))]},
                        call('s', 'h', 'verifyFindings(findings)', 'Confirmed, plausible or rejected findings'),
                        alt(('[confirmed blockers and round available]', [
                            call('s', 'm', 'revise(objectId, findings)', 'Repaired version; confirmed blockers only'),
                            call('s', 'h', 'recheckChangedFields(objectId)', 'New contract result')]),
                            ('[no confirmed blocker or round limit reached]', [db('Record major and minor findings and known risks', 'Review outcome')]))]),
                    db('Publish review record; unresolved evidence withheld', 'Version ready for acceptance policy')]))],
               participants={'h': ': Harness', 'g1': 'guardA : ReviewerPersona', 'g2': 'guardB : ReviewerPersona', 'm': ': MakerPersona'}),
        engine('Execution Stage', 'IV 3.5.5 / Figure IV-10',
               'ExecutionEngine', 'execute(lock)', [
            db('Read immutable Lock and pinned inputs', 'Locked program and split'),
            call('s', 'h', 'enforcePipelineOrder(plan)', 'Pipeline check'),
            alt(('[pipeline violates Lock]', [db('Block run or request pinned deviation', 'No silent algorithm change')]),
                ('[locked pipeline valid]', [
                    call('s', 'x', 'runTwin(lock)', 'Twin and permutation diagnostics'),
                    call('s', 'x', 'dryRun(lock)', 'Counts, types, missingness, convergence, time; no estimates'),
                    call('s', 'x', 'runConfirmatory(lock)', 'Job status; results stay hidden'),
                    call('s', 'h', 'checkDisclosureEligibility(lockId)', 'Disclosure eligibility'),
                    alt(('[disclosure checks fail]', [db('Record rejection; keep results hidden', 'No estimates exposed')]),
                        ('[manual disclosure and user has not approved]', [db('Keep pinned disclosure request pending', 'Results remain hidden')]),
                        ('[checks pass and auto or user approved]', [
                            db('Disclose all hypotheses of Lock; record time', 'Disclosed results'),
                            call('s', 'h', 'computeVerdicts(input)', 'Verdicts, grade and claim ceiling computed in code'),
                            db('Publish EvidenceBundle with replication package', 'Versioned EvidenceBundle')]))]))],
               participants={'h': ': Harness', 'x': ': IsolatedExecutor'}),
        engine('Paper Stage', 'IV 3.5.6', 'PaperEngine', 'draft(input)', [
            db('Read accepted bundle, plan, Lock, literature and log', 'Pinned input references'),
            call('s', 'h', 'renderNumbers(records)', 'Code-rendered tables and figures'),
            db('Build claims and manuscript within claim ceiling', 'PaperPack draft'),
            call('s', 'h', 'validateClaimsAndCitations(pack)', 'Claim, citation and checklist result'),
            alt(('[invalid claim or unresolved citation]', [db('Record repairs; do not publish invalid content', 'Draft with checks_red')]),
                ('[contract green]', [call('s', 'r', 'review(paperPack)', 'Independent findings and known risks'),
                    db('Publish PaperPack for acceptance', 'PaperPack version; no automatic submission')]))],
               participants={'h': ': Harness', 'r': ': IndependentReviewService'}),
        # 2026-11-03: user-facing Must use cases inside the stages (UC-38, UC-40, UC-43).
        flow('Build Literature Base', 'IV 3.5.8', 'III 3.4; UC-38; FR-43, FR-65; EX-04', 'Researcher',
             'LiteratureController', 'LiteratureService', 'search(query)', [],
             participants={'l': ': ScholarlySource'}, custom_tree=[
                 {'from': 'u', 'to': 'w', 'label': 'Search literature(query)'},
                 {'from': 'w', 'to': 'c', 'label': 'search(projectId, query)'},
                 guarded('edit literature base', [
                     {'from': 'c', 'to': 's', 'label': 'search(query)'},
                     call('s', 'l', 'search(query)', 'Metadata, abstracts and source failures'),
                     db('Append search log with protocol and source failures', 'Search log entry'),
                     alt(('[no eligible result]', finish('No eligible result', 'Show empty result and source failures')),
                         ('[else: results found]', [
                             db('Store candidate studies; no paywalled full text', 'Screening list'),
                             finish('Screening list', 'Show studies to screen')]))]),
                 {'from': 'u', 'to': 'w', 'label': 'Include or exclude studies with reason'},
                 {'from': 'w', 'to': 'c', 'label': 'screen(decisions)'},
                 guarded('edit literature base', [
                     {'from': 'c', 'to': 's', 'label': 'screen(decisions)'},
                     db('Save screening decisions and evidence cards as new Literature Base version', 'LiteratureBase version'),
                     finish('LiteratureBase version', 'Show updated Literature Base')])]),
        flow('Lock an Analysis Plan and Request a Deviation', 'IV 3.5.9',
             'III 3.5; UC-40; FR-48, FR-49, FR-56, FR-188, FR-189; LI-14', 'Researcher',
             'RunController', 'LockService', 'lock(planId)', [],
             participants={'t': ': RunOrchestrator', 'q': ': DecisionService'}, custom_tree=[
                 {'from': 'u', 'to': 'w', 'label': 'Lock AnalysisPlan'},
                 {'from': 'w', 'to': 'c', 'label': 'lockPlan(planId)'},
                 guarded('lock plan', [
                     {'from': 'c', 'to': 's', 'label': 'lock(planId)'},
                     db('Read plan checks, rehearsal outputs and lock request', 'Lock eligibility'),
                     alt(('[checks red or plan already locked]', finish('Lock rejected', 'Show lock error')),
                         ('[else: checks green and lock request pending]', [
                             db('Write Lock with hashes, snapshot version, split digest and actor; close lock request', 'Immutable Lock'),
                             event('s', 't', 'advance(runId)'),
                             finish('Lock', 'Show plan locked')]))]),
                 {'from': 'u', 'to': 'w', 'label': 'Request change to locked method with reason'},
                 {'from': 'w', 'to': 'c', 'label': 'requestDeviation(planId, change, reason)'},
                 guarded('request deviation', [
                     {'from': 'c', 'to': 's', 'label': 'requestDeviation(planId, change, reason)'},
                     db('Read Lock and proposed change', 'Deviation context'),
                     alt(('[plan not locked or reason missing]', finish('Deviation rejected', 'Show deviation error')),
                         ('[else: valid deviation]', [
                             call('s', 'q', 'createRequest(pinned deviation)', 'Pinned deviation item'),
                             db('Append deviation log; keep Lock unchanged', 'Deviation pending approval'),
                             finish('Deviation pending', 'Show deviation waiting for approval')]))])]),
        flow('Triage Exploration Candidates', 'IV 3.5.10',
             'III 3.6; UC-43; FR-57, FR-58, FR-59, FR-206, FR-207, FR-208', 'Researcher',
             'DecisionController', 'ExecutionEngine', 'triage(itemId, decision)', [],
             participants={'t': ': RunOrchestrator', 'q': ': DecisionService'}, custom_tree=[
                 {'from': 't', 'to': 's', 'label': 'runExplorationLane(planId)', 'async': True},
                 db('Read exploration part only; no confirmation part or validation source', 'Exploration data'),
                 loop('[for each search procedure]', [
                     db('Append procedure to tried ledger; raise noise threshold', 'Tried ledger entry'),
                     opt('[result above current threshold]', [
                         call('s', 'q', 'createRequest(candidate)', 'Candidate inbox item')])]),
                 {'from': 'u', 'to': 'w', 'label': 'Open candidate; confirm or reject'},
                 {'from': 'w', 'to': 'c', 'label': 'triage(itemId, decision)'},
                 guarded('triage candidate', [
                     {'from': 'c', 'to': 's', 'label': 'triage(itemId, decision)'},
                     db('Read candidate and inbox item state', 'Candidate'),
                     alt(('[item no longer pending]', finish('Triage rejected', 'Show item already decided')),
                         ('[reject]', [
                             db('Record rejection; keep entry in tried ledger', 'Rejected candidate'),
                             finish('Candidate rejected', 'Show candidate rejected')]),
                         ('[confirm]', [
                             db('Assign confirmation tier; append decision log', 'Confirmed candidate with tier'),
                             finish('Candidate confirmed', 'Show candidate with confirmation tier')]))])]),
    ]),
    dict(folder='06-ai-principal-investigator', slug='AI-Principal-Investigator',
         title='AI Principal Investigator', flows=[
        pi('Configure Action Policy', 'IV 3.6.7', 'updatePreset(stage, preset)', [], service='ActionPolicyService',
           repository='ActionPolicyRepository', trigger='Change stage preset or action level', choices=[
               choice('[set stage preset]', 'changePolicy(input)', 'updatePreset(stage, preset)', [
                   db('Save preset as new policy version; append change log', 'New policy version'),
                   db('Reevaluate waiting items; keep past decisions', 'Waiting items reevaluated')]),
               choice('[override action level]', 'changePolicy(input)', 'setOverride(actionType, level)', [
                   db('Read floors and spending ceiling', 'Policy limits'),
                   alt(('[override below floor or above ceiling]', []), ('[else: valid override]', [
                       db('Save override as new policy version; append change log', 'New policy version'),
                       db('Reevaluate waiting items; keep past decisions', 'Waiting items reevaluated')]))])]),
        pi('Handle Must-Ask and Tentative Decisions', 'IV 3.6.8', 'createRequest(input)', [
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
        pi('Confirm or Overturn Tentative Decision', 'IV 3.6.9', 'confirmTentative(itemId)', [],
           participants={'r': ': RunOrchestrator', 'm': ': OverturnMetricService'},
           trigger='Confirm or overturn tentative decision', choices=[
               choice('[confirm]', 'confirmTentative(itemId)', 'confirmTentative(itemId)', [
                   db('Read tentative item and user authority', 'Tentative decision'),
                   alt(('[item not tentative or no longer actionable]', []), ('[else: item actionable]', [
                       db('Confirm tentative decision; append log', 'Confirmed decision'),
                       call('s', 'm', 'compute(actionType)', 'Overturn rate')]))]),
               choice('[overturn with reason]', 'overturn(itemId, reason)', 'overturn(itemId, reason)', [
                   db('Read tentative item and user authority', 'Tentative decision'),
                   alt(('[item not tentative or no longer actionable]', []), ('[else: item actionable]', [
                       db('Record overturn and reason; append log', 'Overturn recorded'),
                       call('s', 'r', 'markDownstreamStale(objectId)', 'Dependent work undone; objects stale'),
                       call('s', 'm', 'compute(actionType)', 'Overturn rate and suggested higher level'),
                       db('Record proposal only; do not change policy', 'Policy suggestion')]))])]),
        pi('View Lab Notebook', 'IV 3.6.5', 'getLabNotebook(runId)', trigger='Open lab notebook', steps=[
            db('Read authorized run notebook', 'Summaries, proposals and tentative reasons'),
            db('Read assumptions with alternatives and actor', 'Assumptions remain distinct from user intent')]),
        pi('View PI Overview and Close Report', 'IV 3.6.6', 'getPiOverview(runId)', trigger='Open PI overview', steps=[
            db('Read run progress, decisions and notebook', 'PI overview'),
            opt('[run ended]', [call('s', 'i', 'proposeNextStep(runId)', 'Proposal from fixed allowed set'),
                db('Read close report and remaining gaps', 'User chooses next step; PI never ends run')])],
           participants={'i': ': AIPrincipalInvestigator'}),
        flow('Charter and Directives', 'IV 3.6.2', 'III 3.7.1; FR-31, FR-32', 'Researcher / Project Manager',
             'DecisionController', 'DecisionService', 'submitCharter(runId, input)', trigger='Submit charter and directives', steps=[
                 db('Read run context and existing charter', 'Current charter'),
                 alt(('[invalid input or unauthorized change]', []), ('[valid charter and directives]', [
                     db('Record goals, limits and questions for this run', 'Charter and directives recorded'),
                     db('Record user action in decision log', 'Action recorded')]))]),
        flow('Stage Outcome Failure and Close Consultations', 'IV 3.6.3', 'III 3.7.2; NS-03; FR-31, FR-35', 'Project member',
             'DecisionController', 'DecisionService', 'requestConsultation(runId, trigger)', [
                 db('Record consultation and event context', 'Queued consultation'),
                 call('s', 'i', 'consult(context)', 'Advice or consultation failure'),
                 alt(('[consultation failed]', [db('Record failure for the consultation', 'Failure recorded')]),
                     ('[advice returned]', [db('Record advice and notebook entry', 'Consultation result'),
                         db('Keep pinned actions for user decision', 'No pinned decision by AI PI')]))],
             participants={'i': ': AIPrincipalInvestigator'}, system_trigger=': RunOrchestrator'),
        flow('Endorse or Retry Consultation', 'IV 3.6.4', 'III 3.7.3; FR-30, FR-177', 'Researcher / Project Manager',
             'DecisionController', 'DecisionService', 'endorseAdvice(consultationId)', [],
                 trigger='Endorse advice or ask again', choices=[
                     choice('[endorse advice]', 'endorseAdvice(consultationId)', 'endorseAdvice(consultationId)', [
                         db('Read consultation and action eligibility', 'Consultation context'),
                         alt(('[not eligible or advice unavailable]', []), ('[else: eligible]', [
                             db('Record endorsement and user action', 'Endorsement recorded')]))]),
                     choice('[request new consultation]', 'retryConsultation(consultationId)', 'retryConsultation(consultationId)', [
                         db('Read consultation and action eligibility', 'Consultation context'),
                         alt(('[not eligible]', []), ('[else: eligible]', [
                             db('Record user override and queue new consultation', 'New consultation queued')]))])]),
    ]),
    dict(folder='07-notifications-integrations', slug='Notifications-Integrations',
         title='Notifications & Integrations', flows=[
        flow('Receive Notifications', 'IV 3.7.2', 'IV 3.7; FR-29, FR-100, FR-255, FR-264', 'Researcher',
             'CollaborationController', 'NotificationService', 'create(event)', [
                     call('s', 'p', 'resolveForProject(projectId)', 'Effective notification settings'),
                     db('Create authorized in-app notification', 'Notification'),
                     opt('[blocking pinned or spending item]', [
                         db('Select recipients authorized to answer', 'Researcher + PM for pinned; PM for spending'),
                         call('s', 'i', 'deliver(notificationId, enabledChannel)', 'External notice delivery result')])],
             participants={'p': ': NotificationPreferenceService', 'i': ': IntegrationService'},
             system_trigger='Project Event Stream'),
        flow('View Decision Inbox', 'IV 3.7.6', 'IV 3.6; FR-28, FR-29; ADR-05', 'Researcher',
             'CollaborationController', 'DecisionService', 'listActionable(userId)', entry='listInbox()',
             trigger='Open Decision Inbox', steps=[
                 db('Filter items by answer authority and membership', 'Authorized pending items'),
                 db('Sort by blocking level then blocking time', 'Single decision inbox')]),
        flow('Set Notification Preferences', 'IV 3.7.4', 'III 3.8.3; IV 3.7', 'Researcher',
             'CollaborationController', 'NotificationPreferenceService', 'update(input)', entry='setPreferences(input)',
             trigger='Save notification groups', steps=[
                 db('Validate notification groups and writable project', 'Preference eligibility'),
                 alt(('[invalid or archived]', []), ('[valid preferences]', [
                     db('Save current user project preferences', 'NotificationPreference'),
                     db('Retain external-notice eligibility restriction', 'Preferences do not widen event eligibility')]))]),
        flow('Mark Notifications as Read', 'IV 3.7.5', 'III 3.8.4', 'Researcher',
             'CollaborationController', 'NotificationService', 'markRead(notificationId)', [],
             session_only=True, trigger='Mark notifications as read', choices=[
                 choice('[one notice]', 'markRead(notificationId)', 'markRead(notificationId)', [
                     db('Check current user owns notification', 'Notification scope'),
                     alt(('[not recipient]', []), ('[else: recipient]', [db('Mark own notification read', 'Read state')]))]),
                 choice('[all own notices]', 'markAllRead()', 'markAllRead(userId)', [
                     db('Mark current user notices read', 'Own read states')])]),
        flow('View Reviewer Queue', 'IV 3.7.3', 'III 3.8.2; SC-13; FE-15', 'Project member',
             'CollaborationController', 'ReviewService', 'listQueue(userId)', entry='listReviewQueue()',
             trigger='Open reviewer queue', steps=[
                 db('Find projects where the user is a member', 'Authorized memberships'),
                 db('Read items awaiting review for this user across those projects', 'Authorized review items'),
                 db('Return project and item references', 'Reviewer queue')], session_only=True,
             display='Show items awaiting the user review'),
    ]),
    dict(folder='08-administration-monitoring', slug='Administration-Monitoring',
         title='Administration & Monitoring', flows=[
        admin('Manage Users', 'IV 3.8.2', 'updateUser(input)', entry='manageUsers(input)', trigger='Invite, suspend or reactivate user', steps=[
            db('Read selected users and validate action', 'User admin context'),
            alt(('[input invalid]', []), ('[permitted user update]', [
                db('updateUser(input)', 'Updated User'), db('Append admin action audit', 'Audit entry')]))]),
        admin('Configure Models and Decision Provider', 'IV 3.8.3', 'configureModel(input)', [
            call('s', 'k', 'seal(key)', 'SecretRef; never raw key in result'),
            db('Save model role, provider and sealed key reference', 'ModelProfile'),
            opt('[test requested]', [call('s', 'x', 'testModel(profileRef)', 'Sanitized capability result')]),
            db('Append configuration audit without secret', 'Audit entry')],
              participants={'k': ': SecretService', 'x': ': ModelProvider'}),
        admin('Edit Platform and Engine Settings', 'IV 3.8.4', 'configureEngine(input)', [
            db('Validate platform limits and engine settings', 'Settings validation'),
            alt(('[invalid settings]', []), ('[valid settings]', [
                db('Save platform settings, engine defaults and budget', 'Updated settings'),
                db('Append settings audit', 'Audit entry')]))]),
        admin('View Usage Audit Log and Log Monitoring', 'IV 3.8.5', 'usage(filter)', [],
              service='MonitoringService', participants={'t': 'Monitoring Event Stream'},
              trigger='Open usage, audit log or logs', choices=[
                  choice('[usage]', 'viewUsage(filter)', 'usage(filter)', [
                      db('Read scoped usage and cost ledger', 'Usage metrics with availability')]),
                  choice('[audit log]', 'viewAudit(filter)', 'readAudit(filter)', [
                      db('Query append-only audit entries', 'Audit entries')]),
                  choice('[service logs]', 'viewLogs(filter)', 'logs(filter)', [
                      db('Read captured logs with secret filtering', 'Log entries and capture gaps'),
                      opt('[log view remains open]', [event('t', 's', 'onMonitoringEvent(event)'),
                          event('s', 'c', 'pushUpdate(event)'), event('c', 'w', 'Update monitoring view')])])]),
        admin('View Admin Overview', 'IV 3.8.6', 'overview()', entry='viewOverview()', trigger='Open admin overview', steps=[
            db('Read usage, health and recent audit activity', 'Overview with availability / missing reasons')],
              service='MonitoringService'),
        admin('View and Edit User Detail', 'IV 3.8.7', 'getUserDetail(userId)', [],
              trigger='Open or edit user detail', choices=[
                  choice('[view]', 'getUserDetail(userId)', 'getUserDetail(userId)', [
                      db('Read user profile and project metadata', 'User detail without research content')]),
                  choice('[edit status or profile]', 'manageUsers(input)', 'updateUser(input)', [
                      db('Validate status or profile change', 'Change validation'),
                      alt(('[input invalid]', []), ('[else: valid]', [
                          db('Save user change; append audit', 'Updated user')]))])]),
        admin('View All Projects', 'IV 3.8.8', 'listProjectMetadata()', entry='listAllProjects()', trigger='Open all projects', steps=[
            db('Read project list, members, usage and run states', 'Metadata only; no datasets or manuscripts')]),
        admin('Grant or Revoke Platform Admin', 'IV 3.8.9', 'grantPlatformAdmin(userId)', [],
              trigger='Grant or revoke Platform Admin', choices=[
                  choice('[grant]', 'grantPlatformAdmin(userId)', 'grantPlatformAdmin(userId)', [
                      db('Validate target user', 'Role action eligibility'),
                      alt(('[invalid target or already admin]', []), ('[else: eligible]', [
                          db('Grant Platform Admin role; append audit', 'Role granted')]))]),
                  choice('[revoke]', 'revokePlatformAdmin(userId)', 'revokePlatformAdmin(userId)', [
                      db('Validate target user', 'Role action eligibility'),
                      alt(('[invalid target or last Platform Admin]', []), ('[else: eligible]', [
                          db('Revoke Platform Admin role; append audit', 'Role revoked')]))])]),
        admin('View System Health and Acknowledge Alerts', 'IV 3.8.10', 'health()', [], service='MonitoringService',
              trigger='Open health or acknowledge alert', choices=[
                  choice('[view health]', 'viewHealth()', 'health()', [
                      db('Read component and worker health with availability', 'HealthSnapshot and active alerts')]),
                  choice('[acknowledge alert]', 'acknowledgeAlert(alertId)', 'acknowledgeAlert(alertId)', [
                      db('Read alert state', 'MonitoringAlert'),
                      alt(('[alert resolved or unknown]', []), ('[else: alert active]', [
                          db('Record acknowledgement; alert stays active; append audit', 'Acknowledged alert')]))])]),
        # 2026-11-03: UC-65, FE-11.4 and FE-17.4 had Must FRs but no design.
        flow('Run Reviewer Benchmark', 'IV 3.8.11', 'III 3.2.5; UC-65; FR-77, FR-134–138, FR-229, FR-259',
             'Platform Admin', 'AdministrationController', 'BenchmarkService',
             'runBenchmark(catalogueVersion, modelProfileId)', [
            db('Read catalogue version, seeded-flaw cases and model profile', 'Benchmark context'),
            alt(('[catalogue or model profile unavailable]', []), ('[else: benchmark ready]', [
                db('Create benchmark run', 'BenchmarkRun'),
                loop('[for each seeded-flaw case]', [
                    call('s', 'r', 'review(object)', 'Findings per persona in fresh context'),
                    call('s', 'h', 'scoreCase(caseId, findings)', 'Case result')]),
                call('s', 'h', 'computeBenchmarkMetrics(benchmarkRunId)', 'Precision, leakage detection and order block rates'),
                db('Store metrics; flag personas without unique detections', 'Benchmark result')]))],
              participants={'r': ': IndependentReviewService', 'h': ': Harness'},
              trigger='Start benchmark run', result='Benchmark result', display='Show benchmark metrics or error'),
    ]),
]


def _slot_key(flow_def):
    number = re.match(r'IV 3\.(\d+)\.(\d+)', flow_def['slot'])
    return int(number.group(1)), int(number.group(2))


# Tabs and PNG numbers follow the report order (IV 3.x.y), so report figure n is tab n.
for _group in GROUPS:
    _group['flows'].sort(key=_slot_key)

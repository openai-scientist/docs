# Class Diagrams — Mermaid

Xuất từ [class_model.py](class_model.py) bằng [build_class_diagrams.py](build_class_diagrams.py), cùng nội dung với file draw.io; mỗi khối đặt nền trắng, chữ và nét đen. Class chỉ có tên (không ngăn thành viên) thuộc nhóm khác và được vẽ lại để thể hiện phụ thuộc. Chạy lại builder sẽ ghi đè các chỉnh tay trong file này.

## 1. Authentication & Account

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class AuthenticationController {
        <<controller>>
        +requestEmailCode(email : String) void
        +signInWithCode(input : EmailCode) Session
        +signInWithGoogle(code : String) Session
        +currentSession(token : String) User
        +completeOnboarding(input : ProfileInput) User
        +updateProfile(input : ProfileInput) User
        +signOut(sessionId : UUID) void
    }
    class AuthenticationService {
        <<service>>
        +requestCode(email : String) void
        +verifyCode(input : EmailCode) Session
        +signInGoogle(code : String) Session
        +validateSession(token : String) User
        +revokeSession(sessionId : UUID) void
        -resolveUser(email : String) User
    }
    class AccountService {
        <<service>>
        +completeOnboarding(input : ProfileInput) User
        +updateProfile(input : ProfileInput) User
    }
    class AuthorizationService {
        <<service>>
        +requireRole(user : User, projectId : UUID, action : Action) void
        +canReadMetadata(user : User) Boolean
    }
    class GoogleIdentityProvider {
        <<external>>
        +authorize(clientId : String, scope : String) AuthorizationCode
        +verifyIdentity(code : String) Identity
    }
    class EmailDelivery {
        <<external>>
        +sendCode(email : String, code : String) void
    }
    class User {
        <<entity>>
        - id : UUID
        - status : String
        - email : String
        - displayName : String [0..1]
    }
    class Session {
        <<entity>>
        - id : UUID
        - userId : UUID
        - status : String
        - expiresAt : DateTime
    }
    class IdentityLink {
        <<entity>>
        - id : UUID
        - userId : UUID
        - status : String
        - provider : String
    }
    class Membership {
        <<entity>>
        - id : UUID
        - tenantId : UUID
        - userId : UUID
        - projectId : UUID
        - status : String
        - validFrom : DateTime
        - validUntil : DateTime [0..1]
        - reason : String
        - grantedBy : UUID
    }
    class RoleGrant {
        <<entity>>
        - id : UUID
        - userId : UUID
        - membershipId : UUID
        - status : String
        - validFrom : DateTime
        - validUntil : DateTime [0..1]
        - reason : String
        - grantedBy : UUID
        - role : ProjectRole
    }
    class ProjectRole {
        <<enumeration>>
        project#95;manager
        researcher
        reviewer
    }
    AuthenticationController ..> AuthenticationService : signs in / out
    AuthenticationController ..> AccountService : updates profile
    AuthenticationController ..> AuthorizationService : checks access
    AuthenticationService ..> GoogleIdentityProvider : verifies identity
    AuthenticationService ..> EmailDelivery : sends code
    AuthenticationService ..> Session : manages sessions
    AuthenticationService ..> User : resolves verified email
    AuthenticationService ..> IdentityLink : links Google identity
    AccountService ..> User : updates
    AuthorizationService ..> Membership : reads memberships
    AuthorizationService ..> RoleGrant : checks project role
    User "1" *-- "0..*" Session : sessions
    User "1" *-- "0..*" IdentityLink : identity links
    User "1" -- "0..*" Membership : memberships
    Membership "1" -- "0..*" RoleGrant : role grants
    RoleGrant ..> ProjectRole : uses type
```

## 2. Project Workspace

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class ProjectController {
        <<controller>>
        +create(input : ProjectInput) Project
        +listProjects() Project [0..∗]
        +getOverview(projectId : UUID) ProjectOverview
        +update(projectId : UUID, input : ProjectInput) void
        +archive(projectId : UUID) void
        +complete(projectId : UUID) void
        +deleteProject(projectId : UUID, confirmation : String) void
        +transferOwnership(projectId : UUID, userId : UUID) void
        +inviteMember(projectId : UUID, email : String, role : ProjectRole) Invitation
        +changeRole(memberId : UUID, role : ProjectRole) void
        +removeMember(memberId : UUID) void
        +acceptInvitation(invitationId : UUID) Membership
        +declineInvitation(invitationId : UUID) void
        +resendInvitation(invitationId : UUID) void
        +cancelInvitation(invitationId : UUID) void
        +uploadDocument(projectId : UUID, input : DocumentInput) Document
        +listDocuments(projectId : UUID) Document [0..∗]
        +downloadDocument(documentId : UUID) File
        +deleteDocument(documentId : UUID) void
        +configure(projectId : UUID, settings : ConfigVersion) void
        +configureIntegration(projectId : UUID, input : IntegrationInput) void
        +testIntegration(integrationId : UUID) CheckResult
        +removeIntegration(integrationId : UUID) void
        +setNotificationPreferences(projectId : UUID, input : PreferencesInput) void
        +listActivity(projectId : UUID, filter : ActivityFilter) AuditEvent [0..∗]
    }
    class ProjectService {
        <<service>>
        +create(input : ProjectInput) Project
        +listForUser(userId : UUID) Project [0..∗]
        +getOverview(projectId : UUID) ProjectOverview
        +update(projectId : UUID, input : ProjectInput) void
        +archive(projectId : UUID) void
        +complete(projectId : UUID) void
        +delete(projectId : UUID) void
        +configure(settings : ConfigVersion) void
        +listActivity(projectId : UUID, filter : ActivityFilter) AuditEvent [0..∗]
        -recordChange(action : String) void
    }
    class MembershipService {
        <<service>>
        +changeRole(memberId : UUID, role : ProjectRole) void
        +remove(memberId : UUID) void
        +transferOwnership(projectId : UUID, userId : UUID) void
        -requireActiveManager(projectId : UUID) void
    }
    class InvitationService {
        <<service>>
        +invite(projectId : UUID, email : String, role : ProjectRole) Invitation
        +accept(invitationId : UUID) Membership
        +decline(invitationId : UUID) void
        +resend(invitationId : UUID) void
        +cancel(invitationId : UUID) void
        -rejectExpired(invitation : Invitation) void
    }
    class DocumentService {
        <<service>>
        +add(projectId : UUID, input : DocumentInput) Document
        +list(projectId : UUID) Document [0..∗]
        +download(documentId : UUID) File
        +delete(documentId : UUID) void
    }
    class AuthorizationService {
        <<service>>
    }
    class AuthenticationService {
        <<service>>
    }
    class IntegrationService {
        <<service>>
    }
    class NotificationPreferenceService {
        <<service>>
    }
    class ActionPolicyService {
        <<service>>
    }
    class Project {
        <<entity>>
        - id : UUID
        - tenantId : UUID
        - projectTemplateId : UUID
        - name : String
        - status : ProjectStatus
    }
    class ProjectStatus {
        <<enumeration>>
        active
        completed
        archived
    }
    class User {
        <<entity>>
        - id : UUID
        - status : String
        - email : String
    }
    class Membership {
        <<entity>>
        - id : UUID
        - tenantId : UUID
        - userId : UUID
        - projectId : UUID
        - status : String
        - validFrom : DateTime
        - validUntil : DateTime [0..1]
        - reason : String
        - grantedBy : UUID
    }
    class Invitation {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - status : String
        - email : String
        - expiresAt : DateTime
    }
    class ConfigVersion {
        <<entity>>
        - id : UUID
        - settingDefinitionId : UUID
        - status : String
    }
    class BudgetAccount {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - status : String
        - monthlyLimit : Decimal
    }
    class NotificationPreference {
        <<entity>>
        - id : UUID
        - userId : UUID
        - status : String
    }
    class ActivityProjection {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - lastEventPosition : Integer
    }
    class AuditEvent {
        <<entity>>
        - id : UUID
        - userId : UUID
        - auditCheckpointId : UUID
        - action : String
        - time : DateTime
    }
    ProjectController ..> ProjectService : manages projects
    ProjectController ..> MembershipService : manages members
    ProjectController ..> InvitationService : manages invitations
    ProjectController ..> DocumentService : manages documents
    ProjectController ..> AuthorizationService : checks access
    ProjectController ..> AuthenticationService : validates session
    ProjectController ..> IntegrationService : configures delivery
    ProjectController ..> NotificationPreferenceService : sets preferences
    ProjectService ..> ActionPolicyService : sets stage presets
    ProjectService ..> Project : manages
    ProjectService ..> AuditEvent : records changes
    ProjectService ..> ConfigVersion : publishes settings
    ProjectService ..> ActivityProjection : lists activity
    MembershipService ..> Membership : maintains
    InvitationService ..> Invitation : issues / resolves
    NotificationPreferenceService ..> NotificationPreference : updates
    Project ..> ProjectStatus : uses type
    Project "1" -- "0..*" Membership : memberships
    Membership "0..*" -- "1" User : member
    Project "1" *-- "0..*" Invitation : invitations
    Project "1" -- "1" BudgetAccount : budget
    Project "1" -- "0..*" ConfigVersion : settings
```

## 3. Data Management

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class DataController {
        <<controller>>
        +upload(input : UploadInput) DataFileVersion
        +getDataset(datasetId : UUID) DatasetDetail
        +renameDataset(datasetId : UUID, name : String) void
        +deleteDataset(datasetId : UUID) void
        +uploadVersion(datasetId : UUID, input : UploadInput) DataFileVersion
        +preview(versionId : UUID) TablePreview
        +download(versionId : UUID) File
        +importData(connectionId : UUID) DataFileVersion
        +browseConnection(connectionId : UUID, schema : String) TableRef [0..∗]
        +previewSource(connectionId : UUID, source : AnySource) TablePreview
        +renameConnection(connectionId : UUID, name : String) void
        +testConnection(connectionId : UUID) CheckResult
        +deleteConnection(connectionId : UUID) void
        +connectGoogle(projectId : UUID) Connector
        +requestPairingCode(projectId : UUID) PairingCode
        +pairNode(code : String) Connector
        +proposeDatasets(nodeId : UUID, manifests : Manifest [1..∗]) void
        +revokeNode(nodeId : UUID) void
        +pushUpdate(event : DomainEvent) void
    }
    class DataService {
        <<service>>
        +createDataset(input : DatasetInput) DataSource
        +getDetail(datasetId : UUID) DatasetDetail
        +rename(datasetId : UUID, name : String) void
        +delete(datasetId : UUID) void
        +addVersion(datasetId : UUID, input : UploadInput) DataFileVersion
        +preview(versionId : UUID) TablePreview
        +download(versionId : UUID) File
        +importData(connection : Connector) DataFileVersion
        +browse(connectionId : UUID, schema : String) TableRef [0..∗]
        +previewSource(connectionId : UUID, source : AnySource) TablePreview
        +renameConnection(connectionId : UUID, name : String) void
        +testConnection(connectionId : UUID) CheckResult
        +deleteConnection(connectionId : UUID) void
        +authorizeGoogle(projectId : UUID) Connector
        -blockInternalHosts(uri : String) void
        -rejectLocalPreview(dataset : DataSource) void
    }
    class DatasetVersionService {
        <<service>>
        +create(datasetId : UUID, source : String) DataFileVersion
        +verifyHash(version : DataFileVersion) Boolean
        -preventOverwrite(versionId : UUID) void
    }
    class LocalNodeService {
        <<service>>
        +issuePairingCode(projectId : UUID) PairingCode
        +pair(projectId : UUID, code : String) Connector
        +registerDatasets(nodeId : UUID, manifests : Manifest [1..∗]) DataSource [1..∗]
        +route(job : LocalJob) JobResult
        +checkHealth(nodeId : UUID) void
        +revoke(nodeId : UUID) void
        -rejectUnavailableNode(nodeId : UUID) void
    }
    class AuthorizationService {
        <<service>>
    }
    class SecretService {
        <<service>>
    }
    class NotificationService {
        <<service>>
    }
    class RunOrchestrator {
        <<service>>
    }
    class ExecutionEngine {
        <<service>>
    }
    class GoogleIdentityProvider {
        <<external>>
    }
    class ConnectorFactory {
        <<interface>>
        +#95;#95;call#95;#95;(kind : String, config : Map, secret : Map) SourceConnector
    }
    class SourceConnector {
        <<interface>>
        +test() void
        +listTables(schema : String, search : String [0..1], limit : Integer) TableRef [0..∗]
        +listColumns(schema : String, table : String) Column [0..∗]
        +openRows(source : AnySource, maxRows : Integer [0..1]) AsyncContext~RowStream~
    }
    class GoogleSheetsConnector {
        <<service>>
        +test() void
        +listTables(schema : String, search : String [0..1], limit : Integer) TableRef [0..∗]
        +listColumns(schema : String, table : String) Column [0..∗]
        +openRows(source : AnySource, maxRows : Integer [0..1]) AsyncContext~RowStream~
    }
    class LocalNodeAgent {
        <<external>>
        +runJob(job : LocalJob) JobResult
    }
    class ReleaseGate {
        <<service>>
        +check(job : LocalJob, result : Aggregate) ReleaseReview
        +recordRelease(release : ReleaseReview) void
        -applyFirewall(result : Aggregate) void
        -round(result : Aggregate) Aggregate
        -checkDisclosure(result : Aggregate) void
        -checkDifferencing(result : Aggregate) void
        -checkProbeBudget(versionId : UUID) void
    }
    class DataSource {
        <<entity>>
        - id : UUID
        - connectorId : UUID
        - status : String
        - name : String
        - location : DataLocation
    }
    class DataLocation {
        <<enumeration>>
        platform
        local
    }
    class DataVersionRef {
        <<entity>>
        - id : UUID
        - dataSourceId : UUID
        - coreId : UUID
        - coreVersion : Integer
        - digest : String
    }
    class DataFileVersion {
        <<entity>>
        - id : UUID
        - dataVersionRefId : UUID
        - status : String
    }
    class Connector {
        <<entity>>
        - id : UUID
        - servicePrincipalId : UUID
        - status : String
    }
    class DataUseGrant {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - dataSourceId : UUID
        - status : String
        - validFrom : DateTime
        - validUntil : DateTime [0..1]
        - reason : String
        - grantedBy : UUID
    }
    class ReleasePolicy {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - status : String
    }
    class ReleaseReview {
        <<entity>>
        - id : UUID
        - releaseManifestId : UUID
        - releasePolicyId : UUID
        - status : String
    }
    class AuditEvent {
        <<entity>>
        - id : UUID
        - userId : UUID
        - auditCheckpointId : UUID
        - action : String
        - time : DateTime
    }
    DataController ..> DataService : manages datasets
    DataController ..> LocalNodeService : manages Local Nodes
    DataController ..> AuthorizationService : checks access
    DataService ..> DatasetVersionService : creates versions
    DataService ..> SecretService : seals credentials
    DataService ..> ConnectorFactory : uses factory
    DataService ..> GoogleIdentityProvider : authorizes Google source
    ConnectorFactory ..> SourceConnector : creates connector
    GoogleSheetsConnector ..|> SourceConnector : implements
    ExecutionEngine ..> LocalNodeService : routes local job
    LocalNodeService ..> LocalNodeAgent : dispatches jobs
    LocalNodeService ..> NotificationService : sends offline notice
    LocalNodeService ..> RunOrchestrator : resumes waiting run
    LocalNodeAgent ..> ReleaseGate : checks aggregates
    DataService ..> DataSource : manages
    DataService ..> Connector : imports through
    DataService ..> DataUseGrant : checks data use
    DatasetVersionService ..> DataFileVersion : creates / verifies
    DatasetVersionService ..> DataVersionRef : references version
    LocalNodeService ..> Connector : pairs / revokes
    ReleaseGate ..> ReleasePolicy : applies
    ReleaseGate ..> ReleaseReview : records
    ReleaseGate ..> AuditEvent : appends release
    DataSource ..> DataLocation : uses type
    DataSource "1" *-- "0..*" DataVersionRef : versions
    DataVersionRef "1" -- "0..1" DataFileVersion : stored file
    Connector "1" -- "0..*" DataSource : sources
    DataSource "1" -- "0..*" DataUseGrant : use grants
    ReleasePolicy "1" -- "0..*" ReleaseReview : reviews
```

## 4. Research Run Orchestration

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class RunController {
        <<controller>>
        +start(caseId : UUID) RunRequest
        +amendCase(input : Amendment) ResearchCaseRef
        +getRun(runId : UUID) RunSnapshot
        +listRuns(projectId : UUID, filter : RunFilter) RunRequest [0..∗]
        +acceptObject(objectId : UUID) void
        +requestRevision(objectId : UUID, reason : String) void
        +rerunStage(stageRunId : UUID) void
        +cancel(runId : UUID) void
        +syncRun(runId : UUID) RunSnapshot
        +raiseTokenBudget(runId : UUID, amount : Integer) void
        +getReviewHistory(stageRunId : UUID) ReviewRound [0..∗]
        +getRecoveryState(runId : UUID) RecoveryState
        +getIterationSummary(stageRunId : UUID) IterationSummary
        +downloadArtifact(versionId : UUID) File
        +compareArtifacts(versionA : UUID, versionB : UUID) VersionDiff
        +addComment(input : CommentInput) Discussion
        +editComment(commentId : UUID, text : String) void
        +deleteComment(commentId : UUID) void
        +lockPlan(planId : UUID) AuthorityReceipt
        +requestDeviation(planId : UUID, change : String, reason : String) DecisionTask
        +reviewSpending(itemId : UUID, approve : Boolean) void
        +approveDossier(dossierId : UUID) DecisionResponse
        +export(dossierId : UUID, format : String) ExportJob
        +pushUpdate(event : DomainEvent) void
    }
    class RunOrchestrator {
        <<service>>
        +start(caseId : UUID) RunRequest
        +getSnapshot(runId : UUID) RunSnapshot
        +listRuns(projectId : UUID, filter : RunFilter) RunRequest [0..∗]
        +advance(runId : UUID) RunPlanStep
        +acceptVersion(objectId : UUID) void
        +requestRevision(objectId : UUID, reason : String) void
        +rerunStage(stageRunId : UUID) void
        +cancel(runId : UUID) void
        +syncRun(runId : UUID) RunSnapshot
        +resume(runId : UUID) void
        +endWithGaps(runId : UUID, reason : String) void
        +markDownstreamStale(objectId : UUID) void
        +onRunEvent(event : RunEvent) void
        +getReviewHistory(stageRunId : UUID) ReviewRound [0..∗]
        +getRecoveryState(runId : UUID) RecoveryState
        +getIterationSummary(stageRunId : UUID) IterationSummary
        +downloadArtifact(versionId : UUID) File
        +compareArtifacts(versionA : UUID, versionB : UUID) VersionDiff
        -requireNoActiveRun(projectId : UUID) void
    }
    class ResearchCaseService {
        <<service>>
        +create(input : CaseInput) ResearchCaseRef
        +amend(caseId : UUID, change : CaseChange, reason : String) ResearchCaseRef
    }
    class BudgetService {
        <<service>>
        +recordUsage(runId : UUID, amount : Decimal) void
        +checkLimits(runId : UUID) void
        +raiseRunBudget(runId : UUID, amount : Integer) void
        +approveSpending(itemId : UUID) void
        +rejectSpending(itemId : UUID) void
        +expireSpending(itemId : UUID) void
    }
    class DossierService {
        <<service>>
        +createFromAccepted(packId : UUID) ScientificPackageRef
        +approve(dossierId : UUID) DecisionResponse
        +exportApproved(dossierId : UUID, format : String) ExportJob
        -verifyReferenceHashes(dossierId : UUID) void
        -requirePinnedExportApproval(dossierId : UUID) void
    }
    class AuthorizationService {
        <<service>>
    }
    class LockService {
        <<service>>
    }
    class CommentService {
        <<service>>
    }
    class DecisionService {
        <<service>>
    }
    class NotificationService {
        <<service>>
    }
    class DatasetEngine {
        <<service>>
    }
    class ScientificCore {
        <<external>>
        +submit(command : CommandEnvelope) void
        +cancel(commandId : UUID) void
    }
    class ResearchCaseRef {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - coreId : UUID
        - coreVersion : Integer
        - digest : String
    }
    class RunRequest {
        <<entity>>
        - id : UUID
        - inquiryRefId : UUID
        - state : RunState
        - waitingReason : WaitingReason [0..1]
        - endingOutcome : EndingOutcome [0..1]
    }
    class RunState {
        <<enumeration>>
        running
        waiting
        ended
    }
    class WaitingReason {
        <<enumeration>>
        decision
        node#95;offline
        budget#95;review
    }
    class EndingOutcome {
        <<enumeration>>
        complete
        complete#95;with#95;gaps
        technical#95;failure
        cancelled
    }
    class RunPlanStep {
        <<entity>>
        - id : UUID
        - runRequestId : UUID
        - lastEventPosition : Integer
    }
    class RunTimelineEntry {
        <<entity>>
        - id : UUID
        - runRequestId : UUID
        - runPlanStepId : UUID
    }
    class AdmissionReceipt {
        <<entity>>
        - id : UUID
        - runRequestId : UUID
        - effectiveConfigSnapshotId : UUID
        - credentialBindingId : UUID
        - modelOfferingId : UUID
        - dataUseGrantIds : UUID
    }
    class CommandEnvelope {
        <<entity>>
        - id : UUID
        - runAttemptId : UUID
        - authorityReceiptId : UUID
        - status : String
    }
    class EventInbox {
        <<entity>>
        - id : UUID
        - runRequestId : UUID
    }
    class BudgetAccount {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - status : String
        - monthlyLimit : Decimal
    }
    class CapacityLease {
        <<entity>>
        - id : UUID
        - runRequestId : UUID
    }
    class BudgetException {
        <<entity>>
        - id : UUID
        - budgetAccountId : UUID
        - status : String
    }
    class DecisionTask {
        <<entity>>
        - id : UUID
        - scientificObjectRefId : UUID
        - status : String
    }
    class DecisionResponse {
        <<entity>>
        - id : UUID
        - decisionTaskId : UUID
        - status : String
    }
    class ScientificPackageRef {
        <<entity>>
        - id : UUID
        - corePackageId : UUID
        - runRequestId : UUID
        - coreId : UUID
        - coreVersion : Integer
        - digest : String
    }
    class ReleaseManifest {
        <<entity>>
        - id : UUID
        - scientificPackageRefId : UUID
        - approvalRequestId : UUID
        - status : String
    }
    class ShareGrant {
        <<entity>>
        - id : UUID
        - releaseManifestId : UUID
        - status : String
        - validFrom : DateTime
        - validUntil : DateTime [0..1]
        - reason : String
        - grantedBy : UUID
    }
    class ExportJob {
        <<entity>>
        - id : UUID
        - releaseManifestId : UUID
        - status : String
    }
    RunController ..> RunOrchestrator : controls runs
    RunController ..> ResearchCaseService : amends cases
    RunController ..> BudgetService : raises budget / reviews spending
    RunController ..> DossierService : approves / exports
    RunController ..> AuthorizationService : checks access
    RunController ..> LockService : locks plan
    RunController ..> CommentService : comments
    RunOrchestrator ..> DatasetEngine : schedules stages
    BudgetService ..> RunOrchestrator : resumes / ends run
    BudgetService ..> NotificationService : alerts Project Managers
    BudgetService ..> DecisionService : creates spending item
    RunOrchestrator ..> RunRequest : orchestrates
    RunOrchestrator ..> AdmissionReceipt : admits run
    RunOrchestrator ..> CommandEnvelope : sends command
    RunOrchestrator ..> EventInbox : reads events
    RunOrchestrator ..> ScientificCore : commands run
    ResearchCaseService ..> ResearchCaseRef : versions
    BudgetService ..> BudgetAccount : records usage
    BudgetService ..> CapacityLease : holds run slot
    BudgetService ..> BudgetException : raises limit
    DossierService ..> ScientificPackageRef : versions / checks
    DossierService ..> ExportJob : exports
    RunRequest "0..*" -- "1" ResearchCaseRef : pinned case
    RunRequest ..> RunState : uses type
    RunRequest ..> WaitingReason : uses type
    RunRequest ..> EndingOutcome : uses type
    RunRequest "1" *-- "0..*" RunPlanStep : plan steps
    RunRequest "1" *-- "0..*" RunTimelineEntry : timeline
    RunRequest "1" -- "0..1" AdmissionReceipt : admission
    RunRequest "1" -- "0..*" CommandEnvelope : commands
    DecisionTask "1" -- "0..*" DecisionResponse : responses
    ScientificPackageRef "1" -- "0..*" ReleaseManifest : manifests
    ReleaseManifest "1" -- "0..*" ShareGrant : grants
    ScientificPackageRef "1" -- "0..*" ExportJob : exports
```

## 5. Research Engines

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class LiteratureController {
        <<controller>>
        +search(projectId : UUID, query : String) StudyRef [0..∗]
        +screen(decisions : ScreeningDecision [1..∗]) LiteratureBase
    }
    class RunOrchestrator {
        <<service>>
    }
    class DecisionService {
        <<service>>
    }
    class RunController {
        <<service>>
    }
    class AuthorizationService {
        <<service>>
    }
    class DatasetEngine {
        <<service>>
        +profile(versionId : UUID) DatasetSnapshot
    }
    class HypothesisEngine {
        <<service>>
        +propose(snapshot : DatasetSnapshot) HypothesisSet
    }
    class ExperimentDesignEngine {
        <<service>>
        +build(set : HypothesisSet) AnalysisPlan
    }
    class ExecutionEngine {
        <<service>>
        +execute(lock : AuthorityReceipt) EvidenceBundle
        +runExplorationLane(planId : UUID) void
        +triage(itemId : UUID, decision : String) Candidate
    }
    class PaperEngine {
        <<service>>
        +draft(input : PaperInput) PaperPack
    }
    class LiteratureService {
        <<service>>
        +search(query : String) StudyRef [0..∗]
        +screen(decisions : ScreeningDecision [1..∗]) LiteratureBase
    }
    class LockService {
        <<service>>
        +lock(planId : UUID) AuthorityReceipt
        +requestDeviation(planId : UUID, change : String, reason : String) DecisionTask
    }
    class IndependentReviewService {
        <<service>>
        +review(object : ScientificObjectRef) ReviewComment [0..∗]
        -enforceTwoRounds(round : Integer) void
    }
    class ReviewerPersona {
        <<service>>
        +review(object : ScientificObjectRef, fields : String [1..∗]) ReviewComment [0..∗]
    }
    class MakerPersona {
        <<service>>
        +revise(objectId : UUID, findings : ReviewComment [1..∗]) ScientificObjectRef
    }
    class Harness {
        <<service>>
        +checkContract(object : ScientificObjectRef) CheckResult
        +enforcePipelineOrder(plan : AnalysisPlan) void
        +renderNumbers(records : Record [0..∗]) String
        +computeProfile(versionId : UUID) Profile
        +createSplit(snapshotId : UUID, policy : SplitPolicy) SplitSpec
        +validatePortfolio(set : HypothesisSet) CheckResult
        +rehearseOnTwin(plan : AnalysisPlan) CheckResult
        +checkDisclosureEligibility(lockId : UUID) CheckResult
        +computeVerdicts(input : EvidenceInput) Verdict [1..∗]
        +validateClaimsAndCitations(pack : PaperPack) CheckResult
        +verifyFindings(findings : ReviewComment [1..∗]) ReviewComment [0..∗]
        +recheckChangedFields(objectId : UUID) CheckResult
        +scoreCase(caseId : UUID, findings : ReviewComment [0..∗]) CaseResult
        +computeBenchmarkMetrics(benchmarkRunId : UUID) BenchmarkMetrics
    }
    class ScholarlySource {
        <<external>>
        +search(query : String) SourceRecord [0..∗]
    }
    class IsolatedExecutor {
        <<external>>
        +runTwin(lock : AuthorityReceipt) Diagnostics
        +dryRun(lock : AuthorityReceipt) Diagnostics
        +runConfirmatory(lock : AuthorityReceipt) JobStatus
    }
    class DatasetSnapshot {
        <<entity>>
        - versionRef : VersionRef
        - qualityProfile : QualityProfile
        - dictionary : Dictionary
        - split : SplitSpec
        - fitness : Fitness
    }
    class HypothesisSet {
        <<entity>>
        - snapshotRef : VersionRef
        - literatureVersionRef : VersionRef
        - hypotheses : Hypothesis [2..∗]
        - primaryClaimKey : String
    }
    class AnalysisPlan {
        <<entity>>
        - hypothesisSetRef : VersionRef
        - patternRefs : VersionRef [0..∗]
        - taskFamily : String
        - pipelineOrder : String [1..∗]
        - interpretationTable : Table
    }
    class EvidenceBundle {
        <<entity>>
        - analysisPlanRef : VersionRef
        - verdicts : Verdict [1..∗]
        - grade : String
        - claimCeiling : String
        - triedLedger : TriedEntry [0..∗]
        - candidates : Candidate [0..∗]
        - replicationHash : String
    }
    class PaperPack {
        <<entity>>
        - evidenceBundleRef : VersionRef
        - manuscript : String
        - reportingChecklist : Checklist
        - limitations : String [0..∗]
        - authorDeclarations : Declaration [0..∗]
    }
    class ScientificObjectRef {
        <<entity>>
        - id : UUID
        - inquiryRefId : UUID
        - corePlanId : UUID
        - coreId : UUID
        - coreVersion : Integer
        - digest : String
    }
    class DataVersionRef {
        <<entity>>
        - id : UUID
        - dataSourceId : UUID
        - coreId : UUID
        - coreVersion : Integer
        - digest : String
    }
    class CommandEnvelope {
        <<entity>>
        - id : UUID
        - runAttemptId : UUID
        - authorityReceiptId : UUID
        - status : String
    }
    class ReviewAssignment {
        <<entity>>
        - id : UUID
        - scientificObjectRefId : UUID
        - userId : UUID
        - status : String
    }
    class ReviewComment {
        <<entity>>
        - id : UUID
        - reviewAssignmentId : UUID
        - status : String
    }
    class DecisionTask {
        <<entity>>
        - id : UUID
        - scientificObjectRefId : UUID
        - status : String
    }
    LiteratureController ..> LiteratureService : searches / screens
    LiteratureController ..> AuthorizationService : checks access
    RunOrchestrator ..> DatasetEngine : starts stage
    DatasetEngine ..> DecisionService : asks to confirm structure
    HypothesisEngine ..> ScholarlySource : searches literature
    LiteratureService ..> ScholarlySource : searches literature
    ExecutionEngine ..> IsolatedExecutor : runs jobs
    ExecutionEngine ..> RunController : pushes update
    LockService ..> DecisionService : requests deviation
    LockService ..> RunOrchestrator : schedules execution
    IndependentReviewService ..> ReviewerPersona : reviews with
    IndependentReviewService ..> MakerPersona : revises with
    IndependentReviewService ..> Harness : verifies findings
    PaperEngine ..> Harness : runs checks
    DatasetEngine ..> DatasetSnapshot : publishes
    HypothesisEngine ..> HypothesisSet : publishes
    ExperimentDesignEngine ..> AnalysisPlan : publishes
    ExecutionEngine ..> EvidenceBundle : publishes
    PaperEngine ..> PaperPack : publishes
    DatasetEngine ..> DataVersionRef : reads data version
    RunOrchestrator ..> CommandEnvelope : starts stage engine
    LockService ..> ScientificObjectRef : locks plan version
    IndependentReviewService ..> ReviewAssignment : reads assignment
    IndependentReviewService ..> ReviewComment : records
    IndependentReviewService ..> DecisionTask : raises decision
    DatasetSnapshot "0..*" -- "1" DataVersionRef : data version
    ReviewAssignment "1" -- "0..*" ReviewComment : comments
    ReviewComment "0..*" -- "1" ScientificObjectRef : anchored to
```

## 6. AI Principal Investigator

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class DecisionController {
        <<controller>>
        +answer(itemId : UUID, option : String) void
        +confirmTentative(itemId : UUID) void
        +overturn(itemId : UUID, reason : String) void
        +changePolicy(input : PolicyInput) void
        +setPresence(value : Presence) void
        +submitCharter(runId : UUID, input : CharterInput) RunTimelineEntry
        +endorseAdvice(consultationId : UUID) void
        +retryConsultation(consultationId : UUID) void
        +getLabNotebook(runId : UUID) RunTimelineEntry [0..∗]
        +getPiOverview(runId : UUID) PiOverview
        +triage(itemId : UUID, decision : String) void
        +pushUpdate(event : DomainEvent) void
    }
    class DecisionService {
        <<service>>
        +createRequest(input : DecisionInput) DecisionTask
        +answer(itemId : UUID, option : String) void
        +confirmTentative(itemId : UUID) void
        +overturn(itemId : UUID, reason : String) void
        +listActionable(userId : UUID) DecisionTask [0..∗]
        +submitCharter(runId : UUID, input : CharterInput) RunTimelineEntry
        +requestConsultation(runId : UUID, trigger : String) RunTimelineEntry
        +endorseAdvice(consultationId : UUID) void
        +retryConsultation(consultationId : UUID) RunTimelineEntry
        +getLabNotebook(runId : UUID) RunTimelineEntry [0..∗]
        +getPiOverview(runId : UUID) PiOverview
        +expirePinnedItem(itemId : UUID) void
        -closeUnansweredAndEndWithGaps(itemId : UUID) void
    }
    class ActionPolicyService {
        <<service>>
        +effectiveLevel(actionType : String) ActionLevel
        +validate(input : PolicyInput) CheckResult
        +updatePreset(stage : String, preset : String) void
        +setOverride(actionType : String, level : ActionLevel) void
        +reevaluateWaitingItems() void
        -enforceFloorAndCeiling(actionType : String) void
    }
    class AIPrincipalInvestigator {
        <<service>>
        +consult(context : RunContext) Advice
        +decideTentatively(item : DecisionTask) void
        +proposeNextStep(runId : UUID) String
        -rejectPinnedDecision(item : DecisionTask) void
    }
    class OverturnMetricService {
        <<service>>
        +compute(actionType : String) Decimal
        +proposeHigherLevel(actionType : String) ActionLevel
    }
    class AuthorizationService {
        <<service>>
    }
    class RunOrchestrator {
        <<service>>
    }
    class ExecutionEngine {
        <<service>>
    }
    class RunRequest {
        <<entity>>
        - id : UUID
        - inquiryRefId : UUID
        - state : RunState
    }
    class RunTimelineEntry {
        <<entity>>
        - id : UUID
        - runRequestId : UUID
        - runPlanStepId : UUID
    }
    class EffectiveConfigSnapshot {
        <<entity>>
        - id : UUID
        - configVersionId : UUID
    }
    class ScientificObjectRef {
        <<entity>>
        - id : UUID
        - inquiryRefId : UUID
        - corePlanId : UUID
        - coreId : UUID
        - coreVersion : Integer
        - digest : String
    }
    class ConfigVersion {
        <<entity>>
        - id : UUID
        - settingDefinitionId : UUID
        - status : String
    }
    class PolicyRule {
        <<entity>>
        - id : UUID
        - configVersionId : UUID
        - status : String
        - level : ActionLevel
    }
    class ActionLevel {
        <<enumeration>>
        auto
        do#95;then#95;review
        must#95;ask
    }
    class DecisionTask {
        <<entity>>
        - id : UUID
        - scientificObjectRefId : UUID
        - status : String
    }
    class DecisionResponse {
        <<entity>>
        - id : UUID
        - decisionTaskId : UUID
        - status : String
    }
    class AuditEvent {
        <<entity>>
        - id : UUID
        - userId : UUID
        - auditCheckpointId : UUID
        - action : String
        - time : DateTime
    }
    DecisionController ..> DecisionService : answers / consults
    DecisionController ..> ActionPolicyService : changes policy
    DecisionController ..> AuthorizationService : checks access
    DecisionController ..> ExecutionEngine : triages candidates
    DecisionService ..> AIPrincipalInvestigator : consults
    DecisionService ..> OverturnMetricService : measures overturns
    DecisionService ..> RunOrchestrator : resumes / marks stale
    DecisionService ..> DecisionTask : creates / resolves
    DecisionService ..> DecisionResponse : records
    DecisionService ..> AuditEvent : logs decision
    DecisionService ..> RunTimelineEntry : records charter
    AIPrincipalInvestigator ..> RunTimelineEntry : writes advice
    AIPrincipalInvestigator ..> EffectiveConfigSnapshot : reads at run start
    AIPrincipalInvestigator ..> ScientificObjectRef : reads outcome
    ActionPolicyService ..> PolicyRule : versions
    ActionPolicyService ..> ConfigVersion : reads
    OverturnMetricService ..> RunRequest : measures by run
    RunRequest "1" *-- "0..*" RunTimelineEntry : timeline
    RunRequest "1" -- "1" EffectiveConfigSnapshot : config
    DecisionTask "1" -- "0..*" DecisionResponse : responses
    PolicyRule ..> ActionLevel : uses type
```

## 7. Notifications & Integrations

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class CollaborationController {
        <<controller>>
        +listNotifications() Notification [0..∗]
        +markRead(notificationId : UUID) void
        +markAllRead() void
        +setPreferences(input : PreferencesInput) void
        +listInbox() DecisionTask [0..∗]
        +listReviewQueue() ReviewItem [0..∗]
        +pushUpdate(event : DomainEvent) void
    }
    class NotificationService {
        <<service>>
        +create(event : ProjectEvent) Notification
        +listForUser(userId : UUID) Notification [0..∗]
        +markRead(notificationId : UUID) void
        +markAllRead(userId : UUID) void
        +retryEmail(emailId : UUID) void
        -allowExternalNotice(item : DecisionTask) Boolean
        -selectAuthorizedRecipients(item : DecisionTask) UUID [0..∗]
    }
    class NotificationPreferenceService {
        <<service>>
        +update(input : PreferencesInput) NotificationPreference
        +resolveForProject(projectId : UUID) NotificationPreference
    }
    class IntegrationService {
        <<service>>
        +configure(input : IntegrationInput) ProjectIntegration
        +test(integrationId : UUID) CheckResult
        +remove(integrationId : UUID) void
        +deliver(notificationId : UUID, channel : String) void
        -resolveSealedCredential(ref : CredentialRef) void
    }
    class CommentService {
        <<service>>
        +add(input : CommentInput) Discussion
        +list(objectRef : ObjectRef) Discussion [0..∗]
        +edit(commentId : UUID, text : String) void
        +delete(commentId : UUID) void
        -requireProjectRole(actorId : UUID) void
    }
    class ReviewService {
        <<service>>
        +listQueue(userId : UUID) ReviewItem [0..∗]
    }
    class AuthorizationService {
        <<service>>
    }
    class AuthenticationService {
        <<service>>
    }
    class DecisionService {
        <<service>>
    }
    class NotificationChannel {
        <<external>>
        +deliver(recipient : String, message : String) void
    }
    class Notification {
        <<entity>>
        - id : UUID
        - userId : UUID
        - lastEventPosition : Integer
        - kind : String
        - readAt : DateTime [0..1]
    }
    class DeliveryAttempt {
        <<entity>>
        - id : UUID
        - notificationId : UUID
        - channel : String
    }
    class NotificationPreference {
        <<entity>>
        - id : UUID
        - userId : UUID
        - status : String
    }
    class Discussion {
        <<entity>>
        - id : UUID
        - scientificObjectRefId : UUID
        - status : String
        - text : String
    }
    class ReviewComment {
        <<entity>>
        - id : UUID
        - reviewAssignmentId : UUID
        - status : String
    }
    class Membership {
        <<entity>>
        - id : UUID
        - tenantId : UUID
        - userId : UUID
        - projectId : UUID
        - status : String
        - validFrom : DateTime
        - validUntil : DateTime [0..1]
        - reason : String
        - grantedBy : UUID
    }
    CollaborationController ..> NotificationService : reads / marks read
    CollaborationController ..> NotificationPreferenceService : sets preferences
    CollaborationController ..> ReviewService : lists review queue
    CollaborationController ..> DecisionService : lists inbox
    CollaborationController ..> AuthorizationService : checks access
    CollaborationController ..> AuthenticationService : validates session
    NotificationService ..> NotificationPreferenceService : resolves settings
    NotificationService ..> IntegrationService : delivers external notice
    IntegrationService ..> NotificationChannel : delivers through
    NotificationService ..> Notification : creates / marks read
    NotificationService ..> DeliveryAttempt : queues / retries
    NotificationPreferenceService ..> NotificationPreference : updates
    IntegrationService ..> DeliveryAttempt : delivers
    CommentService ..> Discussion : anchors
    ReviewService ..> ReviewComment : lists queue
    ReviewService ..> Membership : reads memberships
    Notification "1" *-- "0..*" DeliveryAttempt : deliveries
    Discussion "0..*" -- "1" Membership : author
```

## 8. Administration & Monitoring

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class AdministrationController {
        <<controller>>
        +manageUsers(input : UserAdminInput) void
        +getUserDetail(userId : UUID) UserDetail
        +grantTenantAdmin(userId : UUID) void
        +revokeTenantAdmin(userId : UUID) void
        +listAllProjects() ProjectMetadata [0..∗]
        +configureModel(input : ModelInput) void
        +configureEngine(input : EngineInput) void
        +viewOverview() PlatformOverview
        +viewUsage(filter : UsageFilter) UsageReport
        +viewAudit(filter : AuditFilter) AuditEvent [0..∗]
        +viewLogs(filter : LogFilter) LogEntry [0..∗]
        +viewHealth() HealthSnapshot
        +acknowledgeAlert(alertId : UUID) void
        +viewMetrics(runId : UUID) OperatingMetrics
        +runBenchmark(catalogueVersion : String, modelProfileId : UUID) BenchmarkRun
        +pushUpdate(event : DomainEvent) void
    }
    class AdministrationService {
        <<service>>
        +updateUser(input : UserAdminInput) User
        +getUserDetail(userId : UUID) UserDetail
        +grantTenantAdmin(userId : UUID) void
        +revokeTenantAdmin(userId : UUID) void
        +listProjectMetadata() ProjectMetadata [0..∗]
        +configureModel(input : ModelInput) ModelOffering
        +configureEngine(input : EngineInput) ConfigVersion
        +setDefaultBudget(amount : Decimal) void
        +requireTenantAdmin(userId : UUID) void
    }
    class SecretService {
        <<service>>
        +seal(value : String) CredentialRef
        +rotate(ref : CredentialRef, value : String) void
        +resolveForExecution(ref : CredentialRef) Secret
        -preventSecretDisclosure() void
    }
    class MonitoringService {
        <<service>>
        +overview() PlatformOverview
        +usage(filter : UsageFilter) UsageReport
        +readAudit(filter : AuditFilter) AuditEvent [0..∗]
        +logs(filter : LogFilter) LogEntry [0..∗]
        +health() HealthSnapshot
        +acknowledgeAlert(alertId : UUID) void
        +metrics(runId : UUID) OperatingMetrics
        +onMonitoringEvent(event : MonitoringEvent) void
        +requireModelsAndCredentials(runId : UUID) void
    }
    class BenchmarkService {
        <<service>>
        +runBenchmark(catalogueVersion : String, modelProfileId : UUID) BenchmarkRun
    }
    class ModelProvider {
        <<external>>
        +testModel(profileRef : CredentialRef) CheckResult
    }
    class IdentityService {
        <<service>>
        +requestRoleChange(userId : UUID, change : RoleChange) ApprovalRequest
        +applyReceipt(receipt : AuthorityReceipt) void
    }
    class ApprovalService {
        <<service>>
        +createApprovalRequest(kind : String, digest : String) ApprovalRequest
        +vote(requestId : UUID) AuthorityReceipt
    }
    class IndependentReviewService {
        <<service>>
    }
    class Harness {
        <<service>>
    }
    class Tenant {
        <<entity>>
        - id : UUID
        - status : String
    }
    class User {
        <<entity>>
        - id : UUID
        - status : String
        - email : String
        - isTenantAdmin : Boolean
    }
    class Provider {
        <<entity>>
        - id : UUID
        - status : String
    }
    class ModelOffering {
        <<entity>>
        - id : UUID
        - providerId : UUID
        - status : String
    }
    class CredentialRef {
        <<entity>>
        - id : UUID
        - status : String
    }
    class CredentialBinding {
        <<entity>>
        - id : UUID
        - credentialRefId : UUID
        - projectId : UUID
        - status : String
        - validFrom : DateTime
        - validUntil : DateTime [0..1]
        - reason : String
        - grantedBy : UUID
    }
    class CredentialLease {
        <<entity>>
        - id : UUID
        - credentialBindingId : UUID
    }
    class ConfigVersion {
        <<entity>>
        - id : UUID
        - settingDefinitionId : UUID
        - status : String
    }
    class RunAttempt {
        <<entity>>
        - id : UUID
        - runRequestId : UUID
        - status : String
    }
    class RunTimelineEntry {
        <<entity>>
        - id : UUID
        - runRequestId : UUID
        - runPlanStepId : UUID
    }
    class UsageEvent {
        <<entity>>
        - id : UUID
        - runAttemptId : UUID
    }
    class LedgerEntry {
        <<entity>>
        - id : UUID
        - usageEventId : UUID
        - budgetReservationId : UUID
    }
    class AuditEvent {
        <<entity>>
        - id : UUID
        - userId : UUID
        - auditCheckpointId : UUID
        - action : String
        - time : DateTime
    }
    class AuditCheckpoint {
        <<entity>>
        - id : UUID
    }
    class Incident {
        <<entity>>
        - id : UUID
        - status : String
    }
    AdministrationController ..> AdministrationService : configures platform
    AdministrationController ..> MonitoringService : reads operation
    AdministrationController ..> BenchmarkService : runs benchmark
    AdministrationController ..> IdentityService : changes Tenant Admin
    IdentityService ..> ApprovalService : requests approval
    AdministrationService ..> SecretService : seals keys
    AdministrationService ..> ModelProvider : tests model
    BenchmarkService ..> IndependentReviewService : runs personas
    BenchmarkService ..> Harness : scores cases
    AdministrationService ..> User : manages accounts
    AdministrationService ..> ModelOffering : configures models
    SecretService ..> CredentialBinding : binds credential
    AdministrationService ..> ConfigVersion : publishes settings
    SecretService ..> CredentialRef : seals / rotates
    SecretService ..> CredentialLease : leases to run
    MonitoringService ..> RunAttempt : checks before start
    MonitoringService ..> RunTimelineEntry : records failure
    MonitoringService ..> UsageEvent : reads usage
    MonitoringService ..> LedgerEntry : reads charges
    MonitoringService ..> AuditEvent : reads audit
    MonitoringService ..> AuditCheckpoint : verifies chain
    MonitoringService ..> Incident : raises / acknowledges
    Tenant "1" -- "0..*" User : users
    Provider "1" *-- "0..*" ModelOffering : offerings
    CredentialRef "1" -- "0..*" CredentialBinding : bindings
    CredentialRef "1" -- "0..*" CredentialLease : leases
    UsageEvent "1" -- "0..*" LedgerEntry : charges
    AuditCheckpoint "1" -- "0..*" AuditEvent : covers
```

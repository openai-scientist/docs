# Class Diagrams — Mermaid

Xuất từ [class_model.py](class_model.py) bằng [build_class_diagrams.py](build_class_diagrams.py), cùng nội dung với file draw.io; mỗi khối đặt nền trắng, chữ và nét đen. Class chỉ có tên (không ngăn thành viên) thuộc nhóm khác và được vẽ lại để thể hiện phụ thuộc. Chạy lại builder sẽ ghi đè các chỉnh tay trong file này.

## 1. Authentication & Account

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class AuthenticationController {
        <<controller>>
        +requestEmailCode(email : String) void
        +signInWithCode(input : EmailCode) AuthSession
        +signInWithGoogle(code : String) AuthSession
        +currentSession(token : String) User
        +completeOnboarding(input : ProfileInput) User
        +updateProfile(input : ProfileInput) User
        +signOut(sessionId : UUID) void
    }
    class AuthenticationService {
        <<service>>
        +requestCode(email : String) void
        +verifyCode(input : EmailCode) AuthSession
        +signInGoogle(code : String) AuthSession
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
        - email : String
        - displayName : String [0..1]
        - avatarUrl : String [0..1]
        - isPlatformAdmin : Boolean
    }
    class EmailChallenge {
        <<entity>>
        - id : UUID
        - email : String
        - codeDigest : String
        - expiresAt : DateTime
        - consumedAt : DateTime [0..1]
    }
    class AuthSession {
        <<entity>>
        - id : UUID
        - expiresAt : DateTime
        - revokedAt : DateTime [0..1]
    }
    class Membership {
        <<entity>>
        - projectId : UUID
        - role : ProjectRole
    }
    class ProjectRole {
        <<enumeration>>
        PROJECT#95;MANAGER
        RESEARCHER
        REVIEWER
    }
    AuthenticationController ..> AuthenticationService : signs in / out
    AuthenticationController ..> AccountService : updates profile
    AuthenticationController ..> AuthorizationService : checks access
    AuthenticationService ..> GoogleIdentityProvider : verifies identity
    AuthenticationService ..> EmailDelivery : sends code
    AuthenticationService ..> EmailChallenge : issues / consumes
    AuthenticationService ..> AuthSession : manages sessions
    AuthenticationService ..> User : resolves verified email
    AccountService ..> User : updates
    AuthorizationService ..> Membership : checks project role
    User "1" -- "0..*" Membership : memberships
    User "1" *-- "0..*" AuthSession : sessions
    Membership ..> ProjectRole : uses type
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
        +configure(projectId : UUID, settings : ProjectSettings) void
        +configureIntegration(projectId : UUID, input : IntegrationInput) void
        +testIntegration(integrationId : UUID) CheckResult
        +removeIntegration(integrationId : UUID) void
        +setNotificationPreferences(projectId : UUID, input : PreferencesInput) void
        +listActivity(projectId : UUID, filter : ActivityFilter) AuditLogEntry [0..∗]
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
        +configure(settings : ProjectSettings) void
        +listActivity(projectId : UUID, filter : ActivityFilter) AuditLogEntry [0..∗]
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
        - name : String
        - status : ProjectStatus
        - ownerId : UUID
    }
    class ProjectStatus {
        <<enumeration>>
        active
        completed
        archived
    }
    class ProjectSettings {
        <<entity>>
        - monthlyBudget : Decimal
        - warningThresholds : Decimal [0..∗]
        - defaultPresetPerStage : Map
        - reviewSettings : ReviewSettings
        - notificationChoices : Map
        - pinnedWaitDeadline : Duration
    }
    class Membership {
        <<entity>>
        - projectId : UUID
        - role : ProjectRole
        - dateAdded : DateTime
    }
    class User {
        <<entity>>
        - id : UUID
        - email : String
    }
    class Invitation {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - email : String
        - role : ProjectRole
        - expiresAt : DateTime
        - status : String
    }
    class Document {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - name : String
        - version : Integer
    }
    class AuditLogEntry {
        <<entity>>
        - action : String
        - actorId : UUID
        - projectId : UUID [0..1]
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
    ProjectService ..> AuditLogEntry : records changes
    MembershipService ..> Membership : maintains
    InvitationService ..> Invitation : issues / resolves
    DocumentService ..> Document : stores
    Project ..> ProjectStatus : uses type
    Project "1" *-- "1" ProjectSettings : settings
    Project "1" -- "0..*" Membership : memberships
    Membership "0..*" -- "1" User : member
```

## 3. Data Management

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class DataController {
        <<controller>>
        +upload(input : UploadInput) DatasetVersion
        +getDataset(datasetId : UUID) DatasetDetail
        +renameDataset(datasetId : UUID, name : String) void
        +deleteDataset(datasetId : UUID) void
        +uploadVersion(datasetId : UUID, input : UploadInput) DatasetVersion
        +preview(versionId : UUID) TablePreview
        +download(versionId : UUID) File
        +importData(connectionId : UUID) DatasetVersion
        +browseConnection(connectionId : UUID, schema : String) TableRef [0..∗]
        +previewSource(connectionId : UUID, source : AnySource) TablePreview
        +renameConnection(connectionId : UUID, name : String) void
        +testConnection(connectionId : UUID) CheckResult
        +deleteConnection(connectionId : UUID) void
        +connectGoogle(projectId : UUID) DataConnection
        +requestPairingCode(projectId : UUID) PairingCode
        +pairNode(code : String) LocalNode
        +proposeDatasets(nodeId : UUID, manifests : Manifest [1..∗]) void
        +revokeNode(nodeId : UUID) void
        +pushUpdate(event : DomainEvent) void
    }
    class DataService {
        <<service>>
        +createDataset(input : DatasetInput) Dataset
        +getDetail(datasetId : UUID) DatasetDetail
        +rename(datasetId : UUID, name : String) void
        +delete(datasetId : UUID) void
        +addVersion(datasetId : UUID, input : UploadInput) DatasetVersion
        +preview(versionId : UUID) TablePreview
        +download(versionId : UUID) File
        +importData(connection : DataConnection) DatasetVersion
        +browse(connectionId : UUID, schema : String) TableRef [0..∗]
        +previewSource(connectionId : UUID, source : AnySource) TablePreview
        +renameConnection(connectionId : UUID, name : String) void
        +testConnection(connectionId : UUID) CheckResult
        +deleteConnection(connectionId : UUID) void
        +authorizeGoogle(projectId : UUID) DataConnection
        -blockInternalHosts(uri : String) void
        -rejectLocalPreview(dataset : Dataset) void
    }
    class DatasetVersionService {
        <<service>>
        +create(datasetId : UUID, source : String) DatasetVersion
        +verifyHash(version : DatasetVersion) Boolean
        -preventOverwrite(versionId : UUID) void
    }
    class LocalNodeService {
        <<service>>
        +issuePairingCode(projectId : UUID) PairingCode
        +pair(projectId : UUID, code : String) LocalNode
        +registerDatasets(nodeId : UUID, manifests : Manifest [1..∗]) Dataset [1..∗]
        +route(job : LocalJob) JobResult
        +heartbeat(nodeId : UUID) void
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
        +#95;#95;call#95;#95;(kind : String, config : Map, secret : Map) Connector
    }
    class Connector {
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
        +check(job : LocalJob, result : Aggregate) Release
        +recordRelease(release : Release) void
        -applyFirewall(result : Aggregate) void
        -round(result : Aggregate) Aggregate
        -checkDisclosure(result : Aggregate) void
        -checkDifferencing(result : Aggregate) void
        -checkProbeBudget(versionId : UUID) void
    }
    class Dataset {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - name : String
        - location : DataLocation
    }
    class DatasetVersion {
        <<entity>>
        - id : UUID
        - contentHash : String
        - source : String
        - createdAt : DateTime
    }
    class DataLocation {
        <<enumeration>>
        platform
        local
    }
    class DataConnection {
        <<entity>>
        - id : UUID
        - provider : String
        - authorizationScope : String
        - credentialRef : SecretRef
    }
    class LocalNode {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - status : LocalNodeStatus
        - lastSeenAt : DateTime [0..1]
        - revokedAt : DateTime [0..1]
    }
    class LocalNodeStatus {
        <<enumeration>>
        pairing
        online
        offline
        revoked
    }
    class ReleaseLog {
        <<entity>>
        - datasetVersionId : UUID
        - appendOnly : Boolean
    }
    class Release {
        <<entity>>
        - id : UUID
        - jobId : UUID
        - kind : String
        - reason : String
        - time : DateTime
    }
    DataController ..> DataService : manages datasets
    DataController ..> LocalNodeService : manages Local Nodes
    DataController ..> AuthorizationService : checks access
    DataService ..> DatasetVersionService : creates versions
    DataService ..> SecretService : seals credentials
    DataService ..> ConnectorFactory : uses factory
    DataService ..> GoogleIdentityProvider : authorizes Google source
    DataService ..> Dataset : manages
    ConnectorFactory ..> Connector : creates connector
    GoogleSheetsConnector ..|> Connector : implements
    DatasetVersionService ..> DatasetVersion : creates / verifies
    ExecutionEngine ..> LocalNodeService : routes local job
    LocalNodeService ..> LocalNodeAgent : dispatches jobs
    LocalNodeService ..> NotificationService : sends offline notice
    LocalNodeService ..> RunOrchestrator : resumes waiting run
    LocalNodeService ..> LocalNode : pairs / revokes
    LocalNodeAgent ..> ReleaseGate : checks aggregates
    ReleaseGate ..> ReleaseLog : appends
    Dataset "1" *-- "0..*" DatasetVersion : versions
    Dataset ..> DataLocation : uses type
    Dataset "0..*" -- "0..1" DataConnection : imports from
    LocalNode ..> LocalNodeStatus : uses type
    ReleaseLog "1" *-- "0..*" Release : releases
```

## 4. Research Run Orchestration

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class RunController {
        <<controller>>
        +start(caseId : UUID) Run
        +amendCase(input : Amendment) ResearchCase
        +getRun(runId : UUID) RunSnapshot
        +listRuns(projectId : UUID, filter : RunFilter) Run [0..∗]
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
        +addComment(input : CommentInput) Comment
        +editComment(commentId : UUID, text : String) void
        +deleteComment(commentId : UUID) void
        +lockPlan(planId : UUID) Lock
        +requestDeviation(planId : UUID, change : String, reason : String) DecisionInboxItem
        +reviewSpending(itemId : UUID, approve : Boolean) void
        +approveDossier(dossierId : UUID) Approval
        +export(dossierId : UUID, format : String) Export
        +pushUpdate(event : DomainEvent) void
    }
    class RunOrchestrator {
        <<service>>
        +start(caseId : UUID) Run
        +getSnapshot(runId : UUID) RunSnapshot
        +listRuns(projectId : UUID, filter : RunFilter) Run [0..∗]
        +advance(runId : UUID) StageRun
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
        +create(input : CaseInput) ResearchCase
        +amend(caseId : UUID, change : CaseChange, reason : String) ResearchCase
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
        +createFromAccepted(packId : UUID) Dossier
        +approve(dossierId : UUID) Approval
        +exportApproved(dossierId : UUID, format : String) Export
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
    class ResearchCase {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - version : Integer
        - objective : String
        - constraints : String
        - datasetVersionId : UUID [0..1]
        - amendmentReason : String [0..1]
    }
    class Run {
        <<entity>>
        - id : UUID
        - state : RunState
        - waitingReason : WaitingReason [0..1]
        - endingOutcome : EndingOutcome [0..1]
        - tokenBudget : Integer
        - researchCaseRef : VersionRef
        - pipeline : String = dataset#95;first
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
    class StageRun {
        <<entity>>
        - id : UUID
        - stage : String
        - preset : String
        - presenceAtStart : String
        - contractStatus : String
    }
    class HandOffObject {
        <<entity>>
        - id : UUID
        - version : Integer
        - contentHash : String
        - state : String
        - upstreamRefs : VersionRef [0..∗]
    }
    class BudgetLedger {
        <<entity>>
        - projectId : UUID
        - month : String
        - spending : Decimal
        - notifiedThresholds : Decimal [0..∗]
    }
    class Dossier {
        <<entity>>
        - id : UUID
        - version : Integer
        - evidenceBundleRef : VersionRef
        - paperPackRef : VersionRef
        - approvalState : String
    }
    class Approval {
        <<entity>>
        - membershipId : UUID
        - dossierVersion : Integer
        - decision : String
        - time : DateTime
    }
    class Export {
        <<entity>>
        - dossierVersion : Integer
        - format : String
        - approvedActionRef : UUID
        - auditEntryRef : UUID
    }
    RunController ..> RunOrchestrator : controls runs
    RunController ..> ResearchCaseService : amends cases
    RunController ..> BudgetService : raises budget / reviews spending
    RunController ..> DossierService : approves / exports
    RunController ..> AuthorizationService : checks access
    RunController ..> LockService : locks plan
    RunController ..> CommentService : comments
    RunOrchestrator ..> DatasetEngine : schedules stages
    RunOrchestrator ..> Run : orchestrates
    ResearchCaseService ..> ResearchCase : versions
    BudgetService ..> RunOrchestrator : resumes / ends run
    BudgetService ..> NotificationService : alerts Project Managers
    BudgetService ..> DecisionService : creates spending item
    BudgetService ..> BudgetLedger : records usage
    DossierService ..> Dossier : versions / checks
    Run "0..*" -- "1" ResearchCase : pinned case
    Run ..> RunState : uses type
    Run ..> WaitingReason : uses type
    Run ..> EndingOutcome : uses type
    Run "1" *-- "0..*" StageRun : stages
    StageRun "1" -- "0..*" HandOffObject : outputs
    Dossier ..> HandOffObject : references accepted versions
    Dossier "1" *-- "0..*" Approval : approvals
    Dossier "1" -- "0..*" Export : exports
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
        +execute(lock : Lock) EvidenceBundle
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
        +lock(planId : UUID) Lock
        +requestDeviation(planId : UUID, change : String, reason : String) DecisionInboxItem
    }
    class IndependentReviewService {
        <<service>>
        +review(object : HandOffObject) Finding [0..∗]
        -enforceTwoRounds(round : Integer) void
    }
    class ReviewerPersona {
        <<service>>
        +review(object : HandOffObject, fields : String [1..∗]) Finding [0..∗]
    }
    class MakerPersona {
        <<service>>
        +revise(objectId : UUID, findings : Finding [1..∗]) HandOffObject
    }
    class Harness {
        <<service>>
        +checkContract(object : HandOffObject) CheckResult
        +enforcePipelineOrder(plan : AnalysisPlan) void
        +renderNumbers(records : Record [0..∗]) String
        +computeProfile(versionId : UUID) Profile
        +createSplit(snapshotId : UUID, policy : SplitPolicy) SplitSpec
        +validatePortfolio(set : HypothesisSet) CheckResult
        +rehearseOnTwin(plan : AnalysisPlan) CheckResult
        +checkDisclosureEligibility(lockId : UUID) CheckResult
        +computeVerdicts(input : EvidenceInput) Verdict [1..∗]
        +validateClaimsAndCitations(pack : PaperPack) CheckResult
        +verifyFindings(findings : Finding [1..∗]) Finding [0..∗]
        +recheckChangedFields(objectId : UUID) CheckResult
        +scoreCase(caseId : UUID, findings : Finding [0..∗]) CaseResult
        +computeBenchmarkMetrics(benchmarkRunId : UUID) BenchmarkMetrics
    }
    class ScholarlySource {
        <<external>>
        +search(query : String) SourceRecord [0..∗]
    }
    class IsolatedExecutor {
        <<external>>
        +runTwin(lock : Lock) Diagnostics
        +dryRun(lock : Lock) Diagnostics
        +runConfirmatory(lock : Lock) JobStatus
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
    class LiteratureBase {
        <<entity>>
        - projectId : UUID
        - version : Integer
        - searchProtocol : String
        - searchLog : SearchEntry [0..∗]
        - screeningDecisions : ScreeningDecision [0..∗]
        - evidenceCards : EvidenceCard [0..∗]
    }
    class AnalysisPlan {
        <<entity>>
        - hypothesisSetRef : VersionRef
        - patternRefs : VersionRef [0..∗]
        - taskFamily : String
        - pipelineOrder : String [1..∗]
        - interpretationTable : Table
    }
    class Lock {
        <<entity>>
        - analysisPlanRef : VersionRef
        - specHash : String
        - programHash : String
        - splitDigest : String
        - lockedBy : UUID
        - lockedAt : DateTime
    }
    class ConfirmatoryResults {
        <<entity>>
        - lockId : UUID
        - state : String
        - results : Result [0..∗]
        - disclosedAt : DateTime [0..1]
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
    class Finding {
        <<entity>>
        - anchor : ObjectFieldRef
        - evidence : EvidenceRef
        - severity : String
        - verificationResult : String
        - proposedFix : String
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
    LiteratureService ..> LiteratureBase : versions
    ExperimentDesignEngine ..> AnalysisPlan : publishes
    LockService ..> Lock : writes
    ExecutionEngine ..> EvidenceBundle : publishes
    PaperEngine ..> PaperPack : publishes
    IndependentReviewService ..> Finding : records
    HypothesisSet "0..*" -- "1" LiteratureBase : pins version
    Lock "1" *-- "1" ConfirmatoryResults : confirmatory results
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
        +submitCharter(runId : UUID, input : CharterInput) Charter
        +endorseAdvice(consultationId : UUID) void
        +retryConsultation(consultationId : UUID) void
        +getLabNotebook(runId : UUID) LabNotebookEntry [0..∗]
        +getPiOverview(runId : UUID) PiOverview
        +triage(itemId : UUID, decision : String) void
        +pushUpdate(event : DomainEvent) void
    }
    class DecisionService {
        <<service>>
        +createRequest(input : DecisionInput) DecisionInboxItem
        +answer(itemId : UUID, option : String) void
        +confirmTentative(itemId : UUID) void
        +overturn(itemId : UUID, reason : String) void
        +listActionable(userId : UUID) DecisionInboxItem [0..∗]
        +submitCharter(runId : UUID, input : CharterInput) Charter
        +requestConsultation(runId : UUID, trigger : String) Consultation
        +endorseAdvice(consultationId : UUID) void
        +retryConsultation(consultationId : UUID) Consultation
        +getLabNotebook(runId : UUID) LabNotebookEntry [0..∗]
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
        +decideTentatively(item : DecisionInboxItem) void
        +proposeNextStep(runId : UUID) String
        -rejectPinnedDecision(item : DecisionInboxItem) void
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
    class DecisionInboxItem {
        <<entity>>
        - id : UUID
        - kind : String
        - options : String [1..∗]
        - proposedOption : String
        - status : String
        - pinned : Boolean
        - waitDeadline : DateTime [0..1]
    }
    class DecisionLogEntry {
        <<entity>>
        - actionType : String
        - level : ActionLevel
        - policyVersion : Integer
        - decidedBy : String
        - presence : Presence
        - overturned : Boolean
    }
    class ActionPolicy {
        <<entity>>
        - version : Integer
        - presetPerStage : Map
        - overrides : Map
        - floors : Map
        - spendingCeiling : Decimal
    }
    class ActionLevel {
        <<enumeration>>
        auto
        do#95;then#95;review
        must#95;ask
    }
    class Charter {
        <<entity>>
        - runId : UUID
        - version : Integer
        - goals : String
        - limits : String
        - mustAskMatters : String [0..∗]
    }
    class Consultation {
        <<entity>>
        - runId : UUID
        - trigger : String
        - status : String
        - advice : String [0..1]
        - endorsed : Boolean
    }
    class LabNotebookEntry {
        <<entity>>
        - runId : UUID
        - summary : String
        - proposal : String [0..1]
        - tentativeDecisionRef : UUID [0..1]
        - reason : String
        - presence : Presence
    }
    class Presence {
        <<enumeration>>
        present
        away
    }
    class Run {
        <<entity>>
        - id : UUID
        - state : RunState
        - endingOutcome : EndingOutcome [0..1]
    }
    DecisionController ..> DecisionService : answers / consults
    DecisionController ..> ActionPolicyService : changes policy
    DecisionController ..> AuthorizationService : checks access
    DecisionController ..> ExecutionEngine : triages candidates
    DecisionService ..> AIPrincipalInvestigator : consults
    DecisionService ..> OverturnMetricService : measures overturns
    DecisionService ..> RunOrchestrator : resumes / marks stale
    DecisionService ..> DecisionInboxItem : creates / resolves
    DecisionService ..> Charter : records
    DecisionService ..> Consultation : records
    ActionPolicyService ..> ActionPolicy : versions
    AIPrincipalInvestigator ..> LabNotebookEntry : writes
    OverturnMetricService ..> Run : measures by run
    DecisionInboxItem "1" -- "0..1" DecisionLogEntry : decided record
    ActionPolicy ..> ActionLevel : uses type
    LabNotebookEntry ..> Presence : uses type
    Run "1" -- "0..1" Charter : charter
    Run "1" -- "0..*" Consultation : consultations
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
        +listInbox() DecisionInboxItem [0..∗]
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
        -allowExternalNotice(item : DecisionInboxItem) Boolean
        -selectAuthorizedRecipients(item : DecisionInboxItem) UUID [0..∗]
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
        -resolveSealedCredential(ref : SecretRef) void
    }
    class CommentService {
        <<service>>
        +add(input : CommentInput) Comment
        +list(objectRef : ObjectRef) Comment [0..∗]
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
        - recipientId : UUID
        - kind : String
        - status : String
        - readAt : DateTime [0..1]
        - decisionItemId : UUID [0..1]
    }
    class NotificationEmail {
        <<entity>>
        - id : UUID
        - notificationId : UUID
        - status : EmailStatus
        - attempts : Integer
        - lastError : String [0..1]
    }
    class EmailStatus {
        <<enumeration>>
        pending
        sending
        sent
        failed
        skipped
    }
    class DecisionInboxItem {
        <<entity>>
        - id : UUID
        - kind : String
        - pinned : Boolean
        - blocking : Boolean
        - waitDeadline : DateTime [0..1]
    }
    class NotificationPreference {
        <<entity>>
        - projectId : UUID
        - userId : UUID
        - eventChoices : Map
        - channels : String [0..∗]
    }
    class ProjectIntegration {
        <<entity>>
        - projectId : UUID
        - provider : String
        - credentialRef : SecretRef
        - enabled : Boolean
    }
    class Comment {
        <<entity>>
        - id : UUID
        - membershipId : UUID
        - text : String
        - anchor : ObjectFieldRef
    }
    class Membership {
        <<entity>>
        - projectId : UUID
        - role : ProjectRole
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
    NotificationService ..> NotificationEmail : queues / retries
    NotificationPreferenceService ..> NotificationPreference : updates
    IntegrationService ..> ProjectIntegration : configures
    CommentService ..> Comment : anchors
    ReviewService ..> Membership : reads memberships
    Notification "1" -- "0..1" NotificationEmail : email
    NotificationEmail ..> EmailStatus : uses type
    Notification "0..*" -- "0..1" DecisionInboxItem : decision context
    Comment "0..*" -- "1" Membership : author
```

## 8. Administration & Monitoring

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'mainBkg': '#ffffff', 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'textColor': '#000000', 'fontFamily': 'Arial'}}}%%
classDiagram
    class AdministrationController {
        <<controller>>
        +manageUsers(input : UserAdminInput) void
        +getUserDetail(userId : UUID) UserDetail
        +grantPlatformAdmin(userId : UUID) void
        +revokePlatformAdmin(userId : UUID) void
        +listAllProjects() ProjectMetadata [0..∗]
        +configureModel(input : ModelInput) void
        +configureEngine(input : EngineInput) void
        +viewOverview() PlatformOverview
        +viewUsage(filter : UsageFilter) UsageReport
        +viewAudit(filter : AuditFilter) AuditLogEntry [0..∗]
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
        +grantPlatformAdmin(userId : UUID) void
        +revokePlatformAdmin(userId : UUID) void
        +listProjectMetadata() ProjectMetadata [0..∗]
        +configureModel(input : ModelInput) ModelProfile
        +configureEngine(input : EngineInput) EngineSettings
        +setDefaultBudget(amount : Decimal) void
        +requirePlatformAdmin(userId : UUID) void
    }
    class SecretService {
        <<service>>
        +seal(value : String) SecretRef
        +rotate(ref : SecretRef, value : String) void
        +resolveForExecution(ref : SecretRef) Secret
        -preventSecretDisclosure() void
    }
    class MonitoringService {
        <<service>>
        +overview() PlatformOverview
        +usage(filter : UsageFilter) UsageReport
        +readAudit(filter : AuditFilter) AuditLogEntry [0..∗]
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
        +testModel(profileRef : SecretRef) CheckResult
    }
    class IndependentReviewService {
        <<service>>
    }
    class Harness {
        <<service>>
    }
    class User {
        <<entity>>
        - id : UUID
        - email : String
        - status : String
        - isPlatformAdmin : Boolean
    }
    class ModelProfile {
        <<entity>>
        - id : UUID
        - modelRole : String
        - model : String
        - keyRef : SecretRef
        - unitPrice : Decimal
    }
    class EngineSettings {
        <<entity>>
        - engineId : String
        - enabled : Boolean
        - configuration : Map
    }
    class SealedSecret {
        <<entity>>
        - id : UUID
        - encryptedValue : Bytes
        - keyVersion : String
        - updatedAt : DateTime
    }
    class AuditLogEntry {
        <<entity>>
        - action : String
        - actorId : UUID
        - projectId : UUID [0..1]
        - time : DateTime
    }
    class HealthSnapshot {
        <<entity>>
        - collectedAt : DateTime
        - componentStates : Map
    }
    class MonitoringAlert {
        <<entity>>
        - id : UUID
        - component : String
        - severity : String
        - state : AlertState
        - acknowledgedBy : UUID [0..1]
        - acknowledgedAt : DateTime [0..1]
        - resolvedAt : DateTime [0..1]
    }
    class AlertState {
        <<enumeration>>
        active
        resolved
    }
    class OperatingMetrics {
        <<entity>>
        - runId : UUID
        - questionCount : Integer
        - blockedTime : Duration
        - overturnRates : Map
        - personaPrecision : Map
    }
    class BenchmarkRun {
        <<entity>>
        - id : UUID
        - catalogueVersion : String
        - modelProfileId : UUID
        - personaPrecision : Map
        - leakageDetectionRate : Decimal
        - orderBlockRate : Decimal
        - finishedAt : DateTime [0..1]
    }
    AdministrationController ..> AdministrationService : configures platform
    AdministrationController ..> MonitoringService : reads operation
    AdministrationController ..> BenchmarkService : runs benchmark
    AdministrationService ..> SecretService : seals keys
    AdministrationService ..> ModelProvider : tests model
    AdministrationService ..> User : manages accounts
    AdministrationService ..> ModelProfile : configures model roles
    AdministrationService ..> EngineSettings : configures engines
    SecretService ..> SealedSecret : seals / rotates
    MonitoringService ..> AuditLogEntry : reads append-only log
    MonitoringService ..> HealthSnapshot : reads health
    MonitoringService ..> MonitoringAlert : raises / acknowledges
    MonitoringService ..> OperatingMetrics : computes
    BenchmarkService ..> IndependentReviewService : runs personas
    BenchmarkService ..> Harness : scores cases
    BenchmarkService ..> BenchmarkRun : records
    MonitoringAlert ..> AlertState : uses type
    BenchmarkRun "0..*" -- "1" ModelProfile : model under test
```

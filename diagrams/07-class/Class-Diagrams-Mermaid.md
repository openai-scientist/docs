# Class Diagram — Mermaid (8 nhóm feature)

Mỗi khối là một sơ đồ độc lập. Dán khối `mermaid` vào trình hỗ trợ Mermaid hoặc diagrams.net để tiếp tục chỉnh bố cục. `direction TB` đặt hướng từ trên xuống; Mermaid tự quyết định vị trí thực tế nên có thể cần di chuyển thủ công sau khi import.

Nguồn nội dung: [diagram editable hiện tại](Class-Diagram-Authentication-Account.drawio), [thuyết minh](Class-Diagrams-design.md), [Report IV](../../report/04-software-design-document.md) và [Report III](../../report/03-software-requirements-specification.md). Controller/service, một số class, thành viên và chữ ký là thiết kế đề xuất, không mặc định là code/API thực tế. Local Node là thiết kế dự kiến, chưa triển khai.

Ký hiệu: `..>` dependency (mũi tên mở tới bên được dùng); `--` association; `*--` composition (thoi đặc ở bên toàn thể); `..|>` realization (tam giác rỗng tại interface). Số trong dấu nháy nằm ở đúng đầu quan hệ. Chỉ dùng composition khi có căn cứ về sở hữu và vòng đời; không đổi các association khác chỉ để đủ loại.

Các composition sau là **lựa chọn mô hình hóa đề xuất** cho sơ đồ vẽ tay; thoi đặc luôn đặt ở phía toàn thể:

| Toàn thể | Thành phần | Cách hiểu trong sơ đồ và căn cứ |
|---|---|---|
| `User` | `AuthSession` | Session thuộc một user; model backend gắn session với user. |
| `Project` | `ProjectSettings` | Cấu hình riêng của project; đối chiếu thiết kế và model backend. |
| `Dataset` | `DatasetVersion` | Mỗi version là thành phần thuộc một dataset; version cũ vẫn được giữ bất biến. |
| `Run` | `StageRun` | Mỗi stage run là một phần của lần chạy tương ứng. |
| `Dossier` | `Approval` | Approval thuộc đúng một phiên bản Dossier và không chuyển sang phiên bản mới. |
| `Lock` | `Envelope` | Envelope gắn với một Lock; mô hình này coi envelope là thành phần của lock. |

Các dấu thoi trên thể hiện giả định sở hữu/vòng đời ở mức thiết kế, **không tự khẳng định database phải xóa dây chuyền** hoặc xóa lịch sử. Report mô tả quan hệ và việc lưu giữ, nhưng chưa xác định đầy đủ vòng đời khi xóa cho mọi cặp; cần người phụ trách thiết kế xác nhận, đặc biệt với DatasetVersion, StageRun, Approval và Envelope. Hiện `DatasetVersion` và `StageRun` trong backend có `RESTRICT`, nên không diễn giải composition là xóa cascade. Sáu quan hệ composition đã được đồng bộ sang [file draw.io](Class-Diagram-Authentication-Account.drawio).

`DecisionInboxItem`–`DecisionLogEntry` giữ association vì log còn liên quan lịch sử/audit và chưa rõ có được sở hữu độc quyền bởi item hay không. `GoogleSheetsConnector ..|> Connector` mô tả sự phù hợp cấu trúc với Python Protocol; signature connector đã rút gọn ở mức UML. Xem [thuyết minh](Class-Diagrams-design.md) để phân biệt đề xuất thiết kế và implementation.

## 1. Authentication & Account

11 classifier; 14 quan hệ.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "secondaryColor": "#ffffff", "tertiaryColor": "#ffffff", "lineColor": "#000000", "textColor": "#000000", "background": "#ffffff"}}}%%
classDiagram
    direction TB
    class AuthenticationController {
        <<controller>>
        + requestEmailCode(email : String) : void
        + signInWithCode(input : EmailCode) : AuthSession
        + signInWithGoogle(code : String) : AuthSession
        + completeOnboarding(input : ProfileInput) : User
        + updateProfile(input : ProfileInput) : User
        + signOut(sessionId : UUID) : void
    }
    class AuthenticationService {
        <<service>>
        + requestCode(email : String) : void
        + verifyCode(input : EmailCode) : AuthSession
        + signInGoogle(code : String) : AuthSession
        + validateSession(token : String) : User
        + revokeSession(sessionId : UUID) : void
        - resolveUser(email : String) : User
    }
    class GoogleIdentityProvider {
        <<external>>
        + verifyIdentity(code : String) : Identity
    }
    class EmailDelivery {
        <<external>>
        + sendCode(email : String, code : String) : void
    }
    class AccountService {
        <<service>>
        + completeOnboarding(input : ProfileInput) : User
        + updateProfile(input : ProfileInput) : User
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
    class AuthorizationService {
        <<service>>
        + requireRole(user : User, projectId : UUID, action : Action) : void
        + canReadMetadata(user : User) : Boolean
    }
    class Membership {
        <<entity>>
        - projectId : UUID
        - role : ProjectRole
    }
    class AuthSession {
        <<entity>>
        - id : UUID
        - expiresAt : DateTime
        - revokedAt : DateTime [0..1]
    }
    class ProjectRole {
        <<enumeration>>
        PROJECT_MANAGER
        RESEARCHER
        REVIEWER
    }
    AuthenticationController ..> AuthenticationService : uses
    AuthenticationController ..> AccountService : updates profile
    AuthenticationController ..> AuthorizationService : checks access
    AuthenticationService ..> GoogleIdentityProvider : verifies identity
    AuthenticationService ..> EmailDelivery : sends code
    AuthenticationService ..> User : resolves verified email
    AuthenticationService ..> EmailChallenge : issues / consumes
    AuthenticationService ..> AuthSession : manages sessions
    AccountService ..> User : updates
    AuthorizationService ..> User : checks platform rights
    AuthorizationService ..> Membership : checks project role
    User "1" -- "0..*" Membership : memberships
    User "1" *-- "0..*" AuthSession : sessions
    Membership ..> ProjectRole : uses type
```

## 2. Project Workspace

12 classifier; 12 quan hệ.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "secondaryColor": "#ffffff", "tertiaryColor": "#ffffff", "lineColor": "#000000", "textColor": "#000000", "background": "#ffffff"}}}%%
classDiagram
    direction TB
    class ProjectController {
        <<controller>>
        + create(input : ProjectInput) : Project
        + update(projectId : UUID, input : ProjectInput) : void
        + archive(projectId : UUID) : void
        + manageMembers(projectId : UUID) : void
        + manageInvitations(projectId : UUID) : void
        + manageDocuments(projectId : UUID) : void
        + configure(projectId : UUID, settings : ProjectSettings) : void
    }
    class ProjectService {
        <<service>>
        + create(input : ProjectInput) : Project
        + update(projectId : UUID, input : ProjectInput) : void
        + archive(projectId : UUID) : void
        + configure(settings : ProjectSettings) : void
        + recordChange(action : String) : void
    }
    class Project {
        <<entity>>
        - id : UUID
        - name : String
        - status : String
    }
    class ProjectSettings {
        <<entity>>
        - monthlyBudget : Decimal
        - defaultPresetPerStage : Map
        - reviewSettings : ReviewSettings
        - notificationChoices : Map
        - pinnedWaitDeadline : Duration
    }
    class MembershipService {
        <<service>>
        + changeRole(memberId : UUID, role : ProjectRole) : void
        + remove(memberId : UUID) : void
        + transferOwnership(projectId : UUID, userId : UUID) : void
        - requireActiveManager(projectId : UUID) : void
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
    class InvitationService {
        <<service>>
        + invite(projectId : UUID, email : String) : Invitation
        + accept(invitationId : UUID) : Membership
        + decline(invitationId : UUID) : void
        + resend(invitationId : UUID) : void
        + cancel(invitationId : UUID) : void
        - rejectExpired(invitation : Invitation) : void
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
    class DocumentService {
        <<service>>
        + add(projectId : UUID, input : DocumentInput) : Document
        + update(documentId : UUID, input : DocumentInput) : void
        + list(projectId : UUID) : Document [0..*]
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
    ProjectController ..> ProjectService : uses
    ProjectController ..> MembershipService : manages members
    ProjectController ..> InvitationService : manages invitations
    ProjectController ..> DocumentService : manages documents
    ProjectService ..> Project : manages
    MembershipService ..> Membership : maintains
    InvitationService ..> Invitation : issues / resolves
    DocumentService ..> Document : versions
    Project "1" *-- "1" ProjectSettings : settings
    Membership "0..*" -- "1" User : member
    Project "1" -- "0..*" Membership : memberships
    ProjectController ..> AuditLogEntry : reads project activity
```

## 3. Data Management

15 classifier; 15 quan hệ.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "secondaryColor": "#ffffff", "tertiaryColor": "#ffffff", "lineColor": "#000000", "textColor": "#000000", "background": "#ffffff"}}}%%
classDiagram
    direction TB
    class DataController {
        <<controller>>
        + upload(input : UploadInput) : DatasetVersion
        + importData(connectionId : UUID) : DatasetVersion
        + preview(versionId : UUID) : TablePreview
        + pairNode(code : String) : LocalNode
        + runLocal(job : LocalJob) : Release
    }
    class DataService {
        <<service>>
        + createDataset(input : DatasetInput) : Dataset
        + importData(connection : DataConnection) : DatasetVersion
        - requireAuthorizedSource(uri : String) : void
        - blockInternalHosts(uri : String) : void
        - rejectLocalPreview(dataset : Dataset) : void
    }
    class Dataset {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - name : String
        - location : DataLocation
    }
    class DataConnection {
        <<entity>>
        - id : UUID
        - provider : String
        - authorizationScope : String
        - credentialRef : SecretRef
    }
    class DatasetVersionService {
        <<service>>
        + create(datasetId : UUID, source : String) : DatasetVersion
        + verifyHash(version : DatasetVersion) : Boolean
        - preventOverwrite(versionId : UUID) : void
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
    class LocalNodeService {
        <<service>>
        + pair(projectId : UUID, code : String) : LocalNode
        + route(job : LocalJob) : void
        + revoke(nodeId : UUID) : void
        - rejectUnavailableNode(nodeId : UUID) : void
    }
    class LocalNode {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - status : String
        - isolationManifest : String
    }
    class ReleaseLog {
        <<entity>>
        - datasetVersionId : UUID
        - appendOnly : Boolean
    }
    class ReleaseGate {
        <<service>>
        + check(job : LocalJob, result : Aggregate) : Release
        - applyFirewall(result : Aggregate) : void
        - round(result : Aggregate) : Aggregate
        - checkDisclosure(result : Aggregate) : void
        - checkDifferencing(result : Aggregate) : void
        - checkProbeBudget(versionId : UUID) : void
    }
    class Release {
        <<entity>>
        - id : UUID
        - jobId : UUID
        - kind : String
        - reason : String
        - time : DateTime
    }
    class ConnectorFactory {
        <<interface>>
        + __call__(kind : String, config : Map, secret : Map) : Connector
    }
    class Connector {
        <<interface>>
        + test() : void
        + listTables(schema : String, search : String [0..1], limit : Integer) : TableRef [0..*]
        + listColumns(schema : String, table : String) : Column [0..*]
        + openRows(source : AnySource, maxRows : Integer [0..1]) : AsyncContext~RowStream~
    }
    class GoogleSheetsConnector {
        <<service>>
        + test() : void
        + listTables(schema : String, search : String [0..1], limit : Integer) : TableRef [0..*]
        + listColumns(schema : String, table : String) : Column [0..*]
        + openRows(source : AnySource, maxRows : Integer [0..1]) : AsyncContext~RowStream~
    }
    DataController ..> DataService : uses
    DataController ..> DatasetVersionService : versions data
    DataController ..> LocalNodeService : routes local work
    DataController ..> ReleaseGate : checks aggregates
    DataService ..> Dataset : manages
    Dataset "0..*" -- "0..1" DataConnection : imports from
    Dataset "1" *-- "0..*" DatasetVersion : versions
    DatasetVersionService ..> DatasetVersion : creates / verifies
    Dataset ..> DataLocation : uses location type
    LocalNodeService ..> LocalNode : pairs / revokes
    LocalNode ..> ReleaseLog : appends locally
    ReleaseGate ..> Release : approves release
    DataService ..> ConnectorFactory : uses factory
    ConnectorFactory ..> Connector : creates connector
    GoogleSheetsConnector ..|> Connector : implements
```

## 4. Research Run Orchestration

13 classifier; 13 quan hệ.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "secondaryColor": "#ffffff", "tertiaryColor": "#ffffff", "lineColor": "#000000", "textColor": "#000000", "background": "#ffffff"}}}%%
classDiagram
    direction TB
    class RunController {
        <<controller>>
        + start(caseId : UUID) : Run
        + amendCase(input : Amendment) : ResearchCase
        + cancel(runId : UUID) : void
        + acceptObject(objectId : UUID) : void
        + reviewSpending(itemId : UUID, approve : Boolean) : void
        + approveDossier(dossierId : UUID) : Approval
        + export(dossierId : UUID, format : String) : Export
    }
    class RunOrchestrator {
        <<service>>
        + start(caseId : UUID) : Run
        + advance(runId : UUID) : StageRun
        + cancel(runId : UUID) : void
        + markDownstreamStale(objectId : UUID) : void
        - requireNoActiveRun(projectId : UUID) : void
    }
    class Run {
        <<entity>>
        - id : UUID
        - state : RunState
        - waitingReason : String [0..1]
        - endingOutcome : String [0..1]
        - tokenBudget : Integer
        - researchCaseRef : VersionRef
        - pipeline : String = dataset_first
    }
    class ResearchCase {
        <<entity>>
        - id : UUID
        - projectId : UUID
        - version : Integer
        - objective : String
        - constraints : String
        - datasetVersionId : UUID [0..1]
    }
    class BudgetService {
        <<service>>
        + recordUsage(runId : UUID, amount : Decimal) : void
        + checkLimits(runId : UUID) : void
        + approveSpending(itemId : UUID) : void
        + expireSpending(itemId : UUID) : void
        - endWithGaps(runId : UUID) : void
    }
    class StageRun {
        <<entity>>
        - id : UUID
        - stage : String
        - preset : String
        - presenceAtStart : String
        - contractStatus : String
    }
    class BudgetLedger {
        <<entity>>
        - projectId : UUID
        - month : String
        - spending : Decimal
        - notifiedThresholds : Decimal [0..*]
    }
    class DossierService {
        <<service>>
        + createFromAccepted(packId : UUID) : Dossier
        + approve(dossierId : UUID) : Approval
        + exportApproved(dossierId : UUID, format : String) : Export
        - verifyReferenceHashes(dossierId : UUID) : void
        - requirePinnedExportApproval(dossierId : UUID) : void
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
    class RunState {
        <<enumeration>>
        running
        waiting
        ended
    }
    class HandOffObject {
        <<entity>>
        - id : UUID
        - version : Integer
        - contentHash : String
        - state : String
        - upstreamRefs : VersionRef [0..*]
    }
    class Export {
        <<entity>>
        - dossierVersion : Integer
        - format : String
        - approvedActionRef : UUID
        - auditEntryRef : UUID
    }
    RunController ..> RunOrchestrator : uses
    RunController ..> BudgetService : reviews spending
    RunController ..> DossierService : approves / exports
    RunOrchestrator ..> Run : orchestrates
    Run ..> RunState : uses state type
    RunController ..> ResearchCase : amends case version
    Run "1" *-- "0..*" StageRun : stages
    BudgetService ..> StageRun : checks stage share
    BudgetService ..> BudgetLedger : records usage
    DossierService ..> Dossier : versions / checks
    Dossier "1" *-- "0..*" Approval : approvals
    Dossier ..> HandOffObject : references accepted versions
    Export ..> HandOffObject : reads accepted references
```

## 5. Research Engines

15 classifier; 13 quan hệ.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "secondaryColor": "#ffffff", "tertiaryColor": "#ffffff", "lineColor": "#000000", "textColor": "#000000", "background": "#ffffff"}}}%%
classDiagram
    direction TB
    class DatasetEngine {
        <<service>>
        + profile(versionId : UUID) : DatasetSnapshot
        + assessFitness(snapshot : DatasetSnapshot) : Fitness
        + splitAfterConfirmation(input : SplitInput) : void
    }
    class DatasetSnapshot {
        <<entity>>
        - versionRef : VersionRef
        - qualityProfile : QualityProfile
        - dictionary : Dictionary
        - split : SplitSpec
        - fitness : Fitness
    }
    class HypothesisEngine {
        <<service>>
        + updateLiterature(projectId : UUID) : LiteratureBase
        + propose(snapshot : DatasetSnapshot) : HypothesisSet
        + selectPrimary(input : Selection) : void
    }
    class HypothesisSet {
        <<entity>>
        - snapshotRef : VersionRef
        - literatureVersionRef : VersionRef
        - hypotheses : Hypothesis [2..*]
        - primaryClaimKey : String
    }
    class ExperimentDesignEngine {
        <<service>>
        + build(set : HypothesisSet) : AnalysisPlan
        + rehearseOnTwin(plan : AnalysisPlan) : CheckResult
        + requestUserLock(planId : UUID) : void
    }
    class AnalysisPlan {
        <<entity>>
        - hypothesisSetRef : VersionRef
        - patternRefs : VersionRef [0..*]
        - taskFamily : String
        - pipelineOrder : String [1..*]
        - interpretationTable : Table
    }
    class ExecutionEngine {
        <<service>>
        + execute(lock : Lock) : EvidenceBundle
        + dryRun(lock : Lock) : Diagnostics
        + requestUnseal(lockId : UUID) : void
        + computeVerdicts(input : EvidenceInput) : Verdict [1..*]
    }
    class EvidenceBundle {
        <<entity>>
        - analysisPlanRef : VersionRef
        - verdicts : Verdict [1..*]
        - grade : String
        - claimCeiling : String
        - replicationHash : String
    }
    class PaperEngine {
        <<service>>
        + draft(input : PaperInput) : PaperPack
        + renderNumbers(bundle : EvidenceBundle) : void
        + validateClaimsAndCitations(pack : PaperPack) : CheckResult
    }
    class PaperPack {
        <<entity>>
        - evidenceBundleRef : VersionRef
        - manuscript : String
        - reportingChecklist : Checklist
        - limitations : String [0..*]
        - authorDeclarations : Declaration [0..*]
    }
    class IndependentReviewService {
        <<service>>
        + review(object : HandOffObject) : Finding [0..*]
        + verify(finding : Finding) : String
        + reviseConfirmedBlockers(objectId : UUID) : void
        - enforceTwoRounds(round : Integer) : void
    }
    class Finding {
        <<entity>>
        - anchor : ObjectFieldRef
        - evidence : EvidenceRef
        - severity : String
        - verificationResult : String
        - proposedFix : String
    }
    class Harness {
        <<service>>
        + checkContract(object : HandOffObject) : CheckResult
        + enforcePipelineOrder(plan : AnalysisPlan) : void
        + checkItemBudget(itemId : UUID) : void
        + renderNumbers(records : Record [0..*]) : String
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
    class Envelope {
        <<entity>>
        - lockId : UUID
        - state : String
        - sealedResults : Result [0..*]
        - unsealedAt : DateTime [0..1]
    }
    DatasetEngine ..> DatasetSnapshot : publishes
    HypothesisEngine ..> HypothesisSet : publishes
    ExperimentDesignEngine ..> AnalysisPlan : publishes
    ExecutionEngine ..> EvidenceBundle : publishes
    PaperEngine ..> PaperPack : publishes
    IndependentReviewService ..> Finding : verifies
    HypothesisEngine ..> DatasetSnapshot : reads pinned snapshot
    ExecutionEngine ..> AnalysisPlan : reads locked plan
    IndependentReviewService ..> PaperPack : reviews object version
    PaperEngine ..> Harness : runs checks
    ExecutionEngine ..> IndependentReviewService : reviews evidence
    Harness ..> Lock : checks locked plan
    Lock "1" *-- "1" Envelope : sealed results
```

## 6. AI Principal Investigator

12 classifier; 12 quan hệ.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "secondaryColor": "#ffffff", "tertiaryColor": "#ffffff", "lineColor": "#000000", "textColor": "#000000", "background": "#ffffff"}}}%%
classDiagram
    direction TB
    class DecisionController {
        <<controller>>
        + answer(itemId : UUID, option : String) : void
        + confirmTentative(itemId : UUID) : void
        + overturn(itemId : UUID, reason : String) : void
        + changePolicy(input : PolicyInput) : void
        + setPresence(value : Presence) : void
    }
    class DecisionService {
        <<service>>
        + createRequest(input : DecisionInput) : DecisionInboxItem
        + answer(itemId : UUID, option : String) : void
        + overturn(itemId : UUID, reason : String) : void
        + expirePinnedItem(itemId : UUID) : void
        - closeUnansweredAndEndWithGaps(itemId : UUID) : void
    }
    class DecisionInboxItem {
        <<entity>>
        - id : UUID
        - kind : String
        - options : String [1..*]
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
    class ActionPolicyService {
        <<service>>
        + effectiveLevel(actionType : String) : ActionLevel
        + updatePreset(stage : String, preset : String) : void
        + setOverride(actionType : String, level : ActionLevel) : void
        - enforceFloorAndCeiling(actionType : String) : void
        - reevaluateWaitingItems() : void
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
        do_then_review
        must_ask
    }
    class AIPrincipalInvestigator {
        <<service>>
        + propose(item : DecisionInboxItem) : String
        + decideTentatively(item : DecisionInboxItem) : void
        + proposeNextStep(runId : UUID) : String
        - rejectPinnedDecision(item : DecisionInboxItem) : void
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
    class OverturnMetricService {
        <<service>>
        + compute(actionType : String) : Decimal
        + proposeHigherLevel(actionType : String) : ActionLevel
    }
    class Run {
        <<entity>>
        - id : UUID
        - state : RunState
        - endingOutcome : String [0..1]
    }
    DecisionController ..> DecisionService : answers / overturns
    DecisionController ..> ActionPolicyService : sets policy
    DecisionController ..> AIPrincipalInvestigator : requests proposals
    DecisionController ..> OverturnMetricService : reads measured outcomes
    DecisionService ..> DecisionInboxItem : creates / resolves
    DecisionInboxItem "1" -- "0..1" DecisionLogEntry : decided record
    ActionPolicyService ..> ActionPolicy : versions
    ActionPolicy ..> ActionLevel : uses level type
    AIPrincipalInvestigator ..> LabNotebookEntry : writes proposals
    LabNotebookEntry ..> Presence : records context type
    OverturnMetricService ..> Run : measures decisions by run
    DecisionInboxItem ..> ActionPolicy : evaluated under
```

## 7. Notifications & Integrations

12 classifier; 11 quan hệ.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "secondaryColor": "#ffffff", "tertiaryColor": "#ffffff", "lineColor": "#000000", "textColor": "#000000", "background": "#ffffff"}}}%%
classDiagram
    direction TB
    class CollaborationController {
        <<controller>>
        + listNotifications() : Notification [0..*]
        + markRead(notificationId : UUID) : void
        + setPreferences(input : PreferencesInput) : void
        + configureIntegration(input : IntegrationInput) : void
        + comment(input : CommentInput) : Comment
    }
    class NotificationService {
        <<service>>
        + create(event : ProjectEvent) : Notification
        + listForUser(userId : UUID) : Notification [0..*]
        + markRead(notificationId : UUID) : void
        - allowExternalNotice(item : DecisionInboxItem) : Boolean
        - selectAuthorizedRecipients(item : DecisionInboxItem) : UUID [0..*]
    }
    class Notification {
        <<entity>>
        - id : UUID
        - recipientId : UUID
        - kind : String
        - status : String
        - decisionItemId : UUID [0..1]
    }
    class DecisionInboxItem {
        <<entity>>
        - id : UUID
        - kind : String
        - pinned : Boolean
        - blocking : Boolean
        - waitDeadline : DateTime [0..1]
    }
    class IntegrationService {
        <<service>>
        + configure(input : IntegrationInput) : ProjectIntegration
        + deliver(notificationId : UUID, channel : String) : void
        - resolveSealedCredential(ref : SecretRef) : void
    }
    class ProjectIntegration {
        <<entity>>
        - projectId : UUID
        - provider : String
        - credentialRef : SecretRef
        - enabled : Boolean
    }
    class NotificationChannel {
        <<external>>
        + deliver(recipient : String, message : String) : void
    }
    class CommentService {
        <<service>>
        + add(input : CommentInput) : Comment
        + list(objectRef : ObjectRef) : Comment [0..*]
        - requireProjectRole(actorId : UUID) : void
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
    class NotificationPreferenceService {
        <<service>>
        + update(input : PreferencesInput) : NotificationPreference
        + resolveForProject(projectId : UUID) : NotificationPreference
    }
    class NotificationPreference {
        <<entity>>
        - projectId : UUID
        - userId : UUID
        - eventChoices : Map
        - channels : String [0..*]
    }
    CollaborationController ..> NotificationService : receives / reads
    CollaborationController ..> IntegrationService : configures channels
    CollaborationController ..> CommentService : comments on objects
    CollaborationController ..> NotificationPreferenceService : sets preferences
    NotificationService ..> Notification : creates / marks read
    Notification "0..*" -- "0..1" DecisionInboxItem : decision context
    IntegrationService ..> ProjectIntegration : configures
    IntegrationService ..> NotificationChannel : delivers through
    CommentService ..> Comment : anchors comments
    Comment "0..*" -- "1" Membership : author
    NotificationPreferenceService ..> NotificationPreference : updates
```

## 8. Administration & Monitoring

11 classifier; 10 quan hệ.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ffffff", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "secondaryColor": "#ffffff", "tertiaryColor": "#ffffff", "lineColor": "#000000", "textColor": "#000000", "background": "#ffffff"}}}%%
classDiagram
    direction TB
    class AdministrationController {
        <<controller>>
        + manageUsers(input : UserAdminInput) : void
        + configureModel(input : ModelInput) : void
        + configureEngine(input : EngineInput) : void
        + viewAudit(filter : AuditFilter) : AuditLogEntry [0..*]
        + viewHealth() : HealthSnapshot
        + viewMetrics(runId : UUID) : OperatingMetrics
    }
    class AdministrationService {
        <<service>>
        + updateUser(input : UserAdminInput) : User
        + configureModel(input : ModelInput) : ModelProfile
        + configureEngine(input : EngineInput) : EngineSettings
        + setDefaultBudget(amount : Decimal) : void
        - requirePlatformAdmin(userId : UUID) : void
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
    class SecretService {
        <<service>>
        + seal(value : String) : SecretRef
        + rotate(ref : SecretRef, value : String) : void
        + resolveForExecution(ref : SecretRef) : Secret
        - preventSecretDisclosure() : void
    }
    class SealedSecret {
        <<entity>>
        - id : UUID
        - encryptedValue : Bytes
        - keyVersion : String
        - updatedAt : DateTime
    }
    class User {
        <<entity>>
        - id : UUID
        - email : String
        - status : String
        - isPlatformAdmin : Boolean
    }
    class MonitoringService {
        <<service>>
        + readAudit(filter : AuditFilter) : AuditLogEntry [0..*]
        + health() : HealthSnapshot
        + metrics(runId : UUID) : OperatingMetrics
        + requireModelsAndCredentials(runId : UUID) : void
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
    class OperatingMetrics {
        <<entity>>
        - runId : UUID
        - questionCount : Integer
        - blockedTime : Duration
        - overturnRates : Map
        - personaPrecision : Map
    }
    AdministrationController ..> AdministrationService : configures platform
    AdministrationController ..> SecretService : manages sealed secrets
    AdministrationController ..> MonitoringService : reads operation
    AdministrationService ..> ModelProfile : configures model roles
    AdministrationService ..> EngineSettings : configures engines
    AdministrationController ..> User : manages user accounts
    SecretService ..> SealedSecret : seals / rotates
    MonitoringService ..> AuditLogEntry : reads append-only log
    MonitoringService ..> HealthSnapshot : reads component health
    MonitoringService ..> OperatingMetrics : computes run metrics
```

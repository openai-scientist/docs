# Supplement to Report III

Facts from the web app (`ai-research-platform-fe`: routes, route guards, `lib/auth/project-access.ts`) and the Platform (`logos`: background loops, worker, database script) on 2026-10-29, and the requirements of `report/03`. The build places each section under the template heading with the same number.

### 2.2 Use Case

The use case diagram (section 2.2.1) shows the actors of section 2.1 and the use cases UC-01 to UC-41. Section 2.2.2 describes each use case: actor, trigger, preconditions, main flow, alternative flows and postconditions.

### 3. Functional Requirements

This chapter gives the system functional overview (section 3.1) and then the functions grouped by feature (sections 3.2 to 3.9). Each group first lists its requirements (FR and SR) and then describes each function: actor, screen, behavior and related requirements.

### 3.1.2 Screen Descriptions

| ID | Screen | Route | Description |
| ----- | ----- | ----- | ----- |
| SC-01 | Sign in | `/auth/login` | Sign in with an email code or a Google account. |
| SC-02 | Verify code | `/auth/verify` | Enter the one-time code sent by email. |
| SC-03 | Onboarding | `/onboarding` | Complete the profile (display name, avatar) at first sign-in. |
| SC-04 | Project list | `/projects` | Projects of the user, create a project, pending invitations. |
| SC-05 | Project overview | `/projects/{id}` | Status, members, datasets, runs and activity of one project. |
| SC-06 | Datasets | `/projects/{id}/datasets` | Datasets of the project; upload and import. |
| SC-07 | Dataset detail | `/projects/{id}/datasets/{datasetId}` | Versions, profile and preview of one dataset. |
| SC-08 | Data connections | `/projects/{id}/connections` | Data connections and Google Sheets and Drive import. |
| SC-09 | Documents | `/projects/{id}/files` | Documents uploaded to the project. |
| SC-10 | Research flow (Run Studio) | `/projects/{id}/experiments` | Start and follow runs: stages, gates, artifacts, reviews, comments, PI notebook. |
| SC-11 | Members | `/projects/{id}/members` | Members and invitations; a Project Manager is sent to the Access tab of Settings. |
| SC-12 | Settings | `/projects/{id}/settings` | Project settings, budget, access, integrations, notifications, ownership, delete. |
| SC-13 | Reviewer queue | `/reviews` | Items that wait for a review by the user. |
| SC-14 | Admin overview | `/admin` | Usage, health and activity of the Platform. |
| SC-15 | Users | `/admin/users` | User list; suspend, reactivate, invite. |
| SC-16 | User detail | `/admin/users/{userId}` | Profile, projects and platform role of one user. |
| SC-17 | All projects | `/admin/projects`, `/admin/projects/{projectId}` | Metadata of every project (list, members, usage, run state). |
| SC-18 | Models | `/admin/providers` | Model profiles per model role; test a model. |
| SC-19 | Decision providers | `/admin/decision-providers` | The provider that answers decisions for the AI PI. |
| SC-20 | Platform settings | `/admin/settings` | Platform settings and stage engine settings. |
| SC-21 | Usage | `/admin/usage` | Token usage and cost by project and month. |
| SC-22 | Audit log | `/admin/logs` | Administrative and security actions. |
| SC-23 | Log monitoring | `/admin/log-monitoring` | Captured service logs and alerts. |
| SC-24 | System health | `/admin/system` | Health of services and workers; acknowledge alerts. |
| SC-25 | Unauthorized | `/unauthorized` | Shown when the user lacks the role for a page. |
| SC-26 | Public pages | `/about`, `/contact`, `/privacy`, `/terms` | Information pages that need no sign-in. |

A notification panel in the header of every signed-in page lists the notifications of the user.

### 3.1.3 Screen Authorization

Project roles come from the membership of the user in the project; Platform Admin is a platform role. An archived project is read-only for every role (FR-06). A Platform Admin who is not a member sees project metadata only, never datasets, objects or manuscripts (FR-152).

| Screen | Guest | Reviewer | Researcher | Project Manager | Platform Admin |
| ----- | ----- | ----- | ----- | ----- | ----- |
| SC-01 to SC-03 Sign in, Verify, Onboarding | X | X | X | X | X |
| SC-04 Project list |  | X | X | X | X |
| SC-05 Project overview |  | Read | X | X | Member only |
| SC-06, SC-07 Datasets |  | Read | X | X | Member only |
| SC-08 Data connections |  | Read | X | X | Member only |
| SC-09 Documents |  | Read | X | X | Member only |
| SC-10 Research flow |  | Read, comment, review | X | X | Member only |
| SC-11 Members |  | Read | Read | X | Member only |
| SC-12 Settings |  |  |  | X |  |
| SC-13 Reviewer queue |  | X | X | X |  |
| SC-14 to SC-24 Administration |  |  |  |  | X |
| SC-25, SC-26 Unauthorized, Public pages | X | X | X | X | X |

X: full access to the screen. Read: view only. Member only: the Platform Admin has the access of their project role when they are a member.

### 3.1.4 Non-Screen Functions

| ID | Function | Trigger | Description |
| ----- | ----- | ----- | ----- |
| NS-01 | Run orchestration | API call, engine event | Moves a run through the five stages, calls the stage engines and records stage runs, gates and artifacts. |
| NS-02 | Self-healing sweep | Every 60 seconds (Platform lifespan loop) | Restarts a stage that failed for a transient reason after a growing wait, sends queued AI PI consultations and ends work that passed its deadline. |
| NS-03 | AI PI consultation | Stage outcome, failure or close of a run | The oversight service answers a consultation in the background and posts the result to the Platform. |
| NS-04 | Notification email dispatch | Lifespan loop after commit | Sends queued notification emails in small batches; checks the recipient again at send time; never sends the same email twice. |
| NS-05 | Integration delivery worker | Separate process (`management.integrations.worker`) | Sends queued messages to Slack, Microsoft Teams and Discord with a lease and retries. |
| NS-06 | Dataset ingest | Upload or import | Reads the file, builds the table, computes the content hash and stores an immutable dataset version. |
| NS-07 | Cost ledger | Engine usage report | Writes the increase of token usage and cost per project, run and model role. |
| NS-08 | Budget admission and alerts | Start of work, cost entry | Checks the monthly budget of the project before work starts and raises spending alerts. |
| NS-09 | Audit logging | Administrative or security action | Appends a record to the audit log. |
| NS-10 | Log monitoring | Service log events | Captures service logs, records capture gaps and worker heartbeats, and raises alerts. |
| NS-11 | Database migration | Deployment | Applies Alembic migrations before the API starts. |

### 3.1.5 Entity Relationship Diagram

The ERD is drawn at the conceptual level from the business tables of the database script (Report IV, section 2.4). Technical tables (sessions, sign-in codes, monitoring, system settings, secrets, migration marker) are left out.

| Entity | Table | Description |
| ----- | ----- | ----- |
| User | `users` | A person with an account on the Platform. |
| PlatformRole | `user_platform_roles` | The platform-level role of a user (Platform Admin). |
| AuditEvent | `audit_events` | An append-only record of an administrative or security action. |
| Project | `projects` | The shared workspace of a team. |
| ProjectMembership | `project_memberships` | The membership of a user in a project, with a role and an invitation state. |
| ProjectSetting | `project_settings` | The configuration of one project. |
| ProjectFile | `project_files` | A document uploaded to a project. |
| ProjectIntegration | `project_integrations` | A chat tool that receives project notifications. |
| IntegrationDelivery | `integration_deliveries` | One message queued for, or sent to, a project integration. |
| SpendingAlert | `spending_alerts` | A budget alert of a project in a month. |
| Notification | `notifications` | An in-app notification for a user. |
| NotificationEmail | `notification_emails` | A notification email queued for a member. |
| NotificationPreference | `notification_preferences` | Which notification groups a user receives in a project. |
| DataConnection | `data_connections` | An authorized external data source of a project. |
| GoogleConnectionGrant | `google_connection_grants` | A Google authorization of a user for a project. |
| Dataset | `datasets` | A tabular dataset of a project. |
| DatasetVersion | `dataset_versions` | An immutable version of a dataset. |
| ResearchContext | `research_contexts` | The research case of a project. |
| ResearchRun | `research_runs` | One execution of the research pipeline. |
| CostEntry | `cost_entries` | An increase of model token usage and cost. |
| StageRun | `stage_runs` | One execution of one stage in a run. |
| StageDecision | `stage_decisions` | A decision on the outcome of a stage run. |
| RunGate | `run_gates` | A question of a run that waits for a person. |
| RunEvent | `run_events` | A trace event of a run. |
| RunArtifact | `run_artifacts` | A file that a stage run produces. |
| FrameReview | `frame_reviews` | A review of the research frame of a run. |
| Comment | `comments` | A remark on a run or an artifact. |
| PIConsultation | `pi_consultations` | A consultation of the AI PI. |
| PINote | `pi_notes` | An entry of the AI PI lab notebook. |
| ModelProfile | `model_profiles` | The model configuration of a model role. |

### 3.2.1 Sign In With Email Code

- Actor: any user. Screens: SC-01, SC-02.
- The user enters an email address; the system sends a one-time code and signs the user in when the code is correct and not expired. An account is created at the first sign-in.
- Requirements: FE-01 (FR-01, FR-02).

### 3.2.2 Sign In With Google

- Actor: any user. Screen: SC-01.
- The user signs in with a Google account. When the verified email matches an existing account, the system signs in the same user.
- Requirements: FE-01 (FR-146).

### 3.2.3 Complete Onboarding and Update Profile

- Actor: signed-in user. Screen: SC-03.
- At the first sign-in the user sets a display name and an avatar; later the user can change them.
- Requirements: FE-01.

### 3.2.4 Sign Out

- Actor: signed-in user. Screen: any signed-in page.
- The system ends the session and returns to the sign-in page.
- Requirements: FE-01.

### 3.2.5 View Unauthorized and Session Expired Pages

- Actor: any user. Screens: SC-25, SC-01.
- A user without the role for a page sees the Unauthorized page; a user whose session expired is sent back to sign in. A project is not revealed to a person who is not a member.
- Requirements: FE-01 (FR-02, FR-151).

### 3.3.1 Create Project

- Actor: signed-in user. Screen: SC-04.
- The user creates a project with a name and description and becomes its Project Manager.
- Requirements: FE-02 (FR-04).

### 3.3.2 View Project List and Overview

- Actor: project member. Screens: SC-04, SC-05.
- The user sees the projects in which they are a member and the overview of one project.
- Requirements: FE-02.

### 3.3.3 Update, Archive, Complete Project

- Actor: Project Manager. Screen: SC-12.
- The Project Manager edits the project, marks it completed or archives it. An archived project is read-only.
- Requirements: FE-02 (FR-06, FR-07).

### 3.3.4 Manage Members and Invitations

- Actor: Project Manager. Screen: SC-12 (Access tab).
- The Project Manager invites users by email with a role (Researcher or Reviewer), changes roles and removes members. The last Project Manager cannot be removed.
- Requirements: FE-02 (FR-04, FR-05).

### 3.3.5 Manage Documents

- Actor: Researcher, Project Manager. Screen: SC-09.
- The user uploads, downloads and deletes documents of the project.
- Requirements: FE-02.

### 3.3.6 Manage Project Integrations and Notification Preferences

- Actor: Project Manager. Screen: SC-12.
- The Project Manager connects Slack, Microsoft Teams or Discord to receive project notifications, tests and removes them, and sets the notification groups of the project.
- Requirements: FE-02 (FR-08), FE-15.

### 3.3.7 Accept or Decline Invitation

- Actor: invited user. Screen: SC-04.
- The invited user accepts or declines an invitation. An expired invitation is rejected.
- Requirements: FE-02 (FR-05, FR-153, SR-05).

### 3.3.8 Resend or Cancel Invitation

- Actor: Project Manager. Screen: SC-12 (Access tab).
- The Project Manager sends a pending invitation again or cancels it.
- Requirements: FE-02 (FR-05).

### 3.3.9 Transfer Ownership

- Actor: project owner. Screen: SC-12.
- The owner transfers ownership of the project to another active member.
- Requirements: FE-02 (FR-04, FR-07).

### 3.3.10 Delete Project

- Actor: project owner. Screen: SC-12.
- The owner deletes the project after confirmation; the action is recorded in the audit log.
- Requirements: FE-02 (FR-07).

### 3.3.11 View Project Activity and Audit Log

- Actor: project member. Screen: SC-05.
- The user sees the recent activity of the project, taken from the audit log.
- Requirements: FE-02 (FR-07).

### 3.3.12 Configure Project Settings and Monthly Budget

- Actor: Project Manager. Screen: SC-12.
- The Project Manager sets the monthly budget, warning thresholds, presets per stage, wait deadline and access settings.
- Requirements: FE-02 (FR-08), FE-05 (SR-08), FE-13.

### 3.4.1 Upload Dataset

- Actor: Researcher, Project Manager. Screen: SC-06.
- The user uploads a tabular file; the system creates a dataset and its first immutable version with a hash.
- Requirements: FE-03 (FR-09, FR-112, SR-01, SR-02, SR-07).

### 3.4.2 View Dataset Detail

- Actor: project member. Screen: SC-07.
- The user sees the versions, profile and columns of a dataset.
- Requirements: FE-03 (FR-12).

### 3.4.3 Manage Data Connection and Import

- Actor: Researcher, Project Manager. Screen: SC-08.
- The user creates a data connection to an external source and imports a table as a new dataset version. The credential is never shown again or logged.
- Requirements: FE-03 (FR-10, FR-11, FR-155, FR-156).

### 3.4.4 Rename or Delete Dataset

- Actor: Researcher, Project Manager. Screens: SC-06, SC-07.
- The user renames a dataset or deletes it after confirmation.
- Requirements: FE-03.

### 3.4.5 Upload New Dataset Version

- Actor: Researcher, Project Manager. Screen: SC-07.
- The user uploads a new file to a dataset; the system adds a new version and keeps the older ones unchanged.
- Requirements: FE-03 (FR-09).

### 3.4.6 Download or Preview Dataset Version

- Actor: project member. Screen: SC-07.
- The user previews rows of a version or downloads it. Rows of `local` data are never previewed or downloaded.
- Requirements: FE-03 (FR-158).

### 3.4.7 Browse and Preview Connection Source

- Actor: Researcher, Project Manager. Screen: SC-08.
- The user browses the tables or files of a connection and previews one before import.
- Requirements: FE-03 (FR-10).

### 3.4.8 Rename, Test or Delete Data Connection

- Actor: Researcher, Project Manager. Screen: SC-08.
- The user renames a connection, tests that it still works, or deletes it.
- Requirements: FE-03 (FR-11).

### 3.4.9 Connect Google Sheets and Drive

- Actor: Researcher, Project Manager. Screen: SC-08.
- The user authorizes Google access for the project and picks a sheet or file to import.
- Requirements: FE-03 (FR-10).

### 3.5.1 Start Research Run

- Actor: Researcher, Project Manager. Screen: SC-10.
- The user writes or picks a research case, optionally pins a dataset version and starts a run. A project has at most one active run, and the monthly budget is checked first.
- Requirements: FE-04 (FR-13, FR-14, FR-16), FE-13.

### 3.5.2 Monitor Run in Run Studio

- Actor: project member. Screen: SC-10.
- The user follows the run state, stages, trace events and artifacts as they stream in.
- Requirements: FE-04 (FR-21), NFR-02.

### 3.5.3 Answer Gate

- Actor: Researcher, Project Manager. Screen: SC-10.
- The user answers a question that the run waits for; the run continues from the answer.
- Requirements: FE-05 (FR-28, FR-29, FR-30).

### 3.5.4 Accept, Send Back or Rerun Stage

- Actor: Researcher, Project Manager. Screen: SC-10.
- The user accepts the output of a stage, sends it back with a reason or runs it again. The decision is recorded.
- Requirements: FE-04 (FR-18, FR-161), FE-05 (FR-30).

### 3.5.5 Pause, Resume, Stop, Abandon and Sync Run

- Actor: Project Manager, Researcher who created the run. Screen: SC-10.
- The user pauses, resumes or stops a run, abandons it, or syncs its state with the engines. Accepted objects are kept.
- Requirements: FE-04 (FR-22, FR-166, FR-167, FR-168).

### 3.5.6 Raise Token Budget

- Actor: Project Manager. Screen: SC-10.
- The Project Manager raises the token budget of a run that waits for budget review.
- Requirements: FE-13.

### 3.5.7 View Review Rounds, Diffs and Artifacts

- Actor: project member. Screen: SC-10.
- The user sees the review rounds of a stage, the differences between versions and the produced artifacts.
- Requirements: FE-11.

### 3.5.8 Comment On Run

- Actor: project member. Screen: SC-10.
- The user writes a comment on a run or on one of its artifacts.
- Requirements: FE-15.

### 3.5.9 View Run List

- Actor: project member. Screen: SC-10.
- The user sees the runs of the project with their state.
- Requirements: FE-04, NFR-01.

### 3.5.10 View Recovery State

- Actor: project member. Screen: SC-10.
- The user sees whether a failed stage is being retried by the system or needs a person, with the reason in plain words.
- Requirements: FE-04 (FR-163, FR-164), NFR-03.

### 3.5.11 Download and Compare Artifacts

- Actor: project member. Screen: SC-10.
- The user downloads an artifact or compares two versions of it.
- Requirements: FE-04 (FR-161).

### 3.5.12 View Iteration Summary

- Actor: project member. Screen: SC-10.
- The user sees a summary of the iterations of a stage: what changed and why.
- Requirements: FE-04, FE-11.

### 3.5.13 Edit or Delete Comment

- Actor: author of the comment. Screen: SC-10.
- The author edits or deletes their own comment.
- Requirements: FE-15.

### 3.6.1 Dataset Stage

- Actor: system (stage engine), Researcher. Screen: SC-10.
- The engine profiles the data, checks fitness and prepares the dataset snapshot for the next stages.
- Requirements: FE-06.

### 3.6.2 Hypothesis Stage

- Actor: system (stage engine), Researcher. Screen: SC-10.
- The engine searches the literature and proposes at least two hypotheses; the user chooses the primary one.
- Requirements: FE-07.

### 3.6.3 Experiment Design Stage

- Actor: system (stage engine), Researcher. Screen: SC-10.
- The engine writes the analysis plan with estimand, protocol and analysis program for the user to lock.
- Requirements: FE-08.

### 3.6.4 Independent Review and Revision Rounds

- Actor: system (reviewer), Researcher. Screen: SC-10.
- An independent reviewer checks each stage output and the engine revises it, at most two rounds per accepted version.
- Requirements: FE-11, NFR-30.

### 3.7.1 Charter and Directives

- Actor: Researcher, Project Manager. Screen: SC-10.
- The user gives the AI PI its charter and directives for the run: goals, limits and what to ask the user.
- Requirements: FE-05 (FR-31, FR-32).

### 3.7.2 Stage Outcome, Failure and Close Consultations

- Actor: system (AI PI). Screen: SC-10.
- The Platform consults the AI PI when a stage ends, fails or the run closes; the AI PI answers in the background.
- Requirements: FE-05 (FR-31, FR-35).

### 3.7.3 Endorse or Retry Consultation

- Actor: Researcher, Project Manager. Screen: SC-10.
- The user endorses the advice of the AI PI or asks for a new consultation; an override is recorded.
- Requirements: FE-05 (FR-30, FR-177).

### 3.7.4 View Lab Notebook

- Actor: project member. Screen: SC-10.
- The user reads the lab notebook that the AI PI writes for the run: summary, proposals, tentative decisions and reasons.
- Requirements: FE-05 (FR-35).

### 3.7.5 View PI Overview and Close Report

- Actor: project member. Screen: SC-10.
- The user sees the overview of the AI PI and the close report of a finished run with the proposed next step.
- Requirements: FE-04 (FR-23).

### 3.8.1 Receive Notifications

- Actor: project member. Screen: notification panel.
- The user receives in-app notifications, and email or chat messages when the project enables them.
- Requirements: FE-15, FE-05 (FR-174).

### 3.8.2 View Reviewer Queue

- Actor: Reviewer, Researcher, Project Manager. Screen: SC-13.
- The user sees the items across projects that wait for their review.
- Requirements: FE-15.

### 3.8.3 Set Notification Preferences

- Actor: project member. Screen: SC-12 or the notification panel.
- The user chooses which notification groups they receive in a project.
- Requirements: FE-15.

### 3.8.4 Mark Notifications as Read

- Actor: project member. Screen: notification panel.
- The user marks one or all notifications as read.
- Requirements: FE-15.

### 3.9.1 Manage Users

- Actor: Platform Admin. Screen: SC-15.
- The Platform Admin lists users, invites a user, and suspends or reactivates an account.
- Requirements: FE-17.

### 3.9.2 Configure Models and Decision Provider

- Actor: Platform Admin. Screens: SC-18, SC-19.
- The Platform Admin sets the model and key reference of each model role, tests a model, and sets the decision provider.
- Requirements: FE-17, NFR-09.

### 3.9.3 Edit Platform and Engine Settings

- Actor: Platform Admin. Screen: SC-20.
- The Platform Admin edits platform settings (for example the upload size limit) and the settings of each stage engine.
- Requirements: FE-17 (SR-02).

### 3.9.4 View Usage, Audit Log and Log Monitoring

- Actor: Platform Admin. Screens: SC-21, SC-22, SC-23.
- The Platform Admin sees token usage and cost, the audit log, and captured service logs.
- Requirements: FE-17, NFR-11, NFR-23.

### 3.9.5 View Admin Overview

- Actor: Platform Admin. Screen: SC-14.
- The Platform Admin sees the usage, health and activity of the Platform on one page.
- Requirements: FE-17.

### 3.9.6 View and Edit User Detail

- Actor: Platform Admin. Screen: SC-16.
- The Platform Admin sees the profile and projects of a user and edits the profile.
- Requirements: FE-17.

### 3.9.7 View All Projects

- Actor: Platform Admin. Screen: SC-17.
- The Platform Admin sees the metadata of every project, but not its research content.
- Requirements: FE-01 (FR-03, FR-152).

### 3.9.8 Grant or Revoke Platform Admin

- Actor: Platform Admin. Screen: SC-16.
- The Platform Admin grants or revokes the Platform Admin role of a user; the action is recorded in the audit log.
- Requirements: FE-17, NFR-11.

### 3.9.9 View System Health and Acknowledge Alerts

- Actor: Platform Admin. Screen: SC-24.
- The Platform Admin sees the health of services and workers and acknowledges monitoring alerts.
- Requirements: FE-17, NFR-06.

### 4.2.1 Usability

NFR-15 (a new user creates a valid first run), NFR-16 (the source of information is visible), NFR-17 (verdict labels are understood), NFR-18 (WCAG 2.1 AA and keyboard use) and NFR-19 (English interface). Criteria and methods are in the table of section 4.2.

### 4.2.2 Security

NFR-08 (role and project check on every request, isolation between projects), NFR-09 (no key or secret outside the Platform), NFR-10 (no confirmatory estimate before unseal), NFR-11 (append-only audit log), and the privacy requirements NFR-12, NFR-13 and NFR-14 for `local` data and the release gate.

### 4.2.3 Performance

NFR-01 (run list and decision inbox, p95 under 2 seconds for up to 100 runs) and NFR-02 (trace events displayed, p95 under 5 seconds).

### 4.2.4 Reliability

NFR-03 (every run that is not waiting ends), NFR-04 (clear error and no fake output when a provider fails), NFR-05 (spending within ceilings), NFR-06 (at least 99% monthly availability) and NFR-07 (accepted objects keep their hash after a restart).

### 4.2.5 Maintainability

NFR-20 (one harness for all engines), NFR-21 (every hard rule in both prompt and code validator), NFR-22 (traceability of BR, FR, UC and TC), and the observability requirements NFR-23 and NFR-24.

### 4.2.6 Scientific Validity

NFR-25 and NFR-26 (replayable results with the same hash), NFR-27 (no unreferenced number in a PaperPack), NFR-28 (effect statements trace to a verdict within the claim ceiling), NFR-29 (every citation in the Literature Base with a DOI), NFR-30 (at most two revision rounds) and NFR-31 (the AI PI decides no pinned item).

# VI. Release Package & User Guides

This section describes what the team delivers and how to install and use OpenAI-Scientist. It follows the Diátaxis split: a tutorial teaches by doing, how-to guides solve one task, a reference lists facts, and an explanation gives the reasons. Use cases (UC-xx), system rules (SR-xx) and messages (MSG-xx) are defined in Report III. Design decisions are in Report IV. Test cases are in Report V.

The section describes the system as specified. It does not state an implementation status. It contains no screenshots; each place that needs one holds a placeholder line.

## 1. Deliverable Package

| # | Item | Description | Related |
|---|---|---|---|
| 1 | Web application | The English-only web app for Project Managers, Researchers, Reviewers and Platform Admins. | NFR-19 |
| 2 | Platform and stage engines | The Platform, the five stage engines (dataset, hypothesis, experiment_design, execution, paper) and the AI PI, packaged for an operator to deploy. | NFR-20 |
| 3 | Local Node | The desktop application and background service that keep `local` data on the user's machine. It needs no container runtime. | UC-08, UC-30, UC-31 |
| 4 | Documentation set | The business and product requirements, the glossary, the design description and the capstone reports. | NFR-22 |
| 5 | Replication package of a run | Part of every accepted EvidenceBundle. It lets the replicator reproduce the bundle hash. | UC-23, NFR-25 |
| 6 | Dossier export | The approved Dossier, exported out of the project in the formats set in the review settings. | UC-35, UC-36 |
| 7 | Test materials | The test cases and the benchmark case catalogue, described in Report V. | UC-29 |

Open items 1 to 3 list what the package still needs: version identifier, release notes, sample data and the support contact.

## 2. Installation Guides

### 2.1 System Requirements

#### User side

| Item | Requirement |
|---|---|
| Web app | A current desktop browser. The web app meets the Web Content Accessibility Guidelines (WCAG) 2.1 level AA (NFR-18). The interface language is English (NFR-19). |
| Account | An email address that the system knows or that has an invitation (UC-01). No password is used (FR-01). |
| Local Node (optional) | A desktop operating system of a supported category. The machine stays on while a job needs `local` data (section 1.4 of Report III). No container runtime is needed. |
| Data | Tabular data in a supported format (SR-01), within the upload limit (SR-02). |

The Local Node is needed only when rows must stay on the user's machine. Open item 4 lists the operating system names and the minimum hardware.

#### Operator side

| Category | Requirement |
|---|---|
| Platform host | A host for the Platform, its database and its object storage. The Platform keeps users, projects, runs, keys, the envelope and the Dossier. |
| Engine workers | Capacity to run the five stage engines and the AI PI on one shared harness, the runtime that all engines have in common (NFR-20). |
| Model provider | At least one model provider with keys for the model roles `stage`, `review` and `vision`. Without a model or key, runs end as `failed_technical` (MSG-30). |
| Outbound access | Access to the model provider, a scholarly metadata service, public data services and an identity provider (section 4.1 of Report III). |
| Email delivery | A service that sends sign-in and notification email. |
| Secrets | A place to seal keys and integration secrets at the Platform (UC-39, NFR-09). |
| Availability | At least 99% of the minutes of each calendar month with a passing health check (NFR-06). The measure covers the whole calendar month. |

Open item 5 lists the sizing figures that the sources do not give.

### 2.2 Installation

#### How to pair a Local Node with a project

Goal: keep a dataset on your machine and use it in a project (UC-08).

1. Install the Local Node on your machine from the delivered package.
2. In the web app, open the project and choose the option to pair a Local Node. The web app shows a pairing code.
3. Enter the pairing code in the Local Node. The system confirms with MSG-17.
4. Select the folder that the Local Node watches.
5. Accept each dataset that the Local Node proposes. The system records a dataset version with data location `local`.
6. Before each job, the Local Node checks the hash of the version. If the hash differs, it rejects the job and proposes a new version (MSG-16).

Result: only the Local Node can read the rows. The web app shows no preview and no download of `local` rows (MSG-15).

To stop a Local Node, ask a Project Manager or Researcher to revoke it. Jobs on its `local` data are rejected afterwards (MSG-19). Published objects stay readable.

*Screenshot placeholder: the pairing code dialog in the web app.*

#### How an operator deploys the Platform

Goal: make the web app, the Platform and the engines available to users. The steps are at category level.

1. Prepare the host, database and object storage of section 2.1.
2. Set the secrets: one service key for each engine, the key that seals data-connection credentials, and the email and identity settings. Do not store any secret inside the delivered package.
3. Connect the five stage engines and the AI PI to the Platform. Set `dataset_first` as the pipeline.
4. Start the Platform. It updates its database before it accepts requests.
5. Create the first Platform Admin.
6. Sign in as the Platform Admin. Add model profiles for the roles `stage`, `review` and `vision`, add keys, and set the default budget and the spending ceiling (UC-39, UC-34).
7. Set the platform settings that Report III names: the upload size limit (SR-02).
8. Check the result with the post-install check below.

Post-install check:

| Check | Expected result |
|---|---|
| Health view | Every component shows healthy (UC-05). |
| Sign in | A test user signs in by email or with a Google account (UC-01). |
| First run | A Researcher starts a run from a topic and reaches the first decision inbox question (section 3.2). |
| Missing model | With a model profile removed, a run ends as `failed_technical` with MSG-30 and no output. |

To update, the operator deploys the new package and keeps the previous one for rollback. Open item 6 lists backup, upgrade and rollback rules that the sources do not define.

## 3. User Manual

### 3.1 Overview and navigation

OpenAI-Scientist runs research on tabular data. A Researcher gives a research case. The system runs five stages and ends with a Dossier. Code computes numbers, verdicts, grades and claim ceilings. AI proposes and writes text. The Researcher keeps the pinned decisions (section 3.5.3).

Who does what:

| Role | Main tasks in this manual |
|---|---|
| Platform Admin | Admin tasks (section 3.3.13). Sees project metadata only. |
| Project Manager | Members, settings, budget, cancel a run, approve extra spend, approve a Dossier. Also all Researcher tasks (BR-80). |
| Researcher | Datasets, runs, decision inbox, presets, lock, paper, export. |
| Reviewer | Read and comment on every object. Approve a Dossier by the review settings. |

The table lists the main areas of the web app. The labels are glossary terms. Report III states that screen layout is not specified (Open item 7).

| Area | What it holds |
|---|---|
| Project | Members, project settings, datasets, data connections, research cases, runs, Literature Base, decision inbox and audit log. |
| Run | Run state, the five stages, each contract item as green or red, the live trace, the decision log and the lab notebook. |
| Decision inbox | One queue for all stages with eight kinds of item: question, review batch, tentative decision, deviation, candidate, needs-you, release review and spending. |
| Objects | DatasetSnapshot, HypothesisSet, AnalysisPlan, Lock, EvidenceBundle, PaperPack and Dossier, each with a type, a version and a hash. |
| Administration | Users, model profiles, keys, engine settings, default budget, spending ceiling, audit log and health. Platform Admin only. |

The interface shows the source of each piece of information: AI proposal, code computation, reviewer finding, Researcher approval or AI PI decision (NFR-16).

*Screenshot placeholder: the project home with the area navigation.*

### 3.2 Tutorial: Your first run from a topic

This tutorial follows journey J1 (a topic without a dataset, through the five stages). You start with a topic and no dataset. You end with an accepted DatasetSnapshot and a running pipeline. Time and results depend on your data, so the tutorial gives no timing.

Before you start: you are a Researcher or a Project Manager in an active project, and the project has no active run (BR-09).

1. Sign in. Enter your email address and complete the sign-in request that the system sends (MSG-04). If the request has expired, request a new one (MSG-03). Or choose to sign in with your Google account (FR-146). Both ways give the same user when the verified email address is the same. (UC-01)
2. Open the project. Choose to start a run.
3. Enter the research case: topic, goals, context, constraints, domain and references. Leave the dataset empty. (UC-09)
4. Submit. If a run is already active, the system answers with MSG-08. If the monthly budget is at 100%, the start is blocked and the system shows MSG-51. Otherwise the run starts in state `running` on the `dataset_first` pipeline, which begins with the `dataset` stage.
5. Watch the `dataset` stage. It searches your project and public datasets. If it finds no usable dataset, it adds a question to the decision inbox. (UC-18)
6. Open the decision inbox. Pick one option: use a dataset already in the project, upload data, import from a data connection, or use a Local Node. The system creates a dataset version. (UC-16, UC-06, UC-07, UC-08)
7. Confirm the unit of observation and the data structure when the system asks (MSG-23). This is a pinned decision. The system creates no split before you confirm.
8. Read the DatasetSnapshot: the quality profile, the split, the data dictionary and the fitness (`fit`, `fit_with_limits`, `not_fit`).
9. Wait for the review loop to finish. Then accept the object version (MSG-35). At the default preset `milestones`, the level of acceptance follows the fitness. (UC-11, UC-27)
10. The next stages run. Section 3.3 explains how to choose hypotheses, lock the plan and read the results.

Result: you have an accepted, immutable DatasetSnapshot. The run continues to the hypothesis stage.

*Screenshot placeholder: the decision inbox with a dataset question.*

### 3.3 How-to guides

Each guide maps to use cases. Report III, section 5.3, holds the message catalogue. Three failures can occur in every guide, so the guides do not repeat them: MSG-01 for a missing role, MSG-02 for a non-member and MSG-07 for an archived project.

#### 3.3.1 Manage a project and its members

Roles: Project Manager. Use cases: UC-03, UC-04.

1. Open Members. Invite a user by email and choose a role.
2. The invited user accepts before the invitation expires (SR-05). An expired invitation gives MSG-05. Send a new one.
3. To change a role or remove a member, use the member row. You cannot remove the last active Project Manager (MSG-06).
4. To archive the project, use the project menu. An archived project is read-only (MSG-07).
5. Open the project settings. Set the monthly budget and its warning thresholds (SR-03), the review settings, the default preset per stage, the notifications, the limit of secondary hypotheses (SR-06), the response time for spending decisions (SR-04) and the wait deadline of pinned items.

Review settings are: the number of approvals, who may approve, and whether self-approval is allowed. New runs and new Dossier approvals use the new values. Past decisions do not change.

If a value is invalid, the system keeps the old value and shows the reason.

#### 3.3.2 Add data and versions

Roles: Researcher, Project Manager. Use cases: UC-06, UC-07, UC-08.

Upload a file:

1. Open the datasets of the project. Choose Upload.
2. Select a file. Choose a new dataset or an existing one.
3. The system checks the format (SR-01), the size (SR-02) and that the file holds a readable table (SR-07). It stores a new dataset version with a hash and shows MSG-12.

Failures: unsupported format (MSG-09), file too large (MSG-10), no readable table (MSG-11).

Import from a data connection:

1. Authorize access to the source (a cloud spreadsheet or file source).
2. Select the connection and the source.
3. The system imports a new dataset version (MSG-12). It never shows or logs the credential.

Failures: access not authorized (MSG-13), internal address (MSG-14).

Use data on your machine: follow the pairing steps in section 2.2. For `local` data, rows cannot be previewed or downloaded (MSG-15).

A dataset version never changes. A change creates a new version, and older versions stay as they were.

#### 3.3.3 Start or cancel a run

Roles: Researcher, Project Manager. Use cases: UC-09, UC-10, UC-12, UC-13.

Start a run: follow steps 2 to 4 of the tutorial in section 3.2.

Amend the research case: state the change and the reason. The system records a new case version. Stages that already started keep the old version. An empty reason is rejected (UC-10).

Follow a run: open the run. It shows the run state and, for each stage, each contract item as green or red. A red item becomes a task for the agent. If an item uses up its budget share, it becomes a needs-you item in the inbox (MSG-36). If a limit ends the stage, the stage ends on its best output and lists every red item (MSG-29).

Cancel a run: only a Project Manager, or the Researcher who created the run, can cancel.

1. Choose Cancel run.
2. Confirm (MSG-32). The run ends as `cancelled`.
3. Accepted objects stay. Waiting items close (MSG-33).

No Dossier exists for a cancelled run unless a PaperPack was already accepted (MSG-53).

Choose the next step: when a run ends, the AI PI writes the lab notebook and proposes one next step: `collect_more_data`, `explore_signal`, `replicate`, `write_paper` or `revise_plan`. You choose one (UC-14).

#### 3.3.4 Answer the decision inbox (present and away)

Roles: Researcher, Project Manager. Use cases: UC-15, UC-16, UC-17.

Set your presence first. Presence is `present` or `away`. It changes only how items wait (UC-15).

When you are present:

1. An agent raises a `must_ask` item. The system asks at once with options, a recommended option and a reason. The run shows MSG-24.
2. Choose an option. The system writes the decision log with the action type, level, policy version, decider and presence.
3. The run returns to `running`.

When you are away:

1. `must_ask` items wait. The agents continue work that does not depend on them.
2. Under the preset `autopilot`, the AI PI decides unpinned items tentatively. It never decides a pinned item (MSG-44) and it never ends a run.
3. When only pinned items wait, the stage stops at `ready_to_<action>`. The run stays in `waiting(decision)`. It does not end for that reason before the wait deadline of the item (FR-262).
4. The system sends an external notice only for a blocking pinned item and for a `spending` item (UC-38). Before the wait deadline of a pinned item, a reminder goes to the Researcher who created the run and to the Project Manager. Answer the item before the deadline.
5. If the wait deadline passes without an answer, the run ends `with_gaps`. The item closes unanswered, the gap is listed, and nobody decides the item for you. The Project Manager sets the deadline in the project settings.

When you return:

1. Open the decision inbox. The system shows the tentative decisions (MSG-42).
2. Confirm or overturn each one.
3. An overturn undoes dependent work and marks the affected objects stale (MSG-43, MSG-34). The system may propose a higher level from the overturn rate. You decide.

Pinned actions need you at every preset (section 3.4.3).

#### 3.3.5 Set the presets

Roles: Researcher, Project Manager. Use case: UC-15.

1. Open the control settings of a stage.
2. Choose `co_work`, `milestones` (default) or `autopilot`.
3. The system applies the preset to future actions and re-evaluates waiting items. It does not recompute past decisions.
4. To override the level of one action, choose a level. The system refuses a level below the floor of that action and shows the floor.

A Project Manager sets the default preset per stage in the project settings.

#### 3.3.6 Confirm the data structure

Roles: Researcher, Project Manager. Use cases: UC-18, UC-16.

1. When the system shows MSG-23, open the proposal for the unit of observation and the data structure (independent and identically distributed (IID) rows, grouped rows, time-ordered rows or panel).
2. Check them against your data.
3. Confirm, or change and confirm.
4. The system creates the split by power: `three_way`, `two_way` or `none` with a limitation. Rows of one group stay in one part. Time-ordered data splits by time.

Without your confirmation the system creates no split.

#### 3.3.7 Lock a plan

Roles: Researcher, Project Manager. Use cases: UC-19, UC-20, UC-21.

Before you lock, choose the hypotheses (two or more, with one primary). This is a pinned decision (UC-19).

1. Wait until the plan passed all checks and the review loop. The system creates the pinned item "lock plan".
2. Read the plan: the estimand (the quantity that the study estimates), the protocol, the analysis program, the decision rule and the interpretation table.
3. Choose Lock. Confirm MSG-37. The Platform records the Lock with the hashes, the snapshot version, the split digest, who locked and when.
4. The plan is now immutable.

If you are `away`, the plan waits (MSG-38). Nobody can lock it for you. A later change to the locked algorithm is a deviation. A deviation is pinned, logged and counted in the grade (MSG-39).

The system returns a hypothesis with no comparator, or with a deliberately weak baseline, for repair (MSG-40). Add a fair comparator.

#### 3.3.8 Unseal and read the verdict, grade and claim ceiling

Roles: Researcher, Reviewer, Project Manager. Use cases: UC-22, UC-23, UC-24.

1. After the lock, the execution stage runs the confirmatory job. Results go to the envelope, a sealed store at the Platform. Neither you nor the agent sees them.
2. When all checks are green, the Platform unseals all hypotheses at once (MSG-45). If you chose manual unseal, trigger the unseal yourself. An unseal before the last confirmatory fix is rejected (MSG-41).
3. Open the EvidenceBundle. Read for each hypothesis the verdict and the interpretation row.
4. Read the grade (A to D) and its reasons.
5. Read the claim ceiling. It is the strongest claim the evidence allows.
6. Read the deviation log, the tried ledger (the record of every exploration search and its noise threshold) and the candidates.

If the replicated hash differs, the bundle item turns red and the paper stage does not use it.

Candidates from exploration: each candidate arrives in the decision inbox (MSG-46). A candidate is never a claim. Choose what to do with it. A confirmed candidate gets a confirmation tier (UC-24).

#### 3.3.9 Handle budget review and spending

Roles: Project Manager (decide), Platform Admin (ceiling). Use cases: UC-32, UC-33, UC-34.

Read the budget. The system warns at each warning threshold of the monthly budget (MSG-26). Each run also has a token budget. When it is used up, the run ends `with_gaps` on its best output (MSG-29).

When the project reaches 100%:

1. New runs are blocked (MSG-51).
2. A run that is running enters `waiting(budget_review)` (MSG-25). The system creates a `spending` item and sends you an external notice.
3. A reminder arrives before the deadline (MSG-27).
4. Approve extra spend, and the run continues. Or let the run end with gaps.
5. If nobody decides before the deadline, the run ends `with_gaps` (MSG-28).

The Platform Admin sets the spending ceiling. Under `autopilot`, only spending below the ceiling is `auto`. The usage and cost ledger is available per run and per project.

#### 3.3.10 Use the Local Node and the release review

Roles: Researcher, Project Manager. Use cases: UC-30, UC-31.

1. Run a job on `local` data. The result passes the release gate: small-cell threshold, rounding, differencing check and probe budget.
2. If the release gate rejects a query, the system shows the reason (MSG-20).
3. If the probe budget is used up, the run continues and records a gap (MSG-21).
4. With disclosure mode `standard`, a release inside the policy is `auto`.
5. With disclosure mode `strict`, a number of an unapproved kind creates a release review item (MSG-22). Approve or reject the release.
6. Check the release log. The Platform copy matches the Local Node log.

If the Local Node goes offline, work that needs `local` data waits in `waiting(node_offline)` and other work continues. You receive one combined notice (MSG-18). When the Local Node returns, the run returns to `running`. After a revocation, jobs on its data are rejected (MSG-19).

No rows leave the machine at any time.

#### 3.3.11 Review the paper

Roles: Researcher, Project Manager. Use cases: UC-25, UC-26, UC-27, UC-28.

1. After the EvidenceBundle is accepted, the paper stage builds the PaperPack. Code renders every number from bundle records.
2. Read the draft. Fix the warnings the system shows:
   - a stray number that is not a reference (MSG-47);
   - a claim above the claim ceiling (MSG-48);
   - a citation that is not in the Literature Base or has an unresolved DOI (MSG-49).
3. Fill every field marked "awaiting author". The system fills no author-only field.
4. Read the reporting checklist and the limitations. The checklist is STROBE (Strengthening the Reporting of Observational Studies in Epidemiology) with its extension RECORD for association and causal claims, and TRIPOD (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis) for prediction.
5. If the review ends with open findings, they appear as known risks (MSG-50). Decide between the two sides where the system asks.
6. To ask a persona to review any object, select the persona and the object (UC-28).
7. Accept the PaperPack.

The system does not submit to any publisher. You decide on submission outside the system (UC-26).

#### 3.3.12 Approve and export the Dossier

Roles: Reviewer and Project Manager (approve), Researcher and Project Manager (export). Use cases: UC-35, UC-36, UC-37.

1. When a PaperPack is accepted, the Platform creates Dossier version 1 from the accepted EvidenceBundle and PaperPack versions. It checks each hash.
2. Reviewers and Project Managers read the Dossier and comment (UC-37).
3. Approve. Each approval follows the review settings. Self-approval where it is not allowed gives MSG-52.
4. When there are enough approvals for the current version, the Dossier is approved.
5. To export, choose Export. Export is pinned (MSG-39). Confirm.
6. The system writes the audit log with the Dossier version and the format.

A new accepted EvidenceBundle or PaperPack creates a new Dossier version (MSG-54). Approvals do not carry over. Export before approval is refused (MSG-55).

#### 3.3.13 Admin tasks

Role: Platform Admin. Use cases: UC-02, UC-05, UC-29, UC-34, UC-39.

| Task | Steps | UC |
|---|---|---|
| See all projects | Open the project overview. It shows members, usage and run states. It shows no research content (MSG-01 on an attempt). | UC-02 |
| Manage users, models and keys | Open administration. Manage users, model profiles per role, keys, engine settings and default budgets. Keys are sealed and never shown. | UC-39 |
| Read the audit log and health | Open the audit log (append-only), the health of each component and the run metrics: questions, blocked time, overturn rate. Read the precision of each persona. | UC-05 |
| Set the spending ceiling | Set the ceiling. It is a monetary limit for `spending` items, separate from the floor level of the group. | UC-34 |
| Run the benchmarks | Start a benchmark on request. Read the precision of each persona and the detection and block rates. | UC-29 |

If a model or credential is missing, runs end as `failed_technical` (MSG-30). If one literature source is unavailable, the stage logs the error and continues with the other sources (MSG-31). If the model service is unavailable, no output is created (MSG-58).

Other member tasks: comment on an object (UC-37) and set notification channels (UC-38). Only a blocking pinned item and a `spending` item send external notices.

Two tasks come after the MVP and have no guide here: build a journal profile (UC-40, Could) and compare methods (UC-41, Should).

### 3.4 Reference

#### 3.4.1 Verdict values, grades and claim ceiling

| Verdict | Meaning |
|---|---|
| `supported` | The evidence supports the hypothesis by the locked decision rule. |
| `trivial` | The effect falls in the region below the smallest effect size of interest (SESOI). |
| `not_supported` | The evidence does not support the hypothesis. |
| `insufficient` | The evidence is too weak to decide. |
| `not_tested` | The system did not test the hypothesis. |

Code computes every verdict from the locked decision rule. The text comes from the matching interpretation row. A non-significant p-value never supports equivalence.

| Grade | Meaning |
|---|---|
| A to D | Confidence in the evidence. Code computes it from diagnostics, robustness checks and deviations. A is the highest. |

The claim ceiling is the strongest claim that the verdict, the grade and the confirmation tier allow. The paper never exceeds it. A locked plan is not a proven claim.

Confirmation tiers, strongest first: `replicated`, `reserve`, `unsealed_untouched`, `unsealed_touched`.

Fitness values of a DatasetSnapshot: `fit`, `fit_with_limits`, `not_fit`.

#### 3.4.2 Run states

| State | Reason or result | Meaning |
|---|---|---|
| `running` | none | Work is in progress. |
| `waiting` | `decision` | The run needs an answer in the decision inbox. A pinned item that waits keeps the run in this state until its wait deadline. |
| `waiting` | `node_offline` | A job needs `local` data and the Local Node is offline. |
| `waiting` | `budget_review` | The project reached 100% of the monthly budget. A Project Manager decides. |
| `ended` | `complete` | All contract items are green. |
| `ended` | `with_gaps` | One of three causes: the token budget of the run ran out, a `spending` item passed its deadline, or the wait deadline of a pinned item passed (FR-262). The best output is published and red items are listed. A pinned item closes unanswered. |
| `ended` | `failed_technical` | A model or credential is missing. No output. |
| `ended` | `cancelled` | A Project Manager or the creating Researcher cancelled the run. A run can be cancelled from any state except `ended`. |

A project has at most one active run (BR-09). Every run reaches `ended` (NFR-03).

#### 3.4.3 Object states

| State | Meaning |
|---|---|
| In progress | The stage builds the object. Each contract item is green or red. |
| Ready for acceptance | All items are green and the review loop ran. |
| Accepted | The version is immutable and has a type, a version and a hash. |
| Stale | An upstream object that it pins has a newer version. Nothing updates by itself. You accept the update. |
| Locked | An AnalysisPlan fixed by a Lock. A change is a deviation. |
| Dossier: awaiting approval, approved | An approval belongs to exactly one Dossier version. |

Pinned actions are `must_ask` at every preset:

- define the outcome and the estimand;
- confirm the unit of observation and the data structure;
- choose hypotheses (two or more) and the primary;
- join public data into private data;
- lock the plan;
- deviate from the locked algorithm;
- use a validation source;
- export out of the project.

#### 3.4.4 Preset levels

| Item | Values |
|---|---|
| Preset (per stage) | `co_work`, `milestones` (default), `autopilot` |
| Level of an action | `auto`, `do_then_review`, `must_ask` |
| Presence | `present`, `away` |
| Action groups | `read_compute`, `technical_fix`, `content_judgment`, `object_drafting`, `spending`, `acceptance`, `pinned`, `unseal` |
| Fitness acceptance at `milestones` | `fit` is `auto`, `fit_with_limits` is `do_then_review`, `not_fit` is `must_ask` |

Each action belongs to one group and one level. An override cannot go below the floor. The floor of `object_drafting` is `do_then_review`, the floor of `pinned` is `must_ask`, and every other group has floor `auto`, including `acceptance`. The level of each group for each preset is in the permission model of Report IV, section 3.5.1.

#### 3.4.5 Message catalogue pointers

| Topic | Messages |
|---|---|
| Access and sign-in | MSG-01 to MSG-07 |
| Run start and cancel | MSG-08, MSG-32, MSG-33 |
| Data upload, import and Local Node | MSG-09 to MSG-17 |
| Local Node state and release | MSG-18 to MSG-22 |
| Decisions and the inbox | MSG-23, MSG-24, MSG-36 to MSG-39, MSG-42 to MSG-44 |
| Budget and spending | MSG-25 to MSG-28, MSG-51 |
| Run end and failure | MSG-29 to MSG-31, MSG-58 |
| Stale objects and acceptance | MSG-34, MSG-35 |
| Hypothesis and execution | MSG-40, MSG-41, MSG-45, MSG-46 |
| Paper checks | MSG-47 to MSG-49 |
| Review loop | MSG-50 |
| Dossier | MSG-52 to MSG-55 |

#### 3.4.6 Pipeline reference

| Stage | Hand-off object | Pinned by it |
|---|---|---|
| dataset | DatasetSnapshot | Dataset version |
| hypothesis | HypothesisSet | DatasetSnapshot, Literature Base version |
| experiment_design | AnalysisPlan | HypothesisSet |
| execution | EvidenceBundle | AnalysisPlan, through the Lock |
| paper | PaperPack | EvidenceBundle |

### 3.5 Explanation

#### 3.5.1 Why blind analysis, lock and envelope

An analyst can bias a result without intent. Many analysis choices exist, and a choice made after the result is seen can make a weak effect look strong. The system removes this chance in three steps.

- The lock fixes the plan, the program and the expected outputs before the confirmatory run. A later change is a deviation, and the grade counts it.
- The envelope holds the confirmatory results. Until the unseal, the agent sees only `done` or `error`. The agent works on a twin built from released aggregates, not on the real rows.
- The unseal opens all hypotheses at once, after the last confirmatory fix. The system records the time.

The result is that a verdict means what it says. Code, not a model, computes the verdict, the grade and the claim ceiling. The system promises that no error is hidden, every claim has a source, and every run can be run again. It does not promise that the science is right.

#### 3.5.2 Why the review is independent

An author misses its own errors. For this reason, every object version gets a review by reviewers with fresh context. They do not see the author's trace. Guards run in parallel and do not read each other's findings. Each finding needs an anchor and evidence. Code or a second verifier checks it, and only a confirmed blocking finding starts a revision round. The loop stops after two rounds. What remains is shown as a known risk. The system measures each persona against known flaws. It lowers the severity of the findings of a persona that is below its minimum precision.

#### 3.5.3 The human control model

The human keeps the decisions that only a Researcher should own. These are the pinned actions in section 3.4.3. For all other actions, the preset sets the level, and presence sets whether a waiting item asks now or waits. The AI PI may decide unpinned items tentatively when you are away. It never decides a pinned item and never ends a run. You see each tentative decision when you return, and you can overturn it. The user and the agent go through the same tools, guards and checks, so a user action is not exempt from a check.

The Platform Admin cannot read research content of a project without membership. A Dossier leaves the project only after approval and an explicit export decision.

## Open items

1. The package has no version identifier or release notes in the sources.
2. The sources define no sample dataset or sample project for the post-install check.
3. The sources define no support contact or hand-over of credentials for the deployed system.
4. The supported operating systems and the minimum hardware of the Local Node are not defined.
5. Sizing figures (CPU, memory, disk, network) for the operator side are not defined.
6. Backup, retention, upgrade and rollback rules for research data and for the Platform are not defined (Report III, Open item 8).
7. The screens and labels of the web app are not specified (Report III, Open item 9). The area names in section 3.1 use glossary terms.
8. The sign-in method after the email step (link or code) is not specified (Report III, Open item 11). The tutorial uses neutral wording.
9. The default upload size limit (SR-02) is 1 GB per file. The default values of the settings in SR-03 to SR-05 are not defined (Report III, Open item 5). The default limit of secondary hypotheses (SR-06) is 3, and the default wait deadline of pinned items (SR-08) is 7 days (Report III, Open items 4 and 5).
10. The sources give no time estimate for a first run, so the tutorial states none.

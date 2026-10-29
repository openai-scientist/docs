# III. Software Requirements Specification

This section follows ISO/IEC/IEEE 29148. It specifies OpenAI-Scientist as designed. It does not describe an implementation status. Requirement IDs are stable: BR-xx (business rules), FE-xx (features), FR-xx (functional requirements) and NFR-xx (quality requirements) come from the business and product requirements. This section alone defines UC-xx (use cases), SR-xx (system rules) and MSG-xx (user-facing messages). Test cases (TC-xx) are defined in Report V.

Priority uses MoSCoW. The minimum viable product (MVP) is FE-01 to FE-15 and FE-17. FE-18 (Journal Fingerprint Extraction) is Could. FE-19 (`method_comparison`) is Should; both come after the MVP.

## 1. Product overview

### 1.1 Purpose and scope

OpenAI-Scientist is a web application for research teams that work on tabular data. A Researcher starts from a research case. A dataset is optional at the start. The system runs the `dataset_first` pipeline through five stages: `dataset`, `hypothesis`, `experiment_design`, `execution` and `paper`. Each stage boundary has one hand-off object with a type, a version and a hash.

The system splits the work by what can be checked. Code computes numbers, verdicts, grades and claim ceilings. AI proposes and writes text. The Researcher keeps the pinned decisions (FR-27). An independent review is mandatory for every object version. Rows of `local` data stay on the user's machine. A Local Node releases only aggregates, through one release gate. The final result is a Dossier. Only an approved Dossier can leave the project.

The system promises three things: no error is hidden, every claim has a source, and every run can be run again. It makes no promise that the science is always right.

Out of scope: non-tabular data, new data collection design, full systematic reviews, full text behind paywalls, organizations and multi-tenancy, automatic submission to publishers, causal claims from a plan or a hypothesis alone, evaluating OpenAI-Scientist itself against human-only, AutoML or generic-agent systems, and the task families ranking, survival, forecasting and anomaly (BR-83). A user research topic that compares an AutoML method with baselines on the user's own data stays in scope under `method_comparison` (FE-19, Should, after MVP).

### 1.2 Product perspective

| Element | Role |
|---|---|
| Web app | The user interface. English only (NFR-19). |
| Platform | Holds users, projects, runs, decisions, budgets, keys, the envelope and the Dossier. |
| Stage engines | One engine per stage. All engines run on one shared harness (NFR-20). |
| AI PI | Summarizes, proposes next steps, writes the lab notebook and decides unpinned items tentatively. |
| Local Node | Runs on the user's machine. Keeps `local` data and runs jobs next to it. |
| External services | Model provider, scholarly metadata, public data, data connections, identity and email (section 4.1). |

*Figure 1: System context (diagram to be regenerated from the design model).*

### 1.3 Hand-off objects

| Object | Created by | Pins |
|---|---|---|
| DatasetSnapshot | `dataset` stage | Dataset version |
| HypothesisSet | `hypothesis` stage | DatasetSnapshot; Literature Base version |
| AnalysisPlan | `experiment_design` stage | HypothesisSet |
| Lock | Platform | AnalysisPlan version |
| EvidenceBundle | `execution` stage | AnalysisPlan, through the Lock |
| PaperPack | `paper` stage | EvidenceBundle |
| Dossier | Platform | Accepted versions of EvidenceBundle and PaperPack |

The Literature Base is a versioned evidence store of the project. It is not a hand-off object. Every stage reads it by version (FR-43).

### 1.4 Assumptions and constraints

- The Platform Admin configures the model provider and keys. If they are missing, the run reports a clear error (FR-103).
- The scholarly metadata service returns metadata and abstracts with provenance. Full text behind paywalls is out of scope.
- The user has tabular data for the question, or can use a dataset already in the project.
- The user keeps the Local Node running while a job needs `local` data.
- The system supports tabular data only. The project is the highest scope. The Local Node needs no Docker on the user's machine. A project has at most one active run (BR-09).

## 2. User requirements

### 2.1 Actors

| Actor | Type | Scope | Main goals |
|---|---|---|---|
| Platform Admin | System role | Whole system | Manage users, models, keys, engine settings, default budget, audit log and health. Sees project metadata only. |
| Project Manager | Project role | Managed project | Manage members, settings, budget, datasets and runs. Cancel runs. Approve extra spend. Approve the Dossier. Do all Researcher work (BR-80). |
| Researcher | Project role | Project of membership | Create research cases and runs. Answer the decision inbox. Accept objects. Lock plans. Write the paper. |
| Reviewer | Project role | Project of membership | Read and comment on every object. Approve the Dossier by the review settings. |
| AI PI | Secondary actor (connector persona) | Running run | Acts in use cases on the user's behalf, within its limits: summarize, propose the next step, write the lab notebook, decide unpinned items tentatively under `autopilot` and `away`. Never decides a pinned item. Not a member. |
| Persona | System actor | Stage | Maker personas create objects. Guard personas review objects. Connector personas link the run to the user; the AI PI is one. |

Conceptual permission matrix (BR-02, BR-06, BR-26, BR-30, BR-31, BR-60, BR-63, BR-64, BR-77, BR-80):

| Capability | Platform Admin | Project Manager | Researcher | Reviewer | AI PI |
|---|---|---|---|---|---|
| View | Metadata only | Yes | Yes | Yes | Running run |
| Comment | No | Yes | Yes | Yes | No |
| Run (create and run) | No | Yes | Yes | No | No |
| Answer inbox | No | Yes | Yes | No | Tentative decision for unpinned items only |
| Accept hand-off object | No | Yes | Yes | No | Tentative decision for unpinned items only |
| Lock plan | No | Yes | Yes | No | No (pinned) |
| Cancel run | No | Yes | Yes, own runs | No | No |
| Approve extra spend | No | Yes | No | No | No |
| Approve Dossier | No | Yes [a] | No | Yes [a] | No |
| Export | No | Yes | Yes | No | No (pinned) |
| Administer | System | Project | No | No | No |

[a] By the review settings of the project: number of approvals, who may approve, and whether self-approval is allowed (BR-63). If a Platform Admin is also a member of a project, the project role of that person applies.

### 2.2 Use cases

*Figure 2: Use case diagram (diagram to be regenerated from the design model).*

Coverage: the 41 use cases cover 271 of 271 FRs. Every one of the 254 Must FRs is covered by at least one UC. The 6 Could FRs (FR-106 to FR-109, FR-260 and FR-261) are covered by UC-40. The 11 Should FRs (FR-139 to FR-145, FR-194 and FR-267 to FR-269) are covered by UC-41.

| UC | Name | Primary actor | FE | FR covered |
|---|---|---|---|---|
| UC-01 | Sign in | Any user | FE-01 | FR-01, FR-02, FR-146, FR-151 |
| UC-02 | View project metadata | Platform Admin | FE-01 | FR-03, FR-152 |
| UC-03 | Manage members | Project Manager | FE-02 | FR-04 to FR-06, FR-153 |
| UC-04 | Configure project settings | Project Manager | FE-02, FE-05 | FR-08, FR-263 |
| UC-05 | Review audit log, health and operating metrics | Platform Admin | FE-02, FE-17 | FR-07, FR-104, FR-105, FR-258, FR-259 |
| UC-06 | Upload a dataset | Researcher | FE-03 | FR-09, FR-112, FR-154 |
| UC-07 | Import from a data connection | Researcher | FE-03 | FR-10, FR-11, FR-155, FR-156 |
| UC-08 | Pair a Local Node and register local data | Researcher | FE-03, FE-12 | FR-12, FR-79, FR-84, FR-87, FR-157, FR-158, FR-230, FR-236, FR-240 |
| UC-09 | Start a run from a research case | Researcher | FE-02, FE-04 | FR-13, FR-14, FR-16, FR-111 |
| UC-10 | Amend a research case | Researcher | FE-04 | FR-17, FR-160 |
| UC-11 | Accept a hand-off object | Researcher | FE-04 | FR-18, FR-19, FR-161, FR-162 |
| UC-12 | Monitor and recover a run | Researcher | FE-04, FE-17 | FR-20, FR-21, FR-24, FR-103, FR-163 to FR-165, FR-169, FR-257, FR-262, FR-265 |
| UC-13 | Cancel a run | Project Manager | FE-04 | FR-22, FR-166 to FR-168 |
| UC-14 | Choose the next step | Researcher | FE-04, FE-05 | FR-23, FR-35 |
| UC-15 | Set preset and presence | Researcher | FE-05 | FR-25, FR-26, FR-147 to FR-150, FR-170 to FR-172 |
| UC-16 | Answer a decision inbox item | Researcher | FE-05 | FR-27 to FR-30, FR-33, FR-34, FR-36, FR-173 to FR-176, FR-179, FR-180, FR-263 |
| UC-17 | Confirm or overturn a tentative decision | Researcher | FE-05 | FR-31, FR-32, FR-177, FR-178, FR-266 |
| UC-18 | Run the dataset stage | Researcher | FE-04, FE-06 | FR-15, FR-37 to FR-42, FR-113 to FR-118, FR-159, FR-181 to FR-185 |
| UC-19 | Run the hypothesis stage | Researcher | FE-07 | FR-43 to FR-45, FR-119 to FR-123, FR-186, FR-187 |
| UC-20 | Run the experiment_design stage | Researcher | FE-08 | FR-46, FR-47, FR-124 to FR-132, FR-190 to FR-193, FR-195, FR-196 |
| UC-21 | Lock a plan | Researcher | FE-08 | FR-48, FR-49, FR-188, FR-189 |
| UC-22 | Run the execution stage | Researcher | FE-09 | FR-50 to FR-53, FR-56, FR-133, FR-197 to FR-201, FR-205 |
| UC-23 | Read verdict, grade and claim ceiling | Researcher | FE-09 | FR-54, FR-55, FR-60, FR-61, FR-202 to FR-204, FR-210, FR-211 |
| UC-24 | Triage exploration candidates | Researcher | FE-09 | FR-57 to FR-59, FR-206 to FR-209 |
| UC-25 | Run the paper stage | Researcher | FE-10 | FR-62 to FR-69, FR-212 to FR-220 |
| UC-26 | Decide on submission | Researcher | FE-10 | FR-70 |
| UC-27 | Run the review loop | Persona (guard) | FE-11 | FR-71 to FR-76, FR-221 to FR-227, FR-270, FR-271 |
| UC-28 | Invoke a persona on an object | Researcher | FE-11 | FR-78 |
| UC-29 | Run the benchmarks | Platform Admin | FE-11 | FR-77, FR-134 to FR-138, FR-228, FR-229 |
| UC-30 | Release an aggregate from local data | Researcher | FE-12 | FR-80 to FR-83, FR-86, FR-231 to FR-235, FR-239 |
| UC-31 | Handle a Local Node that is offline or revoked | Researcher | FE-12 | FR-85, FR-110, FR-237, FR-238, FR-241, FR-242 |
| UC-32 | Warn on and enforce budgets | Project Manager | FE-13 | FR-88, FR-89, FR-243, FR-244 |
| UC-33 | Decide extra spend | Project Manager | FE-13 | FR-90, FR-91, FR-245 to FR-247 |
| UC-34 | Set the spending ceiling and read the ledger | Platform Admin | FE-13 | FR-92, FR-93, FR-248 |
| UC-35 | Review and approve a Dossier | Reviewer | FE-14 | FR-94 to FR-96, FR-249 to FR-252 |
| UC-36 | Export a Dossier | Researcher | FE-14 | FR-97, FR-98, FR-253 |
| UC-37 | Comment on an object | Reviewer | FE-15 | FR-99, FR-254 |
| UC-38 | Receive notifications | Any member | FE-05, FE-15 | FR-100, FR-255, FR-264 |
| UC-39 | Manage users, models and keys | Platform Admin | FE-17 | FR-101, FR-102, FR-256 |
| UC-40 | Build a journal profile (Could) | Researcher | FE-18 | FR-106 to FR-109, FR-260, FR-261 |
| UC-41 | Compare methods (Should) | Researcher | FE-19 | FR-139 to FR-145, FR-194, FR-267 to FR-269 |

In every UC, an action by a member without the needed role fails with MSG-01. A user who is not a member of the project receives MSG-02. A write to an archived project fails with MSG-07. These cases are not repeated below.

#### UC-01 Sign in
- Goal: the user signs in with an email address and no password, or with a Google account.
- Actors: any user.
- Preconditions: the user has an email address that the system knows or has an invitation for, or a Google account.
- Trigger: the user opens the web app.
- Main flow: 1. The user enters an email address, or selects sign-in with a Google account. 2. With an email address, the system sends a sign-in request to that address (MSG-04) and the user completes the request. With a Google account, the user completes the sign-in at Google. 3. The system matches the verified email address to a user. A Google account and an email sign-in with the same verified email address give the same user. 4. The system opens a session and shows the projects the user belongs to.
- Alternative and exception flows: the request has expired (MSG-03). The Google sign-in does not complete (MSG-56). The email address of the Google account is not verified (MSG-57). A person who is not a member asks for a project; the system hides that the project exists (MSG-02).
- Postconditions: the user has a session. Every later action is checked against the role of the user.
- Business rules: BR-01, BR-02, BR-103.
- FR traced: FR-01, FR-02, FR-146, FR-151.

#### UC-02 View project metadata
- Goal: the Platform Admin sees project metadata without seeing research content.
- Actors: Platform Admin.
- Preconditions: signed in as Platform Admin.
- Trigger: the Platform Admin opens the project overview.
- Main flow: 1. The system lists all projects with members, usage and run states. 2. The Platform Admin opens one project and sees its metadata.
- Alternative and exception flows: the Platform Admin tries to open a dataset, an object or a manuscript without membership (MSG-01).
- Postconditions: no research content was shown.
- Business rules: BR-06.
- FR traced: FR-03, FR-152.

#### UC-03 Manage members
- Goal: the Project Manager controls who works in the project.
- Actors: Project Manager.
- Preconditions: the user is a Project Manager of an active project.
- Trigger: the Project Manager invites, changes or removes a member, or archives the project.
- Main flow: 1. The Project Manager invites a user with a role. 2. The invited user accepts before the invitation expires (SR-05). 3. The system adds the member and writes the audit log.
- Alternative and exception flows: the invitation has expired (MSG-05). The action would remove the last active Project Manager (MSG-06). The project is archived (MSG-07).
- Postconditions: the project has at least one active Project Manager. An archived project is read-only.
- Business rules: BR-03, BR-04, BR-05.
- FR traced: FR-04 to FR-06, FR-153.

#### UC-04 Configure project settings
- Goal: the Project Manager sets the level of control and review of the project.
- Actors: Project Manager.
- Preconditions: the user is a Project Manager.
- Trigger: the Project Manager opens project settings.
- Main flow: 1. The Project Manager sets the monthly budget and its warning thresholds (SR-03). 2. The Project Manager sets the review settings: number of approvals, who may approve, whether self-approval is allowed. 3. The Project Manager sets the default preset per stage, the notification settings, the limit of secondary hypotheses (SR-06), the response time for spending decisions (SR-04) and the wait deadline of pinned items (SR-08). 4. The system saves the settings and writes the audit log.
- Alternative and exception flows: a value is invalid; the system keeps the old value and shows the reason.
- Postconditions: new runs and new Dossier approvals use the new settings. Existing decisions are not recomputed.
- Business rules: BR-24, BR-59, BR-63, BR-78, BR-92, BR-104.
- FR traced: FR-08, FR-263.

#### UC-05 Review audit log, health and operating metrics
- Goal: the Platform Admin investigates and monitors the system.
- Actors: Platform Admin.
- Preconditions: signed in as Platform Admin.
- Trigger: the Platform Admin opens the audit log, the health view or the run metrics.
- Main flow: 1. The system shows the append-only audit log of important project and system changes. 2. The system shows the health of each component. 3. For each run, the system reports the number of questions, the blocked time and the overturn rate per action type. 4. The system reports the precision of each persona from the seeded-flaw bench.
- Alternative and exception flows: a component is unhealthy; the system marks it and shows the last known state.
- Postconditions: the audit log is unchanged by reading.
- Business rules: BR-05, BR-29, BR-40.
- FR traced: FR-07, FR-104, FR-105, FR-258, FR-259.

#### UC-06 Upload a dataset
- Goal: the user adds tabular data as a new immutable dataset version.
- Actors: Researcher, Project Manager.
- Preconditions: signed in as a project member with the Researcher or Project Manager role.
- Trigger: the user selects a file to upload.
- Main flow: 1. The user selects a file and a dataset (new or existing). 2. The system checks the format (SR-01), the size (SR-02) and that the file holds a readable table (SR-07). 3. The system stores the data as a new dataset version with a hash and data location `platform`. 4. The system shows the version (MSG-12).
- Alternative and exception flows: unsupported format (MSG-09). File too large (MSG-10). No readable table (MSG-11). The user asks for a preview of `local` data (MSG-15).
- Postconditions: a new version exists. Older versions are unchanged.
- Business rules: BR-16, BR-18, BR-102.
- FR traced: FR-09, FR-112, FR-154.

#### UC-07 Import from a data connection
- Goal: the user imports data from an authorized external source.
- Actors: Researcher, Project Manager.
- Preconditions: the user has authorized access to the source.
- Trigger: the user selects a data connection and a source.
- Main flow: 1. The user selects the connection and the source. 2. The system checks that the source is authorized and not an internal host. 3. The system imports the data as a new dataset version (MSG-12). 4. The system never shows or logs the credential.
- Alternative and exception flows: access is not authorized (MSG-13). The source is an internal host (MSG-14).
- Postconditions: a new version exists. No credential appears in any log.
- Business rules: BR-16, BR-17.
- FR traced: FR-10, FR-11, FR-155, FR-156.

#### UC-08 Pair a Local Node and register local data
- Goal: the user keeps data on the own machine and uses it in a project.
- Actors: Researcher, Project Manager.
- Preconditions: the user installed the Local Node. No Docker is needed.
- Trigger: the user enters a pairing code in the Local Node.
- Main flow: 1. The user pairs the Local Node with the project by a pairing code (MSG-17). 2. The Local Node proposes datasets from the folder it watches. 3. The user accepts a dataset. 4. The system records a dataset version with data location `local`. 5. Before a job, the Local Node checks the hash of the version.
- Alternative and exception flows: the hash does not match; the Local Node rejects the job and proposes a new version (MSG-16). The user asks to preview or download rows (MSG-15).
- Postconditions: only the Local Node can read the `local` data.
- Business rules: BR-16, BR-18.
- FR traced: FR-12, FR-79, FR-84, FR-87, FR-157, FR-158, FR-230, FR-236, FR-240.

#### UC-09 Start a run from a research case
- Goal: the user starts a run from a question, with or without a dataset.
- Actors: Researcher, Project Manager (BR-80).
- Preconditions: the project is active and has no active run.
- Trigger: the user submits a research case.
- Main flow: 1. The user enters topic, goals, context, constraints, domain and references. A dataset is optional. 2. The system checks that no run is active. 3. The system creates the run on the `dataset_first` pipeline. 4. The `dataset` stage starts (UC-18).
- Alternative and exception flows: a run is already active (MSG-08). The monthly budget is at 100%; the system blocks the start (MSG-51).
- Postconditions: one run is active in `running` state.
- Business rules: BR-07, BR-08, BR-09, BR-80.
- FR traced: FR-13, FR-14, FR-16, FR-111.

#### UC-10 Amend a research case
- Goal: the user changes a fixed research case in a controlled way.
- Actors: Researcher.
- Preconditions: the research case is fixed.
- Trigger: the user opens an amendment.
- Main flow: 1. The user states the change and the reason. 2. The system records a new case version with an event. 3. Stages that already started keep the old case version.
- Alternative and exception flows: the reason is empty; the system rejects the amendment.
- Postconditions: a new case version exists. Later stages use it.
- Business rules: BR-10.
- FR traced: FR-17, FR-160.

#### UC-11 Accept a hand-off object
- Goal: the user accepts an object version so the next stage can use it, or updates a stale object.
- Actors: Researcher, Project Manager.
- Preconditions: all contract items of the object are green and the review loop ran (UC-27). A contract item is a required part of a stage output that code checks.
- Trigger: the object is ready for acceptance, or an upstream object has a new version.
- Main flow: 1. The system shows the object version, its type, version and hash (MSG-35). 2. The user accepts it by the preset of the stage. 3. The object becomes immutable. 4. If an upstream object has a new version, the system marks each downstream object that pins it as stale (MSG-34). Nothing updates by itself. 5. The user chooses to update through a new acceptance.
- Alternative and exception flows: the user rejects the version; a new version is needed.
- Postconditions: an accepted object never changes. A change creates a new version.
- Business rules: BR-11, BR-12.
- FR traced: FR-18, FR-19, FR-161, FR-162.

#### UC-12 Monitor and recover a run
- Goal: the user follows a run and the run always reaches an end.
- Actors: Researcher, Project Manager.
- Preconditions: a run exists.
- Trigger: the user opens the run.
- Main flow: 1. The system shows the run state and, per stage, each contract item as green or red. 2. A red item becomes a task for the agent to fix. 3. When an item uses up its budget share, it becomes a needs-you item (MSG-36). 4. The system keeps every number computed by code. Model text carries references to records. 5. At a limit, the stage ends on the best output and lists every red item (MSG-29). 6. A run in `waiting(decision)` stays there until the user decides or the wait deadline of the pinned item passes. A run ends with gaps only for one of three causes: its token budget is used up (UC-32), a `spending` item passes its deadline (UC-33), or a pinned item passes its wait deadline (UC-16). In the third case the item closes unanswered and the gap is listed (MSG-60). A cancel moves any state except `ended` to `ended(cancelled)` (UC-13).
- Alternative and exception flows: a model or credential is missing; the run ends as `failed_technical` with a clear error and no output (MSG-30). A literature source is unavailable; the error is logged per source and the stage continues with the other sources (MSG-31). A model service is unavailable; the run creates no output (MSG-58).
- Postconditions: the run ends in `complete`, `with_gaps`, `failed_technical` or `cancelled`, or waits in a defined `waiting` state. No run hangs.
- Business rules: BR-13, BR-14, BR-41, BR-104.
- FR traced: FR-20, FR-21, FR-24, FR-103, FR-163 to FR-165, FR-169, FR-257, FR-262, FR-265.

#### UC-13 Cancel a run
- Goal: the user ends a run that is no longer needed without losing accepted results.
- Actors: Project Manager, or the Researcher who created the run.
- Preconditions: the run is in any state except `ended`.
- Trigger: the user selects Cancel run.
- Main flow: 1. The system asks for confirmation (MSG-32). 2. The user confirms. 3. The run ends as `ended(cancelled)`. 4. The system keeps accepted objects, closes all waiting items and writes the audit log (MSG-33).
- Alternative and exception flows: another Researcher tries to cancel (MSG-01). The user declines the confirmation; nothing changes.
- Postconditions: no Dossier exists unless a PaperPack was already accepted.
- Business rules: BR-77.
- FR traced: FR-22, FR-166 to FR-168.

#### UC-14 Choose the next step
- Goal: after a run, the user picks what to do next.
- Actors: Researcher; AI PI.
- Preconditions: the run ended.
- Trigger: the run ends.
- Main flow: 1. The AI PI writes the lab notebook with a summary, proposals, tentative decisions and reasons. 2. The AI PI proposes a next step from the fixed set: `collect_more_data`, `explore_signal`, `replicate`, `write_paper`, `revise_plan`. 3. The user chooses one.
- Alternative and exception flows: the user chooses none; the run stays ended.
- Postconditions: the user's choice is recorded.
- Business rules: BR-15, BR-34.
- FR traced: FR-23, FR-35.

#### UC-15 Set preset and presence
- Goal: the user sets how much control each stage needs.
- Actors: Researcher, Project Manager.
- Preconditions: a project exists.
- Trigger: the user opens the control settings of a stage.
- Main flow: 1. The user selects a preset for a stage: `co_work`, `milestones` (default) or `autopilot`. 2. The system applies it to future actions and re-evaluates waiting items. Past decisions are not recomputed. 3. The user sets presence to `present` or `away`. 4. The system gives each action one action group and one level and refuses an override below the floor. 5. The system sets the level of each of the eight action groups by the preset (FR-147 to FR-149) and by the floor (FR-150).
- Alternative and exception flows: an override goes below the floor; the system rejects it and shows the floor.
- Postconditions: the preset and presence change only how items wait.
- Business rules: BR-24, BR-25, BR-26, BR-27, BR-33, BR-49, BR-61.
- FR traced: FR-25, FR-26, FR-147 to FR-150, FR-170 to FR-172.

#### UC-16 Answer a decision inbox item
- Goal: the user decides items that need a human.
- Actors: Researcher, Project Manager.
- Preconditions: an item exists in the decision inbox.
- Trigger: an agent raises a `must_ask` action, or the user opens the inbox.
- Main flow: 1. The system collects items of all stages in one decision inbox. The eight kinds are question, review batch, tentative decision, deviation, candidate, needs-you, release review and spending. 2. If the user is `present`, the system asks at once with options, a recommended option and a reason (MSG-24). If the user is `away`, the item waits and the agent continues work that does not depend on it. 3. The user answers. 4. The system records the decision with action type, level, policy version, decider and presence, and computes the overturn rate per action type. The system may propose a higher level and never raises it. 5. If the agent used an assumption, the system records it with the alternatives and the reason.
- Alternative and exception flows: a pinned item stays `must_ask` at every preset: define the outcome and estimand, confirm the unit of observation and data structure, choose hypotheses (two or more) and the primary, join public data into private data, lock the plan, deviate from the locked algorithm, use a validation source, export out of the project (MSG-23, MSG-37, MSG-39). At `milestones`, the level of fitness acceptance follows the code verdict: `fit` is `auto`, `fit_with_limits` is `do_then_review`, `not_fit` is `must_ask`. Every pinned item has a wait deadline, a project setting (SR-08). A pinned item that waits keeps the run in `waiting(decision)` until the deadline; the run does not end before it. The system sends a reminder before the deadline to the Researcher who created the run and to the Project Manager (MSG-59). If nobody answers, the item closes unanswered, the run ends `ended(with_gaps)` and the gap is listed (MSG-60). Nobody decides the item in place of the user: not the AI PI and not a default value. User actions go through the same tools, guards and checks as agent actions. The system sends external notices only for a blocking pinned item and for a `spending` item.
- Postconditions: the decision log has an entry. The run returns to `running`.
- Business rules: BR-26, BR-27, BR-28, BR-29, BR-32, BR-33, BR-75, BR-104.
- FR traced: FR-27 to FR-30, FR-33, FR-34, FR-36, FR-173 to FR-176, FR-179, FR-180, FR-263.

#### UC-17 Confirm or overturn a tentative decision
- Goal: the user checks what the AI PI decided while the user was away.
- Actors: Researcher; AI PI.
- Preconditions: the preset is `autopilot` and the user was `away`.
- Trigger: the user returns and opens the inbox.
- Main flow: 1. While the user is away, the AI PI decides unpinned items tentatively. Each decision is a tentative decision. 2. The AI PI never ends the run and never decides a pinned item. When only pinned items wait, the stage ends at `ready_to_<action>` and the run stays in `waiting(decision)` until the wait deadline of the item; the AI PI and a default value never decide it, also after the deadline (UC-16). 3. The user returns and sees every tentative decision (MSG-42). 4. The user confirms or overturns each one. 5. On an overturn, the system undoes the dependent work, marks the affected objects stale (MSG-43) and records the overturn. The system may propose a higher level from the overturn rate. The user decides.
- Alternative and exception flows: the AI PI would decide a pinned item; the system blocks it (MSG-44).
- Postconditions: the decision log shows confirmed and overturned decisions.
- Business rules: BR-29, BR-30, BR-31, BR-104.
- FR traced: FR-31, FR-32, FR-177, FR-178, FR-266.

#### UC-18 Run the dataset stage
- Goal: the stage turns data into a DatasetSnapshot.
- Actors: Researcher; Persona (dataset).
- Preconditions: a run exists.
- Trigger: the run starts.
- Main flow: 1. If the research case has no dataset, the stage searches the project, searches public datasets (role `enrichment` or `validation`), or asks the user through the inbox. Joining public data into private data stays a pinned action. 2. The stage identifies the unit of observation and the data structure. 3. The Researcher confirms them (MSG-23). 4. The stage creates the split by power: `three_way` if the sample size gives power of at least 0.8 and a reserve remains, `two_way` otherwise, `none` below the minimum sample size with a limitation. Rows of one group stay in one part. Time-ordered data splits by time. Independent and identically distributed (IID) data with a classification task family may use a repeated stratified split, only within the exploration part; the confirmation part is used once. 5. The stage reports covariate shift, label shift and concept drift apart. 6. The dictionary records when each variable is available and flags post-outcome variables. The stage checks duplicate rows across parts. 7. The prefilter flags data signals from marginal distributions only and suggests research patterns. 8. Code concludes fitness. 9. The stage creates the DatasetSnapshot. The review loop runs (UC-27).
- Alternative and exception flows: no usable dataset exists (an inbox question). The Researcher has not confirmed the structure; the system does not create the split. Cleaning that needs the outcome moves to the AnalysisPlan.
- Postconditions: a DatasetSnapshot with source, table model, five-dimension quality profile, dictionary, cleaning recipe, question map, split, source roles and fitness.
- Business rules: BR-08, BR-26, BR-41, BR-43, BR-44, BR-76, BR-84, BR-85, BR-86, BR-88, BR-89.
- FR traced: FR-15, FR-37 to FR-42, FR-113 to FR-118, FR-159, FR-181 to FR-185.

#### UC-19 Run the hypothesis stage
- Goal: the stage reviews the literature and creates a HypothesisSet with evidence.
- Actors: Researcher; Persona (hypothesis).
- Preconditions: an accepted DatasetSnapshot.
- Trigger: the `dataset` stage is accepted.
- Main flow: 1. The stage builds or updates the Literature Base from metadata, abstracts and open-access full text. 2. A source fails: the stage logs the error per source (MSG-31) and continues with others. 3. The stage writes the HypothesisSet with at least two hypotheses that have different claim keys, and one primary. 4. Each hypothesis has a draft estimand, variables, sourced confounders, a smallest effect size of interest (SESOI), a refutation statement, a contribution type, an origin, a comparator, a primary metric that fits the task family, a direction or margin, a scope and a decision rule. 5. A non-inferiority or equivalence margin maps onto the SESOI regions. 6. The Researcher chooses the hypotheses and the primary (pinned).
- Alternative and exception flows: a hypothesis has no comparator or a deliberately weak baseline (MSG-40). All sources fail; the stage records a gap. A non-significant p-value never supports equivalence. The number of secondary hypotheses exceeds the limit (SR-06).
- Postconditions: a HypothesisSet with evidence and a versioned Literature Base.
- Business rules: BR-41, BR-45, BR-90, BR-91, BR-92.
- FR traced: FR-43 to FR-45, FR-119 to FR-123, FR-186, FR-187.

#### UC-20 Run the experiment_design stage
- Goal: the stage creates an AnalysisPlan for existing tabular data.
- Actors: Researcher; Persona (experiment_design).
- Preconditions: an accepted HypothesisSet.
- Trigger: the `hypothesis` stage is accepted.
- Main flow: 1. The stage selects the task family and the research pattern from the registry. 2. The stage writes the AnalysisPlan: estimand, protocol by claim type, adjustment set, analysis program, fallback, decision rule, interpretation table, robustness set, design diagnosis, hypothesis family structure, task family, pattern and pipeline order. 3. For `prediction`, the plan has three evidence families in order: discrimination, reliability and decision. 4. For `rare-event`, the metric is average precision (AP) or precision at fixed recall; AP is not compared across different prevalences; calibration uses data apart from training. 5. The baseline policy applies: simple baselines first, same split, same tuning budget, runtime reported with score. 6. The stage runs the analysis program on the twin, a synthetic table built only from released aggregates. 7. The review loop runs.
- Alternative and exception flows: a step breaks the pipeline order; the system blocks it (MSG-61). A check is red; the agent fixes it.
- Postconditions: an AnalysisPlan with all contract items green, waiting for lock.
- Business rules: BR-46, BR-50, BR-83, BR-86, BR-93, BR-94, BR-95, BR-96, BR-99.
- FR traced: FR-46, FR-47, FR-124 to FR-132, FR-190 to FR-193, FR-195, FR-196.

#### UC-21 Lock a plan
- Goal: the user fixes the plan before the confirmatory run.
- Actors: Researcher, Project Manager.
- Preconditions: the plan passed all checks and the review loop.
- Trigger: the stage creates the pinned item "lock plan".
- Main flow: 1. If the user is `present`, the user reads the plan (MSG-37). 2. The user locks the plan. 3. The Platform records the Lock: hashes of spec, program and golden outputs (the outputs of the locked program on the twin), snapshot version, split digest, who locked and when. 4. The locked plan is immutable. 5. The `execution` stage builds from the Lock.
- Alternative and exception flows: the user is `away`; the plan waits for lock and no one locks for the user (MSG-38).
- Postconditions: a Lock exists. Any later algorithm change is a deviation.
- Business rules: BR-26, BR-31, BR-47.
- FR traced: FR-48, FR-49, FR-188, FR-189.

#### UC-22 Run the execution stage
- Goal: the stage runs the locked plan, seals confirmatory results and unseals them.
- Actors: Researcher; Persona (execution).
- Preconditions: a Lock exists.
- Trigger: the user locks the plan.
- Main flow: 1. The stage runs in a sandbox. The agent works freely on the twin and touches real data only through aggregates or the full program. 2. A dry run on real data returns only row count, types, missingness, convergence and time. 3. The confirmatory job writes results to the envelope, a sealed store at the Platform. Before unseal the agent sees only done or error. 4. When all checks are green, the Platform unseals (opens the envelope for) all hypotheses at once and records the time. If the user chose manual unseal, the user triggers it. 5. The guard blocks a pipeline order violation before the run, or the system records it as a deviation.
- Alternative and exception flows: an unseal earlier than the last confirmatory fix is rejected (MSG-41). Unseal succeeds (MSG-45). A change to the locked algorithm is a deviation (MSG-39), pinned, logged and counted in the grade.
- Postconditions: results are unsealed. Code computes verdicts, grade and claim ceiling (UC-23).
- Business rules: BR-11, BR-26, BR-48, BR-49, BR-50, BR-86, BR-87.
- FR traced: FR-50 to FR-53, FR-56, FR-133, FR-197 to FR-201, FR-205.

#### UC-23 Read verdict, grade and claim ceiling
- Goal: the user reads what the evidence allows.
- Actors: Researcher, Reviewer, Project Manager.
- Preconditions: the results are unsealed.
- Trigger: the `execution` stage produces the EvidenceBundle.
- Main flow: 1. Code computes the verdict of each hypothesis: `supported`, `trivial`, `not_supported`, `insufficient` or `not_tested`. The text comes from the matching interpretation row. 2. Code computes grade A to D from diagnostics, robustness and deviation. 3. The `execution` stage computes the claim ceiling, the strongest claim the evidence allows, from verdict, grade and confirmation tier. A locked plan is not a proven claim. 4. The EvidenceBundle holds ten checked items, including the replication package. 5. The Replicator reproduces the results. 6. The user reads verdicts, grade, ceiling, deviation log and candidates.
- Alternative and exception flows: the replicated hash differs; the bundle item turns red and the paper does not use it.
- Postconditions: an EvidenceBundle with a claim ceiling.
- Business rules: BR-11, BR-54, BR-55, BR-56, BR-57.
- FR traced: FR-54, FR-55, FR-60, FR-61, FR-202 to FR-204, FR-210, FR-211.

#### UC-24 Triage exploration candidates
- Goal: the user decides what to do with candidates from exploration.
- Actors: Researcher.
- Preconditions: lane E produced candidates.
- Trigger: a candidate enters the decision inbox.
- Main flow: 1. Lane E, the exploration lane of the `execution` stage, works only on the exploration part. It does not touch the confirmation part and does not use a validation source. 2. The stage records each search procedure and its noise threshold in the tried ledger. The threshold rises as the number of procedures grows. 3. Each candidate enters the inbox (MSG-46). 4. The user chooses. A candidate never goes straight into the plan. 5. A confirmed candidate gets a confirmation tier. Only confirmatory results and the tiers `replicated` and `reserve` write an evidence e-value to the claim ledger.
- Alternative and exception flows: the user rejects the candidate; it stays in the ledger.
- Postconditions: a candidate is never a claim.
- Business rules: BR-51, BR-52, BR-53.
- FR traced: FR-57 to FR-59, FR-206 to FR-209.

#### UC-25 Run the paper stage
- Goal: the stage writes a PaperPack that the writing team can use without re-deriving numbers.
- Actors: Researcher; Persona (paper).
- Preconditions: an accepted EvidenceBundle.
- Trigger: the `execution` stage is accepted.
- Main flow: 1. The stage builds ten checked items from the EvidenceBundle, AnalysisPlan and Lock, Literature Base, DatasetSnapshot and decision log. 2. The code renders every number from bundle records. 3. Each effect statement maps to a verdict and an interpretation row and stays within the claim ceiling. 4. Each citation is in the Literature Base, has a resolved digital object identifier (DOI) and a supporting quote. 5. Limitations cover every grade reason, gap, known risk, deviation, negative control result, low power and confounding sensitivity. 6. Author-only fields are "awaiting author". The AI-use statement comes from the decision log. 7. The reporting checklist follows the claim type (STROBE with RECORD for association and causal, TRIPOD for prediction; these are public reporting guidelines for observational studies, routinely collected data and prediction models). The PaperPack has at least three main figures. 8. Writing rules apply in three kinds: H (violation is an error), M (over threshold is an issue), G (part of the reviewer rubric).
- Alternative and exception flows: model text has a digit that is not a reference (MSG-47). A claim exceeds the ceiling (MSG-48). A citation is not in the Literature Base (MSG-49).
- Postconditions: a PaperPack. If it is accepted, the Platform creates Dossier version 1 (UC-35).
- Business rules: BR-56, BR-65 to BR-73.
- FR traced: FR-62 to FR-69, FR-212 to FR-220.

#### UC-26 Decide on submission
- Goal: the Researcher decides whether and where to submit.
- Actors: Researcher.
- Preconditions: an approved Dossier or a PaperPack.
- Trigger: the team considers submission.
- Main flow: 1. The Researcher decides. 2. The system does not submit to any publisher.
- Alternative and exception flows: none.
- Postconditions: submission happens outside the system.
- Business rules: BR-73.
- FR traced: FR-70.

#### UC-27 Run the review loop
- Goal: every object version gets an independent review.
- Actors: Persona (guard); Researcher.
- Preconditions: all contract items of the object are green.
- Trigger: a stage produces an object version.
- Main flow: 1. A reviewer starts with fresh context and does not see the author's trace. Guards run in parallel and do not read each other. 2. Each finding has category, severity (`blocking`, `major`, `minor`), anchor, evidence, failure scenario and fix. Code drops a finding with no anchor or no evidence. 3. Code or a second verifier checks each finding: `confirmed`, `plausible` or `rejected`. 4. Only a `blocking` and `confirmed` finding enters a revision round. Other findings are logged and shown. 5. The loop stops after at most two revision rounds. After a revision, the review covers only the findings that were fixed and the fields that changed. A new `blocking` finding on an unchanged field counts only when its evidence is a newly computed fact.
- Alternative and exception flows: findings remain after two rounds; they become known risks, shown to the user (MSG-50), or the user decides between the two sides. The system rejects an object only when provenance or contract is broken. Evidence that does not resolve is not published.
- Postconditions: a review record exists for the object version.
- Business rules: BR-35 to BR-39, BR-42.
- FR traced: FR-71 to FR-76, FR-221 to FR-227, FR-270, FR-271.

#### UC-28 Invoke a persona on an object
- Goal: the user asks any persona to review any object.
- Actors: Researcher, Project Manager.
- Preconditions: an object exists.
- Trigger: the user selects a persona and an object.
- Main flow: 1. The user selects the persona. 2. The persona reviews the object. 3. The system shows the findings.
- Alternative and exception flows: the persona precision is below the minimum; its findings show a lower severity.
- Postconditions: findings are logged.
- Business rules: BR-40.
- FR traced: FR-78.

#### UC-29 Run the benchmarks
- Goal: the team measures reviewers, guards and patterns on known flaws.
- Actors: Platform Admin.
- Preconditions: benchmark data exists.
- Trigger: the Platform Admin starts a benchmark. A full evaluation round runs on request (Should); the bench capability itself is Must.
- Main flow: 1. The seeded-flaw bench measures the precision of each persona. 2. The bench holds the red-team catalogue in three groups: data, experiment and inference flaws. 3. The bench measures the detection rate of seeded leakage and the block rate of seeded pipeline order violations. 4. Each research pattern has a negative test. 5. The benchmark case catalogue of 60 sample projects supplies the cases that Report V turns into test cases.
- Alternative and exception flows: a persona is below its minimum precision; its finding severity is lowered. A persona is enabled only when it catches what other personas miss.
- Postconditions: precision and rates are reported.
- Business rules: BR-40, BR-97, BR-100, BR-101.
- FR traced: FR-77, FR-134 to FR-138, FR-228, FR-229.

#### UC-30 Release an aggregate from local data
- Goal: an aggregate leaves the data holder while rows stay.
- Actors: Researcher, Project Manager.
- Preconditions: a `local` dataset version and a paired Local Node.
- Trigger: a job on `local` data returns a result.
- Main flow: 1. The result passes the one release gate: small-cell threshold, rounding, differencing check and probe budget (a limit that stops many aggregates from revealing individual rows). 2. The release enters the append-only release log. The Platform copy matches the Local Node log. 3. With disclosure `standard`, the release is automatic within policy. With `strict`, only approved kinds of numbers pass; others create a release review item (MSG-22). 4. The Researcher or Project Manager answers. 5. Models and published objects receive only aggregates and code-computed profiles. An exception from real data returns only error type, column and affected row count.
- Alternative and exception flows: the release gate rejects a query (MSG-20). The probe budget is used up; the system records a gap, the run continues and every rejected query is shown with its reason (MSG-21).
- Postconditions: no rows left the machine.
- Business rules: BR-19, BR-20, BR-21, BR-22, BR-80.
- FR traced: FR-80 to FR-83, FR-86, FR-231 to FR-235, FR-239.

#### UC-31 Handle a Local Node that is offline or revoked
- Goal: the run does not hang when the Local Node is not available.
- Actors: Researcher.
- Preconditions: a job needs `local` data.
- Trigger: the Local Node goes offline, or the Platform revokes it.
- Main flow: 1. If the job blocks work and the Local Node is offline, the run enters `waiting(node_offline)`. 2. Work that does not need the data continues. 3. The user receives one combined notice (MSG-18). 4. If the Local Node is revoked, the system rejects jobs on its `local` data and tells the user why (MSG-19). Published objects stay readable.
- Alternative and exception flows: the Local Node returns; the run returns to `running`.
- Postconditions: the run keeps a defined state.
- Business rules: BR-14, BR-27, BR-81.
- FR traced: FR-85, FR-110, FR-237, FR-238, FR-241, FR-242.

#### UC-32 Warn on and enforce budgets
- Goal: spending stays under the set limits.
- Actors: Project Manager.
- Preconditions: a project budget and a run token budget exist.
- Trigger: usage grows.
- Main flow: 1. Each run has a token budget. When it is used up, the run ends as `ended(with_gaps)` on the best output (MSG-29). 2. The system warns at the thresholds of the monthly project budget (MSG-26). 3. At 100%, the system blocks new runs (MSG-51).
- Alternative and exception flows: a run is running when 100% is reached (UC-33).
- Postconditions: no run exceeds its token budget without ending `with_gaps`.
- Business rules: BR-58, BR-59.
- FR traced: FR-88, FR-89, FR-243, FR-244.

#### UC-33 Decide extra spend
- Goal: the Project Manager decides whether a run may spend more.
- Actors: Project Manager.
- Preconditions: the project reached 100% of the monthly budget during a run.
- Trigger: the system creates a `spending` item.
- Main flow: 1. The run enters `waiting(budget_review)`. The system creates a `must_ask` `spending` item with a response time (SR-04) (MSG-25). 2. The system sends an external notice to the Project Manager and a reminder before the deadline (MSG-27). 3. The Project Manager approves extra spend; the run continues. Or the Project Manager lets the run end with gaps.
- Alternative and exception flows: the deadline passes with no decision; the run ends `ended(with_gaps)` on the best output and lists every red item (MSG-28).
- Postconditions: the run continues or ends with gaps.
- Business rules: BR-28, BR-60, BR-78.
- FR traced: FR-90, FR-91, FR-245 to FR-247.

#### UC-34 Set the spending ceiling and read the ledger
- Goal: no preset spends above the ceiling and cost is traceable.
- Actors: Platform Admin; Project Manager.
- Preconditions: signed in with the needed role.
- Trigger: the Platform Admin sets the ceiling, or a user opens usage.
- Main flow: 1. The Platform Admin sets the spending ceiling (FR-92). 2. Under `autopilot`, only spending below the ceiling is `auto`; spending above it is `must_ask` (FR-149). 3. The system keeps a usage and cost ledger per run and per project.
- Alternative and exception flows: a spend above the ceiling needs a decision (UC-33).
- Postconditions: the ledger is complete.
- Business rules: BR-61.
- FR traced: FR-92, FR-93, FR-248.

#### UC-35 Review and approve a Dossier
- Goal: the team approves the result package before it leaves the project.
- Actors: Reviewer, Project Manager.
- Preconditions: a PaperPack was accepted.
- Trigger: the Platform creates a Dossier version.
- Main flow: 1. The Platform creates Dossier version 1 from the accepted EvidenceBundle and PaperPack versions and checks each hash. The Platform versions, checks hashes and records approvals. It does not judge the science. 2. Reviewers and Project Managers read and comment. 3. Each approval follows the review settings: number of approvals, who may approve, whether self-approval is allowed. 4. With enough approvals for the current version, the Dossier is approved.
- Alternative and exception flows: self-approval is not allowed (MSG-52). The run ended `with_gaps` or `cancelled` before a PaperPack was accepted; no Dossier exists (MSG-53). A new accepted EvidenceBundle or PaperPack version creates a new Dossier version; approvals do not carry over (MSG-54).
- Postconditions: an approval belongs to exactly one Dossier version.
- Business rules: BR-62, BR-63, BR-79.
- FR traced: FR-94 to FR-96, FR-249 to FR-252.

#### UC-36 Export a Dossier
- Goal: the user takes an approved Dossier out of the project.
- Actors: Researcher, Project Manager.
- Preconditions: the Dossier is approved.
- Trigger: the user selects Export.
- Main flow: 1. Export is a pinned action; the system asks the user (MSG-39). 2. The user confirms. 3. The system exports the Dossier. 4. The system writes the audit log with the Dossier version and the format.
- Alternative and exception flows: the Dossier is not approved (MSG-55).
- Postconditions: every export is traceable.
- Business rules: BR-05, BR-64.
- FR traced: FR-97, FR-98, FR-253.

#### UC-37 Comment on an object
- Goal: members discuss the same run.
- Actors: Reviewer, Project Manager, Researcher.
- Preconditions: the user is a project member.
- Trigger: the user opens an object.
- Main flow: 1. The user writes a comment on the object. 2. The system shows it to the members.
- Alternative and exception flows: a user without comment rights (MSG-01).
- Postconditions: the comment is stored with its author.
- Business rules: BR-05, BR-06.
- FR traced: FR-99, FR-254.

#### UC-38 Receive notifications
- Goal: members do not miss work that needs them.
- Actors: any member.
- Preconditions: notification settings exist.
- Trigger: a project event happens.
- Main flow: 1. The system notifies the member by the notification settings. 2. The system sends external notices (mail, push) only for a blocking pinned item and for a `spending` item. Each has a reminder before its deadline (MSG-27, MSG-59). The reminder of a pinned item goes to the Researcher who created the run and to the Project Manager. The reminder of a `spending` item goes to the Project Manager only.
- Alternative and exception flows: the member turned a channel off; the notice stays in the inbox.
- Postconditions: other events do not send external notices.
- Business rules: BR-05, BR-28, BR-104.
- FR traced: FR-100, FR-255, FR-264.

#### UC-39 Manage users, models and keys
- Goal: the Platform Admin configures the system in one place.
- Actors: Platform Admin.
- Preconditions: signed in as Platform Admin.
- Trigger: the Platform Admin opens administration.
- Main flow: 1. The Platform Admin manages users, model profiles per model role (`stage`, `review`, `vision`), keys, engine settings and default budgets. 2. The system seals keys and integration secrets at the Platform. They never appear in a prompt, log or output.
- Alternative and exception flows: a model or credential is missing; runs end `failed_technical` (MSG-30).
- Postconditions: configuration is stored. No secret is visible.
- Business rules: BR-02, BR-23.
- FR traced: FR-101, FR-102, FR-256.

#### UC-40 Build a journal profile (Could, after MVP)
- Goal: the `paper` stage can follow the practice of a chosen journal.
- Actors: Researcher.
- Preconditions: an allowed corpus exists.
- Trigger: the Researcher requests a profile.
- Main flow: 1. The system builds a profile with source, usage rights, uncertainty and version. 2. Each feature traces to a corpus snapshot and a source span. The profile separates observed practice from mandatory publisher rules. 3. The Researcher approves the profile. 4. The `paper` stage refers to the approved version. 5. The profile never changes the content or certainty of a claim.
- Alternative and exception flows: the Researcher does not approve; the `paper` stage does not use the profile.
- Postconditions: a versioned, approved profile.
- Business rules: BR-74.
- FR traced: FR-106 to FR-109, FR-260, FR-261.

#### UC-41 Compare methods (Should, after MVP)
- Goal: the user compares machine-learning methods on the same data.
- Actors: Researcher; Persona (experiment_design, execution).
- Preconditions: a project with a dataset.
- Trigger: the Researcher chooses claim type `method_comparison`.
- Main flow: 1. The system uses patterns G (hyperparameter optimization), H (ensemble and stacking), I (ablation) and J (budget-aware), with baseline policy F. 2. It compares pairs on each fold and seed, runs many seeds and gives all methods the same tuning budget. 3. It uses nested validation when there is tuning. 4. It corrects for multiple comparisons. 5. It keeps negative results in the EvidenceBundle. 6. The AnalysisPlan holds the three evidence families in order. The task family chooses the metric policy and protocol. Patterns G to J apply to this claim type only (FR-194).
- Alternative and exception flows: a rule is not met; the stage item is red.
- Postconditions: negative results stay visible.
- Business rules: BR-82, BR-83, BR-93, BR-96, BR-98, BR-99.
- FR traced: FR-139 to FR-145, FR-194, FR-267 to FR-269.

## 3. Functional requirements

Each row shows the requirement ID from the product requirements, one statement with a single "shall", the rationale, the source business rule, the priority and the verification method (Test, Demonstration, Inspection, Analysis). A requirement that covers several rules is split into one row per rule. The first row keeps the original ID. The other rows follow it and have higher IDs.

### 3.1 FE-01 Account and access (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-01 | The system shall let a user sign in with an email address and no password. | Removes the risk of password management. | BR-01 | Must | Test |
| FR-02 | The system shall check the role of the user on every action and reject an action of a member without the right role. | Role-based access underpins all collaboration. | BR-02 | Must | Test |
| FR-151 | The system shall not reveal the existence of a project to a person who is not a member. | A person outside the project does not learn that the project exists. | BR-02 | Must | Test |
| FR-03 | The system shall let a Platform Admin see the metadata of every project (list, members, usage, run state). | The operator monitors the operation of every project. | BR-06 | Must | Test |
| FR-152 | The system shall not let a Platform Admin open a dataset, an object or a manuscript of a project in which the Platform Admin is not a member. | Operators do not read research content. | BR-06 | Must | Test |
| FR-146 | The system shall let a user sign in with a Google account and shall give the same user when the verified email address matches an account that signs in with email. | The user picks a familiar sign-in method and is not split into two accounts. | BR-103 | Must | Test |

### 3.2 FE-02 Project workspace and members (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-04 | The system shall keep at least one active Project Manager in every project and reject an action that removes the last one. | A project always has an accountable person. | BR-03 | Must | Test |
| FR-05 | The system shall admit a user to a project through an invitation. | Controls who enters a project. | BR-04 | Must | Test |
| FR-153 | The system shall reject an invitation that has expired under the access setting. | An old invitation gives no way into the project. | BR-04 | Must | Test |
| FR-06 | The system shall treat an archived project as read-only. | Keeps the record intact when a project closes. | BR-03 | Must | Test |
| FR-07 | The system shall write every important project change to an append-only audit log. | Changes are traceable. | BR-05 | Must | Test |
| FR-08 | The system shall let a Project Manager set the project settings: monthly budget, review settings, default preset per stage, notifications and the wait deadline of pinned items (SR-08). | Each project sets its own level of control and approval. | BR-24; BR-59; BR-63; BR-104 | Must | Demonstration |
| FR-111 | The system shall let a Project Manager do all research actions of a Researcher in the project (create a run, answer the decision inbox, accept an object, lock a plan, export) besides the management rights. | A Project Manager needs no extra Researcher role to run research. | BR-80; BR-02 | Must | Test |

System rule for FE-02:

| ID | Statement | Rationale | Source |
|---|---|---|---|
| SR-05 | The system shall expire an invitation after a period that a Project Manager sets in the access settings of the project. | Projects differ in how long an invitation stays valid. | FR-153; BR-04 |

### 3.3 FE-03 Data management (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-09 | The system shall create an immutable dataset version with a hash for every upload or import and never overwrite an older version. | Replay needs data that does not change. | BR-16 | Must | Test |
| FR-154 | The system shall let every analysis pin one dataset version. | Replay knows exactly which data was used. | BR-16 | Must | Test |
| FR-10 | The system shall import through a data connection only from a source the user authorized. | Prevents unintended import. | BR-17 | Must | Test |
| FR-155 | The system shall block a data connection to an internal host. | Prevents attacks on the internal network. | BR-17 | Must | Test |
| FR-11 | The system shall not return the credential of a data connection to a user. | Protects credentials. | BR-17 | Must | Test |
| FR-156 | The system shall not write the credential of a data connection to a log. | A log does not expose a credential. | BR-17 | Must | Test |
| FR-12 | The system shall give every dataset version a data location (`platform` or `local`). | Every dataset has a clear place where it is kept. | BR-18; BR-19 | Must | Test |
| FR-157 | The system shall let only the Local Node read `local` data. | `local` data takes no other path. | BR-18; BR-19 | Must | Test |
| FR-158 | The system shall not allow a preview or a download of rows of `local` data. | Rows of `local` data never leave the user's machine. | BR-18; BR-19 | Must | Test |
| FR-112 | The system shall let an upload accept common tabular data formats, including Parquet; SR-01 gives the full list. | The user brings data without converting the format. | BR-102 | Must | Test |

System rules for FE-03:

| ID | Statement | Rationale | Source |
|---|---|---|---|
| SR-01 | The system shall accept an upload in these formats: CSV, TSV, spreadsheet workbook, SPSS (standard and compressed), Stata, Parquet, and a compressed archive that contains one of these data files. | Researchers work in these formats. | FR-112; BR-102 |
| SR-02 | The system shall apply an upload size limit that a Platform Admin sets as a setting. The default is 1 GB per file. | The limit is operational, so the Platform Admin can change it. | FR-112 |
| SR-07 | The system shall reject an upload that contains no readable table, including an archive with no data file. | An empty upload cannot become a dataset version. | FR-09 |

### 3.4 FE-04 Research case and run management (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-13 | The system shall create a run from a research case made of topic, goals, context, constraints, domain and references, with the dataset optional. | Researchers often start from a question without a dataset. | BR-07 | Must | Test |
| FR-14 | The system shall run every run on the `dataset_first` pipeline: `dataset`, `hypothesis`, `experiment_design`, `execution`, `paper`. | One pipeline; no branching by dataset. | BR-08 | Must | Test |
| FR-15 | When the research case has no dataset, the system shall let the `dataset` stage search the project, search public datasets (role `enrichment` or `validation`) or ask the user through the decision inbox. | A run can start with no dataset. | BR-08 | Must | Test |
| FR-159 | The system shall treat the join of public data into private data as a pinned action. | Public data does not enter private data without a decision. | BR-08 | Must | Test |
| FR-16 | The system shall reject a new run when the project already has an active run. | Avoids conflicts over data, Literature Base, budget and inbox. | BR-09 | Must | Test |
| FR-17 | The system shall change a fixed research case only through an amendment with a reason, a version and an event. | The goal does not change silently. | BR-10 | Must | Test |
| FR-160 | The system shall let a stage that already started keep the old case version. | A stage does not change its goal midway. | BR-10 | Must | Test |
| FR-18 | The system shall give every stage boundary exactly one hand-off object with a type, a version and a hash. | Traceability needs a defined object. | BR-11 | Must | Test |
| FR-161 | The system shall keep a hand-off object immutable after acceptance and create a new version when it is edited. | Replay needs a fixed object. | BR-11 | Must | Test |
| FR-19 | The system shall mark as `stale` every downstream object that pins an upstream object when the upstream object gets a new version. | Downstream knows that upstream has changed. | BR-12 | Must | Test |
| FR-162 | The system shall not update a `stale` object by itself and shall let the user choose the update through acceptance. | There are no silent updates. | BR-12 | Must | Test |
| FR-20 | The system shall treat a stage as done when every contract item is green by code check. | Done has a criterion that a machine can check. | BR-13 | Must | Test |
| FR-163 | The system shall treat a red contract item as a task for the agent to fix. | Self-healing is visible. | BR-13 | Must | Test |
| FR-164 | The system shall turn a contract item into a `needs-you` item when the item uses up its budget share. | There is no hidden retry counter; the user sees a stuck item. | BR-13 | Must | Test |
| FR-21 | The system shall keep every run in exactly one run state (`running`; `waiting` with reason `decision`, `node_offline` or `budget_review`; `ended` with result `complete`, `with_gaps`, `failed_technical` or `cancelled`). | The state of a run is defined. | BR-14 | Must | Test |
| FR-165 | The system shall end every run, so that at a limit the stage ends on the best output and lists every red contract item. | A run ends and never hangs. | BR-14 | Must | Test |
| FR-262 | The system shall end a run as `ended(with_gaps)` only when the token budget of the run is used up, a `spending` item passes its deadline or a pinned item passes its wait deadline; a pinned item that waits shall not end the run before its wait deadline. | Waiting for the user does not lose the run; only the cost limit or a response deadline ends it. | BR-14; BR-58; BR-78; BR-104 | Must | Test |
| FR-22 | The system shall let the Project Manager, or the Researcher who created the run, cancel the run from any state except `ended`, so that the run moves to `ended(cancelled)`. | The user leaves a run that is no longer needed. | BR-77 | Must | Test |
| FR-166 | The system shall keep accepted objects when a run is cancelled. | Cancelling a run does not lose accepted results. | BR-77 | Must | Test |
| FR-167 | The system shall close every waiting item of the run when the run is cancelled. | The inbox holds no item of a cancelled run. | BR-77 | Must | Test |
| FR-168 | The system shall write the cancellation of a run to the audit log. | Traces who cancelled the run. | BR-77 | Must | Test |
| FR-23 | The system shall let the AI PI propose a next step after a run from the fixed set (`collect_more_data`, `explore_signal`, `replicate`, `write_paper`, `revise_plan`) and let the user choose. | Guides the next step with a shared vocabulary. | BR-15 | Must | Test |
| FR-24 | The system shall compute every number by code. | A model must not invent numbers. | BR-41 | Must | Test |
| FR-169 | The system shall let model text carry references to records and no numbers. | A number in text always traces to a record. | BR-41 | Must | Test |

### 3.5 FE-05 Human control (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-25 | The system shall give each stage a preset (`co_work`, `milestones` as default, `autopilot`). | Control is tuned per stage. | BR-24 | Must | Test |
| FR-170 | The system shall apply a preset change to future actions and not recompute past decisions. | The history of decisions does not change. | BR-24 | Must | Test |
| FR-171 | The system shall re-evaluate waiting items when the preset changes. | Waiting items follow the new level of control. | BR-24 | Must | Test |
| FR-26 | The system shall assign every action to exactly one action group and one level (`auto`, `do_then_review`, `must_ask`). | Permission follows the kind of action, not a run-wide switch. | BR-25 | Must | Test |
| FR-172 | The system shall not allow an override that lowers the level of an action below the floor. | The floor keeps the minimum level of control. | BR-25 | Must | Test |
| FR-27 | The system shall keep the pinned actions at `must_ask` at every preset: define the outcome and estimand; confirm the unit of observation and data structure before the split; choose hypotheses (two or more) and the primary; join public data into private data; lock the plan; deviate from the locked algorithm; use a validation source; export out of the project. | Only the Researcher owns these decisions. | BR-26 | Must | Test |
| FR-28 | For a `must_ask` item, the system shall ask at once with options, a recommended option and a reason when the user is `present`. | The system asks when the user is there. | BR-27 | Must | Test |
| FR-173 | For a `must_ask` item, the system shall queue the item when the user is `away` and let the agent continue every action that does not depend on it. | Presence changes only how an item waits. | BR-27 | Must | Test |
| FR-29 | The system shall collect the items of all stages in one decision inbox with eight kinds (question, review batch, tentative decision, deviation, candidate, needs-you, release review, spending). | One place to act. | BR-28 | Must | Test |
| FR-174 | The system shall send external notices (mail, push) only for a blocking pinned item and for a `spending` item sent to the Project Manager. | Less notification fatigue, while the spending authority still knows. | BR-28 | Must | Test |
| FR-30 | The system shall record every decision in the decision log (action type, level, policy version, decider, presence, overturned or not). | Decisions are traceable. | BR-29 | Must | Test |
| FR-175 | The system shall compute the overturn rate per action type. | Measures the quality of control. | BR-29 | Must | Test |
| FR-176 | The system shall only propose a higher level from the overturn rate and shall not raise the level itself. | The user keeps the right to change levels. | BR-29 | Must | Test |
| FR-31 | The system shall let the AI PI decide an unpinned item tentatively only when the preset is `autopilot` and the user is `away`, and create a tentative decision for the user to confirm or overturn. | The AI PI does not decide for the user outside the allowed scope. | BR-30 | Must | Test |
| FR-177 | The system shall undo the dependent work and mark the affected objects `stale` when the user overturns a tentative decision. | The user can always correct a tentative decision. | BR-30 | Must | Test |
| FR-32 | The system shall not let the AI PI end a run or decide a pinned item; the run waits for the user until the wait deadline of the item (FR-263). | Pinned decisions belong to the user. | BR-31; BR-104 | Must | Test |
| FR-178 | When only pinned items wait, the system shall end the stage at `ready_to_<action>` and keep the run in `waiting(decision)`; the waiting item shall not end the run before its wait deadline (FR-263). | A pinned item waits for the user and does not end the run before its deadline. | BR-31; BR-104 | Must | Test |
| FR-33 | The system shall pass a user action in the interface through the same tools, guards and checks as an agent action. | There is no shortcut for the user or the agent. | BR-32 | Must | Test |
| FR-179 | The system shall record in the decision log who acted. | Tells apart the decisions of the user, the agent and the AI PI. | BR-32 | Must | Test |
| FR-34 | At the `milestones` preset, the system shall set the level of fitness acceptance from the code verdict: `fit` is `auto` (logged), `fit_with_limits` is `do_then_review`, `not_fit` is `must_ask`. | The system asks more when the data fit is poor. | BR-33 | Must | Test |
| FR-35 | The system shall let the AI PI write a lab notebook for the run with the summary, proposals, tentative decisions and reasons. | The user follows the run in readable text. | BR-34 | Must | Demonstration |
| FR-36 | The system shall record in the decision log every assumption of the agent with its alternatives and reason. | An assumption does not become a silent decision. | BR-75 | Must | Test |
| FR-180 | The system shall not treat an assumption of the agent as the intent of the Researcher. | The intent of the Researcher comes only from the Researcher. | BR-75 | Must | Test |
| FR-147 | The system shall set the level of the eight action groups at preset `co_work` as follows: `read_compute` is `auto`; `technical_fix` is `do_then_review`; `content_judgment`, `object_drafting`, `spending`, `acceptance` and `pinned` are `must_ask`; `unseal` is `auto` when every check is green. | At `co_work` the user approves every content decision. | BR-24; BR-25; BR-26; BR-49 | Must | Test |
| FR-148 | The system shall set the level of the eight action groups at preset `milestones` as follows: `read_compute` and `technical_fix` are `auto`; `content_judgment` and `object_drafting` are `do_then_review`; `spending` and `pinned` are `must_ask`; `acceptance` follows the code verdict (FR-34); `unseal` is `auto` when every check is green. | At `milestones` the user approves at the milestones and by the fit of the data. | BR-24; BR-25; BR-26; BR-33; BR-49 | Must | Test |
| FR-149 | The system shall set the level of the eight action groups at preset `autopilot` as follows: `read_compute`, `technical_fix` and `content_judgment` are `auto` (`content_judgment` is logged); `object_drafting` and `acceptance` are `do_then_review`; `spending` is `auto` below the spending ceiling and `must_ask` above it (FR-92); `pinned` is `must_ask`; `unseal` is `auto` when every check is green. | At `autopilot` the agent runs on its own within the floors, the pinned actions and the spending ceiling. | BR-24; BR-25; BR-26; BR-49; BR-61 | Must | Test |
| FR-150 | The system shall set the floor of the action group `object_drafting` to `do_then_review` and the floor of `pinned` to `must_ask`; every other action group has the floor `auto`. | The floor limits how far an override can lower a level. | BR-25; BR-26; BR-33 | Must | Test |
| FR-263 | The system shall give every pinned item a wait deadline for the answer; the wait deadline is a project setting (SR-08), with a default of 7 days. | A pinned item waits for the user and the run does not hang without limit. | BR-104 | Must | Test |
| FR-264 | The system shall send an external notice (mail, push) before the wait deadline to the users who can answer the pinned item: the Researcher who created the run and the Project Manager. | The user learns of the deadline before the run ends. | BR-104; BR-28 | Must | Test |
| FR-265 | The system shall end the run as `ended(with_gaps)` on the best output when the wait deadline of a pinned item passes with no answer, close the item unanswered and list the gap. | The run ends and does not hang, and nobody decides for the user. | BR-104; BR-14 | Must | Test |
| FR-266 | The system shall not let the AI PI or a default value decide a pinned item in place of the user, including after the wait deadline. | A pinned decision comes only from the user. | BR-104; BR-31 | Must | Test |

System rule for FE-05:

| ID | Statement | Rationale | Source |
|---|---|---|---|
| SR-08 | The system shall use a wait deadline for pinned items that a Project Manager sets in the project settings. The default is 7 days, with a reminder 24 hours before the deadline. | The time a project can wait for a user differs between projects. | FR-263; BR-104 |

### 3.6 FE-06 Dataset stage (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-37 | The system shall let the `dataset` stage create a DatasetSnapshot with source, table model, five-dimension quality profile, dictionary, cleaning recipe, question map (question, data requirement, level of fit), split, source roles and fitness. | The hand-off lets later stages work without guessing. | BR-43 | Must | Test |
| FR-38 | The system shall not let the cleaning of the `dataset` stage use the outcome; cleaning that needs the outcome belongs to the AnalysisPlan. | Cleaning must not select results. | BR-43 | Must | Test |
| FR-39 | The system shall let code conclude the fitness of the data for the question (`fit`, `fit_with_limits`, `not_fit`). | The fit conclusion must be checkable. | BR-43; BR-41 | Must | Test |
| FR-40 | The system shall let the `dataset` stage identify the unit of observation and the data structure (group, time, panel). | A correct split and analysis depend on the dependence between rows. | BR-76; BR-26 | Must | Test |
| FR-181 | The system shall let the Researcher confirm the unit of observation and the data structure as a pinned action before the split is created. | The responsible person confirms the structure. | BR-76; BR-26 | Must | Test |
| FR-41 | The system shall not create a split before the Researcher confirms the unit of observation and the data structure. | Prevents leakage between parts. | BR-76; BR-26 | Must | Test |
| FR-182 | The system shall not put rows of one group into two parts of the split. | Rows of one group depend on each other; splitting them causes leakage. | BR-76; BR-26 | Must | Test |
| FR-183 | The system shall split time-ordered data by time. | Prevents using future data to predict the past. | BR-76; BR-26 | Must | Test |
| FR-42 | The system shall choose the split by power: `three_way` when the sample size gives power of at least 0.8 and a reserve remains, `two_way` otherwise, `none` when the sample size is below the minimum, with a limitation. | The split follows the real power of the question. | BR-44 | Must | Test |
| FR-113 | The system shall allow a repeated stratified split for IID data with a classification task family (`binary`, `multiclass`, `rare-event`). | Keeps class proportions stable across parts, mainly when the positive class is rare. The repetition applies only within the exploration part; the confirmation part is used once (BR-86). | BR-84; BR-86 | Must | Test |
| FR-114 | The system shall let the `dataset` stage report each kind of dataset shift apart: covariate shift, label shift and concept drift. | The three kinds need different handling; merging blurs the cause. | BR-85 | Must | Test |
| FR-115 | The system shall let the dictionary record when each variable is available. | The reader knows which variables exist at deployment. | BR-88 | Must | Test |
| FR-184 | The system shall flag as post-outcome a variable recorded after the outcome. | A post-outcome variable causes leakage and is not available at deployment. | BR-88 | Must | Test |
| FR-116 | The system shall let the `dataset` stage check duplicate rows across the parts of the split and report the result. | Duplicate rows give falsely optimistic results. | BR-88 | Must | Test |
| FR-117 | The system shall let the `dataset` stage flag data signals (low positive rate, categorical variables with high cardinality, group or time columns, high missingness). | Signal flags help to pick a pattern that fits the data. | BR-89; BR-26 | Must | Test |
| FR-185 | The system shall let the `dataset` stage suggest research patterns from the signal flags and let the Researcher choose a pattern through the choice of hypotheses (FR-27). | AI suggests and the person decides. | BR-89; BR-26 | Must | Test |
| FR-118 | The system shall let the prefilter of the `dataset` stage use marginal distributions only and not the relation between variables and the outcome. | The suggestion does not reveal results; blind analysis stays intact. | BR-89 | Must | Test |

### 3.7 FE-07 Hypothesis stage and Literature Base (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-43 | The system shall build and update a versioned project-level Literature Base from metadata, abstracts and open-access full text, with search protocol, search log, screening decisions, evidence cards, a code-built evidence map and checked BibTeX. | Shared evidence with provenance for every stage. | BR-41 | Must | Demonstration |
| FR-186 | The system shall log the error per source when a literature source fails, continue with the other sources and record a gap if all sources fail. | One failing source does not stop the review. | BR-41 | Must | Test |
| FR-44 | The system shall let the `hypothesis` stage create a HypothesisSet of at least two hypotheses with different claim keys and one primary. | Avoids locking onto a single hypothesis. | BR-45 | Must | Test |
| FR-45 | The system shall require each hypothesis to have a draft estimand, variables, sourced confounders, SESOI, a refutation statement, a contribution type and an origin. | A hypothesis is testable and refutable. | BR-45 | Must | Test |
| FR-119 | The system shall require each hypothesis to have a comparator, a primary metric that fits the task family, a direction or margin, a scope and a decision rule. | A hypothesis is testable and refutable. | BR-90 | Must | Test |
| FR-120 | The system shall return for repair a hypothesis with no comparator. | A claim such as "the model is better" without a comparator cannot be tested. | BR-90; BR-99 | Must | Test |
| FR-187 | The system shall not accept a deliberately weak baseline. | A weak baseline gives falsely optimistic results. | BR-90; BR-99 | Must | Test |
| FR-121 | The system shall map a non-inferiority or equivalence margin (δ) onto the SESOI regions of the verdict. | Equivalence needs a margin set in advance. | BR-91; BR-54 | Must | Test |
| FR-122 | The system shall not conclude equivalence from a p-value that is not statistically significant. | No evidence of a difference is not evidence of equivalence. | BR-91 | Must | Test |
| FR-123 | The system shall keep a hypothesis portfolio of one primary and secondary hypotheses within the limit set by the project settings (SR-06), with a default of 3 secondary hypotheses. | Limits the number of tests and so the multiple-comparison problem. | BR-92 | Must | Test |

System rule for FE-07:

| ID | Statement | Rationale | Source |
|---|---|---|---|
| SR-06 | The system shall apply a limit on secondary hypotheses that a Project Manager sets in the project settings. The default is 3. | The limit differs between projects. | FR-123; BR-92 |

### 3.8 FE-08 Experiment design stage and Lock (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-46 | The system shall let the `experiment_design` stage create an AnalysisPlan for existing tabular data with estimand, protocol by claim type, adjustment set, analysis program, fallback, decision rule, interpretation table, robustness set, design diagnosis and hypothesis family structure. | The plan is complete enough to run and check without more decisions. | BR-46 | Must | Test |
| FR-47 | The system shall run the analysis program on a twin built from released aggregates before the plan is locked. | Errors are fixed before anyone sees real estimates. | BR-50 | Must | Test |
| FR-48 | The system shall let the Platform write the Lock when the user locks the plan, with the hashes of spec, program and golden outputs, snapshot version, split digest, who locked and when. | The plan is fixed before the confirmatory run. | BR-47; BR-26 | Must | Test |
| FR-188 | The system shall keep a locked object immutable. | A change after the lock is possible only as a deviation. | BR-47; BR-26 | Must | Test |
| FR-49 | The system shall keep the plan waiting for lock while the user is `away`. | Lock is a pinned action. | BR-26; BR-31 | Must | Test |
| FR-189 | The system shall not allow anyone to lock in place of the user. | The decision to lock belongs to the user. | BR-26; BR-31 | Must | Test |
| FR-124 | The system shall record the task family (`binary`, `multiclass`, `regression`, `rare-event`) in the AnalysisPlan. | Metric and protocol fit the kind of problem. | BR-83 | Must | Test |
| FR-190 | The system shall use the task family to choose the metric policy and protocol for `prediction`. For `method_comparison`, see FR-268 (FE-19, after MVP). | Metric and protocol fit the kind of problem. | BR-83 | Must | Test |
| FR-191 | The system shall use the task family to choose the model family for `association` and `causal`. | The model family fits the kind of outcome. | BR-83 | Must | Test |
| FR-125 | The system shall keep a research pattern registry in which each pattern is a versioned unit with applicable task family, eligibility rule, required columns, baseline policy, factor template, metric policy, chart template, statistical plan, failure mode and human actions (reusing the pinned actions of FR-27). | Patterns are reusable and checkable and add no new stop point. | BR-95; BR-26 | Must | Test |
| FR-192 | The system shall have the AnalysisPlan record the chosen research pattern with its version. | The plan traces to the pattern used. | BR-95; BR-26 | Must | Test |
| FR-126 | The system shall let `prediction` use patterns A to E and K to O. | Pattern scope follows the claim type. | BR-96 | Must | Test |
| FR-193 | The system shall let `prediction` use pattern F as baseline policy. For `method_comparison`, see FR-269 (FE-19, after MVP). | `prediction` needs a baseline. | BR-96 | Must | Test |
| FR-127 | The system shall have the AnalysisPlan record the pipeline order: split first; every step that learns from data is fitted on the train part only; resampling on the train part only; calibration and threshold chosen on the validation part; the confirmation part used once. | Prevents leakage from preprocessing. | BR-86 | Must | Test |
| FR-128 | The system shall have the AnalysisPlan of `prediction` hold three evidence families in order: discrimination, reliability (calibration, stress, uncertainty) and decision (threshold, cost, subgroup). For `method_comparison`, see FR-267 (FE-19, after MVP). | One metric is not enough to conclude. | BR-93 | Must | Test |
| FR-129 | The system shall use average precision (AP) or precision at fixed recall as the metric for task family `rare-event`, and not accuracy alone. | Accuracy hides errors on a rare class. | BR-94 | Must | Test |
| FR-130 | The system shall not compare AP between sets with different prevalence. | AP depends on prevalence. | BR-94 | Must | Test |
| FR-131 | The system shall use data apart from the training data for calibration. | Calibration on training data gives falsely optimistic results. | BR-94; BR-86 | Must | Test |
| FR-132 | The system shall apply the baseline policy (pattern F): simple baselines run first, on the same split. | Fair comparison. | BR-99 | Must | Test |
| FR-195 | The system shall use the same tuning budget for the baseline and for the method that is compared. | Different tuning budgets bias the comparison. | BR-99 | Must | Test |
| FR-196 | The system shall report the runtime of the baseline together with its score. | A score alone does not compare cost. | BR-99 | Must | Test |

### 3.9 FE-09 Execution stage (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-50 | The system shall run execution in a sandbox. | The code of the agent does not touch systems outside the sandbox. | BR-50 | Must | Test |
| FR-197 | The system shall let the agent work freely on the twin and touch real data only through aggregates or the full program. | The agent sees no real rows. | BR-50 | Must | Test |
| FR-198 | The system shall let a dry run on real data return only row count, types, missingness, convergence and time, and no estimate. | The agent sees no early estimate. | BR-50 | Must | Test |
| FR-51 | The system shall put confirmatory results in an envelope at the Platform. | Confirmatory results stay out of reach of the agent. | BR-49 | Must | Test |
| FR-199 | The system shall show the agent only done or error before unseal. | Blocks p-hacking. | BR-49 | Must | Test |
| FR-52 | The system shall unseal automatically when all checks are green, unless the user chose manual unseal beforehand. | The default does not block the run; the user can raise the level. | BR-49 | Must | Test |
| FR-53 | The system shall open all hypotheses of one Lock at once at unseal. | Hypotheses are not chosen by their results. | BR-49 | Must | Test |
| FR-200 | The system shall record the unseal time. | Traces when the results were opened. | BR-49 | Must | Test |
| FR-201 | The system shall reject an unseal earlier than the last lane C (confirmatory lane) fix. | Results do not open while lane C is still being fixed. | BR-49 | Must | Test |
| FR-54 | The system shall let code compute the verdict of each hypothesis by the locked decision rule (`supported`, `trivial`, `not_supported`, `insufficient`, `not_tested`). | A model does not create verdicts. | BR-54 | Must | Test |
| FR-202 | The system shall take the conclusion text from the interpretation row that matches the verdict. | The conclusion matches the verdict. | BR-54 | Must | Test |
| FR-55 | The system shall let code compute grade A to D from diagnostics, robustness and deviation. | The level of confidence has a computed source. | BR-55; BR-56 | Must | Test |
| FR-203 | The system shall let the `execution` stage compute the claim ceiling from verdict, grade and confirmation tier. | The allowed claim level has a computed source. | BR-55; BR-56 | Must | Test |
| FR-204 | The system shall not treat a locked plan as a proven claim. | A lock fixes the plan; it does not prove the claim. | BR-55; BR-56 | Must | Test |
| FR-56 | The system shall treat every change of the locked algorithm as a deviation and as a pinned action. | A departure from the plan must be decided by the user. | BR-48; BR-26 | Must | Test |
| FR-205 | The system shall record each deviation in the deviation log and count it in the grade. | A departure from the plan must be visible. | BR-48; BR-26 | Must | Test |
| FR-57 | The system shall keep lane E on the exploration part only and not touch the confirmation part. | Exploration does not damage confirmation. | BR-51 | Must | Test |
| FR-206 | The system shall not use a validation source in lane E. | A validation source is used only when the user decides. | BR-51 | Must | Test |
| FR-207 | The system shall put each candidate of lane E in the decision inbox for the user to choose, and never directly into the plan. | A candidate is never a claim. | BR-51 | Must | Test |
| FR-58 | The system shall record every search procedure of lane E and of the user in the tried ledger with a noise threshold. | The more searching, the higher the threshold. | BR-52 | Must | Test |
| FR-208 | The system shall raise the threshold for later candidates as the number of search procedures grows. | More searching raises the chance of a good-looking result by luck. | BR-52 | Must | Test |
| FR-59 | The system shall give each confirmed candidate a confirmation tier (`replicated`, `reserve`, `unsealed_untouched`, `unsealed_touched`). | The level of confirmation has an order. | BR-53 | Must | Test |
| FR-209 | The system shall write an evidence e-value to the claim ledger only for confirmatory results and for candidates of the tiers `replicated` and `reserve`. | Only rows not used for discovery give a valid evidence e-value. | BR-53 | Must | Test |
| FR-60 | The system shall put a replication package (code hash, environment, data, seed, split) in the EvidenceBundle. | Replay needs all inputs. | BR-57 | Must | Test |
| FR-210 | The system shall let the Replicator reproduce the results of the EvidenceBundle. | Results can be reproduced. | BR-57 | Must | Test |
| FR-211 | The system shall turn a bundle item red when the reproduced results differ. | Detects a difference. | BR-57 | Must | Test |
| FR-61 | The system shall let the `execution` stage create an EvidenceBundle of ten checked items: confirmatory results, verdicts and interpretation rows, grade, diagnostics, robustness, deviation log, tried ledger and candidates, tables and figures, replication package, and Replicator report with envelope log. | The execution hand-off is complete for the `paper` stage. | BR-11; BR-54; BR-55; BR-57 | Must | Test |
| FR-133 | The system shall have the guard of execution block a pipeline order violation (FR-127) before the run, or record the violation as a deviation. | A violation does not enter results silently. | BR-87; BR-86 | Must | Test |

### 3.10 FE-10 Paper stage (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-62 | The system shall let the `paper` stage create a PaperPack of ten checked items (reporting checklist, manuscript, claims, figures and tables, citations, limitations, reproducibility, declarations, review, formats) from the EvidenceBundle, AnalysisPlan and Lock, Literature Base, DatasetSnapshot and decision log. | The writing team gets a complete pack and re-derives nothing. | BR-65 | Must | Test |
| FR-63 | The system shall render every number in the manuscript and on figures from EvidenceBundle records. | No number is written by a model. | BR-66; BR-71 | Must | Test |
| FR-212 | The system shall turn a check red when model text has a digit that is not a reference (except years, item numbers and section numbers). | A machine catches a stray digit. | BR-66; BR-71 | Must | Test |
| FR-64 | The system shall map every effect statement in Abstract, Results and Discussion to a verdict and an interpretation row. | The manuscript does not overstate results. | BR-67; BR-56 | Must | Test |
| FR-213 | The system shall keep the claim-level words matching the verdict. | Claim-level words are not stronger than the verdict. | BR-67; BR-56 | Must | Test |
| FR-214 | The system shall not let a claim exceed the claim ceiling. | The claim ceiling is the upper limit of the manuscript. | BR-67; BR-56 | Must | Test |
| FR-65 | The system shall ensure that every citation is in the Literature Base. | No invented citation. | BR-68 | Must | Test |
| FR-215 | The system shall ensure that every citation has a resolved DOI. | A citation exists in fact. | BR-68 | Must | Test |
| FR-216 | The system shall ensure that every citation has a supporting quote for the claim it supports. | No mismatched citation. | BR-68 | Must | Test |
| FR-66 | The system shall ensure that limitations state every grade reason, gap, known risk, deviation, negative control result, low power and confounding-sensitive result. | No limitation is hidden. | BR-69 | Must | Test |
| FR-217 | The system shall let code check the coverage of the limitations. | A machine can check coverage. | BR-69 | Must | Test |
| FR-67 | The system shall set the author-only fields (authors, affiliation, ethics, funding, conflicts, CRediT) as the placeholder "awaiting author". | The system does not invent author information. | BR-70 | Must | Test |
| FR-218 | The system shall take the AI-use statement from the decision log. | The AI-use statement has a source. | BR-70 | Must | Test |
| FR-68 | The system shall build the reporting checklist by claim type (STROBE with RECORD for association and causal; TRIPOD for prediction). | Reporting follows the standard of the claim type. | BR-71 | Must | Test |
| FR-219 | The system shall point each item of the reporting checklist to an anchor in the paper or mark it "awaiting author" or "not applicable" with a reason. | Each checklist item can be checked. | BR-71 | Must | Test |
| FR-220 | The system shall give the PaperPack at least three main figures. | The manuscript has main figures as evidence. | BR-71 | Must | Test |
| FR-69 | The system shall apply writing rules of three kinds: H (a violation is an error), M (over a threshold is an issue) and G (part of the reviewer rubric). The content of each rule is not yet defined (Open item 2). | Style is checkable. | BR-72 | Must | Inspection |
| FR-70 | The system shall leave the decision to submit to the Researcher and shall not submit to a publisher by itself. | The decision to submit belongs to a person. | BR-73 | Must | Inspection |

### 3.11 FE-11 Independent review loop and personas (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-71 | The system shall run the review loop at every stage, once per object version, after all checks are green. | Independent review is mandatory. | BR-35 | Must | Test |
| FR-72 | The system shall run a reviewer with fresh context that does not see the author's trace. | A reviewer does not share the author's bias. | BR-36 | Must | Test |
| FR-221 | The system shall run guards in parallel and not let a guard read another guard. | Guards are independent of each other. | BR-36 | Must | Test |
| FR-73 | The system shall require each finding to have a category, a severity (`blocking`, `major`, `minor`), an anchor, evidence, a failure scenario and a fix. | A finding is checkable and fixable. | BR-37 | Must | Test |
| FR-222 | The system shall drop a finding that has no anchor or no evidence. | A finding that cannot be checked does not enter a revision round. | BR-37 | Must | Test |
| FR-74 | The system shall check each finding by code or a second verifier (`confirmed`, `plausible`, `rejected`) before fixing. | No fixes follow a false finding. | BR-38 | Must | Test |
| FR-223 | The system shall let only a `blocking` and `confirmed` finding enter a revision round. | A revision round handles only certain errors. | BR-38 | Must | Test |
| FR-224 | The system shall record and show the findings that do not enter a revision round. | Other findings are not hidden. | BR-38 | Must | Test |
| FR-75 | The system shall limit the loop to at most two revision rounds. | Review does not run forever. | BR-39 | Must | Test |
| FR-225 | The system shall show a finding that remains after two revision rounds as a known risk, or let the user decide between the two sides. | The unresolved part is visible. | BR-39 | Must | Test |
| FR-270 | The system shall accept a new `blocking` finding on an unchanged field after a revision only when the evidence of the finding is a newly computed fact. | A revision round does not grow through findings with no new evidence. | BR-39; BR-37 | Must | Test |
| FR-271 | The system shall review again after each revision only the findings that were fixed and the fields that changed. | Repeated review has a narrow scope and a revision does not reopen the whole object. | BR-39 | Must | Test |
| FR-76 | The system shall reject an object only when provenance or contract is broken. | Traceable without demanding perfection. | BR-42 | Must | Test |
| FR-226 | The system shall retry other content problems and then keep them as a finding or a known risk. | A content problem does not block the run. | BR-42 | Must | Test |
| FR-227 | The system shall not publish evidence that does not resolve. | There is no evidence that cannot be traced. | BR-42 | Must | Test |
| FR-77 | The system shall measure the precision of each reviewer persona on the seeded-flaw bench. | Each persona has a measurable value. | BR-40 | Must | Analysis |
| FR-228 | The system shall lower the severity of the findings of a reviewer whose precision is below the minimum. | A weak reviewer does not block progress. | BR-40 | Must | Test |
| FR-229 | The system shall enable a persona only when the bench shows it catches what other personas miss. | No persona is added without value. | BR-40 | Must | Analysis |
| FR-78 | The system shall let the user invoke any persona on any object. | The user checks on demand. | BR-40 | Must | Test |
| FR-134 | The system shall provide a negative test for each research pattern: a case with a seeded flaw that the pattern must detect. | Measures the detection power of each pattern. | BR-97 | Must | Test |
| FR-135 | The system shall include the red-team catalogue in the seeded-flaw bench with three groups of seeded flaws: data (post-outcome column, duplicates across split parts, wrong positive labels, temporal leakage, target encoding fitted on all data, proxy of a protected attribute), experiment (resampling before the split, unequal tuning budget, feature selection on the test part, early stopping on the test part, missing seed, selection of good runs) and inference (equivalence from p above 0.05, causal claim from feature attribution, AP compared across prevalences, no uncertainty reported). | Measures reviewers and guards on named scientific flaws. | BR-100; BR-40 | Must | Analysis |
| FR-136 | The system shall measure the detection rate of seeded leakage (SM-17) on the seeded-flaw bench. | Missed leakage invalidates every later conclusion. | BR-100 | Must | Analysis |
| FR-137 | The system shall measure the block rate of seeded pipeline order violations before the run (SM-18) on the seeded-flaw bench. | A guard must block named flaws. | BR-100 | Must | Analysis |
| FR-138 | The system shall keep a benchmark case catalogue of 60 sample projects, each a test case of a research pattern, from which Report V derives test cases. | Test cases have a source; there are no 60 separate flows. | BR-101 | Must | Inspection |

### 3.12 FE-12 Local Node (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-79 | The system shall provide a Local Node that keeps `local` data and runs jobs next to it. | Sensitive data stays on the data holder's machine. | BR-18 | Must | Demonstration |
| FR-230 | The system shall not require the user to install Docker to use the Local Node. | The user needs no infrastructure knowledge. | BR-18 | Must | Demonstration |
| FR-80 | The system shall not let rows of data leave the data holder. | Rows of private data do not leave. | BR-19 | Must | Test |
| FR-231 | The system shall let only aggregates (releases) leave, through one release gate made of a small-cell threshold, rounding, a differencing check and a probe budget. | One single privacy checkpoint. | BR-19 | Must | Test |
| FR-81 | The system shall record every release of a dataset version in an append-only release log. | The IT of the organization can check every number that left. | BR-20 | Must | Test |
| FR-232 | The system shall keep the Platform copy matching the release log of the Local Node. | Both sides hold the same release history. | BR-20 | Must | Test |
| FR-82 | The system shall release automatically within policy at disclosure `standard`. | The data owner chooses the strictness. | BR-21; BR-80 | Must | Test |
| FR-233 | The system shall, at disclosure `strict`, pass only approved kinds of numbers and create a release review item in the decision inbox for other kinds. | The data owner keeps control of new kinds of numbers. | BR-21; BR-80 | Must | Test |
| FR-234 | The system shall let the Researcher or Project Manager of the project answer a release review item. | A clear person answers. | BR-21; BR-80 | Must | Test |
| FR-83 | The system shall not send rows of data to a model or a published artifact; a model receives only aggregates and code-computed profiles. | A model receives no private data. | BR-22 | Must | Test |
| FR-235 | The system shall return only the error type, the column and the number of affected rows for an exception from real data. | An error message does not expose rows of data. | BR-22 | Must | Test |
| FR-84 | The system shall let the Local Node check the hash of a dataset version and reject a job when the hash does not match. | A job runs only on pinned data. | BR-16; BR-18 | Must | Test |
| FR-236 | The system shall propose a new version when the hash does not match. | The user knows the next step. | BR-16; BR-18 | Must | Test |
| FR-85 | When a local job blocks work and the Local Node is offline, the system shall put the run in `waiting(node_offline)`. | A run does not hang because the user's machine is off. | BR-14; BR-27 | Must | Test |
| FR-237 | The system shall continue work that does not need the data while the run is in `waiting(node_offline)`. | Waiting for the Node does not stop other work. | BR-14; BR-27 | Must | Test |
| FR-238 | The system shall send one combined notice when the run enters `waiting(node_offline)`. | Avoids repeated notices. | BR-14; BR-27 | Must | Test |
| FR-86 | The system shall treat an exhausted probe budget of a dataset version as a gap and not as a stop of the run. | Limits inference from many aggregates and the run still ends. | BR-19; BR-14 | Must | Test |
| FR-239 | The system shall show every rejected query with its reason. | The user knows why a number is missing. | BR-19; BR-14 | Must | Test |
| FR-87 | The system shall let the user pair a Local Node with a project by a pairing code. | The user needs no manual setup. | BR-18 | Must | Demonstration |
| FR-240 | The system shall propose datasets from the folder the Local Node watches. | The user does not declare each dataset. | BR-18 | Must | Demonstration |
| FR-110 | When a Local Node is revoked, the system shall reject jobs on the `local` data of that Node. | A revoked Node runs no jobs. | BR-81 | Must | Test |
| FR-241 | The system shall tell the user the reason when it rejects a job because the Node is revoked. | The user knows the cause. | BR-81 | Must | Test |
| FR-242 | The system shall keep published objects readable when a Local Node is revoked. | Old results are not lost. | BR-81 | Must | Test |

### 3.13 FE-13 Budget and cost (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-88 | The system shall give each run a token budget in tokens. | Run cost has a ceiling. | BR-58 | Must | Test |
| FR-243 | The system shall end the run as `ended(with_gaps)` on the best output when the token budget of the run is used up. | The run does not hang. | BR-58 | Must | Test |
| FR-89 | The system shall warn at the thresholds of the monthly project budget (SR-03). | Project cost has a ceiling. | BR-59 | Must | Test |
| FR-244 | The system shall block new runs when the monthly budget of the project reaches 100%. | No spending above the ceiling without a decision. | BR-59 | Must | Test |
| FR-90 | When a project reaches 100% of the monthly budget, the system shall move the running run to `waiting(budget_review)` and create a `must_ask` `spending` item. | The authorized person decides extra spend and no work is lost. | BR-60 | Must | Test |
| FR-245 | The system shall let the Project Manager approve extra spend so that the run continues, or let the run end with gaps. | The Project Manager decides spending. | BR-60 | Must | Test |
| FR-91 | The system shall give a `spending` item a response deadline (SR-04). | A run does not hang waiting for spend. | BR-78; BR-28 | Must | Test |
| FR-246 | The system shall send an external notice (mail, push) to the Project Manager when a `spending` item is created and a reminder before the deadline. | The Project Manager knows an item waits. | BR-78; BR-28 | Must | Test |
| FR-247 | The system shall end the run `with_gaps` when the deadline passes with no decision. | The run ends and does not hang. | BR-78; BR-28 | Must | Test |
| FR-92 | The system shall block `auto` spending above the spending ceiling set by the Platform Admin, in every preset. | No preset goes above the ceiling. | BR-61 | Must | Test |
| FR-248 | The system shall allow `auto` spending only below the ceiling at preset `autopilot`. | Automatic spending has a limit. | BR-61 | Must | Test |
| FR-93 | The system shall keep a usage and cost ledger per run and per project. | Cost is traceable. | BR-61 | Must | Test |

System rules for FE-13:

| ID | Statement | Rationale | Source |
|---|---|---|---|
| SR-03 | The system shall use warning thresholds for the monthly project budget that a Project Manager sets in the project settings. | Teams differ in how early they need a warning. | FR-89; BR-59 |
| SR-04 | The system shall use a response time for `spending` items that a Project Manager sets in the project settings. | The deadline depends on how fast a project can decide. | FR-91; BR-78 |

### 3.14 FE-14 Dossier, approval and export (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-94 | The system shall create a Dossier when a run has an accepted PaperPack (and none when the run ends `with_gaps` or `cancelled` before that), with references to the accepted EvidenceBundle and PaperPack versions. | There is no content copy that can drift. | BR-62 | Must | Test |
| FR-249 | The system shall check each reference of a Dossier by hash. | A Dossier detects a changed reference. | BR-62 | Must | Test |
| FR-250 | The system shall only version, check hashes and record approval, and shall not judge the science. | The Platform does not judge the science. | BR-62 | Must | Test |
| FR-95 | The system shall record the Approval of a Reviewer or Project Manager by the review settings: number of approvals, who may approve and whether self-approval is allowed. | Approval rights are configured per project. | BR-63 | Must | Test |
| FR-96 | The system shall create a new Dossier version when the EvidenceBundle or PaperPack gets a new accepted version. | The Dossier keeps up with the content. | BR-79 | Must | Test |
| FR-251 | The system shall attach each Approval to one Dossier version. | An approval does not move to other content. | BR-79 | Must | Test |
| FR-252 | The system shall require approval again for a new Dossier version. | New content needs an approver. | BR-79 | Must | Test |
| FR-97 | The system shall allow export out of the project only when the Dossier is approved. | Results do not leave the project without an approver. | BR-64 | Must | Test |
| FR-253 | The system shall treat export as a pinned action. | Export always needs a decision of the user. | BR-64 | Must | Test |
| FR-98 | The system shall record every export in the audit log with the Dossier version and the format. | Traces what left the project. | BR-05; BR-64 | Must | Test |

### 3.15 FE-15 Collaboration (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-99 | The system shall let a Reviewer read and comment on every object of the project. | Collaboration around one run. | BR-05; BR-06 | Must | Test |
| FR-254 | The system shall let a Project Manager and a Researcher comment by role. | Collaboration around one run. | BR-05; BR-06 | Must | Test |
| FR-100 | The system shall send notifications to members about project events by the notification settings. | Members do not miss work that needs them. | BR-05; BR-28 | Must | Test |
| FR-255 | The system shall send external notices only for a blocking pinned item and for a `spending` item. | Less notification fatigue. | BR-05; BR-28 | Must | Test |

### 3.16 FE-17 Administration and monitoring (Must)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-101 | The system shall let a Platform Admin manage users, model profiles by model role (`stage`, `review`, `vision`), keys, engine settings and default budgets. | Central configuration at the Platform. | BR-02; BR-23 | Must | Demonstration |
| FR-102 | The system shall seal model keys and integration secrets at the Platform. | Protects secrets. | BR-23 | Must | Test |
| FR-256 | The system shall keep model keys and integration secrets out of prompts, logs and outputs. | A secret does not leak through an output. | BR-23 | Must | Test |
| FR-103 | When a model or credential is missing, the system shall end the run `ended(failed_technical)` with a clear error. | The user knows what to configure. | BR-14 | Must | Test |
| FR-257 | The system shall create no fake output when a model or credential is missing. | No sample result passes as real. | BR-14 | Must | Test |
| FR-104 | The system shall let a Platform Admin view the system audit log. | Operation and investigation. | BR-05 | Must | Demonstration |
| FR-258 | The system shall let a Platform Admin view the health of the components. | Operation detects a fault. | BR-05 | Must | Demonstration |
| FR-105 | The system shall report for each run the number of questions, the blocked time and the overturn rate per action type. | Measures the quality of control. | BR-29; BR-40 | Must | Analysis |
| FR-259 | The system shall report the precision of personas on the seeded-flaw bench. | Measures the quality of review. | BR-29; BR-40 | Must | Analysis |

### 3.17 FE-18 Journal Fingerprint Extraction (Could, after MVP)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-106 | The system shall build a journal profile from a corpus that may be used, with source, usage rights, uncertainty and version. | The profile rests on evidence. | BR-74 | Could | Test |
| FR-107 | The system shall trace each feature of a journal profile to a corpus snapshot and a source span. | Separates impression from evidence. | BR-74 | Could | Test |
| FR-260 | The system shall separate observed practice from mandatory publisher rules in a journal profile. | The Researcher knows which items are rules. | BR-74 | Could | Test |
| FR-108 | The system shall let the Researcher approve a journal profile. | The Researcher is responsible for the journal choice. | BR-74 | Could | Test |
| FR-261 | The system shall let the `paper` stage refer to the approved version of a journal profile. | The `paper` stage does not use a profile that is not approved. | BR-74 | Could | Test |
| FR-109 | The system shall ensure that a journal profile does not change the content or the certainty of a claim. | Style does not change conclusions. | BR-74 | Could | Inspection |

### 3.18 FE-19 Method comparison research (Should, after MVP)

| ID | Statement | Rationale | Source | Priority | Verification |
|---|---|---|---|---|---|
| FR-139 | The system shall support claim type `method_comparison`, the comparison of machine-learning methods on the same data, with pattern G (hyperparameter optimization), H (ensemble and stacking), I (ablation) and J (budget-aware) and baseline policy F. | Extends from phenomenon research to method comparison. | BR-82; BR-96 | Should | Test |
| FR-140 | The system shall compare in pairs on each fold and seed in `method_comparison`. | Paired comparison removes the variance between folds. | BR-98 | Should | Test |
| FR-141 | The system shall run many seeds in `method_comparison`. | One seed does not measure stability. | BR-98 | Should | Test |
| FR-142 | The system shall use the same tuning budget for every method in `method_comparison`. | Fair comparison. | BR-98; BR-99 | Should | Test |
| FR-143 | The system shall use nested validation when `method_comparison` includes tuning. | Tuning on the evaluation part gives falsely optimistic results. | BR-98 | Should | Test |
| FR-144 | The system shall correct for multiple comparisons in `method_comparison`. | Many comparisons raise false positives. | BR-98 | Should | Test |
| FR-145 | The system shall keep negative results of `method_comparison` in the EvidenceBundle. | A failed method is not hidden. | BR-98 | Should | Test |
| FR-194 | The system shall let only `method_comparison` use patterns G to J. | Patterns G to J belong to the method comparison claim type. | BR-96 | Should | Test |
| FR-267 | The system shall have the AnalysisPlan of `method_comparison` hold three evidence families in order: discrimination, reliability (calibration, stress, uncertainty) and decision (threshold, cost, subgroup). | One metric is not enough to conclude. | BR-93 | Should | Test |
| FR-268 | The system shall use the task family to choose the metric policy and protocol for `method_comparison`. | Metric and protocol fit the kind of problem. | BR-83 | Should | Test |
| FR-269 | The system shall let `method_comparison` use pattern F as baseline policy. | `method_comparison` needs a baseline. | BR-96 | Should | Test |

### 3.19 System rules summary

| SR | Subject | Source |
|---|---|---|
| SR-01 | Supported upload formats | FR-112 |
| SR-02 | Upload size limit as a setting | FR-112 |
| SR-03 | Budget warning thresholds as a project setting | FR-89 |
| SR-04 | Response time for spending items as a project setting | FR-91 |
| SR-05 | Invitation expiry as an access setting | FR-153 |
| SR-06 | Limit of secondary hypotheses as a project setting | FR-123 |
| SR-07 | Rejection of an upload with no readable table | FR-09 |
| SR-08 | Wait deadline of pinned items as a project setting | FR-263 |

## 4. Non-functional requirements

### 4.1 External interfaces

| Category | Purpose | Direction | Constraint | Source |
|---|---|---|---|---|
| User interface | Web app for all users | Two-way | English only (NFR-19); keyboard use for the decision inbox and result tables (NFR-18) | FE-01 to FE-17 |
| Identity | Email sign-in and Google account sign-in | Two-way | No password is stored (FR-01); a Google account and an email sign-in with the same verified email address give the same user (FR-146) | FR-01, FR-146 |
| Model providers | Models by role (`stage`, `review`, `vision`) through the model provider | Prompts out, text and tool calls back | No rows of `local` data in any prompt; keys sealed at the Platform; secrets filtered | FR-83, FR-102 |
| Scholarly metadata | Search, metadata, abstracts and open-access full text for the Literature Base | Queries out, metadata back | No full text behind paywalls; a failing source is logged and skipped | FR-43 |
| Public datasets | Search and read public datasets for roles `enrichment` and `validation` | Queries out, public files back | Joining into private data is a pinned action | FR-15 |
| Data connections | Spreadsheet and cloud-drive sources that the user authorized | Data in | Authorized sources only; internal hosts blocked; credentials never returned or logged | FR-10, FR-11 |
| Notification | Email and push notices | Out | Only for a blocking pinned item and a `spending` item | FR-29, FR-100 |
| Local Node | Desktop application on the user's machine; pairing, jobs, releases | Two-way | No Docker needed; only aggregates leave through the release gate; releases logged | FR-79 to FR-87, FR-110 |

### 4.2 Quality attributes

Measurements marked "pre-release test environment" are made before the release.

| ID | Category | Requirement | Measurable criterion and method | Source |
|---|---|---|---|---|
| NFR-01 | Performance | The system shall return the run list and the decision inbox for a project with up to 100 runs. | p95 under 2 seconds. Load test in a pre-release test environment. | none |
| NFR-02 | Performance | The system shall stream trace events from an engine to the web app. | p95 under 5 seconds from event to display. Test with a shared clock. | ADR-02 |
| NFR-03 | Reliability | Every run that is not in `waiting` shall reach `ended`; no run hangs. | 100% of runs that are not in `waiting` reach `ended`; 0 runs in `waiting` with no waiting item and no Local Node offline; 0 runs in `waiting(decision)` past the wait deadline of a pinned item. Review of run states per project. | SM-01; QS-09; QS-15 |
| NFR-04 | Reliability | When the model provider or an external source fails, the system shall report a clear error, create no fake output and keep published objects readable. | 0 fake outputs in a test that cuts the model provider; 100% of published objects readable after the failure. Fault-injection test. | ADR-11; R-12 |
| NFR-05 | Reliability | The system shall keep spending within the set ceilings. | 0 runs over the token budget that did not end `with_gaps`; 0 runs at 100% of the monthly budget with no `spending` item. Check of the usage ledger and the decision inbox. | SM-11; QS-10 |
| NFR-06 | Availability | The Platform shall be available. | At least 99% of the minutes of each calendar month have a passing health check. The measure covers the whole calendar month. Health monitoring. | BO-08 |
| NFR-07 | Reliability | An accepted object shall stay readable and keep its hash after a restart. | 100% of accepted objects keep their hash after a restart. Restart test. | BR-11 |
| NFR-08 | Security | The system shall check role and project on every request and isolate data between projects. | 0 paths that read data, runs, Literature Base, inbox or audit log of another project. Two-project test. | BR-02; ADR-03 |
| NFR-09 | Security | Keys and secrets shall not appear outside the Platform. | 0 keys or secrets in prompts, logs, traces and outputs. Test with a planted fake key. | BR-23 |
| NFR-10 | Security | The agent shall not see a confirmatory estimate before unseal. | 0 confirmatory estimates in trace and workspace before unseal; 100% of unseal requests earlier than the last lane C fix rejected. Check of the envelope log and unseal log. | SM-07; QS-02; QS-03 |
| NFR-11 | Security | The system shall record every administrative and security action in an append-only audit log. | 100% of actions recorded; 0 edits or deletions of records. Test. | BR-05 |
| NFR-12 | Privacy | No row of `local` data shall leave the Local Node. | 0 rows of `local` data in any message that leaves the Local Node. Packet capture in the Local Node acceptance scenario. | SM-05; QS-06 |
| NFR-13 | Privacy | The release log of the Local Node shall match the Platform copy. | 100% match. Log comparison in the acceptance scenario. | SM-06; QS-06 |
| NFR-14 | Privacy | The release gate shall reject a query that reveals a difference under the small-cell threshold. | 100% of such queries rejected and shown with the reason. Test with two queries that differ by fewer rows than the threshold. | QS-07 |
| NFR-15 | Usability | A new user shall create a valid first run. | At least 5 of 5 users succeed in a test with 5 people. Usability test. | BO-01 |
| NFR-16 | Usability | The interface shall let users tell the source of information: AI proposal, code computation, reviewer finding, Researcher approval, AI PI decision. | At least 9 of 10 random items given the right source by users. Usability test. | BR-41; BR-30 |
| NFR-17 | Usability | The interface shall let users understand the five verdict labels. | At least 4 of 5 labels explained correctly with no help. Usability test. | BR-54 |
| NFR-18 | Accessibility | The web app shall meet WCAG 2.1 level AA; the decision inbox and the result tables shall work with a keyboard. | 0 level A and AA failures on the main screens in automatic and manual checks. Accessibility evaluation. | none |
| NFR-19 | Localization | The web app shall use English only. | 100% of system-generated interface strings in English. Automatic check of interface strings. | none |
| NFR-20 | Maintainability | The system shall use one harness for all five engines; engines differ only in their declaration. | 0 guard, check, trace or decision-log mechanisms owned by one engine. Inspection. | ADR-02 |
| NFR-21 | Maintainability | Every hard rule shall exist both in the prompt of the related step and in a code validator. | 0 rules on one side only. Inspection. | PP-07 |
| NFR-22 | Maintainability | Documents shall trace BR, FR, UC and TC. | 100% of FRs trace to a BR; every Must FR has at least one TC. Traceability matrix. | none |
| NFR-23 | Observability | The system shall emit a trace event for every action and every check change and record the decision log with all fields. | 100% of actions and check changes have an event; 100% of decisions have all decision-log fields. Test. | ADR-02; ADR-05 |
| NFR-24 | Observability | The system shall report operating metrics for each run. | Number of questions, blocked time, overturn rate per action type and rate of `needs-you` items reported for 100% of runs. The targets are those of SM-02. | SM-02; R-06 |
| NFR-25 | Replayability | The Replicator shall reproduce the hash of the EvidenceBundle. | 100% of accepted bundles have a replication package whose hash the Replicator reproduces; otherwise the item is red. Replicator report. | SM-08; QS-05 |
| NFR-26 | Replayability | The same pinned objects, the same Lock and the same seed shall give the same hash. | 100% of runs in the test set give the same hash on a re-run. Re-run and hash comparison. | BO-02; ADR-01 |
| NFR-27 | Integrity | A PaperPack shall contain no digit that is not a reference. | 0 digits outside the allowed list (years, item numbers, section numbers) in an accepted PaperPack; 100% of numbers trace to a record. Contract check at each version. | SM-03; QS-01 |
| NFR-28 | Integrity | Every effect statement shall trace to a verdict and stay within the claim ceiling. | 100% of effect statements in Abstract, Results and Discussion map to a verdict and an interpretation row; 0 claims above the ceiling. Claims contract check. | SM-12; QS-04 |
| NFR-29 | Integrity | Every citation shall be in the Literature Base with a resolved DOI. | 100% of citations. Citations contract check. | SM-04 |
| NFR-30 | Integrity | Every accepted object version shall pass the review loop with at most two revision rounds. | 100% of accepted object versions have a review record; no more than 2 revision rounds per version; 100% of remaining findings shown in the PaperPack. Comparison with review records. | SM-10; QS-12 |
| NFR-31 | Integrity | The AI PI shall not decide a pinned item and every tentative decision shall be visible to the user. | 0 AI PI decisions on pinned items; 100% of tentative decisions in the decision inbox when the user returns. Test of `autopilot` with the user `away`. | QS-11; BR-30; BR-31 |

Quality categories that the requirements do not yet cover (backup and retention of research data, capacity planning beyond NFR-01, and privacy handling by the model provider) are listed under Open items.

## 5. Requirement appendix

### 5.1 Business rules

| ID | Rule |
|---|---|
| BR-01 | A user signs in with an email address and no password. |
| BR-02 | Access depends on the system role Platform Admin and the project roles Project Manager, Researcher and Reviewer. A non-member cannot see that a project exists; a member without the role cannot do the action. |
| BR-03 | Every project has at least one active Project Manager. An archived project is read-only. |
| BR-04 | A user joins a project through an invitation; the invitation expires by the access setting. |
| BR-05 | Important changes go to an append-only audit log. Comments and notifications support collaboration. |
| BR-06 | A Reviewer reads and comments on every object. A Platform Admin sees project metadata but not content without membership. |
| BR-07 | Every run starts from a research case. The dataset is optional. |
| BR-08 | The pipeline is always `dataset_first`. With no dataset, the `dataset` stage searches, finds public data or asks the user. Joining public data into private data is pinned. |
| BR-09 | A project has at most one active run. |
| BR-10 | A fixed research case changes only through an amendment with reason, version and event. |
| BR-11 | Each stage boundary has one hand-off object with type, version and hash, immutable after acceptance. |
| BR-12 | A new upstream version makes pinned downstream objects `stale`; nothing updates by itself. |
| BR-13 | Each stage has contract items with code checks; the stage is done when all are green; a red item is a task for the agent and later a `needs-you` item. |
| BR-14 | A run always ends: `complete`, `with_gaps`, `failed_technical` or `cancelled`. At a limit, the stage ends on the best output and lists every red contract item. `with_gaps` has three causes only: the token budget of the run is used up (BR-58), a `spending` item passes its deadline (BR-78), or a pinned item passes its wait deadline (BR-104). |
| BR-15 | After a run the AI PI proposes a next step from a fixed set and the user chooses. |
| BR-16 | A dataset version is immutable and has a hash; every analysis pins a version. |
| BR-17 | A data connection imports only from authorized sources; credentials are never returned or logged; internal hosts are blocked. |
| BR-18 | Each dataset version has a data location `platform` or `local`; only the Local Node reads `local` data. |
| BR-19 | Rows never leave the data holder; aggregates leave through one release gate. |
| BR-20 | Every release goes to an append-only release log. |
| BR-21 | Disclosure `standard` releases within policy; `strict` passes approved kinds and creates release review items. |
| BR-22 | Models and published artifacts receive no rows, only aggregates and code-computed profiles. |
| BR-23 | Model keys and integration secrets are sealed at the Platform. |
| BR-24 | Each stage has a preset: `co_work`, `milestones` or `autopilot`. |
| BR-25 | Each action has one action group and one level; an override cannot go below the floor. |
| BR-26 | Pinned actions are `must_ask` at every preset. |
| BR-27 | Presence changes only how `must_ask` items wait. |
| BR-28 | One decision inbox with eight item kinds; external notices only for a blocking pinned item and `spending`; both have a reminder before the deadline (BR-78, BR-104). |
| BR-29 | The decision log records every decision; the system proposes but never applies a higher level. |
| BR-30 | The AI PI decides only unpinned items, only under `autopilot` and `away`, as tentative decisions. |
| BR-31 | The AI PI never ends a run and never decides a pinned item. A pinned item that waits keeps the run in `waiting(decision)` until its wait deadline (BR-104). |
| BR-32 | User actions use the same tools, guards and checks as agent actions. |
| BR-33 | At `milestones`, the level of fitness acceptance follows the code verdict. |
| BR-34 | The AI PI writes a lab notebook for the run. |
| BR-35 | The review loop is mandatory at every stage, once per object version. |
| BR-36 | A reviewer has fresh context; guards run in parallel and do not read each other. |
| BR-37 | A finding has category, severity, anchor, evidence, failure scenario and fix. |
| BR-38 | A finding is verified before a fix; only `blocking` and `confirmed` findings enter a revision round. |
| BR-39 | At most two revision rounds; remaining findings are known risks. |
| BR-40 | Reviewer precision is measured on the seeded-flaw bench; the user can invoke any persona. |
| BR-41 | Numbers come from code; model text carries references. |
| BR-42 | Code rejects an object only for broken provenance or contract. |
| BR-43 | The DatasetSnapshot has a fixed set of parts; cleaning that uses the outcome belongs to the plan. |
| BR-44 | The `dataset` stage decides the split from power. |
| BR-45 | A HypothesisSet has at least two hypotheses and one primary, each with required fields. |
| BR-46 | The AnalysisPlan covers analysis of existing tabular data only. |
| BR-47 | The Lock is a separate object written by the Platform; a locked object is immutable. |
| BR-48 | A change of the locked algorithm is a deviation. |
| BR-49 | Confirmatory results go to an envelope; unseal is automatic or manual and opens all hypotheses at once. |
| BR-50 | Execution runs in a sandbox; the agent works on the twin; a dry run returns no estimates. |
| BR-51 | Lane E uses the exploration part only; a candidate is not a claim. |
| BR-52 | The tried ledger records every search procedure and raises the noise threshold. |
| BR-53 | A confirmed candidate has a confirmation tier; only confirmatory results, `replicated` and `reserve` write evidence e-values. |
| BR-54 | Code computes the verdict of each hypothesis. |
| BR-55 | Code computes grade A to D. |
| BR-56 | The `execution` stage computes the claim ceiling; the `paper` stage does not exceed it. |
| BR-57 | The EvidenceBundle has a replication package that the Replicator reproduces. |
| BR-58 | Each run has a token budget; when used up, the run ends `with_gaps`. |
| BR-59 | A project has a monthly budget with warnings; at 100% new runs are blocked. |
| BR-60 | At 100%, a running run waits for a Project Manager decision on a `spending` item. |
| BR-61 | `spending` has a spending ceiling set by the Platform Admin; it is a monetary limit, not a floor. At `autopilot`, spending is `auto` only below the ceiling. Usage and cost are kept in a ledger per run and project. |
| BR-62 | The Dossier references accepted EvidenceBundle and PaperPack versions; the Platform does not judge the science. |
| BR-63 | Approval follows the review settings. |
| BR-64 | Export needs an approved Dossier and is a pinned action. |
| BR-65 | The PaperPack has ten checked items. |
| BR-66 | Every number in the manuscript is a reference rendered by code. |
| BR-67 | Every effect statement maps to a verdict and stays within the claim ceiling. |
| BR-68 | Every citation is in the Literature Base with a resolved DOI and a supporting quote. |
| BR-69 | Limitations state all required reasons; code checks coverage. |
| BR-70 | Author-only fields are "awaiting author". |
| BR-71 | The reporting checklist follows the claim type; at least three main figures. |
| BR-72 | Writing rules are of kind H, M or G. |
| BR-73 | The Researcher decides to submit; the system does not submit. |
| BR-74 | (Could) A journal profile is evidence-based, approved by the Researcher and never changes a claim. |
| BR-75 | An agent assumption is logged with alternatives and reason and is not Researcher intent. |
| BR-76 | The `dataset` stage identifies unit of observation and structure; the Researcher confirms before the split; the split respects the structure. |
| BR-77 | A Project Manager or the creating Researcher can cancel a run from any state except `ended`. |
| BR-78 | A `spending` item has a deadline, a reminder and a default outcome of `with_gaps`. |
| BR-79 | A new accepted bundle or pack creates a new Dossier version that needs new approval. |
| BR-80 | A Project Manager has all Researcher research rights. |
| BR-81 | When a Local Node is revoked, its `local` jobs are rejected and published objects stay readable. |
| BR-82 | Claim types are `association`, `causal`, `prediction` and `method_comparison` (Should). |
| BR-83 | Task families are `binary`, `multiclass`, `regression` and `rare-event`. |
| BR-84 | Data structures are IID (independent and identically distributed rows), group, time and panel; IID may use a repeated stratified split. |
| BR-85 | Dataset shift has three kinds, each reported apart. |
| BR-86 | The pipeline order prevents leakage. |
| BR-87 | A pipeline order violation is blocked before the run or recorded as a deviation. |
| BR-88 | The dictionary records availability time; post-outcome variables are flagged; duplicates across parts are checked. |
| BR-89 | The `dataset` stage flags data signals from marginal distributions and suggests patterns. |
| BR-90 | A hypothesis is testable: comparator, metric, direction or margin, scope and decision rule. |
| BR-91 | Equivalence margins map to SESOI regions; no equivalence from a non-significant p-value. |
| BR-92 | The hypothesis portfolio has one primary and a limited number of secondary hypotheses. |
| BR-93 | `prediction` and `method_comparison` (when FE-19 exists, after MVP) use three evidence families in order. |
| BR-94 | `rare-event` uses AP or precision at fixed recall; calibration uses separate data. |
| BR-95 | A research pattern is a versioned unit with defined parts. |
| BR-96 | Patterns A to E and K to O serve `prediction`; F is the baseline policy; G to J serve `method_comparison` (when FE-19 exists, after MVP). |
| BR-97 | Each research pattern has a negative test. |
| BR-98 | `method_comparison` (when FE-19 exists, after MVP) needs paired comparison, many seeds, equal tuning budget, nested validation, multiplicity correction and kept negative results. |
| BR-99 | The baseline policy: simple baselines first, same split, same tuning budget, runtime reported. |
| BR-100 | The seeded-flaw bench holds a red-team catalogue of seeded flaws in three groups. |
| BR-101 | The benchmark case catalogue has 60 sample projects. |
| BR-102 | Upload accepts common tabular formats, including Parquet. |
| BR-103 | A user signs in with an email address and no password, or with a Google account. Both methods map to the same user by the verified email address. |
| BR-104 | Every pinned item has a wait deadline, a project setting. The system sends a reminder before the deadline to the users who can answer it. If the item is unanswered at the deadline, the run ends `ended(with_gaps)`, the item closes unanswered and the gap is listed. Nobody decides in place of the user: not the AI PI and not a default value. Before the deadline, a waiting pinned item does not end the run. |

### 5.2 Common requirements

| ID | Requirement |
|---|---|
| CR-01 | The system shall page every long list. |
| CR-02 | The system shall store times in a single standard time and show them in the time zone of the user. |
| CR-03 | The system shall accept a change only from a signed-in user with a valid session and shall protect every change against forged requests. |
| CR-04 | The system shall treat a non-member as having no knowledge of the project and shall refuse a member without the role (MSG-02, MSG-01). |
| CR-05 | The system shall give every error a message from the catalogue in 5.3 and shall show no technical detail to the user. |
| CR-06 | The system shall use the glossary term for each concept in every screen and message. |

### 5.3 Application messages

Types: error, warning, info, confirmation. A value filled in at run time is shown as "…".

| ID | Type | User-facing text | When shown | UC |
|---|---|---|---|---|
| MSG-01 | Error | You do not have the role required for this action. | A member does an action without the right role. | All |
| MSG-02 | Error | We could not find what you asked for. | A non-member opens a project resource. | All |
| MSG-03 | Error | This sign-in request has expired. Request a new one. | The sign-in request is expired. | UC-01 |
| MSG-04 | Info | Check your email to finish signing in. | After the user enters an email address. | UC-01 |
| MSG-05 | Error | This invitation has expired. Ask a Project Manager for a new one. | An expired invitation is used. | UC-03 |
| MSG-06 | Error | A project must keep at least one active Project Manager. | An action would remove the last one. | UC-03 |
| MSG-07 | Error | This project is archived and is read-only. | A change in an archived project. | UC-03 |
| MSG-08 | Error | A run is already active in this project. Wait for it to end or cancel it. | A second run is requested. | UC-09 |
| MSG-09 | Error | This file format is not supported. Upload a tabular data file in a supported format. | Upload of an unsupported format. | UC-06 |
| MSG-10 | Error | This file is larger than the upload limit of …. | Upload over the size limit. | UC-06 |
| MSG-11 | Error | This file contains no readable table. | The file or archive has no readable table. | UC-06 |
| MSG-12 | Info | A new dataset version was created. | After an upload or an import. | UC-06, UC-07 |
| MSG-13 | Error | The data connection could not be used. Check that you authorized access to this source. | Access to the source is not authorized. | UC-07 |
| MSG-14 | Error | This address is not allowed as a data source. | The source is an internal host. | UC-07 |
| MSG-15 | Info | Rows of local data cannot be previewed or downloaded. | A preview or download of `local` data is requested. | UC-06, UC-08 |
| MSG-16 | Error | The data no longer matches the recorded version. Create a new dataset version. | The hash check fails at the Local Node. | UC-08 |
| MSG-17 | Confirmation | The Local Node is paired with this project. | After pairing. | UC-08 |
| MSG-18 | Warning | The Local Node is offline. Work that needs local data is waiting. Other work continues. | The run enters `waiting(node_offline)`. | UC-31 |
| MSG-19 | Error | This Local Node was revoked. Jobs on its local data are rejected. Published objects stay readable. | A job targets a revoked Local Node. | UC-31 |
| MSG-20 | Warning | The release gate rejected this query: …. | A query fails the small-cell, rounding or differencing check. | UC-30 |
| MSG-21 | Info | The probe budget for this dataset version is used up. The run continues and records a gap. | The probe budget is exhausted. | UC-30 |
| MSG-22 | Info | Release review needed: approve or reject the release of …. | In `strict` disclosure, a number of an unapproved kind is about to leave. | UC-30 |
| MSG-23 | Confirmation | Confirm the unit of observation and the data structure before the split is created. | The `dataset` stage needs this pinned decision. | UC-16, UC-18 |
| MSG-24 | Info | The run is waiting for your decision. | A `must_ask` item blocks work. | UC-16 |
| MSG-25 | Warning | The project reached 100% of its monthly budget during a run. A Project Manager must approve extra spend or let the run end with gaps. | The monthly budget reaches 100% while a run is active. | UC-33 |
| MSG-26 | Warning | The project has used … of its monthly budget. | A warning threshold is passed. | UC-32 |
| MSG-27 | Warning | A spending decision is due by …. If nobody decides, the run ends with gaps. | A reminder before the deadline of a `spending` item. | UC-33 |
| MSG-28 | Info | The spending decision expired. The run ended with gaps. | The deadline passes with no decision. | UC-33 |
| MSG-29 | Info | The run ended with gaps. The best output is published and the open items are listed. | A limit ends a stage or a run. | UC-12, UC-32 |
| MSG-30 | Error | The run ended with a technical failure: a model or credential is missing. | A model or credential is missing. | UC-12, UC-39 |
| MSG-31 | Warning | A literature source is unavailable. The error was logged and the stage continues with the other sources. | One literature source fails. | UC-12, UC-19 |
| MSG-32 | Confirmation | Cancel this run? Accepted objects stay and waiting items close. | The user selects Cancel run. | UC-13 |
| MSG-33 | Info | The run was cancelled. | After cancellation. | UC-13 |
| MSG-34 | Warning | This object is stale: an upstream object has a newer version. Accept the update to continue. | An upstream object gets a new version. | UC-11, UC-17 |
| MSG-35 | Confirmation | Accept this object version for use by the next stage? | An object version is ready for acceptance. | UC-11 |
| MSG-36 | Warning | A contract item used up its budget and needs you. | An item becomes `needs-you`. | UC-12 |
| MSG-37 | Confirmation | Lock this plan? A locked plan cannot change. A later change is a deviation. | The user locks the plan. | UC-16, UC-21 |
| MSG-38 | Info | The plan is waiting for your lock. Nobody can lock it for you. | The plan is ready and the user is `away`. | UC-21 |
| MSG-39 | Confirmation | This action is pinned and needs your decision: …. | A deviation, an export or another pinned action. | UC-16, UC-22, UC-36 |
| MSG-40 | Error | This hypothesis has no comparator or uses a deliberately weak baseline. Add a fair comparator. | A hypothesis fails the testability rule. | UC-19 |
| MSG-41 | Error | The results cannot be unsealed yet. Unseal must come after the last confirmatory fix. | An early unseal is requested. | UC-22 |
| MSG-42 | Info | The AI PI made … tentative decisions while you were away. Confirm or overturn each one. | The user returns after an `autopilot` period. | UC-17 |
| MSG-43 | Confirmation | Overturning this decision undoes dependent work and marks … objects stale. Continue? | The user overturns a decision. | UC-17 |
| MSG-44 | Error | This decision is pinned. Only a Researcher or the Project Manager can decide it. | The AI PI would decide a pinned item. | UC-17 |
| MSG-45 | Info | The results were unsealed at …. | After unseal. | UC-22 |
| MSG-46 | Info | A candidate needs your choice. A candidate is not a claim. | Lane E proposes a candidate. | UC-24 |
| MSG-47 | Warning | The text contains a number that is not a reference. Replace it with a reference. | A paper check finds a stray digit. | UC-25 |
| MSG-48 | Warning | A claim is stronger than the claim ceiling allows. Weaken the claim. | An effect statement exceeds the ceiling. | UC-25 |
| MSG-49 | Warning | A citation is not in the Literature Base or its DOI does not resolve. | A citation check fails. | UC-25 |
| MSG-50 | Warning | The review ended with open findings. They are shown as known risks. | Findings remain after two revision rounds. | UC-27 |
| MSG-51 | Error | New runs are blocked because the monthly budget is reached. | A run is started at 100% of the budget. | UC-09, UC-32 |
| MSG-52 | Error | Self-approval is not allowed by the review settings of this project. | A user approves own work where it is not allowed. | UC-35 |
| MSG-53 | Info | There is no Dossier: the run ended before a PaperPack was accepted. | The user looks for a Dossier of such a run. | UC-35 |
| MSG-54 | Info | A new Dossier version was created. It needs approval again. | A new accepted bundle or pack version exists. | UC-35 |
| MSG-55 | Error | Export needs an approved Dossier. | Export is requested before approval. | UC-36 |
| MSG-56 | Error | The Google sign-in did not complete. Try again or sign in with your email address. | The Google sign-in fails or the user cancels it. | UC-01 |
| MSG-57 | Error | The email address of this Google account is not verified. Verify it or sign in with your email address. | The Google account has no verified email address. | UC-01 |
| MSG-58 | Error | A model service is unavailable. No output was created. | The model provider fails. | UC-12 |
| MSG-59 | Warning | A pinned decision is due by …. If nobody answers, the run ends with gaps. | A reminder before the wait deadline of a pinned item. | UC-16, UC-38 |
| MSG-60 | Info | The pinned decision expired unanswered. The run ended with gaps. | The wait deadline of a pinned item passes with no answer. | UC-12, UC-16 |
| MSG-61 | Error | This step breaks the pipeline order: split first, and fit every learning step on the train part only. | A step of the AnalysisPlan breaks the pipeline order. | UC-20 |

## 6. Open items

1. Closed. The targets of SM-02 apply to the runs at the `milestones` preset in one month: a median of at most 15 questions per run, a median blocked time of at most 24 hours per run, and an overturn rate of at most 10% per action type. When a value is above its threshold, the team reviews the level of that action type.
2. The content of each writing rule of kinds H, M and G is not defined (FR-69, BR-72).
3. Closed. The seeded-leakage detection rate is at least 90% (SM-17). The pipeline order block rate is 100% (SM-18), because the guard applies a fixed rule.
4. Closed. The default limit of secondary hypotheses (SR-06) is 3.
5. The default upload size limit (SR-02) is 1 GB per file. The values of the budget warning thresholds (SR-03), the spending response time (SR-04) and the invitation validity (SR-05) are not defined in the requirements. They are settings. The default wait deadline of pinned items (SR-08) is 7 days.
6. Benchmark case BC-C07 is in the first wave but its pattern G belongs to FE-19 (Should, after MVP). The choice between keeping it as Should and replacing it is open.
7. Benchmark cases BC-I17 (anomaly detection) and BC-R19 (multi-output regression) use tasks outside the four task families (BR-83). The decision to keep or remove them is open.
8. The sources define no requirement for backup and retention of research data, capacity planning beyond NFR-01, or the handling of data by the model provider. These are not specified here.
9. The sources do not define screens. The screen flow of the web app is not specified in this section.
10. The logical data model (entities and relationships) is not part of this section; it belongs to the design description.
11. The sign-in method after the email step (link or code) is not specified; MSG-03 and MSG-04 use neutral wording.
12. Closed. The availability measure (NFR-06) covers the whole calendar month. It is not narrowed to working hours.

# IV. Software Design Document

This section describes the design of OpenAI-Scientist at the conceptual level. It follows the IEEE 1016-2009 approach: each part of the design is shown through a viewpoint that answers a defined set of concerns. The viewpoints use the names of the standard. The design is independent of programming language, framework and hosting. Requirement IDs (FE, FR, NFR) come from Report III. Rule IDs (SR), use case IDs (UC) and message IDs (MSG) are defined in Report III and are only referenced here.

| Viewpoint | Concern it answers | Where used |
|---|---|---|
| Context | Who and what is outside the system, and what crosses the boundary | 1.1.1 |
| Composition | Which building blocks exist and what each block owns | 1.1.2, 1.2 |
| Resource | Where the blocks run and where trust boundaries lie (this viewpoint covers the deployment nodes) | 1.1.3, 1.1.4 |
| Logical | How the Platform responsibilities group into modules | 1.2 |
| Information | Which entities exist, who owns them, how they relate | 2 |
| Interaction | How actors and blocks exchange work in time order | 3 |
| State dynamics | Which states a run or an object can take and which events change them | 3.4, 3.5, 3.8, 3.11 to 3.14 |

The design rationale (section 1.3) is the design rationale element of the SDD. It is not a viewpoint.

## 1. System Design

### 1.1 System Architecture

#### 1.1.1 Context viewpoint

The system helps a Researcher move from a research question and tabular data to an evidence package that is ready for a paper. The system does the computing and drafting. The Researcher keeps the decisions that only a person can make (the pinned actions, FR-27). The system promises that no defect is hidden, every claim has a source, and every run can be replayed. It does not promise that the science is correct. The promises map to five quality goals: integrity, traceability, replayability, data privacy, and human control with progress (see section 4).

*Figure IV-1: System context: diagram to be regenerated from the design model.*

The context diagram shows the people who use the system on one side, the system in the middle, and the external services on the other side. The people reach the Platform through the web app. The Platform calls the stage engines and the AI PI. The stage engines call the model service, the literature sources, the public dataset sources and the Local Node.

| Actor | Role in the context | Related FE |
|---|---|---|
| Platform Admin | Operates the system. Manages users, models, keys, engine settings, default budget, audit log and health. Does not read project content unless the person is a project member. | FE-17, FE-01 |
| Project Manager | Manages members, settings, budget, datasets and runs. Also holds every research right of a Researcher. | FE-02, FE-13, FE-14 |
| Researcher | Creates research cases, starts runs, answers the decision inbox, accepts hand-off objects. | FE-04, FE-05 |
| Reviewer | Reads and comments on every object of the project. Approves the Dossier according to the review settings. | FE-14, FE-15 |
| AI Principal Investigator (AI PI) | A system actor. Summarizes, proposes the next step and writes the lab notebook. Decides tentatively on non-pinned items only when the preset is `autopilot` and the user is `away`. Never ends a run and never decides a pinned item. | FE-05 |
| Paper team | Receives the PaperPack without rebuilding the numbers. Works outside the system. | FE-10 |
| IT of the data-holding organization | Needs proof that data rows stay on the machine and can inspect every release. | FE-12 |

| External system | Purpose | Data direction |
|---|---|---|
| Model service | Supplies models for three model roles: `stage`, `review` and `vision`. | Prompts go out. Text comes back. No `local` data rows are sent. |
| Literature sources | Search for papers; return metadata, abstracts and open-access full text. | Queries go out. Metadata comes back. |
| Public dataset sources | Find and read public datasets; header peek. | Queries go out. Headers and public files come back. |
| Email | Notifies users about blocking pinned items and `spending` items. | Outbound. |
| Google sign-in | Lets users sign in. | Both directions. |
| Cloud spreadsheet and file service | Data connections that the user authorizes. An import creates a dataset version. | Data comes in. |

The scope of the system is the web app, the Platform, the stage engines, the AI PI, the Local Node and the shared libraries. The external systems in the second table are outside the scope.

Design constraints (from the requirements and the architecture):

- The system handles tabular data only. Image data, text corpora and signals are out of scope. The `experiment_design` stage plans the analysis of existing tabular data. It does not design new data collection. A full systematic review and the reading of paywalled full text are also out of scope.
- The pipeline is always `dataset_first`, and each project has at most one active run (FR-14, FR-16; ADR-13, ADR-14).
- The web app holds no scientific logic. It talks to the Platform through a defined interface.
- The team is small and the project period is fixed. The design therefore uses one harness for all engines (ADR-02, NFR-20).

#### 1.1.2 Composition viewpoint

*Figure IV-2: Building blocks (level 1): diagram to be regenerated from the design model.*

The diagram shows the web app in front of the Platform. The Platform connects to five stage engines (`dataset`, `hypothesis`, `experiment_design`, `execution`, `paper`) and to the AI PI. Every engine runs on the same Harness. The execution engine can send analysis jobs to the Local Node, which sits next to the user's local data. Four shared libraries support the blocks: contract, analysis, tables and discovery.

| Building block | Responsibility | Does not do |
|---|---|---|
| Web app | Shows the workspace, the decision inbox and the live trace. Receives the actions of users. | Holds no scientific logic. Does not call an engine directly. |
| Platform | Owns users, projects, members, runs, run state, budget, keys, audit log, presence, the combined decision inbox, the cross-stage decision log, Lock, envelope, unseal, Dossier, approval and notifications. | Does not judge scientific content (ADR-03). |
| Stage engine (five: `dataset`, `hypothesis`, `experiment_design`, `execution`, `paper`) | Runs one stage on the Harness according to its HarnessSpec. Produces the hand-off object of the stage. | Does not store people, projects or keys. Does not read envelope results before unseal. |
| Harness | Common runtime of all engines (see the table below). | Knows nothing about the science of a stage. |
| AI PI | Connector persona that summarizes, proposes the next step, writes the lab notebook, and decides tentatively when the preset is `autopilot` and the user is `away`. | Does not end a run. Does not decide pinned items. |
| Executor | Runs analysis jobs. It runs in one of two places: inside the engine (cloud) or on the Local Node. Both places use the same analysis library. | Does not create a separate path for data. |
| Local Node | Holds `local` data. Runs jobs next to the data. Applies the release gate. Keeps the release log. Has a desktop application. | Sends no data rows. Needs no container software on the user machine. |
| Contract library | Defines hand-off objects, action types and the job protocol. | |
| Analysis library | Holds the statistics registry, the research pattern registry, the firewall, the disclosure rules, the sandbox and the job executor. | |
| Tables library | Holds the table model, profile, split and cleaning recipe. | |
| Discovery library | Finds public datasets and performs the header peek. | Does not download restricted data automatically. |

Platform, engine and Local Node have three different trust roles:

| Concern | Platform | Stage engine (Harness) | Local Node |
|---|---|---|---|
| People, projects, keys, budget | Owns | Receives the policy and the keys per role with each request | Not involved |
| Scientific work | Never judges | Does the work and produces hand-off objects | Runs analysis jobs only on registered code |
| Confirmatory results | Owns Lock and envelope; opens the envelope | Requests Lock and unseal; sees only "done" or "error" before unseal | Sends results of `local` data only as aggregates |
| Data rows | Holds rows of `platform` data | Sees only a synthetic table (the twin) and aggregates | Holds rows of `local` data; rows never leave |
| Decision inbox | Merges items of all stages; returns answers to the engine | Emits items; asks at once when the user is `present` | Emits release review items for `strict` disclosure |

Harness internals:

| Component | Responsibility |
|---|---|
| Agent loop | Reads the contract status, chooses the next action, calls one tool, observes the result. |
| Action pipeline | Every action of an agent or a user passes through: guard, level, execute or queue, recompute checks, trace event, decision log (FR-33). |
| Workspace | Holds versioned objects, the decision log and progress notes. It lasts per engine and project, not per run. |
| Live trace | Every action and every check change is one event. Events stream to the web app (NFR-02, NFR-23). |
| Budget and exit | Limits tokens, time and job count. When the run budget ends, the run ends with `ended(with_gaps)`. |
| Contract and hand-off | When every contract item is green, or the run ends with gaps, the engine publishes one version of the hand-off object. Acceptance follows the permission table. |
| Built-ins | Workspace tools; tools to ask the user, record a gap, record an assumption and run a job; literature pack; discovery pack; guards (data firewall, numbers only from tools, locked objects are immutable, secret filter); shared checks (schema, reference resolution, source mark per attribute); independent review; a hook for the seeded-flaw bench. |

Split of work between engine and Platform inside the action pipeline:

| Task | Engine (Harness) | Platform |
|---|---|---|
| Level of an action | Computes the level for each action | Stores the policy (preset per stage, overrides) and sends it with the run request |
| Presence | Reads it from the request and from forwarded events | Detects it (UI activity, "away until") and forwards changes |
| Guard, check, trace, decision log | Runs them and emits events | Stores events and builds the cross-stage decision log |
| Decision inbox | Emits items; asks at once when the user is `present` | Merges the items of all stages into one inbox; forwards answers to the engine |
| Contract status | Computes and emits it per item | Displays it |
| Lock, envelope, unseal | Requests them | Owns and enforces them |

#### 1.1.3 Resource viewpoint (deployment nodes)

*Figure IV-3: Conceptual deployment nodes: diagram to be regenerated from the design model.*

| Node | Contains | Notes |
|---|---|---|
| User browser | Web app | Holds no long-term secret. |
| Platform | Platform, database, object storage | Holds people, projects, runs, keys, audit log, Lock, envelope, Dossier and the files of `platform` datasets. |
| Engine workers | Five stage engines; Executor (cloud) | Run on the Harness. Hold no `local` data. |
| AI PI service | The persona service | Receives summaries only, never data rows. |
| Model service | Models by role | External. Receives no `local` data rows. |
| Local Node (user machine) | Background service, desktop application, sandbox, release gate, release log | Holds `local` data. Can run without a user interface for IT staff. |

#### 1.1.4 Trust boundaries and security design

| Boundary | Between | Rule |
|---|---|---|
| TB1 | Browser and Platform | The Platform authenticates the user and checks project rights on every request (NFR-08). |
| TB2 | Platform and engine | The engine receives keys by role and the policy with the request. The engine has no path to the envelope. |
| TB3 | Engine and model service | Only text and schemas cross. No `local` data rows cross. A secret filter runs on outputs. |
| TB4 | Platform or engine and Local Node | The Node emits only aggregates, through the release gate. Data rows never leave the machine (FR-80, NFR-12). |
| TB5 | Agent code and real data | The agent sees only the twin. Real data is reached through probes and jobs. An error firewall reduces errors to a fixed form. |

| Topic | Design rule |
|---|---|
| Authentication | The user signs in with an email address, without a password (FR-01), or with a Google account (FR-146). Both ways map to the same user when the verified email is the same. |
| Authorization | Rights follow the role in the project. Every request is checked (FR-02, NFR-08). The Platform Admin sees project metadata only: list, members, usage and run state (FR-03). |
| Project isolation | Data, runs, Literature Base, inbox and audit log of one project are not readable from another project (NFR-08). |
| Secrets | A key travels with a request by role. The secret filter blocks keys in outputs and traces. Keys never enter objects (FR-102, NFR-09). |
| Data firewall | The agent never sees real data rows. Only aggregates pass, through the release gate (FR-80, FR-83). |
| Envelope | Confirmatory results pass only through the Platform code path. The agent has no path to them (FR-51, NFR-10; ADR-08). |
| Public data join | Joining public data into private data is a pinned action (FR-15, FR-27). |
| Audit log | Every administrative and security action goes into an append-only audit log (FR-07, NFR-11). |
| Threat model | The Platform and the models are trusted not to need data rows, and they never receive them. The Node runs only Platform code in a sandbox. The remaining risk is inference from many aggregates. The design handles it with a small-cell threshold, rounding, a differencing check, a probe budget and noise on exploratory probes (R-02). |

### 1.2 Logical Structure

The logical structure groups the Platform responsibilities into modules. A module owns a set of entities from section 2 and exposes its function to the web app and to the engines. The grouping is conceptual. It does not name code packages.

*Figure IV-4: Logical modules of the Platform and the web app: diagram to be regenerated from the design model.*

| Module | Responsibility | Main entities | FE |
|---|---|---|---|
| Identity and access | Sign-in, session, role check, project isolation | User, Membership | FE-01 |
| Projects and members | Projects, members, invitations, project settings, review settings | Project, Membership, ProjectSettings | FE-02 |
| Data management | Datasets, immutable versions, data connections, data location | Dataset, DatasetVersion, DataConnection | FE-03 |
| Run management | Research case, run, stage runs, run state, stale marking, cancel, next step | ResearchCase, Run, StageRun | FE-04 |
| Human control | Preset and level policy, presence, decision inbox, decision log, overturn rate | DecisionInboxItem, DecisionLogEntry | FE-05 |
| Stage engines | Stage work on the Harness and the hand-off objects | DatasetSnapshot, HypothesisSet, AnalysisPlan, EvidenceBundle, PaperPack, LiteratureBase, ResearchPattern | FE-06 to FE-10; FE-19 (Should, after MVP) |
| Review | Independent review loop, findings, personas | Finding | FE-11 |
| Lock and envelope | Records the Lock, holds the envelope, checks and performs unseal | Lock, Envelope | FE-08, FE-09 |
| Local data release | Local Node jobs, release gate, release log | ReleaseLog, Release | FE-12 |
| Budget | Run token budget, monthly project budget, thresholds, ledger | BudgetLedger | FE-13 |
| Results governance | Dossier versions, hash checks, approval, export | Dossier, Approval | FE-14 |
| Collaboration | Comments and notifications | Comment, Notification | FE-15 |
| Administration and monitoring | Users, model profiles, keys, engine settings, audit log, health, operating metrics | ModelProfile, AuditLogEntry | FE-17 |
| Journal profile (Could, after MVP) | Journal Fingerprint Extraction | Journal profile | FE-18 |

The web app shows the state of these modules and sends the actions of users to them.

### 1.3 Design Rationale

Each decision below has the status Accepted.

| ADR | Decision | Main alternative | Consequence |
|---|---|---|---|
| ADR-01 | The pipeline has five stages. Each boundary has one typed, versioned, hashed hand-off object that is immutable after acceptance. A new upstream version makes downstream objects `stale`. | A free workflow decided by the agent | Each boundary has a testable contract. Tracing and replay are simple. A change of object structure needs a new contract version. |
| ADR-02 | All engines run on one Harness. Engines differ only in their HarnessSpec. | A separate mechanism per engine | Guard, check, trace and decision log live in one place. A change to the Harness affects all five engines and must be tested for all five. |
| ADR-03 | The Platform owns people, projects, runs, budget, keys, audit log, Lock, envelope and Dossier. It does not judge science. | Each engine manages its own rights and budget | The boundary is clear and engines can be replaced. The Platform becomes a trust point and needs strict isolation and audit. |
| ADR-04 | Human control is set per action type: eight action groups, three levels, presets per stage, presence, floors and pinned actions. | One run-wide switch, or fixed stops per stage | The user tunes control per kind of work. A permission table must be designed and tested. Decisions can be measured by overturn. |
| ADR-05 | One decision inbox serves all stages. It tracks overturn. External notices go only to blocking pinned items and `spending` items. | Fixed stops per stage, or one notice per decision | The user has one place to work. The Platform must merge items from all engines. The overturn rate becomes an operating metric. |
| ADR-06 | Independent review is mandatory. Findings are verified. At most two revision rounds. | Author self-review, optional review, or unlimited revision | Model cost rises for each object. Defects that pass the checks can still be caught. The loop is bounded, so the run still ends. |
| ADR-07 | All numbers, verdicts, grades, claim ceilings and fitness come from code. Model text carries references only. | The model writes numbers and the system checks later | Integrity has a machine check. Prompts must state the rule. All number display passes a code renderer. Text is less natural. |
| ADR-08 | The Platform enforces Lock, envelope and unseal through a code path. Results are not encrypted. | Trust the agent not to look, or encrypt results | Access control by code path suffices for this threat. The Platform is a trust point. The design does not stop a person who can change Platform code. |
| ADR-09 | The `dataset` stage decides the split by power. Confirmation tiers rank candidates. An e-value is recorded only on fresh rows. | A fixed random three-way split | The split fits the real power of the question. The `dataset` stage needs draft hypotheses early. |
| ADR-10 | The Local Node keeps `local` rows on the machine. One release gate controls every release. Every release enters an append-only log. No container software is needed. | Upload everything to the Platform, or use a container sandbox on the user machine | Data privacy has one check point. A twin is built from aggregates and the dry run catches drift. The isolation level differs by operating system and is declared. |
| ADR-11 | Self-healing uses one budget per run and a fixed share per item. A run ends with gaps when the budget ends. | A retry counter per mechanism, a multi-step repair scheme, or a stop that waits for the user | Runs always end and nothing is hidden. The item share must be tuned: a wrong value moves items to needs-you too early or too late. |
| ADR-12 | The Dossier holds references to accepted EvidenceBundle and PaperPack versions. Approval follows the review settings. Export needs approval. | The Platform builds the content, or no approval step | There is no content copy that can drift. Approval is tied to one version. A new version needs a new approval. |
| ADR-13 | Each project has at most one active run. | Several concurrent runs per project | State, budget and inbox stay simple. Throughput in one project is limited. A second project covers parallel needs. |
| ADR-14 | A dataset is optional at the start. The pipeline is always `dataset_first`. | A required dataset, or a pipeline that changes with the dataset | One pipeline only. The `dataset` stage serves both entry points: question first and table first. |
| ADR-15 | The monthly project budget has thresholds. At 100% the Platform blocks new runs and moves active runs to `waiting(budget_review)`. | An immediate hard stop, warnings only, or an automatic pause | The person with spending authority decides. The run keeps its work. The right person must be notified when a `spending` item appears. |
| ADR-17 | A research pattern registry with versions, plus a pipeline order that prevents leakage. Each pattern has a negative test. | One workflow per dataset, or let the agent choose the order and let the reviewer catch errors | A new pattern does not change the Harness. The registry needs upkeep. The order guard must be tested for every pattern. |
| ADR-18 | Add the claim type `method_comparison` (Should, after MVP) on the same Harness, Lock, envelope and verdict, with patterns G to J. | No method comparison, or a dedicated engine, or inclusion in the MVP | The scope grows. No new mechanism is needed for Lock, envelope or verdict. The scope risk is R-14. |

## 2. Data Design

This section gives the logical data model. It lists entities, not storage structures. Each entity has a plain-words description, key attributes in plain words, relationships with cardinality, and an owner. A cardinality reads as "one of this entity relates to how many of the other". The notation `0..N` means zero or more. The notation `0..1` means zero or one.

*Figure IV-5: Logical data model (entity-relationship, crow's foot): diagram to be regenerated from the design model.*

Owners are the Platform, a stage engine, or the Local Node. The model does not state a count of entities. It does not state keys, types or column names.

### 2.1 Entities

#### 2.1.1 Identity and project

| Entity | Description | Key attributes | Relationships | Owner |
|---|---|---|---|---|
| User | A person with an account. | Name, email, status | 1 User to N Membership | Platform |
| Project | The shared workspace of a team. | Name, status, default preset per stage | 1 Project to N Membership; to 1 ProjectSettings; to N Dataset; to N ResearchCase; to N Run (at most 1 active); to 1 LiteratureBase; to N Dossier; to N audit log entry; to 1 BudgetLedger per month | Platform |
| Membership | The link between a user and a project, with a role and an invitation state. | Role (Project Manager, Researcher, Reviewer), date added | N to 1 Project; N to 1 User; 1 to N Approval; 1 to N Comment | Platform |
| ProjectSettings (with ReviewSettings) | The configuration of a project. | Monthly budget, warning thresholds, preset per stage, number of approvals, who may approve, whether self-approval is allowed, export formats, notification choices, limit on secondary hypotheses | 1 to 1 Project | Platform |

#### 2.1.2 Data

| Entity | Description | Key attributes | Relationships | Owner |
|---|---|---|---|---|
| Dataset | A tabular dataset of a project. | Name, data location (`platform` or `local`) | N to 1 Project; 1 to N DatasetVersion; 0..N to 1 DataConnection | Platform |
| DatasetVersion | An immutable version of a dataset. Each upload or import creates a new one. | Content hash, source, time of creation | N to 1 Dataset; 1 to N DatasetSnapshot that pin it; 1 to 1 release log when `local` | Platform for `platform` data; Local Node for `local` data |
| DataConnection | An authorized external source such as a cloud spreadsheet and file service. | Provider, scope of authorization | N to 1 Project; 1 to N Dataset | Platform |
| ResearchCase | The research intent of a run. A change after confirmation is an amendment with reason, version and event (FR-17). | Topic, objective, context, constraints, domain, references, optional dataset | N to 1 Project; 1 to N Run; 0..1 to N DatasetVersion (optional) | Platform |
| LiteratureBase | The versioned literature evidence store of a project. | Search protocol, search log, screening decisions, evidence cards, evidence map, verified bibliography | 1 to 1 Project; 1 to N versions; other stages read by version | Hypothesis engine |

#### 2.1.3 Run and stages

| Entity | Description | Key attributes | Relationships | Owner |
|---|---|---|---|---|
| Run | One execution of the pipeline for a research case. | Run state, waiting reason, ending outcome, token budget, pipeline | N to 1 ResearchCase; 1 to N StageRun; 1 to 0..N Lock; 1 to 0..N Dossier version | Platform |
| StageRun | One execution of one stage in a run. | Stage, preset, presence at start, contract status | N to 1 Run; 1 to 0..N hand-off object versions; 1 to N DecisionInboxItem; 1 to N Finding | Platform |
| DecisionInboxItem | One request for the user. | Kind (question, review batch, tentative decision, deviation, candidate, needs-you, release review, spending), options, proposed option, reason, status, blocking order | N to 1 StageRun; 1 to 0..1 DecisionLogEntry once decided | Platform and Harness |
| DecisionLogEntry | The record of one decision. | Action type, level, policy version, who decided (user, agent, AI PI), presence, whether overturned | N to 1 Run; 0..1 to 1 DecisionInboxItem | Platform and Harness |
| Finding | A result of independent review. | Category, severity, anchor (object and field), evidence, failure scenario, proposed fix, verification result | N to 1 hand-off object version; N to 1 StageRun | Stage engine |

#### 2.1.4 Hand-off objects and research patterns

| Entity | Description | Key attributes | Relationships | Owner |
|---|---|---|---|---|
| DatasetSnapshot | The output of the `dataset` stage. | Source, table model, five-dimension quality profile, dictionary, cleaning recipe, question map, split, source role, fitness | N to 1 DatasetVersion; N to 1 StageRun; 1 to N HypothesisSet that pin it | Dataset engine |
| HypothesisSet | The output of the `hypothesis` stage. | At least two hypotheses with different claim keys; one primary | N to 1 DatasetSnapshot; N to 1 LiteratureBase version; 1 to N AnalysisPlan that pin it | Hypothesis engine |
| AnalysisPlan | The output of the `experiment_design` stage. | Estimand, protocol by claim type, adjustment set, analysis program, fallback, decision rule, interpretation table, robustness set, design diagnosis, hypothesis family structure, task family, pipeline order, evidence family | N to 1 HypothesisSet; N to M ResearchPattern (pinned versions); 1 to 0..1 Lock; 1 to N EvidenceBundle | Experiment design engine |
| ResearchPattern | A versioned unit in the pattern registry. | Applicable task family, eligibility rule, required columns, baseline policy, templates, metric policy, statistical plan, failure modes, human actions (reuse of pinned actions), ordering constraints, negative test | 1 to N versions; N to M AnalysisPlan; 1 to N negative tests | Analysis library; the experiment design engine reads it |
| EvidenceBundle | The output of the `execution` stage, with ten checked items. | Confirmatory result, verdicts, grade, diagnostics, robustness, deviation log, tried ledger and candidates, tables and figures, replication package, Replicator report, envelope log; claim ceiling | N to 1 AnalysisPlan (through the Lock); 1 to N PaperPack; 1 to 0..N Dossier references | Execution engine |
| PaperPack | The output of the `paper` stage. | Manuscript, reporting checklist, claims, figures and tables, citations, limitations, reproducibility, declarations, review result, export formats | N to 1 EvidenceBundle; 1 to 0..N Dossier references | Paper engine |
| Lock | The record of a locked plan. | Hashes of spec, program and golden outputs; snapshot version; split digest; who locked; when | N to 1 Run; 1 to 1 AnalysisPlan version; 1 to 1 Envelope | Platform (written at the request of the experiment design engine) |
| Envelope | The sealed store of confirmatory results. | Sealed results, state (sealed or unsealed), time of unseal | 1 to 1 Lock | Platform |

#### 2.1.5 Local release, results governance and administration

| Entity | Description | Key attributes | Relationships | Owner |
|---|---|---|---|---|
| ReleaseLog and Release | The append-only list of aggregates that left the data holder. | Kind of number, reason, job, time | 1 ReleaseLog to 1 DatasetVersion; 1 to N Release | Local Node or cloud Executor; a copy at the Platform |
| Dossier | A package of references to accepted results, for approval and sharing. | Version, references to EvidenceBundle and PaperPack, hash, approval state | N to 1 Run; 1 to N Approval; 1 to N Comment | Platform |
| Approval | A decision on one Dossier version. | Decision, time, Dossier version | N to 1 Dossier; N to 1 Membership | Platform |
| Comment | A remark on an object of the project. | Text, anchor | N to 1 Membership; N to 1 any object of the project | Platform |
| Notification | A message for a user. | Kind, recipient, status | N to 1 User; 0..1 to 1 DecisionInboxItem | Platform |
| Audit log entry | A record of an administrative or security action. Append-only. | Action, actor, time | N to 1 Project, or system level | Platform |
| BudgetLedger | The record of spending by run and by month. | Spending per run and per month, thresholds already notified | 1 to 1 Project per month; 1 to N spending entries per Run | Platform |
| ModelProfile | The model configuration of a model role. | Model role (`stage`, `review`, `vision`), model, key reference, unit price | Used by StageRun | Platform |

### 2.2 Hand-off Objects: Versioning, Hash and Stale Rules

There are five hand-off objects: DatasetSnapshot, HypothesisSet, AnalysisPlan, EvidenceBundle and PaperPack. Each stage boundary has exactly one (FR-18; ADR-01).

| Rule | Statement |
|---|---|
| Immutability | A hand-off object has a version and a content hash. It is immutable after acceptance. A correction creates a new version. |
| Pinning | An object pins the upstream versions it uses by identity and hash. |
| Dataset versions | A dataset version is immutable. Every analysis pins one dataset version (FR-09). |
| Lock | A Lock is immutable. A change to a locked algorithm is a deviation. A deviation is a pinned action and enters the deviation log (FR-48, FR-56). |
| Stale | A new upstream version marks every downstream object that pins the old version as `stale`. Nothing updates itself. The user updates through an acceptance, and the downstream stage then runs again on the new version (FR-19). |
| Replay | The same pinned objects, the same Lock and the same seed give the same hash. The Replicator compares hashes (NFR-25, NFR-26). |
| Dossier | A Dossier version pins accepted versions. A new accepted version of the bundle or the pack creates a new Dossier version. The old version stays and its approvals do not carry over (FR-96). |

How objects link:

| Object | Linked by |
|---|---|
| DatasetSnapshot | Snapshot identity and hash |
| LiteratureBase | Version identity |
| HypothesisSet | Set identity and claim key |
| AnalysisPlan | Hash of the spec and hash of the program |
| Lock | Hash of the spec and hash of the program |
| Envelope | Lock identity |
| EvidenceBundle | Bundle identity and record identity |
| PaperPack | Pack identity |
| ReleaseLog | Dataset version identity |
| ResearchPattern | Pattern identity and version |
| Decision inbox and decision log | Item identity |

### 2.3 Data Ownership Summary

- The Platform owns Project, Membership, ProjectSettings, Run, StageRun, budget, ModelProfile and keys, audit log, Lock, Envelope, Dossier, Approval, and the combined decision inbox and decision log.
- Each stage engine owns the hand-off object of its stage. The hypothesis engine also owns the LiteratureBase. The execution engine also owns the tried ledger.
- The Local Node owns the rows and the release log of `local` datasets. The Platform keeps a copy of the release log (FR-81).
- The engines do not store people, projects or keys (ADR-03).

## 3. Detailed Design

Each subsection covers one feature group. Where a group has runtime behavior, the subsection gives an interaction viewpoint as numbered steps and a state viewpoint as a table. All figures are placeholders for diagrams that will be regenerated from the design model.

### 3.1 Account and Access (FE-01)

Design concern: sign in without a password and enforce role rights on every operation.

1. The user enters an email address.
2. The Platform sends a sign-in challenge to that address (FR-01).
3. The user completes the challenge. The Platform opens a session. A user can instead sign in with a Google account. When the verified email is the same, the Platform maps both ways to the same user (FR-146).
4. On every later request the Platform checks the role of the user in the project (FR-02).
5. If the user has no role in the project, the Platform rejects the request and does not reveal that the project exists (FR-151).

The Platform Admin sees project metadata only: list, members, usage and run state. The Platform Admin cannot open a dataset, an object or a manuscript unless the person is a member (FR-03; NFR-08). Report III defines the sign-in rules (SR) and the user messages (MSG).

### 3.2 Project Workspace and Members (FE-02)

Design concern: every project has a responsible manager, controlled entry and a trace of changes.

1. A user joins a project through an invitation (FR-05).
2. The Platform rejects an invitation that has expired under the access setting.
3. Every important change to the project writes one entry to the append-only audit log (FR-07).
4. The Platform rejects an operation that would remove the last active Project Manager (FR-04).
5. An archived project is read-only (FR-06).

The Project Manager sets the project settings: monthly budget, review settings, default preset per stage, notification choices and the wait deadline of pinned items (FR-08, FR-263). The Project Manager also holds every research right of a Researcher (FR-111).

### 3.3 Data Management (FE-03)

Design concern: immutable versions, safe import and a data location for every version.

1. The user uploads a file or imports from a data connection.
2. For an import, the Platform accepts only a source that the user authorized and blocks internal hosts (FR-10).
3. The Platform creates a new immutable DatasetVersion with a content hash. It never overwrites an older version (FR-09).
4. The Platform assigns a data location, `platform` or `local` (FR-12).
5. For `local` data, only the Local Node reads the rows. The Platform offers no preview and no download of rows (FR-12).

The Platform never returns the credential of a data connection to a user and never writes it to a log (FR-11). Upload accepts common tabular formats, including Parquet (FR-112). Report III lists the supported formats as a system rule.

### 3.4 Research Case and Run Management (FE-04)

Design concern: the run lifecycle, the pipeline order and the state of objects.

#### 3.4.1 Interaction viewpoint: a run through five stages

*Figure IV-6: Run through five stages: diagram to be regenerated from the design model.*

1. The Researcher creates a ResearchCase. A dataset is optional (FR-13).
2. The Platform checks that the project has no active run. If one exists, the Platform rejects the request (FR-16; ADR-13).
3. The Platform creates a Run with the `dataset_first` pipeline. It sends the policy (preset per stage), the presence and the keys by role to the first engine (FR-14).
4. The dataset engine runs a prelude in code. The agent works only on red contract items. If the project has no dataset, the engine searches the project, searches public datasets (role `enrichment` or `validation`), or asks the user through the decision inbox. A join of public data into private data is a pinned action (FR-15; ADR-14). The engine also runs a prefilter. It flags data signals and suggests research patterns using marginal distributions only (FR-117, FR-118; ADR-17). The dictionary records when each variable becomes available and flags post-outcome variables (FR-115).
5. The engine determines the unit of observation and the data structure. The Researcher confirms them (a pinned action) before the split is created (FR-40, FR-41; ADR-09). The engine checks duplicate rows across split parts and reports dataset shift by type (FR-114, FR-116). The engine publishes the DatasetSnapshot. The review loop runs (see 3.11). Acceptance follows the preset. At `milestones`, the level follows fitness: `fit` is `auto`, `fit_with_limits` is `do_then_review`, `not_fit` is `must_ask` (FR-34).
6. The hypothesis engine reads the pinned DatasetSnapshot and updates the Literature Base. It publishes the HypothesisSet. Choosing the hypotheses (at least two) and the primary is a pinned action (FR-44, FR-27).
7. The experiment design engine reads the HypothesisSet. It records the task family and chooses research patterns from the registry. It writes the pipeline order into the plan (FR-124, FR-125, FR-127). It runs the program on the twin. When the user locks the plan (a pinned action), the Platform writes the Lock (see 3.8).
8. The execution engine runs the lifecycle in 3.9 and publishes the EvidenceBundle.
9. The paper engine reads the EvidenceBundle, the AnalysisPlan, the Lock, the Literature Base, the DatasetSnapshot and the decision log. It publishes the PaperPack (FR-62).
10. When every stage is accepted, the Run ends with `ended(complete)`. The AI PI proposes a next step from the fixed set (`collect_more_data`, `explore_signal`, `replicate`, `write_paper`, `revise_plan`). The user chooses (FR-23).
11. If an upstream object gets a new version, the Platform marks the downstream objects that pin the old version as `stale` (FR-19).

Alternative flows:

- The Researcher or Project Manager who created the run can cancel it from any state except `ended`. The Run moves to `ended(cancelled)`, keeps accepted objects, closes pending items and writes the audit log (FR-22).
- A change to a confirmed research case needs an amendment with reason, version and event. A stage that has already started keeps the old case version (FR-17).

#### 3.4.2 State viewpoint: run state machine

*Figure IV-7: Run state machine: diagram to be regenerated from the design model.*

A run is in exactly one state (FR-21).

| Run state | Entry condition | Exit |
|---|---|---|
| `running` | The run starts or resumes. | To `waiting(...)` or to `ended(...)` |
| `waiting(decision)` | A `must_ask` item blocks all remaining work, and the user is `present` or the item is pinned. | Back to `running` when the user answers. A pinned item that waits keeps the run here until its wait deadline; the run does not end for that reason before the deadline (FR-262). To `ended(with_gaps)` when the run token budget ends or when the wait deadline of a pinned item passes without an answer (FR-262, FR-265). To `ended(cancelled)` on cancel. |
| `waiting(node_offline)` | A local job blocks work and the Local Node is offline. | Back to `running` when the Node returns. To `ended(cancelled)` on cancel. |
| `waiting(budget_review)` | The monthly project budget reaches 100%. | Back to `running` if the Project Manager approves more spending; to `ended(with_gaps)` if the item expires or the Project Manager declines; to `ended(cancelled)` on cancel |
| `ended(complete)` | Every stage is accepted. | None |
| `ended(with_gaps)` | One of three causes: the run token budget ran out, a `spending` item passed its deadline, or the wait deadline of a pinned item passed (FR-262, FR-265). The best output is published and red items are listed. For a pinned item, the item closes unanswered and nobody decides it for the user. | None |
| `ended(failed_technical)` | An unrecoverable technical error, or a missing model or credential. No sample output is created (FR-103). | None |
| `ended(cancelled)` | The Project Manager or the Researcher who created the run cancelled it. | None |

When a stage has no work left and a pinned item still waits, the stage stops at "ready for action" with the pinned item pending. The run stays in `waiting(decision)`. This is not a fourth run state (FR-32, FR-262). The run can leave any state except `ended` for `ended(cancelled)` (FR-22).

#### 3.4.3 State viewpoint: object states

*Figure IV-8: Object states: diagram to be regenerated from the design model.*

| Object state | Meaning |
|---|---|
| `draft` | The object is being built. |
| `checks_red` and `checks_green` | At least one contract item is red, or none is red. The object can move between the two. |
| `in_review` | The review loop is running. |
| `ready` | Review is complete. The object waits for acceptance. |
| `accepted` | The object is accepted and immutable. |
| `locked` | Only for AnalysisPlan: a Lock exists. |
| `stale` | A pinned upstream object has a new version. Any state can move to `stale`. |

The normal order is `draft`, `checks_red`/`checks_green`, `in_review`, `ready`, `accepted`, and for a plan `locked`.

### 3.5 Human Control (FE-05)

Design concern: control per action type, a single inbox, and a decision log that can be measured.

#### 3.5.1 Permission model

| Concept | Rule |
|---|---|
| Action group | Eight groups: `read_compute`, `technical_fix`, `content_judgment`, `object_drafting`, `spending`, `acceptance`, `pinned`, `unseal`. Each action type belongs to exactly one group (FR-26). |
| Level | `auto`, `do_then_review`, `must_ask`. |
| Preset | Chosen per stage: `co_work`, `milestones` (default), `autopilot`. A preset sets the level of each group (FR-25, FR-147 to FR-149). |
| Floor | The lowest level of an action type. An override cannot go below the floor. The floor of `object_drafting` is `do_then_review`, the floor of `pinned` is `must_ask`, and every other group has floor `auto` (FR-150). |
| Override | The user can change the level of an action type. The effective level is the override if present, otherwise the preset level, and never below the floor. |
| Pinned actions | Always `must_ask` in every preset: define the outcome and estimand; confirm the unit of observation and data structure before the split; choose hypotheses (at least two) and the primary; join public data into private data; lock the plan; deviate from the locked algorithm; use a validation source; export outside the project (FR-27). |
| `spending` | A monetary ceiling set by the Platform Admin applies in addition to the level. No preset spends above it without `must_ask` (FR-92). |
| `unseal` | `auto` when every check is green, in every preset. The user can raise it to `must_ask` (FR-52). |
| `acceptance` | At `milestones`, the level follows the verdict of code (FR-34). The floor is `auto`. |
| Change of preset | Applies to future actions. Waiting items are evaluated again. Past decisions are not recomputed (FR-25). |
| Presence | `present` or `away`. It changes only how `must_ask` items wait. It is not a mode. |
| Symmetry | Actions of the user and of the agent pass through the same guards, levels and checks. The decision log records who acted (FR-33). |

Level by preset:

| Group | `co_work` | `milestones` | `autopilot` | Floor |
|---|---|---|---|---|
| `read_compute` | `auto` | `auto` | `auto` | `auto` |
| `technical_fix` | `do_then_review` | `auto` | `auto` | `auto` |
| `content_judgment` | `must_ask` | `do_then_review` | `auto` (logged) | `auto` |
| `object_drafting` | `must_ask` | `do_then_review` | `do_then_review` | `do_then_review` |
| `spending` | `must_ask` | `must_ask` | `auto` below the ceiling; `must_ask` above it | `auto` |
| `acceptance` | `must_ask` | by verdict | `do_then_review` | `auto` |
| `pinned` | `must_ask` | `must_ask` | `must_ask` | `must_ask` |
| `unseal` | `auto` when all checks are green | as `co_work` | as `co_work` | `auto` (the user can raise it to `must_ask`) |

#### 3.5.2 Interaction viewpoint: a `must_ask` item, present and away

*Figure IV-9: Decision inbox flow: diagram to be regenerated from the design model.*

1. The engine meets an action with level `must_ask`.
2. The engine creates a DecisionInboxItem with options, a proposed option and a reason (FR-28).
3. If the user is `present`, the web app asks at once. The Run enters `waiting(decision)` if no independent work remains. The user answers and the decision log records it.
4. If the user is `away`, the item waits in the queue. The agent continues every action that does not depend on the item. A pinned item waits until the user returns or until its wait deadline. The run stays in `waiting(decision)` and does not end for that reason before the deadline (FR-262). The system sends a reminder before the deadline (FR-264). If the deadline passes without an answer, the run ends `ended(with_gaps)`, the item closes unanswered, and the gap is listed. Neither the AI PI nor a default value decides the item (FR-265, FR-266).
5. If the preset of the stage is `autopilot` and the user is `away`, the AI PI decides non-pinned items tentatively. Each tentative decision becomes an item of kind tentative decision. The AI PI never decides a pinned item and never ends the run (FR-31, FR-32; NFR-31).
6. When the user returns, the user confirms or overturns each tentative decision. After an overturn, the engine undoes dependent work and marks the affected objects `stale` (FR-31).
7. The decision log records who decided, the presence and any overturn. The system computes the overturn rate per action type and proposes a higher level. The system never raises the level by itself (FR-30).
8. External notifications (email, push) go only to blocking pinned items and to `spending` items. A pinned item reminder goes to the users who can answer the item: the Researcher who created the run and the Project Manager. A `spending` reminder goes to the Project Manager only (FR-29, FR-264).

The inbox has eight item kinds: question, review batch, tentative decision, deviation, candidate, needs-you, release review and spending. The inbox sorts items by blocking level and by blocking time (ADR-05). The AI PI writes the lab notebook with summaries, proposals, tentative decisions and reasons (FR-35). The decision log also records each agent assumption with its alternatives and reason. An assumption is never treated as the intent of the Researcher (FR-36).

### 3.6 Dataset Stage (FE-06)

Design concern: turn data into a DatasetSnapshot that later stages can use without guessing.

1. The prelude profiles the data on five quality dimensions and builds the table model, dictionary and cleaning recipe (FR-37). Cleaning never uses the outcome. Cleaning that needs the outcome belongs to the AnalysisPlan (FR-38).
2. Code decides the fitness of the data for the question: `fit`, `fit_with_limits` or `not_fit` (FR-39).
3. The Researcher confirms the unit of observation and the data structure (pinned). Without this confirmation, no split is created (FR-40, FR-41).
4. The stage chooses the split by power. `three_way` (exploration, confirmation, reserve) applies when the sample keeps a power of at least 0.8 and a reserve remains. `two_way` applies otherwise. `none` applies when the sample size is below the minimum, and the stage records a limitation (FR-42; ADR-09). Rows of one group never fall into two parts. Time-ordered data splits by time. Data with independent rows may use a repeated stratified split for a classification task family, inside the exploration part only (FR-41, FR-113).
5. The stage reports each type of dataset shift (covariate, label, concept) and checks duplicates across the split parts (FR-114, FR-116).
6. The review loop runs and acceptance follows the preset.

### 3.7 Hypothesis Stage and Literature Base (FE-07)

Design concern: a methodical literature review and a testable HypothesisSet.

1. The stage builds or updates the project Literature Base from metadata, abstracts and open-access full text (FR-43).
2. If one literature source fails, the stage records the error for that source and continues with the others. If every source fails, the stage records a gap (FR-43; R-08).
3. The stage produces a HypothesisSet with at least two hypotheses that have different claim keys, and one primary (FR-44).
4. Each hypothesis has a draft estimand, variables, sourced confounders, a smallest effect size of interest (SESOI), a refutation statement, a contribution type and an origin (FR-45). Each hypothesis also has a comparator, a primary metric that matches the task family, a direction or margin, a scope and a decision rule (FR-119). The stage returns a hypothesis without a comparator for repair and does not accept a deliberately weak baseline (FR-120).
5. A non-inferiority or equivalence margin maps onto the SESOI regions of the verdict. The system never concludes equivalence from a non-significant p-value (FR-121, FR-122).
6. The portfolio keeps one primary and no more secondary hypotheses than the project setting allows (FR-123).
7. The Researcher chooses the hypotheses and the primary (pinned).

### 3.8 Experiment Design Stage and Lock (FE-08)

Design concern: a complete AnalysisPlan and a Lock that fixes it before any confirmatory run.

#### 3.8.1 Interaction viewpoint: lock the plan

*Figure IV-10: Lock, rehearsal, envelope and unseal: diagram to be regenerated from the design model (covers 3.8 and 3.9).*

1. The engine produces an AnalysisPlan for existing tabular data (FR-46). It records the task family, the chosen research patterns and the pipeline order (FR-124 to FR-127).
2. The engine runs the analysis program on the twin, which is built from released aggregates only, before the lock (FR-47).
3. The engine requests the pinned action "lock plan". The user locks. The Platform writes the Lock with the hashes of the spec, the program and the golden outputs, the snapshot version, the split digest, who locked and when (FR-48).
4. If the user is `away`, the plan waits for the lock. Nobody locks on behalf of the user (FR-49).
5. From this point the locked parts are immutable. A change is a deviation (pinned) and enters the deviation log (FR-56).

The plan uses evidence families in the order discrimination, reliability and decision for `prediction` (FR-128). The claim type `method_comparison` (FE-19, Should, after MVP) uses the same order (FR-267). Task family `rare-event` uses average precision or precision at fixed recall, and never compares average precision across different prevalences (FR-129, FR-130). Calibration uses data separate from the training data (FR-131). The baseline policy runs a simple baseline first, on the same split with the same tuning budget (FR-132). Pattern scope follows the claim type (FR-126).

### 3.9 Execution Stage (FE-09)

Design concern: protect confirmatory results until unseal, and compute verdicts in code.

#### 3.9.1 Interaction viewpoint: lock, dry run, envelope, unseal, judge, interpret

1. The engine builds the analysis from the Lock. Locked parts are immutable. The guard checks the pipeline order before every run. A violation is blocked or recorded as a deviation (FR-133; ADR-17).
2. Rehearsal on the twin: the implanted effect must be recovered. A clean permutation check runs on the twin without the true effect (FR-50).
3. Dry run on real data: the full program runs. It returns only the row count, types, missingness, convergence and time. It returns no estimate (FR-50).
4. Confirmatory job: it carries an envelope flag. The Executor sends the result directly to the Platform. The agent sees only "done" or "error", after the error firewall. Fix and rerun are allowed because nobody has seen an estimate (FR-51).
5. The engine sends the unseal request with the contract status. The Platform checks four conditions: a Lock exists; every confirmatory job of the Lock is complete; the request comes after the last repair of lane C (the confirmatory lane); the level of `unseal` is `auto` or the user approved (FR-52, FR-53).
6. If a condition fails, the Platform rejects the request (QS-03).
7. The Platform opens all results of the Lock at the same time and records the unseal time (FR-53).
8. Code judges. The primary hypothesis comes first (gatekeeping: a secondary hypothesis is tested only after the primary). Holm correction, a step-down adjustment for multiple tests, applies to secondary hypotheses. The verdict uses three regions around the SESOI and a permutation check. The verdict has one of five values: `supported`, `trivial`, `not_supported`, `insufficient`, `not_tested` (FR-54; ADR-07).
9. The Interpreter chooses one row of the locked interpretation table per hypothesis. The conclusion text comes from that row. Code computes the grade (A to D) and the claim ceiling (FR-54, FR-55).
10. Lane D runs post-hoc, labeled `post_hoc`. Lane P packages. The Replicator reruns and compares hashes. The review loop runs. The engine publishes the EvidenceBundle (FR-60, FR-61).
11. Lane E starts from the rehearsal step and works only on the exploration part. Every procedure goes into the tried ledger. The candidate cap per round limits how many candidates go to the decision inbox. A candidate is never a claim (FR-57, FR-58). A confirmed candidate gets a confirmation tier. Only the tiers `replicated` and `reserve` record an e-value (FR-59; ADR-09).

State of the envelope: sealed, then unsealed. The envelope is bound to one Lock.

### 3.10 Paper Stage (FE-10)

Design concern: a PaperPack that the paper team can use without rederiving numbers.

1. The stage reads the EvidenceBundle, the AnalysisPlan and Lock, the Literature Base, the DatasetSnapshot and the decision log, and builds the PaperPack with ten checked items (FR-62).
2. Code renders every number in the manuscript and in figures from EvidenceBundle records. A digit in model text that is not a reference turns the check red. Years, item numbers and section numbers are allowed (FR-63; QS-01).
3. Every effect statement in the Abstract, Results and Discussion maps to a verdict and an interpretation row. Claim words match the verdict. A claim never exceeds the claim ceiling (FR-64).
4. Every citation lies in the Literature Base, has a resolved digital object identifier (DOI) and has a supporting quote (FR-65).
5. The limitations section names every grade reason, gap, known risk, deviation, negative control result, low power and confounding sensitivity. Code checks the coverage (FR-66).
6. Author-only fields stay as "awaiting author". The AI-use declaration comes from the decision log (FR-67).
7. The reporting checklist follows the claim type: STROBE with RECORD for association and causal, TRIPOD for prediction (public reporting guidelines for observational studies, routinely collected data and prediction models). The PaperPack has at least three main figures (FR-68).
8. Writing rules have three kinds: H (a violation is an error), M (over a threshold it becomes an issue) and G (guidance in the reviewer rubric) (FR-69). The Researcher decides on submission. The system never submits a paper (FR-70).

### 3.11 Independent Review Loop and Personas (FE-11)

Design concern: independent, verified review that is bounded in time.

*Figure IV-11: Review loop: diagram to be regenerated from the design model.*

1. Every check of the object version is green (FR-71).
2. Guard personas run in parallel with a fresh context. They cannot see the trace of the author and they do not read each other (FR-72).
3. Reviewers produce findings. Code drops findings without an anchor or evidence (FR-73).
4. Each finding is verified by code or by a second verifier as `confirmed`, `plausible` or `rejected` (FR-74).
5. Only `blocking` findings that are `confirmed` enter the revision loop. `major` and `minor` findings are recorded and shown (FR-74).
6. The maker revises. Checks run again. Review runs again only on the repaired findings and the changed fields.
7. A new blocking finding on an unchanged field is valid only when its evidence is a newly computed fact (FR-270).
8. There are at most two revision rounds. Remaining findings become known risks, or the user decides between the two sides, where the Facilitator shows both (FR-75; QS-12).
9. A reviewer whose precision on the seeded-flaw bench is below the threshold has the severity of its blocking and major findings reduced (FR-77).

The system rejects an object only when provenance or contract is broken. Other content problems are retried and then kept as findings or known risks. Evidence that cannot be resolved is not published (FR-76). The user can call any persona on any object (FR-78). Personas are of three types: maker, guard and connector. Personas are lenses with a mandate, a finding taxonomy, skills, tools and measured precision. A persona is enabled only when the bench shows that it catches what other personas miss (FR-77).

| Stage | Maker personas | Guard personas |
|---|---|---|
| `dataset` | Data Steward, Data Scout | Data Auditor, Privacy Officer, Domain Expert |
| `hypothesis` | Theorist, Librarian | Skeptic, Methodologist, Prior-art Checker |
| `experiment_design` | Trialist, Analyst | Methodologist, Skeptic, Domain Expert, Equity Reviewer, Code Auditor |
| `execution` | Engineer, Interpreter | Skeptic, Replicator, Code Auditor, Privacy Officer |
| `paper` | Scribe | Reporting Editor, Skeptic, Reviewer 2, Figure Reviewer |
| connector | AI PI, Explainer, Facilitator | None |

Every research pattern has a negative test, which is a seeded defect that the pattern must detect (FR-134). The red-team catalogue of the seeded-flaw bench has three groups: data, experiment and inference defects (FR-135). The bench measures the leakage detection rate and the pipeline order block rate (FR-136, FR-137). The benchmark case catalogue of 60 sample projects supplies test cases (FR-138).

### 3.12 Local Node (FE-12)

Design concern: data rows never leave the machine, and every release is checked and logged.

#### 3.12.1 Interaction viewpoint: a local job through the release gate

*Figure IV-12: Local job and release gate: diagram to be regenerated from the design model.*

1. The Platform routes a job on a dataset version with location `local` to the Local Node.
2. If the Node is offline and the job blocks work, the Run enters `waiting(node_offline)`. Work that needs no data continues: twin rehearsal, planning and drafts. The Platform sends one combined notice (FR-85).
3. The Node checks the hash of the dataset version. On a mismatch, it rejects the job and proposes a new version (FR-84).
4. The Node runs the job in its own sandbox: no network, read-only data, only declared columns.
5. The result passes the release gate in a fixed order: firewall (small-cell threshold, fixed error forms), rounding, disclosure mode, differencing check against the release log of the Node, probe budget of the dataset version (FR-80).
6. If the probe budget is exhausted, the case becomes a gap and the run does not stop (FR-86).
7. A valid release enters the append-only release log. The Platform receives a copy. The aggregate continues to the engine. Data rows never move (FR-81; NFR-13).
8. In disclosure `strict`, a kind of number that is not yet approved creates a release review item in the decision inbox. The Researcher or the Project Manager of the project answers (FR-82). In disclosure `standard`, releases within the policy are automatic.
9. A rejected query is shown together with the reason (FR-86; QS-07).
10. When a Node is revoked, the Platform rejects jobs for the `local` data of that Node and tells the user why. Objects already published stay readable (FR-110).

Other design points: the user pairs a Node with a project by a pairing code, and the Node proposes datasets from a watched folder (FR-87). Models receive only aggregates and profiles computed by code. An exception from real data returns only the kind of error, the column and the number of affected rows (FR-83). The Node declares its isolation level in a manifest. If the machine has no isolation, the Node runs only registered families (ADR-10; R-09).

### 3.13 Budget and Cost (FE-13)

Design concern: spending has a ceiling at three levels, and a run always ends.

*Figure IV-13: Budget flow: diagram to be regenerated from the design model.*

1. Item. Each contract item has a fixed share of the run token budget. When an item uses its share, the Harness creates a needs-you item with the last error and what was tried. It is `must_ask` in every preset. The run continues other work (FR-20; ADR-11).
2. Run. When the run token budget ends, the Run ends with `ended(with_gaps)`. The best output is published and every red contract item is listed (FR-88).
3. Project. The system warns at the thresholds of the monthly budget (FR-89).
4. At 100%, the Platform blocks new runs. An active run enters `waiting(budget_review)` and a `spending` item of level `must_ask` is created (FR-89, FR-90; ADR-15).
5. The Project Manager approves more spending, and the run continues. Or the Project Manager lets the run end with gaps (FR-90).
6. The item has an answer deadline. The Platform sends an external notice (email, push) to the Project Manager when the item is created and a reminder before the deadline. When the deadline passes, the run ends with `ended(with_gaps)` (FR-91; QS-10).
7. The Platform Admin sets a spending ceiling. This ceiling is a monetary limit, separate from the floor level of the `spending` group. At `autopilot`, spending is `auto` only below the ceiling and `must_ask` above it (FR-92, FR-149).
8. The Platform keeps the usage and cost ledger per run and per project (FR-93).

### 3.14 Dossier, Approval and Export (FE-14)

Design concern: a reviewable package that holds references, never copies, and that controls export.

*Figure IV-14: Dossier and approval flow: diagram to be regenerated from the design model.*

1. When a PaperPack is accepted, the Platform creates Dossier version 1. It holds references to the accepted EvidenceBundle and PaperPack versions. The Platform checks the hash of every reference. A run that ends with gaps or is cancelled before an accepted PaperPack has no Dossier (FR-94).
2. If the bundle or the pack gets a new accepted version, the Platform creates a new Dossier version. The old version stays unchanged. Approvals of the old version do not carry over (FR-96).
3. Reviewers and Project Managers read and comment. Approval follows the review settings: number of approvals, who may approve, whether self-approval is allowed (FR-95).
4. When the current version has enough approvals, the Dossier moves to approved.
5. Export outside the project is a pinned action and needs an approved Dossier (FR-97).
6. Each export writes an entry to the audit log with the Dossier version and the format (FR-98).

The Platform only versions, checks hashes and records approvals. It does not judge science (ADR-12). If the Dossier is not approved, the Platform rejects the export.

| Dossier state | Meaning |
|---|---|
| Version N, not approved | The version exists and has fewer approvals than required. |
| Version N, approved | The version has enough approvals under the review settings. Export is allowed. |
| Superseded | A newer version exists. Approvals of this version stay as history only. |

### 3.15 Collaboration (FE-15)

Design concern: members work together around one run.

1. A Reviewer reads and comments on any object of the project. A Project Manager and a Researcher comment according to the role (FR-99).
2. A comment has an anchor on a project object (see Comment in 2.1.5).
3. The Platform sends notifications about project events according to the notification settings. External notices go only to blocking pinned items and `spending` items (FR-100; ADR-05).

### 3.16 Administration and Monitoring (FE-17)

Design concern: central configuration, sealed secrets and visible operation.

1. The Platform Admin manages users, model profiles by model role (`stage`, `review`, `vision`), keys, engine settings and the default budget (FR-101).
2. The Platform seals model keys and integration secrets. They never appear in a prompt, a log or an output (FR-102; NFR-09).
3. If a model or a credential is missing, the Run ends with `ended(failed_technical)` and a clear error. The system creates no sample output (FR-103; R-12).
4. The Platform Admin views the system audit log and the health of components (FR-104).
5. The system reports, for each run, the number of questions, the blocked time and the overturn rate per action type. It also reports persona precision on the seeded-flaw bench (FR-105; NFR-24).

### 3.17 Journal Fingerprint Extraction (FE-18, Could, after MVP)

Design concern: evidence-based journal profiles for the `paper` stage.

1. The system builds a journal profile from a corpus that may be used, with its sources, usage rights, uncertainty and version (FR-106).
2. Each profile feature traces to a corpus snapshot and a source span. The profile separates observed practice from mandatory publisher rules (FR-107).
3. The Researcher approves the profile. The `paper` stage references the approved version (FR-108).
4. The profile never changes the content or the certainty of a claim (FR-109).

### 3.18 Method Comparison Research (FE-19, Should, after MVP)

Design concern: compare machine-learning methods under the same controls, on the same Harness.

The claim type `method_comparison` uses the same Harness, Lock, envelope and verdict. It adds the research patterns G (hyperparameter optimization), H (ensemble and stacking), I (ablation) and J (budget-aware), together with baseline policy F (FR-139, FR-269; ADR-18). The task family chooses the metric policy and the protocol (FR-268). The design adds these conditions to the plan and the checks: paired comparison per fold and seed (FR-140), many seeds (FR-141), equal tuning budget for all methods (FR-142), nested validation when tuning is used (FR-143), correction for multiple comparisons (FR-144), and negative results kept in the EvidenceBundle (FR-145). The MVP does not change. The scope risk is R-14.

### 3.19 Cross-Cutting Behavior

#### 3.19.1 Numbers from code

Model text carries only references to records. Code renders the numbers. A digit in model text that is not a reference fails a check. Years, item numbers and section numbers are allowed. Verdict, grade, claim ceiling and fitness are computed by code. Charts read numbers from the EvidenceBundle and never refit a model (FR-24; ADR-07).

#### 3.19.2 Self-healing and failure behavior

A red check is a task for the agent loop. The trace shows each item as red, then action, then green. There is one budget per run and a share per item. There is no separate retry counter per mechanism (ADR-11).

| Situation | Behavior |
|---|---|
| Model or credential missing | A clear error. `ended(failed_technical)`. No sample output. |
| One literature source is down | Record the error for that source. Continue with other sources. Record a gap if all fail. |
| Node offline and a job blocks work | `waiting(node_offline)`. Other work continues. One combined notice. |
| Source file changed during the run | The job is rejected because the hash does not match. A new version is proposed. |
| Source file deleted | The run ends at that job with a gap. Released data stays. |
| Node revoked | Local jobs are rejected. Published objects stay readable. |
| Item budget used | A needs-you item. The run continues other work (FR-164). |
| Reviewers disagree after two rounds | A known risk, or the user decides with both sides shown. |
| A pinned item passes its wait deadline unanswered | A reminder goes out before the deadline. At the deadline the run ends `ended(with_gaps)`, the item closes unanswered, and the gap is listed (FR-265). |

User messages follow the message catalogue of Report III, not technical codes.

#### 3.19.3 Observability

| Channel | Content |
|---|---|
| Trace event | Every action and every check change, per engine. It streams to the web app. |
| Decision log | Action type, level, policy version, who decided, presence, whether overturned. |
| Audit log | Administrative and security actions. |
| Release log | Every aggregate that left the data holder. |
| Overturn metric | Overturn rate per action type; a proposal to raise a level. The system never raises it. |
| Operating metrics | Questions per run, blocked time, persona precision on the seeded-flaw bench. |
| Lab notebook | Summaries, proposals, tentative decisions of the AI PI and the reasons. |

## 4. Quality Scenarios

Each scenario links a quality goal to a stimulus, a response and a measure. The quality tree shows which decisions support each goal.

| Quality goal | Attribute | Supported by |
|---|---|---|
| Integrity | No model-written number; no hidden defect; confirmatory results are not seen early; leakage is detected or blocked | ADR-06, ADR-07, ADR-08, ADR-11, ADR-17 |
| Traceability | Every claim and number points to a record; objects pin versions | ADR-01, ADR-07, ADR-12 |
| Replayability | The same pinned input gives the same hash | ADR-01, ADR-08 |
| Data privacy | `local` data rows do not leave the machine; every release is logged | ADR-10 |
| Human control with progress | Control by action type; runs always end; spending has a ceiling | ADR-04, ADR-05, ADR-11, ADR-15 |

| ID | Quality goal | Stimulus | Response | Measure |
|---|---|---|---|---|
| QS-01 | Integrity | The paper engine writes a paragraph with a digit that is not a reference. | The check fails and the paragraph returns to the Scribe. | 0 digits outside the allowed list (years, item numbers, section numbers) in an accepted PaperPack. Checked at every version. |
| QS-02 | Integrity | The agent tries to read a confirmatory result before unseal. | The Platform returns no result. The agent sees only "done" or "error". | 0 confirmatory estimates in the trace and the workspace before the unseal time. Checked on every run. |
| QS-03 | Integrity | Unseal is requested before the last repair of lane C. | The Platform rejects the request. | 100% of unseal requests earlier than the last repair are rejected. |
| QS-04 | Traceability | A reviewer picks a claim in the PaperPack at random. | The claim points to a verdict, an interpretation row and a record in the bundle. | 100% of claims in the Abstract, Results and Discussion have a verdict and an interpretation row. |
| QS-05 | Replayability | The Replicator reruns the package of an EvidenceBundle. | The result hash equals the hash of the bundle. | 100% of items have a hash. The Replicator hash equals the bundle hash; if not, the item is red. |
| QS-06 | Data privacy | A local job runs a whole run. | Only aggregates leave the Node. | 0 data rows in any outgoing message, checked by packet capture in the test scenario. The number of releases in the release log equals the number the Platform holds. |
| QS-07 | Data privacy | Two queries differ in fewer rows than the small-cell threshold. | The release gate rejects the second query. | 100% of such queries are rejected and the reason is shown. |
| QS-08 | Human control with progress | A stage uses up the budget share of one item. | A needs-you item is created. The run continues other work. | 1 needs-you item per exhausted item; 0 retries beyond the share. |
| QS-09 | Human control with progress | The run budget ends while a red item remains. | The run ends with `ended(with_gaps)`. | 100% of runs end in one of the defined outcomes; 0 runs wait forever without an item that waits for the user. |
| QS-10 | Human control with progress | The monthly budget reaches 100% during a run. | The run enters `waiting(budget_review)`. A `spending` item is created. New runs are blocked. | 100% of new runs are blocked; 1 `spending` item per affected run. |
| QS-11 | Human control with progress | The user is `away` at `autopilot`. Pinned and non-pinned items exist. | The AI PI decides non-pinned items tentatively. Pinned items wait. | 0 AI PI decisions on pinned items; 100% of tentative decisions appear in the inbox when the user returns. |
| QS-12 | Integrity | The review loop does not resolve a blocking finding. | After two revision rounds the finding becomes a known risk or waits for the user. | No more than 2 revision rounds per object version; 100% of remaining findings are shown in the PaperPack. |
| QS-13 | Integrity | A dataset has a post-outcome column and duplicate rows across split parts (seeded in the red-team catalogue). | The `dataset` stage flags the post-outcome column and reports the duplicates before the DatasetSnapshot is accepted. | Detection rate of seeded leakage on the seeded-flaw bench is at least 90% (SM-17). |
| QS-14 | Integrity | A plan or an agent fits a learning step (for example resampling) before the split or outside the train part. | The execution guard blocks it before the run, or records the violation as a deviation. | Block rate of seeded pipeline order violations on the seeded-flaw bench is 100% (SM-18). |
| QS-15 | Human control with progress | The user is `away` past the wait deadline of a pinned item. | The Platform sends a reminder before the deadline. At the deadline the run moves from `waiting(decision)` to `ended(with_gaps)`, the item closes unanswered, and the gap is listed. | 100% of such pinned items close unanswered; 0 decisions by the AI PI or by a default value on a pinned item; 0 runs stay in `waiting(decision)` after the wait deadline. |

## 5. Risks and Technical Debt

The risks are at design level. This Report describes the system as specified and does not track delivery status.

| ID | Risk | Impact | Mitigation |
|---|---|---|---|
| R-01 | A reviewer has errors correlated with the author because both use the same model. | Defects pass review. | Use a separate model role `review`. Measure persona precision on the seeded-flaw bench. Reduce severity below the threshold. |
| R-02 | Inference from many aggregates reveals personal information. | Breach of data privacy. | Small-cell threshold, rounding, differencing check, probe budget, noise on exploratory probes, a release log that can be inspected. |
| R-03 | The twin differs from the real data. | A plan works on the twin and fails on real data. | The dry run compares with the twin. Repairs happen before the envelope because nobody has seen an estimate. |
| R-04 | The Platform is the only trust point for the envelope. | A person who can change Platform code could see results early. | Access control, append-only audit log, code review. ADR-08 states that it does not stop such a person. |
| R-05 | Model cost exceeds expectations. | Runs end early. | Run budget, item share, monthly budget, notices at thresholds, spending approval by the Project Manager. |
| R-06 | The item share is set wrongly. | Items move to needs-you too early or too late. | The share is a measurable setting. Track the needs-you rate in the operating metrics. |
| R-07 | Approval fatigue at `co_work` and `milestones`. | Users accept without thought. | Batch review items. Track the overturn rate. Propose a higher or lower level and never change it automatically. |
| R-08 | A literature source is missing or fails. | A weak Literature Base. | Record errors per source. Use other sources. Record a gap. Use open-access full text only. |
| R-09 | The isolation level of the Local Node differs by operating system. | Agent-written code may not run on some machines. | The Node declares its capability in a manifest. Fallback to registered families. Known in advance. |
| R-10 | The limit of one active run slows a team. | Low throughput inside one project. | A deliberate choice (ADR-13). Use several projects for parallel work. |
| R-12 | Dependence on the model service. | Runs fail when the service stops. | A clear error and `ended(failed_technical)`. No sample output. Published objects stay readable. |
| R-13 | A small team and a fixed project period. | Not enough time for every persona and bench. | One Harness (ADR-02). Enable only personas with measured value. Journal Fingerprint Extraction (FE-18) is Could. |
| R-14 | The scope grows with `method_comparison` and the 60 sample cases. | The MVP loses focus. | Should, after MVP. The MVP does not change (ADR-18). Cases with patterns G to J belong to `method_comparison`. |

Technical debt: the design sources record no technical debt items beyond the risks above.

## Open items

1. All figures (IV-1 to IV-14) are placeholders. The team must regenerate them from the design model, including the crow's foot entity-relationship diagram for section 2.
2. Closed. QS-13 and QS-14 use the targets of SM-17 and SM-18.
3. The content of the writing rules H, M and G (FR-69) is not defined in the requirements.
4. Closed. The default limit on secondary hypotheses (FR-123, SR-06) is 3.
5. The logical data model has no entity for the Local Node registration, pairing and revocation (FR-87, FR-110), for the lab notebook entry (FR-35), for engine settings (FR-101), for the spending item deadline (FR-91), for the wait deadline of a pinned item (FR-263) or for the journal profile (FE-18). The sources do not define these entities. Add them if the team needs them in the data design.
6. The values of the monthly budget thresholds, the invitation expiry, the answer deadline of the `spending` item, the small-cell threshold, the probe budget and the list of upload formats are system rules in Report III. This section does not set them.
7. The sources do not define the lifecycle states of a project (beyond active and archived, FR-06) or of a membership invitation.
8. The sources list no technical debt items.

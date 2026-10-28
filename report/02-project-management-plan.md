# II. Project Management Plan

## 1. Overview

This Project Management Plan defines how OpenAI-Scientist is planned, estimated, developed, reviewed, tested, and delivered during the capstone period from 07/09/2026 to 27/12/2026.

The plan has two parts:

- The baseline (sections 1.1 and 1.2) keeps the original scope, estimate, and schedule.
- The re-plan (sections 1.4 and 1.5) covers the remaining work and records the scope changes. It takes its scope from the product requirements (Report III).

Section 1.3 gives one risk register for both parts. The Software Requirement Specification is Report III.

The target system is a five-stage research pipeline (`dataset`, `hypothesis`, `experiment_design`, `execution`, `paper`) with mandatory independent review and human control by preset (FE-04, FE-05, FE-11). Report III defines the use cases and system rules.

### 1.1 Scope & Estimation

The baseline estimate is in person-days for the full team. The team re-estimates at the end of each sprint.

Basis of the estimate:

- Team size: four members.
- Duration: 16 weeks (eight two-week sprints), so 320 person-days of nominal capacity.
- The estimate of 240 person-days is 75% of nominal capacity. The remaining 25% (80 person-days) is a reserve for meetings, reviews, rework, and report writing.

Baseline work breakdown structure (WBS):

| # | WBS Item | Complexity | Est. Effort (person-days) |
| ----- | ----- | ----- | ----- |
| 1 | Authentication & Account | | 14 |
| 1.1 | Passwordless sign-in, session, request protection | Medium | 4 |
| 1.2 | Third-party identity sign-in | Medium | 3 |
| 1.3 | Onboarding, profile and avatar | Low | 2 |
| 1.4 | Admin user management (create, suspend, grant admin) | Medium | 3 |
| 1.5 | Rate limits and code lockout | Medium | 2 |
| 2 | Project Workspace | | 18 |
| 2.1 | Project CRUD, archive/restore, complete/reopen, derived status | Medium | 5 |
| 2.2 | Members, invitations and invite candidates | Medium | 5 |
| 2.3 | Project files | Low | 2 |
| 2.4 | Project settings, activity and audit log | Medium | 3 |
| 2.5 | Comments on runs | Low | 3 |
| 3 | Data | | 22 |
| 3.1 | Dataset upload, validation and versions | Medium | 5 |
| 3.2 | Data connections to database servers and a cloud warehouse | High | 7 |
| 3.3 | Cloud spreadsheet and drive connection with file picker | High | 5 |
| 3.4 | Time-series monitoring connectors | Medium | 5 |
| 4 | Stage Contract & Skeleton | | 24 |
| 4.1 | Stage contract: models, interfaces, events and schemas | Complex | 8 |
| 4.2 | Stage skeleton: run loop, store, checks, recovery | Complex | 10 |
| 4.3 | Model client, agent loop and decision step | High | 6 |
| 5 | Research Run Orchestration | | 30 |
| 5.1 | Start run, pipelines and stage runs | Complex | 8 |
| 5.2 | Stage callbacks: events and artifacts | High | 5 |
| 5.3 | Stage checks, acceptance, rerun, iterations | Complex | 7 |
| 5.4 | Pause, resume, stop, abandon, sync, self-healing | High | 5 |
| 5.5 | Token budget, cost ledger, project budget | High | 5 |
| 6 | Research Stages | | 46 |
| 6.1 | Dataset stage | Complex | 12 |
| 6.2 | Hypothesis stage | Complex | 16 |
| 6.3 | Experiment design stage | Complex | 18 |
| 7 | AI Principal Investigator | | 14 |
| 7.1 | Consultations, AI PI agent and guards | Complex | 8 |
| 7.2 | Critic, obligations, charter and directives | High | 6 |
| 8 | Frontend | | 40 |
| 8.1 | Sign-in, onboarding, project list and workspace | Medium | 8 |
| 8.2 | Datasets, connections, documents, members, settings | Medium | 10 |
| 8.3 | Research flow and run studio scenes | Complex | 14 |
| 8.4 | Admin pages | Medium | 8 |
| 9 | Notifications, Integrations & Monitoring | | 12 |
| 9.1 | Notifications and live event stream | Medium | 4 |
| 9.2 | Chat-tool webhooks | Medium | 3 |
| 9.3 | Admin overview, usage, log monitoring | Medium | 5 |
| 10 | Evaluation, Testing & Release | | 20 |
| 10.1 | Evaluation bench (hypothesis cases, seeded flaws) | High | 6 |
| 10.2 | Integration and system testing | Medium | 8 |
| 10.3 | Deployment, documentation and buffer | Medium | 6 |
| | Total | | 240 |

Check of the totals: the group totals are 14 + 18 + 22 + 24 + 30 + 46 + 14 + 40 + 12 + 20 = 240 person-days. Each group total equals the sum of its items.

The baseline WBS predates the target scope. It has no item for the `execution` stage, the `paper` stage, the Local Node, the Dossier, the review loop, the decision inbox, or the tabular control layer. Section 1.4 maps these items to the re-plan. Their effort is an open item.

Assumptions and constraints of the baseline:

- The team has four members with the roles in section 4.
- The model provider is available to the team during development and demonstration.
- Requirements change only through the scope change log in section 1.5.
- Each sprint ends with a supervisor demo. The sprint review checks the remaining effort.

### 1.2 Project Objectives

Quality:

| # | Test Level | Test Coverage | Defect Limit | Notes |
| ----- | ----- | ----- | ----- | ----- |
| 1 | Reviewing | 100% of changes reviewed by a peer | ≤ 10 minor defects | Peer review |
| 2 | Unit Test | Core services and stage steps | ≤ 8 defects | Automated tests |
| 3 | Integration Test | 100% of stage interfaces | ≤ 6 defects | Stage-level test fixtures |
| 4 | System Test | 100% of main pipeline flows | ≤ 5 defects | Complete pipeline runs |
| 5 | Acceptance Test | 100% of agreed features | ≤ 2 defects | Supervisor demo |

The baseline defect budget totals 31 defects.

Milestone timeliness: 95% of sprint milestones delivered on time.

Allocated effort. The table uses the same breakdown as the WBS in section 1.1. The percentages are shares of 240 person-days.

| WBS group | Allocated Effort (person-days) | Percentage |
| ----- | ----- | ----- |
| 1 Authentication & Account | 14 | 5.8% |
| 2 Project Workspace | 18 | 7.5% |
| 3 Data | 22 | 9.2% |
| 4 Stage Contract & Skeleton | 24 | 10.0% |
| 5 Research Run Orchestration | 30 | 12.5% |
| 6 Research Stages | 46 | 19.2% |
| 7 AI Principal Investigator | 14 | 5.8% |
| 8 Frontend | 40 | 16.7% |
| 9 Notifications, Integrations & Monitoring | 12 | 5.0% |
| 10 Evaluation, Testing & Release | 20 | 8.3% |
| Total | 240 | 100.0% |

The baseline WBS has no separate item for requirements analysis, system design, project management, and report writing. The team treats this as a gap. The re-plan lists it as an open item (O-2).

Product objectives. The objectives below come from the success metrics (SM). Report V defines how each metric is tested.

| Objective | Target | Source |
| ----- | ----- | ----- |
| Every run reaches an `ended` state | 100%; no run stays in `running` or `waiting` without a pending decision inbox item | SM-01 |
| No local data row leaves the Local Node | 0 rows in outgoing messages during the Local Node acceptance scenario | SM-05 |
| No run shows a confirmatory estimate before unseal | 0 runs | SM-07 |
| Every accepted object version has passed the review loop | 100% | SM-10 |
| No run exceeds its token budget without ending `with_gaps` | 0 runs | SM-11 |
| Every number in a published object references a code-computed record | 100% | SM-03 |
| Every stage passes its acceptance scenario in one live run | 5 of 5 stages, plus the Local Node | SM-14 |
| Every export comes from an approved Dossier | 100% | SM-15 |

### 1.3 Project Risks

The risk register merges the business risks with the architecture risks (R-01 to R-14). The sources give no probability or impact scale, so the register shows the consequence in words.

| # | Risk | Consequence | Response Plans | Source |
| ----- | ----- | ----- | ----- | ----- |
| 1 | The model invents sources or numbers. | Unsupported claims in a paper. | Numbers come from code (BR-41). Text carries references, not numbers. Citation and provenance checks (BR-42, BR-66, BR-68). The review loop (BR-35). | Business risk |
| 2 | Confirmatory results are p-hacked. | The confirmation loses its value. | Power-based split (BR-44), Lock (BR-47), envelope and unseal (BR-49), tried ledger (BR-52), confirmation tier (BR-53). | Business risk |
| 3 | Data rows leave the place that holds the data. | Privacy breach. | Local Node, single release gate, release log (BR-19 to BR-22). | Business risk |
| 4 | Multiple aggregates reveal personal data. | Privacy breach. | Small-cell thresholds, rounding, differencing checks, probe budget, noise on exploratory probes, auditable release log. | R-02 |
| 5 | The AI reviewer shares the author's bias. | Defects pass review. | Fresh review context, several personas, precision measured on the seeded-flaw bench (BR-36, BR-40). A separate model role for review. Severity drops when precision is below the persona minimum. | Business risk, R-01 |
| 6 | The Researcher changes the goal during a run. | Results no longer match the question. | Versioned amendment (BR-10), stale marking (BR-12), decision log (BR-29). | Business risk |
| 7 | The AI PI decides wrongly. | A wrong tentative decision. | The AI PI decides only tentatively and never decides pinned items. The user can overturn. Overturns suggest a higher level (BR-29 to BR-31). | Business risk |
| 8 | The user receives too many questions or is away. | Slow runs or blind approvals. | Presets per stage, batching, presence. Outside notifications only for blocking pinned items and spending items (BR-24, BR-27, BR-28). | Business risk |
| 9 | Approval fatigue at the `co_work` and `milestones` presets. | The user approves without reading. | Grouped review items, overturn rate, advice to raise or lower the level. The system never changes the level by itself. | R-07 |
| 10 | The share of budget given to an item is wrong. | An item reaches `needs-you` too early or too late. | The share is a measurable setting. The team tracks the `needs-you` rate as an operating metric. | R-06 |
| 11 | Model cost or provider failure. | A run ends early. | Token budget, project budget, `ended(with_gaps)` (BR-58 to BR-61). Clear failure state when the model gateway is down; no sample output; published objects stay readable. | Business risk, R-05, R-12 |
| 12 | The Local Node is offline. | A run waits. | The run moves to `waiting(node_offline)`. Other waiting items do not block other work (BR-27). | Business risk, R-09 |
| 13 | The Local Node isolation level differs by operating system. | Agent-written code cannot run on some machines. | The node declares its capabilities. The AnalysisPlan has a pre-specified fallback analysis from the analysis registry, which runs when the planned analysis cannot run. The plan knows this in advance. | R-09 |
| 14 | An upstream object changes and the downstream object is wrong. | Inconsistent results. | Stale marking (BR-12). The user chooses whether to update. | Business risk |
| 15 | Detailed writing rules are not yet complete. | Paper checks are partly empty. | The content of each writing rule is still an open question (BR-72). | Business risk |
| 16 | Scope grows to `method_comparison` and 60 sample cases. | The MVP loses focus. | `method_comparison` is Should and after MVP; the MVP stays unchanged (BR-82, BR-101). | Business risk, R-14 |
| 17 | Leakage in preprocessing or in the data. | Over-optimistic results. | Pipeline order and guard (BR-86, BR-87), leakage flags (BR-88), red-team catalogue with SM-17 and SM-18 (BR-100). | Business risk |
| 18 | The twin differs from the real data. | A plan works on the twin but fails on real data. | Dry run against the twin. The team fixes the plan before the envelope because nobody has seen an estimate. | R-03 |
| 19 | The Platform is the only trust point for the envelope. | A person who can change Platform code could see results early. | Access control, append-only audit log, code review. The design states that it does not defend against a person who can change the Platform (ADR-08). | R-04 |
| 20 | Literature sources are missing or faulty. | A weak Literature Base. | Record the error per source, use another source, record the gap, use only open-access full text. | R-08 |
| 21 | The limit of one active run per project slows a team. | Low throughput in one project. | Accepted by design (ADR-13). Teams use several projects for parallel work. | R-10 |
| 22 | Documents and the system drift apart. | The team misreads the system. | The documents define the system; every change updates the documents first and is recorded in the change log. | Project risk |
| 23 | The team is small and the schedule is fixed. | Not enough time for every persona and bench. | One shared harness (ADR-02). Enable only personas with measurable value. JFE is Could. | R-13 |

Owners and triggers for each risk are an open item (O-5).

### 1.4 Re-plan

The re-plan covers the remaining work against the product scope in Report III.

- MVP: FE-01 to FE-15 and FE-17 (all Must).
- After MVP: FE-19 `method_comparison` (Should) and FE-18 Journal Fingerprint Extraction (Could).

The baseline estimate of 240 person-days stays unchanged. The team has not re-estimated the target scope. Section 1.6 lists the open items.

Remaining work by workstream:

| # | Workstream | Features | MoSCoW | Baseline WBS items it extends | Schedule |
| ----- | ----- | ----- | ----- | ----- | ----- |
| R1 | Account, workspace, collaboration, administration | FE-01, FE-02, FE-15, FE-17 | Must | 1, 2, 9 | Open item O-1 |
| R2 | Data management: dataset versions, upload, connections, data location | FE-03 | Must | 3 | Open item O-1 |
| R3 | Run management, human control, budget | FE-04, FE-05, FE-13 | Must | 5, 7 | Open item O-1 |
| R4 | Stages: dataset, hypothesis, experiment_design, execution, paper | FE-06, FE-07, FE-08, FE-09, FE-10 | Must | 4, 6 | Open item O-1 |
| R5 | Independent review loop and personas | FE-11 | Must | None (new) | Open item O-1 |
| R6 | Local Node | FE-12 | Must | None (new) | Open item O-1 |
| R7 | Dossier, approval, export | FE-14 | Must | None (new) | Open item O-1 |
| R8 | Evaluation: stage acceptance scenarios, seeded-flaw bench, paper reproduction bench, benchmark case catalogue | Report V; SM-09, SM-13, SM-14, SM-17, SM-18; BR-100, BR-101 | Must (stage acceptance); Should (benches, run on request) | 10 | Integration and system testing in Week 15 |
| R9 | Final documents and demo | The capstone reports | Must | 10.3 | Week 16 (ends 27/12/2026) |
| R10 | Method comparison research | FE-19 | Should, after MVP | None (new) | After MVP; no date |
| R11 | Journal Fingerprint Extraction | FE-18 | Could, after MVP | None (new) | After MVP; no date |

Rules for the re-plan:

- The team delivers all Must features before it starts a Should or Could feature.
- The team re-estimates each workstream at the next sprint planning (see O-1).
- The team records every scope change in the scope change log (section 1.5).

### 1.5 Scope change log

| # | Change | Reason (product) | Affected FE / BR | Impact |
| ----- | ----- | ----- | ----- | ----- |
| 1 | The pipeline has five stages (`dataset`, `hypothesis`, `experiment_design`, `execution`, `paper`). Each stage boundary has one typed, versioned, immutable hand-off object. The pipeline always starts from the `dataset` stage. | One fixed path from research case to paper lets the system trace each claim to a record and lets the team test each stage alone (BO-01, BO-02, BO-09). | FE-04, FE-06 to FE-10; BR-08, BR-11, BR-12, BR-13 | The baseline has three research stages. The `execution` stage and the `paper` stage are new. Estimate is an open item. |
| 2 | Independent review is mandatory for every object version, with verified findings and at most two fix rounds. | An AI that plans and accepts its own work confirms itself (BP-08). | FE-11; BR-35 to BR-40 | New workstream R5. The baseline had a critic role only for the AI PI. |
| 3 | The user controls a run through a preset per stage, pinned actions, presence, and one decision inbox. The AI PI decides only tentatively. | A single run-wide switch is too coarse. The user is asked too often, or loses decisions that only the user may take (BP-15). | FE-05; BR-24 to BR-34, BR-75 | Replaces run-wide modes in the baseline. Affects the frontend and orchestration workstreams. |
| 4 | A Local Node keeps local data on the user's machine and releases only aggregates through one release gate. | Private data rows must not leave the machine that holds them (BP-13). | FE-12; BR-18 to BR-22, BR-81; SM-05, SM-06 | New workstream R6. |
| 5 | A Dossier groups the accepted evidence and paper objects. It has versions and approval. Export needs an approved Dossier. | A result must not leave the project without an authorized person's approval (BP-16). | FE-14; BR-62 to BR-64, BR-79; SM-15 | New workstream R7. |
| 6 | The `paper` stage writes the PaperPack from the evidence. Numbers come from code. Claims stay under the claim ceiling. | A draft can amplify claims, drop caveats, or contain numbers that code did not make (BP-12). | FE-10; BR-65 to BR-73; SM-03, SM-04, SM-12 | The `paper` stage is part of the MVP. Estimate is an open item. |
| 7 | The system adds a tabular control layer: task family, pipeline order, research patterns, and a benchmark case catalogue of 60 sample projects. | Wrong splits and leakage make results falsely optimistic (BP-03, BP-06). | FE-06, FE-08, FE-11; BR-82 to BR-101; SM-17, SM-18 | Limits research to tabular data and four task families (BR-83). Adds acceptance work in workstream R8. |
| 8 | `method_comparison` is a Should feature, after the MVP. | It compares machine-learning methods on the same data. It is not needed for the first complete pipeline, so it must not dilute the MVP (R-14). | FE-19; BR-82, BR-96, BR-98, BR-101 | Workstream R10. The MVP does not change. |
| 9 | Journal Fingerprint Extraction (JFE) is a Could feature, after the MVP. | Journal choice is often made by feel (BP-11). The feature adds value only after the `paper` stage works. | FE-18; BR-74; BO-12; SM-16 | Workstream R11. The team keeps it out of the schedule until the MVP is accepted (R-13). |
| 10 | The system does not compare itself with human-only work, AutoML, or generic agents. | The product goal is traceable and reviewed research. The team evaluates the system by stage acceptance, the seeded-flaw bench, and the paper reproduction bench (BO-09). | BO-09; SM-09, SM-13, SM-14 | The baseline evaluation item 10.1 narrows to the benches in R8. Two catalogue cases (BC-C20, BC-R20) are user research topics under FE-19 (Should): the user compares an AutoML method with baselines on the user's own data. The exclusion covers only an evaluation of OpenAI-Scientist itself against AutoML or generic agents. |

### 1.6 Open items of the plan

See the list at the end of this file.

## 2. Management Approach

### 2.1 Project Process

Model: Scrum with two-week sprints.

Description: The team keeps a prioritized product backlog derived from the BRD, the PRD, and the architecture description. Each sprint starts with planning. It ends with a demo to the supervisor and a retrospective. The team clarifies unclear requirements with the supervisor before implementation.

*Figure 1: Scrum process: diagram to be regenerated from the design model.*

The figure shows the Scrum cycle: product backlog, sprint planning, a two-week sprint with daily standups, sprint review (demo), and retrospective.

Baseline sprint plan (kept from the original plan):

| Iteration | Focus | Expected result |
| ----- | ----- | ----- |
| Sprint 1 (Weeks 1 to 2) | Scope baseline and setup | Roles, workspace setup, requirements baseline, risk register. |
| Sprint 2 (Weeks 3 to 4) | Accounts and workspace | Passwordless sign-in, projects, members, invitations, roles. |
| Sprint 3 (Weeks 5 to 6) | Data and stage contract | Datasets, connections, stage contract and stage skeleton. |
| Sprint 4 (Weeks 7 to 8) | Hypothesis pipeline | Hypothesis stage, run management, stage checks, first run studio scenes. |
| Sprint 5 (Weeks 9 to 10) | Experiment design | Experiment design stage, acceptance, review rounds. |
| Sprint 6 (Weeks 11 to 12) | AI PI and budget | AI PI oversight, human control, token budget, self-healing. |
| Sprint 7 (Weeks 13 to 14) | Dataset pipeline and admin | Dataset stage, admin pages, notifications, integrations, monitoring. |
| Sprint 8 (Weeks 15 to 16) | Evaluation and release | Evaluation bench, system testing, deployment, final report and demo. |

The target pipeline always starts from the `dataset` stage (BR-08). The re-plan in section 1.4 supersedes the stage order of Sprints 4 to 7. Dates for the re-planned sprints are an open item (O-1).

### 2.2 Quality Management

The team uses the following approaches to control quality.

Defect prevention:

- The team reviews requirement changes before implementation.
- Every hard rule that a prompt states has a check in code (BR-13).

Reviewing:

- Every change goes through a pull request with peer review.
- Automated style, architecture-boundary, and type checks run on every change.

Unit testing covers:

- Authentication, sessions, and role checks.
- Dataset validation and versioning.
- Run and stage state transitions, budget, and self-healing.
- Stage steps, contract checks, and code-computed numbers.
- Guards, pinned actions, and action levels.

Integration testing covers:

- The Platform with its database.
- Each stage through its interface with a stubbed Platform.
- Stage events, artifacts, and live event streams.
- The Local Node pairing and release gate.
- Data connections against real services.

System testing verifies complete flows:

- A topic without a dataset through the five stages (journey J1).
- The decision inbox with a present user and an away user (J2).
- Locking a plan (J3).
- Unseal, verdict, grade, and claim ceiling (J4).
- A run on local data through the Local Node (J5).
- A project budget that reaches 100% (J6).
- Dossier approval and export (J7).

Additional quality activities:

- Sprint demo to the supervisor.
- Stage acceptance scenarios: one live run per stage with all hard checks green (SM-14).
- Connection check across stages after every stage passes: pinned objects and hashes across all stages, stale marking, and exploration candidates returning to the inbox.
- Seeded-flaw bench for reviewer precision and for the red-team catalogue. The bench capability is Must; a full evaluation round runs on request (Should) (SM-09, SM-17, SM-18).
- Paper reproduction bench, on request (Should) (SM-13).
- Continuous integration on every change.
- Final acceptance testing before deployment.

### 2.3 Training Plan

| Training Area | Participants | When, Duration | Waiver Criteria |
| ----- | ----- | ----- | ----- |
| Version control and pull-request workflow | All members | Week 1, 2 days | Mandatory |
| Backend language, web service, database access and migrations | Backend team | Week 1, 3 days | Mandatory |
| Build, task runner, test and lint tools | Backend team | Week 1, 1 day | Mandatory |
| Large language model APIs, tool calling and structured output | Backend team | Week 2, 2 days | Mandatory |
| Frontend, typing, styling and component library | Frontend team | Week 1, 3 days | Mandatory |
| Server state, live event streams and the stage event model | Frontend team | Week 3, 2 days | Mandatory |
| Container-based deployment | All members | Week 4, 1 day | Mandatory |

All entries are mandatory. The original plan states no waiver criteria. Training on statistical methods and on sandboxed code execution is an open item (O-6).

## 3. Project Deliverables

| # | Deliverable | Due Date | Notes |
| ----- | ----- | ----- | ----- |
| 1 | Requirements: BRD, PRD, business rules | Week 3 | Functional and non-functional requirements and business rules defined. |
| 2 | Architecture and stage contract | Week 5 | System architecture, logical data model, stage contract. |
| 3 | Core Features (phase 1) | Week 6 | Authentication, projects, members, datasets, connections. |
| 4 | Core Features (phase 2) | Week 10 | Run management, `hypothesis` and `experiment_design` stages, run studio. |
| 5 | Core Features (phase 3) | Week 14 | AI PI, `dataset` stage, budget, admin, notifications, integrations. |
| 6 | Integration and System Testing | Week 15 | Interface tests, flow tests, system test cases and report. |
| 7 | Deployment | Week 16 | Production system deployed. |
| 8 | Complete Documents | Week 16 | Final report, user guide, technical documentation, slides. |

Week 16 ends on 27/12/2026.

Deliverables 3 to 5 reflect the baseline scope. The target deliverables for the `execution` stage, the `paper` stage, the Local Node, the review loop, and the Dossier are in the re-plan (R4 to R7). Their due dates are an open item (O-1).

Acceptance criteria for each deliverable:

| # | Accepted when |
| ----- | ----- |
| 1, 2 | The supervisor reviews the documents and the team closes the review comments. |
| 3 to 5 | The feature passes its sprint demo and its system test flows (section 2.2). |
| 6 | The stage acceptance scenarios and the connection check pass. |
| 7 | The deployed system passes the final acceptance test. |
| 8 | The supervisor accepts the final report. |

## 4. Responsibility Assignments

| Responsibility | Lê Vũ Phương Hòa | Ngô Thành Đạt | Trần Phú Thịnh | Uông Tuấn Vũ |
| ----- | ----- | ----- | ----- | ----- |
| Project planning and tracking | A | C | I | I |
| Project Introduction and Management Plan | R | A | C | C |
| Requirements and use cases | R | A | C | C |
| Platform backend and database | A | C | I | I |
| Stage contract and skeleton | R | A | I | I |
| Research stages and AI PI | C | A | I | I |
| UI/UX design | R | I | A | C |
| Frontend workspace and admin pages | I | I | A | C |
| Run studio | I | C | A | C |
| Testing and defect management | C | C | C | A |
| Deployment and user guide | A | C | C | R |

Legend: R = Responsible (does the work); A = Accountable (owns the result and the final decision; exactly one A per row, who also does the work when the row has no R); C = Consulted (supports the work); I = Informed.

Responsibilities for the Local Node, the `execution` stage, the `paper` stage, and the Dossier are an open item (O-3).

## 5. Project Communications

| Communication Item | Who / Target | Purpose | When, Frequency | Type, Tool, Method(s) |
| ----- | ----- | ----- | ----- | ----- |
| Daily Standup | Team members | Update daily progress and blockers | Daily | Messenger / Google Meet |
| Sprint Planning | Team members | Plan tasks and goals for the sprint | Start of each sprint | Backlog board |
| Sprint Demo & Retrospective | Team, supervisor | Show working features, collect feedback | End of each sprint | Google Meet / in person |
| Supervisor Meeting | Team members, supervisors | Report progress and get technical and academic guidance | Every 2 weeks | Google Meet |
| Issue Escalation | Owner, lead, supervisor | Resolve a blocker or critical defect | Within 1 working day | Issue tracker + direct message |
| Scope Change | Team, supervisor | Agree on any change to scope, estimate, or schedule | When a change is proposed | Entry in the scope change log (section 1.5), reviewed at the next supervisor meeting |

## 6. Configuration Management

### 6.1 Document Management

The team manages project documents (BRD, PRD, architecture description, glossary, traceability matrix, and reports) as documentation-as-code.

- Documents are Markdown files under version control.
- Every documentation change is recorded in a change log with its date, purpose, affected documents, and validation result.
- A traceability matrix links business objectives to business rules, functional requirements, non-functional requirements, and architecture decisions.
- A documentation check verifies links, cross-references, and terminology before each change is accepted. Scripted identifier checks verify that every cited identifier exists.
- The team updates the requirement documents before it changes the design or the reports.

### 6.2 Source Code Management

- The team manages source code with Git.
- Work happens on short-lived feature branches and goes through pull requests with peer review.
- The release branch receives changes only after the continuous integration checks pass.
- History is never rewritten.
- Secrets are never stored in the repository.
- Whether the frontend has the same automated checks as the backend is an open item (O-7).

### 6.3 Tools & Infrastructures

| Category | Tools / Infrastructure |
| ----- | ----- |
| Technology | A web frontend with a typed language and a component library; a web service for the backend and the stages |
| Database | A relational database with schema migrations |
| File storage | Local volume or object storage |
| AI | A language model service with keys supplied by the Platform Admin; scholarly metadata service for literature (open-access full text only) |
| Email | A transactional email service |
| Local data | The Local Node, which runs on the user's machine without a container runtime (ADR-10) |
| Code execution | An isolated sandbox for analysis programs (BR-50) |
| IDEs/Editors | Visual Studio Code |
| Quality | Automated unit and integration tests, style and type checkers, continuous integration |
| Diagramming | Draw.io, Mermaid |
| Documentation | Markdown under version control; shared document storage |
| Version Control | Git with a hosted remote |
| Deployment | Container-based deployment |
| Project management | A backlog board and an issue tracker |

## Open items

| # | Item | Why it is open |
| ----- | ----- | ----- |
| O-1 | Dates and effort for re-plan workstreams R1 to R7, R10, and R11, and the re-ordered sprints. | The sources give no dates or estimates for the target scope. The team will re-estimate at sprint planning. |
| O-2 | Effort for requirements analysis, system design, project management, and report writing. | The baseline WBS has no rows for them. |
| O-3 | Responsibility assignments for the Local Node, the `execution` stage, the `paper` stage, the review loop, and the Dossier. | The baseline table has no rows for them. |
| O-4 | Whether baseline items 3.2 (database servers and cloud warehouse), 3.4 (time-series connectors), and 9.2 (chat-tool webhooks) stay in scope. | The architecture description lists a cloud spreadsheet and drive service as the data connection. BR-17 requires an authorized source. No FE lists the other connector types. |
| O-5 | Risk owners, triggers, and probability and impact ratings. | The BRD and architecture give consequences and responses only. |
| O-6 | Training on statistical methods and on sandboxed code execution. | The target scope needs them (FE-09). The baseline training plan has no entry. |
| O-7 | Continuous integration for the frontend. | Not confirmed from the sources. |
| O-8 | Closed. Report III states the thresholds for SM-02, SM-17, and SM-18. | Report III, Open items 1 and 3. |

# V. Software Testing Documentation

This section follows a light form of ISO/IEC/IEEE 29119-3. It plans the tests of OpenAI-Scientist as specified in Report III. It defines the test case IDs (TC-xx). Requirement IDs (business requirement BR, feature FE, functional requirement FR, non-functional requirement NFR), use cases (UC-xx), system rules (SR-xx), common requirements (CR-xx) and messages (MSG-xx) come from Report III. Design and quality scenarios are in Report IV. Plan, roles and schedule are in Report II.

Priority uses MoSCoW. The minimum viable product (MVP) is FE-01 to FE-15 and FE-17. FE-18 (Journal Fingerprint Extraction) is Could. FE-19 (method comparison) is Should. Both come after the MVP.

The test cases below are designed, not executed. The status of every test case is "Not run" until execution.

## 1. Scope of testing

### 1.1 In scope, by feature

Every feature of the product is in scope. The "Test cases" column lists the cases that cover the functional requirements of the feature (section 4.1.2). Stage acceptance, benchmark and non-functional cases add to these (sections 4.1.3 to 4.1.5).

| FE | Feature | MoSCoW | Test cases |
|---|---|---|---|
| FE-01 | Account and access | Must | TC-01, TC-02, TC-95, TC-96 |
| FE-02 | Project workspace and members | Must | TC-03, TC-04, TC-05, TC-09 |
| FE-03 | Data management | Must | TC-06, TC-07, TC-08 |
| FE-04 | Research case and run management | Must | TC-09, TC-10, TC-11, TC-12, TC-13, TC-14, TC-18, TC-98, TC-100 |
| FE-05 | Human control | Must | TC-14, TC-15, TC-16, TC-17, TC-49, TC-97, TC-98, TC-99, TC-100 |
| FE-06 | Dataset stage | Must | TC-18, TC-42, TC-43 |
| FE-07 | Hypothesis stage and Literature Base | Must | TC-19, TC-44 |
| FE-08 | Experiment design stage and Lock | Must | TC-20, TC-21, TC-45, TC-46 |
| FE-09 | Execution stage | Must | TC-22, TC-23, TC-24 |
| FE-10 | Paper stage | Must | TC-25, TC-26, TC-47 |
| FE-11 | Independent review loop and personas | Must | TC-27, TC-28, TC-29, TC-58, TC-59, TC-61, TC-101 |
| FE-12 | Local Node | Must | TC-08, TC-30, TC-31, TC-48 |
| FE-13 | Budget and cost | Must | TC-32, TC-33, TC-34 |
| FE-14 | Dossier, approval and export | Must | TC-35, TC-36 |
| FE-15 | Collaboration | Must | TC-37, TC-38 |
| FE-17 | Administration and monitoring | Must | TC-05, TC-12, TC-39 |
| FE-18 | Journal Fingerprint Extraction (JFE) | Could, after the MVP | TC-40 |
| FE-19 | Method comparison research (`method_comparison`) | Should, after the MVP | TC-20, TC-41 |

### 1.2 In scope, by quality focus

The product promises three things: no error is hidden, every claim has a source and every run can be run again (Report III, section 1.1). The tests therefore treat the following quality focuses as high-risk.

| Quality focus | What the tests check | Test cases |
|---|---|---|
| Correctness of the verdict, grade and claim ceiling | Code computes each verdict, each grade (A to D) and each claim ceiling as the locked rules require. | TC-23 |
| Seal and unseal | The agent sees no confirmatory estimate before unseal. An early unseal is rejected. | TC-22, TC-82 |
| Leakage and pipeline order | The system finds seeded leakage and blocks seeded pipeline order violations. | TC-42, TC-43, TC-45, TC-58 |
| Isolation of the execution sandbox | The agent touches real data only through aggregates or the full program. | TC-22 |
| Privacy of local data | No row of `local` data leaves the Local Node. The release gate rejects small cells and differencing. | TC-30, TC-48, TC-56, TC-84, TC-85 |
| Secrets | No key or secret appears in a prompt, log, trace or output. | TC-39, TC-81 |
| Reproducibility | The replicator reproduces the hash of the EvidenceBundle. A re-run gives the same hash. | TC-23, TC-91 |
| Integrity of the paper | Every number is a reference. Every claim is inside the ceiling. Every citation resolves. | TC-25, TC-92 |
| Human control | Pinned actions stay `must_ask`. The AI PI decides only unpinned items. A pinned item that waits does not end the run before its wait deadline. At the deadline the run ends with gaps and nobody decides the item. | TC-16, TC-17, TC-94, TC-97, TC-98, TC-99, TC-100 |
| Dossier | A Dossier version is checked, approved by the review settings and exported only when approved. | TC-35, TC-36 |
| Review loop | The loop is bounded to two revision rounds and gives each finding a verified status. | TC-27, TC-93 |

### 1.3 Out of scope

| Item | Reason |
|---|---|
| Non-tabular data; new data collection design; full systematic reviews; full text behind paywalls; organizations and multi-tenancy; automatic submission to publishers; evaluating OpenAI-Scientist itself against human-only, AutoML or generic-agent systems; the task families ranking, survival, forecasting and anomaly | These items are outside the product scope (Report III, section 1.1; BR-83). TC-26 checks that no submission function exists. |
| Quality of model-generated text beyond the code checks, the review loop and the benchmarks | The product does not promise that the science is always right. It promises that no error is hidden. |
| Availability and delivery of third-party services (model provider, scholarly metadata, public data, identity, email) | The tests inject faults and check the reaction of the system (TC-12, TC-19, TC-76). They do not test the services. |
| Backup and retention of research data; capacity planning beyond NFR-01; handling of data by the model provider | Report III does not specify them (Report III, Open items). |
| Cross-browser visual testing | The requirements specify no browser matrix (Open item 7). |
| A full evaluation round on the seeded-flaw bench, the paper reproduction bench and the benchmark case catalogue as a routine run | The bench capability is Must. A full evaluation round is Should and runs on request. It is not an MVP release criterion (TC-58, TC-60, TC-64 to TC-74). The wave 1 cases TC-62 and TC-63 are Must. |
| Execution of FE-18 and FE-19 test cases | The cases are written (TC-40, TC-41, TC-64, TC-74). They run after the MVP. |

## 2. Test strategy

### 2.1 Test types and levels

The strategy is risk-based. Cases for the science-critical quality focuses in section 1.2 are the first to run and the last to drop. Each level maps to the source of its test conditions. L1 to L4 are test levels by scope. L5 (benchmarks) and L6 (NFR measurement) are test types that run at system scope. The numbering groups them by purpose.

| Level | Test type | What it checks | Source of conditions | Test cases |
|---|---|---|---|---|
| L1 | Unit and contract checks | Validators, calculators and contract items in isolation: code-computed numbers, verdict, grade, ceiling, split rules, release gate rules, hash checks. | FR statements verified by Test; hard rules that exist in a prompt and in a code validator (NFR-21) | TC-15, TC-23, TC-25, TC-42 to TC-46, TC-97 |
| L2 | Integration tests | The Platform with its database; each stage through its interface with a stubbed Platform; stage events and live event streams; the Local Node pairing and release gate; data connections against real services. | Use cases and FR statements | TC-03, TC-06 to TC-08, TC-10, TC-30, TC-32, TC-34, TC-38, TC-48 |
| L3 | System tests | Complete use case flows through the web app, the Platform and the stage engines. The seven system flows of Report II (section 2.2) are covered as listed below. | UC-01 to UC-41 | TC-01 to TC-41, TC-47, TC-49, TC-95, TC-96, TC-98 to TC-100 |
| L4 | Acceptance tests | The stage acceptance scenario of each stage and of the Local Node, then the connection check across stages. | Stage acceptance scenarios | TC-50 to TC-57 |
| L5 | Benchmarks | The seeded-flaw bench with the red-team catalogue, the paper reproduction bench and the benchmark case catalogue. The bench capability and the wave 1 cases are Must (TC-29, TC-59, TC-61, TC-62, TC-63, TC-101). A full evaluation round is Should and runs on request (TC-58, TC-60, TC-64 to TC-74). | BR-40, BR-100, BR-101; SM-09, SM-13, SM-17, SM-18 | TC-29, TC-58 to TC-74, TC-101 |
| L6 | NFR measurement | Measurement of each NFR against its measurable criterion. | NFR-01 to NFR-31 | TC-75 to TC-94 |

Manual tests cover usability, accessibility and the user-interface parts of the system flows. The requirements specify no automated browser test of the web app. The plan therefore treats user-interface tests as manual tests (Demonstration or Inspection).

Each case uses the verification method that Report III states for its FRs: Test (T), Demonstration (D), Inspection (I) or Analysis (A). Each case states its method.

System flows of Report II and their cases:

| System flow | Cases |
|---|---|
| A topic without a dataset through the five stages | TC-09, TC-18, TC-19, TC-20, TC-21, TC-22, TC-25, TC-57 |
| Decision inbox with a user who is present and a user who is away | TC-16, TC-17, TC-98, TC-99, TC-100 |
| Lock of a plan | TC-21 |
| Unseal, verdict, grade and claim ceiling | TC-22, TC-23 |
| A run on local data through the Local Node | TC-08, TC-30, TC-31, TC-56 |
| A project budget that reaches 100% | TC-33 |
| Dossier approval and export | TC-35, TC-36 |

#### 2.1.1 Stage acceptance scenarios and the connection check

Each stage is accepted alone. The scenario runs the stage engine alone. The upstream hand-off object is a frozen fixture. The model is a live model. The user follows a script. A stage passes when one live run of its scenario ends with every hard check green.

- A hard check is a check by code on the created object. Examples: totals add up, references resolve, tiers are right, hashes are equal.
- An expectation that depends on model judgment or on a real signal is reported only. It does not decide the result.
- Each count threshold of a scenario is also a contract item. A threshold that is not met is a gap in the output, not a failed run.

The connection check runs only after every stage passes (TC-57).

#### 2.1.2 Benchmarks

The bench capability is Must: the seeded-flaw bench, the red-team catalogue and the measure of persona precision exist, because the review loop uses that precision (FR-77, FR-135 to FR-137). A full evaluation round on the benches is Should. It runs on request and is not an MVP release criterion. SM-17 and SM-18 are measured when such a round runs.

| Benchmark | Purpose | Measure | Cases |
|---|---|---|---|
| Seeded-flaw bench | Measure the precision of each reviewer persona. Measure detection and blocking of the flaws in the red-team catalogue in three groups: data, experiment and inference (BR-100, FR-135). | Persona precision not below the minimum (SM-09). Detection rate of seeded leakage (SM-17). Block rate of seeded pipeline order violations (SM-18). Targets: at least 90% for SM-17 and 100% for SM-18. | TC-29, TC-58, TC-59 |
| Paper reproduction bench | Compare the output of the system with a published paper that has open data. | Direction and interval overlap of the primary estimate; checklist coverage; major flaws by the Reviewer 2 rubric (SM-13). Runs on request. | TC-60 |
| Benchmark case catalogue | 60 sample projects. Each is a test case of a research pattern, not a separate flow (BR-101, FR-138). | Pattern mechanics and hard checks per case (section 4.1.3). | TC-61 to TC-74 |

#### 2.1.3 NFR measurement

Each NFR has a measurable criterion in Report III. The cases TC-75 to TC-94 give the procedure. Measurements that Report III marks "pre-release test environment" run in such an environment before the release. The release condition is that every NFR has a measured result against its approved threshold.

### 2.2 Entry and exit criteria

| Level | Entry criteria | Exit criteria |
|---|---|---|
| L1 Unit and contract | The unit under test is complete. Fixtures for the rule exist. | All cases of the level are run. No S1 or S2 defect is open (section 5.2). |
| L2 Integration | L1 cases of the same area pass. A test database and a stubbed Platform or scripted model provider are ready. | All cases of the level are run. No S1 or S2 defect is open. |
| L3 System | L2 cases of the same area pass. The feature runs in a test environment. | Every Must FR of the feature has at least one passing case, or a recorded Inspection, Analysis or Demonstration. No S1 defect is open. |
| L4 Acceptance | All L3 cases of the feature pass. The frozen upstream fixture and a real model profile are ready. The budget for live runs is approved. | One live run of the stage scenario ends with every hard check green. The connection check passes after all stages pass. |
| L5 Benchmarks | The system passes L4. Benchmark data and the seeded-flaw catalogue are ready. | The measures are reported. SM-17 and SM-18 have no pass or fail until the team defines targets (Open item 1). |
| L6 NFR measurement | A pre-release test environment is ready where the NFR requires it. The measured function passes L3. | Every NFR has a measured result against its criterion. |

Release criteria (MVP):

- Every stage and the Local Node pass their acceptance scenario, and then the connection check passes.
- Every Must FR has at least one passing test case, by the traceability matrix in section 4.1.2. FR-135 to FR-137 are covered by TC-101 (Must), which checks the bench capability on a minimal case set. The full evaluation round in TC-58 runs on request and is not part of the MVP release criteria.
- Every NFR has a measured result against its approved threshold.
- No `blocking` finding is open in the release documents.

Suspension and resumption criteria:

- The team suspends the testing of an area when an S1 defect blocks more than half of the planned cases of the area.
- The team resumes after the fix is verified by a re-test of the failed case and a regression run of the area.

### 2.3 Supporting tools

| Purpose | Tool category |
|---|---|
| Automated tests of the Platform, the stage engines and the Local Node | Test runner for the backend language |
| Automated tests of the web app components | Test runner for the frontend language |
| Style, architecture-boundary and type checks | Static analysis tools; they run on every change |
| Integration of every change | Continuous integration service |
| Model and source service control | Scripted model provider and scripted sources (Fixture D) |
| Isolated execution | Execution sandbox |
| Network observation | Packet capture tool (NFR-12) |
| Load and timing measurement | Load generator and a clock shared by the measuring components (NFR-01, NFR-02) |
| Accessibility checks | Automatic and manual accessibility evaluation tools (NFR-18) |
| Benchmark runs | Benchmark runner for the seeded-flaw bench and the catalogue |
| Traceability | Traceability matrix (section 4.1.2) |
| Defect management | Defect tracker (section 5.2) |

## 3. Test plan

### 3.1 Human resources

The roles follow the responsibility assignments of Report II (section 4). The testing and defect management owner is the Frontend and QA member.

| Member | Role in testing | Responsibility |
|---|---|---|
| Uông Tuấn Vũ | Test lead; defect management owner | Test cases, manual testing, test reports, defect triage. |
| Lê Vũ Phương Hòa | Backend test engineer | Test plan input, run and stage engine tests. |
| Ngô Thành Đạt | Backend and data test engineer | Data and connector tests, benchmarks. |
| Trần Phú Thịnh | Frontend test engineer | Component and user-interface tests. |
| Supervisors | Acceptance reviewers | Observe the sprint demo and the final acceptance test. |

Report II lists the responsibilities for the Local Node, the execution stage, the paper stage and the Dossier as an open item. The test responsibilities for these areas follow that open item (Open item 8).

### 3.2 Test environment

| Environment category | Use |
|---|---|
| Developer workstation | L1 and L2 tests during development. |
| Automated test lane | L1 to L3 tests on every change. It uses an isolated database, a scripted model provider and scripted sources. It makes no call to a live model provider. |
| Pre-release test environment | L3, L4 and L6 tests, including load, restart and availability measurements. |
| Live model lane | Stage acceptance runs and benchmarks with a real model profile. These runs spend budget and run on request or at acceptance. |
| Execution sandbox | Isolated runs of the execution stage (TC-22, TC-81). |
| Local Node machine | A separate machine with no container runtime, a watched folder and a packet capture tool (TC-08, TC-56, TC-84). |
| Browsers | Not specified (Open item 7). |

Test data:

- Fixture A: a project with a Project Manager, a Researcher and a Reviewer, and a Platform Admin who is not a member.
- Fixture B: a sample tabular dataset with a binary outcome, a group variable, a time variable and planted anomalies, with a record of the expected findings.
- Fixture C: one frozen, accepted object of each hand-off type, for runs of a stage alone.
- Fixture D: a scripted model provider and scripted scholarly metadata sources that return planned answers or errors.
- Fixture E: result sets with known expected verdicts and grades.
- Sample projects of the benchmark case catalogue (BC-xx), the seeded-flaw catalogue and published papers with open data.
- Data policy: the tests use no real personal data. Planted keys are fake.

### 3.3 Test milestones

The milestones follow the deliverables and weeks of Report II (section 3). Report II keeps the baseline weeks. It states that the dates of the re-planned sprints are an open item (Report II, O-1). The plan adds no dates.

| Milestone | Report II deliverable | Week | Test content |
|---|---|---|---|
| M1 | 3 Core Features (phase 1) | 6 | L1 and L2 cases for FE-01, FE-02 and FE-03: TC-01 to TC-08, TC-95, TC-96. |
| M2 | 4 Core Features (phase 2) | 10 | Cases for run management (FE-04), the `hypothesis` stage and the `experiment_design` stage: TC-09 to TC-11, TC-19 to TC-21, TC-44 to TC-46, TC-98 to TC-100. |
| M3 | 5 Core Features (phase 3) | 14 | Cases for the AI PI, the `dataset` stage, budget, administration and notifications: TC-05, TC-14, TC-15, TC-17, TC-18, TC-32 to TC-34, TC-38, TC-39, TC-42, TC-43, TC-97. |
| M4 | 6 Integration and System Testing | 15 | L3 system flows, L4 acceptance, L6 measurement and the test summary report (section 5.1). |
| M5 | 7 Deployment; 8 Complete Documents | 16 (ends December 27, 2026) | Final acceptance test before deployment. Final test summary report. |

The baseline plan has no sprint for the execution stage, the paper stage, the review loop, the Local Node and the Dossier. The cases of these areas (TC-22 to TC-31, TC-35 to TC-37, TC-47 to TC-49, TC-50 to TC-57) take their dates from the re-plan (Open item 8).

### 3.4 Test risks

| Risk | Effect | Mitigation |
|---|---|---|
| Output of a live model varies between runs. | An acceptance run fails for a reason outside the stage. | Only hard checks decide the result. Judgment-based expectations are reported only. |
| Live runs cost budget. | The team cannot repeat live runs freely. | Run live cases on request or at acceptance. Use the scripted model provider for L1 to L3. |
| The seeded-flaw catalogue does not mark which flaws count as leakage. | SM-17 cannot be computed. | Classify the flaws before the evaluation round (Open item 2). |
| The benchmark case catalogue has no sample data or expected results yet. | Cases TC-62 to TC-74 check pattern mechanics only. | Define sample data per case before the benchmark run (Open item 3). |
| Four members cover development and testing. | No member tests independently. | The test lead reviews cases written by others. Supervisors observe acceptance (Open item 9). |

## 4. Test cases

### 4.1 Summary

Test case IDs have the form TC-xx. Each case has the status "Not run".

Conventions:

- Level: L1 to L6 as in section 2.1. System cases are L3.
- Method: Test, Demonstration, Inspection or Analysis.
- The cases of the benchmark case catalogue are ordered with wave 1 first.

#### 4.1.1 Test case groups

| Group | Cases | Basis |
|---|---|---|
| Use case scenarios | TC-01 to TC-41 (TC-nn covers UC-nn) | Report III, section 2.2 |
| Rule-level cases | TC-42 to TC-49 | FRs that a use case scenario does not fully check |
| Stage acceptance and connection check | TC-50 to TC-57 | Stage acceptance scenarios |
| Benchmarks | TC-58 to TC-61 | Seeded-flaw bench, paper reproduction bench, catalogue |
| Benchmark case catalogue | TC-62 to TC-74 | BC-xx, wave 1 first |
| NFR measurement | TC-75 to TC-94 | NFR-01 to NFR-31 |
| Additional cases | TC-95 to TC-101 | FR-146 (Google sign-in), FR-147 to FR-150 (preset levels and floors), FR-178 and FR-262 (a waiting pinned item), FR-263 to FR-266 (the wait deadline of a pinned item), FR-135 to FR-137 (the bench capability) |

Summary of all cases:

| TC | Title | UC | Level | Method | Priority | Status |
|---|---|---|---|---|---|---|
| TC-01 | Sign in with an email address | UC-01 | L3 | Test | Must | Not run |
| TC-02 | View project metadata as Platform Admin | UC-02 | L3 | Test | Must | Not run |
| TC-03 | Manage members and archive a project | UC-03 | L2 | Test | Must | Not run |
| TC-04 | Configure project settings | UC-04 | L3 | Demonstration | Must | Not run |
| TC-05 | Review audit log, health and operating metrics | UC-05 | L3 | Test | Must | Not run |
| TC-06 | Upload a dataset | UC-06 | L2 | Test | Must | Not run |
| TC-07 | Import from a data connection | UC-07 | L2 | Test | Must | Not run |
| TC-08 | Pair a Local Node and register local data | UC-08 | L2 | Test; Demonstration | Must | Not run |
| TC-09 | Start a run from a research case | UC-09 | L3 | Test | Must | Not run |
| TC-10 | Amend a research case | UC-10 | L2 | Test | Must | Not run |
| TC-11 | Accept a hand-off object and mark downstream objects stale | UC-11 | L3 | Test | Must | Not run |
| TC-12 | Monitor and recover a run | UC-12 | L3 | Test | Must | Not run |
| TC-13 | Cancel a run | UC-13 | L3 | Test | Must | Not run |
| TC-14 | Choose the next step | UC-14 | L3 | Test; Demonstration | Must | Not run |
| TC-15 | Set preset and presence | UC-15 | L1, L3 | Test | Must | Not run |
| TC-16 | Answer a decision inbox item | UC-16 | L3 | Test | Must | Not run |
| TC-17 | Confirm or overturn a tentative decision | UC-17 | L3 | Test | Must | Not run |
| TC-18 | Run the dataset stage | UC-18 | L3 | Test | Must | Not run |
| TC-19 | Run the hypothesis stage | UC-19 | L3 | Test; Demonstration | Must | Not run |
| TC-20 | Run the experiment_design stage | UC-20 | L3 | Test | Must | Not run |
| TC-21 | Lock a plan | UC-21 | L3 | Test | Must | Not run |
| TC-22 | Run the execution stage | UC-22 | L3 | Test | Must | Not run |
| TC-23 | Read verdict, grade and claim ceiling | UC-23 | L1, L3 | Test | Must | Not run |
| TC-24 | Triage exploration candidates | UC-24 | L3 | Test | Must | Not run |
| TC-25 | Run the paper stage | UC-25 | L1, L3 | Test | Must | Not run |
| TC-26 | Decide on submission | UC-26 | L3 | Inspection | Must | Not run |
| TC-27 | Run the review loop | UC-27 | L3 | Test | Must | Not run |
| TC-28 | Invoke a persona on an object | UC-28 | L3 | Test | Must | Not run |
| TC-29 | Run the benchmarks | UC-29 | L5 | Analysis | Must | Not run |
| TC-30 | Release an aggregate from local data | UC-30 | L2 | Test | Must | Not run |
| TC-31 | Handle a Local Node that is offline or revoked | UC-31 | L3 | Test | Must | Not run |
| TC-32 | Warn on and enforce budgets | UC-32 | L2 | Test | Must | Not run |
| TC-33 | Decide extra spend | UC-33 | L3 | Test | Must | Not run |
| TC-34 | Set the spending ceiling and read the ledger | UC-34 | L2 | Test | Must | Not run |
| TC-35 | Review and approve a Dossier | UC-35 | L3 | Test | Must | Not run |
| TC-36 | Export a Dossier | UC-36 | L3 | Test | Must | Not run |
| TC-37 | Comment on an object | UC-37 | L3 | Test | Must | Not run |
| TC-38 | Receive notifications | UC-38 | L2 | Test | Must | Not run |
| TC-39 | Manage users, models and keys | UC-39 | L3 | Test; Demonstration | Must | Not run |
| TC-40 | Build a journal profile | UC-40 | L3 | Test | Could | Not run |
| TC-41 | Compare methods | UC-41 | L3 | Test | Should | Not run |
| TC-42 | Split by power and group integrity | UC-18 | L1 | Test | Must | Not run |
| TC-43 | Dataset checks that do not use the outcome | UC-18 | L1 | Test | Must | Not run |
| TC-44 | Hypothesis testability rules | UC-19 | L1 | Test | Must | Not run |
| TC-45 | Pipeline order and evidence families | UC-20 | L1 | Test | Must | Not run |
| TC-46 | Rare-event metrics, calibration and baselines | UC-20 | L1 | Test | Must | Not run |
| TC-47 | Paper declarations, reporting checklist and writing rules | UC-25 | L3 | Test; Inspection | Must | Not run |
| TC-48 | Disclosure modes, release log and model input | UC-30 | L2 | Test | Must | Not run |
| TC-49 | Same path for user and agent; fitness acceptance; assumptions | UC-16 | L3 | Test | Must | Not run |
| TC-50 | Acceptance: harness | n/a | L4 | Test | Must | Not run |
| TC-51 | Acceptance: dataset stage | n/a | L4 | Test | Must | Not run |
| TC-52 | Acceptance: hypothesis stage | n/a | L4 | Test | Must | Not run |
| TC-53 | Acceptance: experiment_design stage | n/a | L4 | Test | Must | Not run |
| TC-54 | Acceptance: execution stage | n/a | L4 | Test | Must | Not run |
| TC-55 | Acceptance: paper stage | n/a | L4 | Test | Must | Not run |
| TC-56 | Acceptance: Local Node | n/a | L4 | Test | Must | Not run |
| TC-57 | Connection check across stages | n/a | L4 | Test | Must | Not run |
| TC-58 | Seeded-flaw bench and red-team catalogue (evaluation round) | UC-29 | L5 | Analysis | Should | Not run |
| TC-59 | Negative test per research pattern | UC-29 | L5 | Test | Must | Not run |
| TC-60 | Paper reproduction bench | n/a | L5 | Analysis | Should | Not run |
| TC-61 | Benchmark case catalogue inspection | n/a | L5 | Inspection | Must | Not run |
| TC-62 | Benchmark case BC-C01 (wave 1) | n/a | L5 | Test | Must | Not run |
| TC-63 | Benchmark case BC-C05 (wave 1) | n/a | L5 | Test | Must | Not run |
| TC-64 | Benchmark case BC-C07 (wave 1, Should) | n/a | L5 | Test | Should | Not run |
| TC-65 | Benchmark case BC-R01 (wave 2) | n/a | L5 | Test | Should | Not run |
| TC-66 | Benchmark case BC-R06 (wave 2) | n/a | L5 | Test | Should | Not run |
| TC-67 | Benchmark case BC-R08 (wave 2) | n/a | L5 | Test | Should | Not run |
| TC-68 | Benchmark case BC-I01 (wave 2) | n/a | L5 | Test | Should | Not run |
| TC-69 | Benchmark case BC-I08 (wave 2) | n/a | L5 | Test | Should | Not run |
| TC-70 | Benchmark case BC-I18 (wave 2) | n/a | L5 | Test | Should | Not run |
| TC-71 | Benchmark case Classification cases after wave 2 (parameterized) | n/a | L5 | Test | Should | Not run |
| TC-72 | Benchmark case Regression cases after wave 2 (parameterized) | n/a | L5 | Test | Should | Not run |
| TC-73 | Benchmark case Rare-event cases after wave 2 (parameterized) | n/a | L5 | Test | Should | Not run |
| TC-74 | Benchmark case Method comparison cases (Should, after MVP, parameterized) | n/a | L5 | Test | Should | Not run |
| TC-75 | NFR measurement: Performance | n/a | L6 | Test | Must | Not run |
| TC-76 | NFR measurement: Run termination and failure handling | n/a | L6 | Test | Must | Not run |
| TC-77 | NFR measurement: Spending within ceilings | n/a | L6 | Test | Must | Not run |
| TC-78 | NFR measurement: Availability | n/a | L6 | Test | Must | Not run |
| TC-79 | NFR measurement: Hash stability after restart | n/a | L6 | Test | Must | Not run |
| TC-80 | NFR measurement: Project isolation | n/a | L6 | Test | Must | Not run |
| TC-81 | NFR measurement: Secrets outside the Platform | n/a | L6 | Test | Must | Not run |
| TC-82 | NFR measurement: Seal before unseal | n/a | L6 | Test | Must | Not run |
| TC-83 | NFR measurement: Audit log completeness | n/a | L6 | Test | Must | Not run |
| TC-84 | NFR measurement: Privacy of local data and release log | n/a | L6 | Test | Must | Not run |
| TC-85 | NFR measurement: Small-cell and differencing rejection | n/a | L6 | Test | Must | Not run |
| TC-86 | NFR measurement: Usability | n/a | L6 | Test | Must | Not run |
| TC-87 | NFR measurement: Accessibility | n/a | L6 | Test | Must | Not run |
| TC-88 | NFR measurement: Localization | n/a | L6 | Test | Must | Not run |
| TC-89 | NFR measurement: Maintainability inspection | n/a | L6 | Inspection | Must | Not run |
| TC-90 | NFR measurement: Observability | n/a | L6 | Test | Must | Not run |
| TC-91 | NFR measurement: Replayability | n/a | L6 | Test | Must | Not run |
| TC-92 | NFR measurement: Integrity of the PaperPack | n/a | L6 | Test | Must | Not run |
| TC-93 | NFR measurement: Review loop integrity | n/a | L6 | Test | Must | Not run |
| TC-94 | NFR measurement: AI PI limits | n/a | L6 | Test | Must | Not run |
| TC-95 | Sign in with a Google account | UC-01 | L3 | Test | Must | Not run |
| TC-96 | One user for both sign-in methods | UC-01 | L3 | Test | Must | Not run |
| TC-97 | Preset level table and floors | UC-15 | L1 | Test | Must | Not run |
| TC-98 | A waiting pinned item does not end the run before its deadline | UC-12, UC-17 | L3 | Test | Must | Not run |
| TC-99 | Reminder before the wait deadline of a pinned item | UC-16, UC-38 | L3 | Test | Must | Not run |
| TC-100 | A pinned item expires unanswered and the run ends with gaps | UC-12, UC-16 | L3 | Test | Must | Not run |
| TC-101 | Seeded-flaw bench capability check | UC-29 | L5 | Test | Must | Not run |

#### 4.1.2 Traceability: functional requirements to test cases

Every Must FR has at least one test case. The table lists each FR with its feature, MoSCoW priority and covering cases. Stage acceptance cases (TC-50 to TC-57) add coverage per feature (section 4.1.3).

| FR | FE | MoSCoW | Test cases |
|---|---|---|---|
| FR-01 | FE-01 | Must | TC-01 |
| FR-02 | FE-01 | Must | TC-01 |
| FR-03 | FE-01 | Must | TC-02 |
| FR-04 | FE-02 | Must | TC-03 |
| FR-05 | FE-02 | Must | TC-03 |
| FR-06 | FE-02 | Must | TC-03 |
| FR-07 | FE-02 | Must | TC-05 |
| FR-08 | FE-02 | Must | TC-04, TC-99 |
| FR-09 | FE-03 | Must | TC-06 |
| FR-10 | FE-03 | Must | TC-07 |
| FR-11 | FE-03 | Must | TC-07 |
| FR-12 | FE-03 | Must | TC-08 |
| FR-13 | FE-04 | Must | TC-09 |
| FR-14 | FE-04 | Must | TC-09 |
| FR-15 | FE-04 | Must | TC-18 |
| FR-16 | FE-04 | Must | TC-09 |
| FR-17 | FE-04 | Must | TC-10 |
| FR-18 | FE-04 | Must | TC-11 |
| FR-19 | FE-04 | Must | TC-11 |
| FR-20 | FE-04 | Must | TC-12 |
| FR-21 | FE-04 | Must | TC-12 |
| FR-22 | FE-04 | Must | TC-13 |
| FR-23 | FE-04 | Must | TC-14 |
| FR-24 | FE-04 | Must | TC-12 |
| FR-25 | FE-05 | Must | TC-15 |
| FR-26 | FE-05 | Must | TC-15 |
| FR-27 | FE-05 | Must | TC-16 |
| FR-28 | FE-05 | Must | TC-16 |
| FR-29 | FE-05 | Must | TC-16 |
| FR-30 | FE-05 | Must | TC-16 |
| FR-31 | FE-05 | Must | TC-17 |
| FR-32 | FE-05 | Must | TC-17 |
| FR-33 | FE-05 | Must | TC-49 |
| FR-34 | FE-05 | Must | TC-49 |
| FR-35 | FE-05 | Must | TC-14 |
| FR-36 | FE-05 | Must | TC-49 |
| FR-37 | FE-06 | Must | TC-18 |
| FR-38 | FE-06 | Must | TC-43 |
| FR-39 | FE-06 | Must | TC-18 |
| FR-40 | FE-06 | Must | TC-18 |
| FR-41 | FE-06 | Must | TC-18, TC-42 |
| FR-42 | FE-06 | Must | TC-42 |
| FR-43 | FE-07 | Must | TC-19 |
| FR-44 | FE-07 | Must | TC-19 |
| FR-45 | FE-07 | Must | TC-19 |
| FR-46 | FE-08 | Must | TC-20 |
| FR-47 | FE-08 | Must | TC-20 |
| FR-48 | FE-08 | Must | TC-21 |
| FR-49 | FE-08 | Must | TC-21 |
| FR-50 | FE-09 | Must | TC-22 |
| FR-51 | FE-09 | Must | TC-22 |
| FR-52 | FE-09 | Must | TC-22 |
| FR-53 | FE-09 | Must | TC-22 |
| FR-54 | FE-09 | Must | TC-23 |
| FR-55 | FE-09 | Must | TC-23 |
| FR-56 | FE-09 | Must | TC-22 |
| FR-57 | FE-09 | Must | TC-24 |
| FR-58 | FE-09 | Must | TC-24 |
| FR-59 | FE-09 | Must | TC-24 |
| FR-60 | FE-09 | Must | TC-23 |
| FR-61 | FE-09 | Must | TC-23 |
| FR-62 | FE-10 | Must | TC-25 |
| FR-63 | FE-10 | Must | TC-25 |
| FR-64 | FE-10 | Must | TC-25 |
| FR-65 | FE-10 | Must | TC-25 |
| FR-66 | FE-10 | Must | TC-25 |
| FR-67 | FE-10 | Must | TC-47 |
| FR-68 | FE-10 | Must | TC-47 |
| FR-69 | FE-10 | Must | TC-47 |
| FR-70 | FE-10 | Must | TC-26 |
| FR-71 | FE-11 | Must | TC-27 |
| FR-72 | FE-11 | Must | TC-27 |
| FR-73 | FE-11 | Must | TC-27 |
| FR-74 | FE-11 | Must | TC-27 |
| FR-75 | FE-11 | Must | TC-27 |
| FR-76 | FE-11 | Must | TC-27 |
| FR-77 | FE-11 | Must | TC-29 |
| FR-78 | FE-11 | Must | TC-28 |
| FR-79 | FE-12 | Must | TC-08 |
| FR-80 | FE-12 | Must | TC-30 |
| FR-81 | FE-12 | Must | TC-48 |
| FR-82 | FE-12 | Must | TC-48 |
| FR-83 | FE-12 | Must | TC-48 |
| FR-84 | FE-12 | Must | TC-08 |
| FR-85 | FE-12 | Must | TC-31 |
| FR-86 | FE-12 | Must | TC-30 |
| FR-87 | FE-12 | Must | TC-08 |
| FR-88 | FE-13 | Must | TC-32 |
| FR-89 | FE-13 | Must | TC-32 |
| FR-90 | FE-13 | Must | TC-33 |
| FR-91 | FE-13 | Must | TC-33 |
| FR-92 | FE-13 | Must | TC-34 |
| FR-93 | FE-13 | Must | TC-34 |
| FR-94 | FE-14 | Must | TC-35 |
| FR-95 | FE-14 | Must | TC-35 |
| FR-96 | FE-14 | Must | TC-35 |
| FR-97 | FE-14 | Must | TC-36 |
| FR-98 | FE-14 | Must | TC-36 |
| FR-99 | FE-15 | Must | TC-37 |
| FR-100 | FE-15 | Must | TC-38 |
| FR-101 | FE-17 | Must | TC-39 |
| FR-102 | FE-17 | Must | TC-39 |
| FR-103 | FE-17 | Must | TC-12 |
| FR-104 | FE-17 | Must | TC-05 |
| FR-105 | FE-17 | Must | TC-05 |
| FR-106 | FE-18 | Could | TC-40 |
| FR-107 | FE-18 | Could | TC-40 |
| FR-108 | FE-18 | Could | TC-40 |
| FR-109 | FE-18 | Could | TC-40 |
| FR-110 | FE-12 | Must | TC-31 |
| FR-111 | FE-02 | Must | TC-09 |
| FR-112 | FE-03 | Must | TC-06 |
| FR-113 | FE-06 | Must | TC-42 |
| FR-114 | FE-06 | Must | TC-43 |
| FR-115 | FE-06 | Must | TC-43 |
| FR-116 | FE-06 | Must | TC-43 |
| FR-117 | FE-06 | Must | TC-43 |
| FR-118 | FE-06 | Must | TC-43 |
| FR-119 | FE-07 | Must | TC-44 |
| FR-120 | FE-07 | Must | TC-44 |
| FR-121 | FE-07 | Must | TC-44 |
| FR-122 | FE-07 | Must | TC-44 |
| FR-123 | FE-07 | Must | TC-44 |
| FR-124 | FE-08 | Must | TC-20 |
| FR-125 | FE-08 | Must | TC-20 |
| FR-126 | FE-08 | Must | TC-20 |
| FR-127 | FE-08 | Must | TC-45 |
| FR-128 | FE-08 | Must | TC-45 |
| FR-129 | FE-08 | Must | TC-46 |
| FR-130 | FE-08 | Must | TC-46 |
| FR-131 | FE-08 | Must | TC-46 |
| FR-132 | FE-08 | Must | TC-46 |
| FR-133 | FE-09 | Must | TC-22 |
| FR-134 | FE-11 | Must | TC-59 |
| FR-135 | FE-11 | Must | TC-101, TC-58 |
| FR-136 | FE-11 | Must | TC-101, TC-58 |
| FR-137 | FE-11 | Must | TC-101, TC-58 |
| FR-138 | FE-11 | Must | TC-61 |
| FR-139 | FE-19 | Should | TC-41 |
| FR-140 | FE-19 | Should | TC-41 |
| FR-141 | FE-19 | Should | TC-41 |
| FR-142 | FE-19 | Should | TC-41 |
| FR-143 | FE-19 | Should | TC-41 |
| FR-144 | FE-19 | Should | TC-41 |
| FR-145 | FE-19 | Should | TC-41 |
| FR-146 | FE-01 | Must | TC-95, TC-96 |
| FR-147 | FE-05 | Must | TC-97 |
| FR-148 | FE-05 | Must | TC-97 |
| FR-149 | FE-05 | Must | TC-97 |
| FR-150 | FE-05 | Must | TC-15, TC-97 |
| FR-151 | FE-01 | Must | TC-01 |
| FR-152 | FE-01 | Must | TC-02 |
| FR-153 | FE-02 | Must | TC-03 |
| FR-154 | FE-03 | Must | TC-06 |
| FR-155 | FE-03 | Must | TC-07 |
| FR-156 | FE-03 | Must | TC-07 |
| FR-157 | FE-03 | Must | TC-08 |
| FR-158 | FE-03 | Must | TC-08 |
| FR-159 | FE-04 | Must | TC-18 |
| FR-160 | FE-04 | Must | TC-10 |
| FR-161 | FE-04 | Must | TC-11 |
| FR-162 | FE-04 | Must | TC-11 |
| FR-163 | FE-04 | Must | TC-12 |
| FR-164 | FE-04 | Must | TC-12 |
| FR-165 | FE-04 | Must | TC-12 |
| FR-166 | FE-04 | Must | TC-13 |
| FR-167 | FE-04 | Must | TC-13 |
| FR-168 | FE-04 | Must | TC-13 |
| FR-169 | FE-04 | Must | TC-12 |
| FR-170 | FE-05 | Must | TC-15 |
| FR-171 | FE-05 | Must | TC-15 |
| FR-172 | FE-05 | Must | TC-15 |
| FR-173 | FE-05 | Must | TC-16 |
| FR-174 | FE-05 | Must | TC-16 |
| FR-175 | FE-05 | Must | TC-16 |
| FR-176 | FE-05 | Must | TC-16 |
| FR-177 | FE-05 | Must | TC-17 |
| FR-178 | FE-05 | Must | TC-17, TC-98 |
| FR-179 | FE-05 | Must | TC-49 |
| FR-180 | FE-05 | Must | TC-49 |
| FR-181 | FE-06 | Must | TC-18 |
| FR-182 | FE-06 | Must | TC-42 |
| FR-183 | FE-06 | Must | TC-42 |
| FR-184 | FE-06 | Must | TC-43 |
| FR-185 | FE-06 | Must | TC-43 |
| FR-186 | FE-07 | Must | TC-19 |
| FR-187 | FE-07 | Must | TC-44 |
| FR-188 | FE-08 | Must | TC-21 |
| FR-189 | FE-08 | Must | TC-21 |
| FR-190 | FE-08 | Must | TC-20 |
| FR-191 | FE-08 | Must | TC-20 |
| FR-192 | FE-08 | Must | TC-20 |
| FR-193 | FE-08 | Must | TC-20 |
| FR-194 | FE-19 | Should | TC-20, TC-41 |
| FR-195 | FE-08 | Must | TC-46 |
| FR-196 | FE-08 | Must | TC-46 |
| FR-197 | FE-09 | Must | TC-22 |
| FR-198 | FE-09 | Must | TC-22 |
| FR-199 | FE-09 | Must | TC-22 |
| FR-200 | FE-09 | Must | TC-22 |
| FR-201 | FE-09 | Must | TC-22 |
| FR-202 | FE-09 | Must | TC-23 |
| FR-203 | FE-09 | Must | TC-23 |
| FR-204 | FE-09 | Must | TC-23 |
| FR-205 | FE-09 | Must | TC-22 |
| FR-206 | FE-09 | Must | TC-24 |
| FR-207 | FE-09 | Must | TC-24 |
| FR-208 | FE-09 | Must | TC-24 |
| FR-209 | FE-09 | Must | TC-24 |
| FR-210 | FE-09 | Must | TC-23 |
| FR-211 | FE-09 | Must | TC-23 |
| FR-212 | FE-10 | Must | TC-25 |
| FR-213 | FE-10 | Must | TC-25 |
| FR-214 | FE-10 | Must | TC-25 |
| FR-215 | FE-10 | Must | TC-25 |
| FR-216 | FE-10 | Must | TC-25 |
| FR-217 | FE-10 | Must | TC-25 |
| FR-218 | FE-10 | Must | TC-47 |
| FR-219 | FE-10 | Must | TC-47 |
| FR-220 | FE-10 | Must | TC-47 |
| FR-221 | FE-11 | Must | TC-27 |
| FR-222 | FE-11 | Must | TC-27 |
| FR-223 | FE-11 | Must | TC-27 |
| FR-224 | FE-11 | Must | TC-27 |
| FR-225 | FE-11 | Must | TC-27 |
| FR-226 | FE-11 | Must | TC-27 |
| FR-227 | FE-11 | Must | TC-27 |
| FR-228 | FE-11 | Must | TC-28, TC-29 |
| FR-229 | FE-11 | Must | TC-29 |
| FR-230 | FE-12 | Must | TC-08 |
| FR-231 | FE-12 | Must | TC-30 |
| FR-232 | FE-12 | Must | TC-48 |
| FR-233 | FE-12 | Must | TC-48 |
| FR-234 | FE-12 | Must | TC-48 |
| FR-235 | FE-12 | Must | TC-48 |
| FR-236 | FE-12 | Must | TC-08 |
| FR-237 | FE-12 | Must | TC-31 |
| FR-238 | FE-12 | Must | TC-31 |
| FR-239 | FE-12 | Must | TC-30 |
| FR-240 | FE-12 | Must | TC-08 |
| FR-241 | FE-12 | Must | TC-31 |
| FR-242 | FE-12 | Must | TC-31 |
| FR-243 | FE-13 | Must | TC-32 |
| FR-244 | FE-13 | Must | TC-32 |
| FR-245 | FE-13 | Must | TC-33 |
| FR-246 | FE-13 | Must | TC-33 |
| FR-247 | FE-13 | Must | TC-33 |
| FR-248 | FE-13 | Must | TC-34 |
| FR-249 | FE-14 | Must | TC-35 |
| FR-250 | FE-14 | Must | TC-35 |
| FR-251 | FE-14 | Must | TC-35 |
| FR-252 | FE-14 | Must | TC-35 |
| FR-253 | FE-14 | Must | TC-36 |
| FR-254 | FE-15 | Must | TC-37 |
| FR-255 | FE-15 | Must | TC-38 |
| FR-256 | FE-17 | Must | TC-39 |
| FR-257 | FE-17 | Must | TC-12 |
| FR-258 | FE-17 | Must | TC-05 |
| FR-259 | FE-17 | Must | TC-05 |
| FR-260 | FE-18 | Could | TC-40 |
| FR-261 | FE-18 | Could | TC-40 |
| FR-262 | FE-04 | Must | TC-98, TC-100 |
| FR-263 | FE-05 | Must | TC-04, TC-99 |
| FR-264 | FE-05 | Must | TC-38, TC-99 |
| FR-265 | FE-04 | Must | TC-100 |
| FR-266 | FE-05 | Must | TC-17, TC-100 |
| FR-267 | FE-19 | Should | TC-41 |
| FR-268 | FE-19 | Should | TC-41 |
| FR-269 | FE-19 | Should | TC-41 |
| FR-270 | FE-11 | Must | TC-27 |
| FR-271 | FE-11 | Must | TC-27 |
Check: 254 Must FRs, 11 Should FRs and 6 Could FRs (271 in all). Each has at least one case.

Use case to case:

| UC | Case |
|---|---|
| UC-01 Sign in | TC-01, TC-95, TC-96 |
| UC-02 View project metadata | TC-02 |
| UC-03 Manage members | TC-03 |
| UC-04 Configure project settings | TC-04 |
| UC-05 Review audit log, health and operating metrics | TC-05 |
| UC-06 Upload a dataset | TC-06 |
| UC-07 Import from a data connection | TC-07 |
| UC-08 Pair a Local Node and register local data | TC-08 |
| UC-09 Start a run from a research case | TC-09 |
| UC-10 Amend a research case | TC-10 |
| UC-11 Accept a hand-off object | TC-11 |
| UC-12 Monitor and recover a run | TC-12, TC-98, TC-100 |
| UC-13 Cancel a run | TC-13 |
| UC-14 Choose the next step | TC-14 |
| UC-15 Set preset and presence | TC-15, TC-97 |
| UC-16 Answer a decision inbox item | TC-16, TC-49, TC-99, TC-100 |
| UC-17 Confirm or overturn a tentative decision | TC-17, TC-98 |
| UC-18 Run the dataset stage | TC-18, TC-42, TC-43 |
| UC-19 Run the hypothesis stage | TC-19, TC-44 |
| UC-20 Run the experiment_design stage | TC-20, TC-45, TC-46 |
| UC-21 Lock a plan | TC-21 |
| UC-22 Run the execution stage | TC-22 |
| UC-23 Read verdict, grade and claim ceiling | TC-23 |
| UC-24 Triage exploration candidates | TC-24 |
| UC-25 Run the paper stage | TC-25, TC-47 |
| UC-26 Decide on submission | TC-26 |
| UC-27 Run the review loop | TC-27 |
| UC-28 Invoke a persona on an object | TC-28 |
| UC-29 Run the benchmarks | TC-29 |
| UC-30 Release an aggregate from local data | TC-30, TC-48 |
| UC-31 Handle a Local Node that is offline or revoked | TC-31 |
| UC-32 Warn on and enforce budgets | TC-32 |
| UC-33 Decide extra spend | TC-33 |
| UC-34 Set the spending ceiling and read the ledger | TC-34 |
| UC-35 Review and approve a Dossier | TC-35 |
| UC-36 Export a Dossier | TC-36 |
| UC-37 Comment on an object | TC-37 |
| UC-38 Receive notifications | TC-38, TC-99 |
| UC-39 Manage users, models and keys | TC-39 |
| UC-40 Build a journal profile | TC-40 |
| UC-41 Compare methods | TC-41 |

#### 4.1.3 Stage acceptance, benchmarks and the benchmark case catalogue

Stage acceptance cases, with the features they accept:

| TC | Accepts | Features |
|---|---|---|
| TC-50 | harness | FE-04, FE-05, FE-11 |
| TC-51 | dataset stage | FE-06 |
| TC-52 | hypothesis stage | FE-07 |
| TC-53 | experiment_design stage | FE-08 |
| TC-54 | execution stage | FE-09 |
| TC-55 | paper stage | FE-10 |
| TC-56 | Local Node | FE-12 |
| TC-57 | Connection check across stages | FE-04 to FE-12 |

Benchmark cases (benchmark case catalogue). The catalogue has 60 sample projects. Each is a test case of a research pattern. Wave 1 is BC-C01, BC-C05 and BC-C07. Wave 2 is BC-R01, BC-R06, BC-R08, BC-I01, BC-I08 and BC-I18. Waves 1 and 2 run first. The FE-09 cases of wave 1 are Must: they are the minimum set that shows the tabular branch works. The FE-09 cases from wave 2 onward are Should and run on request with the bench evaluation round. Cases with patterns G to J belong to FE-19 and follow the priority of FE-19 (Should, after the MVP). Pattern letters: A to E are data and feature patterns; K to O are reliability and trust patterns; F is the baseline policy; G to J are patterns of `method_comparison` (G hyperparameter search, H ensemble and stacking, I ablation, J budget-aware).

| BC | Short name | Task family | Pattern | FE | MoSCoW | Test case |
|---|---|---|---|---|---|---|
| BC-C01 | Comparison of classification algorithms | binary / multiclass | F | FE-09 | Must, wave 1 | TC-62 |
| BC-C05 | Is scaling really needed | binary / multiclass | C | FE-09 | Must, wave 1 | TC-63 |
| BC-C07 | Search budget and hyperparameter optimization | binary / multiclass | G | FE-19 | Should, wave 1 | TC-64 |
| BC-R01 | Linear and nonlinear benchmark | regression | F | FE-09 | Should, wave 2 | TC-65 |
| BC-R06 | Robustness to outliers | regression | B | FE-09 | Should, wave 2 | TC-66 |
| BC-R08 | Prediction interval coverage | regression | K | FE-09 | Should, wave 2 | TC-67 |
| BC-I01 | Resampling benchmark | rare-event | L | FE-09 | Should, wave 2 | TC-68 |
| BC-I08 | Calibration after resampling | rare-event | K, L | FE-09 | Should, wave 2 | TC-69 |
| BC-I18 | Statistical reliability across datasets | rare-event | F, L | FE-09 | Should, wave 2 | TC-70 |
| BC-C02 | Stability of feature selection | binary / multiclass | C | FE-09 | Should | TC-71 |
| BC-C03 | Missing data and imputation | binary / multiclass | A | FE-09 | Should | TC-71 |
| BC-C04 | Categorical encoding | binary / multiclass | C | FE-09 | Should | TC-71 |
| BC-C06 | Learning curve and sample efficiency | binary / multiclass | E | FE-09 | Should | TC-71 |
| BC-C08 | Performance and explanation | binary / multiclass | N | FE-09 | Should | TC-71 |
| BC-C09 | Probability calibration | binary / multiclass | K | FE-09 | Should | TC-71 |
| BC-C10 | Performance across subgroups | binary / multiclass | O | FE-09 | Should | TC-71 |
| BC-C11 | Decision threshold optimization | binary / multiclass | K | FE-09 | Should | TC-71 |
| BC-C13 | Label and feature noise robustness | binary / multiclass | B | FE-09 | Should | TC-71 |
| BC-C14 | Class overlap and boundary | binary / multiclass | B | FE-09 | Should | TC-71 |
| BC-C16 | Stability across seeds | binary / multiclass | F | FE-09 | Should | TC-71 |
| BC-C17 | Predictive data drift | binary / multiclass | D | FE-09 | Should | TC-71 |
| BC-C18 | Fairness-performance trade-off | binary / multiclass | O | FE-09 | Should | TC-71 |
| BC-C19 | Out-of-distribution test | binary / multiclass | D | FE-09 | Should | TC-71 |
| BC-R02 | Scaling in regression | regression | C | FE-09 | Should | TC-72 |
| BC-R03 | Polynomial interactions | regression | C | FE-09 | Should | TC-72 |
| BC-R04 | Regularization path | regression | N | FE-09 | Should | TC-72 |
| BC-R05 | Effect of imputation | regression | A | FE-09 | Should | TC-72 |
| BC-R09 | Stability of feature selection | regression | C | FE-09 | Should | TC-72 |
| BC-R10 | Learning from small samples | regression | E | FE-09 | Should | TC-72 |
| BC-R12 | Heteroscedastic uncertainty | regression | K | FE-09 | Should | TC-72 |
| BC-R13 | Measurement noise in inputs | regression | B | FE-09 | Should | TC-72 |
| BC-R15 | Monotonic constrained learning | regression | C | FE-09 | Should | TC-72 |
| BC-R16 | Cross-domain transfer | regression | D | FE-09 | Should | TC-72 |
| BC-R17 | Target transformation | regression | C | FE-09 | Should | TC-72 |
| BC-R18 | Explainability across folds | regression | N | FE-09 | Should | TC-72 |
| BC-R19 | Multi-output regression | regression | F | FE-09 | Should | TC-72 |
| BC-I02 | Variants of synthetic oversampling | rare-event | L | FE-09 | Should | TC-73 |
| BC-I03 | Class weighting or resampling | rare-event | L | FE-09 | Should | TC-73 |
| BC-I04 | Extreme imbalance | rare-event | L | FE-09 | Should | TC-73 |
| BC-I05 | Cost-sensitive learning | rare-event | L, O | FE-09 | Should | TC-73 |
| BC-I06 | Threshold optimization | rare-event | K | FE-09 | Should | TC-73 |
| BC-I07 | Precision-recall operating point | rare-event | K, L | FE-09 | Should | TC-73 |
| BC-I09 | Number of minority samples | rare-event | E, L | FE-09 | Should | TC-73 |
| BC-I10 | Label noise in the minority class | rare-event | B, L | FE-09 | Should | TC-73 |
| BC-I11 | Ensembles for imbalance | rare-event | L | FE-09 | Should | TC-73 |
| BC-I12 | Sampling ratio optimization | rare-event | L | FE-09 | Should | TC-73 |
| BC-I13 | Feature selection under imbalance | rare-event | C, L | FE-09 | Should | TC-73 |
| BC-I14 | Synthetic or duplicated minority | rare-event | L | FE-09 | Should | TC-73 |
| BC-I15 | Imbalance combined with drift | rare-event | D, L | FE-09 | Should | TC-73 |
| BC-I16 | Fairness under imbalance | rare-event | L, O | FE-09 | Should | TC-73 |
| BC-I17 | Anomaly detection or supervised learning | rare-event | F, L | FE-09 | Should | TC-73 |
| BC-I19 | Distribution shift of minority features | rare-event | M, L | FE-09 | Should | TC-73 |
| BC-C12 | Ensemble and stacking | binary / multiclass | H | FE-19 | Should | TC-74 |
| BC-C15 | Feature interaction and ablation | binary / multiclass | C, I | FE-19 | Should | TC-74 |
| BC-C20 | AutoML with a scientific baseline | binary / multiclass | F, J | FE-19 | Should | TC-74 |
| BC-I20 | Automatic choice of imbalance strategy | rare-event | G, L | FE-19 | Should | TC-74 |
| BC-R07 | Hyperparameter optimization in regression | regression | G | FE-19 | Should | TC-74 |
| BC-R11 | Stacking in regression | regression | H | FE-19 | Should | TC-74 |
| BC-R14 | Feature interaction ablation | regression | I | FE-19 | Should | TC-74 |
| BC-R20 | AutoML regression suite | regression | F, J | FE-19 | Should | TC-74 |

BC-C20 and BC-R20 are user research topics under FE-19 (Should, after the MVP). The user compares an AutoML method with baselines on the user's own data under `method_comparison`. They are not a comparison of OpenAI-Scientist with AutoML, which is a non-goal (section 1.3).

### 4.2 Detailed test cases

#### 4.2.1 Use case scenarios

Each case below traces to a use case, its FRs and its business rules. A fixture is a named set of test data (section 3.2). All cases have the status "Not run".

##### TC-01 Sign in with an email address
- Traces: UC-01; FR-01, FR-02, FR-151; BR-01, BR-02.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. The user has an email address that the system knows.
- Steps: 1. Enter the email address. 2. Complete the sign-in request. 3. Repeat with an expired sign-in request. 4. Sign in as a non-member and open a resource of project P. 5. Sign in as a member with the Reviewer role and start a run.
- Test data: One known email address; one expired sign-in request; one project P.
- Expected result: After step 1 the system shows MSG-04. After step 2 a session opens and shows only the projects of the user. The system never asks for a password. Step 3 shows MSG-03. Step 4 shows MSG-02 and reveals nothing about project P. Step 5 shows MSG-01.
- Status: Not run.

##### TC-02 View project metadata as Platform Admin
- Traces: UC-02; FR-03, FR-152; BR-06.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. A Platform Admin account that is not a member of any project.
- Steps: 1. Sign in as the Platform Admin. 2. Open the project list. 3. Open one project. 4. Try to open a dataset, an object and a manuscript of that project. 5. Add the Platform Admin to the project as a Researcher and repeat step 4.
- Test data: Fixture A with one dataset, one object and one manuscript.
- Expected result: Steps 2 and 3 show list, members, usage and run state. Step 4 shows MSG-01 for every content item. After step 5 the project role applies and the content opens.
- Status: Not run.

##### TC-03 Manage members and archive a project
- Traces: UC-03; FR-04 to FR-06, FR-153; BR-03, BR-04, BR-05.
- Priority, level, method: Must; L2; Test.
- Preconditions: Fixture A. The user is the only Project Manager of an active project. The invitation validity (SR-05) is set to a short value.
- Steps: 1. Invite a new user as Researcher. 2. Accept the invitation before it expires. 3. Invite a second user and let the invitation expire. 4. Accept the expired invitation. 5. Remove the only Project Manager. 6. Archive the project and change a setting.
- Test data: Two invitees; invitation validity set for the test.
- Expected result: Step 2 adds the member and writes an audit log entry. Step 4 shows MSG-05. Step 5 is rejected with MSG-06. Step 6 shows MSG-07 and changes nothing.
- Status: Not run.

##### TC-04 Configure project settings
- Traces: UC-04; FR-08, FR-263; BR-24, BR-59, BR-63, BR-78, BR-92, BR-104.
- Priority, level, method: Must; L3; Demonstration.
- Preconditions: Fixture A. Signed in as Project Manager.
- Steps: 1. Set the monthly budget and the warning thresholds (SR-03). 2. Set the review settings: number of approvals, who may approve, self-approval. 3. Set the default preset per stage, the notification settings, the limit of secondary hypotheses (SR-06), the response time for spending items (SR-04) and the wait deadline of pinned items (SR-08). 4. Save. 5. Enter an invalid value and save.
- Test data: One valid and one invalid value per setting.
- Expected result: After step 4 the settings are stored and the audit log has an entry. After step 5 the system keeps the old value and shows the reason.
- Status: Not run.

##### TC-05 Review audit log, health and operating metrics
- Traces: UC-05; FR-07, FR-104, FR-105, FR-258, FR-259; BR-05, BR-29, BR-40.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A with several changes made (TC-03, TC-04). At least one finished run. Signed in as Platform Admin.
- Steps: 1. Open the audit log. 2. Search for the changes of TC-03 and TC-04. 3. Try to edit and to delete an entry. 4. Open the component health view. 5. Open the operating metrics of a run. 6. Open the persona precision view.
- Test data: A run with decision log entries; a component set to unhealthy.
- Expected result: Every important change has an entry. No edit or deletion is possible. An unhealthy component is marked and shows its last known state. The run shows the number of questions, the blocked time and the overturn rate per action type. The persona view shows the precision from the seeded-flaw bench.
- Status: Not run.

##### TC-06 Upload a dataset
- Traces: UC-06; FR-09, FR-112, FR-154; BR-16, BR-18, BR-102.
- Priority, level, method: Must; L2; Test.
- Preconditions: Fixture A. Signed in as Researcher.
- Steps: 1. Upload one file in each format that SR-01 lists, including Parquet. 2. Upload a second file to the same dataset. 3. Upload a file in an unsupported format. 4. Upload a file larger than the limit (SR-02). 5. Upload a file with no readable table (SR-07). 6. Pin a dataset version in an analysis and upload a newer version.
- Test data: One file per supported format; one unsupported file; one oversize file; one file with no table.
- Expected result: Each valid upload creates a new immutable version with a hash and shows MSG-12. The older version stays unchanged and stays pinned. Step 3 shows MSG-09. Step 4 shows MSG-10. Step 5 shows MSG-11.
- Status: Not run.

##### TC-07 Import from a data connection
- Traces: UC-07; FR-10, FR-11, FR-155, FR-156; BR-16, BR-17.
- Priority, level, method: Must; L2; Test.
- Preconditions: Fixture A. One authorized source, one source with no authorization, one internal host address.
- Steps: 1. Import from the authorized source. 2. Import from the source with no authorization. 3. Enter the internal host address as a source. 4. Search every response, trace and log of steps 1 to 3 for the credential.
- Test data: A connection credential with a known planted value.
- Expected result: Step 1 creates a dataset version and shows MSG-12. Step 2 shows MSG-13. Step 3 shows MSG-14. Step 4 finds no credential.
- Status: Not run.

##### TC-08 Pair a Local Node and register local data
- Traces: UC-08; FR-12, FR-79, FR-84, FR-87, FR-157, FR-158, FR-230, FR-236, FR-240; BR-16, BR-18.
- Priority, level, method: Must; L2; Test; Demonstration.
- Preconditions: Fixture A. A Local Node installed on a machine with no container runtime. A watched folder with one data file.
- Steps: 1. Pair the Local Node with the project by a pairing code. 2. Read the datasets that the Local Node proposes. 3. Accept one. 4. Request a preview and a download of its rows. 5. Change the file in the folder and start a job on the registered version.
- Test data: One pairing code; one data file; one changed copy of the file.
- Expected result: Step 1 shows MSG-17. Step 2 lists the file. Step 3 creates a dataset version with data location `local`. Step 4 shows MSG-15 and returns no rows. Step 5 is rejected by the hash check with MSG-16 and the system proposes a new version.
- Status: Not run.

##### TC-09 Start a run from a research case
- Traces: UC-09; FR-13, FR-14, FR-16, FR-111; BR-07, BR-08, BR-09, BR-80.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. The project has no active run.
- Steps: 1. As Researcher submit a research case with topic, goals, context, constraints, domain and references and no dataset. 2. Read the pipeline of the run. 3. Submit a second research case. 4. End the first run and set the monthly budget to 100% used. Submit a case again. 5. As Project Manager create a run, answer an inbox item, accept an object and lock a plan.
- Test data: One research case with all fields.
- Expected result: Step 1 creates a run in state `running` and starts the dataset stage. The pipeline is `dataset_first` with the five stages. Step 3 shows MSG-08. Step 4 blocks the start and shows MSG-51. Step 5 succeeds for the Project Manager.
- Status: Not run.

##### TC-10 Amend a research case
- Traces: UC-10; FR-17, FR-160; BR-10.
- Priority, level, method: Must; L2; Test.
- Preconditions: A run with a fixed research case and a stage that already started.
- Steps: 1. Amend the case with a reason. 2. Read the case version and the event. 3. Read the case version that the started stage uses. 4. Amend the case with an empty reason.
- Test data: One amendment text and reason.
- Expected result: Step 1 creates a new case version and an event. The started stage keeps the old version. Step 4 is rejected.
- Status: Not run.

##### TC-11 Accept a hand-off object and mark downstream objects stale
- Traces: UC-11; FR-18, FR-19, FR-161, FR-162; BR-11, BR-12.
- Priority, level, method: Must; L3; Test.
- Preconditions: A run with an accepted DatasetSnapshot and a HypothesisSet that pins it.
- Steps: 1. Open an object version with all contract items green. 2. Accept it. 3. Try to edit the accepted object. 4. Create a new version of the DatasetSnapshot. 5. Read the state of the HypothesisSet. 6. Accept the update.
- Test data: Frozen upstream objects (Fixture C).
- Expected result: Step 1 shows type, version and hash with MSG-35. After step 2 the object is immutable. Step 3 creates a new version and changes nothing in the old one. After step 4 the HypothesisSet is `stale` with MSG-34 and nothing updates by itself. Step 6 starts a new acceptance.
- Status: Not run.

##### TC-12 Monitor and recover a run
- Traces: UC-12; FR-20, FR-21, FR-24, FR-103, FR-163 to FR-165, FR-169, FR-257; BR-13, BR-14, BR-41. FR-262 and FR-265 are in TC-98 and TC-100.
- Priority, level, method: Must; L3; Test.
- Preconditions: A run in a stage. Fixture D (scripted model provider).
- Steps: 1. Read the run state and the contract items. 2. Force a red item and read the agent action. 3. Use up the budget share of an item. 4. Let a stage reach a limit. 5. Start a run with no model profile. 6. Cut the model provider during a stage. 7. Make one literature source fail. 8. Insert a number in model text.
- Test data: Scripted model answers; a run with no model profile.
- Expected result: Step 1 shows exactly one run state. Step 2 turns the red item into a task for the agent. Step 3 shows MSG-36 and creates a needs-you item. Step 4 ends the stage on the best output with MSG-29 and lists every red item. Step 5 ends the run as `failed_technical` with MSG-30 and creates no output. Step 6 shows MSG-58 and creates no output. In step 7 the error is logged per source, the stage continues with the other sources and MSG-31 shows. In step 8 the number is a reference to a record, not model text.
- Status: Not run.

##### TC-13 Cancel a run
- Traces: UC-13; FR-22, FR-166 to FR-168; BR-77.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. A run created by Researcher R1 with accepted objects and waiting items. A second Researcher R2.
- Steps: 1. As R2 try to cancel the run. 2. As R1 select Cancel run and decline the confirmation. 3. As R1 select Cancel run and confirm. 4. Repeat on another run as Project Manager. 5. As R1 cancel a run in each of the states `running`, `waiting(decision)`, `waiting(budget_review)` and `waiting(node_offline)`. 6. Try to cancel a run in state `ended`.
- Test data: Six runs, one in each state of step 5 and one ended.
- Expected result: Step 1 shows MSG-01. Step 2 changes nothing. Step 3 shows MSG-32, then MSG-33. The run is `ended(cancelled)`, accepted objects stay, waiting items close and the audit log has an entry. Step 4 gives the same result. Step 5 ends each run as `ended(cancelled)`. Step 6 changes nothing and the run keeps its result.
- Status: Not run.

##### TC-14 Choose the next step
- Traces: UC-14; FR-23, FR-35; BR-15, BR-34.
- Priority, level, method: Must; L3; Test; Demonstration.
- Preconditions: A run that ended.
- Steps: 1. Open the lab notebook. 2. Read the proposed next step. 3. Choose one step. 4. On another ended run choose none.
- Test data: Two ended runs.
- Expected result: The lab notebook has the summary, the proposals, the tentative decisions and the reasons. The proposal is one of `collect_more_data`, `explore_signal`, `replicate`, `write_paper`, `revise_plan`. Step 4 leaves the run ended.
- Status: Not run.

##### TC-15 Set preset and presence
- Traces: UC-15; FR-25, FR-26, FR-150, FR-170 to FR-172; BR-24, BR-25, BR-27.
- Priority, level, method: Must; L1, L3; Test.
- Preconditions: A project with default settings and one waiting item.
- Steps: 1. Read the default preset of a stage. 2. Change the preset to `autopilot`. 3. Read the waiting item and a past decision. 4. Set presence to `away`. 5. Override the level of a pinned action below its floor.
- Test data: One pinned action and one unpinned action.
- Expected result: The default is `milestones`. After step 2 the system applies the preset to future actions and re-evaluates the waiting item. The past decision is unchanged. Every action has one action group and one level. Step 5 is rejected and shows the floor.
- Status: Not run.

##### TC-16 Answer a decision inbox item
- Traces: UC-16; FR-27 to FR-30, FR-173 to FR-176; BR-26, BR-27, BR-28, BR-29, BR-32, BR-33, BR-75.
- Priority, level, method: Must; L3; Test.
- Preconditions: A run with items of every kind ready to be raised. Fixture A.
- Steps: 1. With the user `present`, raise a `must_ask` item. 2. With the user `away`, raise a second `must_ask` item. 3. Read the inbox. 4. Answer both items. 5. Read the decision log. 6. At each preset try to lower the level of each pinned action. 7. Create a blocking pinned item and a `spending` item.
- Test data: The eight pinned actions: outcome and estimand, unit of observation and data structure, hypotheses and primary, join of public data, lock, deviation, validation source, export.
- Expected result: Step 1 asks at once with options, a recommended option and a reason (MSG-24, MSG-23 for the structure item). In step 2 the item waits and the agent continues work that does not depend on it. The inbox holds the eight kinds: question, review batch, tentative decision, deviation, candidate, needs-you, release review and spending. Each decision has action type, level, policy version, decider and presence. The overturn rate per action type is computed. The system may propose a higher level and never raises it. Every pinned action stays `must_ask` at every preset. In step 7 the system sends external notices only for these two items.
- Status: Not run.

##### TC-17 Confirm or overturn a tentative decision
- Traces: UC-17; FR-31, FR-32, FR-177, FR-178, FR-266; BR-29, BR-30, BR-31, BR-104.
- Priority, level, method: Must; L3; Test.
- Preconditions: Preset `autopilot`; the user is `away`; unpinned and pinned items wait.
- Steps: 1. Let the AI PI work while the user is away. 2. Try to make the AI PI decide a pinned item. 3. Leave only pinned items waiting. 4. Return as the user. 5. Confirm one tentative decision. 6. Overturn another.
- Test data: Two unpinned items, one pinned item.
- Expected result: The AI PI decides only unpinned items, each as a tentative decision, and never ends the run. Step 2 shows MSG-44. In step 3 the stage ends at `ready_to_<action>` and the run stays in `waiting(decision)`; it does not end before the wait deadline of the item. Step 4 shows MSG-42. Step 6 shows MSG-43, undoes the dependent work, marks the affected objects `stale` and records the overturn.
- Status: Not run.

##### TC-18 Run the dataset stage
- Traces: UC-18; FR-15, FR-37, FR-39 to FR-41, FR-159, FR-181; BR-08, BR-26, BR-41, BR-43, BR-44, BR-76, BR-84, BR-85, BR-88, BR-89.
- Priority, level, method: Must; L3; Test.
- Preconditions: A run whose research case has no dataset. Fixture B (sample dataset) in the project and a public dataset available.
- Steps: 1. Let the stage search the project. 2. Let the stage search public datasets for role `enrichment`. 3. Try to join the public data into the private data. 4. Read the proposed unit of observation and data structure. 5. Try to continue before the Researcher confirms them. 6. Confirm them. 7. Read the DatasetSnapshot. 8. Read the fitness.
- Test data: Fixture B with a known unit of observation and group column.
- Expected result: The stage searches the project, searches public data or asks through the inbox. Step 3 creates a pinned item. Step 5 shows MSG-23 and creates no split. After step 6 the split is created. The DatasetSnapshot has source, table model, five-dimension quality profile, dictionary, cleaning recipe, question map, split, source roles and fitness. Code concludes the fitness as `fit`, `fit_with_limits` or `not_fit`.
- Status: Not run.

##### TC-19 Run the hypothesis stage
- Traces: UC-19; FR-43 to FR-45, FR-186; BR-41, BR-45, BR-90, BR-91, BR-92.
- Priority, level, method: Must; L3; Test; Demonstration.
- Preconditions: An accepted DatasetSnapshot. Fixture D (scripted model provider and a scholarly metadata source that can fail).
- Steps: 1. Run the stage. 2. Make one source fail. 3. Make all sources fail. 4. Read the Literature Base. 5. Read the HypothesisSet.
- Test data: Three metadata sources, one failing; scripted hypotheses.
- Expected result: The Literature Base is versioned and has the search protocol and the search log. A failing source is logged with MSG-31 and the stage continues. When all sources fail the stage records a gap. The HypothesisSet has at least two hypotheses with different claim keys and one primary. Each hypothesis has a draft estimand (the quantity to estimate), variables, sourced confounders, a smallest effect size of interest (SESOI), a refutation statement, a contribution type and an origin.
- Status: Not run.

##### TC-20 Run the experiment_design stage
- Traces: UC-20; FR-46, FR-47, FR-124 to FR-126, FR-190 to FR-193, FR-194; BR-46, BR-50, BR-83, BR-86, BR-93, BR-94, BR-95, BR-96, BR-99.
- Priority, level, method: Must; L3; Test.
- Preconditions: An accepted HypothesisSet for a `prediction` claim.
- Steps: 1. Run the stage. 2. Read the task family and the pattern in the AnalysisPlan. 3. Read the plan fields. 4. Check that the analysis program ran on the twin (a summary table built only from released aggregates) before the lock. 5. Request pattern G for a `prediction` claim. 6. Break the pipeline order in one step.
- Test data: Hypothesis sets for task families `binary`, `multiclass`, `regression`, `rare-event`.
- Expected result: The plan records task family and pattern from the registry. The plan has estimand, protocol by claim type, adjustment set, analysis program, fallback, decision rule, interpretation table, robustness set, design diagnosis and hypothesis family structure. The twin run comes before the lock. Step 5 is refused: `prediction` uses patterns A to E and K to O, and pattern F as baseline policy. Step 6 blocks the step and shows MSG-61.
- Status: Not run.

##### TC-21 Lock a plan
- Traces: UC-21; FR-48, FR-49, FR-188, FR-189; BR-26, BR-31, BR-47.
- Priority, level, method: Must; L3; Test.
- Preconditions: A plan that passed all checks and the review loop.
- Steps: 1. With the user `present`, open the plan. 2. Lock it. 3. Read the Lock. 4. Change the plan. 5. On another run set the user `away` and wait for the plan to be ready. 6. Try to lock for the user.
- Test data: Two plans.
- Expected result: Step 1 shows MSG-37. The Lock holds the hashes of spec, program and golden outputs, the snapshot version, the split digest, who locked and when. After step 4 the change is a deviation. In step 5 the plan waits with MSG-38. Step 6 is not possible for anyone.
- Status: Not run.

##### TC-22 Run the execution stage
- Traces: UC-22; FR-50 to FR-53, FR-56, FR-133, FR-197 to FR-201, FR-205; BR-11, BR-26, BR-48, BR-49, BR-50, BR-86, BR-87.
- Priority, level, method: Must; L3; Test.
- Preconditions: A Lock exists. Fixture B and a twin.
- Steps: 1. Run the stage in the sandbox. 2. Read the result of the dry run on real data. 3. Read what the agent sees during the confirmatory job. 4. Request an unseal before the last confirmatory fix. 5. Let all checks turn green. 6. Repeat with the manual unseal option. 7. Change the locked algorithm. 8. Insert a step that breaks the pipeline order.
- Test data: One plan with two hypotheses.
- Expected result: The dry run returns only row count, types, missingness, convergence and time and no estimate. Before unseal the agent sees only `done` or `error`. Step 4 shows MSG-41. Step 5 unseals all hypotheses at once, records the time and shows MSG-45. Step 6 waits for the user. Step 7 creates a pinned deviation (MSG-39) that is logged and counted in the grade. Step 8 is blocked before the run or recorded as a deviation.
- Status: Not run.

##### TC-23 Read verdict, grade and claim ceiling
- Traces: UC-23; FR-54, FR-55, FR-60, FR-61, FR-202 to FR-204, FR-210, FR-211; BR-11, BR-54, BR-55, BR-56, BR-57.
- Priority, level, method: Must; L1, L3; Test.
- Preconditions: Unsealed results. Fixture E: one result set for each verdict.
- Steps: 1. Run the verdict calculation on the five fixture result sets. 2. Read the grade for a fixture with a diagnostic failure, a fixture with a robustness failure and a fixture with a deviation. 3. Read the claim ceiling for each verdict and confirmation tier. 4. Read the EvidenceBundle. 5. Run the replicator. 6. Alter one replicated output and run it again.
- Test data: Fixture E with expected verdicts `supported`, `trivial`, `not_supported`, `insufficient`, `not_tested` and expected grades A to D.
- Expected result: Code returns the expected verdict and grade for every fixture. The claim ceiling follows verdict, grade and confirmation tier. A locked plan is not a proven claim. The EvidenceBundle has ten checked items including the replication package. The replicator reproduces the hash. After step 6 the bundle item is red and the paper stage does not use the bundle.
- Status: Not run.

##### TC-24 Triage exploration candidates
- Traces: UC-24; FR-57 to FR-59, FR-206 to FR-209; BR-51, BR-52, BR-53.
- Priority, level, method: Must; L3; Test.
- Preconditions: An unsealed run. Lane E (the exploration lane of the execution stage) produces candidates.
- Steps: 1. Run lane E. 2. Inspect which data splits lane E reads. 3. Read the tried ledger after 1, 10 and 50 search procedures. 4. Read the inbox. 5. Reject one candidate. 6. Confirm candidates in each confirmation tier.
- Test data: A search that yields candidates at the four tiers.
- Expected result: Lane E reads the exploration split only and uses no validation source. The noise threshold in the tried ledger rises as the number of procedures grows. Each candidate enters the inbox with MSG-46 and never goes straight into the plan. The rejected candidate stays in the ledger. Each confirmed candidate has a tier. Only confirmatory results and the tiers `replicated` and `reserve` write an evidence e-value (a measure of evidence that multiplies across independent rows) to the claim ledger.
- Status: Not run.

##### TC-25 Run the paper stage
- Traces: UC-25; FR-62 to FR-66, FR-212 to FR-217; BR-56, BR-65, BR-73.
- Priority, level, method: Must; L1, L3; Test.
- Preconditions: An accepted EvidenceBundle.
- Steps: 1. Run the stage. 2. Insert a digit that is not a reference into model text. 3. Insert an effect statement stronger than the claim ceiling. 4. Insert a citation that is not in the Literature Base. 5. Insert a citation with an unresolved DOI. 6. Remove one grade reason from the limitations.
- Test data: One EvidenceBundle with known records.
- Expected result: The PaperPack has ten checked items. Every number is rendered from a bundle record. Step 2 shows MSG-47 and the check is red. Step 3 shows MSG-48. Steps 4 and 5 show MSG-49. Every effect statement maps to a verdict and an interpretation row. Every citation has a supporting quote. Step 6 turns the limitations check red.
- Status: Not run.

##### TC-26 Decide on submission
- Traces: UC-26; FR-70; BR-73.
- Priority, level, method: Must; L3; Inspection.
- Preconditions: An approved Dossier.
- Steps: 1. Search the product for a function that submits to a publisher. 2. Read the decision step of the Researcher.
- Test data: None.
- Expected result: No function submits to a publisher. The decision to submit stays with the Researcher.
- Status: Not run.

##### TC-27 Run the review loop
- Traces: UC-27; FR-71 to FR-76, FR-221 to FR-227, FR-270, FR-271; BR-35, BR-37, BR-39, BR-42.
- Priority, level, method: Must; L3; Test.
- Preconditions: An object with all contract items green. Fixture D with scripted findings.
- Steps: 1. Start the loop. 2. Check the context of the reviewer. 3. Check that guards do not read each other. 4. Return a finding with no anchor. 5. Return findings with each verifier result. 6. Keep one blocking confirmed finding open for three rounds. 7. Break the provenance of an object. 8. Create a new object version. 9. After a revision, return a new `blocking` finding on an unchanged field twice: once with a newly computed fact as evidence and once without. 10. Read the scope of the review after a revision.
- Test data: Scripted findings: one without anchor, one `confirmed` blocking, one `plausible`, one `rejected`; two new `blocking` findings on an unchanged field.
- Expected result: The loop runs once per object version after all checks are green. The reviewer has fresh context and does not see the author trace. Guards run in parallel. Code drops the finding without anchor. Only the `blocking` and `confirmed` finding enters a revision round. The loop stops after two rounds; the open finding becomes a known risk with MSG-50, or the user decides. Step 7 rejects the object. Step 8 starts a new loop. In step 9 the system accepts the finding with the newly computed fact and does not accept the other. In step 10 the review covers only the findings that were fixed and the fields that changed.
- Status: Not run.

##### TC-28 Invoke a persona on an object
- Traces: UC-28; FR-78, FR-228; BR-40.
- Priority, level, method: Must; L3; Test.
- Preconditions: An object. One persona below its minimum precision.
- Steps: 1. Select a persona. 2. Invoke it on an object of each hand-off type. 3. Read the findings. 4. Invoke the persona that is below its minimum precision.
- Test data: Two personas.
- Expected result: Any persona runs on any object and the system shows the findings. The findings of the persona below its minimum show a lower severity.
- Status: Not run.

##### TC-29 Run the benchmarks
- Traces: UC-29; FR-77, FR-228, FR-229; BR-40, BR-97, BR-100, BR-101.
- Priority, level, method: Must; L5; Analysis.
- Preconditions: Benchmark data exists. Signed in as Platform Admin. The case checks the bench capability. A full evaluation round is TC-58 (Should, on request).
- Steps: 1. Start the seeded-flaw bench. 2. Read the precision of each persona. 3. Compare each precision with the minimum. 4. Enable a persona that catches what the other personas miss.
- Test data: The seeded-flaw bench (TC-58).
- Expected result: The precision of each reviewer persona is measured. A persona below the minimum gets lower severity for its findings. A persona is enabled only when the bench shows that it catches what the other personas miss (BR-40).
- Status: Not run.

##### TC-30 Release an aggregate from local data
- Traces: UC-30; FR-80, FR-86, FR-231, FR-239; BR-19, BR-20, BR-21, BR-22, BR-80.
- Priority, level, method: Must; L2; Test.
- Preconditions: A `local` dataset version and a paired Local Node (TC-08).
- Steps: 1. Run a job that returns an aggregate above the small-cell threshold. 2. Run a job that returns a cell below the threshold. 3. Run two queries that differ by fewer rows than the threshold. 4. Run queries until the probe budget is used up. 5. Read the list of rejected queries.
- Test data: Aggregates above and below the threshold.
- Expected result: Step 1 passes the release gate, with rounding. Steps 2 and 3 are rejected with MSG-20. Step 4 records a gap, the run continues and MSG-21 shows. Step 5 shows every rejected query with its reason. No rows leave the data holder.
- Status: Not run.

##### TC-31 Handle a Local Node that is offline or revoked
- Traces: UC-31; FR-85, FR-110, FR-237, FR-238, FR-241, FR-242; BR-14, BR-27, BR-81.
- Priority, level, method: Must; L3; Test.
- Preconditions: A run with a job that needs `local` data and other work that does not.
- Steps: 1. Switch the Local Node offline. 2. Read the run state. 3. Read the notices. 4. Switch the Local Node online. 5. Revoke the Local Node and start a job on its data. 6. Open a published object.
- Test data: One Local Node.
- Expected result: The run enters `waiting(node_offline)`. Work that does not need the data continues. The user receives one combined notice with MSG-18. After step 4 the run returns to `running`. Step 5 is rejected with MSG-19. Published objects stay readable.
- Status: Not run.

##### TC-32 Warn on and enforce budgets
- Traces: UC-32; FR-88, FR-89, FR-243, FR-244; BR-58, BR-59.
- Priority, level, method: Must; L2; Test.
- Preconditions: A project budget with warning thresholds and a run token budget.
- Steps: 1. Run until the token budget is used up. 2. Raise the monthly use over each warning threshold. 3. Raise the monthly use to 100%. 4. Start a new run.
- Test data: Token budget and monthly budget set to small values.
- Expected result: Step 1 ends the run as `ended(with_gaps)` on the best output with MSG-29. Step 2 shows MSG-26 at each threshold. Step 4 shows MSG-51.
- Status: Not run.

##### TC-33 Decide extra spend
- Traces: UC-33; FR-90, FR-91, FR-245 to FR-247; BR-28, BR-60, BR-78.
- Priority, level, method: Must; L3; Test.
- Preconditions: A running run. The monthly budget reaches 100% during the run. The response time (SR-04) is short.
- Steps: 1. Read the run state. 2. Read the inbox. 3. Wait for the reminder. 4. As Project Manager approve extra spend. 5. Repeat on another run and let the deadline pass.
- Test data: Two runs.
- Expected result: The run moves to `waiting(budget_review)` with a `must_ask` `spending` item (MSG-25). The Project Manager receives an external notice and a reminder before the deadline (MSG-27). Step 4 lets the run continue. In step 5 the run ends `ended(with_gaps)` on the best output and lists every red item (MSG-28).
- Status: Not run.

##### TC-34 Set the spending ceiling and read the ledger
- Traces: UC-34; FR-92, FR-93, FR-248; BR-61.
- Priority, level, method: Must; L2; Test.
- Preconditions: Signed in as Platform Admin. Preset `autopilot`.
- Steps: 1. Set the ceiling. 2. Raise one spend below the ceiling. 3. Raise one spend above the ceiling. 4. Read the usage and cost ledger of a run and of a project.
- Test data: Two spend amounts.
- Expected result: The spend below the ceiling is `auto`. The spend above the ceiling is `must_ask` and needs a decision (TC-33). The ledger shows usage and cost per run and per project.
- Status: Not run.

##### TC-35 Review and approve a Dossier
- Traces: UC-35; FR-94 to FR-96, FR-249 to FR-252; BR-62, BR-63, BR-79.
- Priority, level, method: Must; L3; Test.
- Preconditions: An accepted PaperPack. Review settings require two approvals and forbid self-approval.
- Steps: 1. Read the Dossier version 1. 2. Approve as the author of the run. 3. Approve as two other eligible users. 4. Accept a new PaperPack version. 5. Read the approvals. 6. Open the Dossier of a run that ended `with_gaps` before a PaperPack was accepted.
- Test data: One run per case.
- Expected result: Dossier version 1 refers to the accepted EvidenceBundle and PaperPack versions and the hashes are checked. Step 2 shows MSG-52. After step 3 the Dossier is approved. Step 4 creates a new Dossier version with MSG-54 and the approvals do not carry over. Step 6 shows MSG-53.
- Status: Not run.

##### TC-36 Export a Dossier
- Traces: UC-36; FR-97, FR-98, FR-253; BR-05, BR-64.
- Priority, level, method: Must; L3; Test.
- Preconditions: One approved Dossier and one Dossier that is not approved.
- Steps: 1. Export the approved Dossier. 2. Confirm the pinned action. 3. Read the audit log. 4. Export the Dossier that is not approved.
- Test data: Two Dossiers.
- Expected result: Step 1 asks for a decision with MSG-39. After step 2 the Dossier leaves the project. The audit log has the Dossier version and the format. Step 4 shows MSG-55.
- Status: Not run.

##### TC-37 Comment on an object
- Traces: UC-37; FR-99, FR-254; BR-05, BR-06.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A and an object.
- Steps: 1. As Reviewer read every object type and comment. 2. As Researcher and as Project Manager comment. 3. Comment as a user without the right.
- Test data: One object of each hand-off type.
- Expected result: The Reviewer reads every object and comments. Project Manager and Researcher comment by role. Members see the comments. Step 3 shows MSG-01.
- Status: Not run.

##### TC-38 Receive notifications
- Traces: UC-38; FR-100, FR-255; BR-05, BR-28.
- Priority, level, method: Must; L2; Test.
- Preconditions: Notification settings with mail and push on for one member and off for another.
- Steps: 1. Create a normal project event. 2. Create a blocking pinned item. 3. Create a `spending` item. 4. Read the notices of both members.
- Test data: Two members.
- Expected result: All members get the in-system notice by their settings. External notices go out only for the blocking pinned item and the `spending` item. The member with the channel off sees the notice in the inbox only.
- Status: Not run.

##### TC-39 Manage users, models and keys
- Traces: UC-39; FR-101, FR-102, FR-256; BR-02, BR-23.
- Priority, level, method: Must; L3; Test; Demonstration.
- Preconditions: Signed in as Platform Admin.
- Steps: 1. Add a user. 2. Set a model profile for each model role (`stage`, `review`, `vision`). 3. Enter a key with a planted value. 4. Run a stage. 5. Search every prompt, log, trace and output for the planted value. 6. Remove the model profile and start a run.
- Test data: One planted fake key.
- Expected result: The configuration is stored. The key is sealed and never appears in a prompt, log or output. Step 6 ends the run as `failed_technical` with MSG-30.
- Status: Not run.

##### TC-40 Build a journal profile
- Traces: UC-40; FR-106 to FR-109, FR-260, FR-261; BR-74.
- Priority, level, method: Could; L3; Test.
- Preconditions: An allowed corpus exists. Run after the MVP.
- Steps: 1. Build a profile. 2. Trace each feature to a corpus snapshot and a source span. 3. Approve the profile. 4. Run the paper stage. 5. Do not approve a second profile and run the paper stage. 6. Compare the claims with and without the profile.
- Test data: One corpus; two profiles.
- Expected result: The profile has source, usage rights, uncertainty and version. It separates observed practice from mandatory publisher rules. The paper stage refers to the approved version only. The profile changes neither the content nor the certainty of a claim.
- Status: Not run.

##### TC-41 Compare methods
- Traces: UC-41; FR-139 to FR-145, FR-194, FR-267 to FR-269; BR-82, BR-83, BR-93, BR-96, BR-98, BR-99.
- Priority, level, method: Should; L3; Test.
- Preconditions: A project with a dataset. Run after the MVP.
- Steps: 1. Choose claim type `method_comparison`. 2. Request patterns G, H, I and J with baseline policy F. 3. Read the comparison design. 4. Run with a method that has a larger tuning budget. 5. Run with tuning. 6. Read the EvidenceBundle. 7. Read the AnalysisPlan: the evidence families, the metric policy and protocol, and the baseline policy. 8. Request pattern G, H, I or J for a `prediction` claim.
- Test data: Three methods; one `prediction` claim.
- Expected result: Methods are compared in pairs on each fold and seed, over many seeds, with the same tuning budget. Nested validation is used when tuning is included. Multiple comparisons are corrected. Step 4 turns the stage item red. Negative results stay in the EvidenceBundle. The plan holds discrimination, reliability and decision in this order. The task family chooses the metric policy and protocol. Pattern F is the baseline policy. Step 8 is refused: patterns G to J belong to `method_comparison` only.
- Status: Not run.

#### 4.2.2 Rule-level cases

These cases check rules that a use case scenario does not fully cover.

##### TC-42 Split by power and group integrity
- Traces: UC-18; FR-41, FR-42, FR-113, FR-182, FR-183; BR-08, BR-26, BR-41, BR-43, BR-44, BR-76, BR-84, BR-85, BR-88, BR-89.
- Priority, level, method: Must; L1; Test.
- Preconditions: Fixture B variants: large n, medium n, n below the minimum; with a group column; with a time column; IID data.
- Steps: 1. Request a split before the Researcher confirms the structure. 2. Confirm the structure and create the split for each variant. 3. Check the parts for shared groups. 4. Check the order of parts for time data. 5. Check the method for IID data.
- Test data: Four variants of Fixture B.
- Expected result: Step 1 creates no split. The large variant gets `three_way`, the medium variant `two_way`, the small variant `none` with a limitation. Rows of one group stay in one part. Time data splits in time order. IID data with a classification task family may get a repeated stratified split, only within the exploration part; the confirmation part is used once.
- Status: Not run.

##### TC-43 Dataset checks that do not use the outcome
- Traces: UC-18; FR-38, FR-114 to FR-118, FR-184, FR-185; BR-08, BR-26, BR-41, BR-43, BR-44, BR-76, BR-84, BR-85, BR-88, BR-89.
- Priority, level, method: Must; L1; Test.
- Preconditions: Fixture B with planted anomalies: duplicate rows across split parts, a post-outcome column, covariate shift, label shift, concept drift, low positive rate, a categorical column with high cardinality, high missingness.
- Steps: 1. Run the dataset stage. 2. Request a cleaning step that needs the outcome. 3. Read the shift report. 4. Read the dictionary. 5. Read the duplicate check. 6. Read the data signals. 7. Check which statistics the prefilter reads.
- Test data: Fixture B with the planted anomalies and a record of expected findings.
- Expected result: The cleaning step moves to the AnalysisPlan. The three kinds of shift are reported apart. The dictionary records when each variable is available and flags the post-outcome column. The duplicates across parts are reported. The data signals are flagged with a suggestion. The prefilter uses marginal distributions only.
- Status: Not run.

##### TC-44 Hypothesis testability rules
- Traces: UC-19; FR-119 to FR-123, FR-187; BR-41, BR-45, BR-90, BR-91, BR-92.
- Priority, level, method: Must; L1; Test.
- Preconditions: Scripted hypotheses (Fixture D). The limit of secondary hypotheses (SR-06) is set.
- Steps: 1. Submit a hypothesis with comparator, metric, direction, scope and decision rule. 2. Submit a hypothesis with no comparator. 3. Submit a hypothesis with a deliberately weak baseline. 4. Submit a non-inferiority hypothesis with margin δ. 5. Give a non-significant p-value to an equivalence claim. 6. Submit more secondary hypotheses than the limit.
- Test data: Six scripted hypotheses.
- Expected result: Step 1 passes. Steps 2 and 3 are returned for repair with MSG-40. Step 4 maps the margin δ onto the SESOI regions of the verdict. Step 5 never concludes equivalence, because a non-significant p-value is not evidence of equivalence. Step 6 is refused above the limit.
- Status: Not run.

##### TC-45 Pipeline order and evidence families
- Traces: UC-20; FR-127, FR-128; BR-46, BR-50, BR-83, BR-86, BR-93, BR-94, BR-95, BR-96, BR-99.
- Priority, level, method: Must; L1; Test.
- Preconditions: A plan for `prediction`. The `method_comparison` plan (FE-19, Should, after the MVP) is checked in TC-41.
- Steps: 1. Read the pipeline order in the plan. 2. Read the order of the evidence families. 3. Seed each of the five order rules with a violation, one at a time: split not first, a learning step fitted outside the train part, resampling outside the train part, calibration or threshold chosen outside the validation part, the confirmation part used twice.
- Test data: Five seeded violations.
- Expected result: The plan records the order: split first; learning steps fitted on the train part only; resampling on the train part only; calibration and threshold on the validation part; confirmation part used once. The plan holds discrimination, reliability and decision in this order. Each seeded violation is flagged and blocked with MSG-61.
- Status: Not run.

##### TC-46 Rare-event metrics, calibration and baselines
- Traces: UC-20; FR-129 to FR-132, FR-195, FR-196; BR-46, BR-50, BR-83, BR-86, BR-93, BR-94, BR-95, BR-96, BR-99.
- Priority, level, method: Must; L1; Test.
- Preconditions: A `rare-event` plan and two datasets with different prevalence.
- Steps: 1. Read the metric policy of the plan. 2. Compare average precision between the two datasets. 3. Read the data used for calibration. 4. Read the baseline runs and the report of runtime.
- Test data: Two datasets with clearly different prevalence.
- Expected result: The metric is average precision or precision at fixed recall, not accuracy alone. The comparison across prevalences is refused. Calibration uses data apart from the training data. Simple baselines run first with the same split and the same tuning budget, and runtime is reported with the score.
- Status: Not run.

##### TC-47 Paper declarations, reporting checklist and writing rules
- Traces: UC-25; FR-67 to FR-69, FR-218 to FR-220; BR-56, BR-65, BR-73.
- Priority, level, method: Must; L3; Test; Inspection.
- Preconditions: An accepted EvidenceBundle for an association claim and one for a prediction claim.
- Steps: 1. Run the paper stage for both claims. 2. Read the author-only fields. 3. Read the AI-use statement. 4. Read the reporting checklist and follow each item to its anchor. 5. Read the writing rules of kinds H, M and G.
- Test data: Two bundles.
- Expected result: Author-only fields show the placeholder "awaiting author". The AI-use statement comes from the decision log. The checklist is STROBE (observational studies) with RECORD (routinely collected data) for association, and TRIPOD (prediction models) for prediction. Each item points to an anchor. A violation of kind H is an error, kind M over the threshold is an issue, kind G is part of the reviewer rubric.
- Status: Not run.

##### TC-48 Disclosure modes, release log and model input
- Traces: UC-30; FR-81 to FR-83, FR-232 to FR-235; BR-19, BR-20, BR-21, BR-22, BR-80.
- Priority, level, method: Must; L2; Test.
- Preconditions: A paired Local Node and a `local` dataset version.
- Steps: 1. Set disclosure `standard` and run a job. 2. Set disclosure `strict` and run a job that returns a number of an unapproved kind. 3. Compare the release log of the Local Node with the Platform copy. 4. Inspect every prompt and every published artifact. 5. Raise an exception on real data.
- Test data: One approved kind and one unapproved kind of number.
- Expected result: Step 1 releases automatically within policy. Step 2 passes only approved kinds and creates a release review item with MSG-22. Every release is in the append-only release log and the two logs match. Prompts and artifacts hold only aggregates and code-computed profiles. The exception returns only error type, column and affected row count.
- Status: Not run.

##### TC-49 Same path for user and agent; fitness acceptance; assumptions
- Traces: UC-16; FR-33, FR-34, FR-36, FR-179, FR-180; BR-26, BR-27, BR-28, BR-29, BR-32, BR-33, BR-75.
- Priority, level, method: Must; L3; Test.
- Preconditions: Preset `milestones`. Three datasets with fitness `fit`, `fit_with_limits`, `not_fit`.
- Steps: 1. Do an action as a user and the same action as an agent. 2. Read the decision log. 3. Accept the fitness of each dataset. 4. Let the agent make an assumption.
- Test data: Three datasets.
- Expected result: Both actions pass the same tools, guards and checks, and the decision log records the actor. Fitness `fit` is `auto` (logged), `fit_with_limits` is `do_then_review`, `not_fit` is `must_ask`. The assumption is in the decision log with alternatives and reason and is not treated as the intent of the Researcher.
- Status: Not run.

#### 4.2.3 Stage acceptance and connection check

Each case runs one live scenario. The stage passes when every hard check is green. The hard checks of each stage are:

| TC | Hard checks of the scenario |
|---|---|
| TC-50 Acceptance, harness (the shared runtime of all engines) | Contract items turn green. The level follows the preset. A user who is `away` does not block the run. The review loop stops after two revision rounds. |
| TC-51 Acceptance, dataset stage | The DatasetSnapshot has every part. The anomalies planted in the data are found. Cleaning that touches the outcome moves to the plan. A join on an invalid key is refused. Fitness `fit_with_limits` comes with a reason. |
| TC-52 Acceptance, hypothesis stage | The screening flow adds up. The evidence map has at least one cell that can be checked against the snapshot. The HypothesisSet has all hypotheses with contribution type, draft estimand and source. Every number in an evidence card is inside its quotation. |
| TC-53 Acceptance, experiment_design stage | Every contract item is green. The twin recovers the planted effect. The false-positive rate of the permutation test is inside the allowed range. The Lock has golden outputs. |
| TC-54 Acceptance, execution stage | The dry run matches the data. Confirmatory results open only after unseal. Holm correction (control of the family-wise error rate across hypotheses) and gatekeeping (ordered testing of hypotheses) apply. The tried ledger has a noise threshold. A candidate is confirmed and has a tier. The replicator hash equals the bundle hash. |
| TC-55 Acceptance, paper stage | The ten contract items are green. At least three main figures have numbers equal to bundle records. No digit is outside a reference. The coverage table of the reporting checklist is complete. |
| TC-56 Acceptance, Local Node | Pairing by code works. A dataset is proposed from the folder. The release log of the Local Node equals the Platform copy. A differencing query is rejected. A packet capture shows 0 rows of data in messages that leave the machine. |
| TC-57 Connection check across stages | Run only after TC-50 to TC-56 pass. Pinned objects and hashes are consistent across all stages. A change of the snapshot marks every downstream object `stale`. A lane E candidate returns to the inbox and round two uses the reserve. A user who is `away` overnight at `milestones` with a pinned item waiting: the run is in `waiting(decision)` until the wait deadline of the item, work that does not depend on the item continues, the item stays in the decision inbox and the system sends an external notice and a reminder before the deadline. At the deadline the run ends `ended(with_gaps)`, the item closes unanswered and nobody decides it. The replication package reproduces the hash of the bundle. |

Preconditions for all acceptance cases: the upstream hand-off object is a frozen fixture (Fixture C), the model profile is real and the user follows a script. Expected result: one live run ends with every hard check green. Status: Not run.

#### 4.2.4 Benchmarks

##### TC-58 Seeded-flaw bench and red-team catalogue (evaluation round)

- Traces: UC-29; FR-135, FR-136, FR-137; BR-40, BR-86, BR-87, BR-100; SM-09, SM-17, SM-18.
- Priority, level, method: Should (on request); L5; Analysis.
- Preconditions: The catalogue holds the three groups of seeded flaws in BR-100. Each seeded flaw is planted in a case that the system can run.
- Steps: 1. Plant each flaw of the data group, the experiment group and the inference group, one per case. 2. Run the system on each case. 3. Record for each case whether the system detected the flaw. 4. Plant each pipeline order violation of FR-127 (TC-45), one per case. 5. Record for each case whether the system blocked the violation before the run. 6. Compute the rates below.
- Expected result: The report holds the detection rate and the block rate. The detection rate is at least 90% (SM-17) and the block rate is 100% (SM-18).
- Status: Not run.

SM-17 measurement procedure (detection rate of seeded leakage):

1. List the seeded flaws that the team classifies as leakage. The catalogue does not mark them (Open item 2). Leakage means that information from data held out for evaluation reaches the training or the analysis choices.
2. Seed one flaw per case, on a case with known clean results.
3. Run the system. A flaw counts as detected when a check, a guard or a finding names the flaw and its location.
4. SM-17 = number of detected seeded leakage flaws / number of seeded leakage flaws.
5. Run a clean case for each seeded case. A detection on a clean case is a false positive. Report the false positives with the rate.

SM-18 measurement procedure (block rate of seeded pipeline order violations):

1. Seed one violation per case for each rule of the pipeline order (BR-86, FR-127): split not first; a learning step fitted outside the train part; resampling outside the train part; calibration or threshold chosen outside the validation part; the confirmation part used more than once.
2. Run the system. A violation counts as blocked when the guard stops it before the run. A violation that the system records as a deviation counts as recorded, not blocked (BR-87). Report both counts.
3. SM-18 = number of blocked seeded violations / number of seeded violations.
4. Run a correct pipeline for each rule. A block on a correct pipeline is a false positive.

##### TC-59 Negative test per research pattern

- Traces: UC-29; FR-134.
- Priority, level, method: Must; L5; Test.
- Preconditions: The research pattern registry holds the patterns. Each pattern has a case with a seeded flaw.
- Steps: 1. For each pattern, run the case with the seeded flaw. 2. Record whether the pattern detects the flaw.
- Expected result: Every pattern detects its seeded flaw.
- Status: Not run.

##### TC-60 Paper reproduction bench

- Traces: SM-13.
- Priority, level, method: Should (on request); L5; Analysis.
- Preconditions: A published paper with open data and a known primary estimate. The paper set is not defined (Open item 4).
- Steps: 1. Run the system on the open data with the research question of the paper. 2. Compare the direction and the interval overlap of the primary estimate. 3. Compute the coverage of the reporting checklist. 4. Score the major flaws with the Reviewer 2 rubric.
- Expected result: The result is not worse than the rate of papers with no major flaw that comparable data-to-paper systems report (SM-13). The comparison rate comes from the literature (Open item 4).
- Status: Not run.

##### TC-61 Benchmark case catalogue inspection

- Traces: FR-138; BR-101.
- Priority, level, method: Must; L5; Inspection.
- Steps: 1. Count the sample projects. 2. Check that each is a test case of a research pattern. 3. Check that each BC maps to one case in section 4.1.3.
- Expected result: 60 sample projects, each mapped to one case.
- Status: Not run.

##### TC-101 Seeded-flaw bench capability check

- Traces: UC-29; FR-77, FR-135, FR-136, FR-137; BR-40, BR-100; SM-09, SM-17, SM-18.
- Priority, level, method: Must; L5; Test.
- Preconditions: The red-team catalogue is loaded into the seeded-flaw bench. A minimal case set holds one seeded flaw from each group (data, experiment, inference) and one pipeline order violation.
- Steps: 1. Run the bench on the minimal case set. 2. Read the bench output.
- Expected result: The bench runs every case. The output holds the precision of each reviewer persona, the detection rate of seeded leakage (SM-17) and the block rate of seeded pipeline order violations (SM-18). This case checks that the measurement works; it does not judge the rates against a target.
- Status: Not run.

#### 4.2.5 Benchmark case procedure

Cases TC-62 to TC-74 use one procedure. A case with one BC (TC-62 to TC-70) runs it once. A parameterized case (TC-71 to TC-74) runs it for each BC in its group (section 4.1.3). Wave 1 and wave 2 cases run first.

- Traces: FR-138, FR-124 to FR-132, FR-134; BR-96, BR-101.
- Preconditions: The sample project of the BC exists, with its dataset and research case. The sample data is not defined yet (Open item 3).
- Steps: 1. Start a run from the research case of the BC. 2. Read the task family in the AnalysisPlan. 3. Read the pattern in the AnalysisPlan. 4. Check the baseline policy (pattern F), the pipeline order and the order of the evidence families. 5. For a `rare-event` case, read the metric policy. 6. Run to unseal. 7. Read the hard checks.
- Expected result: The AnalysisPlan records the task family and the pattern of the BC. The baseline policy and pipeline order are recorded. For a `rare-event` case, the metric is average precision or precision at fixed recall and no comparison crosses prevalences. Every hard check is green. Code computes the verdict.
- Notes: BC-C07 has pattern G (FE-19, Should, after the MVP) and is in wave 1 (Report III, Open item 6). BC-I17 uses anomaly detection and BC-R19 uses multi-output regression, which are outside the four task families (Report III, Open item 7). Until the team decides, a result for these two cases is reported but does not count toward the exit criteria.
- Status of TC-62 to TC-74: Not run.

#### 4.2.6 NFR measurement

Each case measures the criterion that Report III states for the NFR. Status of all: Not run.

| TC | NFR | Procedure | Measurable criterion (Report III) |
|---|---|---|---|
| TC-75 Performance | NFR-01, NFR-02 | 1. Create a project with 100 runs and load test the run list and the decision inbox in a pre-release test environment. 2. Emit trace events from an engine and compare the emit time with the display time on a shared clock. | NFR-01: 95th percentile (p95) under 2 seconds. Load test in a pre-release test environment.<br>NFR-02: p95 under 5 seconds from event to display. Test with a shared clock. |
| TC-76 Run termination and failure handling | NFR-03, NFR-04 | 1. Review the run states of every project and look for runs that are not in `waiting` and have not reached `ended`, and for runs in `waiting` with no waiting item and no offline Local Node. 2. Cut the model provider and an external source. 3. Count fake outputs and read published objects. | NFR-03: 100% of runs that are not in `waiting` reach `ended`; 0 runs in `waiting` with no waiting item and no Local Node offline; 0 runs in `waiting(decision)` past the wait deadline of a pinned item. Review of run states per project.<br>NFR-04: 0 fake outputs in a test that cuts the model provider; 100% of published objects readable after the failure. Fault-injection test. |
| TC-77 Spending within ceilings | NFR-05 | 1. Check the usage ledger for runs over the token budget that did not end `with_gaps`. 2. Check the decision inbox for a `spending` item for every project at 100% of the monthly budget. | NFR-05: 0 runs over the token budget that did not end `with_gaps`; 0 runs at 100% of the monthly budget with no `spending` item. Check of the usage ledger and the decision inbox. |
| TC-78 Availability | NFR-06 | 1. Monitor the health of the Platform for one calendar month. 2. Compute the share of minutes with a passing health check. | NFR-06: At least 99% of the minutes of each calendar month have a passing health check (Open item 14). Health monitoring. |
| TC-79 Hash stability after restart | NFR-07 | 1. Record the hash of every accepted object. 2. Restart the system. 3. Compare the hashes and read the objects. | NFR-07: 100% of accepted objects keep their hash after a restart. Restart test. |
| TC-80 Project isolation | NFR-08 | 1. Create two projects with runs, a Literature Base, inbox items and audit entries. 2. As a member of project 1 try every path to the data of project 2. | NFR-08: 0 paths that read data, runs, Literature Base, inbox or audit log of another project. Two-project test. |
| TC-81 Secrets outside the Platform | NFR-09 | 1. Plant a fake key. 2. Run all stages. 3. Search prompts, logs, traces and outputs for the key. | NFR-09: 0 keys or secrets in prompts, logs, traces and outputs. Test with a planted fake key. |
| TC-82 Seal before unseal | NFR-10 | 1. Run the execution stage. 2. Search trace and workspace for confirmatory estimates before unseal. 3. Request unseal earlier than the last lane C fix. 4. Read the envelope log and the unseal log. | NFR-10: 0 confirmatory estimates in trace and workspace before unseal; 100% of unseal requests earlier than the last lane C fix rejected. Check of the envelope log and unseal log. |
| TC-83 Audit log completeness | NFR-11 | 1. Do every administrative and security action once. 2. Compare with the audit log. 3. Try to edit and delete entries. | NFR-11: 100% of actions recorded; 0 edits or deletions of records. Test. |
| TC-84 Privacy of local data and release log | NFR-12, NFR-13 | 1. Run the Local Node acceptance scenario with a packet capture. 2. Search the capture for rows of `local` data. 3. Compare the release log of the Local Node with the Platform copy. | NFR-12: 0 rows of `local` data in any message that leaves the Local Node. Packet capture in the Local Node acceptance scenario.<br>NFR-13: 100% match. Log comparison in the acceptance scenario. |
| TC-85 Small-cell and differencing rejection | NFR-14 | 1. Send two queries that differ by fewer rows than the threshold. 2. Read the result and the reason shown. | NFR-14: 100% of such queries rejected and shown with the reason. Test with two queries that differ by fewer rows than the threshold. |
| TC-86 Usability | NFR-15, NFR-16, NFR-17 | 1. Ask 5 new users to create a first run. 2. Show random items and ask for the source of each. 3. Ask users to explain the five verdict labels without help. | NFR-15: At least 5 of 5 users succeed in a test with 5 people. Usability test.<br>NFR-16: At least 9 of 10 random items given the right source by users. Usability test.<br>NFR-17: At least 4 of 5 labels explained correctly with no help. Usability test. |
| TC-87 Accessibility | NFR-18 | 1. Run automatic and manual checks against the Web Content Accessibility Guidelines (WCAG) 2.1 level AA on the main screens. 2. Use the decision inbox and the result tables with a keyboard only. | NFR-18: 0 level A and AA failures on the main screens in automatic and manual checks. Accessibility evaluation. |
| TC-88 Localization | NFR-19 | 1. Extract the system-generated interface strings. 2. Check each string for English. | NFR-19: 100% of system-generated interface strings in English. Automatic check of interface strings. |
| TC-89 Maintainability inspection | NFR-20, NFR-21, NFR-22 | 1. Inspect that no guard, check, trace or decision-log mechanism belongs to one engine. 2. Inspect that every hard rule exists in the prompt and in a code validator. 3. Check the traceability matrix (section 4.1.2). | NFR-20: 0 guard, check, trace or decision-log mechanisms owned by one engine. Inspection.<br>NFR-21: 0 rules on one side only. Inspection.<br>NFR-22: 100% of FRs trace to a BR; every Must FR has at least one TC. Traceability matrix. |
| TC-90 Observability | NFR-23, NFR-24 | 1. Run a full run. 2. Compare actions and check changes with trace events. 3. Check the decision log fields. 4. Read the operating metrics of every run. | NFR-23: 100% of actions and check changes have an event; 100% of decisions have all decision-log fields. Test.<br>NFR-24: Number of questions, blocked time, overturn rate per action type and rate of `needs-you` items reported for 100% of runs. The target values are not yet defined (Open item 12). |
| TC-91 Replayability | NFR-25, NFR-26 | 1. Run the replicator for every accepted bundle. 2. Re-run the test set with the same pinned objects, Lock and seed. 3. Compare hashes. | NFR-25: 100% of accepted bundles have a replication package whose hash the replicator reproduces; otherwise the item is red. Replicator report.<br>NFR-26: 100% of runs in the test set give the same hash on a re-run. Re-run and hash comparison. |
| TC-92 Integrity of the PaperPack | NFR-27, NFR-28, NFR-29 | 1. Run the contract checks on every accepted PaperPack version. 2. Count digits outside the allowed list (years, item numbers, section numbers). 3. Map effect statements to verdicts. 4. Resolve citations. | NFR-27: 0 digits outside the allowed list (years, item numbers, section numbers) in an accepted PaperPack; 100% of numbers trace to a record. Contract check at each version.<br>NFR-28: 100% of effect statements in Abstract, Results and Discussion map to a verdict and an interpretation row; 0 claims above the ceiling. Claims contract check.<br>NFR-29: 100% of citations. Citations contract check. |
| TC-93 Review loop integrity | NFR-30 | 1. Compare accepted object versions with the review records. 2. Count revision rounds. 3. Compare remaining findings with the PaperPack. | NFR-30: 100% of accepted object versions have a review record; no more than 2 revision rounds per version; 100% of remaining findings shown in the PaperPack. Comparison with review records. |
| TC-94 AI PI limits | NFR-31 | 1. Run `autopilot` with the user `away`. 2. Count AI PI decisions on pinned items. 3. Check that every tentative decision is in the inbox when the user returns. | NFR-31: 0 AI PI decisions on pinned items; 100% of tentative decisions in the decision inbox when the user returns. Test of `autopilot` with the user `away`. |

#### 4.2.7 Additional cases

These cases cover requirements that a use case scenario does not check alone. All have the status "Not run".

##### TC-95 Sign in with a Google account
- Traces: UC-01; FR-146; BR-01, BR-103.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. A Google account whose verified email address belongs to an invited user of project P. A second Google account whose email address is not verified.
- Steps: 1. Select sign-in with a Google account and complete it with the first account. 2. Read the projects shown. 3. Sign out and repeat with the second account. 4. Select sign-in with a Google account and cancel it.
- Test data: Two Google accounts, one with a verified email address and one without.
- Expected result: After step 1 a session opens. The system asks for no password. Step 2 shows project P and only the projects of the user. Step 3 shows MSG-57 and opens no session. Step 4 shows MSG-56 and opens no session.
- Status: Not run.

##### TC-96 One user for both sign-in methods
- Traces: UC-01; FR-146; BR-103.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. User U signed in with an email address (TC-01) and is a member of project P. A Google account has the same verified email address.
- Steps: 1. Sign in with the Google account. 2. Read the user and the projects shown. 3. Sign in again with the email address. 4. As Platform Admin read the user list.
- Test data: One email address used by the email sign-in and by the Google account.
- Expected result: Steps 1 and 3 give the same user with the same projects and roles. The user list holds one entry for the email address.
- Status: Not run.

##### TC-97 Preset level table and floors
- Traces: UC-15; FR-147, FR-148, FR-149, FR-150; BR-24, BR-25, BR-26, BR-33, BR-49, BR-61.
- Priority, level, method: Must; L1; Test.
- Preconditions: A project with one action in each of the eight action groups. The spending ceiling is set (TC-34). Three datasets with fitness `fit`, `fit_with_limits` and `not_fit`.
- Steps: 1. Set the preset `co_work` and read the level of one action in each action group. 2. Repeat with `milestones` and accept the fitness of each dataset. 3. Repeat with `autopilot` and raise one spend below and one above the ceiling. 4. At each preset read the level of `unseal` when every check is green and when one check is red. 5. Override `object_drafting` below `do_then_review` and `pinned` below `must_ask`. 6. Override each other action group to `auto`.
- Test data: One action per action group; one spend below and one above the ceiling.
- Expected result: At `co_work`, `read_compute` is `auto`, `technical_fix` is `do_then_review`, and `content_judgment`, `object_drafting`, `spending`, `acceptance` and `pinned` are `must_ask`. At `milestones`, `read_compute` and `technical_fix` are `auto`, `content_judgment` and `object_drafting` are `do_then_review`, `spending` and `pinned` are `must_ask`, and `acceptance` follows the code verdict. At `autopilot`, `read_compute`, `technical_fix` and `content_judgment` are `auto` (`content_judgment` is logged), `object_drafting` and `acceptance` are `do_then_review`, `spending` is `auto` below the ceiling and `must_ask` above it, and `pinned` is `must_ask`. At every preset `unseal` is `auto` when every check is green and is not `auto` while a check is red. The two overrides in step 5 are rejected and the system shows the floor. The overrides in step 6 are accepted.
- Status: Not run.

##### TC-98 A waiting pinned item does not end the run before its deadline
- Traces: UC-12, UC-17; FR-178, FR-262; BR-14, BR-31, BR-58, BR-78, BR-104.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. Preset `milestones` and the user `away`. A run that reaches the pinned item "lock plan". A wait deadline for pinned items that is longer than the wait in step 1 (SR-08). Short response time for `spending` items (SR-04).
- Steps: 1. Let the run reach the pinned item and keep the user away for a time shorter than the wait deadline. 2. Read the stage state and the run state. 3. Read the inbox and the notices. 4. Return as the user and lock the plan. 5. On a second run use up the token budget. 6. On a third run let a `spending` item pass its deadline (TC-33). 7. On a fourth run in `waiting(decision)` cancel the run (TC-13). 8. On a fifth run let a pinned item pass its wait deadline (TC-100).
- Test data: Five runs.
- Expected result: In step 2 the stage is at `ready_to_<action>` and the run is in `waiting(decision)`. The run does not end before the wait deadline. Work that does not depend on the item continues. In step 3 the item stays in the inbox and the system sends an external notice. After step 4 the run returns to `running`. Step 5 ends the run as `ended(with_gaps)` on the best output. Step 6 ends the run as `ended(with_gaps)`. Step 7 ends the run as `ended(cancelled)`. Step 8 ends the run as `ended(with_gaps)`. No other event ends a run with gaps.
- Status: Not run.

##### TC-99 Reminder before the wait deadline of a pinned item
- Traces: UC-16, UC-38; FR-08, FR-263, FR-264; BR-28, BR-104.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. A Researcher R1 created the run. A short wait deadline for pinned items (SR-08). A scripted clock. A `spending` item exists on another run (TC-33).
- Steps: 1. As Project Manager set the wait deadline of pinned items. 2. Let R1's run reach the pinned item "lock plan" with the user `away`. 3. Move the clock to just before the wait deadline. 4. Read the external notices of R1, of the Project Manager and of a Reviewer. 5. Read the reminder of the `spending` item. 6. Answer the pinned item as R1.
- Test data: One pinned item; one `spending` item; three members.
- Expected result: Step 1 stores the wait deadline. After step 2 the item has a wait deadline. In step 4 R1 and the Project Manager each get an external notice with the reminder (MSG-59); the Reviewer gets none. In step 5 only the Project Manager gets the reminder (MSG-27). After step 6 the run returns to `running`.
- Status: Not run.

##### TC-100 A pinned item expires unanswered and the run ends with gaps
- Traces: UC-12, UC-16; FR-32, FR-262, FR-263, FR-265, FR-266; BR-14, BR-31, BR-104.
- Priority, level, method: Must; L3; Test.
- Preconditions: Fixture A. Preset `autopilot` and the user `away`. A short wait deadline for pinned items (SR-08). A scripted clock. A run with accepted objects that reaches the pinned item "lock plan".
- Steps: 1. Let the run reach the pinned item. 2. Let the AI PI work on unpinned items. 3. Move the clock past the wait deadline with no answer. 4. Read the run state, the item, the decision log and the list of gaps. 5. Return as the user.
- Test data: One pinned item; one unpinned item.
- Expected result: Before the deadline the run is in `waiting(decision)`. At the deadline the run ends as `ended(with_gaps)` on the best output and shows MSG-60. The pinned item closes unanswered and the gap is listed. The decision log holds no decision on the pinned item from the AI PI or a default value. Accepted objects stay. After step 5 the user sees the expired item and the gap.
- Status: Not run.

## 5. Test reports

The cases of section 4 are not run, so this section reports no result. The templates below are for use at execution.

### 5.1 Test summary report template

Report identification:

| Field | Content |
|---|---|
| Report ID and version | |
| Test cycle and level | |
| Product version under test | |
| Period | |
| Author and reviewer | |
| Test environment | |

Execution summary by level:

| Level | Planned | Run | Passed | Failed | Blocked | Skipped | Not run |
|---|---|---|---|---|---|---|---|
| L1 Unit and contract | | | | | | | |
| L2 Integration | | | | | | | |
| L3 System | | | | | | | |
| L4 Acceptance | | | | | | | |
| L5 Benchmarks | | | | | | | |
| L6 NFR measurement | | | | | | | |
| Total | | | | | | | |

The count of "Skipped" cases comes with a reason for each case.

Requirement coverage:

| Measure | Value |
|---|---|
| Must FRs with at least one passing case | |
| Must FRs with no passing case (list) | |
| Stage acceptance scenarios passed (stages and Local Node) | |
| Connection check | |
| NFRs measured against the approved threshold | |

NFR and benchmark results:

| Item | Measured value | Criterion | Result |
|---|---|---|---|
| NFR-xx | | | |
| SM-09 persona precision | | | |
| SM-13 paper reproduction | | | |
| SM-17 detection rate of seeded leakage | | | |
| SM-18 block rate of seeded pipeline order violations | | | |

Defect summary:

| Severity | Opened | Fixed and verified | Open | Deferred with approval |
|---|---|---|---|---|
| S1 Critical | | | | |
| S2 Major | | | | |
| S3 Minor | | | | |
| S4 Trivial | | | | |

Other sections of the report: deviations from the plan; evaluation of the exit criteria (section 2.2); residual risks; recommendation (release, release with conditions, do not release); approval signatures of the test lead and the supervisors.

### 5.2 Defect report template

Defect report fields:

| Field | Content |
|---|---|
| Defect ID | |
| Title | |
| Reported by and date | |
| Test case ID (TC-xx) | |
| Traced UC, FR, NFR or BR | |
| Product version and environment | |
| Steps to reproduce | |
| Expected result and actual result | |
| Evidence (record, trace, screenshot) | |
| Severity (S1 to S4) | |
| Priority (P1 to P4) | |
| Owner | |
| Status | New, Confirmed, In progress, Fixed, Verified, Closed, Rejected, Deferred |
| Fix reference and verification result | |

Severity measures the effect of the defect on the product promises and on the users.

| Severity | Definition | Examples |
|---|---|---|
| S1 Critical | The defect breaks a product promise or a safety rule. | A row of `local` data leaves the Local Node. A key appears in a prompt, log or output. The agent sees a confirmatory estimate before unseal. A wrong verdict or a claim above the ceiling is published. A run produces a fake output. |
| S2 Major | A Must function does not work, and no workaround exists. | A run cannot reach `ended`. A Dossier is exported without approval. The review loop runs more than two revision rounds. |
| S3 Minor | A function works with a workaround, or an error message is wrong. | A message does not match the catalogue (CR-05). A list is not paged (CR-01). |
| S4 Trivial | A cosmetic defect with no effect on use. | A label is misaligned. |

Priority measures the order of the fix.

| Priority | Definition |
|---|---|
| P1 | Fix at once. It blocks testing or the release. |
| P2 | Fix before the end of the current sprint. |
| P3 | Fix before the release. |
| P4 | Fix when time allows, or defer with approval of the supervisors. |

Triage rules:

- The test lead sets the severity at triage. The owner of the area proposes the priority.
- An S1 defect gets P1.
- A defect found by a benchmark is also a finding of the review documents when it concerns a document.
- The test lead re-tests a fixed defect. A fixed defect is closed only after the re-test of the failed case and a regression run of the area.

## Open items

1. Closed. TC-58 checks SM-17 (at least 90%) and SM-18 (100%) (Report III, Open item 3).
2. The catalogue (BR-100) does not mark which seeded flaws count as leakage for SM-17. The team needs to classify them before the bench runs.
3. The benchmark case catalogue gives each case a name, task family, pattern and feature. It gives no sample data and no case-specific expected result. TC-62 to TC-74 check the pattern mechanics and the hard checks only.
4. The set of published papers for the paper reproduction bench is not defined. The comparison rate for SM-13 comes from the literature and is not in the sources.
5. The minimum precision of a reviewer persona (SM-09), the small-cell threshold, the rounding rule, the probe budget and the minimum sample size for the split are not given as values. The cases use the configured values.
6. BC-C07 is in wave 1 but its pattern G belongs to FE-19; BC-I17 and BC-R19 use tasks outside the four task families (Report III, Open items 6 and 7). The decisions are open.
7. The sources specify no browser matrix and no operating system matrix for the Local Node. Cross-browser testing is out of scope until the team sets one.
8. Dates for the re-planned sprints (Report II, O-1) and responsibilities for the Local Node, execution stage, paper stage and Dossier (Report II, O-3) are open. The milestones in section 3.3 follow the baseline weeks only.
9. The team has four members, and none is an independent tester. The test lead reviews cases written by others. The team needs to decide whether supervisors or another party give independent review.
10. The content of the writing rules of kinds H, M and G is not defined (Report III, Open item 2). TC-47 checks the kinds, not the content of each rule.
11. The severity and priority definitions, the suspension criteria and the exit thresholds beyond the release conditions of the product requirements are proposed by this section. The team needs to approve them.
12. The target values for the operating metrics (NFR-24) are not defined (Report III, Open item 1). TC-90 checks that the metrics are reported.
13. The budget for live model runs (stage acceptance and benchmarks) is not defined.
14. Closed. TC-78 measures the whole calendar month (Report III, Open item 12).
15. Closed. The default wait deadline of pinned items (SR-08) is 7 days. TC-98 to TC-100 may use a shorter configured value.

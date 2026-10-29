# I. Project Introduction

## Acknowledgement

We thank FPT University and the Faculty of Software Engineering for the academic environment, the project framework, and the resources that this capstone project required.

We thank Trần Trọng Huỳnh for practical guidance on project organization, delivery planning, and report preparation. This guidance helped us structure the work and present the project in a consistent manner.

We thank Lâm Hữu Khánh Phương for academic guidance on the research direction, the system scope, the requirements, and the scientific quality of the project. This guidance helped us turn an initial idea of AI-assisted data analysis into a controlled workflow that emphasizes evidence, reproducibility, and human decisions.

We also thank the lecturers, reviewers, and classmates who gave comments or practical views on scientific data analysis and software development.

Finally, we thank our families and friends for their support throughout the project. The team accepts responsibility for the content of this report and will continue to revise the project based on review feedback.

## Definitions and Acronyms

### Acronyms

| Acronym | Meaning |
| ----- | ----- |
| AI | Artificial Intelligence |
| AI PI | AI Principal Investigator (see Definitions) |
| BO | Business Objective |
| BP | Business Problem |
| BR | Business Rule |
| BRD | Business Requirements Document |
| FE | Feature |
| FR | Functional Requirement |
| IMRaD | Introduction, Methods, Results, and Discussion (manuscript structure) |
| JFE | Journal Fingerprint Extraction |
| MoSCoW | Must, Should, Could, Won't (priority scale) |
| MVP | Minimum Viable Product |
| NFR | Non-Functional Requirement |
| PRD | Product Requirements Document |
| RECORD | REporting of studies Conducted using Observational Routinely-collected health Data |
| SESOI | Smallest Effect Size Of Interest |
| STROBE | STrengthening the Reporting of OBservational studies in Epidemiology |
| TRIPOD | Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis |

### Definitions

This report uses the terms below, as defined in the project glossary. Each concept has one name.

| Term | Definition |
| ----- | ----- |
| Acceptance | The action that accepts a version of a hand-off object so that a later stage can use it. |
| Action group | One of eight groups used to set permissions: `read_compute`, `technical_fix`, `content_judgment`, `object_drafting`, `spending`, `acceptance`, `pinned`, and `unseal`. |
| AI Principal Investigator (AI PI) | A system-side connector persona. It summarizes, proposes the next step, and makes only tentative decisions on items that are not pinned, when the preset is `autopilot` and the user is `away`. The AI PI never ends a run and never decides a pinned item. |
| AnalysisPlan | The hand-off object of the `experiment_design` stage. It holds the estimand, the protocol for the claim type, the adjustment set, the analysis program, the decision rule, the interpretation table, and the robustness set. It plans the analysis of existing tabular data only. |
| Approval | The decision of a Reviewer or Project Manager to approve a Dossier, under the review settings of the project. |
| Audit log | An append-only record of all administrative and security operations in a project and in the system. |
| Candidate | A hypothesis that the exploration lane proposes. A candidate is never a claim. It enters the decision inbox so that the user can choose. |
| Candidate cap per round | A fixed number that limits how many candidates the exploration lane may put into the decision inbox in one round. |
| Claim ceiling | The strongest claim that the text may state. The `execution` stage computes it from the verdict, the grade, and the confirmation tier. The `paper` stage cannot exceed it. |
| Clean permutation check | A permutation test on the twin after the true effect is removed (the outcome is shuffled). The false-positive rate must stay within the allowed range. |
| Claim type | The type of claim of a hypothesis and of an AnalysisPlan: `association`, `causal`, `prediction`, and `method_comparison` (Should, after MVP). |
| Confirmation tier | The way a candidate is confirmed, from strongest to weakest: `replicated`, `reserve`, `unsealed_untouched`, `unsealed_touched`. |
| Contract item | A required part of a stage output, with a check by code. A stage is done when all items are green. |
| Data location | The place where data lives: `platform` (uploaded) or `local` (on the user machine, readable only by the Local Node). |
| Dataset | A tabular dataset in a project. It has one or more dataset versions. |
| Dataset version | An immutable version of a dataset, identified by a hash. Every analysis pins one dataset version. |
| DatasetSnapshot | The hand-off object of the `dataset` stage: source, table model, quality profile, dictionary, cleaning recipe, question map, split, source roles, and fitness. |
| Decision inbox | The single queue, for all stages, of the items that need the user. |
| Decision log | A record of every decision: action type, level, policy version, who decided (user, agent, or AI PI), presence, and whether it was overturned. |
| Deviation | A change to the locked algorithm. It is a pinned action and the system records it in the deviation log. |
| Disclosure mode | The release policy of a Local Node: `standard` (automatic within policy) or `strict` (only approved kinds of numbers; other kinds wait for a release review). |
| Dossier | The result package of a run for review and sharing. It references the accepted versions of the EvidenceBundle and the PaperPack. The Platform versions it, checks its hashes, and records approvals. The Platform does not judge the science. |
| Ended with gaps | The result of a run that ends for one of three causes: the token budget of the run is spent, a `spending` item passes its deadline, or a pinned item passes its wait deadline. The system publishes the best output and lists every red contract item. For a pinned item, the item closes unanswered, nobody decides it for the user, and the gap is listed. |
| Engine | The service that runs one stage. All engines run on the same harness. |
| EvidenceBundle | The hand-off object of the `execution` stage. It holds ten checked items, including the confirmatory result, the verdict, the grade, the diagnostics, the robustness results, the deviation log, the tried ledger, and the replication package. |
| Envelope | A sealed store at the Platform. It holds the confirmatory result until unseal. The agent sees only "done" or "error". |
| Executor | The place where an analysis job runs: inside the engine (cloud) or on a Local Node. Both use the same analysis library. |
| Finding | The result of a review, with category, severity (`blocking`, `major`, `minor`), anchor, evidence, failure scenario, and a fix. |
| Fitness | The conclusion of code on how well the data fit the question: `fit`, `fit_with_limits`, or `not_fit`. |
| Floor | The lowest level that an action type may have. An override cannot go below it. |
| Gatekeeping | Hierarchical testing: a secondary hypothesis is tested only after the primary hypothesis. |
| Grade | The A to D level of confidence in the evidence. Code computes it from diagnostics, robustness, and deviations. |
| Guard | A check that blocks an action before it runs. Examples are the data firewall, numbers-only-from-tools, immutability of locked objects, and secret filtering. |
| Hand-off object | A typed, versioned, hashed output of a stage. It is immutable after acceptance. Each stage boundary has exactly one kind. |
| Harness | The runtime shared by all engines: agent loop, action pipeline, workspace, live trace, budget, and hand-off. |
| Holm correction | A multiple-comparison correction by the step-down procedure of Holm. It tests p-values in increasing order with a gradually relaxed threshold and keeps the chance of at least one false positive within the preset level. The judge applies it to secondary hypotheses. |
| HypothesisSet | The hand-off object of the `hypothesis` stage: at least two hypotheses with different claim keys and one primary hypothesis. |
| Implanted effect | An effect of known size that the system plants in the twin. The rehearsal on the twin must recover it. |
| Journal Fingerprint Extraction (JFE) | A Could capability after MVP. It builds a profile of a journal from a corpus that the system may use, so that the `paper` stage can refer to it. |
| Known risk | A finding that remains after two revision rounds. The system records and shows it, or the user decides between the two sides. |
| Literature Base | The versioned, project-level store of literature evidence: search protocol, search log, screening decisions, evidence cards, evidence map, and checked BibTeX entries. All stages share it. |
| Local Node | A user-side service that keeps `local` data and runs jobs next to the data. It has a desktop application. |
| Lock | A separate object that records the locked plan: hashes of the specification, the program, and the golden outputs; the snapshot version; the split digest; who locked it; and when. The Platform writes it. |
| Needs-you | A decision inbox item that appears when a contract item has used its whole budget share. It is `must_ask` in every preset. |
| Next step | The proposal after a run, taken from a shared vocabulary: `collect_more_data`, `explore_signal`, `replicate`, `write_paper`, `revise_plan`. The AI PI proposes it and the user chooses. |
| PaperPack | The hand-off object of the `paper` stage: IMRaD manuscript, reporting checklist, claims, figures and tables, citations, limitations, reproducibility statement, declarations, review results, and export formats. |
| Persona | A lens with its own mandate, finding categories, skills, tools, and measured precision. A persona is a maker (creates objects), a guard (reviews objects), or a connector (links the run to the user; it neither creates nor reviews objects). |
| Pinned action | An action that is always `must_ask`, in every preset. Each pinned item has a wait deadline that the project settings define, and the system sends a reminder before it. Examples are the definition of the outcome and the estimand, the choice of hypotheses and the primary hypothesis, locking the plan, deviating from the locked algorithm, and exporting outside the project. |
| Pipeline | The order of stages of a run. The standard pipeline is `dataset_first`: `dataset`, `hypothesis`, `experiment_design`, `execution`, `paper`. |
| Pipeline order | The order that prevents leakage: split first; every learning step fits only on the train part; calibration and threshold selection use the validation part; the confirmation part is used once. |
| Platform | The system part that manages users, projects, runs, permissions, budget, keys, audit, and the Dossier. It does not judge the science. |
| Preset | A set of levels for the eight action groups, chosen per stage: `co_work`, `milestones` (default), `autopilot`. |
| Presence | Whether the user can be reached now: `present` or `away`. |
| Project | The shared workspace of a team. It holds members, settings, datasets, research cases, runs, the Literature Base, the decision inbox, and the audit log. |
| Probe budget | A limit on the number of probing queries on one dataset version. The release gate tracks it to limit inference from many aggregates. An exhausted probe budget is a gap and does not stop the run. |
| Project budget | The monthly cost limit of a project. At 100 percent, new runs are blocked and a running run waits for a budget review. |
| Release | An aggregate that leaves the place where the data lives. Data rows never leave. |
| Release gate | The single check point that every release passes: small-cell threshold, rounding, differencing check, and probe budget. |
| Release log | An append-only list of all releases of one dataset version. |
| Research case | The research intent of a run: topic, goal, context, constraints, domain, and references. A dataset is optional at the start. |
| Research pattern | A versioned research unit in a registry. It defines the applicable task family, eligibility rules, required columns, baseline policy, metric policy, statistical plan, failure modes, and negative tests. |
| Review loop | The mandatory independent review. It runs once for each object version after all checks are green. The reviewer has a fresh context. At most two revision rounds follow. |
| Review settings | The part of the project settings that sets the approval of a Dossier: number of approvals, who may approve, whether self-approval is allowed, and export formats. |
| Run | One execution of the pipeline for one research case. A project has at most one active run. |
| Run state | `running`, `waiting` (reason: `decision`, `node_offline`, or `budget_review`), or `ended` (result: `complete`, `with_gaps`, `failed_technical`, or `cancelled`). A pinned item that waits for an answer keeps the run in `waiting(decision)` until the pinned wait deadline. A run ends `with_gaps` for three causes only: the token budget of the run is spent, a `spending` item passes its deadline, or a pinned item passes its wait deadline. The Project Manager or the Researcher who created the run can cancel it from any state except `ended`. |
| Seeded-flaw bench | A dataset with planted flaws. It measures the precision of a reviewer. A reviewer below the threshold gets its finding severity lowered. |
| Split | The division of data rows into parts: `none`, `two_way`, or `three_way` (exploration, confirmation, and reserve). The `dataset` stage decides it from power. |
| Stage | One step of the pipeline: `dataset`, `hypothesis`, `experiment_design`, `execution`, or `paper`. |
| Task family | The type of outcome problem: `binary`, `multiclass`, `regression`, or `rare-event`. |
| Token budget | The limit of model tokens for one run. |
| Tried ledger | A record of every search procedure in the exploration lane and its noise threshold. The more the system searches, the higher the threshold for later candidates. |
| Unseal | The opening of the envelope. It happens automatically when all checks are green, or by hand if the user chose so. |
| Verdict | The conclusion that code computes for each hypothesis under the locked decision rule: `supported`, `trivial`, `not_supported`, `insufficient`, or `not_tested`. The model does not create verdicts. |
| Web app | The user interface in the browser. It shows the workspace, the decision inbox, and the live trace, and it receives the actions of the user. It holds no scientific logic. |

## 1. Overview

OpenAI-Scientist is a web app for research teams that work on tabular data. A Researcher starts with a research case. A dataset is optional at the start. The system then runs a fixed, dataset-first pipeline of five stages: `dataset`, `hypothesis`, `experiment_design`, `execution`, and `paper`. Each stage boundary has exactly one hand-off object. The hand-off object is typed, versioned, hashed, and immutable after acceptance.

The Platform divides the work into three parts. The AI proposes and writes text. Code computes numbers, checks, verdicts, grades, and claim ceilings. The Researcher keeps the decisions that only a person may take. A mandatory independent review applies to every object version. Data rows that stay on the user machine never leave it. A Local Node releases only aggregates through a release gate. The final result is a Dossier. Only an approved Dossier may leave the project.

The Platform is designed so that no error is hidden, every claim has a source, and every run can be replayed. It does not guarantee that the science is right.

### 1.1 Project Information

**Project name (English):** Design and Evaluation of an AI Data Agent for Automated Data Analysis Using User-Provided Datasets

**Project name (Vietnamese):** Thiết kế và Đánh giá Tác nhân AI Hỗ trợ Phân tích Dữ liệu Tự động trên Dữ liệu do Người dùng Cung cấp

**System name:** OpenAI-Scientist

**Project code:** FA26SE115

**Group name:** GFA26SE78

**Supervisors:** Lâm Hữu Khánh Phương ([phuonglhk@fpt.edu.vn](mailto:phuonglhk@fpt.edu.vn)), Trần Trọng Huỳnh ([huynhtt@fpt.edu.vn](mailto:huynhtt@fpt.edu.vn))

### 1.2 Project Team

The table identifies the project members and their principal responsibilities. Contact details are kept in the team records and are not repeated in this report.

| Full Name | Role | Main responsibility |
| ----- | ----- | ----- |
| Lê Vũ Phương Hòa | Project Lead / Backend | Project coordination, backend architecture, and release decisions |
| Ngô Thành Đạt | Backend | Data pipeline, scientific services, AI integration, and requirements |
| Trần Phú Thịnh | Frontend | Web interface, workspace screens, and frontend integration |
| Uông Tuấn Vũ | Frontend | Frontend support, test coordination, and release verification |

### 1.3 Users and Actors

The system has four human roles and two system actors.

| Role | Type | Main work |
| ----- | ----- | ----- |
| Platform Admin | System role | Manages users, models, keys, engine settings, default budgets, audit, and health. Sees project metadata only. |
| Project Manager | Project role | Manages members, settings, budget, datasets, and runs. Approves extra spending and Dossiers. Has all research rights of a Researcher. |
| Researcher | Project role | Creates research cases and runs. Answers the decision inbox, accepts hand-off objects, locks the plan, and exports results. |
| Reviewer | Project role | Reads and comments on all objects. Approves a Dossier under the review settings. |
| AI PI | System actor | Summarizes, proposes the next step, writes the lab notebook, and decides tentatively on items that are not pinned. |
| Persona (maker, guard, connector) | System actor | Creates objects (maker), reviews objects (guard), or links the run to the user (connector). |

*Figure 1: Pipeline and hand-off objects: diagram to be regenerated from the design model.*

| Order | Stage | Hand-off object | Main capability |
| ----- | ----- | ----- | ----- |
| 1 | `dataset` | DatasetSnapshot | Ingests data, profiles quality, flags leakage, decides the split, and concludes fitness. |
| 2 | `hypothesis` | HypothesisSet | Runs a methodical rapid review of the Literature Base and creates at least two testable hypotheses with one primary hypothesis. |
| 3 | `experiment_design` | AnalysisPlan and Lock | Plans the analysis of existing tabular data and locks the plan. |
| 4 | `execution` | EvidenceBundle | Runs the locked program, keeps the confirmatory result in the envelope, unseals it, and computes the verdict, grade, and claim ceiling by code. |
| 5 | `paper` | PaperPack | Drafts the manuscript package with reporting checklist, claims, citations, and limitations. |
| After 5 | Dossier | Dossier | Collects the accepted EvidenceBundle and PaperPack, goes through approval, and allows export. |

## 2. Product Background

Research on tabular data needs several steps: understand the dataset, ask an answerable question, find literature evidence, plan the analysis, run the analysis, and write the paper. Each step has its own risk. Table 1 groups the business problems that the BRD records (BP-01 to BP-16).

| Area | Business problems |
| ----- | ----- |
| Literature and hypotheses | BP-01: literature review, evidence screening, and gap finding take much effort. BP-02: hypotheses are often vague, with missing variables, measures, effect thresholds, or refutation criteria. |
| Analysis planning | BP-03: an analysis plan can lack a baseline, confounding control, missing-data handling, or leakage control. |
| Data understanding and splitting | BP-05: real datasets are hard to understand (variable types, missing codes, cardinality, free text, personal data, unit of observation, quality). BP-06: a wrong data split leaks information and gives falsely optimistic results. |
| Confirmatory integrity | BP-07: looking at confirmatory results before the analysis is final, or trying many procedures and choosing the best result (p-hacking), removes the value of confirmation. BP-08: an AI that plans and approves its own work tends to confirm itself, so independent review and human decisions are needed. |
| Traceability of AI output | BP-04: a language model can invent citations, numbers, or certainty, and artifacts without provenance are hard to audit. BP-12: a draft can amplify claims, drop caveats, misquote citations, or contain numbers that code did not create. |
| Data protection | BP-13: private data rows can leave the machine that holds the data (to a model, a log, or a cloud). |
| Control, cost, and run completion | BP-09: tokens, model keys, and cost need control per run and per project. BP-14: a run can hang when it waits for the user, when the budget ends, or when self-repair is exhausted. BP-15: one control switch for a whole run is too coarse: users are asked too much or lose decisions that only they should take. |
| Collaboration and release | BP-10: research teams need to collaborate, comment, receive notifications, and audit one run. BP-16: results can leave the project without an authorized approval. |
| Journals | BP-11: journal choice and manuscript structure often depend on intuition, and observed practice is hard to separate from mandatory rules. |

*Table 1: Business problems (BP) by area.*

AI can reduce the operational burden of this work. It can support data preparation, literature review, planning, analysis, and writing. Unchecked automation, however, can confuse an exploratory pattern with evidence, hide a failed attempt, or state an assumption as a conclusion. The Platform therefore separates three parts. The AI proposes and writes text. Code computes numbers, checks, and verdicts. The Researcher holds the pinned decisions. The Platform manages data, permissions, runs, audit, and the Dossier, and it does not judge the science.

The Platform does not claim autonomous scientific discovery. The Researcher can inspect, correct, and steer the work during a run. A run always ends with a clear result, including the result `with_gaps`, and it never stays suspended. A pinned item that nobody answers before its wait deadline ends the run `with_gaps`; the item closes unanswered and nobody decides it for the user.

| Element | Description |
| ----- | ----- |
| Input | A research case (topic, goal, context, constraints). A tabular dataset is optional at the start. |
| Process | Five stages in a fixed order. Each stage has checks by code, a mandatory independent review, and human decisions by action type. |
| Output | A Dossier that references the accepted EvidenceBundle and PaperPack. The system exports it only after approval. |
| Control | Preset per stage, pinned actions, presence, decision inbox, decision log, token budget, project budget, release gate, and audit log. |

## 3. Existing Systems and Comparison

Two groups of systems relate to OpenAI-Scientist. The first group is general analysis tools, where the user writes and runs every step. Jupyter represents this group as the baseline. The second group is AI scientist systems, where AI agents carry out part or all of a research cycle. Section 3.2 to section 3.5 describe four of them. The descriptions use the public pages and papers of each system. The report compares the systems qualitatively. It does not benchmark OpenAI-Scientist against them (EX-09).

### 3.1 Jupyter Notebook / JupyterLab

Project Jupyter provides web applications for computational documents. A notebook combines code, its output, and explanatory text in one document. JupyterLab is the newer interactive environment for notebooks, code, and data. Project Jupyter releases the software as open source under a modified BSD license.

**Actors:** researchers, data analysts, students, and developers who can write or run code.

**Key features:**

- Notebooks that combine code, output, and text.
- Interactive code execution through kernels for many programming languages.
- Integration with the data-science libraries of each language.

**Pros:**

- High flexibility.
- Code, narrative, and output are visible together.
- Suitable for exploratory work and teaching.

**Cons:**

- It requires programming skill.
- The user organizes the research process by hand.
- It does not enforce a locked plan, split discipline, provenance, or limits on repeated testing.

**Link URL:** https://jupyter.org/

### 3.2 The AI Scientist (Sakana AI)

The AI Scientist is a pipeline that automates the generation of research papers in machine learning. Sakana AI published the first version in 2024 and The AI Scientist-v2 in 2025. The first version starts from a research direction and a code template. It generates ideas, writes and runs experiment code, writes a full paper, and reviews the paper with an automated reviewer. The second version removes the need for a template and searches the space of experiments as a tree.

**Actors:** machine-learning researchers who run the pipeline in their own environment.

**Key features:**

- Idea generation from a research direction.
- Experiment code that the AI writes and runs.
- A full paper draft.
- An automated reviewer that scores the paper.

**Pros:**

- Covers the full cycle from idea to paper without human steps.
- The source code is public under the license of the project.

**Cons:**

- Its scope is ideas that can be expressed in machine-learning code, not tabular research on a user dataset.
- The authors state that it can implement ideas incorrectly, compare unfairly with baselines, and make critical errors when it evaluates results.
- It runs code that a language model writes, and the authors recommend a strict sandbox.
- The human role during a run is limited to the input and the final reading.

**Link URL:** https://sakana.ai/ai-scientist/

### 3.3 AI co-scientist (Google)

AI co-scientist is a multi-agent system that Google built on Gemini and announced in 2025. A scientist states a research goal in natural language. The system generates research hypotheses, a research overview, and experimental protocols. Agents in the system review, rank, and improve the hypotheses in repeated rounds, and the system uses tools such as web search for grounding.

**Actors:** scientists in research organizations, through a trusted tester program.

**Key features:**

- Hypothesis generation from a research goal.
- Review and ranking of hypotheses by AI agents.
- Research proposals with experimental protocols.
- Feedback from the scientist during the process.

**Pros:**

- The design keeps the scientist in the loop as a collaborator.
- The authors report that laboratory experiments supported some proposals in three biomedical areas.

**Cons:**

- The output is a hypothesis and a proposal. The system does not analyze a user dataset or produce an evidence package.
- The ranking of hypotheses is a self-evaluation without an independent ground truth.
- Access is limited to a trusted tester program.

**Link URL:** https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/

### 3.4 data-to-paper (Technion, Kishony lab)

data-to-paper is a framework that guides interacting AI agents from annotated data to a research paper. The Kishony lab at the Technion published it in 2024. The framework can run fully on its own or under human guidance. Every number in the paper links back to the code that computed it.

**Actors:** researchers who have a dataset and a research goal.

**Key features:**

- A step-by-step research process from data to paper.
- Traceability of every number to the code that created it.
- An application for human guidance and review.

**Pros:**

- It is the closest system to OpenAI-Scientist in its input (a dataset) and its traceability of numbers.
- It is open source under the MIT license.

**Cons:**

- The authors state that it suits simple research goals and simple datasets.
- The authors state that the process is not error-proof and needs human intervention for accuracy.
- It has no locked plan, sealed confirmatory result, or protection of data rows.

**Link URL:** https://github.com/Technion-Kishony-lab/data-to-paper

### 3.5 Kosmos (Edison Scientific)

Kosmos is an AI scientist that Edison Scientific released in 2025. A scientist gives a research objective and a dataset. Kosmos then runs for up to 12 hours with literature agents and data-analysis agents, and it writes a scientific report. Each statement in the report cites the code or the primary literature behind it.

**Actors:** scientists who upload a dataset to the Edison Scientific platform.

**Key features:**

- Long autonomous runs that combine literature review and data analysis.
- A report in which each statement cites code or literature.
- Paid access per run on a hosted platform.

**Pros:**

- It works on the user dataset and traces every statement to a source.
- In the evaluation by the authors, independent scientists judged 79.4% of the statements in its reports to be accurate.

**Cons:**

- The scientist cannot interact with a run in its intermediate cycles.
- The authors state that it can invent unusual metrics, confuse statistically significant results with scientifically valuable ones, and make claims that are too strong.
- Repeated runs can reach different conclusions, and the wording of the objective changes the direction of the research.
- The dataset leaves the user and goes to the hosted platform.

**Link URL:** https://edisonscientific.com/news/announcing-kosmos

### 3.6 Comparison and Research Gap

Table 2 compares the systems on the controls that matter for research on tabular data.

| Dimension | Jupyter | The AI Scientist | AI co-scientist | data-to-paper | Kosmos | OpenAI-Scientist |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Input | Code that the user writes | Research direction (and a code template in the first version) | Research goal | Annotated dataset and goal | Objective and dataset | Research case and an optional tabular dataset |
| Output | Notebook | Paper draft | Hypotheses and proposals | Paper | Report | Dossier with EvidenceBundle and PaperPack |
| Human role during a run | User does every step | Input and final reading | Collaborator who gives feedback | Optional human guidance | None in intermediate cycles | Decisions by action type; pinned actions always ask the user |
| Plan locked before confirmatory analysis | No | No | Not applicable | No | No | Yes: Lock, envelope, unseal |
| Traceability of numbers | Manual | Not a stated feature | Not applicable | Numbers to code | Statements to code or literature | Numbers to code records; citations checked against the Literature Base |
| Independent review | No | Automated reviewer of the paper | Agents rank hypotheses | Human guidance | Human reading after the run | Mandatory review of every object version |
| Protection of data rows | Local | Local | Not applicable | Local | Data on the hosted platform | `local` rows stay on the user machine; only released aggregates leave |
| Limits on claims | None | Not a stated feature | Not applicable | Not a stated feature | Not a stated feature | Verdict and claim ceiling computed by code |

*Table 2: Comparison of existing systems with OpenAI-Scientist.*

The AI scientist systems show that AI agents can carry a research cycle from a goal or a dataset to a paper. Their authors also report the same failure modes: wrong implementations, unfair baselines, invented metrics, significance taken as value, claims that are too strong, and results that change between runs. Two systems, data-to-paper and Kosmos, already trace numbers or statements to code. None of the four systems locks the analysis plan before the confirmatory result is visible, limits the claim by a verdict that code computes, or keeps private data rows on the user machine.

OpenAI-Scientist targets this gap for tabular data (BP-04 to BP-08, BP-13). It connects the research case, the dataset, the literature evidence, the locked plan, the code-computed verdict, and the manuscript in one traceable workflow. The Researcher decides the pinned actions during the run.

## 4. Business Opportunity

Research teams increasingly need to use data without a specialist for every statistical or computational method. A guided system can help a team move from a research case to a defensible analysis and a paper package. The responsibility for scientific judgment stays with the Researcher. This applies to educational projects, early-stage academic research, applied analytics, and small teams that need a repeatable and checkable process.

For researchers and analysts, the Platform reduces repetitive work: dataset profiling, literature screening, method planning, and bookkeeping of what was tried. For Project Managers and Reviewers, it shows what was tested, which dataset version was used, how each number was produced, and whether a Dossier is ready for approval. For the institutions that rely on a team's reports, it reduces the risk that unsupported conclusions enter reports or decisions.

The initial product is a focused entry point. It limits the data scope to tabular data, keeps humans in control of the decisions that only they may take, and lets reviewers check results by evidence. Table 3 lists the business objectives (BO) that the BRD defines.

| ID | Business objective | Addresses |
| ----- | ----- | ----- |
| BO-01 | Shorten the path from a research case to an evidence-based hypothesis and a reviewable analysis plan. | BP-01 to BP-03 |
| BO-02 | Trace every claim, citation, variable, number, and decision to a record or a code computation; make every run replayable. | BP-04, BP-05 |
| BO-03 | Keep data rows at the place where the data live; show models and artifacts only aggregates that passed the release gate. | BP-05, BP-13 |
| BO-04 | Make the confirmatory result resistant to p-hacking: split by power, lock, envelope, unseal, tried ledger, and confirmation tier. | BP-06, BP-07 |
| BO-05 | Require an independent review for every stage and give humans decision rights by action type (preset, pinned, presence). | BP-08, BP-15 |
| BO-06 | Control the token budget per run and the monthly budget per project. | BP-09 |
| BO-07 | Support safe collaboration inside a project, with permissions by role. | BP-10 |
| BO-08 | End every run with a clear result, including `with_gaps`; never leave a run suspended. | BP-14 |
| BO-09 | Evaluate each stage and the whole pipeline with acceptance scenarios, a seeded-flaw bench, and a paper reproduction bench. | BP-06, BP-08 |
| BO-10 | Create a PaperPack that the writing team turns into a submission without re-deriving the numbers; keep claims within the claim ceiling. | BP-04, BP-12 |
| BO-11 | Export outside the project only when the Dossier is approved. | BP-16 |
| BO-12 | (Could, after MVP) Support journal choice with an evidence-based profile, a control corpus, and a clear version (JFE). | BP-11 |

*Table 3: Business objectives.*

- Primary users: research groups, student project teams, data analysts, and supervisors or reviewers.
- Primary value: less manual analysis effort, safer decisions about data, and results that can be traced and replayed.
- Success signal: a run ends with a clear result and a Dossier whose numbers and citations trace to records (success metrics SM-01, SM-03, and SM-04).

## 5. Software Product Vision

For research teams that need to move from a research question on tabular data to a paper package they can defend, OpenAI-Scientist is a web-based research platform. It runs a fixed pipeline of five stages, with a typed hand-off object at each boundary. Unlike a notebook or an autonomous AI scientist, it makes the discipline of a confirmatory study part of the product: a locked plan, a sealed confirmatory result, a verdict computed by code, and an independent review of every object version.

The Researcher keeps the decisions that only a person may take. The AI proposes and writes text. Code owns the numbers. Data rows stay at the place where they live. The Platform versions the results and exports an approved Dossier only.

The team evaluates the product by whether the Researcher reaches a well-supported result, a meaningful negative result, or an insufficient-evidence verdict, and whether every deviation, limitation, and source remains visible, whatever the conclusion. The product is designed so that no error is hidden, every claim has a source, and every run can be replayed.

## 6. Project Scope and Limitations

The project scope covers a web app and an AI research runtime for the five-stage pipeline on tabular data. The scope includes accounts, roles, projects, versioned datasets, human control by action type, mandatory independent review, token and project budgets, collaboration, and a Dossier with approval and export. It also includes the Local Node, which keeps private data rows on the user machine.

The research scope covers research on phenomena in existing data, with the claim types `association`, `causal`, and `prediction`. It adds a control layer for tabular data: task family, research pattern, pipeline order, leakage control, testable hypotheses, and a red-team catalogue of planted flaws (BR-82 to BR-101).

The MVP covers FE-01 to FE-15 and FE-17. FE-18 (JFE) is Could. FE-19 (`method_comparison`) is Should. Both come after the MVP. The system assists users. It does not define a research agenda, guarantee novelty, or replace expert review.

### 6.1 Major Features

The priority uses the MoSCoW scale. The feature numbering skips one number on purpose.

| ID | Feature | MoSCoW | Purpose |
| ----- | ----- | ----- | ----- |
| FE-01 | Account and access | Must | Lets users sign in by passwordless email or with a Google account (FR-146) and limits every action by role. |
| FE-02 | Project workspace and members | Must | Lets a team work in one project with members, settings, and an audit log. |
| FE-03 | Data management (dataset, version, connection, location) | Must | Manages immutable dataset versions, imports data from an upload or a connection, and sets the data location. |
| FE-04 | Research case and run management | Must | Starts a run from a research case and coordinates the five stages, run state, stale objects, cancellation, and next step. |
| FE-05 | Human control | Must | Lets the user control a run by action type: preset, presence, pinned actions, decision inbox, decision log, overturn, AI PI, and lab notebook. |
| FE-06 | Dataset stage | Must | Turns data into a DatasetSnapshot with quality profile, question map, split by power, and fitness. |
| FE-07 | Hypothesis stage and Literature Base | Must | Reviews the literature by a defined method and creates an evidence-based HypothesisSet. |
| FE-08 | Experiment design stage and Lock | Must | Plans the analysis of existing tabular data in an AnalysisPlan and locks the plan. |
| FE-09 | Execution stage | Must | Runs the locked plan, keeps the confirmatory result in the envelope, unseals it, and computes verdict, grade, and claim ceiling by code. |
| FE-10 | Paper stage | Must | Drafts a PaperPack that the writing team can use without re-deriving the numbers. |
| FE-11 | Independent review loop and personas | Must | Reviews every object version independently, with verified findings and at most two revision rounds. |
| FE-12 | Local Node | Must | Keeps `local` data on the user machine, runs jobs next to the data, and releases only aggregates through the release gate. |
| FE-13 | Budget and cost | Must | Controls the token budget of a run and the monthly budget of a project, and makes every run end. |
| FE-14 | Dossier, approval and export | Must | Collects the results in a versioned Dossier, approves it under the review settings, and allows export only after approval. |
| FE-15 | Collaboration (comments, notifications) | Must | Lets members comment and receive notifications around one run. |
| FE-17 | Administration and monitoring | Must | Lets the Platform Admin manage users, models, keys, and audit, and monitor operations. |
| FE-18 | Journal Fingerprint Extraction (JFE) | Could | Builds an evidence-based journal profile that the `paper` stage can refer to (after MVP). |
| FE-19 | Method comparison research | Should | Compares machine-learning methods on the same data with the claim type `method_comparison` (after MVP). |

*Table 4: Major features and priority.*

### 6.2 Limitations and Exclusions

The table below lists the constraints and assumptions.

| ID | Statement |
| ----- | ----- |
| LI-01 | The system supports tabular data only. |
| LI-02 | The project is the highest scope. The system has no organization layer and no custom permission matrix. |
| LI-03 | A project has at most one active run. |
| LI-04 | The supported task families are `binary`, `multiclass`, `regression`, and `rare-event` (BR-83). The system reports an unsupported family as unsupported. |
| LI-05 | The Local Node does not require the user to install container software. The user must keep the Local Node open while a job runs on `local` data. |
| LI-06 | The Platform Admin configures the model gateway and the keys. Without this configuration, a run reports a clear error. |
| LI-07 | The literature provider returns public metadata and abstracts with provenance. The system uses open-access full text only. |
| LI-08 | AI output is advisory. Code supplies numbers and verdicts. The user decides every pinned action. |
| LI-09 | The system produces a draft manuscript. The Researcher decides whether to submit it. |

The table below lists the exclusions, which are outside the scope.

| ID | Excluded capability | Note |
| ----- | ----- | ----- |
| EX-01 | Data that is not tabular (images, text corpora, signals). | The system supports tabular data only. |
| EX-02 | Design of new data collection (laboratory or field experiments). | The `experiment_design` stage plans only the analysis of existing tabular data. |
| EX-03 | A full systematic-review product (registration, full grading, conclusive meta-analysis). | The `hypothesis` stage is a methodical rapid review. |
| EX-04 | Reading full text behind a paywall. | The system uses metadata, abstracts, and open-access full text. |
| EX-05 | Organization, multi-tenant support, and a custom permission matrix. | The project is the highest scope. |
| EX-06 | Automatic submission to a publisher, or a guarantee of acceptance by a journal. | The Researcher decides on submission. |
| EX-07 | A causal claim made only from a plan or a hypothesis. | A claim comes only from a verdict and the claim ceiling. |
| EX-08 | Task families ranking, survival, forecasting, and anomaly detection. | Only `binary`, `multiclass`, `regression`, and `rare-event` are supported (BR-83). |
| EX-09 | A comparison of the Platform with human-only work, AutoML, or generic agents. | The product does not benchmark the Platform against these systems. This does not exclude user research topics: a user may compare an AutoML method with baselines on the user's own data under `method_comparison` (FE-19, Should, after MVP). |

These limitations and exclusions form the baseline scope. They prevent uncontrolled expansion and let the review board judge whether the team can implement and demonstrate the system within the capstone schedule.

## Open items

1. Submission date. The team must state the submission date on the title page.
2. Group name and project code. The team must confirm the group name and the project code before submission.
3. Document structure. The front matter (Acknowledgement, Definitions and Acronyms) sits under the single top-level heading of this file. The final document may move it before Section I.
4. Survey of existing systems. Sections 3.2 to 3.5 use the public pages and papers of each system as they stood in 2026. The team should check them again before submission, because these systems change often.
5. Closed. Report III states the targets of SM-02, SM-17, and SM-18 (Report III, Open items 1 and 3).

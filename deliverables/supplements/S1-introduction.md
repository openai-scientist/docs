# Supplement to Report I

Revised project context for Report 7 (2026-10-29): the product serves students and early-career researchers who do not yet know the path to a paper, based on the team's RBL experience. The build places each section under the template heading with the same number in place of the matching section of `report/00`.

### 1. Overview

OpenAI-Scientist is a web app that guides students and early-career researchers through a clear, step-by-step research process on tabular data, from a research question to a paper. A Researcher starts with a research case. A dataset is optional at the start. The system then runs a fixed, dataset-first pipeline of five stages: `dataset`, `hypothesis`, `experiment_design`, `execution`, and `paper`. Each stage boundary has exactly one hand-off object. The hand-off object is typed, versioned, hashed, and immutable after acceptance.

The Platform divides the work into three parts. The AI proposes and writes text. Code computes numbers, checks, verdicts, grades, and claim ceilings. The Researcher keeps the decisions that only a person may take. A mandatory independent review applies to every object version. Data rows that stay on the user machine never leave it. A Local Node releases only aggregates through a release gate. The final result is a Dossier. Only an approved Dossier may leave the project.

The Platform is designed so that no error is hidden, every claim has a source, and every run can be replayed. It does not guarantee that the science is right.

### 2. Product Background

Many students and early-career researchers want to write a scientific paper but do not know the path from a research question to a paper. During the Research-Based Learning (RBL) project with Ms. Hương, the team worked with many students who took part in research. Few of them reached a paper, and the gap was largest for studies on tabular data. They did not know how to read a dataset, turn a topic into a testable hypothesis, plan an analysis that holds, run it without fooling themselves, or write up the result.

OpenAI-Scientist is therefore not a tool that automates research for experienced scientists. It gives newcomers a research framework with clear stages. Each stage has a defined goal, a defined output and a check, and the user takes the stages one step at a time. The work is still the analysis of tabular data, but it follows an explicit research process, so a newcomer learns the process while doing it.

The current system implements this framework as five stages in a fixed order: `dataset`, `hypothesis`, `experiment_design`, `execution` and `paper`. Each stage ends with one hand-off object that the user reviews and accepts before the next stage starts. Each step also has its own risk. Table 1 groups the business problems that the BRD records (BP-01 to BP-16).

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


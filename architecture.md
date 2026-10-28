# Architecture

Logos là nền tảng nghiên cứu AI. Một researcher tạo `ResearchCase`; Platform điều phối case qua các stage để tạo data card/brief, evidence-linked hypotheses và reviewed experiment plan. AI Principal Investigator (PI) xử lý các quyết định pipeline theo authority được phép.

**Document version:** 2.1 (2026-10-28)\
**Contract source:** `logos_contract.base.CONTRACT_VERSION = 4.0.0`\
**Scope:** source hiện tại trong `capstone-projects/projects/logos`; frontend contract surface trong `ai-research-platform-fe`.\
**Liên quan:** [BRD](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md) · [PRD](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md) · [changelog](changelog.md)

> **Current/next boundary:** Current pipeline kết thúc ở reviewed/locked plan. `DataCard.split` hiện chỉ có `random_rows` cho exploration/confirmation. Structure-aware split, sandbox execution, statistical results, verdict và dossier là FE-16/HGAR next increment, chưa có trong current source.

## Contents

1. [The system](#the-system)
2. [Projects and boundaries](#projects-and-boundaries)
3. [Ownership](#ownership)
4. [A run end to end](#a-run-end-to-end)
5. [The engine contract](#the-engine-contract)
6. [The engine skeleton](#the-engine-skeleton)
7. [Stages](#stages)
8. [The Platform](#the-platform)
9. [Oversight: the AI PI](#oversight-the-ai-pi)
10. [Frontend](#frontend)
11. [Security](#security)
12. [Configuration and deployment](#configuration-and-deployment)
13. [Current boundary and FE-16](#current-boundary-and-fe-16)
14. [Cross-cutting rules](#cross-cutting-rules)
15. [Verification](#verification)

## The system

```text
browser ──HTTP/SSE──> Platform (services/management) ──HTTP──> engines (stages/*)
                          │   ▲                                    │
                          │   └──── callbacks: events, artifacts ──┘
                          └──HTTP──> oversight (AI PI) ──callback──┘
```

- **Platform** là service duy nhất có user surface. Platform sở hữu user, project, role, dataset metadata/version, files, run state, gates, budget, model keys, audit và event stream. Platform không thay engine để phán xét nội dung khoa học.
- **Engine** làm khoa học của một stage. Engine không có UI/CLI; Platform điều khiển qua engine contract và nhận event/artifact qua callback.
- **Oversight** là AI PI. Platform hỏi PI ở charter, stage outcome, failure và close; Critic stage review là đường review riêng và có cờ cấu hình.
- **Contract** chứa wire models/schema ids/version; **engine skeleton** chứa run loop, workspace, event outbox, gates, LLM client và recovery.
- Services/stages giao tiếp qua HTTP; import boundary do workspace và `.importlinter` kiểm soát. Stage không import stage khác.

## Projects and boundaries

Một uv workspace và một lockfile; Python 3.12+.

| Directory | Distribution | Import | Env prefix | Entry point |
|---|---|---|---|---|
| `packages/contract` | `logos-contract` | `logos_contract` | none | library |
| `packages/engine` | `logos-engine` | `logos_engine` | none | library |
| `stages/dataset` | `logos-dataset` | `logos_dataset` | `DATASET_` | `dataset-api` |
| `stages/hypothesis` | `logos-hypothesis` | `logos_hypothesis` | `HYPOTHESIS_` | `python -m logos_hypothesis.main` |
| `stages/experiment-design` | `logos-experiment-design` | `logos_experiment_design` | `EXPERIMENT_DESIGN_` | `experiment-design-api` |
| `services/oversight` | `logos-oversight` | `logos_oversight` | `OVERSIGHT_` | `oversight-api` |
| `services/management` | `management` | `management` | Platform settings | `uvicorn management.main:app` |
| `eval` | `logos-eval` | `logos_eval` | none | `python -m logos_eval.run`, `python -m logos_eval.flaws` |

`deploy/` chứa Compose files; `scripts/` chứa workspace tooling/test selector.

Import rules:

- `packages/*` không import stage/service.
- Stage không import stage khác; service không import stage khác trực tiếp.
- Platform layers được khai báo trong `services/management/pyproject.toml`.
- Một component giữ một tên nhất quán giữa directory, distribution, import, `engine_key`, `stage_key`, schema prefix và env prefix.

## Ownership

| Concern | Owner | Source |
|---|---|---|
| Users, projects, roles, members, datasets, files, connections, audit | Platform | `services/management/src/management/*` |
| Run state, gates, decisions, send-back, accept, amendments | Platform | `services/management/src/management/research/` |
| Token budget, model keys, model pricing | Platform | `management/research/`, admin settings |
| Wire models, schema ids, routes, contract version | Contract | `packages/contract/src/logos_contract/` |
| Run loop, store, outbox, gates, pause/recovery, LLM client | Engine skeleton | `packages/engine/src/logos_engine/` |
| Dataset science | Dataset stage | `stages/dataset/src/logos_dataset/` |
| Literature/evidence/hypothesis science | Hypothesis stage | `stages/hypothesis/src/logos_hypothesis/` |
| Plan/analysis science and review | Experiment-design stage | `stages/experiment-design/src/logos_experiment_design/` |
| PI pipeline decisions and Critic report | Oversight | `services/oversight/` |

Code is the authority for field names, defaults, enum values, limits and current behavior. This document explains the boundary and points to source rather than duplicating every model.

## A run end to end

### 1. Create and settle the research case

`ResearchCase` in `packages/contract/src/logos_contract/case.py` is the single source of a run's researcher intent and scope. It contains:

- `intent.kind`: `test`, `compare`, `explain` or `explore_dataset`, plus intent text;
- optional `problem`, `context`, `constraints`, `references`, `domains` (maximum 10);
- optional `dataset_version_id`;
- durable `clarifications` and `amendments`;
- optional PI `charter` with objective/scope/success/kill criteria, risk posture, assumptions and open questions.

`explore_dataset` requires a dataset while a settled case requires a problem unless it is still the dataset-exploration draft. A non-dataset run needs at least one domain in the Platform route. The engine receives the settled case at `inputs.params.case`; legacy `topic`/`objective` fields are not the canonical source.

When no PI/dataset blocks the case, Platform may settle it at start. When a dataset exploration produces a proposed problem, the case/charter flow can hold the next stage until the researcher/PI settles the missing scope.

### 2. Select the pipeline

`management.research.orchestrator` selects the configured pipeline:

```text
dataset_version_id present + dataset-first route:
    dataset → hypothesis → experiment_design

no dataset:
    hypothesis → experiment_design
```

The default settings are `dataset_pipeline="dataset_first"` and `default_pipeline="default"`. The pipeline is routing; every stage still receives the same case and only declared input artifacts.

### 3. Start each stage

Platform sends `RunCreateRequest` with:

- settled case and pipeline context;
- declared input artifact refs and opaque download URLs;
- `stage` and `review` model configs, integration keys and admin settings;
- remaining token budget, `stage_run_id`, callback URL and request/trace ids.

The engine validates contract/version, creates a run workspace and emits ordered events/artifacts back to Platform. An engine never reads model keys from its environment or writes them to workspace/logs.

### 4. Run steps, gates and review

The skeleton runs declared steps, skips a step on resume when its manifest/hash still matches, archives affected steps for bounded back edges, and exposes gates according to `light`/`auto` mode. A separate review model is used for `reviewing` work when configured.

In `light`, researcher answers engine gates and accepts/sends back stages. In `auto`, Platform answers engine gates by rule and PI decides pipeline actions. Integrity, charter conflict or `cannot_decide` escalates to researcher.

### 5. Stage end and close

Critic/review findings, open gaps, artifact hashes and stage decision are persisted. PI may accept, send back, or escalate under authority rules. Accepted open blocking risks become obligations/guidance for later stages. After the last current stage, close produces a report; it does not execute the experiment or create a scientific verdict.

### Case amendments

`POST /projects/{project_id}/runs/{run_id}/case/amendments` is the only supported mutation of a settled case. An amendment stores changed fields, researcher reason, version and time, then emits `case.amended`. A stage already started keeps the case version it received; the next stage receives the amended version.

## The engine contract

`logos_contract` in `packages/contract/src/logos_contract/` is the single wire definition. `CONTRACT_VERSION` is currently **4.0.0**. Important modules are `base`, `runs`, `service`, `paths`, `events`, `activity`, `review`, `artifacts`, `case` and `pi`.

### Version and compatibility

- Contract version follows semantic versioning; a receiver rejects an incompatible major (`ENGINE_CONTRACT_MISMATCH`).
- Source tests and contract export are the authority for current schema/examples.
- Unknown fields are generally tolerated by contract models; secret-bearing models apply stricter validation.
- After contract changes, run the export and `task verify:contract`.

### Engine routes

All non-public engine routes require `X-Service-Key`; requests carry `X-Request-ID` and `traceparent`; bodies have no wrapper.

| Method | Path | Body/result |
|---|---|---|
| GET | `/health` | Public health; detail with valid key. |
| GET | `/capabilities` | Engine capabilities/spec. |
| POST | `/runs` | `RunCreateRequest → RunCreateResponse`; idempotent by `stage_run_id`. |
| GET | `/runs/{engine_run_id}` | `RunState`. |
| GET | `/runs/{engine_run_id}/events?after=&limit=` | `EventPage`. |
| POST | `/runs/{engine_run_id}/gates/{gate_id}` | `GateAnswer → RunState`. |
| POST | `/runs/{engine_run_id}/pause` | Pause state. |
| POST | `/runs/{engine_run_id}/resume` | Resume state. |
| POST | `/runs/{engine_run_id}/cancel` | Cancel state. |

Engine callbacks go to Platform `/internal/engines/{engine_key}/runs/{stage_run_id}`:

- `/events` receives `EventBatch`; `source_seq` starts at 1 and must be contiguous.
- `/artifacts` receives multipart metadata/file; an artifact is uploaded before an event names its Platform id.
- On `EVENT_GAP`, engine resends from `delivered_seq + 1`; on `STAGE_CLOSED`, local work stops.
- Activity events use the engine prefix and do not contain prompts, full model replies or credentials.

PI contract uses `GET /health`, `GET /capabilities`, `POST /consultations` and `GET /consultations/{id}`; Platform receives the PI callback result and brokers artifact access.

### Review contract

`review.py` currently includes categories such as `leakage`, `baseline`, `control`, `statistics`, `reproducibility`, `evidence`, `metric_validity`, `selective_reporting`, `variable_validity`, `measurement_level`, `missing_data`, `confounding`, `multiplicity`, `split_discipline`, `effect_size`, `small_cells` and `other`.

A review passes when no finding is `blocking`. Exhausted revision or reviewer failure leaves a gate/open finding; it does not silently publish as fully reviewed.

## The engine skeleton

```text
stages/<name>/src/logos_<name>/
    engine.py       EngineSpec: steps, edges, gates, outputs
    steps/          stage science; run(ctx) -> StepResult
    settings.py     admin-edited engine settings model
    main.py         serve(spec, client_factory)
    ...             prompts, packs, calculators, persistence
```

`EngineSpec` declares `steps`, `edges`, `max_loops`, `gates`, `output_schemas`, `primary_artifact`, `input_schemas`, settings, integrations and activity types.

`RunContext` is a step's only world boundary: `ctx.llm(role)`, input/artifact reads, `ctx.params`, settings/integrations, event emit, assumptions, checkpoint, usage/budget, upload, review and revision publication.

Skeleton guarantees:

- Resume skips a step only when its manifest matches output/upstream hashes.
- Back edges archive affected steps under `attempts/<n>/`.
- A revision reuses steps before the declared revision entry.
- Prior runs can be reused with a new engine run id.
- Restart/provider outage pauses running work as `interrupted`; resume requires credentials.
- Event/artifact outbox is idempotent and ordered.

### LLM and agent rules

- `OpenAIClient` owns retry/usage policy; transient 408/429/5xx failures retry with backoff, prolonged outage pauses work.
- Missing usage is charged by the declared fallback and emits an `*.usage.assumed` activity.
- `run_agent` keeps append-only per-agent logs and bounded turns/tokens; tool errors return to the model, not fake output.
- `decide` chooses from code-listed options using TypeSafe, review model or a safe option; it never blocks indefinitely.
- Deterministic code is preferred for rules/calculations; reasoning model is used for open-ended content; human/PI gate is used for decisions requiring authority.

## Stages

Every stage `engine.py` is the implementation authority for steps, edges, gates, settings and outputs.

### Dataset stage

Source: `stages/dataset/src/logos_dataset/`.

```text
ingest → profile → describe → explore → propose → brief
             ▲          │                     │
             └──────────┘                     └─ question_choice gate
                     data_card_review gate
```

- Reads CSV, TSV, XLSX, SAV, ZSAV, DTA, Parquet and supported zip/codebook inputs.
- `profile` creates the current exploration/confirmation row split; contract `Split.method` is only `random_rows` with seed/fraction/counts.
- `describe` creates variable type, label, measure, role/kind, missing values, summaries, flags, source metadata, access records, caveats and decisions.
- Data card aggregates are the model boundary; raw rows are not copied into published artifacts. Small category counts below `min_cell` are hidden.
- `explore` is experimental/off by default (`settings.explore=false`) because current sandbox/privacy boundary is not sufficient for raw-row model exploration.
- `propose` creates dataset questions; researcher selects one at `question_choice`; `brief` creates `dataset.brief/v1`.
- Outputs include `dataset.data_card/v1`, `dataset.data_card_markdown/v1`, `dataset.brief/v1`, `dataset.brief_markdown/v1` and optional `dataset.explore_report/v1`; primary artifact is the brief.

The current dataset card is **not** a group/time/panel structure manifest and does not enforce evaluation split policy. That is FE-16.

### Hypothesis stage

Source: `stages/hypothesis/src/logos_hypothesis/`.

The current workflow is:

```text
understand → search → screen → extract → synthesize → hypothesize
           → critique → verify → lock
```

It stores literature/evidence provenance, evidence-linked gaps and falsifiable hypotheses. Shortlist and hypotheses gates can be answered in `light`; bounded critique/researcher revision handles blocking findings. Missing literature/model/credential produces explicit errors; the stage does not generate fake fallback content.

### Experiment-design stage

Source: `stages/experiment-design/src/logos_experiment_design/`.

```text
understand → ground → design → critique → verify → lock
```

- Inputs include hypotheses/evidence/review plus optional `dataset.data_card/v1` and `dataset.brief/v1`.
- If a data card exists, `workspace.py` marks run role `analysis`; otherwise role is `benchmark`.
- The analysis pack writes a statistical analysis plan. It reads variable names/measurement levels and data-card split, and requires confirmatory analysis to use confirmation rows after the plan is locked; exploratory work is labelled.
- Validators currently cover variable existence/validity, measurement level, missing-data plan, confounding, multiplicity, split discipline, small cells and resampling seed. Calculators provide numerical power/precision quantities where applicable.
- Gates are `resources_review` when resource review is needed and `plan_review` after verify. A plan comment can return to critique within the configured bound.
- Output primary artifact is `experiment_design.exp_plan/v1`; index/resources/review/revision artifacts are declared in the engine spec.
- **It does not execute ML/statistical experiments and does not publish results/verdict/dossier.** `lock` locks the plan artifact, not an execution protocol with a holdout reservation.

## The Platform

Source: `services/management/src/management/`.

### Main responsibilities

- Auth/session/onboarding and fixed platform/project roles.
- Projects, memberships, invitations, files, datasets, immutable versions, preview/download and connectors.
- Research case creation/settlement, PI charter/clarifications, amendment/version history.
- Run aggregate, pipeline dispatch, stage lifecycle, gates, accept/send-back, events/SSE, pause/resume/stop/rerun/sync/abandon.
- Token budget, project budget, usage/cost ledger, model/integration secrets and admin engine settings.
- Comments, notification/webhook, audit, system monitoring and frontend-facing API.

### Dataset API boundary

`management/datasets/router.py` exposes project-scoped list/create/import/read/update/delete/version/download/preview routes. `DatasetVersionItem` records dataset/version ids, original filename, size, SHA, row count, columns, source type and source details. Preview is a Platform capability and may apply PII masking; it is not an automatic grant to send rows to an engine.

### Research run API boundary

`management/research/router/runs.py` exposes project-scoped run list/create/read/events/SSE/gate/pause/resume/stop/budget/sync/abandon. `run_case.py` exposes the amendment endpoint. The route validates case requirements, enforces one active run/project and maps engine/PI errors into stable Platform errors.

### Pipeline and case behavior

`management/research/orchestrator.py` chooses `dataset_first` when the run has a dataset, otherwise `default`. `management/research/case.py` handles settled-from-start, dataset stage proposed problem, charter rounds, researcher clarification, PI skip and durable amendments. Current tests cover explore-first behavior, charter hold, versioned amendment and charter skip after auto failure.

### Authority

`management/research/authority.py` keeps engine gate handling separate from PI pipeline decisions. Engine gates are answered by the researcher in `light` and by Platform rule in `auto`; PI is not consulted at engine gates. Stage outcome/failure/charter are researcher-controlled in `light` and PI-controlled in `auto` within guardrails. **Close is PI-controlled.** Integrity/charter conflict/cannot-decide escalates.

## Oversight: the AI PI

Source: `services/oversight/` and Platform research/PI modules.

The PI receives a consultation with charter, situation, allowed actions, lab notebook and artifact references. It can read permitted artifacts/notebook/literature/data checks, write notes and end with a typed decision/report.

| Consultation | Authority |
|---|---|
| `charter` | PI in auto; researcher in light; may ask clarifications. |
| `stage_review` | Critic report; feeds obligations/directives. |
| `stage_outcome` | PI in auto; researcher in light. |
| `failure` | PI in auto; researcher in light. |
| `close` | PI writes closing report and names open obligations. |

Guards:

- PI cannot directly answer engine gates.
- PI cannot accept a blocking item without an explicit known-risk/obligation path.
- PI cannot change researcher intent; charter is its reading of the case.
- Escalation hands the decision to researcher.
- Current PI close is a workflow/reporting decision; it does not assert that experiments ran.

## Frontend

Source: `ai-research-platform-fe`.

The frontend is a Next.js App Router application with React/TypeScript, Tailwind/shadcn, TanStack Query/Table, Redux Toolkit, Biome and Vitest. It consumes Platform APIs; engines and PI have no direct UI.

Current product areas include public/auth/onboarding, projects, datasets, connections, files/documents, research flow/run studio, members, settings, reviews and admin pages. The current FE adapter remains hypothesis-oriented: the data-stage feature is disabled and the start-run form does not yet submit `dataset_version_id` or expose `explore_dataset`. Thus the dataset-first flow described by the backend contract is a planned FE integration, not an already exposed end-user happy path. Run studio renders existing stage/event scenes and must not imply current execution/result capability when the backend has only produced a plan.

## Security

- Session cookie HttpOnly; CSRF for writes, CORS allowlist and auth rate limiting.
- Non-member is hidden as `404`; role mismatch is `403`/stable role error.
- Dataset connection credentials and model keys are sealed with `SecretBox`, never returned/logged.
- Connection policy rejects loopback/private/link-local hosts where applicable.
- Service-to-service requests use per-engine/PI `X-Service-Key`; callback auth is checked before body processing.
- Engine and PI receive keys per request and do not read `.env` or write secrets to disk.
- The default data-card model boundary is aggregate-only. The opt-in experimental `explore` path can inspect exploration rows under its separate access record; future execution must add a separate sandbox policy, and current `explore=false` is not a substitute for sandbox isolation.

## Configuration and deployment

### Runtime configuration

`logos/deploy/.env.example` declares engine and pipeline wiring:

```json
{
  "ENGINES": {
    "dataset": "...",
    "hypothesis": "...",
    "experiment_design": "..."
  },
  "PIPELINES": {
    "default": [
      {"stage_key": "hypothesis", "engine": "hypothesis"},
      {"stage_key": "experiment_design", "engine": "experiment_design"}
    ],
    "dataset_first": [
      {"stage_key": "dataset", "engine": "dataset"},
      {"stage_key": "hypothesis", "engine": "hypothesis"},
      {"stage_key": "experiment_design", "engine": "experiment_design"}
    ]
  }
}
```

Platform defaults include 50 MiB dataset upload, `dataset_pipeline="dataset_first"`, `default_pipeline="default"`, default run token budget 4,000,000, maximum 20,000,000, PI timeout 180 seconds and `pi_critic_enabled=false`; the settings source is authoritative for deployment overrides.

### Deployment

- Development: `logos/deploy/docker-compose.dev.yml`; build context is repository root.
- Production: `logos/deploy/docker-compose.prod.yml`; migration runs before API.
- API binds behind TLS reverse proxy; proxy must disable buffering for SSE.
- Shared storage/volume is required for engine workspace/artifact delivery according to deployment configuration.

## Current boundary and FE-16

### Current backend tabular path

```text
dataset version
  → data card + random exploration/confirmation split
  → dataset brief/question
  → hypotheses/evidence
  → statistical analysis plan + review + lock
```

The current backend path is useful for data understanding and plan quality. It does **not** establish that the chosen split is valid for every data-generating process, and the current FE does not yet expose the full path.

### FE-16 target

The next increment must add a manifest/registry and researcher-confirmed policy for:

| Structure | Target policy |
|---|---|
| Independent | Repeated stratified k-fold where appropriate. |
| Grouped | Group-disjoint folds; one entity cannot occur in both train/test. |
| Time-ordered | Chronological/rolling-origin; no shuffling across time. |
| Panel/longitudinal | Entity-disjoint plus past-to-future feature availability. |
| Special | Censored/survival, high-frequency, graph, multimodal/tabular+text: dedicated adapter/policy or explicit out-of-scope. |

FE-16 also needs protocol freeze, train-only preprocessing/resampling, holdout-once discipline, sandbox network/data policy, checkpoint/resume/retry, immutable execution lineage and scientific review of effects/CIs/margins. These are design targets, not current engine features.

## Cross-cutting rules

1. **Code truth:** field names, defaults, limits, enum and status come from source/tests.
2. **Research case truth:** all stages read the settled case from `inputs.params.case`; no parallel legacy topic/objective authority.
3. **Immutable lineage:** dataset versions, case amendments, stage artifacts, plan revisions and events remain auditable.
4. **Numbers from code:** profiler/calculator/validator/runner produces numeric values; model text cannot invent them.
5. **Prompt/validator agreement:** every hard prompt rule has code validation and every validator rule is surfaced to the relevant step.
6. **Graceful limits:** budget/revision/turn limits preserve best output with a gap; provider outage pauses and requires recovery, not fake content.
7. **Review boundaries:** review, gate approval, stage acceptance and close have distinct authority and audit entries.
8. **Data boundary:** current model inputs are aggregate/data-card based; raw-row exploration remains disabled by default.
9. **No false completion:** plan lock is not experiment execution, result evidence, scientific verdict or publication dossier.
10. **Future split discipline:** until FE-16 exists, `random_rows` must be documented as the current exploration/confirmation split only.

## Verification

| Command | When |
|---|---|
| `task test:light` | Every backend edit. |
| `task test:impact` | Before commit. |
| `task test:feature` | Before push. |
| `task test:critical` | Before merge. |
| `task verify:fast P=<project>` | Project-level imports/ruff/tests. |
| `task verify:contract` | After contract/schema changes. |
| `task lint-imports` | After dependency/module changes. |
| `task ruff` | Formatting/lint. |

For this documentation-only update, the relevant checks are repository inventory/source cross-check, Markdown cross-reference check and `git diff --check`; backend tests are not rerun because no source code changed.

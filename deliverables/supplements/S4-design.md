# Supplement to Report IV

Facts from the two code repositories (`logos` and `ai-research-platform-fe`) on 2026-10-29: lock files, Dockerfiles, Compose files and CI workflows. The build places each section under the template heading named in the map.

### 1.4 Technology Declaration

#### Technology stack

| Layer | Technology | Version | Use |
| ----- | ----- | ----- | ----- |
| Web app runtime | Node.js | 22 | Build and run the web app (`node:22-alpine` image). |
| Web framework | Next.js, React | 16.3.8, 19.3.0 | Server-rendered web app; passes `/api/v1` calls to the Platform. |
| Web language and UI | TypeScript, Tailwind CSS, shadcn/ui (Radix UI) | 5.9.3, 4.3.3, 4.x | Typed code, styling, accessible components. |
| Web state and data | TanStack Query, Redux Toolkit, Zustand, Axios, Zod | 5.104.0, 2.13.0, 5.0.15, 1.20.0, 4.6.5 | Server state, client state, HTTP calls, input validation. |
| Backend runtime | Python | 3.12 | Platform, oversight service and stage engines (uv workspace). |
| Backend framework | FastAPI, Uvicorn, Pydantic | 0.143.1, 0.54.0, 2.14.1 | HTTP API, ASGI server, request and settings validation. |
| Data access | SQLAlchemy (async), asyncpg, Alembic | 2.1.1, 0.31.0, 1.20.0 | ORM, PostgreSQL driver, schema migrations. |
| Analysis | pandas, NumPy, SciPy | 3.0.6, 2.5.3, 1.18.1 | Dataset profiling and code-computed statistics in the stages. |
| Database | PostgreSQL | 16 (`postgres:16-alpine`) | Platform database (section 2.4). |
| File storage | Local volume or Cloudflare R2 (S3 API through boto3 1.43.113) | – | Uploaded datasets, project files and produced artifacts. |
| Containers | Docker, Docker Compose | – | One image per service; `deploy/docker-compose.dev.yml` and `deploy/docker-compose.prod.yml`. |
| Quality | Ruff 0.17.0, pytest 8.4.2 (backend); Biome 2.5.14, Vitest 5.0.3 (web app) | – | Lint, format and tests. |

#### Third-party services

| Service | Purpose | Data sent |
| ----- | ----- | ----- |
| Language model provider (OpenAI-compatible chat API) | Model calls of the stage engines and the AI PI. The Platform Admin sets the model profiles and keys in the Platform. | Prompts built from the research case, dataset summaries and released aggregates, and literature metadata. No row of `local` data (NFR-12). No key or secret in a prompt (NFR-09). |
| OpenAlex, Semantic Scholar, arXiv | Literature search for the Literature Base. | Search queries (keywords, titles, DOIs). |
| Google Identity (OAuth 2.0) | Sign in with Google; authorization of Google data connections. | OAuth requests; the Platform receives the account email and subject ID. |
| Google Sheets, Google Drive, Google Picker | Import of datasets that the user authorizes. | File and sheet identifiers, the user's access token. |
| Google BigQuery and other database connectors | Data connections that a project owner sets up. | Queries the user defines; connection credentials, stored encrypted. |
| Resend | Transactional email: sign-in codes, invitations, notifications. | Recipient email address and the message text. |
| Cloudflare R2 | Object storage in production. | Uploaded files and produced artifacts. |
| Slack, Microsoft Teams, Discord (incoming webhooks) | Project notifications to chat tools, when a project adds one. | Notification text: event type, project and run names, link. |
| GitHub, GitHub Actions | Source hosting, pull requests, CI and deployment workflows. | Source code. Secrets stay in the GitHub secret store. |
| Docker Hub | Registry of the service images. | Built images. |
| Dokploy | Deployment of the Compose stacks on the server. | Image tag and the environment of the stack. |
| Tailscale | Private network access to the server. | Network traffic of the team. |

#### AI tools used in development

| Tool | Model | Stage of use |
| ----- | ----- | ----- |
| Claude Code (repositories carry `CLAUDE.md`) | Claude, model chosen per task | Code implementation, refactoring, tests, code review, documentation. |
| OpenAI Codex (repositories carry `AGENTS.md`) | GPT, model chosen per task | Code implementation, second-opinion review. |

### 1.5 Environments, Deployment and Rollback

#### Environments

| Environment | Where | Database | Deployment |
| ----- | ----- | ----- | ----- |
| Local (development) | Developer machine | PostgreSQL 16 container | `docker compose -f deploy/docker-compose.dev.yml up -d --build` for the Platform, engines and oversight; `npm run dev` for the web app. `APP_ENV=local`. |
| Test (CI) | GitHub Actions runner | Fresh PostgreSQL 16 service per run | Automatic on each pull request and push (Report II, section 6.2). `APP_ENV=test`; scripted model provider, no live model calls. |
| Production | Team server, managed by Dokploy | PostgreSQL 16 container with a persistent volume | Automatic from `main` (below). `APP_ENV=production`. |

The Platform accepts `APP_ENV=staging`, but no staging stack is deployed yet.

#### Deployment

1. A pull request merges into `main`.
2. Backend (`logos`): when CI passes on `main`, the Deploy workflow builds five images (`capstone-be`, `capstone-dataset`, `capstone-hypothesis`, `capstone-experiment-design`, `capstone-oversight`). Web app: a push to `main` builds `capstone-fe`.
3. Each image is pushed to Docker Hub with two tags: `latest` and the commit SHA.
4. The workflow sets `IMAGE_TAG` to the commit SHA in the Dokploy stack and asks Dokploy to redeploy. The stack pulls that exact image.
5. In the backend stack the `migrate` service runs `alembic upgrade head` once the database is healthy; then `api`, the worker and the engines start. Health checks: `pg_isready` for the database, `/api/v1/health/ready` for the API, an HTTP check for the web app.

#### Rollback

1. Find the commit SHA of the last good release (Docker Hub tags or the Deploy workflow history).
2. If the bad release added migrations, run `alembic downgrade <revision of the good release>` in the `api` container first. Revision `20261002_0004` cannot be reversed.
3. Set `IMAGE_TAG` to the good SHA in the Dokploy stack and redeploy, or run the Deploy workflow by hand (`workflow_dispatch`) on the good commit.
4. Check the health endpoints, then revert the bad commit on `main` so the next deploy does not bring it back.

### 2.2.1 users

A person with an account on the Platform.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `email` | varchar(320) | Yes |  |  |
| `email_normalized` | varchar(320) | Yes | Unique |  |
| `display_name` | varchar(200) | No |  |  |
| `status` | varchar(32) | Yes |  | active, suspended |
| `created_at` | timestamptz | Yes |  |  |
| `updated_at` | timestamptz | Yes |  |  |
| `last_login_at` | timestamptz | No |  |  |
| `created_by_user_id` | uuid | No | FK → users |  |
| `avatar_storage_key` | varchar(400) | No |  |  |
| `avatar_content_type` | varchar(32) | No |  |  |
| `invite_sent_at` | timestamptz | No |  |  |
| `email_verified_at` | timestamptz | No |  |  |
| `google_subject` | varchar(255) | No | Unique |  |
| `onboarded_at` | timestamptz | No |  |  |

### 2.2.2 user_platform_roles

The platform-level role of a user (Platform Admin); one row per user at most.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `user_id` | uuid | Yes | PK, FK → users |  |
| `role_code` | varchar(32) | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.3 auth_sessions

A signed-in browser session; the token is stored only as a digest.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `user_id` | uuid | Yes | FK → users |  |
| `token_digest` | varchar(64) | Yes | Unique |  |
| `created_at` | timestamptz | Yes |  |  |
| `last_seen_at` | timestamptz | Yes |  |  |
| `idle_expires_at` | timestamptz | Yes |  |  |
| `absolute_expires_at` | timestamptz | Yes |  |  |
| `revoked_at` | timestamptz | No |  |  |

### 2.2.4 email_otps

A one-time sign-in code sent by email; stored as a digest with an expiry and attempt count.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `user_id` | uuid | Yes | Unique, FK → users |  |
| `purpose` | varchar(32) | Yes | Unique |  |
| `code_digest` | varchar(64) | No |  |  |
| `expires_at` | timestamptz | Yes |  |  |
| `attempts` | integer | Yes |  |  |
| `failed_attempts` | integer | Yes |  |  |
| `locked_until` | timestamptz | No |  |  |
| `sent_at` | timestamptz | Yes |  |  |
| `send_count` | integer | Yes |  |  |
| `send_window_started_at` | timestamptz | Yes |  |  |
| `link_token_digest` | varchar(64) | No | Unique |  |

### 2.2.5 google_connection_grants

A Google authorization that a user gives to a project for Sheets and Drive import.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `user_id` | uuid | Yes | FK → users |  |
| `project_id` | uuid | Yes | FK → projects |  |
| `state_hash` | varchar(64) | Yes | Unique |  |
| `secret_ciphertext` | text | No |  |  |
| `google_subject` | varchar(255) | No |  |  |
| `account_email` | varchar(320) | No |  |  |
| `expires_at` | timestamptz | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.6 projects

The shared workspace of a team.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `name` | varchar(160) | Yes |  |  |
| `description` | text | No |  |  |
| `domain` | varchar(160) | No |  |  |
| `objective` | text | No |  |  |
| `status` | varchar(20) | Yes |  | draft, data_ready, researching, needs_review, completed |
| `owner_user_id` | uuid | Yes | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |
| `updated_at` | timestamptz | Yes |  |  |
| `tags` | json | Yes |  |  |
| `archived_at` | timestamptz | No |  |  |

### 2.2.7 project_memberships

The membership of a user in a project, with a role and an invitation state.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | FK → projects |  |
| `user_id` | uuid | Yes | FK → users |  |
| `role_code` | varchar(32) | Yes |  | project_manager, researcher, reviewer |
| `status` | varchar(20) | Yes |  | invited, active, revoked |
| `created_by_user_id` | uuid | Yes | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |
| `revoked_at` | timestamptz | No |  |  |
| `invite_sent_at` | timestamptz | No |  |  |
| `invite_expires_at` | timestamptz | No |  |  |

### 2.2.8 project_settings

The configuration of one project (budget, presets, notifications, access settings).

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `project_id` | uuid | Yes | PK, FK → projects |  |
| `version` | integer | Yes |  |  |
| `sections` | json | Yes |  |  |
| `updated_by_user_id` | uuid | No | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.9 project_files

A document uploaded to a project.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | FK → projects |  |
| `kind` | varchar(16) | Yes |  | pdf, csv, excel |
| `original_filename` | varchar(255) | Yes |  |  |
| `content_type` | varchar(100) | Yes |  |  |
| `storage_key` | varchar(400) | Yes | Unique |  |
| `size_bytes` | bigint | Yes |  |  |
| `sha256` | varchar(64) | Yes |  |  |
| `created_by_user_id` | uuid | Yes | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.10 project_integrations

A chat tool (Slack, Microsoft Teams, Discord) that receives project notifications.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | FK → projects |  |
| `provider` | varchar(16) | Yes |  | slack, teams, discord |
| `name` | varchar(80) | Yes |  |  |
| `events` | json | Yes |  |  |
| `secret_ciphertext` | text | Yes |  |  |
| `url_hint` | varchar(300) | Yes |  |  |
| `status` | varchar(8) | Yes |  | active, paused, error |
| `consecutive_failures` | integer | Yes |  |  |
| `config_version` | integer | Yes |  |  |
| `last_delivered_at` | timestamptz | No |  |  |
| `last_error_code` | varchar(40) | No |  |  |
| `last_error_at` | timestamptz | No |  |  |
| `created_by_user_id` | uuid | Yes | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.11 integration_deliveries

One message queued for, or sent to, a project integration, with retry state.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `integration_id` | uuid | Yes | Unique, FK → project_integrations |  |
| `event_id` | uuid | Yes | Unique |  |
| `event_key` | varchar(40) | Yes |  |  |
| `ref` | json | Yes |  |  |
| `status` | varchar(8) | Yes |  | pending, sending, sent, failed |
| `attempts` | integer | Yes |  |  |
| `claims` | integer | Yes |  |  |
| `config_version` | integer | Yes |  |  |
| `next_attempt_at` | timestamptz | Yes |  |  |
| `locked_until` | timestamptz | No |  |  |
| `response_code` | integer | No |  |  |
| `error_code` | varchar(40) | No |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `sent_at` | timestamptz | No |  |  |

### 2.2.12 integration_secrets

The encrypted webhook secret of a project integration.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `name` | varchar(100) | Yes | PK |  |
| `value_encrypted` | text | Yes |  |  |
| `updated_by_user_id` | uuid | No | FK → users |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.13 comments

A remark of a member on a run or on an artifact of a run.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `run_id` | uuid | Yes | FK → research_runs |  |
| `artifact_id` | uuid | No | FK → run_artifacts |  |
| `author_user_id` | uuid | Yes | FK → users |  |
| `body` | text | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `edited_at` | timestamptz | No |  |  |
| `deleted_at` | timestamptz | No |  |  |

### 2.2.14 notifications

An in-app notification for a user.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `recipient_user_id` | uuid | Yes | FK → users |  |
| `kind` | varchar(32) | Yes |  | run_awaiting_review, run_finished, added_to_project, run_commented, project_invited, invite_accepted, invite_declined, member_role_changed, removed_from_project, integration_failed, budget_warning, budget_exceeded |
| `project_id` | uuid | Yes | FK → projects |  |
| `run_id` | uuid | No | FK → research_runs |  |
| `actor_user_id` | uuid | No | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |
| `read_at` | timestamptz | No |  |  |

### 2.2.15 notification_preferences

Which notification groups a user receives in a project.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | Unique, FK → projects |  |
| `user_id` | uuid | Yes | Unique, FK → users |  |
| `events` | json | Yes |  |  |
| `digest` | json | Yes |  |  |
| `quiet_hours` | json | Yes |  |  |
| `version` | integer | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.16 notification_emails

A notification email queued for a member, sent after commit by the dispatch loop.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `recipient_user_id` | uuid | Yes | FK → users |  |
| `kind` | varchar(32) | Yes |  | run_awaiting_review, run_finished, added_to_project, run_commented, project_invited, invite_accepted, invite_declined, member_role_changed, removed_from_project, integration_failed, budget_warning, budget_exceeded |
| `project_id` | uuid | Yes | FK → projects |  |
| `run_id` | uuid | No | FK → research_runs |  |
| `actor_user_id` | uuid | No | FK → users |  |
| `status` | varchar(16) | Yes |  | pending, sending, sent, failed, skipped |
| `attempts` | integer | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `sent_at` | timestamptz | No |  |  |

### 2.2.17 data_connections

An authorized external data source of a project; the credential is stored encrypted.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | FK → projects |  |
| `name` | varchar(120) | Yes |  |  |
| `kind` | varchar(16) | Yes |  | postgres, mysql, bigquery, google_sheets, google_drive, prometheus, influxdb, google |
| `config` | json | Yes |  |  |
| `secret_ciphertext` | text | Yes |  |  |
| `last_tested_at` | timestamptz | No |  |  |
| `last_error_code` | varchar(40) | No |  |  |
| `created_by_user_id` | uuid | Yes | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.18 datasets

A tabular dataset of a project.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | FK → projects |  |
| `name` | varchar(160) | Yes |  |  |
| `description` | text | No |  |  |
| `created_by_user_id` | uuid | Yes | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.19 dataset_versions

An immutable version of a dataset, with its content hash and storage key.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `dataset_id` | uuid | Yes | Unique, FK → datasets |  |
| `version_number` | integer | Yes | Unique |  |
| `storage_key` | varchar(400) | Yes | Unique |  |
| `original_filename` | varchar(255) | Yes |  |  |
| `size_bytes` | bigint | Yes |  |  |
| `sha256` | varchar(64) | Yes |  |  |
| `row_count` | integer | Yes |  |  |
| `column_names` | json | Yes |  |  |
| `created_by_user_id` | uuid | Yes | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |
| `source_type` | varchar(16) | Yes |  | upload, connection |
| `source_details` | json | No |  |  |

### 2.2.20 research_contexts

The research case of a project: topic, goals, context and constraints.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | Unique, FK → projects |  |
| `version_number` | integer | Yes | Unique |  |
| `body` | text | Yes |  |  |
| `front_matter` | json | No |  |  |
| `created_by_user_id` | uuid | Yes | FK → users |  |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.21 research_runs

One execution of the research pipeline for a research case.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | FK → projects |  |
| `dataset_version_id` | uuid | No | FK → dataset_versions |  |
| `research_context_id` | uuid | No | FK → research_contexts |  |
| `created_by_user_id` | uuid | Yes | FK → users |  |
| `status` | varchar(20) | Yes |  | queued, running, paused, awaiting_review, completed, budget_exceeded, failed, stopped |
| `auto_review` | boolean | Yes |  |  |
| `failure_message` | text | No |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `started_at` | timestamptz | No |  |  |
| `finished_at` | timestamptz | No |  |  |
| `updated_at` | timestamptz | Yes |  |  |
| `review_mode` | varchar(20) | No |  |  |
| `last_seq` | integer | Yes |  |  |
| `last_source_seq` | integer | Yes |  |  |
| `pipeline_key` | varchar(100) | No |  |  |
| `current_stage_key` | varchar(100) | No |  |  |
| `interaction_mode` | varchar(20) | No |  |  |
| `iteration` | integer | Yes |  |  |
| `charter_status` | varchar(10) | Yes |  | none, pending, settled, skipped |
| `obligations` | json | Yes |  |  |
| `token_budget` | bigint | Yes |  |  |
| `tokens_used` | bigint | Yes |  |  |
| `research_case` | json | Yes |  |  |

### 2.2.22 stage_runs

One execution of one stage in a run.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `research_run_id` | uuid | Yes | FK → research_runs |  |
| `iteration` | integer | Yes |  |  |
| `stage_key` | varchar(100) | Yes |  |  |
| `engine_key` | varchar(100) | Yes |  |  |
| `engine_run_id` | varchar(200) | No |  |  |
| `prior_stage_run_id` | uuid | No | FK → stage_runs |  |
| `origin_decision_id` | uuid | No | FK → stage_decisions |  |
| `status` | varchar(20) | Yes |  | PENDING, RUNNING, COMPLETED, ACCEPTED, FAILED, STOPPED, SUPERSEDED |
| `phase` | varchar(32) | No |  |  |
| `step_key` | varchar(100) | No |  |  |
| `waiting_input` | boolean | Yes |  |  |
| `open_gate` | json | No |  |  |
| `input_refs` | json | Yes |  |  |
| `config_snapshot` | json | Yes |  |  |
| `last_source_seq` | integer | Yes |  |  |
| `failure` | json | No |  |  |
| `engine_unreachable_since` | timestamptz | No |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `updated_at` | timestamptz | Yes |  |  |
| `finished_at` | timestamptz | No |  |  |
| `tokens_used` | bigint | Yes |  |  |

### 2.2.23 stage_decisions

A decision on the outcome of a stage run (accept, send back, rerun).

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `stage_run_id` | uuid | Yes | Unique, FK → stage_runs |  |
| `gate_id` | varchar(200) | No | Unique |  |
| `action` | varchar(32) | Yes |  | answer_gate, approve, comment, accept, send_back, rerun, stop |
| `payload` | json | Yes |  |  |
| `actor` | varchar(20) | Yes |  | user, system, pi |
| `reason` | text | No |  |  |
| `status` | varchar(20) | Yes |  | pending, applied |
| `decided_by_user_id` | uuid | No | FK → users |  |
| `decided_at` | timestamptz | Yes |  |  |

### 2.2.24 run_events

A trace event that an engine or the Platform emits during a run.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `run_id` | uuid | Yes | PK, FK → research_runs |  |
| `seq` | integer | Yes | PK |  |
| `source_seq` | integer | No |  |  |
| `type` | varchar(48) | Yes |  |  |
| `stage_key` | varchar(32) | No |  |  |
| `actor` | varchar(32) | No |  |  |
| `payload` | json | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `stage_run_id` | uuid | No | FK → stage_runs |  |
| `step_key` | varchar(100) | No |  |  |
| `iteration` | integer | Yes |  |  |
| `phase` | varchar(32) | No |  |  |
| `class` | varchar(20) | Yes |  |  |
| `summary` | text | No |  |  |
| `refs` | json | Yes |  |  |

### 2.2.25 run_gates

A question of a run that waits for a person to answer.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `run_id` | uuid | Yes | FK → research_runs |  |
| `gate_key` | varchar(32) | Yes |  |  |
| `kind` | varchar(32) | Yes |  |  |
| `spec` | json | Yes |  |  |
| `opened_seq` | integer | Yes |  |  |
| `answer` | json | No |  |  |
| `answered_by_user_id` | uuid | No | FK → users |  |
| `answered_at` | timestamptz | No |  |  |
| `resolved_seq` | integer | No |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `stage_run_id` | uuid | No | FK → stage_runs |  |

### 2.2.26 run_artifacts

A file that a stage run produces (hand-off object, report, figure).

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `run_id` | uuid | Yes | FK → research_runs |  |
| `kind` | varchar(20) | Yes |  | paper_pdf, paper_tex, figure, results, other |
| `filename` | varchar(255) | Yes |  |  |
| `content_type` | varchar(100) | Yes |  |  |
| `storage_key` | varchar(400) | Yes | Unique |  |
| `size_bytes` | bigint | Yes |  |  |
| `sha256` | varchar(64) | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |
| `stage_run_id` | uuid | No | Unique, FK → stage_runs |  |
| `schema` | varchar(160) | No | Unique |  |
| `version` | integer | No | Unique |  |
| `review_round` | integer | No |  |  |
| `metadata` | json | Yes |  |  |

### 2.2.27 frame_reviews

A review of the research frame of a run, submitted by a member.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `run_id` | uuid | Yes | Unique, FK → research_runs |  |
| `sequence` | integer | Yes | Unique |  |
| `request_storage_key` | varchar(400) | Yes |  |  |
| `requested_at` | timestamptz | Yes |  |  |
| `decision_storage_key` | varchar(400) | No |  |  |
| `submitted_by_user_id` | uuid | No | FK → users |  |
| `submitted_at` | timestamptz | No |  |  |

### 2.2.28 pi_consultations

A consultation of the AI PI about a run or a stage, with its result.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `research_run_id` | uuid | Yes | FK → research_runs |  |
| `stage_run_id` | uuid | No | FK → stage_runs |  |
| `kind` | varchar(32) | Yes |  | charter, gate_question, gate_review, stage_outcome, failure, close, stage_review |
| `gate_id` | varchar(200) | No |  |  |
| `authority` | varchar(20) | Yes |  | pi, researcher |
| `status` | varchar(24) | Yes |  | queued, sent, decided, applied, awaiting_researcher, endorsed, overridden, stale, failed |
| `request` | json | Yes |  |  |
| `result` | json | No |  |  |
| `failure` | json | No |  |  |
| `applied_decision_id` | uuid | No | FK → stage_decisions |  |
| `created_at` | timestamptz | Yes |  |  |
| `sent_at` | timestamptz | No |  |  |
| `decided_at` | timestamptz | No |  |  |
| `resolved_at` | timestamptz | No |  |  |
| `tokens_used` | bigint | Yes |  |  |

### 2.2.29 pi_notes

An entry of the lab notebook that the AI PI writes for a run.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `research_run_id` | uuid | Yes | FK → research_runs |  |
| `consultation_id` | uuid | No | FK → pi_consultations |  |
| `kind` | varchar(16) | Yes |  | decision, lesson, risk, observation, question, directive, override, brief, critique |
| `text` | text | Yes |  |  |
| `stage_key` | varchar(100) | No |  |  |
| `actor` | varchar(8) | Yes |  | pi, user |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.30 cost_entries

An increase of model token usage and cost, by project, run and model role.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | FK → projects |  |
| `run_id` | uuid | Yes | FK → research_runs |  |
| `source` | varchar(16) | Yes |  | stage, consultation |
| `source_id` | uuid | Yes |  |  |
| `source_key` | varchar(200) | Yes | Unique |  |
| `role` | varchar(20) | No |  |  |
| `provider` | varchar(32) | No |  |  |
| `model` | varchar(200) | No |  |  |
| `input_tokens` | bigint | Yes |  |  |
| `output_tokens` | bigint | Yes |  |  |
| `occurred_at` | timestamptz | Yes |  |  |

### 2.2.31 cost_ledger_start

The time from which the cost ledger is complete; one row.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | integer | Yes | PK |  |
| `started_at` | timestamptz | Yes |  |  |

### 2.2.32 spending_alerts

A budget alert raised for a project in a month.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `project_id` | uuid | Yes | Unique, FK → projects |  |
| `period` | varchar(7) | Yes | Unique |  |
| `kind` | varchar(32) | Yes | Unique | budget_warning, budget_exceeded |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.33 model_profiles

The model configuration of a model role (model, key reference, unit price).

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `role` | varchar(20) | Yes | Unique | stage, review |
| `provider` | varchar(32) | Yes |  |  |
| `base_url` | varchar(500) | No |  |  |
| `model` | varchar(200) | Yes |  |  |
| `api_key_encrypted` | text | No |  |  |
| `extra` | json | Yes |  |  |
| `scope` | varchar(20) | Yes | Unique |  |
| `updated_by_user_id` | uuid | No | FK → users |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.34 platform_settings

Platform-wide settings that a Platform Admin edits; one row.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | integer | Yes | PK |  |
| `updated_by_user_id` | uuid | No | FK → users |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.35 engine_settings

Settings of one stage engine that a Platform Admin edits.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `engine_key` | varchar(100) | Yes | PK |  |
| `updated_by_user_id` | uuid | No | FK → users |  |
| `updated_at` | timestamptz | Yes |  |  |

### 2.2.36 audit_events

An append-only record of an administrative or security action.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `actor_user_id` | uuid | No | FK → users |  |
| `action` | varchar(100) | Yes |  |  |
| `resource_type` | varchar(80) | Yes |  |  |
| `resource_id` | varchar(64) | Yes |  |  |
| `project_id` | uuid | No |  |  |
| `request_id` | varchar(64) | No |  |  |
| `details` | json | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.37 monitoring_events

A captured log event of a service, for log monitoring.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `event_type` | varchar(48) | Yes |  |  |
| `service` | varchar(64) | Yes |  |  |
| `environment` | varchar(20) | Yes |  |  |
| `worker_id` | varchar(36) | Yes |  |  |
| `level` | varchar(16) | Yes |  |  |
| `message` | varchar(160) | Yes |  |  |
| `request_id` | varchar(64) | No |  |  |
| `trace_id` | varchar(64) | No |  |  |
| `project_id` | varchar(64) | No |  |  |
| `run_id` | varchar(64) | No |  |  |
| `actor_id` | varchar(64) | No |  |  |
| `provider_id` | varchar(100) | No |  |  |
| `method` | varchar(10) | No |  |  |
| `route` | varchar(200) | No |  |  |
| `status_code` | integer | No |  |  |
| `duration_ms` | double precision | No |  |  |
| `attributes` | json | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.38 monitoring_alerts

An alert raised from monitoring events, with its acknowledgement.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `service_id` | varchar(160) | Yes |  |  |
| `service` | varchar(64) | Yes |  |  |
| `environment` | varchar(20) | Yes |  |  |
| `code` | varchar(80) | Yes |  |  |
| `severity` | varchar(16) | Yes |  | warning, critical |
| `message` | varchar(240) | Yes |  |  |
| `status` | varchar(16) | Yes |  | active, resolved |
| `active_key` | varchar(220) | No | Unique |  |
| `started_at` | timestamptz | Yes |  |  |
| `resolved_at` | timestamptz | No |  |  |
| `acknowledged_at` | timestamptz | No |  |  |
| `acknowledged_by_user_id` | uuid | No | FK → users |  |
| `details` | json | Yes |  |  |

### 2.2.39 monitoring_capture_gaps

A period in which log capture of a service was incomplete.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `id` | uuid | Yes | PK |  |
| `service` | varchar(64) | Yes |  |  |
| `environment` | varchar(20) | Yes |  |  |
| `worker_id` | varchar(36) | No |  |  |
| `reason` | varchar(48) | Yes |  |  |
| `started_at` | timestamptz | Yes |  |  |
| `ended_at` | timestamptz | Yes |  |  |
| `created_at` | timestamptz | Yes |  |  |

### 2.2.40 monitoring_worker_states

The last heartbeat and state of a background worker.

| Column | Type | Required | Key | Allowed values |
| ----- | ----- | ----- | ----- | ----- |
| `worker_id` | varchar(36) | Yes | PK |  |
| `service` | varchar(64) | Yes |  |  |
| `environment` | varchar(20) | Yes |  |  |
| `status` | varchar(16) | Yes |  |  |
| `started_at` | timestamptz | Yes |  |  |
| `heartbeat_at` | timestamptz | Yes |  |  |
| `stopped_at` | timestamptz | No |  |  |
| `persisted_watermark` | timestamptz | No |  |  |
| `dropped_count` | integer | Yes |  |  |

### 2.4 Database Script

The database script is [`deliverables/database/FA26SE115_database-script.sql`](../database/FA26SE115_database-script.sql). It holds the schema of the 41 tables of the current build (Alembic revision `20261022_0048`), with no data. To regenerate it, apply the migrations of `logos/services/management` to an empty PostgreSQL 16 database (`alembic upgrade head`), then run `pg_dump --schema-only --no-owner --no-privileges`.

Tables: `alembic_version`, `audit_events`, `auth_sessions`, `comments`, `cost_entries`, `cost_ledger_start`, `data_connections`, `dataset_versions`, `datasets`, `email_otps`, `engine_settings`, `frame_reviews`, `google_connection_grants`, `integration_deliveries`, `integration_secrets`, `model_profiles`, `monitoring_alerts`, `monitoring_capture_gaps`, `monitoring_events`, `monitoring_worker_states`, `notification_emails`, `notification_preferences`, `notifications`, `pi_consultations`, `pi_notes`, `platform_settings`, `project_files`, `project_integrations`, `project_memberships`, `project_settings`, `projects`, `research_contexts`, `research_runs`, `run_artifacts`, `run_events`, `run_gates`, `spending_alerts`, `stage_decisions`, `stage_runs`, `user_platform_roles`, `users`.

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

### 2.4 Database Script

The database script is [`deliverables/database/FA26SE115_database-script.sql`](../database/FA26SE115_database-script.sql). It holds the schema of the 41 tables of the current build (Alembic revision `20261022_0048`), with no data. To regenerate it, apply the migrations of `logos/services/management` to an empty PostgreSQL 16 database (`alembic upgrade head`), then run `pg_dump --schema-only --no-owner --no-privileges`.

Tables: `alembic_version`, `audit_events`, `auth_sessions`, `comments`, `cost_entries`, `cost_ledger_start`, `data_connections`, `dataset_versions`, `datasets`, `email_otps`, `engine_settings`, `frame_reviews`, `google_connection_grants`, `integration_deliveries`, `integration_secrets`, `model_profiles`, `monitoring_alerts`, `monitoring_capture_gaps`, `monitoring_events`, `monitoring_worker_states`, `notification_emails`, `notification_preferences`, `notifications`, `pi_consultations`, `pi_notes`, `platform_settings`, `project_files`, `project_integrations`, `project_memberships`, `project_settings`, `projects`, `research_contexts`, `research_runs`, `run_artifacts`, `run_events`, `run_gates`, `spending_alerts`, `stage_decisions`, `stage_runs`, `user_platform_roles`, `users`.

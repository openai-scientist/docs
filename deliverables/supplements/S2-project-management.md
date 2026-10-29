# Supplement to Report II

Facts from the two code repositories (`logos`, the Platform and engines; `ai-research-platform-fe`, the web app) on 2026-10-29. The build places each section under the template heading with the same number.

### 6.2 Source Code Management

#### Repositories and branches

| Repository | Content | Branches |
| ----- | ----- | ----- |
| `logos` | Platform (management service), oversight service (AI PI), stage engines, shared packages | `main` (released), `dev` (integration), `feat/*`, `fix/*`, `perf/*` (short-lived work) |
| `ai-research-platform-fe` | Web app | `main` (released), `dev` (integration), `feat/*` (short-lived work) |

Branch rules:

- A change starts on a short-lived branch from `dev` and reaches `dev` through a pull request with peer review.
- `main` receives `dev` through a pull request. A push to `main` starts the deployment (Report IV, section 1.5).
- Commit messages follow the Conventional Commits format: `type(scope): summary`, for example `feat(run-studio): start runs from a research case`.
- Secrets live in the CI secret store and the deployment server, never in a repository.

#### Continuous integration

| Repository | Trigger | Checks |
| ----- | ----- | ----- |
| `logos` | Every pull request; push to `main` and `release/**`; tags; merge queue; nightly | Import rules, lint and format (Ruff), contract check; test plan by changed files (feature tier on a pull request, every test elsewhere); migrations applied to a clean PostgreSQL 16 database and checked against the models (`alembic upgrade head`, `alembic check`); Docker build of each service image; one required gate job. |
| `ai-research-platform-fe` | Every pull request; push to `dev` and `main` | Lint and format (Biome), unit tests (Vitest). A Git pre-commit hook (Husky, lint-staged) runs Biome on staged files. |

The web app therefore has its own continuous integration. This answers open item O-7.

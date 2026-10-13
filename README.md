# LeadFlow

A single-screen lead manager built with Next.js, the existing shadcn theme, FastAPI,
SQLAlchemy and PostgreSQL. Username/password sign-up and sign-in protect each user’s
workspace. Browser requests use
Next.js Server Actions and same-origin authentication routes; the API URL,
service credential and database connection stay on the server.

Live app: [leadflow.arkapravo.in](https://leadflow.arkapravo.in) ·
[API readiness](https://api.leadflow.arkapravo.in/api/v1/health).
Frontend changes deploy through Vercel CI/CD; backend changes deploy through Render
CI/CD, using Neon PostgreSQL. The parent pins tested application commits.

## Repositories

| Repository | Purpose |
| --- | --- |
| [LeadFlow](https://github.com/Arkapravo-Ghosh/LeadFlow) | Parent: Compose, documentation and submodule versions |
| [LeadFlow-Frontend](https://github.com/Arkapravo-Ghosh/LeadFlow-Frontend) | Next.js frontend, deployed to Vercel |
| [LeadFlow-Backend](https://github.com/Arkapravo-Ghosh/LeadFlow-Backend) | FastAPI backend, deployed to Render |

## Run locally

Requirements: Docker Desktop with Compose Watch support, Git, and optionally Node
and uv for host checks. Both application directories are Git submodules.

```sh
git clone --recurse-submodules https://github.com/Arkapravo-Ghosh/LeadFlow.git
cd LeadFlow
cp .env.example .env
# Replace BACKEND_API_KEY and POSTGRES_PASSWORD with random hex values.
# Generate each value separately: openssl rand -hex 32
docker compose up --build --watch
```

Open `http://localhost:3000` (or the `FRONTEND_PORT` configured in `.env`). The
existing local checkout uses port 3001 because another application occupies 3000.
Only Next.js has a host port. PostgreSQL persists in a named volume; FastAPI and
PostgreSQL communicate on the Compose network. Development uses local PostgreSQL
and does not consume the Neon URL in `backend/.env`.

Choose **Create account** on `/login`, or open `/signup`. Enter a username, a
12–128 character password and its confirmation. Registration signs you in
automatically to your own empty workspace. Existing users sign in at `/login`.
The public homepage explains LeadFlow before sign-up. Your private lead manager
is at `/workspace`, and successful sign-in or sign-up opens it automatically.
The administrator CLI `docker compose exec backend uv run leadflow-create-user`
remains available for private provisioning and legacy data claims.

To add optional deterministic sample leads to an existing account:

```sh
docker compose exec backend uv run leadflow-seed
# Enter the account username when prompted.
```

The seed supplies six leads covering every status, twelve discussions, today's
follow-ups and overdue dates. Running it again preserves existing records. It is
explicitly opt-in; production startup never seeds data.

Use `docker compose up --watch` for normal development. If saved images are stale
after Git updates or a previous Watch session, use
`docker compose up --build --watch` once to update them. Watch syncs running
containers; those edits do not update the saved images used to recreate containers.
Compose retains normal image reuse; rebuilds are explicitly requested with `--build`
or triggered by the configured Watch rules.

Compose syncs source edits; Next.js and Uvicorn reload them. Migration changes
restart the API and dependency/Dockerfile changes rebuild the relevant image.
Restart Compose after changing root environment variables. `docker compose down`
keeps data; adding `--volumes` deletes the local database.

## Features

- Username/password sign-up and login, Argon2id hashes, expiring/revocable sessions and per-user data.
- Create a lead with required name and optional company/phone.
- Search names, filter by all six statuses and Today/Overdue/Unscheduled,
  and pin today's follow-ups.
- Red overdue cues, latest note previews, relative times and discussion timeline.
- Save notes and optional follow-ups atomically; change status immediately.
- Themed shadcn calendar and time field for follow-ups in the configured timezone.
- Light/dark/system support using the original shadcn palette and typography.
- Public landing page with example workflow, shared LeadFlow logo and favicon.
- Public-page SEO metadata, dark landing screenshot for social previews, sitemap and robots.
- Animated form/workspace/timeline skeletons and pending-action spinners; reduced-motion support.
- Keyboard-accessible dialogs, inline validation, retry feedback, responsive UI.
- Mobile/tablet status selectors and wrapping desktop filters; long lead text wraps on phones.

Follow-ups use UTC storage and `APP_TIMEZONE` for calendar input/display. A note
without a new date preserves the lead's current follow-up. Today and overdue may
overlap; leads are rendered only once. Server refreshes preserve active drafts.

## Verify

```sh
docker compose --profile test run --build --rm tests
uv run --project backend ruff check backend/src backend/migrations backend/tests
cd frontend
npm ci
npm run lint
npm run typecheck
npm test
npm run build
```

API tests use an isolated disposable PostgreSQL database, never the application
or Neon database. See [verification](docs/verification.md) for actual results and
screenshots. See [authentication](docs/authentication.md) for account setup and legacy data.
See [API](docs/api.md) for routes and generated client types.

## Structure and deployment

- `frontend/`: Next.js App Router, server API boundary and focused UI components.
- `backend/`: account provisioning, password/session services, thin FastAPI routers, services, repositories, Alembic migrations.
- `docs/`: architecture, API, deployment and verification.
- `agentdocs/`: private original correspondence/images, excluded from public Git.
- `compose.yaml`: frontend, backend, local PostgreSQL and isolated test services.

Production: **Render API → Neon PostgreSQL; Vercel frontend → Render API**.
Configure your public domain through `APP_URL`, with no source edits. Follow
[deployment.md](docs/deployment.md) for service settings and the configured domains.
Deployment and provider configuration remain owner-managed; application pushes
use the existing CI/CD integrations.

The parent repository pins the independently published frontend/backend submodules
using their full GitHub URLs. If you cloned without submodules, run:

```sh
git submodule update --init --recursive
```

To update an existing checkout to the parent's latest pinned versions:

```sh
git pull --ff-only
git submodule update --init --recursive
```

Commit and push changes inside each application repository first, then commit and
push its updated pointer in the parent. Existing initialization history is
preserved. Run `./scripts/install-hooks.sh` to enforce
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) locally.
Hand-written modules stay focused and small; generated types are an exception.

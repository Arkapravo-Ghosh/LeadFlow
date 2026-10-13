# LeadFlow

A single-screen lead manager built with Next.js, the existing shadcn theme, FastAPI,
SQLAlchemy and PostgreSQL. Browser requests use Next.js Server Actions; the API URL,
service credential and database connection stay on the server.

## Run locally

Requirements: Docker Desktop with Compose Watch support, Git, and optionally Node
and uv for host checks. Both application directories are Git submodules.

```sh
git clone --recurse-submodules <your-parent-repository-url> LeadFlow
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

In another terminal, add deterministic sample leads:

```sh
docker compose exec backend uv run leadflow-seed
```

The seed supplies six leads covering every status, twelve discussions, today's
follow-ups and overdue dates. Running it again preserves existing records. It is
explicitly opt-in; production startup never seeds data.

Compose syncs source edits; Next.js and Uvicorn reload them. Migration changes
restart the API and dependency/Dockerfile changes rebuild the relevant image.
Restart Compose after changing root environment variables. `docker compose down`
keeps data; adding `--volumes` deletes the local database.

## Features

- Create a lead with required name and optional company/phone.
- Search names, filter by all six statuses and Today/Overdue/Unscheduled,
  and pin today's follow-ups.
- Red overdue cues, latest note previews, relative times and discussion timeline.
- Save notes and optional follow-ups atomically; change status immediately.
- Light/dark/system support using the original shadcn palette and typography.
- Keyboard-accessible dialogs, inline validation, retry feedback, responsive UI.

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
screenshots. See [API](docs/api.md) for routes and generated client types.

## Structure and deployment

- `frontend/`: Next.js App Router, server API boundary and focused UI components.
- `backend/`: thin FastAPI routers, services, repositories, Alembic migrations.
- `docs/`: architecture, API, deployment and verification.
- `agentdocs/`: private original correspondence/images, excluded from public Git.
- `compose.yaml`: frontend, backend, local PostgreSQL and isolated test services.

Production: **Render API → Neon PostgreSQL; Vercel frontend → Render API**.
Configure your public domain through `APP_URL`, with no source edits. Follow
[deployment.md](docs/deployment.md) for exact service settings. Deployment and
remote publication are left to you.

The parent repository tracks independent frontend/backend submodules. Publish
these as sibling `LeadFlow`, `LeadFlow-frontend` and `LeadFlow-backend` repositories
or update `.gitmodules` to your chosen URLs before sharing a public clone. Commit
child repositories first, then the parent pointers. Existing initialization
history is preserved. Run `./scripts/install-hooks.sh` to enforce
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) locally.
Hand-written modules stay focused and small; generated types are an exception.

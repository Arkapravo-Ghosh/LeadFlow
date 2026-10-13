# Production deployment

Deploy the frontend repository to Vercel and backend repository to Render. Use
Neon for PostgreSQL. No domain, provider host or credential is hardcoded in the
application. The supplied configuration does not provision or deploy services.

## Neon

Create a PostgreSQL database and copy its connection URL, preserving provider SSL
parameters. Put it in Render's `DATABASE_URL`. Alembic creates a dedicated
`leadflow` schema; the database role needs permission to create that schema and
its tables. The small SQLAlchemy connection pool uses pre-ping, recycling and a
connection timeout. Neon pooled connections are suitable for the running API.
Keep a direct connection available for migration operations if your provider
pooler imposes migration restrictions. Never put this URL in Vercel or client code.

## Render backend

Create a Docker Web Service from the backend repository, Dockerfile `Dockerfile`,
build context repository root. The final Docker stage is production and excludes
development dependencies. Leave the Docker command unset: `scripts/start.sh` runs
`alembic upgrade head`, then binds Uvicorn to `0.0.0.0:$PORT`. Set health check
`/api/v1/health`. It returns 503 when the database is unavailable.

| Environment | Value |
| --- | --- |
| `DATABASE_URL` | Neon connection string, including SSL options |
| `BACKEND_API_KEY` | Random private credential, at least 16 characters |
| `AUTH_SESSION_HOURS` | Fixed session lifetime, default 12 hours |
| `PORT` | Provided by Render; optional override, default fallback 8000 |

A Render Web Service has a public network address so Vercel can reach it. Domain
routes require `X-API-Key` plus a valid user session; public API documentation is
disabled. Health reveals only service readiness. Browser traffic never goes
directly to Render. Username/password login issues opaque, database-backed
sessions; each user sees
only their own leads and discussions. In Render’s private shell, run
`uv run leadflow-create-user` and enter your chosen credentials interactively.
There is no default production account. For an existing database with unowned
legacy leads, see [authentication](authentication.md) before claiming them.

Migration-at-start is intended for one API instance. Before scaling replicas,
move migrations into a single pre-deploy/release job to avoid concurrent DDL.
No automatic production seed. Back up data before future schema changes.

## Vercel frontend

Import the frontend repository; framework Next.js, root directory repository root,
install `npm ci`, build `npm run build`. Use the Node 24 runtime to match Docker.
The frontend declares matching Node 24 types compatible with Vitest 5; keep
`package-lock.json` committed so installs use the verified dependency graph.
Set these variables for the Production environment (and separately for Preview
if desired). Redeploy after changing environment values.

| Environment | Value |
| --- | --- |
| `BACKEND_API_URL` | Render HTTPS service origin, no `/api/v1` suffix |
| `BACKEND_API_KEY` | The exact private value configured in Render |
| `APP_TIMEZONE` | IANA timezone, e.g. `Asia/Kolkata` |
| `APP_URL` | Your frontend origin, e.g. `https://your-domain.example` |

None of these needs a `NEXT_PUBLIC_` prefix. Backend URL/key are read only from
`server-only` modules. Server Actions validate payloads and send fixed-path API
requests. SSR fetches use `no-store`; successful mutations revalidate the page.
`APP_URL` supplies the metadata base and exact allowed login/logout origin; configure the same custom domain in Vercel's
Domains settings and your DNS. Changing an env variable does not change DNS.
Next.js uses its normal same-origin Server Action protection; no permissive CORS
or wildcard action origins are configured. Preview deployments should use their
own origin and preferably separate test data.

## Optional production Docker smoke test

`compose.production.yaml` exercises production images with `backend/.env` for the
external database. It runs migrations against that URL, so choose a dedicated test
Neon database/branch before running it. It does not deploy to Render or Vercel.

```sh
docker compose -f compose.production.yaml up --build
```

Use a different `FRONTEND_PORT` if development is running. Do not seed production
unless you explicitly want synthetic sample data there.

## Verify after your deployment

Check Vercel `/health`, then sign in with the account provisioned on Render. Create a synthetic lead, add a note/date, change its
status and reload. Inspect browser network requests: all data interactions should
be on the frontend origin. Verify light/dark persistence and your timezone. Rotate
the service key on both providers together if it is ever disclosed.

References: [Render FastAPI](https://render.com/docs/deploy-fastapi),
[Render port binding](https://render.com/docs/web-services#port-binding),
[Vercel environment variables](https://vercel.com/docs/environment-variables),
[Neon connection strings](https://neon.com/docs/connect/connect-from-any-app).

# API contract

All routes except health require `X-API-Key`. Lead/discussion routes and `/auth/me`
also require `Authorization: Bearer <opaque session>`. Ownership comes from this
session; foreign-user IDs return 404 and are never selectable through payloads. FastAPI is called only by the Next.js server.
All routes use `/api/v1`; interactive docs and public OpenAPI routes are disabled.

| Method / path | Behavior |
| --- | --- |
| GET `/health` | Unauthenticated readiness; 503 if DB unavailable |
| POST `/auth/signup` | Username/password (password: 12–128 characters); 201 with internal session; 409 duplicate, 422 invalid, 429 throttled; new account has no leads |
| POST `/auth/login` | Username/password; internal token + expiry + safe user summary; 401 invalid, 429 throttled |
| GET `/auth/me` | Current user ID/username; 401 expired/missing/disabled session |
| POST `/auth/logout` | Revoke bearer session; 204, idempotent |
| GET `/leads` | Owned summary list; optional `status`, `search`, `timezone` |
| POST `/leads` | Create: `name`, optional `company`/`phone`; starts New |
| GET `/leads/{id}` | Lead summary, or 404 |
| PATCH `/leads/{id}` | Update `status` |
| GET `/leads/{id}/discussions` | Newest-first timeline, or 404 |
| POST `/leads/{id}/discussions` | `note`, optional aware `follow_up_at`; atomic save |

The browser uses Next.js `/api/auth/signup` and `/api/auth/login`, with exact
`APP_URL` origin checks. Sign-up also requires matching `confirmation` in the
frontend request; only username/password reach FastAPI. Next.js sets the HTTP-only
cookie and returns `{ ok: true }`, never the internal API token. The optional
internal `X-Registration-Source` header carries a hashed trusted source for the
registration budget; it is accepted only behind the private service key.

Statuses: `new`, `contacted`, `qualified`, `proposal_sent`, `won`, `lost`.
Names are trimmed, 1–120 characters; company 120, phone 40; note 1–5000. Naive
follow-up timestamps are rejected. UTC timestamps and a server clock/timezone
accompany list results. Invalid input returns 422 with field messages. Missing
records return 404; database failures return redacted 500 responses.

Regenerate frontend types after changing backend schemas:

```sh
mkdir -p agentdocs
docker compose exec -T backend uv run leadflow-openapi > agentdocs/openapi.json
cd frontend
npm run generate:api
```

`src/lib/api-types.ts` is generated; do not hand-edit it. No OpenAPI endpoint needs
to be publicly exposed.

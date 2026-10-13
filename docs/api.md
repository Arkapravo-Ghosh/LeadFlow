# API contract

Domain routes require `X-API-Key`. FastAPI is called only by the Next.js server.
All routes use `/api/v1`; interactive docs and public OpenAPI routes are disabled.

| Method / path | Behavior |
| --- | --- |
| GET `/health` | Unauthenticated readiness; 503 if DB unavailable |
| GET `/leads` | Summary list; optional `status`, `search`, `timezone` |
| POST `/leads` | Create: `name`, optional `company`/`phone`; starts New |
| GET `/leads/{id}` | Lead summary, or 404 |
| PATCH `/leads/{id}` | Update `status` |
| GET `/leads/{id}/discussions` | Newest-first timeline, or 404 |
| POST `/leads/{id}/discussions` | `note`, optional aware `follow_up_at`; atomic save |

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

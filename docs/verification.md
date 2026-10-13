# Verification — 13 October 2026

The application was checked against real PostgreSQL 17 in Docker. Production
images were exercised on a separate local Compose stack with a disposable database;
this is local production-image evidence, not a Render/Vercel/Neon deployment.

| Check | Result |
| --- | --- |
| PostgreSQL integration suite | 36 passed: auth/session expiry/revocation, login limits, ownership isolation, legacy claims and seed ownership plus prior domain cases |
| Frontend unit suite | 6 passed: timezone conversion, ambiguous/nonexistent DST times, relative timestamps |
| ESLint / TypeScript / Ruff | Passed |
| Next.js production build | Passed; dynamic server-streamed workspace and server health route |
| Development / production Docker images | Built; local services reached healthy state |
| Compose Watch | Source sync observed; Next HMR and Uvicorn StatReload verified; dependency rebuild observed |
| Seed | First run inserted 6 leads/12 notes; repeat inserted 0 and preserved data |
| Lead creation | Required name enforced; optional company/phone; New default; visible immediately |
| Name/status/follow-up filters | Search, all six statuses, Today/Overdue/Unscheduled and combined empty results checked in browser |
| Discussion / schedule | Newest-first, immediate preview update; date saved in displayed zone; no-date note preserved schedule |
| Overdue/today grouping | Red overdue cues; a today+overdue lead appeared once in the pinned group |
| Persistence | Notes/status survived page reload; local records survived PostgreSQL restart |
| Failure recovery | Deliberately aborted a save request; draft stayed intact; retry persisted it |
| Background refresh | Focus refresh preserved active discussion draft |
| Dialog completion race | Closing during a delayed save stayed closed after the save completed |
| Light/dark | Both rendered; selected mode survived reload |
| Small screen | Checked 390×667; no horizontal page overflow; follow-up Save button reachable by dialog scrolling |
| Server boundary | Browser interactions stayed on frontend origin; service credential absent from browser static assets |
| Theme preservation | Original `globals.css`, `components.json`, and original backend `.env` hashes unchanged |
| OpenAPI contract | Regenerated response types matched committed generated file |

The Browser plugin was unavailable; browser verification used the installed
Playwright CLI fallback. A single expected console network error came from the
intentionally aborted request. No unexpected runtime console errors were observed.
A mobile form overflow and a closed-dialog completion race found during testing
were fixed and rechecked.

## Screenshots

Captured from working production images with synthetic data:

- [Light workspace](screenshots/light.png)
- [Dark workspace](screenshots/dark.png)
- [Add lead](screenshots/add-lead.png)
- [Discussion timeline](screenshots/timeline.png)
- [Small-screen follow-up form](screenshots/mobile-timeline.png)

## Known limits

The npm audit reported 9 high-severity package entries stemming from the inherited
`braces` dependency through shadcn/ESLint tooling. The advisory lists no patched
version as of this check. A forced audit fix proposed downgrading the selected
framework/tooling, so it was not applied. `braces` could not be resolved in the
standalone production runtime; that check does not eliminate every tooling risk.
Track [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) and
update when a compatible fix becomes available. Do not process untrusted glob
patterns through those development tools.

Starlette's test client emitted an upstream `httpx` deprecation warning; the
integration assertions passed. Username/password authentication and user-owned
workspaces are now implemented. The three repositories are published on GitHub;
DNS and cloud deployment remain for the owner. Provider-specific runtime behavior
must be checked after deployment using the steps in deployment.md.

## AI assistance

Implementation, documentation and checks were developed with Codex assistance.
The app contains no model training/inference feature; FastAPI implements the API.
Results above distinguish actual local runtime checks from unperformed cloud work.

## Hydration regression fix — 13 October 2026

A subsequent check reproduced the reported theme-toggle attribute mismatch with
a saved dark preference. The earlier theme persistence check missed this hydration
warning. The server emitted a moon icon/dark-mode label while the client rendered
a sun icon/light-mode label.

The toggle now uses a deterministic server/hydration snapshot and a fixed-size
neutral placeholder until hydration completes. It then renders the resolved theme
icon, accessible label and title. No new hydration-warning suppression or theme
token changes were introduced. See [React server snapshots](https://react.dev/reference/react/useSyncExternalStore#adding-support-for-server-rendering)
and [next-themes hydration guidance](https://github.com/pacocoursey/next-themes#avoid-hydration-mismatch).

Playwright on localhost:3001 checked saved light/dark (including opposite system
preferences), system dark/light, toggling, and reload persistence. All four initial
states plus reloads after toggling completed without console warnings/errors or
page errors. Labels, titles, icons and document theme agreed. Desktop 1440×1000
and mobile 390×844 screenshots showed meaningful content and no error overlay.
ESLint, TypeScript and the production build passed. Browser plugin not available;
Playwright CLI was used. This targeted fix was checked in Chromium; other browser
engines and a fresh cloud deployment were not exercised for this change.

## Authentication — 13 October 2026

The 36-case PostgreSQL suite includes Argon2id verification, canonical usernames,
generic invalid-credential messages, persisted failed-login limits and expiry,
disabled accounts, missing service/user credentials, session expiry, logout
revocation, cross-account denial on every lead/discussion operation, ownership
spoof rejection, legacy data claims and per-account seed idempotency. Alembic's
metadata check detected no uncommitted schema operations.

Production Docker images ran on an isolated Compose stack with a disposable
PostgreSQL database and randomly generated temporary accounts. Chromium browser
checks passed for anonymous redirects, masked password input, invalid login
feedback, same-origin CSRF checks, authentication response redaction, HTTP-only /
Secure / SameSite=Lax cookie attributes, cookie expiry, authenticated SSR,
lead/note Server Actions, reload persistence, authenticated login-page redirect,
session revocation and removal on logout, an empty second account's workspace,
light/dark persistence, and 390×844 layout without horizontal overflow. Browser
requests stayed on the frontend origin; no unexpected console, page or hydration
errors occurred. One expected 401 network message came from the invalid-login test.

The Playwright CLI inspected the development login page. An ad-hoc Playwright
script exercised the production browser flow with temporary credentials held only
in process memory, avoiding CLI recordings, traces and populated-form screenshots.
The temporary Compose stack was removed after checks. The actual local sample
account was created privately, its sign-in/hash verified, and all 7 existing leads
and 16 discussions assigned without duplication. The documented interactive account-creation command also passed a PTY check
with non-echoing password input; the account-specific seed CLI inserted six
records and zero on repeat. No demo credential was used in browser recordings
or written to a file. Production account provisioning on Neon
remains an explicit owner task through the documented private CLI.

ESLint, TypeScript, six frontend unit tests, Ruff, generated API types and the
Next.js production build passed. Original theme/configuration and original backend
`.env` hashes remained unchanged. Login/logout routes are dynamic; account data
streams under Suspense with no server caching of user-specific responses.


## Compose startup regression — 13 October 2026

A subsequent plain `docker compose up` reproduced an Alembic startup failure:
the database was already at `0002`, while the saved development backend image
contained only `0001`. Watch had synced new files into the previous running
container, but those files were absent from the old image used to recreate it.

Rebuilding the development images restored startup. Alembic's current revision
and code head both reported `0002`, and all three services reached healthy status.
The running backend used the newly built saved image. Frontend `/login` returned
200, and `/health` returned `ok`. The original account, all 7 owned leads and all
16 discussions remained present; no data reset or migration stamp was used.

The temporary forced-build policy was removed following the owner's correction.
Compose retains normal image reuse. Use `docker compose up --build --watch` when
images need updating, then `docker compose up --watch` for normal development.
`docker compose config --quiet` passed after removing the policy. This correction
changed only Compose configuration and documentation; no additional rebuild or
database operation was needed.


## Vercel install dependency correction — 14 October 2026

A fresh install with peer-dependency checks enabled reproduced the reported
`ERESOLVE`: the frontend declared `@types/node` 20 while Vitest 5 required Node
22 or 24+ type definitions. Local npm's `legacy-peer-deps` setting had masked
that mismatch. The frontend now declares `@types/node` 24.19.2 and a lockfile
resolved with peer checks enabled. No framework or theme changes were needed.

Clean-checkout validation also found that plain `tsc` needed Next.js-generated
`LayoutProps`. The typecheck script now runs `next typegen` before `tsc --noEmit`.

A disposable Linux amd64 Compose container with Node 24.21.0 and npm 11.19.0
passed `npm install` and `npm ci` with `legacy-peer-deps=false` and `force=false`,
then ESLint, type checking, all 6 unit tests and the Next.js production build.
The resulting lockfile matched the committed frontend lockfile. This is clean
Linux install/build evidence; a new Vercel deployment was not manually triggered.

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
The owner has now deployed Vercel, Render and Neon at the domains documented in
deployment.md. Historical checks below describe local runs; the sign-up section
records the current deployment observations separately.

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

## Self-service sign-up — 14 October 2026

Added `/signup`, a linked shared sign-in/sign-up form, password confirmation,
server validation, Argon2id hashing and automatic sign-in. New users receive an
empty workspace. Existing demo data remains assigned to its original owner.
Registration cannot claim legacy records or opt into seeding. No new migration
is required: the current `0002` schema already contains users and session tables.

- Backend Ruff lint/format checks passed. The Compose disposable PostgreSQL
  suite passed **47 tests**, including 11 registration cases: secret redaction,
  empty accounts, ownership, canonical duplicates, rejected short/long passwords
  and extra ownership fields, private service-key enforcement, atomic rollback,
  PostgreSQL unique-index conflicts and independent expiring rate limits.
- Frontend ESLint, generated route types + TypeScript, all **6** existing date/DST
  tests, and the Next.js production build passed. Node 24 production Docker
  images built successfully with `npm ci`; Compose readiness passed for all
  services. Development and optional production Compose configuration validated.
- Browser plugin was not available; Playwright 1.64 with system Chrome exercised
  production images at `http://localhost:3002` with a dedicated tmpfs PostgreSQL
  database. Desktop 1440×1000 and mobile 390×844 showed the expected page,
  readable fields, no horizontal overflow, no framework overlay and no unexpected
  console, runtime or hydration errors. Blank-form screenshots were inspected
  outside the public repositories; no populated credential forms were captured.
- The browser flow passed login → sign-up → confirmation error → registration
  → empty workspace → lead/note creation → logout → duplicate registration error
  → second account with empty workspace → original account login with persisted
  data. Authenticated sign-up redirects to the workspace. Light/dark toggles and
  dark-mode reload passed. All browser requests remained on the frontend origin.
- Direct frontend HTTP checks rejected missing/foreign origins, weak passwords,
  mismatched confirmation and ownership spoofing. Successful registration returned
  only `{ ok: true }`. HTTP-only/Secure/SameSite=Lax session cookies were verified,
  inaccessible to JavaScript; logout removed cookies and all temporary sessions.
  All three throwaway accounts stored Argon2id hashes. Credentials were generated
  in process memory and discarded with the disposable database.
- The shadcn theme/preset and private backend `.env` hashes are unchanged. The
  public-source/history scan found no private database URL, service key, database
  password or sample username. No production accounts or leads were created for QA.

At the start of this change, the deployed frontend `/login` returned HTTP 200 and
`https://api.leadflow.arkapravo.in/api/v1/health` returned `{ "status": "ok" }`.
The owner reports Vercel/Render CI/CD configured; provider-specific deployment
observations after the source push are recorded separately below. Local tests
do not assert Vercel proxy-header behavior or production registration mutations.

### Deployment observations after the sign-up source push

The backend sign-up route became available on the configured API domain before
the frontend was pushed (GET returns 405 with POST supported). Vercel reported
production deployment `dpl_DVzNmZ8999nZyYjjDxoeuzqk3un8` **READY** for frontend
commit `0b24e3ec345efbc7ff2b2219b19404a2a1e5a054`. Backend commit
`0963726` was pushed first; no manual provider deployment was triggered.

Chrome/Playwright then verified the actual custom domain:
`https://leadflow.arkapravo.in/signup` displayed the account form with the correct
title and working sign-in/sign-up links. Desktop and mobile screenshots were
inspected. Dark mode persisted after reload, no horizontal overflow or framework
overlay appeared, and console/runtime/hydration checks passed. Browser requests
stayed on the frontend domain. Both frontend `/health` and API `/api/v1/health`
returned HTTP 200; the API reported `status: ok`. Malformed sign-up requests from
the configured origin returned 400; foreign-origin requests returned 403.
These rejected payloads stop in Next.js before account creation.

The complete credential/ownership flow was exercised against local production
images, not by creating production test users. Production registration writes
and Vercel's trusted proxy-IP behavior were not exercised. The original local
database still contains one account, seven owned leads and sixteen discussions;
all disposable QA services/database containers were removed.

## Landing page, branding and loading states — 14 October 2026

The public `/` page now explains the shipped workflow using the existing shadcn
Button styles, Badge and Separator, with explicitly fictional example leads.
The private app moved to `/workspace`; auth redirects and mutation revalidation
use this route. A shared L/arrow SVG appears before LeadFlow in page headers;
the favicon contains matching 16/32/48px PNG images. The preset and theme tokens
remain unchanged.

ESLint, generated route types + TypeScript, and the Next.js production build
passed. The production frontend Docker image built with the unchanged lockfile.
Chrome/Playwright exercised the production images on an isolated Compose stack
at port 3002 with disposable PostgreSQL. A QA-only proxy delayed real backend
requests by 1.6 seconds to observe intermediate states; this delay is absent
from application code.

- Public landing CTAs, the getting-started anchor, desktop 1440×1000 and mobile
  390×844, light/dark persistence, no horizontal overflow and unauthenticated
  workspace-to-login redirection passed. Screenshots were inspected.
- Auth, workspace and discussion skeletons appeared while requests were pending
  and disappeared when ready. CSS pulse/spin animation was verified; reduced
  motion disabled both. Signup, login, logout, lead/note saves and status changes
  showed disabled/busy controls and animated spinners.
- A rejected login cleared its spinner, re-enabled submission and retained the
  draft. Lead, discussion and status edits persisted after reload. Browser
  requests stayed on the frontend origin, with no unexpected console, runtime
  or hydration errors. The only expected network error was the rejected login.
- SVG and favicon requests returned 200; the favicon's three image sizes were
  verified. Auth screenshots contain only blank placeholders; test credentials
  were generated in memory and used only in the disposable database.
- The original theme/preset and backend `.env` hashes are unchanged. Public
  files and all three Git histories passed the private-value scan.

The illustration is static example data, not an interactive demo. Pending retry
controls were implemented but their failure/retry branch was not separately
exercised in this pass. This is local production-image evidence for the complete
credential/write flow; production QA uses only public pages and rejected/unauthenticated reads.

Inspected local screenshots: [Landing in light mode](screenshots/landing-light.png),
[Mobile landing in dark mode](screenshots/landing-mobile-dark.png), and
[Sign-in skeleton](screenshots/loading-login.png).

Vercel CI/CD reported deployment `dpl_GaSW4FgDuBCVBwPaGGmkpnx145gH` **READY**
for frontend commit `5533aea496e9cfcaf765a61325a9da72f34bb0d2`.
Chrome then verified the actual custom domain's landing page, account/home links,
getting-started anchor, persisted dark mode, mobile layout, and unauthenticated
`/workspace` redirect to `/login`. The live SVG and favicon bytes matched the
committed assets. Frontend and backend health returned 200; the API reported
`status: ok`. Live screenshots were inspected, browser traffic stayed on the
frontend origin, and no console/runtime/hydration errors appeared. No production
accounts or lead writes were used. All disposable QA containers were removed;
the original three local Compose services remain healthy.

## SEO, themed date picker and responsive filters — 14 October 2026

The owner-provided `screenshot-1791920524884.png` was copied byte-for-byte to
`frontend/public/leadflow-social.png` (3584×1880). The root copy was deleted only
after `cmp` verified equality, at the owner's request. Open Graph/Twitter cards
share that PNG. Canonical, public indexing policy, WebSite/WebApplication JSON-LD,
`/sitemap.xml` and `/robots.txt` use the build-time `APP_URL`. Private/account
routes remain noindex and excluded from crawl files; auth remains enforced.

The shadcn MCP registry search found `date-picker-demo` and supplied its component
add command. Calendar and Popover were installed using the existing Base UI
preset and Remix icons. The implementation uses the documented composition,
plus a time field and timezone-aware `TZDate`. Generated day-button refs were
connected for keyboard focus. Popovers reserve an 8px viewport margin and limit
height to available space. Incomplete datetime selections are rejected before
Temporal converts the displayed zone to UTC.

The horizontal status scroll strip was replaced with mobile/tablet Selects and
wrapping desktop buttons. Both share one filter state through CSS breakpoints.
Header controls, landing actions/headline, lead-card text and loading placeholders
also adapt to narrow widths. Long unbroken company text no longer widens a card.

| Check | Result |
| --- | --- |
| ESLint, Next route types + TypeScript | Passed |
| Frontend unit tests | 13 passed: previous six date/DST cases plus calendar-day preservation, Kolkata UTC conversion and incomplete selections |
| Production build / Linux Docker install | Passed with `npm ci`; unchanged peer-check-compatible Node types; static robots/sitemap generated |
| SEO runtime | Canonical, OG/Twitter tags and image dimensions, JSON-LD, Googlebot-visible head, XML sitemap, robots exclusions, noindex account pages and 404 response passed |
| Calendar behavior | Selection, keyboard day navigation, Escape/focus return, missing-date error with draft retained, real PostgreSQL persistence and no-date note schedule preservation passed |
| Timezone mismatch | A Los Angeles browser selected 24 Oct 2026 at 13:03 in Asia/Kolkata; expected UTC conversion was unit-tested and the persisted UI time survived reload |
| Responsive pages | Landing/login/signup: 320×568, 375×812, 390×844, 768×1024, 1024×768 and 1440×1000; no horizontal page overflow or controls outside the viewport |
| Responsive workspace | Every status option, follow-up/search, long names/company text, add/timeline dialogs, reachable Save Note, retained draft and on-screen calendar at all six widths |
| Breakpoint changes | Qualified status persisted when switching mobile Select → desktop buttons → tablet Select |
| Browser health | No unexpected console, runtime or hydration errors; requests remained on the frontend origin |
| Preservation | Original shadcn theme/preset and backend `.env` hashes unchanged; private environment values absent from public files/history |

Browser plugin was unavailable. Chrome/Playwright exercised production images at
`http://localhost:3002` with a dedicated tmpfs PostgreSQL Compose project. Test
accounts used randomly generated in-memory credentials. No populated credential
screenshots or production account/lead mutations were used. Screenshot evidence
was inspected outside the repositories. These are emulated viewport checks;
physical devices, iOS Safari and third-party social-cache/indexing behavior were
not verified. Backend source did not change; its suite was not rerun for this UI
change. The existing dependency advisory described above remains unchanged.

Vercel CI/CD reported deployment `dpl_21ytdiYjkbCfvSTcCAS4MbDjeCsd` **READY**
for frontend commit `63fdb6c5c0b7502a0a5f7fc48e713c7da10f466e`.
The actual domain passed the metadata/crawler-file checks and the public
landing/login/signup layout checks at all six widths, without console/runtime
or hydration errors. The deployed thumbnail matched the owner's supplied PNG
byte-for-byte. No live account/lead writes were performed. Stable dark-mode
mobile/tablet/desktop workspace screenshots were inspected from the local
production images; transient closing menus were excluded from those captures.
The disposable Compose project/database was removed after verification.

## Fully themed time picker — 14 October 2026

The calendar's companion field still used a native `type="time"` popup. It now
composes the installed shadcn Selects for hour, minute and AM/PM, with FieldSet /
FieldLegend grouping, individual labels, 44px triggers/items and height-limited
scrollable menus. The MCP registry search returned no standalone time-picker
item; no third-party registry, dependency, preset or theme change was introduced.

`lib/time-input.ts` handles 12/24-hour conversion and partial selections. A minute
chosen before an hour is retained. Successful saves reset all display segments;
server validation handles incomplete values. Midnight maps to 00:00, noon to
12:00, and PM hours retain the chosen calendar date in the application timezone.

- ESLint, Next-generated route types + TypeScript, **20 frontend tests** and the
  production build passed. Seven additional cases cover AM/PM boundaries,
  partial selections, round-trips and timezone conversion. Production Docker
  images reached healthy state with the unchanged dependency lockfile.
- Chrome/Playwright exercised real FastAPI/PostgreSQL on an isolated production
  Compose project at port 3002, using a Los Angeles browser timezone and the
  application's Asia/Kolkata zone. Native time/datetime inputs were absent.
- Hour, minute and period menus stayed on screen at 320×568, 375×812, 390×844,
  768×1024, 1024×768 and 1440×1000. Keyboard End selected minute 59, Escape returned
  focus to the trigger, and selections survived viewport changes. Light/dark
  screenshots were inspected outside the public repositories.
- An incomplete follow-up returned inline validation and retained the note.
  Selecting 01:34 PM saved and survived reload. A direct database check confirmed
  `2026-10-24T08:04:00+00:00`, the expected Kolkata-to-UTC instant. A QA-only
  800ms request delay verified that date/hour/minute/period controls disable while
  saving. The delay is outside application code. No unexpected console, runtime
  or hydration errors appeared; browser requests remained on the frontend origin.
- The shadcn theme/preset and backend `.env` hashes remained unchanged. Backend
  code and dependencies did not change. Test credentials existed only in process
  memory and the disposable database; no production accounts or leads were used.

The Browser plugin was unavailable, so regular Chrome/Playwright was used.
Physical devices, iOS Safari and screen-reader behavior were not exercised.

Vercel CI/CD deployment `dpl_6y6M7K6mBAihcGn8W6ufkdRDAgsw` reported **READY**
for frontend commit `8647fbe8032ab60e25b0d9d9e568b4b5add2aa61`.
The private-value source/history scan passed. All disposable time-picker Compose
services and their tmpfs database were removed. Production credential/write
flows were not exercised; the authenticated UI evidence above comes from the
local production images.

## Date/time alignment and expanded responsive review — 14 October 2026

The earlier desktop check verified bounds and interactions but missed the extra
time-label row and mismatched date/time heights. The form now uses one visible
heading per field, screen-reader labels for each time segment, Hour/Minute empty
hints, and aligned 44px controls. Mobile keeps the date/time groups stacked.
The original shadcn preset, global CSS and private backend environment are unchanged.

Chrome/Playwright exercised local production images with real FastAPI/PostgreSQL
in the disposable `leadflow-layout-smoke` Compose project on port 3002:

- Blank, filled and validation-error follow-up forms in both themes at 320×568,
  375×812, 390×844, 640×800, 768×1024, 1024×768, 1366×768, 1440×1000 and 1920×1080.
  Geometry assertions checked identical date/time top positions and heights when
  side by side, stacked mobile groups, viewport bounds and minimum target height.
- Calendar and all three time menus stayed inside each viewport. Escape focus,
  keyboard minute selection, incomplete-draft retention and pending disabled
  states passed. Saving/reloading 01:34 PM persisted the expected PostgreSQL UTC
  instant `2026-10-24T08:04:00+00:00`. Screenshots of mobile, tablet and desktop
  in both themes were inspected outside the repositories.
- Landing/login/sign-up, workspace filters/search, all seven statuses, long lead
  names/company text, add-lead and timeline dialogs also passed those nine widths
  in both themes. Save Note remained reachable by scrolling on short mobile screens.
- ESLint, generated route types/TypeScript, all 20 frontend unit tests and the
  production Docker build passed. No unexpected console/runtime/hydration errors
  appeared; private-flow browser requests stayed on the frontend origin.

The Browser plugin was unavailable, so regular Chrome/Playwright was used. These
are viewport emulations; physical devices, Safari and screen readers were not
verified. Test credentials were generated only in memory and the temporary DB;
no production accounts/leads were created.

Vercel CI/CD deployment `dpl_2aaPQrHBLonPKK7xdomXQ6YMTSHA` reported **READY**
for frontend commit `21465569fd770f58e558bbbb22fb71ea0645a196`. Read-only
landing/login/sign-up checks on the production domain passed all nine widths in
both themes without unexpected console/runtime/hydration errors. Authenticated
form checks were local; production accounts/leads were not modified. The temporary
Compose project and its tmpfs database were removed after verification.

# Verification — 13 October 2026

The application was checked against real PostgreSQL 17 in Docker. Production
images were exercised on a separate local Compose stack with a disposable database;
this is local production-image evidence, not a Render/Vercel/Neon deployment.

| Check | Result |
| --- | --- |
| PostgreSQL integration suite | 25 passed: validation/statuses, literal search, timeline order, atomic rollback, date boundaries, seed idempotency |
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
integration assertions passed. The app is a shared assignment workspace without
end-user login (optional in the brief). The three repositories are published on GitHub; DNS and cloud
deployment remain for the owner. Provider-specific runtime behavior
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

# Accounts and authentication

Open `/signup` (also linked from `/login`) to create an account with a username,
password and confirmation. New accounts sign in immediately to an empty private
workspace. Existing users open `/login` and enter their username/password.
Successful sign-in opens `/workspace`. The public homepage remains available at
`/` and includes account links and a product introduction. The sign-out icon in the header revokes the current session and returns
to the login page. Other accounts cannot list, read or modify your leads or notes.
Passwords are never displayed, prefilled, seeded, logged or included in repository
environment examples. Self-service registration cannot claim legacy data or seed
leads. Usernames are unique regardless of letter case; a duplicate returns a
readable error without changing the existing account.

## Administrator account provisioning

Self-service sign-up is the usual path. Administrators can alternatively leave
Compose running and use another terminal:

```sh
docker compose exec backend uv run leadflow-create-user
```

The command prompts for a username, password and confirmation. Password input
uses `getpass` and does not echo. Do not put passwords into shell arguments, source
files or environment variables. Usernames are normalized to lowercase and accept
3–64 ASCII letters/numbers/dots/underscores/hyphens, starting with a letter/number.
New passwords require 12–128 characters; use a unique generated password.

To add optional sample leads to an existing account:

```sh
docker compose exec backend uv run leadflow-seed
```

Enter the account username. Each account gets its own deterministic sample IDs;
repeat runs preserve edits and avoid duplicates. Production startup never seeds
accounts or leads. For Render, run `uv run leadflow-create-user` in the private
service shell after migrations. Local accounts/data do not automatically copy to Neon.

## Upgrading the previous shared workspace

Migration `0002` preserves all existing leads and discussion history, leaving
legacy lead ownership unset. Those rows are hidden from all accounts until an
administrator explicitly assigns them while creating the intended account:

```sh
docker compose exec backend uv run leadflow-create-user --claim-unowned
```

This claims only unowned leads; another user’s records are never transferred.
Use this once for the owner of the old shared data. For this existing local
checkout, the requested sample account was provisioned privately and the prior
data assigned to it. Its actual credentials exist only in the private handoff,
not in this guide, Git, fixtures, screenshots or configuration.

## Storage and request boundary

- Passwords use pwdlib’s recommended Argon2id settings with a fresh salt per hash.
- Random 256-bit bearer sessions persist as SHA-256 token digests, never plaintext.
- `AUTH_SESSION_HOURS` sets a fixed lifetime (12 by default; range 1–168). Login
  and sign-up clean expired sessions; expiry and account activation are checked on every request.
- Next.js sets an HTTP-only, SameSite=Lax, host-only cookie at path `/`; production
  requires HTTPS through Secure. Browser JavaScript never receives a session token.
- Sign-up/login/logout accept only POST requests from the exact `APP_URL` origin. Match
  scheme, hostname and port to the deployed frontend, including Preview environments.
- Every lead/discussion request requires the private service key and a user session.
  Missing/expired/revoked sessions return 401; other users’ record IDs return 404.
- Five failed attempts per normalized username in 15 minutes trigger a shared
  database-backed limit. Unknown usernames receive the same invalid-credentials
  message and password verification work. Successful login resets the counter.
- `SIGNUP_RATE_LIMIT` bounds registration attempts per source in a 15-minute
  database-backed window (20 by default; range 1–1000). Failed duplicates also
  consume attempts. Next.js hashes Vercel’s protected client-IP header before
  forwarding it through the private service boundary; raw IPs are not stored.
  Outside Vercel, registration uses a shared bucket and ignores caller-supplied
  forwarded headers. Sign-in and registration counters remain separate.
- Account and first session are committed together; failed session creation rolls
  back the account. A database unique constraint handles competing registrations.
  Browser responses contain only `{ ok: true }`; the token stays in the cookie.
- Logout revokes the current session; an unavailable API shows retry feedback
  rather than reporting a successful revocation. Other device sessions stay active.

The backend legacy claim option remains administrator-only. Password recovery,
email verification and multi-factor authentication are outside this flow. There
is no recovery endpoint; keep your chosen credentials securely.

References: [Vercel request headers](https://vercel.com/docs/headers/request-headers#x-vercel-forwarded-for),
[FastAPI password hashing](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/),
[OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html),
[OWASP session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).

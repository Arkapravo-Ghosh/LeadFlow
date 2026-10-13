# Accounts and authentication

Open `/login` and enter your username/password. Successful sign-in opens your
workspace. The sign-out icon in the header revokes the current session and returns
to the login page. Other accounts cannot list, read or modify your leads or notes.
Passwords are never displayed, prefilled, seeded, logged or included in repository
environment examples. There is no public account registration endpoint.

## Create accounts privately

For a new local database, leave Compose running and use another terminal:

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
  cleans expired sessions; expiry and account activation are checked on every request.
- Next.js sets an HTTP-only, SameSite=Lax, host-only cookie at path `/`; production
  requires HTTPS through Secure. Browser JavaScript never receives a session token.
- Login/logout accept only POST requests from the exact `APP_URL` origin. Match
  scheme, hostname and port to the deployed frontend, including Preview environments.
- Every lead/discussion request requires the private service key and a user session.
  Missing/expired/revoked sessions return 401; other users’ record IDs return 404.
- Five failed attempts per normalized username in 15 minutes trigger a shared
  database-backed limit. Unknown usernames receive the same invalid-credentials
  message and password verification work. Successful login resets the counter.
- Logout revokes the current session; an unavailable API shows retry feedback
  rather than reporting a successful revocation. Other device sessions stay active.

The backend account-creation CLI is deliberately administrator-only. Self-service
registration, password recovery and multi-factor authentication are outside the
requested username/password flow.

References: [FastAPI password hashing](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/),
[OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html),
[OWASP session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).

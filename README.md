# LeadFlow

A planned single-screen lead management app for the PravarAI coding assessment.

**Current status: planning only.** The original email and three wireframes have
been saved locally. Application code, dependency setup, and Git initialization
have not started. There are no verified run commands yet.

## Planned features

- Persistent lead creation with optional company and phone.
- Six lead statuses, status filtering, and name search.
- Today's follow-ups pinned; overdue reminders highlighted.
- A dialog with reverse chronological discussion history.
- Discussion notes with optional follow-up date/time.
- Immediate list updates and persisted status changes.
- Synthetic seed data and Docker Compose.

## Planned stack and organization

Next.js, React, TypeScript, FastAPI, SQLAlchemy, Alembic, and SQLite.
One repository with independently runnable frontend/ and backend/ applications.
Small feature modules and reusable UI primitives; follow AGENTS.md.

The email's "FastAI" preference is interpreted as FastAPI.
The brief explicitly permits choosing another stack.

The local detailed plan is in agentdocs/PLAN.md. During implementation, durable
architecture/API notes will live in docs/.

## Setup documentation to complete during implementation

Only add commands after running them successfully.

- Tested runtime versions and prerequisites.
- Repository clone, dependency installation, and environment setup.
- Every variable in root and per-application .env.example files.
- Database migrations and repeatable seed command.
- Native frontend/backend development commands.
- Docker Compose startup, health checks, and persistence behavior.
- Lint, typecheck, build, API tests, and browser verification commands.
- API overview, timezone/follow-up rules, tradeoffs, and known limitations.
- Screenshots or demonstration video.
- AI assistance disclosure and validation evidence.

## Development history

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
Commit focused changes as implementation milestones are actually completed.

## Assessment references

Original correspondence and supplied PNGs are stored in agentdocs/ for local
reference and are excluded from the planned public repository by .gitignore.

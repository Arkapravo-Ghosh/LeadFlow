# LeadFlow development guidance

## Scope and references

This project lives in the LeadFlow checkout.
Read agentdocs/PLAN.md before implementation and agentdocs/email.txt for the
original requirements. The three PNGs in agentdocs/ are suggested wireframes.
Implementation is authorized. Read docs/architecture.md for current decisions.

## Architecture and readability

Use the parent repository with frontend/ and backend/ Git submodules. Keep routes thin, views focused,
business rules in services, database queries in repositories, and date rules in
one dedicated module. Shared UI primitives must not contain feature or API logic.
Avoid circular imports and generic abstraction frameworks.

Target roughly 80-200 lines per hand-written source file. Review splitting above
250 lines; treat 300 as a strong refactoring signal. Generated code and migrations
are exceptions. Split by responsibility, not arbitrary line count. Extract helpers
for real repeated behavior and keep ordinary functions small.

Use strict TypeScript and explicit boundary schemas/types. Add concise
docstrings/JSDoc for exported helpers and non-obvious decisions. Comments explain
why. Update README.md and docs/ alongside behavior changes.

## Domain rules and verification

Persist UTC instants and use a consistent configurable display timezone.
A note without a follow-up preserves the lead's current schedule.
A note with a follow-up updates the note and lead atomically.
Today and overdue can overlap. Apply filters before grouping and avoid duplicates.
Keep drafts, focus, dialogs, and scroll stable during cache updates.

Run checks appropriate to the change. Verify user flows with the real API and
database, not only mocks/builds. Record incomplete runtime validation honestly.
Use synthetic seed/demo data. Keep agentdocs/ local and excluded from public Git.

## Git and delivery

Use Conventional Commits 1.0.0:
https://www.conventionalcommits.org/en/v1.0.0/
Examples: feat(api): add lead creation; fix(web): preserve draft after failed save.
Use meaningful focused commits as milestones are completed; do not backdate or
manufacture history. Document all environment variables and verify README steps.

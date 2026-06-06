# Feature: Jobs

**Package:** `features.jobs`

## Responsibility

Job description creation, listing, and skill storage.

## Models

- `JobDescription` — Title, description text, required skills (JSON), creator

## Views

| URL | View | Auth |
|-----|------|------|
| `/jobs/` | Job list + create form | Required |

## Services

- `create_job(title, description, user)` — Creates job, optionally extracts skills via Gemini (Phase 2)
- `list_jobs(user)` — Returns all jobs

## API

Job matching is handled by `features.analysis` (`POST /api/jobs/match/`).

## Future

- Edit/delete job descriptions
- Skill auto-extraction from description text on save
- Job templates for common roles

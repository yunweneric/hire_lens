# ADR-001: Feature Package Layout

## Status

Accepted

## Context

HireLens has five distinct domains: accounts, resumes, jobs, analysis, and dashboard. We need a folder structure that scales as features grow without creating tangled imports.

## Decision

Use a `features/` package where each domain is a Django app:

```
features/
├── accounts/
├── resumes/
├── jobs/
├── analysis/
└── dashboard/
```

Shared code lives in `core/`. API routes are aggregated in `api/`.

## Consequences

**Positive:**
- Clear ownership per feature
- Easy to navigate and onboard new developers
- Features can be tested in isolation

**Negative:**
- More directories than a flat Django project
- Cross-feature queries require careful import direction

## Rules

1. Features import from `core`, never from each other (except downstream: `analysis` → `resumes`)
2. Each feature has `services/` for business logic
3. Views stay thin; no Gemini calls in views

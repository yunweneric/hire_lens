# ADR-003: Tailwind + HTMX + Alpine Stack

## Status

Accepted

## Context

HireLens needs a modern SaaS dashboard UI without the complexity of a separate SPA (React/Vue). The team wants fast iteration and server-rendered pages.

## Decision

Use **Django Templates** with:

| Tool | Role |
|------|------|
| **TailwindCSS** | Utility-first styling, design tokens |
| **HTMX** | Partial page updates, form submissions without full reload |
| **Alpine.js** | Lightweight interactivity (dark mode, score ring animation) |

## Rationale

- Keeps frontend in Django — one deployment unit
- Tailwind aligns with the documented design system tokens
- HTMX reduces JavaScript boilerplate for upload/forms
- Alpine handles client-only UI state without a build step for JS

## Consequences

**Positive:**
- No separate frontend build pipeline beyond Tailwind CSS
- SEO-friendly server-rendered pages
- Fast prototyping for school project demos

**Negative:**
- Complex client-side state harder than in React
- Tailwind requires npm build step for production CSS

## Build Commands

```bash
npm run build:css    # Production CSS
npm run watch:css    # Development watch mode
```

## Dark Mode

Class-based strategy on `<html>` element, toggled via Alpine.js, persisted in `localStorage`.

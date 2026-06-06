# Design System

HireLens follows a modern SaaS dashboard design language tailored for recruitment workflows.

## Principles

1. **Clarity over decoration** — Data (scores, skills, rankings) is the hero
2. **Consistent density** — Card-based layouts with predictable spacing
3. **Accessible contrast** — WCAG AA minimum for text on surfaces
4. **Dark mode parity** — Every component works in light and dark themes

## Token Categories

| Category | Document |
|----------|----------|
| Colors | [colors.md](colors.md) |
| Typography | [typography.md](typography.md) |
| Spacing & Layout | [spacing-and-layout.md](spacing-and-layout.md) |
| Components | [components.md](components.md) |
| Dark Mode | [dark-mode.md](dark-mode.md) |

## Implementation

Tokens are defined in:

- `tailwind.config.js` — color palette, font family, spacing extensions
- `static/src/input.css` — Tailwind directives + custom utilities
- `templates/components/` — reusable HTML partials

## Font

**Inter** loaded via Google Fonts CDN in `templates/base.html`.

## Related

- [Architecture Overview](../architecture/overview.md)
- [Components Catalog](components.md)

# Typography

## Font Family

| Role | Font | Fallback |
|------|------|----------|
| UI | Inter | system-ui, sans-serif |
| Code / scores | JetBrains Mono | ui-monospace, monospace |

Loaded in `base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Type Scale

| Name | Class | Size | Weight | Usage |
|------|-------|------|--------|-------|
| Display | `text-4xl` | 36px | 700 | Landing hero (future) |
| Page title | `text-2xl` | 24px | 600 | Page headings |
| Section title | `text-lg` | 18px | 500 | Card titles |
| Body | `text-sm` | 14px | 400 | Default text |
| Caption | `text-xs` | 12px | 400 | Labels, timestamps |
| Mono | `text-sm font-mono` | 14px | 400 | ATS scores, API keys |

## Hierarchy Example

```html
<h1 class="text-2xl font-semibold text-content dark:text-content-dark">Dashboard</h1>
<p class="text-sm text-muted dark:text-content-muted-dark">Overview of recruitment activity</p>
```

## Line Height

- Headings: `leading-tight` (1.25)
- Body: `leading-relaxed` (1.625)
- Dense tables: `leading-normal` (1.5)

## Rules

- One `h1` per page (page title in topbar area)
- Card titles use `h2` or `h3` with `text-lg font-medium`
- Avoid font sizes below `text-xs` for accessibility

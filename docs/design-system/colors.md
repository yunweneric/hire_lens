# Colors

## Brand Palette

| Token | Light | Dark | Tailwind Class | Usage |
|-------|-------|------|----------------|-------|
| `primary` | `#2563EB` | `#3B82F6` | `bg-primary`, `text-primary` | CTAs, links, active nav |
| `surface` | `#FFFFFF` | `#0F172A` | `bg-surface` | Page background |
| `surface-raised` | `#F8FAFC` | `#1E293B` | `bg-surface-raised` | Cards, panels |
| `border` | `#E2E8F0` | `#334155` | `border-border` | Dividers, inputs |
| `text-primary` | `#0F172A` | `#F1F5F9` | `text-content` | Headings, body |
| `text-muted` | `#64748B` | `#94A3B8` | `text-muted` | Secondary text, labels |

## Semantic Colors

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `success` | `#16A34A` | `#22C55E` | High ATS scores, matched skills |
| `warning` | `#D97706` | `#F59E0B` | Medium ATS scores |
| `danger` | `#DC2626` | `#EF4444` | Missing skills, errors, alerts |

## ATS Score Bands

| Range | Label | Color Token |
|-------|-------|-------------|
| 80–100 | Excellent Match | `success` |
| 60–79 | Good Match | `primary` |
| 40–59 | Needs Work | `warning` |
| 0–39 | Poor Match | `danger` |

## Tailwind Config

```javascript
colors: {
  primary: { DEFAULT: '#2563EB', dark: '#3B82F6' },
  surface: { DEFAULT: '#FFFFFF', raised: '#F8FAFC', dark: '#0F172A', 'raised-dark': '#1E293B' },
  border: { DEFAULT: '#E2E8F0', dark: '#334155' },
  content: { DEFAULT: '#0F172A', muted: '#64748B', dark: '#F1F5F9', 'muted-dark': '#94A3B8' },
  success: { DEFAULT: '#16A34A', dark: '#22C55E' },
  warning: { DEFAULT: '#D97706', dark: '#F59E0B' },
  danger: { DEFAULT: '#DC2626', dark: '#EF4444' },
}
```

## Usage Guidelines

- Use `surface-raised` for cards on `surface` backgrounds
- Never use raw hex in templates — always use Tailwind token classes
- Skill tags: `bg-success/10 text-success` for matched, `bg-danger/10 text-danger` for missing

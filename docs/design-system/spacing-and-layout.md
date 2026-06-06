# Spacing & Layout

## App Shell

```text
┌──────────┬──────────────────────────────────────┐
│          │  Topbar (h-16)                     │
│ Sidebar  ├──────────────────────────────────────┤
│ (w-64)   │                                      │
│          │  Main content (p-6, overflow-y)    │
│          │                                      │
└──────────┴──────────────────────────────────────┘
```

| Element | Dimensions | Classes |
|---------|------------|---------|
| Sidebar | 256px fixed | `w-64 fixed inset-y-0 left-0` |
| Topbar | 64px height | `h-16` |
| Main | Remaining viewport | `ml-64 pt-16 p-6` |

## Spacing Scale

Use Tailwind's default spacing scale. Project conventions:

| Context | Padding | Gap |
|---------|---------|-----|
| Page content | `p-6` | — |
| Card interior | `p-5` or `p-6` | — |
| Card grid | — | `gap-6` |
| Form fields | `space-y-4` | — |
| Inline elements | — | `gap-2` or `gap-3` |

## Grid Patterns

### Dashboard stat row

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  <!-- stat cards -->
</div>
```

### Two-column content

```html
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
  <!-- left panel -->
  <!-- right panel -->
</div>
```

### Analysis results

```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div class="lg:col-span-1"><!-- score ring --></div>
  <div class="lg:col-span-2"><!-- skills + suggestions --></div>
</div>
```

## Responsive Breakpoints

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| `sm` | 640px | 2-column stat grid |
| `md` | 768px | Sidebar collapses (future) |
| `lg` | 1024px | Full dashboard layout |

## Border Radius

| Element | Class |
|---------|-------|
| Cards | `rounded-xl` |
| Buttons | `rounded-lg` |
| Tags / pills | `rounded-full` |
| Inputs | `rounded-lg` |

## Shadows

| Element | Class |
|---------|-------|
| Cards | `shadow-sm` |
| Dropdowns | `shadow-lg` |
| Modals (future) | `shadow-xl` |

# Dark Mode

HireLens supports light and dark themes using Tailwind's `class` strategy.

## Implementation

### HTML root

```html
<html lang="en" x-data="{ dark: localStorage.getItem('theme') === 'dark' }"
      :class="{ 'dark': dark }">
```

### Toggle (Alpine.js)

```html
<button @click="dark = !dark; localStorage.setItem('theme', dark ? 'dark' : 'light')">
  <!-- sun/moon icon -->
</button>
```

### Tailwind config

```javascript
module.exports = {
  darkMode: 'class',
  // ...
}
```

## Color Mapping

Every surface component uses dual classes:

```html
<div class="bg-surface dark:bg-surface-dark
            text-content dark:text-content-dark
            border-border dark:border-border-dark">
```

## Persistence

- Theme stored in `localStorage` key `theme`
- Values: `light` or `dark`
- Default: `light` (no preference set)
- On page load, Alpine reads `localStorage` and applies `dark` class

## Component Checklist

All components must support dark mode:

- [x] Base layout (`base.html`)
- [x] Sidebar
- [x] Topbar
- [x] Cards
- [x] Stat cards
- [x] Score ring
- [x] Skill tags
- [x] Forms and inputs
- [x] Tables (rankings)

## Avoid

- Hardcoded `bg-white` or `text-black` without dark variant
- Images/icons that disappear on dark backgrounds
- Box shadows that are too harsh in dark mode (use `shadow-sm` only)

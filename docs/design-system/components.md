# Components

Reusable template partials live in `templates/components/`.

## Primitives

### Card (`_card.html`)

Container with raised surface, border, and padding.

```django
{% include "components/_card.html" with title="Title" %}
  <!-- slot content -->
{% endinclude %}
```

### Button (`_button.html`)

| Variant | Usage |
|---------|-------|
| `primary` | Main CTAs |
| `secondary` | Secondary actions |
| `danger` | Destructive actions |
| `ghost` | Toolbar actions |

### Alert (`_alert.html`)

| Variant | Usage |
|---------|-------|
| `success` | Upload success |
| `warning` | Medium ATS warning |
| `danger` | Errors, validation |
| `info` | Neutral information |

## Layout

### Sidebar (`_sidebar.html`)

- Logo + "HireLens" brand
- Navigation links with active state (`bg-primary/10 text-primary`)
- Role-aware items (admin-only links hidden for recruiters)

### Topbar (`_topbar.html`)

- Page title (passed via context)
- Dark mode toggle
- User menu with logout

## Data Display

### Stat Card (`_stat_card.html`)

| Prop | Description |
|------|-------------|
| `label` | Metric name |
| `value` | Numeric or text value |
| `trend` | Optional trend string (e.g. "+12%") |
| `icon` | Optional SVG icon name |

### Score Ring (`_score_ring.html`)

Circular ATS gauge animated with Alpine.js.

| Prop | Description |
|------|-------------|
| `score` | 0–100 integer |
| `label` | e.g. "Excellent Match" |

### Skill Tags (`_skill_tags.html`)

| Prop | Description |
|------|-------------|
| `matched` | List of matched skill strings |
| `missing` | List of missing skill strings |

### Suggestion List (`_suggestion_list.html`)

| Prop | Description |
|------|-------------|
| `suggestions` | List of recommendation strings |

## Forms

### Upload Dropzone (`_upload_dropzone.html`)

HTMX-enabled drag-and-drop area for PDF/DOCX upload.

- Accepts: `.pdf`, `.docx`
- Shows file name on select
- Posts to upload endpoint with `hx-post`

## Component File Index

| File | Purpose |
|------|---------|
| `_card.html` | Card container |
| `_button.html` | Button variants |
| `_alert.html` | Alert banners |
| `_sidebar.html` | App navigation |
| `_topbar.html` | Header bar |
| `_stat_card.html` | Dashboard metrics |
| `_score_ring.html` | ATS score gauge |
| `_skill_tags.html` | Skill pill tags |
| `_suggestion_list.html` | AI recommendations |
| `_upload_dropzone.html` | File upload area |

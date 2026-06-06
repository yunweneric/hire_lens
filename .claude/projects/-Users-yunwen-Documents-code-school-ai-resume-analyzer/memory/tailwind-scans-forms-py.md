---
name: tailwind-scans-forms-py
description: Tailwind content globs must include forms.py or Python-applied widget classes get purged
metadata:
  type: project
---

In this Django project, Tailwind (v3) purges any class string it doesn't find in its `content` globs. Form widget classes (e.g. `job-editor-textarea`, `job-editor-title`) are applied as `attrs={"class": ...}` inside `features/*/forms.py`, NOT in HTML — so they were silently stripped from `static/dist/output.css`, producing missing padding / stray default borders.

**Why:** Tailwind only scanned `*.html` until 2026-06-06.

**How to apply:** `tailwind.config.js` `content` now includes `./features/**/forms.py`. When adding a custom component class used only via a Python widget `class=`, make sure its source file is covered by a content glob, then re-run `npm run build:css`. Verify with `grep -o "\.your-class[^}]*}" static/dist/output.css`.

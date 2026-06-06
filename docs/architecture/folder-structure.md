# Folder Structure

HireLens uses a **feature-based package layout**. Domain logic lives under `features/`; shared, feature-agnostic code lives under `core/`.

## Repository Layout

```text
hirelens/
├── config/                          # Django project settings
├── core/                            # Shared utilities
│   ├── models/                      # Abstract base models
│   ├── permissions/                 # Role checks
│   ├── ai/                          # Gemini client
│   ├── parsers/                     # Resume text extraction
│   ├── middleware/                  # API logging stubs
│   └── exceptions.py
├── features/                        # Domain features (Django apps)
│   ├── accounts/
│   ├── resumes/
│   ├── jobs/
│   ├── analysis/
│   └── dashboard/
├── api/                             # DRF URL aggregation
├── templates/                       # Global layouts + components
├── static/
├── media/
├── docs/
└── manage.py
```

## Feature App Internal Shape

Every feature app follows the same structure:

```text
features/resumes/
├── apps.py
├── models.py
├── admin.py
├── urls.py              # Web routes
├── forms.py
├── views/               # Template views (thin)
│   └── __init__.py
├── services/            # Business logic
│   └── __init__.py
├── api/                 # DRF serializers + views
│   ├── serializers.py
│   └── views.py
└── templates/resumes/   # Feature-scoped templates
```

## Import Rules

| Allowed | Forbidden |
|---------|-----------|
| `features.analysis` → `features.resumes` | `features.resumes` → `features.analysis` |
| Any feature → `core` | `core` → any feature |
| `api` → feature `api/` modules | Feature → `api` |

When two features need the same logic, extract it to `core/`.

## INSTALLED_APPS Registration

```python
INSTALLED_APPS = [
    # ...
    "features.accounts",
    "features.resumes",
    "features.jobs",
    "features.analysis",
    "features.dashboard",
]
```

## Templates

- **Global:** `templates/base.html`, `templates/components/`
- **Feature-scoped:** `features/<name>/templates/<name>/`

Django resolves feature templates via `APP_DIRS = True`.

## Static Assets

- Source CSS: `static/src/input.css`
- Compiled CSS: `static/dist/output.css` (gitignored, built via npm)

## Related Documents

- [ADR-001: Feature Package Layout](decisions/001-feature-package-layout.md)
- [Overview](overview.md)

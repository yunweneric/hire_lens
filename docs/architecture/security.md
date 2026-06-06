# Security

## Authentication

- Django's built-in session authentication
- `LOGIN_URL = "/accounts/login/"`
- `LOGIN_REDIRECT_URL = "/dashboard/"`
- All dashboard and analysis views require `@login_required`

## Authorization (Roles)

| Resource | Admin | Recruiter |
|----------|-------|-----------|
| Upload resume | Yes | Yes |
| Create job | Yes | Yes |
| Run analysis | Yes | Yes |
| View rankings | Yes | Yes |
| Manage users | Yes | No |
| API monitoring | Yes | No |
| Export reports | Yes | No |

Role checks use `core.permissions.roles`:

```python
from core.permissions.roles import IsAdmin, IsRecruiter

@user_passes_test(IsAdmin())
def admin_only_view(request):
    ...
```

## File Upload Security

| Rule | Implementation |
|------|----------------|
| Allowed types | `.pdf`, `.docx` only |
| Max size | 5 MB |
| Storage | `MEDIA_ROOT/resumes/` with UUID filenames |
| Content validation | Extension + MIME type check in form `clean_file` |
| No execution | Files served with `Content-Disposition: attachment` |

## CSRF Protection

- Enabled globally via `CsrfViewMiddleware`
- All POST forms include `{% csrf_token %}`
- HTMX requests send `X-CSRFToken` header from cookie

## Session Security

Production settings (documented in [deployment/production.md](../deployment/production.md)):

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
```

## Environment Secrets

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Django signing |
| `GEMINI_API_KEY` | AI API access |
| `DATABASE_URL` | PostgreSQL connection |

Never commit `.env`. Use `.env.example` as template.

## API Security

- DRF `IsAuthenticated` permission on all endpoints
- Admin-only endpoints use `IsAdmin` permission class
- Request/response logging via `APIUsageLog` (no PII in logs)

## Threat Logging

`features.dashboard` will capture:

- Failed login attempts (via Django signals)
- Gemini API errors
- File upload validation failures

Stored in `APIUsageLog` with `status=error`.

## Related Documents

- [Environment Setup](../setup/environment.md)
- [Production Deployment](../deployment/production.md)

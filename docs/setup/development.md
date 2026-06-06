# Development Workflow

## Daily Commands

### Start Django server

```bash
source venv/bin/activate
python manage.py runserver
```

### Watch Tailwind CSS (separate terminal)

```bash
npm run watch:css
```

### Run migrations after model changes

```bash
python manage.py makemigrations
python manage.py migrate
```

## Project Structure Quick Reference

| Path | Purpose |
|------|---------|
| `features/` | Domain feature apps |
| `core/` | Shared utilities |
| `templates/` | Global templates + components |
| `static/src/` | Tailwind input CSS |
| `docs/` | Documentation |

## Adding a New Feature

1. Create app under `features/<name>/`
2. Add to `INSTALLED_APPS` in `config/settings.py`
3. Create `urls.py` and include in `config/urls.py`
4. Add `services/` for business logic
5. Document in `docs/features/<name>.md`

## Django Admin

Access at http://127.0.0.1:8000/admin/ with superuser credentials.

Registered models: Resume, JobDescription, Analysis, UserProfile, APIUsageLog.

## API Testing

Use curl or Postman against http://127.0.0.1:8000/api/

```bash
# Login first via browser, then:
curl -X GET http://127.0.0.1:8000/api/dashboard/stats/ \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

## Code Style

- Thin views, fat services
- No Gemini calls outside `core.ai`
- Feature imports flow downstream only
- Use `TimestampedModel` for all new models

## Useful Shell Commands

```bash
python manage.py shell

# Create test data
from features.jobs.models import JobDescription
from django.contrib.auth.models import User
user = User.objects.first()
JobDescription.objects.create(title="Python Dev", description="...", created_by=user)
```

## Related

- [Installation](installation.md)
- [Architecture Overview](../architecture/overview.md)

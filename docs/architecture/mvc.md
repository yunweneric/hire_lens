# MVC Architecture

HireLens follows a layered MVC pattern adapted for Django.

## Layers

| Layer | Location | Responsibility |
|-------|----------|----------------|
| **Model** | `features/*/models.py` | Data schema, relationships, computed properties |
| **View (Controller)** | `features/*/views/`, `features/*/api/` | HTTP handling, auth, form validation, delegate to services |
| **View (Presentation)** | `templates/`, `features/*/templates/` | HTML rendering |
| **Service** | `features/*/services/`, `core/services/` | Business logic and database access |

## Base CRUD Service

All services that persist data extend `core.services.BaseCRUDService`:

```python
from core.services import BaseCRUDService

class ResumeService(BaseCRUDService[Resume]):
    model = Resume

    def upload(self, file, user, candidate_name=""):
        # domain logic using self.create(...)
        ...
```

### Provided methods

| Method | Description |
|--------|-------------|
| `get_queryset()` | Base queryset (override for `select_related`) |
| `get_by_id(pk)` | Fetch single record or raise `DoesNotExist` |
| `get_or_none(pk)` | Fetch single record or `None` |
| `list(**filters)` | Filtered queryset |
| `create(**data)` | Insert new record |
| `update(instance, **data)` | Update fields and save |
| `delete(instance)` | Delete record |
| `delete_by_id(pk)` | Delete by primary key |
| `count(**filters)` | Count records |
| `exists(**filters)` | Check existence |

## Service Instances

| Service | Module | Model |
|---------|--------|-------|
| `profile_service` | `features.accounts.services` | `UserProfile` |
| `resume_service` | `features.resumes.services` | `Resume` |
| `job_service` | `features.jobs.services` | `JobDescription` |
| `analysis_service` | `features.analysis.services` | `Analysis` |
| `api_usage_service` | `features.dashboard.services` | `APIUsageLog` |
| `dashboard_service` | `features.dashboard.services` | (read-only aggregation) |

## Controller Pattern

Views must not call `Model.objects` directly. They call services:

```python
# Good (controller)
resumes = resume_service.list_for_user(request.user)

# Avoid (bypasses service layer)
resumes = Resume.objects.filter(uploaded_by=request.user)
```

## Related

- [Folder Structure](folder-structure.md)
- [Data Flow](data-flow.md)

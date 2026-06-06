# Feature: Accounts

**Package:** `features.accounts`

## Responsibility

User authentication, role management, and profile storage.

## Models

- `UserProfile` — OneToOne with Django `User`, stores `role` (`admin` | `recruiter`)

## Views

| URL | View | Auth |
|-----|------|------|
| `/accounts/login/` | Login form | Public |
| `/accounts/logout/` | Logout | Required |

## Services

- `get_user_role(user)` — Returns role string from profile
- `ensure_profile(user, role)` — Creates profile on first login

## Permissions

Uses `core.permissions.roles`:

- `IsAdmin` — Admin-only views
- `IsRecruiter` — Recruiter-accessible views

## Future

- User management CRUD for admins
- Password reset flow
- Team/organization support

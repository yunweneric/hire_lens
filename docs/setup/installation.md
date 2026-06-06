# Installation

## Prerequisites

- Python 3.11+
- Node.js 18+ (for Tailwind CSS build)
- PostgreSQL 14+ (optional; SQLite used as fallback)

## Steps

### 1. Clone and enter project

```bash
git clone https://github.com/yourusername/hirelens.git
cd hirelens
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Node dependencies

```bash
npm install
npm run build:css
```

### 5. Configure environment

```bash
cp .env.example .env
# Edit .env with your values
```

See [Environment Variables](environment.md) for details.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create superuser

```bash
python manage.py createsuperuser
```

After creating the user, assign a role in Django admin or shell:

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from features.accounts.models import UserProfile, Role
>>> user = User.objects.get(username="admin")
>>> UserProfile.objects.create(user=user, role=Role.ADMIN)
```

### 8. Run development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: features` | Ensure you're in project root with venv active |
| CSS not loading | Run `npm run build:css` |
| Database connection error | Check `DATABASE_URL` or remove it to use SQLite |
| Static files 404 in dev | `DEBUG=True` serves static automatically |

## Next Steps

- [Development Workflow](development.md)
- [Environment Variables](environment.md)

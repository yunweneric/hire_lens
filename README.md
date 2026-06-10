# HireLens

> See Beyond the Resume

Admin panel and public job board for posting roles, collecting applications, and AI-powered resume matching via the Gemini API.

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
npm install && npm run build:css
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- **Public job board:** http://127.0.0.1:8000/jobs/
- **Admin panel:** http://127.0.0.1:8000/admin/ (sign in at `/accounts/login/`)

Full setup: **[docs/setup/installation.md](docs/setup/installation.md)**

## How it works

1. **Admin** creates jobs with Markdown descriptions and publishes them.
2. **Candidates** browse open roles and apply with a resume (PDF/DOCX) and contact form.
3. **Admin** reviews applicants per job and runs **Analyze with AI** (Gemini).
4. **Rankings** show who best matches each role, with a highlighted top pick.

## API (authenticated admin)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/applications/<id>/analyze/` | POST | Run AI analysis |
| `/api/jobs/<job_id>/rankings/` | GET | Ranked matches for a job |
| `/api/admin/dashboard/stats/` | GET | Dashboard metrics |

## Deployment

Production runs on Ubuntu behind **Nginx + Gunicorn** with **PostgreSQL** and a Let's Encrypt SSL certificate.

```bash
# On the server, after the initial setup:
cd /app
sudo ./deploy/redeploy.sh
```

[deploy/redeploy.sh](deploy/redeploy.sh) pulls the latest code, installs dependencies, rebuilds the Tailwind CSS, runs migrations, collects static files, and restarts Gunicorn + Nginx. Override defaults with env vars (`APP_DIR`, `SERVICE`, `BRANCH`, `SKIP_GIT=1`, `SKIP_NPM=1`).

> With `DEBUG=False`, the app forces HTTPS, so a valid SSL certificate must be in place before it's reachable. Set production `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in the server `.env`.

Full guide: **[docs/deployment/production.md](docs/deployment/production.md)**

## Documentation

See **[docs/](docs/README.md)** for architecture, data model, and design system.

## Tech Stack

- Django + Django REST Framework
- PostgreSQL (SQLite fallback for dev)
- Tailwind CSS + Alpine.js
- Google Gemini API (`google-generativeai`)

## License

MIT License — Developed by Yunwen Eric

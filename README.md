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

## Documentation

See **[docs/](docs/README.md)** for architecture, data model, and design system.

## Tech Stack

- Django + Django REST Framework
- PostgreSQL (SQLite fallback for dev)
- Tailwind CSS + Alpine.js
- Google Gemini API (`google-generativeai`)

## License

MIT License — Developed by Yunwen Eric

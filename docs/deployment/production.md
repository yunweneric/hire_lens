# Production Deployment

## Recommended Stack

| Component | Technology |
|-----------|------------|
| Web server | Nginx |
| App server | Gunicorn |
| Database | PostgreSQL |
| Static files | Nginx + `collectstatic` |
| Media files | Nginx or S3 |
| Container | Docker (optional) |

## Environment

Set these in production `.env`:

```env
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@db-host:5432/hirelens
GEMINI_API_KEY=<production-key>
```

## Django Production Settings

Add to `config/settings.py` (or `settings/production.py`):

```python
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
```

## Build Steps

```bash
pip install -r requirements.txt
npm install && npm run build:css
python manage.py collectstatic --noinput
python manage.py migrate
```

## Gunicorn

```bash
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120
```

## Nginx Configuration (outline)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Docker (outline)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Hosting Options

| Provider | Notes |
|----------|-------|
| DigitalOcean | App Platform or Droplet + managed PostgreSQL |
| AWS | EC2 + RDS, or Elastic Beanstalk |
| Railway | Simple Django deploy with PostgreSQL addon |
| Render | Web service + PostgreSQL |

## Media Storage

For production, consider storing resume files in S3:

```python
DEFAULT_FILE_STORAGE = "storages.backends.s3b3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = "hirelens-resumes"
```

## Monitoring

- Log Gemini API errors via `APIUsageLog`
- Use Sentry for exception tracking (future)
- Nginx access logs for traffic analysis

## Related

- [Environment Variables](../setup/environment.md)
- [Security](../architecture/security.md)

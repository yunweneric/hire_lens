# Environment Variables

Create a `.env` file in the project root (never commit this file).

## Required Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `django-insecure-...` | Django secret key for signing |
| `DEBUG` | `True` | Enable debug mode (False in production) |
| `GEMINI_API_KEY` | `AIza...` | Google Gemini API key |

## Optional Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://user:pass@localhost/hirelens` | PostgreSQL connection string |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model name override |

## Example `.env`

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (omit to use SQLite for local dev)
DATABASE_URL=postgresql://hirelens:password@localhost:5432/hirelens

# Gemini API
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash
```

## Database Fallback

If `DATABASE_URL` is not set, HireLens uses SQLite (`db.sqlite3`) for local development. This requires no additional setup.

## Obtaining a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. Add it to `.env` as `GEMINI_API_KEY`

## Security Notes

- Never commit `.env` to version control
- Use strong `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Restrict `ALLOWED_HOSTS` to your domain

# Feature: Dashboard

**Package:** `features.dashboard`

## Responsibility

Aggregated analytics, recent activity, API usage monitoring, and admin overview.

## Models

- `APIUsageLog` — Endpoint, tokens, latency, status per request

## Views

| URL | View | Auth |
|-----|------|------|
| `/dashboard/` | Main dashboard | Required |

## Services

- `get_dashboard_stats()` — Total resumes, avg ATS, recent uploads
- `get_recent_analyses(limit)` — Latest analysis records
- `get_api_usage_summary()` — Gemini call stats (admin only)

## Displayed Metrics

| Metric | Source |
|--------|--------|
| Total resumes analyzed | `Resume.objects.count()` |
| Average ATS score | `Analysis.objects.avg(ats_score)` |
| Recent uploads | `Resume` ordered by `-created_at` |
| Top candidates | `Analysis` ordered by `-ats_score` |
| API usage | `APIUsageLog` aggregation |

## API

- `GET /api/dashboard/stats/` — JSON stats for external consumers

## Admin-Only Sections

- API monitoring panel
- Error/threat log viewer
- Usage statistics export

## Future

- Charts (weekly analysis volume)
- Real-time HTMX polling for live stats
- Exportable CSV reports

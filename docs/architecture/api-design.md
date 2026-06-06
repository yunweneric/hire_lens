# API Design

HireLens exposes a REST API via Django REST Framework. All endpoints are prefixed with `/api/`.

## Authentication

- **Session auth** for browser-based requests (CSRF required)
- **Token auth** (future) for external integrations
- All endpoints require authentication except health check

## Response Format

### Success

```json
{
  "data": { },
  "meta": {
    "timestamp": "2026-05-26T12:00:00Z"
  }
}
```

### Error

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Only PDF and DOCX files are allowed.",
    "details": {}
  }
}
```

## Endpoints

### Resume Upload

```http
POST /api/resumes/upload/
Content-Type: multipart/form-data
```

| Field | Type | Required |
|-------|------|----------|
| `file` | file | Yes |
| `candidate_name` | string | No |

**Response:** `201 Created`

```json
{
  "data": {
    "id": 1,
    "candidate_name": "Jane Doe",
    "file_url": "/media/resumes/jane_doe.pdf",
    "created_at": "2026-05-26T12:00:00Z"
  }
}
```

### Resume Analysis

```http
POST /api/resumes/analyze/
Content-Type: application/json
```

| Field | Type | Required |
|-------|------|----------|
| `resume_id` | integer | Yes |
| `job_id` | integer | Yes |

**Response:** `201 Created` with full `Analysis` object.

### Job Matching

```http
POST /api/jobs/match/
Content-Type: application/json
```

| Field | Type | Required |
|-------|------|----------|
| `resume_id` | integer | Yes |
| `job_id` | integer | Yes |

**Response:** `200 OK` with match details (skills, score, suggestions).

### Candidate Rankings

```http
GET /api/candidates/rankings/?job_id=1
```

**Response:** `200 OK`

```json
{
  "data": [
    {
      "rank": 1,
      "resume_id": 3,
      "candidate_name": "Jane Doe",
      "ats_score": 82.0,
      "skill_match_pct": 75.0,
      "ai_confidence": 0.91
    }
  ]
}
```

### Dashboard Stats

```http
GET /api/dashboard/stats/
```

**Response:** `200 OK` with aggregate metrics.

## Versioning

API version prefix (`/api/v1/`) will be added when breaking changes are introduced. Current scaffold uses `/api/` without version.

## Rate Limiting (Future)

- 100 requests/hour per user for analysis endpoints
- Tracked via `APIUsageLog`

## Related Documents

- [Security](security.md)
- [Data Flow](data-flow.md)

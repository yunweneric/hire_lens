# Feature: Analysis

**Package:** `features.analysis`

## Responsibility

ATS scoring, job-resume matching, AI insights, and candidate ranking.

## Models

- `Analysis` — Links resume + job with scores, skills, suggestions, AI summary

## Views

| URL | View | Auth |
|-----|------|------|
| `/analysis/<id>/` | Analysis results | Required |
| `/rankings/` | Candidate rankings table | Required |

## Services

- `run_analysis(resume, job)` — Full pipeline: skills → match → score → suggestions
- `get_rankings(job_id)` — Sorted candidate list by ATS score
- `calculate_ats_score(match_result)` — Weighted score algorithm

## Dependencies

- `core.ai.client.GeminiClient` — All AI operations
- `features.resumes` — Resume data
- `features.jobs` — Job description data

## API

| Endpoint | Method |
|----------|--------|
| `/api/resumes/analyze/` | POST |
| `/api/jobs/match/` | POST |
| `/api/candidates/rankings/` | GET |

## ATS Score Factors

| Factor | Weight |
|--------|--------|
| Keyword / skill match | 40% |
| Semantic similarity | 30% |
| Resume structure | 15% |
| Length appropriateness | 10% |
| Contact info present | 5% |

## Future

- Batch analysis for multiple resumes
- Re-analysis after resume update
- Export analysis as PDF report

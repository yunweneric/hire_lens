# ADR-002: Gemini as AI Provider

## Status

Accepted

## Context

HireLens requires AI for skill extraction, ATS scoring, candidate summaries, and improvement suggestions. We evaluated OpenAI GPT and Google Gemini.

## Decision

Use the **Google Gemini API** via `google-generativeai` Python SDK, wrapped in `core.ai.client.GeminiClient`.

## Rationale

- Project specification mandates Gemini
- Strong structured JSON output for resume parsing
- Competitive pricing for document analysis
- Single API key configuration (`GEMINI_API_KEY`)

## Consequences

**Positive:**
- Centralized AI client in `core/ai/`
- Easy to swap models (e.g., `gemini-2.0-flash` vs Pro)
- Prompt templates co-located in `core/ai/prompts.py`

**Negative:**
- Vendor lock-in to Google; mitigated by abstracting behind `GeminiClient`
- API latency for large resumes; future Celery queue may be needed

## Implementation Notes

- All Gemini calls go through `GeminiClient`, never directly from views
- Log token usage to `APIUsageLog`
- Scaffold phase uses stub responses; real integration in Phase 2

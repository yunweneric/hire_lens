"""Gemini API client for resume–job matching."""
import json
import time

import google.generativeai as genai
from django.conf import settings

from core.ai.prompts import ANALYZE_APPLICATION_PROMPT
from core.exceptions import GeminiAPIError


class GeminiClient:
    """Wrapper around Google Gemini API."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL

    def _ensure_configured(self) -> None:
        if not self.api_key:
            raise GeminiAPIError("GEMINI_API_KEY is not configured.")

    def _get_model(self):
        self._ensure_configured()
        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(self.model_name)

    def analyze_application(self, resume_text: str, job_description: str) -> dict:
        """
        Compare resume against job description. Returns structured match data.
        """
        if not resume_text.strip():
            raise GeminiAPIError("Resume text is empty; cannot analyze.")

        model = self._get_model()
        prompt = ANALYZE_APPLICATION_PROMPT.format(
            resume_text=resume_text[:12000],
            job_description=job_description[:12000],
        )
        start = time.monotonic()
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
        except Exception as exc:
            raise GeminiAPIError(str(exc)) from exc

        latency_ms = int((time.monotonic() - start) * 1000)
        raw = response.text or "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise GeminiAPIError(f"Invalid JSON from model: {raw[:200]}") from exc

        data["_latency_ms"] = latency_ms
        return data

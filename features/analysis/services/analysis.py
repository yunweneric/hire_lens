from core.ai import GeminiClient
from core.exceptions import GeminiAPIError
from core.services import BaseCRUDService
from features.analysis.models import Analysis
from features.dashboard.services.stats import api_usage_service


def calculate_ats_score(match_result: dict) -> float:
    if "ats_score" in match_result and match_result["ats_score"]:
        return round(float(match_result["ats_score"]), 1)
    skill_pct = match_result.get("skill_match_pct", 0)
    confidence = match_result.get("ai_confidence", 0) * 100
    matched = len(match_result.get("matched_skills", []))
    missing = len(match_result.get("missing_skills", []))
    total = matched + missing or 1
    keyword_score = (matched / total) * 100
    return round(0.4 * keyword_score + 0.3 * skill_pct + 0.3 * confidence, 1)


class AnalysisService(BaseCRUDService[Analysis]):
    model = Analysis

    def get_queryset(self):
        return super().get_queryset().select_related(
            "resume", "job", "application"
        )

    def run_analysis_for_application(self, application, user=None) -> Analysis:
        """Run Gemini analysis for an application; create or update Analysis."""
        resume = application.resume
        job = application.job
        if not resume.raw_text.strip():
            raise GeminiAPIError("Resume has no extractable text.")

        client = GeminiClient()
        result = client.analyze_application(resume.raw_text, job.description)
        latency_ms = result.pop("_latency_ms", 0)

        if user:
            api_usage_service.log_request(
                user,
                endpoint="analyze_application",
                latency_ms=latency_ms,
            )

        ats_score = calculate_ats_score(result)
        existing = Analysis.objects.filter(application=application).first()
        payload = {
            "resume": resume,
            "job": job,
            "application": application,
            "ats_score": ats_score,
            "matched_skills": result.get("matched_skills", []),
            "missing_skills": result.get("missing_skills", []),
            "suggestions": result.get("suggestions", []),
            "ai_summary": result.get("ai_summary", ""),
            "skill_match_pct": float(result.get("skill_match_pct", 0)),
            "ai_confidence": float(result.get("ai_confidence", 0)),
            "recommendation": result.get("recommendation", ""),
        }
        if existing:
            for key, value in payload.items():
                setattr(existing, key, value)
            existing.save()
            application.status = application.STATUS_REVIEWED
            application.save(update_fields=["status", "updated_at"])
            return existing

        analysis = self.create(**payload)
        application.status = application.STATUS_REVIEWED
        application.save(update_fields=["status", "updated_at"])
        return analysis

    def run_analysis(self, resume, job, application=None) -> Analysis:
        """Legacy entry point; prefer run_analysis_for_application."""
        if application:
            return self.run_analysis_for_application(application)
        client = GeminiClient()
        result = client.analyze_application(resume.raw_text, job.description)
        ats_score = calculate_ats_score(result)
        return self.create(
            resume=resume,
            job=job,
            ats_score=ats_score,
            matched_skills=result.get("matched_skills", []),
            missing_skills=result.get("missing_skills", []),
            suggestions=result.get("suggestions", []),
            ai_summary=result.get("ai_summary", ""),
            skill_match_pct=float(result.get("skill_match_pct", 0)),
            ai_confidence=float(result.get("ai_confidence", 0)),
            recommendation=result.get("recommendation", ""),
        )

    def get_rankings(self, job_id=None):
        qs = self.get_queryset().order_by("-ats_score")
        if job_id:
            qs = qs.filter(job_id=job_id)
        return qs

    def get_recent(self, limit: int = 5):
        return self.get_queryset().order_by("-created_at")[:limit]


analysis_service = AnalysisService()

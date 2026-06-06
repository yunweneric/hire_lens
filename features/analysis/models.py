from django.db import models

from core.models import TimestampedModel


class Analysis(TimestampedModel):
    application = models.OneToOneField(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="analysis",
        null=True,
        blank=True,
    )
    resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.CASCADE,
        related_name="analyses",
    )
    job = models.ForeignKey(
        "jobs.JobDescription",
        on_delete=models.CASCADE,
        related_name="analyses",
    )
    recommendation = models.CharField(max_length=64, blank=True)
    ats_score = models.FloatField(default=0.0)
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    suggestions = models.JSONField(default=list, blank=True)
    ai_summary = models.TextField(blank=True)
    skill_match_pct = models.FloatField(default=0.0)
    ai_confidence = models.FloatField(default=0.0)

    class Meta:
        ordering = ["-ats_score"]
        verbose_name_plural = "Analyses"

    def __str__(self):
        return f"Analysis: {self.resume} vs {self.job}"

    @property
    def score_label(self) -> str:
        if self.ats_score >= 80:
            return "Excellent Match"
        if self.ats_score >= 60:
            return "Good Match"
        if self.ats_score >= 40:
            return "Needs Work"
        return "Poor Match"

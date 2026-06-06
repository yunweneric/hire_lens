from django.db import models

from core.models import TimestampedModel


class Application(TimestampedModel):
    STATUS_SUBMITTED = "submitted"
    STATUS_REVIEWED = "reviewed"
    STATUS_SHORTLISTED = "shortlisted"
    STATUS_INTERVIEW = "interview"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_SHORTLISTED, "Shortlisted"),
        (STATUS_INTERVIEW, "Interview"),
        (STATUS_REJECTED, "Rejected"),
    ]

    job = models.ForeignKey(
        "jobs.JobDescription",
        on_delete=models.CASCADE,
        related_name="applications",
    )
    resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.CASCADE,
        related_name="applications",
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SUBMITTED,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.job.title}"

    @property
    def has_analysis(self) -> bool:
        from features.analysis.models import Analysis

        return Analysis.objects.filter(application_id=self.pk).exists()

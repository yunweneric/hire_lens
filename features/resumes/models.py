from django.conf import settings
from django.db import models

from core.models import TimestampedModel


class Resume(TimestampedModel):
    file = models.FileField(upload_to="resumes/")
    raw_text = models.TextField(blank=True)
    candidate_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.candidate_name or f"Resume #{self.pk}"

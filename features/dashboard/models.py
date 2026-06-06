from django.conf import settings
from django.db import models

from core.models import TimestampedModel


class APIUsageLog(TimestampedModel):
    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        ERROR = "error", "Error"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="api_logs",
    )
    endpoint = models.CharField(max_length=255)
    tokens_used = models.IntegerField(default=0)
    latency_ms = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUCCESS)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "API Usage Log"

    def __str__(self):
        return f"{self.endpoint} ({self.status})"

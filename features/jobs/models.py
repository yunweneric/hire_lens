from django.conf import settings
from django.db import models
from django.utils.text import slugify

from core.models import TimestampedModel


class JobDescription(TimestampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(
        help_text="Job description in Markdown (README-style)."
    )
    is_published = models.BooleanField(default=False)
    required_skills = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job Description"
        verbose_name_plural = "Job Descriptions"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self) -> str:
        base = slugify(self.title) or "job"
        slug = base
        counter = 1
        while JobDescription.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{counter}"
            counter += 1
        return slug

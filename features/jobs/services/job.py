from django.db.models import Count

from core.services import BaseCRUDService
from features.jobs.models import JobDescription


class JobService(BaseCRUDService[JobDescription]):
    model = JobDescription

    def get_queryset(self):
        return super().get_queryset().select_related("created_by")

    def create_job(
        self,
        title: str,
        description: str,
        user,
        *,
        is_published: bool = False,
    ) -> JobDescription:
        return self.create(
            title=title,
            description=description,
            created_by=user,
            is_published=is_published,
        )

    def update_job(self, job: JobDescription, **kwargs) -> JobDescription:
        for key, value in kwargs.items():
            setattr(job, key, value)
        job.save()
        return job

    def list_all(self):
        return self.get_queryset().annotate(
            application_count=Count("applications")
        )

    def list_published(self):
        return self.get_queryset().filter(is_published=True)

    def get_by_slug(self, slug: str) -> JobDescription:
        return self.get_queryset().get(slug=slug, is_published=True)


job_service = JobService()

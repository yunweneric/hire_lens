from django.db.models import Count, Q

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

    def get_admin_counters(self) -> dict:
        from features.applications.models import Application

        qs = self.model.objects.all()
        total = qs.count()
        published = qs.filter(is_published=True).count()
        return {
            "total": total,
            "published": published,
            "draft": total - published,
            "applicants": Application.objects.count(),
        }

    def list_published(self):
        return self.get_queryset().filter(is_published=True)

    def search_published(self, *, query: str = "", skill: str = ""):
        qs = self.list_published()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if skill:
            # required_skills is a JSON list; SQLite can't do `contains`
            # lookups on it, so match membership in Python.
            ids = [job.pk for job in qs if skill in (job.required_skills or [])]
            qs = qs.filter(pk__in=ids)
        return qs

    def published_skills(self) -> list[str]:
        skills: set[str] = set()
        for job_skills in self.list_published().values_list(
            "required_skills", flat=True
        ):
            skills.update(job_skills or [])
        return sorted(skills)

    def get_by_slug(self, slug: str) -> JobDescription:
        return self.get_queryset().get(slug=slug, is_published=True)


job_service = JobService()

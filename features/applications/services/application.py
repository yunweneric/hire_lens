from django.db import transaction
from django.db.models import Q

from core.parsers import ResumeParser
from core.services import BaseCRUDService
from features.applications.models import Application
from features.jobs.models import JobDescription
from features.resumes.models import Resume


class ApplicationService(BaseCRUDService[Application]):
    model = Application

    def get_queryset(self):
        return super().get_queryset().select_related("job", "resume", "analysis")

    def list_for_job(self, job_id):
        return self.get_queryset().filter(job_id=job_id)

    def list_all(self):
        return self.get_queryset().order_by("-created_at")

    def search(self, *, query="", job_id=None, status="", analysis=""):
        qs = self.list_all()
        if query:
            qs = qs.filter(
                Q(full_name__icontains=query) | Q(email__icontains=query)
            )
        if job_id:
            qs = qs.filter(job_id=job_id)
        if status:
            qs = qs.filter(status=status)
        if analysis == "analyzed":
            qs = qs.filter(analysis__isnull=False)
        elif analysis == "pending":
            qs = qs.filter(analysis__isnull=True)
        return qs

    def set_status(self, application, status: str, *, notify: bool = True):
        valid = {choice for choice, _ in self.model.STATUS_CHOICES}
        if status not in valid:
            raise ValueError(f"Invalid status: {status}")
        if application.status == status:
            return application, False
        application.status = status
        application.save(update_fields=["status", "updated_at"])
        email_sent = False
        if notify:
            from features.applications.services.notifications import send_status_email

            email_sent = send_status_email(application)
        return application, email_sent

    def get_admin_counters(self) -> dict:
        qs = self.model.objects.all()
        total = qs.count()
        analyzed = qs.filter(analysis__isnull=False).count()
        return {
            "total": total,
            "analyzed": analyzed,
            "pending": total - analyzed,
            "reviewed": qs.filter(status=self.model.STATUS_REVIEWED).count(),
        }

    @transaction.atomic
    def submit_application(
        self,
        job: JobDescription,
        *,
        full_name: str,
        email: str,
        phone: str,
        cover_letter: str,
        resume_file,
    ) -> Application:
        parser = ResumeParser()
        raw_text = parser.extract_text(resume_file)
        resume_file.seek(0)
        resume = Resume.objects.create(
            file=resume_file,
            raw_text=raw_text,
            candidate_name=full_name,
            email=email,
        )
        return self.create(
            job=job,
            resume=resume,
            full_name=full_name,
            email=email,
            phone=phone,
            cover_letter=cover_letter,
        )


application_service = ApplicationService()

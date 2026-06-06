from django.db import transaction

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

from core.parsers import ResumeParser
from core.services import BaseCRUDService
from features.resumes.models import Resume


class ResumeService(BaseCRUDService[Resume]):
    model = Resume

    def get_queryset(self):
        return super().get_queryset().select_related("uploaded_by")

    def list_for_user(self, user):
        if user.is_superuser or getattr(getattr(user, "profile", None), "role", None) == "admin":
            return self.get_queryset()
        return self.list(uploaded_by=user)

    def upload(
        self,
        file,
        user=None,
        candidate_name: str = "",
        email: str = "",
    ) -> Resume:
        parser = ResumeParser()
        raw_text = parser.extract_text(file)
        file.seek(0)
        return self.create(
            file=file,
            raw_text=raw_text,
            candidate_name=candidate_name,
            email=email,
            uploaded_by=user,
        )


resume_service = ResumeService()

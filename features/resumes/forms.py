from django import forms
from django.conf import settings

from features.resumes.models import Resume


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["file", "candidate_name"]

    def clean_file(self):
        file = self.cleaned_data["file"]
        ext = "." + file.name.rsplit(".", 1)[-1].lower()
        allowed = [f".{e.lstrip('.')}" for e in settings.ALLOWED_RESUME_EXTENSIONS]
        if ext not in allowed:
            raise forms.ValidationError("Only PDF and DOCX files are allowed.")
        max_bytes = settings.MAX_RESUME_SIZE_MB * 1024 * 1024
        if file.size > max_bytes:
            raise forms.ValidationError(f"Max file size is {settings.MAX_RESUME_SIZE_MB}MB.")
        return file

from django import forms

from features.accounts.forms import INPUT_CLASS
from features.jobs.models import JobDescription
from features.jobs.validators import (
    MAX_DESCRIPTION_LENGTH,
    validate_no_dangerous_html,
)


class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ["title", "description", "is_published"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "job-editor-title",
                    "placeholder": "Job title — e.g. Senior Python Developer",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "job-editor-textarea",
                    "rows": 24,
                    "placeholder": "# Role title\n\n## About the role\n\nWrite the job description in Markdown (README-style).",
                    "data-job-editor": "description",
                }
            ),
            "is_published": forms.CheckboxInput(
                attrs={"class": "size-4 rounded border-input"}
            ),
        }
        labels = {
            "description": "Description (Markdown)",
            "is_published": "Publish on public job board",
        }

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title

    def clean_description(self):
        description = (self.cleaned_data.get("description") or "").strip()
        if not description:
            raise forms.ValidationError("Description cannot be empty.")
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise forms.ValidationError(
                f"Description is too long (maximum {MAX_DESCRIPTION_LENGTH:,} characters)."
            )
        validate_no_dangerous_html(description)
        return description

from django import forms

from features.accounts.forms import INPUT_CLASS
from features.jobs.models import JobDescription


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

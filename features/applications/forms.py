from django import forms
from django.conf import settings

from features.accounts.forms import INPUT_CLASS


class ApplicationForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASS, "placeholder": "Full name", "autocomplete": "name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": INPUT_CLASS, "placeholder": "you@example.com", "autocomplete": "email"}
        ),
    )
    phone = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASS, "placeholder": "Phone (optional)", "autocomplete": "tel"}
        ),
    )
    cover_letter = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "textarea",
                "rows": 4,
                "placeholder": "Cover letter (optional)",
            }
        ),
    )
    resume = forms.FileField(
        widget=forms.FileInput(attrs={"class": "input-file", "accept": ".pdf,.docx"}),
    )

    def clean_resume(self):
        file = self.cleaned_data.get("resume")
        if not file:
            return file
        ext = "." + file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
        allowed = getattr(settings, "ALLOWED_RESUME_EXTENSIONS", [".pdf", ".docx"])
        if ext not in allowed:
            raise forms.ValidationError("Only PDF and DOCX files are allowed.")
        max_mb = getattr(settings, "MAX_RESUME_SIZE_MB", 5)
        if file.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f"File must be under {max_mb} MB.")
        return file

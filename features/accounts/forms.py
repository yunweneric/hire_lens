from django.contrib.auth.forms import AuthenticationForm

INPUT_CLASS = "input"
CHECKBOX_CLASS = "checkbox accent-primary"


class LoginForm(AuthenticationForm):
    """Styled login form for HireLens."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": INPUT_CLASS,
                "placeholder": "name@company.com",
                "autocomplete": "email",
                "id": "id_username",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": INPUT_CLASS,
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
                "id": "id_password",
            }
        )

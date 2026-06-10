import re

from django.core.exceptions import ValidationError

MAX_DESCRIPTION_LENGTH = 50_000

# Tags that can execute scripts, load active content, or hijack the page.
DANGEROUS_TAG_RE = re.compile(
    r"<\s*/?\s*(script|iframe|object|embed|form|style|link|meta|base)\b",
    re.IGNORECASE,
)

# Inline event handlers such as onclick= / onerror= inside a tag.
EVENT_HANDLER_RE = re.compile(r"<[^>]*\bon\w+\s*=", re.IGNORECASE)

# URI schemes that execute code when followed.
DANGEROUS_URI_RE = re.compile(r"javascript\s*:|data\s*:\s*text/html", re.IGNORECASE)


def validate_no_dangerous_html(text: str) -> None:
    """Reject Markdown containing HTML that could execute scripts."""
    match = DANGEROUS_TAG_RE.search(text)
    if match:
        raise ValidationError(
            f"Raw <{match.group(1).lower()}> tags are not allowed in the description."
        )
    if EVENT_HANDLER_RE.search(text):
        raise ValidationError(
            "Inline event handlers (onclick, onerror, …) are not allowed in the description."
        )
    if DANGEROUS_URI_RE.search(text):
        raise ValidationError(
            "javascript: and data:text/html URLs are not allowed in the description."
        )

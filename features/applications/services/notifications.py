"""Candidate email notifications for application status changes."""
from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import send_mail

from features.applications.models import Application

logger = logging.getLogger(__name__)

# Per-status email copy. Statuses not listed here do not trigger an email.
_STATUS_MESSAGES = {
    Application.STATUS_SHORTLISTED: (
        "You've been shortlisted for {job}",
        "Hi {name},\n\n"
        "Good news — your application for \"{job}\" has been shortlisted. "
        "Our team will be in touch with the next steps soon.\n\n"
        "Thank you for your interest,\nThe HireLens Team",
    ),
    Application.STATUS_INTERVIEW: (
        "Interview invitation — {job}",
        "Hi {name},\n\n"
        "We'd like to invite you to interview for \"{job}\". "
        "We'll follow up shortly to arrange a time that works for you.\n\n"
        "Best regards,\nThe HireLens Team",
    ),
    Application.STATUS_REJECTED: (
        "Update on your application — {job}",
        "Hi {name},\n\n"
        "Thank you for applying for \"{job}\" and taking the time to interview with us. "
        "After careful consideration, we won't be moving forward with your application at this time. "
        "We genuinely appreciate your interest and wish you the best in your search.\n\n"
        "Kind regards,\nThe HireLens Team",
    ),
}


def send_status_email(application: Application) -> bool:
    """Send a candidate email for the application's current status.

    Returns True if an email was sent, False otherwise (disabled, no template,
    missing recipient, or a send failure — failures are logged, not raised).
    """
    if not getattr(settings, "SEND_APPLICATION_EMAILS", False):
        return False
    if not application.email:
        return False

    template = _STATUS_MESSAGES.get(application.status)
    if template is None:
        return False

    subject_tpl, body_tpl = template
    context = {"name": application.full_name, "job": application.job.title}
    subject = subject_tpl.format(**context)
    body = body_tpl.format(**context)

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [application.email],
            fail_silently=False,
        )
        return True
    except Exception:  # noqa: BLE001 - never let email failures break the request
        logger.exception("Failed to send status email for application %s", application.pk)
        return False

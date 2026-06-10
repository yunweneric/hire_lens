from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from features.accounts.models import Role
from features.accounts.services import profile_service

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update the default admin user and admin profile."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            default="admin@hirelens.com",
            help="Admin email (also used as the login username).",
        )
        parser.add_argument(
            "--password",
            default="password@123",
            help="Admin password.",
        )

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]

        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if not created:
            user.email = email
            user.is_staff = True
            user.is_superuser = True

        user.set_password(password)
        user.save()

        profile_service.ensure_profile(user, role=Role.ADMIN)

        verb = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{verb} admin user {email}"))

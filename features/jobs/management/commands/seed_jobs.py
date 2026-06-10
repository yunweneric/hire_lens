from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from features.jobs.models import JobDescription
from features.jobs.seed.job_catalog import JOB_CATALOG, build_description

User = get_user_model()


class Command(BaseCommand):
    help = "Seed published job postings with detailed Markdown descriptions."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of jobs to seed from the catalog (default: 20).",
        )
        parser.add_argument(
            "--unpublished",
            action="store_true",
            help="Create jobs as drafts instead of published.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing jobs before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["count"]
        is_published = not options["unpublished"]

        if count < 1:
            self.stderr.write(self.style.ERROR("--count must be at least 1."))
            return

        if count > len(JOB_CATALOG):
            self.stderr.write(
                self.style.ERROR(
                    f"Catalog has {len(JOB_CATALOG)} jobs; requested {count}."
                )
            )
            return

        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if user is None:
            self.stderr.write(
                self.style.ERROR(
                    "No users found. Run ensure_admin or createsuperuser first."
                )
            )
            return

        if options["clear"]:
            deleted, _ = JobDescription.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing jobs."))

        created = 0
        updated = 0

        for spec in JOB_CATALOG[:count]:
            description = build_description(spec)
            job, was_created = JobDescription.objects.update_or_create(
                title=spec["title"],
                defaults={
                    "description": description,
                    "required_skills": spec["skills"],
                    "is_published": is_published,
                    "created_by": user,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {count} jobs ({created} created, {updated} updated)."
            )
        )

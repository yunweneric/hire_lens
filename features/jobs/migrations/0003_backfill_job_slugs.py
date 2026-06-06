from django.db import migrations
from django.utils.text import slugify


def backfill_slugs(apps, schema_editor):
    JobDescription = apps.get_model("jobs", "JobDescription")
    for job in JobDescription.objects.filter(slug=""):
        base = slugify(job.title) or f"job-{job.pk}"
        slug = base
        counter = 1
        while JobDescription.objects.filter(slug=slug).exclude(pk=job.pk).exists():
            slug = f"{base}-{counter}"
            counter += 1
        job.slug = slug
        job.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0002_jobdescription_is_published_jobdescription_slug_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_slugs, migrations.RunPython.noop),
    ]

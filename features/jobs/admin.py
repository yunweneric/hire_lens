from django.contrib import admin

from features.jobs.models import JobDescription


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")

from django.contrib import admin

from features.resumes.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("candidate_name", "uploaded_by", "created_at")
    list_filter = ("created_at",)
    search_fields = ("candidate_name", "uploaded_by__username")
    readonly_fields = ("raw_text", "created_at", "updated_at")

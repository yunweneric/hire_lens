from django.contrib import admin

from features.applications.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "job", "status", "created_at")
    list_filter = ("status", "job")
    search_fields = ("full_name", "email")

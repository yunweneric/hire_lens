from django.contrib import admin

from features.dashboard.models import APIUsageLog


@admin.register(APIUsageLog)
class APIUsageLogAdmin(admin.ModelAdmin):
    list_display = ("endpoint", "user", "status", "tokens_used", "latency_ms", "created_at")
    list_filter = ("status", "created_at")
    readonly_fields = ("created_at", "updated_at")

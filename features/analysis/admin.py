from django.contrib import admin

from features.analysis.models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("resume", "job", "ats_score", "skill_match_pct", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")

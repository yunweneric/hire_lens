from django.urls import path

from features.applications.api import AnalyzeApplicationAPIView, JobRankingsAPIView
from features.dashboard.api.views import AdminDashboardStatsAPIView

urlpatterns = [
    path(
        "applications/<int:pk>/analyze/",
        AnalyzeApplicationAPIView.as_view(),
        name="api-application-analyze",
    ),
    path(
        "jobs/<int:job_id>/rankings/",
        JobRankingsAPIView.as_view(),
        name="api-job-rankings",
    ),
    path(
        "admin/dashboard/stats/",
        AdminDashboardStatsAPIView.as_view(),
        name="api-admin-dashboard-stats",
    ),
]

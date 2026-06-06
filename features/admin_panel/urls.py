from django.urls import path

from features.applications.views import admin as app_admin
from features.dashboard.views import dashboard as dash_views
from features.jobs.views import admin as job_admin

app_name = "admin_panel"

urlpatterns = [
    path("", dash_views.admin_dashboard, name="dashboard"),
    path("jobs/", job_admin.admin_jobs_list, name="jobs_list"),
    path("jobs/new/", job_admin.admin_job_create, name="job_create"),
    path("jobs/preview/", job_admin.admin_job_preview_markdown, name="job_preview"),
    path("jobs/<int:pk>/edit/", job_admin.admin_job_edit, name="job_edit"),
    path("jobs/<int:pk>/publish/", job_admin.admin_job_toggle_publish, name="job_toggle_publish"),
    path("jobs/<int:pk>/delete/", job_admin.admin_job_delete, name="job_delete"),
    path("jobs/<int:job_id>/applicants/", app_admin.admin_job_applicants, name="job_applicants"),
    path("jobs/<int:job_id>/rankings/", app_admin.admin_job_rankings, name="job_rankings"),
    path("applications/<int:pk>/", app_admin.admin_application_detail, name="application_detail"),
    path(
        "applications/<int:pk>/analyze/",
        app_admin.admin_analyze_application,
        name="application_analyze",
    ),
    path(
        "applications/<int:pk>/resume/",
        app_admin.admin_resume_download,
        name="application_resume",
    ),
]

from django.urls import path

from features.jobs.views import public

app_name = "jobs"

urlpatterns = [
    path("", public.public_job_list, name="public_list"),
    path("<slug:slug>/", public.public_job_detail, name="public_detail"),
    path("<slug:slug>/apply/", public.public_apply, name="public_apply"),
    path("<slug:slug>/apply/success/", public.public_apply_success, name="public_apply_success"),
]

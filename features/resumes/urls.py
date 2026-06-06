from django.urls import path

from features.resumes.views import resume_list, resume_upload

app_name = "resumes"

urlpatterns = [
    path("", resume_list, name="list"),
    path("upload/", resume_upload, name="upload"),
]

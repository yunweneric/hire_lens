from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from features.jobs.forms import JobDescriptionForm
from features.jobs.services import job_service


@login_required
def job_list(request):
    if request.method == "POST":
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            job_service.create_job(
                form.cleaned_data["title"],
                form.cleaned_data["description"],
                request.user,
            )
            messages.success(request, "Job description created.")
            return redirect("jobs:list")
    else:
        form = JobDescriptionForm()
    jobs = job_service.list_all()
    return render(
        request,
        "jobs/list.html",
        {"jobs": jobs, "form": form, "page_title": "Job Descriptions"},
    )

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.utils.markdown import render_markdown
from core.utils.pagination import paginate
from features.applications.forms import ApplicationForm
from features.applications.services import application_service
from features.jobs.services import job_service


def public_job_list(request):
    query = request.GET.get("q", "").strip()
    skill = request.GET.get("skill", "").strip()

    jobs = job_service.search_published(query=query, skill=skill)
    page_obj = paginate(request, jobs)
    return render(
        request,
        "jobs/public_list.html",
        {
            "jobs": page_obj,
            "page_obj": page_obj,
            "skills": job_service.published_skills(),
            "filters": {"q": query, "skill": skill},
            "page_title": "Open Positions",
        },
    )


def public_job_detail(request, slug):
    job = get_object_or_404(job_service.get_queryset(), slug=slug, is_published=True)
    return render(
        request,
        "jobs/public_detail.html",
        {
            "job": job,
            "description_html": render_markdown(job.description),
            "page_title": job.title,
        },
    )


@require_http_methods(["GET", "POST"])
def public_apply(request, slug):
    job = get_object_or_404(job_service.get_queryset(), slug=slug, is_published=True)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application_service.submit_application(
                job,
                full_name=form.cleaned_data["full_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data.get("phone", ""),
                cover_letter=form.cleaned_data.get("cover_letter", ""),
                resume_file=form.cleaned_data["resume"],
            )
            return redirect("jobs:public_apply_success", slug=slug)
        messages.error(request, "Please fix the errors below and try again.")
    else:
        form = ApplicationForm()

    return render(
        request,
        "jobs/public_apply.html",
        {"job": job, "form": form, "page_title": f"Apply — {job.title}"},
    )


def public_apply_success(request, slug):
    job = get_object_or_404(job_service.get_queryset(), slug=slug, is_published=True)
    return render(
        request,
        "jobs/public_apply_success.html",
        {"job": job, "page_title": "Application received"},
    )

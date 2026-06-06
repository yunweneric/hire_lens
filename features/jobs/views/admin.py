import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.permissions import admin_required
from core.utils.markdown import render_markdown
from features.jobs.forms import JobDescriptionForm
from features.jobs.services import job_service


@admin_required
def admin_jobs_list(request):
    jobs = job_service.list_all()
    return render(
        request,
        "jobs/admin_list.html",
        {"jobs": jobs, "page_title": "Jobs"},
    )


@admin_required
@require_http_methods(["GET", "POST"])
def admin_job_create(request):
    if request.method == "POST":
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            job_service.create_job(
                form.cleaned_data["title"],
                form.cleaned_data["description"],
                request.user,
                is_published=form.cleaned_data.get("is_published", False),
            )
            messages.success(request, "Job created.")
            return redirect("admin_panel:jobs_list")
        messages.error(request, "Please fix the errors below.")
    else:
        form = JobDescriptionForm()
    return render(
        request,
        "jobs/admin_form.html",
        {"form": form, "page_title": "New job", "is_edit": False},
    )


@admin_required
@require_http_methods(["GET", "POST"])
def admin_job_edit(request, pk):
    job = get_object_or_404(job_service.get_queryset(), pk=pk)
    if request.method == "POST":
        form = JobDescriptionForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated.")
            return redirect("admin_panel:jobs_list")
        messages.error(request, "Please fix the errors below.")
    else:
        form = JobDescriptionForm(instance=job)
    return render(
        request,
        "jobs/admin_form.html",
        {"form": form, "job": job, "page_title": f"Edit — {job.title}", "is_edit": True},
    )


@admin_required
@require_http_methods(["POST"])
def admin_job_preview_markdown(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    markdown_text = payload.get("markdown", "")
    if not isinstance(markdown_text, str):
        return JsonResponse({"error": "markdown must be a string"}, status=400)
    return JsonResponse({"html": render_markdown(markdown_text)})


@admin_required
@require_http_methods(["POST"])
def admin_job_delete(request, pk):
    job = get_object_or_404(job_service.get_queryset(), pk=pk)
    title = job.title
    job_service.delete(job)
    messages.success(request, f'Job "{title}" deleted.')
    return redirect("admin_panel:jobs_list")


@admin_required
@require_http_methods(["POST"])
def admin_job_toggle_publish(request, pk):
    job = get_object_or_404(job_service.get_queryset(), pk=pk)
    job.is_published = not job.is_published
    job.save(update_fields=["is_published", "updated_at"])
    label = "published" if job.is_published else "unpublished"
    messages.success(request, f"Job {label}.")
    return redirect("admin_panel:jobs_list")

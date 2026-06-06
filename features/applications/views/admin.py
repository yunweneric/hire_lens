from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.exceptions import GeminiAPIError
from core.permissions import admin_required
from core.utils.markdown import render_markdown
from features.applications.services import application_service
from features.analysis.services import analysis_service
from features.jobs.services import job_service


@admin_required
def admin_job_applicants(request, job_id):
    job = get_object_or_404(job_service.get_queryset(), pk=job_id)
    applications = application_service.list_for_job(job_id)
    return render(
        request,
        "applications/admin_applicants.html",
        {
            "job": job,
            "applications": applications,
            "page_title": f"Applicants — {job.title}",
        },
    )


@admin_required
def admin_application_detail(request, pk):
    application = get_object_or_404(application_service.get_queryset(), pk=pk)
    analysis = getattr(application, "analysis", None)
    return render(
        request,
        "applications/admin_detail.html",
        {
            "application": application,
            "analysis": analysis,
            "job_description_html": render_markdown(application.job.description),
            "page_title": application.full_name,
        },
    )


@admin_required
@require_http_methods(["POST"])
def admin_analyze_application(request, pk):
    application = get_object_or_404(application_service.get_queryset(), pk=pk)
    try:
        analysis_service.run_analysis_for_application(application, user=request.user)
        messages.success(request, "AI analysis complete.")
    except GeminiAPIError as exc:
        messages.error(request, str(exc))
    except Exception as exc:
        messages.error(request, f"Analysis failed: {exc}")
    return redirect("admin_panel:application_detail", pk=pk)


@admin_required
def admin_job_rankings(request, job_id):
    job = get_object_or_404(job_service.get_queryset(), pk=job_id)
    analyses = list(analysis_service.get_rankings(job_id))
    return render(
        request,
        "applications/admin_rankings.html",
        {
            "job": job,
            "analyses": analyses,
            "page_title": f"Rankings — {job.title}",
        },
    )


@admin_required
def admin_resume_download(request, pk):
    application = get_object_or_404(application_service.get_queryset(), pk=pk)
    resume = application.resume
    if not resume.file:
        raise Http404("Resume file not found.")
    return FileResponse(resume.file.open("rb"), as_attachment=True, filename=resume.file.name)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from features.resumes.forms import ResumeUploadForm
from features.resumes.services import resume_service


@login_required
def resume_list(request):
    resumes = resume_service.list_for_user(request.user)
    return render(
        request,
        "resumes/list.html",
        {"resumes": resumes, "page_title": "Resumes"},
    )


@login_required
def resume_upload(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_service.upload(
                form.cleaned_data["file"],
                request.user,
                form.cleaned_data.get("candidate_name", ""),
            )
            messages.success(request, "Resume uploaded successfully.")
            return redirect("resumes:list")
    else:
        form = ResumeUploadForm()
    return render(
        request,
        "resumes/upload.html",
        {"form": form, "page_title": "Upload Resume"},
    )

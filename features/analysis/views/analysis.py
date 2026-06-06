from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from features.analysis.services import analysis_service


@login_required
def analysis_detail(request, pk):
    analysis = analysis_service.get_or_none(pk)
    if analysis:
        context = {
            "analysis": analysis,
            "ats_score": int(analysis.ats_score),
            "score_label": analysis.score_label,
            "matched_skills": analysis.matched_skills,
            "missing_skills": analysis.missing_skills,
            "suggestions": analysis.suggestions,
            "ai_summary": analysis.ai_summary,
            "candidate_name": analysis.resume.candidate_name or str(analysis.resume),
            "job_title": analysis.job.title,
            "page_title": "Analysis Results",
        }
    else:
        mock = analysis_service.get_mock_analysis()
        context = {"analysis": None, "page_title": "Analysis Results", **mock}
    return render(request, "analysis/detail.html", context)


@login_required
def rankings_list(request):
    job_id = request.GET.get("job_id")
    analyses = analysis_service.get_rankings(job_id)
    if not analyses.exists():
        analyses = _mock_rankings()
    return render(
        request,
        "analysis/rankings.html",
        {"analyses": analyses, "page_title": "Candidate Rankings"},
    )


def _mock_rankings():
    return [
        {
            "rank": 1,
            "candidate_name": "Jane Doe",
            "job_title": "Senior Python Developer",
            "ats_score": 82,
            "skill_match_pct": 75,
            "ai_confidence": 0.91,
        },
        {
            "rank": 2,
            "candidate_name": "John Smith",
            "job_title": "Senior Python Developer",
            "ats_score": 71,
            "skill_match_pct": 62,
            "ai_confidence": 0.84,
        },
        {
            "rank": 3,
            "candidate_name": "Alice Johnson",
            "job_title": "Senior Python Developer",
            "ats_score": 58,
            "skill_match_pct": 50,
            "ai_confidence": 0.76,
        },
    ]

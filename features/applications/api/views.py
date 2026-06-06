from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import GeminiAPIError
from core.permissions import user_is_admin
from features.analysis.api.serializers import AnalysisSerializer
from features.analysis.services import analysis_service
from features.applications.services import application_service
from features.jobs.services import job_service


class AnalyzeApplicationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not user_is_admin(request.user):
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Admin access required."}},
                status=status.HTTP_403_FORBIDDEN,
            )
        application = application_service.get_by_id(pk)
        try:
            analysis = analysis_service.run_analysis_for_application(
                application, user=request.user
            )
        except GeminiAPIError as exc:
            return Response(
                {"error": {"code": "AI_ERROR", "message": str(exc)}},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response(
            {"data": AnalysisSerializer(analysis).data},
            status=status.HTTP_201_CREATED,
        )


class JobRankingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        job = job_service.get_by_id(job_id)
        analyses = analysis_service.get_rankings(job_id)
        data = [
            {
                "rank": idx + 1,
                "application_id": a.application_id,
                "candidate_name": (
                    a.application.full_name
                    if a.application_id
                    else (a.resume.candidate_name or str(a.resume))
                ),
                "job_title": job.title,
                "ats_score": a.ats_score,
                "recommendation": a.recommendation,
                "skill_match_pct": a.skill_match_pct,
                "ai_confidence": a.ai_confidence,
                "is_best_match": idx == 0,
            }
            for idx, a in enumerate(analyses)
        ]
        return Response({"data": data})

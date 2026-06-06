from rest_framework import serializers

from features.analysis.models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source="resume.candidate_name", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = Analysis
        fields = [
            "id",
            "application",
            "resume",
            "job",
            "candidate_name",
            "job_title",
            "ats_score",
            "recommendation",
            "matched_skills",
            "missing_skills",
            "suggestions",
            "ai_summary",
            "skill_match_pct",
            "ai_confidence",
            "created_at",
        ]


class AnalyzeRequestSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    job_id = serializers.IntegerField()

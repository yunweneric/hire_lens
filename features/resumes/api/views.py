from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from features.resumes.api.serializers import ResumeSerializer
from features.resumes.forms import ResumeUploadForm
from features.resumes.services import resume_service


class ResumeUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        form = ResumeUploadForm(request.data, request.FILES)
        if not form.is_valid():
            return Response(
                {"error": {"code": "VALIDATION_ERROR", "message": str(form.errors)}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        resume = resume_service.upload(
            form.cleaned_data["file"],
            request.user,
            form.cleaned_data.get("candidate_name", ""),
        )
        serializer = ResumeSerializer(resume, context={"request": request})
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

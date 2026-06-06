from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import user_is_admin
from features.dashboard.services import dashboard_service


class AdminDashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not user_is_admin(request.user):
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Admin access required."}},
                status=403,
            )
        return Response({"data": dashboard_service.get_admin_stats()})

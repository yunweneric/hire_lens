from django.shortcuts import render

from core.permissions import admin_required
from features.dashboard.services import dashboard_service


@admin_required
def admin_dashboard(request):
    stats = dashboard_service.get_admin_stats()
    trends = dashboard_service.get_section_card_trends()
    chart = dashboard_service.get_application_chart(months=6)
    recent_applications = dashboard_service.get_recent_applications(limit=10)
    return render(
        request,
        "dashboard/admin_index.html",
        {
            "stats": stats,
            "trends": trends,
            "chart_points": chart["chart_points"],
            "chart_svg": chart["chart_svg"],
            "chart_total": chart["total_in_period"],
            "recent_applications": recent_applications,
            "page_title": "Dashboard",
        },
    )

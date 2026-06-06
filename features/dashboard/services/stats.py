from datetime import timedelta

from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from core.services import BaseCRUDService
from features.analysis.models import Analysis
from features.applications.models import Application
from features.dashboard.models import APIUsageLog
from features.jobs.models import JobDescription


class APIUsageLogService(BaseCRUDService[APIUsageLog]):
    model = APIUsageLog

    def log_request(self, user, endpoint: str, tokens_used: int = 0, latency_ms: int = 0, status: str = "success"):
        return self.create(
            user=user,
            endpoint=endpoint,
            tokens_used=tokens_used,
            latency_ms=latency_ms,
            status=status,
        )


api_usage_service = APIUsageLogService()


class DashboardService:
    """Read-only aggregation service for dashboard metrics."""

    def get_admin_stats(self) -> dict:
        published_jobs = JobDescription.objects.filter(is_published=True).count()
        total_jobs = JobDescription.objects.count()
        total_applications = Application.objects.count()
        pending_analysis = Application.objects.filter(analysis__isnull=True).count()
        analysis_agg = Analysis.objects.aggregate(
            count=Count("id"),
            avg_score=Avg("ats_score"),
        )
        return {
            "published_jobs": published_jobs,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "pending_analysis": pending_analysis,
            "total_analyses": analysis_agg["count"] or 0,
            "avg_ats_score": round(analysis_agg["avg_score"] or 0, 1),
            "api_calls": api_usage_service.count(),
        }

    def get_section_card_trends(self) -> dict:
        """Simple month-over-month trend labels for section cards."""
        now = timezone.now()
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = this_month_start - timedelta(seconds=1)
        last_month_start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        def trend_for(model_qs):
            current = model_qs.filter(created_at__gte=this_month_start).count()
            previous = model_qs.filter(
                created_at__gte=last_month_start, created_at__lt=this_month_start
            ).count()
            if previous == 0:
                if current > 0:
                    return {"direction": "up", "percent": 100}
                return {"direction": "neutral", "percent": 0}
            change = round(((current - previous) / previous) * 100)
            if change > 0:
                return {"direction": "up", "percent": abs(change)}
            if change < 0:
                return {"direction": "down", "percent": abs(change)}
            return {"direction": "neutral", "percent": 0}

        return {
            "applications": trend_for(Application.objects),
            "analyses": trend_for(Analysis.objects),
            "jobs": trend_for(JobDescription.objects),
        }

    def get_application_chart(self, months: int = 6) -> dict:
        now = timezone.now()
        month_starts = []
        cursor = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        for _ in range(months):
            month_starts.append(cursor)
            cursor = (cursor - timedelta(days=1)).replace(day=1)
        month_starts = list(reversed(month_starts))

        qs = (
            Application.objects.filter(created_at__gte=month_starts[0])
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
        )
        counts_by_month = {row["month"]: row["count"] for row in qs}
        counts = [counts_by_month.get(m, 0) for m in month_starts]
        max_count = max(counts) or 1
        min_px = 8
        max_px = 140

        points = [
            {
                "label": m.strftime("%b"),
                "count": c,
                "height_px": round(min_px + ((c / max_count) * (max_px - min_px))),
            }
            for m, c in zip(month_starts, counts)
        ]
        return {
            "chart_points": points,
            "total_in_period": sum(counts),
            "chart_svg": self._build_area_chart_svg(points),
        }

    def _build_area_chart_svg(self, points: list) -> str:
        if not points:
            return ""
        width, height = 400, 160
        n = len(points)
        step = width / max(n - 1, 1)
        coords = []
        for i, p in enumerate(points):
            x = round(i * step, 1)
            y = round(height - (p["height_px"] * height / 140), 1)
            coords.append((x, y))
        line = " ".join(f"{x},{y}" for x, y in coords)
        area = f"M 0,{height} " + " ".join(f"L {x},{y}" for x, y in coords) + f" L {width},{height} Z"
        return (
            f'<svg viewBox="0 0 {width} {height}" preserveAspectRatio="none" '
            f'style="display:block;width:100%;height:100%" aria-hidden="true">'
            f'<defs><linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="hsl(var(--primary))" stop-opacity="0.25"/>'
            f'<stop offset="100%" stop-color="hsl(var(--primary))" stop-opacity="0"/>'
            f'</linearGradient></defs>'
            f'<path d="{area}" fill="url(#areaFill)" stroke="none"/>'
            f'<polyline points="{line}" fill="none" stroke="hsl(var(--primary))" '
            f'vector-effect="non-scaling-stroke" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'</svg>'
        )

    def get_recent_applications(self, limit: int = 10) -> list:
        return list(
            Application.objects.select_related("job", "analysis")
            .order_by("-created_at")[:limit]
        )

    def get_recent_jobs(self, limit: int = 10) -> list:
        return list(
            JobDescription.objects.annotate(application_count=Count("applications"))
            .order_by("-created_at")[:limit]
        )


dashboard_service = DashboardService()

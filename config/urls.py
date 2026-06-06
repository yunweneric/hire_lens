"""
URL configuration for HireLens project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="jobs:public_list", permanent=False)),
    path("jobs/", include("features.jobs.urls")),
    path("accounts/", include("features.accounts.urls")),
    path("admin/", include("features.admin_panel.urls")),
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

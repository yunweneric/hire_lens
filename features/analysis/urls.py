from django.urls import path

from features.analysis.views import analysis_detail

app_name = "analysis"

urlpatterns = [
    path("<int:pk>/", analysis_detail, name="detail"),
]

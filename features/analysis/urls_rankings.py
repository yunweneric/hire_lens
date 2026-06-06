from django.urls import path

from features.analysis.views import rankings_list

urlpatterns = [
    path("", rankings_list, name="rankings"),
]

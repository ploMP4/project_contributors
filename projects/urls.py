from django.urls import path

from .views import CreateProjectView

urlpatterns = [
    path("", CreateProjectView.as_view(), name="project_create"),
]

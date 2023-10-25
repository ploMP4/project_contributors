from django.urls import path

from .views import CreateProjectView, RetrieveUpdateDeleteProjectView

urlpatterns = [
    path("", CreateProjectView.as_view(), name="project_create"),
    path(
        "<int:pk>/",
        RetrieveUpdateDeleteProjectView.as_view(),
        name="project_get_update_delete",
    ),
]

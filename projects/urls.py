from django.urls import path

from .views import (
    ListCreateApplicationView,
    ListCreateProjectView,
    RetrieveUpdateDeleteApplicationView,
    RetrieveUpdateDeleteProjectView,
)

urlpatterns = [
    path("", ListCreateProjectView.as_view(), name="project_list_create"),
    path(
        "<int:pk>/",
        RetrieveUpdateDeleteProjectView.as_view(),
        name="project_get_update_delete",
    ),
    path(
        "application/",
        ListCreateApplicationView.as_view(),
        name="application_list_create",
    ),
    path(
        "application/<int:pk>/",
        RetrieveUpdateDeleteApplicationView.as_view(),
        name="application_retrieve_update_delete",
    ),
]

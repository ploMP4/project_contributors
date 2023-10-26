from django.db.models import F, Count
from django.db.models.query import Prefetch
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Project, Application
from .serializers import ApplicationSerializer, ProjectSerializer


class ListCreateProjectView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = (
            Project.objects.prefetch_related(Prefetch("collaborators"))
            .annotate(Count("collaborators"))
            .filter(collaborators__count__lt=F("maximum_collaborators"))
        )

        return queryset


class RetrieveUpdateDeleteProjectView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(id=self.kwargs["pk"])
        return queryset


class ListCreateApplicationView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        queryset = Application.objects.filter(project__owner=self.request.user)

        return queryset

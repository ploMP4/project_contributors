from django.db.models import F, Q, Count
from django.db.models.query import Prefetch
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import Response

from .models import Project, Application
from .serializers import ApplicationSerializer, ProjectSerializer


class ListCreateProjectView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """
        Return to the user only the projects that have open seats
        """
        return (
            Project.objects.prefetch_related(Prefetch("collaborators"))
            .annotate(Count("collaborators"))
            .filter(collaborators__count__lt=F("maximum_collaborators"))
        )


class RetrieveUpdateDeleteProjectView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Overwrite queryset so anyone can retrieve a project not just the project owner
        """
        self.get_queryset = lambda: Project.objects.filter(id=kwargs["pk"])
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs["pk"], owner=self.request.user)


class ListCreateApplicationView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        """
        A user can only see applications made by him or applications that
        are for a project he owns
        """
        return Application.objects.filter(
            Q(project__owner=self.request.user) | Q(user=self.request.user)
        )


class RetrieveUpdateDeleteApplicationView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        """
        A user can only see/delete applications made by him or applications that
        are for a project he owns
        """
        return Application.objects.filter(
            Q(id=self.kwargs["pk"]),
            Q(project__owner=self.request.user) | Q(user=self.request.user),
        )

    def put(self, request, pk):
        """
        Overwrite put method implementation of the generic APIView to not allow it,
        because we only want to modify the application's status and no other field.
        """
        return Response(
            "Method not allowed",
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

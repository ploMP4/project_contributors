from django.db.models import F, Q, Count
from django.db.models.query import Prefetch
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Project, Application
from .serializers import ApplicationSerializer, ProjectSerializer


class ListCreateProjectView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """
        Return to the user only the projects that have open seats
        """
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
        """
        A user can only see applications made by him or applications that
        are for a project he owns
        """
        queryset = Application.objects.filter(
            Q(project__owner=self.request.user) | Q(user=self.request.user)
        )
        return queryset


class RetrieveUpdateDeleteApplicationView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        """
        A user can only see/modify applications made by him or applications that
        are for a project he owns
        """
        queryset = Application.objects.filter(
            Q(id=self.kwargs["pk"]),
            Q(project__owner=self.request.user) | Q(user=self.request.user),
        )
        return queryset

    def put(self, request, *args, **kwargs):
        """
        Overwrite put method implementation of the generic APIView to not allow it,
        because we only want to modify the application's status and no other field.
        """
        return Response(
            {"message": "Method is not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

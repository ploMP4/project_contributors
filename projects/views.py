from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Project
from .serializers import ProjectSerializer


class CreateProjectView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer


class RetrieveUpdateDeleteProjectView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(id=self.kwargs["pk"], owner=self.request.user)
        return queryset

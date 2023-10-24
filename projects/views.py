from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import ProjectSerializer


class CreateProjectView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

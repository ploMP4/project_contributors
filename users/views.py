from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework import permissions

from users.models import Skill

from .serializers import SkillSerializer, UserSerializerWithToken


class RegisterUserView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializerWithToken


class CreateSkillView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillSerializer


class DeleteSkillView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillSerializer

    def get_queryset(self):
        queryset = Skill.objects.filter(id=self.kwargs["pk"], user=self.request.user)
        return queryset

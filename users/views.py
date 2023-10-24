from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from .serializers import SkillSerializer, UserSerializerWithToken


class RegisterUserView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializerWithToken


class SkillView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillSerializer

from django.db.models import Count, ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from project_contributors import settings

from .models import Skill, User
from .serializers import (
    SkillSerializer,
    UserSerializerWithStats,
    UserSerializerWithToken,
)


class RetrieveUserWithStatsView(RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializerWithStats

    def get_queryset(self):
        queryset = (
            User.objects.filter(id=self.kwargs["pk"])
            .annotate(projects_created=Count("project"))
            .annotate(projects_contributed=Count("collaborator_set"))
        )
        return queryset


class RegisterUserView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializerWithToken


class CreateSkillView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillSerializer


class DeleteSkillView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Skill.objects.filter(id=self.kwargs["pk"], user=self.request.user)
        return queryset

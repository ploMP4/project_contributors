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


class RequestPasswordResetUserView(APIView):
    def post(self, request):
        """
        Send an email to the user containing a url with a PasswordResetToken
        to send a patch request to with the new password
        """
        try:
            user = User.objects.get(email=request.data.get("email"))
            token = PasswordResetTokenGenerator().make_token(user)

            reset_url_args = {"pk": user.id, "token": token}
            reset_path = reverse("password_reset_confirm", kwargs=reset_url_args)

            user.email_user(
                subject="Project Contributors Password Reset",
                message=f"Send a patch request to the following url: {reset_path}",
                from_email=settings.EMAIL_HOST_USER,
            )

            return Response(
                {"message": f"Email has been sent to {user.email}"},
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist:
            return Response(
                {"message": "There is no user with the provided email address"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResetPasswordUserView(APIView):
    def patch(self, request, pk, token):
        """
        Validate the PasswordResetToken and set the new password
        provided by the user
        """
        try:
            user = User.objects.get(id=pk)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("token is not valid")

            user.set_password(request.data.get("password"))
            user.clean()
            user.save()

            return Response(
                {"message": "Password reset successfully"},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response(
                {"message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateSkillView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillSerializer


class DeleteSkillView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillSerializer

    def get_queryset(self):
        queryset = Skill.objects.filter(id=self.kwargs["pk"], user=self.request.user)
        return queryset

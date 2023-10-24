from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework import permissions

from .models import Skill, User
from .serializers import SkillSerializer, UserSerializerWithToken


class RegisterUserView(APIView):
    def post(self, request) -> Response:
        data = request.data

        user = User(
            username=data.get("username"),
            password=make_password(data.get("password")),
            email=data.get("email"),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            age=data.get("age", None),
            country=data.get("country", ""),
            residence=data.get("residence", ""),
        )

        try:
            user.full_clean()
            user.save(force_insert=True)

            serializer = UserSerializerWithToken(user, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )


class SkillView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request) -> Response:
        user = request.user
        if len(user.skill_set.all()) >= 3:
            return Response(
                {"message": "User cannot have more than 3 skills"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data
        skill = Skill(
            user=user,
            language=data["language"],
            level=data["level"],
        )

        try:
            skill.full_clean()
            skill.save()

            serializer = SkillSerializer(skill, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)

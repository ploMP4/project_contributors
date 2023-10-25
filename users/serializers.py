from typing import Any, Dict
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Skill, User


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "age",
            "country",
            "residence",
            "token",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_token(self, obj: User) -> Dict[str, str]:
        refresh = RefreshToken.for_user(obj)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create(self, validated_data: Dict[Any, Any]) -> User:
        user = User.objects.create(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            age=validated_data.get("age", None),
            country=validated_data.get("country", ""),
            residence=validated_data.get("residence", ""),
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class SkillSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        if len(data["user"].skill_set.all()) >= 3:
            raise ValidationError("User cannot have more than 3 skills")

        return data

    class Meta:
        model = Skill
        fields = "__all__"
        extra_kwargs = {"user": {"write_only": True}}
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Skill.objects.all(), fields=["language", "user"]
            )
        ]

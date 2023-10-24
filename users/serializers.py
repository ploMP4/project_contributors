from typing import Dict
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
            "first_name",
            "last_name",
            "age",
            "country",
            "residence",
            "token",
        ]

    def get_token(self, obj: User) -> Dict[str, str]:
        refresh = RefreshToken.for_user(obj)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

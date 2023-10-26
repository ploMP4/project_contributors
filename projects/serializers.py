from typing import Any, Dict
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Application, Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Project.objects.all(), fields=["owner", "name"]
            )
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        if data["project"].owner == data["user"]:
            raise ValidationError("User cannot apply to his own project")

        return data

    class Meta:
        model = Application
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Application.objects.all(), fields=["project", "user"]
            )
        ]

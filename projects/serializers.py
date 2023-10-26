from typing import Any, Dict
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Application, Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        collaborators = instance.collaborators.values("username")
        creator = instance.owner.username
        data = super().to_representation(instance)
        data["collaborators"] = collaborators
        data["creator"] = creator
        return data

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

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "project_id": instance.project.id,
            "project_name": instance.project.name,
            "username": instance.user.username,
            "email": instance.user.email,
            "skills": instance.user.skill_set.values("language", "level"),
        }
        return data

    class Meta:
        model = Application
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Application.objects.all(), fields=["project", "user"]
            )
        ]

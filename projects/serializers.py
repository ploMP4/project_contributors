from typing import Any, Dict
from rest_framework import serializers

from .models import Application, ApplicationStatus, Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        if (
            validated_data.get("collaborators")
            and instance.owner in validated_data["collaborators"]
        ):
            raise serializers.ValidationError(
                "User cannot be a collaborator on his own project"
            )

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Display the usernames of the project's creator and collaborators
        instead of their id's.
        """
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
        if data.get("project") and data.get("user"):
            if data["project"].owner == data["user"]:
                raise serializers.ValidationError(
                    "User cannot apply to his own project"
                )

            if data["user"] in data["project"].collaborators.all():
                raise serializers.ValidationError(
                    "User cannot apply to a project he is already a collaborator at"
                )

        return data

    def create(self, validated_data):
        validated_data["status"] = ApplicationStatus.PENDING
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.user == self.context["request"].user:
            raise serializers.ValidationError(
                "User cannot modify his own application status"
            )

        if validated_data.get("project") or validated_data.get("user"):
            raise serializers.ValidationError("Only status field is editable")

        collaborator_count = len(instance.project.collaborators.all())
        if collaborator_count >= instance.project.maximum_collaborators:
            raise serializers.ValidationError("Cannot exceed maximum_collaborators")

        if validated_data["status"] == ApplicationStatus.ACCEPTED:
            instance.project.collaborators.add(instance.user)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "status": instance.status,
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

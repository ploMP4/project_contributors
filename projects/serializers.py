from rest_framework import serializers

from .models import Project


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

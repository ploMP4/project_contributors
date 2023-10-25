from django.db import models
from users.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(
        User, related_name="collaborator_set", blank=True
    )

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    maximum_collaborators = models.IntegerField(default=5)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="unique name"),
        ]


class Application(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"], name="unique application"
            ),
        ]

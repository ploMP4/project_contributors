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

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="unique name"),
        ]

from django.db import models
from users.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name="collaborator_set")

    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    maximum_collaborators = models.IntegerField()

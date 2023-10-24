from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.IntegerField(null=True)
    country = models.CharField(max_length=255, null=True)
    residence = models.CharField(max_length=255, null=True)


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=255, null=True)
    level = models.CharField(max_length=255, null=True)

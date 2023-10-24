from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    residence = models.CharField(max_length=255, null=True, blank=True)


class Skill(models.Model):
    class Language(models.TextChoices):
        CPP = "C++"
        JAVASCRIPT = "javascript"
        PYTHON = "python"
        JAVA = "java"
        LUA = "lua"
        RUST = "rust"
        GO = "go"
        JULIA = "julia"

    class Level(models.TextChoices):
        BEGINNER = "beginner"
        EXPERIENCED = "experienced"
        EXPERT = "expert"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(
        max_length=255, choices=Language.choices, default=Language.PYTHON
    )
    level = models.CharField(
        max_length=255, choices=Level.choices, default=Level.BEGINNER
    )

    def __str__(self):
        return self.language

# Generated by Django 4.2.6 on 2023-10-24 06:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='collaborators',
            field=models.ManyToManyField(related_name='collaborator_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
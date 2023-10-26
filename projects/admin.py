from django.contrib import admin

from .models import Application, Project

admin.site.register(Project)
admin.site.register(Application)

from django.contrib import admin

from .models import Package, Project, Version

admin.site.register(Version)
admin.site.register(Project)
admin.site.register(Package)

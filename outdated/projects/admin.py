from django.contrib import admin

from .models import Project, Package


admin.site.register(Project)
admin.site.register(Package)

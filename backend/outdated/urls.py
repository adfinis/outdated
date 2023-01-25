from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from outdated.outdated import views

router = routers.DefaultRouter()
router.register(r"projects", views.ProjectViewSet)
router.register(r"dependencies", views.DependencyViewSet)
router.register(r"dependency-versions", views.DependencyVersionViewSet)

urlpatterns = [path("admin/", admin.site.urls), path("", include(router.urls))]

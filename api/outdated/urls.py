from django.urls import include, path
from rest_framework.routers import DefaultRouter

from outdated.outdated import views

router = DefaultRouter(trailing_slash=False)
router.register(r"projects", views.ProjectViewSet)
router.register(r"dependencies", views.DependencyViewSet)
router.register(r"dependency-versions", views.DependencyVersionViewSet)

urlpatterns = [path("", include(router.urls))]

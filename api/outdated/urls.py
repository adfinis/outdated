from django.urls import include, path
from rest_framework.routers import DefaultRouter

from outdated.outdated import views

router = DefaultRouter(trailing_slash=False)
router.register(r"projects", views.ProjectViewSet)
router.register(r"dependencies", views.DependencyViewSet)
router.register(r"release-versions", views.ReleaseVersionViewSet)
router.register(r"versions", views.VersionViewSet)

urlpatterns = [path("api/", include(router.urls))]

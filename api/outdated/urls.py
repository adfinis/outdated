from django.urls import include, path
from rest_framework.routers import DefaultRouter

from outdated.outdated import views
from outdated.user.views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"projects", views.ProjectViewSet)
router.register(r"dependencies", views.DependencyViewSet)
router.register(r"release-versions", views.ReleaseVersionViewSet)
router.register(r"versions", views.VersionViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [path("api/", include(router.urls))]

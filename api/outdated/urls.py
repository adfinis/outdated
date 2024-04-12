from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from watchman import views as watchman_views

from .outdated import views
from .user.views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"projects", views.ProjectViewSet)
router.register(r"maintainers", views.MaintainerViewset)
router.register(r"dependencies", views.DependencyViewSet)
router.register(r"release-versions", views.ReleaseVersionViewSet)
router.register(r"versions", views.VersionViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path(r"api/", include(router.urls)),
    re_path("api/health/?", watchman_views.bare_status, name="health"),
]

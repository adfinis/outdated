from rest_framework.routers import SimpleRouter

from outdated.outdated import views

router = SimpleRouter(trailing_slash=False)
router.register(r"projects", views.ProjectViewSet)
router.register(r"dependencies", views.DependencyViewSet)
router.register(r"dependency-versions", views.DependencyVersionViewSet)

urlpatterns = router.urls

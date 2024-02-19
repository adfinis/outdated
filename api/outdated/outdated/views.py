from django.db.models import Min
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import filters, models, serializers
from .tracking import Tracker


class ProjectViewSet(ModelViewSet):
    queryset = models.Project.objects.annotate(
        min_end_of_life=Min("versioned_dependencies__release_version__end_of_life")
    ).order_by("min_end_of_life")

    serializer_class = serializers.ProjectSerializer
    filterset_class = filters.ProjectFilterSet

    @action(detail=True, methods=["post"])
    def sync(self, *args, **kwargs):
        project = self.get_object()
        Tracker(project).sync()
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    def perform_destroy(self, instance: models.Project) -> None:
        Tracker(instance).delete()
        instance.delete()


class ReleaseVersionViewSet(ModelViewSet):
    queryset = models.ReleaseVersion.objects.all()
    serializer_class = serializers.ReleaseVersionSerializer


class VersionViewSet(ModelViewSet):
    queryset = models.Version.objects.all()
    serializer_class = serializers.VersionSerializer
    filterset_class = filters.VersionFilterSet


class DependencyViewSet(ModelViewSet):
    queryset = models.Dependency.objects.all()
    serializer_class = serializers.DependencySerializer


class MaintainerViewset(ModelViewSet):
    queryset = models.Maintainer.objects.all()
    serializer_class = serializers.MaintainerSerializer

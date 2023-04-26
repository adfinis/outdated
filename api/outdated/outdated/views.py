from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from outdated.outdated.dependencies import ProjectSyncer
from outdated.outdated.models import Dependency, ReleaseVersion, Version, Project
from outdated.outdated.serializers import (
    DependencySerializer,
    VersionSerializer,
    ReleaseVersionSerializer,
    ProjectSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True)
    def sync(self, request, pk=None):
        project = self.get_object()
        ProjectSyncer(project).sync()
        return Response(status=204)


class ReleaseVersionViewSet(viewsets.ModelViewSet):
    queryset = ReleaseVersion.objects.all()
    serializer_class = ReleaseVersionSerializer


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

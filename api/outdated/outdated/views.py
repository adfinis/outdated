from rest_framework import viewsets

from outdated.outdated.models import Dependency, Project, ReleaseVersion, Version
from outdated.outdated.serializers import (
    DependencySerializer,
    ProjectSerializer,
    ReleaseVersionSerializer,
    VersionSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ReleaseVersionViewSet(viewsets.ModelViewSet):
    queryset = ReleaseVersion.objects.all()
    serializer_class = ReleaseVersionSerializer


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

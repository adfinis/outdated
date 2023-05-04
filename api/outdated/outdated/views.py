from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from outdated.outdated.models import Dependency, Project, ReleaseVersion, Version
from outdated.outdated.serializers import (
    DependencySerializer,
    ProjectSerializer,
    ReleaseVersionSerializer,
    VersionSerializer,
)
from outdated.outdated.synchroniser import Synchroniser


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        Synchroniser(self.get_object()).sync()
        return Response(status=status.HTTP_200_OK)


class ReleaseVersionViewSet(viewsets.ModelViewSet):
    queryset = ReleaseVersion.objects.all()
    serializer_class = ReleaseVersionSerializer


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

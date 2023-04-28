from rest_framework import response, status, viewsets
from rest_framework.decorators import action

from outdated.outdated.models import Dependency, DependencyVersion, Project
from outdated.outdated.serializers import (
    DependencySerializer,
    DependencyVersionSerializer,
    ProjectSerializer,
)
from outdated.outdated.synchroniser import Synchroniser


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        project = self.get_object()
        Synchroniser(project).sync()
        return response.Response(status=status.HTTP_200_OK)


class DependencyVersionViewSet(viewsets.ModelViewSet):
    queryset = DependencyVersion.objects.all()
    serializer_class = DependencyVersionSerializer


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

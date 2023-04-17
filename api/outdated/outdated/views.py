from asyncio import run

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from outdated.outdated.dependencies import ProjectSyncer
from outdated.outdated.models import Dependency, DependencyVersion, Project
from outdated.outdated.serializers import (
    DependencySerializer,
    DependencyVersionSerializer,
    ProjectSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True)
    def sync(self, request, pk=None):
        try:
            project = self.get_object()
            run(ProjectSyncer(project).sync())
            return Response(status=204)
        except KeyError:
            return Response(
                status=429,
                data={"error": "Github API rate limit exceeded"},  # pragma: no cover
            )


class DependencyVersionViewSet(viewsets.ModelViewSet):
    queryset = DependencyVersion.objects.all()
    serializer_class = DependencyVersionSerializer


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

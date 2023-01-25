from outdated.outdated.models import Dependency, DependencyVersion, Project
from outdated.outdated.serializers import (
    DependencySerializer,
    DependencyVersionSerializer,
    ProjectSerializer,
)
from rest_framework import viewsets


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DependencyVersionViewSet(viewsets.ModelViewSet):
    queryset = DependencyVersion.objects.all()
    serializer_class = DependencyVersionSerializer


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

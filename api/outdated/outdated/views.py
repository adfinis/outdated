from rest_framework import views, viewsets

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


class DependencyVersionViewSet(viewsets.ModelViewSet):
    queryset = DependencyVersion.objects.all()
    serializer_class = DependencyVersionSerializer


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer


class SyncProjectView(views.APIView):
    """Syncproject endpoint."""

    def get(self, request, id):
        try:
            project = Project.objects.get(id=id)
            ProjectSyncer(project).sync()
            return views.Response(status=204)
        except Project.DoesNotExist:
            return views.Response(status=404, data={"error": "Project does not exist"})

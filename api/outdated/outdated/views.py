from django.db.models import Max
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from outdated.outdated import models, serializers

from .synchroniser import Synchroniser


class ProjectViewSet(ModelViewSet):
    queryset = (
        models.Project.objects.all()
        .annotate(
            latest_eol=Max("versioned_dependencies__release_version__end_of_life")
        )
        .order_by("latest_eol")
    )

    serializer_class = serializers.ProjectSerializer

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        try:
            project = self.get_object()
            Synchroniser(project).sync()
        except Exception as e:
            return Response(
                {"detail": f"Failed to sync project: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        serializer = self.get_serializer(project)
        return Response(serializer.data)


class ReleaseVersionViewSet(ModelViewSet):
    queryset = models.ReleaseVersion.objects.all()
    serializer_class = serializers.ReleaseVersionSerializer


class VersionViewSet(ModelViewSet):
    queryset = models.Version.objects.all()
    serializer_class = serializers.VersionSerializer


class DependencyViewSet(ModelViewSet):
    queryset = models.Dependency.objects.all()
    serializer_class = serializers.DependencySerializer


class MaintainerViewset(ModelViewSet):
    queryset = models.Maintainer.objects.all()
    serializer_class = serializers.MaintainerSerializer

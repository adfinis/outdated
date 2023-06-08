from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, serializers
from .synchroniser import Synchroniser


class ProjectViewSet(ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        try:
            Synchroniser(self.get_object()).sync()
        except Exception as e:
            return Response(
                {"detail": f"Failed to sync project: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(status=status.HTTP_200_OK)


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

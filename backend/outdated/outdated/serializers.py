from outdated.outdated.models import Dependency, DependencyVersion, Project
from rest_framework_json_api import serializers


class DependencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dependency
        fields = "__all__"


class DependencyVersionSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = DependencyVersion
        fields = "__all__"


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = "__all__"

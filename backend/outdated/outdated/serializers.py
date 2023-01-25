from rest_framework_json_api import serializers

from outdated.outdated.models import Dependency, DependencyVersion, Project


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = "__all__"


class DependencyVersionSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = DependencyVersion
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = "__all__"

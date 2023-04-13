from rest_framework_json_api import serializers

from outdated.outdated.models import Dependency, DependencyVersion, Project


class DependencySerializer(serializers.ModelSerializer):
    latest = serializers.ReadOnlyField()
    last_checked = serializers.ReadOnlyField()

    class Meta:
        model = Dependency
        fields = "__all__"


class DependencyVersionSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    included_serializers = {
        "dependency": "outdated.outdated.serializers.DependencySerializer"
    }

    class Meta:
        model = DependencyVersion
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    included_serializers = {
        "dependency_versions": "outdated.outdated.serializers.DependencyVersionSerializer",
    }

    class Meta:
        model = Project
        fields = "__all__"

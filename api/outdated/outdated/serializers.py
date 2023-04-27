from rest_framework_json_api import serializers

from outdated.outdated.models import Dependency, Project, ReleaseVersion, Version


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = "__all__"


class ReleaseVersionSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    included_serializers = {
        "dependency": "outdated.outdated.serializers.DependencySerializer"
    }

    class Meta:
        model = ReleaseVersion
        exclude = ("_latest_patch_version", "last_checked")


class VersionSerializer(serializers.ModelSerializer):
    included_serializers = {
        "release_version": "outdated.outdated.serializers.ReleaseVersionSerializer"
    }

    class Meta:
        model = Version
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    included_serializers = {
        "versioned_dependencies": "outdated.outdated.serializers.VersionSerializer",
    }

    class Meta:
        model = Project
        fields = "__all__"

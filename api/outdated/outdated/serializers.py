from rest_framework_json_api import serializers

from outdated.outdated.models import (
    Dependency,
    Maintainer,
    Project,
    ReleaseVersion,
    Version,
)


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
        fields = "__all__"


class VersionSerializer(serializers.ModelSerializer):
    included_serializers = {
        "release_version": "outdated.outdated.serializers.ReleaseVersionSerializer"
    }

    class Meta:
        model = Version
        fields = "__all__"


class MaintainerSerializer(serializers.ModelSerializer):
    included_serializers = {
        "user": "outdated.user.serializers.UserSerializer",
        "project": "outdated.outdated.serializers.ProjectSerializer",
    }

    class Meta:
        model = Maintainer
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    maintainers = serializers.ResourceRelatedField(
        many=True, required=False, read_only=True
    )

    included_serializers = {
        "versioned_dependencies": "outdated.outdated.serializers.VersionSerializer",
        "maintainers": "outdated.outdated.serializers.MaintainerSerializer",
    }

    class Meta:
        model = Project
        fields = ("name", "repo", "status", "versioned_dependencies", "maintainers")

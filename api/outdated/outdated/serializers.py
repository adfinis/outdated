from rest_framework_json_api import serializers

from outdated.outdated import models
from outdated.tracking import Tracker


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dependency
        fields = "__all__"


class ReleaseVersionSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    included_serializers = {
        "dependency": "outdated.outdated.serializers.DependencySerializer",
    }

    class Meta:
        model = models.ReleaseVersion
        fields = "__all__"


class VersionSerializer(serializers.ModelSerializer):
    included_serializers = {
        "release_version": "outdated.outdated.serializers.ReleaseVersionSerializer",
    }

    class Meta:
        model = models.Version
        fields = "__all__"


class MaintainerSerializer(serializers.ModelSerializer):
    included_serializers = {
        "user": "outdated.user.serializers.UserSerializer",
        "project": "outdated.outdated.serializers.ProjectSerializer",
    }

    class Meta:
        model = models.Maintainer
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    maintainers = serializers.ResourceRelatedField(
        many=True,
        read_only=True,
        required=False,
    )

    included_serializers = {
        "versioned_dependencies": "outdated.outdated.serializers.VersionSerializer",
        "maintainers": "outdated.outdated.serializers.MaintainerSerializer",
    }

    def create(self, validated_data):
        project = models.Project.objects.create(**validated_data)
        Tracker(project).setup()
        project.refresh_from_db()
        return project

    def update(self, instance: models.Project, validated_data: dict) -> models.Project:
        old_instance = models.Project(repo=instance.repo)
        super().update(instance, validated_data)
        if instance.clone_path != old_instance.clone_path:
            Tracker(old_instance).delete()
            Tracker(instance).setup()
            instance.refresh_from_db()
        return instance

    class Meta:
        model = models.Project
        fields = (
            "name",
            "repo",
            "status",
            "versioned_dependencies",
            "maintainers",
        )

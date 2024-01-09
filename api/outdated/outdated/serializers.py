from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from rest_framework_json_api import serializers

from outdated.outdated import models
from outdated.outdated.validators import (
    validate_access_token_required,
    validate_no_access_token_when_public,
    validate_remote_url,
)

from .tracking import Tracker


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

    access_token = serializers.CharField(
        max_length=100,
        write_only=True,
        required=False,
        allow_blank=True,
        validators=[RegexValidator(r"[-_a-zA-Z\d]+")],
    )
    repo = serializers.CharField(
        validators=[
            UniqueValidator(queryset=models.Project.objects.all(), lookup="iexact")
        ]
    )
    name = serializers.CharField(
        validators=[
            UniqueValidator(queryset=models.Project.objects.all(), lookup="iexact")
        ]
    )

    included_serializers = {
        "versioned_dependencies": "outdated.outdated.serializers.VersionSerializer",
        "maintainers": "outdated.outdated.serializers.MaintainerSerializer",
    }

    class Meta:
        model = models.Project
        validators = [
            validate_remote_url,
            validate_access_token_required,
            validate_no_access_token_when_public,
        ]
        fields = (
            "name",
            "repo",
            "repo_type",
            "access_token",
            "status",
            "versioned_dependencies",
            "maintainers",
        )

    def create(self, validated_data: dict) -> models.Project:
        access_token = validated_data.pop("access_token", None)
        instance = super().create(validated_data)
        Tracker(instance, access_token).setup()
        return instance

    def update(self, instance: models.Project, validated_data: dict) -> models.Project:
        old_instance = models.Project(repo=instance.repo, repo_type=instance.repo_type)
        access_token = validated_data.pop("access_token", None)
        super().update(instance, validated_data)
        if (
            instance.clone_path != old_instance.clone_path
            or instance.repo_type != old_instance.repo_type
        ):
            Tracker(old_instance).delete()
            Tracker(instance, access_token).setup()
        return instance

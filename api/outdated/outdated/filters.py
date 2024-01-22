from django_filters import FilterSet, UUIDFilter

from outdated.outdated import models


class VersionFilterSet(FilterSet):
    dependency = UUIDFilter(
        field_name="release_version__dependency",
    )

    class Meta:
        model = models.Version
        fields = ["dependency"]


class ProjectFilterSet(FilterSet):
    dependency = UUIDFilter(
        field_name="versioned_dependencies__release_version__dependency",
    )

    version = UUIDFilter(
        field_name="versioned_dependencies",
    )

    class Meta:
        model = models.Project
        fields = ["dependency"]

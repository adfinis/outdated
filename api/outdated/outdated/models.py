from datetime import date, timedelta
from typing import Optional

from django.db import models
from django.db.models.functions import Lower

from outdated.models import RepositoryURLField, UniqueBooleanField, UUIDModel

from ..user.models import User

STATUS_OPTIONS = {
    "outdated": "OUTDATED",
    "warning": "WARNING",
    "up_to_date": "UP-TO-DATE",
    "undefined": "UNDEFINED",
}

STATUS_CHOICES = [(_, _) for _ in STATUS_OPTIONS.values()]

PROVIDER_OPTIONS = {
    "PIP": "https://pypi.org/pypi/%s/json",
    "NPM": "https://registry.npmjs.org/%s",
}

PROVIDER_CHOICES = [(provider, provider) for provider in PROVIDER_OPTIONS.keys()]


class Dependency(UUIDModel):
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)

    class Meta:
        ordering = ["name", "id"]
        unique_together = ("name", "provider")

    def __str__(self):
        return self.name


class ReleaseVersion(UUIDModel):
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE)
    major_version = models.IntegerField()
    minor_version = models.IntegerField()
    end_of_life = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.dependency.name} {self.version}"

    @property
    def version(self):
        return f"{self.major_version}.{self.minor_version}"  # pragma: no cover

    class Meta:
        ordering = [
            "end_of_life",
            "dependency__name",
            "major_version",
            "minor_version",
        ]
        unique_together = ("dependency", "major_version", "minor_version")

    @property
    def status(self):
        if not self.end_of_life:
            return STATUS_OPTIONS["undefined"]
        elif date.today() >= self.end_of_life:
            return STATUS_OPTIONS["outdated"]
        elif date.today() + timedelta(days=150) >= self.end_of_life:
            return STATUS_OPTIONS["warning"]
        return STATUS_OPTIONS["up_to_date"]


class Version(UUIDModel):
    release_version = models.ForeignKey(
        ReleaseVersion, on_delete=models.CASCADE, related_name="versions"
    )
    patch_version = models.IntegerField()
    release_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = [
            "release_version__end_of_life",
            "release_version__dependency__name",
            "release_version__major_version",
            "release_version__minor_version",
            "patch_version",
        ]
        unique_together = ("release_version", "patch_version")

    def __str__(self):
        return f"{self.release_version}.{self.patch_version}"

    @property
    def version(self):
        return f"{self.release_version.version}.{self.patch_version}"

    @property
    def end_of_life(self):
        return self.release_version.end_of_life


class Project(UUIDModel):
    name = models.CharField(max_length=100, db_index=True)
    repo = RepositoryURLField(max_length=100, unique=True)
    versioned_dependencies = models.ManyToManyField(
        Version, blank=True, related_name="projects"
    )
    notification_queue = models.ManyToManyField(
        "notifications.Notification", blank=True
    )

    class Meta:
        ordering = ["name", "id"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_project_name",
            ),
            models.UniqueConstraint(
                Lower("repo"),
                name="unique_project_repo",
            ),
        ]

    @property
    def status(self) -> str:
        first = self.versioned_dependencies.first()
        return first.release_version.status if first else STATUS_OPTIONS["undefined"]

    @property
    def duration_until_outdated(self) -> Optional[timedelta]:
        if not self.status or self.status == STATUS_OPTIONS["undefined"]:
            return
        return self.versioned_dependencies.first().end_of_life - date.today()

    def __str__(self):
        return self.name


class Maintainer(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="maintainers"
    )
    is_primary = UniqueBooleanField(default=False, together=["project"])

    def __str__(self):
        return self.user.email

    class Meta:
        unique_together = ("user", "project")
        ordering = ("-is_primary",)

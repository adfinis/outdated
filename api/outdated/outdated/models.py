from datetime import timedelta

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

from outdated.models import RepositoryURLField, UniqueBooleanField, UUIDModel
from outdated.user.models import User

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

PROVIDER_CHOICES = [(provider, provider) for provider in PROVIDER_OPTIONS]


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
        if timezone.datetime.now().date() >= self.end_of_life:
            return STATUS_OPTIONS["outdated"]
        if timezone.datetime.now().date() + timedelta(days=150) >= self.end_of_life:
            return STATUS_OPTIONS["warning"]
        return STATUS_OPTIONS["up_to_date"]


class Version(UUIDModel):
    release_version = models.ForeignKey(ReleaseVersion, on_delete=models.CASCADE)
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


class Project(UUIDModel):
    name = models.CharField(max_length=100, db_index=True)
    versioned_dependencies = models.ManyToManyField(Version, blank=True)
    repo = RepositoryURLField(max_length=100)

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
    def repo_domain(self):
        return self.repo.split("/")[0].lower()

    @property
    def repo_namespace(self):
        return self.repo.split("/")[-1].lower()

    @property
    def repo_name(self):
        return self.repo.split("/")[1].lower()

    @property
    def clone_path(self):
        return f"{self.repo_domain}/{self.repo_namespace}/{self.repo_name}"

    def __str__(self):
        return self.name


class Maintainer(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="maintainers",
    )
    is_primary = UniqueBooleanField(default=False, together=["project"])

    class Meta:
        unique_together = ("user", "project")

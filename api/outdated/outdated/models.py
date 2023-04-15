from datetime import date, timedelta

from django.db import models
from django.db.models.functions import Lower
import time
from django.utils import timezone
from requests import get
from semver import compare

from outdated.models import UUIDModel


STATUS_OPTIONS = {
    "outdated": "OUTDATED",
    "warning": "WARNING",
    "up_to_date": "UP-TO-DATE",
    "undefined": "UNDEFINED",
}
STATUS_CHOICES = [(i, status) for i, status in enumerate(STATUS_OPTIONS.keys())]

PROVIDER_OPTIONS = {
    "PIP": {"url": "https://pypi.org/pypi/%s/json", "latest": ("info", "version")},
    "NPM": {"url": "https://registry.npmjs.org/%s", "latest": ("dist-tags", "latest")},
}
PROVIDER_CHOICES = [(provider, provider) for provider in PROVIDER_OPTIONS.keys()]


class Dependency(UUIDModel):
    name = models.CharField(max_length=100)
    last_checked = models.DateTimeField(editable=False, null=True, blank=True)
    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)
    latest = models.CharField(max_length=100, editable=False, null=True, blank=True)

    class Meta:
        ordering = ["name", "id"]
        unique_together = ("name", "provider")
        indexes = [
            models.Index(fields=["name", "provider"], name="name_provider_idx"),
        ]

    def latest(self) -> str:
        if (
            not self.last_checked
            or self.last_checked - timedelta(days=1) > timezone.now()
        ):
            url = PROVIDER_OPTIONS[self.provider]["url"] % self.name
            latest = PROVIDER_OPTIONS[self.provider]["latest"]
            self.last_checked = timezone.now()
            self.save()
            return get(url).json()[latest[0]][latest[1]]
        else:
            print(self.last_checked)
        return self.latest

    def __str__(self):
        return self.name


class DependencyVersion(UUIDModel):
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, editable=False)
    release_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = [
            "release_date",
            "dependency__name",
            "version",
        ]
        unique_together = ("dependency", "version")
        indexes = [
            models.Index(
                fields=["dependency", "version"], name="dependency_version_idx"
            ),
        ]

    @property
    def status(self):
        if self.dependency.latest == "0.0.0":
            return STATUS_OPTIONS["undefined"]
        elif compare(self.version, self.dependency.latest) != 0:
            return STATUS_OPTIONS["outdated"]
        elif date.today() + timedelta(days=365) <= self.release_date:
            return STATUS_OPTIONS["warning"]
        return STATUS_OPTIONS["up_to_date"]

    def __str__(self):
        return self.dependency.name + self.version


class Project(UUIDModel):
    name = models.CharField(max_length=100, db_index=True)
    repo = models.URLField(max_length=100, unique=True)
    dependency_versions = models.ManyToManyField(DependencyVersion, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, editable=False)

    class Meta:
        ordering = ["name", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=models.Q(name__iexact=Lower("name")),
                name="unique_project_name",
            )
        ]

    @property
    def status(self) -> str:
        first = self.dependency_versions.first()
        return first.status if first else STATUS_OPTIONS["undefined"]

    def __str__(self):
        return self.name

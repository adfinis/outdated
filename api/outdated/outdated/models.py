from datetime import date, timedelta

from django.db import models
from django.db.models.functions import Lower
from django.http import Http404
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
    name = models.CharField(max_length=200)
    latest = models.CharField(max_length=100, editable=False, default="0.0.0")
    last_checked = models.DateTimeField(editable=False, default=timezone.now())
    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)

    class Meta:
        ordering = ["name", "id"]
        unique_together = ("name", "provider")

    @property
    def latest(self):
        if self.last_checked + timedelta(days=1) > timezone.now():
            url = PROVIDER_OPTIONS[self.provider]["url"] % self.name
            response = get(url).json()
            if response.get("message") == "Not Found":
                raise Http404
            latest = PROVIDER_OPTIONS[self.provider]["latest"]
            self.last_checked = timezone.now()
            return response[latest[0]][latest[1]]

        return self.latest

    def __str__(self):
        return self.name


class DependencyVersion(UUIDModel):
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    release_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, editable=False)

    class Meta:
        ordering = [
            "dependency__name",
            "version",
            "release_date",
        ]
        unique_together = ("dependency", "version")

    @property
    def status(self):
        if compare(self.version, self.dependency.latest) != 0:
            return STATUS_OPTIONS["outdated"]
        elif date.today() + timedelta(years=1) >= self.release_date:
            return STATUS_OPTIONS["warning"]
        return STATUS_OPTIONS["up_to_date"]

    def __str__(self):
        return self.dependency.name + self.version


class Project(UUIDModel):
    name = models.CharField(
        max_length=100,
    )
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

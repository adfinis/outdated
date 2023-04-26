from datetime import date, timedelta

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone
from requests import get
from semver import Version as SemVer

from outdated.models import UUIDModel

STATUS_OPTIONS = {
    "outdated": "OUTDATED",
    "warning": "WARNING",
    "up_to_date": "UP-TO-DATE",
    "undefined": "UNDEFINED",
}

STATUS_CHOICES = [(_, _) for _ in STATUS_OPTIONS.keys()]

PROVIDER_OPTIONS = {
    "PIP": {"url": "https://pypi.org/pypi/%s/json", "latest": ("info", "version")},
    "NPM": {"url": "https://registry.npmjs.org/%s", "latest": ("dist-tags", "latest")},
}

PROVIDER_CHOICES = [(provider, provider) for provider in PROVIDER_OPTIONS.keys()]


def get_yesterday():
    return timezone.now() - timedelta(days=1)


def get_version(version: str):
    if not SemVer.is_valid(version):
        # turn invalid semver valid e.g. 4.2 into 4.2.0
        version_list = version.split(".")
        version = ".".join(version_list[:3] + ["0"] * (3 - len(version_list)))
    return version


def get_latest_version(dependency):
    url = PROVIDER_OPTIONS[dependency.provider]["url"] % dependency.name
    latest = PROVIDER_OPTIONS[dependency.provider]["latest"]
    version = get(url).json()[latest[0]][latest[1]]
    return get_version(version)


def get_latest_patch_version(lts_version):
    url = (
        PROVIDER_OPTIONS[lts_version.dependency.provider]["url"]
        % lts_version.dependency.name
    )
    return sorted(
        [
            version
            for version in get(url).json().get("releases").keys()
            or get(url).json().get("versions").keys()
            if version.startswith(f"{lts_version.major}.{lts_version.minor}")
        ],
    )[-1]


class Dependency(UUIDModel):
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)

    class Meta:
        ordering = ["name", "id"]
        unique_together = ("name", "provider")
        indexes = [
            models.Index(fields=["name", "provider"], name="name_provider_idx"),
        ]

    def __str__(self):
        return self.name


class ReleaseVersion(UUIDModel):
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE)
    major_version = models.IntegerField()
    minor_version = models.IntegerField()
    _latest_patch_version = models.CharField(max_length=100, editable=False)
    last_checked = models.DateTimeField(
        editable=False,
        null=True,
        blank=True,
        default=get_yesterday,
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, editable=False)
    end_of_life = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.dependency.name} {self.version}"

    @property
    def version(self):
        return f"{self.major_version}.{self.minor_version}"

    @property
    def newest_patch_version(self):
        if self.last_checked < timezone.now() - timedelta(days=1):
            self.last_checked = timezone.now()
            self._latest_patch_version = get_latest_patch_version(self)
            self.save()
        return self._latest_patch_version

    class Meta:
        ordering = [
            "end_of_life",
            "dependency__name",
            "major_version",
            "minor_version",
        ]
        unique_together = ("dependency", "major_version", "minor_version")

        indexes = [
            models.Index(
                fields=["dependency", "major_version", "minor_version"],
                name="dependency_version_idx",
            ),
        ]

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

    def __str__(self):
        return f"{self.release_version.dependency.name} {self.full_version}"

    @property
    def full_version(self):
        return f"{self.release_version.version}.{self.patch_version}"

    @classmethod
    async def aget_or_create_full_dependency(cls, **kwargs):
        major, minor, patch = SemVer.parse(kwargs.get("version")).to_tuple()[0:3]
        dependency = kwargs.get("dependency")
        release_version = (
            await ReleaseVersion.objects.aget_or_create(
                dependency=dependency,
                major_version=major,
                minor_version=minor,
            )
        )[0]
        return await cls.objects.aget_or_create(
            release_version=release_version,
            patch_version=patch,
        )


class Project(UUIDModel):
    name = models.CharField(max_length=100, db_index=True)
    repo = models.URLField(max_length=100, unique=True)
    versioned_dependencies = models.ManyToManyField(Version, blank=True)
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
        for status in STATUS_OPTIONS.values():
            if any(
                dependency_version.status == status
                for dependency_version in self.dependency_versions.all()
            ):
                return status
        return STATUS_OPTIONS["undefined"]

    def __str__(self):
        return self.name

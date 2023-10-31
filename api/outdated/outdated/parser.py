from __future__ import annotations

from re import findall
from typing import TYPE_CHECKING

import requests
from dateutil import parser
from django.conf import settings
from semver import Version as SemVer
from tomllib import loads
from yaml import safe_load

from . import models

if TYPE_CHECKING:
    from pathlib import Path


class LockfileParser:
    """Parse a lockfile and return a list of dependencies."""

    def __init__(self, lockfiles: list[Path]) -> None:
        self.lockfiles = lockfiles

    def _get_provider(self, name: str) -> str:
        """Get the provider of the lockfile."""
        if name in settings.NPM_FILES:
            return "NPM"
        return "PIP"

    def _get_version(
        self,
        requirements: tuple[str, str],
        provider: str,
    ) -> models.Version:
        dependency, dependency_created = models.Dependency.objects.get_or_create(
            name=requirements[0],
            provider=provider,
        )

        semver = SemVer.parse(requirements[1], True)

        (
            release_version,
            release_version_created,
        ) = models.ReleaseVersion.objects.get_or_create(
            dependency=dependency,
            major_version=semver.major,
            minor_version=semver.minor,
        )

        version, version_created = models.Version.objects.get_or_create(
            release_version=release_version,
            patch_version=semver.patch,
        )

        if (
            dependency_created
            or release_version_created
            or version_created
            or not version.release_date
        ):
            version.release_date = self._get_release_date(version)
            version.save()

        return version

    def _get_release_date(self, version):
        """Get the release date of a dependency."""
        dependency = version.release_version.dependency
        name, provider = dependency.name, dependency.provider

        if provider == "NPM":
            response = requests.get(f"https://registry.npmjs.org/{name}", timeout=10)
            response.raise_for_status()
            json = response.json()
            release_date = json["time"][version.version]

        elif provider == "PIP":
            response = requests.get(
                f"https://pypi.org/pypi/{name}/{version.version}/json",
                timeout=10,
            )
            response.raise_for_status()
            release_date = (response.json())["urls"][0]["upload_time"]

        else:  # pragma: no cover
            raise NotImplementedError(
                f"Getting the release date is not implemented for {provider=}",
            )

        return parser.parse(release_date).date()

    def parse(self):
        """Parse the lockfile and return a dictionary of dependencies."""
        versions = []

        for lockfile in self.lockfiles:
            name = lockfile.name
            data = lockfile.read_text()
            provider = self._get_provider(name)

            dependencies = []
            if name == "yarn.lock":
                regex = r'"?([\S]+)@.*:\n  version "(.+)"'
                dependencies = [
                    dependency
                    for dependency in findall(regex, data)
                    if dependency[0] in settings.TRACKED_DEPENDENCIES
                ]
            elif name == "poetry.lock":
                dependencies = [
                    (dependency["name"], dependency["version"])
                    for dependency in loads(data)["package"]
                    if dependency["name"] in settings.TRACKED_DEPENDENCIES
                ]
            elif name == "pnpm-lock.yaml":
                lockfile_data = safe_load(data)
                regex = r"\/(@?[^\s@]+)@([^()]+).*"
                if float(lockfile_data["lockfileVersion"]) < 6.0:
                    raise NotImplementedError(
                        "Outdated does not support pnpm-lock.yaml lockfiles with a version lower than 6",
                    )
                dependencies = [
                    findall(regex, dependency)[0]
                    for dependency in lockfile_data["packages"]
                    if (requirements := findall(regex, dependency))
                    and requirements[0][0] in settings.TRACKED_DEPENDENCIES
                ]

            versions.extend(
                self._get_version(dependency, provider) for dependency in dependencies
            )

        return versions
